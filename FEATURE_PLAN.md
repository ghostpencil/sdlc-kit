# Feature Plan — retro, agents, model tiers

Kit-development artifact (like `IMPROVEMENT_PLAN.md`, which is closed — its backlog
emptied at `v0.3.0`). **Source:** owner feature requests, 2026-07-19 — not a field
report. That matters: `IMPROVEMENT_PLAN.md` §5's caution applies with extra force,
because these features have *zero* field evidence behind them yet. F1 exists partly to
fix that.

Where this plan and the discussion that produced it disagree, this plan wins. Each batch
is sized for one session. Run `/kit-check` before any release this plan produces.

---

## 1. Decisions already made — do not re-litigate

**Slices are strictly sequential.** Owner decision, 2026-07-19: slices have a logical
order determined at planning time, and parallel slice execution would break it —
inter-slice dependencies are the norm, not the exception. Parallelism in this kit is
permitted **only** for read-only fan-out *within* a step: analysis sweeps, repo surveys,
review lenses, verification passes. Never for implementation work; never across slices.

**Owner halts live in the main session — this is a harness fact, not a preference.**
Verified against Claude Code docs (2026-07-19): subagents cannot use `AskUserQuestion`
or otherwise interact with the user mid-run; they are autonomous until they return.
Therefore any workflow containing a halt (slice-scope confirmation, mid-slice design
questions, acceptance, merge approval) keeps its halt-bearing spine in the main session.
Agents get the autonomous middles.

**`/clear` survives.** The fresh-session rhythm is not a cache chore to engineer away —
it is the enforcement mechanism for "everything worth keeping goes to disk." Agents
reduce how much a session holds *between* halts; they do not replace the session
boundary at slice end.

**Model tiers are named by alias, never by model ID.** Verified: command and agent
frontmatter accept stable aliases (`opus`, `sonnet`, `haiku`, `opusplan`), scoped to
that command/agent's execution; an org allowlist exclusion makes the field a no-op
rather than an error. Aliases survive model generations; IDs are the "remembered
constant" trap in a new costume. Three tiers, maximum:

| Tier | Alias | Used for |
|---|---|---|
| High | `opus` | planning, analysis, adversarial review |
| Medium | `sonnet` | writing code to an existing plan/spec |
| Low | `haiku` | mechanical work: file search, log/output collection — *collecting, never analyzing* |

**The kit hard-codes a model only where variance is illegitimate.** `model: haiku` on
mechanical agent definitions is universal — no project has a reason to burn a bigger
model on file search. Everything else is owner policy: polled once at setup, recorded
project-owned, overridable at any moment with `/model`. Setup **never** edits installed
command frontmatter to record the poll — that is the rejected shape of field-report #1
(project-mutated kit files, phantom `DRIFTED` forever).

**Two harness limits that shaped the design** (verified same date): `context: fork`
exists for *skills* only — the kit's files are commands, so there is no
fresh-context-per-command switch available to them; and project-scoped agent
definitions (`.claude/agents/*.md`) are inherited on clone exactly like project
commands, so they follow the kit's existing install pattern.

**Features that change the execution model are trialed before they ship.** The
slice-runner (F3) enters the kit only after a real-project trial passes. This is
`IMPROVEMENT_PLAN.md` §7.3 applied forward: a design validated only by its author
shares its author's blind spots.

---

## 2. Batch order

```
F1  /sdlc-retro — close the improvement loop's input side   ← standalone, cheapest, first
F2  agents (read-only fan-out) + model tiers                ← shared work: both touch agent defs
     └─ cut v0.4.0
F3  slice-runner TRIAL on a real project                    ← not a kit change until it passes
     └─ if passed: encode in kit, cut v0.5.0
```

**Amended 2026-07-19: `v0.4.0` was cut after F1, not after F2.** F1 is only half-built
until it runs on a real adoption, and it cannot run on one until it is released and
migrated — the acceptance criterion *is* the release. Both prior releases were cut for
the same reason and both found defects in the migration itself. F2 therefore ships as
`v0.5.0`, and F3 (if its trial passes) as `v0.6.0`.

**Amended 2026-07-20: R1 (the retro-fix batch, §7) preempts F2.** The first retro's
priority rows lead with `/sdlc-update` deleting un-manifested files — live for every
adopter on the update path, which outranks new capability. R1 ships as `v0.5.0`; F2
slides to `v0.6.0`, F3 to `v0.7.0`. Owner-decided 2026-07-20.

F1 first because it is standalone and improves the evidence supply for everything else.
F2's two halves ship together because the model-tier work lands partly *in* the agent
definitions F2 creates. F3 is gated: the trial happens in an adopting project's repo
(TFit or Dungeon Daddy), not here, and a failed trial costs the kit nothing.

---

## 3. The batches

### F1 — `/sdlc-retro`: lessons-learned extraction *(new installed command)*

The improvement loop has a proven output side (field report → plan → batches → release
→ migrate) and a manual input side: `FIELD_REPORT.md` was written by hand. This command
runs in the **adopting** project and drafts the report from what the kit already forces
onto disk.

**Inputs it mines** (all already exist in any adopted project):
- Deferred-backlog **provenance tags** — the field report's own retrospective called
  them the most useful artifact of the run; they are the raw material here.
- Environment gotchas; Phase History; the gate-baseline trajectory in `spec/SDLC.md`
  (adoption counts vs. current — the burn-down is evidence about the process).
- `git log` friction signals: red-gate fix commits, repeated gate runs, fix-after-review
  churn, reverts.
- A short owner interview, in rounds: what did you fight? what did you override or work
  around? where was the process silent? what would you delete?

**The one structural rule — two audiences, strictly separated:**
- **Project lessons** (facts about this codebase, environment, team) go to the
  project's own files: PROJECT_INDEX Notes/gotchas, backlog. They never leave the repo.
- **Kit lessons** (the process was wrong, unclear, or silent somewhere) become a
  field report: numbered findings, each naming the kit file it implicates, a priority
  table, and a *what worked well* section — `FIELD_REPORT.md` in the kit's home repo is
  the proven template, and the command names it as the format. Output lands as
  `spec/SDLC_RETRO_<date>.md` (project-owned; the owner decides whether and what to
  submit upstream as a GitHub issue on the kit repo — the command never sends anything).

**Constraints:** states no project facts (invariant 1); no new placeholder; the
interview is rounds of ≤4 questions like every other kit interview; halts are not
needed — the whole command is owner-interactive by nature and runs in the main session.

**New-file ripple** (the §8.6 list): `sdlc-setup.md` install list (New mode step 5;
Existing inherits) — the file installs into `.claude/commands/` under the existing
`commands/` prefix, so **both classification scripts need no change**; root README file
tree + ownership table examples; bundle README; manifest (+1 entry, discrimination
check); CHANGELOG **[installable]**.

**Acceptance:** run it for real on TFit. It must produce a report with at least one
genuine kit finding (TFit has known material: the checker-reach problem is live there).
Negative case: run it on a freshly-adopted project with no history — it must say "not
enough evidence yet" rather than hallucinate findings.

**Status (2026-07-19): built in the kit repo; acceptance still open.** Eight files
changed — `commands/sdlc-retro.md` (new), `commands/end-phase.md`,
`commands/sdlc-setup.md`, `templates/CLAUDE.template.md`, `reference/SKILLS.md`,
`MANIFEST.sha256`, root README/CLAUDE/CHANGELOG. Neither acceptance case can run in this
repo: both need an adopting project.

Three decisions taken during the build, recorded so they are not re-opened:

1. **The retro is offered, not required.** `end-phase.md` step 7 offers it after the
   phase closes; `SDLC.template.md` is deliberately untouched. The reasoning is a real
   tension, not an oversight: every other kit command is reachable from the process
   (`SDLC.md` names `/plan-phase`, which hands to `/next-slice`, which hands to
   `/clear`), and a command with no caller runs only if the owner remembers it exists —
   self-defeating for the one command whose purpose is fixing the evidence supply. But
   wiring it into the canonical process would make it mandatory, and a required retro
   after every phase is precisely the ceremony the retro's own *what would you delete?*
   question exists to catch. An offer at the right moment resolves both. Note the
   failure mode this guards against is **silent**: no error, no drift, no `/kit-check`
   finding — just a shipped command that never runs.
2. **The report format is inlined, not pointed at.** An early draft told the command to
   follow `FIELD_REPORT.md`; that file lives in this repo and *not* in an adopted
   project. Caught by invariant 5, which exists for exactly this.
3. **Two pre-existing defects fell out of the batch's `/kit-check`,** both fixed here.
   The root README's update section was missing the *new-files-in-the-target-install-set*
   clause that `sdlc-update.md` step 5 already carried — the two statements of the
   procedure disagreed, which the kit defines as a bug (invariant 8). It had verified
   clean since it was written, because `sdlc-retro.md` is the first new installed file
   to make it bite: a human following the README by hand would finish step 4 with no
   instruction that would ever create the file, and step 6 verifies only files you
   copied. Separately, `reference/SKILLS.md` listed five kit commands, having missed
   `sdlc-update` at 0.3.0 (invariant 7).

---

### F2 — agents for the autonomous middles, and the model-tier poll

**F2a — explicit read-only fan-out.** Make delegation explicit where work is autonomous
and read-heavy; change nothing interactive.

- `plan-phase.md` step 4 (adversarial gap analysis): the seven sweeps run as parallel
  read-only subagents; findings return to the main session, and the interview about
  them — every question, every numbered decision — stays with the owner. This is the
  biggest win: the sweeps are the command's heaviest context load today.
- `sdlc-setup.md` Existing-mode step 1 already says "spawn an Explore agent for large
  ones" — normalize the wording to the same pattern.
- `end-slice.md` / `end-phase.md`: reviews already run through agent-based skills;
  no structural change. Gate runs stay in-session (cheap, and their output is needed
  verbatim).
- Ship kit-owned agent definitions in a new `sdlc-kit/agents/` directory, installed to
  `.claude/agents/` (verified: project-scoped, inherited on clone). Initial set is
  small — a read-only surveyor/sweeper (`model: haiku`, tools restricted to
  read/search) and nothing else until need is proven. **Sequentiality note:** these
  agents are read-only by tool restriction, which is what makes their parallelism safe
  under §1's rule.

**F2b — the model-tier poll.** One new setup interview item (both modes, in the
process-fit round): present the §1 tier table as the recommended default, ask the owner
to confirm or adjust. Record the outcome:
- Session default model → `.claude/settings.json` (project-owned, instantiated —
  verify the exact settings key at implementation time).
- The policy itself → a short *Model policy* note in `spec/SDLC.md` (new
  `{{MODEL_POLICY}}` placeholder — placeholder #35; invariant 3's mapping gains one
  row, resolved by this question).
- Commands **advise, never assert**: `plan-phase.md` opens with one line — "this step
  is analysis-heavy; check the model policy recorded in `spec/SDLC.md` (`/model` to
  switch)". Pointer, not fact; one line, per the context budget.
- The only kit-set models: `haiku` on F2a's mechanical agents. Decision recorded here:
  `opusplan` on `plan-phase.md` frontmatter was considered and **deferred** — it is
  attractive (plan on High, execute on Medium, in one alias) but imposes High-tier cost
  on every adopter by default; revisit with F1 field evidence.

**Install-mapping warning — this is the batch's §8.6 moment.** `agents/` →
`.claude/agents/` is a **new install mapping**, the first since `REVIEW_LENSES.md`,
and that one falsified five derived statements and both classification scripts (plan
§8.6). The ripple this time is strictly larger because the *destination* is new too:
`sdlc-setup.md` install list (the single source); both READMEs; root CLAUDE.md flow
diagram; ownership tables in README and `sdlc-update.md`; **both classification
scripts** — they enumerate `git ls-files .claude/commands` and must now also cover
`.claude/agents/` with an `agents/` prefix, *including their denominator checks*;
`sdlc-update.md` step 5 sources; manifest; both README file trees; CHANGELOG.
Run `/kit-check` invariant 7 explicitly against the finished batch.

**Acceptance:** a plan-phase run on a real spec completes with sweeps delegated and
every owner interaction still in the main session; setup on a scratch project records
the poll in both project-owned homes and leaves zero `{{` in instantiated files; the
`{{` census and invariant-7 pass stay clean.

---

### F3 — slice-runner: TRIAL first, kit change only if it passes

> **CLOSED 2026-08-02 — the trial ran and the runner does not ship. See §14 for the
> disposition and the evidence.** Everything below is the design as written before the
> trial, kept for provenance; where it and §14 differ, §14 is the outcome.

**The pattern.** `/next-slice` keeps halt 2 (scope confirmation) in the main session,
then spawns **one** implementation agent for **the one confirmed slice** — never more
(§1: slices are strictly sequential; the next slice is not spawned until this one's
`/end-slice` completes and the owner clears). The agent runs the TDD loop autonomously
and returns exactly one of:
- **done** — exit criteria met, gate green, diff summary returned; main session
  proceeds to `/end-slice`.
- **blocked: design question X** — the halt-3 protocol: the agent states the question,
  the decision context, and its recorded state (everything already on disk per kit
  rules, plus uncommitted-work status). The main session raises it to the owner
  verbatim, then respawns the agent with the answer. Respawning is cheap *by design* —
  the kit already demands that state worth keeping lives on disk — and the trial exists
  to find out whether that's actually true for mid-slice, mid-TDD state.

**Why trial in an adopting repo, not here:** the risky seams are exactly the ones a
design review can't see — uncommitted in-flight work across respawns, permission
prompts surfacing to the parent, gate output fidelity through the agent boundary,
whether the owner finds the reduced visibility acceptable. §7.3: a synthetic fixture
would inherit this design's assumptions.

**Trial protocol** (run on TFit or Dungeon Daddy, ≥2 real slices, sequentially):
1. Hand-author the slice-runner as a *project-local* command variant in that repo —
   the kit is untouched.
2. At least one slice must exercise the blocked-on-design-question round trip for
   real (if none occurs naturally, plant a spec ambiguity so one must).
3. Pass criteria: no state loss across a respawn; halt 3 reaches the owner verbatim
   and the answer reaches the agent; gate results survive the boundary un-summarized;
   the owner would choose it again over the in-session loop.
4. Failure on any criterion: record why in this file, stop. The in-session TDD loop
   remains the kit's shipped behavior.

**If the trial passes:** encode in `next-slice.md` + the agent definition, mirror the
process change into `SDLC.template.md` (invariant 2 — the slice loop's canonical
statement changes), CHANGELOG **[installable]**, cut `v0.5.0`. The sequential-only rule
gets stated in *both* files.

---

## 4. Rejected or reshaped — do not re-litigate

| Proposal | Disposition |
|---|---|
| Every sdlc command spawns an agent for clean context | **Rejected.** Subagents cannot interact with the user (verified); the owner halts are the kit's spine and three of them live mid-workflow. Agents get the autonomous middles only. |
| Parallel slice execution | **Rejected — owner decision, §1.** Slices are sequential by planned dependency order. Parallelism is for read-only fan-out within a step only. |
| Replace `/clear` with a persistent orchestrator session | **Rejected.** Erodes the write-to-disk discipline that makes fresh sessions possible; parent context grows anyway as reports accumulate. |
| Setup writes polled model choices into installed command frontmatter | **Rejected.** Project-mutates kit-owned files → phantom `DRIFTED` on every update; same shape as field-report #1's rejected fix. Poll lands in project-owned files. |
| Hard-code model IDs anywhere | **Rejected.** Aliases only; IDs are a staleness trap ("a remembered constant is not a measurement"). |
| `opusplan` on `plan-phase.md` frontmatter | **Deferred**, not rejected — imposes High-tier cost on every adopter by default. Revisit with F1 evidence. |
| `context: fork` for command isolation | **Unavailable** — skills-only (verified). Revisit only if the kit ever migrates commands to skill format, which is its own design question. |
| Slice-runner straight into the kit | **Reshaped** into a gated trial (F3), then **declined on the trial's evidence, 2026-08-02** (§14). Three slices on a real arc: two criteria never fired, one degraded across slices, the owner's verdict mixed. Execution-model changes ship on evidence, not on design confidence — and this is what that rule looks like when the evidence says no. |

---

## 4a. The ripple lists in this plan are incomplete — verified, not suspected

F1's §8.6 ripple list named five destinations and **missed three**: `end-phase.md` (the
caller), `templates/CLAUDE.template.md` (the adopted project's own command list — a
command installed and named nowhere the project reads is a command nobody runs), and
`reference/SKILLS.md` (a derived statement of the install mapping). All three were found
by `/kit-check`, none by the plan.

That is a 5-of-8 hit rate on the *easy* batch — F1 adds a file under an existing prefix
with an existing destination, the case the plan itself calls the mild one. **F2's list
must therefore be treated as a starting point, not an inventory**, and its `agents/` →
`.claude/agents/` mapping is the hard case: a new prefix *and* a new destination, where
the analogous `REVIEW_LENSES.md` change falsified five derived statements at once.

The generalizable rule, and the reason this section exists rather than a corrected list:
**derive the ripple set mechanically, do not recall it.** Before the batch, grep for an
existing member of the set being extended (`grep -rn sdlc-update` was what surfaced all
three misses here) and treat every hit as a candidate. `reference/SKILLS.md` had already
missed `sdlc-update` at 0.3.0 and gone unnoticed for a release — a hand-maintained list
of derived statements is itself a derived statement, with the same drift problem.

---

## 5. Cross-cutting

- **Every batch ends with `/kit-check`** — F2 in particular is a live test of ledger
  invariant 7 (install mapping), the class with the worst track record (plan §8.6).
- Evidence discipline: F1's output is the input to every future plan. If F1's first
  real run finds nothing, that is a finding about F1, not proof the kit is done.
- CHANGELOG markers: everything in F1/F2 that touches the bundle is **[installable]**
  or **[adoption-only]** per the (corrected) header definition; F3's trial produces no
  CHANGELOG entry at all until it passes.
- This file joins the root README file tree and root CLAUDE.md's root-docs enumeration
  (invariant 5 / invariant 9 in the ledger) in the same commit that adds it.
