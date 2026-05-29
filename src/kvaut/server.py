"""HTTP server that runs inside the app-under-test process.

Started by the kvaut.run entry point. Exposes the widget tree for
inspection and interaction via a simple JSON HTTP API.
"""

import json
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

import kvaut.tree


logger = logging.getLogger(__name__)

PORT = 5155
HOST = "0.0.0.0"


class _Handler(BaseHTTPRequestHandler):
    """HTTP request handler for the kvaut server."""

    def log_message(self, fmt, *args):
        logger.debug("server: " + fmt % args)

    def _send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        return json.loads(raw)

    def do_GET(self):
        if self.path == "/ping":
            self._handle_ping()
        elif self.path == "/tree":
            self._handle_tree()
        else:
            self._send_json({"error": "not found"}, status=404)

    def do_POST(self):
        handlers = {
            "/find": self._handle_find,
            "/query": self._handle_query,
            "/click": self._handle_click,
            "/input_text": self._handle_input_text,
            "/get_text": self._handle_get_text,
            "/get_attributes": self._handle_get_attributes,
        }
        handler = handlers.get(self.path)
        if handler:
            handler()
        else:
            self._send_json({"error": "not found"}, status=404)

    def _handle_ping(self):
        import kivy.app
        app = kivy.app.App.get_running_app()
        if app is None or app.root is None:
            self._send_json({"status": "booting"}, status=503)
        else:
            self._send_json({"status": "ok"})

    def _handle_tree(self):
        try:
            root = _get_root_widget()
            data = kvaut.tree.serialize(root, recursive=True)
            self._send_json(data)
        except Exception as e:
            self._send_json({"error": str(e)}, status=500)

    def _handle_find(self):
        body = self._read_json()
        hidden = body.get("hidden", False)
        selectors = body.get("selectors", {})
        try:
            widget = kvaut.tree.find_widget(_get_root_widget(), selectors, hidden=hidden)
            if widget is None:
                self._send_json({"error": "not found"}, status=404)
            else:
                self._send_json({"id": widget.uid})
        except kvaut.tree.AmbiguousMatch as e:
            self._send_json({"error": str(e), "ids": [w.uid for w in e.matches]}, status=409)

    def _handle_query(self):
        body = self._read_json()
        hidden = body.get("hidden", False)
        selectors = body.get("selectors", {})
        widgets = kvaut.tree.query_widgets(_get_root_widget(), selectors, hidden=hidden)
        self._send_json({"ids": [w.uid for w in widgets]})

    def _handle_click(self):
        body = self._read_json()
        element_id = body.get("id")
        widget = kvaut.tree.find_by_uid(_get_root_widget(), element_id)
        if widget is None:
            self._send_json({"error": f"element {element_id} not found"}, status=404)
            return
        kvaut.tree.click_widget(widget)
        self._send_json({"clicked": True})

    def _handle_input_text(self):
        body = self._read_json()
        element_id = body.get("id")
        text = body.get("text", "")
        widget = kvaut.tree.find_by_uid(_get_root_widget(), element_id)
        if widget is None:
            self._send_json({"error": f"element {element_id} not found"}, status=404)
            return
        try:
            kvaut.tree.input_text(widget, text)
            self._send_json({"ok": True})
        except kvaut.tree.InvalidOperationError as e:
            self._send_json({"error": str(e)}, status=400)

    def _handle_get_text(self):
        body = self._read_json()
        element_id = body.get("id")
        widget = kvaut.tree.find_by_uid(_get_root_widget(), element_id)
        if widget is None:
            self._send_json({"error": f"element {element_id} not found"}, status=404)
            return
        text = getattr(widget, "text", "")
        self._send_json({"text": text})

    def _handle_get_attributes(self):
        body = self._read_json()
        element_id = body.get("id")
        names = body.get("names", [])
        widget = kvaut.tree.find_by_uid(_get_root_widget(), element_id)
        if widget is None:
            self._send_json({"error": f"element {element_id} not found"}, status=404)
            return
        attrs = {}
        for name in names:
            if hasattr(widget, name):
                val = getattr(widget, name)
                # Make JSON-safe
                if callable(val) or isinstance(val, type):
                    continue
                try:
                    json.dumps(val)
                    attrs[name] = val
                except (TypeError, ValueError):
                    attrs[name] = str(val)
        self._send_json(attrs)


def _get_root_widget():
    import kivy.app
    app = kivy.app.App.get_running_app()
    if app is None:
        raise RuntimeError("No Kivy app is running")
    return app.root


def start():
    """Start the kvaut HTTP server in a daemon thread."""
    logger.info("kvaut server starting on %s:%d", HOST, PORT)
    server = HTTPServer((HOST, PORT), _Handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
