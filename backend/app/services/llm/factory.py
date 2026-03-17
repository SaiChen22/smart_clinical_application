from ...core.config import Settings
from .base import LLMProvider
from .mock import MockProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    if settings.llm_mock_mode:
        return MockProvider()

    if settings.llm_provider == "github_models":
        raise NotImplementedError("GitHub Models provider not yet implemented")

    if settings.llm_provider == "anthropic":
        raise NotImplementedError("Anthropic provider not yet implemented")

    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
