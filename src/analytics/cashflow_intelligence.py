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

OUTPUT_FILE = OUTPUT_DIR / "cashflow_intelligence.xlsx"


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



# -------------------------------------------------
# Remove Duplicate Companies
# Keep Latest Financial Record
# -------------------------------------------------

df = df.drop_duplicates(
    subset=["company_id"],
    keep="last"
)


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
    # CFO Quality
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
    # FCF Status
    # -----------------------------

    if pd.isna(fcf):

        fcf_status = "Unknown"

    elif fcf > 0:

        fcf_status = "Positive"

    else:

        fcf_status = "Negative"



    # -----------------------------
    # CapEx Intensity
    # -----------------------------

    if pd.isna(cfo) or pd.isna(fcf):

        capex_intensity = "Unknown"

    else:

        capex_value = cfo - fcf


        if capex_value < 500:

            capex_intensity = "Low"

        elif capex_value < 2000:

            capex_intensity = "Medium"

        else:

            capex_intensity = "High"



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
    # Distress Flag
    # -----------------------------

    if (
        (pd.notna(fcf) and fcf < 0)
        or
        (pd.notna(debt) and debt > 5000)
        or
        cfo_quality == "Weak"
    ):

        distress_flag = "YES"

    else:

        distress_flag = "NO"



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

        "capex_intensity": capex_intensity,

        "capital_allocation_pattern": capital_pattern,

        "distress_flag": distress_flag,

        "confidence_pct": confidence

    })



# -------------------------------------------------
# Create DataFrame
# -------------------------------------------------

cashflow_df = pd.DataFrame(results)


print("\nCash Flow Intelligence Result")

print(cashflow_df.head())

print("\nRows Generated:", len(cashflow_df))



# -------------------------------------------------
# Save Excel Output
# -------------------------------------------------

cashflow_df.to_excel(
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

print("\nDatabase connection closed!")