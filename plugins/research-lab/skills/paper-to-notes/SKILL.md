---
name: paper-to-notes
description: Distill a paper, article, or technical document into structured notes — core claims, the evidence behind each, caveats and limitations, and concrete ideas for applying it. Use when you need to understand and retain a dense source, or decide whether its findings are worth acting on.
---

# Paper to Notes

A highlighted PDF is not understanding. This skill forces a source through a structure
that separates **what it claims** from **how well it's supported** from **what you'd do
with it** — so you finish with notes you can act on and trust, not a wall of quotes.

## Process

### 1. Capture the frame

Before the details: what question is this source answering, and why does it exist? One
or two sentences. The title, abstract, and conclusion usually give you this — read those
first to know what you're reading for.

### 2. Extract the claims

List the source's **core claims** as plain statements — what it actually asserts to be
true. Strip the hedging and the prose; a claim is something that could be right or wrong.
Distinguish the *central* claim from supporting ones. Aim for the few that matter, not a
summary of every paragraph.

### 3. Attach the evidence to each claim

For each claim, note **what backs it**: the experiment, dataset, sample size, method,
the figure/table, or the citation. A claim with strong evidence and a claim with a
hand-wave should not look the same in your notes. This is the step that turns reading
into evaluation — if you can't find the evidence for a claim, that itself is a note.

### 4. Record the caveats and limitations

What weakens or bounds the claims? Small/biased sample, narrow conditions, correlation-
not-causation, conflicts of interest, results that may not generalize, what the authors
*themselves* flag as limitations (read that section — it's the honest part). Note what
the source conveniently doesn't address.

### 5. Turn it into ideas

The payoff: what would you **do** with this? Implementation ideas, experiments to try,
things to change in your own work, follow-up questions, related sources to chase. Mark
which ideas rest on well-supported claims vs speculative ones.

## Output shape

```text
## Source         (title, author, what question it answers, in one line)
## Core claims    (the central claim first, then supporting)
## Evidence       (per claim: what backs it + how strong)
## Caveats        (limitations, biases, what it doesn't address)
## Ideas          (what to do with it; flagged by claim strength)
## Open questions
```

The test of good notes: months later they tell you not just what the paper said, but
how much to trust it and what to do about it — without re-reading it.
