---
name: spec-to-plan
description: Convert a vague product idea or feature request into a concrete goal, scope (in/out), acceptance criteria, risks, and a sequenced implementation plan. Use when the user hands you a fuzzy ask ("build notifications", "add billing") and you need a shared, testable definition of done before writing code.
---

# Spec to Plan

A vague request is a trap: you'll build the wrong thing confidently. This skill
forces the idea through a fixed structure so the gaps surface *before* implementation,
not in review.

Produce a single document with the sections below. Keep it tight — a plan nobody
reads is worse than no plan.

## Process

### 1. Restate the goal in one sentence

"This lets **[who]** do **[what]** so that **[why]**." If you can't fill all three
blanks from what the user gave you, that's your first question — ask it. The *why*
is the part people skip and the part that kills scope creep later.

### 2. Draw the scope box

Two columns. **In scope** = what this change must do. **Out of scope** = the adjacent
things a reader might *assume* are included but aren't (other platforms, edge cases,
admin tooling, migrations of old data). Naming the "out" explicitly is what prevents
the "I thought that was part of it" conversation.

### 3. Write acceptance criteria as checks

Each criterion is a sentence that's unambiguously true or false after the work:

- "An unauthenticated request to `POST /x` returns 401."
- "A user who hits the limit sees the upsell modal, not an error."

If a criterion can't be phrased as a check, it's a wish, not a criterion. Aim for
the smallest set that pins down "done".

### 4. List risks and unknowns

What could make this take 3x longer or break in prod? Unknown third-party behavior,
data you haven't seen, a migration on a hot table, an auth model that doesn't fit.
For each, note how you'd de-risk it (spike, read the code, ask someone).

### 5. Sequence the implementation

Order the work so something verifiable exists early (see the `thin-slice` skill for
the vertical-slice technique). Number the steps; for each, name the **verify** check.
Flag steps that are blocked by an unknown from step 4.

## Output shape

```
## Goal
## In scope / Out of scope
## Acceptance criteria   (checkbox list)
## Risks & unknowns       (risk → mitigation)
## Plan                   (numbered steps, each with a verify check)
## Open questions         (anything you had to assume — surface it)
```

End with the **open questions** — every assumption you made to fill a gap. Those are
the things to confirm before anyone writes code.
