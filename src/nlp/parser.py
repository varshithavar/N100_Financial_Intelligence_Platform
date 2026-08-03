import re
from pathlib import Path
import pandas as pd

# -------------------------------------------------------
# Project Paths
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "analysis.xlsx"

OUTPUT_DIR = PROJECT_ROOT / "output"
OUTPUT_DIR.mkdir(exist_ok=True)

PARSED_FILE = OUTPUT_DIR / "analysis_parsed.csv"
FAILED_FILE = OUTPUT_DIR / "parse_failures.csv"

# -------------------------------------------------------
# Regex Pattern
# -------------------------------------------------------

PATTERN = re.compile(r"(\d+)\s*Years?:?\s*([\d.\-]+)%", re.IGNORECASE)

# -------------------------------------------------------
# Read Excel
# -------------------------------------------------------

try:
    # Skip title row and use second row as header
    df = pd.read_excel(INPUT_FILE, header=1)

except Exception as e:
    print(e)
    raise

print("\nLoaded Successfully\n")

print(df.head())

print("\nColumns:\n")
print(df.columns.tolist())

# -------------------------------------------------------
# Clean Column Names
# -------------------------------------------------------

df.columns = (
    df.columns.astype(str)
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nCleaned Columns:\n")
print(df.columns.tolist())

# -------------------------------------------------------
# Required Columns
# -------------------------------------------------------

required = [
    "company_id",
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

missing = [c for c in required if c not in df.columns]

if missing:
    print("\nMissing Columns:")
    print(missing)

parsed_rows = []
failed_rows = []

# -------------------------------------------------------
# Parse Text
# -------------------------------------------------------

for _, row in df.iterrows():

    company = row["company_id"]

    for metric in required[1:]:

        value = row[metric]

        if pd.isna(value):
            continue

        value = str(value).strip()

        match = PATTERN.search(value)

        if match:

            parsed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "period_years": int(match.group(1)),
                    "value_pct": float(match.group(2)),
                }
            )

        else:

            failed_rows.append(
                {
                    "company_id": company,
                    "metric_type": metric,
                    "original_text": value,
                }
            )

# -------------------------------------------------------
# Save
# -------------------------------------------------------

parsed_df = pd.DataFrame(parsed_rows)
failed_df = pd.DataFrame(failed_rows)

parsed_df.to_csv(PARSED_FILE, index=False)
failed_df.to_csv(FAILED_FILE, index=False)

# -------------------------------------------------------
# Summary
# -------------------------------------------------------

print("\n--------------------------------------")
print("Parsing Completed")
print("--------------------------------------")

print(f"Rows Loaded     : {len(df)}")
print(f"Parsed Records  : {len(parsed_df)}")
print(f"Failed Records  : {len(failed_df)}")

print(f"\nSaved -> {PARSED_FILE}")
print(f"Saved -> {FAILED_FILE}")

if len(parsed_df):
    print("\nSample Parsed Data:")
    print(parsed_df.head())

if len(failed_df):
    print("\nSample Failed Data:")
    print(failed_df.head())