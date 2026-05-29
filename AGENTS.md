# kvaut

Developer guide for contributing to kvaut.

## Commits

This project uses [Conventional Commits](https://www.conventionalcommits.org/).

```
feat: add scroll support to query selector
fix: resolve tap dispatch on nested layouts
docs: update API reference examples
chore: upgrade CI runner to ubuntu-24.04
```

PR titles must follow the same convention (enforced by CI). Breaking changes
use `feat!:` or a `BREAKING CHANGE:` footer.

## Releases

Releases are automated via [release-please](https://github.com/googleapis/release-please).

- Merging a PR to `main` with a conventional commit triggers release-please to
  open or update a release PR
- The release PR contains the bumped version and auto-generated changelog
- Merging the release PR creates a git tag and GitHub release
- The tag triggers the PyPI publish workflow

Versioning follows [semver](https://semver.org/) based on commit prefixes:
- `fix:` → patch bump
- `feat:` → minor bump
- `feat!:` or `BREAKING CHANGE:` → major bump

## Versioning

The package version is derived from git tags via [setuptools-scm](https://github.com/pypa/setuptools-scm).
There is no hardcoded version string — it is computed at build time from the
most recent tag.

## CI

- **ci.yml** — runs tests (unit + integration) via `xvfb-run` on
  push to `main`/`modernize` and on PRs
- **pr-check.yml** — validates PR titles follow conventional commit format
- **release-please.yml** — manages release PRs and changelog generation
- **publish.yml** — builds and publishes to PyPI when a GitHub release is published

## Running tests

```bash
pip install -e ".[dev]"
pytest                      # locally (requires a display)
xvfb-run -a pytest          # headless (CI)
```

Set `KVAUT_LOG=DEBUG` for verbose server output.

## Project structure

```
src/kvaut/
├── __init__.py    # Public API: Client, error classes
├── client.py      # Test-side client (HTTP)
├── server.py      # stdlib HTTP server in app process
├── tree.py        # Widget tree traversal, matching, tap dispatch
├── run.py         # Entry point: python -m kvaut.run <module>
└── errors.py      # KvautError hierarchy
tests/
├── test_tree.py       # Unit tests (widget matching, visibility, serialization)
├── test_client.py     # Error hierarchy tests
├── test_integration.py # End-to-end tests (launch real Kivy app)
├── conftest.py        # Pytest fixtures
└── test_apps/         # Sample Kivy apps for integration tests
```

## Documentation

- [CONTEXT.md](CONTEXT.md) — project glossary
- [docs/adr/](docs/adr/) — architecture decision records
