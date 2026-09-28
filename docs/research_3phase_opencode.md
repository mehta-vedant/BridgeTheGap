# Gujarat R&B Bridge Lifecycle — Three-Phase Research Record

**Compiled:** 28 September 2026
**Scope:** Pre-construction → Construction → Post-construction, for bridges owned by the
Gujarat Roads & Buildings Department. India-wide evidence, Gujarat-specific wherever it exists.
**Status:** Phases 1 and 2 complete. Phase 3 partially complete — see §4.9.

---

## §0 How to read this document

This is an **evidence record**, not a product document. It is separated from opinion on purpose.

| Marker | Meaning |
|---|---|
| **[V]** | Verified against a primary official source that was read |
| **[S]** | Secondary reporting — outlet named, unconfirmed against the primary document |
| **[A]** | Our own analysis or tabulation of primary data. Not a published statistic. |
| **`NOT ESTABLISHED`** | No source found. What was searched is stated. **Do not infer.** |

Two rules were applied throughout and they are the reason this document exists:

1. **No claim without a source.** Where a claim could not be sourced it is marked, not softened.
2. **No invented arithmetic.** In particular there is no expected-value-of-a-life calculation
   anywhere in this document, and there must never be one in the product.

§7 is the only section containing our conclusions. It is fenced off deliberately. Everything
above it is either sourced or explicitly marked as a gap.

### A correction to the record

An earlier draft of this material attributed a liability-shielding argument to
**IRC:130-2020**. That was a misattribution and has been removed. IRC:130-2020 is
*Guidelines for Road Asset Management System*; its scope clause states it
**"does not cover Bridge Assets."** It cannot be cited as authority for anything
concerning a bridge record. It remains quotable **only** as evidence of that exclusion,
which is itself one of the most useful facts in this document.

→ https://law.resource.org/pub/in/bis/irc/irc.gov.in.005.2024.pdf

---

## §1 Evidence status at a glance

| Phase | Research | Written here | Blocking gaps |
|---|---|---|---|
| **1. Pre-construction** | Complete | Yes, §2 | Gujarat's own contract form could not be opened; Gujarat LA delegate schedule |
| **2. Construction** | Complete | Yes, §3 | Gujarat R&B's own DLP, security and retention terms |
| **3. Post-construction** | **Partial** | Yes, §4.1–§4.8 | Defect taxonomy, decision authority, service life, DLP enforcement in practice |

Phase 3 is the weakest and it is the phase where the product's gate lives. §4.9 states
precisely what is missing. This is not a footnote — it is the next piece of work.

---

## §2 PHASE 1 — PRE-CONSTRUCTION

### 2.1 The stage definition

**[V]** The Indian bridge project is defined in three stages by
**IRC:SP:54** — *Guidelines for Survey and Investigation for Bridge Projects*:

| Stage | Instrument | When required |
|---|---|---|
| 1 | **PFR** — Preliminary Feasibility Report | **Required** for a bridge on a missing link; **optional** for widening or rehabilitation |
| 2 | **FSR / PPR** — Feasibility Study | Required before commitment of major expenditure |
| 3 | **DPR** — Detailed Project Report | Required for sanction. **Includes the tender documents** |

The asymmetry matters: a missing-link bridge is a project with new alignment, new
land, new approvals. A rehabilitation is a project on an existing alignment where
land is already held. **The pre-construction risk profile is not the same, and the
product must not treat it as the same.**

**[V]** CAG found the appraisal discipline failing at national level: projects
"developed based on **deficient cost-benefit study** or **without getting detailed
project reports prepared**", DPR specifications "not found suitable for site
conditions", and **NHAI never prepared the MoRTH-mandated DPR guidance document.**
Zero of 35 sanctioned Multi-Modal Logistics Parks were developed.

→ CAG Report No. 19 of 2023 (MoRTH, Bharatmala Pariyojana), tabled 10 Aug 2023
→ https://cag.gov.in/webroot/uploads/download_audit_report/2023/Report-No.-19-of-203--Bharatmala-English-064d5db7bc63c20.06754442.pdf

### 2.2 Design inputs — where a 100-year claim comes from

**[V]** **IRC:5-2015 Clause 104.1** gives a **design life of 100 years** for bridges.

**[V]** The design discharge standard was tightened. **IRC:5-1998 §103.1** specified the
**50-year** return period; **IRC:5-2015 §106.3.1** moved it to the **100-year** return
period. A bridge designed to the older code was designed against half the flood that
the current code requires it to survive.

**[V]** **IRC:5-2015 §104.2** specifies a 13-item data pack as the minimum design input
set. This is the designer's checklist and it is the natural source for a per-asset
"design basis" record.

**Product implication.** Design life and design discharge are both **recordable facts
with a code citation**. They belong in the bridge's provenance block. Neither is
currently recorded anywhere per-asset that we could find.

### 2.3 The design review ladder

**[V]** **IRC:SP:57-2000** defines a quality-assurance ladder, **Q-1 to Q-4**, for bridge
design and construction:

| Level | In-house check | Third-party check | As-builts |
|---|---|---|---|
| Q-1 | yes | no | **not required** |
| Q-2 | yes | yes | **required** |
| Q-3 | yes | yes | required |
| Q-4 | yes | yes | **100% third-party check** |

**Product implication.** A Q-1 project has **no as-built drawing requirement at all**.
A Q-4 project has full third-party verification. **These are different evidentiary
worlds and a single `as_built_ref` field on the bridge is a lie unless it records
which ladder applied.** This is a schema requirement created by a code.

### 2.4 The cost model — where pre-construction fails in rupees

**[V]** From CAG Report No. 19 of 2023:

| Figure | Sanctioned | CCEA-approved | Overrun |
|---|---|---|---|
| Overall cost | **₹32.17 cr/km** | ₹15.37 cr/km | **109%** |
| **Pre-construction cost** | **₹8.28 cr/km** | ₹1.39 cr/km | **496%** |
| NHAI's own projection | **₹10,55,268 cr** | sanctioned ₹5,35,000 cr | **97%** |
| Excess borrowing | — | — | **₹91,070 cr** |

**Pre-construction is where the cost model is least reliable and most expensive to get
wrong** — sanctioned at 6× the approved rate. MoRTH itself named "delays in
pre-construction activities" as a cause of delay and cost overrun.

**[V]** By June 2025, **26,425 km of 34,800 km** had been awarded at **₹8.53 lakh crore**
against a programme approved at **₹5.35 lakh crore** — a **59% escalation on 76% of the
length.** → LS US Q 1975, 31 Jul 2025

**Gujarat. [V]** **33 CRIF road projects sanctioned at ₹904.54 cr, expenditure reported:
Nil.** Thirty-three projects approved, zero rupees spent. That is a pure pre-construction
failure — approval happened, ground never broke, and no contractor, designer or structure
exists to blame. **The sanctioning machinery has no name attached to it.**

→ RS US Q 1057, 4 Dec 2024 → https://sansad.in/getFile/annex/266/AU1057_d6Ggv5.pdf

**[V]** Gujarat's Bharatmala position: **1,577 km** total, **1,194 km** awarded,
**1,023 km** constructed. → LS US Q 1975

### 2.5 Land acquisition — the real gate

Two live regimes operate simultaneously. Confusing them is a common and expensive error.

**State roads. [V]** The **2013 Act** (Right to Fair Compensation and Transparency in
Land Acquisition) plus **Gujarat Act 12 of 2016** and the **Gujarat Rules 2017**. Relevant
mechanics: **s.11 declaration**, **s.43 Administrator**, **s.10A** allows SIA waiver in
specified cases.

**Legacy. [V]** The **Land Acquisition Act 1894** as amended in 1992 is **still listed in
the Gujarat Collector Manual.** Both regimes are live; a prototype that models only one
will be wrong on some real files.

**National Highways. [V]** **NH Act 1956**, **s.3A → 3C → 3D**, per e-Gazette
**S.O. 620(E), 1056(E), 3788(E)**. **s.3D(2)** vests the land *"absolutely… free from all
encumbrances."* That absoluteness is what makes the possession test below enforceable.

**[V] LAA s.11 — the entire proceeding lapses if no award is made within 2 years.** A
proceeding started and not carried through is not paused; it is destroyed, and it must be
restarted. This is a hard, non-obvious, machine-checkable expiry.

**[V] BhoomiRashi live counters:** 3,748 projects, 153,424.11 ha with 3D notification
done, ₹38,710.64 cr compensation disbursed. → https://bhumi.ras.nic.in

#### 2.5.1 The rule that was broken

**[V] The KPWD Code mandates taking land possession before inviting tenders.**

**CAG found a bridge that was built, completed, and never opened because this was not done:**

> **₹8.7 crore Karwar bridge — completed January 2022, non-operational**, because land
> was never acquired for the approach roads. CAG: *"Contrary to the KPWD Code, which
> mandates taking land possession before inviting tenders."*

**This is the single best demonstration asset in the entire research base.** It requires
zero domain knowledge to grasp: a bridge was paid for, finished, and cannot be used,
because a gate that existed on paper was not enforced. ₹8.7 crore, no service, zero users.

**[V]** The same cause, quantified: **₹17.36 crore of idle rig for 213 days** due to land
acquisition delay. → CAG Report No. 14 of 2021

#### 2.5.2 The machine-checkable form of the gate

**[V] NHAI/MoRTH Standard EPC, clause 8.2** gives the gate an exact, implementable shape:

- **90% possession test** before the Appointed Date
- **10% hard cap**
- **Handover Memorandum in 3 counterparts** — described in the contract as
  *"valid evidence of giving the Right of Way"*

**Product implication.** This is the gate to build. It is a percentage, a document count,
a date, and a named event. It can be evaluated without judgement.

> **Scope limit.** This is NHAI EPC. Gujarat R&B's equivalent is not established — see §6.

### 2.6 Clearances

**[V]** Required clearances for a Gujarat bridge project, as established: **GAD**
(railway, waterways, irrigation authorities), **ESP** (railway zonal HQ), **Land Use
Conversion Certificate**, **Forest and Wildlife Clearance**, **Environmental Clearance**.

**[V] CAG on MoEF&CC, nationally:** Terms of Reference granted on time in only **14%**, and
Environmental Clearance in only **11%**, of **216 projects**. Average delay **89%**.

**[V] Gujarat, and this is the sharpest single finding in the whole phase.**

> CAG Gujarat Report No. 1 of 2026 (Compliance Audit – Civil, period ended March 2024,
> tabled 25 Mar 2026), **para 3.11**: across **six** RF/PF road-widening projects
> (2022–23), actual area diverted was **53.16 ha** against Forest Conservation Act
> applications for only **31.73 ha** — **21.43 ha diverted without MoEF&CC prior
> permission**, including 0.0986 ha inside Purna Wildlife Sanctuary. In one case the
> Deputy Conservator of Forests **expressly instructed in January 2024 that work must not
> execute until approval was obtained**, and the work completed in June 2024 anyway.

State Government's defence rested on PCCF orders of **August 2003 and January 2012** — a
blanket 9.75 m RoW permission. CAG held those **superseded by MoEF&CC's March 2019
Guidelines**, and held that for ESZ projects PCCF (WL) issued NOCs **without forwarding
to NBWL**, violating the May 2012 GR.

→ https://cag.gov.in/webroot/uploads/download_audit_report/2026/Report-No.-01-of-2026-06a69c0ff37dc99.02587918.pdf

**Product implication.** A written instruction to stop work existed, and did not stop
work. This is the same failure shape as Gambhira (§4.5) and it is the argument for the
gate: **a recorded negative finding currently has no authority attached to it.**

### 2.7 Tendering and award — Gujarat-specific and verified

**[V]** From live Gujarat R&B tender notices:

| Item | Value |
|---|---|
| System | **nCode / `tender.nprocure.com`**, mirrored on `statetenders.gujarat.gov.in` |
| Cover structure | **Two-cover — Technical Bid and Price Bid — in SBD/B-1** |
| Form | **B-1 Percentage Rate Tender** |
| EMD | **0.1% of ECPT** |
| Tender fee | **₹18,000** |
| Invited by | **Executive Engineer (Division)** |
| **Opened by** | **Superintending Engineer (Circle)** |
| Operative contract | **GR TNC-1088-D-347-7-C** — *could not be opened* |

**[V] The approval chain is three layers deep, and this is proven, not assumed.**
**EE invites → SE of the Circle opens → Department approves.** CAG para 3.8 establishes
all three as distinct approval acts, and establishes that an error passed through **all
three uncaught**:

> **CAG Gujarat Rep. 1 of 2026, para 3.8 — cost overrun ₹2.21 crore.** DTP for ₹7.04 cr
> approved 05 Jan 2021; L1 bid ₹5.40 cr (23.31% below estimate). The Division computed
> the 120-day bid validity **from the date of opening of the Financial Bid (20 Feb 2021)**
> instead of the **Technical Bid (19 Jan 2021)** — validity stated as 20 Jun 2021 instead
> of the correct 18 May 2021. *"The R&B Circle, Mehsana, also did not take cognizance of
> the incorrect tender validity period and forwarded the same to the Department for
> approval. The Department approved the tender on 09 June 2021, before the [correct]
> validity period ended."* The L1 bidder refused; work was re-tendered and awarded
> 30 Dec 2021 at ₹6.13 cr — **₹72.53 lakh above the original L1 quote** — and completed
> at ₹6.91 cr. The Division's reply: *"This was an oversight error due to workload."*

