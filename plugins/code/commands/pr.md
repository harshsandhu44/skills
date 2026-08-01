---
description: Build a complete pull-request write-up from the current branch (wrapper around the pr-builder skill).
---

Generate a pull-request description for the current branch.

Use the `pr-builder` skill to do the work — it defines the full process (gather the
diff, write the summary, motivation, what-changed, test evidence, risk notes, and a
reviewer checklist).

Treat `$ARGUMENTS` as the base ref to diff against if provided; otherwise default to
the repo's main branch.

After producing the description:

- If a PR template exists (`.github/PULL_REQUEST_TEMPLATE.md` or similar), match its
  structure.
- Present the description in a copy-pasteable block.
- If the user asks to open the PR (and a remote + `gh` are available), offer to create
  it with `gh pr create` — but only when explicitly asked; default to just producing
  the text.
