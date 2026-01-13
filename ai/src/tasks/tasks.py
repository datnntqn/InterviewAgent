"""
CrewAI Tasks for the AI Mock Interview Agent.

This module defines the tasks that agents will execute:
1. Analyze job description
2. Research company culture
3. Prepare interview dossier
"""

from crewai import Task
from typing import List
from ..models.schemas import JobDescriptionAnalysis, CompanyCultureProfile, InterviewDossier


class InterviewTasks:
    """
    Factory class for creating interview preparation tasks.
    
    Tasks define what agents should do and what output is expected.
    """
    
    def __init__(self):
        """Initialize the InterviewTasks factory."""
        pass
    
    def analyze_job_description(
        self,
        agent,
        job_description: str,
        user_cv: str
    ) -> Task:
        """
        Create a task to analyze the job description.
        
        This task extracts technical skills, experience requirements,
        and identifies gaps between the user's CV and job requirements.
        
        Args:
            agent: The JD Analyst agent
            job_description: The job description text
            user_cv: The user's CV/resume text
            
        Returns:
            Task: The job description analysis task
        """
        return Task(
            description=(
                f"Analyze the following job description and compare it with the candidate's CV.\n\n"
                f"**Job Description:**\n{job_description}\n\n"
                f"**Candidate CV:**\n{user_cv}\n\n"
                f"CRITICAL INSTRUCTIONS:\n"
                f"- You MUST provide a COMPLETE analysis in your Final Answer\n"
                f"- DO NOT just say 'I can give a great answer' or 'Thought: ...'\n"
                f"- PROVIDE the actual detailed analysis with all sections filled out\n"
                f"- Your Final Answer should be the complete analysis, not a meta-statement\n\n"
                f"Your analysis MUST include:\n"
                f"1. Extract all technical skills mentioned (programming languages, frameworks, tools)\n"
                f"2. Identify soft skills and behavioral requirements\n"
                f"3. Determine the required years of experience\n"
                f"4. Distinguish between 'must-have' and 'nice-to-have' qualifications\n"
                f"5. Identify skill gaps between the CV and job requirements\n"
                f"6. Highlight the candidate's strengths that match the job\n\n"
                f"Be thorough and analytical. Focus on actionable insights.\n\n"
                f"FORMAT YOUR FINAL ANSWER EXACTLY LIKE THIS:\n\n"
                f"TECHNICAL SKILLS REQUIRED:\n"
                f"- [list each skill]\n\n"
                f"SOFT SKILLS:\n"
                f"- [list each skill]\n\n"
                f"EXPERIENCE REQUIRED: [X years]\n\n"
                f"SKILL GAPS:\n"
                f"- [list gaps]\n\n"
                f"CANDIDATE STRENGTHS:\n"
                f"- [list strengths]\n\n"
                f"RECOMMENDATIONS:\n"
                f"- [list recommendations]"
            ),
            expected_output=(
                "A COMPLETE detailed analysis with ALL sections filled out:\n"
                "- Complete list of technical skills required\n"
                "- Complete list of soft skills and keywords\n"
                "- Required years of experience\n"
                "- Detailed skill gaps and strengths\n"
                "- Specific recommendations for interview preparation\n\n"
                "NOTE: The output should be the ACTUAL ANALYSIS, not a statement about being able to provide it."
            ),
            agent=agent
        )
    
    def research_company_culture(
        self,
        agent,
        company_name: str,
        company_website: str
    ) -> Task:
        """
        Create a task to research company culture.
        
        This task scrapes the company website to extract mission,
        values, and cultural information.
        
        Args:
            agent: The Corporate Researcher agent
            company_name: Name of the company
            company_website: URL of the company website
            
        Returns:
            Task: The company culture research task
        """
        return Task(
            description=(
                f"Research the company culture for: {company_name}\n\n"
                f"**Company Website:** {company_website}\n\n"
                f"Your research should include:\n"
                f"1. Use the Website Scraper tool to extract content from the company website\n"
                f"2. Focus on 'About Us', 'Our Values', 'Mission', and 'Culture' pages\n"
                f"3. Identify the company's core values and mission statement\n"
                f"4. Look for information about recent projects, initiatives, or achievements\n"
                f"5. Understand the company's work culture and environment\n"
                f"6. Note any unique aspects of their organizational culture\n\n"
                f"Provide insights that will help the candidate understand what the company values "
                f"and how to demonstrate culture fit during the interview.\n\n"
                f"Format your response as:\n"
                f"COMPANY MISSION:\n[mission statement]\n\n"
                f"CORE VALUES:\n- [list]\n\n"
                f"WORK CULTURE:\n[description]\n\n"
                f"RECENT INITIATIVES:\n- [list]\n\n"
                f"CULTURE FIT TIPS:\n- [list]"
            ),
            expected_output=(
                "A comprehensive company culture profile containing:\n"
                "- Company mission statement\n"
                "- List of core values\n"
                "- Recent projects or initiatives\n"
                "- Work culture insights\n"
                "- Tips for demonstrating culture fit"
            ),
            agent=agent
        )
    
    def prepare_interview_dossier(
        self,
        agent,
        job_analysis: str,
        company_culture: str,
        interview_type: str = "technical"
    ) -> Task:
        """
        Create a task to prepare the interview dossier.
        
        This task synthesizes all information to create tailored
        interview questions and preparation strategies.
        
        Args:
            agent: The Lead Interviewer agent
            job_analysis: Results from job description analysis
            company_culture: Results from company culture research
            interview_type: Type of interview (technical, behavioral, mixed)
            
        Returns:
            Task: The interview preparation task
        """
        return Task(
            description=(
                f"Create a comprehensive Interview Dossier based on the following information:\n\n"
                f"**Job Analysis:**\n{job_analysis}\n\n"
                f"**Company Culture:**\n{company_culture}\n\n"
                f"**Interview Type:** {interview_type}\n\n"
                f"Your dossier should include:\n\n"
                f"**1. Technical Questions (if applicable):**\n"
                f"   - Create 5-7 technical questions based on required skills\n"
                f"   - Include questions about specific technologies mentioned in the JD\n"
                f"   - Range from basic to advanced difficulty\n\n"
                f"**2. Behavioral Questions (STAR Method):**\n"
                f"   - Create 5-7 behavioral questions using the STAR framework\n"
                f"   - Each question should target: Situation, Task, Action, Result\n"
                f"   - Align questions with company values and culture\n"
                f"   - Focus on leadership, teamwork, problem-solving, and adaptability\n\n"
                f"**3. Company-Specific Questions:**\n"
                f"   - Create 3-5 questions that demonstrate knowledge of the company\n"
                f"   - Reference their mission, values, or recent projects\n\n"
                f"**4. Interview Strategy:**\n"
                f"   - Provide a preparation roadmap\n"
                f"   - Suggest key talking points\n"
                f"   - Recommend how to address skill gaps\n"
                f"   - Tips for demonstrating culture fit\n\n"
                f"Make the questions realistic and relevant. Ensure STAR method is clearly "
                f"explained for behavioral questions.\n\n"
                f"Format your response as:\n\n"
                f"TECHNICAL QUESTIONS:\n"
                f"1. [question]\n"
                f"2. [question]\n\n"
                f"BEHAVIORAL QUESTIONS (STAR METHOD):\n"
                f"1. [question]\n"
                f"   - Situation: [what to address]\n"
                f"   - Task: [what to address]\n"
                f"   - Action: [what to address]\n"
                f"   - Result: [what to address]\n\n"
                f"COMPANY-SPECIFIC QUESTIONS:\n"
                f"1. [question]\n\n"
                f"INTERVIEW STRATEGY:\n"
                f"- [strategy point]\n"
                f"- [strategy point]"
            ),
            expected_output=(
                "A complete Interview Dossier containing:\n"
                "- List of technical interview questions (if applicable)\n"
                "- List of behavioral questions with STAR framework guidance\n"
                "- Company-specific questions\n"
                "- Comprehensive interview preparation strategy\n"
                "- Key talking points and tips\n"
                "- Recommendations for addressing weaknesses"
            ),
            agent=agent
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
