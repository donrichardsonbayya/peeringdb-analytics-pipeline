import requests
import psycopg2
import time

def fetch_ix():
    """
    Fetch major Internet Exchanges from PeeringDB API (portfolio optimized).
    Focus on top-tier IXs like Equinix, DE-CIX, LINX, etc.
    """
    all_data = []
    skip = 0
    limit = 50
    max_records = 50  # Reduced for faster portfolio execution

    while len(all_data) < max_records:
        url = "https://www.peeringdb.com/api/ix"
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

        # Filter for major IXs (those with websites and substantial presence)
        target_countries = {"US", "DE", "GB", "FR", "NL", "IT", "ES", "CH", "AT", "BE", "SE", "NO", "DK", "FI"}
        filtered_batch = [
            ix for ix in batch 
            if (ix.get("website") and 
                ix.get("country") in target_countries and
                len(ix.get("name", "")) > 3)
        ]
        all_data.extend(filtered_batch)
        
        if len(all_data) >= max_records:
            all_data = all_data[:max_records]
            break
            
        skip += limit
        time.sleep(0.5)
        print(f"Fetched {len(all_data)} IXs so far...")

    return all_data


def insert_into_postgres(ix_list):
    """
    Insert IX data into PostgreSQL database.
    """
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="pe_data",
        user="pe_user",
        password="pe_pass"
    )
    cur = conn.cursor()

    for ix in ix_list:
        cur.execute("""
            INSERT INTO internet_exchanges (ix_id, name, city, country, region_continent, website, tech_email, policy_email)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ix_id) DO UPDATE SET
                name = EXCLUDED.name,
                city = EXCLUDED.city,
                country = EXCLUDED.country,
                region_continent = EXCLUDED.region_continent,
                website = EXCLUDED.website,
                tech_email = EXCLUDED.tech_email,
                policy_email = EXCLUDED.policy_email;
        """, (
            ix["id"],
            ix["name"],
            ix.get("city", ""),
            ix.get("country", ""),
            ix.get("region_continent", ""),
            ix.get("website", ""),
            ix.get("tech_email", ""),
            ix.get("policy_email", "")
        ))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    ix_data = fetch_ix()
    insert_into_postgres(ix_data)
    print(f"Inserted {len(ix_data)} Internet Exchanges successfully.")
