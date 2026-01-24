# 🎯 AI Mock Interview Agent

Hệ thống chuẩn bị phỏng vấn thông minh sử dụng **CrewAI**, **LangGraph**, **Groq LLM**, và **Streamlit**.

## 🌟 Features

### 📋 Report Mode (CrewAI)

- **AI-Powered Analysis**: Multi-agent system phân tích JD và CV
- **Company Research**: Tự động nghiên cứu văn hóa công ty
- **Personalized Questions**: Câu hỏi technical, behavioral, company-specific
- **STAR Framework**: Hướng dẫn chi tiết cho câu hỏi behavioral
- **Strategy & Roadmap**: Lộ trình chuẩn bị phỏng vấn

### 🎤 Interactive Mode (LangGraph)

- **Real-time Q&A**: Phỏng vấn thực tế từng câu một
- **Instant Feedback**: Đánh giá và điểm số ngay lập tức
- **Progress Tracking**: Theo dõi tiến độ phỏng vấn
- **Interview History**: Xem lại tất cả câu hỏi và feedback
- **Final Summary**: Tổng kết chi tiết với điểm số và recommendations

## 📊 System Diagrams

Hệ thống có các PlantUML diagrams chi tiết:

- **`architecture.puml`**: System architecture (component diagram)
- **`flow_report_mode.puml`**: CrewAI workflow (sequence diagram)
- **`flow_interactive_mode.puml`**: LangGraph workflow (sequence diagram)
- **`langgraph_state_machine.puml`**: LangGraph state machine (state diagram)

👉 **Xem hướng dẫn**: `DIAGRAMS_README.md`

## 📁 Project Structure

```
Interview-Agent/
├── ai/                          # AI/Agent Layer (CrewAI)
│   ├── prompts/                # YAML-based prompt configurations
│   │   ├── agents/            # Agent configs (JD Analyst, Researcher, Interviewer)
│   │   └── tasks/             # Task configs (Analysis, Research, Dossier)
│   ├── src/
│   │   ├── agents/            # CrewAI agent implementations
│   │   ├── tasks/             # CrewAI task implementations
│   │   ├── crews/             # Crew orchestration
│   │   ├── models/            # Pydantic output schemas
│   │   ├── tools/             # Custom tools (ScrapeWebsiteTool)
│   │   ├── config.py          # LLM configuration (Groq)
│   │   └── prompt_loader.py   # YAML prompt loader
│   └── requirements.txt
│
├── service/                     # Backend API Layer (FastAPI)
│   ├── src/
│   │   ├── langgraph/         # LangGraph interactive interview
│   │   │   ├── state.py       # InterviewState definition
│   │   │   ├── nodes.py       # Graph nodes (ask, evaluate, summary)
│   │   │   ├── graph.py       # StateGraph construction
│   │   │   └── prompts.py     # LLM prompts for evaluation
│   │   ├── api.py             # Main FastAPI app
│   │   ├── api_langgraph.py   # LangGraph endpoints
│   │   ├── api_combined.py    # Combined workflow endpoint
│   │   └── main.py            # Entry point
│   ├── examples/
│   │   ├── langgraph_demo.py  # Interactive demo
│   │   └── integrated_demo.py # Combined workflow demo
│   └── requirements.txt
│
├── client/                      # Frontend Layer (Streamlit)
│   ├── app.py                  # Main Streamlit dashboard
│   ├── interactive_mode.py     # Interactive interview component
│   ├── config.py               # Constants and mock data
│   ├── styles.py               # Custom CSS
│   ├── utils.py                # Utility functions
│   └── README.md               # Client documentation
│
├── scripts/                     # Utility scripts
│   ├── start_server_new.sh    # Start FastAPI backend
│   └── start_streamlit.sh     # Start Streamlit frontend
│
├── .agent/workflows/           # Workflow documentation
│   └── langgraph-interview-flow.md
│
├── docs/                        # Documentation
├── INTEGRATION_GUIDE_VI.md     # Vietnamese integration guide
├── LANGGRAPH_QUICKSTART.md     # LangGraph quick start
└── requirements.txt             # Main dependencies
```

