---
name: auth-boundary-review
description: Audit routes, actions, and data access for missing or weak authorization — unauthenticated endpoints, missing permission checks, and broken tenant/org isolation (IDOR). Use when reviewing an API, server actions, or any code that reads/writes data on behalf of a user in a multi-user or multi-tenant system.
---

# Auth Boundary Review

The most common real-world vulnerability isn't exotic — it's a handler that loads a
record by an ID from the URL and forgets to check the caller is allowed to see it. This
skill systematically checks every data-touching path for the authorization that should
guard it.

Authentication (*who are you?*) and authorization (*are you allowed to do this?*) are
different. This skill is mostly about the second — the one that gets skipped.

## Process

### 1. Enumerate the protected operations

List every route / action / handler that reads or writes data: API endpoints, server
actions, GraphQL resolvers, background jobs triggered by user input. For each, note the
resource it touches and the identity it should act as.

### 2. Check the three layers, in order

For each operation:

1. **Authenticated?** Is a valid identity required at all? Find the unauthenticated
   endpoints and confirm each is *intentionally* public. An accidentally-public mutation
   is a critical finding.
2. **Authorized for the action?** Does the caller have the role/permission this
   operation requires (admin-only, owner-only)? A role check that's missing or only in
   the UI (not the server) is a finding.
3. **Scoped to the caller's data?** This is the big one. When the operation loads a
   resource by an ID the client supplied, is that load **constrained to the caller's
   org/tenant/user**? `SELECT * FROM orders WHERE id = :id` is broken; it must be
   `… WHERE id = :id AND org_id = :caller_org`. Missing scoping = IDOR / broken object-
   level authorization.

### 3. Hunt the specific anti-patterns

Grep the codebase for these:

- Resource fetched by client-supplied ID with no tenant/owner filter in the query.
- Authorization decided in the client / hidden in the UI but not enforced server-side.
- Mass-assignment: request body spread into an update without an allow-list, letting a
  user set `role`, `org_id`, `is_admin`, `user_id`.
- The "first endpoint authorizes, the second trusts it" pattern across a multi-step flow.
- Object references in URLs that are sequential/guessable, amplifying any missing scope.

### 4. Confirm consistency

Isolation must hold on **every** path to a resource — list, detail, update, delete,
export, search. A locked front door with an open side window is still open. Check that
shared data-access helpers enforce scope centrally rather than relying on each caller.

## Output shape

```text
## Operations reviewed
## Critical    (unauth mutations, missing tenant scope / IDOR, privilege escalation)
## Weak        (UI-only checks, inconsistent scoping, mass-assignment exposure)
## OK          (paths confirmed correctly guarded)
## Fixes       (the specific check/filter to add, per finding, with path:line)
```

Lead with anything that lets one user reach another user's data — that's the finding
that becomes an incident.
