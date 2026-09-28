---
name: research
description: Research a hackathon problem systematically using reliable external sources. Establish the existing solution landscape, current workflows, documented pain points, relevant standards/APIs, implementation constraints, and evidence-backed differentiation without inventing claims.
---

# Research Brief Skill

## Purpose

Use this skill after `problem-analysis` identifies questions that require
external evidence.

The goal is NOT to collect random links.

The goal is to reduce uncertainty before product and architecture decisions.

Research should help answer:

- How is this problem handled today?
- Who already solves part of it?
- What existing systems must we integrate with rather than rebuild?
- What problems are actually documented?
- Which assumptions are supported?
- Which assumptions are unsupported?
- What technical standards/APIs exist?
- What solution patterns are already common?
- Where is there a genuine gap?
- What claims can we safely make in front of judges/interviewers?

Do not begin coding.

---

# Core Rule — Evidence Before Claims

Do not state:

- "Nobody solves this"
- "This process is completely manual"
- "Users face this problem everywhere"
- "This will reduce cost by X%"
- "This is the first solution"
- "Government systems do not support this"

unless supported by reliable evidence.

Separate findings into:

CONFIRMED
INFERRED
UNVERIFIED

Never turn an inference into a fact.

---

# Phase 1 — Read Existing Context

Before research, read:

- `AGENTS.md`
- `docs/problem.md`
- `docs/requirements.md`
- `docs/research.md`
- `docs/decisions.md`

Also inspect the original problem statement/source if available.

Do not research a broader problem than the one actually assigned.

---

# Phase 2 — Define Research Questions

Convert ambiguity into specific questions.

Bad:

"Research construction systems."

Good:

- How is contractor milestone verification currently performed?
- Are there existing public portals for project progress reporting?
- What evidence is normally required before payment approval?
- Are site inspections digitized?
- Are geo-tagged photos already used?
- What APIs or standards exist?
- What systems already provide project dashboards?
- Where do delays and fraud commonly occur?

Prioritize:

P0:
changes MVP or architecture

P1:
improves product differentiation

P2:
nice background information

Research P0 first.

---

# Phase 3 — Source Hierarchy

Prefer sources in this order when possible.

## Tier 1 — Primary / authoritative

Examples:

- official government websites
- official documentation
- laws/regulations
- standards bodies
- official APIs
- official technical documentation
- company product documentation
- published reports from responsible organizations

Use these for factual claims.

---

## Tier 2 — High-quality secondary

Examples:

- reputable news outlets
- major research organizations
- academic papers
- respected engineering blogs
- industry reports

Use these for:

- context
- impact
- case studies
- comparisons

---

## Tier 3 — Community / experiential

Examples:

- Reddit
- Stack Overflow
- developer forums
- GitHub discussions
- user reviews

Use these for:

- pain points
- implementation experiences
- community sentiment

Do NOT treat community posts as authoritative factual evidence.

---

# Phase 4 — Existing Workflow Research

Research how the process works TODAY.

Document:

## Actors

Who participates?

## Steps

What happens from start to finish?

## Data exchanged

Which documents/data move between actors?

## Decisions

Where are approvals/rejections made?

## Delays

Where can the workflow stall?

## Systems used

Which portals/software/services already exist?

Use a flow such as:

Actor
→ action
→ system
→ decision
→ next actor

Do not describe the proposed product in this section.

---

# Phase 5 — Existing Solution Landscape

Find systems that already solve:

- the whole problem
- part of the problem
- adjacent problems

For each relevant solution record:

## Name

## Who uses it

## What it does

## What part of our problem it covers

## Strengths

## Limitations relevant to our use case

## Integration opportunity

## Source

Do NOT criticize competitors without evidence.

---

# Phase 6 — Build vs Integrate

For every major proposed feature ask:

Does an existing platform/API already provide this?

Examples:

- authentication
- identity verification
- payments
- mapping
- messaging
- document OCR
- digital signatures
- government scheme data
- location data
- notifications

Classify:

BUILD

INTEGRATE

MOCK FOR HACKATHON

DEFER

Avoid rebuilding established infrastructure unnecessarily.

---

# Phase 7 — Problem Evidence

Find evidence for the pain.

Look for:

- processing delays
- administrative overhead
- fragmented data
- duplicate data entry
- lack of transparency
- fraud
- manual verification
- poor discoverability
- poor accessibility
- low interoperability
- coordination failures

For each pain point document:

## Claim

## Evidence

## Population/context

## Source

## Confidence

HIGH
MEDIUM
LOW

Avoid generalizing a problem from one organization or region to everyone.

---

# Phase 8 — Standards and Regulations

Research relevant:

- technical standards
- data formats
- privacy rules
- identity standards
- accessibility rules
- security requirements
- retention requirements
- interoperability frameworks

Only include standards that materially affect the product.

Do not dump unrelated regulation.

---

# Phase 9 — APIs and Data Sources

Identify usable external resources.

For each:

## Name

## Provider

## Purpose

## Authentication

## Data available

## Rate limits if known

## Cost if known

## Availability

