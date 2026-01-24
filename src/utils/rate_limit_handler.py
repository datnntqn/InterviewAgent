"""
Rate Limit Handler for Groq API with retry logic and API key rotation.

This module provides utilities to handle rate limits gracefully:
1. Exponential backoff retry
2. Multiple API key rotation
3. Alternative model fallback
"""

import time
import os
from typing import Optional, List, Callable, Any
from functools import wraps
import random


class RateLimitHandler:
    """
    Handles rate limiting for Groq API calls with multiple strategies.
    """
    
    def __init__(
        self,
        api_keys: Optional[List[str]] = None,
        max_retries: int = 3,
        base_delay: float = 16.0,
        max_delay: float = 60.0
    ):
        """
        Initialize the rate limit handler.
        
        Args:
            api_keys: List of Groq API keys to rotate through
            max_retries: Maximum number of retry attempts
            base_delay: Base delay in seconds for exponential backoff
            max_delay: Maximum delay in seconds
        """
        # Load API keys from environment or use provided list
        if api_keys is None:
            primary_key = os.getenv("GROQ_API_KEY", "")
            secondary_keys = os.getenv("GROQ_API_KEYS_BACKUP", "").split(",")
            self.api_keys = [k.strip() for k in [primary_key] + secondary_keys if k.strip()]
        else:
            self.api_keys = api_keys
        
        self.current_key_index = 0
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        
        if not self.api_keys:
            raise ValueError(
                "No API keys provided. Set GROQ_API_KEY or GROQ_API_KEYS_BACKUP "
                "in your .env file, or pass api_keys parameter."
            )
    
    def get_next_api_key(self) -> str:
        """
        Rotate to the next API key.
        
        Returns:
            str: Next API key in rotation
        """
        if len(self.api_keys) == 1:
            return self.api_keys[0]
        
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return self.api_keys[self.current_key_index]
    
    def calculate_delay(self, attempt: int, suggested_delay: Optional[float] = None) -> float:
        """
        Calculate delay with exponential backoff.
        
        Args:
            attempt: Current retry attempt number (0-indexed)
            suggested_delay: Delay suggested by API error message
            
        Returns:
            float: Delay in seconds
        """
        if suggested_delay:
            # Use API's suggested delay if available
            return min(suggested_delay, self.max_delay)
        
        # Exponential backoff with jitter
        delay = min(self.base_delay * (2 ** attempt), self.max_delay)
        jitter = random.uniform(0, 0.1 * delay)  # Add 0-10% jitter
        return delay + jitter
    
    def parse_rate_limit_error(self, error_message: str) -> Optional[float]:
        """
        Parse rate limit error message to extract suggested wait time.
        
        Args:
            error_message: Error message from API
            
        Returns:
            Optional[float]: Suggested delay in seconds, or None
        """
        # Example: "Please try again in 16.05s"
        import re
        match = re.search(r'try again in ([\d.]+)s', error_message)
        if match:
            return float(match.group(1))
        return None


def with_rate_limit_retry(
    handler: Optional[RateLimitHandler] = None,
    rotate_keys: bool = True
):
    """
    Decorator to add rate limit retry logic to functions.
    
    Args:
        handler: RateLimitHandler instance (creates default if None)
        rotate_keys: Whether to rotate API keys on rate limit
        
    Example:
        @with_rate_limit_retry()
        def call_groq_api():
            # Your API call here
            pass
    """
    if handler is None:
        handler = RateLimitHandler()
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            
            for attempt in range(handler.max_retries):
                try:
                    # Try the function
                    return func(*args, **kwargs)
                    
                except Exception as e:
                    error_str = str(e)
                    
                    # Check if it's a rate limit error
                    if "rate_limit_exceeded" in error_str.lower() or "ratelimiterror" in error_str.lower():
                        last_exception = e
                        
                        # Parse suggested delay from error
                        suggested_delay = handler.parse_rate_limit_error(error_str)
                        delay = handler.calculate_delay(attempt, suggested_delay)
                        
                        print(f"\n⚠️  Rate limit hit (attempt {attempt + 1}/{handler.max_retries})")
                        print(f"⏳ Waiting {delay:.1f}s before retry...")
                        
                        # Rotate API key if enabled and we have multiple keys
                        if rotate_keys and len(handler.api_keys) > 1:
                            new_key = handler.get_next_api_key()
                            os.environ["GROQ_API_KEY"] = new_key
                            print(f"🔄 Switched to backup API key #{handler.current_key_index + 1}")
                        
                        time.sleep(delay)
                    else:
                        # Not a rate limit error, re-raise immediately
                        raise
            
            # All retries exhausted
            print(f"\n❌ Rate limit retries exhausted after {handler.max_retries} attempts")
            raise last_exception
        
        return wrapper
    return decorator


# Alternative free models with better rate limits
ALTERNATIVE_MODELS = {
    "groq": {
        # Groq models (current)
        "llama-3.3-70b-versatile": {"tpm": 12000, "rpm": 30},
        "llama-3.1-70b-versatile": {"tpm": 12000, "rpm": 30},
        "llama-3.1-8b-instant": {"tpm": 20000, "rpm": 30},  # Faster, higher limit
        "mixtral-8x7b-32768": {"tpm": 15000, "rpm": 30},
    },
    "google": {
        # Google AI Studio (Free tier)
        "gemini-1.5-flash": {"tpm": 250000, "rpm": 5},  # Very high TPM!
        "gemma-3-27b-it": {"tpm": 15000, "rpm": 30},
    },
    "deepseek": {
        # DeepSeek (via OpenRouter free tier)
        "deepseek-v3": {"tpm": 50000, "rpm": 20},
    },
    "qwen": {
        # Qwen (via various providers)
        "qwen-3-8b": {"tpm": 30000, "rpm": 30},
    }
}


def get_recommended_model(current_model: str = "llama-3.3-70b-versatile") -> dict:
    """
    Get recommended alternative models with better rate limits.
    
    Args:
        current_model: Current model being used
        
    Returns:
        dict: Recommended models with their limits
    """
    recommendations = {
        "same_provider": {
            "model": "llama-3.1-8b-instant",
            "reason": "Smaller Groq model with 67% higher TPM limit (20k vs 12k)",
            "limits": ALTERNATIVE_MODELS["groq"]["llama-3.1-8b-instant"]
        },
        "best_free": {
            "model": "gemini-1.5-flash",
            "provider": "Google AI Studio",
            "reason": "Highest free TPM limit (250k), excellent quality",
            "limits": ALTERNATIVE_MODELS["google"]["gemini-1.5-flash"]
        },
        "balanced": {
            "model": "deepseek-v3",
            "provider": "OpenRouter",
            "reason": "Great balance of quality and rate limits (50k TPM)",
            "limits": ALTERNATIVE_MODELS["deepseek"]["deepseek-v3"]
        }
    }
    
    return recommendations
