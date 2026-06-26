---
name: ai-metrics
description: Compute and interpret AI-adoption metrics for developers and QA/testers — productivity, efficiency, and effectiveness (story/PR completion rate, code throughput, defect density, change failure rate, code acceptance rate, defect detection efficiency, defect leakage, reopen rate). Use when measuring the impact of AI coding/testing tools, building an AI-metrics report or dashboard, or when the user mentions any of these formulas or asks "how much did AI help" for a dev or QA team.
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
2. **Gather the raw inputs.** List exactly what each chosen formula needs. Flag anything
   missing, estimated, or proxied — an estimated denominator makes the result an estimate.
3. **Compute.** Apply the formula. Percentages × 100; rates keep their unit (e.g. tests/hr).
   Show the substituted numbers, not just the result.
4. **Interpret against a baseline.** Every number gets a "so what": compare to the prior
   period or the without-AI baseline. Productivity Gain and Coding Time Saved *require* a
   without-AI figure — if there isn't one, say so rather than inventing it.
5. **Caveat.** Note proxy weakness (LOC ≠ value), gaming risk, and small-sample noise.
   Pair a productivity metric with an effectiveness one so "faster" isn't hiding "worse".

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
## Inputs          — raw numbers used; mark estimated/missing ones
## Metrics         — each: formula with numbers substituted → result
## Interpretation  — every result vs its baseline, with a "so what"
## Caveats         — proxy weakness, gaming risk, sample size
```

A table of numbers isn't the deliverable — the read on them is.
