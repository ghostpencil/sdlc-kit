# Field report (kit 0.6.0, 5th phase of a real adoption): 8 findings — the process verifies the artifact but not the environment it runs in

**Source:** [sdlc-kit#1](https://github.com/ghostpencil/sdlc-kit/issues/1), filed
2026-08-01 — the fourth field report, and the first submitted through the issue
templates R2 added. Reproduced verbatim; the triage lives in `FEATURE_PLAN.md` §12,
which records what was verified against the kit tree at **0.8.0** rather than accepted
(the report is written against 0.6.0, and R2/G1 had since moved five of the eight
implicated files). Shipped as **R3** in `v0.9.0`.

Field report from a real adoption, produced by `/sdlc-retro` at a phase boundary. Project
details are generalized; the findings, evidence and numbers are as measured.

**Adopter profile.** A small nonprofit's internal Q&A + task web app, deployed behind an
SSO proxy. Python, stdlib-first, single-maintainer. Kit **0.6.0**, adopted on an existing
ungated codebase (so the type leg started red). This retro covers the **fifth** phase since
adoption — a three-slice security arc touching the app's live authorization path and its
LLM spend.

**Window:** 15 commits, 3 slices, 1 PR, 44 numbered owner decisions.

| Gate leg | At adoption | At this merge | Movement |
|---|---|---|---|
| lint | 0 (cleaned during adoption) | 0 | held green |
| tests | 7 | **338** | ×48 |
| CI coverage floor | 12 | **42** | +30 |
| **typecheck (red baseline)** | 175 | **171** | **−4, all of it in arc 1** |

Whole-arc review: 5 reviewers, 18 items fixed, 7 deferred, **2 reviewer CRITICALs discarded
after verification**. Mutation check: 11 guards, 10 killed by exactly their own test, 1
documented equivalent mutant.

---

## 1. Nothing in the process asks whether a control is actually live in production

**Severity: critical.** The arc described a spend cap as dormant, in three places, and
shipped it enforcing.

**Evidence.** The phase spec's risk section, the PR body, and the project index all carried
a variant of *"merging changes nothing in prod"*. That was true of one control and false of
the other: the deployment manifest commits the environment variable that the second
control's "local/dev no-op" is keyed on, so the no-op never fires in production. Confirmed
post-merge from the running container's own startup log, which printed the control's
`ENABLED` banner with its live cap values.

**Why no slice could catch it.** The test conftest neutralizes that same variable
session-wide, so the entire suite exercises the no-op path and reports green on a premise
that is false in production. **Every in-repo signal agreed with the wrong conclusion.** The
defect is only visible when the slice is composed with the committed deployment manifest
*and* with the runbook step that restarts the service — i.e. structurally invisible below
the arc level.

**The compounding half.** That control's only environment-level off switch was the variable
that also gates the entire identity/authentication layer. The rollback for a *cost* control
was an *authorization* catastrophe — and nothing in the process asks a new control "what is
your independent rollback lever?"

**Implicates:** `commands/plan-phase.md` (no step reads the deployment manifest when a phase
claims flag-gated dormancy); `commands/end-phase.md` §7 (the deploy question asks *has it
happened*, never *what does this deploy activate*).

**Proposed fix.** Two additions. In `plan-phase`: when a phase claims a control ships inert
or flag-gated, require the claim to name the variable **and quote its value from the
deployment manifest** — the claim is about production configuration, and the test
environment is not production configuration. In `end-phase` §7: extend the deploy question
from "did it deploy" to "what does this deploy turn ON, and what is the independent lever to
turn it off".

---

## 2. Planning ratifies numbered decisions before anything is measured

**Severity: high.** One ratified decision implied roughly **$10,200/month** in LLM spend for
a small nonprofit.

**Evidence.** The phase spec was committed, then corrected in the very next commit —
*"decision revised from the measured spend ceiling"* — before a line of code was written.
The app ships its whole corpus on every paid call: **288,084 input tokens**, measured with
`count_tokens`, not estimated. The approved 150/day global cap therefore implied **$341/day**.
Revised to 22/day.

Seven of 44 decisions were corrected on contact with code:

| Decision | Ratified as | Reality |
|---|---|---|
| caps | 50 / 150 per day | implied ~$10,200/mo; revised to 15 / 22 |
| schema | one row per identity, single "current route" column | **could not implement the cap decision at all** — a caller alternating routes never trips the burst limit |
| test-suite premise | "the existing suite would go red without this override" | measured **false**; override kept for a different, real reason |
| audit bound | "these rows are bounded by the caps themselves" | measured **false** one day later by a subsequent decision |

The owner's own reading at interview: *decided too early, on unmeasured ground.* The
corrections all landed at implementation because that is the first point anyone touched
reality.

**Implicates:** `commands/plan-phase.md`. The command produces numbered, approved-looking
decisions with no gate distinguishing one that rests on a measurement from one that rests on
an estimate.

**Proposed fix.** Require every decision carrying a **number** (cap, threshold, cost, size)
to be tagged `measured` or `estimated` at ratification, and require `estimated` ones to be
re-derived before the slice that implements them. This is a tag, not a new step — and all
four rows above would have been caught at planning rather than at implementation.

---

## 3. The gate has three legs; one has a stated ratchet and no mechanism

**Severity: high.** A whole gate leg has been silently inert for the entire life of the
adoption.

**Evidence.** The project's `SDLC.md`, seeded from `templates/SDLC.template.md`, says the
red-baseline typecheck count is:

> a ceiling to **drive down** through the STABILIZATION backlog, never a budget to spend.

The project index records the gate at every slice and phase close. The count reads
**`171 (ceiling held)`** at **12+ recorded gate runs across four arcs**. The single movement
ever (175 → 171) was incidental — a side effect of an unrelated data-integrity fix in arc 1.

Meanwhile `commands/end-phase.md` §7 carries an **explicit bullet** that bumps the coverage
floor from CI's printed number, with a worked rationale and a two-homes reconciliation rule.
There is no equivalent sentence anywhere for the typecheck count. One leg ratchets by
process; the other by hope.

**The reporting format hides it.** Asked why the number never moved, the owner's answer was
*"I didn't know it was static"* — because the per-slice line reads `171 (ceiling held)`, and
**"held" reads as a win**. The same number twelve times reads as sustained success rather
than as a stalled ratchet.

**Implicates:** `commands/end-phase.md` §7; `templates/SDLC.template.md` (which seeds both
the "drive down" wording and the gate-reporting format).

**Proposed fix.** Either give the type leg the mechanism the coverage leg has — an
`/end-phase` bullet that records the count and asks the owner to lower the ceiling or
explicitly ratify holding it — or change the template's wording to match reality ("hold at
N; not a target"). What should not survive is a stated ambition with no step that serves it.
Separately, render an unchanged red-baseline count as **`171 (unchanged for 4 arcs)`** rather
than `(ceiling held)`, so a stall cannot read as an achievement.

---

## 4. `/end-phase` says to apply review fix batches, and never says to verify the findings first

**Severity: medium-high.** Two of five reviewers produced CRITICAL findings whose stated
trigger was factually false.

**Evidence.** `commands/end-phase.md` §5: *"Run `pr-review-toolkit:review-pr` on the PR.
Apply fix batches, re-run the gate, push."* Nothing between "run" and "apply".

Both CRITICALs from one reviewer pinned their trigger on the hosting platform overlapping
containers during deploy — which is false for a service with a mounted persistent disk,
since such a disk cannot attach to two instances. The underlying failure modes were real by
other routes and were filed at honest severity in the backlog, but the severity and urgency
as reported were both wrong. A second reviewer illustrated a genuine type-design concern
with a worked example that does not behave as described.

Followed literally, §5 would have taken two CRITICAL-severity fixes on a false premise into a
live authorization path.

**Implicates:** `commands/end-phase.md` §5.

**Proposed fix.** One sentence: *"Verify each finding against the source before it enters a
fix batch; report findings that did not survive verification alongside those that did."* The
reporting half matters as much as the verification half — a discarded finding is evidence
about the reviewer, and silently dropping it teaches nothing.

*(Scope note: the kit does not mandate a five-reviewer panel — that was the session's
choice. The finding is the missing* verify *step, which scales badly with any panel size
above one.)*

---

## 5. The process does not distinguish agent-verified commands from owner-executed ones

**Severity: medium-high.** A documented command was broken for the owner, and verified
working by agents, for four phases.

**Evidence.** The project's `CLAUDE.md` said to run the app for acceptance review with
`python <app>.py`. In the owner's interactive shell that resolves to a **conda `(base)`
interpreter** with none of `requirements.txt` installed, and dies at import with
`ModuleNotFoundError`. Agent tool-shells do not load the conda profile, so *their* bare
`python` is the correct 3.11 and the gate passes cleanly.

It surfaced at `/end-phase` **step 3 — owner acceptance review**, the first and only step in
the entire process that requires the owner rather than an agent to run the app. Four phases
of green gates had said nothing.

**Implicates:** `commands/end-phase.md` §3; `templates/SDLC.template.md` wherever it seeds
the "run the app" instruction.

**Proposed fix.** State in the template that any command the owner will execute must be
verified **in the owner's own shell**, not an agent's, and that the two can differ. Cheap
concrete version: have `/sdlc-setup` capture `which python` / `(Get-Command python).Source`
**as the owner runs it** and record it in Environment gotchas at adoption. The generalizable
claim: *a command an agent verifies and an owner executes has two different environments, and
only the owner's is authoritative for acceptance instructions.*

---

## 6. A repeated environmental hazard has no path from "recorded" to "enforced"

**Severity: medium.** Four recordings, four recurrences, zero prevention.

**Evidence.** A line-ending hazard — an editor silently rewriting a whole file from LF to
CRLF on Windows — is documented in the project index four times, each with a sharper lesson
than the last:

| Recorded | Recurred as |
|---|---|
| "a mutation harness must write BYTES" | editor rewrote a conftest + a 2,661-line module |
| "check `git status` after an editing session" | editor rewrote two modules — and `git status` showed nothing |
| "check the bytes, not git's opinion" | editor rewrote a **`.yaml`** file (all prior cases were `.py`) |
| "check every file an editor touched, not just `.py`" | — |

Each recording is accurate and each was followed. The hazard recurred anyway, because prose
in a status document is not a control. The process's only response to a recurring
environmental hazard is to describe it again.

**Implicates:** `commands/end-slice.md` (which records gotchas); `templates/SDLC.template.md`
(the gate definition — the natural home for a repo-specific mechanical check).

**Proposed fix.** Add a rule with a threshold: **a gotcha recorded in three consecutive
slices becomes a gate step or a hook, or is explicitly ratified as unpreventable.** This
project already runs a PostToolUse hook for lint on every edited `.py`, so a line-ending
assertion would have cost minutes and prevented three recurrences. The kit-level lesson is
the escalation rule, not the specific check.

---

## 7. Slice write-ups accumulate in the status document with no archival discipline

**Severity: medium.** The single source of truth for "what do I do next" is now **2,400
lines**, with the answer buried above ~2,000 lines of closed history.

**Evidence.** `spec/PROJECT_INDEX.md` describes itself (from the template) as the *"single
source of truth for phase/slice status, the deferred backlog, and what to do next"*, and a
new session is told to read it first. `/end-slice` appends a detailed block per slice and
nothing ever moves one out. START HERE now sits above the accumulated per-slice records of
five phases, nearly all closed and merged.

The detail is genuinely valuable — this retro's entire evidence base is those blocks. The
problem is that one file is asked to be both a dashboard and an archive, and the process has
an append step with no counterpart.

**Implicates:** `commands/end-slice.md`; `templates/PROJECT_INDEX.template.md`.

**Proposed fix.** At `/end-phase`, move the closed phase's per-slice blocks into that phase's
own spec file (which already exists and is already the historical home), leaving the Phase
History row plus a paragraph. The template should mark which sections are **bounded** (START
HERE, Phase, gate baseline) and which may grow.

---

## 8. Kit friction entries have no closure path

**Severity: low-medium.** Recorded friction can sit indefinitely with nothing asking about it.

**Evidence.** The project's Kit friction log holds four entries. Three carry an explicit
`> **Status: absorbed by kit 0.5.0/0.6.0**` line. The fourth — *"`/sdlc-update` step 5
replaces `sdlc-kit/` with an `rm -rf` that fails on Windows"*, logged 2026-07-20 — carries
**no status line at all** and is still live. On the 0.5.0 → 0.6.0 update it deleted all 26
bundle files and then failed to unlink the directory (`Device or resource busy`, a held
Windows handle), leaving the tree empty but git-tracked. It was benign only because the `&&`
blocked the copy and the bundle is committed — neither is guaranteed by the procedure.

The log itself exists because of a *previous* retro's finding, and it works — it is why this
finding is available at all. What is missing is the other half: `/sdlc-retro` step 2 sweeps
the log but has no step that asks *which entries are still open, and how long have they been
open?*

**Implicates:** `commands/sdlc-retro.md` step 2 (sweeps but does not age);
`commands/sdlc-update.md` step 5 (prescribes replacement without prescribing how — every
worked example in the kit is POSIX-shaped).

**Proposed fix.** Have the step-2 sweep report unabsorbed entries **with their age**, and
carry any entry older than one phase into the new report automatically. Separately, fix
`sdlc-update` step 5 to copy-over-in-place (`cp -r $K/. sdlc-kit/`) rather than
delete-then-recreate — strictly better on POSIX too, since it never leaves a window where the
bundle does not exist.

---

## What worked well

Four practices earned their place and should be protected from a future simplification. The
owner named all four independently at interview.

- **Mutation-testing every new guard.** The only thing in this arc that converted suspicion
  into fact. All five test gaps were confirmed by *running* the mutation, not by reading
  code — and it also caught one of the session's own fixes being a no-op: deleting a
  defensive `close()` left the suite green, because CPython refcounting already closed the
  local. The comment and its test were rewritten to say so, rather than implying an
  observable leak had been repaired. **A practice that catches the practitioner is worth
  keeping.**
- **The whole-arc review.** Four arcs, four times it found what clean slice reviews
  structurally could not: a live production bug, two mutation-confirmed test gaps, nothing at
  all (a real and valuable result), and this arc's CRITICAL. Its value is precisely that it
  is the only stage that sees *composition*.
- **Recording corrections in place.** Marking superseded decisions inline, rather than
  silently overwriting them, is why a refuted claim was findable at all — it was still
  standing in the two documents the code cites *by name*. A record that keeps its own history
  is auditable; one that overwrites is not.
- **Owner acceptance review before the PR.** The only step where the owner's real
  environment is under test, and it immediately found what four phases of green gates had
  missed (finding 5).

---

## Suggested priority

| # | Change | File(s) | Effort |
|---|---|---|---|
| 1 | Dormancy claims must quote the deployment manifest; deploy question must ask what the deploy *activates* and what the independent rollback lever is | `commands/plan-phase.md`, `commands/end-phase.md` §7 | S |
| 2 | Tag numeric decisions `measured` / `estimated`; re-derive estimates before the implementing slice | `commands/plan-phase.md` | S |
| 3 | Give the type leg the mechanism the coverage leg has — or restate the ambition; report an unchanged count as *unchanged for N arcs*, not *held* | `commands/end-phase.md` §7, `templates/SDLC.template.md` | S |
| 4 | "Verify each finding against source before it enters a fix batch; report those that did not survive" | `commands/end-phase.md` §5 | XS |
| 5 | Owner-executed commands must be verified in the owner's shell; capture the interpreter at adoption | `commands/end-phase.md` §3, `templates/SDLC.template.md` | S |
| 6 | A gotcha recorded in three consecutive slices becomes a gate step or hook, or is ratified unpreventable | `templates/SDLC.template.md`, `commands/end-slice.md` | M |
| 7 | Archive closed per-slice blocks to the phase spec at `/end-phase`; mark which index sections are bounded | `commands/end-phase.md`, `templates/PROJECT_INDEX.template.md` | M |
| 8 | Age unabsorbed friction entries in the sweep; fix `sdlc-update` step 5 to copy-in-place | `commands/sdlc-retro.md` §2, `commands/sdlc-update.md` §5 | S |

---

## Cross-cutting theme

**The process is excellent at verifying the artifact and silent about verifying the
environment it will run in.**

Every finding above is one instance. The gate proves the code is correct *in the test
environment*; nothing checks the value of the flag that decides whether a control is live
(#1). Decisions are ratified against reasoning; nothing checks them against a measurement
(#2). Coverage is measured from CI's real output; the typecheck count is measured against
nothing at all, so it froze (#3). Reviewer findings are applied; nothing checks the premise
they rest on (#4). Commands are verified in an agent's shell; the owner's shell is a
different environment, and exactly one step ever exercises it (#5).

The two most consequential things this arc nearly shipped — a spend cap that enforced while
three documents called it dormant, and caps that as approved would have cost ~$10,200/month —
were both a carefully-reasoned artifact meeting an unexamined environment.

**The cheapest single change is the habit: whenever the process asks "is this correct?", also
ask "against what did you check it, and is that thing production?"**

