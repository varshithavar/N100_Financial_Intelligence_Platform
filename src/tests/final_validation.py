import sqlite3
from pathlib import Path
import pandas as pd


# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_FILE = PROJECT_ROOT / "database" / "nifty100.db"

OUTPUT_DIR = PROJECT_ROOT / "output"

REPORT_DIR = PROJECT_ROOT / "reports"


print("Starting Final Project Validation...\n")


validation_results = []


# -------------------------------------------------
# 1. Database Validation
# -------------------------------------------------

try:

    conn = sqlite3.connect(DB_FILE)

    print("Database Connected Successfully")

    tables_df = pd.read_sql(
        "SELECT name FROM sqlite_master WHERE type='table';",
        conn
    )

    existing_tables = tables_df["name"].tolist()


    required_tables = [
        "companies",
        "profit_loss",
        "balance_sheet",
        "cash_flow",
        "prices",
        "ratios",
        "financial_ratios",
        "peer_percentiles",
        "sector"
    ]


    for table in required_tables:

        status = (
            "PASS"
            if table in existing_tables
            else "FAIL"
        )

        validation_results.append(
            {
                "check": f"Database Table: {table}",
                "status": status
            }
        )


    conn.close()


except Exception as e:

    validation_results.append(
        {
            "check": "Database Connection",
            "status": "FAIL"
        }
    )

    print(e)



# -------------------------------------------------
# 2. Output File Validation
# -------------------------------------------------

required_outputs = [

    "pros_cons_generated.csv",
    "company_summary.csv",
    "capital_allocation.csv",
    "report_summary.csv"

]


for file in required_outputs:

    file_path = OUTPUT_DIR / file


    validation_results.append(
        {
            "check": f"Output File: {file}",
            "status":
                "PASS"
                if file_path.exists()
                else "FAIL"
        }
    )



# -------------------------------------------------
# 3. Report PDF Validation
# -------------------------------------------------

company_reports = [

    "TCS_tearsheet.pdf",
    "Infosys_tearsheet.pdf",
    "Reliance_tearsheet.pdf"

]


for report in company_reports:

    report_path = REPORT_DIR / report


    validation_results.append(
        {
            "check": f"Company Report: {report}",
            "status":
                "PASS"
                if report_path.exists()
                else "FAIL"
        }
    )



sector_reports = list(
    REPORT_DIR.glob("*_sector_report.pdf")
)


validation_results.append(
    {
        "check": "Sector Reports Generated",
        "status":
            "PASS"
            if len(sector_reports) > 0
            else "FAIL"
    }
)



# -------------------------------------------------
# 4. NLP Validation
# -------------------------------------------------

nlp_file = OUTPUT_DIR / "pros_cons_generated.csv"


if nlp_file.exists():

    nlp_df = pd.read_csv(nlp_file)

    status = (
        "PASS"
        if len(nlp_df) > 0
        else "FAIL"
    )

else:

    status = "FAIL"



validation_results.append(
    {
        "check": "NLP Pros Cons Generation",
        "status": status
    }
)



# -------------------------------------------------
# 5. Cash Flow Validation
# -------------------------------------------------

cashflow_file = OUTPUT_DIR / "capital_allocation.csv"


if cashflow_file.exists():

    cashflow_df = pd.read_csv(cashflow_file)

    status = (
        "PASS"
        if len(cashflow_df) > 0
        else "FAIL"
    )

else:

    status = "FAIL"



validation_results.append(
    {
        "check": "Cash Flow Intelligence",
        "status": status
    }
)



# -------------------------------------------------
# Final Summary
# -------------------------------------------------

result_df = pd.DataFrame(validation_results)


print("\nValidation Results:")
print(result_df.to_string(index=False))


failed = result_df[
    result_df["status"] == "FAIL"
]


print("\n--------------------------------")


if len(failed) == 0:

    print("FINAL VALIDATION PASSED SUCCESSFULLY!")

else:

    print("VALIDATION FAILED")

    print("\nFailed Checks:")
    print(
        failed.to_string(index=False)
    )


print(
    f"\nTotal Checks: {len(result_df)}"
)