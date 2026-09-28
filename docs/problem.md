# Problem Analysis — Infrastructure Asset Lifecycle Inventory

**Status:** in progress · physical-government scope confirmed · specific asset
class OPEN · nothing implemented
**Date:** 2026-09-28
**Method:** `problem-analysis` skill, 16 phases. Only what is known is
recorded. Unknowns are marked, not invented.

**Related:**
- `docs/research.md` — research briefs, incl. the government domain
- `docs/researchassets.md` — 8-class survey (pre-clarification; class
  reasoning partly invalidated, see note below)
- `.agent-artifacts/consensus/consensus_report.md` — consensus matrix

> ## SPONSOR CLARIFICATION RECEIVED 2026-09-28
>
> **"Go with government assets, i.e. physical government assets."**
>
> A confirmation from the sponsors, not an inference. Three consequences:
>
> 1. The assets are **government-owned and physical/tangible**.
> 2. The *domain* is settled. The *class within* the domain is not, and is the
>    live P0.
> 3. **Cloud and SaaS licence classes are eliminated on definition** — software
>    and cloud spend are intangible and cannot be the subject of a physical
>    asset register.
>
> It also **invalidates part of the earlier ranking** in
> `docs/researchassets.md`: plant & machinery was penalised for being "a
> category mismatch" with the word *infrastructure*, and for a government
> sponsor that objection is dead. That survey was also framed around private
> IT/industrial contexts; the government domain has its own taxonomy, its own
> mandated artefacts, and its own failure modes, all recorded in Phase 3 and
> Phase 4. **Treat `docs/researchassets.md` as historical, not as the basis for
> the class decision.**

---

## Problem in One Sentence

Build an end-to-end infrastructure asset inventory that tracks and manages
assets across their entire lifecycle, with depth of process as the scoring
axis.

---

## Phase 1 — Parse the Problem Statement

### Problem Statement (as received)

> Build an end-to-end infrastructure asset inventory to track and manage assets
> across their entire lifecycle. They are looking for depth of process. Told to
> ask intelligent questions in between.

### Stated Goals

- An **inventory** of infrastructure assets (the system of record)
- **Tracking** assets across their **entire** lifecycle
- **Management**, not just recording — the word "manage" is doing work
- **End-to-end** coverage of the lifecycle, not a slice of it
- **Depth of process** — explicitly named as the thing being looked for
- **Asking questions mid-build is expected**, not a detour. The brief invites
  it, which means questioning the sponsor is probably an assessed behaviour.

### Stated Constraints

| Constraint | Value | Source |
|---|---|---|
| Time budget | **UNCONFIRMED** | not stated in the brief |
| Team size | **UNCONFIRMED** | not stated in the brief |
| Asset domain | **Physical government assets — CONFIRMED** | organizer clarification |
| Sponsor / operating context | **Roads & Buildings Department, Government of Gujarat — CONFIRMED** | organizer clarification |
| Specific asset class | **OPEN** — construction plant & machinery leads | see Phase 5 |
| Required integrations | **UNCONFIRMED** | "end-to-end" is not defined as "with real systems" |
| **Jurisdiction** | **India — Gujarat state rules** | **resolved by the department clarification** |
| Technology | **UNCONFIRMED** | not stated |
| User population | **UNCONFIRMED** | not stated |

Only one thing is genuinely stated: the brief rewards depth of process. Every
other constraint is an assumption. This document is therefore mostly a
catalogue of what must be asked.

### Words that carry signal

- **"end-to-end"** and **"entire"** — breadth is not the axis. Covering more
  asset types does not help. Covering the full lifecycle of one type does.
- **"depth of process"** — the deliverable is a *process*, with gates, actors,
  and evidence. Not a CRUD screen over a table.
- **"manage"** — implies a control surface (something acts), not a record
  surface (something is written down). Open question, see P0-3.

---

## Phase 2 — Identify Actors

The actor set is **class-conditional**. The lifecycle research produced a
consistent skeleton across all eight classes, and the actors below are the
ones that survived in more than one class.

| Actor | Goal | Main actions | Appears in |
|---|---|---|---|
| Requester | Get what they need | Raise a requirement, justify it | 8/8 classes |
| Approver / budget holder | Control spend and exposure | Approve or reject, own the decision | 8/8 |
| Procurement | Acquire at the right price | Specify, raise PO, three-way match receipt | 7/8 |
| Asset custodian | Know what exists and where | Receive, tag, store, hand over | 7/8 |
| Operator / technician | Keep it working | Deploy, inspect, maintain, repair | 7/8 |
| Compliance / security | Satisfy an external obligation | Verify, certify, sign off, retain | 6/8 |
| Finance | Protect the balance sheet | Depreciate, write off, reconcile | 6/8 |
| Disposal vendor | Take custody of end-of-life | Receive, sanitize, issue certificate | 4/8 |
| **Decision-maker (viewer)** | Know exposure at a glance | Read dashboards, answer audits | all |

**The structural insight worth carrying into the build:** no two of these
actors are served by the same existing product. That is the gap, in every
class researched. A tool that owns one handoff — and makes the handoff
auditable — is more defensible than a tool that tries to own the whole
lifecycle shallowly.

**Primary users:** requester, approver, operator.
**Secondary users:** compliance, finance.
**Administrators:** asset custodian.
**External systems:** procurement/finance system, HR or directory (class-
dependent), disposal vendor.

### Government-specific actors (post-clarification)

The generic table above came from the 8-class survey. Government asset
management adds roles that **no private company has**, and they are where the
process depth lives:

| Actor | Owns | Can block | Notes |
|---|---|---|---|
| **Using department** | The need, and the asset in daily use | — | The "requester" generalised |
| **Stock / custody officer** | Physical receipt, storage, issue | **Yes — cannot release an asset without a custody transfer** | Audited as the weakest link; see Phase 4 |
| **Accounts / finance officer** | The book: cost, depreciation, write-off | **Yes — owns the register** | Owns the *financial* truth only |
| **Condemnation / survey committee** | Declares an asset unserviceable | **Yes — nothing is disposed without it** | A committee *act*, not a form field |
| **Surplus property office** | Disposal route, auction listing | **Yes** | Often a different ministry from finance |
| **Auction platform + treasury** | The money from disposal | — | **A third actor receiving a third kind of money** |
| **Audit body** (AG / CAG / NAO / GAO) | The finding | Retroactively | Findings are public |
| **Disposal vendor / recycler** | Sanitation, destruction, certificate | **Yes** | Certification is a legal gate, not a checkbox |

