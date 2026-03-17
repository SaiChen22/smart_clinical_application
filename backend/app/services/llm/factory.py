from ...core.config import Settings
from .base import LLMProvider
from .cache import CachedProvider
from .mock import MockProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    if settings.llm_mock_mode:
        return MockProvider()  # DO NOT cache mock responses

    # Real providers - wrap with caching
    if settings.llm_provider == "github_models":
        # base_provider = GitHubModelsProvider(settings)  # Task 12
        # return CachedProvider(base_provider)
        raise NotImplementedError("GitHub Models provider not yet implemented")

    if settings.llm_provider == "anthropic":
        # base_provider = AnthropicProvider(settings)  # Task 12
        # return CachedProvider(base_provider)
        raise NotImplementedError("Anthropic provider not yet implemented")

    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
