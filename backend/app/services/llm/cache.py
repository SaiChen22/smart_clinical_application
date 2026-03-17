"""LLM response caching service for Clinical Data Reconciliation Engine."""

import hashlib
import json
import logging
from datetime import datetime, timedelta

from sqlmodel import Session, select

from ...core.database import engine
from ...models.cache import LLMCache
from ...schemas.data_quality import DataQualityRequest, DataQualityResponse
from ...schemas.reconciliation import ReconciliationRequest, ReconciliationResponse
from .base import LLMProvider

logger = logging.getLogger(__name__)


class LLMCacheService:
    """Service for caching LLM responses with TTL support."""

    def _hash_request(self, provider: str, request_data: dict) -> str:
        """Generate SHA256 hash of provider + request data.
        
        Args:
            provider: LLM provider name
            request_data: Request payload dictionary
            
        Returns:
            SHA256 hash as hexadecimal string
        """
        cache_key = f"{provider}:{json.dumps(request_data, sort_keys=True)}"
        return hashlib.sha256(cache_key.encode()).hexdigest()

    def get_cached(self, provider: str, request_data: dict) -> str | None:
        """Retrieve cached response if exists and not expired.
        
        Args:
            provider: LLM provider name
            request_data: Request payload dictionary
            
        Returns:
            Cached response JSON string or None if not found/expired
        """
        prompt_hash = self._hash_request(provider, request_data)
        with Session(engine) as session:
            statement = select(LLMCache).where(LLMCache.prompt_hash == prompt_hash)
            cache_entry = session.exec(statement).first()

            if not cache_entry:
                return None

            # Check TTL
            expiry_time = cache_entry.created_at + timedelta(seconds=cache_entry.ttl_seconds)
            if datetime.utcnow() > expiry_time:
                # Expired - delete and return None
                session.delete(cache_entry)
                session.commit()
                return None

            return cache_entry.response_json

    def set_cached(
        self, provider: str, request_data: dict, response_json: str, ttl: int = 3600
    ):
        """Store response in cache with TTL.
        
        Args:
            provider: LLM provider name
            request_data: Request payload dictionary
            response_json: Response JSON string to cache
            ttl: Time-to-live in seconds (default: 3600 = 1 hour)
        """
        prompt_hash = self._hash_request(provider, request_data)
        with Session(engine) as session:
            cache_entry = LLMCache(
                prompt_hash=prompt_hash,
                response_json=response_json,
                provider=provider,
                created_at=datetime.utcnow(),
                ttl_seconds=ttl,
            )
            session.add(cache_entry)
            session.commit()

    def clear_expired(self) -> int:
        """Delete all expired cache entries.
        
        Returns:
            Number of entries deleted
        """
        with Session(engine) as session:
            now = datetime.utcnow()
            statement = select(LLMCache)
            all_entries = session.exec(statement).all()
            deleted = 0
            for entry in all_entries:
                expiry_time = entry.created_at + timedelta(seconds=entry.ttl_seconds)
                if now > expiry_time:
                    session.delete(entry)
                    deleted += 1
            session.commit()
            return deleted


class CachedProvider(LLMProvider):
    """Wrapper for LLM providers that adds caching support.
    
    This wrapper intercepts calls to the underlying LLM provider,
    checks the cache first, and only calls the real provider on cache miss.
    """

    def __init__(self, underlying: LLMProvider):
        """Initialize cached provider wrapper.
        
        Args:
            underlying: The real LLM provider to wrap
        """
        self._provider = underlying
        self._cache = LLMCacheService()

    @property
    def provider_name(self) -> str:
        """Return provider name with 'cached-' prefix."""
        return f"cached-{self._provider.provider_name}"

    async def reconcile_medications(
        self, request: ReconciliationRequest
    ) -> ReconciliationResponse:
        """Reconcile medications with caching support.
        
        Args:
            request: Reconciliation request
            
        Returns:
            Reconciliation response (from cache or real provider)
        """
        request_dict = request.model_dump()
        cached = self._cache.get_cached(self._provider.provider_name, request_dict)

        if cached:
            # Cache hit
            logger.info(f"Cache HIT for {self._provider.provider_name} reconciliation")
            return ReconciliationResponse(**json.loads(cached))

        # Cache miss - call real provider
        logger.info(f"Cache MISS for {self._provider.provider_name} reconciliation")
        response = await self._provider.reconcile_medications(request)
        self._cache.set_cached(
            self._provider.provider_name, request_dict, response.model_dump_json()
        )
        return response

    async def assess_data_quality(
        self, request: DataQualityRequest
    ) -> DataQualityResponse:
        """Assess data quality with caching support.
        
        Args:
            request: Data quality request
            
        Returns:
            Data quality response (from cache or real provider)
        """
        request_dict = request.model_dump()
        cached = self._cache.get_cached(self._provider.provider_name, request_dict)

        if cached:
            # Cache hit
            logger.info(f"Cache HIT for {self._provider.provider_name} data quality")
            return DataQualityResponse(**json.loads(cached))

        # Cache miss - call real provider
        logger.info(f"Cache MISS for {self._provider.provider_name} data quality")
        response = await self._provider.assess_data_quality(request)
        self._cache.set_cached(
            self._provider.provider_name, request_dict, response.model_dump_json()
        )
        return response
