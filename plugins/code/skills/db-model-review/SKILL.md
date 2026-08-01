---
name: db-model-review
description: Review a database schema against the queries it must serve — table design, normalization, indexes, constraints, migrations, and data lifecycle. Use when designing new tables, adding columns, or reviewing a schema change, especially before it ships to a table with real data.
---

# DB Model Review

Schema mistakes are the most expensive kind: by the time you notice, there's
production data shaped wrong and a migration that locks a hot table. Review the model
against the *actual access patterns* before it lands.

Pair with the `db-access-pattern-reviewer` agent, which checks a schema against the
queries that already exist in the codebase.

## Process

### 1. Start from the queries, not the tables

List the reads and writes this data must serve: "fetch a user's last 20 orders newest
first", "count active subscriptions per plan". The schema exists to serve these. A
table you can't query efficiently is a bug, however clean it looks.

### 2. Check the shape

- **Normalization**: is data duplicated where it should be referenced? Is it
  over-normalized into a join nobody needs? Denormalize deliberately, never by accident.
- **Types**: money as integer-cents or decimal (never float). Timestamps as
  timezone-aware. Enums constrained, not free-text. IDs — sequential vs UUID, and why.
- **Nullability**: every nullable column should have a reason. `NULL` means "unknown";
  if the real meaning is "none" or "zero", model that instead.

### 3. Constraints earn their keep

Foreign keys, unique constraints, check constraints, and `NOT NULL` push correctness
into the database where the application can't forget it. Name the invariants the data
must always satisfy and add the constraint that enforces each. A uniqueness rule
enforced only in app code *will* be violated under concurrency.

### 4. Index for the access patterns

For each frequent query from step 1, is there an index that serves it? Check:
composite-index column order (equality before range), covering indexes for hot reads,
and the cost — every index slows writes and uses space. Flag the foreign keys that
lack an index (a common source of slow joins and lock contention).

### 5. Plan the migration

- Is the change **backwards-compatible** with running code (expand/contract pattern)?
- Will it **lock** the table? Adding a non-null column with a default, or an index,
  on a large table can block writes — note whether it needs a concurrent/online path.
- What's the **backfill** for existing rows, and is it batched?
- What's the **rollback**?

### 6. Data lifecycle

How does data get created, updated, and *removed*? Soft vs hard delete. Retention and
PII — does anything need to expire or be purgeable for compliance? Orphan cleanup when
a parent is deleted (cascade vs restrict — decide, don't default).

## Output shape

```
## Access patterns        (the queries the schema must serve)
## Findings               (per table/column: issue → fix, with severity)
## Indexes                (proposed, each tied to a query)
## Migration plan         (compatibility, locking, backfill, rollback)
## Lifecycle              (delete strategy, retention, PII)
```

Lead with anything that's hard to reverse once data exists — those are the findings
that actually matter.
