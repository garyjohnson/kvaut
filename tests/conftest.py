"""Pytest fixtures for kvaut.

Provides a `kvaut_client` fixture that launches and tears down
a fresh app under test for each test function.
"""

import pytest

import kvaut


@pytest.fixture
def kvaut_client(request):
    """Create a kvaut Client connected to a fresh app under test.

    Use the `app_module` marker to specify which app to launch:

        @pytest.mark.app_module("tests.test_apps.button_app")
        def test_click(kvaut_client):
            btn = kvaut_client.find(by_text="Hello world")
            kvaut_client.click(btn)
    """
    marker = request.node.get_closest_marker("app_module")
    if marker is None:
        raise pytest.UsageError(
            "kvaut_client fixture requires @pytest.mark.app_module('module.path') "
            "on the test function or class."
        )
    app_module = marker.args[0]
    client = kvaut.Client()
    client.connect(app_module)
    yield client
    client.disconnect()
