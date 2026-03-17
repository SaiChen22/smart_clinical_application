from datetime import date, datetime
from typing import override

from ...schemas.data_quality import (
    DataQualityRequest,
    DataQualityResponse,
    Demographics,
    IssueDetected,
    QualityBreakdown,
    VitalSigns,
)
from ...schemas.reconciliation import (
    MedicationSource,
    PatientContext,
    ReconciliationRequest,
    ReconciliationResponse,
)
from .base import LLMProvider


class MockProvider(LLMProvider):
    _scenario_actions: dict[str, list[str]] = {
        "lisinopril": [
            "Confirm blood pressure trend in next 2 weeks",
            "Continue ACE inhibitor monitoring for renal function",
        ],
        "metformin": [
            "Verify recent HbA1c and renal function before refill",
            "Reinforce adherence and lifestyle counseling",
        ],
        "warfarin": [
            "Check INR within 72 hours due to narrow therapeutic window",
            "Review bleeding risk and interacting medications",
        ],
    }

    @property
    @override
    def provider_name(self) -> str:
        return "mock"

    @override
    async def reconcile_medications(
        self, request: ReconciliationRequest
    ) -> ReconciliationResponse:
        chosen_source = self._select_most_recent_source(request)
        patient_context: PatientContext = request.patient_context
        medication = chosen_source.medication
        source_name = chosen_source.system
        conflicting_sources = sorted({source.system for source in request.sources})
        safety_check = "PASSED"

        scenario_actions = self._actions_for_medication(medication)
        reasoning = (
            f"Selected {medication} from {source_name} based on the most recent "
            f"timestamp among conflicting sources ({', '.join(conflicting_sources)}). "
            f"Medication profile was reviewed against active conditions "
            f"({', '.join(patient_context.conditions)}), with a clinical safety "
            f"check result of {safety_check} and no immediate contraindications detected."
        )

        return ReconciliationResponse(
            reconciled_medication=medication,
            confidence_score=0.85,
            reasoning=reasoning,
            recommended_actions=scenario_actions,
            clinical_safety_check=safety_check,
        )

    @override
    async def assess_data_quality(self, request: DataQualityRequest) -> DataQualityResponse:
        issues: list[IssueDetected] = []

        completeness = self._completeness_score(request, issues)
        accuracy, patient_age = self._accuracy_score_and_age(request, issues)
        timeliness = self._timeliness_score(patient_age, issues)
        plausibility = self._plausibility_score(request, issues)
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

    def _select_most_recent_source(
        self, request: ReconciliationRequest
    ) -> MedicationSource:
        def parse_timestamp(value: str | None) -> datetime | None:
            if not value:
                return None
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return None

        best_index = len(request.sources) - 1
        best_value: datetime | None = None

        for index, source in enumerate(request.sources):
            source_times = [parse_timestamp(source.last_updated), parse_timestamp(source.last_filled)]
            current = max((value for value in source_times if value is not None), default=None)
            if current is not None and (best_value is None or current >= best_value):
                best_value = current
                best_index = index

        return request.sources[best_index]

    def _actions_for_medication(self, medication: str) -> list[str]:
        lowered = medication.lower()
        for key, actions in self._scenario_actions.items():
            if key in lowered:
                return actions
        return [
            "Verify current indication and dosing schedule with patient",
            "Document reconciled regimen in the shared medication list",
        ]

    def _completeness_score(
        self, request: DataQualityRequest, issues: list[IssueDetected]
    ) -> int:
        demographics: Demographics = request.demographics
        vital_signs: VitalSigns = request.vital_signs
        fields: list[str | list[str] | int | float | None] = [
            demographics.name,
            demographics.dob,
            demographics.gender,
            request.medications,
            request.allergies,
            request.conditions,
            vital_signs.blood_pressure,
            vital_signs.heart_rate,
            vital_signs.temperature,
            request.last_updated,
        ]
        total = len(fields)
        present = 0
        for value in fields:
            if value is None:
                continue
            if isinstance(value, str) and not value.strip():
                continue
            if isinstance(value, list) and len(value) == 0:
                continue
            present += 1

        if vital_signs.blood_pressure is None:
            issues.append(
                IssueDetected(
                    field="vital_signs.blood_pressure",
                    issue="Missing blood pressure reading",
                    severity="medium",
                )
            )

        return round((present / total) * 100)

    def _accuracy_score_and_age(
        self, request: DataQualityRequest, issues: list[IssueDetected]
    ) -> tuple[int, int | None]:
        demographics: Demographics = request.demographics
        vital_signs: VitalSigns = request.vital_signs
        warnings = False
        patient_age: int | None = None

        if demographics.dob:
            try:
                birth_date = date.fromisoformat(demographics.dob)
                today = date.today()
                patient_age = today.year - birth_date.year - (
                    (today.month, today.day) < (birth_date.month, birth_date.day)
                )
                if patient_age < 0 or patient_age > 150:
                    warnings = True
                    issues.append(
                        IssueDetected(
                            field="demographics.dob",
                            issue="Derived age is outside the expected clinical range (0-150)",
                            severity="high",
                        )
                    )
            except ValueError:
                warnings = True
                issues.append(
                    IssueDetected(
                        field="demographics.dob",
                        issue="Date of birth is not a valid ISO date",
                        severity="medium",
                    )
                )

        if vital_signs.heart_rate is not None and vital_signs.heart_rate <= 0:
            warnings = True
            issues.append(
                IssueDetected(
                    field="vital_signs.heart_rate",
                    issue="Heart rate must be greater than zero",
                    severity="high",
                )
            )

        return (70 if warnings else 100), patient_age

    def _timeliness_score(
        self, patient_age: int | None, issues: list[IssueDetected]
    ) -> int:
        if patient_age is None:
            issues.append(
                IssueDetected(
                    field="demographics.dob",
                    issue="Unable to determine patient age for timeliness scoring",
                    severity="low",
                )
            )
            return 50

        if patient_age < 1:
            return 100

        score = max(0, 100 - patient_age)
        if patient_age >= 60:
            issues.append(
                IssueDetected(
                    field="demographics.dob",
                    issue="Age suggests data may be outdated and should be reviewed",
                    severity="low",
                )
            )
        return score

    def _plausibility_score(
        self, request: DataQualityRequest, issues: list[IssueDetected]
    ) -> int:
        vital_signs: VitalSigns = request.vital_signs
        plausible = True

        bp: str | None = vital_signs.blood_pressure
        if bp:
            parts = bp.split("/")
            try:
                systolic = int(parts[0].strip())
                if not 80 <= systolic <= 200:
                    plausible = False
                    issues.append(
                        IssueDetected(
                            field="vital_signs.blood_pressure",
                            issue="Systolic blood pressure is outside plausible range (80-200)",
                            severity="medium",
                        )
                    )
            except (ValueError, IndexError):
                plausible = False
                issues.append(
                    IssueDetected(
                        field="vital_signs.blood_pressure",
                        issue="Blood pressure format is invalid; expected systolic/diastolic",
                        severity="medium",
                    )
                )

        hr: int | None = vital_signs.heart_rate
        if hr is not None and not 40 <= hr <= 120:
            plausible = False
            issues.append(
                IssueDetected(
                    field="vital_signs.heart_rate",
                    issue="Heart rate is outside plausible range (40-120)",
                    severity="medium",
                )
            )

        temp: float | None = vital_signs.temperature
        if temp is not None and not 95 <= temp <= 105:
            plausible = False
            issues.append(
                IssueDetected(
                    field="vital_signs.temperature",
                    issue="Temperature is outside plausible range (95-105°F)",
                    severity="medium",
                )
            )

        return 100 if plausible else 60
