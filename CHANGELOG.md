# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project
adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- `dev-workflow` plugin (`commit`, `review`, `branch-tests`, `tdd`).
- `claude-meta` plugin (`write-a-skill`, `grill-me`, `hand-off`, `caveman`), with attribution note.
- `web-perf` plugin (`web-perf`).
- `product-ops` plugin: skills (`spec-to-plan`, `thin-slice`, `api-contract`, `db-model-review`, `debug-ladder`, `mvp-scope-cut`) and agents (`codebase-cartographer`, `spec-skeptic`, `api-contract-reviewer`, `db-access-pattern-reviewer`).
- `release-ops` plugin: skills (`pr-builder`, `release-checklist`, `changelog`, `dependency-upgrade`, `incident-postmortem`) and commands (`/ship-readiness`, `/explain-diff`, `/pr`).
- `security-ops` plugin: skills (`threat-model`, `auth-boundary-review`, `secret-sweep`, `dependency-risk`, `rate-limit-review`), agents (`security-reviewer`, `authz-reviewer`, `secrets-detective`), and guardrail hooks (block dangerous Bash, warn on secrets in edited files).

- `research-lab` plugin: skills (`paper-to-notes`, `competitor-teardown`, `idea-kill-test`) and agents (`evidence-scout`, `source-skeptic`, `market-sizer`, `copy-roaster`).
- `field-notes` plugin: skills (`f1-race-debrief`, `football-match-review`, `astro-observation-plan`).

### Changed

- `web-perf` 0.2.0: added skills `bundle-diet`, `nextjs-perf-review`, `seo-a11y-audit`, and `landing-page-roast`.

### Removed

- Placeholder `skills` plugin and its `hello-world` example.

## [0.1.0] - 2026-06-12

### Added

- Marketplace (`harshsandhu`) and the `skills` plugin scaffold.
- `hello-world` reference skill.
- CI manifest validation and markdown linting.
- Contributor docs and GitHub templates.
