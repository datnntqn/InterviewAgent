"""
CrewAI Crew for the AI Mock Interview Agent.

This module orchestrates agents and tasks to prepare comprehensive
interview materials for candidates.
"""

from crewai import Crew, Process
from typing import Dict, Optional
from ..agents.agents import InterviewAgents
from ..tasks.tasks import InterviewTasks


class InterviewPreparationCrew:
    """
    Main crew for orchestrating the interview preparation workflow.
    
    This crew coordinates three agents to:
    1. Analyze job descriptions
    2. Research company culture
    3. Generate interview questions and strategies
    """
    
    def __init__(
        self,
        tone: str = "friendly",
        level: str = "mid",
        verbose: bool = True
    ):
        """
        Initialize the Interview Preparation Crew.
        
        Args:
            tone: Interview tone - "friendly" or "strict"
            level: Experience level - "junior", "mid", or "senior"
            verbose: Whether to print detailed execution logs
        """
        self.tone = tone
        self.level = level
        self.verbose = verbose
        
        # Initialize agents and tasks
        self.agents_factory = InterviewAgents(tone=tone, level=level)
        self.tasks_factory = InterviewTasks()
    
    def prepare_interview(
        self,
        job_description: str,
        user_cv: str,
        company_name: str,
        company_website: str,
        interview_type: str = "mixed"
    ) -> Dict:
        """
        Execute the full interview preparation workflow.
        
        This method orchestrates all agents and tasks to produce a
        comprehensive interview preparation package.
        
        Args:
            job_description: The job description text
            user_cv: The candidate's CV/resume text
            company_name: Name of the target company
            company_website: URL of the company website
            interview_type: Type of interview ("technical", "behavioral", "mixed")
            
        Returns:
            Dict: Results containing job analysis, company culture, and interview dossier
        """
        # Get all agents
        agents = self.agents_factory.get_all_agents()
        
        # Create all tasks
        tasks = self.tasks_factory.get_all_tasks(
            agents=agents,
            job_description=job_description,
            user_cv=user_cv,
            company_name=company_name,
            company_website=company_website,
            interview_type=interview_type
        )
        
        # Create the crew
        crew = Crew(
            agents=list(agents.values()),
            tasks=tasks,
            process=Process.sequential,  # Execute tasks in order
            verbose=self.verbose,
            memory=False  # Disabled to prevent rate limit from token duplication
        )
        
        # Execute the crew
        print("\n🚀 Starting Interview Preparation Crew...\n")
        print(f"📋 Job: {company_name}")
        print(f"🎯 Interview Type: {interview_type}")
        print(f"💼 Experience Level: {self.level}")
        print(f"😊 Tone: {self.tone}\n")
        
        result = crew.kickoff()
        
        print("\n✅ Interview Preparation Complete!\n")
        
        return result
    
    def quick_analysis(
        self,
        job_description: str,
        user_cv: str
    ) -> Dict:
        """
        Quick job description analysis without company research.
        
        Useful for rapid skill gap analysis.
        
        Args:
            job_description: The job description text
            user_cv: The candidate's CV text
            
        Returns:
            Dict: Job analysis results
        """
        agents = self.agents_factory.get_all_agents()
        
        # Only create the job analysis task
        job_task = self.tasks_factory.analyze_job_description(
            agent=agents["jd_analyst"],
            job_description=job_description,
            user_cv=user_cv
        )
        
        crew = Crew(
            agents=[agents["jd_analyst"]],
            tasks=[job_task],
            process=Process.sequential,
            verbose=self.verbose
        )
        
        print("\n🔍 Running Quick Job Analysis...\n")
        result = crew.kickoff()
        print("\n✅ Analysis Complete!\n")
        
        return result
    
    def research_company_only(
        self,
        company_name: str,
        company_website: str
    ) -> Dict:
        """
        Research company culture without job analysis.
        
        Useful for general company research.
        
        Args:
            company_name: Name of the company
            company_website: Company website URL
            
        Returns:
            Dict: Company culture research results
        """
        agents = self.agents_factory.get_all_agents()
        
        # Only create the company research task
        culture_task = self.tasks_factory.research_company_culture(
            agent=agents["corporate_researcher"],
            company_name=company_name,
            company_website=company_website
        )
        
        crew = Crew(
            agents=[agents["corporate_researcher"]],
            tasks=[culture_task],
            process=Process.sequential,
            verbose=self.verbose
        )
        
        print(f"\n🏢 Researching {company_name}...\n")
        result = crew.kickoff()
        print("\n✅ Research Complete!\n")
        
        return result


# Convenience function for quick usage
def prepare_for_interview(
    job_description: str,
    user_cv: str,
    company_name: str,
    company_website: str,
    tone: str = "friendly",
    level: str = "mid",
    interview_type: str = "mixed",
    verbose: bool = True
) -> Dict:
    """
    Convenience function to prepare for an interview.
    
    This is a simplified interface to the InterviewPreparationCrew.
    
    Args:
        job_description: The job description text
        user_cv: The candidate's CV text
        company_name: Name of the company
        company_website: Company website URL
        tone: Interview tone ("friendly" or "strict")
        level: Experience level ("junior", "mid", "senior")
        interview_type: Type of interview ("technical", "behavioral", "mixed")
        verbose: Whether to print detailed logs
        
    Returns:
        Dict: Complete interview preparation results
        
    Example:
        >>> result = prepare_for_interview(
        ...     job_description="Senior Python Developer...",
        ...     user_cv="Experienced developer with...",
        ...     company_name="TechCorp",
        ...     company_website="https://techcorp.com",
        ...     tone="friendly",
        ...     level="senior"
        ... )
    """
    crew = InterviewPreparationCrew(tone=tone, level=level, verbose=verbose)
    return crew.prepare_interview(
        job_description=job_description,
        user_cv=user_cv,
        company_name=company_name,
        company_website=company_website,
        interview_type=interview_type
    )
