import sqlite3
import pandas as pd
from pathlib import Path

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet


# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_FILE = PROJECT_ROOT / "database" / "nifty100.db"

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)


# -------------------------------------------------
# Database Connection
# -------------------------------------------------

conn = sqlite3.connect(DB_FILE)

print("Database connected successfully!")


# -------------------------------------------------
# Load Sector Data
# -------------------------------------------------

query = """
SELECT
    s.sector_name,
    c.company_name,
    f.net_profit_margin_pct,
    f.return_on_equity_pct,
    f.free_cash_flow,
    f.cash_from_operations
FROM financial_ratios f
JOIN companies c
ON f.company_id = c.company_id
JOIN sector s
ON CAST(c.sector AS INTEGER) = s.sector_id
ORDER BY s.sector_name;
"""

try:

    df = pd.read_sql(query, conn)

except Exception as e:

    print("\nSector data loading failed:")
    print(e)

    conn.close()
    exit()


print("\nSector Data Loaded")

print(df.head())

print("\nTotal Records:", len(df))


# -------------------------------------------------
# Create Sector PDF
# -------------------------------------------------

def create_sector_report(sector_name, sector_df):

    file_name = (
        sector_name
        .replace(" ", "_")
        .replace("/", "_")
        + "_sector_report.pdf"
    )


    pdf_path = REPORT_DIR / file_name


    doc = SimpleDocTemplate(
        str(pdf_path)
    )


    styles = getSampleStyleSheet()

    content = []


    # Title

    content.append(
        Paragraph(
            f"{sector_name} Sector Intelligence Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )


    # Calculate Metrics

    avg_roe = sector_df[
        "return_on_equity_pct"
    ].mean()


    avg_margin = sector_df[
        "net_profit_margin_pct"
    ].mean()


    avg_fcf = sector_df[
        "free_cash_flow"
    ].mean()


    avg_cfo = sector_df[
        "cash_from_operations"
    ].mean()



    # Sector Summary Table

    table_data = [

        ["Metric", "Value"],

        [
            "Number of Companies",
            str(len(sector_df))
        ],

        [
            "Average ROE %",
            round(avg_roe, 2)
        ],

        [
            "Average Profit Margin %",
            round(avg_margin, 2)
        ],

        [
            "Average Free Cash Flow",
            round(avg_fcf, 2)
        ],

        [
            "Average Cash From Operations",
            round(avg_cfo, 2)
        ]

    ]


    table = Table(table_data)


    table.setStyle(
        TableStyle(
            [
                (
                    "GRID",
                    (0,0),
                    (-1,-1),
                    1,
                    None
                )
            ]
        )
    )


    content.append(
        Paragraph(
            "Sector Performance Summary",
            styles["Heading2"]
        )
    )


    content.append(table)


    content.append(
        Spacer(1,20)
    )


    # Company List

    content.append(
        Paragraph(
            "Companies in Sector",
            styles["Heading2"]
        )
    )


    for company in sector_df["company_name"]:

        content.append(
            Paragraph(
                f"- {company}",
                styles["BodyText"]
            )
        )


    doc.build(content)


    print(
        f"Generated: {pdf_path}"
    )


# -------------------------------------------------
# Generate All Sector Reports
# -------------------------------------------------

for sector_name, sector_df in df.groupby("sector_name"):

    print(
        f"\nProcessing Sector: {sector_name}"
    )


    create_sector_report(
        sector_name,
        sector_df
    )


# -------------------------------------------------
# Close Database
# -------------------------------------------------

conn.close()


print(
    "\nSector Reports Generated Successfully!"
)