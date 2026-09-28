---
name: problem-analysis
description: Analyze a hackathon problem statement before implementation. Identify actors, workflow, pain points, requirements, assumptions, constraints, MVP, risks, and open questions. Do not start coding.
---

# Problem Analysis Skill

## Purpose

Use this skill immediately after receiving a hackathon problem statement.

The goal is to convert an ambiguous problem statement into a clear product and engineering brief before implementation begins.

This skill must NOT begin coding.

Its output should reduce uncertainty and help the team decide:

- what problem is actually being solved
- who the users are
- what the current workflow looks like
- where the pain exists
- what the MVP must contain
- what can be deferred
- what requires research
- what assumptions need validation
- whether the default technology stack is suitable

---

# Phase 1 — Parse the Problem Statement

Extract only what is explicitly stated.

Record:

## Problem Statement
Rewrite the provided problem in precise terms without adding assumptions.

## Stated Goals
List explicit expected outcomes.

## Stated Constraints
Examples:

- time
- geography
- user population
- required integrations
- required technology
- offline usage
- security
- scale
- regulatory constraints

If something is not stated, do not invent it.

---

# Phase 2 — Identify Actors

Identify all likely users and system actors.

For each actor record:

- who they are
- what they need
- what they can do
- what information they provide
- what information they consume
- what outcome they care about

Example structure:

| Actor | Goal | Main actions | Pain points |
|---|---|---|---|
| Citizen | Receive benefit | Apply, upload docs | Unclear eligibility |
| Officer | Process applications | Review, approve | Manual verification |

Clearly distinguish:

- primary users
- secondary users
- administrators
- external systems

---

# Phase 3 — Understand the Current Workflow

Describe the likely existing process.

Use a sequence such as:

Actor
→ action
→ decision
→ next actor
→ state change

Do not describe the proposed solution yet.

Example:

Tender issued
→ contractor submits bid
→ department evaluates
→ contract awarded
→ project milestones created
→ contractor reports progress
→ inspector verifies
→ officer approves payment

If the existing workflow is unknown, mark it as:

RESEARCH REQUIRED

rather than inventing details.

---

# Phase 4 — Pain Points

For every major step ask:

- What is slow?
- What is manual?
- What is duplicated?
- What is unclear?
- What is error-prone?
- Where is information fragmented?
- Where do users wait?
- Where can fraud or misuse occur?
- Where does accountability break?
- Where is data unavailable to decision-makers?

Separate:

## Confirmed pain points
Supported directly by the problem statement or research.

## Hypothesized pain points
Reasonable but requiring validation.

Never present hypotheses as facts.

---

# Phase 5 — Functional Requirements

Convert the problem into capabilities.

Use:

MUST
SHOULD
COULD

Example:

## MUST
- user authentication
- create project
- assign contractor
- submit milestone evidence
- inspector verification

## SHOULD
- notifications
- analytics dashboard

## COULD
- AI risk prediction
- automatic tender extraction

Keep the MVP intentionally small.

---

# Phase 6 — Non-Functional Requirements

Evaluate:

- scalability
- availability
- latency
- reliability
- security
- privacy
- auditability
- consistency
- accessibility
- localization
- offline capability
- observability
- maintainability

Do not assume all are equally important.

Rank them by relevance to the problem.

---

# Phase 7 — Data and Entities

Identify likely domain entities without designing the final schema.

Examples:

- User
- Department
- Project
- Application
- Milestone
- Submission
- Inspection
- Payment
- Notification

For each entity ask:

- who creates it
- who owns it
- who reads it
- how it changes state

Do not prematurely design tables.

That belongs in `database-design`.

---

# Phase 8 — External Systems

Identify possible integrations.

Examples:

- identity provider
- payment service
- maps/GIS
- email
- SMS
- WhatsApp
- document storage
- government APIs
- AI provider
- analytics platform

For every integration classify:

