# Architecture Overview

## System Architecture

```mermaid
graph TB
    subgraph "Data Sources"
        API[PeeringDB API]
    end
    
    subgraph "Orchestration Layer"
        AF[Apache Airflow]
        AF_SCHED[Airflow Scheduler]
        AF_WEB[Airflow Webserver]
    end
    
    subgraph "Data Storage"
        PG[(PostgreSQL)]
    end
    
    subgraph "Transformation Layer"
        DBT[dbt Core]
    end
    
    subgraph "Analytics Layer"
        PBI[PowerBI Desktop]
    end
    
    subgraph "Infrastructure"
        DOCKER[Docker Compose]
    end
    
    API --> AF
    AF_SCHED --> AF
    AF_WEB --> AF
    AF --> PG
    PG --> DBT
    DBT --> PG
    PG --> PBI
    
    DOCKER -.-> AF
    DOCKER -.-> PG
    DOCKER -.-> DBT
```

## Data Flow

1. **Data Ingestion**: Airflow DAGs fetch data from PeeringDB API every 6 hours
2. **Data Storage**: Raw data is stored in PostgreSQL tables
3. **Data Transformation**: dbt models clean, validate, and aggregate the data
4. **Analytics**: PowerBI connects to PostgreSQL to create interactive dashboards
5. **Monitoring**: Airflow provides pipeline monitoring and error handling

## Component Details

### Airflow
- **Scheduler**: Manages DAG execution timing
- **Webserver**: Provides web UI for monitoring
- **DAGs**: Define data ingestion workflows

### PostgreSQL
- **Raw Tables**: Store ingested data from PeeringDB
- **Analytics Schema**: Contains transformed data from dbt

### dbt
- **Staging Models**: Clean and standardize raw data
- **Mart Models**: Create business-ready analytics tables

### PowerBI
- **Dashboards**: Interactive visualizations
- **Data Models**: Connect to PostgreSQL analytics schema
