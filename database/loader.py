import sqlite3
from pathlib import Path

# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Correct database location
DATABASE = BASE_DIR / "data" / "db" / "financial_intelligence.db"

# Correct schema location
SCHEMA = BASE_DIR / "sql" / "schema.sql"


def create_database():
    # Create database folder if it doesn't exist
    DATABASE.parent.mkdir(parents=True, exist_ok=True)

    # Connect to SQLite
    conn = sqlite3.connect(DATABASE)

    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")

    # Read and execute schema.sql
    with open(SCHEMA, "r", encoding="utf-8") as file:
        conn.executescript(file.read())

    conn.commit()
    conn.close()

    print("Database created successfully!")
    print(f"Database: {DATABASE}")


if __name__ == "__main__":
    create_database()