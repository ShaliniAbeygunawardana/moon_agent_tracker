import boto3
from botocore.exceptions import ClientError
from typing import Optional, Dict, Any

class S3ServiceException(Exception):
    def __init__(self, message):
        super().__init__(message)

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client('s3')
        
    def list_files(self, bucket_name: str, file_path: str, strip_prefix: bool = False) -> list:
        """
        List files in an S3 bucket directory.
        
        Args:
            bucket_name: Name of the S3 bucket
            file_path: Prefix/directory path to list objects from
            strip_prefix: If True, strips the prefix from returned keys
            
        Returns:
            List of file keys in the directory, excluding the directory itself
        """
        output = []
        try:
            # Ensure file_path ends with a slash if it's meant to be a directory
            if file_path and not file_path.endswith('/'):
                file_path += '/'
                
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=file_path)
            if 'Contents' in response:
                for obj in response['Contents']:
                    key = obj['Key']
                    # Skip the directory object itself
                    if key == file_path:
                        continue
                        
                    # Strip prefix if requested
                    if strip_prefix:
                        key = key.replace(file_path, '', 1)
                        
                    output.append(key)
        
        except ClientError as e:
            raise S3ServiceException(f"Error listing files in bucket {bucket_name}: {e}")
        except Exception as e:
            raise S3ServiceException(f"Unexpected error: {e}") 
            
        return output
            
    def read_file(self, bucket_name: str, file_key:str) -> Optional[Dict[str, Any]]:
        """Download a file from S3."""
        output = {}
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
            output = response['Body'].read()
        
        except ClientError as e:
            raise S3ServiceException(f"Error downloading file {file_key}: {e}")
        except Exception as e:
            raise S3ServiceException(f"Unexpected error: {e}")
        
        return output
    
    def download_file(self, bucket_name: str, file_key:str, local_path:str) -> bool:
        """Download a file from S3 to a local path."""
        output = False
        try:
            self.s3_client.download_file(bucket_name, file_key, local_path)
            output = True
        except ClientError as e:
            raise S3ServiceException(f"Error downloading file {file_key}: {e}")
        except Exception as e:
            raise S3ServiceException(f"Unexpected error: {e}")
        
        return output