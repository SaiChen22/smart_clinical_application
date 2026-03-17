"""LLM cache model for Clinical Data Reconciliation Engine."""

from datetime import datetime

from sqlmodel import Column, DateTime, Field, String, SQLModel
from sqlalchemy import Index


class LLMCache(SQLModel, table=True):
    """SQLModel table for caching LLM API responses.
    
    Stores cached responses from LLM providers to reduce API calls
    and improve application performance.
    """
    
    __tablename__ = "llmcache"
    
    id: int | None = Field(default=None, primary_key=True)
    """Primary key identifier."""
    
    prompt_hash: str = Field(
        sa_column=Column(String(64), nullable=False, index=True, unique=True),
    )
    """SHA256 hash of the prompt for unique indexing and fast lookups."""
    
    response_json: str = Field(sa_column=Column(String, nullable=False))
    """JSON-serialized response from the LLM."""
    
    provider: str = Field(sa_column=Column(String(50), nullable=False))
    """LLM provider name (e.g., 'github-models', 'anthropic')."""
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(DateTime, nullable=False),
    )
    """Timestamp when the cache entry was created."""
    
    ttl_seconds: int = Field(default=3600)
    """Time-to-live in seconds. Default: 1 hour (3600 seconds)."""
    
    class Config:
        """SQLModel configuration."""
        table = True

