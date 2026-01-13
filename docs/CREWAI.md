# CrewAI Implementation Guide - AI Mock Interview Agent

## 📚 Table of Contents

1. [Overview](#overview)
2. [Core Concepts](#core-concepts)
3. [Architecture](#architecture)
4. [Step-by-Step Implementation](#step-by-step-implementation)
5. [Usage Examples](#usage-examples)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Overview

This guide explains how the AI Mock Interview Agent is built using CrewAI, a framework for orchestrating AI agents to work together on complex tasks.

### What is CrewAI?

CrewAI is a framework that allows you to:

- Define **Agents** with specific roles and expertise
- Create **Tasks** that agents need to complete
- Organize agents and tasks into **Crews** that work together
- Execute complex workflows with multiple AI agents collaborating

### Our Use Case

We use CrewAI to prepare candidates for job interviews by:

1. Analyzing job descriptions
2. Researching company culture
3. Generating tailored interview questions

---

## Core Concepts

### 1. Agents 🤖

**What**: AI entities with specific roles and capabilities

**In Our System**:

- **JD Analyst**: Analyzes job descriptions and identifies skill requirements
- **Corporate Researcher**: Scrapes company websites for culture information
- **Lead Interviewer**: Creates interview questions and strategies

**Key Properties**:

```python
Agent(
    role="Senior Technical Recruiter",           # What they are
    goal="Extract core technical skills...",      # What they aim to achieve
    backstory="You are an expert at...",          # Their personality/context
    llm="ollama/llama3",                          # The LLM they use
    tools=[scraper_tool],                         # Tools they can use
    verbose=True,                                 # Show their thinking
    allow_delegation=False                        # Can they ask other agents?
)
```

### 2. Tools 🛠️

**What**: Functions that agents can use to perform actions

**In Our System**:

- **WebsiteScraper**: Scrapes company websites using Playwright

**Implementation**:

```python
class WebsiteScraper(BaseTool):
    name: str = "Website Scraper"
    description: str = "Scrapes text content from a website URL..."
    args_schema: Type[BaseModel] = WebsiteScraperInput

    def _run(self, url: str) -> str:
        # Tool implementation
        pass
```

### 3. Tasks 📋

**What**: Specific jobs that agents need to complete

**In Our System**:

- **Analyze Job Description**: Extract skills and requirements
- **Research Company Culture**: Find mission, values, projects
- **Prepare Interview Dossier**: Generate questions and strategy

**Key Properties**:

```python
Task(
    description="Analyze the following job description...",  # What to do
    expected_output="A detailed analysis containing...",     # What to produce
    agent=jd_analyst,                                        # Who does it
    output_pydantic=JobDescriptionAnalysis,                  # Output format
    context=[previous_task]                                  # Dependencies
)
```

### 4. Crews 👥

**What**: Orchestrators that coordinate agents and tasks

**In Our System**:

- **InterviewPreparationCrew**: Coordinates all agents and tasks

**Key Properties**:

```python
Crew(
    agents=[agent1, agent2, agent3],      # Who's involved
    tasks=[task1, task2, task3],          # What needs to be done
    process=Process.sequential,            # How to execute (order)
    verbose=True,                          # Show progress
    memory=True                            # Remember context
)
```

---

## Architecture

### System Flow

```
┌─────────────────────────────────────────────────────────┐
│                  User Input                             │
│  (Job Description, CV, Company Info)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           InterviewPreparationCrew                      │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Step 1: JD Analyst                              │  │
│  │  ├─ Analyzes job description                     │  │
│  │  ├─ Compares with CV                             │  │
│  │  └─ Outputs: JobDescriptionAnalysis              │  │
│  └──────────────────────────────────────────────────┘  │
│                     │                                   │
│                     ▼                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Step 2: Corporate Researcher                    │  │
│  │  ├─ Uses WebsiteScraper tool                     │  │
│  │  ├─ Extracts company culture                     │  │
│  │  └─ Outputs: CompanyCultureProfile               │  │
│  └──────────────────────────────────────────────────┘  │
│                     │                                   │
│                     ▼                                   │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Step 3: Lead Interviewer                        │  │
│  │  ├─ Synthesizes results from Steps 1 & 2         │  │
│  │  ├─ Generates interview questions (STAR method)  │  │
│  │  └─ Outputs: InterviewDossier                    │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              Interview Preparation Package              │
│  - Job Analysis                                         │
│  - Company Culture Insights                             │
│  - Tailored Interview Questions                         │
│  - Preparation Strategy                                 │
└─────────────────────────────────────────────────────────┘
```

### Directory Structure

```
src/
├── agents/
│   ├── __init__.py
│   └── agents.py              # Agent definitions
├── tasks/
│   ├── __init__.py
│   └── tasks.py               # Task definitions
├── crews/
│   ├── __init__.py
│   └── interview_crew.py      # Crew orchestration
├── tools/
│   ├── __init__.py
│   └── scraper.py             # WebsiteScraper tool
├── models/
│   ├── __init__.py
│   └── schemas.py             # Pydantic data models
├── config.py                  # Configuration
└── main.py                    # Entry point
```

---

## Step-by-Step Implementation

### Step 1: Define Data Models

**File**: `src/models/schemas.py`

```python
from pydantic import BaseModel, Field
from typing import List

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

**Why**: These models define the structure of outputs from each agent.

---

### Step 2: Create Tools

**File**: `src/tools/scraper.py`

```python
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
from playwright.sync_api import sync_playwright

class WebsiteScraperInput(BaseModel):
    url: str = Field(..., description="The URL of the website to scrape")

class WebsiteScraper(BaseTool):
    name: str = "Website Scraper"
    description: str = "Scrapes text content from a website URL..."
    args_schema: Type[BaseModel] = WebsiteScraperInput

    def _run(self, url: str) -> str:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=60000)
            content = page.inner_text("body")
            browser.close()
        return content
```

**Why**: Tools give agents capabilities beyond text generation (web scraping, API calls, etc.).

---

### Step 3: Define Agents

**File**: `src/agents/agents.py`

```python
from crewai import Agent

class InterviewAgents:
    def __init__(self, tone="friendly", level="mid"):
        self.llm = f"ollama/llama3"
        self.scraper = WebsiteScraper()

    def jd_analyst(self) -> Agent:
        return Agent(
            role="Senior Technical Recruiter",
            goal="Extract core technical skills...",
            backstory="You are an expert at analyzing...",
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )

    def corporate_researcher(self) -> Agent:
        return Agent(
            role="Company Culture Investigator",
            goal="Scrape the company website...",
            backstory="You are a detective for corporate identity...",
            llm=self.llm,
            tools=[self.scraper],  # Has access to scraper
            verbose=True,
            allow_delegation=False
        )

    def lead_interviewer(self) -> Agent:
        backstory = "You are a supportive Lead Interview Manager..." if tone == "friendly" else "You are a no-nonsense Lead Interview Manager..."

        return Agent(
            role="Lead Interview Manager",
            goal="Synthesize all data...",
            backstory=backstory,  # Dynamic based on tone
            llm=self.llm,
            verbose=True,
            allow_delegation=True  # Can ask other agents
        )
```

**Why**: Agents are the "workers" with specific expertise and personalities.

---

### Step 4: Define Tasks

**File**: `src/tasks/tasks.py`

```python
from crewai import Task

class InterviewTasks:
    def analyze_job_description(self, agent, job_description, user_cv) -> Task:
        return Task(
            description=f"Analyze the following job description...\n{job_description}\n{user_cv}",
            expected_output="A detailed analysis containing skills, keywords, experience...",
            agent=agent,
            output_pydantic=JobDescriptionAnalysis
        )

    def research_company_culture(self, agent, company_name, company_website) -> Task:
        return Task(
            description=f"Research {company_name} at {company_website}...",
            expected_output="Company culture profile with mission, values...",
            agent=agent,
            output_pydantic=CompanyCultureProfile
        )

    def prepare_interview_dossier(self, agent, job_analysis, company_culture) -> Task:
        task = Task(
            description="Create a comprehensive Interview Dossier...",
            expected_output="Interview questions and strategy...",
            agent=agent,
            output_pydantic=InterviewDossier
        )
        task.context = [job_analysis, company_culture]  # Depends on previous tasks
        return task
```

**Why**: Tasks define what needs to be done and by whom.

---

### Step 5: Create the Crew

**File**: `src/crews/interview_crew.py`

```python
from crewai import Crew, Process

class InterviewPreparationCrew:
    def __init__(self, tone="friendly", level="mid", verbose=True):
        self.agents_factory = InterviewAgents(tone=tone, level=level)
        self.tasks_factory = InterviewTasks()

    def prepare_interview(self, job_description, user_cv, company_name, company_website):
        # Get agents
        agents = self.agents_factory.get_all_agents()

        # Create tasks
        tasks = self.tasks_factory.get_all_tasks(
            agents=agents,
            job_description=job_description,
            user_cv=user_cv,
            company_name=company_name,
            company_website=company_website
        )

        # Create crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,  # Execute in order
            verbose=True,
            memory=True  # Remember context between tasks
        )

        # Execute
        result = crew.kickoff()
        return result
```

**Why**: The crew orchestrates everything and executes the workflow.

---

### Step 6: Create the Main Entry Point

**File**: `src/main.py`

```python
from .crews import prepare_for_interview

def main():
    result = prepare_for_interview(
        job_description="Senior Python Developer...",
        user_cv="John Doe - 6 years Python...",
        company_name="TechCorp",
        company_website="https://techcorp.com",
        tone="friendly",
        level="senior"
    )
    print(result)

if __name__ == "__main__":
    main()
```

**Why**: Provides a simple interface to run the system.

---

## Usage Examples

### Example 1: Basic Usage

```python
from src.crews import prepare_for_interview

result = prepare_for_interview(
    job_description="Looking for a Python developer with 5+ years...",
    user_cv="Experienced Python developer with Django...",
    company_name="TechCorp",
    company_website="https://techcorp.com",
    tone="friendly",
    level="senior"
)
```

### Example 2: Using the Crew Class

```python
from src.crews import InterviewPreparationCrew

crew = InterviewPreparationCrew(tone="strict", level="mid")

result = crew.prepare_interview(
    job_description="...",
    user_cv="...",
    company_name="...",
    company_website="..."
)
```

### Example 3: Quick Job Analysis Only

```python
crew = InterviewPreparationCrew()
result = crew.quick_analysis(
    job_description="...",
    user_cv="..."
)
```

### Example 4: Company Research Only

```python
crew = InterviewPreparationCrew()
result = crew.research_company_only(
    company_name="TechCorp",
    company_website="https://techcorp.com"
)
```

### Example 5: Command Line

```bash
# Run with example data
python -m src.main example

# Run in interactive mode
python -m src.main interactive
```

---

## Best Practices

### 1. Agent Design

✅ **DO**:

- Give agents clear, specific roles
- Write detailed backstories that guide behavior
- Use `allow_delegation=True` only for coordinator agents
- Set `verbose=True` during development

❌ **DON'T**:

- Make agents too general
- Give all agents delegation powers (causes loops)
- Skip the backstory (it's crucial for behavior)

### 2. Task Design

✅ **DO**:

- Write clear, detailed descriptions
- Specify expected outputs explicitly
- Use `output_pydantic` for structured data
- Set task dependencies with `context`

❌ **DON'T**:

- Make tasks too vague
- Forget to specify expected output
- Create circular dependencies

### 3. Tool Design

✅ **DO**:

- Inherit from `BaseTool`
- Provide clear descriptions
- Define input schemas with Pydantic
- Handle errors gracefully

❌ **DON'T**:

- Make tools too complex
- Skip error handling
- Forget to document what the tool does

### 4. Crew Configuration

✅ **DO**:

- Use `Process.sequential` for dependent tasks
- Enable `memory=True` for context sharing
- Set appropriate `verbose` levels
- Test with small examples first

❌ **DON'T**:

- Use `Process.hierarchical` without understanding it
- Disable memory if tasks need context
- Run full workflows without testing components

---

## Troubleshooting

### Issue: "LiteLLM is not available"

**Solution**: Install litellm

```bash
pip install litellm
```

### Issue: "OPENAI_API_KEY is required"

**Solution**: Use the correct LLM format for Ollama

```python
llm = "ollama/llama3"  # ✅ Correct
llm = ChatOllama(...)  # ❌ Wrong for CrewAI
```

### Issue: "Tool validation error"

**Solution**: Ensure tool inherits from `BaseTool`

```python
class MyTool(BaseTool):  # ✅ Correct
    name: str = "My Tool"
    description: str = "..."
    args_schema: Type[BaseModel] = MyInput

    def _run(self, arg: str) -> str:
        pass
```

### Issue: "Ollama connection refused"

**Solution**: Ensure Ollama is running

```bash
# Check if Ollama is accessible
curl http://localhost:11434/api/tags

# Start Ollama (Docker)
docker-compose up ollama -d

# Or start Ollama (native)
ollama serve
```

### Issue: "Task output not structured"

**Solution**: Use `output_pydantic` parameter

```python
Task(
    description="...",
    expected_output="...",
    agent=agent,
    output_pydantic=MyModel  # ✅ Ensures structured output
)
```

---

## Key Takeaways

1. **Agents** = Workers with roles and expertise
2. **Tools** = Capabilities agents can use
3. **Tasks** = Jobs that need to be done
4. **Crews** = Orchestrators that coordinate everything

5. **Sequential Process** = Tasks execute in order
6. **Memory** = Agents remember context
7. **Context** = Tasks can depend on previous results
8. **Delegation** = Agents can ask each other for help

9. **Always test components individually** before running the full crew
10. **Use verbose mode** during development to understand what's happening

---

## Next Steps

1. ✅ Understand the architecture
2. ✅ Review the code in each module
3. ✅ Run the example: `python -m src.main example`
4. ✅ Try interactive mode: `python -m src.main interactive`
5. ✅ Customize agents, tasks, or tools for your needs
6. ✅ Build your own crews for different use cases!

---

**Happy Building! 🚀**
