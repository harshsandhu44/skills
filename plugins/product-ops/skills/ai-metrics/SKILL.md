---
name: ai-metrics
description: Compute and interpret AI-adoption metrics for developers and QA/testers — productivity, efficiency, and effectiveness (story/PR completion rate, code throughput, defect density, change failure rate, code acceptance rate, defect detection efficiency, defect leakage, reopen rate). Auto-sources the inputs from git, the gh CLI, Jira/GitHub MCP, and CI logs instead of asking the user to type numbers. Use when measuring the impact of AI coding/testing tools, building an AI-metrics report or dashboard, or when the user mentions any of these formulas or asks "how much did AI help" for a dev or QA team.
---

# AI Metrics

A metric is only useful when it's tied to a **baseline** and a **decision**. A number with
no "vs what?" (with-AI vs without-AI, or this period vs last) and no "so what?" is noise —
and most of these are easy to game (LOC, raw counts), so interpretation matters more than
the arithmetic.

## Process

1. **Pick the role and the question.** Developer or QA/Tester? What decision does this
   answer — "is AI making us faster?", "is quality holding?", "where's the leak?" Choose
   the few metrics that answer *that*; do not dump all 30.
2. **Auto-source the inputs** (see [Sourcing inputs](#sourcing-inputs)). Pull the numbers
   from the tools that already hold them — git, the `gh` CLI, the Jira/GitHub MCP servers,
   CI logs — before asking the user for anything. Settle the window (`--since`, sprint,
   date range) and run the commands. Only ask the user for what no tool can produce
   (subjective baselines, AI-vs-manual hours). Flag every number that's estimated or
   proxied — an estimated denominator makes the result an estimate.
3. **Compute.** Apply the formula. Percentages × 100; rates keep their unit (e.g. tests/hr).
   Show the substituted numbers, not just the result.
4. **Interpret against a baseline.** Every number gets a "so what": compare to the prior
   period or the without-AI baseline. Productivity Gain and Coding Time Saved *require* a
   without-AI figure — if there isn't one, say so rather than inventing it.
5. **Caveat.** Note proxy weakness (LOC ≠ value), gaming risk, and small-sample noise.
   Pair a productivity metric with an effectiveness one so "faster" isn't hiding "worse".

## Sourcing inputs

Find the inputs yourself before asking. Pick a window first (`SINCE="--since='30 days ago'"`
or a sprint name) and reuse it everywhere. Use whichever tool is connected; fall back down
the list.

| Input | Where to get it |
| --- | --- |
| Merged / total PRs | `gh pr list --state merged --search "merged:>=DATE" \| wc -l` and `--state all`; or GitHub MCP. |
| LOC / code throughput | `git log $SINCE --author=NAME --pretty=tformat: --numstat \| awk '{a+=$1;d+=$2} END{print a"+ "d"-"}'`. |
| Lead time | merge/deploy timestamp − issue created: `gh issue view N --json createdAt` vs deploy time. |
| Cycle time | first commit → merge: `git log` first commit date on the branch vs PR `mergedAt` (`gh pr view N --json mergedAt`). |
| Story completion / validation | Jira MCP `searchJiraIssuesUsingJql` — `project=X AND sprint="S"`, count `status=Done` ÷ total. |
| Defects / bugs (total, prod, reopened) | Jira JQL by `type=Bug`, `labels=production`, `status changed to Reopened`; or `gh issue list --label bug`. |
| Deployments (total/failed/successful) | CI: `gh run list --workflow deploy.yml --json conclusion`; count `success` vs `failure`. |
| Change failure rate | failed deploys ÷ total from the same `gh run list`, or revert/hotfix commits in `git log`. |
| Code acceptance rate | AI tool's own telemetry (Copilot/Cursor/Claude Code dashboards) — usually export/API only; ask if not available. |
| Test counts (created/executed/coverage) | test-runner output (`jest --json`, `pytest --collect-only -q`), coverage report, or the TMS (TestRail/Xray MCP). |
| AI-vs-manual hours, without-AI baseline | not in any tool — **ask the user**; these are the only inputs that should require typing. |

Show the command and its output alongside each sourced number so the figure is auditable.
If a tool isn't connected, say so and fall back to asking rather than guessing.

## Developer metrics

### Productivity (build more, faster)

| Metric | Formula | Measures |
| --- | --- | --- |
| Story Completion Rate | Completed Stories ÷ Planned Stories × 100 | Delivery output |
| Code Throughput | LOC or Features Delivered ÷ Time | Development speed |
| PR Completion Rate | Merged PRs ÷ Total PRs × 100 | Delivery effectiveness |
| Coding Time Saved | Manual Coding Hours − AI Coding Hours | Time reduction |
| Development Productivity Gain | (Output with AI − Output without AI) ÷ Output without AI × 100 | Overall gain |

Example: (18 − 12) ÷ 12 × 100 = **50% productivity increase**.

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
| Code Acceptance Rate | Accepted Suggestions ÷ Generated Suggestions × 100 | AI usefulness |

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
## Question        — the decision being answered, and role (Dev / QA)
## Inputs          — each number with the command/tool that produced it; mark estimated/asked ones
## Metrics         — each: formula with numbers substituted → result
## Interpretation  — every result vs its baseline, with a "so what"
## Caveats         — proxy weakness, gaming risk, sample size
```

A table of numbers isn't the deliverable — the read on them is.
