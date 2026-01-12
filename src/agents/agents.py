"""
CrewAI Agents for the AI Mock Interview Agent.

This module defines the agents responsible for:
1. Analyzing job descriptions
2. Researching company culture
3. Creating interview strategies
"""

from crewai import Agent
from ..config import Settings
from ..tools.scraper import WebsiteScraper


class InterviewAgents:
    """
    Factory class for creating interview preparation agents.
    
    Agents are configured based on interview tone and level.
    """
    
    def __init__(self, tone: str = "friendly", level: str = "mid"):
        """
        Initialize the InterviewAgents factory.
        
        Args:
            tone: Interview tone - "friendly" or "strict"
            level: Experience level - "junior", "mid", or "senior"
        """
        self.tone = tone.lower()
        self.level = level.lower()
        
        # Load configuration
        settings = Settings()
        
        # Initialize LLM using CrewAI's string format for Ollama
        # CrewAI will automatically handle Ollama connections
        # Format: "ollama/<model_name>"
        self.llm = f"ollama/{settings.llm_model}"
        
        # Store base URL for potential custom configuration
        self.ollama_base_url = settings.ollama_base_url
        
        # Initialize tools
        self.scraper = WebsiteScraper()
    
    def jd_analyst(self) -> Agent:
        """
        Create the Job Description Analyst agent.
        
        This agent extracts core technical skills, required experience,
        and identifies gaps between the user's CV and the job description.
        
        Returns:
            Agent: The JD Analyst agent
        """
        return Agent(
            role="Senior Technical Recruiter",
            goal=(
                "Analyze job descriptions and CVs to provide a COMPLETE, DETAILED analysis. "
                "You MUST provide the full analysis in your Final Answer, not just say you can give an answer."
            ),
            backstory=(
                "You are an expert at analyzing technical job descriptions. "
                "You can spot the difference between 'must-have' and 'nice-to-have' skills. "
                "You are analytical and precise, with years of experience in technical recruitment. "
                "You understand the nuances of different tech stacks and can accurately assess "
                "skill requirements across various seniority levels.\n\n"
                "IMPORTANT: You ALWAYS provide complete, detailed analysis in your Final Answer. "
                "You NEVER just say 'I can give a great answer' - you actually GIVE the answer with all details."
            ),
            llm=self.llm,
            verbose=True,
            allow_delegation=False
        )
    
    def corporate_researcher(self) -> Agent:
        """
        Create the Corporate Researcher agent.
        
        This agent scrapes company websites to extract mission, values,
        and recent project details to ensure culture fit.
        
        Returns:
            Agent: The Corporate Researcher agent
        """
        return Agent(
            role="Company Culture Investigator",
            goal="Scrape the company website to extract mission, values, and recent project details to ensure culture fit.",
            backstory=(
                "You are a detective for corporate identity. "
                "You find the hidden details in 'About Us' pages that define a company's DNA. "
                "You excel at reading between the lines to understand what a company truly values. "
                "Your insights help candidates prepare for culture-fit questions and understand "
                "the organizational environment they're stepping into."
            ),
            llm=self.llm,
            tools=[self.scraper],
            verbose=True,
            allow_delegation=False
        )
    
    def lead_interviewer(self) -> Agent:
        """
        Create the Lead Interviewer (Strategist) agent.
        
        This agent synthesizes all data to generate a comprehensive
        Interview Dossier containing tailored questions.
        
        The backstory adapts based on the interview tone setting.
        
        Returns:
            Agent: The Lead Interviewer agent
        """
        # Dynamic backstory based on tone
        if self.tone == "strict":
            backstory = (
                "You are a no-nonsense Lead Interview Manager with high standards. "
                "You believe in rigorous preparation and expect candidates to demonstrate "
                "deep technical knowledge and clear problem-solving abilities. "
                "For culture fit questions, you MUST use the STAR method framework "
                "(Situation, Task, Action, Result) to structure behavioral questions. "
                "You push candidates to be specific and results-oriented. "
                "Your questions are challenging but fair, designed to reveal true competency."
            )
        else:  # friendly
            backstory = (
                "You are a supportive and encouraging Lead Interview Manager. "
                "You believe in helping candidates showcase their best selves through "
                "thoughtful preparation and confidence-building. "
                "For culture fit questions, you MUST use the STAR method framework "
                "(Situation, Task, Action, Result) to help candidates structure compelling stories. "
                "You create a warm environment while still ensuring thorough preparation. "
                "Your questions are designed to help candidates shine while being authentic."
            )
        
        return Agent(
            role="Lead Interview Manager",
            goal="Synthesize all data to generate a comprehensive Interview Dossier containing tailored questions.",
            backstory=backstory,
            llm=self.llm,
            verbose=True,
            allow_delegation=True  # Can delegate to other agents for additional info
        )
    
    def get_all_agents(self) -> dict:
        """
        Get all agents as a dictionary.
        
        Returns:
            dict: Dictionary containing all agents
        """
        return {
            "jd_analyst": self.jd_analyst(),
            "corporate_researcher": self.corporate_researcher(),
            "lead_interviewer": self.lead_interviewer()
        }
