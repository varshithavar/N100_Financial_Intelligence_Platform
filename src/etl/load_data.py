import sqlite3
import pandas as pd
from pathlib import Path


# ==========================
# PATH CONFIG
# ==========================

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_PATH = BASE_DIR / "data" / "raw"

DB_PATH = BASE_DIR / "database" / "nifty100.db"


# ==========================
# CONNECT DATABASE
# ==========================

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()


# ==========================
# CREATE TABLES
# ==========================

cursor.executescript("""

DROP TABLE IF EXISTS companies;
DROP TABLE IF EXISTS profit_loss;
DROP TABLE IF EXISTS balance_sheet;
DROP TABLE IF EXISTS cash_flow;
DROP TABLE IF EXISTS ratios;
DROP TABLE IF EXISTS sector;

CREATE TABLE companies
(
    company_id INTEGER PRIMARY KEY,
    symbol TEXT,
    company_name TEXT,
    website TEXT,
    roe_percentage REAL,
    roce_percentage REAL,
    sector TEXT,
    industry TEXT
);


CREATE TABLE profit_loss
(
    pl_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    financial_year TEXT,
    revenue REAL,
    net_profit REAL,
    eps REAL
);


CREATE TABLE balance_sheet
(
    bs_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    financial_year TEXT,

    total_assets REAL,
    total_debt REAL,
    total_equity REAL,

    equity_capital REAL,
    reserves REAL
);

CREATE TABLE cash_flow
(
    cf_id INTEGER PRIMARY KEY,
    company_id INTEGER,
    financial_year TEXT,
    cash_from_operations REAL,
    capital_expenditure REAL,
    free_cash_flow REAL
);


CREATE TABLE sector
(
    sector_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sector_name TEXT
);


""")

conn.commit()

print("Database schema created")



# ==========================
# LOAD COMPANIES
# ==========================


companies = pd.read_excel(
    RAW_PATH / "companies.xlsx",
    header=1
)

print("\nCompanies Columns")
print(companies.columns.tolist())

companies_new = pd.DataFrame()

# Integer IDs for SQLite
companies_new["company_id"] = range(1, len(companies) + 1)

# Original stock symbol (ABB, TCS, INFY...)
companies_new["symbol"] = companies["id"].astype(str)

companies_new["company_name"] = companies["company_name"]
companies_new["website"] = companies["website"]
companies_new["roe_percentage"] = companies["roe_percentage"]
companies_new["roce_percentage"] = companies["roce_percentage"]

companies_new["sector"] = None
companies_new["industry"] = None

companies_new.to_sql(
    "companies",
    conn,
    if_exists="append",
    index=False
)

print(
    "Companies Loaded:",
    len(companies_new)
)



# ==========================
# LOAD PROFIT LOSS
# ==========================

pl = pd.read_excel(
    RAW_PATH / "profitandloss.xlsx",
    header=1
)

print("\nProfit Loss Columns")
print(pl.columns.tolist())

pl = pl.rename(
    columns={
        "id": "pl_id",
        "year": "financial_year",
        "sales": "revenue"
    }
)

# Map stock symbols (ABB, TCS...) to numeric company IDs
company_map = dict(
    zip(
        companies_new["symbol"].astype(str).str.strip().str.upper(),
        companies_new["company_id"]
    )
)

pl["company_id"] = (
    pl["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
    .map(company_map)
)

# Remove rows that couldn't be mapped
pl = pl.dropna(subset=["company_id"])

# Convert to integer
pl["company_id"] = pl["company_id"].astype(int)

pl = pl[
    [
        "pl_id",
        "company_id",
        "financial_year",
        "revenue",
        "net_profit",
        "eps"
    ]
]

pl.to_sql(
    "profit_loss",
    conn,
    if_exists="append",
    index=False
)

print(
    "Profit Loss Loaded:",
    len(pl)
)


# ==========================
# LOAD BALANCE SHEET
# ==========================
bs = pd.read_excel(
    RAW_PATH / "balancesheet.xlsx",
    header=1
)

print("\nBalance Sheet Columns")
print(bs.columns.tolist())

bs = bs.rename(
    columns={
        "id": "bs_id",
        "year": "financial_year",
        "borrowings": "total_debt"
    }
)

# Company Symbol -> Numeric ID
company_map = dict(
    zip(
        companies_new["symbol"].astype(str).str.strip().str.upper(),
        companies_new["company_id"]
    )
)

bs["company_id"] = (
    bs["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
    .map(company_map)
)

bs = bs.dropna(subset=["company_id"])

bs["company_id"] = bs["company_id"].astype(int)

bs["financial_year"] = (
    bs["financial_year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

bs["financial_year"] = pd.to_numeric(
    bs["financial_year"],
    errors="coerce"
)

bs["total_equity"] = (
    bs["equity_capital"].fillna(0)
    + bs["reserves"].fillna(0)
)

bs = bs[
    [
        "bs_id",
        "company_id",
        "financial_year",
        "total_assets",
        "total_debt",
        "total_equity",
        "equity_capital",
        "reserves"
    ]
]

bs.to_sql(
    "balance_sheet",
    conn,
    if_exists="append",
    index=False
)

print("Balance Sheet Loaded:", len(bs))


# ==========================
# LOAD CASH FLOW
# ==========================

cf = pd.read_excel(
    RAW_PATH / "cashflow.xlsx",
    header=1
)

print("\nCash Flow Columns")
print(cf.columns.tolist())

cf = cf.rename(
    columns={
        "id": "cf_id",
        "year": "financial_year",
        "operating_activity": "cash_from_operations",
        "investing_activity": "capital_expenditure"
    }
)

cf["company_id"] = (
    cf["company_id"]
    .astype(str)
    .str.strip()
    .str.upper()
    .map(company_map)
)

cf = cf.dropna(subset=["company_id"])

cf["company_id"] = cf["company_id"].astype(int)

cf["financial_year"] = (
    cf["financial_year"]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

cf["financial_year"] = pd.to_numeric(
    cf["financial_year"],
    errors="coerce"
)

cf["free_cash_flow"] = (
    cf["cash_from_operations"].fillna(0)
    + cf["capital_expenditure"].fillna(0)
)

cf = cf[
    [
        "cf_id",
        "company_id",
        "financial_year",
        "cash_from_operations",
        "capital_expenditure",
        "free_cash_flow"
    ]
]

cf.to_sql(
    "cash_flow",
    conn,
    if_exists="append",
    index=False
)

print("Cash Flow Loaded:", len(cf))


# ==========================
# LOAD SECTOR
# ==========================


sector_data = pd.DataFrame(
    {
        "sector_name":
        [
            "IT",
            "Energy",
            "Banking",
            "Finance",
            "Healthcare",
            "Automobile",
            "Consumer"
        ]
    }
)


sector_data.to_sql(
    "sector",
    conn,
    if_exists="append",
    index=False
)


print(
    "Sector Loaded:",
    len(sector_data)
)



# ==========================
# VALIDATION
# ==========================


print("\nValidation")


tables = [
    "companies",
    "profit_loss",
    "balance_sheet",
    "cash_flow",
    "sector"
]


for table in tables:

    count = conn.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(
        table,
        ":",
        count
    )


conn.close()


print(
    "\nFULL DATA LOAD COMPLETED SUCCESSFULLY"
)