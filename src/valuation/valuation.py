"""
Valuation Engine
================
Sprint 4 - Financial Intelligence Platform

Features:
- FCF Yield calculation
- P/E classification
- Valuation labels
- Excel export
"""

import sqlite3
import pandas as pd
import os


DB_PATH = "database/nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)



def load_financial_data():
    """
    Load company financial data
    and merge with market cap data
    """

    conn = get_connection()

    query = """
    SELECT
        c.company_id,
        c.symbol,
        c.company_name,
        r.free_cash_flow

    FROM companies c

    JOIN financial_ratios r
    ON c.company_id = r.company_id
    """

    df = pd.read_sql(
        query,
        conn
    )

    conn.close()


    # Load market cap file

    market_file = (
        "data/supporting/market_cap.xlsx"
    )


    market_df = pd.read_excel(
        market_file
    )


    # Latest available year

    latest_year = (
        market_df["year"].max()
    )


    market_df = market_df[
        market_df["year"] == latest_year
    ]


    # Rename columns

    market_df = market_df.rename(
        columns={
            "company_id": "symbol",
            "market_cap_crore": "market_cap"
        }
    )


    # Merge database + market data

    df = df.merge(
        market_df[
            [
                "symbol",
                "market_cap",
                "pe_ratio"
            ]
        ],
        on="symbol",
        how="left"
    )


    return df



def calculate_fcf_yield(df):
    """
    FCF Yield %

    Formula:
    Free Cash Flow / Market Cap * 100
    """

    df["fcf_yield_pct"] = (
        df["free_cash_flow"]
        /
        df["market_cap"]
        *
        100
    )

    return df



def calculate_pe_flag(df):
    """
    Classify PE ratio
    """

    df["pe_flag"] = pd.cut(
        df["pe_ratio"],
        bins=[
            -float("inf"),
            15,
            30,
            float("inf")
        ],
        labels=[
            "Low PE",
            "Normal PE",
            "High PE"
        ]
    )

    return df



def valuation_label(row):
    """
    Generate valuation category
    """

    if (
        row["fcf_yield_pct"] >= 5
        and row["pe_ratio"] <= 20
    ):
        return "Undervalued"


    elif (
        row["fcf_yield_pct"] < 2
        and row["pe_ratio"] > 35
    ):
        return "Overvalued"


    else:
        return "Fair Value"



def run_valuation():
    """
    Complete valuation pipeline
    """

    print(
        "Running valuation engine..."
    )


    df = load_financial_data()


    # Remove missing market values

    df = df.dropna(
        subset=[
            "market_cap",
            "pe_ratio"
        ]
    )


    df = calculate_fcf_yield(df)


    df = calculate_pe_flag(df)


    df["valuation_label"] = (
        df.apply(
            valuation_label,
            axis=1
        )
    )


    # Create output folder

    os.makedirs(
        "output",
        exist_ok=True
    )


    output_file = (
        "output/valuation_summary.xlsx"
    )


    df.to_excel(
        output_file,
        index=False
    )


    print(
        f"Valuation completed: {output_file}"
    )


    return df



if __name__ == "__main__":

    result = run_valuation()


    print(
        "\nValuation Summary:"
    )


    print(
        result.head()
    )