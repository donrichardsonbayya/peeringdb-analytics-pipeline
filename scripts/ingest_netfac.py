import requests
import psycopg2
import time

def fetch_netfac():
    """
    Fetch facility-network mapping data from PeeringDB API (portfolio optimized).
    Focus on major facility-network relationships for faster processing.
    """
    all_data = []
    skip = 0
    limit = 50  # Increased batch size
    max_records = 100  # Ultra-fast portfolio execution

    while len(all_data) < max_records:
        url = "https://www.peeringdb.com/api/netfac"
        params = {"limit": limit, "skip": skip}

        # Add rate limiting with retry logic
        while True:
            response = requests.get(url, params=params)
            if response.status_code == 429:
                print("Rate limit hit. Sleeping for 3 seconds...")
                time.sleep(3)
                continue
            response.raise_for_status()
            break

        batch = response.json().get("data", [])
        if not batch:
            break

        # Filter for valid facility-network mappings
        filtered_batch = [
            item for item in batch 
            if (item.get("fac_id") and 
                item.get("net_id") and
                item.get("fac_id") > 0 and
                item.get("net_id") > 0)
        ]
        all_data.extend(filtered_batch)
        
        if len(all_data) >= max_records:
            all_data = all_data[:max_records]
            break
            
        skip += limit
        time.sleep(0.5)  # Reduced delay
        print(f"Fetched {len(all_data)} facility-network mappings so far...")

    return all_data




def insert_into_postgres(netfac_list):
    conn = psycopg2.connect(
        host="postgres",
        port=5432,  
        database="pe_data",
        user="pe_user",
        password="pe_pass"
    )
    cur = conn.cursor()

    for item in netfac_list:
        # Only insert if both facility and network exist
        cur.execute("""
            INSERT INTO facility_network_map (facility_id, network_id)
            SELECT %s, %s
            WHERE EXISTS (SELECT 1 FROM asset_facilities WHERE facility_id = %s)
            AND EXISTS (SELECT 1 FROM networks WHERE network_id = %s)
            ON CONFLICT (facility_id, network_id) DO NOTHING;
        """, (
            item["fac_id"],
            item["net_id"],
            item["fac_id"],
            item["net_id"]
        ))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    netfac_data = fetch_netfac()
    insert_into_postgres(netfac_data)
    print(f"Inserted {len(netfac_data)} facility-network mappings successfully.")
