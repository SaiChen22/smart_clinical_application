"""Database configuration and session management for Clinical Data Reconciliation Engine."""

import logging
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlmodel import SQLModel

from app.core.config import get_settings
# Import models to register them with SQLModel
from app.models.cache import LLMCache  # noqa: F401

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()

# Create engine with SQLite-specific configuration
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False},
    echo=False,
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Generator[Session, None, None]:
    """Dependency to get database session for FastAPI routes.
    
    Yields:
        Session: SQLAlchemy session for database operations.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Initialize database by creating all tables.
    
    This function should be called on application startup to ensure
    all SQLModel tables are created in the database.
    """
    logger.info("Initializing database...")
    SQLModel.metadata.create_all(engine)
    logger.info("✓ Database initialized successfully")
