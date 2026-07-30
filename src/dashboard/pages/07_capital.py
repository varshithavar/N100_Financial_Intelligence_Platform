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
    page_title="Capital Allocation",
    page_icon="💰",
    layout="wide"
)


st.title("💰 Capital Allocation Dashboard")

st.write(
    "Analyze company cash generation, debt position and capital efficiency."
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
        f"Unable to load capital data: {e}"
    )

    st.stop()



# -------------------------------------------------
# Free Cash Flow Analysis
# -------------------------------------------------

st.subheader(
    "💵 Free Cash Flow Analysis"
)


if "free_cash_flow" in df.columns:


    fcf_df = (
        df[
            [
                "company_name",
                "free_cash_flow"
            ]
        ]
        .dropna()
        .sort_values(
            "free_cash_flow",
            ascending=False
        )
    )


    st.bar_chart(
        fcf_df.set_index(
            "company_name"
        )
    )


    st.dataframe(
        fcf_df,
        use_container_width=True
    )


else:

    st.info(
        "Free cash flow data not available."
    )



# -------------------------------------------------
# Debt Analysis
# -------------------------------------------------

st.divider()

st.subheader(
    "🏦 Debt Analysis"
)


if "total_debt" in df.columns:


    debt_df = (
        df[
            [
                "company_name",
                "total_debt"
            ]
        ]
        .dropna()
        .sort_values(
            "total_debt",
            ascending=False
        )
    )


    st.dataframe(
        debt_df,
        use_container_width=True
    )


else:

    st.info(
        "Debt information not available."
    )



# -------------------------------------------------
# Capital Efficiency Metrics
# -------------------------------------------------

st.divider()

st.subheader(
    "📈 Capital Efficiency"
)


columns = []


for col in [
    "roe",
    "return_on_equity_pct",
    "asset_turnover",
    "debt_to_equity"
]:

    if col in df.columns:

        columns.append(col)



if columns:


    st.dataframe(
        df[
            ["company_name"] + columns
        ],
        use_container_width=True
    )


else:

    st.info(
        "Capital efficiency metrics unavailable."
    )



# -------------------------------------------------
# Export
# -------------------------------------------------

csv = df.to_csv(
    index=False
)


st.download_button(
    label="⬇ Download Capital Data",
    data=csv,
    file_name="capital_analysis.csv",
    mime="text/csv"
)