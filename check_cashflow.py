import pandas as pd
from pathlib import Path

file = Path("output/cashflow_intelligence.xlsx")

if not file.exists():
    print("cashflow_intelligence.xlsx missing")
    exit()

df = pd.read_excel(file)

print("\nCash Flow Intelligence Validation")

print("Rows:", len(df))

print("\nColumns:")
for c in df.columns:
    print("-", c)

print("\nMissing Values:")
print(df.isnull().sum())


if len(df) == 92:
    print("\nCash Flow Validation Completed ✅")
else:
    print("\nRow count mismatch ❌")