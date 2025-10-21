-- Staging model for facilities data
-- This model cleans and standardizes facility data

{{ config(materialized='view') }}

select
    facility_id,
    name,
    city,
    country,
    website,
    created_at,
    updated_at,
    -- Add data quality checks
    case 
        when name is null or name = '' then 'Unknown Facility'
        else name 
    end as clean_name,
    case 
        when country is null or country = '' then 'Unknown'
        else country 
    end as clean_country
from {{ source('raw', 'asset_facilities') }}
