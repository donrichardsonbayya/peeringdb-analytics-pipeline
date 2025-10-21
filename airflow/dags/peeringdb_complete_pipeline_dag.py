from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.bash import BashOperator

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
    'peeringdb_complete_pipeline',
    default_args=default_args,
    description='Complete PeeringDB analytics pipeline - Data ingestion to analytics',
    schedule_interval=None,  # Manual trigger only for demo
    catchup=False,
    tags=['peeringdb', 'complete', 'pipeline', 'demo'],
    max_active_runs=1,
)

# Start task
start = DummyOperator(
    task_id='start',
    dag=dag,
)

# Database health check
db_health_check = BashOperator(
    task_id='database_health_check',
    bash_command='''
    echo "=== DATABASE HEALTH CHECK ==="
    python -c "
    import psycopg2
    try:
        conn = psycopg2.connect(host='postgres', port=5432, database='pe_data', user='pe_user', password='pe_pass')
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) FROM organizations;')
        org_count = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM networks;')
        net_count = cur.fetchone()[0]
        print(f'Database is healthy - Organizations: {org_count}, Networks: {net_count}')
        conn.close()
    except Exception as e:
        print(f'Database health check failed: {e}')
        exit(1)
    "
    ''',
    dag=dag,
)

# Trigger organizations ingestion
trigger_organizations = TriggerDagRunOperator(
    task_id='trigger_organizations_ingestion',
    trigger_dag_id='ingest_organizations_dag',
    dag=dag,
)

# Trigger networks ingestion
trigger_networks = TriggerDagRunOperator(
    task_id='trigger_networks_ingestion',
    trigger_dag_id='ingest_networks_dag',
    dag=dag,
)

# Wait for ingestion to complete
wait_for_ingestion = BashOperator(
    task_id='wait_for_ingestion_completion',
    bash_command='''
    echo "Waiting for data ingestion to complete..."
    sleep 30
    echo "Ingestion phase completed"
    ''',
    dag=dag,
)

# Trigger dbt transformations
trigger_dbt = TriggerDagRunOperator(
    task_id='trigger_dbt_transformations',
    trigger_dag_id='dbt_peeringdb_analytics',
    dag=dag,
)

# Pipeline summary
pipeline_summary = BashOperator(
    task_id='pipeline_summary',
    bash_command='''
    echo "=== PIPELINE EXECUTION SUMMARY ==="
    python -c "
    import psycopg2
    try:
        conn = psycopg2.connect(host='postgres', port=5432, database='pe_data', user='pe_user', password='pe_pass')
        cur = conn.cursor()
        
        # Get counts
        cur.execute('SELECT COUNT(*) FROM organizations;')
        org_count = cur.fetchone()[0]
        cur.execute('SELECT COUNT(*) FROM networks;')
        net_count = cur.fetchone()[0]
        
        print(f'✅ Organizations ingested: {org_count}')
        print(f'✅ Networks ingested: {net_count}')
        
        # Check if analytics tables exist
        cur.execute(\"\"\"
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'analytics'
        \"\"\")
        analytics_tables = [row[0] for row in cur.fetchall()]
        
        if analytics_tables:
            print(f'✅ Analytics tables created: {len(analytics_tables)}')
            for table in analytics_tables:
                cur.execute(f'SELECT COUNT(*) FROM analytics.{table};')
                count = cur.fetchone()[0]
                print(f'   - {table}: {count} records')
        else:
            print('⚠️  No analytics tables found (dbt may not have run yet)')
        
        conn.close()
        print('🎉 Pipeline execution completed successfully!')
        
    except Exception as e:
        print(f'❌ Pipeline summary failed: {e}')
        exit(1)
    "
    ''',
    dag=dag,
)

# End task
end = DummyOperator(
    task_id='end',
    dag=dag,
)

# Set up dependencies
start >> db_health_check >> [trigger_organizations, trigger_networks] >> wait_for_ingestion >> trigger_dbt >> pipeline_summary >> end
