#!/bin/bash

# Start FastAPI in the background
echo "Starting FastAPI server on port 8000..."
uvicorn api.main:app --host 0.0.0.0 --port 8000 &

# Wait a moment for FastAPI to start
sleep 2

# Start Streamlit in the foreground
echo "Starting Streamlit app on port 8501..."
streamlit run app/main.py --server.port=8501 --server.address=0.0.0.0



