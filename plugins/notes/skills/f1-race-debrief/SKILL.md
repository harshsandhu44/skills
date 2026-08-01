---
name: f1-race-debrief
description: Produce a structured Formula 1 race debrief — strategy and tyre stints, key on-track events, driver and team performance, and what decided the result. Use when reviewing a Grand Prix and you want an analytical breakdown rather than a bare results list.
---

# F1 Race Debrief

A results table tells you *who* won; a debrief tells you *why*. This skill structures a
race into the strategy, the moments, and the performances that actually decided it.

Work from what's known — results, the strategy, the key incidents. If you're missing
specifics, say so rather than inventing lap-by-lap detail; a debrief built on made-up
numbers is worse than a short honest one.

## Process

### 1. The result & the headline

Podium and key classified positions, then the one-sentence story of the race: was it a
lights-to-flag control, a strategy gamble that paid off, a chaotic wet race, a late
safety car that reshuffled everything? Lead with what made *this* race what it was.

### 2. Strategy & tyre stints

The analytical core:

- **Stint breakdown** — compounds and approximate stint lengths for the front-runners;
  one-stop vs two-stop and who committed to which.
- **The strategic battle** — undercuts and overcuts that worked or failed, who pitted
  under a safety car / VSC and gained, who got stuck in traffic.
- **Tyre management** — who looked after their rubber and who fell off the cliff; where
  degradation decided track position.

### 3. Key events

Chronological turning points: the start and turn-1, major overtakes, safety cars / VSCs
and how they swung the order, penalties, DNFs, weather changes, team-radio flashpoints.
For each, note *what it changed*.

### 4. Driver & team performance

- **Standouts** — best drive of the day (not always the winner), best overtake, best
  recovery from a poor grid slot.
- **Underperformers** — who lost out, and was it the driver, the car, or the pit wall?
- **Teammate comparisons** — same machinery, different result is the cleanest read on
  driver form.
- **Car/team pace** — who had the legs, and on which tyre/phase.

### 5. What decided it

Synthesize: the two or three factors that actually settled the result — a strategy call,
a first-lap gain, a safety-car lottery, raw pace. And the championship implication, if
relevant.

## Output shape

```text
## Result & headline
## Strategy & stints     (compounds, stop count, the key undercut/overcut)
## Key events            (chronological turning points + what each changed)
## Performances          (standouts, underperformers, teammate reads)
## What decided it       (the 2–3 deciding factors + title implications)
```

Keep it analytical and specific. The value is in the *why* — strategy and the decisive
moments — not in re-listing the finishing order.