**Product implication.** A single miscalculation passed three independent approval layers
with **zero detection**. Whatever we build, the second-person check at the SE and
Department levels did not operate. This is the empirical case for the D-008 gate, in one
paragraph, with a rupee figure attached.

### 2.8 Contractor classification

**[V]** Gujarat R&B classifies contractors under **GR RGN-6089/8/C** and **RGN-6088/23/C**.
**Special Category I (Bridges)** requires **₹300 lakh solvency** and carries an
**unlimited contract limit**; award is by a **Committee of Chief Engineers.**

**Product implication.** The solvency threshold and the unlimited limit are the *reason*
bridge work is not a routine works division decision. A prototype that treats tender
approval as a single EE action misrepresents the authority structure.

### 2.9 Design assignment

**[V]** Bridge design is assigned to **Special Circles**; the **Designs Circle** sits under
the **SE**; technical support is **GERI, Vadodara**.

### 2.10 Security and retention at award

**[V] NHAI/MoRTH:** Performance Security **5% of Contract Price within 30 days of the Letter
of Award.**

**[V] CPWD GCC 2023** (a *different* department, cited for contrast only): 5% of ECPT within
7 days of Letter of Intent, and a bid below **80% of ECPT** is treated as abnormally low.

> **Scope limit.** Gujarat R&B's terms are `NOT ESTABLISHED`. Do not model from these.

### 2.11 What Gujarat does not have

**[V]** Gujarat has **no PIB-style appraisal mechanism for ordinary R&B works.**
**PPPAC applies only to PPP projects.** There is therefore no established, mandatory
appraisal gate in the department for a normal bridge — which is a finding, not an omission
in the research.

**[V] Appraising authority for Gujarat R&B is otherwise unestablished.** Whether a bridge
DPR is examined by GERI, by the Designs Circle, by the Special Circle, or not examined at
all is **`NOT ESTABLISHED`**.

### 2.12 Phase 1 — money found in Gujarat pre-construction

**[V] CAG Gujarat Report No. 1 of 2026, all five paragraphs, complete list:**

| Para | Finding | Amount |
|---|---|---|
| 3.6 | Irregular and overpayment of Price Variation, 11 works. At Bharuch, indices C₀ for **Cement (122.5) and Steel (108.4) were interchanged** in the PV formula — instead of **recovering ₹15.57 lakh** the Division **paid ₹40.13 lakh**. Overpayment **₹55.70 lakh** by arithmetic inversion | **₹4.74 cr** |
| 3.7 | Irregular bonus: the Division **extended the completion timeline after the date of completion**, then paid a ₹2.40 cr early-completion bonus. CAG: *"on an artificial basis for eligibility of bonus"* | **₹2.40 cr** |
| 3.8 | Bid-validity cost overrun, 2 works (§2.7) | **₹2.21 cr** |
| 3.9 | Bhuj, nine W&/S&I works covering **108 horizontal curves**; estimates per **IRC:38-1988** but widening exceeded the limit at **99 of the 108 curves**, on both sides. Circle cited IRC:SP:73-2018; CAG held IRC defers to IRC:38-1988, reply *"not convincing"* | **₹1.62 cr** |
| 3.10 | Electricity not recovered from AAI Surat for private concessionaires; avoidable charges from delayed SPV commissioning | **₹83.05 lakh + ₹62.39 lakh** |

**Total Gujarat R&B money irregularity across a full audit period: ₹8.75 crore.**

**[A] Why that smallness is strategic, not a weakness.** A state department whose entire
CAG monetary exposure for a full audit period is under ₹9 crore is a department with **no
established accountability layer** in this domain. There is nothing to displace.

### 2.13 Phase 1 gaps

- `NOT ESTABLISHED` — **GR TNC-1088-D-347-7-C**, Gujarat R&B's operative contract. Tried: gujarat.gov.in fails TLS hostname validation from the research environment; rd.gujarat.gov.in does not resolve.
- `NOT ESTABLISHED` — Gujarat's land-acquisition delegation schedule.
- `NOT ESTABLISHED` — Gujarat's DPR appraisal/approval chain and its mandatory-ness.
- `NOT ESTABLISHED` — **mobilisation advance.** No primary evidence of any kind. **Do not model it.**
- `NOT ESTABLISHED` — any open unit-level Gujarat project register.

---

## §3 PHASE 2 — CONSTRUCTION

**Governing document for most of this section: NHAI/MoRTH Standard EPC (Model Document),
read in full, 328 pages.** Everything drawn from it is **[V] for NHAI/MoRTH contracts and
`NOT ESTABLISHED` for Gujarat R&B.** This limitation is stated once here and applies to
every table in this section that does not carry a Gujarat source.

### 3.1 The two obligations that start the clock

**[V] Quality Assurance Plan** — due **within 30 days of the Appointed Date**, and the
**Authority's Engineer must approve it within 21 days** (Art. 11.2(ii)).

**[V] Methodology** — to be submitted **15 days before commencement** (Art. 11.3).

**Product implication.** Both are dated, both are document-existence checks, and both are
trivially machine-verifiable. Neither requires engineering judgement to evaluate.

### 3.2 Concrete acceptance — a genuine three-way machine gate

This is the best-evidenced quality rule in the whole research base.

**[V] Sampling frequency (MoRTH Specifications, Table 1700-9):** four samples, plus **one
for each additional 50 m³**, and **"at least one sample per shift."**

**[V] Cube acceptance — both conditions must hold:**

1. the mean of **four consecutive samples** exceeds the specified strength by **3 MPa**; **and**
2. **no sample** falls below the specified strength **less 3 MPa**.

**[V] If cubes fail, cores per IS:1199 — at least three cores, average ≥ 85% of specified,
and no core below 75%.**

**[V] Water permeability per DIN:1048 Part 5, maximum 25 mm.**

**Product implication.** This is a fully computable predicate. Load the sample history,
evaluate two conditions, and the answer is a boolean with a statutory meaning. **This is
the template for every quality gate in the product.** If a rule cannot be expressed this
way, say so rather than pretending.

### 3.3 Durability — three conditions, all must hold

**[V] MoRTH Specifications Table 1700-2:**

| Exposure | Max w/c ratio | Min cement | Min grade |
|---|---|---|---|
| Moderate | 0.45 | 340 kg/m³ | M25 |
| Severe | 0.45 | 360 kg/m³ | M30 |
| Very severe | 0.40 | 380 kg/m³ | M40 |

**Product implication.** A three-way AND on exposure class, mix design and achieved
results. Again fully computable.

### 3.4 Milestones, partial credit, and liquidated damages

**[V] Milestone schedule: 35% / 60% / 85%** of Contract Price, with **preconditions** —
notably **"should have started construction of all bridges"** at Milestone-II.

**[V] Partial credit is pro-rated**, not all-or-nothing. The contract works an example in
which **10% × 0.95 = 9.5%** — a milestone 95% complete earns 95% of its value.

**[V] Liquidated damages: 0.05% per day, capped at 10%** of the relevant milestone or of
the Contract Price.

**Product implication.** Partial-credit pro-rating is the detail most contract-management
software gets wrong, and it is exactly the kind of thing an interviewer probes.

### 3.5 Tests on Completion — the strongest construction gate

**[V]** Per the **IRC Highway Research Board, Special Report No. 17:1996**, at Tests on
Completion:

- **rebound hammer** and **ultrasonic pulse velocity (UPV)** at **two random spots per span**
- **load testing if the span is ≥ 15 metres**

**[V] Insurance proof is a hard precondition** to the Completion Certificate.

**[V] The Completion Certificate is signed by the Authority's Engineer, not the contractor**
(Schedule-L). The issuing authority is the engineer's, not the builder's.

**Product implication.** "Two random spots per span" is *random selection* — a real
requirement for a system, because a self-selected sample is not a test. And the ≥ 15 m
load-test trigger is a **conditional gate keyed off a recorded span length**, which is
precisely the kind of rule a product should enforce and a spreadsheet never will.

### 3.6 The Defect Liability Period — corrected

**This section replaces an earlier claim of 12–24 months. That claim was wrong, and it was
wrong in the direction that made the product look smaller than it is.**

| Item | Value | Source |
|---|---|---|
| **DLP, stand-alone structures and major bridges** | **10 years** from the Completion Certificate | **Art. 17.1(d)** |
| **DLP deemed extended** | *"till the identified Defects under Clause 17.2 have been remedied"* | **Art. 17.5** |
| Cure period after notice | **15 days** | Art. 17 |
| DLP failure, remedy | cost of rectification **plus 20% damages**, deductible from monies due | **Art. 17.4** |

**[V] Independently corroborated by a different department, moving the same way.**
Indian Railways Railway Board letter **No. 20221 CE-II/Bridge, 29 December 2025** set a
**4-year Maintenance Period** for ROB/RUB/rail bridges. Two unrelated departments, 2025,
both settling on *multi-year* periods. **There is no evidence anywhere for a 12-month
bridge DLP.**

#### 3.6.1 Two consequences that must survive into the schema

**1. The DLP is a predicate, not a date.**

```
DLP_active = (now < start + 10 years) AND (open_defects == 0)
```

Art. 17.5 makes an open defect block expiry automatically. So the question *"do defects
quietly lapse?"* has a **contractual** answer: the clock does not run out while a defect
is open. Whether Gujarat enforces it is a separate and still unknown question — see §6.

**2. Retention does not back the DLP, and this is uncomfortable.**

| Item | Value |
|---|---|
| Retention | 6% deduction, **capped at 5% of Contract Price** |
| Alternative | omit retention, raise Performance Security **7.5% → 10%** (footnote 11 swap) |
| **Retention money refunded** | **within 15 days of the Completion Certificate** |
| Performance Security | **5%** within 30 days of the Letter of Award |

**The cash leaves a fortnight into a decade of liability.** The only security standing
behind a 10-year DLP is the performance security.

> **Say this out loud in the interview.** It is the most defensible uncomfortable finding in
> the research base: retention is commonly *assumed* to back the DLP, and it demonstrably
> does not. A model that treats retention as DLP cover is simply wrong.

### 3.7 Escalation — a weight table that will be probed

**[V] For Major Bridges, the MoRTH escalation weights are:**

| Component | Weight |
|---|---|
| Labour | **20%** |
| Cement | **Nil** |
| Steel | **Nil** |
| Bitumen | **15%** |
| Fuel / power | **10%** |
| **Other materials** | **40%** |
| Plant and machinery | **15%** |

**Cement and steel carry zero weight for bridges.** Steel is absorbed inside "Other
Materials" at 40%. This is counter-intuitive and it is exactly the kind of detail that
distinguishes research from assumption.

**[V] Escalation cut-off:** if the Statement of Price Statistics is not submitted **within
30 days** of the milestone, escalation is forfeited for that period.

### 3.8 Money, nationally — the construction-phase figures

**[V] From CAG Report No. 19 of 2023:**

| Finding | Amount |
|---|---|
| **Funds diverted from escrow accounts** (HAM / BOT) | **₹3,598.52 cr** |
| Excess price adjustment | ₹99.16 cr |
| **Liquidated damages not levied** (Dwarka Exp. Pkg III/IV; Varanasi Ring Rd Pkg-II) | **₹208 cr** |
| LD imposed but not recovered (Anakapalli 116 days; Kozhikhode 898 days; Gorhar-Khairatunda 287 days) | ₹40.86 cr |
| **Vadodara–Mumbai Expressway — 390-day delay, no penalty levied at all** | ₹0 |
| CCEA-ordered half-yearly project review | **never established** |
| Independent audit of physical & technical parameters | **never done** |

**Two of those are the strongest form of the argument we have.** A 390-day delay on a
₹4,000-crore expressway with **no penalty levied at all**, and two review mechanisms
ordered by the CCEA that were **never established** and **never done**. The one instrument
designed to cross project phases did not exist.

### 3.9 A correction: SQM and TPQM are not a bridge regime

**This corrects an error that had already been written into our research files.**

- **SQM inspected 4%. TPQM inspected 20%.** (The earlier phrasing inverted these.)
- **State Quality Monitors and Third-Party Quality Monitors are NOT a MoRTH bridge-works
  regime.** They belong to **PMGSY** (NQM/SQM) and to **World Bank PADs**.
- **The NHAI/MoRTH Standard EPC contains no TPQM or SQM clause at all** — verified across
  all 328 pages.

**[V] Gujarat context:** under the World Bank State Roads Project, **793 bridge projects of
which 473 completed (59%)**, with **SQM inspection at 4% and TPQM at 20%** against
instructions. → CAG Report No. 14 of 2021

**[V] The auditor's response is itself instructive.** For the State-Level Expert Committee,
CAG **rejected** the explanation that the loan was closed: the SLEC met **21 times to
June 2017 and then stopped for four years**, meeting gaps of **11 to 344 days**, producing
**₹48.37 cr of non-disbursal.** CAG refused to accept *"the loan was closed so we stopped
meeting."*

**Product implication.** An independent monitoring body that is not contracted to attend
does not attend. Our second-person QC gate must be **structurally incapable** of being
skipped, not merely expected. A rule that depends on someone choosing to show up is a
rule that fails at 4%.

