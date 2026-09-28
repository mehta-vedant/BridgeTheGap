---
name: api-design
description: Design clear, secure, interview-defensible APIs from product workflows, covering routes, payloads, errors, authorization, idempotency, pagination, side effects, and concurrency behavior.
---

# API Design Skill

## Purpose

Turn product workflows into explicit API contracts.

API design must be driven by business actions rather than UI components.

---

# Inputs

Read:

- `docs/problem.md`
- `docs/requirements.md`
- `docs/architecture.md`
- `docs/database.md`
- `docs/decisions.md`

---

# Phase 1 — Identify Resources and Actions

Identify resources:

- projects
- users
- milestones
- submissions
- inspections

Then identify true domain actions.

Example:

`POST /submissions/{id}/approve`

may be clearer than:

`PATCH /submissions/{id}`

when approval has meaningful business semantics.

Do not force everything into generic CRUD if a domain action matters.

---

# Phase 2 — HTTP Method

Use conventions intentionally.

GET:
read

POST:
create/action

PUT:
full replacement where appropriate

PATCH:
partial update

DELETE:
remove

Do not select methods randomly.

---

# Phase 3 — Route Design

Prefer predictable resource-oriented routes.

Examples:

GET /projects

POST /projects

GET /projects/{project_id}

GET /projects/{project_id}/milestones

POST /milestones/{milestone_id}/submissions

POST /submissions/{submission_id}/inspect

Avoid routes tied directly to frontend component names.

---

# Phase 4 — Request Schema

Document:

- path parameters
- query parameters
- headers
- request body
- validation

Use explicit schemas.

Avoid unstructured dictionaries when the shape is known.

---

# Phase 5 — Response Schema

Define stable output.

Include only data the client should receive.

Avoid exposing:

- internal secrets
- raw database objects
- stack traces
- privileged fields

---

# Phase 6 — Errors

Define meaningful error behavior.

Examples:

400:
invalid request

401:
not authenticated

403:
authenticated but not permitted

404:
resource not found

409:
state/conflict/duplicate

422:
validation

500:
unexpected server failure

Do not return HTTP 200 for failed operations merely with `"success": false`.

---

# Phase 7 — Authentication

Document how API identity is established.

Possible:

- session
- JWT
- managed auth provider

Do not duplicate authentication unnecessarily.

---

# Phase 8 — Authorization

For every mutating endpoint ask:

WHO may call this?

Example:

Contractor:
submit milestone

Inspector:
verify

Officer:
approve

Admin:
manage users

Authorization must be enforced server-side.

---

# Phase 9 — Ownership Checks

Role alone may not be enough.

Example:

A contractor may only submit milestones for projects assigned to them.

Document ownership rules.

---

# Phase 10 — Idempotency

For operations that may be retried:

- approval
- payment
- booking
- external webhook processing
- expensive job creation

determine duplicate behavior.

Possible approaches:

- idempotency key
- unique constraint
- existing-state check
- event ID

State the chosen mechanism.

---

# Phase 11 — Concurrency

Ask:

What if two requests happen at the same time?

Examples:

- two approvals
- simultaneous edits
- duplicated claim

Coordinate with database design.

---

# Phase 12 — Pagination

For collections expected to grow:

Prefer bounded results.

Document:

- page/limit or cursor
- ordering
- maximum limit

Do not return unbounded millions of records.

---

# Phase 13 — Filtering and Sorting

Examples:

GET /projects?status=delayed&department_id=123

Document supported filters.

Coordinate frequent filters with database indexes.

---

# Phase 14 — Uploads

For large files determine:

- multipart upload through backend
- direct/presigned object storage upload

Avoid forcing very large binaries through APIs without reason.

---

# Phase 15 — Async Operations

For slow operations:

POST request
→ create job
→ return job ID
→ worker processes
→ client checks status

or equivalent event-driven model.

Do not hold HTTP requests open unnecessarily.

---

# Phase 16 — External Webhooks

If external services call back:

document:

- authentication/signature
- idempotency
- retries
- event ordering
- duplicate handling

---

# Phase 17 — Versioning

Do not add `/v1` automatically unless useful.

For hackathons, versioning may be unnecessary.

State the reasoning.

---

# Required Output

Update:

`docs/api.md`

For every major endpoint record:

| Method | Route | Purpose | Auth | Request | Response | Errors | Idempotent? |

Also document:

- authorization
- ownership rules
- pagination
- concurrency
- uploads
- async behavior

---

# Final API Review

Ask:

- Can another engineer build the frontend from this contract?
- Is authorization explicit?
- What happens if the request arrives twice?
- Are side effects documented?
- Are errors meaningful?
- Are collections bounded?
- Are endpoints based on domain behavior rather than UI implementation?
