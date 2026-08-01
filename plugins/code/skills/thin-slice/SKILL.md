---
name: thin-slice
description: Break a feature into vertical slices (tracer bullets) that each cut through every layer — UI to DB — and ship something usable, instead of building horizontal layers that integrate only at the end. Use when a feature is large enough that a big-bang implementation risks weeks of work before anything runs end to end.
---

# Thin Slice

The failure mode this prevents: building the whole database layer, then the whole API
layer, then the whole UI, and discovering at integration time that the pieces don't
fit — with no working software until the very end.

A **vertical slice** instead does the *narrowest possible* path through all layers, end
to end, so you have running, demoable software early and integrate continuously.

## Process

### 1. Find the spine

What's the one user action at the heart of this feature? "Send a message." "Create an
invoice." "Search a product." That action, done once, for the simplest possible input,
is your first slice — the **tracer bullet**.

### 2. Make slice one embarrassingly thin

The first slice should feel almost too small. One hardcoded value is fine. No edge
cases, no validation beyond what stops a crash, one happy path. The goal is to prove
the wiring through every layer works — request reaches the DB and a result comes back
to the screen. If slice one takes more than a day, it's still too fat.

### 3. Grow by adding slices, not layers

Each subsequent slice adds *behavior the user can see*, not internal plumbing:

- Slice 1: send a message with fixed text, see it appear.
- Slice 2: type your own text.
- Slice 3: validation + error states.
- Slice 4: edit / delete.

Each slice is independently shippable and independently testable. Contrast with the
horizontal trap: "build all the models" is not a slice — nobody can use it.

### 4. Defer the cross-cutting concerns deliberately

Auth, pagination, i18n, accessibility polish, retries — note where each will slot in,
but don't let them block slice one unless a slice is genuinely unusable without them.
Write down the deferral so it isn't forgotten.

## Output shape

```
## Spine            (the one core action)
## Slices           (ordered list; each = a user-visible capability + its verify check)
## Deferred         (cross-cutting concerns, and which slice they attach to)
```

The test of a good slice list: you could stop after any slice and have shipped
something real, just less complete. If stopping early leaves a non-functional stub,
re-cut the slices.
