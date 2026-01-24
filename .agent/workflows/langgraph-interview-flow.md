# LangGraph Interactive Interview System - Workflow

## System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AI Mock Interview Agent                       │
│                         (v2.0.0)                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                │                           │
         ┌──────▼──────┐           ┌───────▼────────┐
         │   Static    │           │  Interactive   │
         │   Report    │           │   Interview    │
         │  (CrewAI)   │           │  (LangGraph)   │
         └─────────────┘           └────────────────┘
```

## Interactive Interview Flow

### Phase 1: Session Initialization

```
User/Frontend
     │
     │ POST /api/interview/start
     │ {job_description, user_cv, company_name}
     ▼
┌─────────────────────┐
│  FastAPI Endpoint   │
│   (start_interview) │
└──────────┬──────────┘
           │
           │ 1. Generate thread_id (UUID)
           │ 2. Create initial_state
           │
           ▼
┌─────────────────────────┐
│   LangGraph Workflow    │
│  ┌──────────────────┐   │
│  │ generate_questions│   │ ← Entry Node
│  └────────┬─────────┘   │
│           │              │
│           │ LLM Call     │
│           │ (Groq)       │
│           ▼              │
│  ┌──────────────────┐   │
│  │ 6-8 Questions    │   │
│  │ Generated        │   │
│  └────────┬─────────┘   │
│           │              │
│           ▼              │
│  ┌──────────────────┐   │
│  │  ask_question    │   │
│  │  (index=0)       │   │
│  └────────┬─────────┘   │
│           │              │
│           ▼              │
│         [END]            │ ← Graph Pauses
│    (awaiting_input)      │
└─────────────────────────┘
           │
           │ State saved via Checkpointer
           │
           ▼
     Return to User:
     {
       thread_id,
       first_question,
       total_questions
     }
```

### Phase 2: Q&A Loop (Repeats for each question)

```
User/Frontend
     │
     │ POST /api/interview/chat/{thread_id}
     │ {answer: "user's response"}
     ▼
┌─────────────────────┐
│  FastAPI Endpoint   │
│  (submit_answer)    │
└──────────┬──────────┘
           │
           │ 1. Load state from checkpointer
           │ 2. Add HumanMessage to chat_history
           │
           ▼
┌─────────────────────────────────────┐
│      LangGraph Workflow (Resume)    │
│                                     │
│  ┌──────────────────┐               │
│  │ evaluate_answer  │ ← Resume here │
│  └────────┬─────────┘               │
│           │                         │
│           │ LLM Evaluation          │
│           │ (Technical/Behavioral)  │
│           ▼                         │
│  ┌──────────────────┐               │
│  │ Score: 0-10      │               │
│  │ Feedback         │               │
│  │ Strengths        │               │
│  │ Improvements     │               │
│  └────────┬─────────┘               │
│           │                         │
│           │ Update state:           │
│           │ - scores.append()       │
│           │ - current_index++       │
│           ▼                         │
│  ┌──────────────────────┐           │
│  │ determine_next_step  │           │
│  │   (Conditional)      │           │
│  └──────────┬───────────┘           │
│             │                       │
│        ┌────┴────┐                  │
│        │         │                  │
│    More Qs?   All Done?             │
│        │         │                  │
│        ▼         ▼                  │
│  ┌─────────┐ ┌──────────────┐      │
│  │  ask_   │ │  generate_   │      │
│  │question │ │  summary     │      │
│  └────┬────┘ └──────┬───────┘      │
│       │             │              │
│       ▼             ▼              │
│    [END]         [END]             │
│   (pause)      (complete)          │
└─────────────────────────────────────┘
           │
           ▼
     Return to User:
     {
       feedback: {...},
       next_question: "...",
       progress: {current, total},
       interview_complete: false
     }
```

### Phase 3: Summary Generation

```
User/Frontend
     │
     │ (After interview_complete: true)
     │ GET /api/interview/summary/{thread_id}
     ▼
┌─────────────────────┐
│  FastAPI Endpoint   │
│  (get_summary)      │
└──────────┬──────────┘
           │
           │ Load final state
           │
           ▼
┌─────────────────────────┐
│   Final Summary         │
│  ┌──────────────────┐   │
│  │ Overall Score    │   │
│  │ Strengths        │   │
│  │ Improvements     │   │
│  │ Recommendations  │   │
│  │ Breakdown        │   │
│  └──────────────────┘   │
└─────────────────────────┘
           │
           ▼
     Return to User:
     {
       overall_score: 7.8,
       strengths: [...],
       areas_for_improvement: [...],
       recommendations: [...],
       detailed_scores: [...]
     }
