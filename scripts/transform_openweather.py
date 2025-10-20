# scripts/transform_openweather.py
# This script reads the raw air quality data from OpenWeatherMap,
# cleans and formats it, and saves it as a new "clean" CSV file.

import pandas as pd
import os

# Input (raw) and output (cleaned) file paths
RAW = "data/raw_openweather.csv"
CLEAN = "data/clean_openweather.csv"

def transform():
    # 1 Check if the raw file exists
    if not os.path.exists(RAW):
        raise FileNotFoundError(f"{RAW} not found. Run extract_openweather.py first.")

    # 2 Read the raw CSV file into a pandas DataFrame
    df = pd.read_csv(RAW)

    # 3 Convert the timestamp (Unix time in seconds) to a human-readable date
    df['date'] = pd.to_datetime(df['dt'], unit='s').dt.strftime('%Y-%m-%d %H:%M:%S')

    # 4 Ensure all expected columns exist, even if missing in the raw data
    for col in ["pm2_5", "pm10", "co", "no", "no2", "o3", "so2", "nh3", "aqi"]:
        if col not in df.columns:
            df[col] = None

    # 5 Select and reorder columns for consistency
    df = df[["city","lat","lon","date","aqi","pm2_5","pm10","co","no","no2","o3","so2","nh3"]]

    # 6 Rename the 'pm2_5' column to 'pm25' (simpler name)
    df = df.rename(columns={"pm2_5": "pm25"})

    # 7 Ensure output directory exists
    os.makedirs("data", exist_ok=True)

    # 8 Save cleaned data to CSV (no index column)
    df.to_csv(CLEAN, index=False)

    # 9 Print confirmation with number of rows saved
    print(f"✅ Saved cleaned file to {CLEAN} ({len(df)} rows)")
    return df

# When running this file directly (not importing), execute the transform function
if __name__ == "__main__":
    transform()
