# Prompt Management System

## Overview

This directory contains structured prompt configurations for agents and tasks using YAML files. This approach provides:

- **Better Readability**: YAML is human-readable and easy to edit
- **Version Control**: Track prompt changes separately from code
- **Maintainability**: Update prompts without touching Python code
- **Collaboration**: Non-developers can review and suggest prompt improvements
- **JSON Schema**: Define expected output structures clearly

## Directory Structure

```
ai/prompts/
├── agents/                          # Agent configurations
│   ├── jd_analyst.yaml             # Job Description Analyst
│   ├── corporate_researcher.yaml   # Company Culture Researcher
│   └── lead_interviewer.yaml       # Lead Interview Manager
│
└── tasks/                           # Task configurations
    ├── analyze_job_description.yaml
    ├── research_company_culture.yaml
    └── prepare_interview_dossier.yaml
```

## Agent Configuration Format

```yaml
# agents/example_agent.yaml

role: "Agent Role Title"

goal: |
  Multi-line description of what the agent should achieve.
  Can include specific instructions and requirements.

backstory: |
  Background story that shapes the agent's behavior.
  Can include personality traits and expertise areas.

  CRITICAL: Instructions for output format.

# For agents with multiple personalities/tones
backstories:
  friendly: |
    Friendly version of backstory...

  strict: |
    Strict version of backstory...

settings:
  verbose: true
  allow_delegation: false
  temperature: 0.7
  tools:
    - tool_name_1
    - tool_name_2
```

## Task Configuration Format

```yaml
# tasks/example_task.yaml

name: "task_identifier"

description_template: |
  Task description with {placeholders} for dynamic content.

  **Input Data:**
  {variable_name}

  Instructions for the agent...

  Expected JSON structure:
  {{
    "field1": "value",
    "field2": ["array", "values"]
  }}

expected_output: |
  Description of what the output should contain.

output_schema:
  type: "object"
  properties:
    field1:
      type: "string"
      description: "Description of field1"

    field2:
      type: "array"
      items:
        type: "string"
      description: "Description of field2"

settings:
  output_json: true
  context_dependencies:
    - "previous_task_name"
  tools_required:
    - "tool_name"
```

## Usage in Python

### Loading Agent Configuration

```python
from ai.src.prompt_loader import get_prompt_loader

# Get the loader instance
loader = get_prompt_loader()

# Load agent config
config = loader.load_agent_config('jd_analyst')

# Access configuration
role = config['role']
goal = config['goal']
backstory = config['backstory']
settings = config['settings']

# For tone-based agents
backstory = loader.get_agent_backstory('lead_interviewer', tone='friendly')
```

### Loading Task Configuration

```python
from ai.src.prompt_loader import get_prompt_loader

loader = get_prompt_loader()

# Load task config
config = loader.load_task_config('analyze_job_description')

# Format description with variables
description = loader.format_task_description(
    'analyze_job_description',
    job_description="Senior Python Developer...",
    user_cv="5 years experience..."
)

# Access output schema
schema = config['output_schema']
```

### Example: Creating an Agent

```python
from crewai import Agent
from ai.src.prompt_loader import get_prompt_loader
from ai.src.config import get_llm

loader = get_prompt_loader()
config = loader.load_agent_config('jd_analyst')

agent = Agent(
    role=config['role'],
    goal=config['goal'],
    backstory=config['backstory'],
    llm=get_llm(),
    verbose=config['settings']['verbose'],
    allow_delegation=config['settings']['allow_delegation']
)
```

### Example: Creating a Task

```python
from crewai import Task
from ai.src.prompt_loader import get_prompt_loader

loader = get_prompt_loader()

# Format the description
description = loader.format_task_description(
    'analyze_job_description',
    job_description=jd_text,
    user_cv=cv_text
)

# Load config for other settings
config = loader.load_task_config('analyze_job_description')

task = Task(
    description=description,
    expected_output=config['expected_output'],
    agent=agent,
    output_json=config['settings']['output_json']
)
```

## Benefits

### 1. **Separation of Concerns**

- Code logic in Python files
- Prompts in YAML files
- Easy to find and update prompts

### 2. **Version Control**

```bash
# See prompt changes
git diff ai/prompts/agents/jd_analyst.yaml

# Review prompt history
git log ai/prompts/tasks/analyze_job_description.yaml
```

### 3. **Collaboration**

- Product managers can review prompts
- Non-developers can suggest improvements
- Clear diff when prompts change

### 4. **Testing**

```python
# Easy to test different prompts
def test_agent_with_different_prompts():
    loader = get_prompt_loader()

    # Test version 1
    config_v1 = loader.load_agent_config('jd_analyst')
    agent_v1 = create_agent(config_v1)
    result_v1 = run_test(agent_v1)

    # Compare with version 2
    # (after updating YAML file)
    config_v2 = loader.load_agent_config('jd_analyst')
    agent_v2 = create_agent(config_v2)
    result_v2 = run_test(agent_v2)
```

### 5. **Documentation**

- YAML files serve as documentation
- JSON schemas define expected outputs
- Easy to generate API documentation from schemas

## Best Practices

### 1. **Use Clear Variable Names**

```yaml
# Good
description_template: |
  Analyze {job_description} and compare with {user_cv}

# Bad
description_template: |
  Analyze {jd} and compare with {cv}
```

### 2. **Include JSON Schemas**

Always define the expected output structure:

```yaml
output_schema:
  type: "object"
  properties:
    # Define all expected fields
```

### 3. **Add Comments**

```yaml
# This agent analyzes technical job descriptions
role: "Senior Technical Recruiter"

# Temperature 0.7 balances creativity and consistency
settings:
  temperature: 0.7
```

### 4. **Version Your Prompts**

```yaml
# Version: 2.0
# Last Updated: 2026-01-13
# Changes: Added JSON output enforcement
```

### 5. **Test After Changes**

Always test agents/tasks after updating prompts:

```bash
python -m pytest ai/tests/test_prompts.py
```

## Migration from Hardcoded Prompts

To migrate existing hardcoded prompts:

1. **Extract the prompt** from Python code
2. **Create YAML file** in appropriate directory
3. **Update Python code** to use PromptLoader
4. **Test thoroughly**
5. **Commit both** YAML and Python changes together

Example:

```python
# Before
backstory = "You are an expert..."

# After
loader = get_prompt_loader()
config = loader.load_agent_config('jd_analyst')
backstory = config['backstory']
```

## Future Enhancements

- [ ] Add prompt versioning system
- [ ] Create prompt validation tool
- [ ] Generate documentation from YAML files
- [ ] Add A/B testing framework for prompts
- [ ] Create prompt optimization tools
- [ ] Add multi-language support

## Contributing

When adding new prompts:

1. Create YAML file in appropriate directory
2. Follow the format guidelines above
3. Include JSON schema for tasks
4. Add usage example in this README
5. Test with actual agents/tasks
6. Submit PR with clear description

---

For questions or suggestions, see the main project README.