**The structural insight, now confirmed by research:** the book is owned by
**finance**, the disposition process by the **property/administration
function**, and the money is received by a **third** actor — auction platform
and treasury. No commercial product wants to be the system of record across
all three. That is why every handoff breaks, and it is the seam this product
should occupy.

---

## Phase 3 — Current Workflow

**RESEARCHED — primary audit and rule sources across five jurisdictions
(India, Kenya, Nigeria, Tanzania, UK, US).** The shape of the state machine is
the finding, not the labels.

### The real government asset lifecycle

```
REQUIREMENT → SOURCING CHECK → PROCUREMENT → RECEIPT → ENTRY IN REGISTER
     → (IN SERVICE + CUSTODY) → *ANNUAL PHYSICAL VERIFICATION* →
  ┌─ IN SERVICE (cycle repeats)
  └─ IDENTIFIED UNSERVICEABLE / SURPLUS / OBSOLETE
        → TECHNICAL CERTIFICATE   (e.g. "not fit for further economical use")
        → CONDEMNATION / BOARD OF SURVEY → *CONDEMNATION REPORT*
        → FINANCIAL WRITE-OFF AUTHORITY → VALUATION → MODE DECISION
        → E-AUCTION → PROCEEDS CREDITED TO GOVT ACCOUNT
        → STRUCK OFF REGISTER
```

**The thing most software gets wrong: verification sits in the MIDDLE of the
lifecycle, not at the end.** Annual physical verification is mandatory and
recurring — India *GFR 213(3)* requires it at least yearly, conducted **in the
presence of the custodian**, with a certificate recorded in the stock
register. It is also the step most often skipped.

A **parallel branch** covers loss, theft, and destruction: report under loss
rules → write-off with recovery from officers → **quarterly statement of
write-offs** to the finance authority (India *DFPR 2024 Rule 13*).

### Document artifacts — this is where the depth is visible

| Step | Artifact | Note |
|---|---|---|
| Requirement | Sanction note; availability certificate | |
| Sourcing | **Certificate that no excess property is available** | "buy surplus before buying" is a rule |
| Receipt | **Inspection-cum-Receipt Report (IRR)** | Audits cite this as *the* key receipt control |
| Register | Fixed Asset Register, Stock Register, asset tag, unique number | Two registers commonly exist |
| Verification | **Certificate of verification in the stock register** | Mandatory, annual, custodian must attend |
| Surplus | **Form GFR-10** — Report of Surplus, Obsolete and Unserviceable Stores | |
| Condemnation | **Minutes of the Condemnation Committee / Board of Survey** | Signed by every member |
| Technical | "Not fit for any further economical use" certificate | External workshop, capacity-constrained |
| Write-off | Delegation-of-financial-power sanction | Delegation is capped (India: 10% sub-delegation) |
| Valuation | Independent valuation report; **confidential reserve price** | Valuer must not be the disposer |
| Auction | EMD (10% of net sale value), Sale Order, Delivery Order | |
| Proceeds | **Sale Account (GFR-11)**, treasury receipt | |
| Close-out | **Struck-off entry** + financial statement reconciliation | *The step that rarely happens* |

### How many humans

Nobody publishes a canonical signature count — it must be derived. For **one
vehicle in India**, a defensible count is **5–7 distinct approvals** before it
leaves the gate: workshop technical certificate → condemnation committee
(≥3 members) → competent authority approving the GFR-10 report → write-off
sanction under delegation → accounting officer → reserve-price setter → STA
approval if the lot clears below reserve.

**Not one of them is the person who wants the asset gone.** That is the
structural design, and it is the single best thing to put in a demo.

### The chain breaks at exactly six points

1. **The register is a location-and-value record, not a custody chain.** Assets
   move between people and places with no recorded handover, so the register
   keeps asserting a custodian who no longer has it. Because the receiving
   officer inherits an asset never added to *their* register, the asset exists
   **in two places in the paperwork and zero places in reality.** Mechanisms,
   all audit-confirmed: intra-department transfer with no entry; **officer
   turnover** (the register still names someone who retired); the site copy
   maintained by a vacant or non-financial post while the financial copy sits
   with accounts and never sees the asset — *both internally consistent and
   jointly wrong*; and the disposal side never closed out, so the register
   counts assets that no longer exist.
2. **Verification is skipped or unevidenced.** Himachal Pradesh required it
   twice yearly and it did not happen in **59 of 170** test-checked bodies.
   Andhra Pradesh: **16 of 44**. Some audits report *"no physical verification
   of fixed assets was conducted after 1998-99."* US CBP could not determine
   utilisation for **1,862 of 2,300** vehicles — *the manual data collection
   was too hard.*
3. **The register exists on paper with no usable content.** Kenya FY2020/21:
   no register at all to support **KSh 5,614,749,805** — the audit's words:
   *"Management was in breach of the law."* Kenya FY2023/24: register closing
   at **KSh 82,814,047,266** whose *"accuracy and completeness… could not be
   confirmed."* Department of Energy: **KSh 322.1bn in assets with no tagging
   or serial numbers, "making it impossible to verify or track them
   physically."* Himachal: registers not maintained in **63%, then 82%** of
   bodies tested.
4. **Nobody reuses excess before buying more.** US GAO: agencies took
   **$3.9bn** of excess property against **$206bn purchased** — excess was
   *"not a significant source of supply."* They cannot even quantify the
   opportunity, because the data lacks the detail to correlate.
5. **Assets held by people who no longer work for government.** Nigeria:
   **₦747,749,365.06** of vehicles *"held illegally by former staff"* across 5
   agencies, because the circular requiring return of property before final
   disengagement **is not enforced**.
