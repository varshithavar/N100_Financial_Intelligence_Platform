import sqlite3
from pathlib import Path
import os

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = Path(__file__).resolve().parents[2]
DB_PATH = BASE_DIR / "database" / "nifty100.db"

OUTPUT_DIR = BASE_DIR / "reports" / "radar_charts"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

conn = sqlite3.connect(DB_PATH)

query = """
SELECT
    c.company_name,
    f.return_on_equity_pct,
    f.net_profit_margin_pct,
    f.debt_to_equity,
    f.asset_turnover,
    f.free_cash_flow
FROM financial_ratios f
JOIN companies c
ON f.company_id = c.company_id
"""

df = pd.read_sql(query, conn)

conn.close()

categories = [
    "ROE",
    "NPM",
    "D/E",
    "Asset Turnover",
    "FCF"
]

angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
angles = np.concatenate((angles, [angles[0]]))

for _, row in df.iterrows():

    values = [

        row["return_on_equity_pct"] or 0,
        row["net_profit_margin_pct"] or 0,
        row["debt_to_equity"] or 0,
        row["asset_turnover"] or 0,
        row["free_cash_flow"] or 0

    ]

    values.append(values[0])

    plt.figure(figsize=(6,6))

    ax = plt.subplot(111, polar=True)

    ax.plot(angles, values, linewidth=2)

    ax.fill(angles, values, alpha=0.25)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories)

    ax.set_title(row["company_name"])

    filename = row["company_name"].replace(" ", "_") + "_radar.png"

    plt.savefig(OUTPUT_DIR / filename)

    plt.close()

print("=" * 50)
print("Radar Charts Generated Successfully")
print("=" * 50)
print("Saved to:", OUTPUT_DIR)