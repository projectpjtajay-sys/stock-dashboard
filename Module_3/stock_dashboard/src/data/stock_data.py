import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_stock_data(symbol: str, period: str) -> pd.DataFrame:
    """
    Fetch stock data from Alpha Vantage (free endpoint)
    """
    API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

    function = "TIME_SERIES_DAILY"  # ✅ Use free endpoint
    outputsize = "compact" if period in ["1d", "5d", "1mo"] else "full"

    url = "https://www.alphavantage.co/query"
    params = {
        "function": function,
        "symbol": symbol,
        "outputsize": outputsize,
        "apikey": API_KEY,
        "datatype": "json"
    }

    try:
        response = requests.get(url, params=params)
        print("Raw Response:", response.text[:500])  # Debug: Print partial response
        data = response.json()

        if "Time Series (Daily)" not in data:
            raise ValueError(f"Alpha Vantage error: {data.get('Note') or data.get('Error Message') or 'Unknown error'}")

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

    except Exception as e:
        raise Exception(f"Error loading stock data: {e}")
