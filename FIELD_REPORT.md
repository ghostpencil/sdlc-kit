# Field Report — first real run of the kit on an existing codebase

**Project:** TFit Foundation Q&A App (Python, ~240 KB app code, live in production)
**Adopted:** 2026-07-19 via `/sdlc-setup`, Existing Project mode
**Run through:** 1 phase (STABILIZATION), 3 slices, 1 whole-arc review, 1 PR merged
**Result:** 7 → 34 tests, mypy 175 → 171, coverage 12.32% → 27.10%, 2 data-integrity
bugs caught that would have shipped.

The process worked. Everything below is a gap found by *using* it — places where the kit
was silent, was wrong, or wrote a rule that nothing enforced. Ordered by how much damage
each one caused.

---

## 1. `/end-slice` contradicts Existing Project mode — CONFIRMED DEFECT

**Severity: high. This is live in the shipped kit right now.**

`commands/end-slice.md` §2 states flatly:

> All steps must be green. If not, fix the failures first (TDD skill rules apply if tests
> change), then re-run. Do not proceed on red. **The typecheck baseline is green — any new
> error is a regression, never an accepted cost.**

`templates/SDLC.template.md` line 48 says the same thing, but *is* aware of the problem —
it carries an HTML comment immediately after:

```
<!-- Existing Project mode: if adopted with a non-green baseline, record the current
     error/failure count here and treat any INCREASE as a regression until the
     STABILIZATION backlog drives it to zero. -->
```

**`end-slice.md` has no such comment and no conditional.** So on any project adopted with
a red type leg — which the README explicitly advertises as supported ("a red gate becomes
your initial STABILIZATION backlog, not a blocker") — the slice-closing command asserts
something false at every single slice.

Confirmed live on this project: `.claude/commands/end-slice.md` is byte-identical to the
kit's, and still says "the typecheck baseline is green," while `spec/SDLC.md` records a
**171-error ceiling**. `spec/SDLC.md`'s own opening rule says "if this file and a command
disagree, this file wins — fix the command." Nobody fixed the command, across three
slices, because nothing surfaced the disagreement.

**Fix:** make the baseline concept first-class rather than an exception.

- `end-slice.md` §2 → "All steps must be green **against the baseline recorded in
  `spec/SDLC.md`**. A green baseline means zero errors; an adopted baseline means the
  recorded count. Any *increase* is a regression and is fixed in this slice."
- Same edit to `end-phase.md` §2 (it defers to `spec/SDLC.md`, which is better, but says
  nothing about counts).
- `sdlc-setup.md` should, in Existing Project mode, **rewrite the command files** to match
  the baseline it just measured — not only the templates. Setup currently instantiates
  templates with placeholders resolved but copies commands verbatim.

**Generalizable lesson for the kit:** the templates are parameterized and the commands are
not. Anything the templates treat as variable (`{{GATE_*}}`, baseline state, main branch)
is hard-coded prose in the commands, and the commands are what the agent actually reads
at slice time.

---

## 2. The kit has no coverage ratchet — and the project invented one badly, three times

**Severity: high. Pure omission; cost two red CI runs and a wrong number in the docs.**

The kit's gate is lint → typecheck → test. There is no coverage concept anywhere — not in
`SDLC.template.md`, not in `GATE_RECIPES.md`, not in the commands. This project needed
one (12% coverage at adoption, and no way to tell whether slices were improving it), so it
built a ratchet from scratch and got the floor wrong **three separate times**:

1. Set to **70** initially — aspirational, would have failed every build from day one.
   Caught before landing. Lesson recorded: *"a 70% floor would fail every build from day
   one and would be switched off within a week, which enforces nothing."*
2. Set to **38**, read off a bare `--cov` (40%) instead of CI's `--cov=.` (16% at the
   time). Red CI.
