import os
import sys
import importlib.util
import streamlit as st

# Add project root to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

st.set_page_config(
    page_title="Nifty 100 Financial Intelligence Platform",
    page_icon="📊",
    layout="wide",
)

st.sidebar.title("Navigation")

pages = {
    "🏠 Home": "01_home.py",
    "🏢 Company Profile": "02_profile.py",
    "📈 Screener": "03_screener.py",
    "🤝 Peer Comparison": "04_peers.py",
    "📊 Trend Analysis": "05_trends.py",
    "🏭 Sector Analysis": "06_sectors.py",
    "💰 Capital Allocation": "07_capital.py",
    "📄 Reports": "08_reports.py",
}

selected = st.sidebar.radio(
    "Go to",
    list(pages.keys())
)

page_path = os.path.join(PROJECT_ROOT, "pages", pages[selected])

spec = importlib.util.spec_from_file_location("page", page_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)