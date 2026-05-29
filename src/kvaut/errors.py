"""Error types for kvaut."""


class KvautError(Exception):
    """Base exception for all kvaut-specific errors."""


class ServerNotFoundError(KvautError):
    """Raised when the kvaut server cannot be reached."""


class ElementNotFoundError(KvautError):
    """Raised when find() matches zero elements."""


class AmbiguousMatchError(KvautError):
    """Raised when find() matches more than one element."""


class InvalidOperationError(KvautError):
    """Raised when an operation is called on an incompatible widget type."""
