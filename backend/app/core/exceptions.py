"""Custom exception classes for Clinical Data Reconciliation Engine."""


class ReconciliationError(Exception):
    """Base exception for reconciliation-related errors."""
    
    def __init__(self, message: str, code: str = "RECONCILIATION_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class DataQualityError(Exception):
    """Exception for data quality assessment errors."""
    
    def __init__(self, message: str, code: str = "DATA_QUALITY_ERROR"):
        self.message = message
        self.code = code
        super().__init__(message)


class RateLimitError(Exception):
    """Exception for rate limiting errors."""
    
    def __init__(self, message: str, retry_after: int = 60):
        self.message = message
        self.code = "RATE_LIMIT_EXCEEDED"
        self.retry_after = retry_after
        super().__init__(message)


class LLMTimeoutError(Exception):
    """Exception for LLM request timeout errors."""
    
    def __init__(self, message: str, retry_after: int = 30):
        self.message = message
        self.code = "LLM_TIMEOUT"
        self.retry_after = retry_after
        super().__init__(message)
