from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src.data.stock_data import get_stock_data
from src.data.summarization import summarize_text

app = FastAPI(
    title="Stock Dashboard API",
    description="API for stock data and text summarization",
    version="1.0.0"
)

# Enable CORS for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SummarizeRequest(BaseModel):
    text: str
    max_length: int = 150
    min_length: int = 50


class StockDataRequest(BaseModel):
    symbol: str
    period: str


@app.get("/")
async def root():
    return {"message": "Stock Dashboard API", "version": "1.0.0"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/api/summarize")
async def summarize(request: SummarizeRequest):
    """
    Summarize text using transformer model
    """
    try:
        summary = summarize_text(
            request.text,
            request.max_length,
            request.min_length
        )
        return {"summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/stock-data")
async def get_stock_data_endpoint(request: StockDataRequest):
    """
    Get stock data for a given symbol and period
    """
    try:
        df = get_stock_data(request.symbol, request.period)
        
        if df is None or df.empty:
            raise HTTPException(
                status_code=404, 
                detail=f"No data available for symbol {request.symbol} for period {request.period}"
            )
        
        # Convert DataFrame to JSON-serializable format
        # Convert datetime index to string for JSON serialization
        df_dict = df.to_dict(orient="index")
        data = {
            "symbol": request.symbol,
            "period": request.period,
            "data": {str(k): v for k, v in df_dict.items()},
            "columns": list(df.columns)
        }
        return data
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        error_detail = f"Error fetching stock data: {str(e)}"
        print(f"Stock data error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_detail)


@app.get("/api/stock-data/{symbol}")
async def get_stock_data_get(symbol: str, period: str = "1mo"):
    """
    Get stock data via GET request
    """
    try:
        df = get_stock_data(symbol, period)
        
        if df is None or df.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data available for symbol {symbol} for period {period}"
            )
        
        df_dict = df.to_dict(orient="index")
        data = {
            "symbol": symbol,
            "period": period,
            "data": {str(k): v for k, v in df_dict.items()},
            "columns": list(df.columns)
        }
        return data
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        import traceback
        error_detail = f"Error fetching stock data: {str(e)}"
        print(f"Stock data error: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=error_detail)

