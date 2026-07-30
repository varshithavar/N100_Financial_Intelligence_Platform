import sqlite3
import pandas as pd
import streamlit as st

DB_PATH = "database/nifty100.db"

RAW_PATH = "data/raw"
SUPPORTING_PATH = "data/supporting"


def get_connection():
    return sqlite3.connect(DB_PATH)


# ==========================
# DATABASE FUNCTIONS
# ==========================

@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    df = pd.read_sql(
        "SELECT * FROM companies ORDER BY company_name",
        conn
    )
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_sector_counts():
    conn = get_connection()

    df = pd.read_sql("""
        SELECT sector,
               COUNT(*) AS company_count
        FROM companies
        GROUP BY sector
        ORDER BY sector
    """, conn)

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_total_companies():
    conn = get_connection()

    total = pd.read_sql(
        "SELECT COUNT(*) AS total FROM companies",
        conn
    ).iloc[0]["total"]

    conn.close()
    return total


# ==========================
# RAW EXCEL DATASETS
# ==========================

@st.cache_data(ttl=600)
def get_raw_companies():
    return pd.read_excel(
        f"{RAW_PATH}/companies.xlsx",
        header=1
    )


@st.cache_data(ttl=600)
def get_analysis():
    return pd.read_excel(
        f"{RAW_PATH}/analysis.xlsx",
        header=1
    )


@st.cache_data(ttl=600)
def get_profit_loss():
    return pd.read_excel(
        f"{RAW_PATH}/profitandloss.xlsx",
        header=1
    )


@st.cache_data(ttl=600)
def get_balance_sheet():
    return pd.read_excel(
        f"{RAW_PATH}/balancesheet.xlsx",
        header=1
    )


@st.cache_data(ttl=600)
def get_cash_flow():
    return pd.read_excel(
        f"{RAW_PATH}/cashflow.xlsx",
        header=1
    )


@st.cache_data(ttl=600)
def get_documents():
    return pd.read_excel(
        f"{RAW_PATH}/documents.xlsx",
        header=1
    )


@st.cache_data(ttl=600)
def get_pros_cons():
    return pd.read_excel(
        f"{RAW_PATH}/prosandcons.xlsx",
        header=1
    )


# ==========================
# SUPPORTING DATASETS
# ==========================

@st.cache_data(ttl=600)
def get_financial_ratios():
    return pd.read_excel(
        f"{SUPPORTING_PATH}/financial_ratios.xlsx"
    )


@st.cache_data(ttl=600)
def get_market_cap():
    return pd.read_excel(
        f"{SUPPORTING_PATH}/market_cap.xlsx"
    )


@st.cache_data(ttl=600)
def get_peer_groups():
    return pd.read_excel(
        f"{SUPPORTING_PATH}/peer_groups.xlsx"
    )


@st.cache_data(ttl=600)
def get_sectors():
    return pd.read_excel(
        f"{SUPPORTING_PATH}/sectors.xlsx"
    )


@st.cache_data(ttl=600)
def get_stock_prices():
    return pd.read_excel(
        f"{SUPPORTING_PATH}/stock_prices.xlsx"
    )