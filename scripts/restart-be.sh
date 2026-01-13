#!/bin/bash
lsof -ti:8000 | xargs kill -9 2>/dev/null; sleep 1; python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000