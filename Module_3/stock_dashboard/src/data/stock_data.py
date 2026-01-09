import os
import requests
import pandas as pd
import yfinance as yf
from dotenv import load_dotenv

load_dotenv()

def get_stock_data(symbol: str, period: str) -> pd.DataFrame:
    """
    Fetch stock data using yfinance (primary) with Alpha Vantage as fallback
    yfinance is more reliable and doesn't have rate limits
    """
    # Map period to yfinance format
    period_map = {
        "1d": "1d",
        "5d": "5d",
        "1mo": "1mo",
        "3mo": "3mo",
        "6mo": "6mo",
        "1y": "1y",
        "ytd": "ytd",
        "max": "max"
    }
    
    yf_period = period_map.get(period, "1mo")
    
    try:
        # Use yfinance as primary source (more reliable, no API key needed)
        ticker = yf.Ticker(symbol)
        df = ticker.history(period=yf_period)
        
        if df is None or df.empty:
            raise ValueError(f"No data returned for {symbol}")
        
        # Rename columns to match expected format
        df = df.rename(columns={
            "Open": "Open",
            "High": "High",
            "Low": "Low",
            "Close": "Close",
            "Volume": "Volume"
        })
        
        # Ensure we have the required columns
        required_cols = ["Open", "High", "Low", "Close", "Volume"]
        if not all(col in df.columns for col in required_cols):
            raise ValueError(f"Missing required columns in data for {symbol}")
        
        # Select only required columns and ensure proper data types
        df = df[required_cols].copy()
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        
        return df
        
    except Exception as yf_error:
        # Fallback to Alpha Vantage if yfinance fails
        print(f"yfinance failed for {symbol}, trying Alpha Vantage fallback: {str(yf_error)}")
        
        try:
            API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
            if not API_KEY:
                raise ValueError("ALPHA_VANTAGE_API_KEY not set and yfinance failed")
            
            function = "TIME_SERIES_DAILY"
            outputsize = "compact"  # Free API only supports compact
            
            url = "https://www.alphavantage.co/query"
            params = {
                "function": function,
                "symbol": symbol,
                "outputsize": outputsize,
                "apikey": API_KEY,
                "datatype": "json"
            }
            
            response = requests.get(url, params=params, timeout=10)
            data = response.json()
            
            if "Time Series (Daily)" not in data:
                error_msg = data.get('Note') or data.get('Error Message') or 'Unknown error'
                raise ValueError(f"Alpha Vantage error: {error_msg}")
            
            # Parse JSON into DataFrame
            df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index", dtype=float)
            df = df.rename(columns={
                "1. open": "Open",
                "2. high": "High",
                "3. low": "Low",
                "4. close": "Close",
                "5. volume": "Volume"
            })
            df.index = pd.to_datetime(df.index)
            df.sort_index(inplace=True)
            
            return df
            
        except Exception as av_error:
            raise Exception(f"Both yfinance and Alpha Vantage failed for {symbol}. yfinance error: {str(yf_error)}, Alpha Vantage error: {str(av_error)}")
