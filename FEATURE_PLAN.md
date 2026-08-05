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

- **0.15.0 — the next release — is STD's audit deadline** (§22): the three lenses and
  the runtime-standards recipe section each need a confirmed catch or become deletion
  candidates. The only field evidence since STD shipped (§31's report) records no lens
  catch.
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
docs at build time**, per §21's standing rule for anything Copilot.

Bookkeeping this section also carries: **0.14.1 shipped 2026-08-05** (Copilot bootstrap
documented in both READMEs; three `/kit-check` findings fixed — the CHANGELOG is the
record; no plan section existed for it until this note). And `sdlc-kit#2` (the fifth
report) is still open on the tracker despite shipping as SIMP (0.10.0) + R4 (0.11.0) —
close it with a pointer to §16/§17 when convenient.

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
shows is the interview's failure mode: the adopter's `spec/SDLC.md` records all three
tiers as `auto` — the mapping question answered with the default, which is exactly what
the gate-recipes principle warns a proposal-shaped question invites. **Remedy (R5.3),
expanded at the 31.4 halt (owner: the routing pain was real, not cosmetic):** the kit
cannot pin models in the files it ships (hazard 2, plus dual-CLI portability), so the
levers are the recorded mapping, the operator, and — pending verification — per-file
pins written at setup time. Four parts:

- **(a) Setup's Copilot tier question requires an explicit mapping.** Each tier maps to
  a named model from the `/model` listing, **or** the owner explicitly ratifies `auto`
  for that tier — recorded as "owner chose auto" with the date. Three `auto`s arrived
  at by accepting a default is neither, and setup says so at the question. The
  gate-recipes rule, applied to models: the mapping must match a decision, or the
  mapping lies.
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
without a status and the sweep infers. **Remedy (R5.4):** the template comment
prescribes the one-line shape — `- <date> — <friction> — open` flipping to `absorbed by
retro <date>` — and `/end-slice`'s friction bullet writes that shape. No new rule; a
format for one that exists.

### 31.3 The research report — what the kit takes, and what it declines

**Taken (inside R5):** the mechanism and vocabulary of 31.1; the evidence-contract
remedies R5.1/R5.2 are the report's "guidance" layer done in kit house style.

**Taken (as recorded hazards, verify against docs at build time):** (a) `gh skill
install`/`gh skill update` **inject provenance fields into `SKILL.md` frontmatter** — an
adopter who "updates" a kit-installed skill that way mutates files `/sdlc-update`'s
enumeration and the provenance regime expect byte-stable; worth one note in `SKILLS.md`
(the file that already tells adopters how skills arrive) and a line in `COPILOT.md`.
(b) Copilot hook facts beyond the kit's current `postToolUse` recipe: `preToolUse` can
deny and **fails closed on command errors but open on timeouts**; `agentStop` can block
with an eight-consecutive-block cap; `userPromptTransformed` can rewrite the
model-facing prompt. Recorded in `COPILOT.md`'s hook section as dated capabilities —
the kit builds nothing on them yet.

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
| R5.5 | `gh skill` frontmatter-injection hazard + hook facts, doc-verified | `SKILLS.md`, `COPILOT.md` | S |

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
R5.5 all approved; the enforcement machinery **addressed, not declined** — reshaped
into ENF below, queued behind R5 (batches are sized for one session, and R5 already
holds five items).

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
  has not run, within the documented eight-block cap. Nothing else from the report's
  architecture: no wrapper interview, no seam capture, no CI check, no CODEOWNERS
  apparatus. Kit-owned sidecar: one hook JSON (`.github/hooks/`) + one small guard
  script + state under `.git/`, template-ized with the same `{{HOOK_*}}` discipline as
  the existing gate hook (inv 1: placeholders taught to setup in the same batch).
- **ENF.2 — path policy reuses what setup already knows.** The guard's
  implementation/test classification comes from the interview answers the kit already
  collects — `{{SOURCE_GLOB}}` (gate hook) and `{{TEST_LAYOUT}}` (TESTING) — not a new
  `policy.json` interview. If those two cannot classify a repo, that is a trial
  finding, not a reason to grow the interview pre-emptively.
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
  `COPILOT.md`: hook matchers use `bash`, not `execute`).
- **ENF.4 — dialect honesty.** The guard is Copilot-dialect (`.github/hooks/`). The
  Claude Code side gets the equivalent decision made explicitly at build time —
  settings.json hooks exist there too — but nothing is assumed portable; a guard that
  runs on one CLI *says so* where `SDLC.md` records the CLI, per inv 15.
- **The owner reads the trial report before anything ships** (§4, the slice-runner
  precedent — this is the step F3 failed, and skipping it because the owner asked for
  the batch would invert the lesson).

