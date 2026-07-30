import sqlite3
import pandas as pd


DB_PATH = "database/nifty100.db"


# ---------------------------------------------------
# Merge Data Function
# ---------------------------------------------------
def merge_data():

    conn = sqlite3.connect(DB_PATH)

    # Load company data
    companies = pd.read_sql(
        """
        SELECT *
        FROM companies
        """,
        conn
    )

    # Load financial ratios
    ratios = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )

    # Load price data
    prices = pd.read_sql(
        """
        SELECT *
        FROM prices
        """,
        conn
    )

    conn.close()


    # Merge companies with ratios
    df = companies.merge(
        ratios,
        on="company_id",
        how="inner"
    )


    # Merge with prices
    df = df.merge(
        prices,
        on="company_id",
        how="left"
    )


    # Load market cap data
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



    # ------------------------------------------------
    # Column aliases required for tests and screener
    # ------------------------------------------------

    # ROE
    if "return_on_equity_pct" in df.columns:
        df["roe"] = df["return_on_equity_pct"]

    else:
        df["roe"] = None



    # P/E Ratio
    if "pe" not in df.columns:

        if "price_to_earnings" in df.columns:

            df["pe"] = df["price_to_earnings"]


        elif "pe_ratio" in df.columns:

            df["pe"] = df["pe_ratio"]


        else:

            df["pe"] = None



    # Market Cap
    if "market_cap" not in df.columns:
        df["market_cap"] = None



    return df




# ---------------------------------------------------
# Quality Compounder
# ---------------------------------------------------
def quality_compounder(df):

    return df[
        (df["roe"] >= 15) &
        (df["net_profit_margin_pct"] >= 10) &
        (df["debt_to_equity"] <= 1)
    ]



# ---------------------------------------------------
# Value Pick
# ---------------------------------------------------
def value_pick(df):

    return df[
        (df["pe"] <= 25) &
        (df["roe"] >= 10)
    ]



# ---------------------------------------------------
# Growth Accelerator
# ---------------------------------------------------
def growth_accelerator(df):

    return df[
        (df["net_profit_margin_pct"] >= 8) &
        (df["roe"] >= 12)
    ]



# ---------------------------------------------------
# Low Debt Companies
# ---------------------------------------------------
def low_debt(df):

    return df[
        df["debt_to_equity"] <= 0.5
    ]



# ---------------------------------------------------
# High ROE Companies
# ---------------------------------------------------
def high_roe(df):

    return df[
        df["roe"] >= 20
    ]



# ---------------------------------------------------
# Dividend Stocks
# ---------------------------------------------------
def dividend_stocks(df):

    if "dividend_yield" in df.columns:

        return df[
            df["dividend_yield"] > 1
        ]

    return pd.DataFrame()



# ---------------------------------------------------
# Custom Filter
# ---------------------------------------------------
def custom_filter(
        df,
        roe=None,
        pe=None,
        debt=None
):

    result = df.copy()


    if roe is not None:
        result = result[
            result["roe"] >= roe
        ]


    if pe is not None:
        result = result[
            result["pe"] <= pe
        ]


    if debt is not None:
        result = result[
            result["debt_to_equity"] <= debt
        ]


    return result



# ---------------------------------------------------
# Run All Screeners
# ---------------------------------------------------
def run_screeners():

    df = merge_data()

    results = {

        "quality_compounder":
            quality_compounder(df),

        "value_pick":
            value_pick(df),

        "growth_accelerator":
            growth_accelerator(df),

        "low_debt":
            low_debt(df),

        "high_roe":
            high_roe(df),

        "dividend":
            dividend_stocks(df)
    }


    return results



# ---------------------------------------------------
# Export Results
# ---------------------------------------------------
def export_screener_results():

    results = run_screeners()


    with pd.ExcelWriter(
        "output/screener_output.xlsx"
    ) as writer:


        for name, data in results.items():

            data.to_excel(
                writer,
                sheet_name=name,
                index=False
            )


    return "output/screener_output.xlsx"