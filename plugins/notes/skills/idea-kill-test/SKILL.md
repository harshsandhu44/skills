---
name: idea-kill-test
description: Stress-test a product idea before building it — try hard to kill it on problem, demand, differentiation, reachability, and economics, so only ideas that survive get built. Use when you're tempted to start coding a new product or feature and want an honest go/no-go instead of motivated reasoning.
---

# Idea Kill Test

The most expensive way to test an idea is to build it. This skill tries to **kill the
idea on paper** first — because an idea that dies to a few hard questions would have died
in the market too, just months and a lot of code later. Adopt the mindset of a skeptic
who wants the idea to fail; the ones that survive that are worth your time.

## Process

Run the idea through each gate. A clear failure at any gate is a kill (or a pivot) — be
honest about which gates it actually passes versus which you're hand-waving.

### 1. Problem — is it real and painful?

Is there a genuine problem, felt by real people, *frequently* and *acutely*? Vitamin or
painkiller? Many ideas solve a problem nobody loses sleep over. **Kill signal:** you
can't name a specific person who has this problem badly, or "the problem" is really just
"my solution would be neat".

### 2. Demand — does anyone want *this*?

Do people currently hack together a workaround, pay for an alternative, or actively
search for a fix? Existing spend and ugly workarounds are demand signals; their absence
is a warning. **Kill signal:** the only evidence of demand is your own enthusiasm.

### 3. Differentiation — why you, why this?

What exists already (including "spreadsheet + duct tape" and "do nothing")? Why would
someone switch to this? **Kill signal:** your edge is a feature an incumbent could copy
in a week, or your honest answer is "ours is a bit nicer". (The `competitor-teardown`
skill feeds this gate.)

### 4. Reachability — can you get to customers?

Even a great product dies if you can't reach buyers affordably. Is there a channel —
and can you afford it relative to what a customer is worth? **Kill signal:** the plan is
"we'll do marketing" with no specific, affordable channel.

### 5. Economics — does the math work?

Roughly: what can you charge, what does it cost to deliver and to acquire a customer, and
is there a believable path to it being worth it? **Kill signal:** the price people will
pay is below the cost to serve them, or you need millions of users at $0 to work. (Hand
this to the `market-sizer` agent for a sharper pass.)

### 6. The honest verdict

Tally the gates. **Build / pivot / kill.** If it passed, name the *riskiest surviving
assumption* and the cheapest experiment to test it (a landing page, ten customer
conversations, a concierge MVP) — before writing code.

## Output shape

```text
## The idea         (one sentence)
## Problem          (real & painful? — verdict + why)
## Demand           (evidence it's wanted? — verdict)
## Differentiation  (why you/why this? — verdict)
## Reachability     (a real channel? — verdict)
## Economics        (does the math work? — verdict)
## Verdict          (build / pivot / kill)
## Riskiest assumption + the cheapest test for it   (if not killed)
```

The point is not to be negative — it's to fail cheaply. An idea that survives a genuine
attempt to kill it is far more worth building than one you only ever cheered for.
