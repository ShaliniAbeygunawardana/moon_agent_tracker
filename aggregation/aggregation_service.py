import os
import uuid
import pandas as pd
import psycopg2
from sqlalchemy import create_engine, Column, String, Integer, Text, DECIMAL, CHAR, ForeignKey, Enum, TIMESTAMP, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import text
from dotenv import load_dotenv

# Load .env variables if available
load_dotenv()

# --- Configuration ---
# RDS_DB_URL = os.getenv("RDS_DB_URL")         # e.g., postgresql://user:pass@host:port/dbname
# REDSHIFT_DB_URL = os.getenv("REDSHIFT_DB_URL")  # e.g., postgres://user:pass@redshift-endpoint/db

RDS_DB_URL = 'http://localhost:8000/moon-agent-database'
REDSHIFT_DB_URL = 'default-workgroup.381492058808.us-east-1.redshift-serverless.amazonaws.com:5439/dev'


# --- Aggregation Functions ---
def get_best_performing_teams(session):
    query = """
        SELECT 
            a.branch_id,
            b.branch_name,
            SUM(s.sale_amount) AS total_sales,
            COUNT(DISTINCT s.agent_id) AS num_agents
        FROM sales_transaction s
        JOIN agent a ON s.agent_id = a.agent_id
        JOIN branch b ON a.branch_id = b.branch_id
        GROUP BY a.branch_id, b.branch_name
        ORDER BY total_sales DESC;
    """
    return pd.read_sql(query, session.bind)

def get_top_products(session, sales_threshold=10000):
    query = """
        SELECT 
            p.name AS product_name,
            SUM(s.sale_amount) AS total_sales
        FROM sales_transaction s
        JOIN product p ON s.product_id = p.product_id
        GROUP BY p.name
        HAVING SUM(s.sale_amount) >= :threshold
        ORDER BY total_sales DESC;
    """
    return pd.read_sql(text(query), session.bind, params={"threshold": sales_threshold})

def get_branch_performance(session):
    query = """
        SELECT 
            b.branch_name,
            COUNT(DISTINCT a.agent_id) AS num_agents,
            SUM(s.sale_amount) AS total_branch_sales
        FROM sales_transaction s
        JOIN agent a ON s.agent_id = a.agent_id
        JOIN branch b ON a.branch_id = b.branch_id
        GROUP BY b.branch_name
        ORDER BY total_branch_sales DESC;
    """
    return pd.read_sql(query, session.bind)

def load_to_redshift(df, table_name):
    conn = psycopg2.connect(REDSHIFT_DB_URL)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cols = ", ".join(df.columns)
        placeholders = ", ".join(["%s"] * len(df.columns))
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        cursor.execute(sql, tuple(row))

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Loaded data into Redshift table: {table_name}")

# --- Main Logic ---
def run_aggregator():
    session = SessionLocal()
    try:
        print("Aggregating best performing teams...")
        best_teams = get_best_performing_teams(session)
        load_to_redshift(best_teams, "aggregated_best_teams")

        print("Aggregating top products...")
        top_products = get_top_products(session)
        load_to_redshift(top_products, "aggregated_top_products")

        print("Aggregating branch performance...")
        branch_performance = get_branch_performance(session)
        load_to_redshift(branch_performance, "aggregated_branch_performance")

        print("Aggregation and loading complete.")
    finally:
        session.close()

if __name__ == "__main__":
    run_aggregator()
