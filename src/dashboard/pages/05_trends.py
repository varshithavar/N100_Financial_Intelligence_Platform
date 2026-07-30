import streamlit as st
import pandas as pd
import sys
import os


# -------------------------------------------------
# Add src path
# -------------------------------------------------

SRC_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.insert(0, SRC_PATH)


from analytics.screener import merge_data


# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="Market Trends",
    page_icon="📈",
    layout="wide"
)


st.title("📈 Market & Financial Trends")

st.write(
    "Analyze historical price and financial performance trends."
)



# -------------------------------------------------
# Load Data
# -------------------------------------------------

@st.cache_data(ttl=600)
def load_data():

    return merge_data()



try:

    df = load_data()


except Exception as e:

    st.error(
        f"Unable to load data: {e}"
    )

    st.stop()



# -------------------------------------------------
# Company Selection
# -------------------------------------------------

company = st.selectbox(
    "Select Company",
    df["company_name"].unique()
)



company_df = df[
    df["company_name"] == company
]



# -------------------------------------------------
# Price Trend
# -------------------------------------------------

st.subheader(
    "📊 Price Trend"
)


if (
    "trade_date" in company_df.columns
    and
    "close_price" in company_df.columns
):

    price_data = company_df[
        [
            "trade_date",
            "close_price"
        ]
    ].copy()


    price_data["trade_date"] = pd.to_datetime(
        price_data["trade_date"]
    )


    price_data = price_data.sort_values(
        "trade_date"
    )


    st.line_chart(
        price_data.set_index(
            "trade_date"
        )
    )


else:

    st.info(
        "Price history data not available."
    )



# -------------------------------------------------
# Financial Metrics
# -------------------------------------------------

st.divider()

st.subheader(
    "💰 Financial Metrics"
)


metrics = []


for col in [
    "revenue",
    "net_profit",
    "roe",
    "return_on_equity_pct",
    "free_cash_flow"
]:

    if col in company_df.columns:

        metrics.append(col)



if metrics:

    st.dataframe(
        company_df[metrics],
        use_container_width=True
    )

else:

    st.info(
        "Financial trend data not available."
    )