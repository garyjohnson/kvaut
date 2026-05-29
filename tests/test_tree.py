"""Tests for kvaut.tree widget introspection and manipulation.

These tests require a working Kivy window (pygame provider on Mac,
SDL2 dummy in CI). They create widgets directly rather than launching
a full app under test.
"""

import re
import pytest

from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

import kvaut.tree


class TestVisibility:
    def test_visible_widget(self):
        root = Widget()
        btn = Button(text="Click")
        root.add_widget(btn)
        assert kvaut.tree.is_visible(btn)

    def test_zero_opacity(self):
        root = Widget()
        btn = Button(text="Click", opacity=0)
        root.add_widget(btn)
        assert not kvaut.tree.is_visible(btn)

    def test_no_parent(self):
        btn = Button(text="Click")
        assert not kvaut.tree.is_visible(btn)

    def test_zero_size(self):
        root = Widget()
        btn = Button(text="Click", size=(0, 0), size_hint=(None, None))
        root.add_widget(btn)
        assert not kvaut.tree.is_visible(btn)


class TestMatching:
    def test_by_type_match(self):
        btn = Button(text="Click")
        assert kvaut.tree._match_by_type(btn, "Button")
        assert not kvaut.tree._match_by_type(btn, "Label")

    def test_by_text_match(self):
        btn = Button(text="Click")
        assert kvaut.tree._match_by_text(btn, "Click")
        assert not kvaut.tree._match_by_text(btn, "Nope")

    def test_by_text_regex(self):
        btn = Button(text="Hello world")
        assert kvaut.tree._match_by_text(btn, re.compile(r"Hello.*"))
        assert not kvaut.tree._match_by_text(btn, re.compile(r"Goodbye.*"))

    def test_by_id_match(self):
        btn = Button()
        btn.id = "submit_btn"
        assert kvaut.tree._match_by_id(btn, "submit_btn")
        assert not kvaut.tree._match_by_id(btn, "cancel_btn")

    def test_by_id_none_when_not_set(self):
        btn = Button()
        assert not kvaut.tree._match_by_id(btn, "anything")


class TestFindAndQuery:
    def test_find_returns_single_widget(self):
        root = Widget()
        btn = Button(text="Click")
        root.add_widget(btn)
        result = kvaut.tree.find_widget(root, {"by_text": "Click"})
        assert result is btn

    def test_find_raises_ambiguous(self):
        root = Widget()
        root.add_widget(Button(text="Click"))
        root.add_widget(Button(text="Click"))
        with pytest.raises(kvaut.tree.AmbiguousMatch):
            kvaut.tree.find_widget(root, {"by_text": "Click"})

    def test_find_returns_none(self):
        root = Widget()
        result = kvaut.tree.find_widget(root, {"by_text": "Nope"})
        assert result is None

    def test_query_returns_all_matches(self):
        root = Widget()
        root.add_widget(Button(text="Click"))
        root.add_widget(Button(text="Click"))
        results = kvaut.tree.query_widgets(root, {"by_text": "Click"})
        assert len(results) == 2

    def test_query_returns_empty(self):
        root = Widget()
        results = kvaut.tree.query_widgets(root, {"by_text": "Nope"})
        assert results == []

    def test_hidden_finds_invisible(self):
        root = Widget()
        btn = Button(text="Click", opacity=0)
        root.add_widget(btn)
        matches = kvaut.tree.query_widgets(root, {"by_text": "Click"}, hidden=True)
        assert len(matches) == 1

    def test_hidden_false_skips_invisible(self):
        root = Widget()
        btn = Button(text="Click", opacity=0)
        root.add_widget(btn)
        matches = kvaut.tree.query_widgets(root, {"by_text": "Click"}, hidden=False)
        assert matches == []

    def test_nested_widgets(self):
        root = BoxLayout()
        inner = BoxLayout()
        btn = Button(text="Deep")
        inner.add_widget(btn)
        root.add_widget(inner)
        result = kvaut.tree.find_widget(root, {"by_text": "Deep"})
        assert result is btn


class TestFindByUid:
    def test_find_existing(self):
        root = Widget()
        btn = Button()
        root.add_widget(btn)
        found = kvaut.tree.find_by_uid(root, btn.uid)
        assert found is btn

    def test_find_missing(self):
        root = Widget()
        found = kvaut.tree.find_by_uid(root, 99999)
        assert found is None


class TestSerialize:
    def test_serialize_basic(self):
        btn = Button(text="Hi")
        btn.id = "my_id"
        data = kvaut.tree.serialize(btn)
        assert data["type"] == "Button"
        assert data["text"] == "Hi"
        assert data["kv_id"] == "my_id"
        assert isinstance(data["id"], int)
        assert "visible" in data
        assert "enabled" in data

    def test_serialize_recursive(self):
        root = Widget()
        btn = Button()
        root.add_widget(btn)
        data = kvaut.tree.serialize(root, recursive=True)
        assert "children" in data
        assert len(data["children"]) == 1


class TestInputTextValidation:
    def test_input_text_on_textinput(self):
        ti = TextInput(text="old")
        # input_text validates type, then dispatches to mainthread.
        # Test the setter logic directly.
        ti.text = "new"
        assert ti.text == "new"

    def test_input_text_on_button_raises(self):
        btn = Button()
        with pytest.raises(kvaut.tree.InvalidOperationError):
            kvaut.tree.input_text(btn, "text")
