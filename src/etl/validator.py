import os
import pandas as pd


def validate(df):
    failures = []

    def add_failure(rule, severity, row, column, message):
        failures.append({
            "Rule": rule,
            "Severity": severity,
            "Row": row,
            "Column": column,
            "Message": message
        })

    # ==================================================
    # DQ-01 : Primary Key NOT NULL
    # ==================================================
    if "id" in df.columns:
        for i, value in enumerate(df["id"]):
            if pd.isna(value):
                add_failure(
                    "DQ-01",
                    "CRITICAL",
                    i,
                    "id",
                    "Primary Key is NULL"
                )

    # ==================================================
    # DQ-02 : Primary Key UNIQUE
    # ==================================================
    if "id" in df.columns:
        duplicates = df[df["id"].duplicated()]
        for i in duplicates.index:
            add_failure(
                "DQ-02",
                "CRITICAL",
                i,
                "id",
                "Duplicate Primary Key"
            )

    # ==================================================
    # DQ-03 : Foreign Key NOT NULL
    # ==================================================
    if "company_id" in df.columns:
        for i, value in enumerate(df["company_id"]):
            if pd.isna(value):
                add_failure(
                    "DQ-03",
                    "CRITICAL",
                    i,
                    "company_id",
                    "Foreign Key missing"
                )

    # ==================================================
    # DQ-04 : Company NOT NULL
    # ==================================================
    if "company" in df.columns:
        for i, value in enumerate(df["company"]):
            if pd.isna(value) or str(value).strip() == "":
                add_failure(
                    "DQ-04",
                    "CRITICAL",
                    i,
                    "company",
                    "Company missing"
                )

    # ==================================================
    # DQ-05 : Ticker NOT NULL
    # ==================================================
    if "ticker" in df.columns:
        for i, value in enumerate(df["ticker"]):
            if pd.isna(value) or str(value).strip() == "":
                add_failure(
                    "DQ-05",
                    "CRITICAL",
                    i,
                    "ticker",
                    "Ticker missing"
                )

    # ==================================================
    # DQ-06 : Year NOT NULL
    # ==================================================
    if "year" in df.columns:
        for i, value in enumerate(df["year"]):
            if pd.isna(value):
                add_failure(
                    "DQ-06",
                    "CRITICAL",
                    i,
                    "year",
                    "Year missing"
                )

    # ==================================================
    # DQ-07 : Sales >= 0
    # ==================================================
    if "sales" in df.columns:
        for i, value in enumerate(df["sales"]):
            if pd.notna(value) and value < 0:
                add_failure(
                    "DQ-07",
                    "CRITICAL",
                    i,
                    "sales",
                    "Negative Sales"
                )

    # ==================================================
    # DQ-08 : Profit >= 0
    # ==================================================
    if "profit" in df.columns:
        for i, value in enumerate(df["profit"]):
            if pd.notna(value) and value < 0:
                add_failure(
                    "DQ-08",
                    "CRITICAL",
                    i,
                    "profit",
                    "Negative Profit"
                )

    # ==================================================
    # DQ-09 : Assets >= Liabilities
    # ==================================================
    if {"assets", "liabilities"}.issubset(df.columns):
        for i, row in df.iterrows():
            if pd.notna(row["assets"]) and pd.notna(row["liabilities"]):
                if row["assets"] < row["liabilities"]:
                    add_failure(
                        "DQ-09",
                        "CRITICAL",
                        i,
                        "assets",
                        "Assets less than Liabilities"
                    )

    # ==================================================
    # DQ-10 : Valid Year
    # ==================================================
    if "year" in df.columns:
        for i, value in enumerate(df["year"]):
            if pd.notna(value):
                if value < 1990 or value > 2035:
                    add_failure(
                        "DQ-10",
                        "CRITICAL",
                        i,
                        "year",
                        "Invalid Year"
                    )

    # ==================================================
    # DQ-11 : OPM Range
    # ==================================================
    if "opm" in df.columns:
        for i, value in enumerate(df["opm"]):
            if pd.notna(value):
                if value < -100 or value > 100:
                    add_failure(
                        "DQ-11",
                        "WARNING",
                        i,
                        "opm",
                        "OPM out of range"
                    )

    # ==================================================
    # DQ-12 : Balance Positive
    # ==================================================
    if "balance" in df.columns:
        for i, value in enumerate(df["balance"]):
            if pd.notna(value):
                if value < 0:
                    add_failure(
                        "DQ-12",
                        "WARNING",
                        i,
                        "balance",
                        "Negative Balance"
                    )

    # ==================================================
    # DQ-13 : Extremely High Sales
    # ==================================================
    if "sales" in df.columns:
        for i, value in enumerate(df["sales"]):
            if pd.notna(value):
                if value > 1_000_000_000:
                    add_failure(
                        "DQ-13",
                        "WARNING",
                        i,
                        "sales",
                        "Unusually High Sales"
                    )

    # ==================================================
    # DQ-14 : Duplicate Company Names
    # ==================================================
    if "company" in df.columns:
        duplicates = df[df["company"].duplicated()]
        for i in duplicates.index:
            add_failure(
                "DQ-14",
                "WARNING",
                i,
                "company",
                "Duplicate Company Name"
            )

    # ==================================================
    # DQ-15 : Empty Optional Fields
    # ==================================================
    optional_columns = [
        "remarks",
        "notes",
        "description"
    ]

    for column in optional_columns:
        if column in df.columns:
            for i, value in enumerate(df[column]):
                if pd.isna(value) or str(value).strip() == "":
                    add_failure(
                        "DQ-15",
                        "WARNING",
                        i,
                        column,
                        "Optional field empty"
                    )

    # ==================================================
    # DQ-16 : Leading/Trailing Spaces
    # ==================================================
    for column in df.columns:

        if df[column].dtype == object:

            for i, value in enumerate(df[column]):

                if pd.notna(value):

                    if str(value) != str(value).strip():

                        add_failure(
                            "DQ-16",
                            "WARNING",
                            i,
                            column,
                            "Leading/Trailing Spaces"
                        )

    # ==================================================
    # Create Report
    # ==================================================

    report = pd.DataFrame(failures)

    os.makedirs("data/reports", exist_ok=True)

    report.to_csv(
        "data/reports/validation_failures.csv",
        index=False
    )

    return report


if __name__ == "__main__":

    sample = pd.DataFrame({
        "id": [1, 2, 2, None],
        "company": ["ABC", "XYZ", "XYZ", ""],
        "ticker": ["ABC", "XYZ", "", "PQR"],
        "company_id": [1, None, 3, 4],
        "year": [2024, 2050, None, 2022],
        "sales": [1000, -500, 5000000000, 100],
        "profit": [100, -50, 30, 20],
        "assets": [100, 50, 100, 300],
        "liabilities": [80, 100, 120, 200],
        "opm": [20, 150, 10, -150],
        "balance": [100, -10, 200, 300],
        "remarks": ["Good", "", None, " Excellent "]
    })

    print(validate(sample))