3. Set to **28**, computed from the local number (29.24%) minus a "~0.3 point offset" the
   project's own `SDLC.md` claimed. The real gap was **2.1 points** (CI: 27.10%). Red CI
   again.

The rule they landed on is worth stealing verbatim:

> **Never compute the floor. Push the branch, read the number CI actually prints, and set
> the floor from that.**

And the meta-lesson, which is the better one:

> **A remembered constant is not a measurement.** That 0.3 came from one observation and
> was then trusted repeatedly. It is the same failure mode as a stale comment.

**Fix:** add a coverage-ratchet section to `SDLC.template.md` and a per-language recipe to
`GATE_RECIPES.md`, encoding:

- Set the floor from the **first CI run**, never from a local number, never from an
  aspiration. Set it just below the real figure.
- Ratchet raises only. Lowering it to make a build pass defeats its only purpose.
- Existing coverage debt is a backlog item, not a merge blocker.
- Measure with the **exact CI invocation** — scoping flags change the number materially
  (`--cov` vs `--cov=.` differed by 9 points here).
- `/end-slice` should prompt: "did coverage rise? if so, raise the floor after CI reports."

---

## 3. A written rule that nothing enforces will be violated, silently, for months

**Severity: high. The single most valuable finding of the whole run.**

`TESTING.template.md` ships a "when mocking is mandatory" table, and this project filled
it in correctly on day one — Google APIs listed, with the reason ("needs
`service_account.json`, absent in CI"). The instantiated `spec/TESTING.md` says, in bold,
**"never call the real service in a test."**

The test suite was calling the live Google Calendar API the entire time.

`tests/test_answer_cache.py::test_suggest_refuses_to_run_ungrounded` called the real
`suggest_items()`, which locally read `service_account.json`, **minted a real OAuth token**,
and hit the Calendar API. It passed in CI only because the credentials are git-ignored and
absent there — so CI took the graceful-degrade branch. **Same pass/fail, different code
path.** The only visible symptom was a coverage discrepancy nobody could explain.

The project's own diagnosis is the lesson:

> `conftest.py` sterilizes `TFIT_DATA_DIR` and nothing else, which is **a half-built
> isolation that reads as complete**. The rule was written and nothing enforced it.

Note the near-miss: `list_events` is a read, so nothing was damaged. But the same seam
covers `insert_event`, and `/calendar/add` is one route away. A future test on that path
would have **written to a real 501(c)(3)'s calendar**.

**Fix:** `TESTING.template.md` should not stop at a policy table. Add a required section:

> ### Making the policy enforceable
> A mock policy that lives only in prose will be violated and the violation will not be
> visible. Your `conftest`/test-setup must make the forbidden thing *fail loudly*:
> - Clear credential env vars and point credential paths at nonexistent files.
> - **Install a socket blocker** so any outbound connection raises with the address it
>   tried to reach.
> - Isolate every data-dir/home-dir seam, not just the obvious one.
> Partial isolation is worse than none, because it reads as complete.

`sdlc-setup.md` should scaffold this blocker as part of test scaffolding, not leave it to
be discovered. This generalizes beyond Python — the shape is "make the harness enforce it,
don't ask people to remember it."

---

## 4. Two environments disagreeing about a number *is the finding* — don't tune the threshold

**Severity: high. Generalizes far past coverage.**

This is the connective tissue between #2 and #3, and it deserves its own entry because the
kit gives no guidance on it at all.

Local coverage and CI coverage disagreed. The project treated the *number* as the problem
and adjusted the floor around it — twice — while the disagreement was actually reporting a
live defect (§3: tests hitting the network). The gap was the symptom; the live API calls
were the disease.

> **When two environments disagree about a measurement, find out why before adjusting the
> threshold.** The disagreement was the finding.

They also landed a good tiebreak rule the kit should adopt:

> **If local and CI diverge, CI is authoritative** — it runs against the clone the deploy
> is built from, without local-only files.

**Fix:** add both to `SDLC.template.md` under CI. The kit currently says "the same checks
run in CI" and stops — it never contemplates the two disagreeing, which on any project
with git-ignored local files is a matter of *when*, not *if*.

---

## 5. Run the whole-arc review even when every slice review passed

**Severity: high — this one is about defending a step the kit already has.**

`end-phase.md` §5 has the whole-arc review. It works. It found **two data-integrity bugs
that three separate clean slice reviews had missed**, both the same shape: a partial write
reported as a total failure, inviting a retry that **duplicates rows in an authoritative,
non-regenerable store**. One would have put a second row for a single regulatory filing
cycle into a nonprofit's compliance history.

One of the two was a regression *introduced by slice #1* and reviewed clean at slice #1's
own review.

Why the slice reviews couldn't see it: **each slice review looks at one layer.** Slice #1
was the data store, #11 the frontend, #12 the dispatch layer. The bug lived in the
relationship between them.

The risk is that a team with three green slice reviews treats the arc review as
box-ticking and skips it. Nothing in `end-phase.md` argues for its value.

**Fix:** add a line to `end-phase.md` §5:

> Run this **even when every slice review came back clean** — especially then. Slice
> reviews see one layer each; arc-level bugs live in the seams between slices and are
> invisible to all of them. On this kit's first production run, three clean slice reviews
> were followed by an arc review that found two data-integrity bugs.

---

## 6. The propagation checklist — the same bug shape recurred in all three slices

**Severity: medium-high. A repeatable checklist the kit is missing.**

Every one of the three slices changed error propagation, and every one introduced
follow-on bugs that review (not process) caught:

- **Slice #1** made the data layer raise instead of swallow → **created new crash paths in
  every unguarded caller.** Four call sites went from degrading gracefully to aborting the
  HTTP connection.
- **Slice #11** made the frontend helper throw → a mid-loop throw left earlier writes
  saved but invisible; browser-native state (checkbox, `<select>`) had already mutated
  before any JS ran; and a board-refresh inside the write's `try` reported *successful*
  writes as failed.
- **Slice #12** caught a dispatch exception → **destroyed the diagnostics.** The escaping
  exception used to reach `socketserver.handle_error`, which printed a full stack trace.
  A naive catch would have handed the owner a response and taken the operator's traceback
  away — trading one blind spot for another and calling it a fix.

Three formulations worth encoding as a review checklist:

> - **Making a call raise is not done when the raise is correct; it is done when every
>   caller's control flow has been re-read.** A propagation change must be paired with a
>   caller audit.
> - **The mirror question:** when you stop something from raising, ask *what did I stop
>   seeing?* Not just *who now crashes?*
> - **A status code is a claim about fault.** 400 was a claim this code couldn't make —
>   the handler parses data read from the *database*, so corrupt stored data raises on a
>   perfectly valid request.

**Fix:** add an "error-propagation changes" block to `end-slice.md` §3 triage, and to the
code-review guidance. This is the single most repeated defect class in the run — 3 for 3.

---

## 7. `spec/PROJECT_INDEX.md` collided with an existing `PROJECT_INDEX.md`

**Severity: medium. Existing Project mode should catch this; it didn't.**

The kit hard-codes `spec/PROJECT_INDEX.md` as the source of truth. This repo already had a
root `PROJECT_INDEX.md` — a large, load-bearing document covering archive state and the
production deploy runbook, with its own rule in `CLAUDE.md` that it "wins" for status.

Two files, same name, opposite authority, one directory apart. The project had to add
warning callouts in **three** places to manage the confusion:

- `spec/PROJECT_INDEX.md` opens with a ⚠️ block explaining it is not the root one
- `spec/SDLC.md` bookkeeping section repeats it
- root `CLAUDE.md` repeats it a third time, in bold, with the note "⚠️ **`spec/PROJECT_INDEX.md`
  is a different file from the root `PROJECT_INDEX.md`**"

Three redundant warnings is what a naming collision costs, and it is still a live trip
hazard for every fresh session.

**Fix:** `sdlc-setup.md`, Existing Project mode, should glob for `PROJECT_INDEX.md`,
`INDEX.md`, `STATUS.md` anywhere in the repo and, on a hit, **halt and offer a rename**
(`spec/SDLC_INDEX.md` or `spec/SDLC_STATUS.md`). The kit already greps for leftover `{{`
as an exit check — this is the same class of check and much higher value.

---

## 8. The kit assumes it governs the whole repo

**Severity: medium.**

This repo is roughly half application code and half a content archive with its own
non-code workflow (writing document summaries, cataloging, a manual production upload).
TDD does not fit content work, and running `/next-slice` to process emails would be
nonsense.

The owner had to make and record an explicit scope decision — "this process governs the
Python application code only" — and then repeat it in `spec/SDLC.md`, `spec/PROJECT_INDEX.md`,
and root `CLAUDE.md`. The kit never asks.

Mixed repos are common: app + docs, app + infra, app + data pipeline, monorepo packages.

**Fix:** `sdlc-setup.md` should ask, in both modes: *"Does this process govern the whole
repo, or a subset? What is explicitly out of scope?"* Then write the answer into
`SDLC.template.md` via a new `{{SDLC_SCOPE}}` placeholder, right below the title where it
cannot be missed.

---

## 9. Nothing prompts you to record new gate dependencies

**Severity: medium. Small fix, real cost.**

Slice #11 introduced a test layer that extracts browser JS from a page string and executes
it under **node**. That made `node` a hard dependency of `python -m pytest` — a contributor
without node cannot run the gate green, locally, at all.

CI was updated (`actions/setup-node@v4`). `CLAUDE.md` was not. It sat in the backlog as
item #29 — *"one line in `CLAUDE.md`'s gate section would save the confusion"* — because
nothing in `/end-slice` asks whether the slice changed what the gate needs.

**Fix:** add to `end-slice.md` §5 bookkeeping: *"If this slice added a tool, runtime, or
service the gate now requires, add it to the gate section of `CLAUDE.md` and to CI in the
same commit. A gate dependency discovered by a contributor's red run is a documentation
bug."*

---

## 10. A baseline count can stop measuring without ever increasing

**Severity: medium. Subtle and genuinely dangerous; worth a warning in the template.**

The kit's baseline rule — "any *increase* in the error count is a regression" — has a hole
this project fell into. Slice #1 added `@_store_guard` to 20 handlers. The decorator is
**unannotated**, so mypy types all 20 decorated handlers as `Any`.

The count held steady at 175. It held steady because the checker had stopped looking.

> **A ceiling that stops measuring is worse than a high one.**

The count is a proxy, and the proxy can be silently degraded by a change that never trips
the rule. This is exactly the shape of Goodhart's law applied to a gate metric.

**Fix:** note it in the baseline section of `SDLC.template.md` — when a slice adds a
wrapper, decorator, or generic boundary, verify it is **typed**, or the count stops
covering everything behind it. A flat count across a large change is itself worth a look.

---

## 11. Testing lessons the kit's TDD references should absorb

**Severity: medium. All three are sharp, general, and cheap to add.**

For `templates/TESTING.template.md` and `skills/tdd-references/tests.md`:

1. **A test that asserts "returns empty on error" is usually pinning a bug, not a
   behavior.** Prefer asserting that the error propagates. This project earned it: a
   production outage (empty to-do board) was a missing dependency swallowed by
   `except duckdb.Error: return []`. A mocked DB would have returned rows happily and the
   suite would have stayed green through the entire outage.

2. **Tests must fail, not skip, when a required tool is absent.** *"A silently-skipped test
   is the same false green the slice removed."* The kit says nothing about skip discipline,
   and conditional-skip is the default idiom in most test frameworks.

3. **Asserting on a string that contains logic pins wording, not behavior.** The bug that
   created this project's node test layer was *a correct value being computed and then
   dropped* — which no text-containment assertion can see. Generalizes to any
   template/codegen/embedded-source test.

Also worth a line: a review-written test can pin a *plausible-sounding rule the codebase
has already decided against*. One test here asserted "no audit row on rejection" — but the
audit layer already mapped failures to `action="fail"`, so the test would have made one
event produce two different histories. It was inverted in review. **Check a new invariant
against what the system already does, not against what sounds right.**

---

## 12. Auditing a pattern by string match will miss instances

**Severity: low-medium. One line in the code-review guidance.**

The silent-except sweep matched `except duckdb.Error:` literally and **silently missed 7
sites** written `except (duckdb.Error, ValueError, TypeError):`.

> When auditing a pattern, enumerate by **AST or by method**, not by exact string.

The failure mode is nasty because the sweep reports success — it found 26 and fixed 26,
and nothing indicated the denominator was wrong.

---

## 13. Small additions worth folding in

- **Acceptance review of error paths needs a safe technique.** To make writes fail without
  damaging an authoritative store: **stop the server.** The page stays live, its writes go
  nowhere, and that exercises the identical failure paths with zero risk to real data.
  `end-phase.md` §3 could offer this pattern — "prefer breaking the *connection* over
  corrupting the *data*" generalizes to most acceptance passes on error handling.

- **`PROJECT_INDEX.template.md` has nowhere to put environment gotchas.** This project
  bolted on a whole section for a platform trap (NTFS Hidden attribute making
  `open(path,'w')` raise `PermissionError` on 371 files — which would have crashed the next
  state-file write). Valuable, recurring, and it had no home. Add an "Environment gotchas"
  heading to the template.

- **The template's phase-history table has no adoption row convention.** This project
  invented one (`| — | **SDLC adopted** | pre-SDLC | ... |`) and back-filled pre-SDLC rows
  from git history, marked as "recorded so the arc of the project is visible, not because
  they followed this process." That is a good pattern for Existing Project mode; make it
  the documented default.

---

## 14. The kit has no upgrade path — adopting projects are pinned at adoption day

**Severity: high, despite its position in this list.** It caused no damage on this project
*yet*, so it sorts late under "damage caused" — but it is the item that blocks delivery of
every other fix in this report.

`README.md` covers installation completely: clone the kit into the target repo,
`rm -rf sdlc-kit/.git` so it is plain files, copy `sdlc-setup.md` into `.claude/commands/`,
run `/sdlc-setup`. It says **nothing about updating an already-adopted project.**

There is no mechanism, documented or scripted, to pull kit improvements into a project
that adopted it three months ago. Every adopting project is pinned to whatever the kit
looked like on its adoption day. Concretely: when the authors fix finding #1, no existing
project will ever receive that fix. They will each keep running a command file that
asserts a false thing, indefinitely, and the fix will only benefit projects adopted after
it lands.

Deliberately stripping the kit's `.git` at install (which is correct — a nested repo would
be worse) is what removes the obvious update route, so the kit owes adopters a replacement
for it.

