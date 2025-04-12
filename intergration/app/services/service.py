import sys
sys.path.append('/home/kosala/git-repos/moon_agent_tracker_test/')
from intergration.app.s3_repository.s3_service import S3Service, S3ServiceException
from intergration.app.db_repository.sql_repository import SQLRepository, DatabaseOperationException
from intergration.app.db_repository.sql_repository import DataNotFoundException
import logging
import hashlib
from intergration.configs import DOWNLOAD_DIR, DB_STRING
import os
import pandas as pd

logger = logging.getLogger(__name__)

class IntergrationService:
    def __init__(self, db_adapter: SQLRepository=None, s3_adapter: S3Service=None):
        self.db_adapter = db_adapter
        self.s3_adapter = s3_adapter
        
    def fetch_data(self, request_params: dict):
        """fetch data from a s3 bucket as files ** process a file at a time **
        1. fetch files from s3 bucket
        2. compare file hash with db to check if file has already been processed
        3. if file has not been processed, process the file
        4. if file has been processed, skip the file and move to the next file
        5. if file has been processed, save the processsed file hash to db \
            and archive and save the file to s3 bucket. delete the processed \
            file from the bucket(source)

        Args:
            request_params (dict): can be any for now
        """ 
        output = False
        try:
            file_path_list = self.s3_adapter.list_files(
                request_params['bucket_name'], 
                request_params['file_path']
            )
            if len(file_path_list) <= 0:
                raise S3ServiceException("No files found in bucket")
            
            for file_path in file_path_list:
                file_name = file_path.split("/")[-1]
                file_hash = self.__generate_file_hash(file_name)
                file_hash_exists = self.db_adapter.check_file_hash_exists(file_hash)
                
                if file_hash_exists:
                    logger.info(f"File {file_name} has already been processed. Skipping...")
                    continue
                else:
                    output_file_path = os.path.join(DOWNLOAD_DIR, file_name) 
                    self.s3_adapter.download_file(
                        request_params['bucket_name'], 
                        file_path, 
                        output_file_path
                    )
                    self.__process_file(output_file_path)
                    self.db_adapter.save_file_hash(file_hash)
                    
                    #TODO: archive the file and delete the file from the bucket
                    
                    # self.s3_adapter.archive_file(file)  
                    # self.s3_adapter.delete_file(file)
            output = True
        except DatabaseOperationException as e:
            raise e
        except FileNotFoundError as e:
            raise e       
        except S3ServiceException as e:
            raise e
        except Exception as e:
            raise e
        return output
    
    def __generate_file_hash(self, file):
        """generate a hash for a file"""
        hasher = hashlib.sha256()
        hasher.update(file.encode('utf-8'))
       
        return hasher.hexdigest()
    
    def __process_file(self, file):
        """process a file"""
        # process the file
        # get the db engine
        db_engine = self.db_adapter.get_db_engine()
        dataframe = pd.read_csv(file)
        
        dataframe.to_sql(
            'sales_transaction', con=db_engine,
            if_exists='append', index=False
        )
    
    
if __name__ == "__main__":
    s3_adapter = S3Service()
    db_adapter = SQLRepository(DB_STRING)
    
    intergration_service = IntergrationService(s3_adapter=s3_adapter,
                                               db_adapter=db_adapter)
    request_params = {
        "bucket_name": "iit-cc-shal-2024",
        "file_path": "sales/",
        "archive_path": "archive/",
    }
    intergration_service.fetch_data(request_params)
        