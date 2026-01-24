"""
LangGraph Node Functions for Interactive Interview System

This module implements the core logic for each node in the interview graph.
Questions are provided by CrewAI, LangGraph handles the interactive Q&A.
"""

import json
import logging
from typing import Dict, Any
from langchain_core.messages import AIMessage, HumanMessage
from langchain_groq import ChatGroq
from langchain_core.output_parsers import JsonOutputParser

from .state import InterviewState
from .prompts import (
    EVALUATE_TECHNICAL_ANSWER_PROMPT,
    EVALUATE_BEHAVIORAL_ANSWER_PROMPT,
    GENERATE_SUMMARY_PROMPT
)

logger = logging.getLogger(__name__)


def get_llm() -> ChatGroq:
    """Get configured Groq LLM instance"""
    import os
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY")
    )


def parse_crewai_questions(crewai_result: Dict[str, Any]) -> list:
    """
    Parse questions from CrewAI result into LangGraph format.
    
    Args:
        crewai_result: The result from /api/prepare endpoint
        
    Returns:
        List of questions in LangGraph format
    """
    questions = []
    
    # Extract technical questions
    technical_qs = crewai_result.get('technical_questions', [])
    for q in technical_qs:
        questions.append({
            'question': q.get('question', ''),
            'type': 'technical',
            'expected_points': q.get('skills_tested', []),
            'difficulty': q.get('difficulty', 'medium'),
            'original_data': q  # Keep original for reference
        })
    
    # Extract behavioral questions
    behavioral_qs = crewai_result.get('behavioral_questions', [])
    for q in behavioral_qs:
        questions.append({
            'question': q.get('question', ''),
            'type': 'behavioral',
            'expected_points': [
                q.get('star_framework', {}).get('situation', ''),
                q.get('star_framework', {}).get('task', ''),
                q.get('star_framework', {}).get('action', ''),
                q.get('star_framework', {}).get('result', '')
            ],
            'difficulty': 'medium',
            'competency': q.get('competency_tested', ''),
            'original_data': q
        })
    
    logger.info(f"Parsed {len(questions)} questions from CrewAI result")
    return questions


def ask_question(state: InterviewState) -> Dict[str, Any]:
    """
    Present the current question to the user.
    
    This node adds the question to chat history and sets awaiting_user_input=True,
    which causes the graph to pause until the next API call.
    """
    current_idx = state["current_index"]
    questions = state["questions"]
    
    if current_idx >= len(questions):
        logger.warning("No more questions to ask")
        return {
            "interview_complete": True,
            "awaiting_user_input": False
        }
    
    current_question = questions[current_idx]
    question_text = current_question["question"]
    
    logger.info(f"Asking question {current_idx + 1}/{len(questions)}: {question_text[:50]}...")
    
    # Add question to chat history
    ai_message = AIMessage(content=question_text)
    
    return {
        "chat_history": [ai_message],
        "awaiting_user_input": True
    }


def evaluate_answer(state: InterviewState) -> Dict[str, Any]:
    """
    Evaluate the user's answer to the current question.
    
    This node is called after the user submits their answer via the API.
    """
    current_idx = state["current_index"]
    questions = state["questions"]
    chat_history = state["chat_history"]
    
    if not chat_history or len(chat_history) < 2:
        logger.error("No user answer found in chat history")
        return {"current_feedback": "Error: No answer provided"}
    
    # Get the last user message (their answer)
    user_answer = None
    for msg in reversed(chat_history):
        if isinstance(msg, HumanMessage):
            user_answer = msg.content
            break
    
    if not user_answer:
        return {"current_feedback": "Error: No answer found"}
    
    current_question = questions[current_idx]
    question_type = current_question["type"]
    
    logger.info(f"Evaluating {question_type} answer for question {current_idx + 1}")
    
    llm = get_llm()
    parser = JsonOutputParser()
    
    # Choose appropriate prompt based on question type
    if question_type == "behavioral":
        prompt = EVALUATE_BEHAVIORAL_ANSWER_PROMPT.format(
            question=current_question["question"],
            expected_points="\n".join(f"- {p}" for p in current_question["expected_points"]),
            user_answer=user_answer
        )
    else:  # technical
        prompt = EVALUATE_TECHNICAL_ANSWER_PROMPT.format(
            question=current_question["question"],
            expected_points="\n".join(f"- {p}" for p in current_question["expected_points"]),
            user_answer=user_answer
        )
    
    try:
        response = llm.invoke(prompt)
        evaluation = parser.parse(response.content)
        
        score_entry = {
            "question_index": current_idx,
            "question": current_question["question"],
            "type": question_type,
            "score": evaluation.get("score", 5.0),
            "feedback": evaluation.get("feedback", ""),
            "strengths": evaluation.get("strengths", []),
            "improvements": evaluation.get("improvements", [])
        }
        
        # Add STAR analysis for behavioral questions
        if question_type == "behavioral" and "star_analysis" in evaluation:
            score_entry["star_analysis"] = evaluation["star_analysis"]
        
        logger.info(f"Score: {score_entry['score']}/10")
        
        return {
            "scores": state["scores"] + [score_entry],
            "current_feedback": evaluation.get("feedback", ""),
            "current_index": current_idx + 1,  # Move to next question
            "awaiting_user_input": False
        }
        
    except Exception as e:
        logger.error(f"Error evaluating answer: {e}")
        return {
            "current_feedback": f"Error evaluating answer: {str(e)}",
            "current_index": current_idx + 1,
            "awaiting_user_input": False
        }


