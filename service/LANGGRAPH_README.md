# LangGraph Interactive Interview System

## Overview

The LangGraph Interactive Interview System transforms the AI Mock Interview Agent from a static report generator into a **real-time, conversational interview simulator**. Using LangGraph's stateful workflow capabilities, candidates can now engage in actual Q&A sessions with AI-powered evaluation and feedback.

## Architecture

### State Management

The system uses `InterviewState` (TypedDict) to maintain conversation context across multiple API calls:

```python
InterviewState:
  - job_description, user_cv, company_name  # Context
  - questions: List[Dict]                    # Generated questions
  - current_index: int                       # Current question tracker
  - chat_history: List[BaseMessage]          # Full conversation
  - scores: List[Dict]                       # Evaluation results
  - awaiting_user_input: bool                # Pause control
  - interview_complete: bool                 # Completion flag
```

### Graph Workflow

```
┌─────────────────────┐
│ generate_questions  │ ← Entry Point
└──────────┬──────────┘
           │
           ▼
    ┌──────────────┐
    │ ask_question │
    └──────┬───────┘
           │
           ▼
        [PAUSE] ← Awaiting user input
           │
           │ (User submits answer via API)
           ▼
   ┌────────────────┐
   │ evaluate_answer│
   └────────┬───────┘
            │
            ▼
   ┌─────────────────────┐
   │ determine_next_step │ (Conditional)
   └─────────┬───────────┘
             │
        ┌────┴────┐
        │         │
    Continue     End
        │         │
        ▼         ▼
 ask_question  generate_summary
                    │
                    ▼
                  [END]
```

### Human-in-the-Loop

The graph **pauses** after `ask_question` by returning `END`. The state is persisted via checkpointing. When the user submits an answer through the API, the graph **resumes** from `evaluate_answer`.

## API Endpoints

### 1. Start Interview Session

**POST** `/api/interview/start`

Initializes a new interview session and returns the first question.

**Request:**

```json
{
  "job_description": "Senior Python Developer...",
  "user_cv": "John Doe - 6 years experience...",
  "company_name": "TechCorp",
  "company_website": "https://techcorp.com",
  "tone": "friendly",
  "level": "senior"
}
```

**Response:**

```json
{
  "thread_id": "550e8400-e29b-41d4-a716-446655440000",
  "first_question": "Tell me about your experience with Python and Django.",
  "total_questions": 7,
  "question_number": 1
}
```

### 2. Submit Answer

**POST** `/api/interview/chat/{thread_id}`

Submit an answer and receive feedback + next question.

**Request:**

```json
{
  "answer": "I have 6 years of Python experience, primarily using Django for web applications..."
}
```

**Response:**

```json
{
  "feedback": {
    "score": 8.5,
    "feedback": "Excellent answer! You provided specific examples...",
    "strengths": ["Detailed experience", "Concrete examples"],
    "improvements": ["Could mention more about scalability"]
  },
  "next_question": "Explain how you would design a RESTful API...",
  "progress": {
    "current": 2,
    "total": 7
  },
  "interview_complete": false
}
```

### 3. Get Final Summary

**GET** `/api/interview/summary/{thread_id}`

Retrieve the complete interview evaluation (call after `interview_complete: true`).

**Response:**

```json
{
  "overall_score": 7.8,
  "total_questions": 7,
  "strengths": [
    "Strong technical foundation in Python",
    "Good communication skills",
    "Provides concrete examples"
  ],
  "areas_for_improvement": [
    "Could elaborate more on system design",
    "Practice STAR method for behavioral questions"
  ],
  "recommendations": [
    "Review distributed systems patterns",
    "Study microservices architecture"
  ],
  "performance_breakdown": {
    "technical_avg": 8.2,
    "behavioral_avg": 7.4
  },
  "detailed_scores": [...]
}
```

## Usage Example

### Python Client

