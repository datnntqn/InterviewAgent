"""
LangGraph State Definition for Interactive Interview System

This module defines the state structure for managing interactive interview sessions.
"""

from typing import TypedDict, List, Dict, Annotated, Optional
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages


class InterviewState(TypedDict):
    """
    State for interactive interview sessions.
    
    This state is maintained across multiple API calls using LangGraph's checkpointing.
    """
    
    # ===== Context =====
    job_description: str
    """The job description being interviewed for"""
    
    user_cv: str
    """The candidate's CV/resume"""
    
    company_name: str
    """Name of the company"""
    
    company_website: Optional[str]
    """Company website URL (optional)"""
    
    tone: str
    """Interview tone: 'friendly' or 'strict'"""
    
    level: str
    """Experience level: 'junior', 'mid', or 'senior'"""
    
    # ===== Question Management =====
    questions: List[Dict]
    """
    List of generated questions. Each dict contains:
    - question: str (The question text)
    - type: str ('technical' or 'behavioral')
    - expected_points: List[str] (Key points to cover)
    - difficulty: str ('easy', 'medium', 'hard')
    """
    
    current_index: int
    """Index of the current question being asked (0-based)"""
    
    # ===== Conversation History =====
    chat_history: Annotated[List[BaseMessage], add_messages]
    """
    Full conversation history using LangChain messages.
    Uses add_messages reducer for automatic message management.
    """
    
    # ===== Evaluation & Feedback =====
    current_feedback: str
    """Feedback for the most recent answer"""
    
    scores: List[Dict]
    """
    List of scores for each answered question. Each dict contains:
    - question_index: int
    - score: float (0-10)
    - feedback: str
    - strengths: List[str]
    - improvements: List[str]
    """
    
    # ===== Control Flow =====
    awaiting_user_input: bool
    """Flag indicating the graph is paused waiting for user response"""
    
    interview_complete: bool
    """Flag indicating all questions have been answered"""
    
    # ===== Summary =====
    final_summary: Optional[Dict]
    """
    Final interview summary (populated at the end). Contains:
    - overall_score: float
    - total_questions: int
    - strengths: List[str]
    - areas_for_improvement: List[str]
    - recommendations: List[str]
    """


def create_initial_state(
    job_description: str,
    user_cv: str,
    company_name: str,
    company_website: Optional[str] = None,
    tone: str = "friendly",
    level: str = "mid"
) -> InterviewState:
    """
    Create initial state for a new interview session.
    
    Args:
        job_description: The job posting text
        user_cv: The candidate's CV/resume
        company_name: Name of the company
        company_website: Company website URL (optional)
        tone: Interview tone ('friendly' or 'strict')
        level: Experience level ('junior', 'mid', 'senior')
        
    Returns:
        Initialized InterviewState
    """
    return InterviewState(
        job_description=job_description,
        user_cv=user_cv,
        company_name=company_name,
        company_website=company_website,
        tone=tone,
        level=level,
        questions=[],
        current_index=0,
        chat_history=[],
        current_feedback="",
        scores=[],
        awaiting_user_input=False,
        interview_complete=False,
        final_summary=None
    )
