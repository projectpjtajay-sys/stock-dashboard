"""
API client utility to switch between direct function calls and FastAPI backend
"""
import os
import requests
import pandas as pd
from typing import Optional

# Check if we should use API (set USE_API=true in environment)
USE_API = os.getenv("USE_API", "false").lower() == "true"
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")


def get_stock_data_via_api(symbol: str, period: str) -> pd.DataFrame:
    """Get stock data via FastAPI"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/stock-data",
            json={"symbol": symbol, "period": period},
            timeout=30
        )
        
        # Check for HTTP errors
        if response.status_code == 404:
            raise ValueError(f"No data available for {symbol}")
        elif response.status_code == 400:
            error_data = response.json() if response.content else {}
            raise ValueError(error_data.get("detail", f"Bad request for {symbol}"))
        elif response.status_code >= 400:
            error_data = response.json() if response.content else {}
            error_msg = error_data.get("detail", f"Server error: {response.status_code}")
            raise Exception(f"API error: {error_msg}")
        
        response.raise_for_status()
        data = response.json()
        
        if not data.get("data"):
            raise ValueError(f"No data returned for {symbol}")
        
        # Convert back to DataFrame
        df = pd.DataFrame.from_dict(data["data"], orient="index")
        df.index = pd.to_datetime(df.index)
        df.sort_index(inplace=True)
        
        if df.empty:
            raise ValueError(f"Empty dataset for {symbol}")
        
        return df
    except requests.exceptions.Timeout:
        raise Exception(f"Request timeout: API took too long to respond for {symbol}")
    except requests.exceptions.ConnectionError:
        raise Exception(f"Connection error: Cannot reach API at {API_BASE_URL}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


def summarize_text_via_api(text: str, max_length: int, min_length: int) -> str:
    """Summarize text via FastAPI"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/api/summarize",
            json={
                "text": text,
                "max_length": max_length,
                "min_length": min_length
            },
            timeout=120  # Longer timeout for summarization
        )
        response.raise_for_status()
        data = response.json()
        return data["summary"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


def get_stock_data(symbol: str, period: str) -> pd.DataFrame:
    """Get stock data - uses API if enabled, otherwise direct call"""
    if USE_API:
        return get_stock_data_via_api(symbol, period)
    else:
        # Direct import and call
        from src.data.stock_data import get_stock_data as get_stock_data_direct
        return get_stock_data_direct(symbol, period)


def summarize_text(text: str, max_length: int, min_length: int) -> str:
    """Summarize text - uses API if enabled, otherwise direct call"""
    if USE_API:
        return summarize_text_via_api(text, max_length, min_length)
    else:
        # Direct import and call
        from src.data.summarization import summarize_text as summarize_text_direct
        return summarize_text_direct(text, max_length, min_length)

