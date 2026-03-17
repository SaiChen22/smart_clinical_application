import importlib
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

data_quality_module = importlib.import_module("app.schemas.data_quality")
reconciliation_module = importlib.import_module("app.schemas.reconciliation")
mock_module = importlib.import_module("app.services.llm.mock")

DataQualityRequest = data_quality_module.DataQualityRequest
DataQualityResponse = data_quality_module.DataQualityResponse
Demographics = data_quality_module.Demographics
VitalSigns = data_quality_module.VitalSigns
MedicationSource = reconciliation_module.MedicationSource
PatientContext = reconciliation_module.PatientContext
ReconciliationRequest = reconciliation_module.ReconciliationRequest
ReconciliationResponse = reconciliation_module.ReconciliationResponse
MockProvider = mock_module.MockProvider


def test_mock_provider_name() -> None:
    provider = MockProvider()
    assert provider.provider_name == "mock"


@pytest.mark.asyncio
async def test_mock_reconcile_medications() -> None:
    provider = MockProvider()
    request = ReconciliationRequest(
        patient_context=PatientContext(age=62, conditions=["hypertension"], recent_labs={}),
        sources=[
            MedicationSource(
                system="Clinic EHR",
                medication="Lisinopril 10mg",
                last_updated="2024-03-01T09:00:00",
                source_reliability="high",
            ),
            MedicationSource(
                system="Hospital A",
                medication="Lisinopril 20mg",
                last_updated="2024-03-15T14:30:00",
                source_reliability="high",
            ),
        ],
    )

    response = await provider.reconcile_medications(request)

    assert isinstance(response, ReconciliationResponse)
    assert response.reconciled_medication
    assert 0.0 <= response.confidence_score <= 1.0
    assert len(response.reasoning.strip()) > 20


@pytest.mark.asyncio
async def test_mock_assess_data_quality() -> None:
    provider = MockProvider()
    request = DataQualityRequest(
        demographics=Demographics(name="Jane Doe", dob="1980-06-12", gender="female"),
        medications=["Metformin 500mg"],
        allergies=["Penicillin"],
        conditions=["Type 2 diabetes"],
        vital_signs=VitalSigns(blood_pressure="128/82", heart_rate=72, temperature=98.6),
        last_updated="2026-03-01T10:00:00",
    )

    response = await provider.assess_data_quality(request)

    assert isinstance(response, DataQualityResponse)
    assert 0 <= response.overall_score <= 100
    assert all(
        0 <= score <= 100
        for score in (
            response.breakdown.completeness,
            response.breakdown.accuracy,
            response.breakdown.timeliness,
            response.breakdown.clinical_plausibility,
        )
    )
    assert isinstance(response.issues_detected, list)
