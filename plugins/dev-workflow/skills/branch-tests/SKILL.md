---
name: branch-tests
description: Writes vitest tests for all changed files in the current git branch vs main. Use when the user asks to "write tests for this branch", "add tests for my changes", "test the branch", or "cover the diff". Reads the branch diff, identifies testable units (pure functions, React components, hooks, Zustand stores), and creates or updates co-located test files following the project's vitest + React Testing Library conventions.
---

# branch-tests

## Quick start

Run `/branch-tests` after making changes to generate tests for everything you changed.

## Process

### Step 1 — Identify changed files

```bash
git diff main...HEAD --name-only --diff-filter=ACMR
```

Filter to testable source files only — skip config, types-only files, CSS, and generated files. Focus on:
- `src/lib/**/*.ts` — pure functions → unit tests
- `src/hooks/**/*.ts(x)` — React hooks → render-probe tests
- `src/store/**/*.ts` — Zustand stores → state mutation tests
- `src/components/**/*.tsx` — React components → render + interaction tests

### Step 2 — Read each changed file

For each file: read the full source, then read its existing test file (if any). Understand:
- What the exports do
- Which code paths are new or changed
- Which external modules need mocking

### Step 3 — Determine test file location

Co-locate tests with source: `foo.ts` → `foo.test.ts`, `Bar.tsx` → `Bar.test.tsx`. Never put tests in a separate `__tests__` directory.

### Step 4 — Write the tests

Follow these patterns exactly:

**Pure functions** (`src/lib/**`):
```ts
import { describe, it, expect } from 'vitest'
import { myFn } from './my-fn'

describe('myFn', () => {
  it('does X when Y', () => {
    expect(myFn(input)).toBe(expected)
  })
})
```

**Zustand stores** (`src/store/**`):
```ts
import { describe, it, expect, beforeEach } from 'vitest'
import { useMyStore } from './my-store'

beforeEach(() => useMyStore.setState(useMyStore.getInitialState()))

describe('myAction', () => {
  it('mutates state correctly', () => {
    useMyStore.getState().myAction(arg)
    expect(useMyStore.getState().someField).toBe(expected)
  })
})
```

**React hooks** (`src/hooks/**`):
```ts
import { render } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useMyHook } from './use-my-hook'

// Probe pattern — render a tiny component that calls the hook
function Probe({ onValue }: { onValue: (v: ReturnType<typeof useMyHook>) => void }) {
  onValue(useMyHook())
  return null
}
```

**React components** (`src/components/**`):
```ts
import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { describe, it, expect, vi } from 'vitest'
import MyComponent from './my-component'
```

### Step 5 — Mock rules

- Mock at the module boundary, not inside the call — use `vi.mock(...)` at the top of the file
- Mock Clerk: `vi.mock('@clerk/nextjs', () => ({ useAuth: vi.fn() }))`
- Mock `@xyflow/react` with minimal stubs (see `circuit-edge.test.tsx` for reference)
- Mock Zustand stores that aren't under test with `vi.mock('@/store/foo', () => ({ useFooStore: selector => selector(stubState) }))`
- Never mock internal `@/lib` pure functions — import them directly

### Step 6 — Run and fix

```bash
cd apps/web && pnpm test --run <test-file-path>
```

Fix any failures before reporting done. Only mark a test complete once it passes.

### Step 7 — Report

List each test file created or updated, and the test count added.

## Conventions (this project)

- Framework: **vitest** with `globals: true` (no need to import `describe`/`it`/`expect` if preferred, but explicit imports are fine)
- DOM: **jsdom** environment (configured in `vitest.config.ts`)
- Setup: `@testing-library/jest-dom` matchers auto-imported via `src/test/setup.ts`
- Path alias: `@/` → `apps/web/src/`
- Never write tests for `src/app/**` route files
- `passWithNoTests: true` is set — empty test files do not fail CI
