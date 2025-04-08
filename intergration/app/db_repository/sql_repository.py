from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from intergration.app.models.dtos import Agent, AgentUpdate, Product, ProductUpdate
from intergration.app.models.db_models import Agent as DBAgent, FileHash as DBFileHash
from intergration.app.models.db_models import Product as DBProduct
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


Base = declarative_base()

class DatabaseOperationException(Exception):
    """Custom exception for database operation errors."""
    def __init__(self, message):
        super().__init__(message)
        
class DataNotFoundException(Exception):
    """Custom exception for data not found errors."""
    def __init__(self, message):
        super().__init__(message)

class SQLRepository:
    def __init__(self, database_url):
        """
        Initialize the SQLRepository with a database URL.
        This will create the database engine and session factory.
        """
        self.engine = create_engine(database_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        return self.Session()
    
    def get_db_engine(self):
        """Get the database engine.
        
        Returns:
            engine: The SQLAlchemy engine instance.
        """
        return self.engine
    
    def save_agen_info(self, agent_info: Agent):
        """Save agent info to the database when agent 
        - data is passed as Agent DTO.
        
        Args:
            agent_info (Agent): Agent information provided 
            from the service layer (business logic).
        
        Raises:
            DatabaseOperationException: If there is an error during 
            the database operation.
        """
        output = False
        session = self.get_session()
        try:
            db_agent_instance = DBAgent(
                agent_id=agent_info.agent_id,
                agent_code=agent_info.agent_code,
                first_name=agent_info.first_name,
                last_name=agent_info.last_name,
                email=agent_info.email,
                phone=agent_info.phone,
                branch_id=agent_info.branch_id
            )
            session.add(db_agent_instance)
            session.commit()
            output = True
        except IntegrityError as e:
            session.rollback()
            raise DatabaseOperationException(f"Integrity error while saving agent info: {e}")
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseOperationException(f"Database error while saving agent info: {e}")
        except Exception as e:
            session.rollback()
            raise DatabaseOperationException(f"Unexpected error while saving agent info: {e}")
        finally:
            session.close()
        return output
    
    def check_file_hash_exists(self, file_hash: str):
        """Check if a file hash exists in the database.
        
        Args:
            file_hash (str): The file hash to check.
        
        Returns:
            bool: True if the file hash exists, False otherwise.
        """
        output = False
        session = self.get_session()
        try:
            result = session.query(DBFileHash).filter_by(file_hash=file_hash).first()
            output = result is not None
        except SQLAlchemyError as e:
            raise DatabaseOperationException(f"Database error while checking file hash: {e}")
        finally:
            session.close()
            
        return output
    
    def save_file_hash(self, file_hash: str):
        """Save a file hash to the database.
        
        Args:
            file_hash (str): The file hash to save.
        
        Raises:
            DatabaseOperationException: If there is an error during 
            the database operation.
        """
        output = False  
        session = self.get_session()
        try:
            db_file_hash_instance = DBFileHash(file_hash=file_hash)
            session.add(db_file_hash_instance)
            session.commit()
            output = True
        except IntegrityError as e:
            session.rollback()
            raise DatabaseOperationException(f"Integrity error while saving file hash: {e}")
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseOperationException(f"Database error while saving file hash: {e}")
        except Exception as e:
            session.rollback()
            raise DatabaseOperationException(f"Unexpected error while saving file hash: {e}")
        finally:
            session.close()
        return output
        
        
        

