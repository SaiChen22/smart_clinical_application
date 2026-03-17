"""Tests for error handling across the Clinical Data Reconciliation Engine."""

import os
import sys
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import Settings, get_settings
from app.core.exceptions import (
    DataQualityError,
    LLMTimeoutError,
    RateLimitError,
    ReconciliationError,
)
from app.main import app


def test_llm_timeout_error_handler() -> None:
    """Test that LLMTimeoutError returns 503 with Retry-After header."""
    app.dependency_overrides[get_settings] = lambda: Settings(
        llm_mock_mode=False,
        llm_provider="github_models",
        api_key="",
        github_token="test-token",
    )

    request_body = {
        "patient_context": {
            "age": 45,
            "conditions": ["diabetes"],
            "recent_labs": {"glucose": 120},
        },
        "sources": [
            {
                "system": "EHR",
                "medication": "Metformin 500mg",
                "last_updated": "2024-01-01T00:00:00",
                "source_reliability": "high",
            }
        ],
    }

    # Mock the reconcile function to raise LLMTimeoutError
    with patch(
        "app.services.reconciliation.ReconciliationService.reconcile",
        new_callable=AsyncMock,
        side_effect=LLMTimeoutError(
            message="LLM request timed out after 30 seconds", retry_after=30
        ),
    ):
        with TestClient(app) as client:
            response = client.post(
                "/api/reconcile/medication",
                json=request_body,
                headers={"X-API-Key": "dev-key"},
            )

    app.dependency_overrides.clear()

    assert response.status_code == 503
    assert response.json() == {
        "detail": {
            "code": "LLM_TIMEOUT",
            "message": "LLM request timed out after 30 seconds",
        }
    }
    assert response.headers.get("Retry-After") == "30"


def test_rate_limit_error_handler() -> None:
    """Test that RateLimitError returns 429 with Retry-After header."""
    app.dependency_overrides[get_settings] = lambda: Settings(
        llm_mock_mode=False,
        llm_provider="github_models",
        api_key="",
        github_token="test-token",
    )

    request_body = {
        "patient_context": {
            "age": 45,
            "conditions": ["diabetes"],
            "recent_labs": {"glucose": 120},
        },
        "sources": [
            {
                "system": "EHR",
                "medication": "Metformin 500mg",
                "last_updated": "2024-01-01T00:00:00",
                "source_reliability": "high",
            }
        ],
    }

    # Mock the ReconciliationService.reconcile to raise RateLimitError
    with patch(
        "app.services.reconciliation.ReconciliationService.reconcile",
        new_callable=AsyncMock,
        side_effect=RateLimitError(
            message="Rate limit exceeded. Try again later.", retry_after=60
        ),
    ):
        with TestClient(app) as client:
            response = client.post(
                "/api/reconcile/medication",
                json=request_body,
                headers={"X-API-Key": "dev-key"},
            )

    app.dependency_overrides.clear()

    assert response.status_code == 429
    assert response.json() == {
        "detail": {
            "code": "RATE_LIMIT_EXCEEDED",
            "message": "Rate limit exceeded. Try again later.",
        }
    }
    assert response.headers.get("Retry-After") == "60"


def test_reconciliation_error_handler() -> None:
    """Test that ReconciliationError returns 500 with error details."""
    app.dependency_overrides[get_settings] = lambda: Settings(
        llm_mock_mode=False,
        llm_provider="github_models",
        api_key="",
        github_token="test-token",
    )

    request_body = {
        "patient_context": {
            "age": 45,
            "conditions": ["diabetes"],
            "recent_labs": {"glucose": 120},
        },
        "sources": [
            {
                "system": "EHR",
                "medication": "Metformin 500mg",
                "last_updated": "2024-01-01T00:00:00",
                "source_reliability": "high",
            }
        ],
    }

    # Mock the ReconciliationService.reconcile to raise ReconciliationError
    with patch(
        "app.services.reconciliation.ReconciliationService.reconcile",
        new_callable=AsyncMock,
        side_effect=ReconciliationError(
            message="Malformed LLM response: missing required fields",
            code="MALFORMED_RESPONSE",
        ),
    ):
        with TestClient(app) as client:
            response = client.post(
                "/api/reconcile/medication",
                json=request_body,
                headers={"X-API-Key": "dev-key"},
            )

    app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "detail": {
            "code": "MALFORMED_RESPONSE",
            "message": "Malformed LLM response: missing required fields",
        }
    }


def test_data_quality_error_handler() -> None:
    """Test that DataQualityError returns 500 with error details."""
    app.dependency_overrides[get_settings] = lambda: Settings(
        llm_mock_mode=False,
        llm_provider="github_models",
        api_key="",
        github_token="test-token",
    )

    request_body = {
        "demographics": {"name": "John Doe", "dob": "1958-01-01", "gender": "male"},
        "medications": ["Lisinopril 10mg"],
        "allergies": ["Penicillin"],
        "conditions": ["hypertension"],
        "vital_signs": {"blood_pressure": "140/90", "heart_rate": 72},
        "last_updated": "2024-01-01T00:00:00",
    }

    # Mock the DataQualityService.assess to raise DataQualityError
    with patch(
        "app.services.data_quality.DataQualityService.assess",
        new_callable=AsyncMock,
        side_effect=DataQualityError(
            message="Validation failed: age must be between 0 and 120",
            code="VALIDATION_ERROR",
        ),
    ):
        with TestClient(app) as client:
            response = client.post(
                "/api/data-quality/validate",
                json=request_body,
                headers={"X-API-Key": "dev-key"},
            )

    app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json() == {
        "detail": {
            "code": "VALIDATION_ERROR",
            "message": "Validation failed: age must be between 0 and 120",
        }
    }
