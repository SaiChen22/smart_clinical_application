"""Configuration management for Clinical Data Reconciliation Engine."""

from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables and .env file."""

    # API Configuration
    api_key: str = ""

    # Authentication
    github_token: str = ""
    anthropic_api_key: str = ""
    openai_api_key: str = ""

    # LLM Configuration
    llm_provider: str = "mock"
    llm_mock_mode: bool = True

    # Database
    database_url: str = "sqlite:///./reconciliation.db"

    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:5173"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
