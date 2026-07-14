import sqlite3
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parents[2]

# Database path
DB_PATH = BASE_DIR / "database" / "nifty100.db"

# SQL schema file
SCHEMA_PATH = BASE_DIR / "sql" / "schema.sql"


def create_database():
    """Create SQLite database and execute schema."""

    # Create database folder if it doesn't exist
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite
    conn = sqlite3.connect(DB_PATH)

    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")

    # Execute schema.sql if it exists
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH, "r", encoding="utf-8") as file:
            conn.executescript(file.read())
        print("Schema created successfully.")
    else:
        print("schema.sql not found.")
        print("Expected location:", SCHEMA_PATH)

    conn.commit()
    conn.close()

    print("\nDatabase created successfully.")
    print("Database file:", DB_PATH)


if __name__ == "__main__":
    create_database()