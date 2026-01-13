"""
Main entry point for the AI Mock Interview Agent.

This module initializes the CrewAI system and orchestrates the interview preparation workflow.
"""

import logging
import sys
from .config import Settings
from .crews import InterviewPreparationCrew, prepare_for_interview

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_example():
    """Run an example interview preparation workflow."""
    logger.info("Running example interview preparation...")
    
    # Example data
    job_description = """
    Senior Python Developer
    
    We are looking for an experienced Python developer to join our team.
    
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
    - Contributions to open-source projects
    """
    
    user_cv = """
    John Doe - Software Engineer
    
    Experience:
    - 6 years of Python development
    - Proficient in Django and Flask
    - Worked with PostgreSQL, MySQL, and MongoDB
    - Experience with Docker
    - Built multiple RESTful APIs
    - Some experience with React
    
    Skills:
    Python, Django, Flask, PostgreSQL, Docker, Git, REST APIs, React
    """
    
    company_name = "TechCorp"
    company_website = "https://www.example.com"
    
    # Create and run the crew
    try:
        crew = InterviewPreparationCrew(
            tone="friendly",
            level="senior",
            verbose=True
        )
        
        result = crew.prepare_interview(
            job_description=job_description,
            user_cv=user_cv,
            company_name=company_name,
            company_website=company_website,
            interview_type="mixed"
        )
        
        logger.info("Interview preparation completed successfully!")
        logger.info(f"Result: {result}")
        
        return result
        
    except Exception as e:
        logger.error(f"Error during interview preparation: {e}", exc_info=True)
        return None


def run_interactive():
    """Run interactive mode where user provides inputs."""
    print("\n" + "="*60)
    print("🎯 AI Mock Interview Agent - Interactive Mode")
    print("="*60 + "\n")
    
    # Get user inputs
    print("Please provide the following information:\n")
    
    job_description = input("📋 Job Description (paste and press Enter twice when done):\n")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    job_description = "\n".join(lines) if lines else job_description
    
    print("\n")
    user_cv = input("📄 Your CV/Resume (paste and press Enter twice when done):\n")
    lines = []
    while True:
        line = input()
        if line == "":
            break
        lines.append(line)
    user_cv = "\n".join(lines) if lines else user_cv
    
    print("\n")
    company_name = input("🏢 Company Name: ")
    company_website = input("🌐 Company Website URL: ")
    
    print("\n")
    tone = input("😊 Interview Tone (friendly/strict) [friendly]: ").lower() or "friendly"
    level = input("💼 Experience Level (junior/mid/senior) [mid]: ").lower() or "mid"
    interview_type = input("🎯 Interview Type (technical/behavioral/mixed) [mixed]: ").lower() or "mixed"
    
    print("\n" + "="*60)
    print("🚀 Starting Interview Preparation...")
    print("="*60 + "\n")
    
    try:
        result = prepare_for_interview(
            job_description=job_description,
            user_cv=user_cv,
            company_name=company_name,
            company_website=company_website,
            tone=tone,
            level=level,
            interview_type=interview_type,
            verbose=True
        )
        
        print("\n" + "="*60)
        print("✅ Interview Preparation Complete!")
        print("="*60 + "\n")
        print(result)
        
        return result
        
    except Exception as e:
        logger.error(f"Error during interview preparation: {e}", exc_info=True)
        print(f"\n❌ Error: {e}")
        return None


def main():
    """Main application entry point."""
    logger.info("Starting AI Mock Interview Agent...")
    
    # Load configuration
    settings = Settings()
    logger.info(f"Groq Model: {settings.groq_model_name}")
    logger.info("Using Groq Cloud API for LLM inference")
    
    logger.info("AI Mock Interview Agent initialized successfully")
    logger.info("Ready to process interview preparation requests")
    
    # Check command line arguments
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "example":
            logger.info("Running in example mode...")
            run_example()
        elif mode == "interactive":
            logger.info("Running in interactive mode...")
            run_interactive()
        else:
            print(f"Unknown mode: {mode}")
            print("Usage: python -m src.main [example|interactive]")
            print("  example     - Run with example data")
            print("  interactive - Run in interactive mode")
            print("  (no args)   - Just initialize the system")
    else:
        print("\n" + "="*60)
        print("🎯 AI Mock Interview Agent")
        print("="*60)
        print("\nSystem initialized and ready!")
        print("\nUsage:")
        print("  python -m src.main example     - Run with example data")
        print("  python -m src.main interactive - Run in interactive mode")
        print("\nOr use the Python API:")
        print("  from src.crews import prepare_for_interview")
        print("  result = prepare_for_interview(...)")
        print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()

