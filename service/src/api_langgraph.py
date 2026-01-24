"""
FastAPI Endpoints for LangGraph Interactive Interview System

This module provides REST API endpoints for managing interview sessions.
"""

import uuid
import logging
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Body
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage

from .langgraph.state import create_initial_state
from .langgraph.graph import get_interview_graph

logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api/interview", tags=["Interactive Interview"])


# ===== Request/Response Models =====

class StartInterviewRequest(BaseModel):
    """Request model for starting a new interview session"""
    crewai_result: Dict[str, Any] = Field(..., description="Result from /api/prepare endpoint containing questions")
    job_description: str = Field(..., description="The job description")
    user_cv: str = Field(..., description="The candidate's CV/resume")
    company_name: str = Field(..., description="Company name")
    company_website: Optional[str] = Field(None, description="Company website URL")
    tone: str = Field("friendly", description="Interview tone: friendly or strict")
    level: str = Field("mid", description="Experience level: junior, mid, or senior")


class StartInterviewResponse(BaseModel):
    """Response model for starting an interview"""
    thread_id: str = Field(..., description="Unique session identifier")
    first_question: str = Field(..., description="The first interview question")
    total_questions: int = Field(..., description="Total number of questions")
    question_number: int = Field(..., description="Current question number (1-based)")


class SubmitAnswerRequest(BaseModel):
    """Request model for submitting an answer"""
    answer: str = Field(..., description="The candidate's answer")


class SubmitAnswerResponse(BaseModel):
    """Response model after submitting an answer"""
    feedback: Dict[str, Any] = Field(..., description="Evaluation feedback")
    next_question: Optional[str] = Field(None, description="Next question (if any)")
    progress: Dict[str, int] = Field(..., description="Progress information")
    interview_complete: bool = Field(..., description="Whether interview is finished")


class InterviewSummaryResponse(BaseModel):
    """Response model for interview summary"""
    overall_score: float = Field(..., description="Overall interview score (0-10)")
    total_questions: int = Field(..., description="Total questions answered")
    strengths: list[str] = Field(..., description="Candidate's strengths")
    areas_for_improvement: list[str] = Field(..., description="Areas to improve")
    recommendations: list[str] = Field(..., description="Recommendations")
    performance_breakdown: Dict[str, float] = Field(..., description="Score breakdown")
    detailed_scores: list[Dict[str, Any]] = Field(..., description="Individual question scores")


# ===== Endpoints =====

