"""Integration tests for the kvaut client and server.

These tests launch real Kivy test apps and interact with them through
the kvaut Client. Requires a display (use SDL_VIDEODRIVER=dummy).
"""

import re
import pytest

import kvaut
from kvaut.errors import ElementNotFoundError, AmbiguousMatchError, InvalidOperationError

pytestmark = pytest.mark.integration


@pytest.mark.app_module("tests.test_apps.button_app")
class TestButtonApp:
    def test_find_button_by_text(self, kvaut_client):
        btn_id = kvaut_client.find(by_text="Hello world")
        assert isinstance(btn_id, int)

    def test_click_button_changes_text(self, kvaut_client):
        btn_id = kvaut_client.find(by_text="Hello world")
        kvaut_client.click(btn_id)
        # After click, text should change to "Howdy"
        text = kvaut_client.get_text(btn_id)
        assert text == "Howdy"

    def test_find_nonexistent_raises(self, kvaut_client):
        with pytest.raises(ElementNotFoundError):
            kvaut_client.find(by_text="Nonexistent")

    def test_get_text(self, kvaut_client):
        btn_id = kvaut_client.find(by_text="Hello world")
        text = kvaut_client.get_text(btn_id)
        assert text == "Hello world"

    def test_get_attributes(self, kvaut_client):
        btn_id = kvaut_client.find(by_text="Hello world")
        attrs = kvaut_client.get_attributes(btn_id, ["text", "disabled"])
        assert attrs["text"] == "Hello world"


@pytest.mark.app_module("tests.test_apps.input_app")
class TestInputApp:
    def test_find_by_type(self, kvaut_client):
        ti_id = kvaut_client.find(by_type="TextInput")
        assert isinstance(ti_id, int)

    def test_input_text(self, kvaut_client):
        ti_id = kvaut_client.find(by_type="TextInput")
        kvaut_client.input_text(ti_id, "Hello Kivy")
        text = kvaut_client.get_text(ti_id)
        assert text == "Hello Kivy"

    def test_find_by_id(self, kvaut_client):
        ti_id = kvaut_client.find(by_id="name_input")
        text = kvaut_client.get_text(ti_id)
        assert text == ""

    def test_query_returns_list(self, kvaut_client):
        ids = kvaut_client.query(by_type="Label")
        assert len(ids) == 1

    def test_tree_debug(self, kvaut_client):
        tree = kvaut_client.tree()
        assert "type" in tree
        assert "children" in tree


@pytest.mark.app_module("tests.test_apps.ambiguous_app")
class TestAmbiguousApp:
    def test_find_raises_ambiguous(self, kvaut_client):
        with pytest.raises(AmbiguousMatchError):
            kvaut_client.find(by_text="Duplicate")

    def test_query_returns_both(self, kvaut_client):
        ids = kvaut_client.query(by_text="Duplicate")
        assert len(ids) == 2

    def test_find_by_id_is_unambiguous(self, kvaut_client):
        btn_id = kvaut_client.find(by_id="btn1")
        text = kvaut_client.get_text(btn_id)
        assert text == "Duplicate"


@pytest.mark.app_module("tests.test_apps.hidden_app")
class TestHiddenApp:
    def test_hidden_element_not_found(self, kvaut_client):
        with pytest.raises(ElementNotFoundError):
            kvaut_client.find(by_text="Hidden")

    def test_hidden_element_found_with_flag(self, kvaut_client):
        btn_id = kvaut_client.find(by_text="Hidden", hidden=True)
        text = kvaut_client.get_text(btn_id)
        assert text == "Hidden"

    def test_visible_element_still_found(self, kvaut_client):
        btn_id = kvaut_client.find(by_text="Visible")
        text = kvaut_client.get_text(btn_id)
        assert text == "Visible"


@pytest.mark.app_module("tests.test_apps.id_app")
class TestIdApp:
    def test_find_by_kv_id(self, kvaut_client):
        label_id = kvaut_client.find(by_id="my_label")
        text = kvaut_client.get_text(label_id)
        assert text == "Label Text"

    def test_find_by_text(self, kvaut_client):
        label_id = kvaut_client.find(by_text="Label Text")
        assert isinstance(label_id, int)
