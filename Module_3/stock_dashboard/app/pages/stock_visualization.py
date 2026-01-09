import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys
import os

# Add project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)
print(f"Project root (stock_visualization.py): {project_root}")
print(f"sys.path (stock_visualization.py): {sys.path}")

from src.utils.api_client import get_stock_data

st.title("Stock Price Visualization")

@st.cache_data(ttl=300)  # Cache for 5 minutes
def load_stock_data(symbol, period):
    try:
        return get_stock_data(symbol, period)
    except Exception as e:
        # Re-raise with more context
        raise Exception(f"Failed to load data for {symbol}: {str(e)}")

# Sidebar controls
st.sidebar.header("Stock Selection")
available_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX"]  # You can add more
symbols = st.sidebar.multiselect(
    "Select Stock Symbols",
    options=available_symbols,
    default=["AAPL"]
)

# Period options that work reliably with yfinance
period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "ytd", "max"]
period = st.sidebar.selectbox("Select Period", period_options, index=2)  # Default to 1mo

# Iterate over each symbol and render the section
for symbol in symbols:
    st.subheader(f"{symbol} Stock Visualization")

    try:
        df = load_stock_data(symbol, period)

        if df is None or df.empty:
            st.warning(f"No data found for {symbol}")
            continue

        # Display metrics
        col1, col2, col3 = st.columns(3)
        latest_price = df['Close'].iloc[-1]
        price_change = df['Close'].iloc[-1] - df['Close'].iloc[0]
        price_change_pct = (price_change / df['Close'].iloc[0]) * 100

        with col1:
            st.metric("Current Price", f"${latest_price:.2f}")
        with col2:
            st.metric("Price Change", f"${price_change:.2f}")
        with col3:
            st.metric("Change %", f"{price_change_pct:.2f}%")

        # Price chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index,
            y=df['Close'],
            name='Close Price',
            line=dict(color='#1f77b4')
        ))
        fig.update_layout(
            title=f"{symbol} Stock Price",
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white",
            hovermode="x unified"
        )
        st.plotly_chart(fig, use_container_width=True)

        # Volume chart
        fig_volume = px.bar(df, x=df.index, y='Volume')
        fig_volume.update_layout(
            title=f"{symbol} Trading Volume",
            xaxis_title="Date",
            yaxis_title="Volume",
            template="plotly_white"
        )
        st.plotly_chart(fig_volume, use_container_width=True)

    except Exception as e:
        error_msg = str(e)
        # Provide user-friendly error messages
        if "API request failed" in error_msg:
            st.error(f"⚠️ Unable to fetch data for {symbol}. The API service may be temporarily unavailable. Please try again in a moment.")
        elif "No data" in error_msg or "not found" in error_msg.lower():
            st.warning(f"ℹ️ No data available for {symbol}. Please check if the symbol is correct.")
        else:
            st.error(f"❌ Error loading data for {symbol}: {error_msg}")
        
        # Show retry suggestion
        if st.button(f"🔄 Retry {symbol}", key=f"retry_{symbol}"):
            st.cache_data.clear()
            st.rerun()
