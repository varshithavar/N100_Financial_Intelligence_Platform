import os
from pathlib import Path
import pandas as pd
from datetime import datetime


# -------------------------------------------------
# Project Paths
# -------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REPORT_DIR = PROJECT_ROOT / "reports"

OUTPUT_DIR = PROJECT_ROOT / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

SUMMARY_FILE = OUTPUT_DIR / "report_summary.csv"


# -------------------------------------------------
# Validate Reports
# -------------------------------------------------

print("Starting Report Validation...\n")


results = []


def validate_file(file_path, report_type):

    exists = file_path.exists()

    size = file_path.stat().st_size if exists else 0


    status = (
        "VALID"
        if exists and size > 0
        else "FAILED"
    )


    results.append(
        {
            "report_name": file_path.name,
            "report_type": report_type,
            "status": status,
            "file_size_bytes": size,
            "generated_date": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        }
    )


    print(
        f"{file_path.name}: {status}"
    )


# -------------------------------------------------
# Company Reports
# -------------------------------------------------

company_reports = [
    REPORT_DIR / "TCS_tearsheet.pdf",
    REPORT_DIR / "Infosys_tearsheet.pdf",
    REPORT_DIR / "Reliance_tearsheet.pdf"
]


for report in company_reports:

    validate_file(
        report,
        "Company Report"
    )


# -------------------------------------------------
# Sector Reports
# -------------------------------------------------

sector_reports = list(
    REPORT_DIR.glob("*_sector_report.pdf")
)


for report in sector_reports:

    validate_file(
        report,
        "Sector Report"
    )


# -------------------------------------------------
# Save Summary
# -------------------------------------------------

summary_df = pd.DataFrame(results)

summary_df.to_csv(
    SUMMARY_FILE,
    index=False
)


print("\nReport Summary Saved:")
print(SUMMARY_FILE)


# -------------------------------------------------
# Final Status
# -------------------------------------------------

failed = summary_df[
    summary_df["status"] == "FAILED"
]


print("\n--------------------------------")

if len(failed) == 0:

    print(
        "All Reports Validated Successfully!"
    )

else:

    print(
        "Some Reports Failed Validation"
    )


print(
    f"Total Reports Checked: {len(summary_df)}"
)