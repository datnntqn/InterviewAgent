"""
FastAPI server for the AI Mock Interview Agent.

This provides REST API endpoints for the web UI with real CrewAI integration.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Optional, Dict, List
import asyncio
import json
from ai.src.crews import InterviewPreparationCrew
from ai.src.agents import InterviewAgents
from ai.src.tasks import InterviewTasks
from crewai import Crew, Process
import logging
from ai.src.crews.rate_limit_safe_crew import RateLimitSafeCrewAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Suppress LiteLLM warnings about optional dependencies
logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
logging.getLogger("litellm").setLevel(logging.CRITICAL)

app = FastAPI(title="AI Mock Interview Agent API")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include LangGraph router if available
try:
    from .api_langgraph import router as langgraph_router
    app.include_router(langgraph_router)
    logger.info("✅ LangGraph interactive interview endpoints enabled")
    LANGGRAPH_ENABLED = True
except ImportError as e:
    logger.warning(f"⚠️  LangGraph not available: {e}")
    LANGGRAPH_ENABLED = False

# Include combined workflow router
try:
    from .api_combined import router as combined_router
    app.include_router(combined_router)
    logger.info("✅ Combined CrewAI + LangGraph workflow enabled")
except ImportError as e:
    logger.warning(f"⚠️  Combined workflow not available: {e}")


class InterviewRequest(BaseModel):
    """Request model for interview preparation."""
    job_description: str
    user_cv: str
    company_name: str
    company_website: str
    tone: str = "friendly"
    level: str = "mid"
    interview_type: str = "mixed"


@app.get("/")
async def root():
    """Root endpoint."""
    endpoints = {
        "prepare": "/api/prepare",
        "prepare_stream": "/api/prepare-stream",
        "health": "/api/health"
    }
    
    if LANGGRAPH_ENABLED:
        endpoints.update({
            "prepare_and_start": "/api/prepare-and-start (Combined: CrewAI + LangGraph)",
            "interview_start": "/api/interview/start",
            "interview_chat": "/api/interview/chat/{thread_id}",
            "interview_summary": "/api/interview/summary/{thread_id}"
        })
    
    return {
        "message": "AI Mock Interview Agent API",
        "version": "2.0.0",
        "features": {
            "static_report": True,
            "interactive_interview": LANGGRAPH_ENABLED,
            "combined_workflow": LANGGRAPH_ENABLED
        },
        "endpoints": endpoints
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "AI Mock Interview Agent"}


@app.post("/api/prepare-stream")
async def prepare_interview_stream(request: InterviewRequest):
    """
    Prepare for an interview with streaming progress updates.
    
    This endpoint streams progress from each agent as they work.
    """
    async def event_generator():
        try:
            # Send start event
            yield f"data: {json.dumps({'type': 'start', 'message': 'Starting interview preparation...'})}\n\n"
            
            # Create agents and tasks
            agents_factory = InterviewAgents(tone=request.tone, level=request.level)
            tasks_factory = InterviewTasks()
            agents = agents_factory.get_all_agents()
            
            # Task 1: JD Analysis
            yield f"data: {json.dumps({'type': 'agent_start', 'agent': 'JD Analyst', 'message': 'Analyzing job description and comparing with CV...'})}\n\n"
            
            job_task = tasks_factory.analyze_job_description(
                agent=agents["jd_analyst"],
                job_description=request.job_description,
                user_cv=request.user_cv
            )
            
            # Create crew for this task
            crew1 = Crew(
                agents=[agents["jd_analyst"]],
                tasks=[job_task],
                process=Process.sequential,
                verbose=False
            )
            
            job_result = crew1.kickoff()
            
            yield f"data: {json.dumps({'type': 'agent_complete', 'agent': 'JD Analyst', 'message': 'Job analysis completed', 'result': str(job_result)})}\n\n"
            
            # Task 2: Company Research
            yield f"data: {json.dumps({'type': 'agent_start', 'agent': 'Corporate Researcher', 'message': 'Scraping company website for culture information...'})}\n\n"
            
            culture_task = tasks_factory.research_company_culture(
                agent=agents["corporate_researcher"],
                company_name=request.company_name,
                company_website=request.company_website
            )
            
            crew2 = Crew(
                agents=[agents["corporate_researcher"]],
                tasks=[culture_task],
                process=Process.sequential,
                verbose=False
            )
            
            culture_result = crew2.kickoff()
            
            yield f"data: {json.dumps({'type': 'agent_complete', 'agent': 'Corporate Researcher', 'message': 'Company research completed', 'result': str(culture_result)})}\n\n"
            
            # Task 3: Interview Dossier
            yield f"data: {json.dumps({'type': 'agent_start', 'agent': 'Lead Interviewer', 'message': 'Generating interview questions and strategy...'})}\n\n"
            
            dossier_task = tasks_factory.prepare_interview_dossier(
                agent=agents["lead_interviewer"],
                job_analysis=str(job_result),
                company_culture=str(culture_result),
                interview_type=request.interview_type
            )
            dossier_task.context = [job_task, culture_task]
            
            crew3 = Crew(
                agents=[agents["lead_interviewer"]],
                tasks=[dossier_task],
                process=Process.sequential,
                verbose=False
            )
            
            dossier_result = crew3.kickoff()
            
            yield f"data: {json.dumps({'type': 'agent_complete', 'agent': 'Lead Interviewer', 'message': 'Interview dossier completed', 'result': str(dossier_result)})}\n\n"
            
            # Send completion event
            yield f"data: {json.dumps({'type': 'complete', 'message': 'Interview preparation completed successfully!'})}\n\n"
            
        except Exception as e:
            logger.error(f"Error during interview preparation: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


@app.post("/api/prepare")
async def prepare_interview(request: InterviewRequest):
    """
    Prepare for an interview (non-streaming version).
    
    This endpoint runs the full CrewAI workflow with rate limit protection.
    Uses automatic delays between tasks to prevent hitting Groq's TPM limits.
    """
    try:
        logger.info(f"Starting interview preparation for {request.company_name}")
        
        # Use rate-limit safe crew with delays between tasks
        
        crew = RateLimitSafeCrewAI(
            tone=request.tone,
            level=request.level,
            verbose=True,
            delay_between_tasks=20.0  # 20 seconds between tasks
        )
        
        # Run the crew with automatic delays
        result = crew.prepare_interview(
            job_description=request.job_description,
            user_cv=request.user_cv,
            company_name=request.company_name,
            company_website=request.company_website,
            interview_type=request.interview_type
        )
        
        logger.info("Interview preparation completed successfully")
        
        return {
            "status": "success",
            "message": "Interview preparation completed",
            "result": str(result)
        }
        
    except Exception as e:
        logger.error(f"Error during interview preparation: {e}", exc_info=True)
        
        # Check if it's a rate limit error
        error_str = str(e)
        if "rate_limit" in error_str.lower() or "429" in error_str:
            raise HTTPException(
                status_code=429,
                detail={
                    "error": "Rate limit exceeded",
                    "message": "Groq API rate limit reached. Please wait a moment and try again.",
                    "suggestion": "The system uses Groq's free tier which has token limits. Please wait 15-30 seconds before retrying.",
                    "alternative": "Consider switching to llama-3.1-8b-instant model (20k TPM) or Google Gemini (250k TPM)."
                }
            )
        
        raise HTTPException(status_code=500, detail=str(e))



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
