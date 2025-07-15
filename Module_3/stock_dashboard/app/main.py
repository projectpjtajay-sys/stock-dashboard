import streamlit as st
import sys
import os

# Add project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)
print(f"Project root (main.py): {project_root}")
print(f"sys.path (main.py): {sys.path}")

st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("Stock Market Analysis Dashboard")
st.markdown("""
Welcome to the Stock Market Analysis Dashboard! 
Use the sidebar to navigate between:
- Stock Visualization: View and analyze stock price trends
- Text Summarization: Summarize stock-related articles or text
""")