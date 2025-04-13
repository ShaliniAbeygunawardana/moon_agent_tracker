import os

DB_USERNAME = os.getenv('DB_USERNAME', 'admin')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'Sha1014*')
DB_ENDPOINT = os.getenv('DB_ENDPOINT', 'moon-agent-database.cu76c40m8t8k.us-east-1.rds.amazonaws.com')
DB_NAME = os.getenv('DB_NAME', 'moon_agent')
DB_STRING_CHECK = os.getenv('DB_STRING')

if not DB_STRING_CHECK:
    os.environ["DB_STRING"] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}'

DB_STRING = os.getenv('DB_STRING')   

DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', r"C:/Users/Shalini Imantha/moon_agent_tracker/intergration/data/output/") 
