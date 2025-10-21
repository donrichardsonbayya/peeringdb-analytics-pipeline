-- Mart model: Internet Exchange Traffic Summary
-- This model provides analytics on IX performance and connectivity

{{ config(materialized='table') }}

with ix_traffic_stats as (
    select
        ix.ix_id,
        ix.clean_name as ix_name,
        ix.clean_country as ix_country,
        ix.clean_region as ix_region,
        ix.city,
        ix.website,
        count(distinct nic.net_id) as connected_networks,
        count(nic.netixlan_id) as total_connections,
        sum(nic.clean_speed) as total_bandwidth_mbps,
        avg(nic.clean_speed) as avg_connection_speed_mbps,
        count(case when nic.is_rs_peer then 1 end) as route_server_connections,
        count(case when nic.ip_version_type = 'Dual Stack' then 1 end) as dual_stack_connections,
        count(case when nic.ip_version_type = 'IPv4 Only' then 1 end) as ipv4_only_connections,
        count(case when nic.ip_version_type = 'IPv6 Only' then 1 end) as ipv6_only_connections,
        count(case when nic.speed_tier = '100G+' then 1 end) as connections_100g_plus,
        count(case when nic.speed_tier = '10G+' then 1 end) as connections_10g_plus,
        count(case when nic.speed_tier = '1G+' then 1 end) as connections_1g_plus,
        max(nic.created_at) as last_connection_added,
        min(nic.created_at) as first_connection_added
    from {{ ref('stg_internet_exchanges') }} ix
    left join {{ ref('stg_network_ixlan_connections') }} nic on ix.ix_id = nic.net_id
    where nic.is_operational = true or nic.is_operational is null
    group by ix.ix_id, ix.clean_name, ix.clean_country, ix.clean_region, ix.city, ix.website
)

select
    *,
    -- Add derived metrics
    case 
        when total_connections >= 1000 then 'Mega IX'
        when total_connections >= 500 then 'Major IX'
        when total_connections >= 100 then 'Large IX'
        when total_connections >= 50 then 'Medium IX'
        when total_connections >= 10 then 'Small IX'
        else 'Micro IX'
    end as ix_size_tier,
    case 
        when total_bandwidth_mbps >= 1000000 then '1T+'
        when total_bandwidth_mbps >= 100000 then '100G+'
        when total_bandwidth_mbps >= 10000 then '10G+'
        when total_bandwidth_mbps >= 1000 then '1G+'
        else 'Sub-1G'
    end as bandwidth_tier,
    case 
        when connected_networks >= 500 then 'Global'
        when connected_networks >= 100 then 'Regional'
        when connected_networks >= 50 then 'Multi-Country'
        when connected_networks >= 10 then 'Country-Level'
        else 'Local'
    end as network_diversity_tier,
    -- Calculate connection density (connections per network)
    case 
        when connected_networks > 0 then round(total_connections::numeric / connected_networks, 2)
        else 0
    end as avg_connections_per_network
from ix_traffic_stats
