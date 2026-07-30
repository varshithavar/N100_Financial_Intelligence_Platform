import streamlit as st

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📈 Nifty 100 Financial Intelligence Platform")
st.markdown("### Sprint 4 Dashboard")

st.success("Dashboard loaded successfully!")

st.sidebar.title("Navigation")
st.sidebar.info(
    """
    Use the sidebar to navigate between pages.

    - Home
    - Company Profile
    - Screener
    - Peer Comparison
    - Trend Analysis
    - Sector Analysis
    - Capital Allocation
    - Annual Reports
    """
)