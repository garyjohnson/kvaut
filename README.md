# kvaut

Automation for testing [Kivy](https://kivy.org) apps. Think Playwright, but for Kivy widgets.

## Requirements

- Python 3.10+
- Kivy 2.1+

## Getting Started

### No app modifications needed

Your Kivy app stays exactly as-is. kvaut handles the instrumentation automatically —
just point it at your app's module path and it takes care of the rest.

### Write a test

```python
import kvaut

client = kvaut.Client()
client.connect("my_app.main")

# Find a button and click it
btn = client.find(by_text="Save")
client.click(btn)

# Find a TextInput and type into it
input_field = client.find(by_type="TextInput")
client.input_text(input_field, "Hello Kivy")

# Read text from a widget
text = client.get_text(input_field)
assert text == "Hello Kivy"

# Check widget attributes
attrs = client.get_attributes(btn, ["disabled", "text"])
assert attrs["disabled"] is False

client.disconnect()
```

### With pytest

kvaut provides an optional pytest fixture for automatic lifecycle management:

```python
import pytest
from kvaut.errors import ElementNotFoundError

@pytest.mark.app_module("my_app.main")
class TestApp:
    def test_save_button(self, kvaut_client):
        btn = kvaut_client.find(by_text="Save")
        kvaut_client.click(btn)
        text = kvaut_client.get_text(btn)
        assert text == "Saved!"

    def test_cancel_button(self, kvaut_client):
        with pytest.raises(ElementNotFoundError):
            kvaut_client.find(by_text="Nonexistent")
```

### Finding elements

kvaut uses an RTL-style approach: `find()` for a single element, `query()` for multiple.
Both return opaque element ids that you pass to actions like `click()` and `input_text()`.

`find()` raises an error if zero or more than one visible element matches.
`query()` returns a list — empty if nothing matches.

By default, only visible elements are searched. Pass `hidden=True` to include hidden elements
(size zero, opacity zero, or no parent).

```python
# Single element — raises if ambiguous
save_btn = client.find(by_text="Save")

# Multiple elements — returns a list
all_buttons = client.query(by_type="Button")
for btn_id in all_buttons:
    print(client.get_text(btn_id))

# Include hidden elements
hidden_btn = client.find(by_text="Hidden", hidden=True)

# Regex matching
import re
client.find(by_text=re.compile(r"^Save"))
```

## API Reference

### `kvaut.Client`

| Method | Description |
|---|---|
| `connect(module_path)` | Launch the app under test as a subprocess and wait for it to be ready |
| `disconnect()` | Stop the app under test |
| `find(*, by_text, by_type, by_id, hidden=False)` | Find a single visible element. Raises `ElementNotFoundError` if 0 matches, `AmbiguousMatchError` if >1 |
| `query(*, by_text, by_type, by_id, hidden=False)` | Find all matching elements. Returns a list (empty if none) |
| `click(element_id)` | Tap the center of an element |
| `input_text(element_id, text)` | Type text into a TextInput element. Raises `InvalidOperationError` if not a TextInput |
| `get_text(element_id)` | Get the `text` property of an element |
| `get_attributes(element_id, names)` | Get named widget attributes as a dict, e.g. `["disabled", "enabled"]` |
| `tree()` | Return the full widget tree as a dict (for debugging) |

### Selectors

- **`by_text`** — Match by widget text. Pass a string for exact match or a compiled `re.Pattern` for regex.
- **`by_type`** — Match by widget class name, e.g. `"Button"`, `"TextInput"`.
- **`by_id`** — Match by the kv lang `id` attribute.

### Exceptions

All exceptions inherit from `kvaut.KvautError`:

- `ElementNotFoundError` — `find()` matched 0 elements, or element id is stale
- `AmbiguousMatchError` — `find()` matched >1 element
- `ServerNotFoundError` — Server couldn't be reached or timed out on connect
- `InvalidOperationError` — Operation on wrong widget type (e.g. `input_text` on a Button)

## How it works

kvaut uses a client/server architecture:

1. **`client.connect("my_app.main")`** spawns a subprocess running `python -m kvaut.run my_app.main`
2. **kvaut.run** starts an HTTP server (stdlib, no dependencies) in a background thread, imports the user's app module, finds the `App` subclass, and calls `App().run()`
3. The **test side** communicates with the server over HTTP — finding widgets, dispatching taps, reading properties
4. **`client.disconnect()`** kills the subprocess

Your app code never imports kvaut. There is no instrumentation step. The `kvaut.run` entry point
handles everything transparently.

## Running tests

```bash
pip install -e ".[dev]"
pytest
```

For headless environments (CI), use xvfb:

```bash
xvfb-run -a pytest
```

Set `KVAUT_LOG=DEBUG` for verbose server output during debugging.

## Contributing

See [CONTEXT.md](CONTEXT.md) for the project glossary and [docs/adr/](docs/adr/) for architecture
decisions.
