# PeeringDB Analytics Dashboard User Guide

## 📊 **Dashboard Overview**

This analytics pipeline provides insights into PeeringDB infrastructure utilization and performance across networks, Internet Exchanges (IXs), and facilities.

## 🎯 **Dashboard 1: Network Peering Overview**

### **Purpose**
Analyzes network peering activities and identifies opportunities for improved connectivity.

### **Key Metrics**
- **Total Networks**: 10 networks in the system
- **Active Networks**: 3 networks with peering connections (30% utilization)
- **Total Bandwidth**: 391,000 Mbps across all networks

### **Key Insights**
- **70% of networks** have no peering connections
- **Swisscom** leads with 4 peering connections
- **Akamai Technologies** has the highest bandwidth (200,000 Mbps)

### **Business Value**
- Identifies networks that could benefit from more peering
- Shows bandwidth leaders for partnership opportunities
- Highlights underutilized network potential

---

## 🏢 **Dashboard 2: Facility Analytics Dashboard**

### **Purpose**
Analyzes data center and colocation facility utilization and market distribution.

### **Key Metrics**
- **Total Facilities**: 150 facilities worldwide
- **Active Facilities**: 13 facilities with networks (8.7% utilization)
- **Average Networks per Facility**: 0.16 networks per facility

### **Key Insights**
- **91.3% of facilities** are empty (massive underutilization)
- **All active facilities** are located in the US
- **Equinix dominates** the active facility market

### **Business Value**
- Identifies massive expansion opportunities
- Shows geographic concentration in US market
- Highlights facility utilization gaps

---

## 🌐 **Dashboard 3: Internet Exchange Performance**

### **Purpose**
Analyzes Internet Exchange performance and connectivity metrics.

### **Key Metrics**
- **Total IXs**: 50 Internet Exchanges
- **Active IXs**: 3 IXs with connections (6% utilization)
- **Average Connections**: 0.12 connections per IX

### **Key Insights**
- **94% of IXs** are inactive
- **All active IXs** are Equinix facilities in the US
- **San Jose** has the most connections (4)

### **Business Value**
- Shows critical IX underutilization
- Identifies Equinix market dominance
- Highlights geographic concentration

---

## 📈 **Dashboard 4: Executive Summary**

### **Purpose**
Provides high-level overview of all infrastructure components and utilization rates.

### **Key Metrics**
- **Infrastructure Utilization**: Networks (30%), IXs (6%), Facilities (8.7%)
- **Geographic Concentration**: All active infrastructure in US
- **Top Performers**: Swisscom, Akamai Technologies, DALnet IRC Network

### **Key Insights**
- **Massive underutilization** across all infrastructure types
- **US market dominance** in active infrastructure
- **Significant growth opportunities** in all areas

### **Business Value**
- Executive-level infrastructure overview
- Identifies strategic expansion opportunities
- Shows market concentration patterns

---

## 🔄 **Data Refresh Schedule**

- **Raw Data**: Updated via Airflow DAGs (every 6 hours)
- **Analytics Models**: Refreshed via dbt (every 6 hours)
- **PowerBI Dashboards**: Refresh manually or set to automatic

## 📞 **Support & Maintenance**

### **Access Points**
- **Airflow UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432 (pe_user/pe_pass)
- **PowerBI**: Desktop application

### **Troubleshooting**
1. **Check Docker containers**: `docker ps`
2. **Verify data**: Check analytics schema tables
3. **Refresh PowerBI**: Click refresh button
4. **Restart services**: `docker-compose restart`

---

## 🎯 **Key Business Recommendations**

1. **Focus on US Market**: All active infrastructure is US-based
2. **Activate More IXs**: Only 6% of IXs are active
3. **Expand Facility Usage**: 91.3% of facilities are empty
4. **Target High-Bandwidth Networks**: Focus on Akamai/Swisscom tier
5. **Geographic Expansion**: Consider international markets

---

*Last Updated: [Current Date]*
*Data Source: PeeringDB API*
*Pipeline: Airflow → PostgreSQL → dbt → PowerBI*
