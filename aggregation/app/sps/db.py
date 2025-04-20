import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from aggregation.configs import DB_STRING as RDS_DB_URL, \
    REDSHIFT_DB_ENDPOINT, REDSHIFT_DB_USERNAME, REDSHIFT_DB_PASSWORD, REDSHIFT_DB_NAME

def get_rds_engine():
    return create_engine(RDS_DB_URL)

def get_redshift_conn():
    return psycopg2.connect(
    host=REDSHIFT_DB_ENDPOINT,
    port=5439,
    dbname=REDSHIFT_DB_NAME,
    user=REDSHIFT_DB_USERNAME,
    password=REDSHIFT_DB_PASSWORD
)

RdsSession = sessionmaker(bind=get_rds_engine())