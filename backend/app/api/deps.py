"""Dependency injection utilities for FastAPI."""

from typing import AsyncGenerator

from app.core.config import Settings, get_settings


async def get_settings_dep() -> Settings:
    """Dependency for getting settings."""
    return get_settings()


async def get_db() -> AsyncGenerator:
    """Dependency for getting database session.
    
    Stub implementation - to be replaced with actual SQLAlchemy session management.
    """
    # TODO: Implement database session management
    yield


async def get_llm_provider() -> str:
    """Dependency for getting configured LLM provider.
    
    Returns the configured LLM provider name.
    """
    settings = get_settings()
    return settings.llm_provider
