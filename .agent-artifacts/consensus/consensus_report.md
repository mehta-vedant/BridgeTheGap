# Stochastic Multi-Agent Consensus Report

**Problem:** Which infrastructure asset class should this hackathon build an
end-to-end lifecycle inventory for?
**Judges:** 8 independent agents, each with a different framing | **Voters:** 9 (8 + one re-run)
**Date:** 2026-09-28
**Input:** 8 parallel research agents (one per asset class), each instructed to
be adversarial toward its own class.

---

## Raw Scores

Each cell is one judge's 1-10. σ is population standard deviation.

| Class | Neutral | Risk-averse | Judges | Timeboxed | Compliance | First-principles | Contrarian | Differentiation | **Mean** | **σ** |
|---|---|---|---|---|---|---|---|---|---|---|
| **End-user devices** | 8.5 | 7 | 9 | 9 | 8 | 9 | **3** | 6 | **7.44** | 1.96 |
| **Data-center hardware** | 7.5 | 5 | 7 | 8 | 9 | 8 | 7 | 8 | **7.44** | **1.10** |
| Plant & machinery | 5.5 | 4 | 7 | 8 | 8 | 7 | 9 | 7 | 6.94 | 1.63 |
| Fleet & vehicles | 6 | 5 | 5 | 7 | 7 | 8 | 5 | 3 | 5.75 | 1.49 |
| Network & edge hardware | 6.5 | 7 | 4 | 5 | 6 | 7 | 6 | 4 | 5.69 | 1.20 |
| Cloud & virtualization | 6 | 8 | 6 | 6 | 5 | 4 | 8 | 2 | 5.63 | 2.08 |
| Facilities & buildings | 5 | 4 | 6 | 8 | 8 | 8 | 4 | 1 | 5.50 | 2.55 |
| Software / SaaS licenses | 8 | 6 | 6 | 7 | 6 | 3 | 2 | 4 | 5.25 | 1.92 |

**Top-choice votes (1 per judge):** end-user devices 4 · data-center hardware 2 ·
cloud 1 · plant 1.

---

## Consensus (7+/9)

**Two classes tie on the mean at 7.44, and that tie is the finding.**

No class won unanimously. The leader pair separated from the field by 0.5
points, and the next four classes are within 0.3 of each other — a genuine
statistical tie for third place onward.

The consensus that *does* exist is negative: **software/SaaS licenses is out.**
Every judge who scored it on the criteria the brief names gave it 6 or below,
and it took last place. It looked like the data-rich obvious answer, and it is
the one class whose most natural product (seat reclamation) is a category that
a funded competitor recently shut down.

## Divergence (the real judgment call)

**End-user devices vs data-center hardware.** Identical means, opposite
characteristics:

- End-user devices wins the **plurality of top votes (4-2)** because it
  dominates on explainability. Four separate judges independently called it the
  most legible option, and the research agent rated it highest of all eight.
- Data-center hardware wins on **robustness**: σ 1.10 versus 1.96. No judge
  scored it below 5. Its worst case is a 5; end-user devices has a 3.

The end-user devices mean depends on the relatability argument holding. The
data-center mean does not.

## Outliers

**The contrarian vote is the one that changed the analysis.** It broke from
the field hard:

- **End-user devices: 3** (everywhere else 6-9)
- **Software/SaaS: 2** — worst score it received from any judge
- **Facilities: 4**, **fleet: 5**
- But **plant & machinery: 9** (highest single score that class received) and
  **cloud: 8**

Its argument, which no other judge raised: *a laptop is not infrastructure.*
Infrastructure is the systems that run the business; a laptop is an endpoint.
The same critique applies to plant machinery, and that judge flagged the
"infrastructure" word as a category risk for manufacturing equipment.

This exposes a second axis the other judges scored on implicitly rather than
explicitly: **semantic fit to the brief's own word.**

| Class | Contrarian's "is it really infrastructure?" score |
|---|---|
| Cloud & virtualization | 8 |
| Data-center hardware | 7 |
| Network & edge hardware | 6 |
| Fleet & vehicles | 5 |
| Facilities & buildings | 4 |
| **End-user devices** | **3** |
| Software / SaaS licenses | 2 |

## Recommendation

**Data-center hardware (servers), scoped to the decommission-and-disposition
thread.**

Not because it scored higher. It scored the same. Because:

1. **It is a server.** It survives the one critique that broke the tie, and it
   is unambiguously the thing the brief's word names. End-user devices is the
   strongest product attached to the most contestable premise.
2. **No judge scored it below 5.** The downside case is "a solid 5," not a
   "3 with a semantic objection attached."
3. **The differentiation judge scored it 8 and the compliance judge scored it
   9** — the two axes most aligned with "depth of process" both put it first
   or joint-first, and neither flagged the brief-fit problem.
4. **Its process depth is documentation-shaped, which is what software is
   good at.** Dependency-gated decommission, four overlapping state machines
   (physical / logical / financial / compliance), a NIST SP 800-88 destruction
   certificate, and an inventory that disagrees with the rack. The sharpest
   finding in the entire research set: *most data-destruction audit failures
   are documentation failures, not wipe failures.* That is a records problem,
   which is the cheapest possible thing to build well.
5. **Seed data is free and deterministic** — NetBox-shaped fixtures and Redfish
   payloads. No hardware, no accounts, no approvals.

**If the team strongly resonates with a human, relatable story**, end-user
devices is a legitimate second choice and won the plurality. Take it only if
you accept the brief-fit critique and answer it deliberately.

## What would flip this

- **If the sponsor says the assets are physical/facilities**, both leaders are
  invalid and this entire vote is void. Re-run restricted to physical classes;
  facilities and plant scored 5.50 and 6.94.
- **If the team has real network-operations experience**, network hardware
  rises — its only weakness was explainability, and a network-literate demo
  cures that.
- **If judges are explicitly FinOps-flavoured**, software/SaaS is worth
  revisiting despite last place, but scoped to true-up compliance, never seat
  reclamation.

## Caveat on the whole exercise

Every score here is a judgment about a problem statement of ~25 words, made
without a single answer from the sponsor. The brief explicitly invites
questions, and the two P0 questions (asset class confirmed, and whether
integration is required) are still unanswered. This report narrows the field
to two candidates. It does not remove the need to ask.
