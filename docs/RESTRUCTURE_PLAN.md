# Project Restructuring Plan

## 🎯 Goal

Reorganize the Interview-Agent project into a clean monorepo structure with three distinct parts:

- **ai/** - CrewAI agents and LLM orchestration
- **service/** - FastAPI backend service
- **client/** - Frontend web application

## 📁 New Structure

```
Interview-Agent/
├── README.md                      # Main project README
├── .gitignore                     # Root gitignore
├── .env.example                   # Environment variables template
├── docker-compose.yml             # Docker orchestration
├── docs/                          # All documentation
│   ├── AGENTS.md
│   ├── COMPLETE.md
│   ├── CREWAI.md
│   ├── GROQ_MIGRATION.md
│   ├── GROQ_API_TESTING.md
│   ├── IMPLEMENTATION.md
│   ├── SETUP.md
│   └── WEB_UI_GUIDE.md
│
├── scripts/                       # Utility scripts
│   ├── setup_groq.sh
│   ├── start_server.sh
│   ├── test_groq_api.sh
│   └── verify.sh
│
├── ai/                            # AI/Agent Layer
│   ├── README.md
│   ├── requirements.txt
│   ├── pyproject.toml
│   ├── src/
│   │   ├── __init__.py
│   │   ├── config.py              # LLM configuration
│   │   ├── agents/                # CrewAI agents
│   │   │   ├── __init__.py
│   │   │   └── agents.py
│   │   ├── crews/                 # CrewAI crews
│   │   │   ├── __init__.py
│   │   │   └── interview_crew.py
│   │   ├── tasks/                 # CrewAI tasks
│   │   │   ├── __init__.py
│   │   │   └── tasks.py
│   │   └── tools/                 # CrewAI tools
│   │       ├── __init__.py
│   │       └── scraper.py
│   └── tests/
│       ├── test_agents.py
│       └── test_components.py
│
├── service/                       # Backend API Layer
│   ├── README.md
│   ├── requirements.txt
│   ├── src/
│   │   ├── __init__.py
│   │   ├── api.py                 # FastAPI application
│   │   ├── models/                # Pydantic models
│   │   │   ├── __init__.py
│   │   │   └── schemas.py
│   │   └── main.py                # Entry point
│   └── tests/
│
└── client/                        # Frontend Layer
    ├── README.md
    ├── package.json               # (if using npm/build tools)
    ├── public/
    │   └── index.html
    ├── src/
    │   ├── js/
    │   ├── css/
    │   └── assets/
    └── dist/                      # Built files
```

## 🔄 Migration Steps

### Step 1: Create New Directory Structure

```bash
# Create main directories
mkdir -p ai/src/{agents,crews,tasks,tools}
mkdir -p ai/tests
mkdir -p service/src/models
mkdir -p service/tests
mkdir -p client/{public,src/{js,css,assets},dist}
mkdir -p docs
mkdir -p scripts
```

### Step 2: Move AI Components

```bash
# Move agent-related code
mv src/agents ai/src/
mv src/crews ai/src/
mv src/tasks ai/src/
mv src/tools ai/src/
mv src/config.py ai/src/
mv src/__init__.py ai/src/

# Move tests
mv test_agents.py ai/tests/
mv test_components.py ai/tests/
```

### Step 3: Move Service Components

```bash
# Move API code
mv src/api.py service/src/
mv src/main.py service/src/
mv src/models service/src/
```

### Step 4: Move Client Components

```bash
# Move web files
mv web/index.html client/public/
```

### Step 5: Move Documentation

```bash
# Move all docs
mv *.md docs/
# Keep README.md in root
mv docs/README.md ./
```

### Step 6: Move Scripts

```bash
# Move utility scripts
mv *.sh scripts/
```

### Step 7: Create Component-Specific Files

#### ai/requirements.txt

```txt
crewai>=0.1.0
langchain>=0.1.0
langchain-community>=0.1.0
langchain-groq>=0.1.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
playwright>=1.40.0
litellm>=1.0.0
python-dotenv>=1.0.0
```

#### service/requirements.txt

```txt
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
python-dotenv>=1.0.0
```

#### ai/README.md

```markdown
# AI Agent Layer

This module contains the CrewAI agents, crews, tasks, and tools for interview preparation.

## Components

- **agents/**: CrewAI agent definitions
- **crews/**: Crew orchestration logic
- **tasks/**: Task definitions
- **tools/**: Custom tools (web scraping, etc.)

## Usage

See main project README for setup instructions.
```

#### service/README.md

```markdown
# Backend Service Layer

FastAPI-based REST API service that exposes the AI agents functionality.

## Endpoints

- `POST /api/prepare-stream` - Stream interview preparation
- `GET /api/health` - Health check

## Usage

See main project README for setup instructions.
```

#### client/README.md

```markdown
# Frontend Client Layer

Web-based UI for interacting with the interview preparation system.

## Features

- Real-time streaming of agent outputs
- Interactive form for job details
- Beautiful, modern UI

## Usage

See main project README for setup instructions.
```

### Step 8: Update Import Paths

After restructuring, you'll need to update imports:

**In service/src/api.py:**

```python
# Old
from .crews import InterviewPreparationCrew
from .models.schemas import InterviewRequest

# New
from ai.src.crews import InterviewPreparationCrew
from .models.schemas import InterviewRequest
```

**In service/src/main.py:**

```python
# Old
from .config import Settings
from .crews import prepare_for_interview

# New
from ai.src.config import Settings
from ai.src.crews import prepare_for_interview
```

### Step 9: Update docker-compose.yml

```yaml
version: "3.9"

services:
  ai:
    build:
      context: ./ai
      dockerfile: Dockerfile
    volumes:
      - ./ai/src:/app/src
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GROQ_MODEL_NAME=${GROQ_MODEL_NAME:-llama-3.3-70b-versatile}
    env_file:
      - .env

  service:
    build:
      context: ./service
      dockerfile: Dockerfile
    volumes:
      - ./service/src:/app/src
    ports:
      - "8000:8000"
    depends_on:
      - ai
    environment:
      - GROQ_API_KEY=${GROQ_API_KEY}
      - GROQ_MODEL_NAME=${GROQ_MODEL_NAME:-llama-3.3-70b-versatile}
    env_file:
      - .env

  client:
    build:
      context: ./client
      dockerfile: Dockerfile
    volumes:
      - ./client/public:/app/public
    ports:
      - "3000:3000"
    depends_on:
      - service
```

### Step 10: Create Individual Dockerfiles

**ai/Dockerfile:**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["python", "-m", "src.main"]
```

**service/Dockerfile:**

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY src/ ./src/
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000"]
```

**client/Dockerfile:**

```dockerfile
FROM nginx:alpine
COPY public/ /usr/share/nginx/html/
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

## ✅ Benefits of This Structure

1. **Separation of Concerns**: Each layer has a clear responsibility
2. **Independent Development**: Teams can work on different layers independently
3. **Easier Testing**: Each component can be tested in isolation
4. **Better Scalability**: Can deploy/scale each service independently
5. **Cleaner Dependencies**: Each layer has only the dependencies it needs
6. **Improved Documentation**: Each component has its own README

## 🚀 Next Steps

1. Run the migration script (see RESTRUCTURE_SCRIPT.sh)
2. Update import paths in Python files
3. Test each component independently
4. Update CI/CD pipelines if any
5. Update team documentation

## ⚠️ Important Notes

- Backup your project before restructuring
- Update all import statements after moving files
- Test thoroughly after migration
- Update any CI/CD configurations
- Inform team members of the new structure
