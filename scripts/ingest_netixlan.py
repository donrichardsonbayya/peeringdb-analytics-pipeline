import requests
import psycopg2
import time

def fetch_netixlan():
    """
    Fetch Network-IX LAN connection data from PeeringDB API (portfolio optimized).
    Focus on connections to major IXs only for faster processing.
    """
    all_data = []
    skip = 0
    limit = 50
    max_records = 100  # Ultra-fast portfolio execution

    while len(all_data) < max_records:
        url = "https://www.peeringdb.com/api/netixlan"
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

        # Filter for operational connections with reasonable speeds
        filtered_batch = [
            conn for conn in batch 
            if (conn.get("operational", True) and 
                conn.get("speed", 0) >= 1000)  # Focus on 1Gbps+ connections
        ]
        all_data.extend(filtered_batch)
        
        if len(all_data) >= max_records:
            all_data = all_data[:max_records]
            break
            
        skip += limit
        time.sleep(0.5)
        print(f"Fetched {len(all_data)} network-IX connections so far...")

    return all_data


def insert_into_postgres(netixlan_list):
    """
    Insert Network-IX LAN connection data into PostgreSQL database.
    """
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="pe_data",
        user="pe_user",
        password="pe_pass"
    )
    cur = conn.cursor()

    for netixlan in netixlan_list:
        # Only insert if both network and IX LAN exist
        cur.execute("""
            INSERT INTO network_ixlan_connections (netixlan_id, net_id, ixlan_id, ipaddr4, ipaddr6, speed, asn, is_rs_peer, notes, operational)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            WHERE EXISTS (SELECT 1 FROM networks WHERE network_id = %s)
            AND EXISTS (SELECT 1 FROM ix_lans WHERE ixlan_id = %s)
            ON CONFLICT (netixlan_id) DO UPDATE SET
                net_id = EXCLUDED.net_id,
                ixlan_id = EXCLUDED.ixlan_id,
                ipaddr4 = EXCLUDED.ipaddr4,
                ipaddr6 = EXCLUDED.ipaddr6,
                speed = EXCLUDED.speed,
                asn = EXCLUDED.asn,
                is_rs_peer = EXCLUDED.is_rs_peer,
                notes = EXCLUDED.notes,
                operational = EXCLUDED.operational;
        """, (
            netixlan["id"],
            netixlan["net_id"],
            netixlan["ixlan_id"],
            netixlan.get("ipaddr4", ""),
            netixlan.get("ipaddr6", ""),
            netixlan.get("speed", 0),
            netixlan.get("asn", 0),
            netixlan.get("is_rs_peer", False),
            netixlan.get("notes", ""),
            netixlan.get("operational", True),
            netixlan["net_id"],
            netixlan["ixlan_id"]
        ))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    netixlan_data = fetch_netixlan()
    insert_into_postgres(netixlan_data)
    print(f"Inserted {len(netixlan_data)} Network-IX LAN connections successfully.")
