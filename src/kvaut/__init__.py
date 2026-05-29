"""kvaut - Automation for testing Kivy apps."""

from kvaut.client import Client
from kvaut.errors import KvautError, ElementNotFoundError, AmbiguousMatchError, ServerNotFoundError, InvalidOperationError

try:
    from kvaut._version import version as __version__
except ImportError:
    __version__ = "1.0.0"

__all__ = [
    "Client",
    "KvautError",
    "ElementNotFoundError",
    "AmbiguousMatchError",
    "ServerNotFoundError",
    "InvalidOperationError",
]
