from fastapi import APIRouter, Depends

from ...core.config import Settings, get_settings
from ...core.security import verify_api_key
from ...schemas.data_quality import DataQualityRequest, DataQualityResponse
from ...services.data_quality import DataQualityService
from ...services.llm.base import LLMProvider
from ...services.llm.factory import get_llm_provider

router = APIRouter(prefix="/api/data-quality", tags=["data-quality"])


@router.post("/validate", dependencies=[Depends(verify_api_key)])
async def validate_data_quality(
    request: DataQualityRequest,
    settings: Settings = Depends(get_settings),
) -> DataQualityResponse:
    llm_provider: LLMProvider = get_llm_provider(settings)
    service = DataQualityService()
    return await service.assess(request, llm_provider)
