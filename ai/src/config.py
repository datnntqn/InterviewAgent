import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Centralized configuration for Groq Cloud API.
    
    IMPORTANT: Make sure to update your actual .env file with:
    - GROQ_API_KEY: Your Groq API key from https://console.groq.com/keys
    - GROQ_MODEL_NAME: The model name (default: llama-3.3-70b-versatile)
    """

    groq_api_key: str = Field(
        default_factory=lambda: os.getenv("GROQ_API_KEY", "")
    )
    groq_model_name: str = Field(
        default_factory=lambda: os.getenv("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")
    )

    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields (like old Ollama variables)


def get_llm(temperature: float = 0.7) -> str:
    """
    Factory function to create and configure the Groq LLM for CrewAI.
    
    CrewAI has built-in support for Groq. This function validates the API key
    and returns the proper string format that CrewAI expects.
    
    Args:
        temperature: Controls randomness in responses (0.0 = deterministic, 1.0 = creative)
        
    Returns:
        str: CrewAI-compatible LLM string in format "groq/<model_name>"
        
    Raises:
        ValueError: If GROQ_API_KEY is not set
        
    Example:
        >>> llm = get_llm(temperature=0.7)
        >>> # Returns: "groq/llama-3.3-70b-versatile"
    """
    settings = Settings()
    
    # Validate API key
    if not settings.groq_api_key or settings.groq_api_key == "your_groq_api_key_here":
        raise ValueError(
            "GROQ_API_KEY is not set or is using the placeholder value. "
            "Please set your Groq API key in the .env file. "
            "Get your API key from: https://console.groq.com/keys"
        )
    
    # Set environment variable for CrewAI to use
    os.environ["GROQ_API_KEY"] = settings.groq_api_key
    
    # Return CrewAI-compatible format
    # CrewAI will automatically use the GROQ_API_KEY from environment
    return f"groq/{settings.groq_model_name}"