6. **The money loop fails to close.** Kenya: **KSh 50,745,140** unremitted to
   the Unclaimed Assets Authority, including vehicle-sale deposits outstanding
   **over 5 years**. Nigeria: auctioneers paid proceeds **directly into agency
   coffers** instead of the consolidated revenue fund. US: exchange/sale
   confusion sends proceeds to the **Treasury** instead of the agency's
   replacement budget — a structural, invisible loss.

### Why the process is deep rather than ceremonial

**Because the delay is self-amplifying: the asset depreciates while it waits.**
The audits do not say "we were slow." They say **prolonged idling is the
primary reason vehicles become unserviceable before completing even a decade of
use.**

- **Tanzania NAO:** disposal decisions took **57 to 2,226 days**. Only **548 of
  2,554** proposals processed; **79% still waiting**. Root causes named: late
  condemnation reports, and *"no specified tenure for the Condemnation
  Committee."* The national vehicle register **was a spreadsheet** and excluded
  vehicles held by public authorities.
- **Kochi Corporation (Kerala):** **74.12% of 143 vehicles idling**; of **116
  waste-movement vehicles purchased, only 11 were in running condition**;
  delays of **up to 10 years** from off-road to auction. **Trivandrum 38.18%,
  Kozhikode 27.06%, Thrissur 17.65%.**
- **CAG Report No. 2 of 2021 — the vessel *Matsya Sugandhi*.** The best case
  study in the domain, because it is a **closed feedback loop**:
  - Identified for decommissioning **Jan 2007**; committee formed **May 2010**;
    reserve **₹70 lakh**. The consultant's own market assessment: **₹52–54 lakh**.
  - Four auctions Aug 2011 → Nov 2014 fetch **₹23.28–31.75 lakh** — under half.
  - Committee **reconstituted May 2015**; reserve cut to **₹31 lakh**. Best bid
    Feb–Jul 2016: **₹13 lakh**.
  - Committee **reconstituted again Nov 2018**; reserve **₹16.18 lakh**. Sold
    **June 2019 for ₹17.76 lakh.**
  - **Total delay 136 months. Avoidable expenditure ₹1.14 crore.** The
    committee was reconstituted *three times* because the reserve price was set
    without reference to the market and the realisations were ignored.
- **US GAO:** 3-years-or-60,000-miles replacement standards; one VA centre
  reported **~1,000 sale transactions — none correct**; six agencies sold
  property they had a continuing need for.

**The loop closes on itself, and that is the product.** Committee re-formed →
clock resets → value decays → reserve re-fixed on stale data → worse outcome →
committee re-formed again. A CRUD app cannot express this. A state machine with
document gates, committee tenures, and a **cost-of-delay counter** can.