### 3.10 Cost and time overrun — the causal finding

**[V] Odisha, World Bank State Roads Project: ₹725.44 cr → ₹963.80 cr — a ₹238.36 cr
(32.86%) overrun, with time overruns of 38 to 116 months.** Contracts were terminated and
re-tendered in 14 packages.

**[V] The root cause identified was awarding before roughly 25% of pre-construction work
was complete.**

**Product implication.** This is the direct evidentiary link between Phase 1 and Phase 2:
**the pre-construction gate protects the construction phase from overrun.** It is not a
bureaucratic preference; it has a measured rupee consequence.

### 3.11 Quality failures with consequences

**[V] Suktel bridge — completed September 2015; concrete described as "very poor and
porous"; collapsed April 2020 during dismantling; two deaths.** A structure that passed
into service and was still defective years later, and whose demolition killed people.

### 3.12 Phase 2 gaps

- `NOT ESTABLISHED` — **Gujarat R&B's own DLP duration, security % and retention %.** The operative text is GR TNC-1088-D-347-7-C.
- `NOT ESTABLISHED` — whether Gujarat R&B applies IRC:SP:57 Q-1..Q-4 or an internal equivalent.
- `NOT ESTABLISHED` — whether Gujarat R&B uses Table 1700-9 sampling and the 3 MPa / 85% acceptance rules.
- `NOT ESTABLISHED` — Gujarat's escalation weight table, if it has its own.
- `NOT ESTABLISHED` — **MoRTH e-Construction module list**, and whether Gujarat R&B uses e-construction at all. The only app found in this class is Punjab's.
- **Never opened by anyone** — CAG Gujarat **Report No. 2 of 2026** (SFAR 2024-25), tabled 25 Mar 2026.

---

## §4 PHASE 3 — POST-CONSTRUCTION

> **Completeness warning.** §4.1 to §4.8 rest on audit, judicial and parliamentary evidence
> and are strong. **The operational core of this phase is missing** — defect taxonomy,
> decision authority, service life and mandated cost recording are all `NOT ESTABLISHED`.
> **§4.9 lists exactly what is absent.** This phase is where the product's gate lives, so
> this is the largest open research item in the project.

### 4.1 The Defect Liability Period is the seam

**This is the central finding of Phase 3, and it is the product's reason for existing.**

A 10-year DLP running from the Completion Certificate (Art. 17.1(d)) creates a period in
which:

- the **contractor** remains liable for defects in a structure the **department** now owns
  and operates;
- Art. 17.5 extends the DLP automatically until every identified defect is remedied;
- Art. 17.4 makes unrectified defects cost **plus 20% damages**;
- retention has already been refunded, so the **performance security** is the only cover.

**This is a ten-year window in which two different parties are responsible for the same
physical asset through two different systems.** Phase 2 records the construction. Phase 3
records the maintenance. **The DLP is the period in which both are true at once, and it is
the only period in the lifecycle where that happens.**

**Product implication.** The DLP gate and the CRITICAL gate are **the same gate with a
different assignee.** One piece of machinery, used at both ends of the handover. That is
what makes the lifecycle claim honest without doubling the build.

### 4.2 DLP enforcement in practice — the gap

**[V]** No CAG paragraph has been found stating that retention was released while defects
remained open.

**[V] What has been found instead:** a Himachal Pradesh bridge whose defect was noticed
**only after DLP expiry**, alongside pervasive CAG coverage of DLP working.

**[A]** That is suggestive, **not proof**. The honest position is:
`NOT ESTABLISHED` whether Gujarat R&B closes DLP defects or lets them lapse.

**Why this question is still worth asking.** If defects routinely expire unclosed, the
contract contains a gate that is decorative. If they never lapse, the gate is real and the
product is enforcing a live obligation. **Either answer is useful. Neither may be assumed.**

### 4.3 The sanction asymmetry — 13 against 3

**[A] This is our own row-by-row tabulation of the annexure to Lok Sabha Unstarred
Question 3054, 18 December 2025 — MoRTH/NHAI/NHIDCL reporting collapses or major
deficiencies across 72 projects and stretches over five years, and stating that
11 officers were removed from service.** 71 of 72 rows were legible in the extracted text.

→ https://sansad.in/getFile/loksabhaquestions/annex/186/AU3054_CnAPuy.pdf

**The original published source of the 13/3 framing could not be found. It must never be
attributed to MoRTH. It is our recomputation and must always be presented as such.**

| Phase of failure | Count |
|---|---|
| **Structural collapse during construction** | **13** |
| **Structural failure of a completed or in-service structure** | **3** |

The 13 construction-phase collapses include Gurugram flyover span P10–P11 (2020);
Thalssery–Mahe, four girders (2020); Bodhwad–Muktainagar P7 girder slid post-launching
(2020); Madurai–Chettikulam, three girders collapsed during bearing fixing (2021);
Chengala–Neeleshwaram VUP (2022); Anaikarai Major Bridge, carriageway fell from
hydraulic-jack failure (2022); Panikoili–Rimuli pier cap P8 and girders during launching
(2022); Silkyara Bend Barkot tunnel cavity collapse (2023); Sangariya–Rasisar Pkg-3, nose
failure launching an 83 m single-span truss bridge (2024); ICTT–Vallarpadam pile-foundation
distress, Bridges 07 and 08 (2025); Thuravoor–Paravoor, four PSC girders (2025); Kollam
Bypass scaffolding collapse (2025); 6L Elevated Corridor Aroor–Thuravoor, two PSC girders
toppled P-202/203 (2025).

The 3 completed-structure failures: **Hero Honda Chowk flyover deck slab** (Haryana, NH-48,
2024); **Kaali Bridge, three spans collapsed in operation** (NH-66, Aug 2024); **ROB deck
slab, Jodhpur–Ajmer NH-65, Nagaur** (2024), post-completion honeycombing.

#### 4.3.1 The sanction table — where the argument lives

| | Under construction | Completed / in service |
|---|---|---|
| Contract termination / PBG forfeiture | Yes (3 cases) | 1 case |
| **Debarment ≥ 12 months** | **4 cases** | **none** |
| **Designer-team / design-consultant debarment** | **2 cases** | **none** |
| **Government officer suspended / transferred / removed** | **3 cases**, plus 11 officers removed | **none listed** |
| Monetary penalty > ₹1 crore | Yes (₹30.74 cr ×2, ₹7.305 cr) | Once (₹134.784 cr) |

**The headline contrast:**

- **#51 Sangariya–Rasisar Pkg-3** — nose failure launching an 83 m single-span truss bridge.
  **₹1 crore; fabrication team AND designer team debarred 2 years; senior bridge engineer
  debarred 2 years; ₹20 lakh on the Authority's Engineer.**
- **#19 Kaali Bridge** — three spans collapsed in operation. **Contractor debarred for
  1 month.**

**Same agency. Same year. Same instrument.**

> ### The system knows exactly who to punish for a bridge that breaks while they are
> ### building it, and has no idea who to punish for one that breaks after they have
> ### finished.

**One row deserves special note. [V] #69, Chandikhole–Bhadrak, Odisha, 2023** — "Faulty
Design" penalties were levied at **four levels simultaneously**: ₹30 lakh on the
concessionaire, ₹5 lakh on the Independent Engineer, ₹5 crore on the contractor, ₹20 lakh
on the supervision consultant, **plus a 1-year debarment of the DPR consultant.** This is
the only row in 72 where a **pre-construction actor is punished for a construction-phase
failure** — and it proves the mechanism works when someone chooses to use it.

### 4.4 Kaali Bridge — the case that replaces a bad citation

This replaces the IRC:130-2020 argument entirely, and it is stronger.

**[V] Kaali Bridge, NH-66, Goa–Karnataka border, km 93.700–283.300.** Four-laning under
BOT/DBFOT, NHDP-IV. **Collapsed in operation, August 2024. Three spans.**

**[V] NHAI's own expert committee found the cause** was *"a combination of central hinge
malfunction and loss of pre-stress in the cable wires."*

**[V] NHAI issued SCN on 19.08.2024 and suspended the Independent Engineer**
(M/s Theme Engineering Services) **for failing to conduct biannual bridge condition surveys
using MBIU, per the IRC SP 35 inspection proforma.**

**[V] The committee's finding, quoted:**

> *"gross failure on part of the Independent Engineer in raising and notifying the issues
> that led to the collapse"*

> the incident *"could have been averted if the Independent Engineer had been more
> vigilant."*

**[V] Progressive loss of pre-stress was visible as drooping of the cantilever tip at
central hinges** — a pre-event signature that the mandated biannual survey exists to record.

**[V] Consequence: contractor debarred for 1 month.**

**Judicial record:** Delhi High Court, **W.P.(C) 9069/2025**, judgment 14.11.2025
→ https://delhihighcourt.nic.in/app/showFileJudgment/58714112025CW90692025_185602.pdf

**Why this is the right argument.** It is not an appeal to a design standard. It is an
adjudicated fact: the regulator itself wrote the indictment — *gross failure*,
*could have been averted* — and then applied the lightest available sanction. **You cannot
overstate it. The regulator supplied the indictment and the sanction.**

### 4.5 Gambhira — the Gujarat anchor

**[S — Indian Express 26 Jul 2025, The Statesman 29 Jul 2025, Times of India. All
secondary. Primary documents not read.]**

**Gambhira / Mujpur bridge, Padra taluka, Vadodara, over the Mahisagar. Collapsed
9 July 2025. 22 dead.** Built **1985**. **22 of 23 spans** collapsed. Official cause:
crushing of the pedestal and articulation.

- **[S]** Four R&B engineers suspended **10 July 2025**.
- **[S]** A panchayat member had **warned in writing in 2022**. TOI reported letters since 2021 and a negative testing report effectively buried.
- **[S]** **All Gujarat bridges, including Gambhira, had been certified "fit and fine" in that year's pre-monsoon inspection.**
- **[S]** **Gujarat High Court, 16–18 July 2025** (CJI Sunita Agarwal, D.N. Rai), in the Morbi *suo motu* matter: *"If inspections were done before monsoon, why were 133 bridges closed only after the Gambhira incident?"* — **Advocate General: "Very sorry, my lord."**
- **[S]** Aftermath: 2,000+ bridges inspected; **133 closed for safety, 30 more for urgent repairs**; 21,480 potholes; ~1,500 km of roads damaged. SSNNL assessed 2,110 bridges. Of 355 bridges in 17 municipal corporations, 39 "dilapidated".
- **[S]** At least six Gujarat bridge collapses since 2021, including a **newly built** Mindhola river bridge on the Tapi (June 2023).

**[V] ₹212 crore replacement was sanctioned four days after the collapse** — the State of
Gujarat's own account.

**The convergence finding, and it is the most important sentence in this document:**

> **Gujarat's mandated inspection frequency is already at or above national best
> practice — twice yearly, pre- and post-monsoon, and IRC SP 018 itself requires annual
> baseline with twice yearly for flood-prone — and it still failed.**

> **The problem is not the absence of a process. It is the absence of the data substrate
> required to execute the process that already exists.**

#### 4.5.1 The enforcement hook

**[V] Gujarat R&B 1990 circular:** district engineers inspect bridges **twice yearly, pre-
and post-monsoon**; and — the sentence that makes the whole thing tractable:

> *"The engineer who signs the supervision report and certifies the structure as fit is
> personally held responsible in case of any mishap."*

**A named person, personally liable, already exists in the rules.** The product does not
need to invent accountability. It needs to make the record that accountability will be
measured against.

**[V] Gujarat GR, 6 March 2023** (UDD bridges, closing the Morbi gap): masonry inspected
twice a year, **May and October**; the DE prepares the report; the **EE physically
re-checks**; the **SE inspects special-type bridges**; urgent damage is reported *"with all
pertinent details and record plans."*

**Note that a second-person physical re-check is already mandated in Gujarat.** Our
second-person QC gate is a *borrowed* rule, not a novel proposal. That is a strength.

### 4.6 Morbi — the accountability chain, broken at the phase boundary

**[S — secondary reporting of primary documents not read: SIT reports, ~5,000 pp.]**

**Morbi cable-stayed footbridge, October 2022, 135–141 deaths.** Colonial-era structure,
O&M held by **Oreva Group / Ajanta Manufacturing**.

- **[S]** SIT Preliminary Report (Dec 2022): **22 of 49 wires in the failed cable were already corroded and likely already broken** before the collapse.
- **[S]** Renovation had replaced **flexible wooden planks with rigid aluminium panels** — a stiffness change on an old structure.
- **[S]** Reopened **26 Oct 2022, four days before collapse, with no load test and no structure test.** No cap on numbers allowed. No security staff or gear.
- **[S]** Contract awarded by Morbi Municipality **without general board approval.**
- **[S]** SIT final report (Oct 2023, ~5,000 pages): Oreva, MD **Jaysukh Patel**, and managers **Dinesh Dave** and **Dipak Parekh** responsible.
- **[S] Police charged only: 2 ticket-booking clerks, 2 operator managers, 2 contractors, 3 security guards.** All arrested, all enlarged on bail. **The engineers and designers who approved the renovation and the reopening were not charged.**

**Eight low-level operational staff prosecuted. Zero decision-makers.**

> The approval that happened in one phase — renovation sign-off, load certification,
> reopening — produced **zero** liability in the phase where the consequence occurred.

