import pandas as pd
from pathlib import Path

raw_dir = Path("data/raw")

files = [
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx"
]

for file in files:
    print("=" * 60)
    print(file)

    path = raw_dir / file

    if not path.exists():
        print(f"File not found: {path}")
        continue

    df = pd.read_excel(path)

    print("Columns:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())
    print()