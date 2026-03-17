from abc import ABC, abstractmethod

from ...schemas.data_quality import DataQualityRequest, DataQualityResponse
from ...schemas.reconciliation import ReconciliationRequest, ReconciliationResponse


class LLMProvider(ABC):
    @abstractmethod
    async def reconcile_medications(
        self, request: ReconciliationRequest
    ) -> ReconciliationResponse:
        raise NotImplementedError

    @abstractmethod
    async def assess_data_quality(
        self, request: DataQualityRequest
    ) -> DataQualityResponse:
        raise NotImplementedError

    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError
