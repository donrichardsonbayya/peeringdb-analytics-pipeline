#!/usr/bin/env python3
"""
PeeringDB Analytics Pipeline Demo Script
This script helps demonstrate the complete pipeline functionality.
"""

import time
import requests
import psycopg2
from datetime import datetime

def check_airflow_status():
    """Check if Airflow is running and accessible."""
    try:
        response = requests.get('http://localhost:8080/health', timeout=10)
        if response.status_code == 200:
            print("✅ Airflow is running and accessible")
            return True
        else:
            print(f"⚠️  Airflow responded with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Airflow is not accessible: {e}")
        return False

def check_database_status():
    """Check database connectivity and data."""
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="pe_data",
            user="pe_user",
            password="pe_pass"
        )
        cur = conn.cursor()
        
        # Get table counts
        cur.execute("SELECT COUNT(*) FROM organizations;")
        org_count = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM networks;")
        net_count = cur.fetchone()[0]
        
        print(f"✅ Database is accessible")
        print(f"   - Organizations: {org_count}")
        print(f"   - Networks: {net_count}")
        
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def trigger_pipeline():
    """Trigger the complete pipeline DAG."""
    try:
        # Trigger the complete pipeline DAG
        response = requests.post(
            'http://localhost:8080/api/v1/dags/peeringdb_complete_pipeline/dagRuns',
            json={
                "conf": {},
                "dag_run_id": f"demo_run_{int(time.time())}"
            },
            headers={'Content-Type': 'application/json'},
            timeout=30
        )
        
        if response.status_code == 200:
            print("✅ Pipeline triggered successfully!")
            return True
        else:
            print(f"❌ Failed to trigger pipeline: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error triggering pipeline: {e}")
        return False

def show_dag_status():
    """Show the status of all DAGs."""
    try:
        response = requests.get('http://localhost:8080/api/v1/dags', timeout=10)
        if response.status_code == 200:
            dags = response.json()['dags']
            print("\n📊 DAG Status Overview:")
            print("-" * 50)
            
            for dag in dags:
                dag_id = dag['dag_id']
                state = dag.get('dag_run_state', 'No runs')
                last_run = dag.get('last_dag_run', 'Never')
                
                status_icon = "✅" if state == "success" else "❌" if state == "failed" else "⏳" if state == "running" else "⚪"
                print(f"{status_icon} {dag_id}: {state} (Last run: {last_run})")
            
            return True
        else:
            print(f"❌ Failed to get DAG status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error getting DAG status: {e}")
        return False

def main():
    """Main demo function."""
    print("🚀 PeeringDB Analytics Pipeline Demo")
    print("=" * 50)
    
    # Check system status
    print("\n1. Checking System Status...")
    airflow_ok = check_airflow_status()
    db_ok = check_database_status()
    
    if not airflow_ok or not db_ok:
        print("\n❌ System not ready. Please ensure:")
        print("   - Docker containers are running: docker-compose up -d")
        print("   - Airflow is accessible at http://localhost:8080")
        print("   - PostgreSQL is running on port 5432")
        return
    
    # Show current DAG status
    print("\n2. Current DAG Status...")
    show_dag_status()
    
    # Ask user if they want to trigger the pipeline
    print("\n3. Pipeline Options:")
    print("   a) Trigger complete pipeline")
    print("   b) Show DAG status only")
    print("   c) Exit")
    
    choice = input("\nEnter your choice (a/b/c): ").lower().strip()
    
    if choice == 'a':
        print("\n🎯 Triggering Complete Pipeline...")
        if trigger_pipeline():
            print("\n⏳ Pipeline is running. You can monitor progress at:")
            print("   http://localhost:8080")
            print("\nThe pipeline will:")
            print("   1. Check database health")
            print("   2. Ingest organizations data")
            print("   3. Ingest networks data")
            print("   4. Run dbt transformations")
            print("   5. Generate analytics tables")
            
            # Wait a bit and show updated status
            print("\n⏳ Waiting 30 seconds for pipeline to start...")
            time.sleep(30)
            show_dag_status()
    
    elif choice == 'b':
        show_dag_status()
    
    elif choice == 'c':
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()
