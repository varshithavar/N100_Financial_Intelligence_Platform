import sqlite3
import pandas as pd

conn = sqlite3.connect("database/nifty100.db")

df = pd.read_sql(
    """
    SELECT company_id, company_name
    FROM companies
    WHERE sector IS NULL;
    """,
    conn
)

print(df.to_string(index=False))

print("\nMissing Count:", len(df))

conn.close()