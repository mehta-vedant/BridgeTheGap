---
name: database-design
description: Design a database model from product workflows and access patterns, including entities, relationships, constraints, transactions, indexes, state transitions, and future scaling considerations.
---

# Database Design Skill

## Purpose

Convert product requirements into a database design that is:

- correct
- understandable
- easy to implement
- safe against invalid state
- appropriate for expected access patterns

Do not begin with tables.

Begin with domain entities and workflows.

---

# Inputs

Read:

- `docs/problem.md`
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/decisions.md`

Review existing schema/migrations if implementation already exists.

---

# Phase 1 — Identify Domain Entities

Extract nouns that represent durable state.

Examples:

- User
- Organization
- Project
- Milestone
- Submission
- Inspection
- Payment
- Document

Avoid creating entities for temporary UI concepts.

For each entity define:

- identity
- owner
- lifecycle
- major attributes
- relationships

---

# Phase 2 — Relationships

Identify:

- one-to-one
- one-to-many
- many-to-many

For every relationship ask:

- is it required?
- can the referenced object be deleted?
- should deletion cascade?
- should historical records remain?

Do not use cascade deletion blindly.

---

# Phase 3 — State Machines

Important workflow entities should have explicit valid states.

Example:

Submission:

DRAFT
→ SUBMITTED
→ UNDER_REVIEW
→ APPROVED

or:

UNDER_REVIEW
→ REJECTED

Document illegal transitions.

Avoid allowing arbitrary status changes.

---

# Phase 4 — Constraints

Use database constraints where they protect business invariants.

Examples:

- foreign keys
- NOT NULL
- UNIQUE
- CHECK
- composite uniqueness

Example:

A user should not submit the same milestone twice if duplicates are invalid.

Possible invariant:

UNIQUE(milestone_id, contractor_id)

Only add constraints that represent real rules.

---

# Phase 5 — Data Types

Choose meaningful types.

Examples:

- UUID / bigint IDs
- timestamp with timezone
- numeric/decimal for money
- boolean where truly binary
- enums/check constraints for bounded states
- JSON only when schema genuinely varies

Avoid storing structured relational data as arbitrary JSON for convenience.

---

# Phase 6 — Money and Precision

If monetary values exist:

Do not use floating-point values.

Use:

DECIMAL / NUMERIC

Document currency assumptions.

---

# Phase 7 — Auditability

For sensitive workflows consider:

- created_at
- updated_at
- created_by
- approved_by
- state history
- audit events

For government/financial/approval systems, ask:

"Can we explain who changed what and when?"

---

# Phase 8 — Access Patterns

List important queries BEFORE indexes.

Examples:

- get active projects for department
- get pending inspections for inspector
- get submissions for project
- get user by email
- get delayed projects ordered by deadline

For each query estimate:

- frequency
- cardinality
- filtering
- sorting
- joins

---

# Phase 9 — Indexes

Create indexes because of access patterns, not because a column exists.

For every index document:

## Index

`(department_id, status)`

## Query supported

"List delayed projects for a department."

## Reason

Avoid full scan of project table for frequent filtered dashboard query.

Consider:

- composite index order
- selectivity
- write overhead
- redundant indexes

Remember:

more indexes improve reads but increase storage and write cost.

---

# Phase 10 — Transactions

Identify operations requiring atomic behavior.

Example:

Approve milestone:

1. mark submission approved
2. update milestone
3. write audit event

If partial completion would corrupt business state, use a transaction.

Document transaction boundaries.

---

# Phase 11 — Concurrency

Ask:

What if two requests modify the same record simultaneously?

Examples:

- two officers approve same submission
- same payment processed twice
- two users claim same resource

Possible controls:

- unique constraints
- row locking
- optimistic locking
- idempotency
- state checks

Do not rely only on frontend prevention.

---

# Phase 12 — Soft Delete vs Hard Delete

Use hard deletion when:

- data truly has no historical value
- compliance/audit does not require retention

Use soft delete only when there is a real requirement.

Do not add `deleted_at` everywhere automatically.

---

# Phase 13 — Files

Large binary files should generally live outside the relational database.

Store:

- URL/storage key
- owner
- type
- size
- metadata
- timestamps

in the DB.

---

# Phase 14 — SQL vs NoSQL Validation

Do not assume PostgreSQL automatically.

Choose relational storage when:

- strong relationships
- transactional workflows
- reporting/joins
- constraints matter

Consider document/key-value/other storage when the access model justifies it.

If PostgreSQL remains the choice, state why.

---

# Phase 15 — Migration Strategy

Schema changes must be reproducible.

Document:

- migration tool
- migration order
- deployment behavior

Do not make undocumented manual production schema changes.

---

# Phase 16 — Seed Data

For hackathons, define deterministic seed data for:

- demo users
- roles
- realistic domain records
- different workflow states

Seed scripts should be repeatable when practical.

---

# Phase 17 — Scale Evolution

Discuss only after the base schema is correct.

Potential progression:

1. query optimization
2. indexes
3. connection pooling
4. caching
5. read replicas
6. partitioning
7. sharding

Do not jump to sharding first.

---

# Required Output

Update:

`docs/database.md`

Add major DB decisions to:

`docs/decisions.md`

If implementation exists, specify migration work but do not silently
perform destructive migrations.

---

# Required Database Document Sections

## Database Choice

## Entities

## Relationships

## Schema

## Constraints

## State Transitions

## Important Queries

## Indexes

## Transactions

## Concurrency Risks

## Audit Requirements

## Seed Strategy

## Scaling Considerations

## Open Questions

---

# Final Review Questions

- What prevents invalid state?
- What happens on duplicate requests?
- Which queries will be hot?
- Why does each index exist?
- What operation needs a transaction?
- What happens with concurrent updates?
- What is the source of truth?
