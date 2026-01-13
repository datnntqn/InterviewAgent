"""
Prompt Loader Utility

This module loads agent and task configurations from YAML files,
making prompts more maintainable and easier to version control.
"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any


class PromptLoader:
    """
    Utility class to load prompts from YAML configuration files.
    
    This allows for better separation of concerns:
    - Code logic stays in Python files
    - Prompts and configurations live in YAML files
    - Easy to version control and review prompt changes
    """
    
    def __init__(self, prompts_dir: str = None):
        """
        Initialize the PromptLoader.
        
        Args:
            prompts_dir: Path to the prompts directory. If None, uses default location.
        """
        if prompts_dir is None:
            # Default to ai/prompts directory (one level up from src/)
            current_dir = Path(__file__).parent  # ai/src/
            self.prompts_dir = current_dir.parent / "prompts"  # ai/prompts/
        else:
            self.prompts_dir = Path(prompts_dir)
        
        self.agents_dir = self.prompts_dir / "agents"
        self.tasks_dir = self.prompts_dir / "tasks"
    
    def load_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Load agent configuration from YAML file.
        
        Args:
            agent_name: Name of the agent (e.g., 'jd_analyst')
            
        Returns:
            Dict containing agent configuration
            
        Example:
            >>> loader = PromptLoader()
            >>> config = loader.load_agent_config('jd_analyst')
            >>> print(config['role'])
            'Senior Technical Recruiter'
        """
        config_path = self.agents_dir / f"{agent_name}.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Agent config not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def load_task_config(self, task_name: str) -> Dict[str, Any]:
        """
        Load task configuration from YAML file.
        
        Args:
            task_name: Name of the task (e.g., 'analyze_job_description')
            
        Returns:
            Dict containing task configuration
            
        Example:
            >>> loader = PromptLoader()
            >>> config = loader.load_task_config('analyze_job_description')
            >>> print(config['name'])
            'analyze_job_description'
        """
        config_path = self.tasks_dir / f"{task_name}.yaml"
        
        if not config_path.exists():
            raise FileNotFoundError(f"Task config not found: {config_path}")
        
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        return config
    
    def format_task_description(
        self,
        task_name: str,
        **kwargs
    ) -> str:
        """
        Load and format task description with provided variables.
        
        Args:
            task_name: Name of the task
            **kwargs: Variables to format into the description template
            
        Returns:
            Formatted description string
            
        Example:
            >>> loader = PromptLoader()
            >>> desc = loader.format_task_description(
            ...     'analyze_job_description',
            ...     job_description="Python Developer needed",
            ...     user_cv="5 years Python experience"
            ... )
        """
        config = self.load_task_config(task_name)
        template = config.get('description_template', '')
        
        return template.format(**kwargs)
    
    def get_agent_backstory(
        self,
        agent_name: str,
        tone: str = None
    ) -> str:
        """
        Get agent backstory, optionally selecting by tone.
        
        Args:
            agent_name: Name of the agent
            tone: Optional tone selection (e.g., 'friendly', 'strict')
            
        Returns:
            Backstory string
            
        Example:
            >>> loader = PromptLoader()
            >>> backstory = loader.get_agent_backstory('lead_interviewer', tone='friendly')
        """
        config = self.load_agent_config(agent_name)
        
        # Check if backstory has multiple options based on tone
        backstory = config.get('backstory')
        if isinstance(backstory, dict) and tone:
            return backstory.get(tone, backstory.get('default', ''))
        elif isinstance(backstory, dict):
            # If backstories is a dict, check for 'backstories' key
            backstories = config.get('backstories', {})
            if tone and tone in backstories:
                return backstories[tone]
            return backstories.get('default', list(backstories.values())[0] if backstories else '')
        
        return backstory or ''
    
    def list_agents(self) -> list:
        """
        List all available agent configurations.
        
        Returns:
            List of agent names
        """
        if not self.agents_dir.exists():
            return []
        
        return [
            f.stem for f in self.agents_dir.glob("*.yaml")
        ]
    
    def list_tasks(self) -> list:
        """
        List all available task configurations.
        
        Returns:
            List of task names
        """
        if not self.tasks_dir.exists():
            return []
        
        return [
            f.stem for f in self.tasks_dir.glob("*.yaml")
        ]


# Global instance for easy access
_loader = None

def get_prompt_loader() -> PromptLoader:
    """
    Get the global PromptLoader instance.
    
    Returns:
        PromptLoader instance
    """
    global _loader
    if _loader is None:
        _loader = PromptLoader()
    return _loader
