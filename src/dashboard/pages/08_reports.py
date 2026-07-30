import streamlit as st
import pandas as pd
import os


st.set_page_config(
    page_title="Reports",
    page_icon="📄",
    layout="wide"
)


st.title("📄 Financial Intelligence Reports")

st.write(
    "Download generated analytics reports and view valuation insights."
)


# -------------------------------------------------
# Valuation Report
# -------------------------------------------------

st.subheader("💰 Valuation Summary")


valuation_file = "output/valuation_summary.xlsx"


if os.path.exists(valuation_file):

    valuation_df = pd.read_excel(
        valuation_file
    )


    st.dataframe(
        valuation_df,
        use_container_width=True
    )


    # Valuation statistics

    if "valuation_flag" in valuation_df.columns:

        st.subheader("📊 Valuation Overview")


        col1, col2, col3 = st.columns(3)


        fair = (
            valuation_df["valuation_flag"]
            .value_counts()
            .get("Fair Value", 0)
        )

        undervalued = (
            valuation_df["valuation_flag"]
            .value_counts()
            .get("Undervalued", 0)
        )

        overvalued = (
            valuation_df["valuation_flag"]
            .value_counts()
            .get("Overvalued", 0)
        )


        col1.metric(
            "Undervalued",
            undervalued
        )

        col2.metric(
            "Fair Value",
            fair
        )

        col3.metric(
            "Overvalued",
            overvalued
        )


    # Download button

    with open(
        valuation_file,
        "rb"
    ) as file:

        st.download_button(
            label="⬇ Download Valuation Report",
            data=file,
            file_name="valuation_summary.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


else:

    st.warning(
        "Valuation report not found. Run valuation.py first."
    )



# -------------------------------------------------
# Screener Report
# -------------------------------------------------

st.divider()

st.subheader("🔎 Screener Report")


screener_file = "output/screener_output.xlsx"


if os.path.exists(screener_file):

    with open(
        screener_file,
        "rb"
    ) as file:

        st.download_button(
            label="⬇ Download Screener Report",
            data=file,
            file_name="screener_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:

    st.info(
        "Screener report not generated yet."
    )



# -------------------------------------------------
# Peer Comparison Report
# -------------------------------------------------

st.divider()

st.subheader("👥 Peer Comparison Report")


peer_file = "output/peer_comparison.xlsx"


if os.path.exists(peer_file):

    with open(
        peer_file,
        "rb"
    ) as file:

        st.download_button(
            label="⬇ Download Peer Comparison Report",
            data=file,
            file_name="peer_comparison.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

else:

    st.info(
        "Peer comparison report not generated yet."
    )