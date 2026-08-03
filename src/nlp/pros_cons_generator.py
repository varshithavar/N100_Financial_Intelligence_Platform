import sqlite3
import pandas as pd
from pathlib import Path

# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_FILE = PROJECT_ROOT / "database" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "pros_cons_generated.csv"
SUMMARY_FILE = OUTPUT_DIR / "company_summary.csv"


# -------------------------------------------------
# Connect Database
# -------------------------------------------------

conn = sqlite3.connect(DB_FILE)

print("Database connected successfully!")


# -------------------------------------------------
# Load Financial Ratios
# -------------------------------------------------

query = """
SELECT
    f.ratio_id,
    f.company_id,
    c.company_name,
    f.financial_year,
    f.net_profit_margin_pct,
    f.return_on_equity_pct,
    f.debt_to_equity,
    f.asset_turnover,
    f.free_cash_flow,
    f.cash_from_operations,
    f.total_debt,
    f.pe_ratio
FROM financial_ratios f
JOIN companies c
ON f.company_id = c.company_id
ORDER BY f.company_id, f.financial_year;
"""


df = pd.read_sql(query, conn)

print("\nFinancial Ratios Loaded")
print(df.head())

print("\nTotal Rows:", len(df))


# -------------------------------------------------
# Sort Data
# -------------------------------------------------

df = df.sort_values(
    by=["company_id", "financial_year"]
)


# -------------------------------------------------
# Generate Pros & Cons
# -------------------------------------------------

results = []


for company_id, company_df in df.groupby("company_id"):

    latest = company_df.iloc[-1]

    company_name = latest["company_name"]

    print(f"Processing {company_name}")


    # ---------------- PRO RULES ----------------


    if pd.notna(latest["return_on_equity_pct"]) and latest["return_on_equity_pct"] >= 20:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "pro",
            "rule_id": 1,
            "text": "High return on equity demonstrates strong capital efficiency.",
            "confidence_pct": 90
        })


    if pd.notna(latest["free_cash_flow"]) and latest["free_cash_flow"] > 0:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "pro",
            "rule_id": 2,
            "text": "Positive free cash flow indicates healthy cash generation.",
            "confidence_pct": 85
        })


    if pd.notna(latest["debt_to_equity"]) and latest["debt_to_equity"] == 0:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "pro",
            "rule_id": 3,
            "text": "Debt-free balance sheet reduces financial risk.",
            "confidence_pct": 95
        })


    if pd.notna(latest["net_profit_margin_pct"]) and latest["net_profit_margin_pct"] >= 15:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "pro",
            "rule_id": 4,
            "text": "High profit margin shows strong operational efficiency.",
            "confidence_pct": 88
        })


    if pd.notna(latest["asset_turnover"]) and latest["asset_turnover"] >= 1:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "pro",
            "rule_id": 5,
            "text": "Efficient asset utilization supports revenue growth.",
            "confidence_pct": 82
        })


    if pd.notna(latest["pe_ratio"]) and latest["pe_ratio"] <= 25:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "pro",
            "rule_id": 6,
            "text": "Low P/E ratio may indicate attractive valuation.",
            "confidence_pct": 82
        })


    if pd.notna(latest["cash_from_operations"]) and latest["cash_from_operations"] > 500:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "pro",
            "rule_id": 7,
            "text": "Strong operating cash flow supports sustainable growth.",
            "confidence_pct": 88
        })


    if pd.notna(latest["total_debt"]) and latest["total_debt"] < 2500:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "pro",
            "rule_id": 8,
            "text": "Low total debt improves financial stability.",
            "confidence_pct": 86
        })


    if pd.notna(latest["asset_turnover"]) and latest["asset_turnover"] >= 1.5:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "pro",
            "rule_id": 9,
            "text": "Strong asset turnover indicates efficient asset usage.",
            "confidence_pct": 84
        })


    # ---------------- CON RULES ----------------


    if pd.notna(latest["return_on_equity_pct"]) and latest["return_on_equity_pct"] < 10:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "con",
            "rule_id": 10,
            "text": "Low ROE indicates weak profitability.",
            "confidence_pct": 90
        })


    if pd.notna(latest["debt_to_equity"]) and latest["debt_to_equity"] > 2:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "con",
            "rule_id": 11,
            "text": "High debt-to-equity increases financial risk.",
            "confidence_pct": 90
        })


    if pd.notna(latest["pe_ratio"]) and latest["pe_ratio"] > 30:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "con",
            "rule_id": 12,
            "text": "High P/E ratio may indicate expensive valuation.",
            "confidence_pct": 84
        })


    if pd.notna(latest["cash_from_operations"]) and latest["cash_from_operations"] < 300:
        results.append({
            "company_id": company_id,
            "company_name": company_name,
            "type": "con",
            "rule_id": 13,
            "text": "Low operating cash flow may impact future growth.",
            "confidence_pct": 87
        })


# -------------------------------------------------
# Create Output DataFrame
# -------------------------------------------------

pros_cons_df = pd.DataFrame(results)


print("\nGenerated Pros & Cons")
print(pros_cons_df)


print("\nTotal Records:", len(pros_cons_df))


# -------------------------------------------------
# Company Summary
# -------------------------------------------------

summary = (
    pros_cons_df
    .groupby(
        ["company_id", "company_name", "type"]
    )
    .size()
    .unstack(fill_value=0)
    .reset_index()
)


summary.rename(
    columns={
        "pro": "total_pros",
        "con": "total_cons"
    },
    inplace=True
)


if "total_pros" not in summary:
    summary["total_pros"] = 0


if "total_cons" not in summary:
    summary["total_cons"] = 0



# -------------------------------------------------
# Save Files
# -------------------------------------------------

pros_cons_df.to_csv(
    OUTPUT_FILE,
    index=False
)


summary.to_csv(
    SUMMARY_FILE,
    index=False
)


print("\nPros & Cons Saved:")
print(OUTPUT_FILE)


print("\nCompany Summary Saved:")
print(SUMMARY_FILE)



# -------------------------------------------------
# Close Connection
# -------------------------------------------------

conn.close()

print("\nDatabase connection closed successfully!")