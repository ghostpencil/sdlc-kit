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
3. **Release batching still open**: rides with the §31.18 guard fix as 0.16.1 or ships
   separately — decided when §31.18's own decision lands. `VERSION` and `CHANGELOG`
   untouched until then; `/kit-check` owed before whichever release carries this.

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
