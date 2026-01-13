# CrewAI Agents Documentation

## Overview

The `src/agents/agents.py` module implements three specialized CrewAI agents for the AI Mock Interview preparation system. Each agent has a specific role in analyzing job requirements, researching company culture, and creating interview strategies.

## Architecture

```
InterviewAgents (Factory Class)
├── LLM: ChatOllama (Llama 3 via Ollama)
├── Tools: WebsiteScraper
└── Agents:
    ├── JD Analyst
    ├── Corporate Researcher
    └── Lead Interviewer (Strategist)
```

## InterviewAgents Class

### Initialization

```python
from src.agents import InterviewAgents

# Create agents with friendly tone for mid-level position
agents = InterviewAgents(tone="friendly", level="mid")

# Create agents with strict tone for senior position
agents = InterviewAgents(tone="strict", level="senior")
```

**Parameters:**

- `tone` (str): Interview tone - "friendly" or "strict" (default: "friendly")
- `level` (str): Experience level - "junior", "mid", or "senior" (default: "mid")

### LLM Configuration

The class automatically initializes a `ChatOllama` instance with:

- **Model**: `llama3` (configurable via Settings)
- **Base URL**: `http://ollama:11434` (configurable via Settings)
- **Temperature**: `0.7` (balanced creativity and consistency)

## The Three Agents

### 1. JD Analyst (Job Description Analyst)

**Purpose**: Analyzes job descriptions to extract requirements and identify skill gaps.

**Configuration:**

- **Role**: "Senior Technical Recruiter"
- **Goal**: Extract core technical skills, required experience, and identify gaps between the User CV and the Job Description
- **Tools**: None (pure text analysis)
- **Delegation**: Disabled

**Key Capabilities:**

- Distinguishes between "must-have" and "nice-to-have" skills
- Identifies technical skill requirements
- Assesses experience level requirements
- Compares candidate qualifications against job requirements

**Usage:**

```python
agents = InterviewAgents()
jd_analyst = agents.jd_analyst()
```

---

### 2. Corporate Researcher (Company Culture Investigator)

**Purpose**: Researches company culture, values, and mission through web scraping.

**Configuration:**

- **Role**: "Company Culture Investigator"
- **Goal**: Scrape the company website to extract mission, values, and recent project details to ensure culture fit
- **Tools**: WebsiteScraper (Playwright-based)
- **Delegation**: Disabled

**Key Capabilities:**

- Scrapes company websites for cultural information
- Extracts mission statements and core values
- Identifies recent projects and initiatives
- Analyzes company DNA and organizational culture

**Usage:**

```python
agents = InterviewAgents()
researcher = agents.corporate_researcher()
```

---

### 3. Lead Interviewer (Interview Strategist)

**Purpose**: Synthesizes all information to create comprehensive interview preparation materials.

**Configuration:**

- **Role**: "Lead Interview Manager"
- **Goal**: Synthesize all data to generate a comprehensive Interview Dossier containing tailored questions
- **Tools**: None
- **Delegation**: Enabled (can request info from other agents)

**Key Capabilities:**

- Synthesizes job requirements and company culture data
- Generates tailored interview questions
- **STAR Method Integration**: Explicitly structures behavioral questions using:
  - **S**ituation: Context and background
  - **T**ask: Specific challenge or responsibility
  - **A**ction: Steps taken to address the situation
  - **R**esult: Outcomes and impact

**Dynamic Backstory:**

The Lead Interviewer's personality adapts based on the `tone` parameter:

#### Friendly Tone:

```
"You are a supportive and encouraging Lead Interview Manager.
You believe in helping candidates showcase their best selves through
thoughtful preparation and confidence-building.
For culture fit questions, you MUST use the STAR method framework..."
```

#### Strict Tone:

```
"You are a no-nonsense Lead Interview Manager with high standards.
You believe in rigorous preparation and expect candidates to demonstrate
deep technical knowledge and clear problem-solving abilities.
For culture fit questions, you MUST use the STAR method framework..."
```

**Usage:**

```python
# Friendly approach
friendly_agents = InterviewAgents(tone="friendly")
interviewer = friendly_agents.lead_interviewer()

# Strict approach
strict_agents = InterviewAgents(tone="strict")
interviewer = strict_agents.lead_interviewer()
```

---

## Complete Usage Example

```python
from src.agents import InterviewAgents

# Initialize agents for a mid-level position with friendly tone
agents = InterviewAgents(tone="friendly", level="mid")

# Get individual agents
jd_analyst = agents.jd_analyst()
researcher = agents.corporate_researcher()
interviewer = agents.lead_interviewer()

# Or get all agents at once
all_agents = agents.get_all_agents()
# Returns: {
#     "jd_analyst": <Agent>,
#     "corporate_researcher": <Agent>,
#     "lead_interviewer": <Agent>
# }
```

## Agent Workflow

```
1. JD Analyst
   ↓ (Analyzes job requirements)

2. Corporate Researcher
   ↓ (Scrapes company culture)

3. Lead Interviewer
   ↓ (Synthesizes everything)

   Interview Dossier
   (Tailored questions + Strategy)
```

## Configuration

Agents use settings from `src/config.py`:

```python
# .env file
OLLAMA_BASE_URL=http://ollama:11434
LLM_MODEL=llama3
```

## Best Practices

1. **Tone Selection**:

   - Use "friendly" for candidates who need confidence building
   - Use "strict" for senior positions requiring rigorous preparation

2. **Level Selection**:

   - "junior": 0-2 years experience
   - "mid": 2-5 years experience
   - "senior": 5+ years experience

3. **Verbose Mode**:

   - All agents have `verbose=True` for debugging
   - Disable in production for cleaner output

4. **Delegation**:
   - Only Lead Interviewer can delegate
   - Prevents circular dependencies
   - Allows strategic information gathering

## Testing

Run the test script to verify agent creation:

```bash
# Activate virtual environment
source venv/bin/activate

# Run test
python test_agents.py
```

Expected output:

```
🧪 Testing InterviewAgents...
1️⃣ Testing Friendly tone agents...
   ✅ Created 3 agents: ['jd_analyst', 'corporate_researcher', 'lead_interviewer']
...
✅ All tests passed!
```

## Next Steps

After implementing agents, you'll need to:

1. **Define Tasks** (`src/tasks/tasks.py`):

   - Job analysis task
   - Company research task
   - Interview preparation task

2. **Create Crews** (`src/crews/interview_crew.py`):

   - Orchestrate agents and tasks
   - Define execution flow
   - Handle outputs

3. **Update Main** (`src/main.py`):
   - Initialize agents
   - Create and run crews
   - Process results

## Troubleshooting

### Issue: "No module named 'crewai'"

**Solution**: Install dependencies

```bash
pip install -r requirements.txt
```

### Issue: "Connection refused to Ollama"

**Solution**: Start Ollama service

```bash
docker-compose up ollama -d
```

### Issue: "ChatOllama not found"

**Solution**: Install langchain-community

```bash
pip install langchain-community
```

---

_For more information, see the [CrewAI Documentation](https://docs.crewai.com/)_
