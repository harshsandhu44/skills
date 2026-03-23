---
name: branch-review
description: Review the current branch holistically by summarizing its intent, changed areas, risk level, test coverage quality, and likely follow-up concerns. Use when preparing a branch for merge or explaining its overall quality.
---

# Branch Review

Use this skill to assess the current branch as a whole.

## Goals

- Summarize what the branch changes
- Evaluate quality and risk at branch level
- Identify gaps in tests, scope, or safety
- Give a concise merge-readiness view

## Instructions

1. Inspect the current branch diff.
2. Determine:
   - primary purpose of the branch
   - major files or areas changed
   - overall complexity and risk
3. Review for:
   - correctness risk
   - missing coverage
   - unclear scope
   - risky assumptions
   - rollout or regression concerns
4. Distinguish blocking issues from non-blocking notes.
5. Keep the assessment concise and practical.

## Output format

### Branch summary

- What the branch does
- Main files or systems affected

### Risk assessment

- Low, medium, or high
- Why

### Merge concerns

- Blocking concerns
- Non-blocking concerns

### Test coverage

- What is covered
- What appears missing

### Recommendation

- Ready to merge, ready with caveats, or not ready
- Why

## Constraints

- Do not turn this into a line-by-line code review
- Do not speculate wildly
- Keep focus on merge readiness and branch-level quality
