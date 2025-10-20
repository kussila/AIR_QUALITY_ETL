# scripts/init_db.py

# Import SQLAlchemy for database connection & execution
from sqlalchemy import create_engine, text
# Import dotenv to load environment variables (like DATABASE_URL)
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Retrieve the database URL (e.g., sqlite:///data/air_quality.db)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create a SQLAlchemy engine using that URL
engine = create_engine(DATABASE_URL, future=True)

# Define SQL command to create the air_quality table if it doesn’t exist yet
create_table_sql = """
CREATE TABLE IF NOT EXISTS air_quality (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  city TEXT,
  country TEXT,
  date TEXT,
  pm25 REAL,
  pm10 REAL,
  co REAL,
  no2 REAL,
  so2 REAL,
  o3 REAL
);
"""

# Connect to the database and execute the CREATE TABLE statement
with engine.connect() as conn:
    conn.execute(text(create_table_sql))
    conn.commit()

# Print confirmation message once done
print("✅ DB initialized at:", DATABASE_URL)