## 🏗️ System Architecture

### High-Level Overview

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                       │
│                   (client/app.py)                            │
│  ┌────────────────────┐  ┌──────────────────────┐          │
│  │   Report Mode      │  │  Interactive Mode    │          │
│  │   (Static View)    │  │  (Real-time Q&A)     │          │
│  └────────┬───────────┘  └──────────┬───────────┘          │
└───────────┼──────────────────────────┼──────────────────────┘
            │                          │
            ▼                          ▼
┌───────────────────────┐  ┌──────────────────────────┐
│   FastAPI Backend     │  │   FastAPI Backend        │
│   /api/prepare        │  │   /api/interview/*       │
└───────────┬───────────┘  └──────────┬───────────────┘
            │                          │
            ▼                          ▼
┌───────────────────────┐  ┌──────────────────────────┐
│   CrewAI Workflow     │  │   LangGraph Workflow     │
│   (Question Gen)      │  │   (Interactive Q&A)      │
└───────────┬───────────┘  └──────────┬───────────────┘
            │                          │
            └──────────┬───────────────┘
                       ▼
              ┌─────────────────┐
              │   Groq LLM API  │
              │   (llama-3.3)   │
              └─────────────────┘
```

### Component Responsibilities

#### 1. **AI Layer** (`ai/`)

**Purpose**: Question generation and analysis using CrewAI

**Components**:

- **JD Analyst Agent**: Analyzes job description vs CV
- **Corporate Researcher Agent**: Researches company culture
- **Lead Interviewer Agent**: Generates interview questions

**Flow**:

```
Input (JD + CV) → JD Analyst → Corporate Researcher → Lead Interviewer → Questions
```

#### 2. **Service Layer** (`service/`)

**Purpose**: API endpoints and business logic

**Endpoints**:

- `/api/prepare`: CrewAI question generation
- `/api/interview/start`: Start LangGraph session
- `/api/interview/chat/{thread_id}`: Submit answer
- `/api/interview/summary/{thread_id}`: Get final summary
- `/api/prepare-and-start`: Combined workflow

#### 3. **LangGraph Layer** (`service/src/langgraph/`)

**Purpose**: Interactive interview with state management

**Nodes**:

- `ask_question`: Present question to user
- `evaluate_answer`: Score and provide feedback
- `generate_summary`: Create final report

**State**: Persisted via checkpointing (MemorySaver)

#### 4. **Client Layer** (`client/`)

**Purpose**: User interface

**Modes**:

- **Report Mode**: View all questions (static)
- **Interactive Mode**: Practice with feedback (dynamic)

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Groq API Key ([Get one here](https://console.groq.com))

### Installation

```bash
# Clone repository
git clone <your-repo-url>
cd Interview-Agent

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your GROQ_API_KEY
```

### Running the Application

**Terminal 1 - Backend:**

```bash
./scripts/start_server_new.sh
```

**Terminal 2 - Frontend:**

```bash
./scripts/start_streamlit.sh
```

**Access**:

- Dashboard: http://localhost:8501
- API Docs: http://localhost:8000/docs

## 🎨 Usage Workflow

### Report Mode (Static Analysis)

```
1. Fill sidebar form (JD, CV, Company)
   ↓
2. Click "🚀 Start Interview Analysis"
   ↓
3. CrewAI generates questions (30-60s)
   ↓
4. View results in tabs:
   - Strategy & Roadmap
   - Technical Questions
   - Behavioral Questions (STAR)
   - Company Fit
```

### Interactive Mode (Practice Interview)

```
1. Complete Report Mode first
   ↓
2. Switch to "🎤 Interactive Interview"
   ↓
3. Click "🎬 Start Interactive Interview"
   ↓
4. Answer questions one by one
   ↓
5. Receive instant feedback + score
   ↓
6. View final summary with recommendations
```

## 🔧 Configuration

### Environment Variables

```bash
# .env file
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_NAME=llama-3.3-70b-versatile
LOG_LEVEL=INFO
```

### Prompt Customization

Edit YAML files in `ai/prompts/`:

```yaml
# ai/prompts/agents/jd_analyst.yaml
role: "Senior Technical Recruiter"
goal: "Analyze job descriptions and match with candidate profiles"
backstory: "You are an expert in technical recruitment..."
```

## 📚 API Reference

### CrewAI Endpoints

#### `POST /api/prepare`

Generate interview questions using CrewAI.

**Request**:

```json
{
  "job_description": "Senior Python Developer...",
  "user_cv": "John Doe - 6 years...",
  "company_name": "TechCorp",
  "company_website": "https://techcorp.com",
  "tone": "friendly",
  "level": "senior",
  "interview_type": "mixed"
}
```

**Response**:

```json
{
  "status": "success",
  "result": {
    "technical_questions": [...],
    "behavioral_questions": [...],
    "interview_strategy": {...}
  }
}
```

### LangGraph Endpoints

#### `POST /api/interview/start`

Start interactive interview session.

**Request**:

```json
{
  "crewai_result": {
    /* from /api/prepare */
  },
  "job_description": "...",
  "user_cv": "...",
  "company_name": "TechCorp"
}
```

**Response**:

```json
{
  "thread_id": "uuid-1234",
  "first_question": "Tell me about...",
  "total_questions": 7
}
```

#### `POST /api/interview/chat/{thread_id}`

Submit answer and get feedback.

**Request**:

```json
{
  "answer": "I have 6 years of Python experience..."
}
```

**Response**:

```json
{
  "feedback": {
    "score": 8.5,
    "feedback": "Excellent answer...",
    "strengths": [...],
    "improvements": [...]
  },
  "next_question": "...",
  "progress": {"current": 2, "total": 7},
  "interview_complete": false
}
```

## 🐛 Troubleshooting

### Rate Limit Errors

**Problem**: Groq API rate limit exceeded

**Solution**:

- CrewAI memory has been disabled to reduce token usage
- Wait a few minutes between requests
- Consider upgrading Groq API tier

### Backend Won't Start

```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r requirements.txt

