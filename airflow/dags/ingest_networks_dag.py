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

def run_networks_ingestion():
    """Run the networks ingestion script with proper error handling."""
    try:
        from ingest_networks import fetch_networks, insert_into_postgres
        import logging
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        
        logger.info("Starting networks ingestion...")
        networks = fetch_networks()
        if networks:
            insert_into_postgres(networks)
            logger.info(f"Successfully processed {len(networks)} networks")
            return f"Processed {len(networks)} networks"
        else:
            logger.warning("No networks fetched")
            return "No networks fetched"
    except Exception as e:
        logger.error(f"Networks ingestion failed: {e}")
        raise

with DAG(
    dag_id='ingest_networks_dag',
    default_args=default_args,
    description='Ingest network data from PeeringDB API',
    schedule_interval=None,  # Manual trigger only for demo
    tags=['peeringdb', 'networks', 'ingestion'],
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

    # Networks ingestion task
    ingest_networks = PythonOperator(
        task_id='run_networks_ingestion',
        python_callable=run_networks_ingestion,
    )

    # Success notification
    success_notification = BashOperator(
        task_id='success_notification',
        bash_command='echo "Networks ingestion completed successfully!"',
    )

    # Set up dependencies
    health_check >> ingest_networks >> success_notification
