"""Unit tests for the Client class (no Kivy required)."""

import pytest

import kvaut
from kvaut.errors import ElementNotFoundError, AmbiguousMatchError


class TestClientErrors:
    def test_error_hierarchy(self):
        assert issubclass(ElementNotFoundError, kvaut.errors.KvautError)
        assert issubclass(AmbiguousMatchError, kvaut.errors.KvautError)
        assert issubclass(kvaut.errors.ServerNotFoundError, kvaut.errors.KvautError)
        assert issubclass(kvaut.errors.InvalidOperationError, kvaut.errors.KvautError)
