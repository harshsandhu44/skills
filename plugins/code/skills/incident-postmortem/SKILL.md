---
name: incident-postmortem
description: Write a blameless incident postmortem — timeline, impact, root cause, contributing factors, and concrete action items with owners. Use after an outage, regression, or production incident when you need a write-up that drives real fixes instead of assigning blame.
---

# Incident Postmortem

A postmortem exists to make the *system* less likely to fail the same way again — not
to find who to blame. Blameless framing isn't politeness; it's what gets people to tell
you what actually happened. This skill produces a write-up that turns an incident into
durable improvements.

## Process

### 1. Establish the facts before the analysis

Pull the objective record first — deploy logs, alert timestamps, dashboards, chat
history, PR/commit history around the incident. The timeline is built from these, not
from memory. Separate **what happened** (facts) from **why** (analysis); don't blur
them.

### 2. Build the timeline

A chronological list with timestamps (and timezone):

- When the triggering change/condition landed.
- When it started affecting users.
- When it was **detected** (and how — alert? customer report? the gap between
  "started" and "detected" is itself a finding).
- Key actions during response.
- When it was mitigated, and when fully resolved.

### 3. Quantify the impact

Be specific and honest: who was affected, how many, for how long, and how badly
(errors, data loss, degraded performance, money). "Some users saw errors" is useless;
"~4% of checkout requests failed for 38 minutes" drives the right urgency.

### 4. Find the root cause — and the contributing factors

The trigger is rarely the whole story. Use "5 whys" or similar to get past the
proximate cause to the systemic one: not "the bad query shipped" but "there was no load
test that would have caught it, and the rollback took 20 minutes because…". List:

- **Root cause** — the core technical reason.
- **Contributing factors** — what let it happen, what made it worse, what slowed
  detection or recovery. These are blameless: "the runbook was out of date", not
  "X forgot the runbook".

### 5. Action items that are real

Each action item must have an **owner**, a **concrete deliverable**, and ideally a due
date. "Be more careful" is not an action item. Good ones: "add a migration-lock check
to CI (owner: A)", "alert on checkout error rate >1% (owner: B)". Distinguish *prevent
recurrence* from *detect faster* from *recover faster* — aim for at least one of each.

### 6. Keep it blameless

Describe decisions in terms of the information available *at the time*. Replace names-
as-causes with system-as-cause. If a human action contributed, the fix is the guardrail
that makes that action safe, not the reprimand.

## Output shape

```text
## Summary          (2–3 sentences: what, impact, status)
## Impact           (who/how many/how long/how bad)
## Timeline         (timestamped, detection gap visible)
## Root cause
## Contributing factors
## What went well    (response things worth keeping)
## Action items     (owner · deliverable · prevent/detect/recover · due)
```

The test of a good postmortem: six months later, the action items shipped and the same
failure can't happen the same way.