**[V] The loop never closed.** **MoRTH's ATR on Morbi remained unfiled.** The Gujarat High
Court directed it; the State sought time in July 2025; the matter was posted for August 2025.

**Product implication.** This is the clearest possible statement of the problem. The gate
does not fail because nobody wrote a rule. It fails because **a decision taken in one phase
carries no consequence in the next.**

### 4.7 The register thesis — the number is not known

**[A/S]** The figures below come from two different scopes and do not reconcile:

| Figure | Source |
|---|---|
| **1,441** bridges | Gujarat High Court, R&B's own figure |
| **6,768** in post-Gambhira inspection scope | **1,054 major + 5,475 minor + 239 culverts** |

**The bridge-classification statistical series runs 1980 → 2014 and then stops.**
**UDD: 461 (2023) vs 355 (2025).**

> **The number of bridges Gujarat owns is not known with confidence.**

**[V] And the register already existed once, and already failed.** The **Bar Chart Register**
— a standing Gujarat R&B record. Its failure is documented in the departmental audit trail.

**This kills "let's build a database" as a pitch.** A database is not the insight. The
insight is that *two official counts of the same department's assets differ by 4,700, and
the department cannot say which is right.*

### 4.8 The system that was supposed to solve this, ten years on

**[S — via secondary reporting; primary PIB release not read.]**

**IBMS launched 04.10.2016.** At launch, **1,15,000 structures inventorised** of an expected
1,50,000 (85,000 culverts, the rest bridges). A later release says *"more than 1,35,000
bridges."* IDDC's IBMS scope for NHAI was 1,72,545 assets.

**Gadkari, at the launch:**

> *"A lack of any data base on bridges in the country has led to a situation where we are
> neither clear about the exact number and location of [bridges] nor have we been able to
> maintain this asset in proper working condition."*

**[S] Ten years later, MoRTH is still issuing instructions to create the inventory:**

- **Circular of 25 June 2026** — re-instructs inventory and condition assessment for **all structures > 6 m on NHs** via a new mobile app and web dashboard; makes inventory and condition data **mandatory at as-built drawing submission** for pending projects; makes it **mandatory input by all DPR Consultants**; and **suspends monthly payment to the AE/IE** if they do not start within one month.
- **MoRTH Circular 1930.8** — **descoping the Bridge Health Monitoring System** from existing contracts and issuing a fresh Model RFP.
- A separate circular on **inventories and condition assessment of Reinforced Soil walls** — MoRTH is retrofitting lifecycle registries onto a *third* asset class because the first one never got built.

**The 25 June 2026 circular is the most important document for this product, and it was
issued in June 2026 — eight months ago.** It does, by circular and without naming it,
exactly what this product proposes: it makes **pre-construction design consultants**
responsible for existing-asset condition data, makes **post-construction condition data a
precondition of payment during construction**, and enforces both with a **payment sanction**.

> **MoRTH has already built the phase seam. By circular. It simply did not name it.**

**What IBMS still does not do. [V]** IBMS is a **data and prioritisation system with no
service-blocking gate.** It records condition and ranks priority; it does not prevent a
critical structure returning to service. **The gate is the product, and the gate is absent.**

### 4.9 WHAT IS MISSING FROM THIS PHASE — read this before using §4

**This is the largest open research item in the project.** Everything above is audit,
judicial and parliamentary evidence. The **operational** foundation of post-construction is
not established:

| Missing | Why it matters | Status |
|---|---|---|
| **Defect taxonomy** — the official Indian vocabulary of defects, components, condition ratings and severity scales | Without it the inspection schema has no controlled vocabulary. We would be inventing one, and a prototype nobody uses | `NOT ESTABLISHED` |
| **Decision authority** — at what level repair vs rehabilitation vs strengthening vs replacement is decided, and any published delegation schedule | The product's entire actor model depends on this. It is the difference between one role and six | `NOT ESTABLISHED` |
| **Repair vs strengthen vs replace criteria** — any codified rule, any life-cycle costing requirement, any formally documented decision record | This is the decision the product exists to record. Currently there is no known template for it anywhere in India | `NOT ESTABLISHED` |
| **Service life** — design life is 100 years (IRC:5-2015); observed life is undocumented. **No published age distribution, no "average age at failure", no design-life-vs-actual-life comparison exists** | Lifecycle costing is unsupportable without it | `NOT ESTABLISHED` — and see the warning below |
| **Mandated cost recording** — required fields per intervention, routine vs rehabilitation boundary in official terms | The C2/C3 cost ledgers depend on it | `NOT ESTABLISHED` |
| **Closure and restriction vocabulary** — official service-status terms, and whether a codified closure threshold exists or it is engineer discretion | Determines whether the CRITICAL gate is grounded or invented | `NOT ESTABLISHED` |
| **Event-triggered inspection** — is post-flood, post-event, on-complaint or pre-DPR inspection mandated anywhere | A calendar-only schedule has a known blind spot: scour appears after the flood, not on the schedule | `NOT ESTABLISHED` |
| **DLP enforcement in practice** (§4.2) | Whether the gate is live or decorative | `NOT ESTABLISHED` |

> ### ⚠ FABRICATED FIGURE — DO NOT USE
> **"CRRI: average age at failure 34.5 years" has no source and must not be used.** An
> exhaustive search found no origin for it. It appears to be fabricated or garbled. **If it
> appears in any presentation, deck or document, remove it.** A design-life-vs-actual-life
> comparison of this form most likely **does not exist** in Indian official documents at
> all — argue from observed cases (Gambhira 1985→2025, Benda Ghat 1980, colonial-era Morbi)
> instead of from an invented statistic.

**[V] What CAN be said about aging stock, from CRRI Annual Report 2023-24 (via search
results, crridom.gov.in):** Odisha PWD engaged CRRI to condition-assess **304 major and
minor bridges that are either > 30 years old or distressed**, across 31 CE Divisions.
**Benda Ghat bridge over the Yamuna, built 1980**, repeated deck-slab damage.
**Chahal and Warm bridges, > 35 years old, carriageway width only 4.30 m.**

**[V] National road stock (MoRTH Annual Report 2024-25):** NH **1,46,195 km**; SH
**1,79,535 km**; other roads **60,19,723 km**.

---

## §4A GUJARAT R&B — GROUND TRUTH

> **Method and its limits.** Search engines were unavailable; all findings come from direct
> retrieval of `rnb.gujarat.gov.in`, its GR AJAX search endpoint, `nprocure.com` and
> `rnbcontractor.com`. **Every R&B resolution on the departmental site is an image-only
> scan**; operative text was recovered by rendering at 300–450 dpi and OCR'ing. **No
> Gujarati OCR model was available**, so Gujarati-language instruments are reported as
> *letter located, operative text not reliably recoverable*. "Per the record" below means
> *recovered by OCR from the official scan* — **not verified against a certified copy.**

### 4A.1 The finding that reframes the entire project

**[V] CAG found that Gujarat R&B has no works accounting and management system, and said so explicitly.**

From the R&B chapter of **CAG Report No. 1 of 2026**, recommending the Department build an
automated PV Calculation Module with correct indices, ceilings and validation rules, in a
works accounting and management system integrated with IFMS:

> *"The WAMIS platform of Odisha may be seen as a good practice."*

**Read that carefully. The auditor is telling Gujarat R&B to build the thing we are
building, and naming another state's system as the model.** Corroborated in the same
report set: a **statutory** asset register does not exist as a database — only the Gujarat
Highways Act 1955 **s.8** obligation, which is a **paper map** in the Highway Authority
office; the 2008 monthly-monitoring `.xls` files **404**; and **₹71.07 cr of ₹71.96 cr
(98.76%) of Roads and Bridges receipts under MH 1054 were wrongly booked under MH 800
(Stock)** — a pure register-to-head accounting failure.

> **Per-asset auditability is not a feature of this product. It is the exact gap an auditor
> has already documented, in writing, for this department.**

### 4A.2 Gujarat's OWN contract terms — this corrects D-010

**This materially changes §3. Gujarat's numbers are not the NHAI numbers, and they are lower.**

**[V] Security deposit, GR TNC-10-2013-3-(BHAG-2)-C dt 20-11-2013** — *partial modification
of practice of acceptance of security deposit from construction contractor.* Recovered
table, verbatim:

| Estimated cost of work | Security deposit | BG validity | Max claim period |
|---|---|---|---|
| Up to ₹2 lakh | **2%** | 1 year | 1 year |
| ₹2 lakh – ₹5 lakh | **2%** | 1 year | 1 year |
| **₹5 lakh and above** | **3%** | **2 years** | 2 years |
| **Hydraulic / bund works** | **5%** | **5 years** | 5 years |

Penalty for breach = **the security-deposit amount then payable by the contractor**.

> **A bridge estimate is essentially always above ₹5 lakh, so 3% with a 2-year BG is the
> operative case.** Not 5%. Not 6%. **Gujarat is 3%.**

**[V] Performance bond = 3%** of total contract amount — **GR PRC-10-2020-329-C dt
01-06-2021**, title *"performance bond security deposit of 3 (three) percent."* The figure
appears in the title, the subject line and the body — three independent places.

**[V] The B-1 monetary ceiling — GR TNC-1088-D-347-(7)-C dt 11-07-2017**, recovered in full:

> *"the monetary limit of Rs. 50.00 lakhs… is hereby enhanced to **Rs. 12.00 Crore… for
> Road works, and Rs. 10.00 Crore… for Bridge and Building works.** This enhanced monetary
> limit shall be applicable to the tenders to be invited hereafter with the strict
> application of a condition that tenders… **should invariably be invited on B-1 tender form
> only.**"*

Chain: 1985 (B-1 concept) → 22-04-1988 and 05-08-1988 → 15-12-2003 (₹50 lakh) →
**11-07-2017** (current). Finance Dept concurrence 27-06-2017. Signed **N.G. Parmar, OSD
(S.P), R&B Department.**

> **B-1 vs B-2 is a function of the amount.** ₹12 cr road / ₹10 cr bridge & building. That
> is a hard, citable, computable branch in the schema.

**[V] Where the DLP lives — CIRCULAR C dt 11-12-2025**, file `RBD/OAS/e-file/16/2022/0002/Section C`:
the **Defect Liability Period sits in the Standard Bidding Document at clause 33, titled
"Identifying Defects / Defect liability period."** References a GR of 30-04-2020 and one of
19-08-2024. The Gujarati body contains બ્રિજ, so bridges are in scope. **The DLP duration is
still `NOT ESTABLISHED`** — the SBD is not published.

**[V] Free Maintenance Guarantee Period** at sub-clause **17(B)(3)**, road work only —
**GR TNC-10-2013-3-BHAG-3-C dt 13-12-2013.** Duration `NOT ESTABLISHED`.

**What this does to §3 and to D-010.** The NHAI/MoRTH substitute is now **partly obsolete**.
Gujarat's own security deposit (**3% banded**), performance bond (**3%**), B-1 ceiling
(**₹10 cr bridge**), DLP **location** (SBD cl. 33) and FMGP **location** (cl. 17(B)(3)) are
all established. **What remains `NOT ESTABLISHED` is the DLP *duration* and the retention
percentage** — those live inside the unpublished SBD/B-1 form. **The escalation weights,
milestone schedule, LD rate and Tests on Completion in §3 are still NHAI substitutes and
still must be labelled so.**

### 4A.3 The post-construction quality engine — Gujarat's own, and citable

**This substantially fills part of the §4.9 gap.**

**[V] GR PRC-10-2017-31-C dt 26-05-2017** — *"use of standard forms for quality control of
roads, bridges and buildings for inspection notes."* **28 standard forms.** The grading
scale:

| Grade | Meaning | Consequence |
|---|---|---|
| **S** | Satisfactory | none |
| **SRI** | Satisfactory but require improvement | **ATR with time-bound rectification: 2, 3, 6 or 12 months**, plus escalation and penalty |
| **U** | Unsatisfactory | ATR, escalation, and can trigger **Reconstruction** |

Plus a **Red Card** issued to the contractor.

> **The entire state machine is citable: `inspection` → `grade ∈ {S, SRI, U}` → if SRI/U,
> `ATR` with `due_date` and `rectified_on` → escalation ladder → `Reconstruction` → `Red
> Card` to contractor.** The form *names* failed OCR, but the workflow needs no legacy data
> — and manual entry is the honest shape of the gap.

**Also established:** **[V] GR PRC-10-2023-779-C / GR BKL-402023-1013-C** — blacklisting in
connection with the **Minor Bridge at Pardi** and **Parnera Vanki River, Valsad.** A real,
published, **bridge-specific** contractor-blacklisting resolution. Cite it.

**[V] Third-party NABL laboratory testing is an established requirement** —
**GR LAB-10-2025-273-C dt 16-10-2025**, with a departmental "Material Testing in Private
Lab" page. So a `test_report` entity with `nabl_lab_id` and a result grade is well-grounded.

**[V] Who is accountable for quality is citable** — **SSR-1080-55899-(10)-C dt 21-05-1980**,
"Responsibility of Engineering officers—Quality control on works." A first-class field on
the inspection entity.

### 4A.4 The price-variation engine — computable, and the department cannot do it

**This is the strongest single demo asset in the entire research base.**

