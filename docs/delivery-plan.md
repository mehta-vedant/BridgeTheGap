# Proposed Delivery Plan - Bridge Lifecycle MVP

**Status:** proposed. This is a build/release design only. Do not initialize
Git or create product code until official hackathon kickoff is confirmed.

## Chosen architecture

```text
Next.js web app (Vercel)
        |
        | HTTPS JSON API
        v
FastAPI workflow API (Render)
        |
        v
PostgreSQL (managed database)
```

This is a **modular monolith**, not microservices:

- one frontend deployment;
- one backend deployment owning all lifecycle rules;
- one relational database owning all business state;
- no queue, cache, GIS service, AI service, or additional database in MVP.

## Why this architecture

| Choice | Why | Trade-off |
|---|---|---|
| Next.js + TypeScript frontend | Fast workflow UI, strong type support, easy Vercel deploy/preview | Requires a separate API client |
| FastAPI backend | Keeps role checks and lifecycle transitions in a trusted, independently reusable API; future mobile/field client can use same API | CORS and second deployment require configuration |
| PostgreSQL | Relationships, constraints, transactions, timeline and dashboard queries are core | More setup than an in-memory demo, but necessary for credible persistence |
| Vercel frontend | Git-driven branch previews and simple Next.js hosting | Frontend needs API URL configuration |
| Render backend | Straightforward Python web-service deployment and health endpoint | Configure CORS and database environment variables carefully |
| Seeded evidence first | Avoids a fourth storage service before core flow works | Real upload is a later iteration |

## Responsibility boundaries

| Component | Owns | Must not own |
|---|---|---|
| Next.js web | Screens, forms, API display states, accessibility, client validation | Authoritative permission or lifecycle decisions |
| FastAPI | Authentication boundary, role authorization, state transitions, validation, error responses | UI state/layout |
| PostgreSQL | Assets, inspections, defects, work orders, evidence metadata, timeline | File bytes or business logic hidden in triggers |
| Static/seed evidence | Demo images/documents | Production upload workflow |

## Deployment model

### Vercel

- Deploy `apps/web`.
- `main` is production.
- Every feature branch gets a preview deployment through Git integration.
- Required environment variable: `NEXT_PUBLIC_API_URL`.

### Render

- Deploy `apps/api` as one FastAPI web service.
- Start command follows Render's documented pattern:
  `uvicorn app.main:app --host 0.0.0.0 --port $PORT`.
- Expose `GET /health` that checks application readiness without leaking
  secrets.
- Required environment variables: `DATABASE_URL`, `CORS_ALLOWED_ORIGINS`, and
  later only the secrets required by chosen authentication/upload mechanisms.

### Database

- Use one managed PostgreSQL instance.
- Apply migrations as a deliberate release step before backend deploy.
- Never put database credentials in Git, frontend variables, screenshots, or
  documentation.

## Branch and merge strategy

Use **short-lived feature branches from `main`**. Do not add a long-lived
`develop` branch in a seven-hour event; Vercel branch previews already provide
safe review space, while an extra integration branch adds merge delay.

```text
main (always runnable; production deployment)
  ├─ feat/bridge-inventory
  ├─ feat/inspection-submission
  ├─ feat/work-order-verification
  └─ feat/dashboard-integrity
```

For each branch:

1. Create from current `main`.
2. Implement one vertical slice only.
3. Update `docs/traceability.md` with source, adaptation, and verification.
4. Run relevant tests/lint/typecheck/build.
5. Open a PR; use Vercel preview for affected frontend flow.
6. Merge only when CI passes and the main affected workflow is verified.
7. `main` triggers production deploy.

### Commit standard

One coherent action per commit:

```text
docs: record bridge lifecycle scope and evidence
feat: add bridge inventory passport
feat: submit inspection and high-severity triage
feat: approve maintenance work and verify closure
test: cover work-order state transitions
fix: prevent contractor from verifying repair closure
```

## CI gate

Run on every pull request and before merge:

```text
Web: lint -> typecheck -> unit tests -> production build
API: Ruff -> tests -> typecheck if configured
Database: migration validation / schema test
```

The deployment must not be treated as verification. Production is promoted only
after these checks pass.

## Build order and initial branches

### 0. Kickoff and foundation

**Branch:** `chore/project-foundation`

Create the repository at official kickoff, scaffold the chosen frontend/API,
configure local environment examples, CI, health endpoint, and deployment
placeholders. Do not build the map or uploads.

**Why:** Creates a reproducible, deployable baseline before domain features.

### 1. Bridge inventory vertical slice

**Branch:** `feat/bridge-inventory`

Implement seeded division/users/bridges, inventory list, bridge passport, and
append-only timeline read view.

**Why:** Proves the system-of-record concept and gives every later workflow a
stable asset.

### 2. Inspection and action vertical slice

**Branch:** `feat/inspection-submission`

Implement inspector submission, defect severity, transactional state update,
and engineer attention queue.

**Why:** This is the first true management behaviour: an observation turns into
an owned decision.

### 3. Work and verification vertical slice

**Branch:** `feat/work-order-verification`

Implement engineer approval/assignment, contractor completion submission, and
engineer-only verification/closure.

**Why:** Completes the end-to-end lifecycle loop and demonstrates governance.

### 4. Management and polish

**Branch:** `feat/dashboard-integrity`

Implement portfolio queues, explainable action cards, workflow-integrity
indicators, demo seed reset, and only then optional map/evidence upload.

**Why:** Improves manager value without risking the core workflow.

## Definition of MVP done

The MVP is done when a fresh deployment can reliably demonstrate:

```text
Seeded bridge
-> Inspector submits High-severity defect
-> Engineer approves and assigns work
-> Contractor records completion evidence
-> Engineer verifies closure
-> Bridge timeline and dashboard reflect every event
```

## Evidence for platform choices

- [Next.js App Router](https://nextjs.org/docs/app)
- [Next.js Route Handlers](https://nextjs.org/docs/app/getting-started/route-handlers)
- [Next.js Backend-for-Frontend guidance](https://nextjs.org/docs/app/guides/backend-for-frontend)
- [Next.js on Vercel](https://vercel.com/docs/frameworks/full-stack/nextjs)
- [Vercel Git deployments and previews](https://vercel.com/docs/git)
- [Render FastAPI deployment](https://render.com/docs/deploy-fastapi)
