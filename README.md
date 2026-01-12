# Role

You are a Senior Python Architect and DevOps Engineer specializing in Generative AI applications. You are an expert in **CrewAI**, **Docker**, and **Microservices Architecture**.

# Objective

Initialize a new Python project for an **"AI Mock Interview Agent"**. The system uses CrewAI for orchestration, Playwright for web crawling, and a local LLM (Llama 3 via Ollama) for inference.

# AI Mock Interview Agent

## Project Structure

```text
ai-mock-interviewer/
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── .env.example
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   └── schemas.py
│   ├── tools/
│   │   └── scraper.py
│   ├── agents/
│   ├── tasks/
│   └── crews/
└── data/
```

---

## Dockerfile

```dockerfile
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy dependency files
COPY pyproject.toml poetry.lock* /app/

# Configure Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# Copy source code
COPY ./src /app/src

CMD ["python", "-m", "src.main"]
```

---

## docker-compose.yml

```yaml
version: "3.9"

services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    healthcheck:
      test: ["CMD", "ollama", "list"]
      interval: 10s
      timeout: 5s
      retries: 5
    # deploy:
    #   resources:
    #     reservations:
    #       devices:
    #         - capabilities: [gpu]

  app:
    build: .
    volumes:
      - ./src:/app/src
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
    depends_on:
      ollama:
        condition: service_healthy

volumes:
  ollama_data:
```

---

## src/models/schemas.py

```python
from typing import List
from pydantic import BaseModel, Field


class JobDescriptionAnalysis(BaseModel):
    skills: List[str] = Field(..., description="Key technical and soft skills")
    keywords: List[str] = Field(..., description="Important keywords from JD")
    experience_years: int = Field(..., description="Required years of experience")


class CompanyCultureProfile(BaseModel):
    values: List[str] = Field(..., description="Company core values")
    mission: str = Field(..., description="Company mission statement")


class InterviewDossier(BaseModel):
    questions: List[str] = Field(..., description="Interview questions")
    strategy: str = Field(..., description="Interview strategy and focus areas")
```

---

## src/tools/scraper.py

```python
from playwright.sync_api import sync_playwright


class WebsiteScraper:
    """
    Simple Playwright-based scraper tool.
    Used by CrewAI agents to fetch raw text from a webpage.
    """

    def scrape_text(self, url: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            content = page.inner_text("body")
            browser.close()
        return content
```

---

## src/config.py

```python
import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    """
    Centralized configuration.

    Docker networking note:
    Inside docker-compose, the app talks to Ollama via
    http://ollama:11434 (service name = hostname).
    """

    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    llm_model: str = os.getenv("LLM_MODEL", "llama3")

    class Config:
        env_file = ".env"
```

---

## .env.example

```env
OLLAMA_BASE_URL=http://ollama:11434
LLM_MODEL=llama3
```

---

## pyproject.toml

```toml
[tool.poetry]
name = "ai-mock-interviewer"
version = "0.1.0"
description = "AI Mock Interview Agent using CrewAI"
authors = ["Your Name"]

[tool.poetry.dependencies]
python = "^3.10"
crewai = "*"
langchain = "*"
pydantic = "*"
playwright = "*"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```