```python
import requests

API_BASE = "http://localhost:8000/api/interview"

# 1. Start interview
response = requests.post(f"{API_BASE}/start", json={
    "job_description": "Senior Python Developer...",
    "user_cv": "John Doe...",
    "company_name": "TechCorp",
    "tone": "friendly",
    "level": "senior"
})

data = response.json()
thread_id = data["thread_id"]
print(f"Q1: {data['first_question']}")

# 2. Answer questions
while True:
    answer = input("Your answer: ")

    response = requests.post(
        f"{API_BASE}/chat/{thread_id}",
        json={"answer": answer}
    )

    result = response.json()

    # Show feedback
    print(f"\nScore: {result['feedback']['score']}/10")
    print(f"Feedback: {result['feedback']['feedback']}\n")

    if result["interview_complete"]:
        break

    # Next question
    print(f"Q{result['progress']['current']}: {result['next_question']}")

# 3. Get summary
summary = requests.get(f"{API_BASE}/summary/{thread_id}").json()
print(f"\nFinal Score: {summary['overall_score']}/10")
print(f"Strengths: {', '.join(summary['strengths'])}")
```

### cURL Examples

```bash
# Start interview
curl -X POST http://localhost:8000/api/interview/start \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "Senior Python Developer",
    "user_cv": "John Doe - 6 years experience",
    "company_name": "TechCorp"
  }'

# Submit answer
curl -X POST http://localhost:8000/api/interview/chat/THREAD_ID \
  -H "Content-Type: application/json" \
  -d '{"answer": "I have 6 years of Python experience..."}'

# Get summary
curl http://localhost:8000/api/interview/summary/THREAD_ID
```

## Technical Details

### State Persistence

- **Development:** Uses `MemorySaver` (in-memory checkpointing)
- **Production:** Recommended to use `PostgresSaver` or `RedisSaver`

### Session Management

- Each session identified by unique `thread_id` (UUID4)
- State persists across API calls via LangGraph checkpointing
- Sessions remain in memory until server restart (dev mode)

### LLM Integration

- Uses **Groq** with `llama-3.3-70b-versatile` model
- Structured output with `JsonOutputParser` for reliability
- Separate prompts for technical vs behavioral evaluation

### Error Handling

- Graceful fallbacks for LLM failures
- Session validation on each request
- Detailed error messages in responses

## Deployment

### Install Dependencies

```bash
cd service
pip install -r requirements.txt
```

### Environment Variables

```bash
# .env file
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_NAME=llama-3.3-70b-versatile
```

### Run Server

```bash
# From project root
./scripts/start_server_new.sh

# Or directly
cd service
uvicorn src.api:app --reload --port 8000
```

### Verify Installation

```bash
curl http://localhost:8000/
```

Should return:

```json
{
  "message": "AI Mock Interview Agent API",
  "version": "2.0.0",
  "features": {
    "static_report": true,
    "interactive_interview": true
  }
}
```

## Comparison: Static vs Interactive

| Feature     | Static Report        | Interactive Interview   |
| ----------- | -------------------- | ----------------------- |
| Endpoint    | `/api/prepare`       | `/api/interview/*`      |
| Interaction | One-shot             | Multi-turn conversation |
| Feedback    | Final report only    | Real-time per question  |
| State       | Stateless            | Stateful (checkpointed) |
| Use Case    | Preparation overview | Practice interview      |

## Future Enhancements

- [ ] PostgreSQL/Redis checkpointing for production
- [ ] Session expiry and cleanup
- [ ] Resume interrupted interviews
- [ ] Multi-language support
- [ ] Voice input/output integration
- [ ] Video interview simulation

## Troubleshooting

### LangGraph Not Available

If you see: `⚠️ LangGraph not available`

```bash
pip install langgraph langchain-core langchain-groq
```

### Session Not Found

- Ensure you're using the correct `thread_id`
- Check if server was restarted (in-memory sessions are lost)

### Slow Responses

- LLM calls can take 5-10 seconds
- Consider implementing response streaming
- Use faster models for development

## License

Same as main project.
