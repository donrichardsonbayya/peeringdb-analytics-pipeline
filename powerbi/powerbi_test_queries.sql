-- PowerBI Connection Test Queries
-- Use these queries to verify data availability for PowerBI dashboards

-- 1. Network Peering Summary - Top 10 Networks by Connections
SELECT 
    network_name,
    org_name,
    network_country,
    total_ixs_connected,
    total_peering_connections,
    total_bandwidth_mbps,
    peering_tier,
    bandwidth_tier
FROM analytics.mart_network_peering_summary
ORDER BY total_peering_connections DESC
LIMIT 10;

-- 2. Internet Exchange Traffic Summary - Top 10 IXs by Connections
SELECT 
    ix_name,
    ix_country,
    ix_region,
    connected_networks,
    total_connections,
    total_bandwidth_mbps,
    ix_size_tier,
    bandwidth_tier
FROM analytics.mart_ix_traffic_summary
ORDER BY total_connections DESC
LIMIT 10;

-- 3. Geographic Analytics - Top Countries by Network Count
SELECT 
    country,
    region,
    total_networks,
    total_organizations,
    total_ixs,
    total_facilities,
    market_size_tier,
    bandwidth_tier
FROM analytics.mart_geographic_analytics
ORDER BY total_networks DESC
LIMIT 15;

-- 4. Facility Analytics - Top Facilities by Network Count
SELECT 
    facility_name,
    facility_country,
    city,
    networks_present,
    organizations_present,
    total_bandwidth_mbps,
    facility_size_tier,
    bandwidth_tier
FROM analytics.mart_facility_analytics
ORDER BY networks_present DESC
LIMIT 10;

-- 5. Peering Tier Distribution
SELECT 
    peering_tier,
    COUNT(*) as network_count,
    SUM(total_peering_connections) as total_connections,
    SUM(total_bandwidth_mbps) as total_bandwidth
FROM analytics.mart_network_peering_summary
GROUP BY peering_tier
ORDER BY network_count DESC;

-- 6. IX Size Distribution
SELECT 
    ix_size_tier,
    COUNT(*) as ix_count,
    SUM(total_connections) as total_connections,
    SUM(total_bandwidth_mbps) as total_bandwidth
FROM analytics.mart_ix_traffic_summary
GROUP BY ix_size_tier
ORDER BY ix_count DESC;

-- 7. Geographic Market Analysis
SELECT 
    region,
    COUNT(*) as country_count,
    SUM(total_networks) as total_networks,
    SUM(total_organizations) as total_organizations,
    SUM(total_ixs) as total_ixs
FROM analytics.mart_geographic_analytics
GROUP BY region
ORDER BY total_networks DESC;

-- 8. Facility Size Distribution
SELECT 
    facility_size_tier,
    COUNT(*) as facility_count,
    SUM(networks_present) as total_networks,
    SUM(organizations_present) as total_organizations
FROM analytics.mart_facility_analytics
GROUP BY facility_size_tier
ORDER BY facility_count DESC;
