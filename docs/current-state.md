# Current State

> **Working-scope note:** Bridge-only is the accepted asset class (`D-007`).
> Earlier generic asset-class research is historical.

**Date:** 2026-09-28

## What exists and runs

| Layer | State |
|---|---|
| API | `apps/api` FastAPI, 17 routes + `/health`, JWT auth, 9-role model |
| Persistence | SQLAlchemy 2.0 + Alembic, single head `0001_initial` |
| Database | SQLite locally; PostgreSQL-compatible via `DATABASE_URL` |
| Seed | 9-bridge synthetic portfolio, 3 per lifecycle phase, non-destructive |
| Web | `apps/web` Next.js App Router, persistent asset rail |
| Config | `render.yaml`, `.env.example`, env-driven CORS, JWT fallback warning |
| Docs | `docs/decisions.md` D-001..D-017, `docs/research_3phase_opencode.md` |

Verification last run: `pytest` 6 passed, `npx tsc --noEmit` clean,
`npm run build` clean.

## The register is the product (`D-016`)

A nine-bridge seeded portfolio spans the department's own three phases, so the
lifecycle is never demonstrated as a single asset:

- **Sanction & Clearance (3)** — all three blocked at the tender-readiness gate,
  each for a different reason (land possession, water/railway NOC, partial
  alignment possession).
- **Execution (3)** — one published tender with a bid, one awarded contract
  with milestones plus an evaluated quality test, one awarded contract with a
  price-variation claim under finance review.
- **Post-Completion (3)** — one `SRI` with an open defect and an approved work
  order, one clean `S`, one `RESTRICTED` with a `U` grade and an open defect.

Three properties were fixed together and are the point of `D-016`:

1. **The register is permanently visible.** `AssetRail` renders every asset on
   every authenticated page, grouped by phase. It is not a navigation
   destination. This is what the operator-reported bug actually was: the
   register sat behind a nav click, so absence of evidence read as absence of
   the asset.
2. **No endpoint hides an asset silently.** `list_assets` returns `total`,
   `returned`, `truncated`, and `register_total`; search and filters run
   server-side against the whole register. The client warns when truncated
   rather than presenting a short list as complete. The old
   `.limit(min(limit, 100))` sat under one percent of the real 7,185-bridge
   register.
3. **The seed is additive and idempotent per asset code.** Verified: operator
   bridges created before a reseed survived it. Two seeded bridges deliberately
   share the name *Orsang River Bridge* with distinct codes, because identity is
   the asset code (`D-014`).

## Deployment configuration (`D-017`)

Per-environment values are read from the environment, never hardcoded:

- `CORS_ORIGINS` — comma-separated allowlist, with the two known-good origins as
  an explicit fallback. A hardcoded allowlist previously meant any other
  deployment hostname passed health checks and then failed every browser
  request.
- `autoDeployTrigger` is `commit`. The previous `checksPass` deadlocked a first
  deploy: the check cannot pass until the service runs, and the service does not
  run until it deploys.
- `render.yaml` declares `DATABASE_URL`, `JWT_SECRET`, and `CORS_ORIGINS` so a
  missing secret is visible in the dashboard rather than inferred from a
  failure.
- The `JWT_SECRET` fallback is retained for the local seeded demo but logs a
  `WARNING` naming the risk. Verified in both directions.

## Research status — three-phase record

`docs/research_3phase_opencode.md` is the **canonical evidence record**: 22
cited sources, 36 explicit `NOT ESTABLISHED` markers, with conclusions fenced
separately from the research. `docs/final_research.md` is superseded.

| Phase | Research | Written |
|---|---|---|
| Pre-construction | Complete | Yes |
| Construction | Complete | Yes |
| Post-construction | **Substantially advanced, not yet written in** | **No** |

**This is the largest open item.** A post-construction research pass completed
and overturned a prior finding — `IRC:SP:35-2024` codifies a numeric severity
scale (condition states I-V, BHI 0-100, five star bands, 62+ distress types,
seven AHP-weighted component groups) and is a mandatory specification that
retires `SP:18` and `SP:52`. It also surfaced the sharpest pitch finding, from
Gujarat's own lender, that defect rectification has no prescribed time limit
because the contract terms are vague. **None of this has been folded into the
canonical record or into `docs/decisions.md`.** It is currently unfiled, and its
IRC citation URLs are internally inconsistent and must be verified from each
document's own front matter before use.

Also unfiled from that pass: the correction that only **7,185** bridges is
sourceable and the other two published counts are not; that closure decisions are
load-capacity-conditional and must never be auto-triggered by a BHI score; and
that "34.5 years average bridge age" is fabricated and permanently barred.

## Open issues

- **The post-construction pass is unfiled.** Highest-value work remaining. It
  changes the product thesis, so it should be written before the thesis is
  defended in the room.
- **No visual browser verification of the new rail.** No browser was attached
  to the session. Build, typecheck, and tests validate the component graph and
  the API contract, but nobody has actually *looked* at the rail rendered.
- **Render is still unconfigured.** The service was created by hand, so
  dashboard settings override `render.yaml`. The previous failure was a
  hand-typed `--port 10000` while the yaml said `$PORT`.
- **`.git` exists with 32 commits on `main` and 5 branches, contradicting
  `D-002`** (no repository before official kickoff). Not deleted, not touched,
  pending an explicit decision.
- **P0 source gaps, unchanged:** B-1/B-2 retention and DLP percentages; the
  GR PDW-3079-D-2959-BHAG-1-136-C delegation of powers; the Gujarat Public
  Works Manual (557 pp + 735 pp annexures); the 28 QC standard-form names; the
  repair-decision authority table; the per-component defect taxonomy and service
  life (permanently unavailable). Gujarat-specific delegation limits, DLP terms,
  and a formal condition taxonomy must **not** be hardcoded as compliance
  rules.
- **`verify_work` writes the same actor literal as `create_work_order`.** The
  gate still checks state, not person, so the second-person approval the product
  claims is not yet enforced in code.
