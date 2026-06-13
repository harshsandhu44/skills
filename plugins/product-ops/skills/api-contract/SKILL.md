---
name: api-contract
description: Design an API surface before implementing it — routes, request/response shapes, validation rules, auth/permission requirements, status codes, and error formats. Use when adding or changing endpoints (REST, RPC, GraphQL mutations) and you want the contract pinned down so client and server agree before code is written.
---

# API Contract

Endpoints are forever — clients depend on them, and breaking changes are expensive.
Designing the contract first catches the awkward shapes, the missing auth rule, and the
unhandled error *on paper*, where they cost nothing to fix.

Pair this with the `api-contract-reviewer` agent: this skill *designs* the contract;
that agent *attacks* it for gaps.

## Process

For each endpoint, pin down all seven of these. A gap in any one is a bug waiting:

### 1. Route & method

Verb + path, with resource nesting that matches the data model. `POST /orders`,
`GET /orders/{id}/items`. Use plural nouns; keep verbs out of paths (the HTTP method
*is* the verb). Note idempotency — can the client safely retry?

### 2. Request shape

Every field: name, type, required vs optional, default. Where it travels — path,
query, body, header. Be explicit about formats (ISO-8601 dates, decimal vs float for
money, enums and their allowed values).

### 3. Validation rules

Per field: bounds, length, pattern, allowed values, cross-field rules ("end after
start"). Decide what's a 400 (client's fault) vs 422 (well-formed but semantically
invalid). State what happens to unknown fields — rejected or ignored.

### 4. Auth & permissions

Who can call this? Authentication (is a valid identity required?) is separate from
authorization (is *this* identity allowed to touch *this* resource?). Name the
permission check explicitly, including tenant/org isolation — the most commonly
forgotten rule. (The `auth-boundary-review` skill exists to catch these.)

### 5. Response shape

Success body for each success status. Shape consistency matters — collection
endpoints return the same item shape as the single-item endpoint. Note pagination
envelope, and which fields are nullable.

### 6. Status codes

Map each outcome to a code: 200/201/204 success, 400/401/403/404/409/422 client
errors, 429 rate limit. One outcome → one code; don't overload 400 for everything.

### 7. Error format

One consistent error envelope across all endpoints — a machine-readable `code`, a
human `message`, and per-field details for validation errors. Decide it once here so
every endpoint matches.

## Output shape

Per endpoint, a compact block:

```
### POST /orders
Auth:      authenticated; user must belong to {org}
Request:   { items: [{sku: string, qty: int>=1}], note?: string<=500 }
Validates: items non-empty; sku exists; qty 1..99
Responses: 201 {order} | 400 invalid body | 403 wrong org | 409 sku out of stock
Errors:    { code, message, fields?: {field: reason} }
Idempotent: no (use Idempotency-Key header to make safe)
```

Finish with the shared error envelope and any cross-cutting conventions (pagination,
versioning, rate-limit headers) stated once.
