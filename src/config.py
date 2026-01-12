import os
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """
    Centralized configuration.

    Docker networking note:
    Inside docker-compose, the app talks to Ollama via
    http://ollama:11434 (service name = hostname).
    """

    ollama_base_url: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    )
    llm_model: str = Field(
        default_factory=lambda: os.getenv("LLM_MODEL", "llama3")
    )
    ollama_host: str = Field(
        default_factory=lambda: os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )

    class Config:
        env_file = ".env"


