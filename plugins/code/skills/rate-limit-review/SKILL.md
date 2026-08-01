---
name: rate-limit-review
description: Check API endpoints and actions for abuse prevention — rate limits, quotas, and protection on expensive or sensitive operations like auth, search, and resource creation. Use when reviewing an API for denial-of-service, brute-force, or cost-amplification risk, or when designing limits for a new endpoint.
---

# Rate Limit Review

An endpoint with no limit is a free lever for an attacker: brute-force a login, scrape
a dataset, run up your cloud bill, or knock the service over. This skill finds the
endpoints that need a limit and checks the ones that have one are actually effective.

## Process

### 1. Find the operations that need protecting

Not everything needs the same limit, but these categories almost always need one:

- **Authentication** — login, password reset, OTP/2FA, token refresh. Unlimited =
  brute-force and credential-stuffing.
- **Expensive operations** — search, report generation, exports, anything that fans out
  to many DB queries or calls a paid third-party API (LLM calls, SMS, email).
- **Resource creation** — sign-up, posting, uploads, invites. Unlimited = spam and
  storage abuse.
- **Enumeration-prone reads** — endpoints that confirm whether something exists (a user,
  a coupon) and could be scraped.

### 2. Check what's actually enforced

For each, find the limit and judge it:

- **Does one exist at all?** Grep for the rate-limit middleware/decorator. A missing
  limit on an auth endpoint is the headline finding.
- **Keyed on the right thing?** Per-IP is evadable behind NAT/proxies and via IP
  rotation; sensitive actions should also be keyed per-account / per-API-key. Login
  should limit per-account *and* per-IP.
- **Right scope & window?** A limit so loose it never triggers is theater. A limit so
  tight it breaks legitimate use causes its own incident. Sanity-check the numbers
  against real usage.
- **Fails correctly?** When the limiter's backing store (e.g. Redis) is down, does the
  endpoint fail open (no protection) or closed? Decide deliberately.

### 3. Check the response and the defense in depth

- Returns **429** with a `Retry-After`, not a 500 or a silent drop.
- Rate limiting is one layer — for auth, pair it with lockout/backoff and ideally
  CAPTCHA or proof-of-work after repeated failures.
- For cost-amplification (paid APIs), there's a hard **quota/budget**, not just a rate —
  a slow drip still runs up the bill.

### 4. Note what's missing by design

Some endpoints are fine unlimited (cheap, idempotent, cached). Say so explicitly so the
absence is a decision, not an oversight.

## Output shape

```text
## Operations         (the protect-worthy endpoints, by category)
## Missing limits     (no protection where it's needed — severity)
## Weak limits        (wrong key, wrong window, fails-open, no 429)
## OK / by-design      (adequately limited, or intentionally open)
## Recommendations    (the limit to add: key, window, threshold, response)
```

Lead with unprotected auth and unbounded paid-API calls — brute-force and surprise
bills are the two abuses that hurt soonest.
