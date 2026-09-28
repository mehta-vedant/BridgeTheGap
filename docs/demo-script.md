# Bridge The Gap — Demo Script

**Length:** 3 minutes 30 seconds. **Format:** screen recording with voiceover.
**Rule:** every claim on screen is clickable. If a number appears, the screen
shows where it came from. No slides, no transitions, no music.

---

## 0:00 — The problem, in one number

**VO:**

> Gujarat's Roads and Buildings Department has **7,185 bridges** — 1,596 major
> and 5,589 minor. In 2012 the World Bank's own evaluation of Gujarat's highway
> project described the department's bridge management as *"presently in the
> form of a catalogue of bridge condition with photographs."* That was thirteen
> years ago. It is still photographs.

**On screen:** type the search, the department register, the CAG finding.

**VO (faster — this is the point of the whole video):**

> Gujarat already mandates twice-yearly inspection, already has a bar-chart
> register, and already names a Deputy Engineer *personally responsible* when
> inspections are missed. The process exists. It failed anyway. So the problem
> was never the absence of a process. **The problem is the absence of the data
> substrate required to execute the process the department already wrote.**

---

## 1:00 — One register, every bridge, nothing hidden

**Action:** sign in as Executive Engineer. The left rail loads.

**VO:**

> This is the whole register. Every bridge the department holds, grouped by
> lifecycle phase — the proposed ones, the ones being built, the ones in
> service.

> **Do not say a bridge count or a per-phase split.** A fresh database seeds
> nine bridges and the derived split is whatever the records say, not an even
> three-three-three. An even split was the old hand-labelled seed and it was
> wrong. Let the screen carry the number; a wrong one is worse than none.

**Action:** click the search box, type a district.

**VO:**

> Search and filter run **server-side**. There is no pagination here and no
> "load more." A query cannot hide an asset. That was an explicit design
> decision, and the register says so on the page.

---

## 1:30 — The phase is derived, not typed

**Action:** click a bridge that is still only proposed. Open its passport.

**VO:**

> This bridge has not been built. The header says **Sanction & Clearance**, and
> below it says *why*: there is no awarded contract, so the bridge cannot be
> under construction. That phase is not a column someone filled in. It is
> **computed from the records**. A published tender with a bid in it is still
> pre-construction — you cannot be under construction without somebody being
> bound to build you.

**Action:** scroll to the Post-Completion panel.

**VO:**

> And Post-Completion is *closed*, with a reason. Not hidden — closed, and it
> says why. An interface that silently omits a stage is indistinguishable from
> one that is broken.

---

## 2:00 — A refusal that explains itself

**Action:** as Executive Engineer, on a bridge whose land gate is unmet, click
**Publish tender**.

**VO:**

> Refused. And look at what it says: the **code**, the missing requirement, the
> remediation step, and the source — *section 2.5 of our research record, ninety
> percent possession and the handover memorandum.*

**VO:**

> That source line is why this refusal is trustworthy. Every rule in this system
> cites a section of a research record, and where the record says *"not
> established"* — where we could not find an official answer — **the system
> returns 501 rather than inventing a value.** A plausible number that nobody
> can defend is worse than no number.

**Action:** record 95% possession and the memo. Publish. Sign in as Contractor,
bid. Back as Executive Engineer — award.

**VO:**

> Now watch the award. Two sourced numbers appear that nobody typed: the
> security deposit at three percent and the performance bond at three percent.
> And the tender had to clear a **one-hundred-and-twenty-day acceptance rule**
> first — *GPWM Clause 212-A, Government Resolution 10-05-2013.* Miss that
> window and the tender must be re-invited. In Mehsana that re-tender cost five
> and a half to six crore.

**VO:**

> Three layers of approval, each one recorded: the Executive Engineer invited
> it, the Superintending Engineer of the circle opened it, the Department
> approved it. CAG found a miscalculation that passed all three layers
> uncaught. That is why each layer is a recorded step and not a status change.

**On screen:** the award response, showing the derived phase has moved to
Execution.

---

## 2:20 — Roles are enforced in the query

**Action:** sign out. Sign in as Contractor.

**VO:**

> The contractor sees a subset. Not a subset *rendered* by the frontend — the
> scope is applied in SQL, before a single row is read. The page says so:
> *"Scoped to your role."*

**Action:** open a tender that is published and open for bidding.

**VO:**

> A tender notice is public by design — nProcure publishes it. So a contractor
> can see a tender they have not yet won. And when they submit a bid, they see
> that a competing bid *exists*. They never see the competitor's price. **The
> notice is public. The tender room is not.**

---

## 2:50 — The money is computed, not accepted

**Action:** sign in as Divisional Accountant. Open the price-variation engine.
Enter a claim with the measured facts only: index components, portions, months
elapsed.

**VO:**

> The client does not send us an entitlement. It sends measured facts — the
> portion, the base index, the current index, elapsed months. The engine
> computes what is payable. Previously it accepted a calculated amount from the
> client and stored the difference, which is not an engine, it is a calculator
> run by the people who got it wrong last time.

**Action:** swap the Cement and Steel base indices and submit.

**VO:**

> It produces **nothing**. Not a smaller number — *no number*. Because this is
> the exact failure the CAG found in Bharuch: Cement at 122.5 and Steel at
> 108.4 interchanged in one cell, and a 15.57 lakh recovery became a 40.13
> lakh payment. Fifty-five lakh inverted, and the wrong answer was entirely
> plausible. **An index-base mismatch does not produce a wrong number. It
> produces a convincing one.**

---

## 3:20 — Close

**VO:**

> CAG's 2026 report found Gujarat R&B has no works accounting and management
> system at all, and recommended building one with an automated price-variation
> module. We built that module. It computes, it cites, and it refuses when the
> evidence does not support a number.

> The rest of this system is the substrate that module needs: one register,
> phases derived from records, authority enforced in the query, and a defect
> liability period that only opens for a bridge that was actually built.

**On screen:** hold on the register. Every bridge. Nothing hidden.

---

## Spoken line to end on

> *Gujarat does not need more process. It needs the data to execute the process
> it already has.*

---

# Fallbacks

If a network call fails on camera: every refusal message is rendered from the
response body, so the error handling *is* the fallback demonstration. Say
"watch what it does when it refuses" and the failure becomes the content.

If the register is slow: the search is server-side and will feel instant on
production. Do not retry on camera.

# Do not say

- **Any bridge count other than 7,185 (1,596 major + 5,589 minor).** Earlier
  figures of 1,441 and 6,768 are unsourceable and must not appear.
- **"34.5 years average bridge age."** Fabricated across all 65 IRC documents
  reviewed. Permanently barred. The sourced substitute is IRC:SP:35-2024 §1.1's
  own hedged *"about 25% of the bridge stock is in some form of distress"* —
  and if you use it, say **"about 25%"**, keeping the hedge.
- **That the system auto-closes a bridge on a condition score.** Closure is
  load-capacity-conditional (Pocket Book §10.8.3), never BHI-conditional. Never
  close on a score.
- **"This is a dashboard for existing systems."** It is not. It is the substrate
  those systems do not have.
