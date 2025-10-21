# 🌐 PeeringDB Analytics Pipeline

[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Airflow](https://img.shields.io/badge/Apache%20Airflow-017CEE?style=for-the-badge&logo=apache-airflow&logoColor=white)](https://airflow.apache.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![dbt](https://img.shields.io/badge/dbt-FF6944?style=for-the-badge&logo=dbt&logoColor=white)](https://www.getdbt.com/)
[![PowerBI](https://img.shields.io/badge/PowerBI-F2C811?style=for-the-badge&logo=power-bi&logoColor=black)](https://powerbi.microsoft.com/)

A comprehensive **data analytics pipeline** that processes PeeringDB infrastructure data to provide actionable business insights through interactive dashboards.

## 📊 **Project Overview**

This project demonstrates a complete **end-to-end data pipeline** using modern data engineering tools:

```
PeeringDB API → Airflow → PostgreSQL → dbt → PowerBI
     ↓            ↓          ↓         ↓       ↓
  Raw Data    ETL Process  Storage  Analytics  Visualization
```

### **Key Features**
- 🔄 **Automated Data Ingestion** via Airflow DAGs
- 🗄️ **Data Storage** with PostgreSQL
- 🔧 **Data Transformation** using dbt
- 📈 **Interactive Dashboards** in PowerBI
- 🐳 **Containerized Infrastructure** with Docker
- 📊 **Real-time Analytics** with 6-hour refresh cycles

## 🎯 **Business Value**

### **Infrastructure Insights**
- **91.3% facility underutilization** - massive expansion opportunity
- **94% Internet Exchange underutilization** - critical infrastructure gap
- **US market concentration** - all active infrastructure in US
- **Equinix market dominance** - clear market leader identification

### **Data Processed**
- **25 Organizations** - Companies owning networks
- **10 Networks** - ASNs and their details
- **50 Internet Exchanges** - Physical peering locations
- **150 Facilities** - Data centers and colocation sites
- **391,000 Mbps** - Total bandwidth capacity

## 🏗️ **Architecture**

### **Technology Stack**
- **Orchestration**: Apache Airflow
- **Database**: PostgreSQL 15
- **Transformation**: dbt (Data Build Tool)
- **Visualization**: Microsoft PowerBI
- **Containerization**: Docker & Docker Compose
- **Languages**: Python, SQL, DAX

### **Data Flow**
1. **Ingestion**: Airflow DAGs fetch data from PeeringDB API
2. **Storage**: Raw data stored in PostgreSQL
3. **Transformation**: dbt models clean and aggregate data
4. **Analytics**: PowerBI dashboards provide business insights
5. **Automation**: 6-hour refresh cycles maintain data freshness

## 📈 **Dashboards**

### **1. Network Peering Overview**
- Network connectivity analysis
- Peering tier distribution
- Bandwidth utilization metrics
- Top performing networks

### **2. Facility Analytics**
- Data center utilization rates
- Geographic distribution
- Facility performance metrics
- Market concentration analysis

### **3. Internet Exchange Performance**
- IX connectivity metrics
- Performance benchmarking
- Geographic distribution
- Utilization analysis

### **4. Executive Summary**
- High-level infrastructure overview
- Cross-component utilization rates
- Strategic insights and recommendations
- Key performance indicators

## 🚀 **Quick Start**

### **Prerequisites**
- Docker Desktop
- PowerBI Desktop
- Git

### **Installation**

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/peeringdb-analytics-pipeline.git
cd peeringdb-analytics-pipeline
```

2. **Start the pipeline**
```bash
docker-compose up -d
```

3. **Verify services**
```bash
docker ps
```

4. **Access services**
- **Airflow UI**: http://localhost:8080
- **PostgreSQL**: localhost:5432 (pe_user/pe_pass)
- **PowerBI**: Connect to localhost:5432

### **Connect PowerBI**
```
Server: localhost
Port: 5432
Database: pe_data
Username: pe_user
Password: pe_pass
Schema: analytics
```

## 📊 **Data Models**

### **Staging Models (dbt)**
- `stg_organizations` - Cleaned organization data
- `stg_networks` - Network data with ASN classification
- `stg_internet_exchanges` - IX data with geographic info
- `stg_network_ixlan_connections` - Peering connection data
- `stg_facilities` - Facility data with utilization metrics

### **Mart Models (dbt)**
- `mart_network_peering_summary` - Network analytics
- `mart_ix_traffic_summary` - IX performance metrics
- `mart_geographic_analytics` - Geographic distribution
- `mart_facility_analytics` - Facility utilization analysis

## 🔧 **Development**

### **Project Structure**
```
├── airflow/
│   ├── dags/                    # Airflow DAGs
│   ├── Dockerfile              # Airflow container
│   └── requirements.txt        # Python dependencies
├── dbt/
│   ├── models/
│   │   ├── staging/           # Staging models
│   │   └── marts/             # Mart models
│   ├── profiles/              # dbt profiles
│   └── Dockerfile             # dbt container
├── postgres/
│   └── init.sql               # Database schema
├── powerbi/
│   ├── README.md              # PowerBI setup guide
│   └── *.sql                  # Test queries
├── scripts/
│   ├── *.py                   # Data ingestion scripts
│   └── *.ps1                  # Setup scripts
├── docker-compose.yml         # Service orchestration
├── README.md                  # This file
├── USER_GUIDE.md              # User documentation
└── MAINTENANCE_GUIDE.md       # Technical maintenance
```

### **Adding New Data Sources**
1. Update `postgres/init.sql` with new schema
2. Create Airflow DAG for data ingestion
3. Add dbt staging and mart models
4. Create PowerBI visualizations
5. Update documentation

## 📚 **Documentation**

- **[User Guide](USER_GUIDE.md)** - Business user documentation
- **[Maintenance Guide](MAINTENANCE_GUIDE.md)** - Technical maintenance
- **[PowerBI Setup](powerbi/README.md)** - Dashboard configuration

## 🎯 **Key Learnings & Skills Demonstrated**

### **Data Engineering**
- **ETL Pipeline Design** - End-to-end data processing
- **Data Orchestration** - Airflow DAG management
- **Data Modeling** - dbt transformations and testing
- **Containerization** - Docker multi-service architecture

### **Analytics & Visualization**
- **Business Intelligence** - PowerBI dashboard development
- **Data Analysis** - SQL queries and aggregations
- **Performance Optimization** - Efficient data transformations
- **User Experience** - Intuitive dashboard design

### **DevOps & Operations**
- **Infrastructure as Code** - Docker Compose configuration
- **Monitoring** - Service health checks and logging
- **Documentation** - Comprehensive user and technical guides
- **Version Control** - Git repository management

## 🔍 **Technical Highlights**

- **Scalable Architecture** - Microservices with Docker
- **Data Quality** - dbt tests and validation
- **Automated Refresh** - 6-hour data pipeline cycles
- **Real-time Analytics** - Live PowerBI dashboards
- **Production Ready** - Comprehensive error handling

## 📈 **Future Enhancements**

- [ ] **Real-time Streaming** - Apache Kafka integration
- [ ] **Cloud Deployment** - AWS/Azure infrastructure
- [ ] **Machine Learning** - Predictive analytics models
- [ ] **API Development** - REST API for data access
- [ ] **Monitoring** - Grafana dashboards for pipeline health

## 🤝 **Contributing**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**Your Name**
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/yourprofile)
- GitHub: [@yourusername](https://github.com/yourusername)
- Portfolio: [Your Portfolio](https://yourportfolio.com)

## 🙏 **Acknowledgments**

- PeeringDB for providing the data API
- Apache Airflow community for orchestration tools
- dbt Labs for data transformation framework
- Microsoft PowerBI for visualization platform

---

⭐ **If you found this project helpful, please give it a star!**