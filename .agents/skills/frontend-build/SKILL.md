---
name: frontend-build
description: Build fast, coherent, workflow-first hackathon frontends with reusable components, realistic data states, accessible interactions, strong demo reliability, and minimal visual complexity.
---

# Frontend Build Skill

## Purpose

Build product UI quickly without sacrificing workflow clarity.

Primary priority:

Working user journey.

Secondary priority:

Visual polish.

---

# Principles

Prefer:

- clear navigation
- consistent layout
- reusable components
- visible status
- useful feedback
- realistic content

Avoid:

- unnecessary animations
- multiple design systems
- excessive custom CSS
- speculative components
- hardcoded disconnected dashboards

---

# Phase 1 — User Journey

Before building UI identify:

- user role
- goal
- entry point
- primary action
- completion state

Every important page should support a real workflow.

---

# Phase 2 — Information Architecture

Define:

- app shell
- navigation
- major pages
- primary actions
- role-specific views

Keep navigation shallow for hackathon products.

---

# Phase 3 — Reuse Existing Components

Before building primitives inspect existing library/components.

Prefer existing:

- Button
- Input
- Select
- Dialog
- Table
- Card
- Badge
- Tabs
- Toast
- Skeleton

Do not recreate design primitives unnecessarily.

---

# Phase 4 — Page States

Every critical screen should handle:

## Loading

## Empty

## Success

## Error

## Submitting/disabled

A screenshot-perfect happy path that crashes on empty data is not demo-ready.

---

# Phase 5 — Forms

Forms should include:

- labels
- validation
- useful errors
- submission state
- disabled duplicate submission
- success feedback

Do not rely only on backend errors for obvious client-side validation.

---

# Phase 6 — Tables and Lists

For operational systems prioritize:

- status
- owner
- dates
- primary action
- filters where genuinely useful

Avoid displaying every DB field.

---

# Phase 7 — Status Language

Use consistent domain states.

Example:

Pending Inspection

not simultaneously:

Pending
Awaiting
To Review

unless they are genuinely different.

---

# Phase 8 — Dashboard Rule

Dashboards should answer useful questions.

Good:

- active projects
- delayed projects
- pending inspections
- amount awaiting approval

Bad:

random charts included only for appearance.

Prefer server-backed data.

---

# Phase 9 — Realistic Demo Data

Use realistic names and domain states.

Avoid:

Test User
Project 1
asdf
Lorem ipsum

Seed data should make the product understandable during the demo.

---

# Phase 10 — Responsive Behavior

Ensure primary workflows remain usable at common laptop resolutions.

Mobile support should match actual product needs.

Do not spend excessive time perfecting rarely used breakpoints.

---

# Phase 11 — Accessibility

At minimum:

- semantic controls
- labels
- keyboard-accessible actions where practical
- readable contrast
- non-color-only status where important

---

# Phase 12 — API Integration

Centralize API configuration.

Do not scatter production URLs throughout components.

Handle:

- loading
- network failure
- auth failure
- validation errors

---

# Phase 13 — Environment Configuration

Frontend URLs/provider keys should come from environment configuration.

Never hard-code deployment-specific endpoints unnecessarily.

---

# Phase 14 — Demo Reliability

Before demo:

- disable impossible double-clicks
- verify navigation
- verify refresh behavior
- verify authentication persistence
- verify empty/error states
- ensure critical forms reset properly

---

# Phase 15 — Visual Consistency

Use one:

- spacing system
- typography scale
- badge pattern
- table style
- card style
- icon family

Consistency beats visual novelty.

---

# Required Output

When implementing frontend work:

- follow current architecture
- update `docs/current-state.md`
- record known UI issues in `docs/known-issues.md`
- verify primary workflow manually or through browser automation

---

# Final Review

Ask:

- Can the user tell what to do next?
- Does every major button perform a real action?
- Does the UI survive empty data?
- Are error states understandable?
- Is status terminology consistent?
- Is any visual feature consuming time without improving the demo?