- REQUIRED
- OPTIONAL
- MOCKABLE FOR HACKATHON

---

# Phase 9 — Existing-System Research Questions

Do not perform research unless a research tool/skill is available.

Generate specific research questions such as:

- What systems currently solve this?
- Which government portal already handles part of this workflow?
- What do existing commercial products provide?
- What known gaps remain?
- What standards/APIs already exist?
- Is there an existing digital public infrastructure component we should integrate rather than recreate?

Pass these questions to the existing research skill.

---

# Phase 10 — Define the MVP

The MVP must represent one complete end-to-end workflow.

Prefer:

User action
→ backend
→ persistence
→ state transition
→ next user
→ visible outcome

Avoid:

- a dashboard with no workflow
- a chatbot with no domain function
- many disconnected features
- speculative AI features before core functionality

State:

## Core demo workflow

Example:

Contractor submits milestone
→ evidence stored
→ inspector receives request
→ inspector verifies
→ officer sees updated project state

This should become the first vertical slice.

---

# Phase 11 — Stretch Features

List features separately.

Examples:

- AI document extraction
- anomaly detection
- predictive analytics
- multilingual assistant
- advanced maps
- notifications
- automated reporting

Stretch features must not block the MVP.

---

# Phase 12 — Technology Fit

Do NOT blindly choose the default stack.

Evaluate:

## Product type
- workflow application
- dashboard
- realtime system
- AI/ML demo
- data pipeline
- mobile-first application
- public portal

## Requirements
- relational data?
- realtime?
- large files?
- AI-heavy?
- offline?
- high write volume?
- heavy search?
- streaming?

Then output one of:

### KEEP DEFAULT STACK
Explain why.

### MODIFY DEFAULT STACK
Explain exactly what changes.

### REPLACE DEFAULT STACK
Explain why another stack is substantially better.

Technology choice must optimize for:

1. implementation speed
2. team familiarity
3. demo reliability
4. requirement fit
5. explainability
6. deployment simplicity

---

# Phase 13 — Assumptions

Maintain an explicit assumptions table.

| Assumption | Impact if wrong | Validation method |
|---|---|---|
| users have internet access | offline users cannot complete the core workflow | confirm target population connectivity |
| every project has one contractor | multi-contractor projects break assignment logic | check tender rules |
| inspectors can upload photos | verification step fails on desktop-only officers | confirm device access |
| payment integration may be mocked | demo cannot show real settlement | confirm sponsor expectations |

High-impact assumptions should be validated early.

---

# Phase 14 — Open Questions

List unanswered questions that materially affect:

- workflow
- schema
- architecture
- security
- deployment
- user experience

Prioritize:

P0 — blocks implementation

P1 — important but can proceed temporarily

P2 — can defer

---

# Phase 15 — Risks

Identify:

## Product risks
Does the solution solve the real problem?

## Technical risks
Unknown APIs, difficult integrations, deployment issues.

## Demo risks
External providers, unstable network, complex setup.

## Time risks
Features likely to consume disproportionate effort.

## Interview risks
Architecture choices likely to be challenged.

For each risk give:

- likelihood
- impact
- mitigation

---

# Phase 16 — Recommended Build Order

Output a vertical implementation sequence.

Example:

1. authentication / role setup
2. project creation
3. milestone creation
4. contractor submission
5. inspector verification
6. officer approval
7. dashboard summary
8. stretch AI feature

Each stage should ideally leave the product runnable.

---

# Required Output

At completion, update:

- `docs/problem.md`
- `docs/requirements.md`
- `docs/tasks.md`

If research questions were identified, add them to:

- `docs/research.md`

Do not modify product code.

---

# Final Summary Format

End with:

## Problem in One Sentence

## Primary Users

## Core Workflow

## MVP

## Top 3 Risks

## Top 3 Open Questions

## Recommended Stack Decision

## First Vertical Slice

## Research Required Before Coding

## What NOT to Build Yet
