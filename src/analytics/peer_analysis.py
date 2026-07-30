"""
Peer Analysis Engine
Sprint 3 - Peer Comparison
"""

import sqlite3
import pandas as pd


DB_PATH = "database/nifty100.db"



def load_data():
    """
    Load peer comparison data
    """

    conn = sqlite3.connect(DB_PATH)


    df = pd.read_sql(
        """
        SELECT
            c.company_id,
            c.symbol,
            c.company_name,
            c.sector,

            r.*

        FROM companies c

        JOIN financial_ratios r

        ON c.company_id = r.company_id
        """,
        conn
    )


    conn.close()


    # Create peer group column
    df["peer"] = (
        df["sector"]
        .fillna("Unknown")
    )


    return df



def peer_percentile(df, metric):

    df[
        metric + "_percentile"
    ] = (
        df[metric]
        .rank(
            pct=True
        )
        *
        100
    )

    return df



def create_peer_comparison():

    df = load_data()


    metrics = [
        "return_on_equity_pct",
        "net_profit_margin_pct",
        "debt_to_equity",
        "asset_turnover"
    ]


    for metric in metrics:

        if metric in df.columns:

            df = peer_percentile(
                df,
                metric
            )


    return df



if __name__ == "__main__":

    print(
        load_data().head()
    )