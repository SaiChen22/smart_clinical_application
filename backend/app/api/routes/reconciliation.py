from fastapi import APIRouter, Depends

from ...core.config import Settings, get_settings
from ...core.security import verify_api_key
from ...schemas.reconciliation import ReconciliationRequest, ReconciliationResponse
from ...services.llm.base import LLMProvider
from ...services.llm.factory import get_llm_provider
from ...services.reconciliation import ReconciliationService

router = APIRouter(prefix="/api/reconcile", tags=["reconciliation"])


@router.post("/medication", dependencies=[Depends(verify_api_key)])
async def reconcile_medication(
    request: ReconciliationRequest,
    settings: Settings = Depends(get_settings),
) -> ReconciliationResponse:
    llm_provider: LLMProvider = get_llm_provider(settings)
    service = ReconciliationService()
    return await service.reconcile(request, llm_provider)
