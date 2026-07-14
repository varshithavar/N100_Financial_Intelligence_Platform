import sqlite3
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Database file
DB_PATH = BASE_DIR / "database" / "nifty100.db"

# SQL schema
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def create_database():
    # Create database folder
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite (creates nifty100.db if it doesn't exist)
    conn = sqlite3.connect(DB_PATH)

    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")

    # Run schema.sql
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        print("Schema created successfully.")
    else:
        print("schema.sql not found!")

    conn.commit()
    conn.close()

    print(f"Database created: {DB_PATH}")


if __name__ == "__main__":
    create_database()