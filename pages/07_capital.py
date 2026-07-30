import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_market_cap,
    get_financial_ratios
)

st.title("💰 Capital Allocation")

market = get_market_cap()
ratios = get_financial_ratios()

companies = sorted(market["company_id"].unique())

company = st.selectbox(
    "Select Company",
    companies
)

market_data = market[
    market["company_id"] == company
].sort_values("year")

ratio_data = ratios[
    ratios["company_id"] == company
].sort_values("year")

st.subheader("Valuation Metrics")

if not market_data.empty:

    latest = market_data.iloc[-1]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Market Cap",
        f"{latest['market_cap_crore']:,.0f} Cr"
    )

    c2.metric(
        "Enterprise Value",
        f"{latest['enterprise_value_crore']:,.0f} Cr"
    )

    c3.metric(
        "Dividend Yield",
        f"{latest['dividend_yield_pct']:.2f}%"
    )

st.divider()

if not ratio_data.empty:

    fig = px.line(
        ratio_data,
        x="year",
        y=[
            "free_cash_flow_cr",
            "cash_from_operations_cr"
        ],
        markers=True,
        title="Cash Flow Trend"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.subheader("Financial Metrics")

if not ratio_data.empty:

    st.dataframe(
        ratio_data[
            [
                "year",
                "free_cash_flow_cr",
                "cash_from_operations_cr",
                "total_debt_cr",
                "debt_to_equity"
            ]
        ],
        width="stretch"
    )