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

OUTPUT_DIR = PROJECT_ROOT / "output"

REPORT_DIR = PROJECT_ROOT / "reports" / "portfolio"
REPORT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_FILE = REPORT_DIR / "portfolio_summary.pdf"


# -------------------------------------------------
# Input Files
# -------------------------------------------------

CASHFLOW_FILE = OUTPUT_DIR / "cashflow_intelligence.xlsx"

DISTRESS_FILE = OUTPUT_DIR / "distress_alerts.csv"

PROS_FILE = OUTPUT_DIR / "pros_cons_generated.csv"

AI_FILE = OUTPUT_DIR / "ai_investment_score.csv"



# -------------------------------------------------
# Load Data
# -------------------------------------------------

print("Loading Portfolio Data...")


if CASHFLOW_FILE.exists():

    cashflow_df = pd.read_excel(CASHFLOW_FILE)

else:

    cashflow_df = pd.DataFrame()



if DISTRESS_FILE.exists():

    distress_df = pd.read_csv(DISTRESS_FILE)

else:

    distress_df = pd.DataFrame()



if PROS_FILE.exists():

    pros_df = pd.read_csv(PROS_FILE)

else:

    pros_df = pd.DataFrame()



if AI_FILE.exists():

    ai_df = pd.read_csv(AI_FILE)

else:

    ai_df = pd.DataFrame()



# -------------------------------------------------
# Portfolio Metrics
# -------------------------------------------------

total_companies = len(cashflow_df)


if not cashflow_df.empty:

    strong_cfo = len(
        cashflow_df[
            cashflow_df["cfo_quality"] == "Strong"
        ]
    )

    positive_fcf = len(
        cashflow_df[
            cashflow_df["fcf_status"] == "Positive"
        ]
    )

    growth_companies = len(
        cashflow_df[
            cashflow_df["capital_allocation_pattern"]
            == "Growth Focused"
        ]
    )

else:

    strong_cfo = 0
    positive_fcf = 0
    growth_companies = 0



distress_count = len(distress_df)



# -------------------------------------------------
# Create PDF
# -------------------------------------------------

doc = SimpleDocTemplate(
    str(OUTPUT_FILE)
)


styles = getSampleStyleSheet()

content = []


# Title

content.append(
    Paragraph(
        "N100 Financial Intelligence Platform",
        styles["Title"]
    )
)


content.append(
    Paragraph(
        "Portfolio Summary Report",
        styles["Heading2"]
    )
)


content.append(
    Spacer(1, 20)
)



# -------------------------------------------------
# Executive Summary
# -------------------------------------------------

content.append(
    Paragraph(
        "Executive Summary",
        styles["Heading2"]
    )
)


summary_table = [

    ["Metric", "Value"],

    [
        "Companies Analysed",
        str(total_companies)
    ],

    [
        "Strong CFO Companies",
        str(strong_cfo)
    ],

    [
        "Positive Free Cash Flow Companies",
        str(positive_fcf)
    ],

    [
        "Growth Focused Companies",
        str(growth_companies)
    ],

    [
        "Distress Companies",
        str(distress_count)
    ]

]


table = Table(summary_table)


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


content.append(table)


content.append(
    Spacer(1,20)
)



# -------------------------------------------------
# Distress Summary
# -------------------------------------------------

content.append(
    Paragraph(
        "Distress Alert Summary",
        styles["Heading2"]
    )
)


if not distress_df.empty:


    distress_table = [

        [
            "Company",
            "FCF Status",
            "CFO Quality"
        ]

    ]


    for _, row in distress_df.head(10).iterrows():

        distress_table.append(
            [
                row["company_name"],
                row["fcf_status"],
                row["cfo_quality"]
            ]
        )


    table = Table(distress_table)


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


    content.append(table)


else:

    content.append(
        Paragraph(
            "No distress alerts found.",
            styles["BodyText"]
        )
    )



content.append(
    Spacer(1,20)
)



# -------------------------------------------------
# AI Insights
# -------------------------------------------------

content.append(
    Paragraph(
        "AI Investment Intelligence",
        styles["Heading2"]
    )
)


if not ai_df.empty:


    content.append(
        Paragraph(
            f"AI scores available for {len(ai_df)} companies.",
            styles["BodyText"]
        )
    )


else:

    content.append(
        Paragraph(
            "AI score data not available.",
            styles["BodyText"]
        )
    )



content.append(
    Spacer(1,20)
)



# -------------------------------------------------
# NLP Summary
# -------------------------------------------------

content.append(
    Paragraph(
        "NLP Analysis Summary",
        styles["Heading2"]
    )
)


if not pros_df.empty:


    content.append(
        Paragraph(
            f"NLP insights generated for {pros_df['company_id'].nunique()} companies.",
            styles["BodyText"]
        )
    )


else:

    content.append(
        Paragraph(
            "NLP insights unavailable.",
            styles["BodyText"]
        )
    )



# -------------------------------------------------
# Build PDF
# -------------------------------------------------

doc.build(content)


print("\nPortfolio Summary Generated Successfully!")

print("Output:")

print(OUTPUT_FILE)