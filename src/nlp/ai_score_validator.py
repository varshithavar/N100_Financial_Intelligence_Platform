import pandas as pd
from pathlib import Path


INPUT_FILE = Path("output/ai_investment_score.csv")


def validate():

    print("\nAI Investment Score Validation")
    print("=" * 40)

    if not INPUT_FILE.exists():
        print("❌ Output file missing")
        return

    df = pd.read_csv(INPUT_FILE)

    print("Companies Loaded :", len(df))

    print("\nColumns:")
    for col in df.columns:
        print(" -", col)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nTop 10 Scores:")
    print(df.head(10))

    print("\nValidation Completed ✅")


if __name__ == "__main__":
    validate()