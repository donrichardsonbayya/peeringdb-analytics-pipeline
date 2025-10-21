-- Staging model for networks data
-- This model cleans and standardizes network data

{{ config(materialized='view') }}

select
    network_id,
    name,
    asn,
    country,
    website,
    org_id,
    created_at,
    updated_at,
    -- Add data quality checks and derived fields
    case 
        when name is null or name = '' then 'AS' || asn::text
        else name 
    end as clean_name,
    case 
        when country is null or country = '' then 'Unknown'
        else country 
    end as clean_country,
    -- Add ASN classification
    case 
        when asn >= 1 and asn <= 1023 then 'Reserved'
        when asn >= 1024 and asn <= 65535 then '16-bit'
        when asn >= 65536 and asn <= 4294967295 then '32-bit'
        else 'Invalid'
    end as asn_type
from {{ source('raw', 'networks') }}
