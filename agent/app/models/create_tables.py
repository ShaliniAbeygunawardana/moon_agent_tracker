## set the BASE DIRECTORY path of the installation directory
import sys
import os

sys.path.append(r"C:/Users/Shalini Imantha/moon_agent_tracker/")


from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy_utils import database_exists, create_database, drop_database
from agent.app.models.db_models import init_db
from agent.configs import DB_STRING
import logging

logger = logging.getLogger(__name__)

def create_db_and_tables():
    try:
        engine = create_engine(DB_STRING, echo=True)
        if not database_exists(engine.url):
            create_database(engine.url)
            logger.info("Database created")
        else:
            logger.info("Database already exists")
        init_db(engine)
    except SQLAlchemyError as e:
        logger.error("Error while creating database and tables")
        logger.error(e)
        raise e
    
def drop_db():
    try:
        engine = create_engine(DB_STRING, echo=True)
        if database_exists(engine.url):
            drop_database(engine.url)
            logger.info("Database dropped")
        else:
            logger.info("Database does not exist")
    except SQLAlchemyError as e:
        logger.error("Error while dropping database")
        logger.error(e)
        raise e


if __name__ == "__main__":
    # create the db and the tables 
    create_db_and_tables()