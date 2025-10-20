# scripts/load_openweather.py
# This script loads the cleaned CSV into the SQLite database.

import pandas as pd
import os
from sqlalchemy import text
from dotenv import load_dotenv

# Load environment variables (DATABASE_URL, etc.)
load_dotenv()

# Import helper functions from db_utils.py
from scripts.db_utils import get_engine, init_db

# File path for the cleaned CSV
CLEAN = "data/clean_openweather.csv"

def load():
    # 1 Check if the cleaned file exists
    if not os.path.exists(CLEAN):
        raise FileNotFoundError(f"{CLEAN} not found. Run transform_openweather.py first.")

    # 2 Make sure the database and table exist
    init_db()

    # 3 Read the cleaned CSV
    df = pd.read_csv(CLEAN)

    # 4 Create a database connection
    engine = get_engine()

    inserted = 0  # counter for number of rows inserted

    # 5 Open connection and insert each row
    with engine.connect() as conn:
        for _, row in df.iterrows():
            # SQL statement to insert one record
            stmt = text("""
                INSERT INTO air_quality (city, country, date, pm25, pm10, co, no2, so2, o3)
                VALUES (:city, :country, :date, :pm25, :pm10, :co, :no2, :so2, :o3)
            """)
            # Map Python variables to SQL query parameters
            params = {
                "city": row.get("city"),
                "country": None,  # could be filled later if available
                "date": row.get("date"),
                "pm25": row.get("pm25"),
                "pm10": row.get("pm10"),
                "co": row.get("co"),
                "no2": row.get("no2"),
                "so2": row.get("so2"),
                "o3": row.get("o3"),
            }

            # Execute the SQL insert for this row
            conn.execute(stmt, params)
            inserted += 1

        # 6️⃣ Commit changes to the database
        conn.commit()

    # 7️⃣ Print how many rows were inserted
    print(f"✅ Inserted {inserted} rows into DB")

# Run the load() function if script is executed directly
if __name__ == "__main__":
    load()
