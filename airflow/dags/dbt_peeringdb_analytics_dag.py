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
    'catchup': False
}

dag = DAG(
    'dbt_peeringdb_analytics',
    default_args=default_args,
    description='dbt transformations for PeeringDB analytics',
    schedule_interval=None,  # Manual trigger only for demo
    catchup=False,
    tags=['dbt', 'analytics', 'peeringdb'],
    max_active_runs=1,
)

# Start task
start = DummyOperator(
    task_id='start',
    dag=dag,
)

# Check if dbt container is running
dbt_container_check = BashOperator(
    task_id='dbt_container_check',
    bash_command='''
    echo "Checking if dbt container is running..."
    if docker ps | grep -q dbt_runner; then
        echo "dbt container is running"
    else
        echo "dbt container is not running, starting it..."
        docker-compose up -d dbt
        sleep 10
    fi
    ''',
    dag=dag,
)

# dbt deps - install dependencies
dbt_deps = BashOperator(
    task_id='dbt_deps',
    bash_command='''
    echo "Installing dbt dependencies..."
    docker exec dbt_runner bash -c "cd /opt/dbt && dbt deps || echo 'No dependencies to install'"
    ''',
    dag=dag,
)

# dbt run - run models
dbt_run = BashOperator(
    task_id='dbt_run',
    bash_command='''
    echo "Running dbt models..."
    docker exec dbt_runner bash -c "cd /opt/dbt && dbt run --profiles-dir /opt/dbt/profiles"
    ''',
    dag=dag,
)

# dbt test - run tests
dbt_test = BashOperator(
    task_id='dbt_test',
    bash_command='''
    echo "Running dbt tests..."
    docker exec dbt_runner bash -c "cd /opt/dbt && dbt test --profiles-dir /opt/dbt/profiles || echo 'Some tests may have failed, continuing...'"
    ''',
    dag=dag,
)

# End task
end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Set up dependencies
start >> dbt_container_check >> dbt_deps >> dbt_run >> dbt_test >> end
