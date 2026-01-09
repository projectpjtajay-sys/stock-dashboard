# Docker Setup Summary

## Files Created for Dockerization

1. **Dockerfile**: Multi-service container running both FastAPI and Streamlit
2. **docker-compose.yml**: Easy orchestration with environment variables
3. **start.sh**: Startup script to run both services
4. **.dockerignore**: Excludes unnecessary files from Docker build

## Architecture

```
┌─────────────────────────────────────┐
│         Docker Container            │
│  ┌─────────────┐  ┌────────────┐ │
│  │   FastAPI   │  │  Streamlit  │ │
│  │   :8000     │  │   :8501     │ │
│  └─────────────┘  └────────────┘ │
│         │                │         │
│         └────────┬───────┘         │
│                  │                 │
│         ┌────────▼────────┐        │
│         │  Shared Code    │        │
│         │  (src/)         │        │
│         └─────────────────┘        │
└─────────────────────────────────────┘
```

## How It Works

1. **FastAPI Backend** (`api/main.py`):
   - Provides REST API endpoints
   - Handles stock data fetching
   - Handles text summarization
   - Runs on port 8000

2. **Streamlit Frontend** (`app/main.py`):
   - Interactive web UI
   - Can use FastAPI backend (when `USE_API=true`)
   - Falls back to direct function calls (default)
   - Runs on port 8501

3. **API Client** (`src/utils/api_client.py`):
   - Smart switching between API and direct calls
   - Controlled by `USE_API` environment variable
   - Enables flexible deployment options

## Environment Variables

- `USE_API`: Enable/disable API mode (default: false)
- `API_BASE_URL`: FastAPI base URL (default: http://localhost:8000)
- `ALPHA_VANTAGE_API_KEY`: Required for stock data

## Deployment Modes

### Mode 1: Standalone (Streamlit Cloud)
- `USE_API=false` (default)
- Streamlit uses direct function calls
- No FastAPI backend needed
- Perfect for Streamlit Cloud

### Mode 2: Full Stack (Docker)
- `USE_API=true`
- Streamlit communicates with FastAPI
- Both services in one container
- Better for production with API access

## Building and Running

```bash
# Build
docker build -t stock-dashboard .

# Run
docker run -d \
  -p 8501:8501 \
  -p 8000:8000 \
  --env-file .env \
  stock-dashboard

# Or use docker compose
docker compose up --build
```

## Verification

After starting, verify both services:
- FastAPI: http://localhost:8000/docs
- Streamlit: http://localhost:8501
- Health: http://localhost:8000/health

