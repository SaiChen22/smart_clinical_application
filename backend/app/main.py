"""Main FastAPI application for Clinical Data Reconciliation Engine."""

import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.routes import data_quality, reconciliation
from .core.config import get_settings
from .core.database import init_db

logger = logging.getLogger(__name__)


async def check_github_models_api() -> bool:
    """Check GitHub Models API access when GitHub token is set and mock mode is disabled.
    
    Returns:
        True if API is accessible or mock mode enabled, False otherwise.
    """
    settings = get_settings()
    
    # Skip check if mock mode is enabled or no GitHub token
    if settings.llm_mock_mode or not settings.github_token:
        return True
    
    try:
        # Test GitHub Models API endpoint
        headers = {"Authorization": f"Bearer {settings.github_token}"}
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.head(
                "https://models.inference.ai.azure.com",
                headers=headers,
                follow_redirects=True
            )
            if response.status_code < 500:
                logger.info("✓ GitHub Models API is accessible")
                return True
            else:
                logger.warning(f"⚠ GitHub Models API returned status {response.status_code}")
                return False
    except Exception as e:
        logger.warning(f"⚠ GitHub Models API check failed: {str(e)}")
        return False


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown lifespan events."""
    # Startup
    logger.info("Starting Clinical Data Reconciliation Engine...")
    init_db()
    await check_github_models_api()
    yield
    # Shutdown
    logger.info("Shutting down Clinical Data Reconciliation Engine...")


app = FastAPI(
    title="Clinical Data Reconciliation Engine",
    description="AI-powered clinical EHR data reconciliation system",
    version="1.0.0",
    lifespan=lifespan,
)

# Get settings
settings = get_settings()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reconciliation.router)
app.include_router(data_quality.router)


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "version": "1.0.0"}
