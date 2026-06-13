---
name: mvp-scope-cut
description: Ruthlessly cut a feature set down to the smallest thing that delivers the core value, so you ship and learn instead of building a cathedral nobody asked for. Use when a plan, backlog, or spec has grown large and you need to decide what to drop, defer, or fake before building.
---

# MVP Scope Cut

The default gravity of every project is *more*: more cases, more polish, more config,
more "while we're in here". This skill applies the opposite force. The question is never
"could we build this?" — it's "what can we *not* build and still deliver the core value?"

## Process

### 1. Name the one job

What's the single job the user hires this feature to do? Everything is justified by that
job or it's a candidate to cut. If you can't name one job, the scope is the problem —
the feature is actually several features wearing a trenchcoat; split it first.

### 2. Sort every item into MUST / LATER / NEVER

Go through the list and force each item into one bucket — no "should":

- **MUST** — the core job genuinely doesn't work without it. Be stingy; most "musts"
  are "wants" in disguise. Test: if you removed it, would a user say "this is broken"
  or merely "I wish it also did X"? Only the first is a MUST.
- **LATER** — real value, but the feature ships and delivers without it. Park it with a
  one-line note so it's not lost.
- **NEVER** — speculative, edge-case, or scope creep. Say so plainly. Writing "never"
  down is what stops it creeping back in next sprint.

### 3. Fake what you can't cut

For MUSTs that are expensive, ask if the *manual or hardcoded* version is good enough to
launch:

- Admin does it by hand instead of a self-serve UI.
- A config file instead of a settings screen.
- A scheduled batch instead of real-time.
- One hardcoded plan instead of a pricing engine.

"Do things that don't scale" is a launch strategy, not a shortcut. Faking buys you the
learning without the build.

### 4. Pressure-test the cut

Walk the core job end to end using only the MUSTs (plus fakes). Does it hold together
and deliver value? If yes, you're done — stop adding. If a gap breaks the job, the
smallest patch for *that gap* graduates from LATER to MUST. Nothing else.

## Output shape

```
## The one job
## MUST       (with the "is it broken without it?" justification)
## LATER      (parked, one line each)
## NEVER      (named explicitly, so it stays dead)
## Fakes      (expensive MUSTs replaced by a manual/hardcoded stand-in for v1)
```

The deliverable is a smaller plan than you started with. If it isn't smaller, you
haven't cut — you've just re-sorted.
