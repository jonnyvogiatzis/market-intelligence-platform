# 02_Stock_Detail.py
# This page lets users search for any stock and see:
# - Key company info and current price
# - An interactive price chart

import streamlit as st
import plotly.graph_objects as go
from services.market_data import get_stock_info, get_stock_history

st.set_page_config(page_title="Stock Detail", page_icon="🔍", layout="wide")

st.title("🔍 Stock Detail")
st.markdown("Search for any stock to see live data and price history.")

# Search input
ticker = st.text_input("Enter a stock ticker symbol:", placeholder="e.g. AAPL, TSLA, MSFT").upper()

if ticker:
    # Fetch stock info
    with st.spinner(f"Loading data for {ticker}..."):
        info = get_stock_info(ticker)
        history = get_stock_history(ticker, period="3mo")

    if "error" in info:
        st.error(f"Could not find data for '{ticker}'. Please check the ticker symbol.")
    else:
        # Display company header
        st.subheader(f"{info['name']} ({info['symbol']})")

        # Display key metrics in columns
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Current Price", f"${info['price']:,.2f}" if isinstance(info['price'], float) else info['price'])
        with col2:
            st.metric("Market Cap", f"${info['market_cap']:,.0f}" if isinstance(info['market_cap'], int) else "N/A")
        with col3:
            st.metric("Sector", info['sector'])
        with col4:
            st.metric("Industry", info['industry'])

        # Display price chart
        st.markdown("### Price History (3 Months)")

        if history is not None and not history.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=history.index,
                y=history['Close'],
                mode='lines',
                name='Close Price',
                line=dict(color='#00b4d8', width=2)
            ))
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (USD)",
                template="plotly_dark",
                height=400,
                margin=dict(l=0, r=0, t=0, b=0)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No historical data available for this ticker.")

        # Company details
        st.markdown("### Company Details")
        st.write(f"**Website:** {info['website']}")