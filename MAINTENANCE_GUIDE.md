# PeeringDB Analytics Pipeline - Maintenance Guide

## 🚀 **Quick Start Commands**

### **Start Everything**
```powershell
cd C:\Users\donri\Desktop\Git\infra_pipeline_airflow
docker-compose up -d
```

### **Stop Everything**
```powershell
docker-compose down
```

### **Restart Everything**
```powershell
docker-compose down
docker-compose up -d
```

---

## 🔍 **Health Check Commands**

### **Check All Services**
```powershell
docker ps
```
**Expected**: 4 containers running (postgres, airflow-webserver, airflow-scheduler, dbt_runner)

### **Check Data**
```powershell
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "SELECT COUNT(*) FROM analytics.mart_network_peering_summary;"
```
**Expected**: 10 networks

### **Check Airflow DAGs**
```powershell
docker exec airflow_webserver airflow dags list
```
**Expected**: dbt_peeringdb_analytics DAG visible

---

## 🔧 **Troubleshooting**

### **Issue: PowerBI Can't Connect**
1. **Check PostgreSQL**: `docker ps | findstr postgres`
2. **Test connection**: `Test-NetConnection -ComputerName localhost -Port 5432`
3. **Restart PostgreSQL**: `docker-compose restart postgres`

### **Issue: Data Not Updating**
1. **Check dbt models**: `docker exec dbt_runner dbt run`
2. **Check Airflow DAGs**: Visit http://localhost:8080
3. **Refresh PowerBI**: Click refresh button

### **Issue: Containers Not Starting**
1. **Check Docker Desktop**: Ensure it's running
2. **Check ports**: Ensure 5432 and 8080 are free
3. **Restart Docker Desktop**: Right-click → Restart

---

## 📊 **Data Refresh Schedule**

### **Automatic (Every 6 Hours)**
- **Raw Data Ingestion**: Airflow DAGs
- **Data Transformation**: dbt models
- **Analytics Tables**: Updated automatically

### **Manual Refresh**
```powershell
# Refresh dbt models
docker exec dbt_runner dbt run

# Refresh specific model
docker exec dbt_runner dbt run --models mart_network_peering_summary
```

---

## 🎯 **Adding New Data Sources**

### **Step 1: Add New Table**
1. **Update** `postgres/init.sql`
2. **Add** new Airflow DAG
3. **Create** ingestion script

### **Step 2: Add dbt Model**
1. **Create** staging model in `dbt/models/staging/`
2. **Create** mart model in `dbt/models/marts/`
3. **Update** `dbt/models/schema.yml`

### **Step 3: Add PowerBI Visualization**
1. **Connect** to new analytics table
2. **Create** new dashboard
3. **Update** user guide

---

## 📈 **Performance Monitoring**

### **Database Performance**
```powershell
# Check table sizes
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "\dt+ analytics.*"

# Check query performance
docker exec sokrates_postgres psql -U pe_user -d pe_data -c "EXPLAIN ANALYZE SELECT COUNT(*) FROM analytics.mart_network_peering_summary;"
```

### **dbt Performance**
```powershell
# Check dbt run time
docker exec dbt_runner dbt run --profiles-dir /opt/dbt/profiles

# Check model dependencies
docker exec dbt_runner dbt list --output name
```

---

## 🔄 **Backup & Recovery**

### **Backup Database**
```powershell
docker exec sokrates_postgres pg_dump -U pe_user pe_data > backup_$(Get-Date -Format "yyyyMMdd").sql
```

### **Restore Database**
```powershell
docker exec -i sokrates_postgres psql -U pe_user pe_data < backup_20241220.sql
```

---

## 📞 **Support Contacts**

- **Technical Issues**: Check Docker logs
- **Data Issues**: Verify Airflow DAG status
- **PowerBI Issues**: Check connection settings
- **Performance Issues**: Monitor resource usage

---

## 🎯 **Key Metrics to Monitor**

- **Data Freshness**: Last update timestamps
- **Pipeline Health**: DAG success rates
- **Resource Usage**: CPU, memory, disk
- **User Access**: PowerBI refresh success

---

*Last Updated: [Current Date]*
*Pipeline Version: 1.0*
*Maintenance Level: Production Ready*
