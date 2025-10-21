# PowerBI PostgreSQL Connection Troubleshooting Guide

## Common Issues and Solutions

### 1. "Cannot connect to server" Error
**Problem**: PowerBI can't connect to localhost:5433

**Solutions**:
- Verify PostgreSQL is running: `docker ps`
- Check if port 5433 is accessible: `netstat -an | findstr 5433`
- Try using `127.0.0.1` instead of `localhost`
- Ensure Windows Firewall allows PowerBI to access localhost

### 2. "Authentication failed" Error
**Problem**: Wrong username/password

**Solutions**:
- Username: `pe_user`
- Password: `pe_pass`
- Database: `pe_data`
- Test connection: `docker exec sokrates_postgres psql -U pe_user -d pe_data -c "SELECT 1;"`

### 3. "Schema not found" Error
**Problem**: Can't see analytics schema

**Solutions**:
- Make sure dbt models ran successfully
- Check analytics schema exists: `docker exec sokrates_postgres psql -U pe_user -d pe_data -c "\dn"`
- Re-run dbt: `docker exec dbt_runner dbt run`

### 4. "Table not found" Error
**Problem**: Analytics tables missing

**Solutions**:
- Check tables exist: `docker exec sokrates_postgres psql -U pe_user -d pe_data -c "\dt analytics.*"`
- Re-run dbt models: `docker exec dbt_runner dbt run`

### 5. Connection String Format
**Alternative connection string**:
```
Server=localhost;Port=5433;Database=pe_data;User Id=pe_user;Password=pe_pass;
```

### 6. Test Connection Commands
```bash
# Test PostgreSQL connection
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "SELECT version();"

# Test analytics data
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "SELECT COUNT(*) FROM analytics.mart_network_peering_summary;"

# List all tables
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "\dt analytics.*"
```

## PowerBI Desktop Tips

### 1. Data Refresh
- Set up automatic refresh schedule
- Use "Refresh" button for manual updates
- Consider incremental refresh for large datasets

### 2. Performance Optimization
- Use DirectQuery for real-time data
- Import mode for better performance
- Create calculated columns for complex logic

### 3. Dashboard Best Practices
- Use appropriate chart types
- Add filters and slicers
- Create drill-through pages
- Use bookmarks for navigation

## Sample PowerBI Queries

### Network Overview Dashboard
```sql
SELECT 
    network_name,
    org_name,
    total_peering_connections,
    peering_tier,
    total_bandwidth_mbps,
    bandwidth_tier
FROM analytics.mart_network_peering_summary
WHERE total_peering_connections > 0
ORDER BY total_peering_connections DESC
```

### IX Analytics Dashboard
```sql
SELECT 
    ix_name,
    ix_country,
    connected_networks,
    total_connections,
    ix_size_tier,
    total_bandwidth_mbps
FROM analytics.mart_ix_traffic_summary
ORDER BY total_connections DESC
```

### Geographic Analysis
```sql
SELECT 
    country,
    region,
    total_networks,
    total_organizations,
    market_size_tier
FROM analytics.mart_geographic_analytics
ORDER BY total_networks DESC
```
