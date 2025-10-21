
# pylint: disable=import-error
import requests
import psycopg2
import time

def fetch_networks():
    """
    Fetch top networks from PeeringDB API (portfolio optimized).
    Focus on major ASNs with significant traffic and presence.
    """
    all_data = []
    skip = 0
    limit = 10  # Smaller batches for faster processing
    max_records = 10  # Ultra-minimal for immediate portfolio results

    while len(all_data) < max_records:
        url = "https://www.peeringdb.com/api/net"
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

        # Filter for major networks (those with websites and substantial ASNs)
        filtered_batch = [
            net for net in batch 
            if (net.get("website") and 
                net.get("asn") and 
                net.get("asn") < 100000)  # Focus on established ASNs
        ]
        all_data.extend(filtered_batch)
        
        if len(all_data) >= max_records:
            all_data = all_data[:max_records]
            break
            
        skip += limit
        time.sleep(0.2)  # Minimal delay for ultra-fast execution
        print(f"Fetched {len(all_data)} networks so far...")

    return all_data



def insert_into_postgres(networks):
    conn = psycopg2.connect(
        host="postgres",
        port=5432,  # Adjust if you used a different port
        database="pe_data",
        user="pe_user",
        password="pe_pass"
    )
    cur = conn.cursor()

    for n in networks:
        # Insert network, set org_id to NULL if it doesn't exist in organizations table
        org_id = n.get("org_id")
        if org_id:
            # Check if org_id exists, if not set to NULL
            cur.execute("SELECT org_id FROM organizations WHERE org_id = %s", (org_id,))
            if not cur.fetchone():
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
            n["id"],
            n["name"],
            n["asn"],
            n.get("country", ""),
            n.get("website", ""),
            org_id
        ))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    networks = fetch_networks()
    insert_into_postgres(networks)
    print(f"Inserted {len(networks)} networks successfully.")
    print(f"Inserted {len(networks)} networks successfully.")