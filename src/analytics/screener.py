import pandas as pd
from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Dataset location
DATA_PATH = BASE_DIR / "data" / "raw"


def load_supporting_data():
    """
    Load Sprint 3 supporting datasets
    """

    financial_ratios = pd.read_excel(
        DATA_PATH / "financial_ratios.xlsx"
    )

    market_cap = pd.read_excel(
        DATA_PATH / "market_cap.xlsx"
    )

    peer_groups = pd.read_excel(
        DATA_PATH / "peer_groups.xlsx"
    )

    return financial_ratios, market_cap, peer_groups



def merge_data():
    """
    Merge financial, market cap and peer data
    """

    financial_ratios, market_cap, peer_groups = load_supporting_data()

    df = financial_ratios.merge(
        market_cap,
        on="company_id",
        how="inner"
    )

    df = df.merge(
        peer_groups,
        on="company_id",
        how="left"
    )

    return df



def quality_compounder(df):
    """
    Quality Compounder Strategy

    Rules:
    - ROE >= 15%
    - PE <= 30
    - Market Cap >= 300000
    """

    return df[
        (df["roe"] >= 15) &
        (df["pe"] <= 30) &
        (df["market_cap"] >= 300000)
    ]



def value_stocks(df):
    """
    Value Stock Strategy

    Rules:
    - PE < 25
    - ROE > 10%
    """

    return df[
        (df["pe"] < 25) &
        (df["roe"] > 10)
    ]



def growth_stocks(df):
    """
    Growth Stock Strategy

    Rules:
    - ROE >= 18%
    - PE <= 35
    """

    return df[
        (df["roe"] >= 18) &
        (df["pe"] <= 35)
    ]



def run_screener():
    """
    Execute all screening strategies
    """

    df = merge_data()

    print("=" * 60)
    print("ALL COMPANIES")
    print("=" * 60)
    print(df)


    print("\n" + "=" * 60)
    print("QUALITY COMPOUNDERS")
    print("=" * 60)
    print(quality_compounder(df))


    print("\n" + "=" * 60)
    print("VALUE STOCKS")
    print("=" * 60)
    print(value_stocks(df))


    print("\n" + "=" * 60)
    print("GROWTH STOCKS")
    print("=" * 60)
    print(growth_stocks(df))



if __name__ == "__main__":
    run_screener()