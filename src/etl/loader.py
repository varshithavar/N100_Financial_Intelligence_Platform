import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "database" / "nifty100.db"


def load_excel(file_path, table_name=None):
    """
    Load Excel file data.
    Returns dataframe when table_name is not provided.
    Loads into SQLite when table_name is provided.
    """

    df = pd.read_excel(file_path)

    if table_name is None:
        return df

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        table_name,
        conn,
        if_exists="append",
        index=False
    )

    conn.close()

    return len(df)