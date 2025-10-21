import requests
import psycopg2
import time

def fetch_org():
    """
    Fetch top organizations from PeeringDB API (portfolio optimized).
    Focus on major ISPs, cloud providers, and large enterprises.
    """
    all_data = []
    skip = 0
    limit = 50  # Increased batch size for faster processing
    max_records = 25  # Ultra-fast portfolio execution

    while len(all_data) < max_records:
        url = "https://www.peeringdb.com/api/org"
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

        # Filter for major organizations (those with websites and substantial presence)
        filtered_batch = [org for org in batch if org.get("website") and len(org.get("name", "")) > 3]
        all_data.extend(filtered_batch)
        
        if len(all_data) >= max_records:
            all_data = all_data[:max_records]
            break
            
        skip += limit
        time.sleep(0.5)  # Reduced delay for faster processing
        print(f"Fetched {len(all_data)} organizations so far...")

    return all_data


def insert_into_postgres(org_list):
    """
    Insert Organization data into PostgreSQL database.
    """
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="pe_data",
        user="pe_user",
        password="pe_pass"
    )
    cur = conn.cursor()

    for org in org_list:
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

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    org_data = fetch_org()
    insert_into_postgres(org_data)
    print(f"Inserted {len(org_data)} Organizations successfully.")