**Fix:** ship an update command or script alongside `sdlc-setup.md`. Two requirements
learned from this project's file layout:

1. **Diff before overwriting.** All three installed commands here are byte-identical to
   the kit's, so a straight overwrite would be safe *on this project* — but that will not
   hold generally. `spec/SDLC.md` says "if this file and a command disagree, this file
   wins — **fix the command**," which explicitly invites local command edits. A project
   that took that advice would be silently clobbered by a naive copy. Diff, report what
   differs, and let the owner decide per file.
2. **The diff report is valuable on its own.** Surfacing "your `end-slice.md` differs from
   the kit's" is exactly the signal that was missing here for three slices. An update
   script that reports drift is also a drift *detector*, which is worth running even when
   there is nothing new upstream.

Worth noting what the update boundary is: `commands/` and `skills/` are kit-owned and
should track upstream. The instantiated `spec/*.md` files are project-owned and must never
be overwritten — they hold recorded baselines, owner decisions, and project-specific
gotchas. `templates/` only matters at adoption. That split should be stated explicitly, so
an update script has an unambiguous rule about what it may touch.

**Meta-point for the authors:** this gap is the same shape as the report's cross-cutting
theme. The kit is well specified as a *process* and under-built as a *product* — install
is handled, upgrade is not, and drift between the kit and its installed copies is
invisible to everyone.

