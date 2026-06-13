---
name: dependency-upgrade
description: Upgrade one or more packages safely — read the changelog for breaking changes, upgrade in isolation, run tests, and keep a rollback path — instead of bumping versions and hoping. Use when updating dependencies, resolving a security advisory, or moving across a major version.
---

# Dependency Upgrade

"Bump everything and run the tests" is how you spend a day bisecting which of fourteen
upgrades broke the build. Upgrade deliberately, one risk unit at a time, with a way
back.

## Process

### 1. Know what you're changing and why

List the target packages and the reason: security advisory, needed feature, routine
maintenance. For each, find the **current** and **target** version and the jump size
(patch / minor / major). Majors are where the danger lives — treat each major upgrade
as its own unit of work.

### 2. Read the release notes — actually read them

For each package crossing a minor or major boundary, read the changelog/migration guide
between current and target. You're hunting for:

- **Breaking changes** — removed/renamed APIs, changed defaults, dropped runtime
  versions (Node/Python/etc.).
- **Deprecations** you should act on now.
- **Required migration steps** (codemods, config changes).

Note the breaking changes that touch how *your* code uses the package. Grep the
codebase for the affected APIs to size the blast radius.

### 3. Upgrade in isolation

One logical change at a time — a single package, or a tightly-coupled set (a framework
and its plugins). Update the manifest **and the lockfile**; let the lockfile pin
transitive deps so the change is reproducible. Don't bundle an unrelated upgrade into
the same step — if something breaks you want to know exactly what.

### 4. Verify

- Install cleanly from the lockfile (fresh install, not just incremental).
- Build / typecheck.
- Run the full test suite.
- For a major or a runtime-sensitive package, smoke-test the app's critical paths, not
  just unit tests — behavior changes slip past green tests.

Apply any required migration from step 2 *before* expecting green.

### 5. Keep the rollback obvious

Each upgrade is its own commit (manifest + lockfile together), so reverting is one
`git revert`. Note in the commit message the version change and any migration applied.
If the upgrade is risky, say how you'd detect a regression in prod and back it out.

## Output shape

```text
## Upgrades        (package: from → to, jump size, reason)
## Breaking changes (per package, what affects us, grep'd call sites)
## Migration       (steps applied)
## Verification    (install / build / test / smoke results)
## Rollback        (per-commit revert; prod detection)
```

When several packages need upgrading, do them as separate commits in dependency order
(runtime → framework → plugins → leaves), not one big bump. Slower, but you'll never be
stuck guessing which one broke.
