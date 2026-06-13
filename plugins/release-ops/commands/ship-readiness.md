---
description: Check whether the current branch is ready to ship — branch status, tests, build, migrations, env vars, and docs.
---

Assess whether the current work is ready to ship to production. Treat `$ARGUMENTS` as
the target environment or release name if provided; otherwise assume the default
production deploy.

Run a real readiness check — don't rubber-stamp. Where a command exists in this repo,
run it and report the actual result.

1. **Branch & commits.** Show `git status` and `git log <main>..HEAD --oneline`.
   Confirm the branch is up to date with its base and there's nothing uncommitted that
   should be in the release.

2. **Tests.** Find and run the project's test command (check `package.json` scripts,
   `Makefile`, `pyproject.toml`, CI config). Report pass/fail with the actual output.

3. **Build / typecheck / lint.** Run the build and any typecheck/lint the project
   defines. Report results.

4. **Migrations.** Detect pending database migrations in the diff. For each, check it's
   reversible and non-locking on large tables, and that it runs in the deploy pipeline.
   Flag anything risky.

5. **Config & secrets.** Diff for new env vars / config keys that must be set in the
   target environment, and scan the diff for accidentally committed secrets.

6. **Docs & changelog.** Check whether the changelog and any user-facing docs were
   updated for what's in this diff.

For the full reasoning behind each section, use the `release-checklist` skill.

Output a single verdict — **ship / don't ship / ship with caveats** — followed by a
short table of each check's status and any blockers that must be cleared first. Be
honest: if tests fail or a migration is unsafe, the verdict is "don't ship".
