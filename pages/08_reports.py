import streamlit as st

from dashboard.utils.db import (
    get_companies,
    get_financial_ratios,
    get_market_cap,
    get_peer_groups,
    get_sectors,
)

st.title("📄 Reports & Downloads")

companies = get_companies()
ratios = get_financial_ratios()
market = get_market_cap()
peers = get_peer_groups()
sectors = get_sectors()

st.header("Dataset Preview")

dataset = st.selectbox(
    "Select Dataset",
    [
        "Companies",
        "Financial Ratios",
        "Market Cap",
        "Peer Groups",
        "Sectors"
    ]
)

if dataset == "Companies":
    df = companies

elif dataset == "Financial Ratios":
    df = ratios

elif dataset == "Market Cap":
    df = market

elif dataset == "Peer Groups":
    df = peers

else:
    df = sectors

st.dataframe(
    df,
    width="stretch"
)

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label=f"Download {dataset}",
    data=csv,
    file_name=f"{dataset.lower().replace(' ','_')}.csv",
    mime="text/csv",
)