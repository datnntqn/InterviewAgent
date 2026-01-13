# AI Agent Layer

This module contains the CrewAI agents, crews, tasks, and tools for interview preparation.

## Structure

```
ai/
├── src/
│   ├── agents/     # CrewAI agent definitions
│   ├── crews/      # Crew orchestration logic
│   ├── tasks/      # Task definitions
│   ├── tools/      # Custom tools (web scraping, etc.)
│   └── config.py   # LLM configuration
└── tests/          # Unit tests
```

## Setup

```bash
cd ai
pip install -r requirements.txt
```

## Usage

```python
from ai.src.crews import prepare_for_interview

result = prepare_for_interview(
    job_description="...",
    user_cv="...",
    company_name="...",
    company_website="...",
    tone="friendly",
    level="senior"
)
```

See main project README for more details.
