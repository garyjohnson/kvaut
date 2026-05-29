"""Client for the kvaut automation server.

Talks to the kvaut server over HTTP to find widgets, send interactions,
and retrieve widget state. Test-runner-agnostic — works with any
Python test framework.
"""

from __future__ import annotations

import json
import logging
import re
import subprocess
import sys
import time
import urllib.request
import urllib.error
from typing import Any

import kvaut.errors


logger = logging.getLogger(__name__)

SERVER_URL = "http://0.0.0.0:5155"
CONNECT_TIMEOUT = 15
REQUEST_TIMEOUT = 5
POLL_INTERVAL = 0.25


class Client:
    """Client for interacting with a Kivy app under test via the kvaut server."""

    def __init__(self):
        self._process: subprocess.Popen | None = None

    def connect(self, app_module: str):
        """Launch the app under test and wait for the server to be ready.

        Args:
            app_module: Dotted Python module path of the app, e.g. "my_app.main".
        """
        self._process = subprocess.Popen(
            [sys.executable, "-m", "kvaut.run", app_module],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self._wait_for_server()

    def disconnect(self):
        """Stop the app under test."""
        if self._process:
            self._process.kill()
            self._process.wait()
            self._process = None

    # --- Finding elements ---

    def find(self, *, by_text: str | re.Pattern | None = None,
             by_type: str | None = None, by_id: str | None = None,
             hidden: bool = False) -> int:
        """Find a single visible element matching the given selectors.

        Raises ElementNotFoundError if no match, AmbiguousMatchError if >1 match.

        Args:
            by_text: Match by widget text (exact string or compiled regex).
            by_type: Match by widget class name, e.g. "Button".
            by_id: Match by kv lang id attribute.
            hidden: If True, include non-visible widgets.

        Returns:
            Element id (int).
        """
        ids = self._query(by_text=by_text, by_type=by_type, by_id=by_id, hidden=hidden)
        if len(ids) == 0:
            raise kvaut.errors.ElementNotFoundError(
                f"No element found matching selectors"
            )
        if len(ids) > 1:
            raise kvaut.errors.AmbiguousMatchError(
                f"Found {len(ids)} elements matching selectors"
            )
        return ids[0]

    def query(self, *, by_text: str | re.Pattern | None = None,
              by_type: str | None = None, by_id: str | None = None,
              hidden: bool = False) -> list[int]:
        """Find all elements matching the given selectors.

        Returns an empty list if none match.

        Args:
            by_text: Match by widget text (exact string or compiled regex).
            by_type: Match by widget class name, e.g. "Button".
            by_id: Match by kv lang id attribute.
            hidden: If True, include non-visible widgets.

        Returns:
            List of element ids.
        """
        return self._query(by_text=by_text, by_type=by_type, by_id=by_id, hidden=hidden)

    # --- Actions ---

    def click(self, element_id: int):
        """Tap the center of the element."""
        self._post("/click", {"id": element_id})

    def input_text(self, element_id: int, text: str):
        """Type text into a TextInput element.

        Raises InvalidOperationError if the element is not a TextInput.
        """
        self._post("/input_text", {"id": element_id, "text": str(text)})

    # --- Reading state ---

    def get_text(self, element_id: int) -> str:
        """Get the text property of an element."""
        data = self._post("/get_text", {"id": element_id})
        return data.get("text", "")

    def get_attributes(self, element_id: int, names: list[str]) -> dict[str, Any]:
        """Get named attributes from an element.

        Args:
            element_id: Element id.
            names: List of attribute names to fetch.

        Returns:
            Dict mapping attribute names to their values.
        """
        data = self._post("/get_attributes", {"id": element_id, "names": names})
        return data

    # --- Debugging ---

    def tree(self) -> dict:
        """Return the full widget tree as a dict. For debugging."""
        return self._get("/tree")

    # --- Internal ---

    def _query(self, **kwargs) -> list[int]:
        selectors = _build_selectors(kwargs)
        hidden = kwargs.get("hidden", False)
        data = self._post("/query", {"selectors": selectors, "hidden": hidden})
        result = data.get("ids", [])
        if isinstance(result, list):
            return [int(i) for i in result]
        return []

    def _get(self, path: str) -> dict:
        url = f"{SERVER_URL}{path}"
        try:
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.URLError as e:
            raise kvaut.errors.ServerNotFoundError(f"Server unreachable: {e}")

    def _post(self, path: str, body: dict) -> dict:
        url = f"{SERVER_URL}{path}"
        try:
            data = json.dumps(body).encode("utf-8")
            req = urllib.request.Request(
                url, data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if "error" in result:
                    self._raise_error(result, resp.status)
                return result
        except urllib.error.HTTPError as e:
            try:
                body = json.loads(e.read().decode("utf-8"))
                self._raise_error(body, e.code)
            except json.JSONDecodeError:
                raise kvaut.errors.ServerNotFoundError(f"Server error: {e}")
        except urllib.error.URLError as e:
            raise kvaut.errors.ServerNotFoundError(f"Server unreachable: {e}")

    def _raise_error(self, body: dict, status: int):
        msg = body.get("error", "Unknown error")
        if status == 404:
            raise kvaut.errors.ElementNotFoundError(msg)
        elif status == 409:
            raise kvaut.errors.AmbiguousMatchError(msg)
        elif status == 400:
            raise kvaut.errors.InvalidOperationError(msg)
        else:
            raise kvaut.errors.KvautError(msg)

    def _wait_for_server(self):
        deadline = time.time() + CONNECT_TIMEOUT
        while time.time() < deadline:
            try:
                data = self._get("/ping")
                if data.get("status") == "ok":
                    return
            except kvaut.errors.ServerNotFoundError:
                pass
            time.sleep(POLL_INTERVAL)
        raise kvaut.errors.ServerNotFoundError(
            f"Timed out waiting for kvaut server after {CONNECT_TIMEOUT}s"
        )


def _build_selectors(kwargs: dict) -> dict:
    selectors = {}
    for key in ("by_text", "by_type", "by_id"):
        value = kwargs.get(key)
        if value is not None:
            if key == "by_text" and isinstance(value, re.Pattern):
                selectors[key] = {"pattern": value.pattern, "flags": value.flags}
            else:
                selectors[key] = value
    return selectors
