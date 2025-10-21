-- Staging model for organizations data
-- This model cleans and standardizes organization data

{{ config(materialized='view') }}

select
    org_id,
    name,
    website,
    city,
    country,
    region_continent,
    address1,
    address2,
    zipcode,
    state,
    phone,
    email,
    created_at,
    updated_at,
    -- Add data quality checks
    case 
        when name is null or name = '' then 'Unknown'
        else name 
    end as clean_name,
    case 
        when country is null or country = '' then 'Unknown'
        else country 
    end as clean_country,
    case 
        when region_continent is null or region_continent = '' then 'Unknown'
        else region_continent 
    end as clean_region
from {{ source('raw', 'organizations') }}
