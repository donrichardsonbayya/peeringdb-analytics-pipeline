import requests
import psycopg2
import time

def fetch_us_europe_facilities():
    """
    Fetch US and European facilities from PeeringDB API (portfolio optimized).
    Focus on major facilities with substantial presence.
    """
    all_data = []
    skip = 0
    limit = 50  # Increased batch size
    max_records = 150  # Reduced for faster portfolio execution
    # Target countries: US and major European countries
    target_countries = {"US", "DE", "GB", "FR", "NL", "IT", "ES", "CH", "AT", "BE", "SE", "NO", "DK", "FI"}

    while len(all_data) < max_records:
        url = "https://www.peeringdb.com/api/fac"
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
            
        raw = response.json().get("data", [])
        if not raw:
            break
            
        # Filter for US and European facilities with substantial presence
        filtered_data = [
            f for f in raw 
            if (f.get("country") in target_countries and
                f.get("name") and
                len(f.get("name", "")) > 3)
        ]
        all_data.extend(filtered_data)
        
        if len(all_data) >= max_records:
            all_data = all_data[:max_records]
            break
            
        skip += limit
        time.sleep(0.5)  # Reduced delay
        print(f"Fetched {len(all_data)} US and European facilities so far...")

    return all_data



def insert_into_postgres(facilities):
    conn = psycopg2.connect(
        host="postgres",
        port=5432,
        database="pe_data",
        user="pe_user",
        password="pe_pass"
    )
    cur = conn.cursor()

    for f in facilities:
        cur.execute("""
            INSERT INTO asset_facilities (facility_id, name, city, country, website)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (facility_id) DO NOTHING;
        """, (
            f["id"],
            f["name"],
            f["city"],
            f["country"],
            f.get("website", "")
        ))

    conn.commit()
    cur.close()
    conn.close()


if __name__ == "__main__":
    us_europe_facilities = fetch_us_europe_facilities()
    insert_into_postgres(us_europe_facilities)
    print(f"Inserted {len(us_europe_facilities)} US and European facilities successfully.")
