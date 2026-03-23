---
name: implement-from-ticket
description: Implement a feature or fix from ticket text by extracting requirements, inferring local conventions from the repository, keeping scope tight, and delivering the smallest complete solution. Use when working from Jira, Linear, GitHub issue, or similar ticket content.
---

# Implement From Ticket

Use this skill when implementing work from a ticket or issue.

## Goals

- Extract the real requirements from the ticket
- Keep implementation scope tight
- Match repository architecture and conventions
- Deliver the smallest complete solution that satisfies the ticket

## Instructions

1. Read the ticket carefully.
2. Extract:
   - problem or requested behavior
   - explicit requirements
   - constraints
   - non-goals if present
3. Inspect nearby code to infer:
   - architecture patterns
   - file placement
   - naming conventions
   - existing helpers and utilities
4. Identify ambiguous parts and resolve them conservatively using repository context.
5. Implement only what is needed for the ticket.
6. Add or update tests if appropriate.
7. Summarize what was implemented and any assumptions made.

## Decision rules

- Prefer local patterns over generic best practices
- Prefer the smallest working change
- If the ticket is ambiguous, choose the narrowest reasonable interpretation
- Do not expand scope just because related improvements are tempting

## Output format

### Ticket interpretation

- Problem being solved
- Requirements implemented
- Assumptions made

### Implementation plan

- Files to create or modify
- Key approach

### Changes made

- Code changes
- Test changes

### Notes

- Anything intentionally left out because it was outside ticket scope
- Risks or follow-ups

## Constraints

- Do not implement speculative extras
- Do not refactor unrelated code
- Do not invent requirements that are not supported by ticket or codebase context
