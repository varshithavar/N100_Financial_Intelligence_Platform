import pandas as pd
from pathlib import Path

file_path = Path("data/raw/market_cap.xlsx")

data = {
    "company_id": [1, 2, 3],
    "market_cap": [700000, 1500000, 300000]
}

df = pd.DataFrame(data)

df.to_excel(
    file_path,
    index=False,
    engine="openpyxl"
)

print("market_cap.xlsx created successfully")