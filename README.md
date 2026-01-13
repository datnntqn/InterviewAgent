# 🎯 AI Mock Interview Agent

An intelligent interview preparation system powered by **CrewAI**, **Groq LLM**, and **Streamlit**.

## 🌟 Features

- **AI-Powered Analysis**: Multi-agent system analyzes job descriptions and CVs
- **Company Research**: Automated company culture and values research
- **Personalized Questions**: Technical, behavioral, and company-specific questions
- **STAR Framework**: Structured guidance for behavioral questions
- **Interactive Dashboard**: Beautiful Streamlit UI for interview preparation
- **Real-time Processing**: Watch AI agents work in real-time

## 📁 Project Structure

```
Interview-Agent/
├── ai/                          # AI/Agent Layer
│   ├── prompts/                # YAML-based prompt configurations
│   │   ├── agents/            # Agent configurations
│   │   └── tasks/             # Task configurations
│   ├── src/
│   │   ├── agents/            # CrewAI agents
│   │   ├── tasks/             # CrewAI tasks
│   │   ├── crews/             # Crew definitions
│   │   ├── models/            # Pydantic output models
│   │   ├── tools/             # Custom tools
│   │   ├── config.py          # LLM configuration
│   │   └── prompt_loader.py   # YAML prompt loader
│   └── requirements.txt
│
├── service/                     # Backend API Layer
│   ├── src/
│   │   ├── api.py             # FastAPI endpoints
│   │   └── main.py            # Application entry
│   └── requirements.txt
│
├── client/                      # Frontend Layer
│   ├── app.py                  # Streamlit dashboard
│   ├── public/                 # Static assets
│   └── README.md               # Client documentation
│
├── scripts/                     # Utility scripts
│   ├── start_server_new.sh    # Start FastAPI backend
│   └── start_streamlit.sh     # Start Streamlit frontend
│
├── docs/                        # Documentation
└── requirements.txt             # Main dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Groq API Key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd Interview-Agent
   ```

2. **Create virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**
   ```bash
   cp .env.example .env
   # Edit .env and add your GROQ_API_KEY
   ```

### Running the Application

#### Option 1: Full Stack (Recommended)

**Terminal 1 - Backend API:**

```bash
./scripts/start_server_new.sh
```

**Terminal 2 - Streamlit Dashboard:**

```bash
./scripts/start_streamlit.sh
```

Then open:

- **Dashboard**: http://localhost:8501
- **API Docs**: http://localhost:8000/docs

#### Option 2: API Only

```bash
./scripts/start_server_new.sh
```

Access API at: http://localhost:8000

## 🎨 Using the Dashboard

1. **Fill in the sidebar:**

   - Job Description
   - Your CV/Resume
   - Company Name
   - Company Website

2. **Configure settings:**

   - Interview Tone (Friendly/Strict)
   - Experience Level (Junior/Mid/Senior)

3. **Start Analysis:**

   - Click "🚀 Start Interview Analysis"
   - Watch AI agents process your data

4. **Explore Results:**
   - **Strategy Tab**: Preparation roadmap and key points
   - **Technical Tab**: Technical questions with difficulty levels
   - **Behavioral Tab**: STAR framework guidance
   - **Company Fit Tab**: Company-specific questions

## 🏗️ Architecture

### Data Flow

```
Streamlit UI (client/app.py)
    ↓ HTTP POST
FastAPI Backend (service/src/api.py)
    ↓
CrewAI Orchestration (ai/src/crews/)
    ↓
AI Agents (ai/src/agents/)
    ↓ Execute
Tasks (ai/src/tasks/)
    ↓ Use
Prompts (ai/prompts/*.yaml)
    ↓ Call
Groq LLM API
    ↓
Structured JSON Output (ai/src/models/)
```

### Key Components

#### 1. **AI Layer** (`ai/`)

- **Agents**: JD Analyst, Corporate Researcher, Lead Interviewer
- **Tasks**: Job analysis, company research, dossier preparation
- **Prompts**: YAML-based configurations for maintainability
- **Models**: Pydantic schemas for type-safe outputs

#### 2. **Service Layer** (`service/`)

- **FastAPI**: RESTful API with streaming support
- **Endpoints**: `/api/prepare`, `/api/prepare-stream`, `/api/health`
- **CORS**: Enabled for frontend integration

#### 3. **Client Layer** (`client/`)

- **Streamlit**: Interactive web dashboard
- **Custom CSS**: Professional, modern design
- **Session State**: Persistent data across interactions

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL_NAME=llama-3.3-70b-versatile

# Optional: Logging
LOG_LEVEL=INFO
```

### Prompt Customization

Edit YAML files in `ai/prompts/`:

**Agents** (`ai/prompts/agents/*.yaml`):

```yaml
role: "Senior Technical Recruiter"
goal: "Analyze job descriptions..."
backstory: "You are an expert..."
settings:
  verbose: true
  allow_delegation: false
```

**Tasks** (`ai/prompts/tasks/*.yaml`):

```yaml
name: "analyze_job_description"
description_template: "Analyze {job_description}..."
output_schema:
  type: "object"
  properties: { ... }
```

## 📚 API Documentation

### Endpoints

#### `POST /api/prepare`

Synchronous interview preparation.

**Request:**

```json
{
  "job_description": "string",
  "user_cv": "string",
  "company_name": "string",
  "company_website": "string",
  "tone": "friendly",
  "level": "mid",
  "interview_type": "mixed"
}
```

**Response:**

```json
{
  "status": "success",
  "result": {
    "technical_questions": [...],
    "behavioral_questions": [...],
    "company_specific_questions": [...],
    "interview_strategy": {...}
  }
}
```

#### `POST /api/prepare-stream`

Streaming interview preparation with real-time updates.

#### `GET /api/health`

Health check endpoint.

## 🧪 Testing

```bash
# Test backend API
curl http://localhost:8000/api/health

# Test with sample data
curl -X POST http://localhost:8000/api/prepare \
  -H "Content-Type: application/json" \
  -d @sample_request.json
```

## 📖 Documentation

- **AI Layer**: See `ai/prompts/README.md`
- **Client Layer**: See `client/README.md`
- **Groq Migration**: See `docs/GROQ_MIGRATION.md`
- **Structure Overview**: See `docs/STRUCTURE_OVERVIEW.md`

## 🛠️ Development

### Adding New Features

1. **New Agent**: Create YAML in `ai/prompts/agents/`
2. **New Task**: Create YAML in `ai/prompts/tasks/`
3. **New Endpoint**: Add to `service/src/api.py`
4. **UI Update**: Modify `client/app.py`

### Code Style

- **Python**: Follow PEP 8
- **YAML**: Use 2-space indentation
- **Prompts**: Keep clear and specific

## 🐛 Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Should be 3.10+

# Reinstall dependencies
pip install -r requirements.txt

# Check Groq API key
echo $GROQ_API_KEY
```

### Streamlit errors

```bash
# Reinstall Streamlit
pip install --upgrade streamlit

# Clear cache
streamlit cache clear
```

### API connection errors

```bash
# Verify backend is running
curl http://localhost:8000/api/health

# Check logs
tail -f logs/api.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

[Your License Here]

## 🙏 Acknowledgments

- **CrewAI**: Multi-agent orchestration
- **Groq**: Fast LLM inference
- **Streamlit**: Beautiful web dashboards
- **FastAPI**: Modern Python web framework

## 📧 Support

For issues or questions:

- Check the documentation in `docs/`
- Review `client/README.md` for UI help
- Check API docs at http://localhost:8000/docs

---

**Built with ❤️ using CrewAI, Groq, Streamlit, and FastAPI**
