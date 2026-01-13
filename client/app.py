"""
AI Mock Interview Agent - Streamlit Dashboard

A professional, interactive dashboard for interview preparation
powered by CrewAI agents and Groq LLM.
"""

import streamlit as st
import requests
import json
from typing import Dict, Any, List
import time

# Page configuration
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful UI
def local_css():
    st.markdown("""
    <style>
    /* Main container styling */
    .main {
        padding: 2rem;
    }
    
    /* Skill badge styling */
    .skill-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        margin: 0.25rem;
        border-radius: 12px;
        background-color: #e3f2fd;
        color: #1976d2;
        font-size: 0.85rem;
        font-weight: 500;
    }
    
    /* Difficulty badges */
    .difficulty-easy {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        background-color: #c8e6c9;
        color: #2e7d32;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .difficulty-medium {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        background-color: #fff9c4;
        color: #f57f17;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    .difficulty-hard {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        background-color: #ffcdd2;
        color: #c62828;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Question card */
    .question-card {
        padding: 1.5rem;
        border-radius: 8px;
        background-color: #f8f9fa;
        border-left: 4px solid #1976d2;
        margin-bottom: 1rem;
    }
    
    /* STAR framework styling */
    .star-item {
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        background-color: #f5f5f5;
    }
    
    .star-label {
        font-weight: 700;
        color: #1976d2;
        margin-right: 0.5rem;
    }
    
    /* Talking point */
    .talking-point {
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #ff6b6b;
        background-color: #fff5f5;
    }
    
    /* Roadmap item */
    .roadmap-item {
        padding: 0.75rem;
        margin: 0.5rem 0;
        border-radius: 6px;
        background-color: #e8f5e9;
        border-left: 4px solid #4caf50;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
def init_session_state():
    if 'analysis_result' not in st.session_state:
        st.session_state.analysis_result = None
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    if 'roadmap_checks' not in st.session_state:
        st.session_state.roadmap_checks = {}

# Render skill badges
def render_skill_badges(skills: List[str]):
    html = ""
    for skill in skills:
        html += f'<span class="skill-badge">{skill}</span>'
    return html

# Render difficulty badge
def render_difficulty_badge(difficulty: str):
    difficulty_lower = difficulty.lower()
    return f'<span class="difficulty-{difficulty_lower}">{difficulty.upper()}</span>'

# Call backend API
def call_backend_api(job_description: str, user_cv: str, company_name: str, 
                     company_website: str, tone: str, level: str):
    """Call the FastAPI backend to get interview analysis"""
    
    api_url = "http://localhost:8000/api/prepare"
    
    payload = {
        "job_description": job_description,
        "user_cv": user_cv,
        "company_name": company_name,
        "company_website": company_website,
        "tone": tone.lower(),
        "level": level.lower(),
        "interview_type": "mixed"
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=300)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return None

# Render Strategy Tab
def render_strategy_tab(data: Dict[str, Any]):
    st.header("🎯 Interview Strategy & Preparation Roadmap")
    
    strategy = data.get('interview_strategy', {})
    
    # Preparation Roadmap
    st.subheader("📋 Preparation Roadmap")
    roadmap = strategy.get('preparation_roadmap', [])
    
    for idx, item in enumerate(roadmap):
        key = f"roadmap_{idx}"
        if key not in st.session_state.roadmap_checks:
            st.session_state.roadmap_checks[key] = False
        
        col1, col2 = st.columns([0.05, 0.95])
        with col1:
            st.session_state.roadmap_checks[key] = st.checkbox(
                "", 
                value=st.session_state.roadmap_checks[key],
                key=key
            )
        with col2:
            if st.session_state.roadmap_checks[key]:
                st.markdown(f"~~{item}~~")
            else:
                st.markdown(f'<div class="roadmap-item">{item}</div>', 
                          unsafe_allow_html=True)
    
    # Key Talking Points
    st.subheader("🔥 Key Talking Points")
    talking_points = strategy.get('key_talking_points', [])
    for point in talking_points:
        st.markdown(f'<div class="talking-point">🔥 {point}</div>', 
                   unsafe_allow_html=True)
    
    # Addressing Gaps
    st.subheader("⚠️ Areas to Improve")
    gaps = strategy.get('addressing_gaps', [])
    for gap in gaps:
        st.warning(f"📚 {gap}")

# Render Technical Questions Tab
def render_technical_tab(data: Dict[str, Any]):
    st.header("💻 Technical Interview Questions")
    
    questions = data.get('technical_questions', [])
    
    if not questions:
        st.info("No technical questions generated for this interview.")
        return
    
    for idx, q in enumerate(questions, 1):
        with st.container():
            st.markdown(f"""
            <div class="question-card">
                <h4>Question {idx}</h4>
                <p style="font-size: 1.1rem; margin: 1rem 0;">{q['question']}</p>
                <div style="margin-top: 1rem;">
                    {render_difficulty_badge(q.get('difficulty', 'medium'))}
                    {render_skill_badges(q.get('skills_tested', []))}
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Add space for user notes
            with st.expander("📝 Your Answer Notes"):
                st.text_area(
                    "Write your answer here...",
                    key=f"tech_answer_{idx}",
                    height=150
                )

# Render Behavioral Questions Tab
def render_behavioral_tab(data: Dict[str, Any]):
    st.header("🤝 Behavioral Interview Questions (STAR Method)")
    
    questions = data.get('behavioral_questions', [])
    
    if not questions:
        st.info("No behavioral questions generated for this interview.")
        return
    
    for idx, q in enumerate(questions, 1):
        with st.expander(f"❓ Question {idx}: {q['question']}", expanded=False):
            st.markdown(f"**Competency Tested:** {q.get('competency_tested', 'N/A')}")
            
            st.markdown("---")
            st.markdown("### 🌟 STAR Framework Guide")
            
            star = q.get('star_framework', {})
            
            # Situation
            st.markdown(f"""
            <div class="star-item">
                <span class="star-label">🏠 SITUATION:</span>
                {star.get('situation', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
            
            # Task
            st.markdown(f"""
            <div class="star-item">
                <span class="star-label">📋 TASK:</span>
                {star.get('task', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
            
            # Action (highlighted)
            st.markdown(f"""
            <div class="star-item" style="background-color: #fff3e0; border-left: 4px solid #ff9800;">
                <span class="star-label">🎬 ACTION (Most Important):</span>
                {star.get('action', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
            
            # Result
            st.markdown(f"""
            <div class="star-item">
                <span class="star-label">🏆 RESULT:</span>
                {star.get('result', 'N/A')}
            </div>
            """, unsafe_allow_html=True)
            
            # Notes area
            st.markdown("---")
            st.text_area(
                "📝 Your STAR Answer:",
                key=f"behavioral_answer_{idx}",
                height=200,
                placeholder="Write your answer following the STAR framework..."
            )

# Render Company Fit Tab
def render_company_tab(data: Dict[str, Any]):
    st.header("🏢 Company-Specific Questions")
    
    company_questions = data.get('company_specific_questions', [])
    questions_to_ask = data.get('questions_to_ask_interviewer', [])
    
    # Company-specific questions
    st.subheader("Questions About the Company")
    for idx, q in enumerate(company_questions, 1):
        with st.container():
            st.markdown(f"### {idx}. {q['question']}")
            
            if 'related_value' in q:
                st.markdown(f"**Related Company Value:** `{q['related_value']}`")
            
            if 'suggested_approach' in q:
                st.info(f"💡 **Suggested Approach:** {q['suggested_approach']}")
            
            st.text_area(
                "Your Answer:",
                key=f"company_answer_{idx}",
                height=100
            )
            st.markdown("---")
    
    # Questions to ask interviewer
    st.subheader("🎤 Questions to Ask the Interviewer")
    st.markdown("*Asking thoughtful questions shows your interest and engagement!*")
    
    for idx, question in enumerate(questions_to_ask, 1):
        st.markdown(f"{idx}. **{question}**")

# Main application
def main():
    # Apply custom CSS
    local_css()
    
    # Initialize session state
    init_session_state()
    
    # Sidebar
    with st.sidebar:
        st.title("🎯 AI Interview Coach")
        st.markdown("---")
        
        # Mock Data Button
        if st.button("📝 Fill Mock Data", use_container_width=True, type="secondary"):
            st.session_state.mock_job_description = """Senior Python Developer

Requirements:
- 5+ years of Python development experience
- Strong knowledge of Django or Flask
- Experience with PostgreSQL and Redis
- Familiarity with Docker and Kubernetes
- Understanding of RESTful API design
- Experience with CI/CD pipelines

Nice to have:
- Experience with React or Vue.js
- Knowledge of AWS or GCP
- Contributions to open-source projects"""
            
            st.session_state.mock_user_cv = """John Doe - Software Engineer

Experience:
- 6 years of Python development
- Proficient in Django and Flask
- Worked with PostgreSQL, MySQL, and MongoDB
- Experience with Docker
- Built multiple RESTful APIs
- Some experience with React

Skills:
Python, Django, Flask, PostgreSQL, Docker, Git, REST APIs, React

Projects:
- E-commerce platform using Django
- Microservices architecture with Flask
- Database optimization for high-traffic applications"""
            
            st.session_state.mock_company_name = "TechCorp"
            st.session_state.mock_company_website = "https://www.example.com"
            st.session_state.mock_tone = "Friendly"
            st.session_state.mock_level = "Senior"
            st.rerun()
        
        st.markdown("---")
        
        # Input fields
        st.subheader("📄 Job Details")
        
        # Use mock data if available
        default_jd = st.session_state.get('mock_job_description', '')
        default_cv = st.session_state.get('mock_user_cv', '')
        default_company = st.session_state.get('mock_company_name', '')
        default_website = st.session_state.get('mock_company_website', '')
        default_tone = st.session_state.get('mock_tone', 'Friendly')
        default_level = st.session_state.get('mock_level', 'Mid')
        
        job_description = st.text_area(
            "Job Description",
            value=default_jd,
            height=200,
            placeholder="Paste the job description here..."
        )
        
        user_cv = st.text_area(
            "Your CV/Resume",
            value=default_cv,
            height=200,
            placeholder="Paste your CV content here..."
        )
        
        company_name = st.text_input(
            "Company Name",
            value=default_company,
            placeholder="e.g., TechCorp"
        )
        
        company_website = st.text_input(
            "Company Website",
            value=default_website,
            placeholder="https://www.example.com"
        )
        
        st.markdown("---")
        st.subheader("⚙️ Configuration")
        
        # Get index for tone
        tone_options = ["Friendly", "Strict"]
        tone_index = tone_options.index(default_tone) if default_tone in tone_options else 0
        
        tone = st.selectbox(
            "Interview Tone",
            tone_options,
            index=tone_index
        )
        
        # Get index for level
        level_options = ["Junior", "Mid", "Senior"]
        level_index = level_options.index(default_level) if default_level in level_options else 1
        
        level = st.selectbox(
            "Experience Level",
            level_options,
            index=level_index
        )
        
        st.markdown("---")
        
        # Start button
        if st.button("🚀 Start Interview Analysis", type="primary", use_container_width=True):
            if not job_description or not user_cv or not company_name:
                st.error("Please fill in all required fields!")
            else:
                st.session_state.processing = True
                st.rerun()
        
        # Clear button
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.analysis_result = None
            st.session_state.roadmap_checks = {}
            st.rerun()
    
    # Main content
    if st.session_state.processing:
        st.session_state.processing = False
        
        # Show processing status
        with st.status("🤖 AI Agents are analyzing...", expanded=True) as status:
            st.write("📊 JD Analyst is comparing your CV with job requirements...")
            time.sleep(1)
            
            st.write("🔍 Corporate Researcher is analyzing company culture...")
            time.sleep(1)
            
            st.write("🎯 Lead Interviewer is generating personalized questions...")
            
            # Call API
            result = call_backend_api(
                job_description, user_cv, company_name,
                company_website, tone, level
            )
            
            if result and result.get('status') == 'success':
                # Parse the result string to JSON
                result_data = result.get('result', '{}')
                if isinstance(result_data, str):
                    try:
                        result_data = json.loads(result_data)
                    except:
                        pass
                
                st.session_state.analysis_result = result_data
                status.update(label="✅ Analysis Complete!", state="complete")
                time.sleep(0.5)
                st.rerun()
            else:
                status.update(label="❌ Analysis Failed", state="error")
                st.error("Failed to get analysis from backend. Please check the API.")
    
    # Display results
    if st.session_state.analysis_result:
        data = st.session_state.analysis_result
        
        st.title("📊 Your Interview Preparation Dashboard")
        st.markdown("---")
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🎯 Strategy & Roadmap",
            "💻 Technical Round",
            "🤝 Behavioral (STAR)",
            "🏢 Company Fit"
        ])
        
        with tab1:
            render_strategy_tab(data)
        
        with tab2:
            render_technical_tab(data)
        
        with tab3:
            render_behavioral_tab(data)
        
        with tab4:
            render_company_tab(data)
    
    else:
        # Welcome screen
        st.title("🎯 Welcome to AI Interview Coach")
        st.markdown("""
        ### Get personalized interview preparation powered by AI
        
        This tool uses advanced AI agents to:
        - 📊 Analyze job descriptions and match them with your CV
        - 🔍 Research company culture and values
        - 💡 Generate tailored interview questions
        - 🎯 Create a personalized preparation strategy
        
        **Get started by filling in the form on the left sidebar!**
        """)
        
        # Show example
        with st.expander("📖 See Example Output"):
            st.json({
                "technical_questions": [
                    {
                        "question": "Explain RESTful API design principles",
                        "difficulty": "medium",
                        "skills_tested": ["REST", "API Design", "HTTP"]
                    }
                ],
                "behavioral_questions": [
                    {
                        "question": "Tell me about a time you resolved a conflict",
                        "star_framework": {
                            "situation": "Describe the context...",
                            "task": "What was your responsibility...",
                            "action": "What actions did you take...",
                            "result": "What was the outcome..."
                        },
                        "competency_tested": "Conflict Resolution"
                    }
                ]
            })

if __name__ == "__main__":
    main()
