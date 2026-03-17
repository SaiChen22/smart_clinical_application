"""API key authentication security for Clinical Data Reconciliation Engine."""

import logging
import secrets
from typing import Annotated

from fastapi import Depends, Header, HTTPException

from app.core.config import get_settings

logger = logging.getLogger(__name__)


async def verify_api_key(
    x_api_key: Annotated[str, Header()] = "",
) -> str:
    """Verify API key from X-API-Key header.
    
    Compares the provided API key against settings.api_key using timing-safe comparison.
    If settings.api_key is empty, logs warning and allows all requests (dev mode).
    
    Args:
        x_api_key: API key from X-API-Key header
        
    Returns:
        The API key if valid
        
    Raises:
        HTTPException: 401 UNAUTHORIZED if API key is invalid or missing
    """
    settings = get_settings()
    
    # If no API key configured, allow all (dev mode)
    if not settings.api_key:
        logger.warning("⚠ API key not configured - allowing all requests (development mode)")
        return x_api_key
    
    # Compare API keys using timing-safe comparison
    if not x_api_key or not secrets.compare_digest(x_api_key, settings.api_key):
        raise HTTPException(
            status_code=401,
            detail={
                "code": "UNAUTHORIZED",
                "message": "Invalid or missing API key"
            }
        )
    
    return x_api_key
