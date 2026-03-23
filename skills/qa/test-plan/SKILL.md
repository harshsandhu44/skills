---
name: test-plan
description: Create a practical test plan for a feature, bug fix, or release by identifying critical scenarios, risks, edge cases, and validation areas. Use when planning QA coverage before or during implementation.
---

# Test Plan

Use this skill to define practical testing coverage for a change.

## Goals

- Identify the most important things to validate
- Cover primary flows, edge cases, regressions, and failure conditions
- Keep the test plan realistic and prioritized

## Instructions

1. Understand the feature, fix, or release scope.
2. Identify:
   - main user flows
   - critical business logic
   - validation rules
   - integrations
   - permissions or role-based behavior
   - regression risks
3. Create a prioritized test plan.
4. Separate must-test paths from lower-priority coverage.
5. Include dependencies, data setup, or environment assumptions where relevant.

## Output format

### Scope

- What is being tested

### Priority scenarios

- Highest-risk or highest-value scenarios

### Functional tests

- Main expected behaviors

### Edge cases

- Important boundary and failure cases

### Regression risks

- Areas likely to break because of the change

### Test data / setup

- Required setup, fixtures, environments, or accounts

## Constraints

- Do not produce a giant unprioritized checklist
- Do not ignore role, permissions, or integration effects when relevant
- Focus on meaningful coverage over quantity
