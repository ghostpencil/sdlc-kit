# Field report (kit 0.24.0, 8th phase of a real adoption): 9 findings — the kit verifies that a step ran, never that it could have caught anything

**Source:** [sdlc-kit#9](https://github.com/ghostpencil/sdlc-kit/issues/9), filed
2026-08-21 — the **ninth** field report, and the sixth from this adopter (their count;
it covers their eighth phase since adoption). Written against **0.24.0** at the Phase 08
boundary. Reproduced verbatim from the **anonymized** issue body — the adopter keeps the
unredacted copy deliberately as the only one, and where the two disagree theirs is right,
so nothing here should be de-anonymized by a later edit (that includes this file's name).
The adopter's own correction, posted as the issue's first comment rather than folded into
the body, is reproduced after the report under *Correction from the adopter*. The triage
lives in `FEATURE_PLAN.md` §70.

**Read the triage before acting on the priority table.** Three of the nine findings did
not survive verification as filed: finding 7 was already fixed in 0.24.0 itself, finding
4's premise is false against the text it quotes, and finding 9's first half asks for the
mechanism 0.26.0 deliberately ruled *out* three days earlier — while its own specimen
shows the shipped recipe is unsafe where the step invokes it. §70.2 has each one.

---

Field report from a real adoption, produced by `/sdlc-retro` at a phase boundary. Project
details are generalized; the findings, evidence and numbers are as measured. Money figures
are withheld — they are the adopter's real spend — and nothing here depends on them.

**Adopter profile.** A small nonprofit's internal Q&A + task web app, deployed behind an SSO
proxy. Python, stdlib-first, single-maintainer, Windows, Claude Code. Kit **0.24.0**, adopted
at 0.1.0 on an existing ungated codebase. **Same adopter as the five prior reports**; this is
the **sixth** report and covers the **eighth** phase since adoption.

**The arc.** 5 slices, 1 PR, 27 numbered owner decisions. It shipped a cost-reporting module
behind a new admin-gated read-only route, two operator flags that ship inert, and a boot
warning. Its most valuable output was not code: a production measurement **overturned the
premise the arc had been planned on**, and a correction that had been sitting in the record
for two days turned out to be a claim the sample could not have distinguished.

**The arc itself went well again**, which is again why the report is worth reading — none of
the nine findings is about the work:

| | previous phase close | this phase close | how measured |
|---|---|---|---|
| lint | 0 | **0 — green** | re-run during the retro |
| typecheck | 0 in 17 source files | **0 in 18 source files** | re-run during the retro |
| tests | 678 | **761, all passing** | re-run during the retro |
| CI coverage floor | 61 | **63** | read from the CI workflow |
| fix commits on the arc branch | 0 | **0** | `git log <arc range>` |
| close-out records COMPLETE | 7 / 7 | **8 / 8** | commit bodies, all four keys present |
| observed REDs recorded | 51 | **53** | `.git/sdlc-tdd/guard.log` |
| skill activations | 33 | **20** | `.git/sdlc-skill-ledger.jsonl` |

Everything the gate **enforces** is green and agrees with CI. **At that same moment two
recorded numbers were wrong on disk and the backlog contained four entries sharing two
identifiers** — both found by this retro, neither by the close that had just run.

**The theme, one step on from the previous report's:** that report concluded *this kit is
good at making a step produce evidence and bad at making a number reconcile.* The kit
answered with a reconcile pass (0.26.0). This arc closed one day later on 0.24.0, and the
generalization the kit has still not made is the reason a reconcile pass would not have
caught it:

> **This kit verifies that a step *ran*. It does not verify that a step could have *caught*
> anything, or that a decision it recorded ever reached a *terminal state*.**

---

## 1. The floor-reconcile bullet names its homes by document — and a document can hold the same number twice

**Severity: high.** It was wrong on disk immediately after the close whose bullet exists to
prevent exactly this, and it is the fourth consecutive retro on this adoption to find a
number with more than one home drifted apart — the second on the coverage floor specifically.

**Measured at the retro**, reading each artifact:

| number | CI workflow (enforcement) | `spec/SDLC.md` *Records* | `spec/SDLC.md` *Coverage floor* | `spec/PROJECT_INDEX.md` |
|---|---|---|---|---|
| coverage floor | **63** | **63** | **61** ❌ | **61** ❌ |
| test count | — | **761** | **678** ❌ | **678** ❌ |

Note the shape, because it is what makes this hard to see: **the enforcement artifact and the
*Records* table agree** — the two things the kit's procedures name — while a *second* home
inside the very same file, and the index's current-ceiling line, were never touched. The
Phase History row recorded the raise correctly, so the *history* is right and the
*current-state* prose is wrong.

**The text implicated**, `commands/end-phase.md` step 7, the *Coverage floor* bullet, read off
the installed copy:

> - **Coverage floor — bump the enforcement, then reconcile:** if the coverage measured
>   for the merged branch rose this arc, set the threshold […] to just under the measured
>   number, in the same docs commit as the bookkeeping below. Then **assert the two homes
>   agree**: the floor recorded in `spec/PROJECT_INDEX.md` (and `spec/SDLC.md`) and that
>   threshold value must be identical — the bullet is not done until they are. […] The
>   recorded number is a claim; the threshold value is the enforcement — a mismatch means
>   the ratchet is not actually ratcheting.

The bullet ran. It set the enforcement and it updated `spec/SDLC.md` — the *Records* table.
It then declared itself done with two of its own named homes still stale, because **"the
floor recorded in `spec/SDLC.md`" is not one location.** That file holds the number twice,
about 300 lines apart: once in the *Records* enforcement table, once in the *Coverage floor*
narrative section that also carries the test count. The phrase "the two homes" is what
licensed stopping after the first match.

`templates/SDLC.template.md` is the second implicated file, because it **seeds both homes**.
Quoted from the instantiated copy, placeholders resolved — *Records*:

> | `pytest` | **7 passing at adoption; suite now 761 tests, 0 failing** | must stay green […] |

and, 300 lines later, *Coverage floor*:

> **Current: 61.45% in CI, floor at 61** (raised there at the previous arc boundary; the
> suite is now **678 tests**).

One template, one file, two homes for two numbers, and no rule saying they are the same fact.
The adoption's own warning had even calcified around the mistake — it read *"The floor lives
in **two** places"* while living in four.

**⚠️ This is not fixed by 0.26.0**, which is the part worth the maintainer's attention. That
release adds a reconcile pass covering *"the **whole *Records* table**, not the two rows the
kit shipped procedures for"*. Here **the *Records* table was already correct.** A pass over
*Records* would have reported this instance clean.

**Suggested fix.** Make the reconcile a **search for the value**, not a visit to named
documents: take the number the enforcing artifact carries, then require that no occurrence of
the *old* value survives anywhere in the spec set — the check is a grep and its failure is a
file list. A list of named homes goes stale the first time anyone writes the number somewhere
new, which is precisely how the adoption's warning came to say "two". Both homes of the rule
need it: `commands/end-phase.md` step 7 and `templates/SDLC.template.md`'s *Coverage floor*.

---

## 2. Nothing allocates a backlog entry's identifier, and two slice reviews in one arc minted the same two numbers

**Severity: high.** Every downstream step addresses entries by number, and the ambiguity is
silent.

**Measured.** The deferred backlog held **106 numbered entries and 104 distinct
identifiers.** Two entries shared identifier *N* and two shared *N+1*:

```
N     entry A — a lock-holding concern in a store module     (Slice review, day 1, slice 1)
N     entry B — stale line-number anchors in an appendix     (Slice review, day 1, slice 3)
N+1   entry C — a test leaking a module into sys.modules     (Slice review, day 1, slice 1)
N+1   entry D — two config tables that nothing reconciles    (Slice review, day 1, slice 3)
```

All four minted in the same arc, on the same day, by two different slice reviews writing into
different regions of a 1,500-line unordered list. Neither read the file's maximum identifier.

**The damage was already live in the document that scopes the next phase.** The adoption's
START HERE carries a paragraph instructing the next `/plan-phase` to re-derive before scoping,
and it names one of these numbers as an entry whose stated risk is overstated. That reference
resolves by content to entry D — and by *number* to two entries, the other being an unrelated,
legitimately open test-hermeticity finding that a scoping pass reading "*N+1* is overstated"
could discard on sight.

**The text implicated**, `commands/end-slice.md` §9, read off the installed copy:

> - Append deferred review findings to the backlog with rationale, provenance
>   (e.g. "(slice review, `<date>`)"), and the cause marker from step 4's triage
>   (**measured** / **suspected**).

Three attributes are prescribed. The identifier — the only one every other step depends on —
is not mentioned. The second home is `commands/end-phase.md` step 7's backlog bullet, written
as though a number addresses exactly one line:

> **Record each verdict on the entry's own line as it is taken** […] The line's marker is
> what the retirement bullet below reads.

and its retirement bullet, which makes a promise a collision quietly breaks:

> move the entries **verbatim** — any numbering, provenance tags, and markers intact, so an
> old reference to an entry still resolves.

With a collision the reference resolves to two things, and "verbatim" preserves the collision
into the history file — where, per the kit's own rule, no session reads at start.
`templates/PROJECT_INDEX.template.md` seeds the backlog section and states no allocation rule
either.

**Suggested fix.** One clause in `end-slice.md` §9 — the entry's number is the next integer
above the file's current maximum, **read from the file at append time** — and a uniqueness
assertion in `end-phase.md` step 7's reconcile, which is one `sort | uniq -d` and would have
caught this on the day it happened.

---

## 3. "Absorbed by a retro" is a third state the escalation rule does not have, and it reads as closure

**Severity: high.** This is the mechanism by which one hazard reached **eleven recorded
recurrences** with two retros and two owner rulings in between, and nothing built.

**The rule**, from `templates/SDLC.template.md` *Bookkeeping rules* and restated in
`commands/end-slice.md` §9:

> ⚠️ **A gotcha recorded in three consecutive slices becomes a check, or is ratified
> unpreventable.** The third recurrence buys a gate step, a hook, or a test; it does not buy
> a fourth, better-worded note. […] **Those are the hazard's only two closed states; a
> sharper note is neither.**

The TDD-ordering guard's ergonomics were logged at four slices of the previous arc, **absorbed
by the previous retro as its finding 3 with an owner ruling** (*scope the guard to tracked
repo paths*), then logged again at three slices of this arc and — for the first time — at a
**phase** close. The adoption's friction log, written at the moment of the ninth:

> ⚠️ **The previous retro absorbed this and the guard is unchanged, so the count is now nine
> with no implemented fix** — the entry above already flags "an absorbed finding with no
> implemented change" as its own defect class. It is no longer a prediction.

**Measured from `.git/sdlc-tdd/guard.log`** over the arc — one clone, the maintainer's
machine, since `.git/` is per-clone:

- **7** production writes denied, **1 of them to a path outside the repository entirely** — a
  session-scratchpad file that can never reach the gate. That is the exact case the previous
  retro's owner ruling addressed.
- **11** distinct refactor licenses hand-declared, **29** writes admitted under them, **9**
  revoked by an intervening test edit — because the mandated close-out steps (quality pass,
  then mutation check) *alternate* production and test edits by nature.
- **40** test runs recognised and **not counted** because the command was compound. This
  repository's path contains a space, so `cd "<path>" && pytest` is the natural form.

**Two of those 40 were produced by the retro session itself**, which writes no production code
at all.

**Why the escalation rule structurally cannot see it.** `commands/sdlc-retro.md` step 6:

> Flip each Kit-friction-log entry this report absorbed to its absorbed form — `- <date> —
> <friction> — absorbed by retro <date>` — the one shape the log's own comment prescribes and
> step 2's sweep reads

and step 2's sweep treats that marker as the closed state:

> entries a previous retro absorbed carry a marker, so report the ones that do not

So an entry absorbed into a report — ruling taken, nothing built — is **invisible to the next
retro's sweep for long-lived friction**, and the three-recurrences rule has no way to count
past absorption. **Absorption records that a finding was transmitted, and the process treats
transmission as resolution.**

**Suggested fix**, three parts, none large:

1. `sdlc-retro.md` step 6's flip carries a disposition, not just a date:
   `absorbed by retro <date> — <implemented in <commit> | ruled unpreventable | RULING OPEN>`.
   Only the first two are closed states.
2. `sdlc-retro.md` step 2's friction sweep reports absorbed-with-open-ruling entries
   **alongside** unabsorbed ones, with how many phases since absorption.
3. The escalation rule in `end-slice.md` §9 and `templates/SDLC.template.md` names absorption
   explicitly as *not* a closed state.

*(This adoption's owner ruled at the interview: implement the guard fix — tracked-path scope
**and** compound-command counting, the second of which had never had a ruling before.)*

---

## 4. The kit ships `mutation-testing` and no workflow command dispatches it — fifth report, second consecutive arc at zero

**Severity: high**, because on this adoption mutation is the step with the best defect record
and it is the only named step the process never invokes by name.

**Measured** from `.git/sdlc-skill-ledger.jsonl`: **20 tool-dispatched skill activations** in
the arc — `tdd` ×4, `change-simplify` ×4, `diff-review` ×6, `change-verify` ×3, plus 3 of an
API-reference skill — and **zero** for `mutation-testing`, while roughly **40 mutations were
run hand-rolled** across five slices and the arc review. The ledger is demonstrably alive in
this window, so this is an absence with a denominator rather than an instrument that stopped
recording.

What those hand-rolled mutations found, from the phase spec's whole-arc review section:

> **2 findings fixed** […] Both fixes came from **mutation, not from reading** — the
> reviewer's eye passed over both.

and on the more serious of the two — a module-scope constant that also had a second copy
inside a reload function:

> deleting the module-scope one left **all 757 tests green**, because every test that reads
> the global calls the reload function first […] the reload path is reachable only from one
> admin route, so the **unpinned copy is the one production runs on for the life of a
> container.**

A defect that had survived **two arcs** with a fully green suite, found by the step no command
dispatches.

**The text implicated.** `commands/end-slice.md` §5, headed *"Mutation check — a new guard
must be seen to fail"*, describes the technique inline and never names the installed skill;
`commands/end-phase.md` §5 likewise. `skills/mutation-testing/SKILL.md` exists and is reachable
only if the operator happens to remember it.

**This is the second report's finding 3, unchanged five reports later.**

Beyond tidiness this is load-bearing, and finding 9 is why: a hand-rolled loop does not carry
the skill's own safety rules.

---

## 5. The Stop-time close-out backstop is scoped to a window the workflow itself empties

**Severity: medium-high.** A control that *cannot* catch logs the same word as a control that
found nothing.

**Measured** from `.git/sdlc-close-out/log`: **121 lines**, of which roughly 100 read

```
stop: clean (no candidate commits; unpushed @{u}..HEAD, cap 20)
```

`/end-slice` step 7 commits **and pushes** the slice. By the time any session stops, the range
`@{u}..HEAD` is empty — so "clean" here means *there was nothing in scope to inspect*, and is
indistinguishable in the log from *the close-out record was complete*. Its only non-clean
firings in the whole arc were **4 WOULD-BLOCK lines on a single documentation commit** made
inside a slice session: a false positive, and log-only by design. **Real catches over the arc:
zero.**

The adoption's *Records* section records the control as installed and proven:

> Fire-proof: a fresh headless session's stop executed the block fail-open and wrote its
> classification to the log

**That proof establishes that the hook *executed*. It says nothing about whether its window
could ever contain anything.** The transferable lesson generalizes past this one hook:

> **A fire-proof and a catch-proof are different tests. A control that has only ever been
> fire-proofed is a control whose reach is unmeasured.**

The kit already reasons this way in one domain and states it beautifully for coverage floors —
*"prove it fires — once: set it above the observed number, run the gate's own commands, watch
the failure, then set the real value"* — and does not apply it to its own hooks.

**The text implicated.** `hooks/sdlc-close-out.sh`, `stop-check` mode (its `@{u}..HEAD` range),
and the *Records* wording seeded by `templates/SDLC.template.md`, which records installation
and a fire-proof as though they settled the question.

**Suggested fix.** Scope `stop-check` to the arc branch's recent commits rather than to
unpushed ones, and add a negative case to the install proof: a session that stops with a real
close-out record missing must be **seen to be flagged**, not merely seen to run.

*(Deletion was considered at the interview and declined — the command-step `check` mode is
fail-closed, separate, and produced 8/8 COMPLETE records this arc.)*

---

## 6. The kit re-derives a backlog entry's cause and its numbers, and discharges neither a ratified *method* nor a ratified *risk*

**Severity: medium-high.** Both halves cost something real this arc, and the adopter named the
second as the arc's genuine silence.

**The risk half.** From the phase spec's whole-arc review:

> **Deferred:** entry X **was neither confirmed nor discarded**, though *Risks* required it be
> settled *"while in [the deployment manifest]"* — and the arc added two more declarations of
> exactly the kind it warns about.

The phase spec's own *Risks & Deferred* section carried an obligation to settle a question
**during** the arc. The arc closed without settling it, having made the question larger, and
nothing at the close noticed. `commands/end-phase.md` step 7 reconciles the product contract,
the coverage floor, the red baseline, the backlog and the Phase History row — **it never
re-reads the phase spec's own Risks section.** `commands/plan-phase.md` step 3 requires risks
be *written*; nothing requires they reach a terminal state.

**The method half**, logged in the friction log at the moment it happened:

> A ratified decision reads *"byte-diff the rendered request JSON, **then** bisect request
> parameters"*; the slice went straight to the bisect, and §2's re-derivation step passed
> cleanly because the entry's cause and numbers were the things it looks at. […] running the
> byte-diff proved the cached region **byte-identical** between the two calls and named a
> fourth request difference the bisect had not tested and had only eliminated by inference.

**The text implicated**, `commands/next-slice.md` §2, whose canonical statement is
`templates/SDLC.template.md` *Slice loop* step 2:

> If the slice comes from the backlog, **re-derive the entry's stated cause before writing any
> fix, proportionally to its marker** […] **The same rule covers an `estimated` number this
> slice implements**. Derive it before starting

Cause and number. Not the method a ratified decision prescribes, and not the obligations the
phase spec attached to the work. Also `skills/diff-review/SKILL.md`, whose Spec axis reads
*exit criteria* — which the slice had met — rather than the decisions the slice was told to
implement *through*. The omission was caught, but by a reviewer who happened to read the
decision, not by a step.

**Suggested fix.** `next-slice.md` §2 extends re-derivation to any ratified decision the slice
implements *through* — a prescribed method is as binding as a ratified number. And
`end-phase.md` step 7 gains a Risks discharge line in its reconcile: every Risks entry reaches
*confirmed / discarded / explicitly carried forward with a new home*, so an obligation cannot
lapse by silence. This is the same shape as 0.26.0's contract-absent-direction pass, applied
to the section that records what the phase was worried about.

---

## 7. `settings.template.json` still pins hooks behind `"shell": "bash"`, which silently never fires on Claude Code for Windows

**Severity: medium**, and it is the **oldest unabsorbed entry in this adoption's friction log
— two phase closes old** — carried into this report automatically by the age rule rather than
by the interview.

From the friction log entry:

> the kit's `settings.template.json` pins every bash-syntax hook behind `"shell": "bash"`, and
> on Claude Code 2.1.231 (Windows, headless route) a pinned hook **never fires** while an
> unpinned `sh <script>` launcher does — bench-measured on Stop and PostToolUse […] this
> project's pre-update gate hook had been silently inert

A lint gate believed installed since adoption was, on measurement, never running. **The failure
mode is total and silent: nothing distinguishes "the hook passed" from "the hook does not
exist."** This adoption now wires every hook the launcher-neutral way and records that as a
deliberate, measured **divergence from the template** — which means the template is the one
artifact still carrying the defect for the next adopter. It is the kit's own 0.18.0
launcher-discipline lesson, learned on one CLI and not carried to the other.

**Suggested fix.** Drop the pin from `templates/settings.template.json` in favour of the
launcher-neutral `sh <script>` / `python <script>` command lines the kit already adopted at
0.18.0 — and add the install check that would have caught it, which is finding 5's lesson
again: after setup, cause a hook to fail on purpose and require the failure be **seen**.

---

## 8. `change-verify` §3 has no shape for the commonest real front door: a process that never returns

**Severity: medium.** It costs minutes rather than correctness — but it cost them again this
arc **with the skill dispatched**, which makes it a text gap rather than an operator lapse.

From the friction log:

> A web app's own entry point binds a socket and serves forever, so the skill's "execute and
> capture the output" costs two failed attempts before it works — `subprocess.run(timeout=…)`
> discards the output it was about to prove the pass with, and a pipe-attached Python
> **buffers stdout**, so the banner under test never arrives. A third trap on Windows: the
> captured bytes are UTF-8 and the console is cp1252, so *printing* the evidence raises
> `UnicodeEncodeError` after the run succeeded.

And again at the **phase-level** verification, where the ledger shows the skill *was*
dispatched:

> ⚠️ Recorded because it cost time: the app's boot banner is **invisible without
> `PYTHONUNBUFFERED=1`** when stdout is redirected, which is the same trap the original deploy
> hit.

**The text implicated.** `skills/change-verify/SKILL.md` §3, *"Reach it the way something real
does — by actually running it"*. The skill's prime directive — quote literal bytes from a real
run — makes the trap expensive by design, because the honest response to a failed capture is to
re-run rather than to describe.

**Suggested fix.** Three lines in §3 naming the long-running-process shape: `Popen` + an
unbuffered environment + `terminate` + `communicate`, with a note that a buffered child is the
commonest reason expected output "does not appear".

**A related observation in the same family**, recorded because it bears on how the ledger
should be read: `change-verify` was dispatched at **3 of 6** verification points; two slices
recorded `verify: ran` with detailed observations and no ledger line. The step happened; the
skill's rules — including its environment-constraint step — were not in context when it did.
The ledger records **dispatch, not diligence**, so this is evidence about *how* a step ran,
never about whether it ran.

---

## 9. Two skill texts state a rule and name no mechanism, and the obvious mechanism is destructive

**Severity: medium-low**, but one of the two nearly cost a slice's uncommitted work.

`skills/mutation-testing/SKILL.md` says, in its standing rules:

> **Always revert:** after each test run, restore the original code

naming no mechanism. The natural one — and the one this adoption's own standing local advice
recommends, for an unrelated line-endings reason — is `git checkout -- <path>`. From the
friction log:

> the mutation was reverted with `git checkout -- <file>`, which reverted the **uncommitted
> implementation along with the mutant** — the file had no committed version of the slice's
> work behind it. It was recoverable only because the code was still in the session's context.

This compounds finding 4 directly: a hand-rolled mutation loop is exactly where a missing
mechanism bites, and the skill is never dispatched.

`skills/change-simplify/SKILL.md` §3 states *"one move at a time, gate between"* as though the
gate were free. At a ~100-second suite, two quality moves cost three backgrounded full-gate
runs and a poll loop each. The rule is right — a batch that goes red says only that the batch
broke something — but its cost scales with suite runtime, which is the one thing a maturing
project reliably grows, and the skill leaves each session to invent the trade silently.

**Suggested fix.** `mutation-testing/SKILL.md`: name the safe revert — re-edit the mutated
characters back — and warn that a VCS-level restore discards uncommitted work the mutation was
applied on top of. `change-simplify/SKILL.md` §3: say what the intermediate gate may be trimmed
to (the axis's own test files plus lint and typecheck, with the full suite once at the end).

**Also carried, unabsorbed one phase:** the PostToolUse lint hook rejects a legitimate
intermediate refactor state — an import added in one edit and its first use in the next is
always unused-import-red in between — so a change cannot be sequenced that way at all. It
*shapes the design*, and it has no notion of a refactor in progress even though the TDD guard
beside it has an explicit license. And `end-slice.md` §5's mutation contract — *"delete it and
watch the suite fail"* — assumes the new branch is reachable; a guard whose only observer is
the typechecker is correctly green when deleted, and the step as written reads that as a test
gap.

---

## What worked well

Named so a simplification pass does not remove them. **Each catch is listed with its
disposition** — a catch is not a fix.

- **The whole-arc review, six arcs running.** Two findings this arc, both fixed before the PR;
  three further candidates **discarded on verification and reported as discarded**, which is
  evidence about the review rather than about the code. Slice review passed over both fixed
  findings.
- **Mutation as the observer of record** — with the caveat of finding 4. Both arc findings came
  from mutation rather than reading, and one had survived two arcs with a fully green suite.
- **Re-derivation before the slice fired again and changed the work.** One entry's stated cause
  was stale in a way that inverted its scope; another was re-derived by execution and re-tagged
  `measured`. This adoption's running score on entries checked at slice start is unchanged: the
  cause has been wrong every time anyone looked.
- **Halt 4 taken on production, and split around the merge by owner ruling.** One acceptance
  item proved a new operator flag **operable rather than merely present** — with the flag live
  for six minutes, a real request recorded zero cache writes while its input token count moved
  by the exact size of the prefix. Then the same record refused the tempting conclusion:
  *"⚠️ It does **not** show `off` is cheaper — the two questions differ in size."* **The kit's
  halt 4 assumes acceptance precedes the PR**; this arc's behavior was only observable in
  production, and the ruling that moved four items after the deploy is worth generalizing into
  the command.
- **The retirement bullet's own re-read check fired for the first time** and produced its
  designed failure: a half-delivered entry was pulled back out of the history file rather than
  retired on a marker it only half-earned. The check has a negative case and the negative case
  ran.
- **The close-out evidence record, 8/8 COMPLETE**, including honest zero-forms with reasons
  (*"RED: not observed — the two boundary guards passed on first write […] their weight was
  proved by mutation instead"*). **This is the only reason the step-evidence table below could
  be built from artifacts rather than from memory.**
- **The slice-close friction prompt, still working two arcs after it shipped.** Five new
  entries, all written at the moment of friction, and **five of this report's nine findings
  rest on them.** Findings 3, 8 and 9 could not have been reconstructed at the boundary.
- **The arc corrected its own record rather than softening it.** A two-day-old ratified claim
  was **deleted, not hedged**, when production contradicted it — and the lesson recorded was
  not the comfortable one. The record now reads: *a measurement that cannot distinguish two
  hypotheses is not evidence for either.*

---

## Step evidence

Every step named by the process, with its state this arc. Sources: slice commit bodies,
`.git/sdlc-skill-ledger.jsonl`, `.git/sdlc-tdd/guard.log`, `.git/sdlc-close-out/log` — **all
four read from one clone, the maintainer's; `.git/` is per-clone.** Slash-typed commands are
injected with no tool call and write no ledger line, so their absence there is **no signal
either way**; the ledger is otherwise demonstrably alive here.

| Step | State | Evidence |
|---|---|---|
| Backlog re-derivation (`next-slice` §2) | **caught** | one entry's cause stale, one re-derived by execution and re-tagged, one found overstated at planning |
| Ratified-*method* re-derivation | **no evidence — not a step** | caught by the review, not by §2 (finding 6) |
| Observed RED (`next-slice` §4) | **ran** | **53** RED observations in the guard log; 30+ `RED:` lines in commit bodies with command, failing line, exit code; 6 honest zero-forms with reasons |
| Quality pass — `change-simplify` | **ran** 4/5, **skipped with reason** 1/5 | 2/2/3/1 moves; the docs-only slice recorded *"skipped — docs-only diff"* |
| Slice review — `diff-review` | **ran** 5/5 | 5 ledger dispatches + 1 at the arc |
| Review lenses | **caught** | a shared-state lens forced a `suspected` tag; arc lenses *unconsumed artifact* (1 genuine hit) and *preserved contract* (clean, negative case proven to fire) |
| Mutation check | **caught** | ~40 mutations; 2 survivors pinned at slice 1; **both** arc findings. ⚠️ skill **0 dispatches** (finding 4) |
| Slice verification — `change-verify` | **ran** 6/6 recorded | `verify:` line in every code commit + phase level. ⚠️ skill dispatched at **3 of 6** (finding 8) |
| Close-out record `check` (fail-closed) | **ran** | 8/8 commits carry all four keys |
| Close-out `stop-check` backstop | **no evidence of reach** | 121 lines, ~100 vacuous `clean`, 4 false positives, **0 real catches** (finding 5) |
| Whole-arc review | **caught** | 2 fixed, 3 discarded on verification and named, 1 deferred |
| Phase-level verification | **ran** | 4 real boots through the app's front door against real data, zero spend |
| Halt 1 — phase scope | **ran** | owner chose from 4 candidate arcs |
| Halt 2 — slice scope | **ran** | 5 slices; one behavior refined by owner ruling inside a slice |
| Halt 3 — design questions | **caught** | a decision taken mid-arc when acceptance overturned the premise; a planned fallback withdrawn |
| Halt 4 — acceptance | **caught** | 8 items, split around the merge by owner ruling; one proved operability, one surfaced the arc's most expensive measurement |
| Halt 5 — merge approval | **ran** | the arc's PR |
| Coverage-floor bump + reconcile | **ran, then failed silently** | enforcement set correctly; 2 of 4 homes left stale (finding 1) |
| Red-baseline re-derivation | **caught** | every *Records* row re-derived rather than carried: 17→18 source files, 678→761 tests |
| Backlog reconcile before counting | **partial** | 5 entries retired with markers; **2 duplicate identifiers uncounted** (finding 2) |
| Retirement + re-read check | **caught** | a half-delivered entry pulled back — the check's negative case, first firing |
| Product-contract reconcile | **ran** | 12 entries added; 1 claim-only promoted to pinned; the contract check's negative case proven |
| Friction prompt (`end-slice` §9) | **caught** | 5 new entries; 5 of 9 findings rest on them |
| TDD-ordering guards | **ran, at cost** | 7 denials (1 outside the repo), 11 licenses, 29 licensed writes, 9 revocations, **40 uncounted compound runs** (finding 3) |

---

## Suggested priority

| # | Change | File(s) | Effort |
|---|---|---|---|
| 1 | Reconcile by **searching for the value**, not by visiting named documents; assert no occurrence of the old value survives | `commands/end-phase.md` step 7; `templates/SDLC.template.md` *Coverage floor* | S |
| 2 | Name the backlog ID allocation rule (next integer above the file max, read at append time) + a uniqueness assertion in the close reconcile | `commands/end-slice.md` §9; `commands/end-phase.md` step 7; `templates/PROJECT_INDEX.template.md` | S |
| 3 | Make **absorbed** carry a disposition and stop reading as closed; sweep absorbed-with-open-ruling entries | `commands/sdlc-retro.md` steps 2 and 6; `commands/end-slice.md` §9; `templates/SDLC.template.md` | S |
| 4 | Dispatch the mutation skill by name instead of paraphrasing it | `commands/end-slice.md` §5; `commands/end-phase.md` §5 | XS |
| 5 | Scope `stop-check` to the arc branch, not `@{u}..HEAD`; add a catch-proof to the install record | `hooks/sdlc-close-out.sh`; `templates/SDLC.template.md` *Records* | S |
| 6 | Discharge Risks entries at the close; re-derive a ratified *method* the slice implements through | `commands/end-phase.md` step 7; `commands/next-slice.md` §2; `skills/diff-review/SKILL.md` | M |
| 7 | Drop the `"shell": "bash"` pin; prove a hook fails on purpose at install | `templates/settings.template.json` | S |
| 8 | Add the long-running-process capture shape (`Popen` + unbuffered + terminate + communicate) | `skills/change-verify/SKILL.md` §3 | XS |
| 9 | Name a safe revert mechanism; bound the intermediate gate's cost | `skills/mutation-testing/SKILL.md`; `skills/change-simplify/SKILL.md` §3 | XS |

---

## Cross-cutting theme

**This kit verifies that a step *ran*; it does not verify that a step could have *caught*
anything, or that a decision it recorded ever *reached a terminal state*.**

The previous report's theme was that the kit is good at making a step produce evidence and bad
at making a number reconcile. One arc later the evidence discipline is stronger than ever —
8/8 close-out records, 53 observed reds with exit codes, a deploy verified from the container's
own log in both flag directions — and every finding above is a place where an artifact exists
and nothing reads it for the right property:

- a **fire-proof** stood in for a catch-proof, and a backstop watched an empty window for a
  whole arc while logging the word "clean" a hundred times (5);
- a **reconcile bullet** visited the documents it names and declared itself done with the
  number wrong in two other places (1) — and the 0.26.0 pass, which reconciles the *Records*
  table, would have reported it clean;
- an **absorbed finding** counted as a closed one, which is how a hazard reached eleven
  recurrences with two rulings taken and nothing built (3);
- a **Risks entry** and a **ratified method** were written down where nothing ever asks whether
  they were discharged (6);
- and the step that actually found this arc's defects is the one **no command dispatches** (4).

The kit already knows the corrective in one domain and states it beautifully for coverage
floors: *prove it fires — once; set it above the observed number, watch the failure, then set
the real value.* The generalization it has not yet made is that **the same demand applies to
its own controls, its own records, and its own rulings** — a check is not installed until it
has been seen to fail, a number is not reconciled until its old value cannot be found, and a
finding is not absorbed until something changed.


---

## Correction from the adopter

**Posted as [sdlc-kit#9 comment 1](https://github.com/ghostpencil/sdlc-kit/issues/9#issuecomment-1), 2026-08-21**, and reproduced verbatim. It corrects the header table (761 → 762) and amends priority item 1 with a second clause.


Posting this rather than quietly editing, because the way it happened is the finding.

**The header table said 761 tests. The real number is 762.** Caught by CI on the push of
the retro's own commits — the first CI run on the main branch after the close printed
`762 passed`, where the report said 761.

**There is no local/CI split.** Local agrees at 762 three independent ways: collected-test
count, progress-dot count, and CI. The 761 was **inherited from the record being audited
rather than read from any run** — inside a report whose finding 1 is that recorded numbers
drift because nothing re-derives them from the artifact.

Two causes, both of which belong *inside* finding 1 rather than beside it:

**1. The local gate produces no number at all.** This adoption's `pyproject.toml` carries
`addopts = "-q"` and the suite emits no `N passed` summary line locally — verified by
capturing stdout to a file, not by watching a terminal. So "re-run the gate and read the
count" yields *nothing*, and the gap gets filled from the document under review. The
transferable rule:

> **A measurement that cannot produce a number is not a measurement.** If the step that is
> supposed to yield a count yields silence, that silence has to be an error, not an
> invitation to remember.

This matters for the kit because `end-phase.md` step 7's red-baseline bullet says *"report
this arc's count beside the recorded one"* without saying **where the count comes from**.
On a quiet-by-default runner there is no count to report, and the bullet still completes.

**2. The recorded number went stale *inside the close that recorded it*.** The baseline was
re-derived correctly at the close — from the PR's CI run, which is exactly what a careful
operator would use. Then a commit **two commits after the merge, part of the same
close-out**, added a test. The PR's CI run cannot see anything committed after the merge,
so the freshly-re-derived baseline was already wrong when the close finished.

That second one is the part I'd ask you to weigh, because **it defeats the fix I proposed
in finding 1.** Reconciling by *searching for the old value* catches the two stale coverage
floors — but not this, because 761 was never an old value. It was a value that was never
true of the main branch at all.

### Amended suggestion for priority item 1

Two clauses, not one:

- reconcile by **searching for the old value** until it cannot be found (as filed); **and**
- re-derive the baseline from **the last commit of the close**, against a run that can see
  it — the first CI run on the main branch after merge, not the PR's run. Any close that
  commits after merging (record commits, contract pins, bookkeeping — i.e. most closes
  under this kit) invalidates a PR-derived baseline by construction.

The adopter-side record has been corrected to 762 with both causes written down. The other
eight findings are unaffected; the two stale coverage floors, the colliding backlog
identifiers, and every measurement in the step-evidence table stand as reported.

