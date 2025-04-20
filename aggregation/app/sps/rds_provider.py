import pandas as pd
from sqlalchemy.sql import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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
    logger.info("Fetching best performing teams")
    result = pd.read_sql(query, session.bind)
    logger.info(f"Fetched {len(result)} best performing teams")
    return result

def get_top_products(session, sales_threshold=10000):
    logger.info("Fetching top products with sales threshold: {}".format(sales_threshold))
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
    result = pd.read_sql(text(query), session.bind, params={"threshold": sales_threshold})
    logger.info(f"Fetched {len(result)} top products")
    return result

def get_branch_performance(session):
    logger.info("Fetching branch performance")
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
    result = pd.read_sql(query, session.bind)
    logger.info(f"Fetched {len(result)} branch performance records")
    return result