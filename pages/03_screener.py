import streamlit as st

from dashboard.utils.db import (
    get_financial_ratios,
    get_market_cap,
)

st.title("🔎 Stock Screener")

ratios = get_financial_ratios()
market = get_market_cap()

st.sidebar.header("Filters")

roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0.0,
    50.0,
    15.0,
)

pe = st.sidebar.slider(
    "Maximum P/E",
    0.0,
    100.0,
    30.0,
)

de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    1.0,
)

year = st.sidebar.selectbox(
    "Financial Year",
    sorted(market["year"].unique(), reverse=True)
)

ratios = ratios[ratios["year"] == year]
market = market[market["year"] == year]

data = ratios.merge(
    market,
    on=["company_id", "year"],
    how="inner"
)

filtered = data[
    (data["return_on_equity_pct"] >= roe)
    & (data["pe_ratio"] <= pe)
    & (data["debt_to_equity"] <= de)
]

st.subheader("Filtered Companies")

st.write(f"Total Companies: {len(filtered)}")

st.dataframe(
    filtered,
    width="stretch"
)

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "Download CSV",
    csv,
    "screener_results.csv",
    "text/csv",
)