- **Trial protocol (R4.9, from the fifth report's finding 8):** a trial pre-registers
  **what the change is supposed to buy and how that is measured**, alongside its
  safety criteria, before it runs. F3's four pass criteria all measured safety; "saved
  no time" was observed and never in dispute, and a trial that cannot fail on value
  cannot justify shipping. Recorded here for any future F3-shaped work, from the
  trial's own results: `blocked` is rare **by design** — for a slice with a detailed
  spec the halts get spent at scope confirmation, before any spawn, so `blocked` and
  respawn-recovery are labeled *unexercised*, not validated — and the two-state return
  contract needs at least two more states: *done except for work that can only happen
  outside the agent boundary*, and *done, with a real design question deferred to a
  later slice*.

---

## 6. Hand-off — state as of 2026-07-19, end of the F1 session

**F1 is built and released; its acceptance is running in the owner's hands, not on
disk.** The owner is manually testing `/sdlc-retro` on TFit. Nothing in this plan should
be actioned on F1 until that result comes back — the whole point of the batch is that
the command's value is unproven until a real run either produces a genuine kit finding
or does not.

### What is on disk

| Where | State | Pushed? |
|---|---|---|
| Kit `main` | `3adccb0` — F1 complete, `/kit-check` clean on all 13 invariants | **no** |
| Kit tag `v0.4.0` | created, annotated; all three `release.yml` gates simulated green | **no** |
| TFit `main` | `0ff6645` — the long-unmerged 0.3.0 branch, finally landed | yes |
| TFit `chore/update-sdlc-kit-0.4.0` | `463f26a` — 0.4.0 installed, version re-stamped | **no** |

Pushing the kit tag is what triggers `release.yml` to build the bundle asset. It was
held deliberately, not forgotten: the owner had not authorized an outward push.

### Resume here

1. **Get the TFit test result first.** Everything below branches on it.
   - *Produced a genuine kit finding* → F1's acceptance is met. The finding itself is
     F1's first real output: triage it into this plan (or a field report) as evidence,
     and note that the deferred `opusplan` decision in F2b was explicitly parked
     awaiting exactly this kind of evidence.
   - *Produced nothing, or nothing usable* → **that is a finding about F1**, per §5's
     evidence discipline, and it is not a reason to weaken the command's refusal
     behavior. Diagnose which half failed: the disk-mining sweeps (step 2) or the
     interview (step 3). They fail differently and are fixed differently.
   - *Refused to run* on a project with TFit's history would itself be a defect — the
     evidence-sufficiency check in step 1 is calibrated for a fresh adoption, not a
     project one phase in.
2. **The negative case is still unrun.** `/sdlc-retro` on a freshly-adopted project with
   no history must say "not enough evidence yet" rather than hallucinate findings. No
   such project exists yet; a scratch adoption is the cheapest way to get one.
3. **Then F2**, which ships as `v0.5.0` (see §2's amendment). Before starting it, read
   §4a — F2's ripple list is the one with the new prefix *and* the new destination, and
   §4a exists because F1's list, on the easy case, was 5-of-8.

### Loose ends, none blocking

- **TFit pins LF only for `.sh`/`Dockerfile`.** Its `.md` files sit CRLF in the working
  tree, so installing the kit's LF files makes `git status` report ~24 modified files
  when only 4 differ in committed content. Harmless — the classifier hashes committed
  content, exactly as the update procedure insists — but alarming to read, and the next
  update will do it again. `*.md text eol=lf` in TFit's `.gitattributes` fixes it. Left
  alone because it is a project-owned file outside the update's remit; it is the owner's
  call, and it is decent `/sdlc-retro` material in its own right.
- `IMPROVEMENT_PLAN.md:77` records TFit as migrated to 0.3.0 as of 2026-07-19. True of
  the work, false of `main` until this session: it sat on an unmerged, unpushed local
  branch for the whole interval. Worth remembering that "migrated" in these plans has
  meant "a branch exists" at least once.

### Result — 2026-07-20: acceptance met

The TFit run came back, and it is the first branch of step 1 above, emphatically:
**twelve findings and a 15-row priority table**, every finding naming the kit file(s) it
implicates, with measured evidence. The anonymized report TFit prepared for submission is
now placed at this repo's root as `FIELD_REPORT_2026-07-20.md` — that file is F1's
acceptance evidence and the input to the next batch. Triage notes:

- **The command also produced a finding about itself.** Finding 12: the retro's
  orientation (steps 1–2) reads only the project's spec files, so friction recorded on
  the *kit's* side — including the line-ending churn this hand-off's own loose end
  called "decent `/sdlc-retro` material" — was invisible until the owner pointed at it.
  §5's evidence discipline anticipated a null result being a finding about F1; a real
  run with a measurable blind spot is the same lesson in a better form. (TFit has since
  pinned `*.md text eol=lf` itself, so the loose end above is closed project-side.)
- **The report's priority rows 1, 13, 2 target `/sdlc-update` and `/sdlc-setup`** — the
  silent deletion of un-manifested files and the phantom-diff noise that hid it. That
  defect class is live for every adopter on the update path, which argues for a
  retro-fix batch *before* F2. Owner's call; the plan's "Then F2" predates this evidence.
- **F2b's parked `opusplan` decision stays parked.** The retro carries no model-tier
  evidence either way; nothing in it speaks to plan-time reasoning depth.
- **Step 2 (the negative case) is still unrun** — unchanged by this result, and worth
  doing before touching `sdlc-retro.md` for finding 12, so both known gaps land in one
  edit.

---

## 7. R1 — the retro-fix batch *(ships as `v0.5.0`; owner-decided 2026-07-20)*

> **Status: DONE, 2026-07-20.** Built, `/kit-check` clean on all 13 invariants,
> released as `v0.5.0` (tag pushed, `release.yml` green in 13s, assets published),
> TFit migrated same day (PR #5, merged). See §8 for the session hand-off.

Actions all 15 rows of `FIELD_REPORT_2026-07-20.md`'s priority table. The report holds
the evidence and rationale per row; this section records only the edit map and the
decisions the rows forced. Every row is prose-and-procedure work — no new files, no new
placeholders.

### Edit map (row → file)

| File | Rows | Edit |
|---|---|---|
| `commands/sdlc-update.md` | 1, 9, 13 | never delete un-manifested files (enumerate the real directory, halt on extras); update only at an arc boundary; report content-changed vs touched counts |
| root `README.md` (update section) | 1, 9, 13 | same three, mirrored — the command and the section must agree (ledger inv. 8) |
| `commands/sdlc-setup.md` | 2, 14 + ripples | `sdlc-kit/` is volatile, project notes go project-owned; offer `*.md text eol=lf` when `.gitattributes` leaves `*.md` undefined; step 1.2 skill check and step 5 install list follow the row-3/row-6 decisions |
| `commands/end-slice.md` | 3, 4, 5, 6 | mutation-check step for new guards; deferred entries mark cause measured/suspected; consumer-of-changed-error-path lens; per-slice reviewer renamed + substitution rule |
| `commands/next-slice.md` | 4, 7, 12 | re-derive a backlog entry's cause before fixing; check for any unmerged arc branch; skip halt 2 when the slice is recorded owner-decided |
| `commands/end-phase.md` | 10, 11 | deploy question after merge; surface the backlog (convert / defer / drop) |
| `commands/sdlc-retro.md` | 15 | orientation reads kit-side planning docs when the kit is co-developed; sweep for recorded-but-unactioned friction on both sides |
| `templates/SDLC.template.md` | 3, 5, 6, 7, 10, 11, 12 | the canonical statement of every process change above (inv. 2: template wins, so it changes in the same batch as the commands) |
| `templates/TESTING.template.md` | 8 | doubles must reproduce side effects and error surface, or the test drives the real thing |
| `templates/PROJECT_INDEX.template.md` | 4 | backlog-entry format gains the measured/suspected cause marker |
| `templates/CLAUDE.template.md` | 10 | one-line `/end-phase` summary gains the deploy check |
| `reference/SKILLS.md` | 3, 6 | mutation-testing flips optional→required; per-slice review row names the real tool |

### Decisions

- **Row 3 makes `mutation-testing.md` a required install**, not an offer — a step the
  slice loop mandates cannot depend on an install-time "maybe". `sdlc-setup.md` step 5
  and `reference/SKILLS.md` change together.
- **Row 6 resolution:** the per-slice reviewer is `pr-review-toolkit:code-reviewer`
  (agent-runnable, plugin already required by `/end-phase`); the built-in `/code-review`
  is the owner-typed escalation and is named as such. A substituted tool must be named
  in the hand-back. Setup's step 1.2 check moves from the built-in skill to the plugin,
  now needed at slice end as well as phase end.
- **Row 11 is an offer, not a sixth halt.** The five-halt-point invariant stands;
  surfacing the backlog at phase end joins the `/sdlc-retro` offer in post-merge
  bookkeeping.
- **Row 12 narrows halt 2 rather than removing it** — exactly as the report proposes
  (the owner's own first instinct to delete it outright was revised in the retro).

### Ripple check (§4a discipline — F1 scored 5-of-8 on the easy case)

Destinations enumerated by grep before editing: `code-review` (4 files + SKILLS),
`mutation` (setup + SKILLS), halt-2 phrasing (next-slice, SDLC.template), branch rules
(next-slice, end-slice notes, SDLC.template Shape), update procedure (sdlc-update +
root README, ledger inv. 8). The root README file tree does not change — no files are
added or renamed. `/kit-check` closes the batch.

---

## 8. Hand-off — state as of 2026-07-20, end of the R1 session

Everything in this plan through R1 is **done, released, migrated, and pushed**. Unlike
every prior hand-off, nothing is being deliberately held: both repos' `main` match
their remotes, all four release tags are published with green `release.yml` runs and
bundle assets, and the merged branches are pruned on both sides.

### What is where

| Where | State |
|---|---|
| Kit `main` = origin | `46e8ec6` — v0.5.0 release commit; working tree clean except this hand-off |
| Kit releases | `v0.2.0`–`v0.5.0` published; `v0.5.0` latest, assets + checksums attached |
| TFit `main` = origin | `917922f` — PR #5 merged (0.5.0 update + the spec merge), CI green |
| TFit spec state | `spec/SDLC.md`/`spec/TESTING.md` merged with the 0.5.0 process changes, so the template/spec drift the update commit warned about is closed; friction log #1 and #3 marked absorbed, #2 partially |

R1's acceptance evidence worth one sentence here: the update procedure's new rules ran
for real on TFit the same day they shipped — enumeration found 26/26 manifested (clean,
and *proven* clean rather than assumed), classification discriminated on exactly the
six changed files, and the `*.md` eol pin produced zero phantom modifications.

### Resume here

1. ~~**The `/sdlc-retro` negative case is still the cheapest open item.**~~ **Done,
   passed — 2026-07-20.** A scratch New Project adoption (`notegrep`, Python CLI,
   kit v0.5.0 instantiated faithfully: templates filled, commands installed, one
   scaffold commit, PRE-PHASE-1, empty backlog) was handed to a blind agent told only
   "the owner invoked `/sdlc-retro`" — no hint of the expected answer. The agent ran
   the step-1 sufficiency check before anything else, counted 0 phases / 0 slices /
   0 backlog entries / 1 commit, reported "not enough evidence yet — stopping without
   a report", named exactly what the command says to name (a merged phase, a populated
   backlog with provenance tags, a baseline trajectory), pointed the owner at
   `/plan-phase`, and wrote nothing — working tree verified clean after the run. It
   did not interview its way around the missing evidence and did not manufacture
   findings. Both halves of F1 are now exercised; the sufficiency check's calibration
   is trusted.
2. **Then F2** (read-only agents + model tiers), shipping as `v0.6.0` per §2's second
   amendment. Read §4a first — F2's ripple list has both a new prefix and a new
   destination, the class with the worst track record. The `opusplan` decision in F2b
   remains parked: R1 produced no model-tier evidence either way.
3. **Two small kit-side residues from the TFit migration**, either fold into F2's
   batch or take as one-offs:
   - The template seeds no *Kit friction log* section, so other adopters have nothing
     for `sdlc-retro`'s new recorded-but-unactioned sweep to mine (TFit friction log
     #2's unabsorbed half).
   - Setup's new eol check covers `*.md` only; TFit's update still warned LF→CRLF on
     four non-markdown bundle files (`LICENSE`, `MANIFEST.sha256`, `VERSION`,
     `settings.template.json`). Harmless to the hashes, but the same noise class one
     size smaller — a `* text=auto eol=lf`-shaped recommendation may be the real fix.

### Standing context

- `FIELD_REPORT_2026-07-20.md` at the root is the canonical submitted copy of the
  retro; TFit's project-side kit-bound twin was cleared for deletion by its own note
  once placement happened — deleting it is TFit-side housekeeping nobody has done.
- The five-halt-point invariant survived R1 intact (halt 2 narrowed, not removed; the
  end-phase backlog prompt is an offer). Guard it in F2 — agent fan-out is exactly the
  kind of feature that breeds new halts.

---

## 9. F2 — done, released as `v0.6.0` (2026-07-20)

Both halves shipped together as planned, plus §8's two residues, folded in. What is on
disk matches §3's design with one deliberate sharpening: the plan's single
"surveyor/sweeper (`model: haiku`)" would have put *analysis* on the tier the table
reserves for *collection*. Resolved without a second agent definition: the shipped
`agents/sdlc-surveyor.md` is collection-only (`haiku`, `Read/Grep/Glob`, "collects,
never analyzes"), and `plan-phase.md`'s seven sweeps run as parallel read-only
subagents that **inherit the session model**, with the surveyor explicitly excluded
from that step. The command's advisory line points at the recorded model policy.

The poll lands in exactly the two project-owned homes §3 named — `{{MODEL_POLICY}}`
(new *Model policy* section, `SDLC.template.md`) and `{{DEFAULT_MODEL}}`
(`settings.template.json` `"model"` line, deleted on decline; key name verified
against current docs, aliases confirmed valid, org-exclusion confirmed silent-fallback).
`opusplan` stays parked — still no field evidence either way. Five halt points,
unchanged: the poll is setup-interview material, and the template now states the
fan-out rule (read-only, within a step, findings return, no owner interaction ever
leaves the main session).

### Ripple score (§4a discipline)

Derived mechanically before editing (grep for `REVIEW_LENSES` and `.claude/commands`
enumeration), not recalled. §3's list named ~10 destinations and all were real; the
derivation surfaced **three it missed**: `KIT_INVARIANTS.md` (the inv-4 census scope
and inv-1 reading-pass scope now include `agents/`), root `kit-check.md` (checks 1, 4,
5, 7 — same scopes), and `reference/SKILLS.md` — **the same file F1's list missed**,
now missed by a plan list twice; treat it as a standing member of every
install-mapping ripple. Call it 10-of-13, found *before* editing rather than by the
check after — the §4a rule did its job.

### Verification and acceptance

- `/kit-check` full pass, 13/13 after fixing the three findings it raised: halt 3's
  template wording now owns the whole-arc-review case ("mid-slice or by a review");
  root README's stale "optional" on `mutation-testing.md`; README gained the
  command's "claim only what was checked" rule (inv 8's first real catch). Reading
  passes ran as four parallel read-only subagents — the batch's own pattern, used to
  verify the batch.
- Manifest regenerated twice, discrimination proven both times (exactly the edited
  files changed hash; 27 entries = `ls-files` − 1).
- **Acceptance, setup half — met.** A scripted-owner scratch adoption (`loglens`,
  New mode, Python) run by a subagent against the 0.6.0 bundle: poll recorded in both
  homes (`"model": "sonnet"` in settings; owner-confirmed tier table in
  `spec/SDLC.md` §Model policy), `sdlc-surveyor.md` installed with `model: haiku`
  intact, `{{` exit grep clean, gate green, hook and isolation harness proven by
  negative cases, `* text=auto eol=lf` written. Spot-checked independently after the
  agent's report.
- **Acceptance, plan-phase half — exercised 2026-07-22; delegation mechanics
  unconfirmed.** TFit Arc 3 (PR #7) was planned under 0.6.0 (the update, `bc9db7e`,
  opened the arc). The gap analysis demonstrably ran and earned its keep — it cut #39
  by measuring its premise false (recorded as D6 in the phase plan) and surfaced the
  D4 caller-controlled-path fact — and every recorded decision in the plan is
  owner-attributed. What was *not* observed: whether the sweeps ran as parallel
  read-only subagents. The owner didn't watch for the fan-out and no artifact records
  the mechanics — correctly, since the design says findings return and nothing else
  leaves a trace. Per inv 8 (claim only what was checked): the *behavior* is
  field-verified, the *delegation* is still design-verified only. Residual: watch for
  the fan-out on the next `/plan-phase`; one observation closes it.
- **The fan-out watch — worked 2026-08-01 (§12 step 5). Verdict: independence is now
  field-evidenced; delegation remains unobserved, and no artifact can ever observe it.**
  Denominator: `grep -rn -i "subagent|surveyor|fan-out|parallel|sweep"` over all of
  TFit's `spec/` (10 files), plus the two `/plan-phase` runs that post-date F2 —
  Phase 04 (2026-07-24) and Phase 05 (2026-07-25), **both planned on kit 0.8.0**, with
  the parallel-subagent instruction verified present in the installed file at that time
  (`git show 5fbb3ff:.claude/commands/plan-phase.md:62`). Two findings:
  - **Positive evidence of independence, from Phase 05.** `PHASE_05:531` records that
    *"the sweep produced **two mutually contradictory analyses** of what the browser
    sends"* — and carries **both** forward, as an acceptance instruction to measure the
    real `Origin` header rather than assume it. A single in-context sequential pass has
    the earlier sweep's conclusion in view when the later one runs; two live, unreconciled
    answers to one factual question is the signature of workers that could not see each
    other. `PHASE_05:60–61` is the same shape read the other way — *"Three sweeps
    converged on this **independently**"* is only worth recording if convergence was not
    guaranteed by shared context. Phase 04's coupling sweep shows sweeps reading code
    mechanically (`D8`: sanitizer references *zero* server globals; `D9`: 16 of 19
    card-timing members pure) but says nothing about how they were run.
  - **The residual cannot close by the means it was queued to close by.** No artifact
    names an agent, a model, or a spawn — by design (findings return, nothing else leaves
    a trace), so *more* `/plan-phase` runs cannot raise this above inference. Waiting for
    another one was the wrong instruction. Per inv 8 the claim is downgraded, not
    completed: **sweep independence is field-evidenced by its consequences; the spawn
    mechanics are design-verified only.** One live observation still closes it, and TFit's
    Phase 06 planning (#64) is the free opportunity — the owner watches once, or the claim
    stays where it now is permanently. **The `sdlc-surveyor` spawn at `plan-phase.md:112`
    has zero field evidence of any kind** — its only occurrence anywhere in TFit is the
    process description at `spec/SDLC.md:300`. It has never been observed to run.

### Resume here — owner-confirmed order, 2026-07-20 end of session
### (statuses re-verified against both trees, 2026-07-22 — superseded by §10's list)

1. ~~**Migrate TFit to 0.6.0.**~~ **Done, 2026-07-22** — `bc9db7e`, at the Arc 3
   boundary, inside PR #7's window. (Step 5's replacement tripped on Windows —
   Finding 3 of the third field report; benign, but now R2 work.)
2. **Apply the two [adoption-only] follow-ups to TFit by hand** — **half done.**
   - *Model policy* section: **NOT applied** — verified 2026-07-22 by grep: no such
     section in TFit's `spec/SDLC.md`, no `"model"` key in `.claude/settings.json`.
     Still owner work; carried into §10's list.
   - Friction-log seed: **confirmed** — TFit's section survived and was mined by the
     2026-07-22 retro (its Finding 3 came from friction log #4, exactly the
     recorded-but-unactioned sweep working as designed).
3. ~~**Close F2's open acceptance half**~~ **Recorded, 2026-07-22** — see the
   acceptance bullet above: behavior field-verified on Arc 3's planning, delegation
   mechanics unobserved; one watched fan-out on a future `/plan-phase` closes the
   residual.
4. **TFit housekeeping — still undone.** Both kit-bound field-report twins remain in
   TFit's `spec/` (`SDLC_FIELD_REPORT_2026-07-19.md`, `SDLC_FIELD_REPORT_2026-07-20.md`),
   verified 2026-07-22. TFit's `SDLC_RETRO_*.md` files are project records and stay.
5. **Then F3** (slice-runner TRIAL, §3) — hand-authored as a project-local command on
   TFit or Dungeon Daddy, ≥2 real slices, one exercising the blocked-on-design-question
   round trip; the kit stays untouched unless all four pass criteria hold. A failure is
   recorded here and costs the kit nothing. **Re-sequenced 2026-07-22:** the owner put
   the R2 fix batch (§10) ahead of it.

Steps 1–4 need the owner in the loop (update halt, spec edits, acceptance are theirs
by design); step 5's kit-side encoding is a normal session's work after the trial.

---

## 10. Third field report and R2 — triaged 2026-07-22

TFit's Arc 3 retro (`SDLC_RETRO_2026-07-22.md`, the second real `/sdlc-retro` run, first
on kit 0.6.0) was submitted upstream as `FIELD_REPORT_2026-07-22.md` — copied verbatim,
owner-decided the same day. Three findings, all effort-S, plus the strongest worked-well
signal the kit has: **the whole-arc review is 3-for-3** across TFit's arcs at finding
mutation-confirmed gaps that zero-finding slice reviews missed. Protect it from any
future simplification pass.

The report's cross-cutting theme sharpens the lineage (report 1: specify → self-check;
report 2: enumerate the denominator): **a number recorded in prose is not the number the
machine enforces, and the kit's bookkeeping updates prose without reconciling against
the enforcing artifact.** The fix shape it implies — bump both homes, then assert they
agree — is the R2 batch's through-line.

### Claims verified against the kit tree before triage (not taken from the report)

- **Finding 1 confirmed as stated:** `commands/end-phase.md` contains zero mentions of
  coverage, floor, or `fail-under`; the template's ratchet is a rule with no boundary
  procedure. The sharp edge: TFit's floor was read off CI *correctly* and then written
  only to prose — CI enforced 28 while the index claimed 32 for two days.
- **Finding 2 confirmed in substance:** `next-slice.md` §2 *names* the marker
  ("Check the marker (`measured` / `suspected`)") but prescribes the same full
  reproduce-or-disprove for both — the marker is read and then ignored, the report's
  mirror case of Finding 1. The rule also lives at `SDLC.template.md:154` (inv 2:
  both change together).
- **Finding 3 confirmed in refined form:** step 5 of `sdlc-update.md` prescribes
  *replacement* ("replace it with the target version's bundle") without prescribing
  the mechanism; the `rm -rf` that failed on Windows was the agent's improvisation in
  the vacuum. Fix is to prescribe copy-over-in-place.
- **One report claim measured FALSE:** the worked-well section's "the kit ships
  `mutation-testing.md` but no command invokes it." `end-slice.md` §4 has *mandated*
  the mutation check and named the skill since R1 (v0.5.0) — and the retro's own S4
  narrative describes that step running five times. The "standing open finding" it
  cites is closed, not standing. No kit action; recorded here so the false claim
  doesn't get re-triaged from the report later.

### R2 — the fix batch *(owner-decided 2026-07-22: ships before F3)*

| File | Finding | Edit |
|---|---|---|
| `commands/end-phase.md` step 7 | 1 | new bookkeeping bullet: if CI's printed coverage rose, set `--cov-fail-under` in the CI workflow to just under it, in the same docs commit; then **assert** the index's recorded floor and the workflow value are identical — the record is a claim, the workflow is the enforcement |
| `templates/SDLC.template.md` (ratchet) | 1 | the canonical statement of the boundary procedure (inv 2: same batch as the command) |
| `commands/next-slice.md` §2 | 2 | proportional re-derivation: `measured` → spot-check the cited anchors/behavior still hold; `suspected`, or a `measured` entry whose anchors drifted → full re-derivation; a surprising spot-check → fall back to full and re-tag |
| `templates/SDLC.template.md` §slice-start | 2 | same rule, canonical home (`:154`) |
| `commands/sdlc-update.md` step 5 | 3 | prescribe the mechanism: remove only the files the *old* manifest lists, then `cp -r $K/. sdlc-kit/` — never remove the directory; no window where the bundle is absent, and it sidesteps the Windows busy-directory failure |
| root `README.md` (update section) | 3 | mirror if the section states the mechanism (inv 8: command and section must agree — verify at edit time) |

Ripple discipline (§4a): the map above was derived by grep, not recalled. No
install-set change, so `reference/SKILLS.md` — the twice-missed standing member — has
no role this time; verified, not assumed. No files added or renamed by R2 itself, so
the README tree is untouched by the batch (it already gained the report's line the day
of triage). `/kit-check` closes the batch as always.

**Version:** next minor at ship time — `v0.7.0` by R1's precedent (process changes are
minor). §3's "F3 ships as `v0.7.0`" reads as "the minor current when the trial passes";
the number was a placeholder, not a reservation.

