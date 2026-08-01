---
description: Summarize the diff since main (or a given ref) for a human reviewer — what changed, why, and what to scrutinize.
---

Explain the changes on the current branch for a human reviewer who hasn't seen them.

Pick the base ref from `$ARGUMENTS` if given (a branch, tag, or commit); otherwise
default to the repo's main branch.

1. Gather the change:

   ```bash
   git log <base>..HEAD --oneline
   git diff <base>...HEAD --stat
   git diff <base>...HEAD
   ```

2. Read the actual diff — do not summarize from commit messages alone.

Then produce, in plain language for a reviewer:

- **TL;DR** — two sentences on what this branch does and why.
- **Walkthrough** — the changes grouped by area/concern (not file-by-file), each with
  the *intent* behind it, in an order that tells the story of the change.
- **Notable decisions** — anything non-obvious: a tradeoff, a workaround, a pattern
  chosen over another.
- **Where to look hardest** — the riskiest or subtlest parts a reviewer should not skim:
  auth, migrations, concurrency, money, anything with wide blast radius.
- **Not covered** — what this change deliberately does *not* do, to set scope.

Keep it scannable and reviewer-focused. The goal is that someone can review with
judgement instead of reverse-engineering the diff. This is a read-only explanation —
do not modify code.
