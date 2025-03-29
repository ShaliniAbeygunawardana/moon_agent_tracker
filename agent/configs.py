import os

DB_USERNAME = os.getenv('DB_USERNAME', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'sha1014*')
DB_ENDPOINT = os.getenv('DB_ENDPOINT', '127.0.0.1')
DB_NAME = os.getenv('DB_NAME', 'moon_agent')
DB_STRING_CHECK = os.getenv('DB_STRING')

if not DB_STRING_CHECK:
    os.environ["DB_STRING"] = f'mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}'

DB_STRING = os.getenv('DB_STRING')    