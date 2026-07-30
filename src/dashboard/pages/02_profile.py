import streamlit as st
import plotly.express as px

from utils.db import get_companies, get_ratios

st.title("🏢 Company Profile")

companies = get_companies()
ratios = get_ratios()

data = companies.merge(ratios, on="company_id", how="left")

company = st.selectbox(
    "Select Company",
    sorted(data["company_name"].unique())
)

row = data[data["company_name"] == company].iloc[0]


def safe(value):
    if value is None:
        return "N/A"
    try:
        if str(value) == "nan":
            return "N/A"
        return round(float(value), 2)
    except:
        return "N/A"


st.header(company)

col1, col2 = st.columns(2)

with col1:
    st.metric("Symbol", row["symbol"])
    st.metric("Sector", row["sector"])

with col2:
    st.metric("Net Profit Margin", safe(row["net_profit_margin_pct"]))
    st.metric("ROE", safe(row["return_on_equity_pct"]))

st.divider()

st.subheader("Financial Ratios")

ratio_df = row[
    [
        "net_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "asset_turnover"
    ]
].fillna(0)

chart = px.bar(
    x=ratio_df.index,
    y=ratio_df.values,
    labels={"x": "Ratio", "y": "Value"},
    title=f"{company} Financial Ratios"
)

st.plotly_chart(chart, use_container_width=True)

st.divider()

st.subheader("Complete Company Data")

st.dataframe(
    data[data["company_name"] == company],
    use_container_width=True,
    hide_index=True
)