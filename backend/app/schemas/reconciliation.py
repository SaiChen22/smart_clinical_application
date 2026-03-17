"""Reconciliation request/response schemas."""

from typing import Literal
from pydantic import BaseModel, Field, field_validator


class PatientContext(BaseModel):
    """Patient clinical context for reconciliation."""

    age: int = Field(..., ge=0, le=150, description="Patient age in years")
    conditions: list[str] = Field(
        ..., min_length=1, description="List of active medical conditions"
    )
    recent_labs: dict[str, float] = Field(
        default_factory=dict, description="Recent lab values (test_name: value)"
    )


class MedicationSource(BaseModel):
    """Medication from a single source system."""

    system: str = Field(..., description="Source system name (e.g., EHR, Pharmacy)")
    medication: str = Field(..., description="Medication name or identifier")
    last_updated: str | None = Field(
        default=None, description="ISO timestamp of last update"
    )
    last_filled: str | None = Field(default=None, description="ISO timestamp of last fill")
    source_reliability: Literal["high", "medium", "low"] = Field(
        ..., description="Reliability assessment of the source"
    )


class ReconciliationRequest(BaseModel):
    """Request to reconcile medications from multiple sources."""

    patient_context: PatientContext
    sources: list[MedicationSource] = Field(
        ..., min_length=1, max_length=50, description="Medication sources to reconcile"
    )


class ReconciliationResponse(BaseModel):
    """Response with reconciled medication information."""

    reconciled_medication: str = Field(
        ..., description="Canonical medication name after reconciliation"
    )
    confidence_score: float = Field(
        ..., ge=0.0, le=1.0, description="Confidence in reconciliation (0.0-1.0)"
    )
    reasoning: str = Field(..., description="Explanation of reconciliation logic")
    recommended_actions: list[str] = Field(
        ..., description="List of recommended clinical actions"
    )
    clinical_safety_check: Literal["PASSED", "FAILED", "WARNING"] = Field(
        ..., description="Safety assessment result"
    )

    @field_validator("confidence_score")
    @classmethod
    def validate_confidence_score(cls, v: float) -> float:
        """Validate confidence score is in valid range."""
        if not (0.0 <= v <= 1.0):
            raise ValueError("confidence_score must be between 0.0 and 1.0")
        return v
