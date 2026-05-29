# kvaut 1.0 is a full rewrite — new architecture, new API, no backwards compatibility

**Context:** kvaut was a Behave/Gherkin-based BDD automation library for Kivy
apps (Python 2.7/3.4, Kivy 1.9.x, Bottle HTTP server). The rewrite drops BDD in
favor of a test-runner-agnostic, Playwright-style Client API, targets modern
Python (3.10+) and Kivy (2.1+), and eliminates all app-side modifications by
using a separate entry point (`python -m kvaut.run`).

**Key decisions:**
- **No backwards compatibility.** Old Behave step files, `kvaut.client.tap()`,
  `CustomAutomator`, `nose` dependency, and `bottle` are all removed.
- **App under test requires zero modifications.** kvaut launches the user's app
  via a separate entry point that starts the HTTP server before importing the
  user's module and calling `App().run()`.
- **stdlib HTTP server** instead of Bottle/Flask/FastAPI. Five routes, no
  concurrency requirements, zero dependency overhead.
- **Widget uids as element IDs.** Every Kivy widget has a process-unique `.uid`;
  using this for element handles avoids a server-side cache and is simpler than
  lazy path encoding.
- **RTL-style find/query model.** `find()` raises on 0 or >1 visible matches;
  `query()` returns a list. Visible-only by default, `hidden=True` opt-in.
- **Selectors:** `by_text` (exact string or compiled regex), `by_type`, `by_id`.
- **Visibility:** size > 0, opacity > 0, has parent.
- **Test-runner-agnostic with optional pytest fixture.**
- **No layout assertions** (above/below/leading). Dropped as out of scope for v1.
- **No custom automator system.** Dropped; `query` + `get_attributes` covers the
  use case on the client side.
