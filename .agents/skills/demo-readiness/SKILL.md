---
name: demo-readiness
description: Prepare a hackathon product for a reliable live demo by verifying startup, deployment, data, authentication, core workflows, external dependencies, fallback paths, and concise presentation scripts.
---

# Demo Readiness Skill

## Purpose

Use near the end of implementation.

A technically strong product that fails during the demo is not ready.

Optimize for reliable demonstration.

---

# Phase 1 — Fresh Start Test

Verify:

- repository setup instructions
- dependencies install
- environment configuration
- migrations
- seed
- backend startup
- frontend startup

Document exact commands.

---

# Phase 2 — Deployment Check

Verify production URLs.

Check:

- frontend loads
- backend health
- database connectivity
- API URL configuration
- CORS
- authentication callback URLs
- object storage
- AI provider

---

# Phase 3 — Demo Accounts

Prepare known users.

Example:

Admin
Officer
Inspector
Contractor

Document safe demo credentials outside committed secret files where required.

Never commit real credentials.

---

# Phase 4 — Seed State

Create deterministic demo records.

Ensure different useful states exist.

Example:

- active
- delayed
- pending review
- completed

The demo should not require 15 minutes of manual setup.

---

# Phase 5 — Core Workflow Test

Run the exact demo flow.

Example:

Login
→ project
→ submit milestone
→ inspector verifies
→ officer approves
→ dashboard updates

Test the entire path rather than individual pages.

---

# Phase 6 — Refresh Test

Refresh on important screens.

Verify:

- authentication survives as expected
- route state survives
- data reload works
- direct URL navigation works

---

# Phase 7 — Error Recovery

Test:

- backend temporarily unavailable
- AI provider error
- invalid form
- duplicate action
- missing record

Critical failure should not leave the demo irrecoverable.

---

# Phase 8 — External Dependency Fallbacks

For each dependency ask:

"What if this dies during the presentation?"

Examples:

AI API:
sample fallback result

Map API:
static coordinates/data

Email:
show in-app notification state instead

External government API:
mocked adapter

Use fallbacks transparently.

Do not claim mocks are live integrations.

---

# Phase 9 — Reset Strategy

Provide a way to restore demo state.

Examples:

seed command

reset script

known database snapshot

Do not make reset destructive to unrelated data.

---

# Phase 10 — Browser Check

Verify:

- correct screen size
- no accidental dev console
- no ugly debug output
- no broken image
- no placeholder text
- no exposed keys
- no irrelevant browser tabs

---

# Phase 11 — 60-Second Demo

Prepare:

1. problem
2. actor
3. action
4. system reaction
5. outcome

Avoid architecture detail here.

---

# Phase 12 — 3-Minute Demo

Prepare:

1. problem/context
2. user workflow
3. core product
4. differentiated feature
5. impact/result

---

# Phase 13 — Technical Walkthrough

Prepare separately:

- architecture
- DB
- API
- tech-stack choice
- security
- scaling path
- trade-offs

Do not mix all technical details into the product demo.

---

# Phase 14 — Backup Demo

If live system fails, have:

- screenshots
- short recording if allowed
- seeded local setup
- backup URL where practical

Live product remains preferred.

---

# Required Output

Update:

`docs/demo-script.md`

Include:

## Demo Preconditions

## Demo Accounts

## Demo Data

## 60-Second Script

## 3-Minute Script

## Technical Walkthrough

## Failure Fallback

## Reset Procedure

## Last-Minute Checklist

---

# Final Gate

Mark DEMO READY only if:

- deployment works
- main workflow works
- required accounts work
- data exists
- critical external dependencies tested
- fallback exists for risky integrations
- script rehearsed
