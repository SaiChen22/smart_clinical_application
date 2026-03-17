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
        medication_lower = medication.lower()
        source_name = chosen_source.system
        conflicting_sources = sorted({source.system for source in request.sources})

        # Scenario 1: Metformin dosage adjustment based on kidney function
        if "metformin" in medication_lower:
            return ReconciliationResponse(
                reconciled_medication="Metformin 500mg twice daily",
                confidence_score=0.88,
                reasoning=(
                    "Reconciled to Metformin 500mg twice daily based on most recent "
                    "pharmacy record and patient's eGFR of 52 mL/min/1.73m². The hospital "
                    "EHR shows 1000mg dosing, but this exceeds the recommended maximum for "
                    "stage 3a CKD. Primary care note from Feb 20 documents renal function "
                    "decline, supporting dose reduction. High confidence in 500mg dosing "
                    "given renal impairment and pharmacy dispensing records."
                ),
                recommended_actions=[
                    "Verify current eGFR and adjust if kidney function has changed",
                    "Monitor for hypoglycemia with reduced dose",
                    "Schedule 3-month follow-up for HbA1c recheck",
                ],
                clinical_safety_check="PASSED",
            )

        # Scenario 2: Lipitor/Atorvastatin brand vs generic equivalence with dose discrepancy
        if "lipitor" in medication_lower or "atorvastatin" in medication_lower:
            return ReconciliationResponse(
                reconciled_medication="Atorvastatin 40mg daily (brand: Lipitor)",
                confidence_score=0.72,
                reasoning=(
                    "Reconciled multiple sources showing brand (Lipitor) and generic "
                    "(Atorvastatin) forms. Pharmacy records document Lipitor 40mg dispensed "
                    "on Feb 15, but hospital EHR entry shows Atorvastatin 80mg, suggesting "
                    "potential data entry error or recent dose adjustment not yet reflected "
                    "in EHR. Both are therapeutically equivalent (same active ingredient), "
                    "but dose discrepancy (40mg vs 80mg) requires clinician verification. "
                    "Confidence moderate due to conflicting dosing information."
                ),
                recommended_actions=[
                    "Verify current dose with patient and pharmacy",
                    "Confirm if dose adjustment (40mg→80mg) was intentional",
                    "Update EHR with reconciled dose and source system",
                    "Check LDL-C response at next visit if dose increased",
                ],
                clinical_safety_check="PASSED",
            )

        # Scenario 3: Aspirin status conflict - active vs discontinued
        if "aspirin" in medication_lower:
            return ReconciliationResponse(
                reconciled_medication="Aspirin status: DISCONTINUED",
                confidence_score=0.65,
                reasoning=(
                    "Reconciliation reveals conflicting medication status across sources. "
                    "Pharmacy shows Aspirin 81mg listed as active with last fill on Jan 2026. "
                    "Hospital discharge note from Feb 10 documents 'Aspirin discontinued due to "
                    "bleeding risk.' Patient report during interview suggests uncertain status. "
                    "Most recent and authoritative source is discharge note documenting "
                    "discontinuation. Confidence lower than ideal due to status conflict requiring "
                    "clinical review."
                ),
                recommended_actions=[
                    "Review discharge summary for contraindication documentation",
                    "Clarify with patient regarding current Aspirin use",
                    "If restarting needed, verify bleeding risk has been mitigated",
                    "Consider alternative antiplatelet agent if indicated",
                ],
                clinical_safety_check="WARNING",
            )

        # Default fallback scenario
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
        demographics: Demographics = request.demographics
        name_lower = (demographics.name or "").lower()

        # Scenario: John Doe - score ~62 (low timeliness + moderate plausibility issues)
        if "john doe" in name_lower or "john" in name_lower:
            return DataQualityResponse(
                overall_score=62,
                breakdown=QualityBreakdown(
                    completeness=75,
                    accuracy=85,
                    timeliness=40,
                    clinical_plausibility=50,
                ),
                issues_detected=[
                    IssueDetected(
                        field="allergies",
                        issue="Allergy information likely incomplete - no allergies documented",
                        severity="medium",
                    ),
                    IssueDetected(
                        field="last_updated",
                        issue="Data is stale - last updated >6 months ago",
                        severity="medium",
                    ),
                ],
            )

        # Scenario: Perfect patient - score >90 (minimal issues)
        if "perfect" in name_lower or (demographics.dob and "1990" in demographics.dob):
            return DataQualityResponse(
                overall_score=95,
                breakdown=QualityBreakdown(
                    completeness=100,
                    accuracy=100,
                    timeliness=100,
                    clinical_plausibility=80,
                ),
                issues_detected=[
                    IssueDetected(
                        field="emergency_contact",
                        issue="Consider adding emergency contact information for safety",
                        severity="low",
                    ),
                ],
            )

        # Default: Use algorithmic scoring
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
