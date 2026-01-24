"""
Interactive Interview Mode for Streamlit
Uses LangGraph for real-time Q&A with evaluation
"""

import streamlit as st
import requests
from typing import Dict, Any, Optional


def render_interactive_mode():
    """Render the interactive interview interface"""
    
    st.title("🎤 Interactive Interview Mode")
    st.markdown("Practice interview with real-time AI evaluation")
    
    # Initialize session state
    if 'interview_thread_id' not in st.session_state:
        st.session_state.interview_thread_id = None
    if 'interview_active' not in st.session_state:
        st.session_state.interview_active = False
    if 'current_question' not in st.session_state:
        st.session_state.current_question = None
    if 'interview_progress' not in st.session_state:
        st.session_state.interview_progress = {"current": 0, "total": 0}
    if 'interview_history' not in st.session_state:
        st.session_state.interview_history = []
    if 'crewai_result' not in st.session_state:
        st.session_state.crewai_result = None
    
    # Check if we have preparation data
    if not st.session_state.get('analysis_result'):
        st.warning("⚠️ Please run interview preparation first in the 'Report Mode' tab")
        st.info("💡 Go to the sidebar and click '🚀 Start Interview Analysis' to generate questions")
        return
    
    # Start Interview Button
    if not st.session_state.interview_active:
        st.markdown("### Ready to Start?")
        st.info("📋 Questions have been prepared. Click below to begin your interactive interview.")
        
        if st.button("🎬 Start Interactive Interview", type="primary", use_container_width=True):
            start_interactive_interview()
    
    # Active Interview Interface
    if st.session_state.interview_active and st.session_state.current_question:
        render_active_interview()
    
    # Show interview history
    if st.session_state.interview_history:
        render_interview_history()


def start_interactive_interview():
    """Start a new interactive interview session"""
    
    with st.spinner("🚀 Starting interactive interview session..."):
        try:
            # Get the analysis result from session state
            analysis_result = st.session_state.analysis_result
            
            # Call LangGraph start endpoint
            response = requests.post(
                "http://localhost:8000/api/interview/start",
                json={
                    "crewai_result": analysis_result,
                    "job_description": st.session_state.get('input_jd', ''),
                    "user_cv": st.session_state.get('input_cv', ''),
                    "company_name": st.session_state.get('input_company', ''),
                    "company_website": st.session_state.get('input_website', ''),
                    "tone": st.session_state.get('input_tone', 'Friendly').lower(),
                    "level": st.session_state.get('input_level', 'Mid').lower()
                },
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                st.session_state.interview_thread_id = data['thread_id']
                st.session_state.current_question = data['first_question']
                st.session_state.interview_progress = {
                    "current": 1,
                    "total": data['total_questions']
                }
                st.session_state.interview_active = True
                st.session_state.interview_history = []
                st.success("✅ Interview started!")
                st.rerun()
            else:
                st.error(f"❌ Failed to start interview: {response.text}")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def render_active_interview():
    """Render the active interview Q&A interface"""
    
    progress = st.session_state.interview_progress
    
    # Progress bar
    st.progress(progress['current'] / progress['total'])
    st.markdown(f"**Question {progress['current']} of {progress['total']}**")
    
    # Current question
    st.markdown("---")
    st.markdown(f"### ❓ {st.session_state.current_question}")
    st.markdown("---")
    
    # Answer input
    with st.form(key="answer_form", clear_on_submit=True):
        user_answer = st.text_area(
            "Your Answer:",
            height=150,
            placeholder="Type your answer here...",
            key="current_answer_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            submit_button = st.form_submit_button(
                "📤 Submit Answer",
                type="primary",
                use_container_width=True
            )
        with col2:
            end_button = st.form_submit_button(
                "🛑 End Interview",
                use_container_width=True
            )
    
    if end_button:
        end_interview()
        st.rerun()
    
    if submit_button and user_answer:
        submit_answer(user_answer)
        st.rerun()


def submit_answer(answer: str):
    """Submit answer and get next question"""
    
    with st.spinner("🤔 AI is evaluating your answer..."):
        try:
            response = requests.post(
                f"http://localhost:8000/api/interview/chat/{st.session_state.interview_thread_id}",
                json={"answer": answer},
                timeout=60
            )
            
            if response.status_code == 200:
                data = response.json()
                
                # Save to history
                st.session_state.interview_history.append({
                    "question": st.session_state.current_question,
                    "answer": answer,
                    "feedback": data['feedback']
                })
                
                # Update progress
                st.session_state.interview_progress = data['progress']
                
                # Check if interview is complete
                if data['interview_complete']:
                    st.session_state.interview_active = False
                    st.session_state.current_question = None
                    st.success("🎉 Interview Complete! Check the summary below.")
                    show_final_summary()
                else:
                    # Update to next question
                    st.session_state.current_question = data['next_question']
                    
            else:
                st.error(f"❌ Error: {response.text}")
                
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")


def end_interview():
    """End the interview early"""
    st.session_state.interview_active = False
    st.session_state.current_question = None
    st.info("Interview ended. You can review your answers below.")


def render_interview_history():
    """Show the history of Q&A with feedback"""
    
    st.markdown("---")
    st.markdown("## 📝 Interview History")
    
    for idx, item in enumerate(st.session_state.interview_history, 1):
        with st.expander(f"Question {idx}: {item['question'][:60]}...", expanded=False):
            st.markdown(f"**Question:** {item['question']}")
            st.markdown(f"**Your Answer:** {item['answer']}")
            
            feedback = item['feedback']
            
            # Score
            score = feedback.get('score', 0)
            st.metric("Score", f"{score}/10")
            
            # Feedback
            st.markdown(f"**💬 Feedback:**")
            st.info(feedback.get('feedback', 'No feedback available'))
            
            # Strengths
            if feedback.get('strengths'):
                st.markdown("**✅ Strengths:**")
                for strength in feedback['strengths']:
                    st.markdown(f"- {strength}")
            
            # Improvements
            if feedback.get('improvements'):
                st.markdown("**⚠️ Areas for Improvement:**")
                for improvement in feedback['improvements']:
                    st.markdown(f"- {improvement}")


def show_final_summary():
    """Show final interview summary"""
    
    try:
        response = requests.get(
            f"http://localhost:8000/api/interview/summary/{st.session_state.interview_thread_id}",
            timeout=30
        )
        
        if response.status_code == 200:
            summary = response.json()
            
            st.markdown("---")
            st.markdown("## 🎯 Final Interview Summary")
            
            # Overall score
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Score", f"{summary['overall_score']}/10")
            with col2:
                st.metric("Technical Avg", f"{summary['performance_breakdown']['technical_avg']}/10")
            with col3:
                st.metric("Behavioral Avg", f"{summary['performance_breakdown']['behavioral_avg']}/10")
            
            # Strengths
            st.markdown("### ✅ Your Strengths")
            for strength in summary['strengths']:
                st.success(f"✓ {strength}")
            
            # Improvements
            st.markdown("### ⚠️ Areas for Improvement")
            for area in summary['areas_for_improvement']:
                st.warning(f"→ {area}")
            
            # Recommendations
            st.markdown("### 💡 Recommendations")
            for rec in summary['recommendations']:
                st.info(f"💡 {rec}")
                
    except Exception as e:
        st.error(f"❌ Error fetching summary: {str(e)}")
