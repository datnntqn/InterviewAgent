"""
Enhanced CrewAI Crew with rate limit protection via task delays.

This adds automatic delays between tasks to prevent rate limit errors.
"""

from crewai import Crew, Process
from typing import Dict
from ..agents.agents import InterviewAgents
from ..tasks.tasks import InterviewTasks
import time


class RateLimitSafeCrewAI:
    """
    Interview Preparation Crew with automatic rate limit protection.
    
    Adds delays between tasks to stay within Groq's 12k TPM limit.
    """
    
    def __init__(
        self,
        tone: str = "friendly",
        level: str = "mid",
        verbose: bool = True,
        delay_between_tasks: float = 20.0  # 20 seconds between tasks
    ):
        """
        Initialize the crew with rate limit protection.
        
        Args:
            tone: Interview tone
            level: Experience level
            verbose: Verbose logging
            delay_between_tasks: Seconds to wait between tasks (default: 20s)
        """
        self.tone = tone
        self.level = level
        self.verbose = verbose
        self.delay = delay_between_tasks
        
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
        Execute interview preparation with delays between tasks.
        
        This prevents rate limit errors by spacing out API calls.
        """
        print(f"\n🚀 Starting Interview Preparation (Rate-Limit Safe Mode)")
        print(f"⏱️  Delay between tasks: {self.delay}s\n")
        
        agents = self.agents_factory.get_all_agents()
        
        # Task 1: Job Analysis
        print("📋 Task 1/3: Analyzing Job Description...")
        job_task = self.tasks_factory.analyze_job_description(
            agent=agents["jd_analyst"],
            job_description=job_description,
            user_cv=user_cv
        )
        
        crew1 = Crew(
            agents=[agents["jd_analyst"]],
            tasks=[job_task],
            process=Process.sequential,
            verbose=self.verbose,
            memory=False
        )
        
        job_result = crew1.kickoff()
        print(f"✅ Task 1 complete. Waiting {self.delay}s before next task...\n")
        time.sleep(self.delay)
        
        # Task 2: Company Research
        print("🏢 Task 2/3: Researching Company Culture...")
        culture_task = self.tasks_factory.research_company_culture(
            agent=agents["corporate_researcher"],
            company_name=company_name,
            company_website=company_website
        )
        
        crew2 = Crew(
            agents=[agents["corporate_researcher"]],
            tasks=[culture_task],
            process=Process.sequential,
            verbose=self.verbose,
            memory=False
        )
        
        culture_result = crew2.kickoff()
        print(f"✅ Task 2 complete. Waiting {self.delay}s before next task...\n")
        time.sleep(self.delay)
        
        # Task 3: Interview Dossier
        print("💼 Task 3/3: Generating Interview Questions...")
        dossier_task = self.tasks_factory.prepare_interview_dossier(
            agent=agents["lead_interviewer"],
            job_analysis=str(job_result),
            company_culture=str(culture_result),
            interview_type=interview_type
        )
        
        crew3 = Crew(
            agents=[agents["lead_interviewer"]],
            tasks=[dossier_task],
            process=Process.sequential,
            verbose=self.verbose,
            memory=False
        )
        
        final_result = crew3.kickoff()
        print("✅ Task 3 complete!\n")
        
        return final_result
