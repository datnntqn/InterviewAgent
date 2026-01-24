"""
LangGraph StateGraph Construction for Interactive Interview System

This module builds the complete interview workflow graph with checkpointing.
Questions are provided by CrewAI, this graph handles the Q&A interaction.
"""

import logging
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver

from .state import InterviewState
from .nodes import (
    ask_question,
    evaluate_answer,
    generate_summary,
    determine_next_step
)

logger = logging.getLogger(__name__)


def create_interview_graph():
    """
    Build and compile the interview workflow graph.
    
    Graph Flow (Questions from CrewAI):
    1. ask_question (entry) -> END (pause for user input)
    2. User submits answer via API -> evaluate_answer
    3. evaluate_answer -> determine_next_step (conditional)
       - If more questions: -> ask_question
       - If done: -> generate_summary -> END
    
    Returns:
        Compiled StateGraph with memory checkpointing
    """
    logger.info("Creating interview StateGraph...")
    
    # Initialize graph
    workflow = StateGraph(InterviewState)
    
    # Add nodes (NO generate_questions - questions come from CrewAI)
    workflow.add_node("ask_question", ask_question)
    workflow.add_node("evaluate_answer", evaluate_answer)
    workflow.add_node("generate_summary", generate_summary)
    
    # Set entry point - start by asking first question
    workflow.set_entry_point("ask_question")
    
    # Define edges
    # After asking a question, pause (END) to wait for user input
    workflow.add_edge("ask_question", END)
    
    # After evaluating, use conditional routing
    workflow.add_conditional_edges(
        "evaluate_answer",
        determine_next_step,
        {
            "continue": "ask_question",  # More questions remain
            "end": "generate_summary"     # All questions answered
        }
    )
    
    # After summary, end the interview
    workflow.add_edge("generate_summary", END)
    
    # Add checkpointing for state persistence
    memory = MemorySaver()
    
    logger.info("Compiling graph with checkpointing...")
    compiled_graph = workflow.compile(checkpointer=memory)
    
    logger.info("Interview graph created successfully")
    return compiled_graph


# Create singleton instance
interview_graph = create_interview_graph()


def get_interview_graph():
    """Get the compiled interview graph instance"""
    return interview_graph
