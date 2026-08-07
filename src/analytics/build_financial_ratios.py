import sqlite3
from pathlib import Path

# ----------------------------------------------------
# Project Paths
# ----------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "nifty100.db"


def calculate_ratios():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ----------------------------------------------------
    # Recreate financial_ratios table
    # ----------------------------------------------------

    cur.execute("DROP TABLE IF EXISTS financial_ratios")

    cur.execute("""
    CREATE TABLE financial_ratios (
        ratio_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        financial_year TEXT,

        net_profit_margin_pct REAL,
        return_on_equity_pct REAL,
        debt_to_equity REAL,
        asset_turnover REAL,

        free_cash_flow REAL,
        cash_from_operations REAL,
        total_debt REAL
    )
    """)

    # ----------------------------------------------------
    # Read source tables
    # ----------------------------------------------------

    query = """
    SELECT
        p.company_id,
        p.financial_year,
        p.revenue,
        p.net_profit,

        b.total_assets,
        b.total_debt,
        b.total_equity,

        c.cash_from_operations,
        c.free_cash_flow

    FROM profit_loss p

    LEFT JOIN balance_sheet b
        ON p.company_id = b.company_id
        AND substr(p.financial_year,-4) = CAST(b.financial_year AS TEXT)

    LEFT JOIN cash_flow c
        ON p.company_id = c.company_id
        AND substr(p.financial_year,-4) = CAST(c.financial_year AS TEXT)

    ORDER BY p.company_id, p.financial_year
    """

    rows = cur.execute(query).fetchall()

    inserted = 0

    for row in rows:

        (
            company_id,
            financial_year,
            revenue,
            net_profit,
            total_assets,
            total_debt,
            total_equity,
            cash_from_operations,
            free_cash_flow
        ) = row


        # -----------------------------
        # Net Profit Margin
        # -----------------------------

        if revenue not in (None, 0):
            net_profit_margin = (net_profit / revenue) * 100
        else:
            net_profit_margin = None


        # -----------------------------
        # Return on Equity
        # -----------------------------

        if total_equity not in (None, 0):
            roe = (net_profit / total_equity) * 100
        else:
            roe = None


        # -----------------------------
        # Debt to Equity
        # -----------------------------

        if total_equity not in (None, 0) and total_debt is not None:
            debt_equity = total_debt / total_equity
        else:
            debt_equity = None


        # -----------------------------
        # Asset Turnover
        # -----------------------------

        if total_assets not in (None, 0):
            asset_turnover = revenue / total_assets
        else:
            asset_turnover = None


        # ⭐ FIX START
        # -----------------------------
        # Handle Missing Free Cash Flow
        # -----------------------------

        if free_cash_flow is None:
            free_cash_flow = cash_from_operations

        # If both are missing, store 0
        # prevents NLP comparison errors
        if free_cash_flow is None:
            free_cash_flow = 0

        # ⭐ FIX END


        # -----------------------------
        # Insert
        # -----------------------------

        cur.execute("""
        INSERT INTO financial_ratios(
            company_id,
            financial_year,
            net_profit_margin_pct,
            return_on_equity_pct,
            debt_to_equity,
            asset_turnover,
            free_cash_flow,
            cash_from_operations,
            total_debt
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            company_id,
            financial_year,
            net_profit_margin,
            roe,
            debt_equity,
            asset_turnover,
            free_cash_flow,
            cash_from_operations,
            total_debt
        ))

        inserted += 1


    conn.commit()

    print("=" * 50)
    print("Financial Ratio Build Completed")
    print("=" * 50)
    print(f"Rows Inserted : {inserted}")

    conn.close()


if __name__ == "__main__":
    calculate_ratios()