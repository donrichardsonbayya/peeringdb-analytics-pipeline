-- Staging model for network-IX LAN connections
-- This model cleans and standardizes peering connection data

{{ config(materialized='view') }}

select
    netixlan_id,
    net_id,
    ixlan_id,
    ipaddr4,
    ipaddr6,
    speed,
    asn,
    is_rs_peer,
    notes,
    operational,
    created_at,
    updated_at,
    -- Add data quality checks and derived fields
    case 
        when speed is null or speed <= 0 then 0
        else speed 
    end as clean_speed,
    case 
        when operational is null then false
        else operational 
    end as is_operational,
    -- Add IP version classification
    case 
        when ipaddr4 is not null and ipaddr6 is not null then 'Dual Stack'
        when ipaddr4 is not null then 'IPv4 Only'
        when ipaddr6 is not null then 'IPv6 Only'
        else 'No IP'
    end as ip_version_type,
    -- Add speed tier classification
    case 
        when speed >= 100000 then '100G+'
        when speed >= 10000 then '10G+'
        when speed >= 1000 then '1G+'
        when speed >= 100 then '100M+'
        when speed > 0 then 'Sub-100M'
        else 'Unknown'
    end as speed_tier
from {{ source('raw', 'network_ixlan_connections') }}
