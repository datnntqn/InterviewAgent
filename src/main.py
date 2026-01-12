"""
Main entry point for the AI Mock Interview Agent.

This module initializes the CrewAI system and orchestrates the interview preparation workflow.
"""

import logging
from .config import Settings
from .tools.scraper import WebsiteScraper

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """Main application entry point."""
    logger.info("Starting AI Mock Interview Agent...")
    
    # Load configuration
    settings = Settings()
    logger.info(f"Ollama URL: {settings.ollama_base_url}")
    logger.info(f"LLM Model: {settings.llm_model}")
    
    # Initialize scraper
    scraper = WebsiteScraper()
    logger.info("WebsiteScraper initialized")
    
    # TODO: Initialize CrewAI agents, tasks, and crews
    # This will be implemented in the next phase
    
    logger.info("AI Mock Interview Agent initialized successfully")
    logger.info("Ready to process interview preparation requests")


if __name__ == "__main__":
    main()
