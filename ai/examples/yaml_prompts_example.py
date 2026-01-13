"""
Example: Using the YAML-based Prompt System

This example shows how to use the new prompt management system
with YAML configuration files.
"""

from ai.src.prompt_loader import get_prompt_loader
from ai.src.config import get_llm
from crewai import Agent, Task

# Initialize the prompt loader
loader = get_prompt_loader()

# Example 1: Create an agent from YAML config
print("=" * 60)
print("Example 1: Creating Agent from YAML")
print("=" * 60)

# Load JD Analyst configuration
jd_config = loader.load_agent_config('jd_analyst')

# Create the agent
jd_analyst = Agent(
    role=jd_config['role'],
    goal=jd_config['goal'],
    backstory=jd_config['backstory'],
    llm=get_llm(),
    verbose=jd_config['settings']['verbose'],
    allow_delegation=jd_config['settings']['allow_delegation']
)

print(f"Agent Role: {jd_analyst.role}")
print(f"Agent Goal: {jd_analyst.goal[:100]}...")
print()

# Example 2: Create agent with tone-based backstory
print("=" * 60)
print("Example 2: Agent with Tone-based Backstory")
print("=" * 60)

# Load Lead Interviewer with friendly tone
lead_config = loader.load_agent_config('lead_interviewer')
friendly_backstory = loader.get_agent_backstory('lead_interviewer', tone='friendly')

lead_interviewer_friendly = Agent(
    role=lead_config['role'],
    goal=lead_config['goal'],
    backstory=friendly_backstory,
    llm=get_llm(),
    verbose=lead_config['settings']['verbose'],
    allow_delegation=lead_config['settings']['allow_delegation']
)

print(f"Friendly Interviewer Backstory: {friendly_backstory[:150]}...")
print()

# Load Lead Interviewer with strict tone
strict_backstory = loader.get_agent_backstory('lead_interviewer', tone='strict')

lead_interviewer_strict = Agent(
    role=lead_config['role'],
    goal=lead_config['goal'],
    backstory=strict_backstory,
    llm=get_llm(),
    verbose=lead_config['settings']['verbose'],
    allow_delegation=lead_config['settings']['allow_delegation']
)

print(f"Strict Interviewer Backstory: {strict_backstory[:150]}...")
print()

# Example 3: Create a task from YAML config
print("=" * 60)
print("Example 3: Creating Task from YAML")
print("=" * 60)

# Sample data
job_description = """
Senior Python Developer
- 5+ years Python experience
- Django, Flask
- PostgreSQL, Redis
"""

user_cv = """
John Doe
- 6 years Python development
- Expert in Django
- PostgreSQL experience
"""

# Format the task description with variables
description = loader.format_task_description(
    'analyze_job_description',
    job_description=job_description,
    user_cv=user_cv
)

# Load task config
task_config = loader.load_task_config('analyze_job_description')

# Create the task
analysis_task = Task(
    description=description,
    expected_output=task_config['expected_output'],
    agent=jd_analyst,
    output_json=task_config['settings']['output_json']
)

print(f"Task Description (first 200 chars): {description[:200]}...")
print(f"Output JSON: {task_config['settings']['output_json']}")
print()

# Example 4: View output schema
print("=" * 60)
print("Example 4: Viewing Output Schema")
print("=" * 60)

schema = task_config['output_schema']
print("Expected Output Schema:")
print(f"  Type: {schema['type']}")
print(f"  Properties:")
for prop_name, prop_def in schema['properties'].items():
    prop_type = prop_def.get('type', 'unknown')
    prop_desc = prop_def.get('description', 'No description')
    print(f"    - {prop_name} ({prop_type}): {prop_desc}")
print()

# Example 5: List all available prompts
print("=" * 60)
print("Example 5: Available Prompts")
print("=" * 60)

available_agents = loader.list_agents()
available_tasks = loader.list_tasks()

print(f"Available Agents: {', '.join(available_agents)}")
print(f"Available Tasks: {', '.join(available_tasks)}")
print()

# Example 6: Accessing nested configuration
print("=" * 60)
print("Example 6: Accessing Nested Configuration")
print("=" * 60)

culture_config = loader.load_task_config('research_company_culture')
tools_required = culture_config['settings'].get('tools_required', [])
context_deps = culture_config['settings'].get('context_dependencies', [])

print(f"Tools Required: {tools_required}")
print(f"Context Dependencies: {context_deps}")
print()

print("=" * 60)
print("All Examples Complete!")
print("=" * 60)
print()
print("Benefits of YAML-based prompts:")
print("  ✓ Easy to read and edit")
print("  ✓ Version control friendly")
print("  ✓ Separate prompts from code")
print("  ✓ Non-developers can review")
print("  ✓ Clear JSON schemas")
print("  ✓ Reusable configurations")
