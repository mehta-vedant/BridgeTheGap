# Proposed Database Design - Bridge Lifecycle MVP

**Status:** proposed design only. No database or migration exists yet.

## Database choice

Use PostgreSQL. The workflow has strong relationships and auditable state
changes: a bridge belongs to a division; inspections create defects; defects
lead to maintenance work; work needs approval and independent verification.
Foreign keys, transactions, constraints, and reporting joins are more useful
than a schemaless store. Store actual photo/document bytes in private object
storage if uploads are enabled; store only metadata and a storage key here.

## Entities and justification

| Entity | Purpose | Why separate |
|---|---|---|
| `rnb_divisions` | Organisational owner | Permissions and dashboard views are division-based |
| `users` | Named workflow actor | Inspection, approval, and verification require authorship |
| `bridges` | Stable asset passport | One bridge has many inspections and repairs over time |
| `inspections` | Point-in-time field observation | Past condition evidence must not be overwritten |
| `defects` | Specific finding | One inspection can have multiple component defects |
| `work_orders` | Approved intervention | A reported defect is not the same as work execution |
| `evidence` | Photo/document metadata | Keeps file bytes out of relational rows |
| `lifecycle_events` | Append-only bridge history | Makes every decision and state change auditable |

## Relationships

```text
RBDivision 1 -> many Bridges
Bridge 1 -> many Inspections
Inspection 1 -> many Defects
Defect 0..1 -> 1 active WorkOrder in the MVP
WorkOrder 1 -> many Evidence items
Bridge 1 -> many LifecycleEvents
User 1 -> many authored actions
```

## Schema outline

### `rnb_divisions`

```text
id UUID PK
name TEXT NOT NULL UNIQUE
district TEXT NOT NULL
created_at TIMESTAMPTZ NOT NULL
```

### `users`

```text
id UUID PK
name TEXT NOT NULL
email TEXT NOT NULL UNIQUE
role TEXT NOT NULL CHECK role IN
  (INSPECTOR, EXECUTIVE_ENGINEER, CONTRACTOR, SUPERINTENDING_ENGINEER)
division_id UUID NULL FK rnb_divisions(id)
created_at TIMESTAMPTZ NOT NULL
```

### `bridges`

```text
id UUID PK
bridge_code TEXT NOT NULL UNIQUE
name TEXT NOT NULL
division_id UUID NOT NULL FK rnb_divisions(id)
route_name TEXT NOT NULL
chainage_km NUMERIC(10,3) NULL
bridge_type TEXT NOT NULL
commissioned_year SMALLINT NULL
length_m NUMERIC(10,2) NULL CHECK length_m > 0
span_count SMALLINT NULL CHECK span_count > 0
condition_band TEXT NOT NULL CHECK condition_band IN (GOOD, FAIR, POOR, CRITICAL)
lifecycle_status TEXT NOT NULL CHECK lifecycle_status IN
  (REGISTERED, OPERATIONAL, INSPECTION_DUE, UNDER_INSPECTION,
   ATTENTION_REQUIRED, MAINTENANCE_APPROVED, REPAIR_IN_PROGRESS,
   VERIFICATION_PENDING, RETIRED)
next_inspection_due_on DATE NULL
version INTEGER NOT NULL DEFAULT 1
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
```

### `inspections`

```text
id UUID PK
bridge_id UUID NOT NULL FK bridges(id)
inspector_id UUID NOT NULL FK users(id)
inspection_type TEXT NOT NULL CHECK inspection_type IN (ROUTINE, SPECIAL, FOLLOW_UP)
occurred_at TIMESTAMPTZ NOT NULL
overall_condition TEXT NOT NULL CHECK overall_condition IN (GOOD, FAIR, POOR, CRITICAL)
notes TEXT NULL
recommendation TEXT NULL
submitted_at TIMESTAMPTZ NOT NULL
```

### `defects`

```text
id UUID PK
inspection_id UUID NOT NULL FK inspections(id)
component TEXT NOT NULL CHECK component IN
  (DECK, SUPERSTRUCTURE, SUBSTRUCTURE, BEARING, EXPANSION_JOINT, APPROACH, OTHER)
category TEXT NOT NULL
severity TEXT NOT NULL CHECK severity IN (LOW, MEDIUM, HIGH, CRITICAL)
description TEXT NOT NULL
status TEXT NOT NULL CHECK status IN (OPEN, MONITORING, IN_WORK, RESOLVED)
created_at TIMESTAMPTZ NOT NULL
resolved_at TIMESTAMPTZ NULL
```

### `work_orders`

