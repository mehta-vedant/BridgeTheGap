---
name: architecture-design
description: Design the smallest defensible architecture for a hackathon product, including components, data flow, failure boundaries, deployment shape, and a realistic scale-up path. Avoid unnecessary infrastructure.
---

# Architecture Design Skill

## Purpose

Use this skill after problem analysis and before substantial implementation.

The goal is to design an architecture that is:

- fast to build
- easy to deploy
- easy to explain
- appropriate for the requirements
- capable of evolving if scale increases

Do not optimize for architectural sophistication.

Optimize for justified complexity.

---

# Inputs

Read before designing:

- `AGENTS.md`
- `docs/problem.md`
- `docs/requirements.md`
- `docs/research.md`
- `docs/decisions.md`

If requirements are materially incomplete, identify the missing information
before finalizing architecture.

---

# Phase 1 — Architecture Drivers

Extract the requirements that actually affect architecture.

Examples:

- number/types of users
- expected traffic
- read/write balance
- file uploads
- realtime updates
- background processing
- external integrations
- AI/ML inference
- offline requirements
- security requirements
- consistency requirements
- geographic distribution
- deployment constraints

Separate:

## MVP drivers

Requirements that affect the hackathon implementation.

## Future-scale drivers

Requirements that matter only if usage grows.

Do not let future-scale requirements unnecessarily complicate the MVP.

---

# Phase 2 — Choose Architecture Style

Evaluate the smallest reasonable architecture.

Preferred initial options:

### Single full-stack application

Use when:
- backend complexity is low
- deployment speed dominates
- product can reasonably live in one framework

### Modular monolith

Use when:
- meaningful backend logic exists
- domains should remain separated
- one deployment is sufficient

### Backend + frontend separation

Use when:
- API backend is independently useful
- frontend/backend technology requirements differ
- AI/data workload is Python-heavy
- deployment independence provides value

### Microservices

Use only when justified by:
- independent scaling
- strong domain isolation
- independent deployments
- different runtime requirements
- significant team ownership boundaries

Do not select microservices merely because the product might someday scale.

---

# Phase 3 — Component Identification

For each component record:

- responsibility
- inputs
- outputs
- owned state
- dependencies
- failure behavior

Typical components may include:

- browser/web frontend
- mobile client
- API/backend
- authentication provider
- relational database
- object storage
- cache
- queue
- worker
- AI provider
- notification provider
- search engine
- analytics pipeline

Every component must answer:

"Why does this need to exist?"

If there is no strong answer, remove it.

---

# Phase 4 — Data Flow

Document important request flows.

Example:

User
→ frontend
→ API
→ authorization
→ service
→ database
→ response

For asynchronous work:

API
→ persist state
→ publish job/event
→ queue
→ worker
→ external service
→ update state

For each flow identify:

- synchronous operations
- asynchronous operations
- network boundaries
- persistent state changes
- external dependencies

---

# Phase 5 — Source of Truth

Explicitly identify where authoritative state lives.

Examples:

PostgreSQL:
- projects
- users
- workflow state

Object storage:
- documents
- images

Redis:
- cache only

AI provider:
- never authoritative

Avoid ambiguous ownership.

If two components both appear to own the same business state,
resolve the conflict.

---

# Phase 6 — Sync vs Async Decisions

Use synchronous calls when:

- immediate result is required
- work is short
- failure should be visible immediately

Consider asynchronous processing when:

- work is slow
- external provider latency is high
- retries are useful
- processing can continue after response
- workload is bursty
- operation is non-critical to immediate response

Examples:

Good async candidates:
- email
- SMS
- report generation
- image processing
- document extraction
- analytics
- notifications

Do not introduce a queue without a concrete async workflow.

---

# Phase 7 — File Handling

If files exist, determine:

- upload path
- storage location
- metadata location
- authorization model
- maximum size
- public/private access
- expiration behavior

Prefer:

Client
→ backend/presigned upload
→ object storage

Database stores metadata/reference.

Avoid large binary content in relational database rows unless justified.

---

# Phase 8 — AI Architecture

For AI-enabled features identify:

- model/provider
- prompt/input source
- structured output schema
- validation
- timeout
- fallback
- human review if required
- persistence strategy
- retry behavior

Critical product state should not rely blindly on unvalidated model output.

---

# Phase 9 — Authentication and Authorization

Document:

Authentication:
How identity is established.

Authorization:
How permissions are enforced.

Specify:

- roles
- protected actions
- backend authorization point
- ownership rules

Frontend visibility is not authorization.

---

# Phase 10 — Failure Analysis

For every major dependency ask:

"What happens if this fails?"

At minimum inspect:

- database
- AI provider
- object storage
- authentication provider
- queue
- worker
- cache
- notification provider

Classify:

CRITICAL:
core product cannot proceed

DEGRADED:
product still works partially

OPTIONAL:
feature can disappear temporarily

Design graceful degradation where valuable.

---

# Phase 11 — Scaling Path

Do not redesign everything immediately.

Describe evolution in stages.

## Stage 0 — Hackathon MVP

Example:

Frontend
→ API
→ PostgreSQL

Optional:
Object storage

## Stage 1 — Moderate usage

Possible additions:

- horizontal API scaling
- managed DB
- connection pooling
- indexes
- CDN
- cache

## Stage 2 — High usage

Possible additions:

- read replicas
- background queue
- workers
- partitioning
- search system

## Stage 3 — Large-scale distributed system

Only where relevant:

- sharding
- regional deployment
- service extraction
- event-driven workflows
- advanced observability

Every future component should have a trigger:

"When would we actually need this?"

---

# Phase 12 — Bottleneck Prediction

Predict likely first bottlenecks.

Examples:

- database query
- AI API latency
- large uploads
- expensive dashboard aggregation
- synchronous external calls
- single worker
- hotspot records

For each:

- why it may become a bottleneck
- what metric would reveal it
- what optimization comes first

---

# Phase 13 — Deployment Shape

Document:

- frontend hosting
- backend hosting
- database hosting
- object storage
- secrets
- environment variables
- health checks
- migration strategy

Prefer the simplest deployable shape.

---

# Phase 14 — Security Boundaries

Identify:

- public endpoints
- authenticated endpoints
- admin operations
- secrets
- sensitive data
- privileged integrations

Document the trust boundaries.

---

# Phase 15 — Architecture Trade-offs

For important decisions record:

- decision
- alternative
- reason
- trade-off
- reconsideration trigger

Add meaningful decisions to:

`docs/decisions.md`

---

# Required Output

Update:

- `docs/architecture.md`
- `docs/decisions.md`
- `docs/current-state.md` if architecture is now selected

If architecture decisions imply future DB/API work, do not design those
details here unless necessary.

Invoke the relevant database/API skill separately.

---

# Architecture Documentation Must Include

## Context

## Architecture Drivers

## Chosen Architecture

## Component Diagram

Prefer Mermaid when possible.

## Component Responsibilities

## Main Request Flows

## Source of Truth

## External Dependencies

## Failure Behavior

## Security Boundaries

## MVP Deployment

## Scaling Evolution

## Known Trade-offs

## Deferred Infrastructure

---

# Final Sanity Check

Before completion ask:

- Could one component be removed?
- Are we solving a future problem instead of today's problem?
- Is any infrastructure present only to sound sophisticated?
- Can every box in the diagram be defended in an interview?
- Can the team build this in the available time?

If not, simplify.
