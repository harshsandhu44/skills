---
name: write-tests
description: Write or update tests only for files modified in the current branch. Use the repository’s existing testing library, helpers, conventions, and file patterns. Do not add or modify tests for untouched files unless a directly related shared test helper must be adjusted.
allowed-tools: Read, Grep, Glob, Edit, MultiEdit, Bash(npm test:*), Bash(bun test:*), Bash(pnpm test:*), Bash(yarn test:*)
---

# Write Tests For Modified Files Only

Use this skill when you need to add or update automated tests for work already changed in the current branch.

## Goals

- Only write or modify tests for files changed in the current branch
- Use the testing tools and conventions already present in the repository
- Keep test changes tightly scoped to the branch diff
- Add the smallest useful set of tests that gives meaningful coverage

## Scope Rules

You must scope all work to the current branch diff.

### Allowed

- Add or update tests for source files modified in the current branch
- Update an existing nearby test file when it covers behavior changed in the current branch
- Create a new test file for a modified source file if no suitable one exists
- Make a very small related change to a shared test helper only if it is required to test a modified file in the branch

### Not allowed

- Do not add tests for files that were not modified in the current branch
- Do not clean up unrelated tests
- Do not refactor unrelated test suites
- Do not broaden coverage outside the changed behavior just because it seems nice
- Do not modify production files unless the smallest possible change is required for testability of a modified file

If a useful test would require touching unrelated files, stop and explicitly say so instead of making broad changes.

## Instructions

1. Inspect the current branch diff first.
   - Identify modified source files
   - Identify modified test files already in the branch
   - Limit all planned test work to those changed files and their directly associated tests

2. Inspect the repository’s current testing setup.
   - Determine the test runner already in use
   - Determine assertion style, mocking utilities, setup files, fixtures, factories, and helper utilities
   - Look first at tests nearest to each modified file

3. Reuse existing conventions.
   - Do not introduce a new testing library if one already exists
   - Do not switch assertion style or mocking style
   - Match existing file suffixes, folder placement, naming, and structure
   - Prefer updating a nearby existing test file when it directly covers a modified file

4. Test changed behavior only.
   - Cover the happy path introduced or affected by the modified file
   - Cover important edge cases caused by the change
   - Add regression coverage for bugs fixed in the modified file
   - Avoid asserting private implementation details unless that is already the repo convention

5. Keep tests deterministic.
   - Avoid flaky timing-based assertions unless the repository already uses a stable pattern
   - Reuse existing setup helpers, render helpers, mocks, fixtures, factories, or database utilities

6. Keep production changes minimal.
   - Only make the smallest necessary code change if a modified file is otherwise untestable
   - Clearly explain any production-code change made for testability

7. Verify before finishing.
   - Check imports and file paths
   - Run only the relevant tests first when possible
   - Fix failures before concluding

## Workflow

Follow this sequence:

1. Get the list of files changed in the current branch
2. Filter to the modified files that need test coverage
3. Inspect nearby tests and shared test setup
4. Decide whether to update an existing test file or create a new one
5. Write the smallest useful set of tests for the changed files only
6. Run relevant tests
7. Fix failures
8. Summarize what was changed and why it stayed in scope

## Output format

Structure your response like this:

### Branch scope

- Modified files considered
- Tests created or updated for those files only
- Any file intentionally skipped because it was outside scope

### Testing approach

- Testing library and helpers found
- Where tests were added
- What changed behavior is covered

### Changes made

- Test files created or modified
- Any minimal production-code changes made for testability

### Test cases covered

- Happy path
- Edge cases
- Regression coverage

### Notes

- Anything intentionally not tested because it would require touching unrelated files
- Any assumptions made because repository context was incomplete

## Constraints

- Do not add a new test framework if one already exists
- Do not modify tests unrelated to modified files in the current branch
- Do not rewrite unrelated tests
- Do not broad-refactor code just to make tests prettier
- Do not replace local conventions with preferred conventions
- Do not add unnecessary comments unless that is already standard in the repo

## Decision rules

When choosing whether a test file is in scope, use these rules:

- In scope: a test file directly covering a source file modified in the branch
- In scope: a new test file for a modified source file
- In scope only if necessary: a tiny change to a shared test helper required to test a modified file
- Out of scope: any test file changed only for cleanup, style consistency, or opportunistic extra coverage
- Out of scope: tests for neighboring modules not modified in the branch

When uncertain, choose the narrower scope and state the limitation explicitly.
