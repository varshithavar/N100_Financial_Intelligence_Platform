@st.cache_data(ttl=600)
def get_documents():
    return pd.read_excel(
        f"{RAW_PATH}/documents.xlsx",
        header=1
    )