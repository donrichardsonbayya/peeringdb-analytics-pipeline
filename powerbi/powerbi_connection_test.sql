-- PowerBI Connection Test Query
-- Run this in PowerBI Desktop's Advanced Query Editor to test the connection

-- Test 1: Basic connection test
SELECT 'Connection Successful!' as status, NOW() as timestamp;

-- Test 2: Check raw data availability
SELECT 
    'Raw Data Check' as test_type,
    (SELECT COUNT(*) FROM organizations) as organizations_count,
    (SELECT COUNT(*) FROM networks) as networks_count,
    (SELECT COUNT(*) FROM internet_exchanges) as ix_count;

-- Test 3: Check analytics data availability
SELECT 
    'Analytics Data Check' as test_type,
    (SELECT COUNT(*) FROM analytics.mart_network_peering_summary) as network_summary_count,
    (SELECT COUNT(*) FROM analytics.mart_ix_traffic_summary) as ix_summary_count,
    (SELECT COUNT(*) FROM analytics.mart_geographic_analytics) as geo_analytics_count,
    (SELECT COUNT(*) FROM analytics.mart_facility_analytics) as facility_analytics_count;

-- Test 4: Sample data from each analytics table
SELECT 'Sample Network Data' as table_name, * FROM analytics.mart_network_peering_summary LIMIT 3;
SELECT 'Sample IX Data' as table_name, * FROM analytics.mart_ix_traffic_summary LIMIT 3;
SELECT 'Sample Geographic Data' as table_name, * FROM analytics.mart_geographic_analytics LIMIT 3;
SELECT 'Sample Facility Data' as table_name, * FROM analytics.mart_facility_analytics LIMIT 3;
