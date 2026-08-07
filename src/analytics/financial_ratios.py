import sqlite3
import pandas as pd
from pathlib import Path

# ==========================
# DATABASE CONNECTION
# ==========================

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "nifty100.db"

conn = sqlite3.connect(DB_PATH)

# ==========================
# LOAD TABLES
# ==========================

profit = pd.read_sql(
    "SELECT * FROM profit_loss",
    conn
)

balance = pd.read_sql(
    "SELECT * FROM balance_sheet",
    conn
)

cash = pd.read_sql(
    "SELECT * FROM cash_flow",
    conn
)

# ==========================
# DEBUG
# ==========================

print("\nProfit Data Types")
print(profit.dtypes)

print("\nBalance Data Types")
print(balance.dtypes)

print("\nCash Flow Data Types")
print(cash.dtypes)

# ==========================
# CLEAN YEAR
# ==========================

profit["financial_year"] = (
    profit["financial_year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

balance["financial_year"] = (
    balance["financial_year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

balance["financial_year"] = pd.to_numeric(
    balance["financial_year"],
    errors="coerce"
)

balance = balance.dropna(subset=["financial_year"])
balance["financial_year"] = balance["financial_year"].astype(int)

# ==========================
# ENSURE TYPES MATCH
# ==========================

profit["company_id"] = profit["company_id"].astype(int)
balance["company_id"] = balance["company_id"].astype(int)
cash["company_id"] = cash["company_id"].astype(int)

# Extract only the year (e.g. "Mar 2022" -> 2022)
profit["financial_year"] = (
    profit["financial_year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

# Convert to numeric
profit["financial_year"] = pd.to_numeric(
    profit["financial_year"],
    errors="coerce"
)

# Remove rows where year is missing
profit = profit.dropna(subset=["financial_year"])

# Convert profit year
profit["financial_year"] = pd.to_numeric(
    profit["financial_year"],
    errors="coerce"
)
profit = profit.dropna(subset=["financial_year"])
profit["financial_year"] = profit["financial_year"].astype(int)

# Convert balance year
balance["financial_year"] = pd.to_numeric(
    balance["financial_year"],
    errors="coerce"
)
balance = balance.dropna(subset=["financial_year"])
balance["financial_year"] = balance["financial_year"].astype(int)

# Convert cash year
cash["financial_year"] = (
    cash["financial_year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

cash["financial_year"] = pd.to_numeric(
    cash["financial_year"],
    errors="coerce"
)

cash = cash.dropna(subset=["financial_year"])
cash["financial_year"] = cash["financial_year"].astype(int)

print("\nProfit Years:", sorted(profit["financial_year"].unique())[:10])
print("Balance Years:", sorted(balance["financial_year"].unique())[:10])
print("Cash Years:", sorted(cash["financial_year"].unique())[:10])

print("\nProfit Years:", sorted(profit["financial_year"].unique())[:10])
print("Balance Years:", sorted(balance["financial_year"].unique())[:10])
print("Cash Years:", sorted(cash["financial_year"].unique())[:10])

print("\nProfit Rows:", len(profit))
print("Balance Rows:", len(balance))
print("Cash Rows:", len(cash))

# ==========================
# MERGE
# ==========================

df = profit.merge(
    balance,
    on=["company_id", "financial_year"],
    how="inner"
)

df = df.merge(
    cash,
    on=["company_id", "financial_year"],
    how="inner"
)

print("\nMerged Rows:", len(df))

# ==========================
# CALCULATE RATIOS
# ==========================

df["net_profit_margin_pct"] = (
    df["net_profit"] / df["revenue"]
) * 100

df["return_on_equity_pct"] = (
    df["net_profit"] / df["total_equity"]
) * 100

df["debt_to_equity"] = (
    df["total_debt"] / df["total_equity"]
)

df["asset_turnover"] = (
    df["revenue"] / df["total_assets"]
)

# free_cash_flow already exists in cash_flow table

ratios = df[
    [
        "company_id",
        "financial_year",
        "net_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "asset_turnover",
        "free_cash_flow"
    ]
]

# ==========================
# SAVE
# ==========================

ratios.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

print("\nFinancial Ratios Generated Successfully")
print(ratios.head())
print("Rows:", len(ratios))

conn.close()