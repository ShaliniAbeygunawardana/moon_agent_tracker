import pandas as pd
from sqlalchemy.sql import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_best_performing_teams(session):
    query = """
        SELECT
        b.branch_id,
        b.branch_name,
        b.monthly_target,
        SUM(s.sale_amount) AS total_sales,
        CASE
            WHEN SUM(s.sale_amount) >= b.monthly_target THEN 'Target Achieved'
            ELSE 'Target Not Achieved'
        END AS target_status
        FROM moon_agent.sales_transaction s
        JOIN moon_agent.agent a ON s.agent_id = a.agent_id
        JOIN moon_agent.branch b ON a.branch_id = b.branch_id
        GROUP BY b.branch_id, b.branch_name, b.monthly_target
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
        p.product_id,
        p.name as product_name,
        pt.product_target_sales,
        SUM(s.sale_amount) AS total_sales,
        CASE
            WHEN SUM(s.sale_amount) >= pt.product_target_sales THEN 'Target Achieved'
            ELSE 'Target Not Achieved'
        END AS target_status
        FROM moon_agent.sales_transaction s
        JOIN moon_agent.product p ON s.product_id = p.product_id
        JOIN moon_agent.product_target pt ON p.product_id = pt.product_id
        GROUP BY p.product_id, p.name, pt.product_target_sales
        ORDER BY total_sales DESC;
    """
    result = pd.read_sql(text(query), session.bind)
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