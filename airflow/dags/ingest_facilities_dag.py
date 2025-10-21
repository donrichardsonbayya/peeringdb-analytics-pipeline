from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 1, 1),
    'catchup': False
}

with DAG(
    dag_id='ingest_facilities_dag',
    default_args=default_args,
    schedule_interval=None,
    tags=['peeringdb'],
) as dag:

    ingest_facilities = BashOperator(
        task_id='run_facilities_ingestion',
        bash_command='python /opt/airflow/scripts/ingest_facilities.py'
    )