**[V] Gujarat's own PV rules, clauses 59/59A** (B-2) and **60/60A** (B-1), as amended by
GR TNC-1089-4-C dt 21-10-2005:

| Rule | Value |
|---|---|
| Admissible only if | **estimated cost > ₹25 lakh AND time limit > 12 months** |
| First 12 months | **no PV at all** |
| Ceiling | **5% of estimated cost, less the value of Cement, Steel and Asphalt** |
| Escalation | **`1.1^n`** |
| GR 24-03-2022 (COVID relief) | material-only PV for works in progress as of 01-01-2021, items to 30-09-2022, 5% ceiling removed for Cement/Steel/Asphalt only |
| **EPC variant** | WPI/CPI + IOCL HSD + refinery bitumen; **Base Date = bid due date − 28 days**; claimed against the **Interim Payment Certificate** |

**[V] And the department gets it wrong.** **₹4.74 cr overpaid across 11 works in 5 R&B
divisions** (Bharuch, Godhra, Kheda-Nadiad, Palanpur, Surat). The Bharuch case: indices C₀
for **Cement (122.5) and Steel (108.4) were interchanged** — instead of *recovering* ₹15.57
lakh the Division *paid* ₹40.13 lakh. **An arithmetic inversion, ₹55.70 lakh, in one cell of
a formula.** NH Division Gandhidham paid **₹7.35 cr PV with ₹78.30 lakh excess.**

> **Build the PV engine. It is entirely computable from citable rules, and it is the exact
> computation CAG has formally recommended the department build.** No demo beat in this
> project is better matched to a documented auditor's recommendation.

### 4A.5 Two more engines that need no legacy data

**[V] Schedule-G dispute appeal SLA** — **Letter No. RBD/0098/12/2025, approved 17-01-2026
by the Chief Secretary** (Karmayogi e-signature), file `RBD/CMO/e-file/16/2024/2935/Section G2`.
The English SCHEDULE-G attachment OCR'd cleanly and gives a **three-stage appeal with day
counts**:

| Stage | to parent dept | to Legal | for Legal clearance | to file | **Total** |
|---|---|---|---|---|---|
| 1 | 7 days | 7 days | 7 days | 9 | **30 days** |
| 2 | 14 days | 14 days | 14 days | 18 | **60 days** |
| 3 | 30 days | 14 days | 14 days | 32 | **90 days** |

> A **government-approved, SLA-shaped, three-stage escalation that goes into the Legal arm**,
> with a hard outer bound. A deadline calculator needs no data at all. **Zero data risk.**

**[V] Bid capacity — `ABC = 2·A·N − B`**, with turnover `X = tender amount ÷ time limit in
years`. Directly computable. Combined with the prequalification thresholds below, it
demonstrates that the GR was read rather than invented.

### 4A.6 The prequalification regime — GR SSR/10/2015/17-C dt 20-06-2020

**[V]**, ~26 pages recovered:

| Rule | Value |
|---|---|
| **Threshold** | Road **> ₹7.50 cr** · **Bridge/Building > ₹7.0 cr** · Electrical > ₹0.5 cr |
| Joint venture | max **3 firms**; lead **≥ 51%**; others **≥ 20%**; **3-year sister-concern bar** |
| Turnover | JV lead ≥ 51% of X, others ≥ 30% of X, collectively ≥ X |
| **Similar work** | ≥ **40%** of tender amount, last **5 financial years** for roads — **last 10 financial years for bridges** |
| Bid capacity | **`ABC = 2·A·N − B`** |
| **Mandatory plant** | **15 items**, including **CBM plant min 120 TPH**, **concrete mixers with integral weight batching**, **auto batch plant min 100 cum/h**, concrete paver 7.5 m extensible to 10 m |

> **The bridge prequalification threshold (₹7.0 cr) is *lower* than the road threshold
> (₹7.50 cr), and the look-back for bridges is *ten* years against *five* for roads.** Both
> are designed distinctions, not accidents, and both are excellent interview detail.

**Evaluation committees. [V]** **Committee A** (lower band) — Concern **SE** (chair) + another
SE + Concern **EE** + **Concern Divisional Accountant**. **Committee B** (above the band) —
Concern **CE as Chairman** + another CE + Concern SE + **Financial Advisor**. Wing-specific CE
pairings are tabulated. **GR dt 17-10-2022** substitutes *"any other Chief Engineer available
in the Headquarter"* when the chair is unavailable — **the committee is bench-based**, so
`committee_member` must be a **dated association with `from_date`/`to_date`**, not a static
array.

**False information → EMD forfeited and bidder disqualified. Discovered after award →
performance security forfeited and contract terminated.** That is the risk state machine,
and it is citable.

### 4A.7 Three bridge-specific rules worth more than their length suggests

**[V] SSR-1084-28088-12-C dt 23-05-1984 — bridge specifications must be on site.** The
Standard Specifications and code of practices for bridge works must be maintained at the
site, *"because field staff are not conversant with bridge specifications"*, creating quality
risk. Copies in Division and Sub-Division offices **and at the site of major bridge works
costing more than Rs. 25.00 lakhs.**

> **Three things.** (i) **₹25 lakh is a published bridge-specific threshold.** (ii) The
> department **itself records that bridge quality is at risk because field staff lack bridge
> competence** — *that is our problem statement, in the department's own words.* (iii)
> Distribution confirms **GERI, Vadodara 390 007** is a real office with a real budget head
> **RBD-103**.

**[V] PWM-2105-MP-219-(3)-C dt 17-10-1985 — correct writing of the names of Bridges.** The
spelling of bridge names to be **finalised within 15 days**, compliance reported immediately.
Trivial on its face, and a real design requirement: the `bridge` table needs a **canonical,
human-authored, once-finalised asset name that is not auto-derived**, plus a
`naming_finalised_on` date.

**[V] TNC-1480-815-(64)-C dt 18-06-1984 — anti-fragmentation.** A composite contract shall
be awarded and **splitting of works avoided, noting that splitting had raised cost by 45%.**
Exception only where the specialised part is **50% complete** via a separate agency, with
approval. **A scope-integrity rule with a measured 45% cost-esrunation penalty.**

### 4A.8 Organisation — nine wings, not three

**[V]** The department has **nine CE&AS-level wings**, each headed by a **Chief Engineer &
Additional Secretary** — one officer holding an engineering post in Additional Secretary
capacity. That dual charge is real and is a schema question: **`person` separate from
`post`**, and CE&AS is not two people.

South Gujarat · North Gujarat (+ MD GSRDC) · Saurastra · Capital Project & Arbitration ·
National Highways · **Quality Control** · Policy & Planning · Staff Training College ·
World Bank. Plus **Expressway** and **SHDP-PIU**, revealed by the 2022 distribution list and
**absent from the CE roster** — add with an `UNKNOWN_CE` placeholder.

**Published sanctioned posts:** CE 14 · SE(Civil) 35 · EE(Civil) 167 · EE(Elec) 15 ·
DyEE(Civil) 587 · DyEE(Elec) 40 · AE(Civil) 839 · AE(Elec) 53 · AAE(Civil) 538 ·
AAE(Elec) 48 · **Class III 6,709**. Civil line 8,889; electrical 156. **≈9,045 total is our
arithmetic from the published table, not a published figure.**

**Chain:** Secretary → Special Secretary → CE&AS → SE (circle) → EE (division) → DyEE
(sub-division) → AE (section) → AAE → Class III.

**Non-technical actors that are first-class because real resolutions name them:** **Divisional
Accountant** (required member of Committee A) · **Financial Advisor** (required member of
Committee B, **appointed by the Finance Department**) · Sectional Officer · Legal Executive ·
Additional Secretary (Budget) · Chief Secretary.

> **A three-wing actor model would not survive contact with a Gujarat division.**

**Circular counters — do not collapse these two partitions:** 7 **contractor-registration**
circles (Ahmedabad City, Ahmedabad 1, Ahmedabad 2, Rajkot 1, Rajkot 2, Surat, Vadodara) and
**26 named divisions**, 28 per-division files. The 7 are evidenced as *registration*
circles because the 8,113-contractor register is partitioned by them. **Which registration
circle maps to which CE is `NOT ESTABLISHED`.** Use a `unit_kind` enum.

**Designs Circle, Gandhinagar** — **[V]** ~1,700 major bridges and 3,000 buildings designed
over **46 years**; strength 201; **MIDAS, STAADPro, STRUDWIN, AUTOCAD**. Bridge design is
assigned **both** to the Designs Circle **and** to Special Circles; **"Special Circle" is
undefined anywhere on the departmental site** — real designation, undocumented scope.

**The register trap. [V]** A contractor's **class is a dated history, not an attribute** —
**demotion to lower class** is an enforceable sanction (GR 13-02-1976). So
`contractor` / `contractor_class` must be dated. And registration requires a **solvency
certificate of a Revenue Authority** (GR RGN-6085-68218-(1)-C dt 28-01-1985) — a
cross-departmental dependency at registration time.

### 4A.9 Systems — e-procurement yes, e-construction no

**[V] The distinction that must be got right:**

| System | Status | What it is |
|---|---|---|
| **nprocure.com** | **Live** | e-**procurement**. Tender notice → bid → opening → award. Class 3 DSC, Indian Root CA. A Client Name dropdown lists all Gujarat departments, confirming R&B is a live client |
| **rnbcontractor.com** | **Live** | Contractor **registration + fees + document upload**. Separate Contractor and Department User logins. Publishes `ContractorManual.pdf` |
| **Guj-MARG** | Live but opaque | Citizen grievance portal. A **JavaScript SPA**. An intake, not a works system |
| **Karmayogi** | **Live** | e-office / file workflow. Confirmed via a departmental circular |
| **PFMS / RTGS-NEFT** | **Live** | **GR SSR-102017-57-C dt 30-04-2018 mandates e-payment to contractors** |
| **`rnbwms.guj.nic.in`** | **NXDOMAIN** | The works monitoring host. **Dead** |
| `lrd.gujarat.gov.in` | **NXDOMAIN** | Land records. No live RoR system |
| Gujarat R&B **e-construction** | **`NOT ESTABLISHED`** | **None exists** |

> **There is no works-order, contract-execution, running-account, measurement or
> contractor-payment module on nprocure. It is a procurement platform. The moment the
> contract is signed, the data leaves the system — and there is no established successor.**
>
> **That gap, between "award" and "running account", is precisely the gap this product
> occupies. And CAG has recommended the department build a works accounting system.**

**Say it plainly in the interview:** *"Gujarat R&B has e-procurement and does not have
e-construction. CAG has recommended they build it. We built the smallest defensible slice."*
That is far stronger than pretending to extend nprocure.

**[V] The monitoring chain, and it is a real 4-level hierarchy.** OSD circular
ખરચ-૧૦૨૦૦૮-૭૩૦(૨)-૫ dt 7-6-2008 imposes **three monthly formats** — Administrative Approval,
Monthly New Item Works, Monthly Continuous Item Works. **EEs send to Circle/Division by the
7th, in hard copy *and* online. CEs compile to the Additional Secretary (Budget).** And the
enforcement lever is named: **salary grants are stopped if the returns are not received.**
**All three `.xls` files now 404.**

**[V] The 120-day rule.** Tender must be accepted and the work order issued **within 120
days** of tender opening — **GPWM Clause 212-A** with **GR 10 May 2013**. Breach → re-tender.
CAG cost it: Mehsana Asjol–Karansagar **L1 ₹5.40 cr → ₹6.13 cr**; Palanpur Boys Hostel
**₹3.66 cr → ₹5.14 cr.**

**[V] A published document taxonomy nobody else will have.** The e-file paths decompose
consistently: **`dept/wing/e-file/16/<year>/<serial>/Section <X>`** — e.g.
`RBD/OAS/e-file/16/2022/0002/Section C`, `RBD/CMO/e-file/16/2024/2935/Section G2`,
`RBD/POM/e-file/16/2026/2573/Section C`, `RBD/APM/e-file/16/2026/5146`. Sections include
**C, G2, E2, Bldg-1, Bldg-2, SR, NH, HQ, PR-I/II/III**. **Model a `file_record` entity
directly on this**, with a many-to-many `file_section` join. Very few projects can point to
a real, department-published document taxonomy.

### 4A.10 The numbers — and a third official bridge count

**[V] Gujarat R&B's own Achievements and Performance page:**

| Bridge class | Count |
|---|---:|
| **Major bridges** | **1,596** |
| **Minor bridges** | **5,589** |
| Causeways / cross-drainage | 105,830 |
| **Total** | **113,015** |

Roads: NH 6,722 km · SH 15,738 · MDR 20,153 · ODR 10,052 · village 28,041 · **total 80,706 km**.
Bituminous coverage SH 98.58% · MDR 97.88% · ODR 94.11% · village 92.88%.
**17,825 of 17,843 villages pucca (99.90%).**

**[V] 8,113 registered civil contractors** as on 14-09-2026 — AA 692 · A 648 · B 581 ·
C 1,269 · D 879 · E-1 2,826 · E-2 1,219.

