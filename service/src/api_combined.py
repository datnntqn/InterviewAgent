"""
Combined endpoint to prepare interview with CrewAI and start LangGraph session

This provides a convenient single endpoint that:
1. Calls CrewAI to generate questions
2. Starts LangGraph interactive session with those questions
"""

import logging
import requests
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["Combined Workflow"])


class PrepareAndStartRequest(BaseModel):
    """Request for combined prepare + start workflow"""
    job_description: str = Field(..., description="The job description")
    user_cv: str = Field(..., description="The candidate's CV/resume")
    company_name: str = Field(..., description="Company name")
    company_website: str = Field(..., description="Company website URL")
    tone: str = Field("friendly", description="Interview tone: friendly or strict")
    level: str = Field("mid", description="Experience level: junior, mid, or senior")
    interview_type: str = Field("mixed", description="Interview type: technical, behavioral, or mixed")


class PrepareAndStartResponse(BaseModel):
    """Response with both CrewAI result and LangGraph session"""
    crewai_result: dict = Field(..., description="Full result from CrewAI")
    thread_id: str = Field(..., description="LangGraph session ID")
    first_question: str = Field(..., description="First interview question")
    total_questions: int = Field(..., description="Total number of questions")


@router.post("/prepare-and-start", response_model=PrepareAndStartResponse)
async def prepare_and_start_interview(request: PrepareAndStartRequest):
    """
    Combined endpoint: Generate questions with CrewAI, then start interactive interview.
    
    This is a convenience endpoint that combines:
    1. POST /api/prepare (CrewAI question generation)
    2. POST /api/interview/start (LangGraph session initialization)
    
    Returns both the full CrewAI analysis and the LangGraph session details.
    """
    try:
        logger.info(f"Starting combined workflow for {request.company_name}")
        
        # Step 1: Call CrewAI to generate questions
        logger.info("Step 1: Calling CrewAI to generate questions...")
        
        prepare_response = requests.post(
            "http://localhost:8000/api/prepare",
            json={
                "job_description": request.job_description,
                "user_cv": request.user_cv,
                "company_name": request.company_name,
                "company_website": request.company_website,
                "tone": request.tone,
                "level": request.level,
                "interview_type": request.interview_type
            },
            timeout=300
        )
        
        if prepare_response.status_code != 200:
            raise HTTPException(
                status_code=prepare_response.status_code,
                detail=f"CrewAI preparation failed: {prepare_response.text}"
            )
        
        crewai_result = prepare_response.json()
        logger.info("✅ CrewAI questions generated successfully")
        
        # Step 2: Start LangGraph interactive session
        logger.info("Step 2: Starting LangGraph interactive session...")
        
        start_response = requests.post(
            "http://localhost:8000/api/interview/start",
            json={
                "crewai_result": crewai_result.get("result", {}),
                "job_description": request.job_description,
                "user_cv": request.user_cv,
                "company_name": request.company_name,
                "company_website": request.company_website,
                "tone": request.tone,
                "level": request.level
            }
        )
        
        if start_response.status_code != 200:
            raise HTTPException(
                status_code=start_response.status_code,
                detail=f"LangGraph session start failed: {start_response.text}"
            )
        
        session_data = start_response.json()
        logger.info(f"✅ LangGraph session started: {session_data['thread_id']}")
        
        # Return combined result
        return PrepareAndStartResponse(
            crewai_result=crewai_result,
            thread_id=session_data["thread_id"],
            first_question=session_data["first_question"],
            total_questions=session_data["total_questions"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in combined workflow: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail=f"Combined workflow failed: {str(e)}"
        )
