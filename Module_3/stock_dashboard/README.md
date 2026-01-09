# Stock Dashboard - FastAPI + Streamlit App

This application provides an interactive dashboard to:

- Visualize stock price trends and trading volume using Plotly charts.
- Summarize stock-related news or reports using state-of-the-art NLP models.

The application consists of:
- **FastAPI Backend**: REST API for stock data and text summarization
- **Streamlit Frontend**: Interactive web dashboard

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
- Get clean summaries powered by HuggingFace's `facebook/bart-large-cnn` model

### API Endpoints
- RESTful API for programmatic access
- Health check endpoint
- Swagger documentation at `/docs`

---

## Quick Start

### Local Development (Without Docker)

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Create a .env File**
```bash
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

3. **Run the Application**

Terminal 1 - Start FastAPI:
```bash
uvicorn api.main:app --reload --port 8000
```

Terminal 2 - Start Streamlit:
```bash
streamlit run app/main.py
```

Access:
- Streamlit UI: http://localhost:8501
- FastAPI API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Docker Deployment

1. **Create a .env File**
```bash
ALPHA_VANTAGE_API_KEY=your_api_key_here
```

2. **Build and Run with Docker Compose**
```bash
docker compose up --build
```

Or with Docker directly:
```bash
docker build -t stock-dashboard .
docker run -d -p 8501:8501 -p 8000:8000 --env-file .env stock-dashboard
```

### Streamlit Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

Quick steps:
1. Push code to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Connect your repository
4. Set main file path: `app/main.py`
5. Add `ALPHA_VANTAGE_API_KEY` in secrets
6. Deploy!

---

## Project Structure

```
stock_dashboard/
├── api/                 # FastAPI backend
│   └── main.py         # API endpoints
├── app/                # Streamlit frontend
│   ├── main.py         # Main Streamlit app
│   └── pages/          # Streamlit pages
├── src/                # Core functionality
│   ├── data/           # Data fetching & processing
│   └── utils/          # Utility functions
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose config
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

---

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Example API Calls

**Get Stock Data:**
```bash
curl -X POST "http://localhost:8000/api/stock-data" \
  -H "Content-Type: application/json" \
  -d '{"symbol": "AAPL", "period": "1mo"}'
```

**Summarize Text:**
```bash
curl -X POST "http://localhost:8000/api/summarize" \
  -H "Content-Type: application/json" \
  -d '{"text": "Your text here", "max_length": 150, "min_length": 50}'
```

---

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).