
#!/usr/bin/env python3
"""
Network data ingestion script for PeeringDB analytics pipeline.
Fetches network data from PeeringDB API and stores it in PostgreSQL.
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
        logging.FileHandler('/opt/airflow/logs/ingest_networks.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def fetch_networks():
    """
    Fetch network data from PeeringDB API.
    Returns a list of network dictionaries.
    """
    logger.info("Starting network data fetch from PeeringDB API")
    all_data = []
    skip = 0
    limit = 100
    max_records = 1000

    while len(all_data) < max_records:
        url = "https://www.peeringdb.com/api/net"
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

            # Filter for networks with valid data
            filtered_batch = [
                net for net in batch 
                if net.get("asn") and net.get("name")
            ]
            all_data.extend(filtered_batch)
            
            logger.info(f"Fetched {len(filtered_batch)} networks (total: {len(all_data)})")
            
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

    logger.info(f"Successfully fetched {len(all_data)} networks")
    return all_data

def insert_into_postgres(networks):
    """
    Insert network data into PostgreSQL database.
    """
    logger.info(f"Starting database insert for {len(networks)} networks")
    
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
        for network in networks:
            try:
                # Validate organization reference
                org_id = network.get("org_id")
                if org_id:
                    cur.execute("SELECT org_id FROM organizations WHERE org_id = %s", (org_id,))
                    if not cur.fetchone():
                        logger.warning(f"Organization {org_id} not found, setting to NULL")
                        org_id = None
                
                cur.execute("""
                    INSERT INTO networks (network_id, name, asn, country, website, org_id)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    ON CONFLICT (network_id) DO UPDATE SET
                        name = EXCLUDED.name,
                        asn = EXCLUDED.asn,
                        country = EXCLUDED.country,
                        website = EXCLUDED.website,
                        org_id = EXCLUDED.org_id;
                """, (
                    network["id"],
                    network["name"],
                    network["asn"],
                    network.get("country", ""),
                    network.get("website", ""),
                    org_id
                ))
                inserted_count += 1
                
            except Exception as e:
                logger.error(f"Failed to insert network {network.get('id', 'unknown')}: {e}")

        conn.commit()
        cur.close()
        conn.close()
        
        logger.info(f"Successfully inserted {inserted_count} networks into database")
        
    except psycopg2.Error as e:
        logger.error(f"Database error: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected database error: {e}")
        raise

if __name__ == "__main__":
    start_time = datetime.now()
    logger.info("Network ingestion script started")
    
    try:
        networks = fetch_networks()
        if networks:
            insert_into_postgres(networks)
            logger.info(f"Network ingestion completed successfully. Processed {len(networks)} networks.")
        else:
            logger.warning("No networks fetched from API")
    except Exception as e:
        logger.error(f"Script failed: {e}")
        raise
    
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    logger.info(f"Script execution completed in {duration:.2f} seconds")