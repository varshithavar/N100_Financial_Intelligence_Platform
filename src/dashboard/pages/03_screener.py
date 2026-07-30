import streamlit as st
import pandas as pd
import sys
import os


# Add src folder to Python path
SRC_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.insert(0, SRC_PATH)


from analytics.screener import (
    merge_data,
    quality_compounder,
    value_pick,
    growth_accelerator,
    low_debt,
    high_roe
)


st.set_page_config(
    page_title="Stock Screener",
    page_icon="🔎",
    layout="wide"
)


st.title("🔎 Nifty 100 Stock Screener")


@st.cache_data(ttl=600)
def load_data():

    return merge_data()



try:
    df = load_data()

except Exception as e:

    st.error(
        f"Database loading failed: {e}"
    )

    st.stop()



st.sidebar.header("Select Screener")


strategy = st.sidebar.selectbox(
    "Choose Strategy",
    [
        "Quality Compounder",
        "Value Pick",
        "Growth Accelerator",
        "Low Debt",
        "High ROE"
    ]
)



if strategy == "Quality Compounder":

    result = quality_compounder(df)


elif strategy == "Value Pick":

    result = value_pick(df)


elif strategy == "Growth Accelerator":

    result = growth_accelerator(df)


elif strategy == "Low Debt":

    result = low_debt(df)


else:

    result = high_roe(df)



st.subheader(
    f"📊 {strategy} Results"
)


st.metric(
    "Companies Found",
    len(result)
)


st.dataframe(
    result,
    use_container_width=True
)



csv = result.to_csv(
    index=False
)


st.download_button(
    "⬇ Download CSV",
    csv,
    "screener_results.csv",
    "text/csv"
)