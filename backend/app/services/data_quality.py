from __future__ import annotations

from datetime import UTC, datetime

from ..schemas.data_quality import (
    DataQualityRequest,
    DataQualityResponse,
    Demographics,
    IssueDetected,
    QualityBreakdown,
    VitalSigns,
)
from .llm.base import LLMProvider


class DataQualityService:
    async def assess(
        self, request: DataQualityRequest, llm_provider: LLMProvider
    ) -> DataQualityResponse:
        _ = llm_provider

        issues: list[IssueDetected] = []
        completeness = self._score_completeness(request, issues)
        accuracy = self._score_accuracy(request, issues)
        timeliness = self._score_timeliness(request.last_updated, issues)
        plausibility = self._score_clinical_plausibility(request.vital_signs, issues)

        overall_score = round((completeness + accuracy + timeliness + plausibility) / 4)

        return DataQualityResponse(
            overall_score=overall_score,
            breakdown=QualityBreakdown(
                completeness=completeness,
                accuracy=accuracy,
                timeliness=timeliness,
                clinical_plausibility=plausibility,
            ),
            issues_detected=issues,
        )

    def _score_completeness(
        self, request: DataQualityRequest, issues: list[IssueDetected]
    ) -> int:
        demographics: Demographics = request.demographics
        vital_signs: VitalSigns = request.vital_signs

        weighted_fields: list[tuple[object, int]] = [
            (demographics.name, 2),
            (demographics.dob, 2),
            (demographics.gender, 1),
            (request.medications, 2),
            (request.allergies, 1),
            (request.conditions, 1),
            (vital_signs.blood_pressure, 1),
            (vital_signs.heart_rate, 1),
            (vital_signs.temperature, 1),
            (request.last_updated, 1),
        ]

        total_weight = sum(weight for _, weight in weighted_fields)
        present_weight = 0

        for value, weight in weighted_fields:
            if self._is_present(value):
                present_weight += weight

        if len(request.allergies) == 0:
            issues.append(
                IssueDetected(
                    field="allergies",
                    issue="Allergy information likely incomplete",
                    severity="medium",
                )
            )

        return round((present_weight / total_weight) * 100)

    def _score_accuracy(
        self, request: DataQualityRequest, issues: list[IssueDetected]
    ) -> int:
        score = 100

        demographics: Demographics = request.demographics

        if demographics.dob:
            try:
                datetime.fromisoformat(demographics.dob)
            except ValueError:
                score -= 25
                issues.append(
                    IssueDetected(
                        field="demographics.dob",
                        issue="Date of birth is not a valid ISO date",
                        severity="medium",
                    )
                )

        if demographics.gender and demographics.gender.lower() not in {
            "male",
            "female",
            "other",
        }:
            score -= 20
            issues.append(
                IssueDetected(
                    field="demographics.gender",
                    issue="Gender must be one of: male, female, other",
                    severity="low",
                )
            )

        invalid_medications = [med for med in request.medications if not med.strip()]
        if invalid_medications:
            score -= min(30, 10 * len(invalid_medications))
            issues.append(
                IssueDetected(
                    field="medications",
                    issue="Medication entries must be non-empty strings",
                    severity="medium",
                )
            )

        return max(0, score)

    def _score_timeliness(
        self, last_updated: str | None, issues: list[IssueDetected]
    ) -> int:
        if not last_updated:
            issues.append(
                IssueDetected(
                    field="last_updated",
                    issue="Last updated timestamp is missing; timeliness is uncertain",
                    severity="low",
                )
            )
            return 50

        timestamp = self._parse_datetime(last_updated)
        if timestamp is None:
            issues.append(
                IssueDetected(
                    field="last_updated",
                    issue="Last updated timestamp is not a valid ISO datetime",
                    severity="medium",
                )
            )
            return 50

        age_days = (datetime.now(UTC) - timestamp).days
        if age_days < 30:
            return 100
        if age_days < 90:
            return 80
        if age_days < 180:
            return 60
        if age_days < 365:
            return 40
        return 20

    def _score_clinical_plausibility(
        self, vital_signs: VitalSigns, issues: list[IssueDetected]
    ) -> int:
        has_out_of_range = False

        bp = vital_signs.blood_pressure
        if bp:
            systolic, diastolic = self._parse_blood_pressure(bp)
            if systolic is None or diastolic is None:
                has_out_of_range = True
                issues.append(
                    IssueDetected(
                        field="vital_signs.blood_pressure",
                        issue="Blood pressure format is invalid; expected systolic/diastolic",
                        severity="high",
                    )
                )
            else:
                if not 60 <= systolic <= 250:
                    has_out_of_range = True
                    issues.append(
                        IssueDetected(
                            field="vital_signs.blood_pressure",
                            issue=(
                                f"Systolic BP {systolic} is outside plausible range (60-250)"
                            ),
                            severity="high",
                        )
                    )
                if not 30 <= diastolic <= 150:
                    has_out_of_range = True
                    issues.append(
                        IssueDetected(
                            field="vital_signs.blood_pressure",
                            issue=(
                                f"Diastolic BP {diastolic} is outside plausible range (30-150)"
                            ),
                            severity="high",
                        )
                    )

        heart_rate = vital_signs.heart_rate
        if heart_rate is not None and not 30 <= heart_rate <= 220:
            has_out_of_range = True
            issues.append(
                IssueDetected(
                    field="vital_signs.heart_rate",
                    issue=f"Heart rate {heart_rate} is outside plausible range (30-220)",
                    severity="medium",
                )
            )

        temperature = vital_signs.temperature
        if temperature is not None and not 35 <= temperature <= 42:
            has_out_of_range = True
            issues.append(
                IssueDetected(
                    field="vital_signs.temperature",
                    issue=(
                        f"Temperature {temperature}°C is outside plausible range (35-42°C)"
                    ),
                    severity="medium",
                )
            )

        return 40 if has_out_of_range else 100

    @staticmethod
    def _is_present(value: object) -> bool:
        if value is None:
            return False
        if isinstance(value, str):
            return bool(value.strip())
        if isinstance(value, list):
            return len(value) > 0
        return True

    @staticmethod
    def _parse_datetime(value: str) -> datetime | None:
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            if parsed.tzinfo is None:
                return parsed.replace(tzinfo=UTC)
            return parsed.astimezone(UTC)
        except ValueError:
            return None

    @staticmethod
    def _parse_blood_pressure(value: str) -> tuple[int | None, int | None]:
        parts = value.split("/")
        if len(parts) != 2:
            return None, None
        try:
            systolic = int(parts[0].strip())
            diastolic = int(parts[1].strip())
            return systolic, diastolic
        except ValueError:
            return None, None
