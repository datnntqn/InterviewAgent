"""
CrewAI Tasks for the AI Mock Interview Agent.

This module defines the tasks that agents will execute:
1. Analyze job description
2. Research company culture
3. Prepare interview dossier

All tasks are configured to return strict JSON output.
Task configurations are loaded from YAML files for better maintainability.
"""

from crewai import Task
from typing import List
from ..prompt_loader import get_prompt_loader
from ..models import JobAnalysisOutput, CompanyCultureOutput, InterviewDossierOutput


class InterviewTasks:
    """
    Factory class for creating interview preparation tasks.
    
    All tasks are configured to return structured JSON output.
    Configurations are loaded from YAML files in ai/prompts/tasks/
    """
    
    def __init__(self):
        """Initialize the InterviewTasks factory."""
        self.prompt_loader = get_prompt_loader()
    
    def analyze_job_description(
        self,
        agent,
        job_description: str,
        user_cv: str
    ) -> Task:
        """
        Create a task to analyze the job description with JSON output.
        
        Configuration is loaded from ai/prompts/tasks/analyze_job_description.yaml
        
        Args:
            agent: The JD Analyst agent
            job_description: The job description text
            user_cv: The user's CV/resume text
            
        Returns:
            Task: The job description analysis task
        """
        # Load configuration from YAML
        config = self.prompt_loader.load_task_config('analyze_job_description')
        
        # Format description with variables
        description = self.prompt_loader.format_task_description(
            'analyze_job_description',
            job_description=job_description,
            user_cv=user_cv
        )
        
        return Task(
            description=description,
            expected_output=config['expected_output'],
            agent=agent,
            output_pydantic=JobAnalysisOutput  # Use Pydantic model for structured output
        )
    
    def research_company_culture(
        self,
        agent,
        company_name: str,
        company_website: str
    ) -> Task:
        """
        Create a task to research company culture with JSON output.
        
        Configuration is loaded from ai/prompts/tasks/research_company_culture.yaml
        
        Args:
            agent: The Corporate Researcher agent
            company_name: Name of the company
            company_website: URL of the company website
            
        Returns:
            Task: The company culture research task
        """
        # Load configuration from YAML
        config = self.prompt_loader.load_task_config('research_company_culture')
        
        # Format description with variables
        description = self.prompt_loader.format_task_description(
            'research_company_culture',
            company_name=company_name,
            company_website=company_website
        )
        
        return Task(
            description=description,
            expected_output=config['expected_output'],
            agent=agent,
            output_pydantic=CompanyCultureOutput  # Use Pydantic model for structured output
        )
    
    def prepare_interview_dossier(
        self,
        agent,
        job_analysis: str,
        company_culture: str,
        interview_type: str = "technical"
    ) -> Task:
        """
        Create a task to prepare the interview dossier with JSON output.
        
        Configuration is loaded from ai/prompts/tasks/prepare_interview_dossier.yaml
        
        Args:
            agent: The Lead Interviewer agent
            job_analysis: Results from job description analysis
            company_culture: Results from company culture research
            interview_type: Type of interview (technical, behavioral, mixed)
            
        Returns:
            Task: The interview preparation task
        """
        # Load configuration from YAML
        config = self.prompt_loader.load_task_config('prepare_interview_dossier')
        
        # Format description with variables
        description = self.prompt_loader.format_task_description(
            'prepare_interview_dossier',
            job_analysis=job_analysis,
            company_culture=company_culture,
            interview_type=interview_type
        )
        
        return Task(
            description=description,
            expected_output=config['expected_output'],
            agent=agent,
            output_pydantic=InterviewDossierOutput  # Use Pydantic model for structured output
        )
    
    def get_all_tasks(
        self,
        agents: dict,
        job_description: str,
        user_cv: str,
        company_name: str,
        company_website: str,
        interview_type: str = "mixed"
    ) -> List[Task]:
        """
        Get all tasks in the correct execution order.
        
        Args:
            agents: Dictionary of agents (from InterviewAgents.get_all_agents())
            job_description: The job description text
            user_cv: The user's CV text
            company_name: Name of the company
            company_website: Company website URL
            interview_type: Type of interview
            
        Returns:
            List[Task]: List of tasks in execution order
        """
        # Task 1: Analyze job description
        job_task = self.analyze_job_description(
            agent=agents["jd_analyst"],
            job_description=job_description,
            user_cv=user_cv
        )
        
        # Task 2: Research company culture
        culture_task = self.research_company_culture(
            agent=agents["corporate_researcher"],
            company_name=company_name,
            company_website=company_website
        )
        
        # Task 3: Prepare interview dossier (depends on tasks 1 & 2)
        dossier_task = self.prepare_interview_dossier(
            agent=agents["lead_interviewer"],
            job_analysis="Results from job analysis task",
            company_culture="Results from company culture task",
            interview_type=interview_type
        )
        
        # Set context for the final task
        dossier_task.context = [job_task, culture_task]
        
        return [job_task, culture_task, dossier_task]
