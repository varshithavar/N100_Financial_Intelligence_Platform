import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DB_PATH = BASE_DIR / "database" / "nifty100.db"


def calculate_ratios():

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    # Clear existing data
    cur.execute("DELETE FROM financial_ratios")


    query = """
    SELECT
        p.company_id,
        p.year,
        p.sales,
        p.net_profit,

        b.assets,
        b.liabilities,

        c.operating_cashflow

    FROM profit_loss p

    LEFT JOIN balance_sheet b
        ON p.company_id = b.company_id
        AND p.year = b.year

    LEFT JOIN cash_flow c
        ON p.company_id = c.company_id
        AND p.year = c.year
    """


    rows = cur.execute(query).fetchall()


    inserted = 0


    for row in rows:

        (
            company_id,
            year,
            sales,
            net_profit,
            assets,
            liabilities,
            operating_cashflow

        ) = row


        # Net Profit Margin

        net_profit_margin = None

        if sales and sales != 0:
            net_profit_margin = (net_profit / sales) * 100



        # ROE approximation
        # equity = assets - liabilities

        equity = None

        if assets is not None and liabilities is not None:
            equity = assets - liabilities


        roe = None

        if equity and equity != 0:
            roe = (net_profit / equity) * 100



        # Debt to Equity

        debt_to_equity = None

        if equity and equity != 0:
            debt_to_equity = liabilities / equity



        # Asset Turnover

        asset_turnover = None

        if assets and assets != 0:
            asset_turnover = sales / assets



        # Free Cash Flow
        # Only CFO available currently

        free_cash_flow = operating_cashflow



        # Insert KPI values

        cur.execute(
            """
            INSERT INTO financial_ratios
            (
                company_id,
                year,
                net_profit_margin_pct,
                return_on_equity_pct,
                debt_to_equity,
                asset_turnover,
                free_cash_flow_cr,
                cash_from_operations_cr,
                total_debt_cr
            )

            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)

            """,

            (
                company_id,
                year,
                net_profit_margin,
                roe,
                debt_to_equity,
                asset_turnover,
                free_cash_flow,
                operating_cashflow,
                liabilities
            )
        )


        inserted += 1



    conn.commit()
    conn.close()


    print(f"Inserted rows: {inserted}")



if __name__ == "__main__":
    calculate_ratios()