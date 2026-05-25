# 01_Dashboard.py
# This is the Market Overview dashboard page.
# It shows the current values of the major market indices.

import streamlit as st
from services.market_data import get_market_overview

st.set_page_config(page_title="Dashboard", page_icon="📊", layout="wide")

st.title("📊 Market Overview")
st.markdown("Live data from major market indices.")

# Fetch the market data
with st.spinner("Loading market data..."):
    indices = get_market_overview()

# Display each index as a metric card
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

for i, index in enumerate(indices):
    with columns[i]:
        if "error" not in index:
            change = index["change_percent"]
            # Format the change as a percentage
            change_display = f"{change * 100:.2f}%" if isinstance(change, float) else "N/A"
            st.metric(
                label=index["name"],
                value=f"${index['price']:,.2f}",
                delta=change_display
            )
        else:
            st.error(f"{index['name']}: Error loading data")