**The audit body is a reporter, not a gatekeeper, in every jurisdiction except
a handful** (the Philippines' COA is a real gate). That is exactly why the
register diverges: **nobody with enforcement power sits in the loop at the
moment of divergence.**

**MARKED RESEARCH REQUIRED — JURISDICTION IS NOT NEUTRAL.** The rules above are
country-specific and drawn from five jurisdictions. **Which single
jurisdiction's rules govern the sponsor is an open P0 question**, and the depth
of mandate varies by an order of magnitude across them.

### One step is now a commodity — do not build it

**The auction.** GeM's Forward Auction module has run **₹2,200 crore across
13,000+ auctions** since Dec 2021 with 23,000+ registered bidders; MSTC runs the
mandated e-auction service for most Indian ministries; GSA Auctions and
GSAXcess do the same in the US. Selling is fast, well-served, and fully
digitised. It is also the visible, exciting, demo-able part — which is exactly
where a team will lose the day.

---

## Phase 4 — Pain Points

### Confirmed (supported by research, cited in researchassets.md)

1. **Accountability breaks at handoffs.** No commercial product owns the full
   chain from one actor's decision to the next actor's obligation. The
   evidence is structural: in every class, incumbent products each own a
   contiguous *slice* (Intune owns the technical half, ServiceNow owns
   process, Snipe-IT owns the label) and the seam between them is unowned.
2. **Process depth that is externally mandated is unverifiable without
   records.** In data-centre hardware: *most data-destruction failures in
   audits are documentation failures, not wipe failures.* The same pattern
   appears in fleet (statutory retention clocks), plant (OSHA LOTO), and
   end-user devices (NIST 800-88 certificate fields).
3. **Systems of record disagree with physical reality.** In DC hardware, four
   state machines (physical, logical, financial, compliance) can hold
   contradictory values and nothing reconciles them — a server can be
   financially written off while still carrying production traffic.
4. **The best-of-breed tools are expensive, slow, or single-slice.** ServiceNow
   ITAM is ~$100/user/month with a multi-month deployment. A funded competitor
   in the SaaS-licence class shut down rather than continue.

### Confirmed — government physical assets (post-clarification)

These are **stronger and more specific** than the generic findings above, and
they are the better evidence to build the product on. All figures are from
published national audit reports, cited in `docs/research.md`.

5. **The asset register and physical reality diverge, at scale, everywhere.**
   The finding repeats across four continents, which makes it a *structural*
   gap rather than one agency's incompetence:
   - **NY State Comptroller 2023-S-17** — **17,887 devices** categorised
     "absent" and still on the books; **82% because location was unknown**.
     Auditors searched stockrooms for 102 listed devices and **could not find
     94**. **~2,500 devices** stuck "In-transit" because stockrooms never
     scanned receipt. **924** new or lightly-used devices marked for
     destruction, valued **$530,000–$660,000**, including 175 unused laptops
     on a single pallet.
   - **NYC Dept of Education**, re-audit 2.5 years later — **35% of ~14,000
     machines** unaccounted for in a nine-site sample; only **234 of 1,817**
     previously-missing items ever accounted for; **1,090 never even
     attempted**. Still running decentralised records.
   - **NARA OIG 26-R-03** — the incumbent asset module *"cannot be relied upon
     as a complete or accurate record"*.
   - **ICAO Internal Audit** — **1,158 of 1,479 records (78%)** had no
     barcode, in offices with *"quite similar"* budgets and staff.
   - **US Treasury OIG** — three authorities each reported losses with no
     reconciliation, so *"we do not believe the number of computers reported
     lost or stolen is reliable."*

6. **Root cause is always a handoff nobody owns.** NY State's own root cause:
   *"stockrooms often did not scan the devices as they were supposed to on
   arrival."* And NY's remedy was to **buy a Hardware Asset Management
   module** — a bolt-on product, not a process fix. NARA's Recommendation 3 is
   verbatim our product statement: *"Implement an IT asset management
   lifecycle approach that documents the complete transaction history of an IT
   asset from its acquisition to its excess from service."*

7. **Governments are formally required to keep two registers in sync by hand.**
   A live government condemnation policy states: *"the physical Asset Register
   and the same has to be updated in the Inventory Software on timely basis."*
   Manual double-entry is the **mandated** process. Automating that join is
   both valuable and completely uncontroversial.

8. **Governments keep two tiers of register simultaneously.** Above the
   capitalisation threshold an asset is depreciated and GL-tracked; below it,
   it is still tagged, barcoded and physically counted as a *stewardship
   resource*. The threshold is **not uniform across departments** — the same
   device can sit on two different books in two offices of the same
   government. (US federal equipment thresholds range $0–$250,000; a UK force
   raised its threshold from £1,000 to £5,000 explicitly because of laptops.)

9. **The disposal chain is legally gated and nobody models it.** Sanitisation
   certification is a *precondition* for release — one state's rule: *"The
   Surplus Property Office will not receive any IT equipment without a properly
   completed IT Equipment Disposal Certification form."* Disposal is a minuted
   public event with an auction committee, witnesses, and proceeds deposited
   into the government account. The **register write-back is a separate manual
   transaction** from the proceeds receipt, reconciled by hand.

10. **The department already has a mandated register, and it already failed.**
    The one hard Gujarat-specific finding located: **CAG, Government of Gujarat,
    Audit Report (Economic Sector), year ended 31 March 2012, Chapter III,
    para 3.2.9.2 — "Non-updation of Bar Chart Register."** Each R&B division is
    required to maintain a *computerised Bar Chart Register* of all roads and
    works carried out in the previous five years. It was **not updated after
    2009-10 in ten divisions** and **not updated after 2010-11 in two
    divisions**. The department replied in September 2012 that action was
    *"being taken."* Twelve separate divisions, twelve separately stale
    registers, one department-level reply. **The documented failure mode is a
    register nobody updates — which is the product thesis in one sentence.**

11. **Utilisation is a void in the rules, and the void is load-bearing.**
    GFR mandates **annual verification** of fixed assets, with a certificate in
    the stock register, in the presence of the custodian. GFR's only surplus
    trigger is **stock held over one year** (GFR 214) — a *consumables* rule that
    does not apply to a machine. **Nothing requires anyone to record that a
    machine was used.** Therefore a **₹1.2 crore excavator can be verified
    every year, pass every year, and never leave the division yard for six
    years, with no rule broken anywhere.** Not negligence. Not even
    non-compliance. *A complete compliance that produces total invisibility.*
    The existing verification pass actively **certifies an idle machine as
    compliant** — it cannot distinguish "present and working" from "present and
    dead for six years." That is a defect in the control, not a missing
    feature, and closing it is what a lifecycle product is for.

### Hypothesized (reasonable, unvalidated — do not present as fact)

1. ~~Teams doing this work use spreadsheets at the seams.~~ **CONFIRMED** for
   government: the national vehicle register in Tanzania *was* a spreadsheet,
   and excluded vehicles held by public authorities.
2. The decommission/disposal step is the one most likely to be skipped, since
   it is manual, slow, and has no immediate operational payoff. **CONFIRMED** —
   79% of Tanzania's disposal proposals were still pending, and Kenya's
   Judiciary excluded 26 disposed vehicles with no disposal summaries at all.
3. Approval steps are the friction users complain about most, but the ones
   they would refuse to give up. **SUPPORTED** — the root cause of the Tanzania
   backlog was *"no specified tenure for the Condemnation Committee."*
4. A commissioning or baseline capture step, once missed, is permanently
   unrecoverable. **CONFIRMED in government form** — where a physical
   verification never happened, audits state the shortfall *"could not be
   ascertained"* at all.
5. **NEW — the strongest hypothesis in this document, and it is the product:**
   *the register is the output of a document-and-approval process, not the
   source of truth.* The source of truth is the signed verification
   certificate plus the condemnation file. A register row that no document
   backs is a claim, not a fact.

---

## Phase 5 — Class Evaluation

> ## ⚠ SUPERSEDED BY THE GUJARAT R&B CLARIFICATION
>
> The analysis below ranked **vehicles & fleet** for *government assets in
> general*. It was correct on its own terms and is retained as an audit trail.
>
> It no longer applies. The sponsor is **Gujarat's Roads and Buildings
> Department**, which is not a general-government sponsor. Under that
> constraint:
>
> 1. **Vehicles are out of the R&B remit as a centrepiece.** R&B does hold
>    vehicles, but its distinctive holdings are **construction plant and
>    machinery** and its public works. Recommending a fleet product to a roads
>    department would read as having not read the department.
> 2. **The jurisdiction P0 is closed.** India, Gujarat state rules.
> 3. **The current recommendation is construction plant & machinery** — see
>    `docs/research.md`, section *Gujarat R&B: What the Department Actually
>    Owns*, sections D and G.
> 4. **Roads and bridges are out**, on two independent grounds: Indian
>    government accounts *do not depreciate physical assets and do not expense
>    end-of-life losses*, so there is no accounting substrate for a lifecycle
>    product; and MoRTH's **IBMS** and **RAMS** already own the bridge/road
>    inventory slot nationally.
>
> **One asset class: construction plant & machinery of a single R&B division.**
> The spine is the **utilisation void** — GFR mandates annual verification but
> nothing mandates recording that a machine was *used*, so an idle ₹1.2 crore
> machine can be verified every year and pass every time. The depth is the
> condemnation-to-disposal chain.

**RESEARCHED.** The domain is fixed (government physical assets); the class is
the live P0. Full comparison in `docs/researchassets.md` and `docs/research.md`.

### The standard taxonomy

Governments' physical assets, per **IPSAS 45** (effective 1 Jan 2025, superseding
IPSAS 17): land, operational buildings, infrastructure, machinery, motor
vehicles, aircraft, ships, weapons systems, furniture and fixtures, and office
equipment.

