# Local Development Setup (Without Docker for App)

This guide shows you how to run the AI Mock Interview Agent directly on your local machine without using Docker for the application.

## 📋 Prerequisites

- **Python 3.10+** installed on your system
- **Poetry** (Python dependency manager)
- **Ollama** (for LLM - can run via Docker or natively)

## 🛠️ Installation Steps

### 1. Install Python Dependencies

First, install Poetry if you don't have it:

```bash
# Install Poetry
curl -sSL https://install.python-poetry.org | python3 -

# Or using pip
pip install poetry
```

Then install project dependencies:

```bash
# Navigate to project directory
cd /Users/datnnt/Desktop/DatNNT/Web/Interview-Agent

# Install dependencies
poetry install

# Or if you prefer using pip with a virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
pip install crewai langchain pydantic pydantic-settings playwright
```

### 2. Install Playwright Browsers

Playwright needs to download browser binaries:

```bash
# If using Poetry
poetry run playwright install chromium

# If using venv
playwright install chromium
```

### 3. Setup Ollama

You have two options for running Ollama:

#### Option A: Run Ollama via Docker (Recommended)

```bash
# Start only Ollama service
docker-compose up ollama -d

# Pull the Llama 3 model
docker-compose exec ollama ollama pull llama3

# Verify it's running
curl http://localhost:11434/api/tags
```

#### Option B: Install Ollama Natively on macOS

```bash
# Download and install from https://ollama.ai/download
# Or using Homebrew
brew install ollama

# Start Ollama service
ollama serve &

# Pull Llama 3 model
ollama pull llama3
```

### 4. Configure Environment Variables

Create a `.env` file for local development:

```bash
cp .env.example .env
```

Edit `.env` to use localhost:

```env
OLLAMA_BASE_URL=http://localhost:11434
LLM_MODEL=llama3
```

### 5. Run the Application

Now you can run the Python application directly:

```bash
# Using Poetry
poetry run python -m src.main

# Or if using venv
source venv/bin/activate
python -m src.main
```

## 🔧 Development Workflow

### Running the App

```bash
# Activate virtual environment (if using venv)
source venv/bin/activate

# Run the application
python -m src.main
```

### Adding New Dependencies

```bash
# Using Poetry
poetry add <package-name>

# Using pip
pip install <package-name>
pip freeze > requirements.txt
```

### Running Tests (when you add them)

```bash
# Using Poetry
poetry run pytest

# Using venv
pytest
```

### Code Formatting & Linting

```bash
# Install dev dependencies
poetry add --group dev black flake8 mypy

# Format code
poetry run black src/

# Lint code
poetry run flake8 src/

# Type checking
poetry run mypy src/
```

## 📁 Project Structure for Local Development

```
Interview-Agent/
├── venv/                   # Virtual environment (if using venv)
├── .env                    # Local environment variables
├── pyproject.toml          # Poetry configuration
├── poetry.lock             # Locked dependencies (generated)
└── src/
    └── ...                 # Your source code
```

## 🐛 Troubleshooting

### Issue: "Module not found" errors

**Solution**: Make sure you're running from the project root and using the `-m` flag:

```bash
# ✅ Correct
python -m src.main

# ❌ Wrong
python src/main.py
```

### Issue: Ollama connection refused

**Solution**: Check if Ollama is running:

```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# If using Docker
docker-compose ps ollama

# If using native Ollama
ps aux | grep ollama
```

### Issue: Playwright browser not found

**Solution**: Install Playwright browsers:

```bash
poetry run playwright install chromium
# or
playwright install chromium
```

### Issue: Pydantic validation errors

**Solution**: Make sure you have the correct Pydantic version:

```bash
poetry add pydantic@^2.0 pydantic-settings
```

## 🔄 Switching Between Docker and Local

### Stop Docker App (Keep Ollama Running)

```bash
# Stop all services
docker-compose down

# Start only Ollama
docker-compose up ollama -d
```

### Use Docker for Everything

```bash
# Stop local app (Ctrl+C)
# Start all services
docker-compose up --build
```

## 📊 Performance Comparison

| Aspect           | Docker                      | Local                           |
| ---------------- | --------------------------- | ------------------------------- |
| **Startup Time** | Slower (container overhead) | Faster                          |
| **Hot Reload**   | Supported (volume mount)    | Native                          |
| **Debugging**    | More complex                | Easier (direct IDE integration) |
| **Isolation**    | Complete                    | Shared with system              |
| **Deployment**   | Production-ready            | Development only                |

## 🎯 Recommended Setup

For **development**: Run app locally, Ollama in Docker

```bash
# Terminal 1: Start Ollama
docker-compose up ollama -d

# Terminal 2: Run app locally
poetry run python -m src.main
```

For **production/testing**: Use full Docker setup

```bash
docker-compose up --build
```

## 📝 Quick Reference Commands

```bash
# Setup (one-time)
poetry install
poetry run playwright install chromium
cp .env.example .env

# Daily development
docker-compose up ollama -d          # Start Ollama
poetry run python -m src.main        # Run app

# Cleanup
docker-compose down                  # Stop Ollama
deactivate                          # Exit venv (if using)
```

## 🚀 Next Steps

1. Install dependencies: `poetry install`
2. Start Ollama: `docker-compose up ollama -d`
3. Run the app: `poetry run python -m src.main`
4. Start coding! 🎉

---

_For Docker-based setup, see [SETUP.md](SETUP.md)_

```bash
lsof -ti:8000 | xargs kill -9
```
