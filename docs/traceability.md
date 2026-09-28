# Build Traceability Ledger

## Non-negotiable rule

No product feature, schema field, workflow transition, score, integration, or
visualisation may be implemented solely because it “looks good.” Before build,
it needs one of these recorded bases:

1. **Organizer requirement** — stated or confirmed by the organizers.
2. **Authoritative source** — government, standard, or official guidance.
3. **Product decision** — an explicit team choice with reason and trade-off.
4. **Prototype assumption** — clearly labelled, with validation question.

No source means no feature.

## Evidence quality labels

| Label | Meaning | Permitted claim |
|---|---|---|
| Organizer-confirmed | Direct organizer/sponsor clarification | “The organizer asked for…” |
| Authoritative | Government, standard body, law, official agency documentation | “This is informed by…” |
| Vendor pattern | Product documentation/case study | “This is a common implementation pattern…” |
| Team adaptation | Deliberate MVP design choice | “For the prototype, we chose…” |
| Assumption | Unverified temporary choice | “We assume…, pending confirmation.” |

Never describe a vendor pattern or team adaptation as Gujarat R&B policy,
MoRTH compliance, or a structural-engineering rule.

## Required record for every implementation item

| Field | Record |
|---|---|
| ID | `F-` feature, `C-` component, `S-` schema, `W-` workflow, `P-` prototype policy |
| Item | Exact proposed feature, field, rule, or component |
| Need | Product problem it solves |
| Source / decision | Direct link or organizer/team decision record |
| Evidence type | One of the labels above |
| Adaptation | What we take and what we intentionally omit |
| User value | Which user can make which decision/action better |
| Data provenance | Real authorised, public attributed, fictional seed, or none |
| Implementation status | Planned / implemented / tested / deferred |
| Verification | Test, demo path, or manual check that proves it works |

## Initial bridge MVP ledger

| ID | Item | Need | Source / decision | Adaptation and boundary | Status |
|---|---|---|---|---|---|
| F-01 | Bridge asset passport | Stable identity and lifetime record | [MoRTH IBMS](https://www.pib.gov.in/newsite/PrintRelease.aspx?lang=2&reg=48&relid=151406) | ID, division, route, condition; no claim of official IBMS data | Planned |
| F-02 | Structured inspection | Capture repeatable condition observations | [IRC:SP:35 description](https://www.irc.nic.in/admnis/admin/showimg.aspx?ID=901) | Inspector enters condition/defects/evidence; no automated structural calculation | Planned |
| F-03 | High/Critical action queue | Ensure serious findings become visible work | [MoRTH IBMS](https://www.pib.gov.in/newsite/PrintRelease.aspx?lang=2&reg=48&relid=151406), [FDOT](https://fdot.gov/maintenance/divisions.shtm/structures/inspection.shtm) | Transparent prototype triage; not an official Gujarat threshold | Planned |
| F-04 | Engineer approval and work order | Turn a finding into accountable repair | [FHWA bridge management](https://www.fhwa.dot.gov/bridge/management/), [IBM Maximo](https://www.ibm.com/products/maximo/asset-inspection) | One approval/assignment path; no tendering or budget module | Planned |
| F-05 | Completion evidence + independent verification | Avoid self-certification and retain proof | [Bentley AssetWise](https://www.bentley.com/products/assetwise-inspections), [FDOT follow-up](https://pdl.fdot.gov/api/procedures/downloadProcedure/850-010-030) | Contractor submits; engineer alone verifies closure | Planned |
| F-06 | Append-only lifecycle timeline | Audit and future-inspection context | [Caltrans](https://dot.ca.gov/programs/maintenance/structure-maintenance-investigations), [Bentley](https://www.bentley.com/products/assetwise-inspections) | Events link to records/evidence; no immutable-ledger/blockchain claim | Planned |
| F-07 | Workflow integrity indicator | Reveal missing approval/evidence/verification | Team adaptation from the above workflow | Complete/Action Required/Overdue; not a safety/compliance score | Planned |
| F-08 | Optional locator map | Faster bridge discovery/portfolio context | Team adaptation; public data only if approved | Markers only; no GIS analytics; list view remains core | Deferred |
| S-01 | `bridges` entity | Preserve asset identity/current state | IBMS/DOT inventory pattern | Current state plus history; no official data schema claim | Planned |
| S-02 | `inspections` and `defects` entities | Preserve observation and multiple issues | IRC/MoRTH inspection pattern | Human-entered prototype values | Planned |
| S-03 | `work_orders`, `evidence`, `lifecycle_events` | Link action, proof, and history | DOT/enterprise work-management pattern | Minimal workflow only; no procurement/payment tables | Planned |
| P-01 | Recorded condition band | Describe field assessment | Organizer/standard form pending | Good/Fair/Poor/Critical is a prototype controlled vocabulary | Planned |
| P-02 | Workflow integrity | Process completeness | Team adaptation | Never label as Gujarat R&B compliance | Planned |

## Change protocol during implementation

Before each vertical slice:

1. Add or update the applicable ledger row.
2. Add a source link, decision rationale, or explicit assumption.
3. Update `docs/requirements.md`, `docs/database.md`, or `docs/api.md` if a
   contract changes.
4. Build the smallest complete slice.
5. Record the test/demo verification beside the ledger item.
6. Update `docs/current-state.md` and `HANDOFF.md` before agent handoff.

## Review checklist

- Can we point to the exact source or explicit decision behind every screen?
- Is the source being described accurately, without overstating compliance?
- Does the schema field enable a documented workflow or query?
- Can the feature be shown in the main demo journey?
- If not, should it be deferred?