**Two exclusions that matter:**
- **Software and licences are intangible** (IPSAS 31) — the IFAC module lists
  "computer software" explicitly under intangible. This is why the earlier
  cloud and SaaS classes are now eliminated *on definition*.
- **Inventories are physical but are a different product** and must be excluded
  **explicitly**, not implicitly. Easy to build the wrong thing here.

### Class comparison

| Class | Mandated process depth | Explainability | Demo data | Verdict |
|---|---|---|---|---|
| **Vehicles & fleet** | **Deepest, statute-traceable** — condemnation by a named board, two-valuation rule, signed bill of sale, fixed reporting deadlines, traceable to numbered regulations in 5 jurisdictions | **Best** — 74% of a fleet idling is a number anyone grasps | **Best** — audit findings are public and unit-level | **LEAD** |
| Medical equipment | Deepest *per-unit* regime — decommissioning interlocks, PPM frequencies, uptime targets | Good | Weak — census data, not lifecycle records | Strong alternate |
| IT hardware | Good, but dual-tier register complexity | Medium — "laptops are boring" | Good | Weaker; most digitised already |
| Plant & machinery | Jurisdiction-dependent | Medium | Weak | **Fails in India** — see below |
| Buildings / property | Deep but the register often does not exist | Medium | **None** | Disqualifying |
| Infrastructure (roads, water) | Probably second-deepest in reality | Good | None | **Unassessed — do not assume cleared** |
| Heritage assets | Distinct regime (IPSAS 45) | Low | None | Deliberately not assessed; a trap here |

### Why vehicles lead

1. **The process is traceable to numbered regulation** in five jurisdictions on
   three continents — Tanzania PFR Regs 253–257, Jamaica FAA Act + Financial
   Management Regulations 2011, South Carolina Code 1976 §§1-11-220–340,
   44 Ill. Adm. Code 5010, Florida DMS. A judge can verify any claim.
2. **The failures are independently documented** in published national audit
   reports, so the demo's numbers are real rather than invented.
3. **It is the smallest honest slice.** The UN's own building-vs-equipment test
   settles the scope argument: the raised flooring and HVAC are *building*; the
   **servers and racks are machinery and equipment**. Same logic for vehicles —
   **the depot is a location field on a vehicle record**; modelling the depot
   pulls in the entire property problem for zero process gain.
4. **Best demo data of any class**, and it comes from audit findings rather
   than imagination.
5. Estimated **5–7 hours for three people.**

### The named weaknesses of the vehicles pick — answer these in advance

1. A judge may call fleet management a **solved commercial category**. Defend
   by framing the product as *accountability and write-off assurance*, leading
   with the **missing bill of sale**, not the vehicle list.
2. A small department has too few vehicles. **Fictionalise a central state or
   national fleet bureau** — which is also where the mandate is deepest.
3. The process is deep but **narrow**: one dominant branch (disposal) and one
   dominant failure mode (missing paperwork). A judge weighting breadth over
   depth may prefer medical.
4. It reads as a "vehicles app" **unless the register, the board, the
   valuation, and the proceeds are all visible in the demo.**

### The jurisdiction trap

**In India, generic plant & machinery is not a viable pick** — computers and
furniture are booked under *revenue* object heads and never captured as capital
expenditure, and *"no de-recognition of asset takes place even after the asset
is no longer in use."* The mandates are not there to model. Conversely,
India's **category-specific regulators (AERB, BMMP, IPHS) make the medical and
vehicle picks stronger there than anywhere else researched.**

In the **UK, Australia, and New Zealand** the strongest mandates sit in
*framework instruments*, not statute.

**Consequence: "the class with the deepest mandated process" is only
well-posed given a jurisdiction.** If the sponsor is Indian, medical equipment
would likely overtake vehicles. **This is a P0 question, not a detail.**

### Two things deliberately NOT assessed

- **Heritage assets** — IPSAS 45 now requires recognition where reliably
  measurable and adds deemed cost. A genuinely distinct regime, skipped
  because it is a trap for a 10-hour build.
- **Infrastructure** (roads, water, power, bridges) — network-level, not
  item-level, with condition-index and multi-decade renewal modelling. **Very
  plausibly the second-deepest class in reality. It is unassessed.** If someone
  proposes it, that proposal has not been researched and must be treated as
  open.

### The honest residual

The class comparison is assembled from **individual national instruments**. No
consolidated cross-country survey of mandated lifecycle depth by asset class
was found. The consistency claim for vehicles is an observation across sources,
**not a finding from any single source** — label it as inference in any
decision record.

---

## Phase 6 — Functional Requirements

**Class-independent core. These hold for any class chosen.**

### MUST

- An asset record as the single system of record, with a durable identity
  (serial / asset tag) bound to the thing
- A **state machine** where illegal transitions are impossible, not discouraged
- An **append-only event log** of every state change: who, when, from what
  state, to what state, on what evidence
- At least one **human approval gate** enforced server-side, with the
  approving identity recorded
- A **lifecycle timeline** view per asset, rendered from the event log
- Role-based authorization, enforced in the backend
- A **decommission / disposal** path that refuses to complete until its
  required evidence is present
- Evidence attachments tied to transitions (a certificate, an approval, a
  dependency check)
- An exposure/exception view: what is stuck, what is at risk, what is overdue

### Government-specific (post-clarification)

These are additions the government domain demands and a private-sector asset
tool would not have:

- **A physical verification pass as a first-class workflow** — a verifier
  walks the register, scans the tag, and the system computes
  **found / not-found / found-in-wrong-place / found-unregistered**, then
  **quantifies the exposure in currency**. This is the highest-value single
  feature in the domain and it is estimated at ~4 hours, not 12.
- **A gated document checklist per transition** — you may not move from
  `IN_SERVICE` to `PENDING_CONDEMNATION` unless: a verification certificate
  exists, the tag was scanned within 12 months, the technical certificate is
  attached, and the row has an assigned custodian.
- **Committee quorum enforcement** — condemnation requires **three distinct
  signatures**, and the **write-off authority must be a different person from
  the committee** (separation of duties, mandated in Lagos and Nigeria).
- **A custody chain, not just a location field** — issuing an asset must
  create a custody transfer, because officer turnover is a confirmed root
  cause of divergence.
