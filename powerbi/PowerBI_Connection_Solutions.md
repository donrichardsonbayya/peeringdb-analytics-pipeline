# PowerBI PostgreSQL Connection Solutions

## 🎯 **TRY THESE CONNECTION DETAILS IN POWERBI DESKTOP:**

### **Option 1: Port 5434 (NEW - Recommended)**
```
Server: localhost
Port: 5434
Database: pe_data
Username: pe_user
Password: pe_pass
```

### **Option 2: Port 5434 with IP Address**
```
Server: 127.0.0.1
Port: 5434
Database: pe_data
Username: pe_user
Password: pe_pass
```

### **Option 3: Connection String Format**
```
Server=localhost;Port=5434;Database=pe_data;User Id=pe_user;Password=pe_pass;
```

## 🔧 **If Still Getting "Connection Refused" Error:**

### **Step 1: Restart Docker Desktop**
1. Right-click Docker Desktop icon in system tray
2. Select "Restart Docker Desktop"
3. Wait for it to fully restart
4. Try connecting again

### **Step 2: Check Windows Firewall**
1. Open Windows Defender Firewall
2. Click "Allow an app or feature through Windows Defender Firewall"
3. Find "PowerBI Desktop" and ensure it's allowed
4. If not found, click "Change settings" → "Allow another app" → Browse to PowerBI Desktop

### **Step 3: Try Different Connection Methods**

**Method A: Direct Connection**
- In PowerBI Desktop: Get Data → PostgreSQL database
- Use the connection details above

**Method B: Advanced Query**
- In PowerBI Desktop: Get Data → PostgreSQL database
- Click "Advanced options"
- Enter this SQL query:
```sql
SELECT 'Connection Test' as status, COUNT(*) as network_count 
FROM analytics.mart_network_peering_summary;
```

**Method C: Import vs DirectQuery**
- Try both "Import" and "DirectQuery" modes
- Import mode downloads data (better for small datasets)
- DirectQuery mode queries live data (better for large datasets)

### **Step 4: Alternative Ports**
If port 5434 doesn't work, try these ports:
- 5432 (default PostgreSQL port)
- 5435
- 5436

### **Step 5: Docker Desktop Settings**
1. Open Docker Desktop
2. Go to Settings → Resources → Network
3. Ensure "Enable Kubernetes" is OFF (if not needed)
4. Try switching between "WSL 2" and "Hyper-V" backends

## 🚨 **Emergency Solutions:**

### **Solution A: Use Docker Host Network**
If nothing else works, modify docker-compose.yml:
```yaml
services:
  postgres:
    image: postgres:15
    network_mode: "host"
    environment:
      POSTGRES_USER: pe_user
      POSTGRES_PASSWORD: pe_pass
      POSTGRES_DB: pe_data
```

### **Solution B: Install PostgreSQL Locally**
1. Download PostgreSQL from https://www.postgresql.org/download/windows/
2. Install with default settings
3. Create database `pe_data` and user `pe_user`
4. Import your data using pg_dump/pg_restore

### **Solution C: Use Cloud Database**
- Set up a free PostgreSQL database on:
  - Supabase (free tier)
  - Railway (free tier)
  - Neon (free tier)
- Export your data and import to cloud database

## 📊 **Test Your Connection:**

Run this PowerShell command to test:
```powershell
Test-NetConnection -ComputerName localhost -Port 5434
```

Should return: `TcpTestSucceeded : True`

## 🎯 **Quick Test Queries for PowerBI:**

Once connected, try these queries:

```sql
-- Test 1: Basic connection
SELECT 'PowerBI Connection Successful!' as status;

-- Test 2: Check analytics data
SELECT COUNT(*) as total_networks FROM analytics.mart_network_peering_summary;

-- Test 3: Sample data
SELECT network_name, total_peering_connections, peering_tier 
FROM analytics.mart_network_peering_summary 
LIMIT 5;
```
