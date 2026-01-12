#!/bin/bash

# AI Mock Interview Agent - Quick Verification Script
# This script verifies that the project structure is correctly set up

echo "🔍 Verifying AI Mock Interview Agent Setup..."
echo ""

# Check required files
echo "📁 Checking project structure..."
files=(
    "pyproject.toml"
    "Dockerfile"
    "docker-compose.yml"
    ".env.example"
    ".gitignore"
    "src/__init__.py"
    "src/main.py"
    "src/config.py"
    "src/models/schemas.py"
    "src/tools/scraper.py"
    "src/agents/__init__.py"
    "src/tasks/__init__.py"
    "src/crews/__init__.py"
)

missing_files=0
for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✅ $file"
    else
        echo "  ❌ $file (MISSING)"
        missing_files=$((missing_files + 1))
    fi
done

echo ""
if [ $missing_files -eq 0 ]; then
    echo "✅ All required files present!"
else
    echo "❌ Missing $missing_files file(s)"
    exit 1
fi

echo ""
echo "🐳 Checking Docker..."
if command -v docker &> /dev/null; then
    echo "  ✅ Docker is installed"
    docker --version
else
    echo "  ❌ Docker is not installed"
    echo "     Please install Docker from https://www.docker.com/get-started"
fi

echo ""
if command -v docker-compose &> /dev/null; then
    echo "  ✅ Docker Compose is installed"
    docker-compose --version
else
    echo "  ❌ Docker Compose is not installed"
fi

echo ""
echo "📝 Next Steps:"
echo "  1. Copy .env.example to .env: cp .env.example .env"
echo "  2. Build and start services: docker-compose up --build"
echo "  3. Pull Llama 3 model: docker-compose exec ollama ollama pull llama3"
echo "  4. Check logs: docker-compose logs -f app"
echo ""
echo "📚 Documentation:"
echo "  - Setup Guide: SETUP.md"
echo "  - Implementation Summary: IMPLEMENTATION.md"
echo "  - Project Plan: README.md"
echo ""
echo "✨ Project verification complete!"
