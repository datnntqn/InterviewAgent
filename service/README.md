# Backend Service Layer

FastAPI-based REST API service that exposes the AI agents functionality.

## Structure

```
service/
├── src/
│   ├── api.py      # FastAPI application
│   ├── main.py     # Entry point
│   └── models/     # Pydantic models
└── tests/          # API tests
```

## Endpoints

- `POST /api/prepare-stream` - Stream interview preparation results
- `GET /api/health` - Health check endpoint

## Setup

```bash
cd service
pip install -r requirements.txt
```

## Run

```bash
uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

See main project README for more details.
