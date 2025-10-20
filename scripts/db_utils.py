# scripts/db_utils.py
# Helper utilities to get a SQLAlchemy engine and initialize the DB schema.

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()


def get_engine():
    """Return a SQLAlchemy engine connected to the database from .env."""
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL not found in .env")
    return create_engine(DATABASE_URL, future=True)


def init_db():
    """
    Create the air_quality table if it does not exist.
    This function creates its own engine so it can be called without parameters.
    """
    engine = get_engine()
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
    with engine.connect() as conn:
        conn.execute(text(create_table_sql))
        conn.commit()
