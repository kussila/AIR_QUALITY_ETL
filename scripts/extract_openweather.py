# scripts/extract_openweather.py
import os, time, csv
import requests
import pandas as pd
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

BASE = os.getenv("OPENWEATHER_BASE")
API_KEY = os.getenv("OPENWEATHER_API_KEY")
OUTPATH = "data/raw_openweather.csv"

if not API_KEY:
    raise RuntimeError("OPENWEATHER_API_KEY missing in .env")

def fetch_for_coord(lat, lon):
    """Fetch air pollution data for one coordinate."""
    params = {"lat": lat, "lon": lon, "appid": API_KEY}
    r = requests.get(BASE, params=params, timeout=15)
    r.raise_for_status()
    return r.json()

def run(locations_csv="data/locations.csv"):
    """Loop through all cities in CSV and fetch data."""
    rows = []
    with open(locations_csv, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for rec in reader:
            city = rec['city']
            lat = rec['lat']
            lon = rec['lon']
            print(f"Fetching {city} ({lat},{lon}) ...")
            try:
                data = fetch_for_coord(lat, lon)
            except Exception as e:
                print("  Error:", e)
                continue
            for item in data.get("list", []):
                row = {
                    "city": city,
                    "lat": lat,
                    "lon": lon,
                    "aqi": item.get("main", {}).get("aqi"),
                    "pm2_5": item.get("components", {}).get("pm2_5"),
                    "pm10": item.get("components", {}).get("pm10"),
                    "co": item.get("components", {}).get("co"),
                    "no": item.get("components", {}).get("no"),
                    "no2": item.get("components", {}).get("no2"),
                    "o3": item.get("components", {}).get("o3"),
                    "so2": item.get("components", {}).get("so2"),
                    "nh3": item.get("components", {}).get("nh3"),
                    "dt": item.get("dt"),
                }
                rows.append(row)
            time.sleep(1)  # pause between API calls
    if not rows:
        print("No rows fetched.")
        return None
    df = pd.DataFrame(rows)
    os.makedirs("data", exist_ok=True)
    df.to_csv(OUTPATH, index=False)
    print(f"Saved {len(df)} rows to {OUTPATH}")
    return df

if __name__ == "__main__":
    run()
