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