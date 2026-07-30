import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

# Project root
ROOT_DIR = Path(__file__).resolve().parents[3]

DB_PATH = ROOT_DIR / "database" / "nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


@st.cache_data
def get_companies():
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT *
        FROM companies
        ORDER BY company_name
        """,
        conn,
    )
    conn.close()
    return df


@st.cache_data
def get_total_companies():
    conn = get_connection()
    total = pd.read_sql(
        """
        SELECT COUNT(*) AS total
        FROM companies
        """,
        conn,
    )["total"][0]
    conn.close()
    return total


@st.cache_data
def get_ratios():
    conn = get_connection()
    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn,
    )
    conn.close()
    return df