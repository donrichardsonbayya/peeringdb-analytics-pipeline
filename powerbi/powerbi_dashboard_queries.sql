-- PowerBI Dashboard Queries for PeeringDB Analytics
-- Copy and paste these into PowerBI Desktop's Advanced Query Editor

-- ==============================================
-- DASHBOARD 1: NETWORK OVERVIEW
-- ==============================================
SELECT 
    network_name,
    org_name,
    network_country,
    total_peering_connections,
    total_ixs_connected,
    total_bandwidth_mbps,
    peering_tier,
    bandwidth_tier,
    ix_presence_tier,
    route_server_connections,
    dual_stack_connections
FROM analytics.mart_network_peering_summary
WHERE total_peering_connections > 0
ORDER BY total_peering_connections DESC;

-- ==============================================
-- DASHBOARD 2: INTERNET EXCHANGE ANALYTICS
-- ==============================================
SELECT 
    ix_name,
    ix_country,
    ix_region,
    city,
    connected_networks,
    total_connections,
    total_bandwidth_mbps,
    avg_connection_speed_mbps,
    ix_size_tier,
    bandwidth_tier,
    network_diversity_tier,
    avg_connections_per_network,
    route_server_connections,
    dual_stack_connections
FROM analytics.mart_ix_traffic_summary
ORDER BY total_connections DESC;

-- ==============================================
-- DASHBOARD 3: GEOGRAPHIC ANALYSIS
-- ==============================================
SELECT 
    country,
    region,
    total_networks,
    total_organizations,
    total_ixs,
    total_facilities,
    total_peering_connections,
    total_bandwidth_mbps,
    market_size_tier,
    bandwidth_tier,
    avg_networks_per_ix,
    avg_connections_per_network
FROM analytics.mart_geographic_analytics
ORDER BY total_networks DESC;

-- ==============================================
-- DASHBOARD 4: FACILITY ANALYTICS
-- ==============================================
SELECT 
    facility_name,
    facility_country,
    city,
    networks_present,
    organizations_present,
    peering_connections,
    total_bandwidth_mbps,
    facility_size_tier,
    bandwidth_tier,
    avg_networks_per_org,
    avg_connections_per_network
FROM analytics.mart_facility_analytics
WHERE networks_present > 0
ORDER BY networks_present DESC;

-- ==============================================
-- SUMMARY KPI QUERIES
-- ==============================================

-- KPI 1: Total Networks by Peering Tier
SELECT 
    peering_tier,
    COUNT(*) as network_count,
    SUM(total_peering_connections) as total_connections,
    SUM(total_bandwidth_mbps) as total_bandwidth
FROM analytics.mart_network_peering_summary
GROUP BY peering_tier
ORDER BY network_count DESC;

-- KPI 2: IX Size Distribution
SELECT 
    ix_size_tier,
    COUNT(*) as ix_count,
    SUM(total_connections) as total_connections,
    SUM(total_bandwidth_mbps) as total_bandwidth
FROM analytics.mart_ix_traffic_summary
GROUP BY ix_size_tier
ORDER BY ix_count DESC;

-- KPI 3: Geographic Market Analysis
SELECT 
    region,
    COUNT(*) as country_count,
    SUM(total_networks) as total_networks,
    SUM(total_organizations) as total_organizations,
    SUM(total_ixs) as total_ixs
FROM analytics.mart_geographic_analytics
GROUP BY region
ORDER BY total_networks DESC;

-- KPI 4: Facility Size Distribution
SELECT 
    facility_size_tier,
    COUNT(*) as facility_count,
    SUM(networks_present) as total_networks,
    SUM(organizations_present) as total_organizations
FROM analytics.mart_facility_analytics
GROUP BY facility_size_tier
ORDER BY facility_count DESC;
