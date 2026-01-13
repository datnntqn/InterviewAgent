# 🎯 AI Interview Coach - Streamlit Dashboard

A beautiful, interactive web dashboard for AI-powered interview preparation.

## Features

### 📊 **Interactive Dashboard**

- Clean, modern UI with custom CSS styling
- Organized into 4 main tabs for easy navigation
- Real-time processing status updates
- Session state management for persistent data

### 🎯 **Strategy & Roadmap Tab**

- **Interactive Checklist**: Mark off preparation tasks as you complete them
- **Key Talking Points**: Highlighted points to emphasize in your interview
- **Skill Gaps**: Warning boxes showing areas that need improvement

### 💻 **Technical Questions Tab**

- **Visual Question Cards**: Each question in a styled container
- **Difficulty Badges**: Color-coded (Green=Easy, Yellow=Medium, Red=Hard)
- **Skill Tags**: Pill-shaped badges showing skills being tested
- **Answer Notes**: Text areas to practice your responses

### 🤝 **Behavioral Questions Tab**

- **STAR Framework Guide**: Structured guidance for each question
  - 🏠 **Situation**: Context setting
  - 📋 **Task**: Your responsibility
  - 🎬 **Action**: What you did (highlighted as most important)
  - 🏆 **Result**: The outcome
- **Expandable Cards**: Click to reveal detailed STAR guidance
- **Practice Areas**: Write and refine your STAR answers

### 🏢 **Company Fit Tab**

- **Company-Specific Questions**: Tailored to the company's values
- **Suggested Approaches**: Tips on how to answer each question
- **Questions to Ask**: Thoughtful questions to ask the interviewer

## Installation

### Prerequisites

- Python 3.10+
- Backend API running on `http://localhost:8000`

### Quick Start

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Start the backend API** (in a separate terminal):

   ```bash
   ./scripts/start_server_new.sh
   ```

3. **Launch the Streamlit dashboard:**

   ```bash
   ./scripts/start_streamlit.sh
   ```

   Or manually:

   ```bash
   streamlit run app.py
   ```

4. **Open your browser:**
   - Dashboard: `http://localhost:8501`
   - Backend API: `http://localhost:8000`

## Usage

### Step 1: Fill in the Sidebar Form

- **Job Description**: Paste the full job posting
- **Your CV/Resume**: Paste your resume content
- **Company Name**: e.g., "TechCorp"
- **Company Website**: e.g., "https://www.techcorp.com"

### Step 2: Configure Settings

- **Interview Tone**: Choose "Friendly" or "Strict"
- **Experience Level**: Select "Junior", "Mid", or "Senior"

### Step 3: Start Analysis

- Click **"🚀 Start Interview Analysis"**
- Watch the AI agents work in real-time
- Wait for the analysis to complete (~30-60 seconds)

### Step 4: Review Your Dashboard

Navigate through the tabs to:

- ✅ Check off preparation tasks
- 📝 Practice answering questions
- 💡 Review strategy and talking points
- 🎯 Prepare company-specific responses

## Architecture

```
app.py (Streamlit Frontend)
    ↓
    HTTP POST to http://localhost:8000/api/prepare
    ↓
FastAPI Backend (service/src/api.py)
    ↓
CrewAI Agents (ai/src/)
    ↓
Groq LLM (Cloud API)
```

## Custom Styling

The dashboard uses custom CSS for:

- **Skill Badges**: Blue pill-shaped tags
- **Difficulty Badges**: Color-coded (Green/Yellow/Red)
- **Question Cards**: Styled containers with left border
- **STAR Items**: Highlighted framework sections
- **Talking Points**: Red-accented boxes
- **Roadmap Items**: Green-accented checkboxes

## Session State

The app uses Streamlit's session state to persist:

- Analysis results across interactions
- Roadmap checkbox states
- User's answer notes

## API Integration

### Endpoint

```
POST http://localhost:8000/api/prepare
```

### Request Payload

```json
{
  "job_description": "string",
  "user_cv": "string",
  "company_name": "string",
  "company_website": "string",
  "tone": "friendly" | "strict",
  "level": "junior" | "mid" | "senior",
  "interview_type": "mixed"
}
```

### Response Format

```json
{
  "status": "success",
  "result": {
    "technical_questions": [...],
    "behavioral_questions": [...],
    "company_specific_questions": [...],
    "interview_strategy": {...},
    "questions_to_ask_interviewer": [...]
  }
}
```

## Troubleshooting

### Backend Not Running

```
⚠️ Backend API is not running!
```

**Solution**: Start the backend with `./scripts/start_server_new.sh`

### API Connection Error

```
API Error: Connection refused
```

**Solution**: Ensure backend is running on port 8000

### Missing Dependencies

```
ModuleNotFoundError: No module named 'streamlit'
```

**Solution**: Run `pip install -r requirements.txt`

## Development

### Adding New Features

1. **New Tab**: Add to the `st.tabs()` list and create a render function
2. **Custom Styling**: Update the `local_css()` function
3. **New API Fields**: Update the `call_backend_api()` function

### File Structure

```
app.py                      # Main Streamlit application
scripts/start_streamlit.sh  # Launcher script
requirements.txt            # Python dependencies
```

## Tips for Best Results

1. **Detailed Job Description**: Include all requirements and responsibilities
2. **Complete CV**: Provide comprehensive experience and skills
3. **Accurate Company Info**: Use the official company website
4. **Practice Regularly**: Use the answer notes to refine responses
5. **Check Off Tasks**: Use the roadmap to track your preparation

## Future Enhancements

- [ ] PDF upload for CV
- [ ] Export dashboard as PDF report
- [ ] Mock interview recording
- [ ] Progress tracking over time
- [ ] Multi-language support
- [ ] Interview scheduling integration

## Support

For issues or questions:

1. Check the backend logs: `./scripts/start_server_new.sh`
2. Check Streamlit logs in the terminal
3. Verify API health: `curl http://localhost:8000/api/health`

---

**Built with ❤️ using Streamlit, FastAPI, CrewAI, and Groq LLM**
