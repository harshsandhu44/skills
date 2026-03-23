---
name: create-acceptance-criteria
description: Create clear, testable acceptance criteria from a feature, user story, bug fix, or product request. Use when requirements need to be specific enough for engineering, QA, and review.
---

# Create Acceptance Criteria

Use this skill to turn a feature or bug description into testable acceptance criteria.

## Goals

- Make requirements precise and testable
- Clarify expected behavior, edge cases, and constraints
- Help engineering and QA align on done-ness

## Instructions

1. Read the input feature, story, or bug description.
2. Identify:
   - core expected behavior
   - user-visible outcomes
   - validation rules
   - state changes
   - error cases
   - non-goals if implied
3. Write acceptance criteria that are observable and testable.
4. Include edge cases when they materially affect correctness.
5. Keep criteria implementation-neutral unless technical constraints are explicit.

## Preferred format

- Given / When / Then when useful
- Otherwise concise bullet criteria is acceptable

## Output format

### Acceptance criteria

- Criterion 1
- Criterion 2
- Criterion 3

### Edge cases

- Important edge cases or failure conditions

### Non-goals

- Anything intentionally outside scope

## Constraints

- Do not write vague statements like “works correctly”
- Do not hide multiple behaviors in one criterion if they should be separate
- Do not turn implementation details into acceptance criteria unless required
