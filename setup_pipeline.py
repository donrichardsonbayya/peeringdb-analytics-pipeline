#!/usr/bin/env python3
"""
PeeringDB Analytics Pipeline Setup and Validation Script
This script ensures the pipeline is properly configured and ready for demo.
"""

import subprocess
import time
import requests
import psycopg2
import sys
from datetime import datetime

def run_command(command, description):
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def wait_for_service(url, service_name, max_attempts=30):
    """Wait for a service to become available."""
    print(f"⏳ Waiting for {service_name} to be ready...")
    for attempt in range(max_attempts):
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {service_name} is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        
        time.sleep(2)
        print(f"   Attempt {attempt + 1}/{max_attempts}...")
    
    print(f"❌ {service_name} failed to start within {max_attempts * 2} seconds")
    return False

def setup_pipeline():
    """Set up the complete pipeline."""
    print("🚀 Setting up PeeringDB Analytics Pipeline")
    print("=" * 50)
    
    # Step 1: Stop any existing containers
    print("\n1. Cleaning up existing containers...")
    run_command("docker-compose down", "Stopping existing containers")
    
    # Step 2: Build and start containers
    print("\n2. Building and starting containers...")
    if not run_command("docker-compose up -d --build", "Building and starting containers"):
        print("❌ Failed to start containers. Please check Docker is running.")
        return False
    
    # Step 3: Wait for services to be ready
    print("\n3. Waiting for services to be ready...")
    
    # Wait for PostgreSQL
    if not wait_for_service("http://localhost:5432", "PostgreSQL", 15):
        print("❌ PostgreSQL failed to start")
        return False
    
    # Wait for Airflow
    if not wait_for_service("http://localhost:8080/health", "Airflow", 30):
        print("❌ Airflow failed to start")
        return False
    
    # Step 4: Initialize Airflow database
    print("\n4. Initializing Airflow database...")
    if not run_command("docker exec airflow_webserver airflow db init", "Initializing Airflow database"):
        print("⚠️  Airflow database initialization may have failed, but continuing...")
    
    # Step 5: Create Airflow admin user
    print("\n5. Creating Airflow admin user...")
    admin_command = """
    docker exec airflow_webserver airflow users create \
        --username admin \
        --firstname Admin \
        --lastname User \
        --role Admin \
        --email admin@example.com \
        --password admin
    """
    run_command(admin_command, "Creating Airflow admin user")
    
    # Step 6: Verify database schema
    print("\n6. Verifying database schema...")
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="pe_data",
            user="pe_user",
            password="pe_pass"
        )
        cur = conn.cursor()
        
        # Check if tables exist
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        print(f"✅ Database schema verified. Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False
    
    # Step 7: Test DAG loading
    print("\n7. Testing DAG loading...")
    time.sleep(10)  # Give Airflow time to load DAGs
    
    try:
        response = requests.get('http://localhost:8080/api/v1/dags', timeout=10)
        if response.status_code == 200:
            dags = response.json()['dags']
            print(f"✅ Found {len(dags)} DAGs:")
            for dag in dags:
                print(f"   - {dag['dag_id']}")
        else:
            print(f"❌ Failed to load DAGs: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error loading DAGs: {e}")
        return False
    
    print("\n🎉 Pipeline setup completed successfully!")
    print("\n📋 Next Steps:")
    print("   1. Open http://localhost:8080 in your browser")
    print("   2. Login with username: admin, password: admin")
    print("   3. Run the demo script: python demo_pipeline.py")
    print("   4. Or manually trigger DAGs from the Airflow UI")
    
    return True

def validate_pipeline():
    """Validate that the pipeline is working correctly."""
    print("\n🔍 Validating Pipeline...")
    
    # Check Airflow
    try:
        response = requests.get('http://localhost:8080/health', timeout=5)
        if response.status_code == 200:
            print("✅ Airflow is healthy")
        else:
            print("❌ Airflow health check failed")
            return False
    except Exception as e:
        print(f"❌ Airflow validation failed: {e}")
        return False
    
    # Check Database
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="pe_data",
            user="pe_user",
            password="pe_pass"
        )
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM organizations;")
        org_count = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM networks;")
        net_count = cur.fetchone()[0]
        
        print(f"✅ Database is healthy - Organizations: {org_count}, Networks: {net_count}")
        conn.close()
    except Exception as e:
        print(f"❌ Database validation failed: {e}")
        return False
    
    print("✅ Pipeline validation completed successfully!")
    return True

def main():
    """Main function."""
    if len(sys.argv) > 1 and sys.argv[1] == "validate":
        validate_pipeline()
    else:
        setup_pipeline()

if __name__ == "__main__":
    main()
