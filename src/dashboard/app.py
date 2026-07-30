import streamlit as st

st.set_page_config(
    page_title="N100 Financial Intelligence Platform",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 N100 Financial Intelligence Platform")

st.markdown("""
Welcome to the **N100 Financial Intelligence Platform**.

Use the sidebar to navigate between dashboard pages.
""")

st.sidebar.success("Select a page above.")