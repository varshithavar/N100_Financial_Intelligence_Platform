import pandas as pd
from pathlib import Path


# ---------------------------------------
# Project Path
# ---------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_FILE = (
    PROJECT_ROOT
    / "output"
    / "pros_cons_generated.csv"
)


# ---------------------------------------
# Check File
# ---------------------------------------

if not INPUT_FILE.exists():
    print("pros_cons_generated.csv not found")
    print(INPUT_FILE)
    exit()


# ---------------------------------------
# Load CSV
# ---------------------------------------

df = pd.read_csv(INPUT_FILE)


print("\n# Pros Cons Validation\n")

print("Total Records :", len(df))

print(
    "Companies Loaded :",
    df["company_id"].nunique()
)


print("\nColumns:")

for col in df.columns:
    print("-", col)


# ---------------------------------------
# Missing Values
# ---------------------------------------

print("\nMissing Values:")

print(df.isnull().sum())


# ---------------------------------------
# PRO / CON Check
# ---------------------------------------

summary = (
    df.groupby("company_id")
    .agg(
        pros=(
            "type",
            lambda x: (x.str.upper()=="PRO").sum()
        ),
        cons=(
            "type",
            lambda x: (x.str.upper()=="CON").sum()
        )
    )
)


missing_pros = summary[
    summary["pros"] == 0
]


missing_cons = summary[
    summary["cons"] == 0
]


print("\nMissing PRO Companies:")
print(len(missing_pros))


print("\nMissing CON Companies:")
print(len(missing_cons))


# ---------------------------------------
# Final Status
# ---------------------------------------

if (
    len(missing_pros) == 0
    and len(missing_cons) == 0
    and df["company_id"].nunique() == 92
):

    print(
        "\nPros & Cons Validation Completed ✅"
    )

else:

    print(
        "\nPros & Cons Validation Failed ❌"
    )