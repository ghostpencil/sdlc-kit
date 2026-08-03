# Field report (kit 0.9.0, 6th phase of a real adoption): 10 findings — the kit says what each step must produce, almost never what makes it done

**Source:** [sdlc-kit#2](https://github.com/ghostpencil/sdlc-kit/issues/2), filed
2026-08-02 — the fifth field report, the second submitted through the issue templates
R2 added, and the first written against the current kit release (0.9.0, so no findings
can have been fixed since). Reproduced verbatim; the triage lives in
`FEATURE_PLAN.md` §15. The owner has already ruled on batch order: the
simplification pass the report ranks first (finding 7) runs as its **own batch**,
before any R4 fix batch — per the report's own argument and R3's standing note.

Field report from a real adoption, produced by `/sdlc-retro` at a phase boundary. Project
details are generalized; the findings, evidence and numbers are as measured.

**Adopter profile.** A small nonprofit's internal Q&A + task web app, deployed behind an SSO
proxy. Python, stdlib-first, single-maintainer, Windows. Kit **0.9.0**, adopted on an existing
ungated codebase (so the type leg started red). Same adopter as the three prior reports; this
is the **fourth** report and covers the **sixth** phase since adoption — the first under BUILD,
after STABILIZATION ended.

**The arc.** 33 commits, 5 slices, 1 PR, **31 numbered owner decisions**. It replaced a
whole-corpus LLM prompt (288,084 tokens per paid call, measured) with index-driven selective
retrieval over new full-text-search tables — an architecture change, deliberately scheduled as
the arc that ends STABILIZATION rather than as an exception carved into it.

**Gate legs, re-measured for this report rather than quoted from the close-out:**

| Gate leg | At adoption | At this merge | Movement |
|---|---|---|---|
| lint | 0 (cleaned during adoption) | 0 | held green |
| tests | 7 | **474** | +136 this arc |
| CI coverage floor | 12 | **52** | +10 this arc; both homes agree |
| **typecheck (red baseline)** | 175 | **171** | unchanged for **5 arcs** |

Two 0.9.0 rules got their first real exercise and both worked. **R3.3** (the type ceiling must
be lowered, scheduled, or ratified at each phase close) produced its first mandatory answer and
the owner took outcome 2 — the next arc is a stabilization arc whose product is that number
falling, rather than a fifth ratification. **The coverage floor's two homes agreed** for the
second arc running, which is the third report's finding still holding.

Whole-arc review: 4 reviewers, 25 items fixed, 3 deferred, **3 re-graded or discarded after
verification**. Mutation check: **22 across the arc close, all killed.** Backlog yield: **26 new
entries**, every one carrying a provenance tag and a `measured`/`suspected` cause marker — the
vocabulary R2/R3 added is being applied without exception.

**Ten findings, ordered by damage caused. Three of the four worst are at the phase boundary** —
which is new for this adopter, whose previous three reports found their worst material inside
slices. That shift is itself the report's most useful signal: as the slice loop has hardened,
the unguarded surface has moved to `/end-phase`.

---

## 1. The `/end-phase` review fan-out silently reverted uncommitted work, and the fix-batch commit message then asserted it anyway

**Severity: high.** Silent destruction of work, plus a false entry in the repository's own
record of itself.

**What happened.** During the whole-arc review, a review subagent ran
`git checkout -- <module>` in the **shared** working tree while the calling session was editing
that same module. Two uncommitted fixes were reverted. Neither had a test, so nothing caught it
— and the fix-batch commit that had just been written claims both of them. The damage is not
the two lines; it is that the project's account of what shipped was wrong, and survived only
because a later session happened to re-read its own diff.

Quoted from the recovery commit, which is the primary evidence:

> **TWO FIXES HAD BEEN SILENTLY LOST.** The reviewer ran `git checkout -- <module>` in the main
> working tree while I was editing it, which reverted [two fixes] before they were committed.
> Neither had a test, so nothing caught it and [the fix-batch commit]'s message claims both.

**Why the kit does not prevent it.** The kit owns read-only discipline and applies it
consistently — to the wrong agents. `agents/sdlc-surveyor.md` (*"You are a read-only
surveyor"*), `commands/plan-phase.md` (sweeps as *"parallel read-only subagent"*),
`commands/sdlc-retro.md` §2 (*"read-only sweeps … none of them writes anything"*). All three are
**collection** agents. The **review** fan-out — `pr-review-toolkit:review-pr` at
`commands/end-phase.md` §5, and the reviewer at `commands/end-slice.md` §3 — is the one that
runs concurrently with an editing session, and it carries no such statement. `end-phase.md` §1
does check *"working tree clean, branch pushed"*, but at §1, before the review, and it is never
re-asserted at §5 where it is load-bearing.

**Kit file(s) implicated.** `commands/end-phase.md` §5; `commands/end-slice.md` §3.

**Suggested fix.** The cheaper of the two available (the owner's choice over worktree
isolation): make a clean tree with every fix committed a **precondition** of spawning any review
fan-out, so there is nothing uncommitted to lose. Plus the corollary, which is the half that
generalizes furthest: **a fix with no test is a fix that can silently leave, so a commit message
must not claim one.**

---

## 2. Nothing requires the composed system to run for real before the PR — and the acceptance halt goes vacuous on exactly the arcs where that matters most

**Severity: high.** The arc's most consequential product defect was found by a step the owner
invented, three commits before the PR opened.

**What happened.** Four of the arc's five slices were behavior-neutral by construction (new code
behind a default-off flag), so **no slice's exit criteria ever required a running application**.
The phase spec, corrected at the owner's request at the last slice's close-out, states the
result plainly:

> S1–S4 were behavior-neutral by construction, so no slice's exit criteria ever required a
> running server; the checklist below was then written entirely for the activation moment, in
> prod. The result is that **the production retriever has never opened the real index**, and the
> composed system has never run outside pytest.

The local pass added to fill that gap immediately found the arc's worst defect: **the escalation
gate is a question-length detector.** Its score threshold had been fitted to an evaluation set
whose shortest question is 15 words; **8 of 10 five-word questions of the form the owner
actually asks escalate**, and one such question retrieved five chunks all containing the exact
answer and discarded all five. It forced an amendment to a ratified owner decision before the PR
could open. **474 hermetic tests were green throughout**, and could not have been otherwise —
the defect is in the composition, not in any unit.

**Why the acceptance halt does not cover it.** `templates/SDLC.template.md` and
`commands/end-phase.md` §3 define the owner acceptance review as exercising *"the phase's
visible behavior."* A flag-gated arc has none by design — this one's container came up with its
new subsystem reporting `OFF`, exactly as specified — so **the halt passes vacuously, and the
process is at its most confident precisely where it has observed least.** This is adjacent to
but distinct from R3.1's inertness rule: R3.1 asks whether a control is *live*; this asks
whether anything has ever *run*.

Worth noting because it argues against treating this as a one-off: **the adopter already had the
practice and lost it.** The previous arc ran a local pass before its production half, and the
phase spec records that this is *"the reason that arc's inertness claims were trustworthy."* An
unwritten practice does not survive the first arc that does not obviously need it.

**Kit file(s) implicated.** `commands/end-phase.md` §3; `templates/SDLC.template.md`
(acceptance-review halt); `commands/plan-phase.md` step 2 (testability sweep, where the
condition is detectable at planning time).

**Suggested fix.** Trigger on the condition rather than on every arc: **when no slice's exit
criteria required running the application, `/end-phase` adds a local pass in which the composed
system runs against real data before the PR opens.** An arc whose slices are all
"behavior-neutral by construction" is announcing the condition in its own spec, so the
testability sweep can flag it at planning time rather than the owner noticing at the end.

---

## 3. The whole-arc review has no completion condition, so the fix batch closes before the reviewers do

**Severity: high.** The arc's worst test gap arrived *after* the arc was believed closed, and the
batch applied in the interim shipped its own regression.

**What happened.** The order of the arc's last three commits:

| Commit | What it was |
|---|---|
| 1 | *"whole-arc review — verified findings from four reviewers"* — the fix batch, committed |
| 2 | a follow-on fix — **which introduced a regression** |
| 3 | *"close 9 surviving mutations; restore two lost fixes"* |

From the third commit's message:

> The 4th arc reviewer (test coverage) returned **after the others** and found what they could
> not: [the two new modules] sit at **100% LINE coverage** with no behavioral net under large
> parts of it. It ran 9 mutations against a clean worktree; **all 9 survived.**

Among them, in its own words, **the worst gap**: a preamble constant carrying the arc's single
completeness guarantee — the one property the whole design trades retrieval recall against —
**could be deleted with the suite green**, because every existing test asserted against the
instruction *string* and never against the assembled prompt. So could three other section
headings the instructions explicitly promise. The same commit also closes a regression it had
itself introduced two commits earlier.

**Why the kit does not prevent it.** `commands/end-phase.md` §5 says to run the review, verify
findings, *"then apply, re-run the gate, push."* It says nothing about **when the review is
done.** With a fan-out, "done" is whenever the last reviewer returns, and nothing holds the batch
until then. 0.9.0's R3.4 (*verify each finding before it enters a fix batch*) worked well here —
3 of 31 findings were re-graded or discarded — but it governs **quality of intake**, not
**sequencing**.

**Kit file(s) implicated.** `commands/end-phase.md` §5.

**Suggested fix.** One clause: the fix batch is assembled only after **every** reviewer has
returned, and goes through the gate as one unit. A finding arriving after the batch is committed
re-opens the review rather than starting a second batch. The failure shape here — fix, then fix
the fix, then fix both plus restore lost work — is what a batch assembled too early looks like.

---

## 4. No review lens reaches shared mutable state under the runtime's concurrency model

**Severity: medium-high.** A CRITICAL with a *measured* consequence that both inline lenses and
both lenses in `reference/REVIEW_LENSES.md` structurally cannot see.

**What happened.** A slice review found that a per-request retrieval object held **one** database
connection, and its selection method ran four queries on it with no lock, under the stdlib
threading HTTP server. Reproduced against the real index: **410 of 600 concurrent selects
returned the wrong question's passages**, and 26 raised a `ValueError` from column values
crossing between queries — which is not the database's own error type, so it escaped a narrow
`except` and left the POST handler with no response written at all. **Two browser tabs is
enough.**

This finding is submitted at the kit maintainer's own request. The kit's `FEATURE_PLAN.md` §14
diagnosed the gap and deliberately deferred writing the lens to this retro:

> [The] CRITICAL is not reachable by either inline lens or either lens in
> `reference/REVIEW_LENSES.md` (error propagation; verify the denominator). A per-request object
> holding a single connection under a threading server is neither a changed consumer nor a
> simplified double — it is **shared mutable state under the runtime's concurrency model**, with
> a measured consequence (410/600) rather than an asserted severity.

**Kit file(s) implicated.** `reference/REVIEW_LENSES.md`.

**Suggested fix.** Add the lens, with 410/600 as its specimen: *for every object that outlives a
request or is reachable from more than one, name the runtime's concurrency model and state what
serializes access.* The measurement is the point — §14 itself contrasts it with "asserted
severity", and this adopter has now twice had reviewers assert CRITICAL on premises that turned
out to be false.

---

## 5. The planning sweeps wrote an unsatisfiable exit criterion twice in one arc

**Severity: medium.** Caught both times at scope confirmation; cost a corrected spec and a
re-scope each time.

**What happened.** Two consecutive slices carried an exit criterion phrased *"coverage floor
raised from CI's printed number"* / *"a floor enforced in the CI workflow."* Both are
unsatisfiable **by construction**, for two independent reasons the project had already written
down elsewhere: CI cannot see the archive or the index (both git-ignored, as the CI workflow's
own header states), and the workflow triggers only on push/PR to the main branch, so **CI never
runs on an arc branch at all**. The convention that makes this so had been recorded during the
*previous* arc — and the same planning session wrote both criteria anyway.

**Why the kit does not catch it.** `commands/plan-phase.md` step 2 runs a **contradiction
sweep** over the phase's decisions. Nothing sweeps the **exit criteria** against what the
project's own CI configuration can actually observe on an arc branch. These are different
objects: a criterion can be internally consistent with every decision in the spec and still be
unobservable at the moment it is claimed.

**Kit file(s) implicated.** `commands/plan-phase.md` step 2.

**Suggested fix.** One line in the sweep list: each slice's exit criteria must name **what
observes it and when** — a local command, the gate, CI on the main branch, or the owner — and a
criterion naming an observer that does not run at that point is a planning defect, not a slice
problem. Note the exposure is kit-shipped: *"raise the coverage floor"* is the kit's own
ratchet, and every adopter whose CI runs only on the main branch inherits this trap.

---

## 6. The friction log has a reader, an aging rule, and no writer

**Severity: medium, structural.** The retro's own evidence base has been empty for three arcs.

**What happened.** The adopter's Kit friction log holds **four entries, all dated within two days
of adoption, all now carrying status lines** (absorbed by 0.5.0 ×2, 0.6.0, and
0.7.0-with-a-correction). **Zero entries have been added since** — across three arcs — while the
retros over those same arcs produced **23 findings**. Friction is plainly occurring; it is not
reaching the log.

The kit has built steadily on the **reading** side: `commands/sdlc-retro.md` step 2 sweeps the log
first (0.5.0/0.6.0), `templates/PROJECT_INDEX.template.md` seeds the section (0.6.0), and R3.8
(0.9.0) added **aging** — *"the sweep reports unabsorbed entries with their age, and any entry
older than one phase is carried into the new report automatically."* All of that reads a log
nothing writes to. **R3.8 shipped an aging rule with nothing to age.**

The log's own charter states the gap without noticing it is still open: *"Findings about the
process … recorded **when they happened** rather than reconstructed at the phase boundary."*
Three arcs of reconstruction later, that is aspiration, not practice. Asked directly at the
interview, the owner's diagnosis was one sentence: **nothing prompts it at the moment friction
occurs.** No command names the log except `/sdlc-retro`, which is by definition too late.

One specific shape worth flagging, because it made this arc look healthier than it was: this
window's friction *was* recorded — into a project-local trial log that existed only because a
trial happened to be running, and which is now closed. The next arc has no parallel instrument
and no prompt.

**Kit file(s) implicated.** `commands/end-slice.md` (no step writes friction);
`commands/sdlc-retro.md` §2; `templates/SDLC.template.md`.

**Suggested fix.** One bullet in `commands/end-slice.md`'s close-out, beside the existing gotcha
and gate-dependency bullets: was anything in this slice friction with *the process* rather than
with the code, and if so write it to the log. Slice close is the last moment the evidence is
still accurate, and it is already a bookkeeping step.

---

## 7. Five rule batches, no simplification pass — and the kit is the one saying so

**Severity: medium, cumulative.** Ranked **first for action** by the owner at the interview,
regardless of where damage-ordering places it.

**What happened.** `FEATURE_PLAN.md` §12's standing note, written by the maintainer and quoted in
§14 when it declined to write the concurrency lens of finding 4:

> R3's standing note (§12) records that R3 was the **fourth consecutive batch of process rules
> added on field evidence with no simplification pass between them.** Writing a fifth batch's
> worth the moment that note was made is precisely what it warns against.

**This report is that fifth batch's worth, and the note now applies to it.** It is submitted with
that stated.

The evidence that the weight is now landing on the adopter, rather than being a maintainer's
abstract worry, is two concrete deletions the owner named unprompted at the interview — both of
them **ceremony the kit's own rules produced**:

- **Per-slice detail in `PROJECT_INDEX.md`** — finding 9 below.
- **A triplicated acceptance checklist.** The phase spec carries a local pre-PR pass *and* an
  8-step production checklist, and the production steps also live in a separate activation
  runbook that is what the index actually points at. Three homes for one checklist, none of which
  says which is authoritative.

**Kit file(s) implicated.** `FEATURE_PLAN.md` §12 (the kit's own release process);
`commands/*.md`; `templates/*.md`.

**Suggested fix.** Before shipping the batch this report implies, run a pass over the commands
and templates asking of each rule added since 0.5.0: *what did this catch, in which adopter, and
when?* A rule with no confirmed catch after two releases is a candidate for deletion. The data
exists — four field reports and this one. Against that, this arc gives unusually clean evidence
that four rules **did** earn their keep (see *What worked well*), so the pass is a pruning, not a
retreat.

⚠️ This is the one finding here an adopter cannot act on. It goes upstream or nowhere.

---

## 8. A trial with four safety criteria and no value criterion cannot fail on value

**Severity: medium.** Three slices of observation overhead produced a disposition that did not
turn on what the change was for.

**What happened.** F3 — the slice-runner — was trialled on this arc as a project-local command,
across three slices, and closed undelivered. Its four pass criteria measure **safety**: no state
loss across a respawn, halt-3 fidelity, gate results surviving the agent boundary, and *"would
the owner choose it again."* From the trial log's own conclusion:

> **"Saved no time" is an observation, and it was never in dispute.** … What is missing is
> upstream of the trial: **nothing anywhere states what the runner was supposed to buy.** The
> four pass criteria all measure whether it is *safe*; none measures whether it is *better*. **A
> trial that cannot fail on value is a trial that cannot justify shipping.**

Two of the four criteria were never exercised at all across three slices — no `blocked` return,
no respawn — and criterion 4's cost half never got a number, because **the two measurements an
owner decision explicitly ordered captured at a named point were never written down.** The trial
skipped its own instrument. The log's own summary of that, its fourth sighting of one failure in
a fresh costume: **a number that lives only in a transcript is not a number** — a sibling of the
third report's theme (*a number recorded in prose is not the number the machine enforces*) by a
different mechanism.

Two further results from the trial that belong in the kit's record regardless of F3's fate:

- **`blocked` is rare by design, not flaky.** Two different agents met the *same* genuine spec
  conflict; neither reached for `blocked`, because both times a better move existed (one measured
  both readings and deferred the choice to the slice that owns it; the other decided it and
  pinned it by test). **For a slice with a detailed spec, the halts get spent at scope
  confirmation, before any spawn.** Any future encoding of F3 should label `blocked` and
  respawn-recovery as **unexercised**, not validated.
- **The two-state return contract needs at least two more states**: *done except for work that
  can only happen outside the agent boundary* (the CI-dependent exit criterion of finding 5), and
  *done, with a real design question deferred to a later slice*.

**Kit file(s) implicated.** `FEATURE_PLAN.md` §3 (trial protocol).

**Suggested fix.** A trial states what the change is supposed to buy, and how that would be
measured, **before it runs** — alongside its safety criteria. The pre-registration mechanism
already exists and was used well for the safety half.

---

## 9. Per-slice detail is written into the wrong file by construction, and R3.7 relocates it rather than preventing it

**Severity: low-medium.** Wasted effort every slice, paid back once per arc, and the file it was
meant to fix is still unusable.

**What happened.** Five slice close-outs wrote 83, 163, 119, 84 and 86 lines of per-slice detail
into `spec/PROJECT_INDEX.md`. The phase close then ran R3.7's archiving step and moved **1,571
lines** out into the phase spec. **The file is still 1,716 lines afterwards**, with START HERE
sitting above 90 backlog entries and five environment write-ups.

The arithmetic is the finding: **the detail was written into the wrong file five times and
corrected once.** R3.7 (0.9.0) added the archiving step and the bounded/growing markers, both of
which work as specified; neither stops the detail being written to the dashboard in the first
place.

**Kit file(s) implicated.** `commands/end-slice.md` step 9;
`templates/PROJECT_INDEX.template.md`; `commands/end-phase.md` step 7 (R3.7's archiving bullet).

**Suggested fix.** `commands/end-slice.md` step 9 records **status only** — one line per slice —
and the detail goes where it will live anyway. The commit message is already the better record:
this arc's recovery commit message is 40 lines and more precise than any index entry the arc
produced. **This deletes R3.7's relocation rather than optimizing it**, which is a small worked
example of what finding 7 is asking for. Note R3.7's own triage already identified the cause —
*"no section is marked bounded and no step ever removes anything"*; marking sections was half the
fix, and not writing there is the other half.

---

## 10. R3.6 escalates a recurring gotcha into a control and says nothing about the control's remediation being safe

**Severity: low.** Caught immediately; costly if unnoticed.

**What happened.** A line-endings hazard hit its **sixth** recurrence during this arc, and the
control R3.6 mandated worked exactly as designed — the check failed the gate the same minute an
editor silently rewrote all 685 lines of a test module. R3.6 is validated by this. But the
control's **failure message** hands the operator a one-line byte-replacement fix, which is
correct only for the files the check names. Applied over the whole tracked tree it **corrupted
two PNG files**, whose 8-byte magic legitimately contains a CR LF pair. Caught and restored
within minutes, magic bytes re-verified.

**Why it belongs here.** `commands/end-slice.md` §6 requires the third recurrence to buy *"a gate
step, a hook, or a test."* It says nothing about the control's output, which is the part an
operator acts on under time pressure — and the kit's own *verify the denominator* lens, in
`reference/REVIEW_LENSES.md`, is exactly what the control's error message failed.

**Kit file(s) implicated.** `commands/end-slice.md` §6.

**Suggested fix.** One clause: a control that hands the operator a remediation command must scope
that command to the population the control actually flags.

---

## What worked well

Four practices earned their keep with hard evidence this arc. Finding 7's simplification pass
must not touch them.

- **Mutation testing.** The two new modules sat at **100% line coverage with 9 surviving
  mutations**, including one that deletes the arc's single completeness guarantee with the suite
  green. All 9 were reproduced independently before any fix; all 9 killed on exactly their own
  new test. **22 mutations across the arc close, all killed.** Line coverage said nothing true
  here, and the 52% CI floor would have been met either way.
- **Re-derivation before the slice** (`commands/next-slice.md` §2, R2/R3.2). The strongest single
  result of the arc: re-deriving the evidence for a ratified score threshold **disproved the
  claim it existed to make reproducible** — the recorded separation figure does not reproduce, an
  in-corpus probe scores well above the threshold and is not escalated, so the margin is
  negative. A rule that retracts a ratified number pays for itself outright. It also caught both
  unsatisfiable exit criteria in finding 5, and a slice budget that did not cover the slice (the
  approved figure itemized the offline half and omitted the paid spot-checks named in the same
  sentence).
- **The whole-arc review — fifth arc running that it caught what clean slice reviews missed.**
  Across four reviewers this time. Its CRITICAL was a *comment*: two newly-written comments
  asserted that a hot-reload endpoint picks up a replaced index file, which it does not — the
  database's instance cache is path-keyed — and the project's own runbook had known this for
  months.
- **Verify findings before applying them** (R3.4, 0.9.0). 25 fixed / 3 deferred / **3 re-graded
  or discarded**. One discarded finding claimed a missing line-endings config file and framed the
  slice's new files as the anomaly; the file exists, is tracked, pins the setting, and **all 128
  committed blobs** were already correct — the *working copies* were the anomaly, 14 of 128 of
  them. Applied literally it would have driven a repo-wide change in the wrong direction.

One more, recorded separately because it is 0.9.0's R3.1 paying for itself twice in one session:
**deploy verification read from the running container's own startup log** confirmed this arc
deployed inert exactly as designed **and**, with the same command, **disproved a standing
liveness claim from the previous arc** — a CSRF origin check believed enabled read `DISABLED` on
all 9 container starts since that merge, and a 30-day log search for its `ENABLED` banner
returned zero rows. It had never been live. Fixed the same day, with the header value **measured
from a real authenticated request first** rather than guessed.

---

## Suggested priority

| # | Change | Kit file(s) | Effort |
|---|---|---|---|
| **7** | **Simplification pass before this batch ships** — audit every rule added since 0.5.0 against a confirmed catch | `FEATURE_PLAN.md` §12, `commands/*.md`, `templates/*.md` | **M** (owner-ranked first) |
| 1 | Clean tree + all fixes committed as a precondition to any review fan-out; a commit message may not claim an untested fix | `commands/end-phase.md` §5, `commands/end-slice.md` §3 | S |
| 2 | When no slice's exit criteria required running the app, `/end-phase` adds a local real-data pass before the PR; detect the condition in the testability sweep | `commands/end-phase.md` §3, `commands/plan-phase.md` step 2, `templates/SDLC.template.md` | S |
| 3 | The fix batch is assembled only after every reviewer returns, and goes through the gate as one unit | `commands/end-phase.md` §5 | S |
| 4 | New lens — shared mutable state under the runtime's concurrency model, with 410/600 as its specimen | `reference/REVIEW_LENSES.md` | S |
| 5 | Each exit criterion names what observes it and when | `commands/plan-phase.md` step 2 | S |
| 6 | Slice close-out asks whether anything was friction with the *process*, and writes it to the log | `commands/end-slice.md` close-out | S |
| 9 | Slice close-out records status only; detail goes to the phase spec or stays in the commit message (deletes R3.7's relocation) | `commands/end-slice.md` step 9, `commands/end-phase.md` step 7 | S |
| 8 | A trial states what the change is supposed to buy, and how it is measured, before it runs | `FEATURE_PLAN.md` §3 | S |
| 10 | A control's remediation command is scoped to the population the control flags | `commands/end-slice.md` §6 | XS |

---

## Cross-cutting theme

**The kit specifies what each step must produce and almost never what makes it done.**

The gate is the exception, and it is the only step that never failed this arc: three commands,
all green, no judgment required. Every finding above is a step with an output and no completion
condition — so it ends when attention runs out rather than when the work is finished.

- The **review** ended when a batch was committed, not when the reviewers returned — and the
  reviewer who returned last found the worst gap in the arc (finding 3).
- The **acceptance review** ended when there was nothing visible to look at, on the arc whose
  main defect was invisible to every test (finding 2).
- The **fix batch's commit message** ended as written, not as verified against the tree it
  described (finding 1).
- The **friction log** has a reader, an aging rule, and no moment at which anyone is asked to
  write to it (finding 6).
- The **trial** ended by running out of slices, having never defined what success was (finding
  8) — and skipped its own instrument at the one point an owner decision named it, because
  nothing downstream blocked on it.

That is also the honest link to the owner's top-ranked item. **Five consecutive batches have
added *steps*; not one has added a *stopping condition*.** The simplification pass finding 7 asks
for is not only about volume — it is the opportunity to convert some of what has accumulated from
*"do this"* into *"this is done when"*, which is the only form the gate has ever taken and the
only one that has never been skipped.

---

*Produced by `/sdlc-retro` on kit 0.9.0. The project half of these lessons was applied to the
adopter's own `spec/PROJECT_INDEX.md` and is not reproduced here.*
