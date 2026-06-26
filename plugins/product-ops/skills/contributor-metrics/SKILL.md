---
name: contributor-metrics
description: Measure one contributor's productivity across GitHub and Jira — for the authenticated "me". Covers Dev metrics (story completion, code throughput, PR completion, lead/cycle time, defect density, change failure rate) and QA metrics (test creation/execution rate, defect detection efficiency, leakage, reopen rate). Auto-sources the inputs from git, the gh CLI, and the Jira MCP, scoped to your authorship; compares this 30-day window to the prior one. Pick the scope at runtime — a single repo, several repos, or a whole org. Use when answering "how productive have I been on GitHub and Jira?" or building a personal contributor report/dashboard.
---

# Contributor Metrics

A metric is only useful when it's tied to a **baseline** and a **decision**. A number with
no "vs what?" (this period vs last) and no "so what?" is noise — and most of these are easy
to game (LOC, raw counts), so interpretation matters more than the arithmetic. This skill
measures **one person — you** — across GitHub and Jira, and the default baseline is
**period-over-period** (last 30 days vs the prior 30).

## Preflight: resolve identity (runs first)

Everything here is scoped to *you*, so resolve your identity before sourcing anything.

| System | How to resolve |
| --- | --- |
| GitHub | `gh api user --jq .login` for the login; `git config user.email` / `git config user.name` for the commit identity. |
| Jira | `atlassianUserInfo` for your account; if needed `lookupJiraAccountId` by your email. |

**Stop conditions — exit, don't guess:**

- `git config user.email` / `user.name` is unset, or `gh api user` fails →
  *"Set your git identity (`git config user.email`…) and authenticate `gh` (`gh auth login`), then re-run."*
- The Atlassian MCP isn't connected / `atlassianUserInfo` fails →
  *"Connect the Atlassian (Jira) MCP server, then re-run."*

There is **no inference fallback** — if either side can't be resolved, say which one and stop.

## Pick the scope

Ask which GitHub scope to measure (default: current repo):

1. **Single repo** — the current repo, or a named `owner/repo`.
2. **Several repos** — a list of `owner/repo`; loop the same queries over each.
3. **Whole org** — every repo under an org, kept bounded by author-scoping the search.

Use **author-scoped `gh search`** as the engine so "org" stays bounded no matter how many
repos exist. Set `ME="$(gh api user --jq .login)"` once and reuse it.

```bash
gh search prs    --author="$ME"  --owner ORG   --created ">=DATE" --json url   | jq length   # PRs opened, org-wide
gh search commits --author="$ME" --owner ORG   --committer-date ">=DATE"                      # commits, org-wide
gh search issues --author="$ME"  --owner ORG   --created ">=DATE"                              # issues opened
```

For single/several repos, swap `--owner ORG` for `--repo owner/repo` (loop for several), or
within one checked-out repo use local `git log --author` + `gh pr list`.

## Process

1. **Pick the role and the question.** Are you reporting as a **Developer** or **QA/Tester**?
   What decision does this answer — "am I shipping more?", "is my quality holding?",
   "where am I leaking defects?" Choose the few metrics that answer *that*; do not dump all.
2. **Settle two windows.** Default `SINCE="--since='30 days ago'"` for the **current**
   window and the equal **prior** window (days 31–60). Run every metric **twice** — current
   and prior — so each result carries a period-over-period delta. Reuse the same window
   everywhere.
