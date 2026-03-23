---
name: debug-issue
description: Debug an issue systematically by identifying reproduction steps, tracing likely code paths, forming grounded hypotheses, and proposing or implementing the smallest safe fix. Use when investigating a bug, failure, or unexpected behavior.
---

# Debug Issue

Use this skill when debugging a bug, failure, or unexpected behavior.

## Goals

- Understand the issue before changing code
- Trace likely code paths and failure points
- Form grounded hypotheses and verify them
- Prefer the smallest safe fix that addresses root cause

## Instructions

1. Start by clarifying the issue from available context.
   - expected behavior
   - actual behavior
   - affected area
   - user-visible impact
2. Try to identify or infer reproduction steps.
3. Inspect relevant code paths, logs, state transitions, API contracts, and recent changes.
4. Form a small number of plausible root-cause hypotheses.
5. Test or validate hypotheses using repository evidence.
6. Identify the most likely root cause.
7. Propose or implement the minimal safe fix.
8. Add or update tests if appropriate.

## Debugging principles

- Do not jump to code changes before narrowing the cause
- Do not treat symptoms as root cause
- Prefer repository evidence over assumptions
- Check nearby tests, error handling, and data shape assumptions
- Consider regressions from recent changes first

## Output format

### Issue framing

- Expected behavior
- Actual behavior
- Affected area

### Likely reproduction

- Reproduction steps or best available approximation

### Investigation

- Relevant files or code paths inspected
- Key observations
- Hypotheses considered

### Root cause

- Most likely root cause
- Why it is the best explanation

### Fix

- Minimal proposed or applied fix
- Why it should work

### Follow-up

- Recommended test coverage
- Any remaining uncertainty

## Constraints

- Do not make broad speculative rewrites
- Do not claim certainty without evidence
- If reproduction is incomplete, say so clearly
- Prefer minimal safe fixes over large cleanups
