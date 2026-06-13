---
name: secret-sweep
description: Scan a diff, file, or config for exposed secrets — API keys, tokens, passwords, private keys, connection strings — before they're committed or shipped. Use before committing, in a pre-release check, or when reviewing config and infrastructure files for accidental credential exposure.
---

# Secret Sweep

A committed secret is compromised the moment it's pushed — rewriting history doesn't
un-leak it, because it's already in clones, forks, and caches. The only safe secret is
the one that never lands. This skill catches them first.

The `security-ops` plugin also ships a PostToolUse hook that warns on secrets in files
Claude writes; this skill is the deliberate, on-demand sweep of a diff or tree.

## Process

### 1. Scope the sweep

Pick the surface:

```bash
git diff --staged          # about to commit
git diff <base>...HEAD      # the whole branch
```

…or a directory/file set. Prioritize the high-risk files: `.env*`, `config/*`,
`*.yml`/`*.yaml`, CI definitions, Terraform/IaC, notebooks, and anything in the diff
that adds a credential-shaped string.

### 2. Look for the known shapes

High-signal patterns (low false-positive):

- **Cloud keys** — AWS `AKIA…`, Google `AIza…`, Azure connection strings.
- **Provider tokens** — `sk-…` (OpenAI/Stripe), GitHub `ghp_`/`gho_`/`github_pat_`,
  Slack `xox[baprs]-…`, npm/PyPI tokens.
- **Private keys** — `-----BEGIN … PRIVATE KEY-----` blocks.
- **Connection strings** — `postgres://user:pass@…`, `mongodb+srv://…`, `redis://…`
  with inline credentials.
- **Generic** — assignments like `password = "…"`, `api_key: "…"`, `secret = "…"` with a
  long literal value.

### 3. Triage each hit

Not every match is a live secret. For each, decide:

- **Real & live** — a working credential. Top priority.
- **Example / placeholder** — `AKIAIOSFODNN7EXAMPLE`, `your-key-here`, `xxx`. Safe, but
  confirm it's obviously fake, not a real key lightly redacted.
- **Test fixture** — a dummy used in tests. Fine, but flag if it looks real.

When unsure, treat it as real. The cost of a false alarm is a glance; the cost of a
missed key is a breach.

### 4. Remediate properly

For a real exposed secret:

1. **Rotate it** — assume it's compromised; revoking is the only real fix. Removing the
   line is not enough.
2. **Remove it from the code** — move to an env var / secret manager; reference it, don't
   embed it.
3. **Keep it out** — add the file pattern to `.gitignore`; add a secret scanner to
   pre-commit/CI so the next one is caught automatically.
4. If already committed, note that history rewriting + rotation are both required.

## Output shape

```text
## Scanned         (what surface)
## Findings        (file:line · type · real / example / fixture · severity)
## Must rotate     (live secrets — rotate + remove + keep-out steps)
## Prevention      (gitignore / pre-commit / CI scanner gaps)
```

The headline is the count of *live* secrets. If it's zero, say so plainly; if it's not,
rotation comes before anything else.
