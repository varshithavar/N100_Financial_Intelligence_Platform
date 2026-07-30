import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_companies,
    get_financial_ratios,
    get_sectors,
    get_market_cap
)

st.title("🏠 Nifty 100 Dashboard")

companies = get_companies()
ratios = get_financial_ratios()
sectors = get_sectors()
market = get_market_cap()

# Sidebar
year = st.sidebar.selectbox(
    "Financial Year",
    sorted(market["year"].unique(), reverse=True)
)

ratios = ratios[ratios["year"] == year]
market = market[market["year"] == year]

# KPI Cards
col1, col2, col3 = st.columns(3)

col1.metric("Companies", len(companies))

col2.metric(
    "Average ROE",
    f"{ratios['return_on_equity_pct'].mean():.2f}%"
)

col3.metric(
    "Median P/E",
    f"{market['pe_ratio'].median():.2f}"
)

col4, col5, col6 = st.columns(3)

col4.metric(
    "Median D/E",
    f"{ratios['debt_to_equity'].median():.2f}"
)

col5.metric(
    "Average Dividend Yield",
    f"{market['dividend_yield_pct'].mean():.2f}%"
)

col6.metric(
    "Total Sectors",
    sectors["broad_sector"].nunique()
)

st.divider()

st.subheader("Sector Distribution")

sector_counts = (
    sectors.groupby("broad_sector")
    .size()
    .reset_index(name="Companies")
)

fig = px.pie(
    sector_counts,
    names="broad_sector",
    values="Companies",
    hole=0.5
)

st.plotly_chart(fig, width="stretch")

st.subheader("Top 10 Companies by Market Cap")

top = market.sort_values(
    "market_cap_crore",
    ascending=False
).head(10)

st.dataframe(
    top[
        [
            "company_id",
            "market_cap_crore",
            "pe_ratio",
            "pb_ratio"
        ]
    ],
    width="stretch"
)