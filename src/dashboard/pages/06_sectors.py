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
    page_title="Sector Analysis",
    page_icon="🏢",
    layout="wide"
)


st.title("🏢 Sector Analysis Dashboard")

st.write(
    "Analyze Nifty 100 companies across different sectors."
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
        f"Unable to load sector data: {e}"
    )

    st.stop()



# -------------------------------------------------
# Sector Summary
# -------------------------------------------------

st.subheader(
    "📊 Sector Distribution"
)


if "sector" in df.columns:


    sector_count = (
        df["sector"]
        .value_counts()
        .reset_index()
    )


    sector_count.columns = [
        "Sector",
        "Companies"
    ]


    st.bar_chart(
        sector_count.set_index(
            "Sector"
        )
    )


else:

    st.warning(
        "Sector information not available."
    )



# -------------------------------------------------
# Sector Filter
# -------------------------------------------------

st.divider()

st.subheader(
    "🔍 Explore Sector Companies"
)


if "sector" in df.columns:


    selected_sector = st.selectbox(
        "Select Sector",
        df["sector"]
        .dropna()
        .unique()
    )


    sector_df = df[
        df["sector"] == selected_sector
    ]


    st.metric(
        "Companies in Sector",
        len(sector_df)
    )


    st.dataframe(
        sector_df,
        use_container_width=True
    )


    csv = sector_df.to_csv(
        index=False
    )


    st.download_button(
        label="⬇ Download Sector Data",
        data=csv,
        file_name=f"{selected_sector}_companies.csv",
        mime="text/csv"
    )


else:

    st.info(
        "No sector data available."
    )