```text
id UUID PK
defect_id UUID NOT NULL FK defects(id)
bridge_id UUID NOT NULL FK bridges(id)
status TEXT NOT NULL CHECK status IN
  (DRAFT, APPROVED, IN_PROGRESS, VERIFICATION_PENDING, VERIFIED, REJECTED, CANCELLED)
priority TEXT NOT NULL CHECK priority IN (PLANNED, HIGH, URGENT)
work_description TEXT NOT NULL
assigned_contractor_id UUID NULL FK users(id)
approved_by_id UUID NULL FK users(id)
approved_at TIMESTAMPTZ NULL
target_completion_on DATE NULL
completion_notes TEXT NULL
completed_at TIMESTAMPTZ NULL
verified_by_id UUID NULL FK users(id)
verified_at TIMESTAMPTZ NULL
verification_note TEXT NULL
created_at TIMESTAMPTZ NOT NULL
updated_at TIMESTAMPTZ NOT NULL
```

### `evidence`

```text
id UUID PK
bridge_id UUID NOT NULL FK bridges(id)
inspection_id UUID NULL FK inspections(id)
work_order_id UUID NULL FK work_orders(id)
uploaded_by_id UUID NOT NULL FK users(id)
kind TEXT NOT NULL CHECK kind IN (INSPECTION_PHOTO, COMPLETION_PHOTO, DOCUMENT)
storage_key TEXT NOT NULL UNIQUE
original_filename TEXT NOT NULL
content_type TEXT NOT NULL
byte_size BIGINT NOT NULL CHECK byte_size > 0
created_at TIMESTAMPTZ NOT NULL
```

Require exactly one parent: an inspection or a work order. This is a database
CHECK constraint in implementation, plus API validation.

### `lifecycle_events`

```text
id UUID PK
bridge_id UUID NOT NULL FK bridges(id)
actor_id UUID NOT NULL FK users(id)
event_type TEXT NOT NULL
from_status TEXT NULL
to_status TEXT NULL
related_inspection_id UUID NULL FK inspections(id)
related_work_order_id UUID NULL FK work_orders(id)
note TEXT NULL
created_at TIMESTAMPTZ NOT NULL
```

Events are append-only. Corrections create a new explanatory event rather than
rewriting past history.

## State rules

| Transition | Rule |
|---|---|
| Under Inspection -> Operational | No High/Critical open defect in submitted inspection |
| Under Inspection -> Attention Required | At least one High/Critical finding |
| Attention Required -> Maintenance Approved | Executive Engineer approval and work description |
| Maintenance Approved -> Repair In Progress | Contractor assigned |
| Repair In Progress -> Verification Pending | Completion note and required evidence |
| Verification Pending -> Operational | Executive Engineer verification only |

The database enforces valid values and relationships. The service layer
enforces actor-role checks because role-aware state transitions depend on who
is making the request.

## Query-led indexes

| Index | Query it supports |
|---|---|
| `bridges(division_id, lifecycle_status)` | Division action queues |
| `bridges(next_inspection_due_on)` | Inspections due/overdue |
| `inspections(bridge_id, occurred_at DESC)` | Bridge inspection history |
| `defects(status, severity)` | High/critical open-defect queue |
| `work_orders(assigned_contractor_id, status)` | Contractor work queue |
| `work_orders(status, target_completion_on)` | Overdue repair/verification queue |
| `lifecycle_events(bridge_id, created_at DESC)` | Asset timeline |

## Transactions and concurrency

Submitting an inspection must atomically persist the inspection, defects,
evidence metadata, lifecycle event, and current bridge state. Verifying a
repair must atomically verify the work order, resolve the defect, update the
bridge status, and create a timeline event. Use a row lock or `version` check
so two engineers cannot approve or verify the same work twice.

## Seed strategy

Seed one fictional R&B division, four role-based users, and five fictional
bridges in different states: operational, inspection due, attention required,
repair in progress, and verification pending. Never use live government data.

## Evidence justification

This separation of inventory, inspection, work, evidence, and history adapts
the patterns described by [MoRTH IBMS](https://www.pib.gov.in/newsite/PrintRelease.aspx?lang=2&reg=48&relid=151406),
[FHWA bridge management](https://www.fhwa.dot.gov/bridge/management/),
[Caltrans](https://dot.ca.gov/programs/maintenance/structure-maintenance-investigations),
and [Bentley AssetWise](https://www.bentley.com/products/assetwise-inspections).

## Open questions

1. Are actual photo uploads required, optional, or seeded only?
2. Which exact R&B approval title should the prototype use?
3. Should a Critical finding support a temporary closure/restriction state?
4. Are contractor accounts in scope, or does an engineer record completion?
