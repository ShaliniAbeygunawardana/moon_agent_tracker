import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_to_redshift(df, table_name, conn):
    cursor = conn.cursor()
    logger.info(f"Loading data into Redshift table: {table_name}")
    for _, row in df.iterrows():
        cols = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))
    conn.commit()
    cursor.close()
    logger.info(f"Loaded data into Redshift table: {table_name}")