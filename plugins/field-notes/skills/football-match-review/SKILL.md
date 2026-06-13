---
name: football-match-review
description: Produce a tactical football (soccer) match review — formations and game plan, an xG-style read of the chances, player roles and key performers, and the turning points that decided the result. Use when reviewing a match analytically rather than just recapping the score.
---

# Football Match Review

The scoreline lies more often in football than in almost any sport — a 1-0 can be a
smash-and-grab or a stroll. This skill reviews *how* the game was actually played and
won, beyond the result.

Work from what's known — the result, formations, key moments, the run of play. Where you
don't have data (exact xG figures, possession stats), reason qualitatively and say so
rather than fabricating precise numbers.

## Process

### 1. Result & overall read

The score, then the honest one-line summary: deserved win, smash-and-grab, dominant
performance that the scoreline flatters or undersells, a game decided by a single moment
or by sustained control.

### 2. Setup & tactics

- **Formations** and how each side actually lined up (shape out of possession often
  differs from the nominal formation).
- **Game plans** — who tried to control possession, who sat deep and countered, who
  pressed high. Did the plans clash or cancel out?
- **Key tactical battles** — the matchups that mattered (a winger vs a full-back, the
  midfield battle, how one side's press broke the other's build-up).
- **In-game changes** — substitutions and tweaks that shifted momentum, and whether they
  worked.

### 3. Chances & an xG-style read

Without necessarily having the numbers, assess the *quality* of chances, not just the
count:

- Who created the better openings, and from where (open play, set pieces, transitions)?
- Did the scoreline match the balance of clear chances, or did finishing / goalkeeping
  distort it?
- Big misses, big saves, and the moments that "should" have been goals.

### 4. Players & roles

- **Key performers** — who controlled the game or decided it, and *how* (not just who
  scored).
- **Roles** — how individuals were used (a false 9, an inverted full-back, a deep
  playmaker) and whether it worked.
- **Underperformers** — who struggled or got exposed, and why.

### 5. Turning points

The 2–3 moments that swung it: a goal against the run of play, a red card, a missed
penalty, a tactical switch, an injury. For each, what it changed.

## Output shape

```text
## Result & read         (score + honest one-line summary)
## Tactics               (formations, game plans, key battles, subs)
## Chances               (xG-style quality read; did the score reflect play?)
## Players & roles       (key performers, how they were used, who struggled)
## Turning points        (the moments that decided it)
```

Lead with the tactical *why*. A good review explains how the result happened — anyone can
read the score.