## Hackathon suitability

Classify:

READY TO USE

REQUIRES ACCESS

LIKELY MOCK

UNKNOWN

Do not assume an API is publicly usable merely because documentation exists.

---

# Phase 10 — Technical Feasibility Research

For uncertain technical components research:

- SDK maturity
- deployment constraints
- browser support
- file-size limits
- model limitations
- API latency
- rate limits
- pricing
- authentication requirements
- regional availability

Focus only on technology that is actually under consideration.

---

# Phase 11 — AI Feasibility

If AI is proposed, answer:

## What exact task requires AI?

Examples:

- extraction
- classification
- ranking
- summarization
- anomaly detection
- natural-language interaction

Then research:

- existing models/tools
- expected input
- expected output
- known failure modes
- latency
- cost
- privacy implications
- deterministic alternatives

Challenge unnecessary AI.

If rules-based logic is sufficient, state that.

---

# Phase 12 — Differentiation Analysis

Do NOT write marketing claims first.

Create a comparison table.

| Capability | Existing System A | Existing System B | Proposed Product |
|---|---|---|---|

Then identify differentiation based on evidence.

Possible differentiation:

- combines fragmented workflows
- reduces context switching
- improves accessibility
- provides cross-system visibility
- automates a manual step
- supports underserved workflow
- integrates systems that currently remain separate

Avoid:

"AI-powered"

as a differentiation by itself.

AI is technology, not automatically a USP.

---

# Phase 13 — Research Contradictions

If sources disagree:

Do not silently pick one.

Record:

## Claim A

Source/support

## Claim B

Source/support

## Likely explanation

Examples:

- different jurisdictions
- different years
- different user populations
- old vs new system
- pilot vs production

Mark unresolved contradictions explicitly.

---

# Phase 14 — Time Sensitivity

Check dates.

For changing information such as:

- API availability
- pricing
- program eligibility
- government portals
- current regulations
- active products
- technology versions

prefer recent sources.

Do not treat an old report as proof of the current situation without
checking whether the system has changed.

---

# Phase 15 — Source Quality Check

Before using a source ask:

- Who published it?
- When?
- Is it primary or secondary?
- Does it actually support the claim?
- Is the population/context comparable?
- Is it marketing material?
- Could the information be outdated?

Reject weak sources when stronger evidence exists.

---

# Phase 16 — Research Stop Condition

Do not research forever.

Stop when:

- P0 questions are sufficiently answered
- major architecture blockers are understood
- existing solution landscape is clear enough
- differentiation can be stated carefully
- remaining uncertainty is documented

For hackathons, time matters.

A 30-minute evidence-backed research brief is usually more valuable than
two hours of indiscriminate browsing.

---

# Phase 17 — Convert Research Into Decisions

For every major finding ask:

SO WHAT?

Examples:

Finding:
Existing portal already handles identity verification.

Decision:
Integrate/mock identity instead of implementing verification.

Finding:
Users struggle with cross-department visibility.

Decision:
Prioritize unified case timeline.

Finding:
Real government API requires approval.

Decision:
Create adapter interface and mock provider during hackathon.

Research must influence product or architecture.

Otherwise it is trivia.

---

# Required Output

Update:

`docs/research.md`

Use this structure:

# Research Brief

## Research Objective

## Questions Investigated

## Current Workflow

## Existing Systems

## Documented Pain Points

## Relevant Standards / Regulations

## APIs / Data Sources

## Technical Feasibility Findings

## AI Feasibility

## Build vs Integrate Decisions

## Differentiation

## Unsupported Assumptions

## Contradictions / Uncertainty

## Product Implications

## Architecture Implications

## Sources

---

# Source Record Format

For important sources record:

- title
- publisher
- date
- URL/reference
- type: primary / secondary / community
- claim supported

Do not maintain a giant undifferentiated bookmark list.

---

# Required Research Summary

End with:

## 5 Most Important Findings

1.
2.
3.
4.
5.

## 3 Things We Should Build

1.
2.
3.

## 3 Things We Should NOT Build

1.
2.
3.

## Existing System We Must Understand Best

## Strongest Evidence-Backed Differentiator

## Biggest Unsupported Assumption

## Research Question Still Blocking Architecture

## Safe Claims for Presentation

## Claims We Must NOT Make

---

# Presentation Safety

Before finalizing, explicitly identify statements the team can safely say.

Example:

SAFE:

"Platform X currently provides A and B, while our prototype focuses on
connecting B to workflow C."

UNSAFE:

"No existing product does this."

unless comprehensive evidence genuinely supports the statement.

---

# Interview Defense Preparation

Expect questions such as:

- What did you research before building?
- What already exists?
- Why not use the existing system?
- What was missing?
- Which assumptions did you validate?
- Which assumptions remain?
- Which external APIs exist?
- Which integration did you mock?
- Where did your workflow information come from?

The research brief should make those questions easy to answer.

---

# Final Rule

Research exists to make product decisions better.

Do not optimize for the number of sources.

Optimize for:

- decision relevance
- source quality
- uncertainty reduction
- defensible claims