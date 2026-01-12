#!/bin/bash

# Start the FastAPI server for AI Mock Interview Agent

echo "🚀 Starting AI Mock Interview Agent API Server..."
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated"
    echo "Activating virtual environment..."
    source venv/bin/activate
fi

# Check if FastAPI is installed
if ! python -c "import fastapi" 2>/dev/null; then
    echo "📦 Installing FastAPI and uvicorn..."
    pip install fastapi uvicorn[standard]
fi

# Check if Ollama is running
echo "🔍 Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "✅ Ollama is running"
else
    echo "⚠️  Ollama is not running"
    echo "Starting Ollama with Docker..."
    docker-compose up ollama -d
    echo "Waiting for Ollama to be ready..."
    sleep 5
fi

echo ""
echo "="*60
echo "🎯 AI Mock Interview Agent API Server"
echo "="*60
echo ""
echo "API will be available at:"
echo "  - http://localhost:8000"
echo "  - API Docs: http://localhost:8000/docs"
echo ""
echo "Web UI will be available at:"
echo "  - http://localhost:8000/web"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start the server
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
