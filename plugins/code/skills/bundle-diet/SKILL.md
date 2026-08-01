---
name: bundle-diet
description: Find and cut JavaScript bundle bloat — heavy dependencies, client/server boundary mistakes, missing code-splitting, and duplicate packages. Use when a web app ships too much JS, has a slow Time-to-Interactive, or you want to shrink the bundle before it grows further.
---

# Bundle Diet

Every kilobyte of JavaScript is downloaded, parsed, and executed on the user's device —
on a mid-range phone that's the difference between snappy and sluggish. This skill finds
what's fat in the bundle and trims it without breaking the app.

## Process

### 1. Measure before cutting

Get a real bundle breakdown — don't guess:

- Build with the analyzer (`webpack-bundle-analyzer`, `vite-bundle-visualizer`,
  `source-map-explorer`, `@next/bundle-analyzer`, `rollup-plugin-visualizer`).
- Note total JS shipped, the largest modules, and **per-route** size (a heavy admin page
  shouldn't tax the landing page).

The visualization tells you where the weight is. Sort by size and start at the top.

### 2. Attack the heavy dependencies

The usual offenders:

- **Whole-library imports** — `import _ from 'lodash'` pulls the entire library; import
  the function (`lodash-es` + named import, or `lodash/get`). Same for `date-fns`,
  icon packs, and UI kits.
- **Oversized libraries** — moment.js (→ `date-fns`/`dayjs`), full `chart.js` for one
  chart, a 100KB animation lib for a fade. Check if a lighter equivalent or a few lines
  of your own would do.
- **Duplicate packages** — two versions of the same lib pulled by different deps. Dedupe
  the lockfile; check for multiple React/copies.
- **Polyfills you don't need** — shipping legacy polyfills to modern browsers. Check the
  browserslist target.

### 3. Fix the client/server boundary

In an SSR/RSC framework, the most expensive mistake is shipping server-only code to the
client:

- Code marked client (`"use client"`, or imported into a client component) that didn't
  need to be — it and its dependencies now ship to the browser.
- Heavy libraries (markdown parsers, syntax highlighters, validation schemas, SDKs) used
  only to render — keep them on the server.
- Pull the client/server line as tight as possible; a single misplaced import can drag a
  large dependency across it.

### 4. Split and defer

- **Route-level code-splitting** — each route loads only its own JS.
- **Dynamic import** for below-the-fold or interaction-gated components (modals, editors,
  charts): `const X = lazy(() => import(...))`.
- **Defer third-party scripts** (analytics, chat widgets) — load after interactive, not
  blocking it.

### 5. Re-measure

Rebuild the analyzer and confirm the number actually dropped. A "diet" with no
before/after is a guess. Watch that you didn't just move weight to a different route.

## Output shape

```text
## Baseline        (total + per-route JS, largest modules)
## Findings        (per item: what's heavy → the cut, est. savings)
## Boundary fixes  (code wrongly shipped to the client)
## Splitting       (what to dynamic-import / defer)
## Result          (before → after numbers)
```

Prioritize by bytes-on-the-critical-path: a 40KB cut on the landing page beats a 200KB
cut on a rarely-visited settings screen.
