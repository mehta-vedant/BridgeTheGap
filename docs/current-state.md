# Current State

> **Working-scope note:** Bridge-only is the current recommendation, not yet a
> formally accepted team decision. Treat earlier generic asset-class research
> as historical; use the bridge-specific documents below for this MVP.

**Date:** 2026-09-28

## Completed discovery

- Official problem statement, physical-government scope, and Gujarat R&B
  sponsor context have been recorded.
- Evidence on MoRTH IBMS/RAMS, Gujarat R&B/WMS, US DOT examples, and enterprise
  patterns is preserved in `docs/bridge-research-dossier.md`.
- The bridge-only scope is accepted in `docs/decisions.md` D-007.
- `docs/final_research.md` is the canonical evidence record for the three-stage
  lifecycle prototype; older post-construction-only documents are historical
  drafts until reconciled in the foundation branch.
- Feature-by-feature evidence, safe claims, and the end-to-end example are in
  `docs/feature-rationale.md`.
- Proposed entities, state rules, constraints, transactions, and indexes are in
  `docs/database.md`.
- Research-backed product differentiation and deliberate non-features are in
  `docs/differentiation.md`.
- The mandatory feature/component/schema evidence protocol is in
  `docs/traceability.md`.

## Not yet decided or built

- Gujarat-specific delegation limits, DLP terms, and formal condition taxonomy
  remain unverified and must not be hard-coded as compliance rules.
- No application code exists yet; implementation begins after the research
  documentation branch is merged.
