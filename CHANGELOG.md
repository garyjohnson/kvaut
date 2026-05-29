# Changelog

## [1.0.0](https://github.com/garyjohnson/kvaut/compare/v0.0.18...v1.0.0) (2026-05-29)


### ⚠ BREAKING CHANGES

* drops Behave/Gherkin BDD layer, Python 2.7/3.4 support, Kivy 1.x support, custom automators, layout assertions, Bottle/nose/shovel/tox dependencies.

### Features

* modernize kvaut ([41362ef](https://github.com/garyjohnson/kvaut/commit/41362efac15d696aa13a650eba8a939e4a829314))
* rewrite kvaut as a test-runner-agnostic Playwright-style library ([e462e83](https://github.com/garyjohnson/kvaut/commit/e462e833709209ae7481332eb7b6a3d93359b4d3))


### Bug Fixes

* populate release-please manifest with current version ([d415105](https://github.com/garyjohnson/kvaut/commit/d415105ec18e192d48e60b0b746a58bb936e64af))
* remove stale old-layout directories before pip install in CI ([388b2db](https://github.com/garyjohnson/kvaut/commit/388b2db3a3dbea5669ca3c1c6f7b12080e588e58))
* restrict CI triggers to push on main and pull_request only ([6320a3a](https://github.com/garyjohnson/kvaut/commit/6320a3ac928149ae1fe2f1f60ee502badf627733))


### Documentation

* add CONTEXT.md glossary, ADR, AGENTS.md, updated README ([91c04fe](https://github.com/garyjohnson/kvaut/commit/91c04fe583ec822c96b4cd6ec60228c18bdd180e))
