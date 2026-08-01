---
name: debug-ladder
description: Debug a defect systematically — reproduce, isolate, instrument, hypothesize, fix, and add a regression test — instead of guessing and changing code at random. Use when facing a bug whose cause isn't obvious, an intermittent failure, or a "works on my machine" report.
---

# Debug Ladder

Random changes ("try this, try that") sometimes work and always teach you nothing —
and often introduce a second bug. The ladder is a fixed sequence of rungs; you don't
skip a rung, and you don't change code until you've climbed to a hypothesis you can
test.

## Process

### 1. Reproduce — reliably

You cannot fix what you can't trigger. Find the smallest, most reliable reproduction:
exact input, environment, sequence of steps. If it's intermittent, find what raises the
hit rate (load, timing, a specific record). **No repro → stop and get one** (logs, a
failing user's data, a stress loop). A bug you "fixed" without a repro isn't fixed; you
just stopped looking.

### 2. Isolate — shrink the surface

Cut the problem space in half repeatedly. Which layer — client, network, server, DB?
Bisect: does it fail on an older commit (`git bisect`)? Remove inputs until it stops
failing — the last thing you removed is implicated. Disable half the code path. The
goal is to corner the bug into the smallest region that still reproduces it.

### 3. Instrument — make the invisible visible

Now, and only now, add observability *inside the isolated region*: log the actual
values at the boundary, assert the invariant you believe holds, inspect state in a
debugger. You're collecting evidence, not fixing. The bug is almost always a gap
between what you *assume* is true here and what *is* true. Print both.

### 4. Hypothesize — state the cause out loud

Write one sentence: "The bug is X because Y." A good hypothesis predicts something you
haven't checked yet ("if this is it, then value Z will be wrong too"). Verify the
prediction. If it holds, you've found it; if not, your hypothesis is wrong — back to
instrument, don't patch the symptom.

### 5. Fix — the cause, not the symptom

Fix the root cause. If you're tempted to add a null-check at the crash site, ask *why*
it's null — that's usually the real bug, upstream. A fix that only suppresses the
symptom relocates the bug; it doesn't remove it.

### 6. Regression test — lock it shut

Write a test that **fails before your fix and passes after**. This proves the fix works
*and* stops the bug from coming back. Run it against the unfixed code (revert mentally
or with stash) to confirm it actually catches the bug. A debug session without a
regression test is unfinished.

## Output shape

```
## Repro            (exact steps; reliability %)
## Isolation        (how the surface was narrowed; the implicated region)
## Evidence         (instrumented values vs expected)
## Root cause       (one sentence; the verified hypothesis)
## Fix              (what changed and why it's the cause not the symptom)
## Regression test  (the test that now guards it)
```

If you get stuck on a rung for too long, the usual reason is you skipped the rung
below it — go back down.
