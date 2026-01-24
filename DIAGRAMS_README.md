# System Flow Diagrams

This directory contains PlantUML diagrams documenting the AI Mock Interview Agent system architecture and workflows.

## 📊 Available Diagrams

### 1. `architecture.puml` - System Architecture

**Component diagram** showing the complete system architecture with all layers and their interactions.

**Includes:**

- Frontend Layer (Streamlit)
- Backend Layer (FastAPI)
- AI Processing Layer (CrewAI + LangGraph)
- External Services (Groq LLM)
- Data Models

**View:** Shows how components communicate and data flows between layers.

### 2. `flow_report_mode.puml` - Report Mode Sequence

**Sequence diagram** for the CrewAI question generation workflow.

**Flow:**

1. User fills form and clicks "Start Analysis"
2. FastAPI receives request
3. CrewAI orchestrates 3 agents sequentially:
   - JD Analyst: Analyzes job description vs CV
   - Corporate Researcher: Researches company culture
   - Lead Interviewer: Generates interview questions
4. Results returned to Streamlit dashboard

**Duration:** ~30-60 seconds

### 3. `flow_interactive_mode.puml` - Interactive Mode Sequence

**Sequence diagram** for the LangGraph interactive interview workflow.

**Flow:**

1. User starts interactive interview
2. LangGraph creates session with thread_id
3. Q&A Loop:
   - Present question
   - User answers
   - LLM evaluates answer
   - Provide feedback + next question
4. Generate final summary when complete

**Duration:** Varies based on user response time

### 4. `langgraph_state_machine.puml` - LangGraph State Machine

**State diagram** showing the LangGraph state transitions.

**States:**

- Initial State: Parse questions, create state
- Ask Question: Present question, pause
- Waiting for User: State persisted
- Evaluate Answer: Score and provide feedback
- Determine Next: Conditional routing
- Generate Summary: Final report

## 🎨 Viewing Diagrams

### Option 1: Online PlantUML Viewer

1. Go to http://www.plantuml.com/plantuml/uml/
2. Copy content from `.puml` file
3. Paste and view

### Option 2: VS Code Extension

1. Install "PlantUML" extension
2. Open `.puml` file
3. Press `Alt+D` to preview

### Option 3: Command Line

```bash
# Install PlantUML
brew install plantuml  # macOS
# or
sudo apt-get install plantuml  # Linux

# Generate PNG
plantuml architecture.puml
plantuml flow_report_mode.puml
plantuml flow_interactive_mode.puml
plantuml langgraph_state_machine.puml

# Output: *.png files
```

### Option 4: Docker

```bash
docker run -v $(pwd):/data plantuml/plantuml architecture.puml
```

## 📝 Diagram Descriptions

### System Architecture (`architecture.puml`)

```
User
  ↓
Streamlit (Report Mode | Interactive Mode)
  ↓
FastAPI (/api/prepare | /api/interview/*)
  ↓
CrewAI (3 Agents) | LangGraph (StateGraph)
  ↓
Groq LLM API
```

### Report Mode Flow (`flow_report_mode.puml`)

```
POST /api/prepare
  ↓
CrewAI Crew Initialization
  ↓
Task 1: JD Analyst → Groq → Job Analysis
  ↓
Task 2: Corporate Researcher → Groq → Company Culture
  ↓
Task 3: Lead Interviewer → Groq → Questions + Strategy
  ↓
Return: {technical_questions, behavioral_questions, strategy}
```

### Interactive Mode Flow (`flow_interactive_mode.puml`)

```
POST /api/interview/start
  ↓
Parse CrewAI Questions → Initialize State
  ↓
ask_question → Return Q1
  ↓
POST /api/interview/chat (User Answer)
  ↓
evaluate_answer → Groq → Feedback + Score
  ↓
determine_next_step
  ├─ More Questions → ask_question (loop)
  └─ All Done → generate_summary → Final Report
```

### State Machine (`langgraph_state_machine.puml`)

```
[*] → InitialState
InitialState → AskQuestion
AskQuestion → WaitingForUser (PAUSE)
WaitingForUser → EvaluateAnswer (User submits)
EvaluateAnswer → DetermineNext
DetermineNext → AskQuestion (more Q's)
DetermineNext → GenerateSummary (done)
GenerateSummary → [*]
```

## 🔑 Key Concepts

### CrewAI Workflow

- **Sequential Process**: Tasks execute in order
- **Context Sharing**: Each task receives previous results
- **Memory**: DISABLED to prevent rate limits
- **Agents**: Specialized roles (Analyst, Researcher, Interviewer)

### LangGraph Workflow

- **Stateful**: State persisted via MemorySaver
- **Human-in-the-Loop**: Graph pauses for user input
- **Thread-based**: Each session has unique thread_id
- **Conditional Routing**: Dynamic flow based on state

### State Management

```python
InterviewState:
  - questions: List[Dict]
  - current_index: int
  - chat_history: List[BaseMessage]
  - scores: List[Dict]
  - awaiting_user_input: bool
  - interview_complete: bool
  - final_summary: Optional[Dict]
```

## 🐛 Common Issues

### Diagram Won't Render

- Check PlantUML syntax
- Ensure all `@startuml` have matching `@enduml`
- Verify component names don't have special characters

### Missing Connections

- Check arrow syntax: `-->`, `->`, `->`
- Verify component names match exactly

## 📚 PlantUML Resources

- **Official Site**: https://plantuml.com/
- **Sequence Diagrams**: https://plantuml.com/sequence-diagram
- **Component Diagrams**: https://plantuml.com/component-diagram
- **State Diagrams**: https://plantuml.com/state-diagram

## 🔄 Updating Diagrams

When updating the system:

1. Modify relevant `.puml` file
2. Regenerate diagram
3. Update this README if needed
4. Commit changes

---

**These diagrams provide a visual understanding of the AI Mock Interview Agent system architecture and workflows.**
