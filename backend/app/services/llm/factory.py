from ...core.config import Settings
from .anthropic_provider import AnthropicProvider
from .base import LLMProvider
from .cache import CachedProvider
from .github_models import GitHubModelsProvider
from .mock import MockProvider
from .openai_provider import OpenAIProvider


def get_llm_provider(settings: Settings) -> LLMProvider:
    if settings.llm_mock_mode:
        return MockProvider()  # DO NOT cache mock responses

    # Real providers - wrap with caching
    if settings.llm_provider == "github_models":
        if not settings.github_token:
            raise ValueError("github_token is required for github_models provider")
        return CachedProvider(GitHubModelsProvider(settings))

    if settings.llm_provider == "anthropic":
        if not settings.anthropic_api_key:
            raise ValueError("anthropic_api_key is required for anthropic provider")
        return CachedProvider(AnthropicProvider(settings))

    if settings.llm_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("openai_api_key is required for openai provider")
        return CachedProvider(OpenAIProvider(settings))

    raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
