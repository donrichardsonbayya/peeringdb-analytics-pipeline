# PowerBI Connection Configuration for PeeringDB Analytics

## Database Connection Details
- **Server**: localhost:5433
- **Database**: pe_data
- **Username**: pe_user
- **Password**: pe_pass
- **Schema**: analytics (for dbt models)

## Key Tables for PowerBI Dashboards

### 1. Network Peering Summary (mart_network_peering_summary)
- **Purpose**: Network-level analytics and peering behavior
- **Key Metrics**: 
  - Total IXs connected
  - Total peering connections
  - Total bandwidth
  - Peering tier classification
  - Bandwidth tier classification

### 2. Internet Exchange Traffic Summary (mart_ix_traffic_summary)
- **Purpose**: IX performance and connectivity analytics
- **Key Metrics**:
  - Connected networks count
  - Total connections
  - Total bandwidth
  - IX size tier
  - Network diversity tier

### 3. Geographic Analytics (mart_geographic_analytics)
- **Purpose**: Geographic distribution of peering infrastructure
- **Key Metrics**:
  - Networks per country/region
  - Organizations per country/region
  - IXs per country/region
  - Market size tier

### 4. Facility Analytics (mart_facility_analytics)
- **Purpose**: Data center and colocation analytics
- **Key Metrics**:
  - Networks per facility
  - Organizations per facility
  - Facility size tier
  - Bandwidth capacity

## PowerBI Dashboard Recommendations

### Dashboard 1: Network Overview
- Network peering summary table
- Top networks by connections
- Bandwidth distribution chart
- Geographic network distribution map

### Dashboard 2: Internet Exchange Analytics
- IX traffic summary table
- Top IXs by connections
- IX size distribution
- Regional IX analysis

### Dashboard 3: Geographic Analysis
- Country-wise network distribution
- Regional market analysis
- Geographic bandwidth distribution
- Market size tier analysis

### Dashboard 4: Facility Analytics
- Facility network density
- Top facilities by network count
- Facility size distribution
- Colocation market analysis

## Connection String Template
```
Server=localhost,5433;Database=pe_data;User Id=pe_user;Password=pe_pass;Schema=analytics;
```

## Refresh Schedule
- **Recommended**: Every 6 hours (aligned with dbt DAG schedule)
- **Manual**: On-demand for real-time analysis
