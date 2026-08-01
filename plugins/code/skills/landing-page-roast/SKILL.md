---
name: landing-page-roast
description: Brutally review a landing or product page for conversion — clarity of the value proposition, hero, call-to-action, page structure, friction, trust, and the performance that affects bounce. Use when a landing page isn't converting or before launching one, and you want an honest critique rather than reassurance.
---

# Landing Page Roast

This is a conversion roast, not a copyedit — it judges whether the page *makes a visitor
act*: structure, message hierarchy, friction, trust, and the load speed that decides
whether they stay at all. (For line-by-line copy clarity, that's the `copy-roaster`
agent's job — this skill is about the page as a conversion machine.)

Be honest, not kind. A page told "looks great" learns nothing.

## Process

### 1. The 5-second test

Land on the page cold. In five seconds, can you answer:

- **What is this?** (the product/offer)
- **Who is it for?**
- **What do I do next?** (the action)

If any answer is unclear, that's the headline finding — everything else is secondary.
Most landing pages fail right here: a clever tagline that says nothing, a hero that
describes the company instead of the visitor's outcome.

### 2. Hero & value proposition

- The headline states a **benefit/outcome**, not a feature or a slogan. "Ship faster"
  beats "Next-gen synergy platform".
- The subhead clarifies and adds specificity; together they pass the 5-second test.
- There's a primary **CTA above the fold**, visually dominant, with action-specific text
  ("Start free trial" not "Submit").
- A supporting hero visual that shows the product/outcome, not a generic stock photo.

### 3. Page structure & flow

- One **primary** conversion goal; the page funnels toward it. Competing CTAs dilute.
- Logical narrative: hook → problem → solution → proof → objection-handling → CTA.
- Scannable — headings, short blocks, whitespace. Walls of text don't get read.
- The CTA repeats at natural decision points (after benefits, after proof, at the end).

### 4. Friction & objections

- The form asks for the **minimum** needed; every extra field costs conversions.
- Obvious objections are pre-empted (price, "is it for me?", "how hard to switch?",
  commitment/lock-in).
- No dead ends, confusing navigation, or surprise gates.

### 5. Trust

- Social proof that's **specific** — real logos, named testimonials, concrete numbers —
  not "trusted by thousands".
- Credibility signals where they matter (security/privacy near sign-up, guarantees near
  price).

### 6. Performance & mobile (bounce killers)

- **Load speed** — a slow LCP means visitors leave before they read a word; the best copy
  can't convert a closed tab. (Measure with the `web-perf` skill.)
- **Mobile** — most traffic is mobile: is the hero/CTA usable, is text readable without
  zoom, do tap targets work, is the form painless on a phone?
- No layout shift bouncing the CTA as the page loads.

## Output shape

```text
## 5-second verdict   (could you tell what/who/next? — the core diagnosis)
## Hero & value prop   (headline, subhead, CTA, visual)
## Structure & flow
## Friction            (form fields, objections, dead ends)
## Trust               (proof quality)
## Performance/mobile  (load + mobile issues that cause bounce)
## Top 3 fixes         (ranked by likely conversion impact)
```

End with the **top 3** changes most likely to move conversion — ruthlessly prioritized.
A roast that lists 30 equal issues is just noise; name the three that matter.
