import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "raw"
REPORTS_PATH = BASE_DIR / "reports"

REPORTS_PATH.mkdir(exist_ok=True)


def load_data():
    ratios = pd.read_excel(DATA_PATH / "financial_ratios.xlsx")
    market_cap = pd.read_excel(DATA_PATH / "market_cap.xlsx")
    peers = pd.read_excel(DATA_PATH / "peer_groups.xlsx")

    df = ratios.merge(market_cap, on="company_id")
    df = df.merge(peers, on="company_id")

    return df


def generate_report(df):
    report = pd.DataFrame({
        "Company": df["peer"],
        "ROE": df["roe"],
        "PE": df["pe"],
        "Market Cap": df["market_cap"]
    })

    report["Investment Score"] = (
        report["ROE"] * 2
        - report["PE"] * 0.5
        + report["Market Cap"] / 100000
    )

    report = report.sort_values(
        by="Investment Score",
        ascending=False
    )

    return report


def save_report(report):
    output_file = REPORTS_PATH / "investment_report.csv"
    report.to_csv(output_file, index=False)

    print(f"\nReport saved successfully:")
    print(output_file)


if __name__ == "__main__":
    df = load_data()

    report = generate_report(df)

    print("=" * 60)
    print("INVESTMENT REPORT")
    print("=" * 60)
    print(report)

    save_report(report)