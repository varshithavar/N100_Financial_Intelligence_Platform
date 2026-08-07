import sqlite3
import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_FILE = PROJECT_ROOT / "database" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "pros_cons_generated.csv"
SUMMARY_FILE = OUTPUT_DIR / "company_summary.csv"


conn = sqlite3.connect(DB_FILE)

print("Database connected successfully!")


query = """
SELECT
    f.company_id,
    c.company_name,
    f.financial_year,
    f.net_profit_margin_pct,
    f.return_on_equity_pct,
    f.debt_to_equity,
    f.asset_turnover,
    f.free_cash_flow
FROM financial_ratios f
JOIN companies c
ON f.company_id = c.company_id
ORDER BY f.company_id, f.financial_year;
"""


df = pd.read_sql(query, conn)


print("\nFinancial Ratios Loaded")
print(df.head())

print("\nCompanies:", df["company_id"].nunique())


df = df.sort_values(
    ["company_id", "financial_year"]
)


results = []


for company_id, company_df in df.groupby("company_id"):

    latest = company_df.iloc[-1]

    company_name = latest["company_name"]

    print("Processing:", company_name)


    # ---------------- PRO RULES ----------------

    if latest["return_on_equity_pct"] >= 20:
        results.append([
            company_id,
            company_name,
            "pro",
            1,
            "Consistently high return on equity demonstrates capital efficiency.",
            90
        ])


    if latest["free_cash_flow"] > 0:
        results.append([
            company_id,
            company_name,
            "pro",
            2,
            "Positive free cash flow indicates healthy business fundamentals.",
            85
        ])


    if latest["debt_to_equity"] == 0:
        results.append([
            company_id,
            company_name,
            "pro",
            3,
            "Debt-free balance sheet provides financial flexibility.",
            95
        ])


    if latest["net_profit_margin_pct"] >= 15:
        results.append([
            company_id,
            company_name,
            "pro",
            4,
            "Strong profit margin indicates operational efficiency.",
            85
        ])


    if latest["asset_turnover"] >= 1:
        results.append([
            company_id,
            company_name,
            "pro",
            5,
            "Efficient asset utilisation supports business growth.",
            80
        ])


    # fallback pro

    company_pros = [
        x for x in results
        if x[0] == company_id and x[2] == "pro"
    ]

    if len(company_pros) == 0:
        results.append([
            company_id,
            company_name,
            "pro",
            99,
            "Stable financial indicators based on available metrics.",
            65
        ])


    # ---------------- CON RULES ----------------


    if latest["return_on_equity_pct"] < 10:
        results.append([
            company_id,
            company_name,
            "con",
            10,
            "Low ROE indicates weak profitability.",
            85
        ])


    if latest["debt_to_equity"] > 2:
        results.append([
            company_id,
            company_name,
            "con",
            11,
            "High debt-to-equity increases financial risk.",
            90
        ])


    if latest["net_profit_margin_pct"] < 5:
        results.append([
            company_id,
            company_name,
            "con",
            12,
            "Low profit margin indicates operational pressure.",
            80
        ])


    if latest["free_cash_flow"] < 0:
        results.append([
            company_id,
            company_name,
            "con",
            13,
            "Negative free cash flow requires monitoring.",
            85
        ])


    # fallback con

    company_cons = [
        x for x in results
        if x[0] == company_id and x[2] == "con"
    ]

    if len(company_cons) == 0:
        results.append([
            company_id,
            company_name,
            "con",
            99,
            "No major negative signal detected; continuous monitoring recommended.",
            65
        ])



pros_cons_df = pd.DataFrame(
    results,
    columns=[
        "company_id",
        "company_name",
        "type",
        "rule_id",
        "text",
        "confidence_pct"
    ]
)


pros_cons_df.to_csv(
    OUTPUT_FILE,
    index=False
)


summary = (
    pros_cons_df
    .groupby(["company_id","company_name","type"])
    .size()
    .unstack(fill_value=0)
    .reset_index()
)


summary.to_csv(
    SUMMARY_FILE,
    index=False
)


print("\nSaved:")
print(OUTPUT_FILE)

print(SUMMARY_FILE)


conn.close()

print("Database connection closed!")