"""
Wrapper for CrewAI with rate limit handling.

This module wraps CrewAI crew execution with automatic rate limit retry.
"""

from typing import Dict, Optional
from ..crews.interview_crew import InterviewPreparationCrew
from .rate_limit_handler import RateLimitHandler, with_rate_limit_retry
import os


class RateLimitAwareCrewAI:
    """
    Wrapper around InterviewPreparationCrew with rate limit handling.
    """
    
    def __init__(
        self,
        tone: str = "friendly",
        level: str = "mid",
        verbose: bool = True,
        api_keys: Optional[list] = None,
        max_retries: int = 3
    ):
        """
        Initialize rate-limit aware CrewAI wrapper.
        
        Args:
            tone: Interview tone
            level: Experience level
            verbose: Verbose logging
            api_keys: List of Groq API keys for rotation
            max_retries: Maximum retry attempts on rate limit
        """
        self.tone = tone
        self.level = level
        self.verbose = verbose
        
        # Initialize rate limit handler
        self.rate_handler = RateLimitHandler(
            api_keys=api_keys,
            max_retries=max_retries,
            base_delay=16.0  # Based on Groq's suggested delay
        )
        
        print(f"🔑 Loaded {len(self.rate_handler.api_keys)} API key(s)")
        if len(self.rate_handler.api_keys) > 1:
            print(f"🔄 API key rotation enabled")
    
    @with_rate_limit_retry(rotate_keys=True)
    def prepare_interview(
        self,
        job_description: str,
        user_cv: str,
        company_name: str,
        company_website: str,
        interview_type: str = "mixed"
    ) -> Dict:
        """
        Execute interview preparation with rate limit handling.
        
        This method automatically retries on rate limit errors and rotates
        API keys if multiple keys are available.
        
        Args:
            job_description: Job description text
            user_cv: Candidate's CV
            company_name: Company name
            company_website: Company website URL
            interview_type: Interview type
            
        Returns:
            Dict: Interview preparation results
        """
        # Create crew instance
        crew = InterviewPreparationCrew(
            tone=self.tone,
            level=self.level,
            verbose=self.verbose
        )
        
        # Execute with current API key
        return crew.prepare_interview(
            job_description=job_description,
            user_cv=user_cv,
            company_name=company_name,
            company_website=company_website,
            interview_type=interview_type
        )


def prepare_interview_with_retry(
    job_description: str,
    user_cv: str,
    company_name: str,
    company_website: str,
    tone: str = "friendly",
    level: str = "mid",
    interview_type: str = "mixed",
    verbose: bool = True,
    api_keys: Optional[list] = None
) -> Dict:
    """
    Convenience function to prepare interview with automatic rate limit handling.
    
    This function wraps the CrewAI execution with retry logic and API key rotation.
    
    Args:
        job_description: Job description text
        user_cv: Candidate's CV
        company_name: Company name
        company_website: Company website URL
        tone: Interview tone
        level: Experience level
        interview_type: Interview type
        verbose: Verbose logging
        api_keys: Optional list of API keys for rotation
        
    Returns:
        Dict: Interview preparation results
        
    Example:
        >>> # Single API key (from .env)
        >>> result = prepare_interview_with_retry(
        ...     job_description="...",
        ...     user_cv="...",
        ...     company_name="TechCorp",
        ...     company_website="https://techcorp.com"
        ... )
        
        >>> # Multiple API keys for rotation
        >>> result = prepare_interview_with_retry(
        ...     job_description="...",
        ...     user_cv="...",
        ...     company_name="TechCorp",
        ...     company_website="https://techcorp.com",
        ...     api_keys=["key1", "key2", "key3"]
        ... )
    """
    crew_wrapper = RateLimitAwareCrewAI(
        tone=tone,
        level=level,
        verbose=verbose,
        api_keys=api_keys
    )
    
    return crew_wrapper.prepare_interview(
        job_description=job_description,
        user_cv=user_cv,
        company_name=company_name,
        company_website=company_website,
        interview_type=interview_type
    )
