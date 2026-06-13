---
name: release-checklist
description: Run a pre-release readiness check across app, API, database, config, and docs before cutting a release or deploying to production. Use when preparing to ship a release and you want to catch the migration, env-var, or breaking-change landmine before it reaches users.
---

# Release Checklist

Most production incidents trace to something boring that nobody checked: a migration
that wasn't run, an env var that wasn't set, a breaking change nobody flagged. This
checklist makes the boring checks systematic so the deploy is uneventful.

Adapt to the project — drop sections that don't apply, but justify dropping rather than
skipping silently.

## Process

Walk each section and record a status (✅ ok / ⚠️ needs action / n/a). Don't guess —
verify against the diff, the migrations, and the config.

### Code & version

- The release branch/tag is what you think it is (`git log`, the right commits in).
- Version bumped where the project tracks it (manifest, `__version__`, tag).
- Changelog updated (see the `changelog` skill).
- No debug code, leftover `console.log`/`print`, commented-out blocks, or `TODO: before
  ship` markers in the diff.

### API & compatibility

- Any breaking API change is versioned or behind a flag; clients won't break.
- Backwards compatibility with the *previous* release holds during the rollout window
  (old and new run side by side mid-deploy).
- New required request fields have defaults or a migration path.

### Database

- Migrations are present, ordered, and run in the deploy pipeline.
- Each migration is non-locking on large tables (or has an online path) and reversible.
- Backfills are batched and idempotent.
- The migration is compatible with the *currently running* code (expand/contract).

### Config & secrets

- New env vars / secrets are documented and set in every target environment.
- No secret is committed (see the `secret-sweep` skill / a secret scan).
- Feature flags default to a safe state; the on/off plan is written down.
- Third-party keys, webhooks, and callback URLs are configured for the target env.

### Observability & rollback

- Logging/metrics exist for the new paths; you'll be able to tell if it's broken.
- The rollback plan is concrete: revert the deploy, and what to do about any migration
  that can't be trivially undone.
- Alerts/dashboards cover the new failure modes.

### Docs & comms

- User-facing docs / API docs updated.
- The team/stakeholders know what's shipping and when.

## Output shape

```text
## Ready to ship?   (overall: yes / no / yes-with-caveats)
## Blockers         (⚠️ items that must be resolved first)
## Checklist        (each section, status per item)
## Rollback plan
```

If anything is ⚠️, the headline is "not ready" until it's resolved or explicitly
accepted. The checklist's job is to make someone *decide*, not to rubber-stamp.
