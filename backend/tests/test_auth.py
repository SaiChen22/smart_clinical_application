"""Tests for API key authentication."""

import os
import sys
import pytest
from unittest.mock import patch

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from fastapi import HTTPException
from app.core.security import verify_api_key
from app.core.config import Settings


@pytest.mark.asyncio
async def test_unauthenticated_request_rejected():
    """Test that unauthenticated requests without API key are rejected with 401."""
    # Mock settings with an API key configured
    with patch("app.core.security.get_settings") as mock_settings:
        mock_settings.return_value = Settings(api_key="test-secret-key-12345")
        
        # Test with empty API key - should raise 401
        with pytest.raises(HTTPException) as exc_info:
            await verify_api_key(x_api_key="")
        
        # Verify the exception details
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail["code"] == "UNAUTHORIZED"
        assert exc_info.value.detail["message"] == "Invalid or missing API key"


@pytest.mark.asyncio
async def test_authenticated_request_passes():
    """Test that authenticated requests with valid API key pass."""
    test_key = "test-secret-key-12345"
    
    # Mock settings with an API key configured
    with patch("app.core.security.get_settings") as mock_settings:
        mock_settings.return_value = Settings(api_key=test_key)
        
        # Test with valid API key - should not raise exception
        result = await verify_api_key(x_api_key=test_key)
        assert result == test_key
