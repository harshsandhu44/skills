---
name: reduce-complexity
description: Simplify overly complex code while preserving behavior. Use when a function, component, module, or flow is harder to read, reason about, test, or maintain than necessary.
---

# Reduce Complexity

Use this skill when code is too complex for its job.

## Goals

- Reduce cognitive load
- Preserve behavior
- Improve readability, structure, and maintainability
- Avoid unnecessary rewrites

## Instructions

1. Identify the complexity source.
   - nested conditionals
   - duplicated logic
   - mixed responsibilities
   - unclear naming
   - oversized functions or components
   - unnecessary abstraction
2. Confirm the intended behavior from existing code and tests.
3. Simplify with the smallest effective changes.
4. Prefer:
   - extracting focused helpers
   - flattening control flow
   - removing duplication
   - clarifying names
   - separating responsibilities
5. Keep public behavior unchanged unless explicitly asked otherwise.
6. Update or add tests if needed to preserve confidence.

## Output format

### Complexity assessment

- Where the complexity is
- Why it hurts readability or safety

### Simplification approach

- What was simplified
- Why this approach was chosen

### Changes made

- Structural changes
- Any extracted helpers or renamed units

### Behavior safety

- How existing behavior was preserved
- Relevant tests added or updated

## Constraints

- Do not perform a large rewrite unless clearly justified
- Do not change external behavior without explicit reason
- Do not introduce new abstractions unless they clearly reduce complexity
- Prefer simple local improvements over ambitious redesigns
