import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

DATA_PATH = BASE_DIR / "data" / "raw"


def load_data():
    """
    Load required datasets
    """

    ratios = pd.read_excel(
        DATA_PATH / "financial_ratios.xlsx"
    )

    market_cap = pd.read_excel(
        DATA_PATH / "market_cap.xlsx"
    )

    peers = pd.read_excel(
        DATA_PATH / "peer_groups.xlsx"
    )

    df = ratios.merge(
        market_cap,
        on="company_id"
    )

    df = df.merge(
        peers,
        on="company_id"
    )

    return df



def calculate_score(df):
    """
    Investment scoring model

    Score components:
    ROE score     -> 40%
    PE score      -> 30%
    Market cap    -> 30%
    """

    df["roe_score"] = (
        df["roe"] / df["roe"].max()
    ) * 40


    df["pe_score"] = (
        1 - (df["pe"] / df["pe"].max())
    ) * 30


    df["market_cap_score"] = (
        df["market_cap"] / df["market_cap"].max()
    ) * 30


    df["total_score"] = (
        df["roe_score"]
        +
        df["pe_score"]
        +
        df["market_cap_score"]
    )

    return df



def rank_companies():

    df = load_data()

    df = calculate_score(df)

    ranking = df.sort_values(
        by="total_score",
        ascending=False
    )

    return ranking[
        [
            "company_id",
            "peer",
            "roe",
            "pe",
            "market_cap",
            "total_score"
        ]
    ]



if __name__ == "__main__":

    result = rank_companies()

    print("=" * 60)
    print("COMPANY RANKING")
    print("=" * 60)

    print(result)