- **A cost-of-delay counter** — days since declared-unserviceable, against a
  target, with accrued idle maintenance and depreciating value. This is the
  demo's punchline and it is defensible in a judging room.
- **A recovery-rate view** — reserve price vs realised price vs time-to-sale.
  Real anchors: ₹23–32 lakh against a ₹70 lakh reserve, then ₹13 lakh against
  ₹31 lakh, finally ₹17.76 lakh. A documented collapse to roughly a quarter of
  the original reserve, driven purely by procedural delay.
- **A working-paper view** — an audit-query list with ageing and a
  "remains unresolved as at <date>" status, seeded from real prior-year
  findings. Half a day, and it makes the domain instantly credible.

### SHOULD

- A dependency constraint that can block a state change and explain why
- A second-approver rule for the highest-consequence transition
- Seeded demo data that shows a partially-completed lifecycle, not a clean one
- A printable/exportable audit record for one asset
- Seeded failure states from real audit findings: a condemnation report with no
  valuation; approved disposal with no bill of sale returned; a board report
  with no disposition record; a removal date missing so a scrapped vehicle
  still shows Live

### COULD

- Reconciliation against a simulated external system of record
- Cost or exposure figure per asset
- Due-by dates and overdue flags
- Photo/attachment evidence

### Explicitly deferred

See "What NOT to Build" at the end.

---

## Phase 6b — Non-Functional Requirements

Ranked by relevance to *this* problem. The brief rewards depth of process, so
auditability and consistency outrank throughput.

| Rank | Property | Why it matters here |
|---|---|---|
| 1 | **Auditability** | The product's claim is accountability. An unauditable action is not an accountable one. |
| 2 | **Correctness of state** | An illegal transition that succeeds destroys the product's entire premise. |
| 3 | **Explainability** | Named in the brief. Judges must understand the model in 90 seconds. |
| 4 | **Demo reliability** | No external dependency may be able to break the live demo. |
| 5 | **Security / authorization** | Approvals must not be forgeable by the wrong role. |
| 6 | **Consistency** | Four disagreeing state machines are the *subject matter*, not a bug. |
| 7 | Maintainability | Interview defensibility. |
| 8 | Latency | Not a real constraint at demo scale. |
| 9 | Scalability | Not a real constraint at demo scale. |
| 10 | Offline / i18n / a11y | Not stated. Do not build. |

---

## Phase 7 — Data and Entities

Conceptual only. Schema belongs in `database-design`, after the class is fixed.

| Entity | Created by | Owned by | Read by | Changes state |
|---|---|---|---|---|
| **Asset** | custodian (at receipt) | custodian | all | via the lifecycle state machine only |
| **Lifecycle state** | system | system | all | one legal value at a time |
| **Event** (append-only) | system, on every transition | immutable | all, via timeline | never |
| **Approval** | approver | approver | requester, compliance | requested → granted/denied |
| **Evidence** | actor, at a transition | attached to event | compliance, auditor | immutable once attached |
| **Role** | admin | admin | all | assignment only |
| **Dependency** | operator | operator | system (blocks transitions) | graph edges |

**The load-bearing idea:** `Event` is append-only and `Asset.lifecycle_state`
is derived-or-validated-against it. One of the two is truth and the other is a
cache; deciding that wrongly is the most common way this kind of system rots.

---

## Phase 8 — External Systems

| System | Class | Decision |
|---|---|---|
| Procurement / finance | all | **MOCKABLE FOR HACKATHON** — mock with seeded records |
| HR / identity directory | end-user devices | **MOCKABLE** — Azure AD Graph is a known 2h permission trap |
| MDM / device manager | end-user devices | **MOCKABLE** — cite the published state enum, do not call the API |
| Monitoring / DCIM export | DC hardware | **MOCKABLE** — NetBox-shaped fixtures, no hardware needed |
| Hardware telemetry (Redfish/SNMP) | DC hardware, network | **DEFER** — no hardware at a hackathon |
| Telematics | fleet | **DEFER** — needs hardware and an enterprise contract |
| CMMS / sensor feed | plant | **DEFER** — MQTT live beat is a stretch, not core |
| Email / notifications | all | **OPTIONAL** — in-app only is enough for the demo |

**Recommendation: every integration is mockable, and the product should be
architected so that mocking is the default path, not a fallback.** The brief
says "end-to-end" without defining it as "against real systems"; a
seeded-but-honest dataset is a legitimate reading and carries zero demo risk.

---

## Phase 9 — Existing-System Research

**DONE.** See `docs/researchassets.md` (8 classes, 8 research agents) and
`docs/research.md` (EAM product landscape: IBM Maximo, ServiceNow EAM,
MaintainX, ISO 55000).

**Scope update:** an organizer clarified that assets are physical government
assets. The product patterns in `docs/research.md` still hold. Its critical
facility-equipment framing is now a valid **candidate** for the government
scope, not a selected class. Do not treat it as confirmed.

---

## Phase 10 — Define the MVP

### The asset class is not yet fixed. See Phase 14, P0-1.

### Core demo workflow (class-independent shape)

The MVP must be one complete chain with two different humans in it, ending in a
refusal or a certificate:

```
Actor A requests → Actor B approves (recorded)
  → asset acquired, received, tagged
  → asset deployed and put in service
  → asset begins to fail; a work item is raised and completed
  → Actor C requests decommission
  → **system REFUSES** — required evidence missing (a dependency still
    references this asset, or a required certificate was never captured)
  → Actor C resolves the blocking evidence
  → decommission completes, certificate is issued
  → the timeline shows the entire chain with both approvals attached
```

**The refusal is the product.** A system that lets you do everything is a CRUD
app. A system that says "not yet, here is exactly what is missing, and here is
who must supply it" is depth of process, and it is legible to a judge in one
sentence.

### First vertical slice

Request → approve → receive → tag. Small, runnable, proves the state machine
and the event log before any complexity is added.

---

## Phase 11 — Stretch Features

Must not block the MVP.

- Live reconciliation against a simulated external system
- Cost / exposure figure per asset
- Overdue and at-risk queues
- Anomaly or "this looks wrong" hint
- Second-approver flow
- Printable audit pack

