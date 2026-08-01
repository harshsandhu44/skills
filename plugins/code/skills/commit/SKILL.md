---
name: commit
description: "Detect project type, run formatter + linter, then commit changes progressively with conventional commit messages"
trigger: /commit
---

# /commit

Detect the project's language/toolchain, run the appropriate formatter and linter, fix any issues, then commit staged or unstaged changes progressively using conventional commit messages.

## Usage

```
/commit           # fmt + lint + commit all changes as one or more logical commits
/commit --dry-run # show what would be committed without committing
```

## What You Must Do When Invoked

Follow these steps in order. Do not skip steps.

### Step 1 — Check working tree state

```bash
git status --short
git diff --stat
git diff --cached --stat
```

If the working tree is completely clean (no staged, no unstaged, no untracked files), print:

```
Nothing to commit — working tree is clean.
```

And stop.

### Step 2 — Detect project type

Check for project manifests to determine the toolchain:

```bash
ls Cargo.toml package.json pyproject.toml setup.py go.mod Gemfile mix.exs pom.xml build.gradle 2>/dev/null
```

Use the first match in this priority order:

| File found | Toolchain | Formatter | Linter |
|------------|-----------|-----------|--------|
| `Cargo.toml` | Rust | `cargo fmt` | `cargo clippy -- -D warnings` |
| `package.json` (check for `biome`, else eslint/prettier) | Node/TS | `npm run format` or `npx prettier --write .` | `npm run lint` or `npx eslint .` |
| `pyproject.toml` / `setup.py` | Python | `ruff format .` or `black .` | `ruff check .` or `flake8` |
| `go.mod` | Go | `gofmt -w .` | `go vet ./...` |
| `Gemfile` | Ruby | `rubocop -a` | `rubocop` |
| `mix.exs` | Elixir | `mix format` | `mix credo` |

If none of the above are found, note it and skip Steps 3 and 4.

For Node projects, check `package.json` scripts to pick the right commands:
```bash
cat package.json | grep -E '"(format|lint|check)"'
```

### Step 3 — Run formatter

Run the formatter detected in Step 2. After running, check what changed:

```bash
git diff --name-only
```

Note any reformatted files. Do not stage them yet.

### Step 4 — Run linter

Run the linter detected in Step 2.

**If the linter exits non-zero:**
- Read the output carefully.
- Fix every warning/error in the source files. Do not suppress warnings with `#[allow(...)]`, `// eslint-disable`, `# noqa`, or similar unless the warning is a genuine false positive — explain why if you do.
- After fixing, re-run the linter to confirm it passes. Repeat until it exits 0.
- If you cannot fix a warning after two attempts, stop and explain the blocker to the user. Do not commit with a failing linter.

**If the linter exits 0:** proceed to Step 5.

### Step 5 — Understand the changes

Run:

```bash
git diff HEAD
git status --short
```

Read the full diff. Group the changes into logical units based on:
- **What** changed (feature, fix, refactor, test, docs, chore, style, perf, build, ci)
- **Why** it changed (the intent, not the mechanism)
- **Scope** (which module, command, file, or subsystem was affected)

Formatting-only changes (from Step 3) and lint-only fixes (from Step 4) should be their own commits, separate from intentional feature/fix changes, unless the mechanical changes are trivially small (1-2 lines).

### Step 6 — Stage and commit progressively

For each logical unit identified in Step 5:

1. Stage only the files that belong to this unit:
   ```bash
   git add <specific files>
   ```
   Prefer named files over `git add -A` to avoid accidentally staging sensitive or unrelated files.

2. Write a conventional commit message:
   - Format: `<type>(<optional scope>): <short imperative description>`
   - Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `style`, `perf`, `build`, `ci`
   - Keep the subject line under 72 characters.
   - Use imperative mood: "add", "fix", "remove" — not "added", "fixes", "removes".
   - Do not mention Claude, tools, or this skill.
   - Examples:
     - `feat(push): implement notion page update on re-push`
     - `fix(write): resolve duplicate note creation on existing titles`
     - `style: apply cargo fmt`
     - `chore: fix clippy warnings`

3. Commit:
   ```bash
   git commit -m "<message>"
   ```

4. Confirm the commit landed:
   ```bash
   git log --oneline -3
   ```

5. Move to the next logical unit and repeat until all changes are committed.

### Step 7 — Final status

After all commits:

```bash
git log --oneline -<N>   # N = number of commits made
git status --short
```

Print a brief summary:
- How many commits were made
- What each commit contained (one line each)
- Whether the working tree is now clean

If `--dry-run` was passed, print the plan (grouped changes + proposed commit messages) **without** running `git commit`, and stop.

## Conventional commit type guide

| Type | When to use |
|------|-------------|
| `feat` | New user-visible behavior |
| `fix` | Bug fix |
| `refactor` | Code restructure with no behavior change |
| `test` | Adding or fixing tests |
| `docs` | Documentation only |
| `chore` | Tooling, deps, config, non-code maintenance |
| `style` | Formatting/whitespace only (e.g. from `cargo fmt`, `prettier`) |
| `perf` | Performance improvement |
| `build` | Build system or compilation changes |
| `ci` | CI/CD pipeline changes |

## Rules

- Never use `--no-verify` or bypass hooks.
- Never amend a commit already in the log — create a new one instead.
- Never force-push.
- Never commit files that look like secrets (`.env`, credential files, tokens). Warn and stop if you encounter them.
- If the linter cannot be fixed, do not commit. Report the blocker to the user.
