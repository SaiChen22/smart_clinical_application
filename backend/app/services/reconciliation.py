from __future__ import annotations

import re
from datetime import datetime

from ..schemas.reconciliation import (
    MedicationSource,
    PatientContext,
    ReconciliationRequest,
    ReconciliationResponse,
)
from .llm.base import LLMProvider


class ReconciliationService:
    async def reconcile(
        self, request: ReconciliationRequest, llm_provider: LLMProvider
    ) -> ReconciliationResponse:
        try:
            sorted_sources = self._sort_sources_by_date(request.sources)
            self._validate_medication_names(sorted_sources)

            normalized_request: ReconciliationRequest = request.model_copy(
                update={"sources": sorted_sources}
            )
            response: ReconciliationResponse = await llm_provider.reconcile_medications(
                normalized_request
            )

            clamped_confidence = max(0.0, min(1.0, response.confidence_score))
            safety_check = self._check_safety(
                response.reconciled_medication,
                normalized_request.patient_context,
            )

            if safety_check == "WARNING":
                recommended_actions = list(response.recommended_actions)
                recommended_actions.append(
                    "Escalate reconciliation result for clinician safety review"
                )
                return response.model_copy(
                    update={
                        "confidence_score": clamped_confidence,
                        "clinical_safety_check": "WARNING",
                        "recommended_actions": recommended_actions,
                    }
                )

            return response.model_copy(
                update={
                    "confidence_score": clamped_confidence,
                    "clinical_safety_check": response.clinical_safety_check,
                }
            )

        except Exception as exc:
            fallback_medication = request.sources[0].medication if request.sources else "unknown"
            return ReconciliationResponse(
                reconciled_medication=fallback_medication,
                confidence_score=0.0,
                reasoning=(
                    "Fallback response generated due to reconciliation processing "
                    f"error: {exc}"
                ),
                recommended_actions=[
                    "Review source records manually",
                    "Retry reconciliation after data validation",
                ],
                clinical_safety_check="WARNING",
            )

    def _sort_sources_by_date(
        self, sources: list[MedicationSource]
    ) -> list[MedicationSource]:
        def parse_timestamp(value: str | None) -> datetime:
            if not value:
                return datetime.min
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                return datetime.min

        return sorted(
            sources,
            key=lambda source: max(
                parse_timestamp(source.last_updated),
                parse_timestamp(source.last_filled),
            ),
            reverse=True,
        )

    def _validate_medication_names(self, sources: list[MedicationSource]) -> None:
        for source in sources:
            if not source.medication.strip():
                raise ValueError("Medication name cannot be empty")

    def _check_safety(self, medication: str, patient_context: PatientContext) -> str:
        lowered_medication = medication.lower()

        if "metformin" in lowered_medication:
            dosages: list[str] = re.findall(r"(\d+(?:\.\d+)?)\s*mg", lowered_medication)
            if any(float(dose) > 2550 for dose in dosages):
                return "WARNING"

        if "warfarin" in lowered_medication:
            for condition in patient_context.conditions:
                if "aspirin" in condition.lower():
                    return "WARNING"

        return "PASSED"
