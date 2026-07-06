---
name: claude-vs-dev
description: Compare developer-written vs Claude-assisted code in a git repo by reading commit trailers — Claude-assisted commits carry a `Co-Authored-By: Claude` trailer. Aggregates commit count and line churn per bucket over a user-chosen time range and writes a temp HTML report to open in the browser. Use when the user asks how much code was Claude-assisted, wants to split human vs AI commits, or requests a Claude-vs-developer contribution report for a repo.
---

# claude-vs-dev

Splits a repo's commits into **developer-only** and **Claude-assisted** (message has a
`Co-Authored-By: Claude` trailer), aggregates them, and writes an HTML report.

## What to do when invoked

1. **Confirm the repo.** Default to the current directory. Ensure it's a git repo.

2. **Ask the user for the time range** — do not guess. Offer these and accept a custom answer:
   - Last 30 days
   - Last 90 days
   - Custom range (a start date, optionally an end date)

   Map the answer to `git`-friendly dates: `--since "30 days ago"`, or `--since 2026-01-01 --until 2026-06-30`.

3. **Run the script:**

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/claude-vs-dev/scripts/report.py" \
     --since "30 days ago" --repo . --open
   ```

   Add `--until "<date>"` for a bounded range. `--open` launches each report in the
   default browser (`open`/`xdg-open`/`start`); drop it to only write files.
   The script prints one `author<TAB>path` line per report written. Exit code 2 means
   no matching commits — tell the user and offer a wider range.

   **Target scope** (repo/org): pass whichever the user provides; otherwise use the current repo.
   - `--repo owner/name` — a single remote GitHub repo (shallow-cloned to temp for the range).
   - `--repos a,b,c --org <org>` — a curated list; bare names are prefixed with `--org`.
   - `--org <org>` alone — every non-archived repo in the org/user (needs `gh`).
   - neither → the current local repo (`.`).

   Remote repos are shallow-cloned **once** and reused across all authors.

   **Author scope:** if the user names GitHub usernames (or author names/emails):
   - one user → `--author <value>`.
   - several users → `--authors u1,u2,u3` — writes **one HTML report per user**.
   - omit → current git user (`git config user.email`); `--author all` → everyone combined.

   When the scope is a GitHub repo/org, a bare username is resolved to the commit
   email(s) it authors under via `gh` (GitHub links commits to a login by email, so
   the login rarely appears in the git author string). A value containing `@` is used
   as-is; against a purely local repo, matching falls back to a name/email substring.

   Use `--out-dir <dir>` to collect all reports in one folder (default: a temp dir).

4. **Return the links.** For each `author<TAB>path` line, give the user a clickable
   `file://` URL (one per user) plus a one-line summary (total commits, Claude share).

## Notes

- Detection is purely the commit trailer; commits authored before that convention won't count as Claude-assisted.
- Line churn comes from `git log --numstat` (merge commits contribute no numstat, so they only count toward commit totals).
