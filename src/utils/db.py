import sqlite3
import pandas as pd
import streamlit as st

# Database path
DB_PATH = "database/nifty100.db"


def get_connection():
    """Create and return a SQLite connection."""
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def get_companies():
    conn = get_connection()
    df = pd.read_sql("SELECT * FROM companies", conn)
    conn.close()
    return df


@st.cache_data(ttl=600)
def get_valuation():
    """
    Placeholder for Day 26 valuation module.
    """
    return pd.DataFrame()

    query = """
        SELECT *
        FROM financial_ratios
        WHERE 1=1
    """

    params = []

    if ticker:
        query += " AND company_id = (SELECT company_id FROM companies WHERE symbol = ?)"
        params.append(ticker)

    if year:
        query += " AND financial_year = ?"
        params.append(year)

    df = pd.read_sql(query, conn, params=params)

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_pl(ticker):
    conn = get_connection()

    query = """
        SELECT pl.*
        FROM profit_loss pl
        JOIN companies c
        ON pl.company_id = c.company_id
        WHERE c.symbol = ?
        ORDER BY financial_year
    """

    df = pd.read_sql(query, conn, params=[ticker])

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_bs(ticker):
    conn = get_connection()

    query = """
        SELECT bs.*
        FROM balance_sheet bs
        JOIN companies c
        ON bs.company_id = c.company_id
        WHERE c.symbol = ?
        ORDER BY financial_year
    """

    df = pd.read_sql(query, conn, params=[ticker])

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_cf(ticker):
    conn = get_connection()

    query = """
        SELECT cf.*
        FROM cash_flow cf
        JOIN companies c
        ON cf.company_id = c.company_id
        WHERE c.symbol = ?
        ORDER BY financial_year
    """

    df = pd.read_sql(query, conn, params=[ticker])

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_sectors():
    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT sector,
               COUNT(*) AS company_count
        FROM companies
        GROUP BY sector
        ORDER BY sector
        """,
        conn,
    )

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_peers(group_name):
    conn = get_connection()

    query = """
        SELECT *
        FROM companies
        WHERE sector = ?
    """

    df = pd.read_sql(query, conn, params=[group_name])

    conn.close()
    return df


@st.cache_data(ttl=600)
def get_valuation(ticker=None):
    conn = get_connection()

    query = """
        SELECT *
        FROM valuation
        WHERE 1=1
    """

    params = []

    if ticker:
        query += " AND company_id = (SELECT company_id FROM companies WHERE symbol = ?)"
        params.append(ticker)

    df = pd.read_sql(query, conn, params=params)

    conn.close()
    return df