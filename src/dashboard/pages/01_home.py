import streamlit as st
import plotly.express as px

from utils.db import (
    get_companies,
    get_total_companies,
    get_ratios
)

st.set_page_config(
    page_title="Dashboard Home",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 Dashboard Home")

# -----------------------
# Load Data
# -----------------------

companies = get_companies()
ratios = get_ratios()

chart_data = companies.merge(ratios, on="company_id", how="left")

# -----------------------
# KPI Cards
# -----------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Companies",
        get_total_companies()
    )

with col2:
    st.metric(
        "Financial Ratio Records",
        len(ratios)
    )

with col3:
    avg_margin = chart_data["net_profit_margin_pct"].mean()

    if avg_margin == avg_margin:
        st.metric(
            "Average Net Profit Margin",
            f"{avg_margin:.2f}%"
        )
    else:
        st.metric(
            "Average Net Profit Margin",
            "N/A"
        )

st.divider()

# -----------------------
# Net Profit Margin Chart
# -----------------------

st.subheader("📊 Net Profit Margin by Company")

fig = px.bar(
    chart_data,
    x="company_name",
    y="net_profit_margin_pct",
    text="net_profit_margin_pct",
    title="Net Profit Margin (%)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
st.divider()

st.subheader("📈 Return on Equity (ROE) by Company")

fig2 = px.bar(
    chart_data,
    x="company_name",
    y="return_on_equity_pct",
    text="return_on_equity_pct",
    title="Return on Equity (%)"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.divider()

# -----------------------
# Companies Table
# -----------------------

st.subheader("🏢 Companies")

st.dataframe(
    companies,
    use_container_width=True,
    hide_index=True
)

st.divider()

# -----------------------
# Financial Ratios
# -----------------------

st.subheader("📈 Financial Ratios")

st.dataframe(
    ratios,
    use_container_width=True,
    hide_index=True
)