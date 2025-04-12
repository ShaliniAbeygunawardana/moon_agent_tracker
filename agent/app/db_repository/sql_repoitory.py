from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from agent.app.models.dtos import Agent, AgentUpdate, Product, ProductUpdate
from agent.app.models.db_models import Agent as DBAgent
from agent.app.models.db_models import Product as DBProduct
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
    
    def update_agent_info(self, agent_id: str, agent: AgentUpdate):
        """Update agent info in the database when agent 
        - data is passed as Agent DTO.
        
        Args:
            agent (Agent): Agent information provided 
            from the service layer (business logic).
        
        Raises:
            DatabaseOperationException: If there is an error during 
            the database operation.
        """
        output = False
        session = self.get_session()
        try:
            db_agent_instance = session.query(DBAgent).filter(DBAgent.agent_id == agent_id).first()
            if db_agent_instance:
                db_agent_instance.agent_code = agent.agent_code
                db_agent_instance.first_name = agent.first_name
                db_agent_instance.last_name = agent.last_name
                db_agent_instance.email = agent.email
                db_agent_instance.phone = agent.phone
                db_agent_instance.branch_id = agent.branch_id
                session.commit()
                output = True
            else:
                raise DataNotFoundException("Agent not found")
        except DataNotFoundException as e:
            session.rollback()
            raise e
        except IntegrityError as e:
            session.rollback()
            raise DatabaseOperationException(f"Integrity error while updating agent info: {e}")
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseOperationException(f"Database error while updating agent info: {e}")
        except Exception as e:
            session.rollback()
            raise DatabaseOperationException(f"Unexpected error while updating agent info: {e}")
        finally:
            session.close()
        return output
    
    def delete_agent(self, agent_id: str):
        """Delete agent info from the database when agent 
        - data is passed as Agent DTO.
        
        Args:
            agent (Agent): Agent information provided 
            from the service layer (business logic).
        
        Raises:
            DatabaseOperationException: If there is an error during 
            the database operation.
        """
        output = False
        session = self.get_session()
        try:
            db_agent_instance = session.query(DBAgent).filter(DBAgent.agent_id == agent_id).first()
            if db_agent_instance:
                session.delete(db_agent_instance)
                session.commit()
                output = True
            else:
                raise DataNotFoundException("Agent not found")
        except DataNotFoundException as e:
            session.rollback()
            raise e
        except IntegrityError as e:
            session.rollback()
            raise DatabaseOperationException(f"Integrity error while deleting agent info: {e}")
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseOperationException(f"Database error while deleting agent info: {e}")
        except Exception as e:
            session.rollback()
            raise DatabaseOperationException(f"Unexpected error while deleting agent info: {e}")
        finally:
            session.close()
        return output
    
    def save_product_info(self, product_info: Product):
        """Save product info to the database when product 
        - data is passed as Product DTO.
        
        Args:
            product_info (Product): Product information provided 
            from the service layer (business logic).
        
        Raises:
            DatabaseOperationException: If there is an error during 
            the database operation.
        """
        output = False
        session = self.get_session()
        try:
            db_product_instance = DBProduct(
                product_id=product_info.product_id,
                name=product_info.name,
                description=product_info.description
            )
            session.add(db_product_instance)
            session.commit()
            output = True
        except IntegrityError as e:
            session.rollback()
            raise DatabaseOperationException(f"Integrity error while saving product info: {e}")
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseOperationException(f"Database error while saving product info: {e}")
        except Exception as e:
            session.rollback()
            raise DatabaseOperationException(f"Unexpected error while saving product info: {e}")
        finally:
            session.close()
        return output

    def update_product_info(self, product_id: str, product: ProductUpdate):
        """Update product info in the database when product 
        - data is passed as Product DTO.
        
        Args:
            product (ProductUpdate): Product information provided 
            from the service layer (business logic).
        
        Raises:
            DatabaseOperationException: If there is an error during 
            the database operation.
        """
        output = False
        session = self.get_session()
        try:
            db_product_instance = session.query(DBProduct).filter(DBProduct.product_id == product_id).first()
            if db_product_instance:
                db_product_instance.name = product.name
                db_product_instance.description = product.description
                session.commit()
                output = True
            else:
                raise DataNotFoundException("Product not found")
        except DataNotFoundException as e:
            session.rollback()
            raise e
        except IntegrityError as e:
            session.rollback()
            raise DatabaseOperationException(f"Integrity error while updating product info: {e}")
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseOperationException(f"Database error while updating product info: {e}")
        except Exception as e:
            session.rollback()
            raise DatabaseOperationException(f"Unexpected error while updating product info: {e}")
        finally:
            session.close()
        return output

    def delete_product(self, product_id: str):
        """Delete product info from the database when product 
        - data is passed as Product DTO.
        
        Args:
            product_id (str): Product ID to delete.
        
        Raises:
            DatabaseOperationException: If there is an error during 
            the database operation.
        """
        output = False
        session = self.get_session()
        try:
            db_product_instance = session.query(DBProduct).filter(DBProduct.product_id == product_id).first()
            if db_product_instance:
                session.delete(db_product_instance)
                session.commit()
                output = True
            else:
                raise DataNotFoundException("Product not found")
        except DataNotFoundException as e:
            session.rollback()
            raise e
        except IntegrityError as e:
            session.rollback()
            raise DatabaseOperationException(f"Integrity error while deleting product info: {e}")
        except SQLAlchemyError as e:
            session.rollback()
            raise DatabaseOperationException(f"Database error while deleting product info: {e}")
        except Exception as e:
            session.rollback()
            raise DatabaseOperationException(f"Unexpected error while deleting product info: {e}")
        finally:
            session.close()
        return output
        
        
        

