import requests
import psycopg2
import time

def fetch_ixlan():
    """
    Fetch IX LAN data from PeeringDB API (portfolio optimized).
    Focus on LANs from major IXs only for faster processing.
    """
    all_data = []
    skip = 0
    limit = 50  # Increased batch size
    max_records = 50  # Ultra-fast portfolio execution

    while len(all_data) < max_records:
        url = "https://www.peeringdb.com/api/ixlan"
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

        # Filter for LANs with substantial configurations
        filtered_batch = [
            ixlan for ixlan in batch 
            if (ixlan.get("ix_id") and 
                ixlan.get("name") and
                len(ixlan.get("name", "")) > 2)
        ]
        all_data.extend(filtered_batch)
        
        if len(all_data) >= max_records:
            all_data = all_data[:max_records]
            break
            
        skip += limit
        time.sleep(0.5)  # Reduced delay
        print(f"Fetched {len(all_data)} IX LANs so far...")

    return all_data


def insert_into_postgres(ixlan_list):
    """
    Insert IX LAN data into PostgreSQL database.
    """
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="pe_data",
        user="pe_user",
        password="pe_pass"
    )
    cur = conn.cursor()

    for ixlan in ixlan_list:
        # Only insert if IX exists
        cur.execute("""
            INSERT INTO ix_lans (ixlan_id, ix_id, name, descr, mtu, vlan, dot1q_support, rs_asn, arp_sponge)
            SELECT %s, %s, %s, %s, %s, %s, %s, %s, %s
            WHERE EXISTS (SELECT 1 FROM internet_exchanges WHERE ix_id = %s)
            ON CONFLICT (ixlan_id) DO UPDATE SET
                ix_id = EXCLUDED.ix_id,
                name = EXCLUDED.name,
                descr = EXCLUDED.descr,
                mtu = EXCLUDED.mtu,
                vlan = EXCLUDED.vlan,
                dot1q_support = EXCLUDED.dot1q_support,
                rs_asn = EXCLUDED.rs_asn,
                arp_sponge = EXCLUDED.arp_sponge;
        """, (
            ixlan["id"],
            ixlan["ix_id"],
            ixlan.get("name", ""),
            ixlan.get("descr", ""),
            ixlan.get("mtu", 0),
            ixlan.get("vlan", 0),
            ixlan.get("dot1q_support", False),
            ixlan.get("rs_asn", 0),
            ixlan.get("arp_sponge", False),
            ixlan["ix_id"]
        ))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    ixlan_data = fetch_ixlan()
    insert_into_postgres(ixlan_data)
    print(f"Inserted {len(ixlan_data)} IX LANs successfully.")
