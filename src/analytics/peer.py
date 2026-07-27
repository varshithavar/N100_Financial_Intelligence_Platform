import sqlite3
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "nifty100.db"


def build_peer_percentiles():

    conn = sqlite3.connect(DB_PATH)

    # -----------------------------------------
    # Load company and ratio data
    # -----------------------------------------

    companies = pd.read_sql("""
        SELECT
            company_id,
            company_name,
            sector
        FROM companies
    """, conn)

    ratios = pd.read_sql("""
        SELECT
            company_id,
            return_on_equity_pct,
            net_profit_margin_pct,
            debt_to_equity,
            asset_turnover,
            free_cash_flow
        FROM financial_ratios
    """, conn)

    df = companies.merge(ratios, on="company_id", how="inner")

    # -----------------------------------------
    # Create peer_percentiles table
    # -----------------------------------------

    conn.execute("""
    CREATE TABLE IF NOT EXISTS peer_percentiles(

        peer_id INTEGER PRIMARY KEY AUTOINCREMENT,

        company_id INTEGER,
        company_name TEXT,
        sector TEXT,

        roe_percentile REAL,
        npm_percentile REAL,
        debt_equity_percentile REAL,
        asset_turnover_percentile REAL,
        free_cash_flow_percentile REAL

    )
    """)

    conn.execute("DELETE FROM peer_percentiles")

    # -----------------------------------------
    # Calculate Percentiles
    # -----------------------------------------

    result = []

    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "asset_turnover",
        "free_cash_flow"
    ]

    for sector, group in df.groupby("sector"):

        temp = group.copy()

        for metric in metrics:

            ascending = metric == "debt_to_equity"

            temp[metric + "_pct"] = (
                temp[metric]
                .rank(method="average",
                      pct=True,
                      ascending=ascending)
                * 100
            )

        result.append(temp)

    final = pd.concat(result)

    # -----------------------------------------
    # Save to SQLite
    # -----------------------------------------

    for _, row in final.iterrows():

        conn.execute("""
        INSERT INTO peer_percentiles(

            company_id,
            company_name,
            sector,

            roe_percentile,
            npm_percentile,
            debt_equity_percentile,
            asset_turnover_percentile,
            free_cash_flow_percentile

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (

            row.company_id,
            row.company_name,
            row.sector,

            row.return_on_equity_pct_pct,
            row.net_profit_margin_pct_pct,
            row.debt_to_equity_pct,
            row.asset_turnover_pct,
            row.free_cash_flow_pct

        ))

    conn.commit()

    print("=" * 50)
    print("Peer Percentiles Generated")
    print("=" * 50)
    print("Rows:", len(final))

    conn.close()


if __name__ == "__main__":
    build_peer_percentiles()