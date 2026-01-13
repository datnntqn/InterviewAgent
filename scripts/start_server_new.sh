#!/bin/bash

# Start the FastAPI server for AI Mock Interview Agent (Restructured)

echo "🚀 Starting AI Mock Interview Agent API Server..."
echo ""

# Check if virtual environment is activated
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "⚠️  Virtual environment not activated"
    if [ -d "venv" ]; then
        echo "Activating virtual environment..."
        source venv/bin/activate
    fi
fi

# Check if Groq API configuration exists
echo "🔍 Checking Groq API configuration..."
if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "Please run: cp .env.example .env"
    echo "Then add your Groq API key from: https://console.groq.com/keys"
    exit 1
fi

if grep -q "GROQ_API_KEY=your_groq_api_key_here" .env || ! grep -q "GROQ_API_KEY=" .env; then
    echo "❌ Error: GROQ_API_KEY not configured in .env file"
    echo "Please update your .env file with your Groq API key"
    echo "Get your API key from: https://console.groq.com/keys"
    exit 1
fi

echo "✅ Groq API configuration found"

# Set Python path to include project root
export PYTHONPATH="${PYTHONPATH}:$(pwd)"

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
cd service
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
