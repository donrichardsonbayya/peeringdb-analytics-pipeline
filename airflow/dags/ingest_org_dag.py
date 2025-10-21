from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add scripts directory to Python path
sys.path.append('/opt/airflow/scripts')

default_args = {
    'owner': 'peeringdb_analytics',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'catchup': False
}

def run_organizations_ingestion():
    """Run the organizations ingestion script with proper error handling."""
    try:
        from ingest_org import fetch_organizations, insert_into_postgres
        import logging
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        logger.info("Starting organizations ingestion...")
        organizations = fetch_organizations()
        if organizations:
            insert_into_postgres(organizations)
            logger.info(f"Successfully processed {len(organizations)} organizations")
            return f"Processed {len(organizations)} organizations"
        else:
            logger.warning("No organizations fetched")
            return "No organizations fetched"
    except Exception as e:
        logger.error(f"Organizations ingestion failed: {e}")
        raise

with DAG(
    dag_id='ingest_organizations_dag',
    default_args=default_args,
    description='Ingest organization data from PeeringDB API',
    schedule_interval=None,  # Manual trigger only for demo
    tags=['peeringdb', 'organizations', 'ingestion'],
    max_active_runs=1,
) as dag:

    # Health check task
    health_check = BashOperator(
        task_id='health_check',
        bash_command='''
        echo "Checking database connection..."
        python -c "
        import psycopg2
        try:
            conn = psycopg2.connect(host='postgres', port=5432, database='pe_data', user='pe_user', password='pe_pass')
            conn.close()
            print('Database connection successful')
        except Exception as e:
            print(f'Database connection failed: {e}')
            exit(1)
        "
        ''',
    )

    # Organizations ingestion task
    ingest_organizations = PythonOperator(
        task_id='run_organizations_ingestion',
        python_callable=run_organizations_ingestion,
    )

    # Success notification
    success_notification = BashOperator(
        task_id='success_notification',
        bash_command='echo "Organizations ingestion completed successfully!"',
    )

    # Set up dependencies
    health_check >> ingest_organizations >> success_notification
