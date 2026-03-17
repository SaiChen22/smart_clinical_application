"""Data quality assessment schemas."""

from typing import Literal
from pydantic import BaseModel, Field, field_validator


class Demographics(BaseModel):
    """Patient demographic information."""

    name: str | None = Field(default=None, description="Patient name")
    dob: str | None = Field(default=None, description="Date of birth (ISO format)")
    gender: str | None = Field(default=None, description="Gender")


class VitalSigns(BaseModel):
    """Patient vital signs."""

    blood_pressure: str | None = Field(
        default=None, description="Blood pressure (e.g., '120/80')"
    )
    heart_rate: int | None = Field(default=None, description="Heart rate in bpm")
    temperature: float | None = Field(default=None, description="Temperature in Celsius")


class IssueDetected(BaseModel):
    """Data quality issue identified."""

    field: str = Field(..., description="Field name with issue")
    issue: str = Field(..., description="Description of the issue")
    severity: Literal["low", "medium", "high"] = Field(
        ..., description="Issue severity level"
    )


class QualityBreakdown(BaseModel):
    """Detailed quality scores for different dimensions."""

    completeness: int = Field(
        ..., ge=0, le=100, description="Completeness score (0-100)"
    )
    accuracy: int = Field(..., ge=0, le=100, description="Accuracy score (0-100)")
    timeliness: int = Field(..., ge=0, le=100, description="Timeliness score (0-100)")
    clinical_plausibility: int = Field(
        ..., ge=0, le=100, description="Clinical plausibility score (0-100)"
    )


class DataQualityRequest(BaseModel):
    """Request for data quality assessment."""

    demographics: Demographics
    medications: list[str] = Field(..., description="List of medications")
    allergies: list[str] = Field(..., description="List of allergies")
    conditions: list[str] = Field(..., description="List of active conditions")
    vital_signs: VitalSigns
    last_updated: str | None = Field(
        default=None, description="ISO timestamp of last update"
    )


class DataQualityResponse(BaseModel):
    """Response with overall and detailed data quality assessment."""

    overall_score: int = Field(
        ..., ge=0, le=100, description="Overall quality score (0-100)"
    )
    breakdown: QualityBreakdown = Field(..., description="Breakdown by quality dimension")
    issues_detected: list[IssueDetected] = Field(
        ..., description="List of detected quality issues"
    )

    @field_validator("overall_score")
    @classmethod
    def validate_overall_score(cls, v: int) -> int:
        """Validate overall score is in valid range."""
        if not (0 <= v <= 100):
            raise ValueError("overall_score must be between 0 and 100")
        return v
