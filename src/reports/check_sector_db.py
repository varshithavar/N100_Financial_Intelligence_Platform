import sqlite3
import pandas as pd

DB = "database/nifty100.db"

conn = sqlite3.connect(DB)

print("\n--- Sector Table ---")
print(
    pd.read_sql(
        "SELECT * FROM sector;",
        conn
    )
)


print("\n--- Companies Sector Values ---")
print(
    pd.read_sql(
        """
        SELECT company_id, company_name, sector
        FROM companies
        LIMIT 20;
        """,
        conn
    )
)


print("\n--- Financial Ratios Count ---")
print(
    pd.read_sql(
        """
        SELECT COUNT(*) AS count
        FROM financial_ratios;
        """,
        conn
    )
)


conn.close()