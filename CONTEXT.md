# kvaut

A library for automating Kivy application testing, providing a Playwright-style API for finding, interacting with, and asserting on Kivy widgets from a test process.

## Language

**App under test**: The Kivy application being tested. It runs in its own process, launched by the kvaut launch mechanism. The app under test requires no modifications — kvaut injects instrumentation at launch time.
_Avoid_: Target app, test subject, instrumented app

**kvaut server**: The HTTP server that runs inside the app-under-test process, exposing the widget tree for inspection and interaction. Started automatically by kvaut's launcher; never configured manually by the user.
_Avoid_: Automation server, Bottle server, widget server

**kvaut client / test side**: The process where the user writes their test code. Talks to the kvaut server over HTTP to find widgets, send interactions, and make assertions. Test-runner-agnostic — works with pytest, unittest, or any Python test framework.
_Avoid_: Test harness, BDD layer

**find**: Locates a single widget matching the given criteria. Raises if zero or more than one visible widget matches. By default only searches visible widgets; pass `hidden=True` to include non-visible widgets.
_Avoid_: locate, get, select, pick

**query**: Locates all widgets matching the given criteria. Returns a list — empty list if none match. By default only searches visible widgets; pass `hidden=True` to include non-visible widgets.
_Avoid_: find_all, locate_all, select_all

**Selector**: A set of `by_*` keyword arguments passed to `find` or `query`. Supported selectors: `by_text` (exact string or compiled regex), `by_type` (widget class name, e.g. "Button"), `by_id` (kv lang id).
_Avoid_: locator, matcher, query params

**click**: Taps the center point of a widget. Called on the client with an element id: `client.click(element_id)`.
_Avoid_: tap, press

**input_text**: Types text into a TextInput widget. Called on the client with an element id and the text: `client.input_text(element_id, "hello")`. Raises if the widget is not a TextInput.
_Avoid_: type, enter_text, set_text

**Element id**: An opaque string identifier returned by `find` and `query`. Used as a handle to refer to a specific widget in subsequent `click`, `input_text`, or `get_text` calls. Not guaranteed stable across requests.
_Avoid_: locator, handle, ref, widget id

**Client**: The test-side object that talks to the kvaut server. Instantiated explicitly: `client = kvaut.Client()` then connected: `client.connect("my_app.main")`. All interactions (find, query, click, input_text, get_text, get_attributes) flow through the client using element ids. Test-runner-agnostic — works with pytest, unittest, or any Python test framework.
_Avoid_: driver, browser, session

**get_text**: Returns the `text` property of a widget. Called on the client: `client.get_text(element_id)`.
_Avoid_: read_text, text_content, inner_text

**get_attributes**: Returns a dict of named widget properties. Called on the client: `client.get_attributes(element_id, ["enabled", "disabled"])`. Properties are read directly from the Kivy widget instance.
_Avoid_: get_properties, fetch_attributes, read_attrs

**visible widget**: A widget is considered visible when all three conditions hold: its width and height are both greater than zero, its opacity is greater than zero, and it has a parent (it is connected to the widget tree). All other widgets are hidden.
_Avoid_: shown, displayed, on-screen

**kvaut launch**: The entry-point mechanism that starts the app under test. Invoked as `python -m kvaut.run <module.path>`. This module starts the kvaut server in a background thread, imports the user's module, and then calls `App().run()`. The user's application code requires no modifications.
_Avoid_: bootstrap, runner, wrapper

**KvautError**: Base exception class for all kvaut-specific errors. Subclasses include errors for element not found, ambiguous matches, server connection failures, and invalid operations (e.g. `input_text` on a non-TextInput widget).
_Avoid_: AutomationError, KvautException

## Example dialogue

**Dev**: I'm writing a test for my login screen. I have a TextInput for the username and a Button labeled "Log In". I want to type a username and tap the button.

**Expert**: Create a Client, connect to your app, then use `find` with `by_type` and `by_text` to get element ids for the TextInput and Button, then call `input_text` and `click`.

**Dev**: So something like:
```python
client = kvaut.Client()
client.connect("my_app.main")
username = client.find(by_type="TextInput")
client.input_text(username, "alice")
login_btn = client.find(by_text="Log In")
client.click(login_btn)
```

**Expert**: Exactly. If there's only one TextInput on screen, `find` returns its element id. If there were two visible TextInputs, `find` would raise — you'd use `query` instead and pick from the list. And since you're only checking the button by text, `find` will raise if "Log In" isn't visible or if there's somehow more than one.
