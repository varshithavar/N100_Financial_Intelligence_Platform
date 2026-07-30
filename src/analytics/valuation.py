import sqlite3
import pandas as pd
import os


DB_PATH = "database/nifty100.db"
OUTPUT_PATH = "output/valuation_summary_v2.xlsx"


# ---------------------------------------------------
# Load required data
# ---------------------------------------------------
def load_valuation_data():

    conn = sqlite3.connect(DB_PATH)

    companies = pd.read_sql(
        """
        SELECT *
        FROM companies
        """,
        conn
    )

    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )

    prices = pd.read_sql(
        """
        SELECT *
        FROM prices
        """,
        conn
    )

    conn.close()


    df = companies.merge(
        ratios,
        on="company_id",
        how="inner"
    )


    df = df.merge(
        prices,
        on="company_id",
        how="left"
    )


    return df



# ---------------------------------------------------
# Calculate valuation metrics
# ---------------------------------------------------
def calculate_valuation(df):


    # ROE
    if "return_on_equity_pct" in df.columns:
        df["roe"] = df["return_on_equity_pct"]

    else:
        df["roe"] = None



    # Load market cap
    try:

        market_cap = pd.read_excel(
            "data/raw/market_cap.xlsx"
        )


        df = df.merge(
            market_cap,
            on="company_id",
            how="left"
        )


    except Exception:

        df["market_cap"] = None



    # FCF Yield
    if (
        "free_cash_flow" in df.columns
        and "market_cap" in df.columns
    ):

        df["fcf_yield"] = (
            df["free_cash_flow"]
            /
            df["market_cap"]
        ) * 100


    else:

        df["fcf_yield"] = None



    # PE column
    if "pe" not in df.columns:
        df["pe"] = None



    return df


# ---------------------------------------------------
# Valuation Classification
# ---------------------------------------------------
def valuation_label(row):


    pe = row["pe"]
    fcf = row["fcf_yield"]


    if pd.notna(pe):

        if pe < 15:
            return "Undervalued"

        elif pe > 40:
            return "Overvalued"



    if pd.notna(fcf):

        if fcf > 5:
            return "Attractive"



    return "Fair Value"



# ---------------------------------------------------
# Generate valuation summary
# ---------------------------------------------------
def generate_valuation_summary():


    df = load_valuation_data()


    df = calculate_valuation(df)


    df["valuation_flag"] = (
        df.apply(
            valuation_label,
            axis=1
        )
    )


    columns = [
        "company_id",
        "company_name",
        "roe",
        "pe",
        "free_cash_flow",
        "market_cap",
        "fcf_yield",
        "valuation_flag"
    ]


    available_columns = [
        col
        for col in columns
        if col in df.columns
    ]


    result = df[
        available_columns
    ]



    # create output folder
    os.makedirs(
        "output",
        exist_ok=True
    )


    result.to_excel(
        OUTPUT_PATH,
        index=False
    )


    return result



# ---------------------------------------------------
# Main execution
# ---------------------------------------------------
if __name__ == "__main__":


    valuation = generate_valuation_summary()


    print(
        "Valuation summary generated successfully"
    )


    print(
        valuation.head()
    )