---

## Phase 12 — Technology Fit

**DEFERRED — deliberately.**

Decision **D-006** removed the pre-built starter templates, on the grounds
that a pinned stack pre-commits to an answer and contradicts the rule that the
stack is selected *from* the problem. The stack must be selected here, after
the class and the requirements are fixed.

**Standing selection procedure** (use when Phase 13 assumptions are settled):

1. Product type is a **workflow application** with a relational, strongly
   stateful domain and an audit trail. Not a dashboard, not realtime, not
   AI-heavy, not a data pipeline.
2. Relational data with real invariants (illegal transitions, append-only
   events, foreign keys) → a relational database is justified, not optional.
3. No large files, no streaming, no offline, no heavy search.
4. No AI requirement has been identified. **Do not add AI to justify the
   project.** Nothing in the research supports it.
5. Optimize, in order: implementation speed → team familiarity → demo
   reliability → requirement fit → explainability → deployment simplicity.
6. Deployment must be one command and must not require a paid account or a
   cloud account to demo.

---

## Phase 13 — Assumptions

| # | Assumption | Impact if wrong | Validation |
|---|---|---|---|
| A1 | Time budget is roughly one working day | Changes scope, not architecture | ask sponsor |
| A2 | A single physical government asset class will be selected | Choosing the wrong department/class invalidates the demo story | ask sponsor — P0-1 |
| A3 | Seeded data is acceptable for "end-to-end" | Demo loses its strongest beat if a real integration is required | ask sponsor — P0-2 |
| A4 | Single organisation, not multi-tenant | Adds auth and row-scoping work | ask sponsor — P1-3 |
| A5 | 3–4 actors is enough; more is sprawl | Approval UI grows non-linearly | ask sponsor — P0-3 |
| A6 | One asset class, deeply, beats several shallowly | If breadth is actually scored, this is the wrong product | inferred from "end-to-end"/"entire"/"depth" — verify with sponsor |
| A7 | Auditors care about documentation, not the physical act | If false, the refusal gate is the wrong hook | research-backed for DC/fleet/plant; unvalidated |
| A8 | No AI/ML is required | Wasted effort if a judge expects it | ask sponsor — P2 |

**A2 and A6 are load-bearing.** A6 is the assumption that produced the entire
recommendation in `docs/researchassets.md`, and it is inferred from three
words in a 25-word brief. It should be the first thing confirmed.

---

## Phase 14 — Open Questions

Each question is included only if its answer **changes the build**.

### P0 — blocks implementation

> **P0-1 is ANSWERED.** Jurisdiction is India / Gujarat state rules, and the
> sponsor is the Gujarat R&B Department. The re-ranking consequence of that
> answer is recorded in the Phase 5 supersession note.

1. **Can the team obtain the Gujarat R&B Works Manual and the Gujarat DFPR
   monetary delegation schedule?** This is now the **highest-leverage open
   question in the project** and it is a person-in-the-loop task, not a search
   task. Neither document is on the open web in readable form, and together
   they define the exact condemnation gates, signature counts, and write-off
   ceilings we intend to model. **If they cannot be obtained, every
   Gujarat-specific claim softens to "modelled on GFR practice"** — still
   defensible, weaker in the room. *This is the top pre-event action.*
2. **Which asset class, and which division?** Researched lead is
   **construction plant & machinery** of a single R&B division. Unasked and
   potentially inverting: does the sponsor mean the **mechanical wing**
   (plant, workshops, fleet) or the **roads wing**? If roads, the
   recommendation changes and the class question reopens.
3. **Does "end-to-end" mean a real external system, or a complete internal
   workflow over realistic data?** Note: **no open unit-level government asset
   register exists for any class** — every dataset must be synthesised, so
   "seeded from audit findings" is the only honest path either way.
4. **Single actor or multiple roles?** If the product needs a condemnation
   committee, it needs an auth model, a role model, and multiple demo users.
   Research says **fake it with a role switcher** — but only if the committee
   is demonstrable without real login.
5. **What artifact must "manage" produce?** For this domain the candidates are
   sharply drawn: an **idle-capital exposure report**, a **bill of sale /
   write-off assurance file**, an audit working paper, a verification
   certificate register, or a **cost-of-idle report**. This is the
   deliverable.

### P1 — important, can proceed temporarily

5. Is retirement/disposal genuinely in scope, or does "lifecycle" mean the
   operational phase only? Disposal is the deepest and most defensible part —
   worth confirming it is not out of bounds.
6. What is the real scale — asset count and how many distinct types? Decides
   generic-core-plus-config versus typed tables.
7. Is there an existing system we are meant to replace or integrate with? A
   sponsor with an existing spreadsheet changes the MVP shape.
8. Single organisation or multi-tenant?
9. Are there audit or regulatory obligations we must satisfy, and whose?

### P2 — can defer

10. Does the judging panel expect any AI/ML component?
11. Realistic live demo or recorded demo if the network fails?
12. Presentation format, and who the audience is.

---

## Phase 15 — Risks

| # | Risk | Type | Likelihood | Impact | Mitigation |
|---|---|---|---|---|---|
| R1 | Class is wrong within the confirmed physical-government scope | Product | Medium | **Total** — the demo story is invalid | P0-1 before any code |
| R2 | Scope sprawl into a second asset class | Time | **High** | High — the exact failure mode of this brief | One class. Write it down. Refuse additions |
| R3 | Building a CRUD app with a status column, not a process | Product | **High** | High — fails the stated scoring axis | Make illegal transitions impossible; the refusal is the demo |
| R4 | Depth becomes unexplainable in 90 seconds | Product | Medium | High — loses the other scoring axis | One refusal beat, one certificate, one timeline. Nothing else |
| R5 | A real integration is required and is unavailable or slow | Demo | Unknown until P0-2 | High | Mock-first architecture; fixtures committed to the repo |
| R6 | Approval/auth sprawl eats the time budget | Time | **High** | Medium | Cap at 3 roles. One gate for MVP, second-approver is stretch |
| R7 | Physicality (racks, cabling, floorplans) consumes the day | Time | Medium | High | One physical dimension only. No topology graph |
| R8 | "Depth of process" is read as more features, not fewer states with harder gates | Product | Medium | Medium | State the model in one sentence in the demo; let a refusal prove it |
| R9 | Time budget is shorter than assumed | Time | Medium | Medium | Vertical slices, each runnable |
| R10 | Judges ask why not the incumbent | Interview | **High** | Medium | The gap is the handoff seam, not features. Have the answer ready |

