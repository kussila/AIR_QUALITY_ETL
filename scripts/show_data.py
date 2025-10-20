# scripts/show_data.py
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()
engine = create_engine(os.getenv("DATABASE_URL"), future=True)

with engine.connect() as conn:
    rows = conn.execute(text("""
        SELECT id, city, date, pm25, pm10, co, no2, so2, o3
        FROM air_quality
        ORDER BY id DESC
        LIMIT 10
    """)).fetchall()

    for row in rows:
        print(row)