**Shipped:** R2 landed and released as `v0.7.0` on 2026-07-22, same day as triage. The
distribution-readiness batch (stable release-asset names, issue templates, prerequisites,
repo description — pre-public-launch work, owner-directed) rode in the same release.
Remaining from the resume list below: TFit's migration to 0.7.0 at its next arc boundary
(which exercises Finding 3's fix on the platform that surfaced it), the TFit owner work
carried from §9, the fan-out watch, then F3.

**TFit follow-through (2026-07-22, later the same day):** both TFit steps ran and are
**merged** (owner approved at halt 5; merge commits `98f3be1` and `12d69df`, branches
deleted — TFit is on kit 0.7.0). The 0.7.0 migration is **TFit PR #8** — executed with
the R2-fixed procedure on the Windows platform that surfaced finding 3: 16/16 installed
files UNCHANGED against the 0.6.0 manifest, bundle replaced by copy-over-in-place (28 on
disk vs 27 manifested, the extra being `MANIFEST.sha256` itself), 16/16 UNCHANGED on the
0.7.0 re-classification, stamp re-written last. The §9 owner work is **TFit PR #9**:
Model policy applied as the kit default (no `"model"` pin — the optional half left
unexercised), both kit-bound twins deleted per their disposal notes, index reconciled.
One flag raised in that PR for the owner: the 2026-07-19 copy was *not* a byte-twin — it
carried the provenance header and the 14-finding absorption audit (vs. 0.4.0, three
versions stale); preserved at `git show cce681c:spec/SDLC_FIELD_REPORT_2026-07-19.md`
and summarized in this repo's `FIELD_REPORT_2026-07-20.md` companion note. After the
merges, only the fan-out watch and F3 remain.

### Resume here — owner-confirmed order, 2026-07-22

1. **Build R2** (the map above), `/kit-check` clean, release as `v0.7.0`, migrate TFit
   at the next arc boundary — the migration itself exercises Finding 3's fix on the
   platform that surfaced it.
2. **TFit owner work, carried from §9:** apply the *Model policy* section to
   `spec/SDLC.md` (confirm/adjust opus-planning / sonnet-code / haiku-collection;
   optionally pin `"model"` in settings); delete the two field-report twins from
   `spec/`.
3. **Watch the fan-out** on the next real `/plan-phase` and record one line in §9's
   acceptance bullet — closes F2's last residual.
4. **Then F3** (slice-runner TRIAL, §3, unchanged in shape) — kit untouched unless all
   four pass criteria hold; ships as the then-current next minor only if they do.
   *(Superseded ordering note, 2026-07-22: G1 — §11 — was owner-decided to precede F3
   and is built; F3 remains next after it.)*

### State as of 2026-07-22, end of session

- Kit `main`: the triage commit is `6f4e9ed` (this hand-off follows it); working tree
  otherwise clean. **Not yet pushed** — the only thing held. `v0.6.0` remains the
  latest release; no tag work pending until R2 ships.
- TFit `main` = origin at `cce681c` (Arc 3 retro committed), CI green, on kit 0.6.0
  with the floor now reconciled at 32 (the retro's own fix); its `spec/` still holds
  the two field-report twins and still lacks the Model policy section — both owner
  work, resume steps 2 above.
- Next session opens directly on **R2 step 1** — the batch is fully specified in the
  map above and every claim behind it was pre-verified against the tree this session;
  no analysis is pending, it is edit work. `/kit-check` closes it, then `v0.7.0`.
- Nothing else is in flight: no scratch adoptions live, no subagent output awaited,
  no undecided questions. The one deliberate residual (F2 delegation mechanics) waits
  on a future `/plan-phase`, not on this repo.

---

## 11. G1 — the gap-analysis batch *(triaged and built 2026-07-22; owner-decided: G1 before F3)*

> **Status: SHIPPED, 2026-07-22.** All 14 edit-map rows applied, plus the release
> bookkeeping (`VERSION` → 0.8.0, CHANGELOG entry, README tree line for the committed
> source document). Owner decisions taken the same day: build G1, commit
> `CRITICAL_GAPS_ANALYSIS.md`, and G1 precedes F3 in the §10 resume order. Released
> as `v0.8.0` (tag pushed, `release.yml` green in 9s, three assets published;
> `checkout` bumped to v5 right after — its v4 deprecation warning was the run's one
> annotation). **TFit migrated the same day** (PR #10, merged `e5b5b88`, owner
> approval at halt 5): 16/16 UNCHANGED against the 0.7.0 manifest, copy-over-in-place,
> 16/16 UNCHANGED + bundle 27/27 against the 0.8.0 manifest, stamp re-written last,
> gate green. Carried in that PR as owner follow-up: TFit's instantiated `spec/SDLC.md`
> predates the 0.8.0 templates — the hotfix exception, the deploy-outcome bookkeeping
> (with a Render verification pointer for the deploy note), and the consequence sweep
> are flagged for manual porting. Next: the fan-out watch, then F3.

Source: `CRITICAL_GAPS_ANALYSIS.md` (root), an external review of the kit at 0.7.0
naming five gaps. It was **challenged before acceptance**, per owner instruction, and
most of it did not survive the challenge. What follows records the verdict (so the
document is never re-triaged from scratch), then the edit map for the five S-effort
changes that did survive — each shaped like R2: small, reconcile-shaped, markdown-only.

### The verdict — what was challenged, what stood

The document is factually careful (no false claims about the kit's contents were found)
but fails its own cross-cutting §5 standard: every gap argues from hypothetical failure
modes, none from an observed defect. In the kit's own vocabulary, all five are
`suspected`, not `measured`:

- **Gap 1** (state machine interpreted, not enforced) recycles four real incidents as
  evidence — all four already fixed (v0.2.0, R1, R2) and all four *caught by the retro
  loop*, which cuts against the urgency claim. Its "interpreted vs. mechanical"
  dichotomy is refuted by invariant 13's own specimen: three deterministic checks
  returned confident wrong answers in one session. The operative axis is "has the check
  demonstrated its negative case", not prose-vs-code. Its closure condition ("a
  transition *cannot be represented* as complete unless…") quietly demands an
  enforcement engine while claiming not to prescribe one. **Kernel accepted:** verify
  transitions against artifacts the agent did not author — already the kit's direction
  (R2's floor reconcile); becomes invariant 14 (G1.5).
- **Gap 2** (delayed integration): zero occurrences in three arcs, and structurally
  near-moot under current rules — one unmerged arc branch, strictly sequential slices,
  solo owner: main cannot drift mid-arc except by a hotfix the rules don't yet define.
  **Sliver accepted:** define the hotfix path (G1.2). The rest is a team-scale gap,
  parked pending that expansion.
- **Gap 3** (not risk-adaptive): the one *real* over-processing datum on record (FR2's
  uniform re-derivation) was already fixed by R2's proportional rule — incremental risk
  adaptation by field evidence, the kit's existing method. The document's own "Important
  tension" section demolishes every profile-assignment scheme it gestures at.
  **Hook accepted:** a consequence sweep in `/plan-phase` (G1.4), justified by the
  owner's Daiwa (finance) target, where small high-consequence changes are real.
- **Gap 4** (no full SDL): wrong product scale; a compliance encyclopedia invites
  bypass, and scanners/identity models are project facts commands may not state.
  **Sentence accepted:** security checks CI already runs are part of "the gate must
  match CI" (G1.3). The rest waits for the first Daiwa adoption's field report.
- **Gap 5** (lifecycle ends at merge): most upgraded by the owner's answers — TFit
  deploys to Render, work usage will deploy via GitHub Actions. **Kernel accepted:**
  the deploy question hardens into a recorded, reconciled outcome (G1.1). Canary,
  incident lifecycle, and delivery metrics stay parked.

Owner answers that re-weighted the triage (2026-07-22): target is a small enterprise
team at Daiwa, devs mostly solo per service; TFit has a Render production deploy; no
state divergence observed since R2; flexibility high, maintenance low — which rules out
shipping executable enforcement tooling (the kit's one POSIX line already broke on
Windows in the field; a lifecycle CLI multiplies that surface).

### Edit map

| # | File | Edit |
|---|---|---|
| G1.1 | `commands/end-phase.md` step 7 (deploy bullet) | when the project deploys ({{DEPLOY_NOTE}} ≠ none): after the deploy, **verify the deployed artifact is the merged commit against the platform's own record** (the Actions deploy run's SHA, Render's deployed-commit field — an artifact the agent did not author), and record the outcome in the Phase History row's Notes cell: `deployed+verified <date>` / `deploy pending — <where tracked>` / `n/a — no deploy`. A merged-but-undeployed phase must not read as complete in START HERE |
| G1.1 | `templates/SDLC.template.md` phase-end step 6 | canonical statement of the same (inv 2: same batch as the command) |
| G1.1 | `templates/PROJECT_INDEX.template.md` (Phase History comment) | note that deploying projects carry the deploy outcome in the Notes cell |
| G1.1 | `templates/CLAUDE.template.md` (~line 32) | "(merge, deploy question)" → deploy question *and recorded outcome* |
| G1.1 | `commands/sdlc-setup.md` (New Round 3 + Existing step 2 — both deploy questions) | the {{DEPLOY_NOTE}} answer now also captures **how a deploy is verified**: where the platform exposes the deployed commit, and the URL/command for a post-deploy smoke check. Same placeholder, richer resolution — no inv-3 impact |
| G1.2 | `templates/SDLC.template.md` (Shape, after the one-arc paragraph) | the hotfix exception: an urgent production fix while an arc is open branches `fix/<slug>` off main, gets its own minimal PR (gate green against the baseline; review scaled to the diff; merge approval is halt 5 as ever), and its own Phase History row — it is not a slice of the arc. Afterward the arc branch merges main and re-runs the gate before its next slice. This is the **only** sanctioned second unmerged branch |
| G1.2 | `commands/next-slice.md` §3 | the unmerged-arc-branch check gains: if main has moved since the arc branched (a hotfix landed), merge main into the arc branch and re-run the gate before starting the slice; the "second branch" warning cross-references the hotfix exception |
| G1.3 | `reference/GATE_RECIPES.md` (intro, after "the gate must match CI, or the gate lies") | security checks CI already runs (dependency audit, secret scan, SAST) are part of "what CI runs": fast ones join the local gate; slow or credentialed ones stay CI-only but are listed in the gate section of `spec/SDLC.md` so merge readiness includes them knowingly — the same placement logic as the coverage floor (enforced in CI, recorded locally) |
| G1.3 | `commands/sdlc-setup.md` (Existing step 1 survey) | collect any security scanning CI runs, alongside the existing CI/CD survey items; step 2's proposed gate folds them in per the GATE_RECIPES rule |
| G1.4 | `commands/plan-phase.md` step 4 | new **consequence sweep** (between trust-boundary and cross-system): scan behaviors for authentication/authorization changes, money or financial calculation, destructive or irreversible data operations (migration, deletion, retention), credential handling, regulated data. Each hit must name its extra verification in the spec (slice exit criteria or the acceptance checklist) and appear in Risks & Deferred; a hit absorbed silently is the finding |
| G1.4 | `templates/SDLC.template.md` phase-start step 2 (sweep enumeration, ~:142) | add "consequence sweep" to the list (inv 2) |
| G1.5 | `KIT_INVARIANTS.md` | new **invariant 14 — a recorded value names its enforcing artifact**: any value or state the process records in prose must name the artifact that enforces it, and the step that writes it must reconcile the two (or state explicitly that it is claim-only). **Specimen, already on record:** TFit's coverage floor — recorded 28 → 32 in two prose homes while `gate.yml` enforced 28 for two days (FIELD_REPORT_2026-07-22 finding 1) |
| G1.5 | `.claude/commands/kit-check.md` §3 | the invariant-14 reading pass: enumerate record-a-value steps in commands/templates; each names its enforcing artifact and reconcile step, or is explicitly claim-only |
| G1.5 | root `CLAUDE.md` (~:68) | "13 invariants" → "14 invariants" |

### Decisions

- **Deploy outcome lives in the existing Notes cell**, not a new Phase History column —
  project-owned files are never migrated by `/sdlc-update`, so a schema change would
  fork every existing adopter's table.
- **The hotfix branch is the only sanctioned second unmerged branch**; `next-slice`'s
  unmerged-branch check remains the guard, now with a defined answer instead of a
  vacuum.
- **G1.3 adds no mandatory tooling.** The rule only folds in what CI already runs;
  scanners are project facts and stay out of command prose (inv 1 holds).
- **The consequence sweep adds no owner halt.** Hits route through the existing
  question/decision mechanism; the five-halt-point invariant stands.
- **Invariant 14 ships now, not later** — its specimen requirement is already satisfied
  by FR3 finding 1; waiting would add nothing. It is kit-development-side only (nothing
  installed changes for G1.5), and the batch is its own first test: G1.1's deploy
  outcome must name its enforcing artifact (the platform's deploy record) to pass the
  check it helps create.
- **Rejected or parked — do not re-litigate without field evidence:** the lifecycle
  enforcement engine / state schema (gap 1 as scoped), risk profiles (gap 3 as scoped),
  the full secure-development lifecycle (gap 4 as scoped), slice PRs or any change to
  the arc/PR unit (gap 2 as scoped), and deployment lifecycle states beyond the
  outcome record (gap 5 as scoped). Grounds are recorded in the verdict above.
- **The source document is committed at the root** (kit-development artifact, same
  class as the field reports) — owner-confirmed 2026-07-22; the README file tree
  gained its line (inv 9).

### Ripple check (§4a discipline — derived by grep this session, not recalled)

`deploy` → `end-phase.md`, `SDLC.template.md`, `CLAUDE.template.md:32`,
`PROJECT_INDEX.template.md` (comment), `sdlc-setup.md` ×2 (both modes' questions) — all
in the map. Sweep enumeration → `SDLC.template.md:142–144` + `plan-phase.md` step 4 —
both in the map. Branch rules → `next-slice.md` §3 + `SDLC.template.md` Shape;
`end-slice.md` has no branch-rule text (verified by grep, no match). Invariant count →
root `CLAUDE.md:68` only; the README states no count (grep: no match). Security → no
existing mentions to reconcile. Install set unchanged → `reference/SKILLS.md` has no
role (verified, not assumed). No kit files added or renamed → README tree untouched by
the batch itself; only the source document's own line if the owner commits it.
`MANIFEST.sha256` regenerates at release (inv 10), `VERSION` → next minor at ship time
(process changes are minor, R1 precedent), `CHANGELOG.md` gains the entry. `/kit-check`
closes the batch — including the first run of the invariant-14 pass over the batch's
own edits.

**Ordering:** R2's precedent routed fix batches ahead of F3, and G1 touches files F3's
trial would exercise — recommendation is G1 before F3, but the resume-list order in §10
was owner-confirmed, so re-ordering it is the owner's call, not the batch's.

---

## 12. Fourth field report and R3 — triaged 2026-08-01

> **Status: BUILT, 2026-08-01 — `v0.9.0` pending release.** Every claim below was
> verified against the kit tree at **0.8.0** before triage (the report is written
> against **0.6.0**, and R2/G1 had since touched five of the eight implicated files).
> All 18 edit-map rows applied plus two added during the build (recorded in *Built as*
> below), the report committed at the root, invariant 15 shipped, and the release
> bookkeeping done (`VERSION` → 0.9.0, CHANGELOG entry, `MANIFEST.sha256` regenerated —
> nine bundle files changed, `sha256sum -c` clean, README tree line added).
>
> **Built as — deltas from the map:** (a) `end-phase.md` §3 gained the owner's-shell
> clause (R3.5's third home — the report implicated it, the map did not list it; it is
> where the failure actually surfaces); (b) `end-slice.md` §7 hand-back now reports
> discarded findings, which R3.4's rule in §3 references and would otherwise dangle
> (inv 6). Both are one-clause additions in files the batch already opened.

Source: **[sdlc-kit#1](https://github.com/ghostpencil/sdlc-kit/issues/1)**, filed
2026-08-01 — a `/sdlc-retro` report from the same adoption as the three prior reports,
covering its **fifth** phase (a three-slice security arc touching the live authorization
path and LLM spend): 15 commits, 3 slices, 1 PR, 44 numbered owner decisions, 8 findings
with a priority table. Gate movement over the adoption: tests 7 → 338, CI floor 12 → 42,
lint held at 0, **typecheck 175 → 171** — the last of those is finding 3.

**This report is a different class from `CRITICAL_GAPS_ANALYSIS.md`.** G1's source argued
from hypothetical failure modes and mostly did not survive challenge; every finding here
cites an observed defect with evidence, and seven of eight survived verification intact.
The challenge pass changed *scope* and *attribution* on three of them, and found one
already fixed — it did not refute any.

### Verified against the tree at 0.8.0 — what stood, what changed

| # | Claim | Verdict at 0.8.0 |
|---|---|---|
| 1 | Nothing asks whether a control is actually live in production | **Stands, and the void is total.** `grep -rn -i "flag-gated\|feature flag\|dormant\|inert\|rollback\|environment variable\|deployment manifest" commands templates reference` → **zero matches**. G1's consequence sweep (`plan-phase.md:75–81`) would have *flagged* this arc (auth + money) but only demands the extra verification be named — never that a neutralized-by-configuration claim be checked against production configuration. `end-phase.md:82–95` asks whether the deploy happened and verifies *which commit* shipped (G1.1); it never asks what the deploy turns **on** |
| 2 | Decisions ratified before anything is measured | **Stands.** `plan-phase.md:55–56` (*Tuning*) asks which numbers are adjustable, never how they were arrived at; the spec skeleton's `## Owner Decisions` (:109) carries no provenance. **Reshaped:** the kit already owns the vocabulary — `measured`/`suspected` on backlog entries (`next-slice.md:41–50`, R2) — so this extends an existing mechanism rather than adding one |
| 3 | The type leg has a stated ratchet and no mechanism | **Stands; one quotation is not verbatim.** The report quotes *"a ceiling to drive down… never a budget to spend"*; 0.8.0's template says *"The baseline only ever moves down, as the STABILIZATION backlog burns it toward zero"* (`SDLC.template.md:92–94`) — same ambition, older seeding. The mechanism gap is exact: `end-phase.md:101–109` carries the coverage-floor bump-and-reconcile bullet and there is **no type-leg counterpart anywhere** (verified by grep). The `(ceiling held)` rendering is the project's own — the kit specifies no gate-reporting format, so the fix *seeds* a convention rather than changing one. **This is a second specimen of invariant 14:** one leg reconciles against its enforcing artifact, the other records into a vacuum |
| 4 | `/end-phase` applies review fix batches without verifying findings | **Stands verbatim.** `end-phase.md:60` — *"Run `pr-review-toolkit:review-pr`… Apply fix batches"*, nothing between. **Ripple the report missed:** `end-slice.md:55–63` has the identical shape — triage straight to *Fix now* with no verification step. Same one-sentence fix, both files |
| 5 | Agent-verified vs owner-executed commands are not distinguished | **Stands.** `sdlc-setup.md:182` collects the run command from the owner's *answer*; nothing has the owner run it. `CLAUDE.template.md:107` (`{{RUN_COMMAND}}`) is where the unverified value lands, and `end-phase.md:30–35` is the one step that exercises it. The nearest existing rule (`sdlc-setup.md:228–230`) covers local-vs-CI, a different axis |
| 6 | A repeated environmental hazard has no path from recorded to enforced | **Stands.** No recurrence threshold anywhere. **But the escalation shape already exists** at `end-slice.md:99–102` (a new gate dependency is recorded *and* added to CI in the same commit) — so this generalizes a rule the kit already ships, which drops it from the report's M to an S |
| 7 | Slice write-ups accumulate with no archival discipline | **Stands, but the attribution is wrong.** `PROJECT_INDEX.template.md` seeds no per-slice section at all, and `end-slice.md:94–103` says only *"mark the slice done"* — the 2,400 lines are the project's elaboration, not a kit-prescribed append. The kernel survives on its own terms: **no section is marked bounded and no step ever removes anything**, so any project that elaborates gets this outcome |
| 8 | Friction entries have no closure path | **Half already fixed.** `sdlc-update.md:146–149` has copied-in-place since **0.7.0** — the `rm -rf` the report cites is a 0.6.0 artifact, and its own footnote (*"on Windows the directory…"*) is this same adopter's incident. The aging half stands: `sdlc-retro.md:70–81` sweeps the friction log and reads it for *content*, never for **status or age** |

### R3 — the fix batch *(recommended: ships as `v0.9.0`, before F3)*

Same shape as R2 and G1: small, reconcile-shaped, markdown-only. No new files (except
the report itself), no new placeholders, no tooling — the maintenance-low constraint
from G1's owner answers still holds.

| # | File | Edit |
|---|---|---|
| R3.1 | `commands/plan-phase.md` step 4 (consequence sweep, ~:75) | two additions to the existing sweep, not a new sweep: (a) a claim that a consequence is **neutralized by configuration** (flag, env var, "ships inert", "dormant", "changes nothing in prod") must name the variable and **quote its value from the artifact that configures production** — the deployment manifest, not the test environment, which is configured to be false; a claim that cannot be quoted from a production artifact is an open question, not a decision. (b) each hit names its **independent off switch** — a control whose only lever also disables an unrelated system has no rollback, and that is a finding before the slice, not after |
| R3.1 | `commands/end-phase.md` step 7 (deploy bullet, ~:82) | the deploy question extends from *did it happen* to **what does this deploy turn on** — which controls become live that were not, and the lever for each; recorded with the deploy outcome already in the Notes cell |
| R3.1 | `templates/SDLC.template.md` phase-start step 2 + phase-end step 6 | canonical statement of both (inv 2 — same batch as the commands) |
| R3.2 | `commands/plan-phase.md` step 3 (*Tuning*, :55) + step 5 skeleton (`## Owner Decisions`, :109) | a decision carrying a number is tagged **`measured`** (with the run, count, or query it came from) or **`estimated`** — the same distinction the backlog already draws, applied where the number is first ratified |
| R3.2 | `commands/next-slice.md` §2 | the slice that implements an `estimated` decision re-derives it **before** scope confirmation, and a changed number goes back to the owner as a question — reusing R2's proportional re-derivation rule verbatim rather than adding a step |
| R3.2 | `templates/SDLC.template.md` phase-start step 2 + slice-loop step 2 | mirror both (inv 2) |
| R3.3 | `commands/end-phase.md` step 7 | the type leg's counterpart to the coverage bullet: record the current typecheck count against the baseline in `spec/SDLC.md`; if it fell, lower the baseline in the same docs commit; if it did not, the owner **ratifies holding it** and the record says how many arcs it has been unchanged. A ceiling nobody is asked about is not a ratchet |
| R3.3 | `templates/SDLC.template.md` gate-baseline section (~:92) | the boundary procedure canonically, plus the reporting convention: an unchanged red baseline renders as **`N (unchanged for K arcs)`**, never `held` — a stall must not read as an achievement |
| R3.4 | `commands/end-phase.md` §5 (:60) | *"Verify each finding against the source before it enters a fix batch; report findings that did not survive verification alongside those that did."* The reporting half is not optional — a discarded finding is evidence about the reviewer |
| R3.4 | `commands/end-slice.md` §3 triage (~:55) | the same sentence at slice-review triage (ripple, not in the report) |
| R3.5 | `commands/sdlc-setup.md` (New Round 3 + Existing step 2, both run-command questions) | the owner **runs the acceptance command in their own shell during setup** and pastes the result; the resolved interpreter/toolchain path is recorded in PROJECT_INDEX's Environment gotchas. The rule is generic; the path is a project fact and lands in a project-owned file (inv 1 holds) |
| R3.5 | `templates/SDLC.template.md` (acceptance-review step) | any command the **owner** executes is verified in the owner's shell — an agent's shell is a different environment and only the owner's is authoritative for acceptance instructions |
| R3.6 | `commands/end-slice.md` §6 (~:99, beside the gate-dependency rule) | recurrence threshold: an Environment gotcha recorded for a **third consecutive slice** becomes a gate step or a hook, or is explicitly ratified unpreventable and marked as such. Prose in a status document is not a control |
| R3.6 | `templates/SDLC.template.md` gate section | the escalation rule canonically (inv 2) |
| R3.7 | `templates/PROJECT_INDEX.template.md` | mark each section **bounded** (Phase, START HERE, gate baseline — a fresh session reads these first and they must stay short) or **growing** (backlog, Phase History, friction log), and state that per-slice detail, if a project keeps it, is not this file's job past the phase close |
| R3.7 | `commands/end-phase.md` step 7 bookkeeping | at phase close, move the closed phase's per-slice detail into that phase's spec file — which already exists and is already the historical home — leaving the Phase History row and a paragraph |
| R3.8 | `commands/sdlc-retro.md` §2 (friction sweep, ~:70) | the sweep reports **unabsorbed entries with their age**, and any entry older than one phase is carried into the new report automatically. The log already distinguishes absorbed from live; nothing reads that distinction |
| R3.9 | `KIT_INVARIANTS.md` + `.claude/commands/kit-check.md` + root `CLAUDE.md` (~:68) | **owner's call:** new **invariant 15 — every verification step names the environment it verifies against**, with the report's cross-cutting theme as its specimen. See *Decisions* |
| — | root: `FIELD_REPORT_2026-08-01.md`, `README.md` tree (inv 9), root `CLAUDE.md` field-report paragraph | commit the report as a root file, same class as the three prior ones (G1 precedent for committing its source document) — **owner confirmation, as G1's was** |

### Decisions

- **Findings 1 and 2 are the batch.** They are the only two that nearly shipped real
  harm (a spend cap enforcing while three documents called it dormant; caps implying
  ~$10,200/month), and both are S-effort. If the batch has to shrink, it shrinks from
  the bottom.
- **Nothing here adds a halt point.** R3.1's rollback lever and R3.2's re-derivation
  route through the existing question/decision mechanism; R3.3's ratification happens
  inside the bookkeeping conversation, like G1.1's deploy outcome. The five-halt-point
  invariant stands.
- **R3.2 reuses `measured`, and adds `estimated` rather than reusing `suspected`.**
  `suspected` is about a *cause*; a number's antonym is how it was obtained. Two words
  in one vocabulary is the cost; inventing a second vocabulary is worse.
- **R3.5 keeps the value out of command prose.** The rule ("verify in the owner's
  shell") is generic and installable; the interpreter path is a project fact and lives
  in Environment gotchas — invariant 1, and the same split G1.3 used for scanners.
- **R3.7 ships reduced.** The template gains bounded/growing marks and `/end-phase`
  gains the archival move; the kit does **not** start prescribing per-slice write-up
  blocks it never prescribed in the first place.
- **Invariant 15 is genuinely optional (R3.9).** For: the specimen requirement is met
  (finding 1 — the gate proved the code correct in the test environment while the
  control was live in production), it is readable as a pass over `commands/` and
  `templates/`, and it is the report's cross-cutting theme in one line. Against: the
  ledger grew to 14 nine days ago, and R3.1/R3.3/R3.5 each fix one instance — the
  invariant may be earning its place or may be generalizing three fixes that have not
  yet been in the field. **Recommendation: ship it**, on the same grounds G1 shipped
  inv 14 — the batch is its own first test, and R3.1's dormancy check must name the
  production artifact to pass it.
- **Do not re-litigate:** finding 8's `sdlc-update` half (fixed in 0.7.0 — do not
  "fix" it again), and the report's `(ceiling held)` rendering as a *change* (the kit
  never specified a format; R3.3 seeds one).
- **What worked well is load-bearing and stays protected:** mutation-testing every new
  guard (`end-slice.md` §4), the whole-arc review (`end-phase.md` §5), recording
  corrections in place, and owner acceptance review before the PR (`end-phase.md` §3) —
  the owner named all four independently, and finding 5 exists *because* the fourth one
  is in the process. Any future simplification pass must clear these explicitly.

### Ripple check (§4a discipline — derived by grep this session, not recalled)

Dormancy/rollback vocabulary → **zero existing occurrences** across `commands`,
`templates`, `reference` (grep above), so R3.1 adds vocabulary rather than reconciling
it. Consequence sweep → `plan-phase.md:75–81` + `SDLC.template.md:150–153` (both in the
map). Deploy question → `end-phase.md:82–95` + `SDLC.template.md` phase-end step 6 +
`sdlc-setup.md` ×2 — R3.1 touches the first two; setup's deploy questions need no change
(they already capture *how* a deploy is verified, G1.1). Gate baseline → `SDLC.template.md:86–102`,
`end-phase.md:23–25`, `end-slice.md:26–29` — R3.3 touches the template and `end-phase`
step 7 only; the two "green means green" paragraphs are unaffected (they define the
comparison, not the ratchet). Review-then-apply → `end-phase.md:60` **and**
`end-slice.md:55–63`; `REVIEW_LENSES.md` has a *verify the denominator* lens (:34) but
nothing about a finding's premise — no reconcile needed there. `{{RUN_COMMAND}}` →
`CLAUDE.template.md:107` only (grep). Friction log → `PROJECT_INDEX.template.md:49–59` +
`sdlc-retro.md:70–81`; the "mark absorbed" convention already exists, R3.8 reads it.
No new placeholders (R3.5 records into an existing project-owned section, not a
template slot) → invariant 3 unaffected. Install set unchanged → `reference/SKILLS.md`
has no role. `MANIFEST.sha256` regenerates at release (inv 10); `VERSION` → 0.9.0
(process changes are minor, R1 precedent); `CHANGELOG.md` gains the entry with
**[installable]** marks on five commands and **[adoption-only]** on the templates.
`/kit-check` closes the batch.

### Resume here

1. ~~**Build R3**~~ — done. Both owner calls went the recommended way: invariant 15
   shipped, and the report is committed at the root.
2. ~~`/kit-check`, then release `v0.9.0`~~ — done. Clean pass (two findings fixed in
   the session, plus one pre-existing gap closed: `SDLC.template.md` had never
   mentioned `/sdlc-retro`). Tag pushed, `release.yml` green in 11s, three assets.
   `sdlc-kit#1` closed with a finding-by-finding mapping comment.
3. ~~**Migrate TFit**~~ — done the same day, PR #13 (merged `40c08bd`): 16/16
   UNCHANGED against the 0.8.0 manifest, 6 content-changed of 16, bundle 28 on disk =
   27 + manifest with nothing un-manifested, copy-over-in-place, 16/16 + 27/27 against
   0.9.0, and the negative case demonstrated (the same 6 read DRIFTED against the old
   manifest afterward). Gate 0 lint / 171 type / 338 passed.
4. ~~**The template-side port**~~ — done, PR #14 (merged `0a2a6f3`). **Twelve rules,
   not the nine estimated** — the estimate omitted the review-verification rule and the
   deploy-activation question, and folded archival with the bounded/growing marks.
   Two TFit records corrected in passing: friction #4 claimed "still open in the kit"
   while being submitted upstream as finding 8, when `/sdlc-update`'s `rm -rf` had been
   fixed in **0.7.0** five days earlier (backlog #84 closed), and `PROJECT_INDEX.md`
   (2,529 lines) is now marked bounded/growing.
5. ~~**The fan-out watch**~~ (§10 step 3, F2's last residual) — worked 2026-08-01,
   **closed as far as artifacts can close it**; the finding is recorded in full in §9's
   acceptance bullet. Short version: Phase 05's *"two mutually contradictory analyses"*
   (`PHASE_05:531`) is positive evidence that the sweeps ran independently, since a
   sequential in-context pass would have reconciled them; but no artifact records a spawn
   and none ever will, so **waiting for another `/plan-phase` was the wrong instruction**
   and the claim is downgraded rather than completed (inv 8). One live observation during
   Phase 06 planning closes it for free; otherwise it stands as-is permanently.
   **Carried:** the `sdlc-surveyor` spawn has *no* field evidence at all — if Phase 06's
   feasibility checks do not use it, that is a signal about the optional step, not noise.
6. ~~**Then F3**~~ — **done, and declined.** The trial ran three slices on TFit Phase 06
   and closed 2026-08-02: the slice-runner does not enter the kit and `/next-slice`
   stands. §14 carries the disposition, the five findings, and the two candidate kit
   changes that are being held for the next `/sdlc-retro` rather than written now.

**Standing note for the next retro** (raised 2026-08-01, not yet field-tested): R3 is
the fourth batch of process rules added on field evidence with no simplification pass
between them. The next `/sdlc-retro` is the place to ask which earned their keep —
finding 6's escalation threshold and finding 2's re-derivation are the two most likely
to read as ceremony if they never catch anything. A rule that costs and returns nothing
is a finding too.

---

## 13. F3 trial — S2's pre-registration *(sealed 2026-08-01, before the slice ran)*

Kept in this repo rather than in TFit, and the placement **is** the point: TFit's
`CLAUDE.md` §"Writing or changing app code" tells *every* session there to read
`spec/PROJECT_INDEX.md` first, and the runner's spawned implementation agent is one of
those sessions. Anything written there about what the runner is being measured on is
readable by the thing being measured. TFit's `spec/SLICE_RUNNER_TRIAL.md` carries a dated
stub pointing here; this text is copied back into it, unedited, once S2 closes.

### The instrumentation leak — a finding before it is a precaution

Until 2026-08-01 the trial's protocol was documented *inside the adopted project's own
source of truth*. `spec/PROJECT_INDEX.md` stated outright:

> **S2 must exercise the runner's `blocked` round trip**: after S1, two of the trial's four
> pass criteria (state loss across a respawn, halt-3 fidelity) are still untested because
> S1 raised no design question. Per the trial protocol, if none surfaces naturally in S2, a
> genuine spec ambiguity gets planted so one must.

An agent that reads that has every incentive to manufacture a design question. It would
have produced a **false pass on criterion 2** and a respawn that measured nothing — and
the trial would have recorded a success. The text has been replaced with a non-leaking
note that says a pre-registration exists, says where, and says why it is not here.

The generalisation outlives this trial: **a trial documented inside the artifact its
subject reads cannot measure unprompted behaviour.** If F3 is ever encoded into the kit,
the instrumentation rule ships with it — the same way the review step does.

**Residual leak, accepted and recorded rather than fixed:**
`.claude/commands/next-slice-runner.md` states all four criteria and the plant note in its
own body. Nothing directs a session to read it, so the exposure is far below
`PROJECT_INDEX.md`'s, but it is not zero. Editing the command mid-trial would change the
instrument between slices and make S1 and S2 incomparable, which costs more than the leak.

### Why S2, and why the timing had to move

The money is not where it looks. S2's ~$10.50 is **entirely in labelling** — $2.88 for the
prompt-cache write plus 40 × ~$0.19 — and the sweep that follows is *free*, because BM25
costs nothing per question (D6). A respawn mid-*sweep* would therefore have been a free
respawn and a weak test of criterion 1, whatever it looked like in the log. The ambiguity
has to fire **mid-labelling**, with partial labels in hand and the 1-hour cache clock
running.

### The plant

**Question: may the golden set contain questions whose correct source is one of the 6
image-only documents?** D21 accepts that they are structurally unretrievable by BM25 — no
full-text index can ever return them, and under retrieval they are reachable only through
D4's unit index. S2 says "~40 labelled questions" and never states the sampling frame. The
spec connects neither to the other.

Genuine in both directions, which is what qualifies it as a plant rather than a trap:

- **Include them** → recall@k is structurally capped below 100%, and the floor enforced in
  `gate.yml` governs a metric containing known-impossible cases.
- **Exclude them** → the set omits the corpus's known-weak region, which is exactly the
  failure the spec's own Residual Risk paragraph names.

It fits `blocked` cleanly — a design decision about what the metric *means*, made before
the metric exists — so it does not fall into S1's third-state hole. And the difficulty is
right: D21 plus the Residual Risk note give the agent enough to recognise the question,
and nothing gives it enough to resolve it.

**How it was made unavoidable.** Left latent it *might* have fired; the protocol wants it
to *must*. S2 now carries a sampling-frame requirement — the ~40 questions are allocated
across the full **53 emails and 65 documents** rather than written from whichever units
make questions easiest. Walking all 65 reaches the 6. The requirement is defensible
entirely on its own merits (it is what the Residual Risk paragraph is asking for), and
that is what keeps the plant honest: a real improvement to the spec that happens to force
the question, not a fabricated conflict. Image-only documents are **not** named in the
frame, so it forces the walk without pointing at the answer.

### Settled at step 2 instead — the metric definition (D23)

Document-level labels keyed on `citation_key`, owner-decided 2026-08-01. Left to the agent
this would have been a *budget failure*, not a trial result: chunk-level labels are
invalidated by every step of the chunk-size sweep, forcing a relabel at each of the four
widths at ~4 × the approved $10.50. The runner's step 2 says scope questions belong to the
main session before the spawn, so resolving it there follows the protocol rather than
coaching the agent.

### Free backup probe, left unresolved on purpose

Recall@k alone **cannot** choose `SCORE_FLOOR` and `MIN_HITS`: escalation only ever *adds*
the 118 summaries, so `SCORE_FLOOR = 0` / `MIN_HITS = 0` trivially maximises measured
recall. The spec never states the second objective; D7 gestures at one (*"reopen if the
golden set shows escalation firing so often that a router would cut cost"*) without giving
a target. It fires during the free sweep and is informative either way — raised, it is a
second data point for criterion 2; resolved silently, it is a contract violation and a
finding, since the runner forbids exactly that.

### Predictions, recorded before the run

1. **The halt burns the cache clock.** The TTL is one hour; owner response is human
   latency. If the halt runs long, the respawn pays $2.88 again *however good the agent's
   disk discipline was*. This is a counterexample class the runner's *"respawning is cheap
   by design"* does not contemplate: an agent can hold a **perishable paid resource**, and
   cheapness then depends on owner response time rather than on the kit's write-to-disk
   rule. Log the halt's wall-clock beside the state-loss finding or the two confound.
2. **Nothing in the brief tells the agent to persist labels before blocking.** S1 passed
   criterion 3 only because the brief said *"do not paraphrase, do not round, do not say
   all green"* — and the log flags that it is untested whether it holds unprompted.
   Instructing persistence would buy criterion 1 the same hollow pass. The kit already
   requires state worth keeping to live on disk; whether an agent *following the kit* does
   it when failure costs real money is the whole measurement.
3. **Expected shape of a pass:** the fresh agent resumes from labels on disk, re-writes the
   cache only if the TTL expired, and redoes no labelling. **Expected shape of a fail:**
   labels held in agent context only, and the respawn re-spends some fraction of $7.60.
   Either outcome closes criterion 1; only the second stops the trial.

**Seal opened 2026-08-02, after S2 closed**, and copied unedited into TFit's
`spec/SLICE_RUNNER_TRIAL.md` as promised. Scored: **predictions 1–3 were never reached**
(no halt, no respawn), the plant fired through the escalation gate rather than labelling
and arrived after the paid work was done, and the money premise was wrong — $3.99 spent
against the ~$10.50 modelled. The design error is the transferable one: the
pre-registration assumed a binary (block, or resolve silently) when a **third option
existed and the agent took it** — measure both readings and refer the choice to the slice
that must own it. **No plant can force criterion 2 while the question stays deferrable.**
One cost of sealing is on the record too: S2's calling session, blinded to the instrument,
deliberated a decision already made and logged *"no ambiguity was planted"* — true from its
knowledge, false in fact. Blinding the observer protects the measurement and corrupts the
log; §14's disposition inherits that as an open design question, not a solved one.

---

## 14. F3 — trial CLOSED, the runner does not ship *(2026-08-02)*

**Disposition: `/next-slice` stands.** Three slices on TFit's Phase 06 arc — S1 chunk+FTS
index, S2 golden set, S3 tiered retrieval — closed at S3's close-out under the rule
recorded *before* S3 ran. **No CHANGELOG entry**, per §5: F3's trial produces none until it
passes, and it did not. The full record is TFit's `spec/SLICE_RUNNER_TRIAL.md`, now closed
and marked a record rather than a live instrument.

### The four criteria, as they actually landed

| # | Criterion | Result |
|---|---|---|
| 1 | No state loss across a respawn | **NEVER TESTED** — no respawn in three slices |
| 2 | Halt 3 verbatim to the owner, answer back to the agent | **NEVER TESTED** — no `blocked` return in three slices |
| 3 | Gate results survive the boundary un-summarized | **Conditional pass, degrading** — verbatim at S1, mypy's body elided to `...` at S2, unestablishable at S3 |
| 4 | Owner would choose the runner again | **MIXED** — and its cost half never got a number |

### Criteria 1 and 2 did not fail — they never fired, and that is the finding

Not flakiness. Two agents met the *same* genuine spec conflict — D8/B3's "fewer than
`MIN_HITS` **chunks**" against the 59 of 118 units that have no chunk at all — and neither
reached for `blocked`, because both times a better move existed. S2 measured both readings
and deferred the choice to the slice that owns it; S3 decided it, pinned it by test, and
reported it in the commit message. **For a slice with a spec this detailed, `blocked` is
rare by design — the halts get spent at scope confirmation, before the spawn.**

Consequence for anyone who revisits this: `blocked` and respawn-recovery would have shipped
**unexercised**. The owner ruled out manufacturing an event, correctly — the only ambiguity
that can force a halt is one making the slice uncompletable either way, which is spec
corruption in an artifact four downstream slices depend on. A trial that needs the event
needs many more slices, not a cleverer plant.

### What the trial did establish — and it is not what it set out to test

**The value attaches to the re-derivation before the spawn, not to the spawn.** Same
conclusion in all three slices, from `/next-slice` step 2 — the part the runner never
moved:

- **S1 and S2 both carried an unsatisfiable exit criterion** ("raised from CI's printed
  number" / "a floor enforced in `gate.yml`"). CI has neither archive nor index, and
  `gate.yml` never runs on an arc branch at all. The same defect twice, caught at scope
  confirmation both times and missed by the planning sweep both times.
- **S2's approved budget did not cover S2.** The ~$10.50 itemised the offline harness and
  omitted the 3–5 live spot-checks named in the same sentence (~$3.03). Raised in the halt,
  re-approved at ~$13.50.
- **D27 is the strongest single result of the trial.** Re-deriving the evidence for
  `SCORE_FLOOR = 3.0` *disproved* the claim it existed to make reproducible: the 3.292
  off-corpus figure does not reproduce, an in-corpus generic probe scores **5.651** and is
  not escalated, so the separation margin is negative. A re-derivation that retracts a
  ratified number is the rule paying for itself outright.

### The argument against the runner, stated as the log states it

Three slices, three reviews, one shape: **the agent nets the mechanism it set out to net,
and what escapes is everything composed with the diff.** Rigor was never the problem — 28
mutations inside S3's slice, 8 more on the review fixes, each killed on exactly its own
test. What got through: **S1**, three docstrings asserting properties their tests did not
exercise; **S2**, a fixture net holed precisely where the headline number is most sensitive
(dropping one `::`-split left 16/16 tests green while moving the real-corpus figure 40/40 →
39/40); **S3**, a **CRITICAL** — one DuckDB connection shared across threads under
`ThreadingHTTPServer`, **410 of 600 concurrent selects returning the wrong question's
passages**, and 26 raising `ValueError` past a narrow `except duckdb.Error`, leaving
`do_POST` with no response written. Two browser tabs is enough.

⚠️ **An argument, not a measurement.** No slice was run both ways, so whether an unspawned
`/next-slice` session would have caught any of it is untested. The trial log says so itself
and this section does not upgrade it.

### The new finding — and the trial committed it against itself

**A number that lives only in a transcript is not a number.** The owner decision recorded
before S3 named exactly two measurements, at exactly S3's close-out, for exactly the reason
that criterion 4's cost half was "in theory." **Neither exists.** S3's session skipped the
trial log — the trial's own instrument — and everything transcript-only died with the
session.

Fourth appearance of one failure in a fresh costume, and the sharpest, because this time
the instrument ate itself. It is a sibling of the third field report's theme (*a number
recorded in prose is not the number the machine enforces*) by a different mechanism: **a
step whose output nothing downstream blocks on is a step that gets skipped.** The gate
blocks on lint, types and tests. Nothing blocks on "was the observation written down."

### Candidate kit changes — identified, and deliberately NOT taken

1. **The review step needs nothing.** `commands/end-slice.md` step 3 already runs the
   reviewer without asking, already refuses to mark a slice done with unfixed CRITICALs,
   and already carries the *consumers of changed behavior* lens whose stated rationale is
   that "the defects that survive clean slice reviews live one layer away." Three slices
   produced three confirmations. **This is a rule that earned its keep** — which is exactly
   what R3's standing note asks about the last four batches, now with an answer for one of
   them.
2. **One real gap, one candidate lens.** S3's CRITICAL is not reachable by either inline
   lens or either lens in `reference/REVIEW_LENSES.md` (error propagation; verify the
   denominator). A per-request object holding a single connection under a threading server
   is neither a changed consumer nor a simplified double — it is **shared mutable state
   under the runtime's concurrency model**, with a measured consequence (410/600) rather
   than an asserted severity.

**Why the lens is not being written now.** R3's standing note (§12) records that R3 was the
fourth consecutive batch of process rules added on field evidence with **no simplification
pass between them**. Writing a fifth batch's worth the moment that note was made is
precisely what it warns against. The concurrency lens goes to the next `/sdlc-retro` as a
candidate, alongside finding 6's escalation threshold and finding 2's re-derivation — and
it arrives there with one thing the others lack: the re-derivation rule **demonstrably**
earned its keep three times in three slices, D27 included.

### State of the plan after F3

Every batch in this file is now closed — F1, R1, F2, R2, G1, R3 shipped; F3 tried and
declined. **The backlog is empty.** The next input is field evidence: TFit's Phase 06 close
(`/end-phase`, and the first close that must answer for the 171 type-error ceiling under
R3.3 — now four arcs unchanged), and the `/sdlc-retro` that follows it.

> **Update 2026-08-03: it landed.** Phase 06 closed 2026-08-02 (TFit PR #15); the retro
> filed **[sdlc-kit#2](https://github.com/ghostpencil/sdlc-kit/issues/2)** — 10 findings,
> ingested verbatim as `FIELD_REPORT_2026-08-02.md`. R3.3 fired for real: the 171 ceiling
> was **not** ratified; TFit's Phase 07 is a stabilization arc whose product is that
> number falling. **Owner decision on batch order (2026-08-03, do not re-litigate):** the
> simplification pass the report ranks first (finding 7 — audit every rule added since
> 0.5.0 against a confirmed catch, convert survivors from "do this" toward "this is done
> when") runs **as its own batch, before R4**. Otherwise the fifth batch of added steps
> would arrive inside the pass meant to prune the previous four. Triage: §15.

---

## 15. Fifth field report — triaged 2026-08-03; SIMP queued before R4

> **Status: BUILT — both batches shipped 2026-08-03.** SIMP shipped as `v0.10.0`
> (§16); R4 built as `v0.11.0` (§17). Every claim below was verified against the kit tree at
> **0.9.0** before triage — and for the first time verification was pure claim-checking:
> the report is written against the *current* release, so nothing can have been fixed
> since it was filed. Nine of ten findings stand as filed (three with step-number or
> scope corrections); finding 9 repeats a misattribution §12 already caught once, and
> its fix is actionable anyway. **Owner decisions (2026-08-03, do not re-litigate):**
> the simplification pass (finding 7) runs **as its own batch — SIMP, proposed
> `v0.10.0` — before the fix batch R4 (proposed `v0.11.0`)**.

Source: **[sdlc-kit#2](https://github.com/ghostpencil/sdlc-kit/issues/2)**, filed
2026-08-02, ingested verbatim as `FIELD_REPORT_2026-08-02.md` — the same adoption's
sixth phase, its first BUILD arc: 33 commits, 5 slices, 1 PR, 31 numbered owner
decisions, 10 findings. Theme: **the kit specifies what each step must produce and
almost never what makes it done** — the gate is the only step with a completion
condition and the only step that never failed. Three of the ten findings sit at the
phase boundary, where the previous three retros found little; the process's weight has
moved to where its checks are thinnest.

### Verification against the tree at 0.9.0

| # | Finding | Verdict |
|---|---|---|
| 1 | Review fan-out mutated the shared tree; commit claimed the lost fixes | **Stands.** All three read-only quotes verbatim (`agents/sdlc-surveyor.md:12`, `plan-phase.md:66`, `sdlc-retro.md` §2). Clean tree checked at `end-phase.md` §1:17, never re-asserted at §5. **Scope correction:** the clean-tree precondition cannot apply verbatim to `end-slice.md` §3 — the slice review reviews the *uncommitted working diff by design* (:33–35); there the fix is read-only discipline on the reviewer, not a clean tree |
| 2 | Acceptance halt vacuous on flag-gated arcs; nothing requires a real run | **Stands.** "the phase's visible behavior" verbatim at `SDLC.template.md:74`. **Attribution correction:** the testability sweep is `plan-phase.md` **step 4**, not step 2 (step 2 is candidate selection) |
| 3 | Whole-arc review has no completion condition | **Stands.** "Then apply the surviving batches, re-run the gate, push" at `end-phase.md` §5:76. **Ripple the report missed:** `SDLC.template.md` phase-end item 4 carries the same wording — inv 2 says both change together |
| 4 | No lens reaches shared mutable state under the concurrency model | **Stands — pre-agreed.** `REVIEW_LENSES.md` has exactly the two lenses named. This is §14's own candidate arriving at the retro as promised. **Ripple the report missed:** `end-slice.md` §3:52 enumerates the lens triggers inline ("changed error propagation or swept the codebase"), so a third lens updates that sentence too |
| 5 | Planning wrote an unsatisfiable exit criterion twice | **Stands.** Contradiction sweep checks decisions against decisions; testability sweep checks behaviors; nothing checks exit criteria against what observes them. **Attribution correction:** step 4, not step 2 — and step 5's closing line ("exit criteria a test (or the acceptance checklist) can verify") is the natural home for the fix |
| 6 | Friction log has a reader, an aging rule, no writer | **Stands.** `grep -ri friction` over the bundle: `sdlc-retro.md` and `PROJECT_INDEX.template.md` only. R3.8 confirmed in the 0.9.0 CHANGELOG. No command writes to the log |
| 7 | Five rule batches, no simplification pass | **Stands by construction** — it quotes the kit's own §12 standing note back at it. Owner-ranked first; becomes SIMP. Root-only: the one finding an adopter cannot act on |
| 8 | The F3 trial had four safety criteria and no value criterion | **Stands.** §3's trial protocol verified: four pass criteria, all safety. Fix lands at the root (this file, §5), not in the bundle |
| 9 | Per-slice detail written into the wrong file; R3.7 relocates, doesn't prevent | **Misattributed, fix actionable.** "`end-slice.md` step 9" does not exist — the file has seven steps; the close-out record is step 6, and it prescribes *no* per-slice detail blocks (mark done, backlog entries, gotchas, next slice). Same catch §12 made on the fourth report's finding 7. But the adopter wrote 83–163 lines five times against the kit's silence, so silence is not prevention: an explicit status-only clause is cheap. R3.7's own fate (keep as safety net vs delete per the report) is **SIMP's call**, made with the audit in hand |
| 10 | R3.6's control handed out an unscoped remediation command | **Stands.** `end-slice.md` §6:108–116 verified — "a gate step, a hook, or a test", nothing about the control's output. One-clause fix, and the report correctly notes the *verify the denominator* lens is exactly what the message failed |

**The "worked well" list is triage input, not decoration.** Four practices carry
confirmed catches from this arc alone — mutation testing (9 survivors at 100% line
coverage, all killed), re-derivation before the slice (R2/R3.2 — retracted a ratified
number, caught both bad exit criteria and a short budget), the whole-arc review (fifth
arc running it caught what slice reviews missed), and R3.4's verify-before-apply (3 of
31 findings re-graded or discarded). Plus R3.1 paying twice in one session (deploy
verified inert *and* a prior arc's liveness claim disproved from the same log), and
R3.3 producing its first mandatory answer (the ceiling was not ratified). These seed
SIMP's protected list.

### SIMP — the simplification pass *(own batch, first; proposed `v0.10.0`)*

Scope, per the owner's ruling and the report's suggested fix:

1. **Enumerate the denominator first** (second report's lesson, applied to the pass
   itself): every rule added in R1 (0.5.0), F2 (0.6.0), R2 (0.7.0), G1 (0.8.0), R3
   (0.9.0) — from the CHANGELOG entries and the edit maps in §7, §9, §10, §11, §12.
   The audit shows the count it examined equals the count that exists.
2. **Ask of each rule:** what did it catch, in which adopter, when? Sources: five field
   reports, the trial log's record in §13–§14, TFit's retro evidence quoted in the
   report. A rule with no confirmed catch after two releases is a deletion candidate —
   presented to the owner as a list, not deleted silently.
3. **Convert survivors from "do this" toward "this is done when"** where the rule
   admits a completion condition — the report's cross-cutting theme, and the form the
   gate (the only never-skipped step) already takes.
4. **Known candidates going in:** R3.7's relocation step (finding 9 — fired once,
   moved 1,571 lines, file still 1,716 lines after); R3.8's aging rule (nothing to age
   — verdict contingent on R4 shipping finding 6's writer); any rule whose only
   evidence is the defect that motivated it.
5. **SIMP adds no new rules.** Everything additive — the lens included — waits for R4.
   Deletions and rewordings of installable files make it a real release: version bump,
   CHANGELOG, manifest, `/kit-check`.

### R4 — the fix batch *(after SIMP; proposed `v0.11.0`)*

Edit map, in the report's damage order, ripples added from verification:

| Rule | File(s) | Change |
|---|---|---|
| R4.1 | `end-phase.md` §5 + `SDLC.template.md` phase-end 4 (inv 2) | clean tree with every fix committed is a stated **precondition of spawning the review fan-out**, re-asserted at §5 where it is load-bearing; a commit message may not claim a fix that has no test pinning it |
| R4.1 | `end-slice.md` §3 | the reviewer reviews the working diff by design, so the discipline binds to the **agent**: the review is read-only in the shared tree — no `git checkout/restore/stash`, fixes come back as findings, never as edits |
| R4.2 | `end-phase.md` §3 + `SDLC.template.md` halt 4 + `plan-phase.md` step 4 (testability sweep) | when no slice's exit criteria required running the application, `/end-phase` adds a local real-data pass of the composed system before the PR; the testability sweep flags the all-slices-behavior-neutral condition at planning time |
| R4.3 | `end-phase.md` §5 + `SDLC.template.md` phase-end 4 (inv 2) | the fix batch is assembled only after **every** reviewer has returned, and goes through the gate as one unit; a later-arriving finding re-opens the review rather than starting a second batch |
| R4.4 | `reference/REVIEW_LENSES.md` + `end-slice.md` §3:52 (trigger pointer) | the §14 lens, with 410/600 as its specimen: for every object that outlives a request or is reachable from more than one, name the runtime's concurrency model and state what serializes access |
| R4.5 | `plan-phase.md` steps 4–5 | each slice exit criterion names **what observes it and when** (a local command, the gate, CI on the main branch, the owner); an observer that does not run at that point is a planning defect. The kit's own ratchet phrasing is the exposure — every adopter whose CI runs only on main inherits it |
| R4.6 | `end-slice.md` step 6 | one bullet beside the gotcha/gate-dependency bullets: was anything in this slice friction with the *process*, and if so write it to the Kit friction log now — giving R3.8's aging rule a writer |
| R4.7 | `end-slice.md` step 6 | slice close-out records **status only** — one line; detail lives in the phase spec and the commit message. Whether R3.7's archiving bullet stays as a safety net is decided in SIMP |
| R4.8 | `end-slice.md` §6 | one clause: a control that hands the operator a remediation command must scope that command to the population the control actually flags |
| R4.9 | this file, §5 | trial protocol rule: a trial pre-registers **what the change is supposed to buy and how that is measured**, alongside its safety criteria — F3's four measured only safety, and a trial that cannot fail on value cannot justify shipping. Also recorded for any future F3-shaped work: `blocked` is rare by design (halts get spent at scope confirmation), and the two-state return contract needs *done-except-outside-boundary* and *done-with-deferred-design-question* |
| R4.10 | `sdlc-retro.md` step 5 (:153–156 gate + :142 skeleton line) | extends the existing "not yet a finding" gate rather than adding a step: a finding **quotes the implicated text from the kit file, at a section number read off the file at writing time** — or, for a silence finding, locates the silence between two named steps — and names **every home** of the quoted wording (a rule usually lives in a command *and* `spec/SDLC.md`'s canonical statement; a fix touches them together). Skeleton line becomes "by path and quoted section". Not from the report — from its triage: two consecutive reports shipped citations written from memory of the process (report 4: finding 7's attribution, finding 3's non-verbatim quote; report 5: "plan-phase step 2" ×2, the nonexistent "end-slice step 9", finding 1's fix contradicting `end-slice.md` §3's own design), every one caught only maintainer-side. R3.4 makes the *review* verify findings against the source; the retro — which produces findings about kit files — carried no such rule. Enters R4 by SIMP's own standard: two confirmed would-be catches, not a hypothetical |

Cross-cutting, both batches: every batch ends with `/kit-check` (§5); README file-tree
and root-CLAUDE.md roster already updated at ingestion. The report's own numbering is
trusted nowhere the tree disagreed — the three step-number corrections above are why
§4a's rule (ripple lists are incomplete until walked) now applies to reports as well as
to this plan.

---

## 16. SIMP — the simplification pass *(audit done 2026-08-03; owner decisions pending)*

> **Status: DECIDED 2026-08-03 — building.** Owner decisions at the halt, all four
> dated 2026-08-03, do not re-litigate: **(1) the surveyor is DELETED now** — agent
> file, spawn sentence, install mapping, the lot ("it will never get called from what
> I have seen and we haven't seen much benefit from spawning our own agents in this
> kit") — the recommended final-warning marker was declined for the stronger form;
> **(2) the doubles lens stays**; **(3) R3.7's archival bullet stays as the safety
> net** behind R4.7's prevention; **(4) all six conversions approved.** The deletion
> retires the `agents/` → `.claude/agents/` install mapping (the surveyor was its
> only occupant) and requires the update path's first **removed-from-install-set**
> clause — machinery the deletion needs to reach adopters, not a new process rule.
>
> The §15 scope executed:
> denominator enumerated from the CHANGELOG (0.5.0–0.9.0) cross-checked against the
> edit maps (§7, §9, §10, §11, §12), every rule audited against the catch record in
> the five field reports, the trial record (§13–§14), and the TFit migration notes
> (§10–§12). Verdicts below are **proposed**; deletions happen only on owner decision.

### The denominator

Unit of audit: **one process requirement with its own trigger and cost** — not one
CHANGELOG bullet (bullets bundle) and not one edit-map row (rows split by file).
Enumerated: **38 adopter-facing rules** — R1: 18, F2: 5, R2: 3, G1: 4, R3: 8 — with
one supersession (R1's `*.md eol` offer widened into F2's `* text=auto`, counted once
under F2). Kit-development-side additions (invariants 14 and 15, their `/kit-check`
passes, the issue templates, the release-asset renaming) are out of audit scope: they
constrain this repo, not an adopter's process. Cross-check: every 0.5.0–0.9.0
CHANGELOG `[installable]`/`[adoption-only]` bullet and every §7/§10/§11/§12 edit-map
row maps into the 38; nothing in either source is uncovered.

### The audit — catches are quoted from the record, not remembered

Rule types matter for what counts as evidence: a **check** proves itself by catching;
a **constraint** proves itself by its founding defect not recurring under exercise; an
**availability** (optional tool, defined path) costs nothing until used and can only
be audited on use.

**Confirmed catches — 24 rules, the protected core.** The heavy hitters, each with at
least one post-ship catch on record:

| Rule | Catch record (post-ship only) |
|---|---|
| Mutation check (R1, `end-slice.md` §4) | FR4: 5 gaps converted to fact + caught the session's own no-op fix; trial: 28+8 mutations killed on exactly their tests; FR5: 22 at arc close, 9 survivors at 100% line coverage found and killed |
| Re-derivation before the slice (R1+R2+R3.2, `next-slice.md` §2) | FR3: "still earns its keep"; trial/FR5: **D27 retracted a ratified number**, caught two unsatisfiable exit criteria and a budget that omitted half its own sentence |
| Consumer-of-changed-behavior lens (R1, `end-slice.md` §3) | §14: three slices, three confirmations of its rationale; quoted by FR5 finding 1 as the discipline to extend |
| Verify findings before applying (R3.4) | FR5: 3 of 31 re-graded or discarded, one of which would have driven a repo-wide change in the wrong direction |
| Inertness + deploy-activation (R3.1) | FR5: **paid twice in one session** — deploy verified inert as designed, and a prior arc's CSRF liveness claim disproved from the same log (never live, fixed same day) |
| Type-ceiling ratchet (R3.3) | FR5: first mandatory answer — the 171 ceiling **not** ratified; TFit Phase 07 exists to lower it |
| Coverage bump-and-reconcile (R2) | FR5: two homes agree, second arc running; 42→52 bumped in one commit — the founding drift never recurred |
| Gotcha escalation (R3.6) | FR5 finding 10: the mandated control "worked exactly as designed — failed the gate the same minute" an editor rewrote 685 lines |
| Deploy question + verified outcome (R1+G1.1) | FR5: the live-server verification lineage — M4's acceptance gap found ~3h after phase "completion"; the CSRF disproof above |
| Update-path rules (R1 ×3 + R2 copy-in-place) | three clean migrations (PRs #8, #10, #13) including the Windows platform that broke the old mechanism; the enumeration visibly working (28 on disk = 27 + manifest, nothing un-manifested) |
| Retro co-development clause + unactioned-friction sweep (R1) | FR5 finding 4 exists because the retro read §14; finding 6 is the sweep reporting its own starvation — the reader working on an empty log |
| measured/suspected + measured/estimated vocabulary (R1+R3.2) | FR5: all 26 new backlog entries tagged; the budget and threshold catches above ride on the tags |
| Plan-phase fan-out + governing rules (F2) | §12.5: two mutually contradictory sweep analyses = positive evidence of independence; FR5 finding 1 cites the read-only discipline as the model |
| Branch rules + halt-2 narrowing + volatile-bundle warning + changed-vs-touched + boundary-only updates + reviewer naming + model poll + eol pin (R1/F2) | constraints under continuous exercise, founding defects unrecurred (the eol pin: FR5 shows all 128 committed blobs correct while working copies drifted — the pin's job done; the drift is editor-side and now gated by R3.6's control) |

**No post-ship catch — presented honestly, per §15's own criterion** ("no confirmed
catch after two releases is a deletion candidate"):

| Rule | Age | Standing cost | Assessment |
|---|---|---|---|
| `sdlc-surveyor` agent + optional feasibility spawn (F2) | 4 releases | ~zero (an availability; one sentence in `plan-phase.md`, one installed file) | **Zero observed uses in four arcs** — §12 carried exactly this signal clause. Complication: FR5 finding 1 quotes its text as the read-only-discipline specimen R4.1 copies, and deleting an install-mapped file complicates every future `/sdlc-update`. **Owner decision** |
| Test-doubles lens (R1, `end-slice.md` §3) | 5 releases | one bullet per slice review | No attributed post-ship catch. But its failure class is demonstrably alive — FR5's S2 fixture hole (one dropped `::`-split, 16/16 green, headline number wrong) is the premise recurring, caught by other means. Founding defect was live in production. **Owner decision; recommend keep** |
| Hotfix exception (G1.2) | 2 releases | zero until a hotfix happens | Unexercised. Fills a vacuum that was real (the only defined answer to "second branch"). Recommend keep |
| Security-checks-in-gate (G1.3) | 2 releases | setup-time only | Unexercised — no adopter with security CI on record yet; Daiwa-targeted. Recommend keep |
| Owner-shell verification (R3.5) | 1 release | setup-time + one clause | Under the two-release threshold; founding defect was a command broken for four phases. R4.2 extends the same step. Keep, re-audit next pass |
| Mock policy (R1, `TESTING.template.md`) | 5 releases | template prose, zero recurring | Constraint whose exercise is invisible from here (adopter-side test authorship). Keep |

**The two §15-named candidates:**

- **R3.7's relocation** (archive per-slice detail at phase close): fired once, moved
  1,571 lines, the file was still 1,716 lines after — FR5 finding 9's arithmetic:
  written wrong five times, corrected once. R4.7 adds the prevention (status-only
  close-outs). **Owner decision:** keep the archival bullet as the safety net for
  legacy accumulation and leaks (recommended), or delete it as the report proposes
  once prevention ships.
- **R3.8's aging rule**: nothing to age — the log has had no writer for three arcs
  (FR5 finding 6). **Contingent keep:** R4.6 ships the writer; if the log is still
  empty at the retro after next, the aging rule goes. Same contingency covers F2's
  friction-log seed itself.

### Conversions — "do this" → "this is done when" *(rewordings, not new rules)*

Six spots where a survivor admits a completion condition in one clause, applying FR5's
cross-cutting theme to the rules that stay. Deliberately excluded: the whole-arc
review and the acceptance pass — their completion conditions are R4.3 and R4.2,
additions that belong to R4.

1. `end-slice.md` §3 (triage): done when every finding is dispatched — fixed,
   deferred-with-tag, discarded-with-reason, or raised to the owner — and the
   hand-back names the discards.
2. `end-slice.md` §4 (mutation): done when every new guard has been seen to fail on
   exactly its own test — a guard not yet seen to fail is not yet closed.
3. `next-slice.md` §2 (re-derivation): done when every `estimated` number the slice
   implements carries a recorded derivation, and every changed number went back to
   the owner.
4. `end-phase.md` step 7 (coverage): done when the workflow value and both recorded
   homes are identical — sharpening the existing assert into the stop condition.
5. `end-slice.md` §6 (gotcha escalation): a third-recurrence hazard is closed only as
   a check or a ratified-unpreventable entry — never as a sharper note.
6. `sdlc-retro.md` §2 (friction sweep): done when no unabsorbed entry is left
   unreported — each named with its age.
7. `templates/SDLC.template.md`: the canonical statements of 1–5 move in the same
   batch (inv 2).

### What SIMP does not do

No new rules (everything additive waits for R4), no new files, no new placeholders,
no halt-point changes. The batch's headline is honest and small: **the audit found the
rules mostly earned their keep** — 24 of 38 with post-ship catches on record, exactly
as FR5 predicted ("a pruning, not a retreat") — and the pruning is one availability
with zero uses, one relocation bullet under owner judgment, two contingent keeps, and
six completion-condition rewordings.

### Built as — 2026-08-03

The surveyor deletion ran wider than the file, because the file was the mapping's only
occupant: `agents/sdlc-surveyor.md` removed; `plan-phase.md` keeps the feasibility
practice agent-free (verify seams by quoting the codebase) and drops the
surveyor-exclusion sentence from the sweep paragraph; `sdlc-setup.md` loses the
preflight `agents/` check, the install block (both modes), the Explore-type aside, and
the Low tier's "kit-set" instance; `reference/SKILLS.md` loses its row;
`SDLC.template.md` loses the kit-set-model sentence; both READMEs and root
`CLAUDE.md`'s flow diagram lose the mapping; `KIT_INVARIANTS.md` inv 1/4/7 and
`/kit-check` scopes updated ("since 0.10.0 the mapping has one destination").
`sdlc-update.md` gained the **removed-from-install-set clause** (step 5, symmetric to
new-files; mirrored in the root README per inv 8) and keeps `.claude/agents/`
classification for the 0.6.0–0.9.0 transition — an updating project's surveyor copy is
deleted when `UNCHANGED`, owner's call when `DRIFTED`. Six conversions applied as
listed, five mirrored in `SDLC.template.md` (the friction sweep lives retro-side
only). Bookkeeping: `VERSION` → 0.10.0, CHANGELOG entry (with a **Removed** section,
the kit's first), manifest regenerated at 26 entries (27 − surveyor, `sha256sum -c`
clean), README trees updated. `/kit-check` closes the batch.

### Hand-off — state as of 2026-08-03, end of the SIMP session

- **Shipped and verified.** `v0.10.0` released (tag pushed, `release.yml` green, three
  assets); the published tarball itself checked — zero `agents/` entries, 26 files,
  `VERSION` reads 0.10.0. `/kit-check` clean on all 15 invariants; the one in-pass
  finding (a regenerated manifest carrying sha256sum's binary-mode `*` prefixes, which
  would have broken both classification scripts' `$2` matching) was fixed and
  discrimination re-proven. Kit `main` = origin at the SIMP commit; working tree clean;
  nothing in flight.
- **Next session opens directly on R4** (`v0.11.0`) — the ten-rule edit map in §15 is
  fully specified and verified against the tree at 0.9.0; SIMP touched three of its
  target files (`end-slice.md`, `end-phase.md`, `next-slice.md` — conversions only, no
  §15 row invalidated) so re-read the exact anchor lines before editing, per §4a. Two
  R4 rows carry SIMP-decided context: R4.7 keeps R3.7's archival bullet as the safety
  net (owner decision, §16), and R4.6's writer is what R3.8's contingent keep waits on.
- **TFit migrates 0.9.0 → 0.11.0 directly, once, after R4 ships** — owner-decided
  2026-08-03. Skipping 0.10.0 is the update command's documented case (classify against
  0.9.0's manifest, copy from the target); the removal clause fires on the same hop, its
  first real exercise: `.claude/agents/sdlc-surveyor.md` should classify UNCHANGED and
  be deleted. **Phase 07 must not open before that migration** — the arc-boundary
  window is open now, and `/plan-phase` would close it until Phase 07's end.

---

## 17. R4 — the fix batch, built 2026-08-03 *(ships as `v0.11.0`)*

All ten rules of §15's edit map landed as specified, anchor lines re-read against the
tree at 0.10.0 per §4a before editing (SIMP's conversions had moved lines in three
target files; no row was invalidated, and every anchor was found where the re-read put
it). R4.1's read-only-reviewer wording was written fresh rather than copied — the
surveyor specimen the report quoted was deleted in SIMP.

**Ripples the map did not carry, found by the §4a walk and the `/kit-check` inv-2
pass, not recalled:**

- `SDLC.template.md` phase-start item 3 — R4.5's observer rule is a process rule, so
  inv 2's mirror obligation applies even though the map named only `plan-phase.md`;
  exit criteria in the canonical spec skeleton now name what observes them.
- `templates/PROJECT_INDEX.template.md`, two section comments — the bounded-sections
  comment now states R4.7's write rule (status only; archival is the safety net, not
  the plan), and the friction-log charter names R4.6's writer (`/end-slice`'s
  close-out) instead of describing recording-at-the-moment as aspiration. Both were
  homes of the changed wording in exactly the sense R4.10 now requires findings to
  enumerate.

`/kit-check` ran clean on all 15 invariants — no in-pass findings this time.
Bookkeeping: `VERSION` → 0.11.0, CHANGELOG entry (nine [installable] bullets, one
[adoption-only] mirror bullet, R4.9 noted as root-side), manifest regenerated at 26
entries with discrimination proven (exactly the eight edited bundle files changed
hash; text-mode hashes, no `*` prefixes — §16's in-pass finding did not recur).

### Hand-off — state as of 2026-08-03, end of the R4 session

- **R4 is committed; the fifth report is fully actioned** — all ten §15 rows plus
  SIMP's four owner decisions are on disk. Nothing from `sdlc-kit#2` remains queued.
- **Release status: shipped and verified.** Tag `v0.11.0` pushed (owner-approved),
  `release.yml` green (run 30815265100 — manifest-coverage check, package, publish all
  passed), three assets published. The published tarball itself checked, not assumed:
  `CHECKSUMS.txt` verifies both archives, 27 files, zero `agents/` entries, `VERSION`
  reads 0.11.0, and the shipped `MANIFEST.sha256` verifies clean against the extracted
  contents. Kit `main` = origin at the R4 commit; working tree clean; nothing in
  flight.
- **TFit migration DONE — 2026-08-03, PR #16 merged.** 0.9.0 → 0.11.0 in one hop,
  exactly per the several-versions case: 16 UNCHANGED / 1 UNKNOWN (the trial's
  project-local runner, untouched) / 0 DRIFTED, denominator 17/17. The
  removed-from-install-set clause passed its first real exercise: the surveyor
  classified UNCHANGED and was deleted from both `.claude/agents/` (directory now
  gone) and the kept bundle, which was enumerated first (28 = 28, zero un-manifested)
  and replaced by copy-over-in-place. Re-classification against the 0.11.0 manifest:
  all copied files UNCHANGED — the two runs disagreeing about the copied files is the
  discrimination proof. Gate CI green on the PR; only project-owned line touched was
  the `spec/SDLC.md` stamp. **Phase 07 is now free to open** on kit 0.11.0.
- **Next session opens on owner-led brainstorming** (owner-decided 2026-08-03, end of
  the R4 session): the owner wants to plan additional improvements with the session,
  not work a queued batch — nothing is queued. Come with the kit's own record as the
  raw material: the five reports' cross-cutting themes, §16's audit (what earned its
  keep, what is on a clock), and the §4 rejected list, so brainstorming starts from
  evidence rather than a blank page. Ideas that survive get triaged into this plan the
  usual way before anything is built.
- **Standing kit inputs, independent of the brainstorm:** any sixth field report
  (TFit Phase 07 would produce it). R3.8's aging rule is on a clock — if the friction
  log is still empty at the retro after next despite R4.6's writer, it goes (§16
  contingent keep).

---

## 18. Brainstorm triage — 2026-08-03; three batches queued (LEG → COP → STD)

The owner-led brainstorm the §17 hand-off called for. Six owner ideas, clustered into
three themes against the tree at 0.11.0 and the record (five reports' themes, §16's
audit, §4's rejected list). **Owner decisions, all dated 2026-08-03 — do not
re-litigate:** (1) batch order is **LEG, then COP, then STD**; (2) secure coding
ships as review lenses, not a new command; (3) logging and error handling ship as
setup interview + project-owned conventions + fail-loud lenses + gate rules where
mechanical — not prose standards.

The clustering, with the original idea numbers: LEG = ideas 5+6 (token cost of the
prompts; owner-facing verbosity), COP = idea 4 (Copilot CLI), STD = ideas 1+2+3
(logging, error handling, secure coding).

### LEG — the legibility batch *(next to build; ships as `v0.12.0`)*

Input-side and output-side legibility, in that internal order — **LEG.1 first**, so
LEG.2's baseline measures the tree that includes it (LEG.1 adds words, LEG.2 removes
them; one batch keeps the tension honest).

- **LEG.1 — owner hand-back standard.** Every owner-facing moment (the five halt
  points and each command's hand-back) gets a required format: a dirt-simple
  executive summary in plain English, bullet form, with every owner decision
  **numbered and explicitly marked**. Canonical statement lands in
  `templates/SDLC.template.md` (inv 2 — the template wins); the four daily commands
  plus `sdlc-retro.md` and `sdlc-update.md` enforce it at their halt/hand-back
  steps. Motivation: the owner finds phase/slice output so detailed it is hard to
  follow — the record's sixth theme, before a report files it: five generations of
  rigor fixes, none of them for owner legibility.
- **LEG.2 — measured token pass.** Per-file token baseline over `sdlc-kit/` first
  (the denominator, enumerated not assumed), then trim wording for economy without
  losing meaning — **wording, not rules**: §16 just established the rules earn their
  keep, and no rule, halt, or completion condition is in scope. `/kit-check` on all
  15 invariants closes the pass; the before/after counts are recorded here so the
  reduction is a measurement, not an assertion.

### COP — Copilot CLI research spike *(read-only; no build decision)*

Idea 4 reshaped into a bounded investigation, because it touches the kit's deepest
couplings (the `.claude/commands/` install path, the settings.json hook, built-in
skill references, subagent/model-tier language). Deliverables:

1. The enumerated denominator of Claude-Code-specific couplings in the kit — every
   file, every mechanism, found by sweep rather than recall (§4a applies).
2. Copilot CLI's actual current capabilities, verified against its documentation at
   spike time, not remembered — which of those couplings it can express, which it
   cannot.
3. A verdict with evidence: portable-with-translation-layer, fork-required, or
   decline. **Nothing is built until the owner reads that report** — execution-model
   changes ship on evidence (§4, the slice-runner precedent).

Sequencing note: COP runs before STD because its findings may reshape STD's lens
work (portable lenses vs. Claude-only built-ins — the `/security-review` built-in
the kit currently recommends does not exist on Copilot CLI).

### STD — the standards batch *(logging, error handling, secure coding)*

The kit's first product-quality standards — opinions about what the built software
does at runtime, where today the kit's only runtime opinions are tests, coverage,
and types. A real scope extension, done in the shape FR1 taught (checks that fail
loudly, not prose rules):

- **Setup interview**: `sdlc-setup.md` asks for the project's logging and
  error-handling conventions; Existing Project mode *discovers* them from the code
  first and proposes, per the gate-recipes principle (match reality, not defaults).
  Answers land in a project-owned conventions file.
- **Fail-loud lenses** in `reference/REVIEW_LENSES.md`: a logging/swallowed-error
  lens (trigger: the slice added a catch/except or a new failure path — is it
  logged at the right level, or swallowed?) sited next to the existing error
  propagation lens; a small set of secure-coding lenses (owner decision 2:
  lenses, not a command — a command would duplicate the recommended
  `/security-review` built-in; revisit only if COP's verdict changes the picture).
- **Gate-side rules where mechanical**: where the language permits, lint rules
  (no-bare-except, no-console-log and kin) go into the gate via the existing
  GATE_RECIPES.md machinery — mechanical enforcement beats a paragraph.

Open at build time (not decided now): whether the conventions file is a new
template or a section of an existing one; the exact lens set; which gate rules per
ecosystem. Every addition enters the §16 audit regime — no post-ship catch after
two releases makes it a deletion candidate, so prefer few and fail-loud.

### Hand-off — state as of 2026-08-03, end of the brainstorm session

- **Nothing built this session; the queue is set.** Three batches triaged above,
  owner-ordered LEG → COP → STD. Kit `main` at v0.11.0, working tree clean apart
  from this plan update.
- **Next session opens on LEG** — LEG.1 (hand-back standard) then LEG.2 (measured
  token pass), one batch, shipping as `v0.12.0`. LEG.1's edit map should be derived
  mechanically at build time (§4a): sweep for every owner-facing hand-back and halt
  across the six installed commands, don't recall the list.
- **Standing kit inputs unchanged from §17:** any sixth field report (TFit Phase
  07); R3.8's aging rule still on its clock (§16 contingent keep).

## 19. LEG shipped — 2026-08-03; released as v0.12.0

Built to §18's definition in one session; `/kit-check` clean on all 15 invariants,
with one root-side finding fixed inside the pass (the README said "four
`FIELD_REPORT*.md` files" over a tree holding five — the stale-denominator class
again, caught by inv 9's reading pass).

- **LEG.1 — hand-back standard.** Edit map derived by sweep (§4a), not recall.
  Canonical statement in `templates/SDLC.template.md` under *Owner halt points*
  (inv 2); enforcement at every owner-facing step the sweep found: `plan-phase`
  steps 2/6 (the spec presentation — the moment that motivated the batch — now
  opens with a summary and numbers everything being ratified), `next-slice` 2/4/5
  (the derived-number return is its own marked decision), `end-slice` 3/7 (the
  hand-back restructured: summary first, dispositions as detail), `end-phase`
  3/5/6/7 (the bookkeeping conversation presents its several decisions together,
  numbered), `sdlc-retro` 2/6 (submit-upstream as a marked decision),
  `sdlc-update` 4/5 (per-file DRIFTED calls and un-manifested-file halts as
  numbered decisions). Each command restates the format inline, so an updated
  command set still carries the rule where a pre-0.12.0 project-owned `SDLC.md`
  lacks the section (the accepted [adoption-only] skew). The standard enters the
  §16 audit regime: it needs a confirmed catch — an owner decision that would
  have been missed in prose — or it is a deletion candidate after two releases.
- **LEG.2 — measured token pass.** Method recorded: `wc -w` words and bytes÷4
  token estimate per file over `git ls-files` in `sdlc-kit/`, POSIX `wc`, LF
  tree, 2026-08-03. Baseline post-LEG.1 (as §18 required): **27,882 words /
  ~46,677 est. tokens**. After the trim: **27,765 words / ~46,487** (−117 words,
  −0.4%). Wording only — no rule, halt, or completion condition touched;
  `skills/**` untouched (inv 3/11). The largest single win was Existing-mode
  setup restating New-mode asks verbatim (now cross-references). The measured
  finding, worth carrying forward: **SIMP already took the wording fat** — what
  remains is rules, negative cases, and confirmed-catch evidence §16 protects,
  so future economy gains come from structure (pointers over restatement), not
  from adjectives. A trim pass of this shape is not worth re-running until the
  tree has grown substantially.

### Hand-off — state as of 2026-08-03, end of the LEG session

- Kit `main` at v0.12.0, tag pushed, tree clean. LEG closed.
- **Next session opens on COP** (§18): the read-only Copilot CLI research spike —
  enumerate the kit's Claude-Code couplings by sweep (§4a), verify Copilot CLI's
  capabilities against its documentation at spike time, deliver a verdict with
  evidence (portable-with-translation-layer / fork-required / decline). Nothing
  is built until the owner reads that report.
- STD stays queued behind COP (§18's sequencing note: COP's verdict may reshape
  STD's lens work).
- **Standing kit inputs unchanged:** any sixth field report (TFit Phase 07);
  R3.8's aging rule still on its clock (§16 contingent keep).

## 20. COP shipped — 2026-08-03; verdict: portable-with-translation-layer

§18's read-only Copilot CLI research spike, run to its definition: couplings
enumerated by sweep (§4a), capabilities verified against GitHub's documentation on
2026-08-03, verdict delivered below. **Nothing was built; nothing is built until the
owner reads this and says so.**

### 20.1 The denominator — Claude-Code couplings in the shipped tree, by sweep

27 shipped files (`git ls-files sdlc-kit/`). Ten coupling mechanisms, found by
grepping the tree for platform markers (`.claude/`, hook vocabulary, model names,
built-in and plugin names, subagent language), not by recalling them:

| # | Mechanism | Where (files) |
|---|---|---|
| C1 | `.claude/commands/` install path for commands and skills | 9 files, 46 mentions — heaviest: `sdlc-update.md` (15), `sdlc-setup.md` (10) |
| C2 | `CLAUDE.md` as the auto-loaded instructions file | `CLAUDE.template.md` (is one), `sdlc-setup.md`, `sdlc-update.md`, `README.md` |
| C3 | Edit-time gate hook: Claude Code `PostToolUse` schema — `Edit\|Write` matcher, `tool_input.file_path` on stdin, `$CLAUDE_PROJECT_DIR`, exit-2-is-blocking, `statusMessage` | `settings.template.json` (the whole file), `GATE_RECIPES.md` (recipe + 4 `{{HOOK_*}}` placeholders), `CLAUDE.template.md`, `SDLC.template.md`, `sdlc-setup.md` |
| C4 | Slash-command invocation — the seven kit commands are Claude Code custom commands; `$ARGUMENTS` in `skills/hypothesis-tests.md`; YAML frontmatter on the five vendored skills | all of `commands/`, `skills/` |
| C5 | Model tiers by alias (`opus`/`sonnet`/`haiku`), `{{DEFAULT_MODEL}}` in settings, `/model` switching | `SDLC.template.md`, `sdlc-setup.md` (tier table), `plan-phase.md`, `settings.template.json` |
| C6 | Subagents: parallel read-only sweeps, the built-in Explore type, "subagents cannot ask the owner anything" | `SDLC.template.md`, `plan-phase.md`, `sdlc-setup.md` |
| C7 | `pr-review-toolkit@claude-plugins-official` plugin — per-slice and whole-arc review | `end-slice.md`, `end-phase.md`, `sdlc-setup.md`, `SKILLS.md`, `SDLC.template.md` |
| C8 | Recommended built-ins: `/code-review`, `verify`, `simplify`, `security-review`, `update-config`; `claude update` | `SKILLS.md` (the table), `end-slice.md` |
| C9 | `/clear`-per-slice session model | `README.md`, `CLAUDE.template.md`, `SDLC.template.md`, `end-slice.md`, `next-slice.md`, `plan-phase.md`, `sdlc-setup.md` |
| C10 | `.claude/agents/` classification (0.6.0–0.9.0 transition support) | `sdlc-update.md` |

Process-pure (zero hits): `sdlc-retro.md`, `PROJECT_INDEX.template.md` (1 incidental
hook mention), `TESTING.template.md`, `tdd-references/*`, `LICENSE`,
`MANIFEST.sha256`, `VERSION`. The process core — phases/slices/TDD, halt points, the
gate-matches-CI principle, the lenses — is platform-neutral prose.

### 20.2 What Copilot CLI can express — verified against docs.github.com, 2026-08-03

Per coupling, from the CLI command reference, hooks reference, custom-agents,
skills, plugins, and custom-instructions pages (Copilot CLI GA'd 2026-02; docs note
it "ships updates constantly" — this table is dated evidence, not a durable fact):

- **C2 instructions — yes, directly.** Reads `AGENTS.md`,
  `.github/copilot-instructions.md`, and `.github/instructions/**/*.instructions.md`.
  `CLAUDE.template.md` content ports as an `AGENTS.md` unchanged.
- **C4 commands — yes, as agent skills, not slash commands.** User-defined slash
  commands from prompt files do not exist (the command reference lists built-ins
  only; `github/copilot-cli#618` asked for `.github/prompts/` support). But **agent
  skills** (`SKILL.md` + name/description frontmatter) are explicitly invocable as
  `/skill-name` in a prompt, and the documented project-level skill locations
  include **`.claude/skills/`** alongside `.github/skills/`. The seven commands
  would each become a skill directory — a packaging change; the prompt bodies port.
  Note the near-miss: the kit installs to `.claude/commands/`, which Copilot does
  *not* read.
- **C3 hook — yes, different dialect, same reach.** Hooks live in
  `.github/hooks/*.json` (`"version": 1`, `bash`/`powershell` command keys,
  `timeoutSec`). `postToolUse` receives `toolName`/`toolArgs`/`toolResult` on stdin
  and can return `additionalContext` that reaches the model (capped 10 KB) —
  functionally what the kit's exit-2 stderr feedback does (Claude Code's "blocking"
  is also advice-to-the-model, not a rollback). Regex matcher on `toolName` replaces
  `Edit|Write`. The recipe in `GATE_RECIPES.md` rewrites; the semantics survive.
  Bonus not available on Claude Code: `agentStop` can force another turn — a
  possible "gate not green → keep going" enforcement point.
- **C5 models — yes, different names.** `/model`, `--model`, `COPILOT_MODEL`,
  persisted model in `~/.copilot/settings.json`, per-agent model pinning. The
  `opus`/`sonnet`/`haiku` alias table does not port; tier names would be
  re-interviewed at setup (the gate-recipes principle: ask, don't assume).
- **C6 subagents — yes.** Custom agents (`.github/agents/*.agent.md`,
  name/description/tools frontmatter) run as subagents with their own context
  window; a read-only "explore" profile is definable via `tools` restriction.
  Parallel fan-out is not documented — the sweeps in `plan-phase`/`sdlc-setup` may
  serialize. Flagged, not disqualifying.
- **C9 sessions — yes.** `/clear`, `/new`, `/reset` exist verbatim.
- **C7 review plugin — NO.** Copilot has its own plugin system
  (`plugin.json`: agents/skills/hooks/MCP components, marketplaces) but
  `pr-review-toolkit@claude-plugins-official` and its reviewer agents do not exist
  there. The review steps in `end-slice`/`end-phase` would need a replacement — a
  custom review agent shipped by the kit, or the review lenses run inline.
- **C8 built-ins — NO.** `/code-review`, `verify`, `simplify`, `security-review`,
  `update-config` have no Copilot counterparts; `claude update` is `npm`-style CLI
  update. `SKILLS.md`'s built-ins table and the owner-typed escalation path are
  Claude-only. (§18's sequencing hunch confirmed: the `/security-review` built-in
  the kit recommends does not exist on Copilot CLI.)
- **C1/C10 paths — translation table.** `.claude/commands/` → skill dirs;
  `.claude/settings.json` → `.github/hooks/*.json` + `.github/copilot/settings.json`;
  `.claude/agents/` → `.github/agents/`. `sdlc-setup`/`sdlc-update` would carry the
  mapping.

### 20.3 Verdict: portable-with-translation-layer

Eight of ten couplings have documented Copilot equivalents; the translation is real
(different paths, hook dialect, skills-not-commands packaging) but mechanical, and
it concentrates in six files: `sdlc-setup.md`, `sdlc-update.md`,
`settings.template.json`, `GATE_RECIPES.md`'s hook recipe, `SKILLS.md`, and the
review steps of `end-slice.md`/`end-phase.md`. The two genuine losses are C7 and C8
— the entire third-party review apparatus and every recommended built-in — which is
not an install-path problem but a *content* rewrite: a Copilot edition ships its own
review machinery or runs lenses inline. Everything else the kit is — the process,
the halt points, the gate, the specs, the TDD skills, the lenses — is prose Copilot
reads as well as Claude does.

Not fork-required: no coupling is inexpressible. Not decline: the losses are two
bounded subsystems, not the architecture. **Recommendation if built:** a translation
layer in `sdlc-setup` (target-CLI question at setup; path/hook/skill mapping table),
not a maintained second kit — a fork doubles every future batch's edit surface.
Cost honestly stated: the C7/C8 replacement is new content with no upstream, it
enters the §16 audit regime, and Copilot CLI's documented churn ("ships updates
constantly") makes any mapping table a drift liability the kit's own field reports
warn about. Whether that cost buys an audience is an owner question, not an
evidence question. **Owner decision required: build the translation layer, park
this report as reference, or decline the direction** — STD does not depend on the
answer.

### Hand-off — state as of 2026-08-03, end of the COP session

- Read-only spike; kit tree untouched at v0.12.0. This section is the deliverable.
- **One owner decision open (above): what, if anything, to do with the verdict.**
- **Next session opens on STD** (§18) unless the owner redirects: setup interview
  for logging/error-handling conventions, fail-loud lenses in `REVIEW_LENSES.md`,
  mechanical gate rules via `GATE_RECIPES.md`. COP's input to STD, now confirmed:
  keep the secure-coding work in *lenses* (portable prose) — the built-in it would
  otherwise lean on is Claude-only (C8).
- **Standing kit inputs unchanged:** any sixth field report (TFit Phase 07);
  R3.8's aging rule still on its clock (§16 contingent keep).

## 21. PORT queued — 2026-08-03; owner resolved §20's open decision: build it

**Owner decision, dated 2026-08-03 — do not re-litigate:** build the translation
layer, and solve both genuine losses (C7, C8) rather than shipping a degraded
Copilot edition. Recorded the same day §20 posed the question. Ordering (owner,
amended later the same day): **STD stays first; PORT queues behind it** (queue is
STD → PORT). The order helps PORT: STD's secure-coding lenses exist before PORT
builds the reviewer that consumes them, so PORT.3's `security-review` replacement
no longer waits on anything.

### PORT — the Copilot CLI translation layer *(queued behind STD; version assigned
at build)*

Shape per §20.3's recommendation: a seam in `sdlc-setup`, not a maintained second
kit. All §20.2 capability claims must be **re-verified against the docs at build
time** before code is written against them — Copilot CLI's documented churn is the
standing risk, and §20.2 is dated evidence, not a durable fact.

- **PORT.1 — target-CLI seam, detection-first (owner amendment, 2026-08-03).**
  `sdlc-setup.md` *detects* the target CLI before asking, in the Existing-mode
  shape the kit already uses (discover → propose → confirm; detection sets the
  proposed answer, never the answer — the prime directive stands). Signals, in
  strength order:
  1. The session itself — setup runs *inside* one of the two CLIs. Verify each
     CLI's environment marker at build time (Claude Code's session env vars;
     Copilot's documented equivalent — find it, don't assume one exists) and fall
     through to the weaker signals if neither is present.
  2. Repo artifacts (Existing mode): `.claude/settings.json`/`CLAUDE.md` vs
     `.github/copilot-instructions.md`/`.github/hooks/`/`.github/agents/`.
     `AGENTS.md` alone is not a signal (cross-agent standard).
  3. PATH binaries (`claude`, `copilot`) — machine-level, weak tiebreak only.
  Unambiguous evidence → propose as the default inside the existing interview,
  one confirm, no new question. Conflicting or absent evidence → ask open-ended.
  Both-CLIs teams answer "both" at the confirm — the mapping table must tolerate
  a dual install. One mapping table, stated once in a new
  `reference/COPILOT.md` (dated, provenance-style like `SKILLS.md`) and consumed by
  setup:
  - Commands/skills: `.claude/commands/*.md` → per-command skill directories
    (`SKILL.md` + name/description frontmatter), invoked as `/skill-name`.
  - `CLAUDE.template.md` → `AGENTS.md`.
  - Gate hook: new Copilot-dialect hook template (`.github/hooks/` JSON,
    `postToolUse`, regex `toolName` matcher, lint/typecheck output returned as
    `additionalContext`); the recipe added to `GATE_RECIPES.md` beside the
    existing one, same `{{HOOK_*}}` placeholder set (inv 1 applies).
  - Model tiers: keep High/Medium/Low as the kit's vocabulary; map to concrete
    models per CLI at interview (`/model` listing on Copilot), recorded in the
    project's `SDLC.md` — ask, don't assume (gate-recipes principle).
  - Subagent sweeps: ship a tools-restricted read-only `explore.agent.md` profile
    for `plan-phase`/`sdlc-setup` sweeps; if parallel fan-out is still
    undocumented at build time, the sweeps run serially on Copilot — noted in the
    generated `SDLC.md`, not silently.
- **PORT.2 — C7 solution (review apparatus).** Candidate, to be confirmed at
  build: a **kit-owned reviewer** — a review agent/skill that reads
  `REVIEW_LENSES.md` and the diff, shipped by the kit itself, no third-party
  dependency. Evaluate before committing to it: (a) whether it also *replaces*
  `pr-review-toolkit` on the Claude side — one review path on both CLIs would
  cancel the dual-maintenance cost §20.3 warned about, but swaps a proven plugin
  for new unproven content (owner call at build time, presented with evidence);
  (b) whether a Copilot marketplace equivalent of pr-review-toolkit exists by
  then (verify, don't assume absence from a 2026-08-03 search).
- **PORT.3 — C8 solutions (built-ins), one per built-in, no hand-waving:**
  - `/code-review` (owner-typed escalation) → candidate: GitHub's Copilot code
    review requested on the phase PR at `end-phase` — same owner-typed, billed,
    out-of-band shape. Verify capability at build time.
  - `verify` / `simplify` → small kit-shipped skills stating the pass each
    performs (the built-ins are prompts; the kit can carry portable equivalents).
    Each enters the §16 audit regime individually — no confirmed catch after two
    releases, deletion candidate.
  - `security-review` → covered by STD's secure-coding lenses (the PORT.2
    reviewer runs them). This is the C8 item STD was already solving, and with
    STD sequenced first the lenses exist before PORT builds against them.
  - `update-config` → no equivalent needed: Copilot config is plain JSON files;
    a paragraph in `reference/COPILOT.md` suffices.
  - `SKILLS.md` gains a per-CLI availability column rather than a second edition.
- **PORT.4 — `sdlc-update` awareness.** The update command classifies the
  Copilot-side artifacts (`.github/skills/`, `.github/hooks/`, `.github/agents/`,
  `AGENTS.md`) exactly as it does the `.claude/` set today; MANIFEST covers any
  new templates. `sdlc-setup` records the chosen target CLI in `PROJECT_INDEX.md`
  so `/sdlc-update` knows which mapping to walk.

Invariant surface, flagged now: inv 1 (new templates' placeholders must be taught
to setup), inv 2 (the CLI seam is process-neutral — `SDLC.template.md` should need
only the model-tier and review wording checked), inv 5 (README tree grows), inv 6
(`reference/COPILOT.md` ships to adopters — it is setup-time material, so it
belongs under `sdlc-kit/`), inv 15 (setup verifies the *installed* Copilot version
against the mapping's verified-on date and says so — fail loudly, per FR1).

Open at build time (not decided now): Copilot-side skills directory
(`.github/skills/` vs `.claude/skills/`, both documented as read); whether
`AGENTS.md` is emitted on both CLIs or Copilot-only; PORT.2(a), the
single-review-path question — an explicit owner halt in the build session.

### Hand-off — state as of 2026-08-03, end of the COP session (amended)

- **Next session opens on STD** (§18's definition, unchanged): setup interview
  for logging/error-handling conventions, fail-loud lenses in `REVIEW_LENSES.md`,
  mechanical gate rules via `GATE_RECIPES.md`. Build the lenses knowing PORT.2's
  reviewer will consume them.
- **PORT queued behind STD**, defined above — PORT.1 first (detection, then the
  seam and mapping table), then PORT.4, then PORT.2/PORT.3, which carry their own
  build-time verifications and one owner halt (PORT.2a). Re-verify §20.2 against
  the docs before building.
- **Standing kit inputs unchanged:** any sixth field report (TFit Phase 07);
  R3.8's aging rule still on its clock (§16 contingent keep).

## 22. STD shipped — 2026-08-03; release 0.13.0

The standards batch, built to §18's definition with §20's confirmed input (lenses,
portable prose — the built-in they would otherwise lean on is Claude-only). The three
build-time opens, resolved:

1. **Conventions home: a *Runtime Conventions* section in `CLAUDE.template.md`**, not
   a new file. Two placeholders (`{{LOGGING_CONVENTIONS}}`, `{{ERROR_CONVENTIONS}}`),
   taught to setup in the same batch (inv 3). Rationale: the conventions govern every
   slice's code, and the instantiated `CLAUDE.md` is one of the two files every
   session already reads — a separate `spec/CONVENTIONS.md` would carry a spec-loading
   trigger that fires on essentially every slice, i.e. an indirection with no
   filtering value, plus a README-tree/manifest/install-mapping surface the section
   avoids entirely. The section names its enforcement (inv 14): linter rules for the
   mechanical part, the new lenses for the rest.
2. **Lens set: three.** *Logging and swallowed errors* (sited next to *error
   propagation*, per §18), *untrusted input*, *secrets and exposure*. Each names its
   own trigger; the trigger summaries in `SDLC.template.md` slice-loop step 6 and
   `end-slice.md` §3 were extended to match (inv 2). The file carries an explicit
   provenance note: shipped as standards, not from a measured field catch — the
   *error propagation* caveat applies doubly.
3. **Gate rules: a *Runtime-standards rules* section in `GATE_RECIPES.md`.** Rules
   land in the linter's own config, so the existing gate + hook enforce them with no
   new command: ruff `E722`/`BLE001`/`B904`/`T20` + the bandit `S` family; eslint
   `no-console`/`no-empty`/`no-eval` kin + `no-floating-promises`; .NET
   `latest-recommended` analyzers; golangci-lint `errcheck`+`gosec`; checkstyle
   `EmptyCatchBlock`/`IllegalCatch`; clippy `unwrap_used`/`expect_used`/
   `print_stdout`. Existing mode measures each proposed rule's violation count before
   the owner adopts it, and new-rule violations land in the step 4 measured baseline —
   never a setup-time fix spree. The adopted set is proven the way the hook is proven:
   one deliberate violation must fail the lint run (inv 13).

**§16 audit clocks start now, individually:** the three lenses and the
runtime-standards recipe section each need a confirmed catch by 0.15.0 or become
deletion candidates. The conventions section itself is exempt as a record, not a rule
— but a conventions bullet no lens or rule ever enforced is worth the same skepticism.

### Hand-off — state as of 2026-08-03, end of the STD session

- STD shipped as `v0.13.0`; `/kit-check` run before release — clean on the STD
  additions themselves (both new trigger lists match; both new placeholders asked in
  both modes; all new pointers and step references resolve), and it surfaced **seven
  pre-existing findings** (invariants 2, 3, 5 — none introduced by this batch), all
  fixed in the same release; the itemized list is CHANGELOG 0.13.0 *Fixed*. Manifest
  regenerated with discrimination proven.
- **Next session opens on PORT** (§21's definition, unchanged): PORT.1 first
  (detection, then the seam and mapping table), then PORT.4, then PORT.2/PORT.3 —
  re-verify §20.2 against the Copilot docs before building; one owner halt (PORT.2a).
  STD's lenses now exist for PORT.2's reviewer to consume, as §21 sequenced.
- **Standing kit inputs unchanged:** any sixth field report (TFit Phase 07);
  R3.8's aging rule still on its clock (§16 contingent keep); STD's four new audit
  clocks above.

---

## 23. PORT.0 — §20.2 re-verified against the docs, 2026-08-03; four claims moved

The re-verification §21 made a precondition ("all §20.2 capability claims must be
**re-verified against the docs at build time** before code is written against them").
Run before any PORT file was touched; kit tree still at v0.13.0, untouched. Sources are
`docs.github.com` pages fetched this session — hooks reference, CLI add-skills,
create-custom-agents-for-cli, cli-command-reference, cli-plugin-reference, CLI
add-custom-instructions, Copilot code review — plus two non-GitHub sources named where
used. **Six claims stand as written; four moved.** The four that moved are below first,
because three of them change what PORT builds.

### 23.1 C2 instructions — MOVED, in the kit's favour: no translation needed

§20.2 recorded "Reads `AGENTS.md`, `.github/copilot-instructions.md`,
`.github/instructions/**`" and §21 wrote the mapping row `CLAUDE.template.md` →
`AGENTS.md`. The CLI's own custom-instructions page is more generous than the spike
found: **Copilot CLI reads `CLAUDE.md` directly**, alongside
`$HOME/.copilot/copilot-instructions.md`, `.github/copilot-instructions.md`, and
`AGENTS.md`. Multiple applicable files are **combined**, and the page states it "does
not define a general precedence order between these files."

Consequences, both real:

- **The `CLAUDE.template.md` → `AGENTS.md` mapping row is deleted.** The instantiated
  `CLAUDE.md` — including STD's new *Runtime Conventions* section — is read unchanged
  by both CLIs. C2 stops being a coupling. This is the single largest simplification
  the re-verification bought.
- **§21's open question "whether `AGENTS.md` is emitted on both CLIs or Copilot-only"
  is answered: emit neither.** And it converts to a *prohibition* — because the files
  merge with no precedence, a project carrying both `CLAUDE.md` and a kit-written
  `AGENTS.md` would load two copies of the same instructions with no rule for which
  wins. Setup emits exactly one instructions file on either CLI, and
  `reference/COPILOT.md` must say why rather than leaving a future batch to
  "helpfully" add the second.

### 23.2 C3 hook — stands in substance, four corrections that change the recipe

The dialect is as §20.2 recorded (`.github/hooks/*.json`, `"version": 1`,
`bash`/`powershell`/`command` keys, `cwd`, `env`, `timeoutSec`; also settable via a
`hooks` field in `.github/copilot/settings.json`). Four details the spike did not have,
each of which lands in the recipe PORT.1 writes:

1. **`postToolUse` cannot block or deny.** Its documented output is `modifiedResult`
   and `additionalContext` only (the 10 KB cap applies when multiple hooks return).
   §20.2's "functionally what the kit's exit-2 stderr feedback does" survives — Claude
   Code's exit-2 is advice-to-the-model too — but the recipe must not promise blocking.
2. **`preToolUse` *can* deny**, is **fail-closed** on error and exit 2, and takes
   `permissionDecision: allow|deny|ask`. It is the closer analogue to the kit's exit-2
   gate. Not adopting it in PORT (the kit's gate is a post-edit check, not a
   pre-approval), but the recipe should record that the stronger event exists so a
   later batch doesn't rediscover it.
3. **`timeoutSec` defaults to 30, and timeouts are documented fail-open** — "a
   timed-out hook surfaces a warning and lets the tool call proceed." The kit's gate
   hook runs lint *and* typecheck; on a cold typecheck 30s is not a generous budget,
   and the failure mode is a **silently green gate**. This is invariant 15 territory
   (the process is silent about the environment it runs in) and FR1's fail-loudly
   principle: the Copilot recipe sets `timeoutSec` explicitly, states the value's
   basis, and says in the generated `SDLC.md` that a timeout reads as a pass. Claude
   Code's hook has no equivalent documented fail-open, so this is a Copilot-only hazard
   the mapping table must carry, not a symmetric detail.
4. **The `matcher` regex is anchored** — compiled as `^(?:PATTERN)$`. So `Edit|Write`
   does not port as a substring match, and it does not port at all until Copilot's own
   edit-tool names are known. **Open, build-time, unresolved by this pass:** the exact
   `toolName` values Copilot CLI emits for file edits. The command and hooks references
   document the matcher mechanism, not the tool vocabulary. PORT.1 must establish these
   empirically or from a tool reference before the recipe can be written — a guessed
   matcher is a gate that never fires, which is the FIELD_REPORT_2026-07-22 failure
   mode exactly (a number in prose that isn't the number the machine enforces).

Also confirmed, unchanged in status: `agentStop` can force another turn via
`decision: "block"`, now with a documented bound — "After 8 consecutive `block`
continuations, the CLI overrides the hook and ends the turn anyway." Still out of PORT
scope; still the most interesting Copilot-only capability the kit doesn't use.

### 23.3 C7 review — MOVED: the marketplace absence was overstated

§20.2 said the plugin system exists but `pr-review-toolkit` "and its reviewer agents do
not exist there," and §21 told PORT.2 to "verify, don't assume absence." Verified, and
the picture is different in one structurally important way: Copilot's plugin system
reads a `marketplace.json` from **`.github/plugin/` or `.claude-plugin/`** — i.e. the
Claude plugin marketplace layout is one of the two documented locations, with
`copilot plugin install` accepting a marketplace, GitHub repo, Git URL, or local path,
and `plugin.json` declaring `agents`, `skills`, `commands`, `hooks`, `mcpServers`,
`lspServers`, `extensions`.

What this does and does not license:

- It does **not** establish that `pr-review-toolkit@claude-plugins-official` installs
  and runs on Copilot CLI. Its reviewer agents are Claude Code subagent definitions;
  reading the manifest layout is not executing the contents. **Build-time experiment,
  cheap and decisive:** attempt the install and invoke one reviewer. Until run, treat
  C7 as a loss.
- It does mean the kit's own Copilot-side delivery has a packaging option §20/§21 did
  not consider: **ship the kit as a plugin** (`plugin.json` naming its skills, agents,
  and hooks) rather than as loose files setup copies into place. Not proposing it —
  it is a second install path to maintain and setup already copies files well — but it
  belongs in `reference/COPILOT.md` as a considered-and-declined alternative.
- Still no evidence of an official GitHub-published review plugin. The plugin reference
  lists no official plugin inventory; absence of a listing is not absence of a plugin,
  so this stays "not found," not "does not exist."

### 23.4 PORT.1 signal 1 — MOVED: the session marker is asymmetric, and one CLI has none

§21 required this be settled rather than assumed: "verify each CLI's environment marker
at build time (Claude Code's session env vars; Copilot's documented equivalent — find
it, don't assume one exists)." Both halves answered, and they do not match.

- **Claude Code: verified empirically, in this session.** `CLAUDECODE=1`,
  `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CODE_SESSION_ID`, `CLAUDE_CODE_EXECPATH`, plus
  `AI_AGENT=claude-code_2-1-220_agent`. Solid positive signal.
- **Copilot CLI: no documented session marker exists.** The command reference
  enumerates `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN`, `COPILOT_HOME`,
  `COPILOT_MODEL` — every one of them **user-set configuration or auth**, not something
  the CLI stamps on a running session. `vercel/detect-agent` (third-party, MIT; cited
  as the only structured detection source found) detects Copilot on exactly those
  user-set vars: `COPILOT_MODEL` / `COPILOT_ALLOW_ALL` / `COPILOT_GITHUB_TOKEN`. A
  developer who exported `GITHUB_TOKEN` in their shell profile trips that test from
  inside Claude Code; a Copilot user who authenticated by `/login` may trip none of it.

Two design consequences for PORT.1, both tightening what §21 sketched:

1. **Signal 1 becomes positive-only, per CLI, and never negative.** Absence of
   `CLAUDECODE` is not evidence of Copilot. If no CLI's positive marker fires,
   detection falls through to signals 2 and 3 — it does not infer the other CLI. The
   Copilot-side auth-var test is too weak to propose an answer on and is **not**
   adopted as signal 1; Copilot detection rests on signals 2/3 (repo artifacts, PATH)
   until GitHub documents a session marker.
2. **`AI_AGENT` is a proposed convention, not an implemented standard** —
   `vercel/detect-agent` promotes it and does not claim the tools set it. It is usable
   only as a bonus positive signal, and **only matched by prefix**: the observed value
   here is `claude-code_2-1-220_agent`, while the convention's documented form is
   `claude-code`. An equality test against the convention would have failed in the very
   session that verified it. Recorded because it is precisely the kind of assumption
   the kit's field reports keep catching.

### 23.5 The six claims that stand

- **C4 commands→skills — stands, and the near-miss is confirmed.** Markdown custom
  slash commands still do not exist: `github/copilot-cli#1113` (markdown slash
  commands) is **closed as a duplicate of #618** (`.github/prompts/` support), which
  remains open. Skills are invoked `/skill-name`, `SKILL.md` frontmatter is `name` +
  `description` required with **`license` and `allowed-tools` optional** (both new,
  both useful — see 23.6). Project skill directories: `.github/skills`,
  **`.claude/skills`**, `.agents/skills`; personal: `~/.copilot/skills`,
  `~/.agents/skills`. `.claude/commands` is read by neither the docs nor Copilot — the
  kit's install path remains the near-miss. **§21's open question "`.github/skills/` vs
  `.claude/skills/`" is now an owner decision, not a build detail — see 23.7.**
- **C5 models — stands, with one claim downgraded.** `/model` and `/models` confirmed;
  `COPILOT_MODEL` confirmed. §20.2's "per-agent model pinning" was **not** confirmed by
  the custom-agents page, which documents `name`, `description`, and an optional
  `tools` restriction and mentions no `model` field. Downgraded to unverified; the tier
  table must not be built assuming per-agent pinning.
- **C6 subagents — stands, including the gap.** `.github/agents/*.agent.md`, project
  and user level (`~/.copilot/agents/`), user-level wins on name collision; invocable
  via `/agent`, by name, by inference from the description, or
  `copilot --agent NAME --prompt`. Tool restriction exists; **exact `tools` syntax is
  undocumented** on that page — PORT.1 must find it before writing `explore.agent.md`.
  **Parallel fan-out is still undocumented**, so §21's fallback stands unchanged:
  sweeps serialize on Copilot, stated in the generated `SDLC.md`, never silently.
  (Corroborating evidence subagents are first-class: the hooks reference documents
  `subagentStart`/`subagentStop`.)
- **C8 built-ins — stands.** No `/code-review`, `security-review`, `verify`, `simplify`,
  or `update-config`. Newly noted, and useful: **`/diff`** ("Review changes in the
  current directory") and **`/ask`** exist.
- **C8's `/code-review` replacement — confirmed available.** GitHub Copilot code review
  is requestable on a PR from the Reviewers sidebar, can be configured to run
  automatically, and — the part that matters to the kit — **is customizable via
  `.github/copilot-instructions.md`**. So PORT.3's candidate holds *and* gains a
  steering surface: the kit's review lenses can be written where that reviewer reads
  them. Note the interaction with 23.1: that same file is also merged into CLI
  instructions, so lenses placed there are not free — PORT.3 must decide placement
  deliberately.
- **C9 sessions — stands.** `/clear`, `/new`, `/reset` documented verbatim.

### 23.6 `mattpocock/skills` — assessed as owner-directed, 2026-08-03

The owner pointed PORT at `github.com/mattpocock/skills` as a first place to look for
replacements for the missing components. Assessed against C7/C8; **MIT-licensed**,
`SKILL.md` format, README states the skills "work with any model" and ships three
installs (Claude plugin, `npx skills add`, manual). Findings:

- **`code-review` is a genuine C7/C8 candidate, and a good one.** Two axes —
  *Standards* (does the diff follow the repo's documented standards?) and *Spec* (does
  it implement what the originating issue/spec asked?) — run as parallel sub-agents and
  reported side by side, deliberately not merged or reranked. The fit with this kit is
  unusually close and not accidental: the kit **has** a spec (`spec/`, the whole point
  of the process) and, as of STD, **has** documented runtime standards. Its Standards
  axis also carries a built-in Fowler smell baseline (12 smells, each *what it is* →
  *how to fix*), with the rule that a documented repo standard overrides the baseline.
- **Three frictions, all real, none disqualifying:** (a) it depends on
  `docs/agents/issue-tracker.md` and a `/setup-matt-pocock-skills` bootstrap the kit
  would have to supply or excise; (b) it spawns Claude Code's `Agent` tool with the
  `general-purpose` subagent type — a C6 coupling that needs `.github/agents/` on
  Copilot and hits the undocumented-parallel-fan-out gap in 23.5; (c) its smell
  baseline **overlaps `REVIEW_LENSES.md`**, and two review checklists in one kit is the
  duplication invariant 2 exists to prevent. Adoption means reconciling them, not
  shipping both.
- **Coverage of the rest is partial, and the gaps should be stated plainly:**
  `improve-codebase-architecture` is the nearest thing to `simplify` but is a
  scan-and-grill workflow, not a diff-scoped cleanup pass; **nothing corresponds to
  `verify`**; `tdd` duplicates the kit's already-vendored TDD skill and is not needed;
  `security-review` is covered by STD's lenses as planned; `update-config` needs no
  equivalent. So the repo solves C7 and part of C8, and PORT.3 still writes `verify`
  and `simplify` itself.
- **Vendoring regime, if adopted:** identical to the existing TDD skills under
  invariant 3 — per-file provenance and verification date in `reference/SKILLS.md`,
  attribution in `THIRD_PARTY_NOTICES.md`, and any kit edit recorded as a divergence
  rather than silently drifted. The `license` frontmatter field found in 23.5 is the
  natural place to carry it in-file.

### 23.7 What this pass changed, and the two decisions it surfaced

Net effect on PORT as defined in §21: **C2's mapping row is deleted** (23.1), **the
hook recipe gains four requirements and one hard build-time unknown** (23.2), **C7
gains a cheap decisive experiment and a real third option** (23.3, 23.6), and
**PORT.1's strongest detection signal turns out to work on one CLI only** (23.4).
Nothing found invalidates the owner's build decision; the translation layer remains
mechanical.

Carried into the build as build-time unknowns: the custom-agent `tools` restriction
syntax (23.5) and whether `pr-review-toolkit` installs on Copilot at all (23.3).

**23.2's `toolName` unknown — closed enough to build on, with a discovery procedure.**
The hooks reference's own matcher example is `"matcher": "bash|edit"`, which makes
`bash` and `edit` documented tool names. A third-party cookbook shows a *post-edit
quality-feedback* hook — the kit's gate-hook shape exactly — matching
`^(?:edit|create|apply_patch)$` at `timeoutSec: 60`, and an SDK example filtering on
`toolName !== "edit" && toolName !== "create"`. So `create` and `apply_patch` are
plausible but unofficial, and `github/copilot-cli#3820` ("Document matcher support for
command hooks") confirms the vocabulary is under-documented. The kit does not guess
silently: the recipe ships `edit|create|apply_patch` as the **starting** matcher and
leans on the proof step it already requires (invariant 13 — a deliberate violation must
fail the run), which turns a wrong matcher into a loud setup-time failure rather than a
gate that never fires. `reference/COPILOT.md` carries the provenance of each name and
the discovery procedure for when the proof fails: register a matcher-less `postToolUse`
hook that echoes `toolName`, edit one file, read the real vocabulary off the log.
Same-source caveat, recorded for invariant 15: that cookbook states postToolUse
matchers "were fixed in v1.0.63" — so setup reads `copilot --version` and says
plainly if the installed CLI is older, rather than installing a gate that cannot fire.

**Two owner decisions, both surfaced by evidence rather than planned:**

1. **Skills install path — RESOLVED by the owner, 2026-08-03, both parts.** The
   question: `.claude/skills/` is read by *both* CLIs, which means the kit's five
   vendored skills could install once and need no translation at all, but the kit
   installs them to `.claude/commands/` and `CLAUDE.md` records that as deliberate
   ("project-scoped, so they travel with a `git clone`") — a rationale that applies
   just as well to `.claude/skills/`. **Decisions: (a) the Copilot-side install writes
   to `.claude/skills/`, not `.github/skills/`** — one directory both CLIs read, so a
   dual-CLI repo carries one copy of each skill and there is no sync surface to drift
   (invariant 2); the Claude-flavoured directory name on a Copilot-only project is the
   accepted cost and `reference/COPILOT.md` must explain it. **(b) The five vendored
   skills move from `.claude/commands/` to `.claude/skills/`** — they are skills, not
   user-typed commands, and `.claude/skills/` is equally project-scoped, so the
   original rationale is preserved rather than overturned. Consequences PORT.1 owns:
   C1's mentions across 9 shipped files, the README tree, `reference/SKILLS.md`, the
   MANIFEST, and an `sdlc-update` migration (remove from the old path, add at the new
   one) for adopters already on ≤0.13.0 — the removal clause exercised in §17 is the
   mechanism. **The seven kit commands stay commands** in `.claude/commands/` on Claude
   Code and are packaged as skills under `.claude/skills/` on Copilot; the owner
   declined moving them, on the ground that they are user-typed workflow entry points
   and model-invocable skills could fire unbidden.
2. **PORT.2a, now with better evidence than §21 anticipated** — the review path is no
   longer a two-way choice between a kit-owned reviewer and keeping `pr-review-toolkit`.
   `mattpocock/skills`' `code-review` is a third option that is MIT, portable, and
   spec-aware. Presented at the PORT.2 halt as planned, not now.

### Hand-off — state as of 2026-08-03, mid-PORT

- **PORT.0 (this pass) is complete**; kit tree untouched at v0.13.0. §20.2 remains the
  spike's record; §23 supersedes it wherever the two disagree.
- **Next session opens on PORT.1 — unblocked; decision 1 is resolved (23.7).** Per
  §21's order, and now with a known shape. The work, in build order:
  1. **Detection + confirm in `sdlc-setup.md` preflight** — built to 23.4's corrected
     signal model: positive-only per CLI, never negative, `AI_AGENT` prefix-matched as
     a bonus signal only, Copilot resting on repo artifacts and PATH. Detection sets
     the *proposed* answer inside the existing interview; the prime directive stands.
  2. **`sdlc-kit/reference/COPILOT.md`** — the mapping table, stated once, dated and
     provenance-style like `SKILLS.md`. Minus the C2 row (23.1), plus: the
     `AGENTS.md`-prohibition rationale, the `toolName` provenance and discovery
     procedure, the v1.0.63 floor, the `.claude/skills/` naming explanation, and the
     ship-as-a-plugin alternative recorded as considered-and-declined (23.3).
  3. **Copilot hook recipe in `GATE_RECIPES.md`**, beside the existing one, same
     `{{HOOK_*}}` placeholder set (inv 1) and 23.2's four requirements — explicit
     `timeoutSec`, the fail-open-timeout warning in the generated `SDLC.md`, no
     promise of blocking, the anchored starting matcher.
  4. **`explore.agent.md`** read-only profile — blocked on finding the `tools`
     restriction syntax (23.5); if parallel fan-out is still undocumented, sweeps
     serialize on Copilot and the generated `SDLC.md` says so, never silently.
  5. **The `.claude/commands/` → `.claude/skills/` migration** for the five vendored
     skills (decision 1b): 9 shipped files, the README tree (inv 5),
     `reference/SKILLS.md`, `MANIFEST.sha256`, and an `sdlc-update` removal-and-re-add
     path for adopters on ≤0.13.0.
  Close with `/kit-check` before release, as STD did — it surfaced seven pre-existing
  findings last time, so budget for that.
- **Then PORT.4, then PORT.2/PORT.3**, PORT.2 opening with the `pr-review-toolkit`
  install experiment (23.3) and closing at the PORT.2a halt — now a three-way choice
  (kit-owned reviewer / keep `pr-review-toolkit` / adopt `mattpocock/skills`'
  `code-review`, 23.6), to be presented with evidence.
- **Standing kit inputs unchanged:** any sixth field report (TFit Phase 07); R3.8's
  aging rule (§16 contingent keep); STD's four audit clocks (§22).

---

## 24. PORT.1 built — 2026-08-03; detection, COPILOT.md, the hook dialect, the skills move

Built to §23's hand-off order. **Items 1–3 are §24.0–24.4 below; items 4 and 5 are
§24.5–24.6.** Unreleased: the tree is 0.13.0 + these changes, and CHANGELOG, the VERSION
bump, and the `/kit-check` pass still wait. `MANIFEST.sha256` was regenerated early —
the skills move renamed seven bundle files, so a stale manifest would have listed paths
that no longer exist; it verifies 29/29 and was proven to discriminate (a deliberate
byte appended to `VERSION` failed the check, then restored).

### 24.0 Items 1–3

**Shipped:**

- **`sdlc-kit/reference/COPILOT.md`** (new, ~200 lines) — the mapping stated once,
  dated and provenance-style like `SKILLS.md`: the file-by-file table, the `AGENTS.md`
  prohibition and why, the install-path rationale, the four hook hazards, the tool-name
  provenance table with the discovery procedure, the v1.0.63 floor, models and tiers,
  the subagent gaps, *What the kit loses on Copilot today*, ship-as-a-plugin recorded as
  declined, the detection signal table with its three traps, and a Provenance section
  separating GitHub docs from the two named third-party sources.
- **`sdlc-kit/templates/copilot-hook.template.json`** (new) + a *Hook dialects* section
  in `GATE_RECIPES.md` — same `{{HOOK_*}}` set, no new hook-body placeholder.
- **Detection and the CLI seam in `sdlc-setup.md`** — new preflight step 2 (the old
  2–4 shift to 3–5; the one internal cross-reference was updated, and the 2a step
  numbers that README and `/kit-check` cite are untouched). Install step 5 and hook
  step 6 branch per CLI, the model-policy poll asks rather than proposes on Copilot,
  Existing mode's survey collects the artifact signals, and the close-out `{{` grep
  covers the Copilot hook file.

**Four decisions taken at build, none of them re-litigating §23:**

1. **Owner decision, 2026-08-03: the seven kit commands packaged as Copilot skills
   install to `.github/skills/`, not `.claude/skills/`.** 23.7's decision 1a resolved
   the *vendored skills* question, and its rationale (one directory both CLIs read → no
   sync surface) does not transfer to the seven, whose Claude-side copy lives in
   `.claude/commands/` regardless. Putting them in `.claude/skills/` would make them
   model-invocable in Claude Code on any dual-CLI repo — precisely what the owner
   declined when they kept them as commands. `.github/skills/` is read by Copilot and
   not by Claude Code, so the carve-out costs one directory and nothing else.
2. **Two new placeholders, `{{HOOK_CONFIG_PATH}}` and `{{HOOK_FEEDBACK_NOTE}}`**, both
   in the existing `{{HOOK_*}}` family, both taught to setup at step 6 (inv 1). They
   exist because `CLAUDE.template.md` asserted the hook's feedback "is blocking" and
   `SDLC.template.md` named `.claude/settings.json` — two sentences that are simply
   false on Copilot, where `postToolUse` cannot block. The second placeholder is also
   what carries the timeout-reads-as-a-pass warning into the generated `spec/SDLC.md`
   (inv 15). Two further Claude-only paths in template prose were made path-free rather
   than parameterized.
3. **The hook body parses with `python`, not `jq`** — the reverse of the draft. `jq` is
   absent from the machine this kit is developed on while Python is present, which is
   the same asymmetry the existing Claude-side hook already assumes; adding a second
   tool dependency to the Copilot path would have made the Copilot gate the more
   fragile of the two for no gain.
4. **`/kit-check` check 7 now names `reference/COPILOT.md`** as a derived statement and
   states that the install mapping is per-CLI — a statement naming one CLI's path as
   universal is a finding.

**Verified, not assumed.** Two facts §23 left open were closed by fetching the docs
before writing code against them: the `postToolUse` stdin payload (both the camelCase
and VS Code shapes) and the stdout contract (`modifiedResult` / `additionalContext`).
The instantiated hook body was then run against six payloads — both dialects with a
failing linter, a non-source file, a clean source file, a payload with no path, a path
whose file is missing, and unparseable input — and behaved correctly in all six
(recorded in `GATE_RECIPES.md` with its date). That run also produced two fixes no
reading pass would have found: non-ASCII in the hook's own text came back mojibake
through a Windows locale codec, so the messages are ASCII-only and stdin is decoded
`errors='replace'`; and the no-path case, which had been a quiet `exit 0`, is now loud —
a hook that cannot find the file it was called about is otherwise indistinguishable
from a clean edit.

**Still open, unchanged:** the `toolArgs` key holding the edited file path is
undocumented for every tool, exactly like the `toolName` vocabulary — the body tries the
plausible keys, reports loudly when none matches, and the same echo-hook discovery
procedure answers both.

### 24.5 Item 4 — the blocker was a wrong page, and closing it reversed a §23 downgrade

§23.5 recorded the custom-agent `tools` restriction syntax as undocumented, having read
the CLI how-to page. The **custom-agents configuration reference** documents it fully,
and states it applies to the CLI as well as GitHub.com and the IDEs. Two consequences:

- **Item 4 is unblocked and built.** `tools` takes a YAML array or a comma-separated
  string; omitted or `["*"]` means everything, `[]` means nothing. The built-in aliases
  are `execute`, `read`, `edit`, `search`, `agent`, `web`, `todo`. Read-only is
  `tools: ["read", "search"]`, which is what `templates/explore.agent.template.md`
  ships with → `.github/agents/explore.agent.md`, Copilot only (Claude Code has its
  built-in `Explore`).
- **§23.5's "per-agent model pinning is unverified" is overturned** — `model` is a
  documented field. Recorded in `COPILOT.md` with the correction named, because the
  earlier reading was not wrong about the how-to page; it was wrong to treat a how-to as
  the contract. The kit still ships no model in any installed file: a model name is a
  project fact.
- **A trap found while closing it, now recorded:** the agent tool aliases are *not* the
  hook's `toolName` vocabulary — the agent reference calls the shell tool `execute`, the
  hooks reference's matcher example calls it `bash`, and `edit` appears in both, which
  is exactly what would make someone derive a hook matcher from the wrong list.

Parallel fan-out is still undocumented, so §21's fallback stands and is now stated where
it binds: `SDLC.template.md`'s parallelism rule and `plan-phase.md` both say that where
the CLI cannot fan out the sweeps run one after another, and that a sweep dropped for
time is reported as not run — never as a sweep that found nothing.

### 24.6 Item 5 — the skills move, done as a bundle restructure

Decision 1b said the five vendored skills move to `.claude/skills/`. Building it forced
one design choice §23 did not anticipate: **the kit-side layout had to move too.** Skills
are directories (`<name>/SKILL.md`), so five installed files would have shared the
basename `SKILL.md` — and `/sdlc-update`'s classifier matches installed files to manifest
entries **by basename**. Left flat kit-side, every vendored skill would have collided in
that lookup. So `skills/` is now one directory per skill, mirroring the install layout,
with `tdd/tdd-references/` nested under `tdd/` so `SKILL.md`'s relative links survive.

Touched, all verified against the install list as invariant 7 requires: `sdlc-setup.md`
(the install list, now a per-CLI table), `sdlc-update.md` (ownership table, the classify
loop's new `.claude/skills/*` case, the denominator, the apply sources, and the
removal-and-re-add clause), `end-slice.md`, `sdlc-retro.md`, `reference/SKILLS.md`
(tables, provenance paths, onboarding checklist), `THIRD_PARTY_NOTICES.md`, both READMEs
(trees, ownership tables, both classification scripts), root `CLAUDE.md`, `COPILOT.md`,
`KIT_INVARIANTS.md` (invariant 7 restated as per-CLI with two destinations), and
`MANIFEST.sha256`.

**The classifiers keep the `skills/` → `.claude/commands/` prefix on purpose.** It is
what classifies a project still on ≤ 0.13.0; dropping it would report every vendored
skill `UNKNOWN` — "not from the kit, yours" — which is invariant 7's own specimen
failure repeated. The migration then runs as the removal clause's second exercise: old
paths leave, new paths arrive, stated to the owner as one move, with an explicit check
that no skill ends up at both paths.

### Hand-off — state as of 2026-08-03, PORT.1 complete

- **PORT.1 is done, items 1–5.** Not released: CHANGELOG, the VERSION bump to 0.14.0,
  and the full `/kit-check` pass remain (STD's pass surfaced seven pre-existing findings
  — budget for it). `MANIFEST.sha256` is current but will need one more regeneration
  after the VERSION bump, since `VERSION` is itself a bundle file.
- **Next: PORT.4**, then PORT.2/PORT.3, unchanged from §23. PORT.4 still owns recording
  the chosen CLI in `PROJECT_INDEX.md` — setup uses the answer within its own run today,
  but nothing persists it for `/sdlc-update` to read, and `SKILLS.md`'s onboarding
  checklist currently tells a new developer to infer the CLI from what the repo holds.
  PORT.4 also owns teaching `/sdlc-update` the Copilot-side paths (`.github/skills/`,
  `.github/hooks/`, `.github/agents/`), which this batch deliberately left alone.
- **One thing PORT.2 should know:** `reference/SKILLS.md` now points at COPILOT.md's
  loss table rather than carrying a per-CLI availability column. §23.5's "SKILLS.md
  gains a per-CLI availability column" is still PORT.3's to build if it wants one.

---

## 25. PORT.4 built — 2026-08-03; `/sdlc-update` learns the Copilot side

§21's definition, minus `AGENTS.md`, which 23.1 turned into a prohibition — there is no
such file to classify. Two halves: the target CLI is now *recorded*, and the update
command classifies the Copilot artifacts.

**The record.** `{{TARGET_CLI}}` — an *Agent CLI:* line at the top of
`PROJECT_INDEX.template.md`, resolved from the preflight confirmation (`Claude Code` /
`Copilot CLI` / `both`). `/sdlc-update` reads it at step 1 to know which directories are
kit-owned. Projects adopted before 0.14.0 have no such line: the update infers it from
what the repo holds, has the owner confirm, and writes the line as it lands — so
`spec/SDLC.md`'s version stamp and this line are now **the two** project-owned lines an
update may write, the second only when absent. Both READMEs and `sdlc-update.md` say so
identically (invariant 8).

**The problem PORT.4 actually had to solve, which §21 did not anticipate.** "Classify
the Copilot artifacts exactly as the `.claude/` set" is not possible as written: the
kit's whole proof of "unmodified" is byte-identity with a manifest entry, and a packaged
skill is *not* byte-identical to anything in the bundle — it is a frontmatter block plus
the kit command. Options considered and rejected: shipping a second copy of each command
in Copilot shape (body duplication, a drift surface between two files with the same
content), and shipping pointer-skills whose body just names the real file (an
indirection the model may or may not follow). What shipped instead: **the packaging
shape is specified exactly** — frontmatter, one blank line, then the kit file
byte-for-byte, nothing else inserted — and the classifier strips that block and compares
the remainder against `commands/<name>.md`. The install rule and the update rule are now
the same statement read in two directions.

Three consequences worth recording:

- **It fails safe.** A broken strip hashes nothing, matches no manifest entry, and the
  file lands in `DRIFTED` in front of the owner rather than in `UNCHANGED` behind their
  back. Both `sdlc-update.md` and the README say that seven packaged skills going
  `DRIFTED` at once means the strip, not seven edits.
- **It tolerates the right edit.** An owner who rewords a skill's `description` has not
  modified the command; the strip ignores frontmatter by construction, so that file
  still classifies `UNCHANGED` and still gets the new body.
- **The gate hook is project-owned**, like `.claude/settings.json` — it holds the
  project's own lint and typecheck commands. A release that changes the hook recipe
  reaches an adopted project as a changelog entry, never as an overwrite.

`.github/agents/explore.agent.md` needed no special handling but did need a rule: it
copies `templates/explore.agent.template.md` verbatim (no placeholders), so it is the
**second exception** to "templates are never re-applied to an adopted project" —
`reference/REVIEW_LENSES.md` was the first. Both READMEs now name both.

**Verified against a synthetic adopted project**, not by reading. The classifier block
was extracted verbatim from `sdlc-update.md` and run over a repo holding all five
classes: a kit command, `REVIEW_LENSES.md`, a vendored skill with its nested
`tdd-references/`, a packaged Copilot skill, the agent profile, one deliberately drifted
command, and one file the kit never shipped. Nine files, nine lines, every verdict
correct — and correct on a repo with **no `.gitattributes`**, whose working tree is CRLF,
which is the kit's own standing warning demonstrated rather than asserted. Two negative
cases followed: editing the packaged skill's body → `DRIFTED`; editing only its
`description` → `UNCHANGED`.

**One latent bug fixed on the way.** The classify loop had no `*)` catch-all, so a path
matching none of its cases would silently reuse the previous iteration's `want` and
`base` — unreachable while the directory list produced only matching paths, and no longer
unreachable now that `.github/skills/*/SKILL.md` is a specific pattern. A stray file
under a kit-owned directory now reports `UNKNOWN`, which is the honest answer.

---

## 26. Release shape — owner decision, 2026-08-03: one release for all of PORT

**Owner decision, dated 2026-08-03 — do not re-litigate:** PORT.1, PORT.2, PORT.3 and
PORT.4 ship together as a single release. Nothing is cut until PORT.2 and PORT.3 are
built, so the tree stays at `0.13.0` with PORT.1 and PORT.4 committed on top of it, and
the version bump is the last act before tagging.

The consequence to hold onto: **an adopter never sees a half-translated kit.** A release
carrying detection, the mapping, the hook dialect, the sweep agent and the update path
but no review apparatus would install a process on Copilot whose `/end-slice` names a
reviewer that does not exist there. That is precisely the "specifies what each step must
produce and almost never what makes it done" failure §15 was written about, and shipping
it would have made `reference/COPILOT.md`'s *What the kit loses on Copilot today* a
description of the kit's own release rather than of the CLI.

### Hand-off — state as of 2026-08-03, end of the PORT.1/PORT.4 session

**Done and committed** (three commits on `main`, tree clean, `VERSION` still `0.13.0`):
PORT.0 (§23, the re-verification), PORT.1 items 1–5 (§24), PORT.4 (§25).

**A fresh session opens on PORT.2.** Everything it needs, in order:

1. **The experiment first, before any design** (23.3): attempt
   `pr-review-toolkit@claude-plugins-official`'s install on Copilot CLI and invoke one
   reviewer. Copilot's plugin system reads `marketplace.json` from `.github/plugin/` **or
   `.claude-plugin/`**, so the layout is one of the two documented locations — but the
   reviewers are Claude Code subagent definitions, and reading a manifest layout is not
   executing its contents. Until the experiment runs, C7 is a loss. Cheap and decisive:
   run it, then design.
2. **The PORT.2a owner halt** — a three-way choice, presented with evidence, not
   decided in advance: a kit-owned reviewer, keeping `pr-review-toolkit`, or adopting
   `mattpocock/skills`' `code-review` (23.6: MIT, portable, spec-aware, and unusually
   well fitted since this kit *has* a spec and, since STD, documented standards). The
   three frictions in 23.6 are real and none is disqualifying; note especially that its
   smell baseline overlaps `REVIEW_LENSES.md`, and two review checklists in one kit is
   what invariant 2 exists to prevent — adoption means reconciling them, not shipping
   both.
3. **Then PORT.3** (§21, as amended by 23.5): `/code-review` → Copilot code review on
   the phase PR, steered by `.github/copilot-instructions.md` — but that same file is
   merged into CLI instructions with no precedence order (23.1), so placement is a
   deliberate choice, not a free one. `verify` and `simplify` are kit-written skills,
   each entering the §16 audit regime individually. `security-review` is already covered
   by STD's lenses. `update-config` needs no equivalent. `SKILLS.md` currently points at
   COPILOT.md's loss table instead of carrying a per-CLI availability column — building
   that column is PORT.3's call.

**Then, and only then, the release** — the checklist, in order:

1. Reconcile `reference/COPILOT.md`'s *What the kit loses on Copilot today* against what
   PORT.2/PORT.3 actually shipped. That table is the honest statement of the gap and it
   must not outlive the gap.
2. `CHANGELOG.md` for 0.14.0, entries marked *[installable]* / *[adoption-only]* — note
   that the skills move (§24.6) is installable and is a *move*, so its entry says so
   rather than listing deletions and additions.
3. Bump `sdlc-kit/VERSION` to `0.14.0`.
4. **Regenerate `MANIFEST.sha256` after the bump** — `VERSION` is itself a bundle file,
   so the manifest is stale the moment it changes. Prove discrimination on a *copy*, not
   on a tracked file.
5. Full `/kit-check`. Budget for it: STD's pass surfaced seven pre-existing findings, and
   this batch moved install paths, which is invariant 7's whole surface. Expect findings
   against invariants 3, 5, 7 and 8 in particular.

**Standing kit inputs unchanged:** any sixth field report (TFit Phase 07); R3.8's aging
rule (§16 contingent keep); STD's four audit clocks (§22), whose deadline is 0.15.0 —
one release later than the one now being assembled.

## 27. PORT.2 step 1 — the C7 experiment, run 2026-08-03; C7 is NOT a loss

§23.3 told PORT.2 to run this before any design work and to treat C7 as a loss until it
did: "attempt the install and invoke one reviewer." Run. **Both halves succeeded**, so
the C7-is-a-loss default is retired — but the win is narrower and more dated than a bare
"it works" implies, and the four caveats below are the substance of the finding.

**Bench:** Copilot CLI **1.0.77**, installed via winget (not npm — the binary is
`%LOCALAPPDATA%\Microsoft\WinGet\Packages\GitHub.Copilot_*\copilot.exe`), authenticated,
against a throwaway git repo at `D:\AICourse\copilot-ci-test` with a two-defect JS
fixture. All runs non-interactive (`-p … -s --no-ask-user`) under a read-only tool grant.

### 27.1 The install: the working path is the deprecated one

- **Marketplace registration fails.** `copilot plugin marketplace add
  anthropics/claude-plugins-official` errors out. Copilot *did* fetch
  `.claude-plugin/marketplace.json` — confirming 23.3's claim that the Claude layout is
  one of the two locations it reads — but its schema for `plugins[].source` is stricter:
  it accepts the plain relative-path string and rejects the `{source: "git-subdir", url,
  path, ref, sha}` object form. 79 of 276 entries use the object form, validation is
  all-or-nothing, and the whole marketplace is refused.
- **`pr-review-toolkit` is not one of the rejected entries.** It sits at index 191 with
  `"source": "./plugins/pr-review-toolkit"`. Its exclusion is collateral damage from
  third-party entries, which matters: the incompatibility is not with Anthropic's plugin
  but with other publishers' use of a form Copilot has not implemented.
- **The subdirectory install works:** `copilot plugin install
  anthropics/claude-plugins-official:plugins/pr-review-toolkit` → "installed
  successfully."
- **…and is announced as deprecated in the same breath.** Verbatim: "Direct plugin
  installs (repos, URLs, local paths) are deprecated. Only plugin@marketplace installs
  will be supported in a future release." **So the only path that works today is the one
  being removed, and the path about to be mandatory is the one the schema mismatch
  blocks.** Any kit instruction that depends on this is a dated dependency, and
  `COPILOT.md` must date it rather than state it as a capability.

### 27.2 Five of six agents loaded; the sixth was dropped silently

`--agent` reports: `code-reviewer`, `code-simplifier`, `comment-analyzer`,
`pr-test-analyzer`, `type-design-analyzer`. **`silent-failure-hunter` is absent.**

Cause established, and the correlation is 1:1 across the six files: it is the only agent
whose unquoted YAML plain-scalar `description` contains a `: ` — from the embedded
example line `Daisy: "I've added error handling to the API client."`. Copilot's
frontmatter parser rejects the document; Claude Code's tolerates it and loads the agent
fine.

**The failure mode is worse than the failure.** There is no warning at install, and
`copilot plugin list` reports the plugin as healthy. The drop is visible only by passing
a bogus `--agent` name and reading the "available:" list in the error. This is invariant
15's shape exactly — the artifact verified clean, the environment it runs in silently
carrying less — and it is a *kit* hazard, not just a plugin one: any kit-authored agent
or skill whose frontmatter description contains a colon-space will vanish on Copilot
without saying so.

### 27.3 `model:` pinning is silently downgraded

`code-reviewer.md` declares `model: opus`. Copilot warns — "specifies model 'opus' which
is not available; using 'auto' instead" — and proceeds. Kit-authored agents must not pin
a Claude model name if they are meant to run on both CLIs.

### 27.4 The agents genuinely execute, and the fan-out exists

- **Execution, not just parsing.** `comment-analyzer` returned its report in that agent
  file's exact section structure (*Critical Issues / Improvement Opportunities /
  Recommended Removals / Positive Findings*). The Claude-authored prompt is running.
- **`task` is a builtin.** Copilot's tool set includes `task`, `list_agents`,
  `read_agent`, `write_agent`. Delegation to a plugin agent via `task` succeeded.
  **23.6's friction (b) is therefore half-solved:** fan-out works, but `general-purpose`
  is *not* among the available agent names, so any skill naming that subagent type
  literally — `mattpocock/skills`' `code-review` does — still needs translation.
- **A commands→skills mapping fact for `COPILOT.md`:** the plugin's `commands/review-pr.md`
  registers on Copilot as a **Plugin skill** (`copilot skill list` → "review-pr"), not as
  a command. Copilot has no separate user-command kind here.

### 27.5 A false negative that did NOT survive checking

First run, `code-reviewer` against the fixture reported "No high-confidence correctness
or error-handling issues found" — on a function that swallows every exception and
returns `null`. Tempting as evidence that Claude agents degrade on Copilot. **It is not,
and the check is recorded because the claim would have been wrong:** the fixture was
fully committed, so `git diff` was empty, and `code-reviewer` is diff-scoped. Re-run
against a real uncommitted diff, it flagged the swallow as its one high-confidence issue
at confidence 92 with a correct fix suggestion, and noted the absence of a `CLAUDE.md` to
review against. Review quality on Copilot is *not* a demonstrated problem.

### 27.6 Incidental findings PORT.3 needs

- **`copilot skill list` reports exactly one builtin skill:** `customize-cloud-agent`.
  Copilot's builtin surface is far smaller than Claude Code's, so PORT.3's per-built-in
  list is mostly a list of things the kit must supply, not map.
- **Copilot's builtin tools**, verbatim: `powershell`, `read_powershell`,
  `stop_powershell`, `list_powershell`, `view`, `create`, `edit`, `web_fetch`,
  `fetch_copilot_cli_documentation`, `skill`, `sql`, `session_store_sql`, `read_agent`,
  `list_agents`, `write_agent`, `grep`, `glob`, `task`, plus a `github-mcp-server-*`
  subset. Note `view`/`create`/`edit` where Claude Code has `Read`/`Write`/`Edit`, and
  `powershell` where it has `Bash` — `COPILOT.md`'s tool-name table should be checked
  against this list, which is a live 1.0.77 reading rather than a docs reading.
- **Skill discovery paths**, verbatim from `copilot skill --help`: project
  `.github/skills/`, `.agents/skills/`, `.claude/skills/`; personal `~/.copilot/skills/`
  or `~/.agents/skills/`; plugin; custom. This confirms §24.6's skills-move rationale
  first-hand.

### 27.7 State of the bench

The plugin is **still installed** on the owner's Copilot CLI and the test repo still
exists, both deliberately, in case PORT.2a wants more probing. Neither is a kit artifact
and neither is tracked here. Reversal is `copilot plugin uninstall pr-review-toolkit`.
