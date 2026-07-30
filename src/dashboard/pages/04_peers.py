import streamlit as st
import pandas as pd
import sys
import os
import importlib


# -------------------------------------------------
# Add src folder to Python path
# -------------------------------------------------

SRC_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )
)

sys.path.insert(0, SRC_PATH)


from analytics.screener import merge_data


# Import peer analysis module
peer_module = importlib.import_module(
    "analytics.peer_analysis"
)


# -------------------------------------------------
# Page Config
# -------------------------------------------------

st.set_page_config(
    page_title="Peer Comparison",
    page_icon="👥",
    layout="wide"
)


st.title("👥 Peer Comparison Dashboard")

st.write(
    "Compare companies with peer groups using financial metrics."
)


# -------------------------------------------------
# Load company data
# -------------------------------------------------

@st.cache_data(ttl=600)
def load_data():

    return merge_data()



try:

    df = load_data()

except Exception as e:

    st.error(
        f"Data loading failed: {e}"
    )

    st.stop()



# -------------------------------------------------
# Company Selection
# -------------------------------------------------

company = st.selectbox(
    "Select Company",
    df["company_name"].unique()
)


selected_company = df[
    df["company_name"] == company
]


# -------------------------------------------------
# Find peer function automatically
# -------------------------------------------------

peer_result = None


possible_functions = [
    "generate_peer_comparison",
    "build_peer_comparison",
    "peer_analysis",
    "calculate_peer_percentiles",
    "peer_percentile",
    "get_peer_comparison"
]


for func_name in possible_functions:

    if hasattr(peer_module, func_name):

        peer_function = getattr(
            peer_module,
            func_name
        )

        try:

            peer_result = peer_function(
                df,
                company
            )

            break

        except Exception:

            try:

                peer_result = peer_function(
                    df
                )

                break

            except Exception:
                continue



# -------------------------------------------------
# Display Results
# -------------------------------------------------

st.subheader(
    f"📊 Peer Analysis - {company}"
)


if peer_result is not None:

    if isinstance(
        peer_result,
        pd.DataFrame
    ):

        st.dataframe(
            peer_result,
            use_container_width=True
        )

    else:

        st.write(peer_result)


else:

    st.warning(
        "No peer comparison function found in peer_analysis.py"
    )



# -------------------------------------------------
# Company Details
# -------------------------------------------------

st.divider()

st.subheader(
    "Company Financial Metrics"
)


st.dataframe(
    selected_company,
    use_container_width=True
)



# -------------------------------------------------
# Download
# -------------------------------------------------

csv = selected_company.to_csv(
    index=False
)


st.download_button(
    label="⬇ Download Company Data",
    data=csv,
    file_name=f"{company}_peer_data.csv",
    mime="text/csv"
)