# Feature Rationale and Evidence Traceability

**Product under consideration:** Bridge Lifecycle Management MVP for one
Gujarat R&B division.

**Use in judging:** For each feature, explain (1) the operational problem it
addresses, (2) the real-world pattern that informed it, (3) the deliberately
smaller hackathon adaptation, and (4) the value it creates. Do not imply that
the source agency uses our exact screen, workflow, or implementation.

## Feature-to-evidence matrix

| Planned feature | Why it is needed | Evidence / reference | Hackathon adaptation | User value |
|---|---|---|---|---|
| Unique bridge ID and asset passport | Inspection and maintenance records must remain attached to the same physical structure across time | MoRTH IBMS inventories bridges/structures; US bridge programmes maintain inventory records | One bridge ID, division, route/chainage, type, age, status and condition | One trusted record instead of scattered files or sheets |
| Condition inspection form | Asset management begins with a recorded observation of current condition | IBMS condition survey; FHWA inspection framework; Bentley structured inspection forms | Inspector-entered condition, component, defect, severity, note, evidence | Consistent, comparable field information |
| Evidence attachment | A serious finding or completed repair should be reviewable | Caltrans inspection reporting; Bentley/IBM mobile photo/report capture | Seeded evidence or a small private image upload path | Decision maker can see the basis of a claim |
| Inspection schedule and overdue queue | Inspections must happen before issues are lost | Bentley supports due/overdue inspection tracking; FHWA relies on periodic inspection | Next-inspection date plus due/overdue dashboard card | Managers see what needs attention now |
| Severity-based triage | Not every defect deserves the same response; urgent findings need ownership | IBMS focuses on distressed structures; FDOT follows up critical deficiencies | Transparent Low/Medium/High/Critical business rule, not engineering scoring | Serious cases do not disappear in a general list |
| Engineer approval | Maintenance actions need a responsible decision maker | DOT workflows use inspection findings/recommendations to drive repair work | Executive Engineer approves/rejects an action and records a note | Clear accountability and auditability |
| Work order and assignment | A finding must become actual planned work | FDOT work-order practice; IBM Maximo maintenance management | One work item with contractor, due date, priority, status | Links diagnosis to execution |
| Contractor completion evidence | Completion should be documented, not verbally asserted | Enterprise asset-management inspection/work history patterns | Completion note and before/after evidence | Creates a reviewable repair record |
| Independent verification | The work performer should not self-certify final operational closure | Public-sector quality-control/inspection principles; FDOT follow-up model | Engineer verifies or rejects completion | Prevents silent or premature closure |
| Immutable lifecycle timeline | Audits and future inspections need historical context | Bentley historical inspection records; Caltrans central information/reporting | Append-only events for inspection, approval, work, evidence and verification | Full answer to “what happened to this bridge?” |
| Portfolio dashboard | Leaders need to prioritise limited attention and funding | FHWA bridge management supports inventory-level decisions | Counts/queues for critical, overdue, active repair and verification pending | Makes the next action obvious |

## Reference register

