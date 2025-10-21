from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.dummy import DummyOperator

default_args = {
    'owner': 'peeringdb_analytics',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'dbt_peeringdb_analytics',
    default_args=default_args,
    description='dbt transformations for PeeringDB analytics',
    schedule_interval=timedelta(hours=6),  # Run every 6 hours
    catchup=False,
    tags=['dbt', 'analytics', 'peeringdb'],
)

# Start task
start = DummyOperator(
    task_id='start',
    dag=dag,
)

# dbt deps - install dependencies
dbt_deps = BashOperator(
    task_id='dbt_deps',
    bash_command='docker exec dbt_runner dbt deps',
    dag=dag,
)

# dbt seed - load seed data
dbt_seed = BashOperator(
    task_id='dbt_seed',
    bash_command='docker exec dbt_runner dbt seed',
    dag=dag,
)

# dbt run - run models
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='docker exec dbt_runner dbt run',
    dag=dag,
)

# dbt test - run tests
dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='docker exec dbt_runner dbt test',
    dag=dag,
)

# dbt docs generate - generate documentation
dbt_docs = BashOperator(
    task_id='dbt_docs',
    bash_command='docker exec dbt_runner dbt docs generate',
    dag=dag,
)

# End task
end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Set up dependencies
start >> dbt_deps >> dbt_seed >> dbt_run >> dbt_test >> dbt_docs >> end
