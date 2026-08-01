---
name: changelog
description: Turn a range of commits or a diff into a human-readable changelog grouped by type of change, written for the people who consume the software. Use when cutting a release, updating CHANGELOG.md, or summarizing what changed between two versions.
---

# Changelog

A changelog is for *humans deciding whether and how to upgrade* — not a `git log` dump.
It answers "what's new, what's fixed, and what will break me?" This skill turns raw
commits into that.

The repo's own `CHANGELOG.md` follows [Keep a Changelog](https://keepachangelog.com/)
and SemVer — match that format when editing it.

## Process

### 1. Get the commit range

```bash
git log <last-tag>..HEAD --oneline          # commits since last release
git diff <last-tag>...HEAD --stat           # scope of change
```

If there's no tag, ask the user for the starting point. Read the commits *and* skim the
diff — commit messages often undersell or mislabel the actual change.

### 2. Group by change type

Use Keep a Changelog's categories; drop empty ones:

- **Added** — new features/capabilities.
- **Changed** — changes to existing behavior.
- **Deprecated** — soon-to-be-removed features.
- **Removed** — features taken out.
- **Fixed** — bug fixes.
- **Security** — vulnerability fixes.

### 3. Rewrite each entry for the consumer

Translate from developer-speak to user-impact:

- ❌ "refactor auth middleware" → ✅ nothing (internal; omit it).
- ❌ "fix bug in `OrderService.total()`" → ✅ "Fixed order totals being off by a cent on
  multi-currency carts."
- Each line: what changed, from the reader's point of view. Imperative or past tense,
  consistent. Link the PR/issue if the project does.

Internal-only churn (refactors, test changes, formatting, dependency bumps with no
user effect) does **not** belong in a user-facing changelog. A separate "Internal"
section is fine only if the audience is other developers.

### 4. Flag breaking changes loudly

Anything that requires the consumer to change their code/config gets called out
explicitly — a **BREAKING** prefix or a dedicated section, with the migration step.
This is the single most important thing a changelog does; bury it and you've failed.

### 5. Set the version & date

Per SemVer: breaking → major, additive → minor, fixes only → patch. Add the release
date. Put new content under `## [Unreleased]` if the release isn't cut yet.

## Output shape

```text
## [x.y.z] - YYYY-MM-DD

### Added
- ...
### Changed
- ...
### Fixed
- ...

### ⚠️ Breaking
- <what breaks> — <how to migrate>
```

If you're unsure whether something is user-visible, ask rather than dumping the commit
verbatim. A short, accurate changelog beats a long, noisy one.