@router.post("/start", response_model=StartInterviewResponse)
async def start_interview(request: StartInterviewRequest):
    """
    Start a new interactive interview session using questions from CrewAI.
    
    This endpoint:
    1. Creates a new thread_id for the session
    2. Parses questions from CrewAI result
    3. Initializes the interview state
    4. Returns the first question
    
    The questions should come from calling /api/prepare first.
    """
    try:
        # Generate unique thread ID
        thread_id = str(uuid.uuid4())
        logger.info(f"Starting new interview session: {thread_id}")
        
        # Parse questions from CrewAI result
        from .langgraph.nodes import parse_crewai_questions
        questions = parse_crewai_questions(request.crewai_result)
        
        if not questions:
            raise HTTPException(
                status_code=400,
                detail="No questions found in CrewAI result. Please run /api/prepare first."
            )
        
        # Create initial state with questions from CrewAI
        initial_state = create_initial_state(
            job_description=request.job_description,
            user_cv=request.user_cv,
            company_name=request.company_name,
            company_website=request.company_website,
            tone=request.tone,
            level=request.level
        )
        
        # Add parsed questions to state
        initial_state["questions"] = questions
        initial_state["current_index"] = 0
        
        # Get graph
        graph = get_interview_graph()
        
        # Run graph to ask first question
        config = {"configurable": {"thread_id": thread_id}}
        result = graph.invoke(initial_state, config)
        
        # Extract first question from chat history
        first_question = ""
        if result.get("chat_history"):
            first_question = result["chat_history"][-1].content
        
        total_questions = len(questions)
        
        logger.info(f"Session {thread_id}: Starting with {total_questions} questions from CrewAI")
        
        return StartInterviewResponse(
            thread_id=thread_id,
            first_question=first_question,
            total_questions=total_questions,
            question_number=1
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error starting interview: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start interview: {str(e)}")


@router.post("/chat/{thread_id}", response_model=SubmitAnswerResponse)
async def submit_answer(thread_id: str, request: SubmitAnswerRequest):
    """
    Submit an answer and get the next question.
    
    This endpoint:
    1. Resumes the graph from the paused state
    2. Adds the user's answer to chat history
    3. Evaluates the answer
    4. Returns feedback and the next question (if any)
    """
    try:
        logger.info(f"Session {thread_id}: Submitting answer")
        
        # Get graph
        graph = get_interview_graph()
        config = {"configurable": {"thread_id": thread_id}}
        
        # Get current state
        current_state = graph.get_state(config)
        if not current_state or not current_state.values:
            raise HTTPException(status_code=404, detail="Session not found")
        
        state_values = current_state.values
        
        # Add user's answer to chat history
        user_message = HumanMessage(content=request.answer)
        
        # Update state with user's answer and trigger evaluation
        update = {
            "chat_history": [user_message]
        }
        
        # Continue graph execution from evaluate_answer node
        result = graph.invoke(
            update,
            config,
            # Resume from evaluate_answer node
            {"recursion_limit": 10}
        )
        
        # Extract feedback
        current_feedback = result.get("current_feedback", "")
        scores = result.get("scores", [])
        latest_score = scores[-1] if scores else {}
        
        feedback = {
            "score": latest_score.get("score", 0),
            "feedback": current_feedback,
            "strengths": latest_score.get("strengths", []),
            "improvements": latest_score.get("improvements", [])
        }
        
        # Check if interview is complete
        interview_complete = result.get("interview_complete", False)
        
        # Get next question if available
        next_question = None
        if not interview_complete and result.get("chat_history"):
            # Find the last AI message (the next question)
            for msg in reversed(result["chat_history"]):
                if hasattr(msg, 'type') and msg.type == 'ai':
                    next_question = msg.content
                    break
        
        # Progress information
        current_idx = result.get("current_index", 0)
        total_questions = len(result.get("questions", []))
        
        progress = {
            "current": min(current_idx + 1, total_questions),
            "total": total_questions
        }
        
        logger.info(f"Session {thread_id}: Progress {progress['current']}/{progress['total']}")
        
        return SubmitAnswerResponse(
            feedback=feedback,
            next_question=next_question,
            progress=progress,
            interview_complete=interview_complete
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error submitting answer: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to process answer: {str(e)}")


@router.get("/summary/{thread_id}", response_model=InterviewSummaryResponse)
async def get_interview_summary(thread_id: str):
    """
    Get the final interview summary.
    
    This endpoint should be called after the interview is complete.
    """
    try:
        logger.info(f"Session {thread_id}: Fetching summary")
        
        # Get graph
        graph = get_interview_graph()
        config = {"configurable": {"thread_id": thread_id}}
        
        # Get current state
        current_state = graph.get_state(config)
        if not current_state or not current_state.values:
            raise HTTPException(status_code=404, detail="Session not found")
        
        state_values = current_state.values
        
        # Check if interview is complete
        if not state_values.get("interview_complete"):
            raise HTTPException(
                status_code=400,
                detail="Interview not yet complete. Continue answering questions."
            )
        
        # Get summary
        final_summary = state_values.get("final_summary")
        if not final_summary:
            # Generate summary if not already done
            result = graph.invoke(None, config)
            final_summary = result.get("final_summary", {})
        
        # Get detailed scores
        scores = state_values.get("scores", [])
        
        return InterviewSummaryResponse(
            overall_score=final_summary.get("overall_score", 0),
            total_questions=final_summary.get("total_questions", 0),
            strengths=final_summary.get("strengths", []),
            areas_for_improvement=final_summary.get("areas_for_improvement", []),
            recommendations=final_summary.get("recommendations", []),
            performance_breakdown=final_summary.get("performance_breakdown", {}),
            detailed_scores=scores
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching summary: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to get summary: {str(e)}")


@router.delete("/session/{thread_id}")
async def delete_session(thread_id: str):
    """
    Delete an interview session.
    
    This cleans up the session state from memory.
    """
    try:
        logger.info(f"Deleting session: {thread_id}")
        
        # Note: MemorySaver doesn't have a delete method
        # In production with PostgreSQL/Redis, implement proper cleanup
        
        return {"message": f"Session {thread_id} marked for cleanup"}
        
    except Exception as e:
        logger.error(f"Error deleting session: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to delete session: {str(e)}")
