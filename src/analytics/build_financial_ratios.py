import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "nifty100.db"


def calculate_ratios():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # ----------------------------------------------------
    # Create financial_ratios table if it doesn't exist
    # ----------------------------------------------------
    cur.execute("""
    CREATE TABLE IF NOT EXISTS financial_ratios (
        ratio_id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_id INTEGER,
        financial_year TEXT,

        net_profit_margin_pct REAL,
        return_on_equity_pct REAL,
        debt_to_equity REAL,
        asset_turnover REAL,

        free_cash_flow REAL,
        cash_from_operations REAL,
        total_debt REAL,

        FOREIGN KEY(company_id) REFERENCES companies(company_id)
    )
    """)

    # Clear previous data
    cur.execute("DELETE FROM financial_ratios")

    # ----------------------------------------------------
    # Read data from existing tables
    # ----------------------------------------------------
    query = """
    SELECT
        p.company_id,
        p.financial_year,
        p.revenue,
        p.net_profit,

        b.total_assets,
        b.total_liabilities,
        b.equity,

        c.operating_cf

    FROM profit_loss p

    LEFT JOIN balance_sheet b
        ON p.company_id = b.company_id
        AND p.financial_year = b.financial_year

    LEFT JOIN cash_flow c
        ON p.company_id = c.company_id
        AND p.financial_year = c.financial_year
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
            total_liabilities,
            equity,
            operating_cf
        ) = row

        # -----------------------------
        # Net Profit Margin
        # -----------------------------
        if revenue and revenue != 0:
            net_profit_margin = (net_profit / revenue) * 100
        else:
            net_profit_margin = None

        # -----------------------------
        # ROE
        # -----------------------------
        if equity and equity != 0:
            roe = (net_profit / equity) * 100
        else:
            roe = None

        # -----------------------------
        # Debt to Equity
        # -----------------------------
        if equity and equity != 0:
            debt_equity = total_liabilities / equity
        else:
            debt_equity = None

        # -----------------------------
        # Asset Turnover
        # -----------------------------
        if total_assets and total_assets != 0:
            asset_turnover = revenue / total_assets
        else:
            asset_turnover = None

        # -----------------------------
        # Free Cash Flow
        # (Using Operating CF for now)
        # -----------------------------
        free_cash_flow = operating_cf

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
            operating_cf,
            total_liabilities
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