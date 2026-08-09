# Feature Plan

Kit-development artifact. **Sections §1–§30 (2026-07-19 → 2026-08-03) are retired to
`FEATURE_PLAN_HISTORY.md`, numbering preserved** — a `§N` reference below 31, in this
file or any other document, points there. This file carries what is live: the standing
decisions, the running clocks, and the active work.

Where this plan and the discussion that produced it disagree, this plan wins. Each
batch is sized for one session. Run `/kit-check` before any release this plan produces.

## Standing decisions — do not re-litigate

A digest with pointers; the full record with each decision's evidence is the history
file. Restating a decision here in more detail than the pointer needs would create a
second source of truth, which is its own recurring hazard
(`CRITICAL_GAPS_ANALYSIS.md`).

- **Foundation decisions, 2026-07-19** (§1), and the rejected/reshaped list (§4) —
  notably: execution-model changes ship on evidence; the slice-runner trial closed
  without shipping (§14), and every trial since is pre-registered with a value
  criterion (§5's trial-protocol rule).
- **Ripple lists in plans are incomplete** (§4a) — derive edit maps mechanically at
  build time, never from the plan's own list.
- **SIMP, 2026-08-03** (§16): the surveyor is deleted and the bar for any future
  custom agent is high; the doubles lens stays; R3.7's archival bullet is the safety
  net. The §16 audit regime binds every rule since: **no confirmed catch after two
  releases makes it a deletion candidate.**
- **Brainstorm, 2026-08-03** (§18): batch order was LEG → COP → STD; secure coding
  ships as lenses, not a command; standards ship as interview + conventions + lenses +
  mechanical gate rules, not prose.
- **PORT, 2026-08-03** (§21, §26, §28, §30): build the translation layer; all of PORT
  ships as one release; the kit owns its reviewer — neither `pr-review-toolkit` nor
  `mattpocock/skills` adopted, `pr-review-toolkit` optional and Claude Code only;
  setup emits exactly one instructions file (§23.1's prohibition); `change-simplify`
  and `change-verify` ship **wired** (§30.2).
- **R5 and ENF, 2026-08-05** (§31 below): R5.1–R5.5 approved as defined; the Copilot
  enforcement machinery is **addressed trial-first, not declined**.

## Standing clocks and inputs

**Clocks are counted in field arcs, not releases — owner decision 2026-08-05.** Both
clocks below were originally set in release numbers, and 0.15.0 and 0.16.0 then shipped
on the same day. Applied literally that would have deleted three pieces of machinery for
failing a test they were never given the chance to sit: the evidence each clock demands
is produced by steps that shipped hours earlier, and no adopter had run an arc under
them. A release is something this repo can do twice in an afternoon; an arc is the unit
that actually exercises a rule. The denominator was wrong, not the rule — this is the
same defect the field reports keep surfacing, found this time in the audit regime
itself. **The §16 audit regime ("no confirmed catch after two releases") has the
identical flaw and is a standing decision, so it is flagged here rather than rewritten:
it wants the same re-denomination whenever it is next opened.**

- **STD's audit clock — two field arcs from 2026-08-05** (§22, §31.6): the audit ran at
  its 0.15.0 deadline — no lens catch, and no evidence the lenses *activated* in the one
  arc of exposure, which the pre-R5.6 records could not distinguish from "ran and caught
  nothing". R5.6's step-evidence sweep now produces the per-step catch record at source,
  so the next two arcs are a deadline with real evidence behind it. No further extension
  on no-evidence grounds once those arcs have run: after R5.6, "no evidence" means "did
  not run". **Arc one banked 2026-08-06 with the evidence table present (§32.3).**
- **`change-simplify` and `change-verify` — two field arcs from 2026-08-05** (§30.4): a
  confirmed field catch each, or deletion candidates. R5.1 (shipped 0.15.0) exists partly
  to give `change-verify` a slice-level path to one, and had no arc of exposure before
  this clock was re-denominated. **`change-verify`'s catch landed in arc one, at slice
  level, 2026-08-06 (§32.3) — its clock is satisfied; `change-simplify` has one arc
  left.**
- **R3.8's aging rule** — §16 contingent keep, waiting on R4.6's writer producing
  friction entries to age.
- **Standing input:** a TFit field report (Phase 07), whenever it arrives.
- **The Copilot bench is still standing** (§29.3): fixture repo
  `D:\AICourse\copilot-ci-test`; `pr-review-toolkit` installed on the owner's Copilot
  CLI; neither is tracked, reversal steps recorded there. ENF's trial runs on it.

---

## 31. Sixth field report and R5 — triaged 2026-08-05

Filed as `sdlc-kit#3` with the retro artifact attached in a comment. Two firsts: the
first report from a **second adopter** (`ai-news-dashboard`, Phase 01, merged
2026-08-05), and the first from a **Copilot CLI adoption** — kit 0.14.0, the PORT batch
getting its first field exercise. Four findings. The owner additionally supplied a
deep-research report (`deep-research-report.md`, 2026-08-05, on enforcing a TDD skill in
Copilot CLI without forking the markdown), processed below as a triage input — its
capability claims are dated research with citations and are **re-verified against the
docs at build time**, per §21's standing rule for anything Copilot. **A first
verification pass ran 2026-08-05, same day as this triage, against GitHub's live docs:
every capability claim §31 relies on held** — no claim from the research report was
hallucinated — and the build-relevant findings are folded inline below with that date.
§21's build-time re-check still applies to anything checked earlier than the build
session.

Bookkeeping this section also carries: **0.14.1 shipped 2026-08-05** (Copilot bootstrap
documented in both READMEs; three `/kit-check` findings fixed — the CHANGELOG is the
record; no plan section existed for it until this note). And `sdlc-kit#2` (the fifth
report), open on the tracker despite shipping as SIMP (0.10.0) + R4 (0.11.0), was
closed 2026-08-05 with a pointer to §16/§17.

### 31.1 The report's theme is the kit's own rule, arrived at independently

The report's cross-cutting theme — *"converting key steps from 'instruction present' to
'evidence required' is the main leverage point"* — is COPILOT.md hazard 4 verbatim
(§30.3: an instruction to *do* is unenforceable; an instruction to produce evidence that
could only exist if it was done is enforceable), measured on the bench 2026-08-03 and
now confirmed from the field two days later by an adopter who had not read the bench
record. The research report supplies the mechanism with citations: on **both** CLIs a
`SKILL.md` is model-visible instruction, not enforcement, and Copilot's skill activation
is relevance-based unless explicitly invoked — a skill that is merely *present* is
guidance, not a step. That mechanism is what findings 1 and 2 are instances of.

### 31.2 The findings, verified against the tree

**Finding 1 — `change-verify` has no slice-level trigger — STANDS, sharper than
filed.** Verified: the skill's own description says "Use before committing a nontrivial
slice and at phase end", and its *How to use* repeats it — but `/end-slice` never names
it (steps: gate → `change-simplify` → `diff-review` → mutation → commit), and
`SDLC.template.md`'s slice loop has no verification step; only `/end-phase` step 2 fires
it. The skill and the process disagree about the skill's trigger — invariant-2-shaped,
with the skill as the second voice. On Claude Code the model can self-invoke from the
description; on Copilot, activation being relevance-based, it demonstrably did not — the
adopter's ingestion break survived S8's close-out and surfaced at phase end, four fix
commits later. **Remedy (R5.1):** an explicit `/end-slice` step in exactly the shape
step 3 already uses for `change-simplify` — **optional but never silent**: run
`change-verify` on a nontrivial slice, or state the skip and its reason in the
hand-back; `SDLC.template.md` slice loop gains the matching step (inv 2 — template
first). §30.2 is the worked precedent for the renumber, and it verified that nothing
outside the plan doc referenced the old numbers — re-verify at build time.

**Finding 2 — RED is written, never evidenced — STANDS, and the template is weaker
than the adopter's copy.** Verified: `next-slice.md` §4.3 says "implement the slice in
small red–green–refactor cycles" — instruction, no artifact. `/end-slice` step 8's
hand-back enumerates quality-pass, review, and mutation outcomes; RED appears nowhere.
And `TESTING.template.md`'s own loop says only "**RED:** Write **one** test targeting
the public interface" — it never says *run it and watch it fail*; the "Run `mvn test`
immediately — confirm the test fails" line the report quotes from the instantiated
`spec/TESTING.md` is the **adopter's** post-drift addition, not the kit's. The kit's
mutation check (step 5, confirmed-catch record: FR4, FR5) proves test *sensitivity*
after the fact; nothing proves red-before-green *ordering*. **Remedy (R5.2), hazard 4's
shape:** the template's RED step becomes "write one test, **run it, and observe it
fail** — the failing run is the evidence"; `next-slice.md` §4 says the observed-red is
recorded as it happens (it cannot be reconstructed at close-out); `/end-slice` step 8's
hand-back gains a RED-evidence line per behavior batch — command, the failing line, exit
code — with **"not observed" stated, never omitted**, same contract as the quality pass.
No state machine, no hook (see 31.3).

**Finding 3 — Copilot model routing and process-state visibility — PARTIALLY STANDS,
as a guidance gap.** Verified: `COPILOT.md` already covers the machinery — setup asks
the owner to map tiers against `/model`, hazard 2 explains why kit files pin no
`model:`, per-agent pinning is documented, `COPILOT_MODEL` exists. What the field run
shows is sharper than the triage first recorded (**corrected 2026-08-05 against the
generated tree**): the adopter's `spec/SDLC.md` records the three `auto` tiers as
"(owner decision, 2026-08-03)" — in the adoption commit itself (`2a006a7`), not a later
edit. The dated-ratification record the remedy first prescribed already existed in the
field, and the routing pain happened anyway (the adopter's friction log, still open:
"owner had to manually override model selection"). A record cannot distinguish an
informed ratification from a rubber-stamped default; the setup-time lever is what the
question *says*, and the operative gap is that no installed file names the moment a
tier choice is executed. **Remedy (R5.3), expanded at the 31.4 halt (owner: the
routing pain was real, not cosmetic):** the kit cannot pin models in the files it
ships (hazard 2, plus dual-CLI portability), so the levers are the
consequence-stating question, the operator, and — pending verification — per-file
pins written at setup time. Four parts, (b) and (c) load-bearing:

- **(a) Setup's Copilot tier question states the consequence, not just the choice.**
  Each tier maps to a named model from the `/model` listing, **or** the owner ratifies
  `auto` for that tier — and the question itself must state what `auto` forfeits:
  process-heavy commands (`/plan-phase`, `/end-phase`, `/end-slice`'s review) may
  route below the work's tier, and the field run shows what that costs. The dated
  record alone is not the fix — the adopter's file already carried "(owner decision,
  2026-08-03)" and the pain happened anyway; a record cannot show whether the
  consequence was understood, so the question must carry it. The gate-recipes rule,
  applied to models: the mapping must match an *informed* decision, or the mapping
  lies.
- **(b) `SDLC.template.md`'s model policy gains the Copilot dialect: routing is
  operator-performed.** On Copilot no installed file routes for you, so the generated
  `SDLC.md` names which commands run at which tier from the recorded mapping and
  instructs the operator to set the model (`/model` in-session, or `COPILOT_MODEL` for
  a scripted run) **before** a High-tier command — `/plan-phase`, `/end-phase`, and
  `/end-slice`'s review at minimum. A tier policy nobody executes is prose; naming the
  moment it is executed is what makes it a step.
- **(c) `COPILOT.md` operator paragraph** — the three levers (`/model`,
  `COPILOT_MODEL`, per-agent `model:` pin for the explore agent), the escalation rule
  from (b), and the caveat that low execution visibility is a CLI property the kit can
  report around but not fix.
- **(d) Build-time verification: does frontmatter honor a *Copilot* model name?**
  Hazard 2's bench run only proved a **Claude** model name is downgraded — it says
  nothing about `model: <copilot-model>` in a skill or agent file. Verify on the bench.
  Doc datum, 2026-08-05: the CLI skills page documents SKILL.md frontmatter as `name`,
  `description`, `license`, `allowed-tools` — **no `model` field**; only the
  custom-agents reference documents `model`. Expect the bench answer to be agents-only,
  which is why (b) and (c) are the load-bearing parts, not this.
  If honored, setup on a **Copilot-only** project may offer to pin the process-heavy
  skills to the mapped tier models — owner-decided at setup, written into the
  *instantiated* copies (a model name is a project fact; the kit's shipped files stay
  unpinned), and explicitly off the table for dual-CLI projects, where one CLI's model
  name is the other's downgrade warning.

The "skills felt like prompts" half of the finding is the mechanism in 31.1 and is
addressed by R5.1/R5.2 and ENF, not by new prose.

**Finding 4 — friction-log status markers unnormalized — STANDS, small.** Verified:
the absorbed-marker convention lives in an HTML comment in `PROJECT_INDEX.template.md`
and in `sdlc-retro.md`'s sweep; no entry *format* is prescribed, so entries are written
without a status and the sweep infers. (The adopter's log carries markers *now* only
because the 2026-08-05 retro added them — its finding 4 states neither entry had one
before the retro; the premise stands.) **Remedy (R5.4):** the template comment
prescribes the one-line shape — `- <date> — <friction> — open` flipping to `absorbed by
retro <date>` — and `/end-slice`'s friction bullet writes that shape. The prescribed
shape must match what the retro sweep already writes when it flips an entry (the
adopter's normalized log is the reference), so prescription and sweep produce one
format, not two. No new rule; a format for one that exists.

### 31.3 The research report — what the kit takes, and what it declines

**Taken (inside R5):** the mechanism and vocabulary of 31.1; the evidence-contract
remedies R5.1/R5.2 are the report's "guidance" layer done in kit house style.

**Taken (as recorded hazards — doc-verified 2026-08-05):** (a) `gh skill
install`/`gh skill update` **inject provenance fields into `SKILL.md` frontmatter** —
confirmed against GitHub's changelog (2026-04-16): the fields are repository, ref, and
git tree SHA, and `update` compares tree SHAs against upstream. An adopter who
"updates" a kit-installed skill that way mutates files `/sdlc-update`'s enumeration and
the provenance regime expect byte-stable; worth one note in `SKILLS.md` (the file that
already tells adopters how skills arrive) and a line in `COPILOT.md`. One sharpening
from the verification: `gh skill` targets six agents **including Claude Code**, so the
`SKILLS.md` note is written CLI-neutral, not as a Copilot hazard. (b) Copilot hook
facts beyond the kit's current `postToolUse` recipe, all confirmed against the hooks
reference: `preToolUse` can deny and **fails closed on command errors but open on
timeouts** (timeouts fail open even for `preToolUse` — the reference is explicit);
`agentStop` can block with an eight-consecutive-block cap, and its input carries a
`stop_hook_active` flag telling a hook it is already in a forced continuation;
`userPromptTransformed` can rewrite the model-facing prompt (mutation-only — it cannot
block). Recorded in `COPILOT.md`'s hook section as dated capabilities — the kit builds
nothing on them yet.

**The enforcement machinery — owner decision, 2026-08-05: address it; do not
decline.** The report's recommended architecture (a wrapper capturing approved seams, a
`preToolUse`/`agentStop` state machine denying production writes until observed red,
sidecar path policy, a counterfactual-red CI check). The triage recommended declining on
three grounds — the F3 slice-runner precedent (§14: execution-model changes ship on
evidence, and a far smaller runner did not survive its own trial), §16's regime (an
enforcement layer whose evidence-contract predecessor has not yet failed), and
counterfactual-red duplicating the mutation check's proven ground. The owner overrode
with a field observation the issue undersold: **the Copilot run of the kit is clearly
weaker than the Claude Code run — skills are treated like prompts — and that is a real
issue to address**, not an escalation to hold in reserve. Decision recorded; the
grounds above survive as *shape* constraints, not as a veto: the machinery is built
**trial-first**, which is what the F3 precedent actually demands — see 31.5.

Two of the triage's technical points stand regardless of disposition:
counterfactual-red stays out (the mutation check owns test sensitivity, with catches on
record), and the report's own rollout ordering (logging-only → warnings → denial) is
adopted as the trial's ramp.

### 31.4 R5 — the batch *(all items owner-approved 2026-08-05)*

| # | Item | Files | Effort |
|---|---|---|---|
| R5.1 | `change-verify` checkpoint at slice close, optional-but-never-silent | `SDLC.template.md`, `end-slice.md`, `SKILLS.md` row | M |
| R5.2 | Observed-RED evidence: template RED step, record-as-it-happens, hand-back line | `TESTING.template.md`, `next-slice.md`, `end-slice.md`, `SDLC.template.md` | M |
| R5.3 | Copilot model routing: explicit tier mapping at setup, operator-performed routing in `SDLC.md`, operator levers in `COPILOT.md`, Copilot-model pin verification | `sdlc-setup.md`, `SDLC.template.md`, `COPILOT.md` | M |
| R5.4 | Friction-log entry format | `PROJECT_INDEX.template.md`, `end-slice.md` | S |
| R5.5 | `gh skill` frontmatter-injection hazard + hook facts (doc-verified 2026-08-05, CLI-neutral note) | `SKILLS.md`, `COPILOT.md` | S |
| R5.6 | Retro step-evidence enumeration sweep: named process steps → evidence in window; feeds the deletion clocks | `sdlc-retro.md` | S |

**R5.6, added at the 2026-08-05 pre-build scrutiny (owner-approved same day):** no
retro sweep enumerates the steps the process names and asks which left evidence in the
window — finding 1 was caught by damage (the ingestion break surviving to phase end),
not by enumeration, and on Copilot, where presence is not activation (31.1),
catch-by-damage is the only detector the retro currently has. The sweep reads
`spec/SDLC.md`'s named steps and reports each skill/lens/check as ran / caught /
skipped-with-stated-reason / no evidence: silent non-activation surfaces by
enumeration instead of luck, and the §22 / §30.4 deletion clocks get their
catch-or-no-catch record produced at the source, rather than re-read kit-side off
field reports. Scope: one sweep bullet in step 2 and one line in the report skeleton,
`sdlc-retro.md` only. Binding on R5.2's build: this sweep reads the records R5.1/R5.2
create, so the observed-RED evidence must persist somewhere durable on disk (the
retro's own prime directive is evidence on disk), not only in the conversational
hand-back — where it lands is R5.2's build decision, to be made explicitly, not by
omission. Lineage: FR2's assumed-denominator theme and FR3's prose-vs-enforced theme,
applied to the retro itself.

Release note for whoever builds this: **the next release is 0.15.0, which is STD's
audit deadline** (§22 — the three lenses and the runtime-standards recipe section each
need a confirmed catch or become deletion candidates). This report is the only field
evidence since STD shipped and records **no lens catch** — one Copilot arc, one adopter.
The audit is owed in the R5 session, and "no catch, one arc of exposure, clock extended
or candidate declared" is an owner decision to present honestly, not a formality. The
0.16.0 clocks (§30.4: `change-simplify`, `change-verify`) are unaffected, though R5.1
exists precisely to give `change-verify` a slice-level path to a field catch.

**Owner decisions at the 31.4 halt, all dated 2026-08-05 — do not re-litigate:**
R5.1 wired (recommended form); R5.2 evidence-required (recommended form); R5.3, R5.4,
R5.5 all approved; R5.6 added and approved at the same-day pre-build scrutiny; the
enforcement machinery **addressed, not declined** — reshaped into ENF below, queued
behind R5 (batches are sized for one session, and R5 now holds six items — if the
session runs long, R5.6 is the item to split out, since nothing else in R5 depends
on it landing in the same release).

### 31.5 ENF — the Copilot enforcement batch *(queued behind R5; trial-first)*

The owner's framing is the scope: on Copilot CLI, a skill is a prompt — presence is not
process. ENF gives the kit's highest-risk steps a deterministic backstop on Copilot,
built in the F3 shape: **pre-registered trial on the bench before anything enters the
installed set.**

- **ENF.1 — scope: two guards, not a TDD operating system.** The field report's two
  High findings name them: (a) **observed-RED ordering** — deny production-file writes
  until a test run has been seen to fail since the last test edit (`preToolUse` on
  `create`/`edit`/`apply_patch` + `postToolUseFailure` observing the test command);
  (b) **premature completion** — `agentStop` blocks while the cycle is red or the gate
  has not run, within the documented eight-block cap; the hook input's
  `stop_hook_active` flag says the guard is already in a forced continuation — read
  it rather than fight the cap. Nothing else from the report's
  architecture: no wrapper interview, no seam capture, no CI check, no CODEOWNERS
  apparatus. Kit-owned sidecar: one hook JSON (`.github/hooks/`) + one small guard
  script + state under `.git/`, template-ized with the same `{{HOOK_*}}` discipline as
  the existing gate hook (inv 1: placeholders taught to setup in the same batch). The
  guard script stays cheap — state reads and writes only, never running the suite
  inline: the field's gate hook runs on a 30 s budget and a hook that times out fails
  open, so a guard that ran the tests would time out, and silently stop guarding, on
  every invocation.
- **ENF.2 — path policy reuses what setup already knows, via one new placeholder.**
  *Corrected 2026-08-05 against the generated tree.* The original claim — the guard's
  implementation/test classification comes from `{{SOURCE_GLOB}}` and `{{TEST_LAYOUT}}`,
  and "cannot classify" is a trial finding — is contradicted before any trial: the
  adopter's instantiated hook classifies with `*.java`, which matches `src/test/java`
  as readily as `src/main/java`, and every `GATE_RECIPES.md` recipe defines
  `SOURCE_GLOB` the same extension-only way. The placeholder answers "should the
  edit-hook fire," where matching tests is harmless; the guard repurposes it for the
  one question it cannot answer. And `{{TEST_LAYOUT}}` is free prose no script can
  consume. The fix keeps ENF.2's instinct — still no new interview: setup already
  *learns* the layout (the adopter's `TESTING.md` states `src/test/java/...` mirroring
  `src/main/java/...`); it just never records it machine-readably. ENF adds a
  test-path case-pattern placeholder to the guard hook, instantiated from the
  `{{TEST_LAYOUT}}` answer setup already collects (inv 1: taught to setup in the same
  batch). A repo whose layout genuinely resists a case-pattern remains a trial
  finding.
- **ENF.3 — the trial, pre-registered before it runs (§13 shape).** Bench:
  `copilot-ci-test` (§29.3, still standing). Criteria must include a **value
  criterion**, not safety only — FR5 finding 8 is the precedent (a trial with four
  safety criteria and no value criterion cannot fail on value). Candidate value
  criterion: on the bench fixture, the guard denies the write in the
  implementation-before-red run and stays silent through a clean TDD run, with a
  false-block rate the owner would tolerate. Ramp per the report's own advice:
  logging-only first, deny second. Verify every hook fact against the docs first —
  R5.5 does this inside R5, so ENF opens with the facts already dated and checked
  (fail-closed on command error, fail-open on timeout, the tool-name trap in
  `COPILOT.md`: hook matchers use `bash`, not `execute`). One fact is named here
  because the whole observed-red mechanism turns on it: does a test command that exits
  non-zero via the shell tool surface as `postToolUseFailure`, or as a *successful*
  tool call whose command failed? **Checked 2026-08-05: the docs do not settle it** —
  the hooks reference defines the events only as "after a tool completes successfully"
  / "with a failure," and two readings of that page support opposite answers. The
  payload shapes constrain the guard either way: `postToolUse` delivers
  `toolResult.textResultForLlm`, `postToolUseFailure` an `error` string — neither a
  structured exit code — so observed-red detection **parses text whichever event
  fires**. Only the bench answers this: the probe run logs *both* events on a
  deliberately failing test command before the state machine is designed, not after.
  A second trial-scope fact, same date: a write matcher on `create|edit|apply_patch`
  does not cover file writes made *through the shell tool*, and the shell tool's hook
  name is itself platform-uncertain (`bash` in the reference's matcher example;
  `powershell` is the builtin observed on 1.0.77). The guard is a cooperative backstop,
  not a security boundary — the trial report says so in those words, and the bench
  discovers the real matcher vocabulary per `COPILOT.md`'s procedure rather than
  trusting either name.
- **ENF.4 — dialect honesty.** The guard is Copilot-dialect (`.github/hooks/`). The
  Claude Code side gets the equivalent decision made explicitly at build time —
  settings.json hooks exist there too — but nothing is assumed portable; a guard that
  runs on one CLI *says so* where `SDLC.md` records the CLI, per inv 15.
- **The owner reads the trial report before anything ships** (§4, the slice-runner
  precedent — this is the step F3 failed, and skipping it because the owner asked for
  the batch would invert the lesson).

### 31.6 R5 built and shipped — 2026-08-05, release 0.15.0

All six items, one session, commit `39dda84`. Build decisions and deltas against 31.4:

- **R5.2's durable-home decision (the one 31.4 required be made explicitly): the
  slice commit body.** The `RED:` lines (one per behavior batch — command, failing
  line, exit code, `not observed — <reason>` never omitted) live in the slice commit;
  `/next-slice` §4 keeps the running record as each red is observed; `/sdlc-retro`'s
  sweep reads them off `git log`. Mode-independent (STABILIZATION has no phase spec,
  which ruled that home out).
- **The commit body grew into the full close-out evidence record** — `quality:`,
  `mutation:`, and `verify:` one-liners beside `RED:` — forced by the pre-release
  `/kit-check`: R5.6's sweep enumerated the quality pass and mutation check with
  nowhere durable to read them, so they would have classified "no evidence" forever.
  Inv-14-shaped extension, applied template-first.
- **R5.3(d) did not run: the Copilot CLI is not reachable from the kit session's
  shell** (owner-shell install, §29.3). Recorded in `COPILOT.md` as
  unverified-pending-bench, dated; no per-file pins ship, the operator levers are the
  mechanism — the outcome 31.4 predicted. The probe joins ENF's bench session.
- **Renumber sweep**: nothing in shipped files referenced the old step numbers except
  one already-stale pointer this batch caught and fixed (`REVIEW_LENSES.md` header
  still said `/end-slice` §3, stale since 0.14.0). `sdlc-update.md` gained the 0.15.0
  transition note — a ripple the 31.4 file list missed and the mechanical sweep found
  (§4a's rule, vindicated again): template changes never reach adopted projects, so
  the note tells the updater the project's `spec/SDLC.md` now disagrees with the
  commands *in the direction that disables the new steps*, until the owner folds the
  template diff in.
- **`/kit-check`**: full 15-invariant pass (five parallel readers + mechanical
  checks); 14 findings, all fixed in the release commit — CHANGELOG 0.15.0 carries
  the headline ones. All four release-workflow gates simulated green before the tag;
  manifest discrimination proven (exactly the 17 edited bundle files changed hash).
- **STD audit at its deadline — owner decision 2026-08-05: extended once to 0.16.0**
  (see *Standing clocks*; the honest finding was "no evidence of activation", which
  pre-R5.6 records cannot distinguish from "ran, caught nothing").
- Bookkeeping: `sdlc-kit#2` closed 2026-08-05 with the §16/§17 pointer.

**Next session opens on ENF** (31.5, unchanged): the bench probe first — log both
`postToolUse`/`postToolUseFailure` on a deliberately failing test command, plus the
R5.3(d) model-pin probe while the bench is warm — then the two guards, logging-only
ramp, pre-registered criteria before anything runs.

### 31.7 ENF bench probes — run 2026-08-05, Copilot CLI 1.0.77, Windows 11

The probes 31.5 pre-registered, run same-day from the kit session (copilot.exe reached
via its WinGet install path; bench-side record and reversal list in the fixture repo's
`ENF_PROBE_NOTES.md`; raw payloads kept as `probe-*.jsonl` there). Five facts, each
load-bearing for the guard design:

1. **The ENF.3 named question is settled: `postToolUseFailure` never fires for a
   failing shell command.** `node test-fail.js` (exit 1) arrived as `postToolUse` with
   `resultType: "success"`. The exit code is recoverable without parsing test-runner
   output: `textResultForLlm` ends with a `<shellId: N completed with exit code M>`
   trailer. The observed-red detector is therefore a `postToolUse` text parse keyed on
   that trailer — cheaper and sharper than expected.
2. **Tool-name vocabulary, measured (supersedes the provenance table's
   plausible-unofficial rows):** shell = `powershell`, write = `apply_patch` for both
   create and edit flows (the UI label "Edit" is not the hook name — the display-name
   trap, confirmed), read = `view`. `edit` and `create` did not fire on the tested
   flows; ENF.1's draft matcher `create|edit|apply_patch` would have worked by its
   third alternative only, and the shipped gate hook's matcher misses shell-tool
   writes exactly as 31.5 warned.
3. **`apply_patch` breaks the toolArgs-is-JSON assumption**: its `toolArgs` is raw
   patch text (`*** Begin Patch / *** Add File: <path>`), so the kit's gate hook —
   which JSON-parses `toolArgs` for a path — falls to its loud no-path branch on
   every `apply_patch` edit and never runs the gate on it. Real 0.15.0 hook-recipe
   defect, found by the probe; the fix (a patch-text path parse) belongs to the ENF
   batch or a hook-recipe patch release, owner's call at the trial halt.
4. **R5.3(d) closed, both halves, as the doc datum predicted: agents yes, skills
   no.** An agent pinned `model: claude-sonnet-4.5` executed on it while the session
   default was `gpt-5.3-codex` (the CLI's own transcript names it:
   `Pin-probe(claude-sonnet-4.5)`). A skill carrying `model:` loads and fires
   normally — the undocumented field does not trip hazard 1 — but the turn stays on
   the session model. `COPILOT.md`'s pending-bench paragraph can now be resolved
   (0.16.0 material); the Copilot-only setup pin offer in R5.3(d) becomes *possible*
   for the explore agent only, and remains off the table for skills and dual-CLI
   projects.
5. **A new environment hazard with field reach: hook `bash` commands resolve against
   the system PATH, and on Windows-with-WSL that is WSL bash** (`system32\bash.exe`),
   where `D:/…` paths do not exist. Observed live, both documented fail modes in one
   errored run: cold WSL start blew the 10 s `timeoutSec` → fail-open (the command
   ran unguarded); warm error → `preToolUse` fail-closed (denied). The kit's shipped
   hook body runs `python` via that same `bash` — on a machine like this one (which
   is also the sixth report's adopter machine) the gate hook's behavior under WSL
   bash is untested and plausibly broken. Needs its own bench check before the ENF
   guards ship; inv 13's proof step is what catches it per-project today.

**ENF's remaining work, revised by the probes:** the guards' event surface is
`preToolUse`/`postToolUse` only (drop `postToolUseFailure` from ENF.1's design); the
write-guard matcher must cover `apply_patch` with a patch-text path parse and treat
shell-tool writes as out of scope honestly (cooperative backstop, not a boundary);
guard scripts must be WSL-bash-safe (or the hook recipe grows a bash-flavor detection
note). Trial criteria pre-registration (ENF.3) is still owed before the guards run.

### 31.8 ENF trial protocol — pre-registered 2026-08-05, before any guard ran

**Written before the guard code existed**, per §5's trial-protocol rule and §13's
shape. Bench: `copilot-ci-test`, Copilot CLI 1.0.77, hooks under WSL bash (31.7.5).
The trial runs **logging-only**; deny is a separate later ramp step, taken only if the
criteria below hold, and nothing enters the kit's installed set until the owner reads
the trial report (§4, the F3 step).

**The two guards under trial (ENF.1's scope, revised by 31.7):**
- **G1 observed-RED write guard** — `preToolUse` on `apply_patch`: parse the touched
  paths out of the patch text; a production-source write is a violation unless a
  failing test run has been observed since the last test-file edit (`postToolUse` on
  `powershell` watches test commands and records red/green off the
  `<shellId … exit code N>` trailer). State: marker files under `.git/enf/`, mtime
  ordering. Bench path policy (ENF.2's case-pattern, bench values): `test*.js` = test,
  other `*.js` = production, everything else exempt.
- **G2 premature-stop guard** — `agentStop`: would-block when no green test run has
  been observed, or the latest observed run is red; stands down unconditionally when
  `stop_hook_active` is true.

**Value criteria (FR5 finding 8: a trial without one cannot fail on value):**
1. **V1 — catch:** a scripted implementation-before-red run (session told to add a
   production function without tests) produces a logged G1 violation naming the file.
2. **V2 — stop-catch:** that same run ends with G2 logging would-block (no green
   observed).
3. **V3 — silence on clean TDD:** a scripted strict-TDD run (failing test written and
   observed red, then implementation, then green) produces **zero** G1 violations and
   a clean G2 at stop.

**Safety criteria:**
4. **S1 — false-block rate: zero** on the bench fixture. Any G1 violation logged in
   the clean run is a false positive and fails the trial (the owner-tolerated rate for
   a fixture this small is zero; a real repo's tolerance is a ship-time decision).
5. **S2 — cheap enough to not fail open:** every guard invocation completes well
   inside `timeoutSec` (30 s) on warm runs; the guard never runs the suite inline.
   Measured from hook-log timestamps.
6. **S3 — logging mode is inert:** guards always exit 0 in logging mode; no tool call
   is denied and no stop is blocked during the trial (the WSL fail-closed incident in
   31.7.5 is the specimen this guards against).
7. **S4 — reversible:** deleting the guard hook file and `.git/enf/` restores the
   bench; verified by a post-trial session with no guard artifacts in its transcript.

**Decision rule, fixed now:** all seven → the deny-ramp may be proposed to the owner,
with the trial report. Any V-criterion fails → the guard design is wrong, back to
31.5. Any S-criterion fails → logging mode itself is not safe enough to ship in any
form; ENF halts on that evidence. Known accepted limits, stated up front: shell-tool
writes are invisible to G1 (cooperative backstop, not a boundary); state is
repo-scoped, not session-scoped (a trial finding if it bites); G2's "green observed"
accepts any green test run, not specifically the full gate (bench fixture has one
suite; the distinction is a ship-time design point).

### 31.9 ENF logging-mode trial — run 2026-08-05, same day: ALL SEVEN CRITERIA MET

Guards built after 31.8 was committed (`4928fa9` precedes the guard code, provably).
Offline first: a 12-case unit pass drove every state transition with the *captured
probe payloads* before any live session — every verdict as expected, including
red-goes-stale-on-test-edit and the exempt-file no-op. Then live, on the bench:

- **V1 met** — implementation-before-red run: `VIOLATION production write without
  observed red: payments.js` (`.git/enf-runA.log`).
- **V2 met** — same run's close: `stop: WOULD-BLOCK — no green test run observed`.
- **V3 + S1 met** — scripted strict-TDD run: test-edit → RED observed (exit 1) → OK
  production write → GREEN → `stop: clean`. **Zero violations, zero false positives**
  (`.git/enf-runB.log`).
- **S2 met** — every guard invocation 31–88 ms against the 30 s budget; the guard
  reads and writes marker files only.
- **S3 met** — nothing denied, nothing blocked, in any run.
- **S4 met** — hooks renamed away + state deleted → clean session, no guard artifact
  recreated; hooks restored after.

Facts the trial added to the record (each would have bitten the shipped version):

1. **Patch paths arrive in both forms** — absolute Windows (`D:\…\payments.js`, run
   A) *and* repo-relative (`payments.js`, run B). Classification must normalize to
   the basename; fixed between runs A and B (disclosed: run A's verdict predates the
   fix and is unaffected — the fix touches test-file classification only).
2. **`agentStop` fires in `-p` mode**; payload measured: `sessionId`, `cwd`,
   `transcriptPath`, `stopReason: "end_turn"`, snake_case `stop_hook_active`.
   `sessionStart`/`sessionEnd` also exist and fire. (The run-A "agentStop missing"
   scare was a harness artifact: piping `copilot -p` through a head-style filter
   kills the CLI before its stop hooks run — recorded on the bench as a hazard.)
3. **The guard depends on `jq`** (present in this bench's WSL) — a ship-time
   dependency question for the template, alongside 31.7.5's WSL-bash hazard.

**Per the decision rule, the deny-ramp may now be proposed — and is. Owner halt:**
the report is above; the options are (a) ramp the bench guards to deny (next unknown
to measure: `preToolUse`'s deny output schema in practice, plus G2's real block
behavior and the 8-block cap), (b) skip to template-izing for the kit with deny
unproven, or (c) stop at logging. Recommendation: (a) — the report's own rollout
ordering, and deny is exactly the half the field problem needs (31.3: skills treated
as prompts). Nothing enters the installed set before the ramp's own results are read.
**Owner decision 2026-08-05: (a), ramp to deny.**

### 31.10 Deny-ramp protocol — pre-registered 2026-08-05, before any deny code ran

Deny is a flag file (`.git/enf/deny-enabled`); absent = logging mode, unchanged. Two
schema discoveries come first, each its own scripted run: the `preToolUse` deny
output as the CLI actually honors it, and the `agentStop` block output ditto —
neither is fully documented, so the probe tries the documented/plausible shape and
reads the transcript for whether it took effect (a denial that does not deny is the
failure mode being hunted).

**Criteria:**
- **D1 — deny catches:** the implementation-before-red run has its production write
  **actually denied** (transcript shows the denial with the guard's reason), and the
  session visibly reacts to the feedback rather than silently ending.
- **D2 — stop blocks:** with no green observed, session close is blocked at least
  once with the guard's reason; on a forced continuation (`stop_hook_active` true)
  the guard stands down — the 8-block cap is never hit by the guard's own doing.
- **D3 — zero false denials:** the clean strict-TDD run completes with no denial and
  no stop block.
- **D4 — no lockup:** every denied session ends (possibly after reacting); no
  unbounded deny loop. Watched live; the runs are `-p` scripted, so a hang is a
  timeout, which fails this criterion.
- **D5 — no error-denials:** no "hook errored" denial appears in any ramp run (the
  31.7.5 specimen); the guard script's own failure must not become a spurious deny.
- **D6 — reversible:** deleting the flag file returns the bench to logging mode,
  verified by re-running the violation prompt and seeing log-only behavior.

Decision rule: all six → ENF's build phase (template-izing, the `{{HOOK_*}}`
discipline, ENF.4's dialect decision, the apply_patch gate-hook fix) may be proposed;
the owner reads this ramp's report first. Any failure → recorded, and the guard
ships logging-only or not at all — a deny that cannot be trusted is worse than a log
line, because it reads as enforcement.

### 31.11 Deny-ramp report — run 2026-08-05: five of six clean; D3 failed once,
### fixed, and passed on re-run — the disposition is the owner's

**Schemas, both confirmed on the bench:** `preToolUse` deny is
`{"permissionDecision":"deny","permissionDecisionReason":…}` — the transcript shows
the guard's message verbatim and the write did not happen. `agentStop` block is
`{"decision":"block","reason":…}` — the session continued under forced continuation
and the next stop arrived with `stop_hook_active: true`, on which the guard stood
down; the 8-block cap was never approached.

- **D1 met, and the thesis demonstrated:** told "do not write tests", the session was
  denied, wrote a test, was denied *again* for implementing before running it (the
  guard enforced ordering, not presence), ran the test, observed red, and got the
  write through. Enforcement converted an anti-TDD instruction into a red→green
  cycle. (Evidence: transcript of session `4c2201d8`, quoted in-session; its guard
  log was consumed by the next run's reset — a bench-hygiene lesson, noted.)
- **D2 met** — one block, one forced continuation, stand-down on the flag.
- **D3 FAILED on its first run, as pre-registered:** the session ran
  `node test-negate.js; Write-Output "EXIT_CODE=$LASTEXITCODE"` — the exit-code
  trailer reflects the *compound*, so a red run recorded a false **GREEN** (which
  could also silently un-block G2), and the next clean write was denied. Detector
  fixed: only bare single-command test invocations count as observations; compounds
  log loudly and are not counted; the deny message teaches the bare-command remedy.
  Fix unit-tested against the captured defect payload, then **the D3 re-run passed
  clean** — zero denials, zero blocks (`.git/enf-runD3-retry.log`).
- **D4, D5 met** — every session terminated (the deny session took 1m36s and ~4×
  a clean run's credits, the price of introspection); no hook-error denials.
- **D6 met** — flag removed, same violation prompt: log-only, write proceeded
  (`.git/enf-runD6.log`).

Ship-relevant observations beyond the criteria: the session **read the guard's own
source** to learn the recognized test-command format — it complied, but it could as
easily have touched the state files; "cooperative backstop, not a boundary" is now
observed fact, not caveat. It also deleted its guard-satisfying test afterwards as
"temporary" — enforcement produces the red, not the conviction; the kit's R5.2
commit-body evidence is what makes that deletion visible. And `node .\test-x.js`
is invisible to the command pattern (the `.\` prefix) — ship-time pattern work.

**Owner decision owed (the rule's letter vs its intent):** §31.10's decision rule
says any failure → logging-only. D3's failure was real, its cause identified, the
fix unit-tested and clean on re-run — whether a fixed-and-repassed criterion counts
as met is not the builder's call. Option A: accept the re-run, proceed to proposing
ENF's build phase. Option B: hold the guards at logging per the rule as written and
let a future field arc argue for deny.

**Owner ruling, 2026-08-05: Option A — the re-run is accepted.** The failure did its
job (a state-corruption defect caught and fixed pre-ship). Deny mode is
trial-proven; **the next session opened on ENF's build phase, recorded in §31.12** — template-izing
the guards (`{{HOOK_*}}` discipline, inv 1 placeholders taught to setup in the same
batch), ENF.4's Claude-Code-dialect decision, the `apply_patch` gate-hook path-parse
fix (31.7.3), the `.\`-prefix and command-pattern work, and the jq / WSL-bash
dependency questions (31.7.5, 31.9.3) — all of it returning to the owner before
anything enters the installed set, per 31.5's standing rule. Bench state: guards
live in **logging mode** (deny flag removed by D6; recreate `.git/enf/deny-enabled`
to re-arm), fixture drift and reversal steps recorded in `ENF_PROBE_NOTES.md`.


### 31.12 ENF build phase — built 2026-08-05, awaiting the owner's read before release

Everything §31.11 listed is built and proven offline. **Nothing is released**: `VERSION`
still reads 0.15.0 and `MANIFEST.sha256` is deliberately not regenerated, because the
manifest must be regenerated in the release commit (inv 10) and the release is the
owner's call. The shipped files below are the halt §31.5 pre-registered.

**The guards, template-ized.** `templates/tdd-guard.template.sh` +
`tdd-guard.template.json` → `.github/hooks/sdlc-tdd-guard.{sh,json}`, offered (never
imposed) at `sdlc-setup.md` New-mode step 6, logging-mode-only at install. Named for the
adopter, not for us: "ENF" and `.git/enf/` were kit-batch vocabulary and are gone —
state now lives in `.git/sdlc-tdd/`. Four changes the bench version could not have
survived shipping:

1. **The hook JSON carries no absolute path.** The bench hardcoded
   `/mnt/d/AICourse/copilot-ci-test`, which is correct for one machine and broken for
   every teammate who clones the repo. A committed hook file must work for all of them,
   so the JSON now derives the repo root from the payload's own `cwd` and translates
   path flavour (`D:\…` → `/mnt/d/…` → `/d/…`, first one that exists). Pure `sed`/`tr`,
   no interpreter, so it survives a hook shell with no python. This also removed a
   placeholder rather than adding one.
2. **`jq` is gone**; the guard parses with `python`, matching the gate hook's existing
   and deliberate choice (`GATE_RECIPES.md`: python is the likelier of the two, and this
   development machine has python and no jq — confirmed again this session). 31.9.3's
   ship-time dependency question is closed in the direction the kit had already chosen.
3. **The test-command pattern keys on the runner, not on a filename.** The bench matched
   `node test…` as adjacent words and was blind to `node .\test-x.js`; `*pytest*`-shaped
   patterns spanning runner and `test` match every invocation form. That is the
   `.\`-prefix item, fixed generically rather than by special-casing a prefix.
4. **Observations are session-scoped** (new, and unproven live): a `sessionId` change
   clears them, so yesterday's red cannot license today's write. 31.8 listed repo-scoped
   state as an accepted limit "if it bites"; it was cheap to close, and it is flagged
   here precisely because the bench never exercised it.
5. **A path containing a space is one path.** Both the bench guard and this rewrite's
   first draft iterated the patch paths with `for p in $PATHS`, which word-splits, so
   `src/my module.py` became two files and matched neither pattern — a production write
   that classified as exempt and passed the guard silently. Now a `while IFS= read -r`
   loop over a heredoc (not a pipe, which would put the accumulator in a subshell). Found
   by the same reading pass that found the inv-5 defect below, not by the tests, which is
   the honest provenance: the case was written after the fix, and the mutation that
   restores `for p in $PATHS` is what makes the case worth having.

**The `apply_patch` gate-hook defect (31.7.3) is fixed, and it was worse than recorded.**
The old body JSON-parsed `toolArgs` unconditionally; on `apply_patch` — the only write
tool that actually fires on 1.0.77 — the parse throws, so **every edit** fell to the
loud no-path branch and the gate never ran once. Demonstrated both directions against
the captured bench payload: shipped template says "gate did NOT run", fixed template
lints and reports the error. The fix parses the patch text, handles multi-file patches
(previously one path only), and skips `Delete` headers. It keeps the loud branch for
genuinely unrecognisable payloads — that honesty was the one thing the old body had.

**ENF.4 decided: the guards ship Copilot-only, and the Claude Code port is deferred, not
declined.** Claude Code has the matching events, which is what makes the port look like
translation. It is not. Checked against the Claude Code hooks reference 2026-08-05: the
`PreToolUse` deny shape and `Stop` block shape are documented, but **the two facts the
guard mechanism actually turns on are not** — what `PostToolUse` receives for a Bash
call (no input example; no statement of whether an exit code is available or in what
form) and which `tool_input` field holds the path for `Edit`/`Write` (no schema
documented for either). Also unstated: whether Claude Code's Stop input carries
`stop_hook_active`, whether a block cap exists, and whether a timed-out `PreToolUse`
fails open or closed. That is precisely the position Copilot was in before §31.7, and
§31.7 is the reason the Copilot guards work — the exit code turned out to arrive as a
*text trailer*, which nobody would have predicted from documentation. Writing the port
from those gaps ships a guard whose failure mode is silence into the CLI where the kit's
users would trust it most. The port is a future batch that opens with its probe run.
Two Claude-side facts banked for it: hooks get `$CLAUDE_PROJECT_DIR`, and the Windows
shell is stated (Git Bash, per-hook `"shell"` key) rather than inherited from `PATH` —
so the port needs no self-locating prelude, and the WSL hazard is Copilot-specific.

**The WSL hazard (31.7.5) became a setup step, not a note.** A hook runs in the shell the
CLI resolves, not the one you type in, and on Windows-with-WSL that has been measured to
be WSL bash — where the project's paths and its whole toolchain are absent. `GATE_RECIPES.md`
gains *The hook environment — measure it, do not assume it*: a one-line probe run **from
the CLI's own session**, read for which shell answered, whether `python` resolves there,
and whether the project's own lint command runs there, resolving a new
`{{HOOK_ENVIRONMENT}}` in `spec/SDLC.md`. This is inv 15 turned on the kit itself — the
process specified checks and was silent about the environment the checks would run in.

**Proof, because a rewrite that was never run is the defect this kit exists to find.**
Both artifacts got a re-runnable check at the root (`tools/`, inv 12 — never inside the
bundle), and both are green:

- `tools/gate-hook-check.py` — 13 cases over the real payload shapes, every silent case
  also run dirty so silence means something.
- `tools/tdd-guard-check.py` — 24 cases driving every state transition, **then six
  mutations of the guard, each of which the suite must catch.** All six caught: drop the
  compound-command check, drop the session reset, deny on the guard's own failure,
  classify by source glob before test pattern, never stand down on `stop_hook_active`,
  and word-split the path list. The mutation pass is the load-bearing half; the unit
  pass alone would have proved only that the guard agrees with itself. Neither count is
  written in prose — both are derived at run time, because a hardcoded "22 cases" header
  had already gone stale against 24 within this session (inv 14, in miniature).

**One invariant-5 defect caught in this batch's own output, by reading rather than by
running.** The guard script's header comment pointed at `reference/GATE_RECIPES.md` for
the hook-environment probe — and the guard is an *installed* file, while the kit folder
is explicitly optional after setup. Exactly the defect inv 5 exists for, introduced by
the same session that was writing the probe. Fixed: the header now points at
`spec/SDLC.md`, which setup does install, and carries the one-line re-measure command
inline. Worth recording because it is the second time a pointer written from inside the
kit repo assumed the kit repo would still be there.

**Two things an update cannot deliver, both now stated at the halt** in `sdlc-update.md`
and the root README (inv 8, kept in step): the instantiated gate hook is project-owned,
so the `apply_patch` fix reaches an adopted Copilot project only as a changelog entry the
owner re-applies by hand — until they do, their edit-time gate has never run — and the
guards are offered by an update, never installed unasked, with the logging ramp and the
proof step non-skippable just because it is an update.

**Owner decisions owed before release:** (a) ship the guards as an *offer* in setup, as
built, or hold them out of the installed set for another arc; (b) whether the
session-scoping change (unproven live) ships now or waits for a bench re-run; (c) the
release itself — `VERSION` → 0.16.0, `CHANGELOG`, and the manifest regenerated in that
same commit, with `/kit-check`'s full pass before the tag.
*(a) and (b) were both ruled on the same day — see §31.14; (c) is still open.)*

### 31.13 The dependency audit — owner question 2026-08-05, and what it turned up

**The question:** does the kit impose requirements beyond Copilot CLI's own? Asked
before the release decision, and the honest answer was yes, in a place nobody had
written down.

**The finding, and it predates ENF.** The edit-time hook parses its JSON payload with
`python -c` — **in both dialects**, `settings.template.json` as well as the Copilot one,
since the hook shipped. `GATE_RECIPES.md` mentioned it in a note offering a hand-edited
`jq` substitute; the Prerequisites section never listed it; and the root README's FAQ
answered **"Does this require Python? No."** That answer is true of the *gate commands*
(language-agnostic, per-project) and false of the *hook implementation*, which is what
an adopter reads it as. A claim true about one thing, stated as though it covered
everything — the same defect shape the field reports keep finding, this time in the
kit's own front door. ENF's guards then added a third `python` call site with no
fallback at all, making it worse.

**`node` is not a free substitute, which is the interesting part.** The intuition is
that Copilot CLI is a Node application, so `node` must be present. Checked against
GitHub's install docs: Copilot CLI's stated prerequisites are a Copilot subscription and
PowerShell 6+ on Windows, and **four of its five install methods** (WinGet, Homebrew,
curl script, direct download) are standalone binaries. The bench machine's own install
is a single 159 MB `copilot.exe` with no `node` beside it. Only `npm install -g` implies
Node. So swapping python for node trades one absent interpreter for another.

**Owner decision 2026-08-05: ship both dialects with run-time detection**, plus three
fixes. Detection rather than an interview question, for an inv-15 reason worth keeping:
asked which interpreter to use, an owner answers for *the shell they type in*, while the
hook runs in a different one. A configured parser is a claim about the wrong
environment; a run-time probe asks the only shell whose answer counts. Order is
`python`, `python3`, then `node`; with none, every hook says so on each edit rather than
passing quietly.

**A latent Windows defect found while testing the two against each other.** Python's
`print()` emits CRLF on Windows; node emits LF. The hooks split the parser's output with
`sed` and compare fields to literals, so a stray `\r` makes `[ "$st" = "ok" ]` false and
sends the hook down its "could not run" branch on **every edit**. It has never bitten
because Git Bash's MSYS `sed` silently strips CR — but GNU sed under WSL bash does not,
and WSL exposes Windows `python.exe` through PATH interop, which is exactly the
environment 31.7.5 flagged. Both hook bodies and the guard now pipe through
`tr -d '\r'`. Demonstrated mechanism, not a confirmed field failure: no WSL bench exists
here to close it, and the record says so rather than claiming a fix for something never
seen to fail.

**The third fix is the most serious thing in this section.** The **Claude Code** hook
exited 0 whenever it could not find the edited file's path — no message, no signal, gate
not run. A silently green gate, in the kit's own file, on the CLI its users trust most.
`COPILOT.md` had framed loud-reporting as a Copilot concern; it never was, that dialect
was just the only one that had it. Claude Code's hook now reports on stderr and exits 2
for every case it cannot handle: no parser, no path, file missing, unusable
`CLAUDE_PROJECT_DIR`. This outranks the `apply_patch` bug — that one at least shouted.

**Proof.** `tools/gate-hook-check.py` was rewritten to cover **both hook dialects under
both parsers** — 44 cases, all green, each silent case also run dirty.
`tools/tdd-guard-check.py` runs its 25 cases under each parser (50 runs) plus the six
mutations. The suites pin `PATH` to one interpreter at a time, because a dialect that is
never exercised is a dialect that is not proven.

**The mutation harness caught its own decay, which is the point of it.** Rewriting the
guard's error branch made the D5 mutation stop applying; the tool printed `STALE
mutation no longer applies` and failed the run rather than reporting five passes and
quietly testing nothing. A mutation that silently stops mutating is indistinguishable
from a suite that catches it — that is invariant 13 pointed at the checking apparatus
itself.

**Also corrected:** README Prerequisites now lists the interpreter; the FAQ is split
into "must my project be Python" (no) and "does the kit need it" (one of python or node,
for the hook only, and it says the old answer was wrong); `jq` is dropped as a suggested
substitute, since it was never a shipped path and never tested, and two proven dialects
replace it; `sdlc-update.md` and the root README both carry the both-CLI hook-recipe
change, which — being project-owned — no update can deliver.

### 31.14 Owner rulings, 2026-08-05 — guards ship as an offer; session-scoping ships

**(a) The guards ship as a setup offer, not held back.** Built that way already
(`sdlc-setup.md` step 6: offered with its trade-off stated, default to offering rather
than installing, logging mode only, proof step required).

**And an update must offer them to a project that missed them — which exposed a defect
in the build.** Setup had been told to *delete* the `{{TDD_GUARD_NOTE}}` line when the
owner declined. That erases the difference between "considered and declined" and "never
asked", and those are the two cases an update has to tell apart: absent guards look
identical on disk either way. Fixed in three places: setup now records a decline **with
its date** and never deletes the line; `SDLC.template.md`'s comment says why; and
`sdlc-update.md` gains an explicit two-step check — is this a Copilot project
(`{{TARGET_CLI}}`), and are the guard files present? Absent plus a recorded decline is a
settled decision that gets one sentence; absent plus **no line at all** is a project that
never had the choice, and gets the full offer. That last case is the whole point of the
instruction, and it is invisible unless something looks for it. Inv 14 in its usual
shape: the state had to name the artifact that evidences it, or the next step could not
act on it.

**(b) Session-scoped observations ship now.** A `sessionId` change clears the recorded
red/green, so yesterday's failing run cannot license today's production write. Proven
offline (case 16) and mutation-covered (removing the reset is caught), under both parser
dialects.

**The one thing to watch when deny is armed, stated because it is unmeasured:** the
scoping assumes a session keeps its `sessionId` for its lifetime. If **resuming** a
Copilot session issues a *new* id, the guard clears its observations mid-work, and the
next production write is denied even though the red was genuinely observed minutes
earlier — a false denial, the failure class D3 was written against. Harmless in logging
mode (a spurious VIOLATION line), which is exactly what the ramp is for: the bench
transcripts show sessions are resumable (§31.11 names a resumable one), but whether
resume preserves the id was never measured. Watch the log across a resume before arming
deny; if it clears, the fix is to key on session start rather than id equality. Recorded
here so the ramp has something specific to look for rather than a general instruction to
be careful.

**A second self-inflicted invariant defect, caught the same way as the first.** The new
update step was first written as "read `{{TARGET_CLI}}` in `spec/PROJECT_INDEX.md`" —
which puts a `{{` into `sdlc-update.md`, an **installed** file, breaking inv 4 (only the
installed `sdlc-setup.md` may carry placeholder syntax), and was wrong on its own terms
besides: in an adopted project that placeholder is long since resolved, so the file the
updater opens contains `**Agent CLI:** Copilot CLI`, not the placeholder name. Fixed to
name the *Agent CLI:* line, which is what step 1 of the same command already reads.
Both this and §31.13's inv-5 defect were written by a session fluent in the kit repo and
caught only by running the invariant checks against its own output — which is the
argument for running them on every batch rather than before releases only.

### 31.15 0.16.0 released — 2026-08-05, after a fifteen-finding `/kit-check`

Full pass: four mechanical checks inline, five parallel readers over the twelve semantic
invariants. **Fifteen findings, every one fixed before the tag**, and the pass earned its
place — six would have shipped, and three of those would have broken adoptions:

- **`{{TDD_GUARD_NOTE}}` had no resolver on a Claude-Code-only project.** The placeholder
  sits in `SDLC.template.md`, instantiated on both CLIs; its only resolver was inside the
  Copilot-only guard offer. Setup's own close-out `{{` check would have fired on the
  commonest adoption shape with no instruction for what to write — the prime directive's
  exact failure mode, introduced by the batch that added the placeholder.
- **`spec/SDLC.md` asserted an edit-time hook exists and runs**, while the new step 6
  sanctions declining one when the probe shows it cannot work. The template wins by its
  own first paragraph, so the command was the bug; the template now carries the negative
  case and setup resolves `{{HOOK_CONFIG_PATH}}` to name no file in that branch.
- **The guard's recorded mode named no enforcing artifact and went stale by design.** The
  note is written at the one moment it can only say "logging", and the ramp then tells the
  owner to change the flag file with no step updating the record — inv 14's specimen one
  abstraction up. Worse, `/sdlc-update` held the record and the artifact in the same step
  and never compared them, leaving two of four states unhandled. The note now names
  `.git/sdlc-tdd/deny-enabled` (and that `.git/` is per-clone, so the line describes one
  machine), and the update gained both reconcile branches.
- **"Never denies on its own failure" was false one layer up.** True of the script, which
  exits 0 on any parse failure — but if the *hook* fails before the script runs, the CLI
  decides, and this same file had measured `preToolUse` failing **closed** under WSL. The
  promise is now scoped to the script, with the hook layer named as the case the ramp
  exists to catch.
- **The recipe's dated proof certified a body that no longer existed** — "verified
  2026-08-03, six cases" against a hook rewritten two days later, and never naming which
  interpreter ran it, over a body whose failure modes are interpreter-specific. Replaced
  with the real one: 44 cases, both dialects, both parsers.
- **Kit-development vocabulary had leaked into shipped files** — a `FEATURE_PLAN.md §31.7`
  pointer and bare invariant numbers in files an adopter receives and can never resolve,
  plus a project-fact assertion in `sdlc-update.md` ("its edit-time gate has been
  reporting that it did not run") that the command has no evidence for.

**And invariant 13's own enumeration was stale**, listing six checks while this release
added four more — so the check that verifies every check states its negative case would
not have led anyone to the new ones. Both homes now carry the extended list plus a note
that the denominator is the part that goes stale silently. That is the fourth time this
lineage has caught a check whose denominator was assumed rather than enumerated, and the
first time it was caught inside the invariant that exists to catch it.

**Released:** `VERSION` 0.16.0, CHANGELOG entry, `MANIFEST.sha256` regenerated in the
release commit from **staged** content in text mode (no `*` prefix — the trap that has
broken two previous tags), discrimination proven, and all four release-workflow gates
simulated green locally before the tag.

### 31.16 Bench protocol for the shipped guard — pre-registered 2026-08-05, before the run

**Why a bench run at all, when the guard passed 25 offline cases under both parsers:**
the offline suite proves the *script's logic* against captured payloads. It cannot prove
the *wiring*. The shipped guard is a rewrite of the one the trial proved — dual-parser
detection, a self-locating prelude that derives the repo root from the payload, session
scoping, and a rewritten path loop — and **the prelude has never executed inside a real
Copilot session.** Everything between the CLI and the script's first line is unproven,
which is exactly the gap the 0.15.0 gate hook sat in for a whole release. This run is
also the only way to answer the resume question §31.14 flagged and could not close.

Bench: `copilot-ci-test`, Copilot CLI 1.0.77, hooks under WSL bash (31.7.5). Runs stay
in **logging mode** — nothing is armed. Known harness hazards, both already paid for:
`copilot.exe` is reachable only by its WinGet path, and piping `copilot -p` output
through a head-style filter kills the CLI before its stop hooks run (capture to a
variable instead).

**Criteria, and what each outcome means:**

- **B1 — the wiring works at all.** On a real session that edits a file and runs a test,
  `.git/sdlc-tdd/guard.log` gains lines from the shipped guard. Failure means the
  prelude, the matcher, or the parser detection is broken in the live environment, and
  0.16.0's guards do not work as shipped — a point-release fix, and the honest reading
  is that the offline suite bought less than it appeared to.
- **B2 — the parser resolves in the hook's own shell.** No `GUARD ERROR` line appears.
  A `GUARD ERROR: no JSON parser` line is a *pass for the guard's honesty* and a finding
  about this machine, and it makes the dual-dialect work load-bearing rather than
  theoretical.
- **B3 — the catch still catches.** A session told to write production code without a
  failing test first produces a `VIOLATION` line naming the file. This is V1 from §31.8
  re-run against the rewritten script; failure is a regression the offline suite missed.
- **B4 — silence on a clean run.** A strict-TDD sequence produces zero `VIOLATION` lines
  and a clean stop. Failure is a false positive, which under deny would block real work.
- **B5 — the resume question, the one genuinely new unknown.** Record the `sessionId` of
  a session, resume it, and read whether the guard logs `new session … previous
  observations cleared`. **Cleared on resume = the session-scoping shipped in 0.16.0
  false-denies after any resume once deny is armed**, and the fix is to key on session
  *start* rather than id equality. Not cleared = the scoping is sound as shipped. Either
  answer is worth the run; this is the criterion the batch shipped without.

**Decision rule, fixed now:** B1–B4 green and B5 "not cleared" → the shipped guards are
proven live and the deny ramp is available to any adopter who wants it. B5 "cleared" →
a 0.16.1 fix to the scoping, and the changelog says plainly that session-scoping as
shipped is unsafe to arm. Any B1–B4 failure → the guards are not what 0.16.0 claimed,
and that is a point release, not a note.

### 31.17 Shipped-guard bench run — 2026-08-05: all five criteria met, and the resume question is answered

Run against §31.16's protocol, which was committed before the guard was installed
(`ea892b3` precedes it, provably). Copilot CLI had moved to **1.0.78** during the batch;
everything measured on 1.0.77 held, which is itself worth having.

- **B1 met — the wiring works.** The self-locating prelude resolved the repo root from
  the payload's own `cwd` inside a real session, found the script, and ran it. This is
  the half the 25 offline cases could not touch, and the half the 0.15.0 gate hook
  failed for a whole release.
- **B2 met — no `GUARD ERROR`.** A JSON parser resolved in the hook's own shell (WSL
  bash on this machine), so the dual-dialect detection works where it has to.
- **B3 met.** Told to write production code with no test, the session was caught:
  `VIOLATION production write without observed red`.
- **B4 met — zero violations on a strict-TDD run**, and the trace is textbook: test edit
  recorded → `RED observed (exit 1)` → `OK production write (red observed since last
  test edit)` → `GREEN observed` → `stop: clean`.
- **B5 answered, favourably: `--continue` PRESERVES the `sessionId`.** The resumed
  session logged no "new session" line and cleared nothing. **Session-scoping as shipped
  in 0.16.0 is sound** — it does not false-deny after a resume, and no 0.16.1 is needed.
  This was the one unknown the batch shipped with, and it came back the right way.

Two things the run added beyond its criteria. **Both path forms appeared in a single
session** — absolute-Windows on one write and repo-relative on another — which is the
31.9.1 finding reproduced against the rewritten classifier, and the reason it normalises
before matching. And **the guard has now been proven live at the layer that matters**:
per §31.16's decision rule, B1–B4 green with B5 not-cleared means the deny ramp is
available to any adopter who wants it, on evidence rather than on the offline suite's
say-so.

**One process note, honestly recorded.** The first B4 reading said "2 violations" and was
wrong: the count swept the whole log, including the earlier sessions' lines, because the
archive step copied the log rather than truncating it. Scoped to the B4 session the count
is zero. That is the second time this session a harness asserted over the wrong range —
the first was the exempt-file case in the offline suite — and both times the artifact was
correct and the measurement was not. Worth remembering that a check reporting a failure
is as capable of being wrong as one reporting a pass.

**Bench state:** the shipped guards are installed and live in **logging mode** (no deny
flag), the trial script is archived rather than deleted, and the reversal list plus both
logs are recorded in the fixture's `ENF_PROBE_NOTES.md`.

### 31.18 First field arc on 0.16.0 — and the guards' first real defect, found by arming them

`ai-news-dashboard` (Java/Spring Boot, Copilot CLI) updated 0.14.0 → 0.16.0 on
2026-08-06, guards installed and deny armed at the owner's request. Two findings, and
the second is the important one.

**The `apply_patch` fix landed on a live adopter, and the defect was exactly as
predicted.** Their instantiated hook JSON-parsed `toolArgs`, so their edit-time gate had
never run once since adoption on 2026-08-03 — Checkstyle and compile fired on zero
edits across a whole merged phase. Rebuilt from the 0.16.0 recipe, keeping their
commands, and proved live: a deliberate star import produced Checkstyle feedback in a
real session; reverting restored silence. **This is the first confirmed field catch of
0.16.0**, and it validates the project-owned-so-apply-by-hand path end to end.

**G1 can be satisfied without writing any test — measured, not theorised.** Armed for
deny, the session was denied twice, then ran
`mvn test -Dtest=ThisTestDoesNotExist`. Maven exits non-zero because no tests matched
the pattern; the guard recorded `RED observed (exit 1)` and licensed the write. No test
for that class ever existed.

The denial mechanism was not at fault — it denied, correctly, twice. The broken step is
the **inference that a red implies a test**, and it lives in one branch:

```sh
if [ ! -f "$S/last-test-edit" ] || [ "$S/red-observed" -nt "$S/last-test-edit" ]; then ok=1; fi
```

`[ ! -f "$S/last-test-edit" ]` licenses a write whenever **no test file was edited this
session at all**, so any non-zero exit from a test-shaped command satisfies G1. The
bench never saw this because the bench session complied by writing a real test — the
anti-TDD instruction there produced cooperation, and here it produced circumvention.
§31.11 predicted the shape ("it could as easily have touched the state files") and
guessed the mechanism wrong: this session did not read the guard's source, it just
found a command that exits non-zero.

**Candidate fix for 0.16.1, not yet built or approved:** require `last-test-edit` to
*exist* and the red to be newer than it — "you changed a test this session, then saw it
fail". The cost is a resumed session whose test was written earlier: session-scoped
state clears, and re-running the suite gives a red with no test edit, so the next
production write is denied until a test file is touched. That is a real false-denial
risk and is the reason this is a proposal rather than a patch. **Owner decision owed**,
and it wants the offline suite extended with this exact case first — a mutation that
manufactures a red with no test edit, which the current 25 cases do not cover.

Bench note: the guards stay armed on that project by owner decision — the hole needs
deliberate circumvention, produced no false denials, and disarms with one file deletion.
The finding is recorded in their `spec/SDLC.md` and Kit friction log, which is the
kit's own feedback channel working as designed.

---

## 32. Seventh field report — triaged 2026-08-06

Filed as `sdlc-kit#4`. Second arc from `ai-news-dashboard` (Phase 02, four slices,
PR #4, merged 2026-08-06), and the first report produced *under* 0.16.0 — the arc
§31.18 already mined for the guard hole; the retro's carried-friction entry 3 is
§31.18's finding, already tracked, no double-count. The local retro
(`spec/SDLC_RETRO_2026-08-06.md` in their tree) carries **three** findings; the owner
submitted 1 and 3 and kept 2 (a per-session execution log of which steps ran, Low)
local — the issue's numbering gap is a decision, not a loss, and finding 2 is noted
here only because its kit half (`end-slice` §7/§9, the template's Bookkeeping rules)
may return in a later report.

The retro itself is worth a line: all four slice commits carried complete evidence
records (`RED:`/`quality:`/`mutation:`/`verify:` lines), the step-evidence table
(R5.6's sweep) is present with per-step outcomes including two stated-reason skips,
and the report reads directly off `git log`. The bookkeeping machinery R4/R5 shipped
is doing in the field what it was built to do.

### 32.1 Finding 1 — the chain is exactly as filed, and it is the design

**Verified, every quote:** `commands/next-slice.md` §5 (lines 113–116) is one
instruction — "tell the owner the slice is ready for close-out … and run `/end-slice`" —
with no seam between the telling and the running; `end-slice.md` line 4 runs without
asking; `end-slice`'s Notes (line 257) push the branch. The session that ran §5 to
commit-and-push was *complying*, not drifting — this is not a Copilot activation
defect, and no halt was skipped, because no halt exists there:
`SDLC.template.md` lines 63–64 designate it — "The process runs autonomously except at
these five points. Everything else (gates, reviews, fix application, bookkeeping,
commits) proceeds without asking."

So the finding's damage claim is bounded — the commit lands on the arc branch, and
halts 4 and 5 still stand between the work and `{{MAIN_BRANCH}}` — but its sharpest
form is an internal contradiction the filed text circles without naming: **the
hand-back standard (template line 91) promises that every owner-facing moment opens
with an executive summary the owner can act on, and at this boundary the summary and
the close-out arrive in the same turn, so there is nothing left to act on.** The
"tell the owner" clause writes a cheque the five-halt design does not cash.

Three dispositions, verified against the tree before asking:

- **(a) The filed fix — a sixth halt.** `AskUserQuestion` between summary and
  `/end-slice`, named in the halt list. Cost is real and enumerable: the five-count is
  load-bearing prose in `SDLC.template.md` (lines 63, 91), root `README.md` (lines 19,
  36–37, 570), `reference/COPILOT.md` line 4, root `CLAUDE.md` line 63, plus the halt
  renumber ripple (derive mechanically at build time per §4a). And it adds one
  ceremony question to every slice — the coin the halt-2 skip rule exists to conserve.
- **(b) A command boundary, not a halt.** `next-slice` §5 ends at the hand-back
  summary; the owner runs `/end-slice`. The template's own slice loop (line 274)
  already reads this way — "Run `\end-slice` when the slice's exit criteria are met"
  is addressed to whoever runs commands, and §5's "and run" clause is the chaining
  text. The five-halt architecture is untouched (owner-typed command boundaries —
  `/plan-phase`, `/next-slice` — have never counted as halts), the inspection moment
  the hand-back standard promises becomes real, and the diff is two files
  (`next-slice.md` §5; a template sentence making the boundary explicit).
- **(c) Decline** — keep autonomy, rely on halts 4/5 plus branch recoverability, and
  record the ruling as standing. Honest but leaves the hand-back-standard
  contradiction in the template.

**Enforcement caveat, either way (a) or (b):** on Copilot both are prose — the CLI
that produced this finding is the CLI where instructions demonstrably bend (§31.1).
An evidence-shaped version (a commit guard requiring an owner-created confirmation
marker, ENF-style) exists but is 0.17.0-scale machinery; the prose fix ships first
and the friction log will say whether the boundary holds.

### 32.2 Finding 3 — stands as a hardening; its central claim did not survive

The lineage holds (§12 had three such): **"there is nowhere in the project to read the
URL from" is false against the filer's own tree.** The URL ships in the installed
update skill — their `.github/skills/sdlc-update/SKILL.md` line 65, the clone line of
the update procedure — and in `sdlc-setup`'s installed copy (line 491), and this
adopter additionally kept a full `sdlc-kit/` source copy in-tree (`sdlc-kit/README.md`
line 8, where the owner eventually pointed). The retro searched `spec/` and "the
project tree" and missed all three — the second report's theme, a denominator assumed
rather than enumerated, this time inside the retro's own search.

What survives is the architecture point: a URL embedded as an *example* inside an
installed command is incidental, not recorded — the gate-baseline pattern is that
facts commands need are written into `spec/SDLC.md` at adoption and read from there.
Remedy shape if accepted: `{{KIT_HOME_REPO}}` in `SDLC.template.md` (invariant 1 —
setup must be taught to resolve it; the exit-check grep is already scoped right),
`sdlc-retro.md` §6 resolves the URL from `spec/SDLC.md` **with the installed
`sdlc-update` clone line as the stated fallback** for pre-placeholder adoptions, and
`sdlc-update.md` backfills the line on update. Small batch; `ai-news-dashboard`
already hand-applied the project half (`spec/SDLC.md` line 16 now names the repo).

### 32.3 Clock effects — the first of the two field arcs has run

- **§30.4 clock (`change-simplify` / `change-verify`): `change-verify` has its
  confirmed field catch.** TagBackfillRunner re-processing zero-match items on every
  boot, caught at S3 — slice level, before phase end — owner-confirmed in the retro.
  That is R5.1's slice-level trigger doing precisely what it shipped for, one arc
  after shipping. `change-simplify` ran on all four slices ("moves applied or
  nothing-to-do" quality lines) but the retro confirms no catch — one arc remains on
  its clock.
- **STD's audit clock:** arc one of two banked, and this time with R5.6's per-step
  evidence table in the retro — `diff-review` shows catches at both altitudes (arc:
  SpotBugs `EI_EXPOSE_REP` + N+1; slice: tagged backlog entries). The next arc's
  retro closes the clock with evidence of the same grade.
- **§31.18's 0.16.1 decision** (guard-hole fix) is unchanged by this report — still
  owed, still wants the offline suite extended first.

### 32.4 Owner rulings, 2026-08-06 — both recommendations accepted; built same day

1. **Finding 1 ships as (b), the command boundary.** `/next-slice` ends at the
   slice-ready hand-back; `/end-slice` is owner-typed. Not a sixth halt — the
   five-count prose everywhere stands unchanged.
2. **Finding 3 accepted as scoped in §32.2** — `{{KIT_HOME_REPO}}` placeholder, retro
   resolution order, update backfill.
3. **Release batching ruled 2026-08-06, second sitting: one release.** The owner
   approved §31.18's candidate fix — it ships as **0.16.1** together with this
   section's two fixes. §31.18's own condition holds: the offline suite is extended
   with the circumvention case *first*, the case is watched to fail against the
   shipped guard, and only then does the fix land (§32.6). `/kit-check` before
   release.

### 32.5 Build record — 2026-08-06

Edits, derived at build time per §4a (the chain turned out to be stated in exactly one
place — `next-slice.md` §5; every daily-loop description elsewhere already read as an
owner-typed sequence, which is what made (b) the template's own framing):

- `templates/SDLC.template.md` **[adoption-only]**, three edits: the *Kit home
  repository* line in the header ({{KIT_HOME_REPO}}); the boundary paragraph above the
  slice loop's `/end-slice` steps; a halt-preamble sentence — autonomy runs *within* a
  command, never across the boundary between them — placed where the finding looked
  for protection and found silence.
- `commands/next-slice.md` §5 **[installable]** — "stop there; do not run
  `/end-slice`; the owner runs it", with the why (a summary delivered in the same turn
  as the commit it describes is a summary no one could act on).
- `commands/end-slice.md` *How to use* **[installable]** — the mirror guard:
  owner-typed only; reached without the owner asking → stop. On Copilot commands
  install as model-invocable skills, so the boundary is stated on both of its sides.
- `commands/sdlc-setup.md` preflight 1 **[installable]** — resolves
  `{{KIT_HOME_REPO}}` from the kit README's opening, falls back to the clone URL in
  `commands/sdlc-update.md`, asks only when both are missing (invariant 3 satisfied by
  a step, not a question; no new interview round).
- `commands/sdlc-retro.md` §6 **[installable]** — resolve the URL *before* presenting
  Decision 1: `spec/SDLC.md` first, installed `sdlc-update`'s clone line as the stated
  fallback for pre-placeholder adoptions — and a fallback-resolved URL is written into
  `spec/SDLC.md` in the report's docs commit, so the next retro reads it from where it
  belongs.
- `commands/sdlc-update.md` step 6 **[installable]** — backfills the *Kit home
  repository* line when absent, with the URL step 2 cloned the target kit from — the
  same fact, observed in-session; joins the absent-only writes, never overwrites.

### 32.6 The §31.18 guard fix — suite-first, red observed, and the suite caught its
### own regression — 2026-08-06

Built in §31.18's pre-registered order, which is the kit's own discipline applied to
the kit:

1. **The case first.** `tools/tdd-guard-check.py` gained unit case 20 — a red
   manufactured by a test-shaped command matching nothing, no test edit in session,
   then a production write — plus a mutation that reverts the fix, so the suite
   enforces it permanently.
2. **Red observed, not assumed.** Against the shipped 0.16.0 guard, case 20 failed
   exactly as the field did: `OK production write (red observed since last test
   edit): payments.py` — with no test edit ever made. The new mutation reported
   STALE, as it must: its target string is the fixed source.
3. **The fix.** G1's licensing branch now requires all three of: red observed, a
   test-file edit existing this session, red newer than the edit. The deny message
   says "write **or edit** one test" — the way out of the known false-denial (a
   resumed session's cleared state), which the owner accepted in ruling the fix
   shipped. Header comment, `reference/GATE_RECIPES.md`'s G1 statement, and the deny
   text all restate the same rule.
4. **The re-run caught a regression the fix itself created.** All 26 cases green on
   both parser dialects and the new mutation caught (by cases 9 and 20) — but the
   session-reset mutation, caught before the fix, **SURVIVED** it: case 16 had leaked
   only a bare red across sessions, and the fixed G1 refuses a bare red anyway, so
   the case could no longer tell the reset from the fix. Case 16 now carries a fully
   licensing state (test edit, then newer red) across the boundary, which is the only
   shape that distinguishes them. A suite whose mutation pass is re-run after every
   guard change is the reason this was found the same hour it was created.
5. **Final run, 2026-08-06: 26 cases green on both dialects, all 7 mutations caught**
   — including the strengthened session-reset case and the fix-reverting one. Exit 0.

### 32.7 The 0.16.1 `/kit-check` — fifteen findings, ten fixed in-session, five
### deferred with a record

Run 2026-08-06 pre-release: mechanical checks in-session, the reading passes fanned to
four read-only agents, every agent finding re-verified against the tree before any
edit. The census (inv 4), README tree (inv 9, by no-adds-since-0.16.0 plus the 0.16.0
pass), step references (inv 6), bundle purity (inv 12), pointers (inv 5), and the
boundary itself (inv 2A — template, all seven commands, both READMEs, zero residual
chaining text) all pass clean.

Fixed in-session, ten: the two mislabels calling all eight skills vendored
(`sdlc-setup.md`, both modes — invariant 11's own defect definition); the root
README's now-false "two exceptions" / "only content an update writes" claims and
`sdlc-update.md`'s stale "third line" ordinal (both fallout from §32.5's backfill —
caught the same session they were created); `sdlc-update.md`'s copy rule naming
`.claude/commands/` as universal for commands (per-CLI now, "both gets both");
the README tree's unqualified `settings.template.json` row (Claude Code dialect);
`end-phase.md`'s `--cov-fail-under` as primary referent (stack-neutral now); the
`{{KIT_HOME_REPO}}` reconcile gap (inv 14 — update now compares the recorded line
against the URL it actually cloned when present, mismatch is an owner finding); the
false "setup checks the skill listing" claim (`SKILLS.md` — setup verifies files and
copies, the listing needs a fresh session, and setup's close-out now says which it
reports); "green" naming its shell in `end-slice` §2 and `end-phase` §2 (CI
authoritative on disagreement, per the template's existing rule); the `verify:` line
naming the shell it ran in, in the template first and the command with it, with the
explicit sentence that an agent-shell pass does not stand in for halt 4. Three
placeholder-mapping minors from inv 3 (TEST_LAYOUT unnamed in New mode;
START_HERE/PHASE_HISTORY_ROWS/NOTES resolved only generically; the `{{HOOK_*}}`
wildcard not covering `{{SOURCE_GLOB}}`) were fixed the same hour.

Deferred, five, recorded in `IMPROVEMENT_PLAN.md` §9 with sizes: the two live
step-numbering bases (command-local vs template-canonical — real, wide, sized like
the 0.15.0 renumber); `{{ADOPTION_DATE}}` claim-only unmarked; the `Agent CLI:`
line's missing staleness reconcile; the guard proof step naming no session/shell;
root `CLAUDE.md`'s Claude-Code-first command-path wording.

### 32.8 0.16.1 released — 2026-08-06

Tag `v0.16.1`, release workflow green on the first run (all three checks — version
match, manifest current, manifest coverage — were replicated locally before the tag;
the text-mode MANIFEST regeneration held, no recurrence of the `*`-prefix failure).
Assets published: `sdlc-kit.tar.gz`, `sdlc-kit.zip`, `sdlc-kit.CHECKSUMS.txt`.
`sdlc-kit#4` closed with the shipping pointer and the apply-by-hand note for the
project-owned guard.

Open threads leaving this section: `ai-news-dashboard` runs 0.16.0 with the G1 hole
and the chaining `next-slice` — its next `/sdlc-update` picks up the commands, and
the guard's one-line G1 change is the owner's hand-apply (changelog states it).
The §30.4 clock: `change-verify` satisfied; `change-simplify` one arc left. STD's
audit clock: arc one of two banked. The five deferred kit-check findings sit in
`IMPROVEMENT_PLAN.md` §9. And the boundary fix itself is prose on the CLI that
produced the finding — whether it holds is exactly what the next field arc's
friction log will say (§32.1's enforcement caveat pre-registers the escalation
shape: an owner-created confirmation marker, ENF-style, if it bends).

---

## 33. R6 candidates — extracted from the ai-news-dashboard standards audit,
## 2026-08-06

Source: a whole-tree audit of the second adopter after two merged phases (three
read-only sweeps — every logger call site, every catch block, all 53 tests — plus the
gate run live and the enforcement chain traced; findings verified, agent claims
re-checked). The adopter-side findings are damage the owner can fix there; this
section extracts only what generalizes to the kit. The audit's meta-result repeats
ENF's thesis on fresh evidence: **every mechanized rule held (Checkstyle catches,
no-stdout, SpotBugs); every prose-only rule bent (level ladder, mock policy, the
blind-catch license, a ratified JOIN FETCH decision).** But four gaps are sharper
than that thesis, and none is covered by existing machinery — each was checked
against the tree before being written here.

**What already exists and therefore is NOT proposed:** `diff-review` names
`CLAUDE.md` *Runtime Conventions* as its Standards axis (SKILL.md input 1);
`end-slice` §4 states the two axes; `end-phase` has the backlog presentation point
("defer knowingly, or drop"); the coverage floor has a two-homes reconcile. The
violations shipped *through* this machinery, which is what makes the gaps below
gaps.

### 33.1 The candidates, each with its confirmed field evidence

**R6.1 — Absence is invisible to every existing check; the acceptance halt gains
the log.** The adopter's recorded logging ladder promises INFO at run boundaries and
ERROR for a failed run; after two phases there are zero ERROR sites, no run-boundary
INFO, and no logging config, so the DEBUG tier is unreachable. No step caught it
because reviews are diff-shaped (the violation is in what no diff ever contained)
and halt 4 verifies *visible behavior*, not the log. Fix: `SDLC.template.md` halt 4
and `end-phase` §3 add one sentence — the run the owner exercises produces a log,
and reading it against the recorded logging conventions is part of the acceptance
surface; silence at a promised boundary is a finding. Environment-true by
construction (the owner's shell, the composed run).

**R6.2 — A finding that contradicts a ratified phase decision is a spec conflict,
not a backlog line.** The dashboard N+1 violates the phase spec's own decision D5
("single JPQL JOIN FETCH … to avoid N+1"); the arc review caught it and it was
backlogged and merged anyway. The kit's halt 3 says spec conflicts are never
resolved silently — but nothing classifies a review finding *as* a spec conflict
when it contradicts a decision the owner ratified at halt 1. Fix: one rule in
`diff-review` (severity: a finding that contradicts a ratified spec decision is
CRITICAL and named as a spec conflict) and one clause in `end-phase`'s backlog
presentation (such a finding cannot be deferred by default — it takes halt 3's
owner ruling: fix now, or amend the decision it contradicts).

**R6.3 — A catch is not a fix, and the retro currently lets one read as the
other.** The retro's *What worked well* cites "caught the N+1" and the backfill
catch as wins; both defects are still in the code, open in the backlog. The kit's
own §32 triage then repeated the claim. Fix: `sdlc-retro` — a catch may be cited as
evidence a practice worked **only with its disposition attached** (fixed in
`<commit>` / open in backlog as `<entry>`), and a cited catch whose entry is still
open is listed under open damage, not only under wins. One rule, retro-side.

**R6.4 — A recorded enforcement claim is proven by its negative case, once, when
established.** The adopter's PROJECT_INDEX says the 83% floor is "Enforced in
`pom.xml` coverage-check execution" — false in the machine: `jacoco:check` binds to
`verify`, the gate runs `mvn test`, CI runs `jacoco:report`. The two-homes
reconcile passed because both homes record 0.83 — nothing checks the enforcing
goal ever *runs* in the commands the gate actually executes. This is the third
report's theme, reproduced in the second adopter, one layer deeper than the
existing reconcile reaches. Fix: `end-phase`'s coverage bullet (and setup, when a
floor is first established) gains the kit's own hook discipline: prove the floor
fires — set it above the observed number, run the gate's commands, watch them
fail; not failing means the floor is not wired into the gate, and the wiring (not
the record) is the fix. One-time per establishment, not per phase.

**R6.5 — The retro sweeps commit evidence but never sweeps spec claims against the
tree.** `spec/TESTING.md` names `TestIsolationConfig.java` and records "outbound
network is blocked"; the file has never existed, across two phases and two retros.
Fix: `sdlc-retro`'s sweep gains one enumeration — every concrete artifact the spec
files name (file paths, harnesses, configs, floors), checked for existence, absent
ones reported with their age. Mechanizable (grep paths, stat files),
denominator-true.

**R6.6 — the unconsumed-artifact lens (arc review).** Three dead artifacts shipped
in one small codebase: an entity+repository with no production writer, a seeded
column nothing reads (its accessor does not exist), and factory overloads only
tests call. The consumers lens covers *changed* paths only; nothing asks of a
**new** artifact "what reads this?" Fix: one lens in `REVIEW_LENSES.md`, applied at
arc review: every artifact this arc introduced (entity, table/column, endpoint,
config key, public API) names its consumer; no consumer is a finding. Three
confirmed catches justify it under the §16 audit regime from day one.

### 33.2 Sizing and the regime

R6.1, R6.3, R6.4 are one-to-two-sentence edits (template + one command each).
R6.2 is two edits (skill + command). R6.5 is one retro step. R6.6 is one lens.
All six enter under the §16 audit regime: no confirmed catch in two arcs from
shipping makes any of them a deletion candidate — and each arrives with the field
evidence above as its founding catch.

### 33.3 Owner approval and build — 2026-08-06, same day

The owner approved **all six**. Built template-first (inv 2), each rule stated once
canonically and once at its acting step:

- **R6.1** — `SDLC.template.md` halt 4 + `end-phase.md` §3: the run's log output is
  part of the acceptance surface, read against the recorded logging conventions;
  silence at a promised boundary is a finding.
- **R6.2** — `SDLC.template.md` halt 3 (a finding contradicting a ratified spec
  decision is a spec conflict and takes the halt), `diff-review/SKILL.md` (the one
  fixed severity rule: such a finding is CRITICAL, named as a spec conflict — which
  end-slice's existing no-unfixed-CRITICAL rule then enforces at slice level for
  free), `end-phase.md` backlog presentation (exempt from default deferral).
- **R6.3** — `sdlc-retro.md` interview: a catch cited as evidence carries its
  disposition; open ones list under damage, never wins alone.
- **R6.4** — `SDLC.template.md` *Coverage floor* + `end-phase.md` coverage bullet:
  when a floor is first established, prove it fires (set above observed, run the
  gate's commands, watch the failure) — the hook-install discipline applied to the
  floor.
- **R6.5** — `sdlc-retro.md` step 2 gains the spec-claims-against-the-tree sweep
  (named artifacts stat-checked, absences reported with age).
- **R6.6** — `REVIEW_LENSES.md` gains *the unconsumed artifact* (arc-scoped, three
  numbered questions, provenance note with the three founding catches); wired at
  both ends — the lens file's header now names `/end-phase` as an entry point, and
  `end-phase.md` step 5 + the template's phase-end step 4 name the lens.

Not released: this batch is 0.17.0-shaped (new process rules), `/kit-check` owed
before it ships, release timing the owner's call.

---

## 34. The pre-0.17.0 `/kit-check` — run 2026-08-06, eighteen findings, all fixed in-session

Full 15-invariant pass on the R6 batch: four mechanical checks in-session, the twelve
semantic invariants fanned to five read-only agents, every agent finding re-verified
against the tree before any edit. Invariants 1, 3, 6, 9, 11 pass clean (inv 1 with the
sanctioned GitHub note; inv 6 with all ~80 step references verified, zero stale;
inv 10 expected-stale — exactly the five R6-edited files mismatch, discrimination
proven, regeneration belongs to the release commit).

The headline finding is invariant 13 catching itself again: **R6.4's coverage-floor
fire-proof was a check added without joining the denominator** in `KIT_INVARIANTS.md`
or `kit-check.md` — the exact staleness the ledger's own rule names, caught pre-release
this time. Both lists extended; and the fire-proof's own gap closed with it (the
Existing-mode adoption path recorded an inherited CI floor as-is, unproven — the R6.4
founding specimen *is* an adoption-time claim; setup and `GATE_RECIPES.md` *Coverage*
now both carry the prove-it-fires discipline).

The rest, grouped: **inv 2** — `end-slice`'s triage lacked the R6.2 spec-conflict
carve-out (its Fix-now bucket silently forecloses "amend the decision", the choice
halt 3 reserves for the owner); the lens-routing summary in both homes omitted three
trigger clauses the lens file states (trusted-check scripts, logging around a failure
path, logging near credentials), so those triggers could never fire. **Inv 15** — the
retro's gate-trajectory run named no shell; the backlog reproduce-or-disprove could
falsely disprove an owner-shell/CI-observed cause from the agent's shell and then
"correct" the entry (both homes now require reproducing where the cause was observed,
with a different-environment failure downgrading to "could not reproduce here"); the
gate-baseline record format gains the shell it was measured in. **Inv 14** — the gate
baseline had a second prose home in PROJECT_INDEX's phase block that nothing
reconciled while `SDLC.template.md` claimed to be its single home (mirror replaced
with a pointer, keeping the claim true); the Claude-side model pin is now marked
claim-only. **Inv 5/7** — `sdlc-retro`'s citation read named `.claude/commands/` as
universal, false on Copilot-only adoptions (per-CLI now). **Inv 12** — "the bench"
anchored at first use in `GATE_RECIPES.md`. **Inv 3** — `{{HOOK_TOOLS}}`/
`{{SOURCE_EXT}}` were the last two placeholders resolved only generically (setup step
6 now names all four prose-restated hook facts). **Inv 8** — four one-sided
asymmetries closed (README gains the `{{KIT_HOME_REPO}}` mismatch-compare, the two
guard-contradiction branches, and the read-the-transition-notes-first warning whose
absence would strand a ≤0.13.0 hand-updater with a spec that disables the new steps;
`sdlc-update`'s Notes now name `explore.agent.template.md` as installable-on-Copilot).
Plus the root FAQ's skills-provenance answer, stale since PORT (vendored-only wording;
now states both regimes — inv 11's shape in a kit-dev doc).

Seven below-threshold observations recorded in `IMPROVEMENT_PLAN.md` §10 with sizes —
notably R6.4's CI-only-activation residual and R6.6's missing denominator cross-ref.
The five 0.16.1 deferrals (§9 there) stand unchanged.

**0.17.0 released — 2026-08-06, same day, owner's call.** Commit `473f1b4`, tag
`v0.17.0`, workflow green on the first run; assets `sdlc-kit.tar.gz`, `sdlc-kit.zip`,
`sdlc-kit.CHECKSUMS.txt` published. The manifest was regenerated from **staged**
content (`git cat-file` on the index) in text mode — no `*`-prefix recurrence, third
consecutive tag the trap has held. Discrimination proven: exactly the 12 edited bundle
files changed hash. The release commit also carries the two release-owed edits the
kit-check table did not: the 0.17.0 transition note in `sdlc-update.md` step 5 (the
0.15.0-shaped hazard — updated commands pointing at spec sections an un-re-instantiated
`spec/SDLC.md` does not carry, and the spec wins) and the CHANGELOG entry, whose
update-path paragraph states the same thing.

Open threads leaving §34: all six R6 rules are now on the §16 audit clock (two arcs,
founding catches recorded); `change-simplify` has one arc left (§30.4); STD's audit
clock has arc one of two banked (§32.3); `ai-news-dashboard`'s next `/sdlc-update`
crosses 0.16.1 **and** 0.17.0 — the G1 one-line hand-apply and the R6 template diff
land together at that halt. Deferred records: `IMPROVEMENT_PLAN.md` §9 (five, from
0.16.1) and §10 (seven, from this pass).

---

## 35. Post-0.17.0 cleanup — six recorded deferrals actioned, 2026-08-07

The six §9/§10 items whose records already stated a fix direction and needed no owner
ruling, built template-first, each marked actioned at its record: **§9.2**
(`{{ADOPTION_DATE}}` now names the adoption commit as its evidencing artifact — inv
14's claim-only rule); **§9.4** (the guard proof step names the Copilot CLI's own
session and the measured hook shell — inv 15); **§9.5** (root `CLAUDE.md`'s command
install path stated per-CLI); **§10.2** (phase-level `change-verify` names the
agent's shell in both homes, symmetric with its slice-level twin); **§10.3** (the
unconsumed-artifact lens cross-references *verify the denominator*, with the
framework-wiring caveat); **§10.7** (the template's phase-spec content list gained
trust boundaries, aligning it with `plan-phase`'s skeleton). Manifest regenerated in
the same commit (inv 10). **Unreleased** — 0.17.1-or-later content; it rides along
with whatever ships next.

**What remains deferred, with the reason it stayed:** §9.1 (step-numbering sweep —
its own batch, needs a convention chosen), §9.3 (`Agent CLI:` reconcile — needs a
designed evidence source), §10.1 (R6.4's CI-only-activation residual — rule-cost
call), §10.4 (inv 13 scope clause — ledger edit, owner's call), §10.5
(hypothesis-tests frontmatter — needs the upstream), §10.6 (interview asymmetries —
notes, resolve semantically today).

---

## 36. Second adopter on 0.17.0 — audit filed, update landed, 2026-08-07

Adopter-side session (`ai-news-dashboard`), closing §34's open thread. Three commits,
all merged to their `main` (PR #5, merge `28c137e`):

- **The 2026-08-06 audit's adopter half is finally filed** (`979d52e`, direct to
  main): eight backlog entries with `(external audit, 2026-08-06)` provenance, every
  claim re-verified against the tree first — including sharpening the mock-policy
  finding to its real offenders (`RefreshOrchestrationServiceTest`,
  `RefreshSchedulerTest`; the `@WebMvcTest` mocks are sanctioned by their own
  protocol). The dashboard-N+1 entry now names its Phase 02 D5 spec conflict (R6.2's
  founding shape, pre-classified for their next `/plan-phase`), and the index's
  "Enforced in pom.xml" coverage claim is marked disputed rather than silently
  rewritten.
- **`/sdlc-update` 0.16.0 → 0.17.0 ran clean end to end**: 17/17 installed files
  `UNCHANGED` both directions (denominator proven, discrimination proven), kept-bundle
  enumeration found one file ahead of 0.16.0 (`COPILOT.md` — replaced wholesale,
  moot), nothing project-owned touched but the re-stamp. First field execution of the
  no-structural-moves update path.
- **Both update-owed hand-applies landed in the same PR** (`5c3b26e`): the G1 guard
  fix applied by template diff — their guard was provably placeholder-only-divergent
  from the 0.16.0 template, so the fixed file inherits the offline proof (26 cases,
  7 mutations) rather than being a bespoke edit — and the full 0.16.1+0.17.0
  `SDLC.template.md` fold-in, so their spec no longer disables the updated commands.
  Their guard record updated with the artifact (the stale "absent, as now" clause was
  the §31.15 inv-14 specimen recurring in the field; now corrected).

**Phase 03 is the next arc, and it runs on current machinery.** It is the arc that
closes `change-simplify`'s clock (§30.4), banks STD's second arc (§32.3), and gives
all six R6 rules their first exposure (§34) — with R6.2's specimen (the D5 conflict)
already sitting classified in their backlog, so the rule fires on its founding case
the first time `/plan-phase` reads it.

---

## 37. Deterministic verification of guidance — brainstorm 2026-08-07, two batches
## approved

Owner session, 2026-08-07. The prompt: the kit's guidance should be verifiable in a
deterministic manner on both CLIs — LLM help allowed where a script cannot reach —
and the new Copilot CLI surface (`/plan`, rubber duck, orchestration) examined for
what it offers. A cited research sweep ran the same day against GitHub's official
docs and changelogs; the capability facts below carry that date, and **every one
re-verifies at build time per §21's standing rule** — the sweep is triage input, not
build authority.

### 37.1 Capability facts the plan rests on (verified 2026-08-07, official sources
### unless marked)

- **`/plan` (plan mode) is real** — changelog 2026-01-21, CLI best-practices page.
  The plan is checkbox-structured Markdown saved to the **session folder**
  (`~/.copilot/session-state/<id>/plan.md` — community-sourced path), not the repo;
  approval is awaited before implementation. Press-sourced only, re-check at build:
  since ~2026-07-14 plan mode **hard-blocks workspace-mutating tool calls at
  runtime**.
- **`/rubber-duck` is real** (hyphenated) — GA per changelog 2026-06-02. A built-in
  reviewer agent over the session's current plan/design/implementation — **not a
  diff or PR reviewer** — whose critic runs on a model from a *different family*
  than the session orchestrator (changelog 2026-05-07). Fires automatically and via
  `/rubber-duck`.
- **`/orchestrate` is a Copilot desktop-app command, not a CLI one** (github.blog
  slash-command guide, 2026-08-06). The CLI analog is **`/fleet`** (github.blog,
  2026-04-01): orchestrator decomposes an objective into dependency-ordered work
  items dispatched to sub-agents with **isolated contexts on a shared filesystem,
  no file locking** — last write wins, silently. `.github/agents/` definitions can
  serve as the sub-agents.
- **The hooks reference has grown past `COPILOT.md`'s record**: events now include
  `permissionRequest`, `preCompact`, `errorOccurred`, `notification`, and
  `subagentStop` — the last **blocking-capable**, alongside `preToolUse`,
  `permissionRequest`, and `agentStop`. A documented **exit-2-equals-deny** path
  exists for `preToolUse`/`permissionRequest` (stderr shown to the model; exit 2
  denies even if stdout says allow). Timeouts still always fail open. Org policy
  hooks (`policy.d`, cannot be disabled) exist; cloud agent honors only the `bash`
  field.
- **Skills discovery and frontmatter**: unchanged from `COPILOT.md`'s record
  (`.github/skills`, `.claude/skills`, `.agents/skills`; `name`/`description`
  required). `/skills reload` and `/skills info <NAME>` exist. Custom slash
  commands from prompt files remain unsupported (`#618` still open).
- **`COPILOT.md` is stale in named places**: "parallel fan-out is still
  undocumented" (it is `/fleet`, April 2026); the events list; the deny channel.
  Its own closing rule applies — a capability table whose date never changes is a
  table nobody rechecked.

### 37.2 The framing the batches serve

The parity worry runs the opposite direction from the obvious reading: **Copilot is
currently the more-enforced CLI** (gate hook + both TDD guards, deny-proven);
Claude Code has the gate hook only, with the guard port deferred on two
undocumented payload facts (§31.12). And §33's field evidence stands: every
mechanized rule held, every prose-only rule bent. So the plan's through-line is not
"protect Copilot" but **convert existing prose promises into machine records or
machine refusals, on both CLIs** — and extend verification to the one thing no
current check sees, whether guidance *activated* at all (§31.1: presence is not
process; R5.6's sweep still reads self-reported evidence).

### 37.3 OBS — the observability batch (first)

| # | Item | Files | Effort |
|---|---|---|---|
| OBS.1 | `COPILOT.md` re-verification: `/fleet` supersedes the fan-out claim; events list extended (incl. `subagentStop` blocking); exit-2 deny channel; plan-mode facts; provenance dated | `COPILOT.md` | S |
| OBS.2 | Operator-lever paragraphs: `/rubber-duck` as an optional deepening (analogous to `pr-review-toolkit` on Claude Code — the kit owns its reviewer, per PORT; a feature the kit can neither configure nor verify is a lever, not a step) and plan mode's hard-block as a read-only wrapper for survey/gap-analysis work | `COPILOT.md` | S |
| OBS.3 | **Skill-activation ledger** — a logging-only hook on the skill-invocation tool, both CLIs, writing one line per activation (skill name, session, timestamp); the retro's step-evidence sweep (R5.6) gains it as a machine evidence source | hook templates, `sdlc-setup.md`, `sdlc-retro.md`, `GATE_RECIPES.md`, `sdlc-update.md` | M |

**OBS.3's pre-registered probes, before any design** (§5's rule; the display-name
trap of §31.7 is the precedent — the UI label is never the hook name):

- **P1 (Copilot):** does invoking a skill fire `postToolUse`, and under what
  `toolName`? The builtin tool list names a `skill` tool; measured, not assumed.
  Bench: `copilot-ci-test` (§29.3, standing).
- **P2 (Claude Code):** does invoking a skill fire `PostToolUse`, and under what
  tool name (`Skill`?) — and what does its `tool_input` carry? This probe is cheap
  and independent of the guard-port probe, but the two can share a bench session.
- Either probe failing to fire is itself the finding: the ledger ships only for the
  CLI where activation is observable, and `SDLC.md` says which (inv 15 — a
  verification step names the environment it verifies against).

**OBS.3 build decisions to make explicitly, not by omission** (R5.2's durable-home
decision is the precedent): where the ledger lives (`.git/` is per-clone and
machine-local — acceptable for a retro that runs on the working clone, but the
retro must say so when citing it); whether the ledger hook joins the existing gate
hook's config file or ships as its own; and the update path (project-owned like
every hook — offered by `/sdlc-update` to projects that missed it, never installed
unasked, per §31.14's two-state rule: a decline is recorded with its date).

Why OBS is first: pure logging — no deny, no timeout hazard, no false-block risk —
and it gives every deletion clock (§16 regime) and R5.6's table ground-truth
denominators before the enforcement batch adds new rules to audit.

### 37.4 VER — the verification batch (second)

| # | Item | Files | Effort |
|---|---|---|---|
| VER.1 | **Close-out evidence checker** — a script that parses the slice commit body for the R5-mandated record (`RED:` / `quality:` / `mutation:` / `verify:` lines, each present or carrying its stated-skip form) and fails loudly on silent absence; `/end-slice` runs it as its own step and quotes its output (both CLIs, evidence-producing) | checker script template, `end-slice.md`, `SDLC.template.md`, `sdlc-setup.md` | M |
| VER.2 | **Claude Code guard port** — opens with the §31.12 pre-registered probe run: log a real `PostToolUse` payload for a deliberately failing Bash command, and real `PreToolUse` payloads for an `Edit` and a `Write`; the state machine is designed from what they contain. Banked facts: `$CLAUDE_PROJECT_DIR`, stated Git Bash shell — no self-locating prelude, no WSL hazard. Unknowns the probe must answer: exit-code availability and form, write-path field, `stop_hook_active` equivalent, block cap, `PreToolUse` timeout direction | probe first; then guard templates, `sdlc-setup.md`, `GATE_RECIPES.md`, `settings.template.json`, `sdlc-update.md` | L |
| VER.3 | VER.1's enforcement wiring, ramped: an `agentStop` hook that would-block when the session's slice commit lacks the record — Copilot first (schema proven, §31.11), Claude Code only after VER.2's port proves the `Stop` dialect | guard/hook templates | M |

VER.1 before VER.3, and logging/step-form before any block — the ENF ramp
discipline (§31.8→§31.10) applies unchanged: pre-registered criteria including a
value criterion, the owner reads each report before the next step, nothing enters
the installed set unproven. VER.2's port, if its probe surprises (as Copilot's
did — the exit code arrived as a text trailer nobody predicted), redesigns rather
than approximates.

### 37.5 JUDGE — queued behind VER, not scheduled

The LLM-assisted layer, for the contracts a script can verify *structurally* but
not *semantically* — the canonical case: is a `change-verify` transcript block real
output or a characterization wearing a result's clothes (COPILOT.md hazard 4's
tell, currently detected by prose instruction only). Design constraints recorded
now so the batch inherits them:

- **Never inside a timeout-bound tool hook** — hook timeouts fail open on both
  dialects, so an LLM call there is a check that silently stops checking under
  load. A judge runs as a command step with its own evidence contract (verdict
  quoted, rubric named), or at most at `agentStop`, where slowness degrades to
  not-blocking rather than to a fake pass.
- **Headless invocation exists on both CLIs** (`copilot -p`, `claude -p`); the
  cross-model-family pattern is the one GitHub itself shipped as rubber duck.
- Fixed rubric, forced verdict-plus-quotation output, logging ramp first, §16
  deletion clock attached from day one. Waits until VER.1 exists: judge what the
  script cannot parse, not what it can.

### 37.6 Considered and held (recorded so it is not rediscovered as a proposal)

- **`/fleet` for the kit's sweeps**: would obsolete the serial-sweep caveat, but
  the no-locking shared-filesystem model is a silent last-write-wins hazard, and
  whether the TDD guards even fire inside sub-agents (`preToolUse` in a sub-agent?
  `subagentStop` vs `agentStop`?) is unmeasured. A bench question before any use;
  OBS.1 records the capability, nothing builds on it.
- **Plan mode wrapping `/plan-phase`**: the plan artifact lands in the session
  folder, not the repo — against the evidence-on-disk directive — and the
  hard-block would prevent writing `spec/`. At most it wraps the reading half;
  recorded as an operator note in OBS.2, not process.

### 37.7 Order, halts, and regime

OBS then VER, each sized for one session; JUDGE queued. Every bench probe is
pre-registered before code (§5, §13 shape); the owner reads every probe and trial
report before anything enters the installed set (§4 — the F3 step, unskipped).
New placeholders are taught to setup in the same batch (inv 1). New hooks are
project-owned, offered never imposed, with the §31.14 decline-record rule.
`/kit-check` before each release; release timing the owner's call. All new rules
enter the §16 audit clock — counted in field arcs, per the standing re-denomination
note at the top of this file.

---

## 38. OBS built — 2026-08-07, probes answered, and a launcher-route discovery that
## outranks the batch

All three OBS items built in one session, §37's discipline held: the §21 build-time
re-verification ran before any edit, the P1/P2 probes ran before any ledger design,
and two of the ledger's three designs died on the bench before the third proved out
live in all three environments. Nothing is released: `VERSION` reads 0.17.0, the
manifest is deliberately stale (inv 10 — regenerated in the release commit), and
`/kit-check` is owed before the tag.

### 38.1 OBS.1/OBS.2 — the re-verification moved more than expected

Every §37.1 capability fact was rechecked against live sources; `COPILOT.md` §-dated
throughout. Confirmed as recorded: `/fleet` (with the no-locking hazard verbatim from
the blog), `/rubber-duck` (GA, cross-family, conversation-only), `/orchestrate` as an
app command, the fourteen-event hooks reference (exit-2 deny channel, fail-open
timeouts even for policy hooks, `policy.d`, the cloud agent's `bash`-only subset).
Two claims **did not survive**: `#618` is not open — closed 2026-03-05, prompt files
*declined* in favour of skills, so the SKILL.md packaging is now permanent by
upstream decision rather than provisional; and `#3820` closed completed 2026-06-17 —
the hooks reference now carries a *Tool names for hook matching* section plus a
Claude-name mapping table, which corroborates the bench vocabulary (its own Edit row
maps to `apply_patch`) without displacing it. New small facts recorded: `/skills
reload` and `/skills info` exist (the "listing needs a fresh session" claim in
`SKILLS.md`/setup was stale on Copilot and is now per-CLI); `disable-model-invocation`
on skills is community-claimed only, documented nowhere official, and per the
hazard-1 precedent presumed silently ignored — bench probe first if ever wanted.
OBS.2's two operator-lever paragraphs are in `COPILOT.md`: `/rubber-duck` (a lever,
not a step — conversation-only output cannot satisfy an evidence-shaped step) and
plan mode (session-folder artifact, press-sourced hard-block, and the MCP-connected
exception that makes its read-only guarantee conditional).

### 38.2 The probes — both answered favourably, in one run each plus one design probe

- **P1 (Copilot 1.0.78):** skill invocation fires `preToolUse` **and** `postToolUse`,
  `toolName: "skill"` — absent from the docs' new tool-name list — with `toolArgs` a
  normal JSON-encoded string. **Relevance-based activation logs identically to
  explicit invocation** (measured, one run each), which is the case the field defect
  (§31.1) is actually about. Payload carries its own `timestamp`; no trailing newline.
- **P2 (Claude Code):** `PostToolUse` fires under `tool_name: "Skill"`,
  `tool_input.skill` structured; snake_case payload with `session_id` but **no
  timestamp** — the hook stamps its own.
- **Design probe:** the hook process's cwd is the session's cwd, in the executing
  shell's own path flavour — which became the ledger's root-finding mechanism.

### 38.3 The discovery — the hook shell is per-launcher, and the WSL route corrupts
### hook bodies

Found because the ledger's first live proof failed (§31.16's lesson paying out
again): **the hook shell follows the launching shell's `PATH`.** PowerShell launch →
WSL bash; Git Bash launch → Git Bash — same repo, same day. And the WSL launcher
**re-parses the hook command line**: backslash-carrying bodies arrive corrupted and
`$(cat)` returns empty while a bare `cat` receives the payload (reproduced offline:
`wsl.exe bash -c <body>` fails where `bash body.sh` inside WSL succeeds,
byte-identical). Second observed consequence: a `/mnt/…` path that works from a
PowerShell launch makes the same `preToolUse` hook **error and fail closed** — a
denied tool call — from a Git Bash launch.

**This resolves the §31.7.5/§31.17 tension** (how could hook-bash-is-WSL and the
guards' live proof both be true: different launchers) — and it means **the shipped
TDD-guard JSON prelude silently no-ops on the WSL launcher route**: `$(cat)` +
backslashed `sed`/`tr` is exactly the corrupted shape, and the prelude exits 0
quietly by design. The bench ran the natural experiment inside one day: of the day's
sessions, guard-log lines came from exactly the one launched from Git Bash and from
none launched from PowerShell. Recorded in `GATE_RECIPES.md` and `COPILOT.md`'s
provenance; the *hook environment* section now states the per-launcher rule and
requires the probe be run from the CLI launched the way the operator actually
launches it. The fix was built same-session at the owner's direction — §38.6.

### 38.4 OBS.3 — the ledger as built and proven

One line per activation — ISO-8601 UTC stamp + raw payload + hook-added newline
(the payloads' missing trailing newline would otherwise concatenate the file into
one unparseable line) — appended to `.git/sdlc-skill-ledger.jsonl`. Copilot dialect
`templates/skill-ledger.template.json` → `.github/hooks/sdlc-skill-ledger.json`,
verbatim, no values: the body is backslash-free, parses nothing, pipes `cat`
straight into the file, and keys on the measured cwd fact with a loud not-at-root
branch — primitive by *necessity*, per 38.3 (two cleverer designs measurably died:
the guard-style prelude, then a `$(cat)`-based body that logged an empty payload).
Claude dialect: a `"Skill"`-matcher block in `settings.template.json` (stated shell,
no boundary — `$(cat)` legal there), removed by setup on decline. Both loud when
they cannot write. Wiring: offered (never imposed) at setup step 6 with
`{{SKILL_LEDGER_NOTE}}` under the §31.14 two-state rule (inv 1: setup taught in the
same batch, including the step-2 enumeration); `/sdlc-retro`'s step-evidence sweep
reads it as machine evidence with the per-clone caveat stated; `/sdlc-update` gains
the 0.18.0 offer-when-absent branch; recipe in `GATE_RECIPES.md`; both READMEs and
the update command's absent-only-writes list extended (inv 8/9).

**Proof:** `tools/skill-ledger-check.py` — cases derived at run time, both dialects,
loud branches run dirty, plus a case pinning the body's no-backslash property so the
boundary hazard cannot be silently reintroduced. All green. **Live:** three
environments, one full line each — Copilot/WSL route (session `371731bd`),
Copilot/Git-Bash route (`920504fc`), Claude Code (`54999703`). Bench-side record and
reversal list in the fixture's `ENF_PROBE_NOTES.md`.

### 38.5 Owner decisions owed *(item 1 executed same day at the owner's direction — §38.6)*

1. **The guard-prelude fix** (38.3) — ~~its own small batch~~ **built and proven,
   §38.6.** What remains of it is the field half: the apply-by-hand notes are written
   into `sdlc-update.md` and the root README, and `ai-news-dashboard` runs the old
   config until their next update's halt delivers it.
2. **Release 0.18.0** — this batch is release-shaped (new template, new placeholder,
   setup/update/retro wiring, the guard fix). `/kit-check` before the tag; manifest
   regenerated in the release commit; the `sdlc-update` transition notes are already
   written.
3. **VER remains next** per §37.7 — unchanged, except VER.2's Claude-side probe can
   reuse the P2 bench, and 38.3's boundary rule now binds every VER hook body.
4. **New, found while fixing the guards: the Copilot gate hook is exposed to the same
   boundary, and its symptom lies.** Its logic is embedded in the JSON body (the two
   parser sources, backslash-dense), and the measured failure on the WSL route is a
   *false diagnostic* — "no JSON parser (python or node) on the PATH" emitted on
   every edit with python present, because the corruption breaks the body before
   parser detection runs. A structural fix (split the body into a script file, guards-
   style, leaving only a bare launcher line in the JSON) touches the template pair,
   setup, update classification, and `tools/gate-hook-check.py`.
   *Executed same day at the owner's direction — §38.7.*

### 38.6 The guard-prelude fix — built, proven offline and on both launcher routes,
### 2026-08-07 (same session, owner-directed)

The ledger's shape applied to the guards, template-first:

- **`tdd-guard.template.json`**: each of the three hook bodies is now the bare
  `if [ -d .git ] && [ -f .github/hooks/sdlc-tdd-guard.sh ]; then cat | sh … <mode>; fi`
  — zero backslashes, zero `$`, zero quote characters, nothing for the boundary to
  eat. The JSON passes no `SDLC_REPO_ROOT` (any expansion is boundary-exposed);
  root-finding moved into the script.
- **`tdd-guard.template.sh`**: when `SDLC_REPO_ROOT` is unset it now trusts the
  working directory **only if `.git` sits there** (the measured cwd fact), else
  no-ops; an explicit `SDLC_REPO_ROOT` still wins, which is what the offline harness
  uses. The header comment states the boundary reason so the shape reads as a
  constraint, not a style choice.
- **Suite** (`tools/tdd-guard-check.py`): five new cases — the boundary-property
  case pinning the no-backslash/no-`$`/no-quote shape of every hook body (so the
  prelude cannot be silently re-cleverified), prelude-at-root piping the payload
  end-to-end into the script, prelude-away-from-root silent with no deny and no
  state, and the script's two no-env cwd branches — plus an eighth mutation (drop
  the `.git` check when defaulting → caught by the no-op case). **31 cases green
  under both parser dialects; all 8 mutations caught.**
- **Bench, both routes, all three events**: PowerShell/WSL route (session
  `961a8634`) — `RED observed (exit 1)` and a stop-check would-block, the lines this
  route never produced under the old config; Git Bash route (session `e74b8062`) —
  a pre-write `VIOLATION` and the stop-check. The bench's installed pair is updated
  (JSON replaced verbatim; the script's root-defaulting block hand-applied — the
  same two motions the field will make).
- **Docs**: `GATE_RECIPES.md`'s known-limit note replaced by the fixed design with
  the natural-experiment evidence; `COPILOT.md` provenance updated (guard fixed
  same-day; gate hook named as the remaining exposed artifact); the 0.18.0
  transition note in `sdlc-update.md` and the root README's update section both
  carry the two hand-apply motions and the consequence of skipping them.

What deliberately did **not** ship: the gate-hook fix (38.5.4 — structural, its own
batch) and any change to the Claude-side dialect, which has a stated per-hook shell
and no launcher boundary to survive. *(The former was then executed the same day at
the owner's direction — §38.7; the Claude-side non-change stands.)*

### 38.7 The gate-hook split — built, proven offline and on both launcher routes,
### 2026-08-07 (same session, owner-directed)

§38.5.4 executed: the Copilot gate hook is now the same shape as the guards — logic
in a script file that never crosses the launcher boundary, a bare launcher in the
JSON.

- **`templates/copilot-hook.template.sh`** (new): the old JSON body's logic verbatim,
  unescaped into a readable script — parser detection, `emit`, the patch-text/JSON
  payload parse, the loud did-NOT-run branches, the 8000-char cap — plus every
  placeholder (`{{SOURCE_GLOB}}`, `{{HOOK_LINT_CMD}}`, `{{HOOK_TYPECHECK_BLOCK}}`),
  and one behavior the live proof forced: **`resolve_path`**, the guard-proven
  drive-letter translation applied to each touched file and to the payload cwd. The
  first WSL-route live run failed honestly without it — the patch header carried an
  absolute-Windows path that does not exist as written under WSL bash (31.9.1's
  both-forms fact reaching the gate's existence check; the old body never got far
  enough on that route to meet it).
- **`copilot-hook.template.json`**: now the bare launcher
  (`if [ -d .git ] && [ -f .github/hooks/sdlc-gate.sh ]; then cat | sh …; fi`) —
  no backslash, no `$`, no quotes, no placeholders; verbatim copy, only `timeoutSec`
  ever edited.
- **Proof.** `tools/gate-hook-check.py` reads the Copilot body from the script
  template; all previous cases pass unchanged (the split is behavior-preserving),
  plus the launcher boundary-property case (pinning the no-backslash/no-`$`/no-quote
  shape), launcher wiring at a repo root, launcher silence elsewhere, and a
  backslashed-path normalization case — green under both parser dialects. Boundary
  repro: the launcher through `wsl.exe bash -c` — the exact call that produced the
  false no-parser message from the old body — runs the gate and returns real lint
  output. **Live, both routes**, with the session quoting the injected feedback and
  the transcript confirming it verbatim: WSL route (session `bc5413ff`) —
  `lint/typecheck failed … /mnt/d/…/lintprobe.js` (the `/mnt` form: resolve_path
  working); Git Bash route (session `a17ec507`) — same failure in `D:/` form. Bench
  gate artifacts removed after proof; record and reversal in `ENF_PROBE_NOTES.md`.
- **Ripples, derived by grep (§4a):** setup step 6 (instantiate the `.sh`, copy the
  `.json` verbatim) and its close-out `{{` scope (now `sdlc-gate.sh`; neither `.json`
  launcher in scope); `sdlc-update` ownership row + a 0.18.0 gate-restructure
  transition note (hand-apply: read the `{{HOOK_*}}` values out of the current JSON
  before replacing it) + a forward pointer from the 0.16.0 note so nobody re-applies
  the superseded single-JSON body; both READMEs (tree, ownership, update section);
  `GATE_RECIPES.md` (intro, dialects table, the known-limit note replaced by the
  fixed design); `COPILOT.md` (mapping table, gate-hook section, provenance).

With this, every Copilot-dialect hook the kit ships — gate, guards, ledger — is
launcher-boundary-proof by construction, and each shape is pinned by its proof
suite. The Claude-side dialect keeps its single-file form: its shell is stated
per-hook, so there is no boundary to survive.

### 38.8 The pre-0.18.0 `/kit-check` — run 2026-08-07; twenty-four findings fixed
### in-session, seven deferred with a record

Full 15-invariant pass: four mechanical checks in-session, the twelve semantic
invariants fanned to five read-only readers (the inv 5+6+7 reader died on a session
limit before reporting; that pass's delta since §34's full green was covered
in-session — its one catch was the missing skill-ledger row in `COPILOT.md`'s mapping
table). Every reader finding was re-verified against the tree before any edit.
Invariants 6, 11 (core), 12 (purity of the tree itself) pass clean; inv 10 was
expected-stale with discrimination proven (exactly the batch's 12 edits plus the two
new templates), regenerated in the release commit.

The pass earned its keep on the two invariants that keep catching their own
custodians:

- **Inv 4's census caught this session's own `{{HOOK_*}}` leak into `sdlc-update.md`**
  (the §31.14-era specimen, recurring), and **inv 13 caught its own stale denominator
  a second consecutive release** — neither §38 batch had extended the ledger's list;
  it now carries the skill-ledger proof step, the skills-listing check, and the deploy
  verification, and `kit-check.md`'s copy is re-stamped 0.18.0.
- **The §31.15 no-resolver specimen recurred in the ledger offer**: the
  resolve-`{{SKILL_LEDGER_NOTE}}`-on-every-adoption bullet sat structurally inside
  "If accepted:", unreachable on a decline — found independently by two readers.
  Restructured to the guard note's unconditional shape, with the decline-artifact
  check made explicit.
- **The update's ledger clause had dropped the guard clause's own correction**: the
  artifact-present branch never read the record, so present-but-recorded-as-declined
  — a contradiction the clause itself names — was unreachable. Fixed; and setup's
  decline path now states the artifacts must actually be absent.
- **The per-launcher discovery propagated into the paper trail**: `{{HOOK_ENVIRONMENT}}`
  now records the launch route first; every hook proof (gate, guards, ledger) and the
  probe itself name "launched the way this project's operator actually launches it";
  the `timeoutSec` basis records the route it was timed on; the update's re-probe is
  standing at every hook-touching crossing rather than trapped in the 0.16.0 note;
  and setup's superseded per-machine framing is rewritten.
- **Inv 14 parity**: the ledger note now names the hook artifact that makes
  "installed" true (per CLI) plus the update-this-line-or-nothing-will sentence, the
  guard note's own discipline.
- **Negative cases stated for three checks that lacked them**: the deploy
  verification (`deploy NOT verified — <what was seen>`, a halt-5 fact), the retro's
  ledger read (a silent ledger reports "hook health unknown", never per-skill
  no-evidence — the confident-plausible-wrong shape), and the ledger/guard/gate
  proofs' route qualification above.
- **Inv 1/2 sweep**: the gate parenthetical asserting a three-leg gate is now "the
  steps recorded there, in order"; `gh pr merge --merge` no longer asserts the
  project's merge strategy; `/code-review ultra` carries its Claude-Code-only
  qualifier at phase end; the commit-subject convention gained its canonical template
  home; "the same way the adoption landed" dropped (false for New-mode adoptions);
  the update's no-project-writes rule states its accepted-re-offer exception with the
  Claude-side merge path; the retro's four-state vocabulary is enumerated as four.
- **Inv 8/11/12 sweep**: README↔update parity restored (step-5 list gains
  `sdlc-gate.sh`; the re-probe and the 0.16.0→0.18.0 skip-ahead now exist on both
  sides; ownership rows match; copy-directories-not-files stated for humans);
  python-pro's self-declared-MIT status no longer flattened to "all MIT" in three
  places; the bundle README's verbatim-template count corrected to four; the new
  gate script template's `FEATURE_PLAN` citation removed (inv 12's exact shape, in
  an instantiated file) and `COPILOT.md`'s §37 citation made self-contained.

Seven below-threshold observations recorded in `IMPROVEMENT_PLAN.md` §11. Suites
re-verified green after the fixes (gate, ledger; guard inputs untouched since their
green run). **0.18.0 released the same day — the release record is the CHANGELOG
entry and the tag.**

---

## 39. Second adopter on 0.18.0 — same-day update, every new branch field-executed,
## 2026-08-07

Adopter-side session (`ai-news-dashboard`), hours after the release. Two commits,
merged to their `main` (PR #6, merge `09f7403`):

- **`/sdlc-update` 0.17.0 → 0.18.0 ran clean end to end** (`c3a64c0`): 17/17
  installed files `UNCHANGED` both directions — second consecutive zero-drift update
  — with the denominator proven and discrimination proven the cheap way this time:
  six files changed content between releases, so the same all-`UNCHANGED` verdict
  against both manifests is itself the discrimination evidence. Kept-bundle
  enumeration was exactly the 0.17.0 manifest (35 on disk = 34 + the manifest
  itself), replaced by copy-over-in-place and re-verified with `sha256sum -c` against
  the target. Nothing project-owned touched beyond the halt-approved hooks and the
  two allowed spec lines, verified by reading the final diff against the ownership
  table.
- **All three 0.18.0 hand-applies landed and were proven on the recorded route.**
  The gate restructure (bare-launcher `sdlc-gate.json` + new `sdlc-gate.sh` carrying
  their values read out of the old JSON — glob `*.java`, the mvn lint command, empty
  typecheck per the recipe's stated case) and the guard pair (`.json` verbatim,
  inheriting the offline proof; the root-defaulting diff atop their 0.16.1-fixed
  `.sh`). Proofs all ran from a Git Bash launch — the route their spec records as the
  operator's: the re-probe matched the 2026-08-06 record exactly (no moved answer, no
  finding), the gate proved both directions (star-import → verbatim Checkstyle
  feedback; revert → silence), and the proof session's guard log showed the new
  launcher firing live (two `pre-write` VIOLATIONs + a stop WOULD-BLOCK from the
  deliberate edit — deny disarmed for the proof run, re-armed after, arming record
  untouched and still true).
- **The ledger offer-when-absent branch fired its first field case**: no
  skill-ledger line in their `spec/SDLC.md` → offered as a first setup would →
  accepted → installed → proof (an `sdlc-update` activation appended a ledger line
  carrying that session's ID, read back in the same proof) → recorded in
  `spec/SDLC.md` with the artifact-names-and-per-clone content the template note
  prescribes.
- **The spec fold-in landed in the same PR** (`4d4b8be`, on the owner's word after
  the update flagged it): the gate-hook paragraphs now carry the launcher + script
  split with its why, the re-proof, the route-first `{{HOOK_ENVIRONMENT}}` shape, and
  a `timeoutSec` basis naming its route; `CLAUDE.md`'s one-line hook reference
  updated to match. So this adopter's spec disagrees with its commands nowhere.

Worth banking: every branch 0.18.0 added to `/sdlc-update` got a real execution on
release day — the three hand-applies, the route-named proofs, and the ledger offer's
no-line-at-all state. The offer's other states (recorded decline, both contradiction
directions) remain field-unexecuted, reachable only on adopters with different
histories.

---

## 40. The silent-refusal fix — first extraction from the Phase 03 guard friction,
## 2026-08-08

The adopter's first armed BUILD day on 0.18.0 produced three TDD-guard friction
specimens (their `spec/PROJECT_INDEX.md` friction log, four entries dated
2026-08-08), and the session's own hook feedback, adversarially triaged there: two of
its four premises false against the guard source (compile-failure reds and `-Dtest=`
selectors already count — the guard reads exit codes only; both beliefs grew from
compound-refused runs being misattributed), one defect confirmed, two gaps found by
the triage itself that the feedback missed.

**The confirmed defect is fixed on the owner's word, ahead of the retro report:**
`observe-test` refused a run (compound command, or no exit-code trailer) by logging
to `guard.log` and emitting nothing — the session learned only at the next
unexplained deny, and every misattribution above grew in that gap. Both refusal
shapes now emit the reason plus what IS allowed as postToolUse `additionalContext`
(the gate hook's measured schema); counted runs stay silent. Suite: 35 cases (was
31), ninth mutation added — re-silencing the refusal must be caught — offline proof
green both dialects. CHANGELOG carries it under *Unreleased* as adoption-only with
the hand-apply note.

**Queued, deliberately not changed** — these arrive with the adopter's retro report
so the fix batch works from a filed report, not a memory: (a) G2's green is
pattern-based, so a targeted single-test green satisfies the stop guard
(process-covered by the end-slice gate; documentation gap at minimum); (b) the
separator list lacks single `&` — the field's `cmd /c "… & …"` probe was refused by
the `;` inside its `PATH` value, luck not design; (c) the deny message could carry
the last refusal reason; (d) disposal-intent reds (a red written to be deleted after
licensing the write — observed in-session, `@SpyBean` on an internal bean against
their mock policy) named as review-lens territory, not guard territory.

**§40.1 — the refactor license, second same-day extraction on the owner's word
(2026-08-08).** The S3 end-slice produced the fifth friction specimen, and the
sharpest: during `change-simplify` the session derived the full synthetic-red recipe
(edit test → red → revert → production edit, with timestamp-staleness analysis),
briefly committed to it, then dropped its only candidate move as not worth the
dance — observed by the owner in the reasoning stream, recorded into the adopter's
friction log by hand, since the session's own reporting cannot see what it *almost*
did. The structural gap none of (a)–(d) named: G1 encoded only one of TDD's two
licenses — a fresh red for new behavior — and had nothing for the refactor leg,
so the kit's own close-out passes (`change-simplify`, mutation testing) were either
taxed into dropping legitimate moves or normalized into synthetic cycles (three
consecutive slices). Fixed ahead of the retro report at the owner's direction: G1
now also licenses a production write while `.git/sdlc-tdd/refactor-license` exists
**and** a green has been observed this session — the session's own logged one-line
declaration, revoked by a test edit, session-scoped, surviving reds on purpose
(mutation reverts; G2 still refuses a red stop). A naive green-license was
considered and rejected: the suite is green at the start of every cycle, so green
alone would license test-last production code everywhere. Suite: 42 cases (was
35), three new mutations (bare declaration must not license; revocation must not
drop; no cross-session leak) — twelve total, green both dialects. CHANGELOG
*Unreleased* under **Added**, adoption-only, hand-apply note; field-applied to
ai-news-dashboard the same day (their `spec/SDLC.md` guard section, second
same-day patch paragraph). Items (a)–(d) stay queued; (d)'s disposal-intent lens
now has a smaller surface, since the honest path no longer prices worse than the
synthetic one.

---

## 41. sdlc-kit#5 triaged against the tree — two shipped, one fixed by its own
## sibling, two open with verified fix shapes, 2026-08-08

The Phase 03 retro is filed (`sdlc-kit#5`, five findings from the adopter's
`spec/SDLC_RETRO_2026-08-08.md`, damage-ordered), which is what §40's queue was
waiting for. Every finding checked against kit main before any fix work:

- **Findings 1–2 — already shipped unreleased** (§40 the spoken refusal, §40.1 the
  refactor license). The issue's closing line ("they should ship in the kit
  template") is satisfied on main; both CHANGELOG *Unreleased* entries carry the
  hand-apply note.
- **Finding 3 — fixed by §40's own message, ahead of the filing.** The refusal
  context already says "Flags and single-test selectors are fine — to trim output
  use the runner's quiet flag, not a pipe." The finding's asked-for
  `Allowed: mvn test, mvn -q test -Dtest=Class#method` examples are the adopter's
  instantiation of that sentence, not the template's to state: the template is
  project-agnostic and cannot name `mvn`. No change.
- **Finding 4 — confirmed against source, open** (= §40's queued (a)):
  `observe-test` touches `green-observed` on any counted green, so a `-Dtest=`
  single-test green satisfies G2's stop check. Two fix shapes, both verified
  against the tree: **(A)** teach the guard to distinguish full-suite green —
  needs a per-project selector-marker placeholder, so template + setup interview +
  suite growth (invariant 1's full cost) for a backstop the end-slice gate already
  covers; **(B)** state the division of labor where the guards are documented —
  G2's green is *any* counted green, the full-suite guarantee is the gate's job at
  end-slice — in the guard header and the `{{TDD_GUARD_NOTE}}` text. (B) matches
  the guard's own philosophy (cooperative backstop, never runs tests inline) and
  §40's triage note ("process-covered by the end-slice gate"). Recommended: B.
- **Finding 5 — confirmed, and the fix belongs in the guard note, not the vendored
  skill.** The bare-command rule appears nowhere a session reads at slice time:
  `skills/tdd/SKILL.md` and `SDLC.template.md` never state it (checked — the only
  mention outside the guard's own messages is a GATE_RECIPES.md aside). Editing the
  vendored skill would diverge it from upstream (inv 3) and impose a guard-only
  rule on adopters who declined the guards; the right home is the
  `{{TDD_GUARD_NOTE}}` text setup resolves into `spec/SDLC.md` exactly when the
  guards are installed. The disposal-intent-red half (= queued (d)) is a review
  lens, not guard logic: a `REVIEW_LENSES.md` line naming tests written to be
  deleted after licensing a write — surface already smaller post-§40.1, still
  worth the lens since the recipe was derived in-session once.
- **Kit-found extras the retro does not file**: **(b)** single `&` missing from
  the separator list stands (line-verified: `*"&&"*` matches only the double form,
  and the field's `cmd /c "… & …"` probe was refused by the `;` inside its `PATH`
  value — luck, not design) — one-line pattern fix plus a suite case; **(c)**
  deny-carries-last-refusal-reason is largely mooted by §40's spoken refusal —
  proposed below-threshold → `IMPROVEMENT_PLAN.md`.

**Proposed batch, smallest-first**: (b)'s separator fix + suite case; finding 4's
(B) documentation; finding 5's guard-note sentence + review lens; (c) recorded
below-threshold. Owner decisions owed: finding 4's shape (B recommended), and
(c)'s below-threshold call.

**§41.1 — batch executed, both owner decisions taken as recommended (same
session).** (b): the guard's separator classes are now single-character (`;`, `&`,
`|` — the doubled forms covered by containment), with the comment naming the
luck-not-design field fact; suite 44 cases (4e/4f: a single-`&` compound must not
count and must not record a false green) and a thirteenth mutation (regressing to
the doubled-only list is caught by exactly those two cases) — mutation pass green,
13/13 caught. Finding 4 (B): the any-counted-green division of labor is stated in
the guard header, GATE_RECIPES' G2 bullet (marked owner-decided), and the guard
note's required content. Finding 5: the two session-facing rules are required
content of `{{TDD_GUARD_NOTE}}` (SDLC template comment + setup's record-the-outcome
bullet — inv 2's both-sides rule); the disposal-intent lens added to
`REVIEW_LENSES.md` with its trigger in `/end-slice`'s conditional list, and
GATE_RECIPES' delete-the-test-afterwards honest limit now points at it. (c):
`IMPROVEMENT_PLAN.md` §12, with its revisit condition. CHANGELOG *Unreleased*
gains two entries (the separator fix adoption-only with the hand-apply note; the
documentation/lens work under **Changed**). Existing guard-running adoptions owe
two hand-applies: the separator fix and the guard-note extension.

---

## 42. G2 session-scoping — the owner's TDD-doctrine assessment, one gap confirmed,
## fixed same day, 2026-08-08

The owner assessed the process against TDD's own doctrine in three claims:
refactoring (simplification included) rides existing greens in small increments
rather than fresh reds; mutation testing follows only a completed red→green; and
`/plan-phase` writes no code, so the gates must not apply to it. Checked against the
tree: the first two are already the design — §40.1's declared refactor license is
claim one mechanized (the declaration being the only way a shell script can tell
"refactor on greens" from "test-last new behavior"), and the mutation check's
placement at `/end-slice` step 5, after gate and review, is claim two by
construction. Claim three was already true for the write-path guards — spec and
docs writes match neither `{{SOURCE_GLOB}}` nor the test pattern, an exemption by
file-kind rather than by command, which also covers code written mid-"planning" —
but it confirmed one real gap: **G2 fired on `agentStop` unconditionally**, so a
session with no production write and no test edit (`/plan-phase`, docs,
bookkeeping, `/sdlc-retro`, `/sdlc-update`) could not stop clean in deny mode,
refused for running no tests when it had no business running any. Logging mode
masked it as WOULD-BLOCK log lines nobody read back.

**Fixed on the owner's word, same session.** G1's pre-write now drops a
session-scoped marker (`.git/sdlc-tdd/prod-write-observed`) when a production
write actually goes through — the deny branch sets nothing on purpose, because a
denied write leaves the tree unchanged — and stop-check stands down when neither
the marker nor `last-test-edit` exists. A test edit alone still arms G2: a written
test never run is exactly the never-ran stop the guard exists to refuse. The
setup-time proof ("end a session with no green run, confirm a would-block") is
unaffected — its scripted session makes a production write first. Suite: 48 cases
(was 44; a no-writes session and a docs-only session stop clean deny-mode
included, a denied write arms nothing, a test edit alone blocks) and two new
mutations (dropping the stand-down; arming from the deny branch) — fifteen total,
proof green both dialects, 15/15 caught. Documented in all three homes that state
G2's rules — the guard header, GATE_RECIPES' G2 bullet, and the
`{{TDD_GUARD_NOTE}}` required content (template comment + setup bullet, inv 2's
both-sides rule). CHANGELOG *Unreleased* under **Fixed**, adoption-only with the
hand-apply note — existing guard-running adoptions now owe three hand-applies.

---

## 43. The pre-0.19.0 `/kit-check` — run 2026-08-08; fifteen findings fixed
## in-session, three deferred with a record, five discarded with reasons

Full pass, fanned out as six read-only agents over the eleven reading invariants,
mechanical checks run inline, every agent finding verified against the source before
any edit. Mechanical: inv 9 clean (tree matches, `sdlc-kit-process-flow.md`
included); inv 10 stale-as-expected (six bundle files since 0.18.0; regenerated in
the release commit as every release does); inv 4 clean (`{{` in `sdlc-setup.md`
only, exit-check scope exact); inv 6 delegated and clean (76 references, all
correct).

**The converged finding — three agents, three directions, one gap:** the refactor
license (§40.1) was stated nowhere a session reads at slice time. The
`{{TDD_GUARD_NOTE}}` required content claimed to exist for exactly that purpose and
named only two rules; setup's re-offer trade-off and `sdlc-update.md`'s 0.16.0
re-offer bullet still described pre-license, pre-scoping semantics ("block a stop
while the suite is red" — wrong denominator, no scoping); and the disposal-intent
lens pointed reviewers at the guard note for license content the note was never
told to carry. Fixed at the root: the note's required content is now three rules
plus the mode flag file, per-clone caveat, and proof record (template comment +
setup bullet, inv 2's both-sides rule); both stale descriptions rewritten to the
current semantics.

**Also fixed:** the §41 disposal-intent trigger added to `SDLC.template.md`'s lens
list (it was in `end-slice.md` only — the canonical file was the one missing it);
`/code-review` qualified Claude-Code-only in `end-slice.md`; commit recipe states
project-convention-wins; `next-slice.md`'s merge-drift gate run cites the recorded
definition; setup's close-out URL → the recorded *Kit home repository* line; the
Agent CLI present-but-wrong check in `sdlc-update.md` + root README (a recorded CLI
the artifacts contradict is a finding — the absent case was already handled, the
wrong case was trusted silently); root README step 6's "only lines" claim now
admits accepted-offer artifact writes and carries the do-them-last rule; bundle
README's project-owned list gains the ledger hook; the "four `{{HOOK_*}}`" count
corrected in `CLAUDE.md` + `KIT_INVARIANTS.md` (eight in the table plus two prose);
the retro's ledger-alive precheck added to inv 13's denominator list (ledger +
`/kit-check`'s copy, now "as of 0.19.0"); mutation check names its environment in
both homes; setup's final gate and measured violation counts name their shell;
`change-verify`'s re-entry pointer names step 3.

**Deferred with a record** (`IMPROVEMENT_PLAN.md` §13): `{{CI_DESCRIPTION}}` has no
reconcile step (inv 14); the hook-timeout basis vs `timeoutSec` has none (inv 14);
the per-project guard proof exercises two of three licenses, offline covers the
third (inv 13 residue, kin: the exit-check grep never demonstrated to fire).

**Discarded with reasons:** README step-6 "exception lacking" (partially refuted —
the offer-answer exception was present; the artifact half was real and fixed);
SKILLS.md line 8's "vendored from public repos" tension (self-corrects in the same
file; notices agree); the hypothesis-tests frontmatter "verbatim" question
(unverifiable offline; the one-word-diff record stands); Dungeon-Daddy examples in
the vendored tdd-references (divergence recorded — compliant; upstream-adaptation
choice, not drift); SKILLS.md's Dungeon Daddy mention (illustrative, harmless).

Released same session as 0.19.0.

---

## 44. FBK — hook feedback audited against the usable-context criterion, drafted
## 2026-08-09

Owner session. The prompt: every hook must produce usable context for the LLM — its
result described on success and on failure; a deny explaining exactly why and
restating the guard's purpose; a passed guard stating the next action only where that
action is exactly known. Assessed against the four hook artifacts themselves
(`settings.template.json`, `copilot-hook.template.sh`, `tdd-guard.template.sh`, the
ledger pair), not the walkthrough — `sdlc-kit-process-flow.md` was checked first and
matches the artifacts everywhere, including the subtle claims (session scoping, the
single-`&` rule, "none denies on its own failure"); the findings are in the hooks.

**What already meets the bar, verified so it is not re-proposed:** G1's deny message
(names the file, states both licenses and the way out of each, pre-empts the
compound-command trap); the §40 spoken refusals; every could-not-do-my-job branch in
every hook (loud, framed, never vacuously green). The criterion's hard part is the
success side, and one dialect asymmetry.

### 44.1 The findings, ranked

**FBK.1 — the Claude Code gate hook's lint-failure output is unframed; the Copilot
dialect's is not.** On lint/typecheck failure `copilot-hook.template.sh` emits
"SDLC gate hook: lint/typecheck failed on the file just edited. Fix it before
continuing: <file>" before the output; `settings.template.json`'s body does
`{ echo "$l"; echo "$t"; } >&2; exit 2` — raw linter output, no statement of which
hook produced it, which file it checked, or what is expected, plus a stray blank
line when the typecheck half is empty. §31.13 made this dialect loud on its
can't-run branches and never reached the one branch that fires most. Fix: port the
Copilot framing line (with the file name) and drop the empty-half echo. Suite:
`tools/gate-hook-check.py` gains the framing assertion on the Claude dialect's
failure case.

**FBK.2 — counted observations are silent; the guard's state machine is invisible
on the success side.** `observe-test` records RED/GREEN to the log only. §40 fixed
the identical failure shape for *refusals* after a field session thrashed against
invisible state; counted runs stayed silent as that fix's scope, and the same gap
remains pointed the other way: a session never learns its run WAS counted, so the
license it just earned (or the stop-guard satisfaction) is knowable only by the
next deny not arriving. This is also the one place the pass-side criterion applies
safely, because the next state is exactly known. Fix: emit the measured
`additionalContext` schema on each counted observation, phrased as state facts,
never instructions — one short line (the Core Rule is minimize context; a TDD loop
runs many tests):

- RED counted: `TDD ordering: RED counted (exit <N>). A production write is now
  licensed for this cycle.`
- GREEN counted: `TDD ordering: GREEN counted. The stop guard is satisfied;
  full-suite assurance remains the end-slice gate's job.` — the second clause is
  §41's (B) division-of-labor ruling, spoken where it applies, so a single-test
  green is never misread as gate-grade.

Suite: `tools/tdd-guard-check.py` cases for both messages plus a sixteenth
mutation — re-silencing a counted observation must be caught (the §40 ninth
mutation's symmetric twin). Copilot dialect only for now; VER.2's Claude port
inherits the behavior by porting the fixed script.

**FBK.3 — considered and subsumed: the G2 block message carrying observed state.**
The candidate (block reason reports "last counted run: none / RED at <time>") dies
to the same argument as `IMPROVEMENT_PLAN.md` §12.1: with FBK.2 shipped, every
transition — counted or refused — is spoken at the run itself, so the block never
arrives against a state the session was not told about, and a state dump would
re-read the log for a message already seen. Not built; §12.1's record is extended
to cover this shape rather than contradicted, same revisit condition (a field
report showing a session missing the spoken lines and thrashing at the block).

**FBK.4 — truncation is silent.** `emit()` caps `additionalContext` at 8000
characters with no marker, so lint output cut mid-error reads as complete. Fix:
when the cap bites, the capped text ends with a
`…[truncated by the gate hook at 8000 chars]` marker inside the cap. Suite: one
case with oversized dirty output asserting the marker.

**Deliberate silences kept, enumerated so each is a decision and not an omission:**
the gate hook on a genuine pass and on a non-source skip (fires on every edit; a
per-edit "passed" line is noise, and pass-vs-skip only matters at
trust-establishment time, which is what logging mode and the guard log are for);
G1's pass (the write proceeding is the feedback; the OK is logged); the ledger's
success (bookkeeping); G2's clean stop (terminal — there is no next action to
inform).

### 44.2 The batch

| # | Item | Files | Effort |
|---|---|---|---|
| FBK.1 | Frame the Claude gate hook's lint-failure output (file named, no empty echo) | `settings.template.json`, `tools/gate-hook-check.py` | S |
| FBK.2 | Spoken counted observations, state-fact phrasing, division-of-labor clause on GREEN | `tdd-guard.template.sh`, `tools/tdd-guard-check.py`, `GATE_RECIPES.md` (observe-test bullet), guard header | S |
| FBK.4 | Truncation marker in `emit()` | `copilot-hook.template.sh`, `tools/gate-hook-check.py` | S |

Ripples, to re-derive by grep at build time (§4a): `sdlc-kit-process-flow.md`'s
hook section (observe-test's counted-runs sentence goes stale the moment FBK.2
lands); the CHANGELOG *Unreleased* entries — all three adoption-only with
hand-apply notes, since every touched artifact is project-owned. No new
placeholders (inv 1 untouched); no `{{TDD_GUARD_NOTE}}` change (spoken
observations are feedback the guard gives, not a rule the session must follow —
the note's three rules stand); no §16 audit clock (messages are not process rules;
stated so the omission is not read as one).

**Checked against scheduled work, no conflicts found:** VER (§37.4) touches none
of these branches, and FBK-before-VER is the profitable order — VER.2's port then
carries the spoken observations instead of re-porting them later. §40's
"counted runs stay silent" was that fix's scope, not a standing decision; FBK.2
revises it on the owner's stated criterion, recorded here with its date. §12.1 is
extended, not contradicted (FBK.3). The §42 stand-down, §41's separator classes,
and the three-license structure are untouched. `ai-news-dashboard` currently owes
three guard hand-applies (§42) — if FBK ships before their next `/sdlc-update`,
FBK.2's joins them at the same halt rather than adding a second visit.

**Owner decisions owed:** (a) approve FBK.2's revision of §40's counted-silent
scope — the 2026-08-09 session's criterion is the basis, recorded here, not yet
ruled; (b) batch order (recommendation: FBK before VER, above); (c) the release
vehicle — the batch is fix-and-feedback shaped, 0.19.1-sized, owner's call.
*(a) and (b) approved as recommended, 2026-08-09, same session; (c) still open —
the CHANGELOG entries sit under Unreleased.*

### 44.3 Build record — 2026-08-09, suite-first, red observed before any fix

Executed in the kit's own discipline: every new case written first and watched to
fail against the unmodified artifacts before either hook changed.

- **Red observed, both suites.** Gate-hook suite: exactly the two new cases failed
  (the Claude framing assertion, the truncation marker), both parser dialects,
  everything else green. Guard suite: exactly the three new cases failed (5b — the
  flipped case, 7b, 20b) under both dialects, 50 cases total, and the two new
  re-silencing mutations reported STALE against the old source — which is the proof
  they target the fixed one. Nothing failed that was not supposed to.
- **One design delta against 44.1, forced by honesty: the RED message is
  state-aware.** The drafted single message ("a production write is now licensed")
  would be false in exactly case 20's shape — a red counted with *no test edit this
  session* is counted but licenses nothing (the §31.18 field circumvention is that
  gap). The shipped message claims the license only when G1 would grant one (test
  edit this session, or refactor-license + green); otherwise it says the red
  licenses nothing yet and why. Case 20b pins the negative direction: the spoken
  observation must never claim a license the guard would refuse — the
  confident-plausible-wrong shape, caught at design time.
- **Case 5b flipped rather than added.** Until this batch it pinned counted-run
  silence ("no context noise on the happy path") — §40's scope choice, enforced by
  the suite as designed. It now pins the spoken observation, with the comment
  recording the flip and its date.
- **Two mutations, not the drafted one** — silencing GREEN and silencing the REDs
  are separate regressions with separate witnesses (7b; 5b + 20b), so each gets its
  own mutation. Seventeen total.
- **Suites green after the fix:** gate-hook 56 checks across both dialects and both
  parsers, exit 0, including the new cases; guard suite 50 cases green under both
  parser dialects, all 17 mutations caught, exit 0. Both counts read off the runs,
  not asserted (§31.12's rule — a hardcoded count is the part that goes stale).
- **Ripples landed:** `GATE_RECIPES.md` — the spoken-observation paragraph after
  the G2 bullet, and the cap bullet now names the truncation marker (found by the
  §4a grep, not the plan's file list); guard header — the spoken-outcomes
  paragraph; `sdlc-kit-process-flow.md` — the observe-test bullet;
  `IMPROVEMENT_PLAN.md` §12.1 — extended per FBK.3, same revisit condition;
  CHANGELOG — three *Unreleased* entries, all adoption-only with hand-apply notes
  (every touched artifact is project-owned). The 0.19.0 CHANGELOG entry's "counted
  runs stay silent" stands as history; the new entry names itself the completion of
  that fix.

---

## 45. The pre-0.19.1 `/kit-check` — run 2026-08-09; nine findings fixed in-session

Full pass: four mechanical checks inline (inv 9 clean, 61 tracked files; inv 10
clean, 36 entries = bundle minus manifest, zero mismatches; inv 4 clean, `{{` in
`sdlc-setup.md` only with the exit-check scope exact; inv 6 delegated — 77 step
references plus 4 §-forms, all verified, zero stale), the eleven reading invariants
fanned to four read-only readers, every reader finding re-verified against the tree
before any edit. Invariants 2, 3, 5, 7 pass clean — inv 2 in both directions across
the full claim table, inv 3 with all 48 placeholders mapped and the FBK batch
confirmed placeholder-neutral against the diff.

The findings, all fixed in-session:

- **Inv 8, the pass's largest:** no transition note existed for 0.19.0's four guard
  hand-applies or FBK's three — the first hand-apply-bearing releases to skip the
  0.16.x/0.18.0 precedent — and the root README's "adoption-only… affects new
  adoptions, not yours" was false for exactly those entries, in the direction that
  stops the reader looking. Fixed in both homes: a combined 0.19.0/0.19.1 note in
  `sdlc-update.md` step 5 and the README's update section, and the adoption-only
  claim now states the project-owned-file exception.
- **Inv 1:** `AskUserQuestion` — a Claude Code tool absent from `COPILOT.md`'s
  mapping — named unconditionally at six sites in four commands (qualified per-CLI
  at first use); `end-slice.md`'s commit step prescribed "the Bash tool with a
  heredoc", unexecutable on Copilot's measured `powershell` shell tool (now names
  both CLIs' literal forms).
- **Inv 11:** `hypothesis-tests/SKILL.md` carries `disable-model-invocation: true`
  while `COPILOT.md` called the field "deliberately not adopted" and `SKILLS.md`
  recorded nothing. Settled from in-tree history: present since the initial
  vendoring commit — provenance, not adoption. `SKILLS.md` now records the field
  and its per-CLI meaning; `COPILOT.md` scopes its claim to "kit mechanism".
- **Inv 12:** `COPILOT.md`'s "levers in the R5.3 sense" — a kit-development batch
  number unresolvable in the bundle — removed. The FBK batch's own four bundle
  files came back clean, and the bench anchor moved to its first use in
  `GATE_RECIPES.md`.
- **Inv 13:** the guard suite's docstring said "fifteen ways" over 17 mutations —
  FBK's own stale count, in the batch that restated the derived-counts rule; the
  count is now derived-only. `GATE_RECIPES.md`'s dated 2026-08-05 proof paragraph
  certified a body FBK.4 had rewritten (the §31.15 specimen recurring) —
  re-stamped 2026-08-09, count-free, with the new case classes named.
- **Inv 15:** `CLAUDE.template.md`'s *Runtime Conventions* Enforcement sentence is
  a third home of the edit-time-hook claim that setup's no-hook fall-together
  branch never named (it carries no placeholder, so nothing else flags it) — on a
  declined-hook adoption the instantiated file would assert edit-time enforcement
  that does not exist. Setup's branch now names all three homes.
- **Inv 2 observation, fixed template-first:** the guard-note rationale "nowhere
  else the session reads at slice time says them" went stale the moment FBK made
  the guard speak; both homes now state the real division — the note is proactive,
  the guard's messages are reactive.

**0.19.1 released same session** — VERSION, CHANGELOG (Unreleased folded into the
release section), manifest regenerated from staged content in the release commit,
all four workflow gates simulated locally before the tag.
