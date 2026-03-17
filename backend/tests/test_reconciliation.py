import os
import sys
from typing import Any

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import Settings, get_settings
from app.main import app


def test_reconcile_medication_happy_path() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        llm_mock_mode=True,
        llm_provider="mock",
        api_key="",
    )

    request_body = {
        "patient_context": {
            "age": 58,
            "conditions": ["type 2 diabetes"],
            "recent_labs": {"hba1c": 7.1},
        },
        "sources": [
            {
                "system": "Hospital EHR",
                "medication": "Metformin 500mg",
                "last_updated": "2024-02-20T08:00:00",
                "source_reliability": "high",
            },
            {
                "system": "Pharmacy",
                "medication": "Metformin 1000mg",
                "last_updated": "2024-03-02T10:30:00",
                "source_reliability": "high",
            },
        ],
    }

    with TestClient(app) as client:
        response = client.post(
            "/api/reconcile/medication",
            json=request_body,
            headers={"X-API-Key": "dev-key"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload: dict[str, Any] = response.json()

    required_fields = {
        "reconciled_medication",
        "confidence_score",
        "reasoning",
        "recommended_actions",
        "clinical_safety_check",
    }
    assert required_fields.issubset(payload.keys())
    assert 0.0 <= payload["confidence_score"] <= 1.0
    assert payload["reasoning"].strip()


def test_reconcile_medication_single_source() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        llm_mock_mode=True,
        llm_provider="mock",
        api_key="",
    )

    request_body = {
        "patient_context": {
            "age": 45,
            "conditions": ["hypertension"],
            "recent_labs": {},
        },
        "sources": [
            {
                "system": "Clinic EHR",
                "medication": "Lisinopril 10mg",
                "last_updated": "2024-03-01T09:00:00",
                "source_reliability": "high",
            }
        ],
    }

    with TestClient(app) as client:
        response = client.post(
            "/api/reconcile/medication",
            json=request_body,
            headers={"X-API-Key": "dev-key"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload: dict[str, Any] = response.json()
    assert payload["reconciled_medication"] == "Lisinopril 10mg"
    assert payload["confidence_score"] >= 0.8