> ### ⚠ THE REGISTER THESIS IS NOW STRONGER, NOT WEAKER. There are **three** official counts.
>
> | Figure | Source | Bridges |
> |---|---|---|
> | **1,441** | Gujarat High Court, R&B's own figure | R&B bridges |
> | **6,768** | Post-Gambhira inspection scope | 1,054 major + 5,475 minor + 239 culverts |
> | **7,185** | **R&B's own Achievements page** | **1,596 major + 5,589 minor** |
>
> **The department publishes 1,596 major bridges. The post-collapse inspection scope used
> 1,054 major. The High Court recorded 1,441. The department cannot reconcile its own
> numbers, and it publishes the aggregate on its own website.** That is the demo.

**[V] The 24 ongoing-project pages publish exactly four fields each** — Project Name,
District, Project Cost ₹ cr, Physical Progress %. Scraped; selected bridge items: **Pedadhpur
Major Bridge ₹22.00 cr, 96.25%** · Bardoli ROB LC17/A ₹78.89 cr · Navsari ROB LC-127 ₹114.50
cr, 88% · Sisodra Tarsadi ROB LC161 ₹31.39 cr, 92% · Bilimora ROB LC-107 ₹27.50 cr, 100% ·
Kim-Sahol ROB LC158 ₹65.00 cr, 100% · pardi ROB LC90 ₹27.97 cr, 82% · Narmada near Golden
Bridge ₹401.70 cr, 100%. **No contractor, no sanction date, no work-order date, no chainage,
no fund source, no geometry. That is the ceiling of what is published — and the honest scope
of the demo seed data.**

### 4A.11 Budget taxonomy — and a design constraint

**[V] Minor heads: 051 Construction · 052 Machinery & Equipment · 053 Maintenance & Repairs ·
001/004 Direction & Administration · 799/800 Stock.** Schemes include **RBD-2(b) = Bridge**,
RBD-1, RBD-4, RBD-10/100, RBD-99, RBD-102, **RBD-103 (GERI)**, UDP-26/27/28/31.

> **There is no budget line for a pre-construction phase. A bridge's pre-construction cost is
> capitalised inside 051.** So pre-construction cost **cannot be obtained from the accounts**
> — only from the Administrative Approval and its sub-estimates. That is a real design
> constraint, and it is also the cleanest possible justification for a separate
> pre-construction stage in the product: **the department's own accounting cannot separate
> the phase ours must manage.**

**A reconciliation trap. [V]** The department's Budget page shows **₹29,709.62 lakh
(₹296.97 cr)** for 2026-27, while CAG reports **MH 5054 capital outlay of ₹16,513.22 cr**
for 2024-25 — off by roughly two orders of magnitude. The Budget page figure is an
office/sub-head-level listing, internally labelled a schematic. **Never place the two in the
same slide.**

### 4A.12 The taxonomy search — independent corroboration of D-009

**[V]** The full text of the **Gujarat SFAR 2024-25 (739 KB)**, **CAG Report No. 1 of 2026
(701 KB, entire R&B chapter)**, a CAG Annual Appropriation/Accounts General report, **CAG
G2012 chapters 2 and 3 (PWD)**, and Karnataka PWD and Roads chapters were searched.
**Zero hits** for the pre-/construction/post-construction triad or any close paraphrase.

**The mitigation, and it is better than a borrowed vocabulary:**

> **CAG's actual split** is: (i) **sanction-to-order timeliness** (the 120-day rule),
> (ii) **completion** (the ≥₹10 cr cohort), (iii) **cost control** (PV, bonus, over-widening),
> (iv) **environmental compliance**, (v) **asset/fund accounting**.

> **Adopt Gujarat's own: `Sanction & Clearance` → `Execution` → `Post-Completion`,** anchored
> to the budget's 051/053 split, and hang our three stages off it. Each element is citable, and
> the phase names then **agree with the department's own accounting vocabulary** instead of
> importing an American one. Note the only confirmed user of the exact triad is **US FHWA
> Road Safety Audit guidelines** — a different administrative tradition, and **not Indian
> precedent.**

### 4A.13 What this pass could not establish

- **B-1/B-2 clause-level percentages** — performance guarantee %, **retention %**, **DLP %**. Searched for "performance guarantee", "retention", "25 percent retention", "defect" → **zero hits**. The forms are unpublished. **GR SSR-10-2017-50-C** (the GST clause-amendment tables, the likeliest published home) **failed OCR at 300 and 450 dpi, psm 4 and 6**. **These are physically issued to every tendering contractor — ask a Gujarat contractor.** A two-page document that would close the largest gap in this section.
- **DLP and FMGP durations.** Locations established; durations not.
- **The 28 QC form names.** Count, grading and consequences established; pages 2 and 4 did not OCR.
- **Delegation of Powers — GR PDW-3079-D-2959-BHAG-1-136-C dt 17-04-2002**, extended annually. **The instrument exists and is the authority table for the approval model. The operative monetary limits did not OCR.** **Request this from the department — highest-value single document for the schema.**
- **The Gujarat Public Works Manual** — 557 pp + 735 pp annexures, Gujarati, corrupt text layer, TOC unreadable at every setting tried. **A genuine retrieval failure, not an absence.**
- **Works sanctioned per year vs completed per year.** Not published anywhere; the 2008 `.xls` files 404 and the host is NXDOMAIN.
- Circle/division/sub-division counts for most wings; the definition of a "Special Circle"; which registration circle maps to which CE.
- Any per-asset inventory, e-construction system, PMIS, PRAGATI, or land-record link.
- **A standalone R&B "Rules of Business" or "Manual of Instructions" — both NOT FOUND.** One unexplored lead: `/Pages/Contents/ACT` on the departmental site.

> **⚠ SCHEMA TRAPS — including these is a tell.** **`eMD` is MGNREGA/Shram Sudhi vocabulary;
> Gujarat R&B says EMD. `challan` is a tax instrument, not tender vocabulary — R&B receipts
> run through e-payment. Drop both.** "TRA" is ambiguous; **ATR** is real and established,
> anything else must be clarified. Measurement book, cash book, muster roll, stock register and
> works register are **standard GPWM practice, not Gujarat-published** — model them, but label
> them as such. **Never present them as "as prescribed by Gujarat R&B."**

---

## §5 Is the three-phase split the established taxonomy?

**No. And that is the most useful finding in this document.**

It was tested against every document that actually defines Indian road audit practice.

| Source | What it actually uses |
|---|---|
| **CAG *Manual of Civil Audit Procedure 2023** — Principal Director of Audit (Infrastructure), whose portfolio explicitly includes **MoRTH** | **No** pre- / construction / post-construction definition anywhere → https://cag.gov.in/uploads/media/Civil-Audit-Manual-064e844259517c8-44941627.pdf |
| **CAG Report No. 19 of 2023 (MoRTH, Bharatmala)** | Functional chapters: Conceptualisation & Planning · Fund Management · Award of Projects · Execution · Monitoring & IT. **Stops at execution.** No O&M chapter |
| **CAG Report No. 8 of 2022 (Karnataka, PWD road works)** | Planning & Policy · Cost Estimation & Sanction · Tendering · Variations/Advances · Quality Control. **Explicitly excludes maintenance and O&M from scope** |
| **CAG Report No. 5 of 2021 (Sikkim)**, **No. 11 of 2022 (Tamil Nadu)** | The only two flagship roads audits reaching maintenance — each covers *two* phases, not three. **Neither was opened or read.** |
| **MoRTH** | Uses "pre-construction activities" as a formal **cost category** (LS US Q 1975), not a lifecycle |
| **RS Standing Committee, 296th Report, 28 Jul 2021** | Recommended fixing accountability *"from the stage of drafting the project report till complete project execution"* — as a **recommendation**, not current practice |

**The audit universe, structurally, ends when the contractor is paid.**

Parliament noticed. The Committee took up *"Operation and Maintenance of National Highways
and Management of Toll Plazas"* as a **separate 367th Report on 8 February 2024** — three
years after telling MoRTH to fix accountability across the whole lifecycle.
→ https://sansad.in/getFile/rsnew/Committee_site/Committee_File/ReportFile/20/193/367_2024_2_14.pdf

### 5.1 The fragments that already exist

- CAG's functional chapters, which stop short.
- MoRTH's "pre-construction activities" cost line.
- The Standing Committee's *"from DPR drafting till complete project execution."*
- **MoRTH's circular of 25 June 2026** (§4.8), which stitches pre-construction, construction
  and post-construction together for the first time, via a payment sanction.

> ### The three-phase model is not our invention. It is the only reading under which CAG's
> ### own Bharatmala findings, MoRTH's cost-escalation categories, the Standing Committee's
> ### accountability recommendation, and MoRTH's June 2026 circular all become simultaneously
> ### coherent — and the only reading under which a completed-structure failure has an
> ### accountable owner at all.

**And it is not being established that makes it a product.** Being established would make
it a feature request. Every claim we make must argue the taxonomy's absence alongside it.

### 5.2 The taxonomy search, run a second time, independently — **[V]**

**§5 above was tested against national documents. It has now also been tested against
Gujarat's own records, and the result is the same.**

**[V]** The **full text** of the following was searched for the pre-/construction/
post-construction triad or any close paraphrase:

- **Gujarat SFAR 2024-25** (739 KB)
- **CAG Report No. 1 of 2026** — Gujarat, Compliance Audit (Civil), period ended March 2024,
  including its **entire R&B chapter** (701 KB)
- A CAG Annual Appropriation / Accounts General report
- **CAG G2012 chapters 2 and 3** (PWD)
- **Karnataka PWD and Roads chapters**

> **Zero hits. In Gujarat's own audit record, the department's own audit manual, and the
> national PWD audit guidance.**

One qualification, stated because it is a real one: **Karnataka's PWD/Roads chapter does
contain a formal "Defect Liability Period" concept**, so the *vocabulary* exists in Indian
public-works practice. **The *phase split* does not.** The only confirmed user of the exact
triad anywhere is **US FHWA Road Safety Audit guidelines** — a different administrative
tradition, and **not Indian precedent. Do not cite it as such.**

### 5.3 The mitigation — use Gujarat's own lifecycle vocabulary **[V]**

**The defensible move is not to defend the American triad. It is to adopt the vocabulary
Gujarat and CAG actually use, which our three stages then sit inside.**

**[V] CAG does not audit by lifecycle phase.** It audits by: (i) **sanction-to-order
timeliness** (the 120-day rule, GPWM cl. 212-A); (ii) **completion** (the ≥ ₹10 cr
incomplete cohort); (iii) **cost control** (price variation, EPC bonus, avoidable
over-widening); (iv) **environmental compliance** (RoW, wildlife); and (v) **asset and
fund accounting** (the MH 800 misuse).

**[V] Gujarat's own budget taxonomy already splits the lifecycle** into **051
Construction** and **053 Maintenance & Repairs** (§4A.11).

> ### The frame we will use in the room:
> > **`Sanction & Clearance` → `Execution` → `Post-Completion`**
> >
> > Anchored to the budget's own **051 / 053** minor-head split, so our stage names **agree
> > with the department's accounting vocabulary** instead of importing one. Every element
> > is citable, and the phases are then a *refinement* of an existing split rather than an
> > imported taxonomy.
>
> > This is strictly better than arguing for the triad. It is also more likely to be true.

---

## §6 THE `NOT ESTABLISHED` REGISTER

**Every gap in one place, with what was searched.** This is the honest boundary of the
project. Nothing in this list may be inferred, estimated, or filled from general practice.

### 6.1 Blocking — the product cannot be finalised without these

> **Status as at §4A.** One row is closed, one is partly closed, and the SFAR row is now
> **answered** — with the answer that strengthens the thesis rather than overturning it.

| # | Gap | Effect | Status after §4A |
|---|---|---|---|
| ~~1~~ | ~~**GR TNC-1088-D-347-7-C**~~ | ~~DLP, security %, retention % for Gujarat all unknown~~ | **PARTLY CLOSED.** The B-1 chain was recovered in full, verbatim (§4A.2). **ESTABLISHED: B-1 ceiling ₹12 cr road / ₹10 cr bridge & building**; **security deposit 3% banded** (≥ ₹5 lakh, 2-yr BG); **performance bond 3%**; **DLP lives at SBD clause 33**; **FMGP at cl. 17(B)(3)**. **STILL OPEN: the DLP *duration*, the retention %, and every B-1 clause percentage** — these live inside the unpublished SBD/B-1 form. Searched "performance guarantee", "retention", "25 percent retention", "defect" → zero hits. **GR SSR-10-2017-50-C** (the GST clause-amendment tables) failed OCR at every setting |
| 2 | **Post-construction operational core** — defect taxonomy, decision authority, service life, mandated cost recording (§4.9) | The inspection schema, the actor model and the lifecycle costing have no evidential base | **PARTLY CLOSED.** The **quality state machine is now Gujarat's own and citable**: `S / SRI / U` → ATR at 2/3/6/12 months → escalation → Reconstruction → Red Card (§4A.3). **STILL OPEN: a per-component defect taxonomy, a service life, and the repair-vs-strengthen-vs-replace authority table** |
| ~~3~~ | ~~**CAG Gujarat Rep. 2 of 2026** (SFAR 2024-25)~~ | ~~Does it contain an R&B lifecycle or O&M chapter?~~ | **ANSWERED — and §5 SURVIVES.** The full 739 KB was read. **No lifecycle chapter, no O&M chapter, and zero hits for the triad.** §5 is **corroborated, not superseded**. The report is dated **24 February 2026** — *not* "tabled 25 March 2026" as previously recorded. **Correction made.** Its real content is far more valuable: the ₹451.41 cr Grant 86 excess, the R&B 166-project incomplete cohort, the 98.76% MH 800 misbooking, and **CAG's recommendation that the department build a works accounting system** |
| 4 | **Mobilisation advance** — Gujarat or national | No primary evidence of any kind exists | **STILL OPEN.** Extensively searched; the Gujarat pass did not find it either. **Do not model it** |
| 5 | **Gujarat's delegation-of-powers monetary limits** | Who signs what at what value — the authority table for the approval model | **STILL OPEN, but the instrument is now identified.** **GR PDW-3079-D-2959-BHAG-1-136-C dt 17-04-2002**, *Delegation of Powers to Technical Officers*, extended annually. **Gujarati; operative text did not OCR. Request this from the department — highest-value single document for the schema** |
| 6 | **The 28 QC standard form names** | Which form is filled at which stage | **STILL OPEN.** Count, grading and consequences established (§4A.3); pages 2 and 4 failed OCR |
| 7 | **Gujarat Public Works Manual** — register list, measurement-book rules, form list | Whether the manualised registers are Gujarat-shaped or merely standard GPWM | **STILL OPEN. A retrieval failure, not an absence.** 557 pp + 735 pp annexures, Gujarati, corrupt text layer, TOC unreadable at 300/450 dpi, psm 4 and 6 |