# Check Groq API key
echo $GROQ_API_KEY
```

### Streamlit Connection Errors

```bash
# Verify backend is running
curl http://localhost:8000/api/health

# Restart backend
./scripts/start_server_new.sh
```

## 📖 Documentation

- **Integration Guide**: `INTEGRATION_GUIDE_VI.md`
- **LangGraph Quick Start**: `LANGGRAPH_QUICKSTART.md`
- **Workflow Diagram**: `.agent/workflows/langgraph-interview-flow.md`
- **Client Guide**: `client/README.md`

## 🛠️ Development

### Adding New Features

1. **New Agent**: Create YAML in `ai/prompts/agents/`
2. **New Task**: Create YAML in `ai/prompts/tasks/`
3. **New LangGraph Node**: Add to `service/src/langgraph/nodes.py`
4. **New API Endpoint**: Add to `service/src/api.py`
5. **UI Update**: Modify `client/app.py`

### Code Organization

- **Separation of Concerns**: AI, Service, Client layers
- **YAML-based Prompts**: Easy to modify without code changes
- **Type Safety**: Pydantic models for all data structures
- **Modular Design**: Each component is independent

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Your License Here]

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent orchestration framework
- **LangGraph**: Stateful agent workflows
- **Groq**: Fast LLM inference
- **Streamlit**: Interactive web dashboards
- **FastAPI**: Modern Python web framework

---

**Built with ❤️ using CrewAI, LangGraph, Groq, Streamlit, and FastAPI**
