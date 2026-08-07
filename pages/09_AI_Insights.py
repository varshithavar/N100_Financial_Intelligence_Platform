import streamlit as st
import pandas as pd
from pathlib import Path


# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="AI Insights",
    layout="wide"
)


st.title("🤖 AI Financial Insights")


# -----------------------------------
# Paths
# -----------------------------------

BASE_DIR = Path(__file__).resolve().parents[3]

PROS_FILE = BASE_DIR / "output" / "pros_cons_generated.csv"
SUMMARY_FILE = BASE_DIR / "output" / "company_summary.csv"


# -----------------------------------
# Load Data
# -----------------------------------

@st.cache_data
def load_data():

    pros = pd.read_csv(PROS_FILE)
    summary = pd.read_csv(SUMMARY_FILE)

    return pros, summary


pros, summary = load_data()


# -----------------------------------
# Company Selection
# -----------------------------------

company = st.selectbox(
    "Select Company",
    sorted(pros["company_name"].unique())
)


# -----------------------------------
# Filter Company
# -----------------------------------

company_pros = pros[
    (pros["company_name"] == company)
    &
    (pros["type"] == "pro")
]

company_cons = pros[
    (pros["company_name"] == company)
    &
    (pros["type"] == "con")
]


# -----------------------------------
# Display Insights
# -----------------------------------

st.subheader(company)


col1, col2 = st.columns(2)


with col1:

    st.success("✅ Strengths")

    for text in company_pros["text"]:
        st.write(text)

    st.metric(
        "Confidence",
        f"{company_pros['confidence_pct'].iloc[0]}%"
    )


with col2:

    st.error("⚠️ Risks")

    for text in company_cons["text"]:
        st.write(text)

    st.metric(
        "Confidence",
        f"{company_cons['confidence_pct'].iloc[0]}%"
    )


# -----------------------------------
# Summary
# -----------------------------------

st.subheader("Financial Summary")

company_summary = summary[
    summary["company_name"] == company
]


st.dataframe(
    company_summary,
    use_container_width=True
)