| Short name | Source type | Claim used | Direct source |
|---|---|---|---|
| Gujarat R&B mandate | Primary government manual | Department is responsible for roads, bridges and government buildings | [CAG manual](https://cag.gov.in/uploads/act_and_mannual/Merged-Manual-064c9ebeb900754-06606429.pdf) |
| MoRTH IBMS | Primary government release | Inventory and condition assessment support timely repair/rehabilitation by criticality | [PIB IBMS release](https://www.pib.gov.in/newsite/PrintRelease.aspx?lang=2&reg=48&relid=151406) |
| MoRTH RAMS | Primary government/NHAI procedure | Road/bridge management separates specialised inventory and decision modules | [RAMS SOP](https://nhai.gov.in/nhai/sites/default/files/2021-01/SOP_RAMS_NSV.pdf) |
| FHWA NBIS | Primary federal standard/guidance | Inventory and periodic inspection support bridge-owner asset decisions | [FHWA NBIS](https://www.fhwa.dot.gov/bridge/nbis.cfm) |
| FHWA bridge management | Primary federal guidance | Bridge programmes use data for maintenance, preservation, repair and prioritisation | [FHWA bridge management](https://www.fhwa.dot.gov/bridge/management/) |
| Caltrans | Primary state-agency source | Central bridge information, inspections and repair recommendations support multiple users | [Caltrans](https://dot.ca.gov/programs/maintenance/structure-maintenance-investigations) |
| Florida DOT | Primary state-agency source | Inspection practice, critical-deficiency follow-up and work-order accountability | [FDOT inspection](https://fdot.gov/maintenance/divisions.shtm/structures/inspection.shtm) |
| Bentley AssetWise | Vendor documentation | Inspection history, evidence, scheduling, review and maintenance-loop patterns | [Bentley](https://www.bentley.com/products/assetwise-inspections) |
| IBM Maximo | Vendor documentation | Mobile inspection, standard checklists, assignment and maintenance patterns | [IBM](https://www.ibm.com/products/maximo/asset-inspection) |

## Full user-flow example: Inspector Asha and Bridge GJ-RB-042

### Starting situation

Bridge **GJ-RB-042**, on a state route in an R&B division, is operational but
its routine inspection is due. The dashboard marks it `Inspection Due`.

### 1. Inspector records the field observation

**User:** Asha, Deputy Engineer / Inspector.

She opens the bridge passport, reviews its previous repair history, and starts
a routine inspection. She records a deck-slab crack, marks severity `High`,
adds notes, and attaches two photographs. On submission the system:

1. stores a completed inspection and defect record;
2. appends an inspection event to the bridge timeline;
3. changes the bridge state to `Attention Required`;
4. places the case in the Executive Engineer approval queue.

**Why this exists:** It adapts the inventory-and-condition-survey pattern from
IBMS and the structured inspection model used in DOT/enterprise systems.

### 2. Engineer turns the finding into accountable work

**User:** Rohan, Executive Engineer.

Rohan sees the high-severity queue, reviews Asha's evidence and the bridge's
history, then approves a repair work order. He assigns contractor `ABC Works`,
sets a target date, and records a decision note. The system changes the state
to `Maintenance Approved`, then `Repair In Progress` once work begins.

**Why this exists:** It adapts the real-system progression from inspection
finding to prioritised maintenance action. Our priority is a transparent
workflow rule, not a structural engineering calculation.

### 3. Contractor records completion, but cannot close the bridge

**User:** Meera, contractor representative.

Meera opens only the work assigned to her, records the repair summary and
uploads completion photos. The work becomes `Verification Pending`.

**Why this exists:** Completion evidence creates a reviewable work history;
restricting final closure keeps the maker and verifier separate.

### 4. Engineer verifies closure

Rohan reviews the repair evidence and either rejects it with a reason or
verifies it. On verification, the bridge becomes `Operational` and the system
adds a closure event. The original inspection, defect, approval, work order,
evidence, and verification remain visible forever on the bridge timeline.

**Why this exists:** It provides the accountable closure and audit history
that a static inventory cannot provide.

### 5. Manager sees portfolio impact

**User:** Sana, Superintending Engineer.

Sana's dashboard changes from “one high-severity bridge awaiting action” to
“repair verified.” She can still drill into GJ-RB-042 to see who made every
decision and when.

## Demo sentence

“A routine inspection found a high-severity deck defect on GJ-RB-042. The
system converted that observation into an approved repair, preserved evidence
from both inspection and completion, required independent engineer
verification, and retained the complete lifecycle history for future audit.”

## Integrity boundary

This is a workflow and governance prototype. It must never claim to calculate
structural safety, replace a licensed engineering assessment, integrate with a
government production system, or comply with a standard without validation.
