-- Mart model: Facility Analytics
-- This model provides facility and colocation analytics

{{ config(materialized='table') }}

with facility_stats as (
    select
        f.facility_id,
        f.clean_name as facility_name,
        f.clean_country as facility_country,
        f.city,
        f.website,
        count(distinct fnm.network_id) as networks_present,
        count(distinct n.org_id) as organizations_present,
        count(distinct nic.netixlan_id) as peering_connections,
        sum(nic.clean_speed) as total_bandwidth_mbps,
        avg(nic.clean_speed) as avg_connection_speed_mbps,
        count(case when nic.is_rs_peer then 1 end) as route_server_connections,
        count(case when nic.ip_version_type = 'Dual Stack' then 1 end) as dual_stack_connections,
        max(nic.created_at) as last_connection_added,
        min(nic.created_at) as first_connection_added
    from {{ ref('stg_facilities') }} f
    left join {{ source('raw', 'facility_network_map') }} fnm on f.facility_id = fnm.facility_id
    left join {{ ref('stg_networks') }} n on fnm.network_id = n.network_id
    left join {{ ref('stg_network_ixlan_connections') }} nic on n.network_id = nic.net_id
    where nic.is_operational = true or nic.is_operational is null
    group by f.facility_id, f.clean_name, f.clean_country, f.city, f.website
)

select
    *,
    -- Add derived metrics
    case 
        when networks_present >= 100 then 'Mega Facility'
        when networks_present >= 50 then 'Major Facility'
        when networks_present >= 20 then 'Large Facility'
        when networks_present >= 10 then 'Medium Facility'
        when networks_present >= 5 then 'Small Facility'
        else 'Micro Facility'
    end as facility_size_tier,
    case 
        when total_bandwidth_mbps >= 1000000 then '1T+'
        when total_bandwidth_mbps >= 100000 then '100G+'
        when total_bandwidth_mbps >= 10000 then '10G+'
        when total_bandwidth_mbps >= 1000 then '1G+'
        else 'Sub-1G'
    end as bandwidth_tier,
    -- Calculate network density per organization
    case 
        when organizations_present > 0 then round(networks_present::numeric / organizations_present, 2)
        else 0
    end as avg_networks_per_org,
    -- Calculate connection density per network
    case 
        when networks_present > 0 then round(peering_connections::numeric / networks_present, 2)
        else 0
    end as avg_connections_per_network
from facility_stats
order by networks_present desc
