---
name: edge-case-hunter
description: Identify edge cases, boundary conditions, and failure modes for a feature, bug fix, workflow, or API. Use when trying to reduce surprises before implementation, review, or release.
---

# Edge Case Hunter

Use this skill to identify what could go wrong around a feature or flow.

## Goals

- Find edge cases that are easy to miss
- Highlight boundary conditions and failure modes
- Improve robustness before implementation or release

## Instructions

1. Understand the feature or flow.
2. Examine it from these angles:
   - empty, null, or missing input
   - invalid input
   - boundary values
   - race conditions or ordering issues
   - stale state
   - partial failure
   - permissions and role mismatches
   - API or network failure
   - retries and duplicate actions
   - unexpected user navigation
   - concurrency or multiple sessions
3. Prefer concrete edge cases over generic warnings.
4. Group cases by area when helpful.

## Output format

### Core flow

- Brief summary of the normal expected behavior

### Edge cases

- Case
- Why it matters
- Expected behavior

### Highest-risk cases

- The few edge cases most likely to cause real bugs

## Constraints

- Do not list trivial or irrelevant cases just to make the list longer
- Do not repeat the same case in different words
- Prefer product-relevant and system-relevant cases
