import streamlit as st
import plotly.express as px

from dashboard.utils.db import (
    get_sectors,
    get_market_cap,
    get_financial_ratios
)

st.title("🏭 Sector Analysis")

# Load data
sectors = get_sectors()
market = get_market_cap()
ratios = get_financial_ratios()

# ============================
# Sector Selection
# ============================

sector_list = sorted(sectors["broad_sector"].unique())

selected_sector = st.selectbox(
    "Select Sector",
    sector_list
)

sector_companies = sectors[
    sectors["broad_sector"] == selected_sector
]

st.subheader("Sector Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Companies",
    len(sector_companies)
)

col2.metric(
    "Average Index Weight",
    f"{sector_companies['index_weight_pct'].mean():.2f}%"
)

col3.metric(
    "Large Cap Companies",
    len(
        sector_companies[
            sector_companies["market_cap_category"] == "Large Cap"
        ]
    )
)

st.divider()

# ============================
# Market Cap Distribution
# ============================

market_sector = market.merge(
    sector_companies,
    on="company_id",
    how="inner"
)

if not market_sector.empty:

    latest_year = market_sector["year"].max()

    latest_market = market_sector[
        market_sector["year"] == latest_year
    ]

    fig = px.bar(
        latest_market.sort_values(
            "market_cap_crore",
            ascending=False
        ),
        x="company_id",
        y="market_cap_crore",
        color="company_id",
        title=f"{selected_sector} - Market Cap"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.divider()

# ============================
# ROE Distribution
# ============================

ratio_sector = ratios.merge(
    sector_companies,
    on="company_id",
    how="inner"
)

if not ratio_sector.empty:

    fig = px.box(
        ratio_sector,
        x="company_id",
        y="return_on_equity_pct",
        title=f"{selected_sector} - ROE Distribution"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )

st.divider()

st.subheader("Companies in Sector")

st.dataframe(
    sector_companies,
    width="stretch"
)