import streamlit as st

from dashboard.utils.db import (
    get_peer_groups,
    get_market_cap,
    get_financial_ratios,
)

st.title("👥 Peer Comparison")

peers = get_peer_groups()
market = get_market_cap()
ratios = get_financial_ratios()

peer_groups = sorted(peers["peer_group_name"].unique())

selected_group = st.selectbox(
    "Select Peer Group",
    peer_groups
)

peer_companies = peers[
    peers["peer_group_name"] == selected_group
]

market_data = market.merge(
    peer_companies,
    on="company_id",
    how="inner"
)

ratio_data = ratios.merge(
    peer_companies,
    on="company_id",
    how="inner"
)

st.subheader("Peer Companies")

st.dataframe(
    peer_companies,
    width="stretch"
)

st.subheader("Market Valuation")

st.dataframe(
    market_data[
        [
            "company_id",
            "year",
            "market_cap_crore",
            "pe_ratio",
            "pb_ratio",
            "dividend_yield_pct"
        ]
    ],
    width="stretch"
)

st.subheader("Financial Ratios")

st.dataframe(
    ratio_data[
        [
            "company_id",
            "year",
            "return_on_equity_pct",
            "net_profit_margin_pct",
            "debt_to_equity",
            "interest_coverage"
        ]
    ],
    width="stretch"
)