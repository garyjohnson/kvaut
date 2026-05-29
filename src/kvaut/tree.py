"""Widget tree introspection and manipulation.

Runs inside the app-under-test process. Handles widget traversal,
matching, serialization, and simulated input events.
"""

from __future__ import annotations

import re
import logging
from typing import Any

from kivy.app import App
from kivy.input.motionevent import MotionEvent
from kivy.uix.textinput import TextInput


logger = logging.getLogger(__name__)


class AmbiguousMatch(Exception):
    def __init__(self, message: str, matches: list):
        super().__init__(message)
        self.matches = matches


class InvalidOperationError(Exception):
    pass


# --- Visibility ---

def is_visible(widget) -> bool:
    """A widget is visible if it has non-zero size, positive opacity, and a parent."""
    if widget is None:
        return False
    return (
        widget.width > 0
        and widget.height > 0
        and widget.opacity > 0
        and widget.parent is not None
    )


# --- Widget matching ---

def _match_by_type(widget, type_name: str) -> bool:
    return widget.__class__.__name__ == type_name


def _match_by_id(widget, kv_id: str) -> bool:
    return getattr(widget, "id", None) == kv_id


def _match_by_text(widget, text) -> bool:
    widget_text = getattr(widget, "text", None)
    if widget_text is None:
        return False
    if isinstance(text, re.Pattern):
        return bool(text.search(str(widget_text)))
    return str(widget_text) == str(text)


def _widget_matches(widget, selectors: dict[str, Any]) -> bool:
    matchers = {
        "by_type": _match_by_type,
        "by_id": _match_by_id,
        "by_text": _match_by_text,
    }
    for key, value in selectors.items():
        matcher = matchers.get(key)
        if matcher is None:
            continue
        if not matcher(widget, value):
            return False
    return True


# --- Tree traversal ---

def find_widget(root, selectors: dict[str, Any], *, hidden: bool = False):
    """Find a single widget matching selectors.

    Raises AmbiguousMatch if more than one widget matches.
    Returns None if no match.
    """
    matches = _collect_matches(root, selectors, hidden=hidden)
    if len(matches) == 0:
        return None
    if len(matches) > 1:
        raise AmbiguousMatch(
            f"Found {len(matches)} elements matching {selectors}",
            matches,
        )
    return matches[0]


def query_widgets(root, selectors: dict[str, Any], *, hidden: bool = False) -> list:
    """Find all widgets matching selectors."""
    return _collect_matches(root, selectors, hidden=hidden)


def _collect_matches(root, selectors: dict[str, Any], *, hidden: bool = False) -> list:
    matches = []
    _traverse(root, selectors, hidden, matches)
    return matches


def _traverse(widget, selectors: dict[str, Any], hidden: bool, matches: list):
    if widget is None:
        return
    if hidden or is_visible(widget):
        if _widget_matches(widget, selectors):
            matches.append(widget)
    for child in getattr(widget, "children", []) or []:
        _traverse(child, selectors, hidden, matches)


def find_by_uid(root, uid: int):
    """Find a widget by its internal uid."""
    return _find_by_uid_recursive(root, uid)


def _find_by_uid_recursive(widget, uid: int):
    if widget is None:
        return None
    if widget.uid == uid:
        return widget
    for child in getattr(widget, "children", []) or []:
        result = _find_by_uid_recursive(child, uid)
        if result is not None:
            return result
    return None


# --- Serialization ---

def serialize(widget, *, recursive: bool = False) -> dict:
    x, y = _global_center(widget)
    data = {
        "type": widget.__class__.__name__,
        "id": widget.uid,
        "kv_id": getattr(widget, "id", None),
        "text": getattr(widget, "text", None),
        "visible": is_visible(widget),
        "enabled": getattr(widget, "disabled", True) is False,
        "global_position": {"x": x, "y": y},
    }
    if recursive:
        children = getattr(widget, "children", []) or []
        data["children"] = [serialize(c, recursive=True) for c in children]
    return data


def _global_center(widget):
    try:
        pos = widget.to_window(widget.center_x, widget.center_y)
        return pos[0], pos[1]
    except Exception:
        return 0, 0


# --- Actions ---

import threading

from kivy.clock import Clock


def click_widget(widget):
    """Simulate a tap on the center of the widget."""
    done = threading.Event()
    error = []

    def _do_click(dt):
        try:
            _dispatch_tap(widget)
        except Exception as e:
            error.append(e)
        finally:
            done.set()

    Clock.schedule_once(_do_click, 0)
    if not done.wait(timeout=5):
        raise RuntimeError("Timed out waiting for tap to dispatch")
    if error:
        raise error[0]


def _dispatch_tap(widget):
    app = App.get_running_app()
    if app.root is None:
        raise RuntimeError("App root is None")
    global_x, global_y = _global_center(widget)
    touch = _FakeMotionEvent("fake", 1, {"x": global_x, "y": global_y})

    # Dispatch through the root widget so collision detection works.
    # Coordinates must be absolute window coordinates.
    app.root.dispatch('on_touch_down', touch)
    app.root.dispatch('on_touch_up', touch)


def input_text(widget, text: str):
    """Set text on a TextInput widget."""
    if not isinstance(widget, TextInput):
        raise InvalidOperationError(
            f"input_text requires a TextInput widget, got {widget.__class__.__name__}"
        )
    done = threading.Event()
    error = []

    def _do_set(dt):
        try:
            widget.text = str(text)
        except Exception as e:
            error.append(e)
        finally:
            done.set()

    Clock.schedule_once(_do_set, 0)
    if not done.wait(timeout=5):
        raise RuntimeError("Timed out waiting for text input to dispatch")
    if error:
        raise error[0]


# --- Fake motion event ---

class _FakeMotionEvent(MotionEvent):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('is_touch', True)
        kwargs.setdefault('type_id', 'touch')
        super().__init__(*args, **kwargs)
        self.profile = ['pos']

    def depack(self, args):
        self.sx = args['x']
        self.sy = args['y']
        super().depack(args)
        # Explicitly set pos from sx, sy (Kivy's MotionEvent computes this
        # from the window transform, but for fake events we set directly)
        self.x = args['x']
        self.y = args['y']
