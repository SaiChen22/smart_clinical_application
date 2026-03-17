import os
import sys
from datetime import UTC, datetime, timedelta

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.core.config import Settings, get_settings
from app.main import app


def test_validate_implausible_vitals() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        llm_mock_mode=True,
        llm_provider="mock",
        api_key="",
    )

    stale_timestamp = (datetime.now(UTC) - timedelta(days=210)).isoformat()

    request_body = {
        "demographics": {
            "name": "John Doe",
            "dob": "1975-06-15",
            "gender": "male",
        },
        "medications": ["Lisinopril 10mg"],
        "allergies": [],
        "conditions": ["hypertension"],
        "vital_signs": {
            "blood_pressure": "340/180",
            "heart_rate": 88,
            "temperature": 37.0,
        },
        "last_updated": stale_timestamp,
    }

    with TestClient(app) as client:
        response = client.post(
            "/api/data-quality/validate",
            json=request_body,
            headers={"X-API-Key": "dev-key"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()

    assert 30 <= payload["overall_score"] <= 80
    assert payload["breakdown"]["clinical_plausibility"] < 60

    bp_issues = [
        issue
        for issue in payload["issues_detected"]
        if issue["field"] == "vital_signs.blood_pressure"
        and "outside plausible range" in issue["issue"]
    ]
    assert bp_issues
    assert any(issue["severity"] == "high" for issue in bp_issues)


def test_validate_perfect_record() -> None:
    app.dependency_overrides[get_settings] = lambda: Settings(
        llm_mock_mode=True,
        llm_provider="mock",
        api_key="",
    )

    fresh_timestamp = (datetime.now(UTC) - timedelta(days=5)).isoformat()

    request_body = {
        "demographics": {
            "name": "Jane Doe",
            "dob": "1988-04-12",
            "gender": "female",
        },
        "medications": ["Metformin 500mg"],
        "allergies": ["Penicillin"],
        "conditions": ["type 2 diabetes"],
        "vital_signs": {
            "blood_pressure": "120/80",
            "heart_rate": 72,
            "temperature": 37.0,
        },
        "last_updated": fresh_timestamp,
    }

    with TestClient(app) as client:
        response = client.post(
            "/api/data-quality/validate",
            json=request_body,
            headers={"X-API-Key": "dev-key"},
        )

    app.dependency_overrides.clear()

    assert response.status_code == 200
    payload = response.json()

    assert payload["overall_score"] > 85
    assert all(issue["severity"] == "low" for issue in payload["issues_detected"])
