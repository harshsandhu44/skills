---
name: deliverables
description: Report what a user (or users) delivered in a repo (or repos) over a time range, mapping their git commits to the Jira tickets they reference. A helper script scans git and groups each author's commits by Jira key (pattern ABC-123); commits with no key are kept in a separate bucket so nothing is lost. Claude enriches each ticket with its summary/status/type via the Atlassian (Jira) MCP, writes a markdown report plus a styled HTML rendering, hands back the markdown link (convertible to docx), and opens the HTML in the browser. Use when the user asks for a deliverables report, what someone shipped/worked on, per-person contributions tied to Jira tickets, or a commit-to-ticket breakdown for a repo, list of repos, or GitHub org.
---

# deliverables

Maps each author's commits to the Jira tickets they reference and writes a markdown
report plus a styled HTML rendering. `deliverables.py` = git → commits grouped by
Jira key (JSON); Claude = Jira enrichment + markdown; `md2html.py` = markdown → HTML.

## What to do when invoked

1. **Confirm scope.** Repo(s) and user(s) — default to the current repo and current
   git user if the user doesn't say. Accept a single repo, a `--repos` list, or an
   `--org`; a single user, `--authors` list, or `all`.

2. **Ask the time range** — do not guess. Offer *Last 30 days* / *Last 90 days* /
   *Custom*, and map to git dates (`--since "30 days ago"`, or `--since 2026-01-01
   --until 2026-06-30`).

3. **Run the script** — it prints one JSON blob to stdout:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/deliverables/scripts/deliverables.py" \
     --since "30 days ago" --repo . --authors alice,bob
   ```

   - Repo scope: `--repo .` (local), `--repo owner/name`, `--repos a,b,c --org acme`,
     or `--org acme` alone (all its repos, needs `gh`). Remotes are shallow-cloned once.
   - Author scope: `--author <x>` (name/email/GitHub login), `--authors a,b`, or
     `--author all`. GitHub logins are resolved to commit emails via `gh`.
   - JSON shape: `authors[].tickets` is `{ "ABC-123": [{sha,date,subject,repo}, …] }`,
     plus `authors[].no_ticket` for commits with no Jira key, and `ticket_keys`.
   - Empty `authors[].tickets` **and** empty `no_ticket` → no commits in range; tell
     the user and offer a wider range.

4. **Enrich the Jira tickets.** Collect every key across all authors (`ticket_keys`).
   Get the cloudId with `mcp__atlassian__getAccessibleAtlassianResources`, then fetch
   all tickets in one call with `mcp__atlassian__searchJiraIssuesUsingJql`, JQL
   `key in (ABC-123, ABC-124, …)`, requesting `summary,status,issuetype,assignee`.
   A key with no match (typo, other project) still gets a row — mark it *not found*.

5. **Write the markdown report** with the Write tool to
   `<scratchpad>/deliverables-<label>-<since>.md` (one file, a section per user).
   Per user, use this shape:

   ```markdown
   ## <user> — <N> commits, <M> tickets

   | Ticket | Type | Status | Summary | Commits |
   |--------|------|--------|---------|---------|
   | [ABC-123](<jira-base>/browse/ABC-123) | Story | Done | Fix login redirect | 4 |

   ### No linked ticket (<K> commits)
   - `a1b2c3d` 2026-06-30 — chore: bump deps *(repo)*
   ```

   Link each key to `<jira-base>/browse/<KEY>` using the site URL from
   `getAccessibleAtlassianResources`. Add a one-line header with repo scope + range.

6. **Render HTML and open it.** Convert the markdown to a styled standalone HTML with
   the bundled renderer (no pandoc needed), then open the **HTML** in the browser — a
   browser shows a raw `.md` as plain text, so the `.html` is what gets opened:

   ```bash
   python3 "${CLAUDE_PLUGIN_ROOT}/skills/deliverables/scripts/md2html.py" "<path>.md"
   open "<path>.html"   # macOS; xdg-open on Linux, start on Windows
   ```

7. **Return the links.** Give the user the markdown `file://` link (their editable
   artifact — converts straight to docx via `pandoc file.md -o file.docx`) and note the
   HTML opened in the browser, plus a one-line summary (commits, tickets, no-ticket count).

## Notes

- Jira keys are matched by regex (`[A-Z][A-Z0-9]+-\d+`) anywhere in the commit
  message — subject, body, or squash-merged PR title. No project config needed.
- One commit referencing two tickets is counted under both.
- Merge commits carry no numstat, but their message is still scanned for keys.
