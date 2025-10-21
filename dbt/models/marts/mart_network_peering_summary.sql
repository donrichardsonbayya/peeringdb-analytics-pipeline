-- Mart model: Network Peering Summary
-- This model provides a comprehensive view of network peering activities

{{ config(materialized='table') }}

with network_peering_stats as (
    select
        n.network_id,
        n.asn,
        n.clean_name as network_name,
        n.clean_country as network_country,
        n.asn_type,
        o.clean_name as org_name,
        o.clean_country as org_country,
        o.clean_region as org_region,
        count(distinct nic.ixlan_id) as total_ixs_connected,
        count(nic.netixlan_id) as total_peering_connections,
        sum(nic.clean_speed) as total_bandwidth_mbps,
        avg(nic.clean_speed) as avg_connection_speed_mbps,
        count(case when nic.is_rs_peer then 1 end) as route_server_connections,
        count(case when nic.ip_version_type = 'Dual Stack' then 1 end) as dual_stack_connections,
        count(case when nic.ip_version_type = 'IPv4 Only' then 1 end) as ipv4_only_connections,
        count(case when nic.ip_version_type = 'IPv6 Only' then 1 end) as ipv6_only_connections,
        max(nic.created_at) as last_connection_added,
        min(nic.created_at) as first_connection_added
    from {{ ref('stg_networks') }} n
    left join {{ ref('stg_organizations') }} o on n.org_id = o.org_id
    left join {{ ref('stg_network_ixlan_connections') }} nic on n.network_id = nic.net_id
    where nic.is_operational = true or nic.is_operational is null
    group by n.network_id, n.asn, n.clean_name, n.clean_country, n.asn_type,
             o.clean_name, o.clean_country, o.clean_region
)

select
    *,
    -- Add derived metrics
    case 
        when total_peering_connections >= 100 then 'Heavy Peer'
        when total_peering_connections >= 20 then 'Active Peer'
        when total_peering_connections >= 5 then 'Moderate Peer'
        when total_peering_connections > 0 then 'Light Peer'
        else 'No Peering'
    end as peering_tier,
    case 
        when total_bandwidth_mbps >= 100000 then '100G+'
        when total_bandwidth_mbps >= 10000 then '10G+'
        when total_bandwidth_mbps >= 1000 then '1G+'
        when total_bandwidth_mbps >= 100 then '100M+'
        else 'Sub-100M'
    end as bandwidth_tier,
    case 
        when total_ixs_connected >= 20 then 'Global'
        when total_ixs_connected >= 10 then 'Regional'
        when total_ixs_connected >= 5 then 'Multi-IX'
        when total_ixs_connected > 0 then 'Single-IX'
        else 'No IX'
    end as ix_presence_tier
from network_peering_stats
