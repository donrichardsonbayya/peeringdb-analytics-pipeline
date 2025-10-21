-- Staging model for internet exchanges data
-- This model cleans and standardizes IX data

{{ config(materialized='view') }}

select
    ix_id,
    name,
    city,
    country,
    region_continent,
    website,
    tech_email,
    policy_email,
    created_at,
    updated_at,
    -- Add data quality checks
    case 
        when name is null or name = '' then 'Unknown IX'
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
from {{ source('raw', 'internet_exchanges') }}
