"""
Ranking Engine
Sprint 3 - Company Ranking
"""

import sqlite3
import pandas as pd


DB_PATH = "database/nifty100.db"



def load_data():

    conn = sqlite3.connect(DB_PATH)


    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )


    conn.close()

    return df



def rank_companies():
    """
    Rank companies based on financial metrics
    """

    df = load_data()


    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "asset_turnover"
    ]


    for metric in metrics:

        if metric in df.columns:

            df[
                metric + "_rank"
            ] = (
                df[metric]
                .rank(
                    ascending=False
                )
            )


    rank_columns = [
        "return_on_equity_pct_rank",
        "net_profit_margin_pct_rank",
        "asset_turnover_rank"
    ]


    available = [
        col
        for col in rank_columns
        if col in df.columns
    ]


    df["total_score"] = (
        df[available]
        .sum(axis=1)
    )


    return df



if __name__ == "__main__":

    print(
        rank_companies().head()
    )