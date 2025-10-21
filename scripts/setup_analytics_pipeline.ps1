# PeeringDB Analytics Pipeline Setup Script (PowerShell)
# This script sets up the complete pipeline with Airflow, PostgreSQL, dbt, and PowerBI integration

Write-Host "🚀 Setting up PeeringDB Analytics Pipeline..." -ForegroundColor Green

# Create analytics schema in PostgreSQL
Write-Host "📊 Creating analytics schema..." -ForegroundColor Yellow
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "CREATE SCHEMA IF NOT EXISTS analytics;"

# Grant permissions
Write-Host "🔐 Setting up permissions..." -ForegroundColor Yellow
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "GRANT ALL PRIVILEGES ON SCHEMA analytics TO pe_user;"
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics TO pe_user;"
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics TO pe_user;"

# Initialize dbt
Write-Host "🔧 Initializing dbt..." -ForegroundColor Yellow
docker exec dbt_runner dbt deps
docker exec dbt_runner dbt seed
docker exec dbt_runner dbt run
docker exec dbt_runner dbt test

# Generate dbt documentation
Write-Host "📚 Generating dbt documentation..." -ForegroundColor Yellow
docker exec dbt_runner dbt docs generate

Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Cyan
Write-Host "1. Access Airflow UI: http://localhost:8080" -ForegroundColor White
Write-Host "2. Access PostgreSQL: localhost:5433 (pe_user/pe_pass)" -ForegroundColor White
Write-Host "3. Connect PowerBI to PostgreSQL with connection string:" -ForegroundColor White
Write-Host "   Server=localhost,5433;Database=pe_data;User Id=pe_user;Password=pe_pass;Schema=analytics;" -ForegroundColor Gray
Write-Host "4. Use the test queries in powerbi/powerbi_test_queries.sql" -ForegroundColor White
Write-Host ""
Write-Host "🎯 Key Analytics Tables:" -ForegroundColor Cyan
Write-Host "- analytics.mart_network_peering_summary" -ForegroundColor White
Write-Host "- analytics.mart_ix_traffic_summary" -ForegroundColor White
Write-Host "- analytics.mart_geographic_analytics" -ForegroundColor White
Write-Host "- analytics.mart_facility_analytics" -ForegroundColor White
