#!/usr/bin/env python3
"""
Organization data ingestion script for PeeringDB analytics pipeline.
Fetches organization data from PeeringDB API and stores it in PostgreSQL.
"""

import logging
import requests
import psycopg2
import time
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/opt/airflow/logs/ingest_org.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_organizations():
    """
    Fetch organization data from PeeringDB API.
    Returns a list of organization dictionaries.
    """
    logger.info("Starting organization data fetch from PeeringDB API")
    all_data = []
    skip = 0
    limit = 100
    max_records = 500

    while len(all_data) < max_records:
        url = "https://www.peeringdb.com/api/org"
        params = {"limit": limit, "skip": skip}
        
        try:
            # Handle rate limiting with retry logic
            retry_count = 0
            while retry_count < 3:
                response = requests.get(url, params=params, timeout=30)
                
                if response.status_code == 429:
                    logger.warning(f"Rate limit hit. Retrying in 5 seconds... (attempt {retry_count + 1})")
                    time.sleep(5)
                    retry_count += 1
                    continue
                
                response.raise_for_status()
                break
            
            if retry_count >= 3:
                logger.error("Max retries exceeded for API request")
                break
                
            batch = response.json().get("data", [])
            if not batch:
                logger.info("No more data available from API")
                break

            # Filter for organizations with valid data
            filtered_batch = [
                org for org in batch 
                if org.get("name") and len(org.get("name", "")) > 2
            ]
            all_data.extend(filtered_batch)
            
            logger.info(f"Fetched {len(filtered_batch)} organizations (total: {len(all_data)})")
            
            if len(all_data) >= max_records:
                all_data = all_data[:max_records]
                break
                
            skip += limit
            time.sleep(0.5)  # Be respectful to the API
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            break
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            break

    logger.info(f"Successfully fetched {len(all_data)} organizations")
    return all_data

def insert_into_postgres(organizations):
    """
    Insert organization data into PostgreSQL database.
    """
    logger.info(f"Starting database insert for {len(organizations)} organizations")
    
    try:
        conn = psycopg2.connect(
            host="postgres",
            port=5432,
            database="pe_data",
            user="pe_user",
            password="pe_pass"
        )
        cur = conn.cursor()

        inserted_count = 0
        for org in organizations:
            try:
                cur.execute("""
                    INSERT INTO organizations (org_id, name, website, city, country, region_continent, address1, address2, zipcode, state, phone, email)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (org_id) DO UPDATE SET
                        name = EXCLUDED.name,
                        website = EXCLUDED.website,
                        city = EXCLUDED.city,
                        country = EXCLUDED.country,
                        region_continent = EXCLUDED.region_continent,
                        address1 = EXCLUDED.address1,
                        address2 = EXCLUDED.address2,
                        zipcode = EXCLUDED.zipcode,
                        state = EXCLUDED.state,
                        phone = EXCLUDED.phone,
                        email = EXCLUDED.email;
                """, (
                    org["id"],
                    org["name"],
                    org.get("website", ""),
                    org.get("city", ""),
                    org.get("country", ""),
                    org.get("region_continent", ""),
                    org.get("address1", ""),
                    org.get("address2", ""),
                    org.get("zipcode", ""),
                    org.get("state", ""),
                    org.get("phone", ""),
                    org.get("email", "")
                ))
                inserted_count += 1
                
            except Exception as e:
                logger.error(f"Failed to insert organization {org.get('id', 'unknown')}: {e}")

        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"Successfully inserted {inserted_count} organizations into database")
        
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        raise

if __name__ == "__main__":
    start_time = datetime.now()
    logger.info("Organization ingestion script started")
    
    try:
        organizations = fetch_organizations()
        if organizations:
            insert_into_postgres(organizations)
            logger.info(f"Organization ingestion completed successfully. Processed {len(organizations)} organizations.")
        else:
            logger.warning("No organizations fetched from API")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"Script execution completed in {duration:.2f} seconds")
