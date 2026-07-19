import sqlite3


DB_PATH = "database/nifty100.db"


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS financial_ratios (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER,
    year INTEGER,

    net_profit_margin_pct REAL,
    operating_profit_margin_pct REAL,
    return_on_equity_pct REAL,
    return_on_assets_pct REAL,
    return_on_capital_employed_pct REAL,

    debt_to_equity REAL,
    high_leverage_flag INTEGER,

    interest_coverage REAL,
    icr_label TEXT,
    icr_warning_flag INTEGER,

    asset_turnover REAL,

    free_cash_flow_cr REAL,
    capex_cr REAL,

    earnings_per_share REAL,
    book_value_per_share REAL,

    dividend_payout_ratio_pct REAL,

    total_debt_cr REAL,
    cash_from_operations_cr REAL,

    revenue_cagr_5yr REAL,
    pat_cagr_5yr REAL,
    eps_cagr_5yr REAL,

    composite_quality_score REAL
);
""")


conn.commit()

print("financial_ratios table created successfully")

conn.close()