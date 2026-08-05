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

- **0.16.0 — STD's audit clock, extended once** (§22, §31.6): the audit ran at its
  0.15.0 deadline (2026-08-05) — no lens catch, and no evidence the lenses *activated*
  in the one arc of exposure, which the pre-R5.6 records could not distinguish from
  "ran and caught nothing". Owner decision 2026-08-05: **extended to 0.16.0, once** —
  R5.6's step-evidence sweep now produces the per-step catch record at source, so
  0.16.0 is a deadline with real evidence behind it. No further extension on
  no-evidence grounds: after R5.6, "no evidence" means "did not run".
- **0.16.0 — `change-simplify` and `change-verify`** (§30.4): a confirmed field catch
  each, or deletion candidates. R5.1 exists partly to give `change-verify` a
  slice-level path to one.
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