### 6.2 Real but bounded — documented, and labelled

| Gap | Status |
|---|---|
| Gujarat R&B's condition taxonomy and DLP terms | Borrowed from IBMS / NHAI / IRC SP 35, **labelled as such** |
| Whether Gujarat R&B uses e-construction | **ANSWERED [V] — it does not exist.** `nprocure` is e-**procurement** only; there is **no works-order, measurement, running-account or payment module** on it, and `rnbwms.guj.nic.in` is **NXDOMAIN**. **The moment the contract is signed the data leaves the system, and there is no established successor** (§4A.9). This is no longer an absence of evidence — it is a positive finding, and it is the gap the product occupies |
| Any open unit-level Gujarat register for any asset class | **ANSWERED [V] — none exists, and the department publishes three inconsistent counts of its own bridges.** No GIS, no RoW layer, no asset IDs, no chainage register. Only static undated aggregate tables, one 2018 spreadsheet, 24 project pages with four fields each, and the Gujarat Highways Act 1955 **s.8** statutory map, which is **paper, in the Highway Authority office**. **We are defining the first per-asset register, not importing one** (§4A.10) |
| Gujarat's DLP *duration* | **Location established [V]** — SBD clause 33, *"Identifying Defects / Defect liability period"* (CIRCULAR C 11-12-2025, file `RBD/OAS/e-file/16/2022/0002/Section C`). **Duration `NOT ESTABLISHED`** — the SBD is not published. §3's 10-year figure remains an **NHAI substitute, labelled as such** |
| Gujarat R&B's condition taxonomy | **Partly resolved [V].** The **grading scale is Gujarat's own**: **S / SRI / U** with ATR at 2/3/6/12 months, escalation, Reconstruction, Red Card (GR PRC-10-2017-31-C). **The per-component defect taxonomy behind those grades remains `NOT ESTABLISHED`** |
| Gujarat Vidhan Sabha PAC / Estimates Committee reports on roads & bridges | **Not searched.** Vidhan Sabha site not visited. A real gap |
| CAG Gujarat Rep. 1 of 2026 paras 3.6–3.11 | **Read in full.** Confirmed |
| Sikkim Rep. 5 of 2021, Tamil Nadu Rep. 11 of 2022 | **Existence confirmed; neither opened.** Their chapter structure is inferred from titles only |

### 6.3 Claims STRUCK — verified as unsourceable, removed from the project

| Struck claim | Why |
|---|---|
| Gujarat **168 projects ≥ ₹10 cr** incomplete | **Wrong number, right idea.** The real CAG figure is **166 projects** (§4A / SFAR 2024-25). The claim was struck; the corrected figure is now recorded |
| Gujarat **₹5,194 cr** spent vs **₹7,353 cr** estimated | **Both figures wrong.** The real CAG figures are **₹5,740.44 cr spent against ₹7,978.85 cr estimated, 71.95% complete** |
| **"CRRI: average age at failure 34.5 years"** | **No source whatsoever. Almost certainly fabricated. Removed and permanently barred** |
| **DLP of 12–24 months** | **Wrong.** NHAI EPC Art. 17.1(d) says **10 years** for major bridges |
| **"TPQM inspected 80%, SQM 4%"** | **Inverted.** SQM inspected **4%**, TPQM **20%** |
| **TPQM/SQM as a MoRTH bridge regime** | **Wrong.** They belong to PMGSY and World Bank PADs. The NHAI/MoRTH EPC has **no such clause** in 328 pages |
| **IRC:130-2020 as authority on bridge records** | **Misattribution.** It is a roads standard that disclaims bridges in its scope clause |
| The 13-vs-3 split as a **published government statistic** | **Not found as a citation.** The numbers reproduce from our own tabulation of the LS Q 3054 annexure. **Always present as ours** |

### 6.4 Claims CORRECTED after §4A — one of them was a real number, mislabelled

> **This row is recorded because a strike is a claim too, and getting a strike wrong is as bad
> as getting a claim wrong.**

| Original claim | What happened | Correct position |
|---|---|---|
| Gujarat **₹11,146 cr** capex — struck as *"Not found in any primary or secondary source"* | **The number is REAL. The label was wrong.** It is **MH 5054 Roads & Buildings, capital outlay, 2023-24 = ₹11,146.00 cr**, from CAG SFAR 2024-25. It is **not** a department-wide "capex" figure, and it is not the 2024-25 number | **Use it as:** *MH 5054 R&B capital outlay rose from ₹11,146.00 cr (2023-24) to ₹16,513.22 cr (2024-25), **+48.15%**.* **Never as** a bare "Gujarat capex" |
| A later research pass asserted the ₹11,146 cr figure was **never real** | **Both halves of that assertion were wrong** — the earlier "not found" was a retrieval failure, and the correction was a re-identification | Recorded here so the next agent does not strike it a second time |

> **The lesson, and it generalises: `NOT ESTABLISHED` means *we did not find it*, not *it does
> not exist*.** §4A found real Gujarat instruments that two earlier passes had recorded as
> unfindable. **A gap in the register is a claim about our search, not about the world.**

---

## §7 WHAT WE CONCLUDE

> # ⛔ FENCED — everything below is our judgement, not research
> ### Nothing in this section is evidence. It is inference from §2–§6, and it is
> ### separated so that no reader can mistake it for a finding.

### 7.1 The thesis, in one line

> **India can name who to punish for a bridge that breaks while they are building it, and
> has no idea who to punish for one that breaks after they have finished.**

This is measurable (§4.3), it is adjudicable (§4.4), and it holds at state level (§4.6).

### 7.2 Why the three-phase split is the right organising principle

1. **The gap in the audit taxonomy and the gap in the sanction table are the same gap.** A three-phase view is the only structure under which a design decision, a construction defect and an operational collapse can be traced to one asset and one decision chain.
2. **It is the seam the DLP already creates** (§4.1). Ten years of contractor liability on a department-owned structure is a real, specified, contractually-extended period. We are not inventing a boundary; we are naming one that exists in every bridge contract.
3. **The regulator has conceded it twice** — the Standing Committee in 2021, and MoRTH's circular of 25 June 2026, which built the phase seam by circular and attached a payment sanction to it.
4. **Not being established is what makes it a product.**

### 7.3 What we will build, and what we will refuse to build

**The gate is the product.** A bridge graded critical cannot return to service without a
**recorded, reasoned, second-person-approved decision**. The DLP gate and the CRITICAL gate
are the same machinery with a different assignee.

> **The framing that ends the interview in our favour [V]:**
>
> **CAG Report No. 1 of 2026 found that Gujarat R&B has no works accounting and management
> system, and recommended that the department build one — integrated with IFMS, with an
> automated price-variation module, naming Odisha's WAMIS as good practice.**
>
> **We are building what the auditor told them to build. And we are building the one part
> of it — the price-variation module — that is fully computable from citable rules and
> against which CAG found ₹4.74 cr overpaid across 11 works in 5 divisions.** *(§4A.1, §4A.4)*

**Three demonstrations do the work:**

1. **The refusal** — a request to proceed; the system names exactly what is missing and who must supply it. *(§2.5: possession test, Handover Memorandum count, date.)*
2. **The register that lies** — **1,441 against 6,768 against 7,185**, where the third number is **the department's own website**. *(§4A.10.)*
3. **Karwar** — ₹8.7 crore, completed January 2022, still not open, because a gate that existed on paper was not enforced. *(§2.5.1.)* Requires zero domain knowledge.

**Two more that need no legacy data, because they are computed from rules rather than
recovered from a dead system [V]:**

4. **The price-variation engine** — clauses 59/59A, the ₹25 lakh and 12-month gates, no PV
   in the first 12 months, the 5%-less-Cement-Steel-Asphalt ceiling, `1.1^n`, the EPC
   variant with Base Date = bid due date − 28 days. **CAG's own recommendation, and CAG's own
   quantified failure.** *(§4A.4.)*
5. **The Schedule-G clock** — 30/60/90 days, three stages, escalating into the Legal arm,
   **approved by the Chief Secretary on 17-01-2026.** Needs no data at all. *(§4A.5.)*

**And the uncomfortable findings to volunteer unprompted:**

- **Retention is refunded 15 days after the Completion Certificate, so the cash leaves a
  fortnight into a decade of liability.** *(§3.6.1. Label: NHAI substitute.)*
- **The department's own budget has no line for a pre-construction phase** — it is
  capitalised inside 051 — **so the department's own accounting cannot separate the phase our
  product must manage.** *(§4A.11.)*
- **The department published bridge specifications-on-site rules in 1984 because, in its own
  words, field staff are not conversant with bridge specifications.** That is our problem
  statement, in its own words. *(§4A.7.)*

**We will not multiply rupees by days by lives into a single expected value.** C5 reports
rupees, days and traffic as **three separate columns**. No exception, ever.

**We will not present a measurement book, cash book, muster roll or stock register as
"prescribed by Gujarat R&B."** They are standard GPWM practice, and Gujarat R&B publishes no
such list. Model them, label them honestly. *(§4A.13.)*

**We will not put `eMD` or `challan` in the schema.** `eMD` is MGNREGA/Shram Sudhi
vocabulary — **Gujarat R&B says EMD** — and `challan` is a tax instrument, not tender
vocabulary. Including either is exactly the plausible-but-wrong detail a Gujarat engineer
would notice.

### 7.4 What would falsify this

> **Two of the three original falsification tests have now been run. Both were resolved in
> our favour, and neither is available to be re-argued.**

- ~~**If CAG Gujarat SFAR 2024-25 contains a lifecycle or O&M chapter, §5 is superseded.~~
  **TESTED. The full 739 KB was read. It does not.** No lifecycle chapter, no O&M chapter,
  zero hits for the triad. **§5 stands, and is now corroborated against Gujarat's own audit
  record rather than only against national documents.** A separate search of CAG Report No. 1
  of 2026's full R&B chapter, a CAG AAG report, CAG G2012 ch. 2–3 and the Karnataka PWD and
  Roads chapters also returned **zero hits**. *(§5.2)*
- ~~**If Gujarat's own contract is opened and its DLP turns out to be 12 months, §4.1
  collapses.**~~ **PARTLY TESTED. The B-1 chain was opened in full, verbatim** — and the
  answer is *not* the GR, because **the GR only ever touched the monetary ceiling.** The DLP
  lives at **SBD clause 33** and the SBD is not published. **The test is narrowed, not
  closed: it now reads — if the SBD's clause 33 sets a short DLP, the ten-year seam in §4.1
  is a national figure, not a Gujarat one, and the DLP must be labelled NHAI throughout.**
  Security deposit (**3%**, banded) and performance bond (**3%**) *are* now Gujarat's own.
  *(§4A.2)*
- **STILL OPEN:** if a Gujarat R&B delegate schedule (**GR PDW-3079-D-2959-BHAG-1-136-C**,
  identified but not readable) turns out to assign repair-vs-replace decisions to a **single
  engineer at Section level**, the multi-role actor model is wrong and §7.3's second-person
  gate has no institutional home. **§4A.8 makes this more likely, not less** — the department
  publishes a real post chain down to AAE and 6,709 Class III staff, and names a Divisional
  Accountant and a Financial Advisor as required committee members. **But it is not evidence
  of a repair-decision authority.** Unresolved.

### 7.5 Confidence, stated honestly