def generate_summary(state: InterviewState) -> Dict[str, Any]:
    """
    Generate final interview summary after all questions are answered.
    """
    logger.info("Generating final interview summary...")
    
    scores = state["scores"]
    
    if not scores:
        return {
            "final_summary": {
                "overall_score": 0,
                "total_questions": 0,
                "strengths": [],
                "areas_for_improvement": ["No answers provided"],
                "recommendations": []
            },
            "interview_complete": True
        }
    
    # Calculate averages
    technical_scores = [s["score"] for s in scores if s["type"] == "technical"]
    behavioral_scores = [s["score"] for s in scores if s["type"] == "behavioral"]
    
    technical_avg = sum(technical_scores) / len(technical_scores) if technical_scores else 0
    behavioral_avg = sum(behavioral_scores) / len(behavioral_scores) if behavioral_scores else 0
    overall_avg = sum(s["score"] for s in scores) / len(scores)
    
    # Format scores for prompt
    scores_summary = "\n".join([
        f"Q{i+1} ({s['type']}): {s['score']}/10 - {s['question'][:60]}..."
        for i, s in enumerate(scores)
    ])
    
    llm = get_llm()
    parser = JsonOutputParser()
    
    prompt = GENERATE_SUMMARY_PROMPT.format(
        company_name=state["company_name"],
        total_questions=len(scores),
        scores_summary=scores_summary
    )
    
    try:
        response = llm.invoke(prompt)
        summary = parser.parse(response.content)
        
        # Ensure we have calculated values
        summary["overall_score"] = round(overall_avg, 1)
        summary["total_questions"] = len(scores)
        summary["performance_breakdown"] = {
            "technical_avg": round(technical_avg, 1),
            "behavioral_avg": round(behavioral_avg, 1)
        }
        
        logger.info(f"Summary generated. Overall score: {summary['overall_score']}/10")
        
        return {
            "final_summary": summary,
            "interview_complete": True,
            "awaiting_user_input": False
        }
        
    except Exception as e:
        logger.error(f"Error generating summary: {e}")
        return {
            "final_summary": {
                "overall_score": round(overall_avg, 1),
                "total_questions": len(scores),
                "strengths": ["Completed the interview"],
                "areas_for_improvement": ["Error generating detailed summary"],
                "recommendations": [],
                "performance_breakdown": {
                    "technical_avg": round(technical_avg, 1),
                    "behavioral_avg": round(behavioral_avg, 1)
                }
            },
            "interview_complete": True
        }


def determine_next_step(state: InterviewState) -> str:
    """
    Conditional routing function to determine next step in the interview.
    
    Returns:
        "continue" - More questions remain
        "end" - All questions answered, move to summary
    """
    current_idx = state["current_index"]
    total_questions = len(state["questions"])
    
    if current_idx < total_questions:
        logger.info(f"Continuing to question {current_idx + 1}/{total_questions}")
        return "continue"
    else:
        logger.info("All questions answered, generating summary")
        return "end"
