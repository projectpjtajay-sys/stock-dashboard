# Stock Dashboard Streamlit App

This Streamlit application provides an interactive dashboard to:

- Visualize stock price trends and trading volume using Plotly charts.
- Summarize stock-related news or reports using state-of-the-art NLP models.

---

## Features

### Stock Visualization
- Select **multiple stock symbols** (e.g., AAPL, MSFT, TSLA)
- Choose from multiple time periods (e.g., 1mo, 6mo, 1y)
- View:
  - Current stock price
  - Price change and percentage change
  - Line chart of historical stock prices
  - Volume bar chart

### Text Summarization
- Paste **news articles, financial reports, or analysis**
- Customize **summary length** (min/max words)
- Get clean summaries powered by HuggingFace’s `facebook/bart-large-cnn` model

---

## Setup Instructions

## 1. Install Dependencies
pip install -r requirements.txt

## 2. Create a .env File
ALPHA_VANTAGE_API_KEY=your_api_key_here

## 3. Run the Streamlit App
streamlit run app/main.py

---