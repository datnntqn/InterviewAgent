"""
CrewAI Agents for the AI Mock Interview Agent.

This module defines the agents responsible for:
1. Analyzing job descriptions
2. Researching company culture
3. Creating interview strategies

Agents are now configured using YAML files for better maintainability.
"""

from crewai import Agent
from ..config import get_llm
from ..tools.scraper import WebsiteScraper
from ..prompt_loader import get_prompt_loader


class InterviewAgents:
    """
    Factory class for creating interview preparation agents.
    
    Agents are configured based on interview tone and level.
    Configurations are loaded from YAML files in ai/prompts/agents/
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
        
        # Initialize LLM using Groq Cloud API
        self.llm = get_llm(temperature=0.7)
        
        # Initialize tools
        self.scraper = WebsiteScraper()
        
        # Initialize prompt loader
        self.prompt_loader = get_prompt_loader()
    
    def jd_analyst(self) -> Agent:
        """
        Create the Job Description Analyst agent.
        
        Configuration is loaded from ai/prompts/agents/jd_analyst.yaml
        
        Returns:
            Agent: The JD Analyst agent
        """
        # Load configuration from YAML
        config = self.prompt_loader.load_agent_config('jd_analyst')
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            llm=self.llm,
            verbose=config['settings']['verbose'],
            allow_delegation=config['settings']['allow_delegation']
        )
    
    def corporate_researcher(self) -> Agent:
        """
        Create the Corporate Researcher agent.
        
        Configuration is loaded from ai/prompts/agents/corporate_researcher.yaml
        
        Returns:
            Agent: The Corporate Researcher agent
        """
        # Load configuration from YAML
        config = self.prompt_loader.load_agent_config('corporate_researcher')
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=config['backstory'],
            llm=self.llm,
            tools=[self.scraper],
            verbose=config['settings']['verbose'],
            allow_delegation=config['settings']['allow_delegation']
        )
    
    def lead_interviewer(self) -> Agent:
        """
        Create the Lead Interviewer (Strategist) agent.
        
        Configuration is loaded from ai/prompts/agents/lead_interviewer.yaml
        The backstory adapts based on the interview tone setting.
        
        Returns:
            Agent: The Lead Interviewer agent
        """
        # Load configuration from YAML
        config = self.prompt_loader.load_agent_config('lead_interviewer')
        
        # Get tone-specific backstory
        backstory = self.prompt_loader.get_agent_backstory('lead_interviewer', tone=self.tone)
        
        return Agent(
            role=config['role'],
            goal=config['goal'],
            backstory=backstory,
            llm=self.llm,
            verbose=config['settings']['verbose'],
            allow_delegation=config['settings']['allow_delegation']
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
