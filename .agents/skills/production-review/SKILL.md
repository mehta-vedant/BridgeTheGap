---
name: production-review
description: Review a working hackathon MVP for performance, correctness, reliability, security, concurrency, scaling, and production evolution without blindly refactoring or overengineering it.
---

# Production Review Skill

## Purpose

Use only after meaningful functionality works.

This skill reviews.

It does NOT automatically rewrite the system.

The objective is to determine:

- what must be fixed now
- what should be fixed before demo
- what can be explained as production evolution
- what does not matter yet

---

# Review Classification

Every finding must be labeled:

## MUST FIX NOW

Critical correctness, security, data-loss, deployment, or demo blocker.

## SHOULD FIX BEFORE DEMO

Meaningful reliability or UX problem with manageable effort.

## PRODUCTION EVOLUTION

Valid concern that does not justify hackathon implementation.

## IGNORE FOR NOW

Technically possible but irrelevant at current scope.

---

# Phase 1 — Correctness

Inspect:

- broken workflows
- invalid state transitions
- partial writes
- duplicate operations
- wrong authorization
- inconsistent business rules

Correctness outranks performance.

---

# Phase 2 — Database

Inspect:

- N+1 queries
- table scans
- missing constraints
- missing indexes
- unnecessary indexes
- bad transactions
- race conditions
- duplicate rows
- inefficient joins

For index recommendations, name the actual query.

---

# Phase 3 — API

Inspect:

- missing validation
- inconsistent errors
- unbounded list endpoints
- duplicate side effects
- unclear idempotency
- authentication gaps
- authorization gaps
- oversized payloads

---

# Phase 4 — Frontend

Inspect:

- duplicate requests
- stale state
- broken refresh
- bad loading/error states
- hardcoded production configuration
- unnecessary re-renders only when meaningful
- large blocking assets
- broken navigation

Do not micro-optimize React rendering without evidence.

---

# Phase 5 — External Calls

Inspect:

- missing timeout
- missing retry where appropriate
- synchronous slow provider calls
- provider failure behavior
- malformed responses
- rate limits

---

# Phase 6 — AI Features

Inspect:

- hallucination impact
- schema validation
- fallback path
- prompt injection risks where relevant
- excessive latency
- excessive cost
- provider lock-in
- model output directly changing critical state

---

# Phase 7 — Security

Inspect:

- hardcoded secrets
- exposed credentials
- frontend-only authorization
- insecure object access
- user-controlled identifiers without ownership checks
- injection risks
- unrestricted uploads
- sensitive logs
- overly permissive CORS

---

# Phase 8 — Performance

Use this order:

1. inefficient code
2. inefficient DB query
3. repeated calls
4. indexing
5. caching
6. background jobs
7. replication
8. partitioning
9. sharding

Do not recommend distributed systems as the first optimization.

---

# Phase 9 — Cache Opportunities

Cache only when:

- data is expensive to compute/fetch
- read frequency is high
- some staleness is acceptable

For each cache recommendation state:

- key
- value
- TTL
- invalidation strategy
- stale-data tolerance

---

# Phase 10 — Async Candidates

Identify operations that could move behind a queue.

Examples:

- email
- SMS
- report generation
- AI document extraction
- analytics
- image processing

State whether queue implementation is needed now or only at scale.

---

# Phase 11 — Scaling

Ask:

What breaks at:

- 10x usage
- 100x usage
- 1000x usage

Prioritize likely bottlenecks rather than generic distributed-system theory.

---

# Phase 12 — Reliability

Inspect:

- retries
- timeouts
- idempotency
- duplicate events
- restart behavior
- data durability
- backups
- degraded mode

---

# Phase 13 — Observability

Assess:

- useful logs
- error visibility
- health endpoint
- basic metrics
- tracing only when complexity justifies it

Hackathon MVP does not require an enterprise observability stack.

---

# Required Output

Create a table:

| Priority | Finding | Evidence | Impact | Recommended action |

Then provide:

## Must Fix Now

## Before Demo

## Production Evolution

## Interview Talking Points

Do not modify working architecture without explicit instruction.
