#!/bin/bash

# AI Mock Interview Agent - Streamlit Dashboard Launcher
# This script starts the Streamlit web interface

echo "🎯 Starting AI Interview Coach Dashboard..."
echo "============================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run: python -m venv venv && source venv/bin/activate && pip install -r requirements.txt"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if streamlit is installed
if ! python -c "import streamlit" 2>/dev/null; then
    echo "📦 Installing Streamlit..."
    pip install streamlit>=1.28.0 requests>=2.31.0
fi

# Check if backend is running
echo "🔍 Checking if backend API is running..."
if ! curl -s http://localhost:8000/api/health > /dev/null 2>&1; then
    echo "⚠️  Backend API is not running!"
    echo "Please start the backend first with: ./scripts/start_server_new.sh"
    echo ""
    read -p "Do you want to continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo "✅ Backend API is running"
fi

echo ""
echo "🚀 Launching Streamlit Dashboard..."
echo "📱 Dashboard will open at: http://localhost:8501"
echo "============================================"
echo ""

# Start Streamlit from client directory
cd client
streamlit run app.py \
    --server.port 8501 \
    --server.address localhost \
    --browser.gatherUsageStats false

