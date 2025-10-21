#!/bin/bash

# PeeringDB Analytics Pipeline Setup Script
# This script sets up the complete pipeline with Airflow, PostgreSQL, dbt, and PowerBI integration

echo "🚀 Setting up PeeringDB Analytics Pipeline..."

# Create analytics schema in PostgreSQL
echo "📊 Creating analytics schema..."
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "CREATE SCHEMA IF NOT EXISTS analytics;"

# Grant permissions
echo "🔐 Setting up permissions..."
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "GRANT ALL PRIVILEGES ON SCHEMA analytics TO pe_user;"
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO pe_user;"
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics TO pe_user;"

# Initialize dbt
echo "🔧 Initializing dbt..."
docker exec dbt_runner dbt deps
docker exec dbt_runner dbt seed
docker exec dbt_runner dbt run
docker exec dbt_runner dbt test

# Generate dbt documentation
echo "📚 Generating dbt documentation..."
docker exec dbt_runner dbt docs generate

echo "✅ Setup complete!"
echo ""
echo "📋 Next Steps:"
echo "1. Access Airflow UI: http://localhost:8080"
echo "2. Access PostgreSQL: localhost:5433 (pe_user/pe_pass)"
echo "3. Connect PowerBI to PostgreSQL with connection string:"
echo "   Server=localhost,5433;Database=pe_data;User Id=pe_user;Password=pe_pass;Schema=analytics;"
echo "4. Use the test queries in powerbi/powerbi_test_queries.sql"
echo ""
echo "🎯 Key Analytics Tables:"
echo "- analytics.mart_network_peering_summary"
echo "- analytics.mart_ix_traffic_summary"
echo "- analytics.mart_geographic_analytics"
echo "- analytics.mart_facility_analytics"
