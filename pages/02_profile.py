import streamlit as st

from dashboard.utils.db import (
    get_companies,
    get_financial_ratios,
    get_market_cap,
    get_sectors,
)

st.title("🏢 Company Profile")

companies = get_companies()
ratios = get_financial_ratios()
market = get_market_cap()
sectors = get_sectors()

company_list = sorted(companies["company_name"].tolist())

selected_company = st.selectbox(
    "Select Company",
    company_list
)

company = companies[
    companies["company_name"] == selected_company
].iloc[0]

st.header(company["company_name"])

col1, col2 = st.columns(2)

col1.write(f"**Company ID:** {company['company_id']}")
col1.write(f"**Symbol:** {company['symbol']}")

col2.write(f"**Sector:** {company['sector']}")
col2.write(f"**Industry:** {company['industry']}")

market_data = market[
    market["company_id"] == company["symbol"]
]

if not market_data.empty:

    latest = market_data.sort_values("year").iloc[-1]

    st.subheader("Latest Valuation")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Market Cap",
        f"{latest['market_cap_crore']:,.0f} Cr"
    )

    c2.metric(
        "P/E Ratio",
        round(latest["pe_ratio"], 2)
    )

    c3.metric(
        "P/B Ratio",
        round(latest["pb_ratio"], 2)
    )

ratio_data = ratios[
    ratios["company_id"] == company["symbol"]
]

if not ratio_data.empty:

    st.subheader("Financial Ratios")

    st.dataframe(
        ratio_data,
        width="stretch"
    )

sector = sectors[
    sectors["company_id"] == company["symbol"]
]

if not sector.empty:

    st.subheader("Sector Details")

    st.dataframe(
        sector,
        width="stretch"
    )