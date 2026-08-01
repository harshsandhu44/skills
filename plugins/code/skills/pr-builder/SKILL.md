---
name: pr-builder
description: Generate a complete pull-request write-up from a branch diff — summary, motivation, what changed, test evidence, risk notes, and a reviewer checklist. Use when opening a PR and you want a description that a reviewer can act on without re-deriving the whole change.
---

# PR Builder

A good PR description is a gift to your reviewer: it tells them *what* changed, *why*,
and *how to be confident it works*, so review is about judgement, not archaeology. This
skill builds that description from the actual diff.

## Process

### 1. Gather the facts from git

```bash
git log <base>..HEAD --oneline      # the commits
git diff <base>...HEAD --stat       # files touched, churn
git diff <base>...HEAD              # the actual change
```

Default `<base>` to the repo's main branch unless the user says otherwise. Read the
diff — don't summarize from commit messages alone; commit messages lie, diffs don't.

### 2. Write the summary (the part people actually read)

Two or three sentences, top of the PR: what this does and why it matters, in plain
language. A reviewer should understand the change from this alone. Lead with the user-
or system-visible effect, not the implementation.

### 3. Motivation / context

Why now? Link the issue/ticket. State the problem this solves or the capability it
adds. If it's a fix, name the bug and its impact. This is what justifies the change
existing at all.

### 4. What changed

A short, grouped list — by area or concern, not file-by-file. "Auth: added org-scoping
to the orders endpoint. Migration: new index on `orders.org_id`. Tests: …" Call out
anything non-obvious: a deliberate design choice, a workaround, a thing you considered
and rejected.

### 5. Test evidence

How do we know it works? Be concrete:

- Tests added/changed, and what they cover.
- Commands run and their result (`pytest -q` → 142 passed).
- Manual verification steps, if any, and what you observed.

"Tested locally" with no detail is not evidence. If something is *not* tested, say so.

### 6. Risk notes

What could go wrong in review or prod? Migrations (locking, backfill), breaking API
changes, feature flags, config/env changes, data backfills, anything touching auth or
billing. For each risk, the mitigation or rollback. An honest risk section gets a PR
merged faster than a silent one.

### 7. Reviewer checklist

A short list of things you specifically want eyes on, plus the mechanical ones:
screenshots for UI, migration reviewed, secrets not committed, docs updated.

## Output shape

```text
## Summary
## Motivation
## What changed        (grouped)
## Test evidence       (commands + results)
## Risk & rollback
## Reviewer checklist  (checkboxes)
```

Keep it scannable. A reviewer who has to read 600 words before understanding the change
will skim and miss things — front-load the summary and the risks.
