---
name: threat-model
description: Run a lightweight STRIDE-style threat model on a feature or design — enumerate assets, entry points, and trust boundaries, then walk threats and pick mitigations. Use when designing something security-sensitive (auth, payments, file upload, multi-tenant data) and you want the attack surface mapped before building.
---

# Threat Model

You can't defend an attack surface you haven't drawn. This is a fast, structured pass —
not a formal audit — that surfaces the threats worth designing against *before* code
exists, when fixing them is free.

## Process

### 1. Draw the system

Sketch the data flow for the feature: the components, who/what talks to what, and where
data is stored. Mark the **trust boundaries** — every line where data crosses from less-
trusted to more-trusted (internet → server, user → admin, tenant A → tenant B, app →
database). Threats live on these boundaries.

### 2. List assets and entry points

- **Assets** — what an attacker wants: user data, credentials, money, PII, the ability
  to act as someone else, compute.
- **Entry points** — where untrusted input enters: endpoints, forms, file uploads,
  webhooks, query params, headers, message queues.

### 3. Walk STRIDE at each entry point / boundary

For each entry point, ask the six questions; skip the ones that don't apply:

- **S**poofing — can someone pretend to be another user/service? (authentication)
- **T**ampering — can data be modified in transit or at rest? (integrity, validation)
- **R**epudiation — can an action be denied later? (audit logging)
- **I**nformation disclosure — can data leak to someone who shouldn't see it?
  (authorization, error messages, IDOR, tenant isolation)
- **D**enial of service — can it be overwhelmed or made expensive? (rate limits, quotas)
- **E**levation of privilege — can a user gain rights they shouldn't have? (authz,
  injection, deserialization)

For each real threat, write it as "an attacker could **X** by **Y**".

### 4. Rate and mitigate

For each threat, a rough **likelihood × impact**, then the mitigation: validate input,
authorize the action, scope by tenant, rate-limit, encrypt, log, etc. Decide which to
**fix now**, which to **accept** (with a stated reason), and which to **defer** (tracked).

## Output shape

```text
## System & trust boundaries   (the data-flow sketch + boundary lines)
## Assets / entry points
## Threats                     (STRIDE; each = "attacker could X by Y")
## Mitigations                 (per threat: fix now / accept / defer + the control)
## Top risks                   (the 3 that matter most)
```

Don't boil the ocean — a focused model of the riskiest boundary beats an exhaustive one
nobody finishes. The companion skills `auth-boundary-review` and `rate-limit-review`
drill into the two most common gaps this turns up.
