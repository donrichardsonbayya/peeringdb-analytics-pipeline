from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

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
    ingest_organizations = BashOperator(
        task_id='run_organizations_ingestion',
        bash_command='cd /opt/airflow/scripts && python ingest_org.py',
    )

    # Success notification
    success_notification = BashOperator(
        task_id='success_notification',
        bash_command='echo "Organizations ingestion completed successfully!"',
    )

    # Set up dependencies
    health_check >> ingest_organizations >> success_notification
