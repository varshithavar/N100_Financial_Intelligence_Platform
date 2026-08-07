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

PROS_FILE = PROJECT_ROOT / "output" / "pros_cons_generated.csv"

CASHFLOW_FILE = PROJECT_ROOT / "output" / "capital_allocation.csv"

VALUATION_FILE = PROJECT_ROOT / "output" / "valuation_summary.xlsx"

AI_SCORE_FILE = PROJECT_ROOT / "output" / "ai_investment_score.csv"


# -------------------------------------------------
# Database Connection
# -------------------------------------------------

conn = sqlite3.connect(DB_FILE)

print("Database connected successfully!")


# -------------------------------------------------
# Load Financial Data
# -------------------------------------------------

query = """
SELECT
c.company_id,
c.company_name,
f.financial_year,
f.net_profit_margin_pct,
f.return_on_equity_pct,
f.debt_to_equity,
f.free_cash_flow,
f.cash_from_operations
FROM financial_ratios f
JOIN companies c
ON f.company_id = c.company_id
ORDER BY c.company_id;
"""


financial_df = pd.read_sql(query, conn)


# Clean company names

financial_df["company_name"] = (
    financial_df["company_name"]
    .astype(str)
    .str.replace("\n", " ", regex=False)
    .str.replace("\r", " ", regex=False)
    .str.strip()
)


print("\nFinancial Data Loaded")
print(financial_df.head())


# -------------------------------------------------
# Load NLP Pros Cons
# -------------------------------------------------

if PROS_FILE.exists():

    pros_df = pd.read_csv(PROS_FILE)

else:

    pros_df = pd.DataFrame()



# -------------------------------------------------
# Load Cash Flow Intelligence
# -------------------------------------------------

if CASHFLOW_FILE.exists():

    cashflow_df = pd.read_csv(CASHFLOW_FILE)

else:

    cashflow_df = pd.DataFrame()



# -------------------------------------------------
# Load Valuation Data
# -------------------------------------------------

if VALUATION_FILE.exists():

    valuation_df = pd.read_excel(
        VALUATION_FILE
    )

else:

    valuation_df = pd.DataFrame()



# -------------------------------------------------
# Load AI Investment Score
# -------------------------------------------------

if AI_SCORE_FILE.exists():

    ai_df = pd.read_csv(
        AI_SCORE_FILE
    )

else:

    ai_df = pd.DataFrame()



# -------------------------------------------------
# Create PDF Function
# -------------------------------------------------

def create_pdf(company_id, company_name):


    clean_name = (
        str(company_name)
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("/", "-")
        .replace("\\", "-")
        .strip()
    )


    pdf_file = REPORT_DIR / f"{clean_name}_tearsheet.pdf"


    doc = SimpleDocTemplate(
        str(pdf_file)
    )


    styles = getSampleStyleSheet()

    content = []


    # Title

    content.append(
        Paragraph(
            f"{clean_name} Financial Intelligence Report",
            styles["Title"]
        )
    )


    content.append(
        Spacer(1,20)
    )
    content.append(
        Spacer(1,20)
    )


    # -------------------------------------------------
    # AI Investment Intelligence
    # -------------------------------------------------

    content.append(
        Paragraph(
            "AI Investment Intelligence",
            styles["Heading2"]
        )
    )


    if not ai_df.empty:


        ai_data = ai_df[
            ai_df["company_id"] == company_id
        ]


        if not ai_data.empty:


            ai = ai_data.iloc[0]


            ai_table = [

                ["Metric", "Value"],

                [
                    "AI Score",
                    str(ai["ai_score"])
                ],

                [
                    "AI Rating",
                    str(ai["ai_rating"])
                ],

                [
                    "NLP Confidence",
                    f"{ai['nlp_confidence']}%"
                ],

                [
                    "Positive Factors",
                    str(ai["pro"])
                ],

                [
                    "Risk Factors",
                    str(ai["con"])
                ]

            ]


            table = Table(ai_table)


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
                "No AI score available.",
                styles["BodyText"]
            )
        )



    content.append(
        Spacer(1,20)
    )


    # -------------------------------------------------
    # Financial Summary
    # -------------------------------------------------

    company_data = financial_df[
        financial_df["company_id"] == company_id
    ]


    if not company_data.empty:


        latest = company_data.iloc[-1]


        financial_table = [

            ["Metric","Value"],

            [
                "Profit Margin %",
                str(latest["net_profit_margin_pct"])
            ],

            [
                "ROE %",
                str(latest["return_on_equity_pct"])
            ],

            [
                "Debt To Equity",
                str(latest["debt_to_equity"])
            ],

            [
                "Free Cash Flow",
                str(latest["free_cash_flow"])
            ],

            [
                "Cash From Operations",
                str(latest["cash_from_operations"])
            ]

        ]


        table = Table(financial_table)


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
                "Financial Summary",
                styles["Heading2"]
            )
        )


        content.append(table)



    content.append(
        Spacer(1,20)
    )



    # -------------------------------------------------
    # Pros & Cons
    # -------------------------------------------------

    content.append(
        Paragraph(
            "AI Generated Pros & Cons",
            styles["Heading2"]
        )
    )


    if not pros_df.empty:


        company_pros = pros_df[
            pros_df["company_id"] == company_id
        ]


        for _, row in company_pros.iterrows():


            text = (
                f"{row['type'].upper()} : "
                f"{row['text']} "
                f"(Confidence {row['confidence_pct']}%)"
            )


            content.append(
                Paragraph(
                    text,
                    styles["BodyText"]
                )
            )


    else:

        content.append(
            Paragraph(
                "No NLP insights available.",
                styles["BodyText"]
            )
        )



    content.append(
        Spacer(1,20)
    )



    # -------------------------------------------------
    # Cash Flow Intelligence
    # -------------------------------------------------

    content.append(
        Paragraph(
            "Cash Flow Intelligence",
            styles["Heading2"]
        )
    )


    if not cashflow_df.empty:


        cash_data = cashflow_df[
            cashflow_df["company_id"] == company_id
        ]


        if not cash_data.empty:


            cash = cash_data.iloc[0]


            content.append(
                Paragraph(
                    f"CFO Quality : {cash['cfo_quality']}",
                    styles["BodyText"]
                )
            )


            content.append(
                Paragraph(
                    f"FCF Status : {cash['fcf_status']}",
                    styles["BodyText"]
                )
            )


            content.append(
                Paragraph(
                    f"Capital Allocation : {cash['capital_allocation_pattern']}",
                    styles["BodyText"]
                )
            )


    else:

        content.append(
            Paragraph(
                "No cash flow intelligence available.",
                styles["BodyText"]
            )
        )



    # Build PDF

    doc.build(content)


    print(
        f"Generated: {pdf_file}"
    )



# -------------------------------------------------
# Generate All Reports
# -------------------------------------------------

companies = (
    financial_df[
        [
            "company_id",
            "company_name"
        ]
    ]
    .drop_duplicates()
)



for _, company in companies.iterrows():

    create_pdf(
        company["company_id"],
        company["company_name"]
    )



conn.close()


print(
    "\nAll Company Tearsheet PDFs Generated Successfully!"
)