```

## State Transitions

```
State Machine:

[INIT]
  │
  │ generate_questions()
  ▼
[QUESTIONS_READY]
  │
  │ ask_question()
  ▼
[AWAITING_INPUT] ◄──────┐
  │                     │
  │ user submits        │
  │ answer              │
  ▼                     │
[EVALUATING]            │
  │                     │
  │ evaluate_answer()   │
  ▼                     │
[SCORED]                │
  │                     │
  │ determine_next()    │
  ├─────────────────────┘ (more questions)
  │
  │ (all done)
  ▼
[GENERATING_SUMMARY]
  │
  │ generate_summary()
  ▼
[COMPLETE]
```

## Data Flow

```
┌─────────────┐
│   User CV   │
│     +       │
│ Job Desc    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│ LLM (Question   │
│  Generation)    │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Question List   │
│ [Q1, Q2, ...]   │
└──────┬──────────┘
       │
       │ For each question:
       │
       ├──► Present Question
       │         │
       │         ▼
       │    User Answer
       │         │
       │         ▼
       │    ┌──────────────┐
       │    │ LLM (Eval)   │
       │    └──────┬───────┘
       │           │
       │           ▼
       │    ┌──────────────┐
       │    │ Score +      │
       │    │ Feedback     │
       │    └──────┬───────┘
       │           │
       └───────────┘
       │
       │ After all questions:
       │
       ▼
┌─────────────────┐
│ LLM (Summary)   │
└──────┬──────────┘
       │
       ▼
┌─────────────────┐
│ Final Report    │
│ - Overall Score │
│ - Strengths     │
│ - Improvements  │
└─────────────────┘
```

## Component Interaction

```
┌──────────────┐
│   Frontend   │
│  (Streamlit) │
└──────┬───────┘
       │ HTTP REST
       ▼
┌──────────────────┐
│    FastAPI       │
│  ┌────────────┐  │
│  │ /start     │  │
│  │ /chat      │  │
│  │ /summary   │  │
│  └────┬───────┘  │
└───────┼──────────┘
        │
        ▼
┌────────────────────┐
│   LangGraph        │
│  ┌──────────────┐  │
│  │ StateGraph   │  │
│  │ - Nodes      │  │
│  │ - Edges      │  │
│  │ - Checkpoint │  │
│  └──────┬───────┘  │
└─────────┼──────────┘
          │
          ▼
┌────────────────────┐
│   Checkpointer     │
│  (MemorySaver)     │
│                    │
│  thread_id → state │
└────────────────────┘
          │
          ▼
┌────────────────────┐
│   Groq LLM API     │
│  (llama-3.3-70b)   │
└────────────────────┘
```

## File Structure

```
service/
├── src/
│   ├── langgraph/
│   │   ├── __init__.py
│   │   ├── state.py          # InterviewState definition
│   │   ├── nodes.py          # Graph node functions
│   │   ├── graph.py          # StateGraph construction
│   │   └── prompts.py        # LLM prompts
│   │
│   ├── api_langgraph.py      # FastAPI endpoints
│   ├── api.py                # Main API (includes router)
│   └── main.py               # Entry point
│
├── requirements.txt          # Dependencies
└── LANGGRAPH_README.md       # Documentation
```

## Key Design Decisions

1. **Human-in-the-Loop**: Graph pauses at `ask_question` → `END`, resumes on API call
2. **Checkpointing**: State persists across requests using `thread_id`
3. **Conditional Routing**: `determine_next_step` decides continue vs summary
4. **Structured Output**: JSON parsing for reliable LLM responses
5. **Modular Design**: Separate files for state, nodes, graph, prompts
6. **Backward Compatible**: Old `/api/prepare` still works alongside new system

## Performance Considerations

- **LLM Latency**: 5-10 seconds per evaluation
- **State Size**: Grows with chat history (consider truncation)
- **Memory**: In-memory checkpointing not suitable for production
- **Concurrency**: Each thread_id is independent, supports multiple users

## Security Considerations

- **Session Isolation**: thread_id prevents cross-session access
- **Input Validation**: Pydantic models validate all inputs
- **API Rate Limiting**: Consider adding for production
- **Data Privacy**: Interview data stored in memory (ephemeral)
