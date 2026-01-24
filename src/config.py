import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Centralized configuration for LLM APIs.
    
    Supports:
    - Groq Cloud API (llama models)
    - Google Gemini API (gemini models)
    
    IMPORTANT: Update your .env file with appropriate API keys:
    - GROQ_API_KEY: For Groq models
    - GOOGLE_API_KEY: For Gemini models
    - GROQ_MODEL_NAME: Model identifier (e.g., "llama-3.1-8b-instant" or "gemini-1.5-flash")
    """

    groq_api_key: str = Field(
        default_factory=lambda: os.getenv("GROQ_API_KEY", "")
    )
    groq_model_name: str = Field(
        default_factory=lambda: os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    )
    google_api_key: str = Field(
        default_factory=lambda: os.getenv("GOOGLE_API_KEY", "")
    )

    class Config:
        env_file = ".env"
        extra = "ignore"


def get_llm(temperature: float = 0.7) -> str:
    """
    Factory function to create and configure the LLM for CrewAI.
    
    Automatically detects provider based on model name:
    - Models containing "gemini" → Google Gemini API
    - Other models → Groq API
    
    Args:
        temperature: Controls randomness in responses (0.0 = deterministic, 1.0 = creative)
        
    Returns:
        str: CrewAI-compatible LLM string in format "provider/model_name"
        
    Raises:
        ValueError: If required API key is not set
        
    Example:
        >>> # For Groq
        >>> llm = get_llm(temperature=0.7)
        >>> # Returns: "groq/llama-3.1-8b-instant"
        
        >>> # For Gemini
        >>> llm = get_llm(temperature=0.7)
        >>> # Returns: "gemini/gemini-1.5-flash"
    """
    settings = Settings()
    
    # Detect provider based on model name
    if "gemini" in settings.groq_model_name.lower():
        # Google Gemini provider
        if not settings.google_api_key or settings.google_api_key == "your_google_api_key_here":
            raise ValueError(
                "GOOGLE_API_KEY is not set or is using the placeholder value. "
                "Please set your Google API key in the .env file. "
                "Get your API key from: https://aistudio.google.com/apikey"
            )
        
        # Set environment variable for LiteLLM/CrewAI to use
        os.environ["GOOGLE_API_KEY"] = settings.google_api_key
        
        print(f"🤖 Using Google Gemini: {settings.groq_model_name}")
        return f"gemini/{settings.groq_model_name}"
    
    else:
        # Groq provider (default)
        if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
            raise ValueError(
                "GROQ_API_KEY is not set or is using the placeholder value. "
                "Please set your Groq API key in the .env file. "
                "Get your API key from: https://console.groq.com/keys"
            )
        
        # Set environment variable for CrewAI to use
        os.environ["GROQ_API_KEY"] = settings.groq_api_key
        
        print(f"🤖 Using Groq: {settings.groq_model_name}")
        return f"groq/{settings.groq_model_name}"

