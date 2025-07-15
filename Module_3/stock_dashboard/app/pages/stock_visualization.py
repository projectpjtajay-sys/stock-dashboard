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

from src.data.stock_data import get_stock_data

st.title("Stock Price Visualization")

@st.cache_data
def load_stock_data(symbol, period):
    return get_stock_data(symbol, period)

# Sidebar controls
st.sidebar.header("Stock Selection")
available_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", "NFLX"]  # You can add more
symbols = st.sidebar.multiselect(
    "Select Stock Symbols",
    options=available_symbols,
    default=["AAPL"]
)

period_options = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "ytd", "max"]
period = st.sidebar.selectbox("Select Period", period_options, index=4)

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
        st.error(f"Error loading data for {symbol}: {str(e)}")
