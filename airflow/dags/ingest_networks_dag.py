from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2023, 1, 1),
    'catchup': False
}

with DAG(
    dag_id='ingest_networks_dag',
    default_args=default_args,
    schedule_interval=None,
    tags=['peeringdb'],
) as dag:

    ingest_networks = BashOperator(
        task_id='run_networks_ingestion',
        bash_command='python /opt/airflow/scripts/ingest_networks.py'
    )