---

## What worked well — don't regress these

Worth stating, since a report of only gaps misrepresents the run:

- **The five halt points were correctly placed.** No halt felt like rubber-stamping, and
  no unwanted autonomy occurred. The owner made scope, design, acceptance, and merge calls;
  everything else ran unattended.
- **Existing Project mode's honest baselining is the right call.** Recording "175 type
  errors" rather than pretending, and marking the CI typecheck step `continue-on-error`
  with an explicit instruction to delete the flag at zero, kept the gate credible on day
  one. A kit that demanded green would have been abandoned in an afternoon.
- **One slice per session, `/clear` between,** held up across three slices with no context
  degradation.
- **`spec/PROJECT_INDEX.md` as single source of truth is the load-bearing piece.** Every
  fresh session oriented in seconds. Its backlog also became the honest record of
  everything found-but-deferred — 30 numbered items, each with provenance ("Slice review
  2026-07-19", "Whole-arc review, PR #2"). The provenance tags were an unplanned local
  addition and turned out to be the most useful part; consider making them a template
  convention.
- **Deferred-findings discipline worked.** Nothing was silently dropped, and scope creep
  did not happen once across three slices.

---

## Suggested priority for the kit authors

| # | Change | File(s) | Effort |
|---|---|---|---|
| 14 | **Ship an update path (diff-before-overwrite)** — do this first; without it none of the fixes below reach an already-adopted project | new `commands/sdlc-update.md`, `README.md` | M |
| 1 | Fix the "typecheck baseline is green" contradiction | `commands/end-slice.md`, `end-phase.md`, `sdlc-setup.md` | S |
| 2 | Add coverage ratchet + "never compute the floor" | `templates/SDLC.template.md`, `reference/GATE_RECIPES.md` | M |
| 3 | Enforceable mock policy (socket blocker scaffolding) | `templates/TESTING.template.md`, `sdlc-setup.md` | M |
| 4 | "Environments disagree → investigate, don't tune"; CI is authoritative | `templates/SDLC.template.md` | S |
| 5 | Defend the arc review explicitly | `commands/end-phase.md` | S |
| 6 | Error-propagation review checklist | `commands/end-slice.md` | S |
| 7 | Detect `PROJECT_INDEX.md` name collision | `commands/sdlc-setup.md` | S |
| 8 | Ask what's out of scope (`{{SDLC_SCOPE}}`) | `sdlc-setup.md`, `SDLC.template.md` | S |
| 9 | Prompt to record new gate dependencies | `commands/end-slice.md` | S |
| 10 | Warn that a baseline count can stop measuring | `templates/SDLC.template.md` | S |
| 11 | Three testing lessons | `TESTING.template.md`, `skills/tdd-references/tests.md` | S |
| 12 | Audit by AST, not string match | code-review guidance | S |

**The cross-cutting theme, if the authors take only one thing:** every high-severity item
here (#1, #2, #3, #4, #10) is a case of **a rule that was written down but not enforced,
or a number that was trusted but not measured.** The kit is strong at specifying process
and weak at making the process self-checking. The single highest-leverage direction is to
move rules out of prose and into things that fail loudly — scaffolded blockers, commands
that read the recorded baseline instead of asserting one, floors set from observed CI
output instead of remembered constants.
