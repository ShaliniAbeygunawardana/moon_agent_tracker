import os

# Load env variables for RDS database connection
DB_USERNAME = os.getenv('DB_USERNAME', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Sha1014*')
DB_ENDPOINT = os.getenv('DB_ENDPOINT', 'moon-agent-database.cu76c40m8t8k.us-east-1.rds.amazonaws.com')
DB_NAME = os.getenv('DB_NAME', 'moon_agent')
DB_STRING_CHECK = os.getenv('DB_STRING')

if not DB_STRING_CHECK:
    os.environ["DB_STRING"] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}'

DB_STRING = os.getenv('DB_STRING')  

# Load env variables for Redshift database connection
REDSHIFT_DB_USERNAME = os.getenv('REDSHIFT_DB_USERNAME', 'admin')
REDSHIFT_DB_PASSWORD = os.getenv('REDSHIFT_DB_PASSWORD', 'Sha1014*')
REDSHIFT_DB_ENDPOINT = os.getenv('REDSHIFT_DB_ENDPOINT', 'default-workgroup.381492058808.us-east-1.redshift-serverless.amazonaws.com')
REDSHIFT_DB_NAME = os.getenv('REDSHIFT_DB_NAME', 'dev')
REDSHIFT_DB_STRING_CHECK = os.getenv('REDSHIFT_DB_STRING')

if not REDSHIFT_DB_STRING_CHECK:
    os.environ["REDSHIFT_DB_STRING"] = f'postgresql://{REDSHIFT_DB_USERNAME}:{REDSHIFT_DB_PASSWORD}@{REDSHIFT_DB_ENDPOINT}/{REDSHIFT_DB_NAME}'
REDSHIFT_DB_STRING = os.getenv('REDSHIFT_DB_STRING') 