| Claim | Confidence |
|---|---|
| Pre-construction failure modes and the land gate | **High** — CAG primary, read in full |
| Construction contract mechanics | **Split.** **High for Gujarat's security deposit (3%), performance bond (3%), B-1 ceiling (₹10 cr bridge), 120-day rule, price-variation rules and QC/ATR state machine** — all verbatim from GRs and a circular. **Still a labelled NHAI substitute for: the escalation weights, the milestone schedule, the LD rate, Tests on Completion, the DLP duration, and the retention %** |
| The sanction asymmetry and Kaali Bridge | **High** — parliamentary annexure, recomputed; judicial record |
| The three-phase gap | **High, and now doubled** — the national audit manual was read, **and Gujarat's own SFAR, CAG Rep. 1 of 2026, a CAG AAG report, CAG G2012 ch. 2–3 and the Karnataka PWD chapters were searched in full. Zero hits in all of them** |
| **The absence of a works accounting system** | **High — and it is an auditor's finding, not ours.** CAG Report No. 1 of 2026 recommends Gujarat R&B build one integrated with IFMS, with an automated PV module, naming Odisha's WAMIS. **We are building what CAG told them to build** *(§4A.1)* |
| The register thesis | **High, and upgraded.** No longer partly secondary: **three official counts now exist** — 1,441 (High Court), 6,768 (post-Gambhira scope), **7,185 (the department's own Achievements page: 1,596 major + 5,589 minor)**. The department cannot reconcile its own numbers *(§4A.10)* |
| **The price-variation engine** | **High to build, and the case is proven.** Gujarat's own clauses 59/59A rules are recovered verbatim and fully computable; **CAG found ₹4.74 cr overpaid across 11 works in 5 divisions**, including a ₹55.70 lakh arithmetic inversion from two interchanged indices, and **formally recommended the department build the module** *(§4A.4)* |
| **Post-construction quality state machine** | **High** — `S / SRI / U` → ATR at 2/3/6/12 months → escalation → Reconstruction → Red Card is Gujarat's own, verbatim *(§4A.3)* |
| **The actor model** | **Medium.** Nine CE&AS wings, the full post chain with sanctioned counts, and the non-technical actors are all **[V]**. **The repair-decision authority is not** — the Delegation of Powers did not OCR |
| **Post-construction defect taxonomy and service life** | **NONE.** The per-component defect vocabulary and any service-life figure remain unestablished. **No Indian bridge-stock age distribution or design-life-vs-actual-life figure exists; argue from observed cases only. The CRRI "34.5 years" figure is permanently barred** |

---

## Appendix A — Sources

### Primary official documents read
- CAG *Manual of Civil Audit Procedure 2023* — https://cag.gov.in/uploads/media/Civil-Audit-Manual-064e844259517c8-44941627.pdf
- CAG Report No. 19 of 2023, MoRTH (Bharatmala) — https://cag.gov.in/webroot/uploads/download_audit_report/2023/Report-No.-19-of-203--Bharatmala-English-064d5db7bc63c20.06754442.pdf
- CAG Report No. 8 of 2022, Karnataka PWD road works — https://cag.gov.in/uploads/download_audit_report/2021/Contract-Management-ENGLISH-(Recovered-1)-06406e0f41d1e42.22736124.pdf
- **CAG Gujarat Report No. 1 of 2026** (Compliance Audit – Civil) — https://cag.gov.in/webroot/uploads/download_audit_report/2026/Report-No.-01-of-2026-06a69c0ff37dc99.02587918.pdf
- Lok Sabha US Q 3054, 18 Dec 2025 — https://sansad.in/getFile/loksabhaquestions/annex/186/AU3054_CnAPuy.pdf
- Lok Sabha US Q 1975, 31 Jul 2025 — https://sansad.in/getFile/loksabhaquestions/annex/185/AU1975_CUkQe9.pdf
- Rajya Sabha US Q 1057, 4 Dec 2024 — https://sansad.in/getFile/annex/266/AU1057_d6Ggv5.pdf
- RS Standing Committee 296th Report, 28 Jul 2021 — https://rajyasabha.nic.in/rsnew/Committee_site/Committee_File/ReportFile/20/148/296_2021_10_17.pdf
- RS Standing Committee 367th Report, 8 Feb 2024 — https://sansad.in/getFile/rsnew/Committee_site/Committee_File/ReportFile/20/193/367_2024_2_14.pdf
- Delhi High Court W.P.(C) 9069/2025, 14 Nov 2025 — https://delhihighcourt.nic.in/app/showFileJudgment/58714112025CW90692025_185602.pdf
- IRC:130-2020 (cited **only** for its scope exclusion) — https://law.resource.org/pub/in/bis/irc/irc.gov.in.005.2024.pdf
- NHAI/MoRTH Standard EPC Model Document, 328 pp — read in full
- MoRTH Specifications, Tables 1700-2 and 1700-9
- IRC:SP:54 · IRC:5-2015 · IRC:SP:57-2000 · IRC:SP 35 · IRC:SP 40 · IRC:38-1988 · IS:1199 · DIN:1048 Pt 5
- IRC Highway Research Board Special Report No. 17:1996
- Gujarat GR 1990 (twice-yearly inspection, personal responsibility) · GR 6 March 2023 (UDD) · GR RGN-6089/8/C · GR RGN-6088/23/C · **GR TNC-1088-D-347-7-C — COULD NOT BE OPENED**
- BhoomiRashi — https://bhumi.ras.nic.in
- PRS Legislative Research, Gujarat Budget Analysis 2022-23 / 2024-25 / **2026-27**
- nCode Gujarat e-tendering — `tender.nprocure.com`, `statetenders.gujarat.gov.in` (live NITs)

### Via secondary reporting — labelled in text
- Indian Express, 26 Jul 2025 · The Statesman, 29 Jul 2025 · Times of India (Gambhira, Morbi, C5, D5, D6, B1, B6, H1, H5, H6)
- CRRI Annual Report 2023-24, crridom.gov.in (C5, D4)
- MoRTH Annual Report 2024-25 (E1)
- PIB 2016 release on IBMS (A1, A3) — **primary release not read**
- MoRTH circular 25 Jun 2026 · MoRTH Circular 1930.8 (H1) — **via secondary reporting**
- Lexology / Fox Mandal, 9 Apr 2026 (H2) — law-firm commentary, secondary

### Listed but NOT opened
- CAG Report No. 5 of 2021 Sikkim · CAG Report No. 11 of 2022 Tamil Nadu
- C5 `NOT ESTABLISHED` / C6 `NOT ESTABLISHED` — Gujarat Vidhan Sabha PAC and Estimates Committee
- **Gujarat Public Works Manual** — 557 pp + 735 pp annexures, Gujarati, corrupt text layer; TOC unreadable at 300/450 dpi, psm 4 and 6. **A retrieval failure, not an absence**
- **GR PDW-3079-D-2959-BHAG-1-136-C** (Delegation of Powers, 17-04-2002) — Gujarati, operative text did not OCR
- **GR SSR-10-2017-50-C** (GST clause-amendment tables) — failed OCR at every setting
- `/Pages/Contents/ACT` on the departmental site — **the single most promising unexplored URL**

---

## Appendix B — Gujarat R&B sources recovered in §4A

> **Retrieval method, and its limit.** Direct retrieval of `rnb.gujarat.gov.in`
> and its GR AJAX search endpoint. **Every departmental resolution and circular
> is an image-only scan.** Operative text was recovered by rendering at
> **300–450 dpi and OCR'ing**. **No Gujarati OCR model was available**, so
> Gujarati-language instruments are cited as *letter located, operative text not
> reliably recoverable*. **"Per the record" means recovered by OCR from the
> official scan — not verified against a certified copy.**

### Departmental pages
- Organization Hierarchy (updated 17 Sep 2026) — https://rnb.gujarat.gov.in/Pages/Contents/Organization%20Hierarchy
- Achievements and Performance — https://rnb.gujarat.gov.in/Pages/Contents/Achievements%20and%20Performance
- Budget (head and scheme-code taxonomy) — https://rnb.gujarat.gov.in/Pages/Contents/Budget
- Contractor List (8,113 contractors; 7 registration circles, 26 divisions) — https://rnb.gujarat.gov.in/Pages/Contents/Contractor%20List
- Monitoring projects (OSD circular of 7-6-2008) — https://rnb.gujarat.gov.in/Pages/Contents/monitoringprojects
- Design (Designs Circle, Gandhinagar) — https://rnb.gujarat.gov.in/Pages/Contents/Design
- Electrical and Mechanical (incl. Drilling Division) — https://rnb.gujarat.gov.in/Pages/Contents/Electrical%20And%20Mechanical
- Quality Control · Panchayat Highways · Privatization Projects
- Ongoing projects (24 pages, 4 fields each) — https://rnb.gujarat.gov.in/Pages/Contents/Ongoingproject
- Circular (187 files) — https://rnb.gujarat.gov.in/Pages/Contents/Circular
- GR database — https://rnb.gujarat.gov.in/GovernmentResolutionsList

### Live and dead systems
- **(n)Procure** e-procurement — https://nprocure.com — **live; procurement only, no works-order/payment module**
- Contractor registration — https://rnbcontractor.com — **live**
- Guj-MARG grievances — https://margsahayak.gujarat.gov.in — live, JS SPA
- `rnbwms.guj.nic.in` · `gujnwrws.gujarat.gov.in` · `lrd.gujarat.gov.in` — **NXDOMAIN**
- `govtawasallot.gujarat.gov.in` — expired TLS; `stms.guj.nic.in` — times out

### Instruments recovered, verbatim or near-verbatim
- **GR TNC-1088-D-347-(7)-C dt 11-07-2017** — B-1 ceiling ₹12 cr road / ₹10 cr bridge & building. Chain: 1985 · 22-04-1988 · 05-08-1988 · 15-12-2003
- **GR TNC-10-2013-3-(BHAG-2)-C dt 20-11-2013** — security deposit bands, BG validity
- **GR PRC-10-2020-329-C dt 01-06-2021** — performance bond 3%
- **CIRCULAR C dt 11-12-2025**, file `RBD/OAS/e-file/16/2022/0002/Section C` — DLP at SBD clause 33
- **GR TNC-10-2013-3-BHAG-3-C dt 13-12-2013** — FMGP at cl. 17(B)(3), road work
- **GR TNC-102022-458-C** dt 29-03-2022 and 30-04-2022 — Standard Bidding Documents
- **GR SSR/10/2015/17-C dt 20-06-2020** (26 pp) — prequalification, Committee A/B, bid capacity, 15-item plant list. Amended dt 17-10-2022
- **GR PRC-10-2017-31-C dt 26-05-2017** — 28 QC forms, S/SRI/U, ATR 2/3/6/12 months, Reconstruction, Red Card
- **GR PRC-1022-944-C dt 05-08-2022** — third-party supervision consultant; delay penalty 0.1%/day cap 10%; debarment 1–3 years
- **Schedule-G**, Letter No. RBD/0098/12/2025, **approved 17-01-2026 by the Chief Secretary** — 30/60/90-day appeal SLA
- **GR TNC-1089-4-C dt 21-10-2005** — clauses 59/59A and 60/60A price variation
- **GR 24-03-2022** — COVID material-only price-variation relief
- **GR TNC-10-2015-05-C dt 28-03-2016** (+ TNC-10-2015-05-S, 2018) — Road Safety Audit before commencement of road works
- **GR TNC-1480-815-(64)-C dt 18-06-1984** — anti-fragmentation; splitting raised cost 45%
- **SSR-1084-28088-12-C dt 23-05-1984** — bridge specifications on site above ₹25 lakh
- **PWM-2105-MP-219-(3)-C dt 17-10-1985** — bridge nameplate spelling, finalise within 15 days
- **SSR-102017-57-C dt 30-04-2018** — RTGS/NEFT e-payment to contractors
- **SSR-1080-55899-(10)-C dt 21-05-1980** — engineering officers' quality-control responsibility
- **GR LAB-10-2025-273-C dt 16-10-2025** — NABL laboratory testing
- **GR PRC-10-2023-779-C / GR BKL-402023-1013-C** — bridge-specific contractor blacklisting (Pardi, Parnera Vanki)
- Contractor discipline: 04-11-1986 registration/suspension/removal/banning code · 13-02-1976 demotion to lower class · 28-01-1985 solvency certificate
- **GR RBD/POM/e-file/16/2026/2573/Section C** — OPRC and PBMC
- **GR TNC/102022/457/C dt 05-04-2022** — tender amount exclusive of GST

### CAG, Gujarat — read in full
- **CAG Report No. 1 of 2026** — Gujarat, Compliance Audit (Civil), period ended March 2024, R&B chapter. **No works accounting system exists; PV module recommended, WAMIS named.** PV overpayment ₹4.74 cr across 11 works. 120-day breach: ₹5.40→6.13 cr, ₹3.66→5.14 cr. EPC bonus ₹2.40 cr on a 93-day claim. Bhuj 99 of 108 curves, ₹1.62 cr. 53.16 Ha vs 31.73 Ha applied.
- **CAG Report No. 2 of 2026** — SFAR, Gujarat, 2024-25, **dated 24 February 2026**. MH 5054 capital outlay ₹11,146.00 cr → ₹16,513.22 cr (+48.15%). Grant 86 excess ₹451.41 cr. R&B 166 projects ≥₹10 cr, ₹7,978.85 cr estimated, ₹5,740.44 cr spent, 71.95% complete. MH 1054: ₹71.07 cr of ₹71.96 cr (98.76%) booked under MH 800. Prior-year unregularised excess ₹11,065.30 cr.
- **⚠ All plausible CAG Gujarat URLs return 404. Cite by number and title only. Never fabricate a link.**

### Also read in full for the §5.2 corroboration
- CAG G2012 chapters 2 and 3 (PWD) · CAG Annual Appropriation / Accounts General report · Karnataka PWD and Roads chapters — **zero hits for the phase triad**