3. **Auto-source the inputs** (see [Sourcing inputs](#sourcing-inputs)), author-scoped to
   `$ME`. Only ask the user for what no tool can produce. Flag every number that's estimated
   or proxied.
4. **Compute.** Apply the formula. Percentages × 100; rates keep their unit (e.g. tests/hr).
   Show the substituted numbers, not just the result.
5. **Interpret against the baseline.** Every number gets a "so what": show
   `value (Δ vs prior 30d)`. An up-and-to-the-right count still needs a quality metric
   beside it so "faster" isn't hiding "worse". *Opt-in:* if the user asks to benchmark
   against peers, pull the same metrics for teammates and report the team median — heavier,
   and politically loaded, so only on request.
6. **Caveat.** Note proxy weakness (LOC ≠ value), gaming risk, and small-sample noise.

## Sourcing inputs

Find the inputs yourself before asking. Author-scope everything to `$ME`, and run each
against both the current and prior window. Use whichever tool is connected; fall back down
the list.

| Input | Where to get it |
| --- | --- |
| Merged / total PRs (you) | `gh search prs --author="$ME" --merged --merged-at ">=DATE"` and without `--merged`; scope with `--owner`/`--repo`. |
| Reviews given | `gh search prs --reviewed-by="$ME" --updated ">=DATE" --json url \| jq length` — PRs you reviewed. |
| Avg PR size | total additions+deletions of your merged PRs ÷ PR count: `gh pr list --author "$ME" --state merged --json additions,deletions`. |
| Commits / LOC | `git log $SINCE --author="$(git config user.email)" --pretty=tformat: --numstat \| awk '{a+=$1;d+=$2} END{print a"+ "d"-"}'`; org-wide via `gh search commits --author="$ME"`. |
| Lead time | merge/deploy timestamp − issue created: `gh issue view N --json createdAt` vs deploy time. |
| Cycle time | first commit → merge: `git log` first commit on the branch vs PR `mergedAt` (`gh pr view N --json mergedAt`). |
| Story completion / validation (you) | Jira MCP `searchJiraIssuesUsingJql` — `assignee=currentUser() AND resolved >= -30d`, count `status=Done` ÷ assigned. |
| Defects / bugs (total, prod, reopened) | Jira JQL `assignee=currentUser() AND type=Bug`, `labels=production`, `status changed to Reopened`; or `gh issue list --assignee "$ME" --label bug`. |
| Deployments (total/failed/successful) | CI: `gh run list --workflow deploy.yml --json conclusion`; count `success` vs `failure`. |
| Change failure rate | failed deploys ÷ total from the same `gh run list`, or your revert/hotfix commits in `git log`. |
| Test counts (created/executed/coverage) | test-runner output (`jest --json`, `pytest --collect-only -q`), coverage report, or the TMS (TestRail/Xray MCP). |
| AI-vs-manual hours, subjective baselines | not in any tool — **ask the user**; the only inputs that should require typing. |

Show the command and its output alongside each sourced number so the figure is auditable.
If a tool isn't connected, say so and fall back to asking rather than guessing.

## Developer metrics

### Productivity (build more, faster)

| Metric | Formula | Measures |
| --- | --- | --- |
| Story Completion Rate | Completed Stories ÷ Planned Stories × 100 | Delivery output |
| Code Throughput | LOC or Features Delivered ÷ Time | Development speed |
| PR Completion Rate | Merged PRs ÷ Total PRs × 100 | Delivery effectiveness |
| Reviews Given | PRs Reviewed ÷ Time | Collaboration / review load |
| Avg PR Size | (Additions + Deletions) ÷ Merged PRs | Change granularity |

Example: 12 merged ÷ 15 opened × 100 = **80% PR completion** (vs 71% prior 30d, ▲).

### Efficiency (build with less effort)

| Metric | Formula | Measures |
| --- | --- | --- |
| Lead Time | Deployment Date − Requirement Date | End-to-end speed |
| Cycle Time | Completion Time − Start Time | Development efficiency |

### Effectiveness (build better quality)

| Metric | Formula | Measures |
| --- | --- | --- |
| Defect Density | Defects ÷ KLOC (1000 lines) | Code quality |
| Escape Defect Rate | Production Bugs ÷ Total Bugs × 100 | Missed defects |
| Change Failure Rate | Failed Deployments ÷ Total Deployments × 100 | Release quality |
| First Pass Success | Features Accepted First Time ÷ Total Features × 100 | Quality |
| Deployment Success Rate | Successful Deployments ÷ Total Deployments × 100 | Stability |

Example: 95 ÷ 100 × 100 = **95% deployment success**.

## QA / Tester metrics

### Productivity (test more)

| Metric | Formula | Measures |
| --- | --- | --- |
| Test Case Creation Rate | Test Cases Created ÷ Hours | Writing speed |
| Execution Productivity | Executed Tests ÷ Time | Testing speed |
| Bug Logging Productivity | Valid Bugs ÷ Tester Hours | Output |
| Coverage Productivity | Covered Requirements ÷ Time | Efficiency |
| Story Validation Rate | Validated Stories ÷ Sprint | Throughput |

Example: 300 Test Cases ÷ 20 Hours = **15 / hr**.

### Efficiency (reduce effort)

| Metric | Formula | Measures |
| --- | --- | --- |
| Test Execution Efficiency | Executed Tests ÷ Total Available Time | Utilization |

### Effectiveness (find better defects)

| Metric | Formula | Measures |
| --- | --- | --- |
| Defect Detection Efficiency (DDE) | Defects Found in Testing ÷ Total Defects × 100 | Detection power |
| Defect Leakage | Production Defects ÷ Total Defects × 100 | Escaped issues |
| Requirement Coverage | Covered Requirements ÷ Total Requirements × 100 | Completeness |
| Valid Defect Rate | Accepted Bugs ÷ Reported Bugs × 100 | Bug quality |
| Reopen Rate | Reopened Bugs ÷ Closed Bugs × 100 | Fix quality |
| Test Effectiveness | Detected Defects ÷ Executed Tests | Test value |

Example: 120 ÷ 150 × 100 = **80% defect detection efficiency**.

## Output shape

```
## Subject & scope  — who (GitHub login + Jira account), scope (repo/repos/org), both windows
## Question         — the decision being answered, and role (Dev / QA)
## Inputs           — each number with the command/tool that produced it; mark estimated/asked ones
## Metrics          — each: formula with numbers substituted → result (Δ vs prior 30d)
## Interpretation   — every result vs the prior period, with a "so what"
## Caveats          — proxy weakness, gaming risk, sample size
```

A table of numbers isn't the deliverable — the read on them is.

## Deliver the report

After presenting the report in chat, also write it to a self-contained HTML file in the
system temp dir so the user can view and share it. Render the same sections; include a
header block (who / scope / both windows) and a **vs prior 30d** delta column in the metrics
table; include a print stylesheet so it paginates cleanly.

```bash
REPORT="${TMPDIR:-/tmp}/contributor-metrics-$(date +%Y%m%d-%H%M).html"
# write the HTML to "$REPORT" (Write tool), then offer to open it:
```

Use a minimal HTML shell — a styled `<body>` with the sections, plus:

```html
<style>
  body { font: 15px/1.5 system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; }
  table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
  th, td { border: 1px solid #ddd; padding: 6px 10px; text-align: left; }
  @media print { body { margin: 0; } }
</style>
```

Then tell the user the path and offer to open it — **ask first, don't auto-open**:

```bash
open "$REPORT"        # macOS
xdg-open "$REPORT"    # Linux
start "$REPORT"       # Windows
```

**To export as PDF:** open it in the browser, then **Print** (`Cmd/Ctrl+P`) →
**Destination: Save as PDF** → Save. Browser print-to-PDF keeps the table styling and
needs no extra tooling.
