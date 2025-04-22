import sys
sys.path.append("/app/")
from app.sps.db import RdsSession, get_redshift_conn
from app.sps.rds_provider import get_best_performing_teams, get_top_products, get_branch_performance
from app.sps.redshift_provider import load_to_redshift
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_aggregator():
    rds_connection = RdsSession()
    redshift_conn = get_redshift_conn() 
    try:
        logger.info("Aggregating best performing teams...")
        best_teams = get_best_performing_teams(rds_connection)
        load_to_redshift(best_teams, "best_teams", redshift_conn)

        logger.info("Aggregating top products...")
        target_achieved_products = get_top_products(rds_connection)
        load_to_redshift(target_achieved_products, "target_achieved_products", redshift_conn)

        logger.info("Aggregating branch performance...")
        branch_performance = get_branch_performance(rds_connection)
        load_to_redshift(branch_performance, "branch_performance", redshift_conn)

        logger.info("Aggregation and loading complete.")
        
    except Exception as e:
        logger.error("An error occurred during aggregation and loading.")
        logger.error(e)
        raise e
    finally:
        rds_connection.close()
        redshift_conn.close()

if __name__ == "__main__":
    run_aggregator()