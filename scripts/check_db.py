# scripts/check_db.py
from sqlalchemy import create_engine, inspect, text
from dotenv import load_dotenv
import os

# Load .env to get the database URL
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, future=True)
inspector = inspect(engine)

# Print available tables
print("Tables:", inspector.get_table_names())

# Count rows in air_quality table
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM air_quality"))
    count = result.scalar()
    print(f"Rows in air_quality: {count}")
