#!/bin/bash

# Local Setup Script for AI Mock Interview Agent
# This script sets up the Python environment without Docker

set -e  # Exit on error

echo "🚀 Setting up AI Mock Interview Agent for local development..."
echo ""

# Check Python version
echo "📍 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "   Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Install Playwright browsers
echo ""
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create .env file if it doesn't exist
echo ""
echo "⚙️  Setting up environment variables..."
if [ -f ".env" ]; then
    echo "   .env file already exists, skipping..."
else
    cp .env.example .env
    echo "   ✅ Created .env file from .env.example"
fi

# Check if Ollama is running
echo ""
echo "🔍 Checking Ollama status..."
if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "   ✅ Ollama is running on http://localhost:11434"
else
    echo "   ⚠️  Ollama is not running"
    echo "   Please start Ollama with one of these commands:"
    echo "   - Docker: docker-compose up ollama -d"
    echo "   - Native: ollama serve"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Activate the virtual environment:"
echo "      source venv/bin/activate"
echo ""
echo "   2. Start Ollama (if not running):"
echo "      docker-compose up ollama -d"
echo ""
echo "   3. Pull Llama 3 model (first time only):"
echo "      docker-compose exec ollama ollama pull llama3"
echo ""
echo "   4. Run the application:"
echo "      python -m src.main"
echo ""
echo "🎉 Happy coding!"
