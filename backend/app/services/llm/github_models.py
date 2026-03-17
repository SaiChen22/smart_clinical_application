# pyright: reportMissingImports=false, reportMissingTypeStubs=false, reportUnknownVariableType=false, reportUnknownMemberType=false, reportUnknownArgumentType=false, reportUnknownParameterType=false, reportUntypedFunctionDecorator=false, reportUnannotatedClassAttribute=false
import importlib
import json
from typing import override

from ...core.config import Settings
from ...schemas.data_quality import (
    DataQualityRequest,
    DataQualityResponse,
    IssueDetected,
    QualityBreakdown,
)
from ...schemas.reconciliation import ReconciliationRequest, ReconciliationResponse
from .base import LLMProvider
from .prompts import (
    DATA_QUALITY_SYSTEM_PROMPT,
    DATA_QUALITY_USER_PROMPT_TEMPLATE,
    RECONCILIATION_SYSTEM_PROMPT,
    RECONCILIATION_USER_PROMPT_TEMPLATE,
)


class _TransientLLMError(Exception):
    pass


class GitHubModelsProvider(LLMProvider):
    def __init__(self, settings: Settings):
        openai_module = importlib.import_module("openai")
        async_openai = getattr(openai_module, "AsyncOpenAI")
        self._client = async_openai(
            api_key=settings.github_token,
            base_url="https://models.inference.ai.azure.com",
            timeout=30.0,
        )
        self._model = "gpt-4o"
        tenacity = importlib.import_module("tenacity")
        self._retry = getattr(tenacity, "retry")
        self._stop_after_attempt = getattr(tenacity, "stop_after_attempt")
        self._wait_exponential = getattr(tenacity, "wait_exponential")
        self._retry_if_exception_type = getattr(tenacity, "retry_if_exception_type")

    @property
    @override
    def provider_name(self) -> str:
        return "github_models"

    @override
    async def reconcile_medications(
        self, request: ReconciliationRequest
    ) -> ReconciliationResponse:
        user_prompt = RECONCILIATION_USER_PROMPT_TEMPLATE.format(
            age=request.patient_context.age,
            conditions=json.dumps(request.patient_context.conditions),
            recent_labs=json.dumps(request.patient_context.recent_labs),
            sources=self._format_sources(request),
        )
        data = await self._request_json_with_parse_retry(
            system_prompt=RECONCILIATION_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            fallback=self._reconciliation_fallback("Malformed or unavailable model response"),
        )
        return ReconciliationResponse(**data)

    @override
    async def assess_data_quality(self, request: DataQualityRequest) -> DataQualityResponse:
        user_prompt = DATA_QUALITY_USER_PROMPT_TEMPLATE.format(
            name=request.demographics.name,
            dob=request.demographics.dob,
            gender=request.demographics.gender,
            medications=json.dumps(request.medications),
            allergies=json.dumps(request.allergies),
            conditions=json.dumps(request.conditions),
            blood_pressure=request.vital_signs.blood_pressure,
            heart_rate=request.vital_signs.heart_rate,
            temperature=request.vital_signs.temperature,
            last_updated=request.last_updated,
        )
        data = await self._request_json_with_parse_retry(
            system_prompt=DATA_QUALITY_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            fallback=self._data_quality_fallback("Malformed or unavailable model response"),
        )
        return DataQualityResponse(**data)

    async def _call_api_once(self, system_prompt: str, user_prompt: str) -> str:
        decorated = self._retry(
            stop=self._stop_after_attempt(3),
            wait=self._wait_exponential(multiplier=1, min=1, max=10),
            retry=self._retry_if_exception_type(_TransientLLMError),
            reraise=True,
        )(self._call_api_raw)
        return await decorated(system_prompt, user_prompt)

    async def _call_api_raw(self, system_prompt: str, user_prompt: str) -> str:
        try:
            response = await self._client.chat.completions.create(
                model=self._model,
                temperature=0.2,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                timeout=30.0,
            )
            content = response.choices[0].message.content
            return content if content else "{}"
        except Exception as exc:
            if exc.__class__.__name__ in {
                "APITimeoutError",
                "APIConnectionError",
                "RateLimitError",
                "TimeoutException",
                "ReadTimeout",
                "ConnectTimeout",
            }:
                raise _TransientLLMError from exc
            raise

    async def _request_json_with_parse_retry(
        self, system_prompt: str, user_prompt: str, fallback: dict[str, object]
    ) -> dict[str, object]:
        for _ in range(2):
            try:
                raw_content = await self._call_api_once(system_prompt, user_prompt)
                return self._parse_json(raw_content)
            except json.JSONDecodeError:
                continue
            except Exception:
                return fallback
        return fallback

    def _parse_json(self, content: str) -> dict[str, object]:
        cleaned = content.strip()
        if cleaned.startswith("```"):
            lines = cleaned.splitlines()
            lines = lines[1:] if lines else lines
            if lines and lines[-1].strip().startswith("```"):
                lines = lines[:-1]
            cleaned = "\n".join(lines)
        return json.loads(cleaned)

    def _format_sources(self, request: ReconciliationRequest) -> str:
        lines: list[str] = []
        for index, source in enumerate(request.sources, start=1):
            lines.append(
                (
                    f"{index}. system={source.system}; medication={source.medication}; "
                    f"last_updated={source.last_updated}; last_filled={source.last_filled}; "
                    f"source_reliability={source.source_reliability}"
                )
            )
        return "\n".join(lines)

    def _reconciliation_fallback(self, reason: str) -> dict[str, object]:
        return ReconciliationResponse(
            reconciled_medication="Unable to reconcile",
            confidence_score=0.0,
            reasoning=f"Fallback response due to provider failure: {reason}.",
            recommended_actions=[
                "Review medication list manually with all source systems",
                "Escalate to clinical pharmacist for adjudication",
            ],
            clinical_safety_check="WARNING",
        ).model_dump()

    def _data_quality_fallback(self, reason: str) -> dict[str, object]:
        return DataQualityResponse(
            overall_score=0,
            breakdown=QualityBreakdown(
                completeness=0,
                accuracy=0,
                timeliness=0,
                clinical_plausibility=0,
            ),
            issues_detected=[
                IssueDetected(
                    field="llm.provider",
                    issue=f"Fallback response due to provider failure: {reason}.",
                    severity="high",
                )
            ],
        ).model_dump()
