---
name: implementation-plan
description: Convert approved requirements, architecture, database, and API designs into a minimal vertical implementation plan. Identify file changes, dependencies, tests, sequencing, risks, and stop conditions before coding.
---

# Implementation Plan Skill

## Purpose

Use immediately before implementing a substantial feature.

Do not modify application code during planning.

The objective is to define the smallest coherent implementation.

---

# Inputs

Read relevant:

- requirements
- architecture
- database design
- API design
- current state
- tasks
- known issues

Inspect existing code before proposing file changes.

---

# Phase 1 — Define the Feature

State:

## Feature

## User Outcome

## Acceptance Criteria

Avoid vague goals such as:

"Improve dashboard."

Prefer:

"Officer can view all submissions awaiting approval and approve one."

---

# Phase 2 — Vertical Slice

Identify the complete path.

Example:

Frontend form
→ API
→ validation
→ business logic
→ DB
→ response
→ UI update

If any layer is unnecessary, remove it.

---

# Phase 3 — Existing Code Reuse

Before creating files identify:

- existing services
- existing components
- existing schemas
- existing utilities
- existing patterns

Prefer extending established conventions.

Do not duplicate equivalent abstractions.

---

# Phase 4 — File Plan

List exact likely changes.

Example:

MODIFY:
- `backend/app/api/submissions.py`
- `backend/app/services/submission_service.py`

CREATE:
- `backend/tests/test_submission_approval.py`

Avoid enormous speculative file lists.

---

# Phase 5 — Schema/Migration Changes

State explicitly:

NONE

or

Required:
- migration
- field
- constraint
- index

Never let schema changes appear accidentally during implementation.

---

# Phase 6 — API Changes

State:

- new endpoint
- changed contract
- no API change

If an established API contract changes, flag it prominently.

---

# Phase 7 — Dependency Changes

State:

NONE

or explain exactly why a new package is necessary.

Prefer existing dependencies.

---

# Phase 8 — Authorization

Describe:

- who can invoke feature
- ownership checks
- backend enforcement point

---

# Phase 9 — Failure Cases

List expected failures.

Examples:

- resource missing
- invalid state
- unauthorized
- duplicate operation
- external provider timeout

Include intended behavior.

---

# Phase 10 — Tests

Prioritize:

- happy path
- authorization
- invalid state
- duplicate behavior
- critical regression

Do not create tests with no meaningful behavior coverage merely to increase count.

---

# Phase 11 — Implementation Order

Use smallest dependency-aware sequence.

Example:

1. schema change
2. backend service
3. API
4. backend tests
5. frontend integration
6. E2E check

At each useful point, preserve runnable state.

---

# Phase 12 — Stop Conditions

Define when feature is done.

Example:

DONE when:

- authorized officer can approve submission
- duplicate approval is rejected safely
- state persists
- frontend reflects change
- tests pass

Do not expand scope once acceptance criteria are satisfied.

---

# Required Output

Provide:

## Objective

## Acceptance Criteria

## Existing Components Reused

## Files to Modify

## Files to Create

## DB Changes

## API Changes

## Authorization

## Error Cases

## Test Plan

## Implementation Sequence

## Risks

## Definition of Done

Do not implement until plan is accepted or clearly implied by the task.
