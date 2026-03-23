---
name: pr-description
description: Write a clear pull request description from branch changes, commit history, ticket text, or notes. Use when preparing a PR for reviewers and you want a concise, useful summary with context, scope, risks, and test notes.
---

# PR Description

Use this skill to write a clean pull request description.

## Goals

- Help reviewers understand what changed and why
- Summarize scope without dumping the whole diff
- Highlight risks, testing, and important context
- Keep the PR description readable and useful

## Instructions

1. Inspect the branch diff, commit history, or provided notes.
2. Identify:
   - problem being solved
   - main code changes
   - scope boundaries
   - risks or tricky parts
   - test coverage or validation done
3. Write a concise description aimed at reviewers.
4. Mention follow-ups only if relevant.

## Output format

### Summary

- What this PR changes and why

### Changes

- Key implementation changes

### Risk areas

- Areas reviewers should inspect carefully

### Testing

- Tests added, updated, or run
- Manual validation if relevant

### Notes

- Any assumptions, non-goals, or follow-up work

## Constraints

- Do not narrate every changed file
- Do not hide risky changes
- Do not write vague filler like “misc fixes”
- Keep it reviewer-friendly
