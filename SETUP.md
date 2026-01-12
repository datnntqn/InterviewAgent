# AI Mock Interview Agent - Setup Guide

## 🚀 Quick Start

This guide will help you set up and run the AI Mock Interview Agent using Docker and Docker Compose.

## 📋 Prerequisites

- **Docker** (version 20.10+)
- **Docker Compose** (version 2.0+)
- **Git**

## 🛠️ Installation Steps

### 1. Clone the Repository (if not already done)

```bash
git clone <your-repo-url>
cd Interview-Agent
```

### 2. Create Environment File

Copy the example environment file and customize if needed:

```bash
cp .env.example .env
```

The default configuration:

- `OLLAMA_BASE_URL=http://ollama:11434`
- `LLM_MODEL=llama3`

### 3. Build and Start Services

Build the Docker images and start all services:

```bash
docker-compose up --build
```

This will:

- Pull the Ollama image
- Build the application container
- Start both services with proper networking
- Wait for Ollama to be healthy before starting the app

### 4. Pull the Llama 3 Model (First Time Only)

In a new terminal, pull the Llama 3 model into Ollama:

```bash
docker-compose exec ollama ollama pull llama3
```

This may take several minutes depending on your internet connection.

### 5. Verify Installation

Check that both services are running:

```bash
docker-compose ps
```

You should see both `ollama` and `app` services running.

## 🧪 Testing the Setup

### Test Ollama Service

```bash
curl http://localhost:11434/api/tags
```

This should return a list of available models.

### Test the Application

The application logs will show initialization messages:

```bash
docker-compose logs app
```

## 📁 Project Structure

```
ai-mock-interviewer/
├── docker-compose.yml      # Docker orchestration
├── Dockerfile              # Application container definition
├── pyproject.toml          # Python dependencies (Poetry)
├── .env.example            # Environment variables template
├── src/
│   ├── __init__.py
│   ├── main.py            # Application entry point
│   ├── config.py          # Configuration management
│   ├── models/
│   │   └── schemas.py     # Pydantic data models
│   ├── tools/
│   │   └── scraper.py     # Playwright web scraper
│   ├── agents/            # CrewAI agents (to be implemented)
│   ├── tasks/             # CrewAI tasks (to be implemented)
│   └── crews/             # CrewAI crews (to be implemented)
└── data/                  # Data storage directory
```

## 🔧 Development Workflow

### Local Development with Hot Reload

The `docker-compose.yml` mounts the `src/` directory as a volume, allowing you to edit code locally and see changes reflected in the container.

### Running Commands Inside Container

```bash
# Access the app container shell
docker-compose exec app bash

# Run Python scripts
docker-compose exec app python -m src.main

# Install new dependencies
docker-compose exec app poetry add <package-name>
```

### Viewing Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f ollama
```

## 🛑 Stopping Services

```bash
# Stop services (keeps containers)
docker-compose stop

# Stop and remove containers
docker-compose down

# Stop and remove containers + volumes (removes Ollama models)
docker-compose down -v
```

## 🐛 Troubleshooting

### Ollama Service Not Healthy

If the app service fails to start with "ollama service is unhealthy":

1. Check Ollama logs: `docker-compose logs ollama`
2. Ensure port 11434 is not already in use
3. Try restarting: `docker-compose restart ollama`

### Playwright Browser Issues

If you encounter browser-related errors:

```bash
# Rebuild the container
docker-compose build --no-cache app
docker-compose up
```

### Port Conflicts

If port 11434 is already in use, modify `docker-compose.yml`:

```yaml
services:
  ollama:
    ports:
      - "11435:11434" # Change external port
```

And update `.env`:

```
OLLAMA_BASE_URL=http://ollama:11434  # Keep internal port the same
```

## 📚 Next Steps

1. **Implement CrewAI Agents**: Define agents in `src/agents/`
2. **Create Tasks**: Define tasks in `src/tasks/`
3. **Build Crews**: Orchestrate agents and tasks in `src/crews/`
4. **Extend Functionality**: Add more tools and capabilities

## 🔗 Useful Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [Ollama Documentation](https://ollama.ai/docs)
- [Playwright Python Documentation](https://playwright.dev/python/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 📝 License

[Your License Here]
