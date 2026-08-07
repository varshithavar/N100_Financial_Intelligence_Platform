import pandas as pd
from pathlib import Path


# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "output" / "cashflow_intelligence.xlsx"

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "distress_alerts.csv"


# -------------------------------------------------
# Check Input File
# -------------------------------------------------

if not INPUT_FILE.exists():

    print("cashflow_intelligence.xlsx missing")

    exit()


# -------------------------------------------------
# Load Cash Flow Intelligence
# -------------------------------------------------

df = pd.read_excel(INPUT_FILE)


print("Cash Flow Intelligence Loaded")

print(df.head())

print("\nTotal Companies:", len(df))



# -------------------------------------------------
# Generate Distress Alerts
# -------------------------------------------------

distress_df = df[
    df["distress_flag"].astype(str).str.upper() == "YES"
]


# -------------------------------------------------
# Select Important Columns
# -------------------------------------------------

if not distress_df.empty:

    distress_df = distress_df[
        [
            "company_id",
            "company_name",
            "cash_from_operations",
            "free_cash_flow",
            "total_debt",
            "cfo_quality",
            "fcf_status",
            "capital_allocation_pattern",
            "distress_flag",
            "confidence_pct"
        ]
    ]


else:

    distress_df = pd.DataFrame(
        columns=[
            "company_id",
            "company_name",
            "cash_from_operations",
            "free_cash_flow",
            "total_debt",
            "cfo_quality",
            "fcf_status",
            "capital_allocation_pattern",
            "distress_flag",
            "confidence_pct"
        ]
    )



# -------------------------------------------------
# Save Output
# -------------------------------------------------

distress_df.to_csv(
    OUTPUT_FILE,
    index=False
)


print("\nDistress Alert Generation Completed!")

print("Distress Companies:", len(distress_df))

print("Output File:")

print(OUTPUT_FILE)