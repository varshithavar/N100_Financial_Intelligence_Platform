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

OUTPUT_FILE = OUTPUT_DIR / "capital_allocation.csv"


# -------------------------------------------------
# Connect Database
# -------------------------------------------------

conn = sqlite3.connect(DB_FILE)

print("Database connected successfully!")


# -------------------------------------------------
# Load Cash Flow Data
# -------------------------------------------------

query = """
SELECT
    f.company_id,
    c.company_name,
    f.cash_from_operations,
    f.free_cash_flow,
    f.total_debt
FROM financial_ratios f
JOIN companies c
ON f.company_id = c.company_id
ORDER BY f.company_id;
"""


df = pd.read_sql(query, conn)


print("\nCash Flow Data Loaded")
print(df.head())

print("\nTotal Companies:", len(df))


# -------------------------------------------------
# Cash Flow Intelligence Rules
# -------------------------------------------------

results = []


for _, row in df.iterrows():

    company_id = row["company_id"]
    company_name = row["company_name"]

    cfo = row["cash_from_operations"]
    fcf = row["free_cash_flow"]
    debt = row["total_debt"]


    print(f"Processing {company_name}")


    # -----------------------------
    # CFO Quality Classification
    # -----------------------------

    if pd.isna(cfo):
        cfo_quality = "Unknown"

    elif cfo >= 1000:
        cfo_quality = "Strong"

    elif cfo >= 500:
        cfo_quality = "Moderate"

    else:
        cfo_quality = "Weak"



    # -----------------------------
    # Free Cash Flow Status
    # -----------------------------

    if pd.isna(fcf):

        fcf_status = "Unknown"

    elif fcf > 0:

        fcf_status = "Positive"

    else:

        fcf_status = "Negative"



    # -----------------------------
    # Capital Allocation Pattern
    # -----------------------------

    if (
        pd.notna(fcf)
        and pd.notna(debt)
        and fcf > 0
        and debt < 2500
    ):

        capital_pattern = "Growth Focused"


    elif (
        pd.notna(fcf)
        and fcf > 0
    ):

        capital_pattern = "Balanced"


    else:

        capital_pattern = "Conservative"



    # -----------------------------
    # Confidence Score
    # -----------------------------

    confidence = 85


    results.append({

        "company_id": company_id,
        "company_name": company_name,
        "cash_from_operations": cfo,
        "free_cash_flow": fcf,
        "total_debt": debt,
        "cfo_quality": cfo_quality,
        "fcf_status": fcf_status,
        "capital_allocation_pattern": capital_pattern,
        "confidence_pct": confidence

    })


# -------------------------------------------------
# Create DataFrame
# -------------------------------------------------

cashflow_df = pd.DataFrame(results)


print("\nCash Flow Intelligence Result:")
print(cashflow_df)



# -------------------------------------------------
# Save Output
# -------------------------------------------------

cashflow_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nCash Flow Intelligence Generated Successfully!")

print("Output File:")
print(OUTPUT_FILE)



# -------------------------------------------------
# Close Database
# -------------------------------------------------

conn.close()

print("\nDatabase connection closed.")