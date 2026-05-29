"""Entry point for launching an app under test with kvaut instrumentation.

Usage: python -m kvaut.run <module.path>

Example: python -m kvaut.run my_app.main

This starts the kvaut server in a background thread, imports the user's
app module, finds the Kivy App subclass, instantiates and runs it.
The user's application code requires no modifications.
"""

import importlib
import logging
import os
import sys


logger = logging.getLogger(__name__)


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m kvaut.run <module.path>", file=sys.stderr)
        sys.exit(1)

    app_module = sys.argv[1]

    if os.environ.get("KVAUT_LOG"):
        logging.basicConfig(level=logging.DEBUG)

    logger.info("kvaut launching app: %s", app_module)

    # Start the server in a daemon thread before importing the user's module.
    from kvaut import server
    server.start()

    # Import the user's module (this registers their App class).
    importlib.import_module(app_module)

    # Find the App instance (may have been created during import) or create one.
    from kivy.app import App
    app = App.get_running_app()
    if app is None:
        # Look for an App subclass in the imported module
        mod = sys.modules.get(app_module)
        if mod:
            app_cls = _find_app_class(mod)
            if app_cls:
                app = app_cls()
            else:
                print(
                    "Error: No Kivy App subclass found in {}. "
                    "Make sure your module defines a class extending kivy.app.App.".format(
                        app_module
                    ),
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            print("Error: Failed to import module {}.".format(app_module), file=sys.stderr)
            sys.exit(1)

    logger.info("kvaut running app: %s", app.__class__.__name__)
    app.run()


def _find_app_class(module):
    """Find the first kivy.app.App subclass defined in a module."""
    from kivy.app import App

    for name in dir(module):
        obj = getattr(module, name)
        if (
            isinstance(obj, type)
            and issubclass(obj, App)
            and obj is not App
        ):
            return obj
    return None


if __name__ == "__main__":
    main()
