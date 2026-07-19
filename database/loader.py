import sqlite3
from pathlib import Path
import pandas as pd


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Database path
DATABASE = BASE_DIR / "database" / "nifty100.db"

# Raw Excel files path
RAW_DATA = BASE_DIR / "data" / "raw"


def create_database():
    """
    Create/connect SQLite database
    """

    DATABASE.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DATABASE)

    conn.execute("PRAGMA foreign_keys = ON;")

    print("Database connected successfully")

    return conn


def load_excel(conn, file_name, table_name):
    """
    Load Excel file into SQLite table
    """

    file_path = RAW_DATA / file_name

    if not file_path.exists():
        print(f"File not found: {file_path}")
        return


    df = pd.read_excel(file_path)

    print("\nLoading:", file_name)
    print("Rows:", len(df))


    df.to_sql(
        table_name,
        conn,
        if_exists="replace",
        index=False
    )


    print("Loaded table:", table_name)


def main():

    conn = create_database()


    load_excel(
        conn,
        "companies.xlsx",
        "companies"
    )


    load_excel(
        conn,
        "profitandloss.xlsx",
        "profit_loss"
    )


    load_excel(
        conn,
        "balancesheet.xlsx",
        "balance_sheet"
    )


    load_excel(
        conn,
        "cashflow.xlsx",
        "cash_flow"
    )


    conn.commit()
    conn.close()


    print("\nData loading completed!")
    print("Database:", DATABASE)


if __name__ == "__main__":
    main()