---
name: review-changed-files
description: Review only files modified in the current branch for bugs, regressions, edge cases, maintainability issues, and missing validation. Use when assessing the quality and risk of branch changes without drifting into unrelated code.
---

# Review Changed Files

Use this skill to review the current branch changes only.

## Goals

- Review only files modified in the current branch
- Identify correctness risks, regressions, edge cases, and maintainability concerns
- Focus on meaningful findings, not cosmetic nitpicks
- Keep the review scoped to changed behavior and directly affected areas

## Scope Rules

### Allowed

- Review modified source files in the current branch
- Review modified tests for quality and gaps
- Mention closely related unchanged files only if necessary to explain a concrete risk

### Not allowed

- Do not review unrelated files
- Do not suggest broad architecture rewrites unless the branch already moves in that direction
- Do not flood the review with minor style comments unless they hide a real problem

## Instructions

1. Inspect the current branch diff first.
2. Identify modified files and the purpose of the change.
3. Review for:
   - correctness issues
   - regression risk
   - missing edge-case handling
   - error handling gaps
   - data validation issues
   - state consistency issues
   - test coverage gaps
   - maintainability concerns in changed code
4. Prefer findings that are specific, actionable, and tied to changed lines or changed behavior.
5. Separate real risks from optional improvements.
6. Keep comments concise and evidence-based.

## Output format

### Summary

- What the branch appears to change
- Overall risk level: low, medium, or high

### Findings

For each finding include:

- Severity: high, medium, or low
- File
- Problem
- Why it matters
- Suggested fix

### Test gaps

- Missing or weak tests related to the changed behavior

### Optional improvements

- Small non-blocking improvements worth considering

## Constraints

- Do not invent issues without code evidence
- Do not comment on untouched code unless directly relevant
- Do not pad the review with generic advice
- Prefer fewer strong findings over many weak ones
