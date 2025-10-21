-- Mart model: Geographic Analytics
-- This model provides geographic distribution analytics

{{ config(materialized='table') }}

with geographic_stats as (
    select
        coalesce(n.clean_country, 'Unknown') as country,
        coalesce(o.clean_region, 'Unknown') as region,
        count(distinct n.network_id) as total_networks,
        count(distinct o.org_id) as total_organizations,
        count(distinct ix.ix_id) as total_ixs,
        count(distinct f.facility_id) as total_facilities,
        count(distinct nic.netixlan_id) as total_peering_connections,
        sum(nic.clean_speed) as total_bandwidth_mbps,
        avg(nic.clean_speed) as avg_connection_speed_mbps,
        count(case when nic.is_rs_peer then 1 end) as route_server_connections,
        count(case when nic.ip_version_type = 'Dual Stack' then 1 end) as dual_stack_connections
    from {{ ref('stg_networks') }} n
    left join {{ ref('stg_organizations') }} o on n.org_id = o.org_id
    left join {{ ref('stg_network_ixlan_connections') }} nic on n.network_id = nic.net_id
    left join {{ ref('stg_internet_exchanges') }} ix on nic.net_id = ix.ix_id
    left join {{ ref('stg_facilities') }} f on f.facility_id = n.network_id  -- This might need adjustment based on actual relationships
    where nic.is_operational = true or nic.is_operational is null
    group by coalesce(n.clean_country, 'Unknown'), coalesce(o.clean_region, 'Unknown')
)

select
    *,
    -- Add derived metrics
    case 
        when total_networks >= 1000 then 'Major Market'
        when total_networks >= 500 then 'Large Market'
        when total_networks >= 100 then 'Medium Market'
        when total_networks >= 50 then 'Small Market'
        else 'Micro Market'
    end as market_size_tier,
    case 
        when total_bandwidth_mbps >= 1000000 then '1T+'
        when total_bandwidth_mbps >= 100000 then '100G+'
        when total_bandwidth_mbps >= 10000 then '10G+'
        when total_bandwidth_mbps >= 1000 then '1G+'
        else 'Sub-1G'
    end as bandwidth_tier,
    -- Calculate network density per IX
    case 
        when total_ixs > 0 then round(total_networks::numeric / total_ixs, 2)
        else 0
    end as avg_networks_per_ix,
    -- Calculate connection density per network
    case 
        when total_networks > 0 then round(total_peering_connections::numeric / total_networks, 2)
        else 0
    end as avg_connections_per_network
from geographic_stats
order by total_networks desc
