---
name: competitor-teardown
description: Analyze a competing product across positioning, pricing, target user, UX, feature set, and defensibility (moat) to find gaps and opportunities. Use when sizing up a market, deciding how to differentiate, or before building something that already has incumbents.
---

# Competitor Teardown

"We have no competitors" means you haven't looked. A teardown maps how an existing
product actually works and wins, so you can find the gap you'd exploit instead of
building a worse copy. Be objective — the goal is to learn, not to reassure yourself.

## Process

### 1. Position the product

- **One-line positioning** — how do they describe themselves, and who's the hero? Read
  their homepage hero and category.
- **Target user** — who is this *really* for (segment, size, sophistication)? Often
  narrower than the marketing implies; the pricing and onboarding reveal it.
- **The job** — what job does the customer hire it for? Frame it as the outcome, not the
  feature list.

### 2. Map the offering

- **Core features** — what it does, and which features are the *spine* vs the long tail.
- **What it deliberately doesn't do** — the scoped-out areas are as informative as the
  features; they reveal the bet and the gap.
- **Differentiators** — what they lead with as their edge (speed, integrations, price,
  design, a specific workflow).

### 3. Pricing & business model

- Tiers, what gates each tier, and the **value metric** (per seat, per usage, flat).
- The entry point (free tier, trial) and where the paywall bites.
- What this implies about their target customer and unit economics. Pricing is a
  positioning statement — who they price *out* tells you who they're for.

### 4. UX & product quality

- Onboarding: time-to-value, friction, the "aha" moment.
- Core flow quality: is the main job smooth or clunky? Where do users likely stumble?
- Polish vs depth: is it a beautiful demo or a deep tool? (Their reviews/forums show the
  cracks.)

### 5. Moat & weaknesses

- **Defensibility** — what makes them hard to displace: network effects, data, switching
  costs, integrations, brand, distribution? Or is the moat shallow?
- **Weaknesses** — what do users complain about (pull from reviews, social, support
  threads)? Underserved segments, missing features, pricing resentment, neglected
  platforms.

### 6. The opportunity

Synthesize: where's the gap *you* could win — an underserved user, a better workflow, a
pricing wedge, a platform they ignore? Be specific and honest about whether it's a real
gap or just a feature they'd add in a week.

## Output shape

```text
## Snapshot       (positioning, target user, the job)
## Offering       (spine features, scoped-out areas, differentiators)
## Pricing        (tiers, value metric, what it reveals)
## UX             (onboarding, core flow, polish vs depth)
## Moat           (defensibility — real or shallow)
## Weaknesses     (complaints, underserved segments)
## Opportunity    (the specific gap to exploit, and how durable it is)
```

For sourcing claims about a competitor, delegate to the `evidence-scout` and
`source-skeptic` agents so the teardown rests on facts, not assumptions. Lead with the
opportunity — that's the decision the teardown exists to inform.
