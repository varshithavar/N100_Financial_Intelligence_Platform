import sqlite3
import pandas as pd
import streamlit as st


DB_PATH = "database/nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data(ttl=600)
def get_companies():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_ratios():

    conn = get_connection()

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_sector_counts():

    conn = get_connection()

    df = pd.read_sql(
        """
        SELECT sector, COUNT(*) as count
        FROM companies
        GROUP BY sector
        """,
        conn
    )

    conn.close()

    return df


@st.cache_data(ttl=600)
def get_total_companies():

    conn = get_connection()

    count = pd.read_sql(
        "SELECT COUNT(*) as total FROM companies",
        conn
    )

    conn.close()

    return int(count.iloc[0]["total"])