---

## Phase 16 — Recommended Build Order

Class-conditional steps are marked. Ordered so **each stage leaves the product
runnable**, and so the demo beat is reached as early as possible.

| # | Step | Why here |
|---|---|---|
| 1 | Roles + role switcher (no real auth) | Needed to demo any gate. Faked deliberately. |
| 2 | Asset record with identity fields | Foundation |
| 3 | Lifecycle state machine, illegal transitions rejected **server-side** | The load-bearing piece. Everything else proves it works. |
| 4 | Append-only event log + per-asset timeline | The audit trail is the product's claim |
| 5 | **Physical verification pass** — scan, compute found / not-found / wrong-place / unregistered, quantify exposure | **Highest value per hour (~4h est). Do this before the disposal chain.** |
| 6 | First approval gate enforced by role | Proves the refusal works |
| 7 | Acquire → receipt (IRR) → register → custody transfer | Note custody transfer is separate from entry — it is a confirmed root cause |
| 8 | In service → verification cycle repeats | Verification sits mid-lifecycle, not at the end |
| 9 | Unservicable → technical certificate → condemnation (3 signatures) | Quorum enforced |
| 10 | Write-off authority as a **distinct** actor from the committee | Separation of duties. Mandated. |
| 11 | Valuation → reserve price (confidential) | Valuer ≠ disposer |
| 12 | **Disposal → REFUSAL → bill of sale attached → proceeds credited → register struck off** | **The vertical slice that makes it a product** |
| 13 | Cost-of-delay counter + recovery-rate view | The punchline, computable from our own data |
| 14 | Audit working-paper view, seeded with real prior-year findings | Cheap credibility, half a day |
| 15 | *Stretch:* reserve re-pricing loop, second approver, surplus-before-purchase check | Must not block |

**Steps 1–4 are class-independent.** Step 12 is the demo. Nothing after step
13 matters if step 12 is not working.

**Deliberately excluded from this build:** the auction engine, the depreciation
engine, barcode generation, real RBAC, and the building itself.

---

## What NOT to Build

### The four domain traps, in order of how likely they are to eat the day

1. **You will build the auction.** It is the visible, exciting, demo-able
   part — and it is now a **commodity** (₹2,200 crore across 13,000+ GeM
   forward auctions since 2021). The moment you start writing *"bid history /
   auto-extend / highest bid wins / EMD"*, you have already lost the day.
2. **You will model asset types generically.** A configurable asset-type
   engine with per-type rules does not fit the timebox. Pick one class,
   hard-code the rest, and say so on screen: *"MVP scope: road vehicles only;
   the state machine is generic, the rule set is vehicle-specific."*
3. **You will build real auth and real RBAC.** Six roles × document-gated
   transitions × audit trail is genuinely 2–3 days done properly. Fake it: a
   role switcher and an append-only events table. Nobody has ever lost a
   demo because the login screen was a dropdown, and plenty have lost because
   RBAC ate hour seven.
4. **You will ship an inventory CRUD app.** If the demo can be summarised as
   *"assets have a status field,"* it is indistinguishable from any asset SaaS
   and loses on the only axis being judged. **The differentiator: in
   government, the register is the OUTPUT of a document-and-approval process,
   not the source of truth.** The source of truth is the signed verification
   certificate plus the condemnation file.

### Also out of bounds

5. **A depreciation or GL accounting engine.** SAP, Oracle, ERPNext, Odoo,
   OpenGov have years of correctness. **Read book value as an input.**
6. **Barcode/QR generation and GS1 standards compliance.** Commodity.
7. **Asset CRUD / a register.** Snipe-IT is a weekend; ERPNext ships it free.
   No judge awards this.
8. **AI of any kind.** No requirement supports it. Adding it to look
   sophisticated is the opposite of depth of process.
9. **A second asset class.** The single most likely way to fail this brief.
10. **Topology, cabling graphs, or 3D.** Physicality is a scope trap.
11. **The building or the depot.** Model the **vehicle**, not the depot
    building. See Phase 5.
12. **Multi-tenancy**, unless P1 says otherwise.
13. **Live telemetry.** No hardware at a hackathon.
14. **Notifications, email, mobile.** In-app is sufficient.
15. **Timeline scrubber, animations, theming.** Cosmetic, and last.

---

## Status

| Item | State |
|---|---|
| Problem parsed | done |
| Sponsor clarification | **received — government physical assets, Gujarat R&B Department** |
| Jurisdiction | **CLOSED — India, Gujarat state rules** |
| Actors | done — generic + government-specific |
| **Mandated lifecycle** | **done — researched from primary audit/rule sources, 5 jurisdictions** |
| **Failure modes** | **done — quantified, cited, cross-jurisdiction** |
| **Gujarat R&B holdings** | **done — see `docs/research.md`; Bar Chart Register finding recorded** |
| **Class evaluation** | **done — construction plant & machinery leads; roads/bridges and vehicles both out** |
| **Gujarat Works Manual / DFPR** | **NOT OBTAINED — top pre-event blocker, see P0-1** |
| Requirements | MUST/SHOULD drafted; class-specific set pending |
| Data model | conceptual only — blocked on class confirmation |
| Open questions | 5 at P0 |
| Stack | deliberately not selected (D-006) |
| **Asset class** | **construction plant & machinery — recommended, needs sponsor confirmation** |
| Implementation | none |

**Nothing here is implemented. No stack has been chosen. The project has not
started.**

**The single highest-leverage action right now is not coding.** It is obtaining
the **Gujarat R&B Works Manual** and the **Gujarat DFPR delegation schedule**.
Both are outside the open web, both define the gates we intend to model, and
no amount of additional research substitutes for them.

**Superseded recommendations, retained for audit trail:** critical facility
equipment → emergency generators → bridges → vehicles & fleet → **construction
plant & machinery (current)**. See `docs/research.md` for why each was dropped.
