# Feature Plan — history (§1–§51, 2026-07-19 → 2026-08-12)

Retired sections of `FEATURE_PLAN.md`, moved here in two passes — §1–§30 on
2026-08-05, §31–§51 on 2026-08-13 (the second pass opens at its own header below) —
so the live plan stays readable. **Section numbers are preserved** — any document
(CHANGELOG entries, field reports, the live plan) citing `FEATURE_PLAN.md` §N for
N ≤ 51 means this file. Nothing
was edited on retirement: these are records of shipped work and of standing decisions,
reproduced verbatim. The live plan carries a digest of the decisions and clocks that
remain binding, with pointers back into this file.

The original plan header, for provenance:

> Kit-development artifact (like `IMPROVEMENT_PLAN.md`, which is closed — its backlog
> emptied at `v0.3.0`). **Source:** owner feature requests, 2026-07-19 — not a field
> report. That matters: `IMPROVEMENT_PLAN.md` §5's caution applies with extra force,
> because these features have *zero* field evidence behind them yet. F1 exists partly
> to fix that.
>
> Where this plan and the discussion that produced it disagree, this plan wins. Each
> batch is sized for one session. Run `/kit-check` before any release this plan
> produces.

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

## 28. PORT.2 built — 2026-08-03; the kit owns its reviewer

**Owner decision at the PORT.2a halt, dated 2026-08-03 — do not re-litigate:** the kit
writes its own two-axis reviewer. Neither `pr-review-toolkit` (which §27 proved works
but on a deprecated install path) nor `mattpocock/skills`' `code-review` (which fits the
axes but not the plumbing) is adopted.

Unreleased: the tree is 0.13.0 plus §24, §25 and this. `MANIFEST.sha256` is **stale by
exactly one file** — 29 entries against 30 bundle files, `diff-review/SKILL.md` absent —
which is correct per §26's checklist, where regeneration follows the version bump
because `VERSION` is itself a bundle file. Do not regenerate it early and then bump.

### 28.1 The foundation question that changed the decision

The owner asked the right question before choosing: *do I have the foundation for the
mattpocock reviewer, or am I adding a skill with little support?* Answering it against
the real files rather than §23.6's docs-level read moved two things.

**One claim did not survive.** §23.6 told the halt that the skill's smell baseline
"overlaps `REVIEW_LENSES.md`, and two review checklists in one kit is the duplication
invariant 2 exists to prevent." Read side by side, that does not hold. The upstream
baseline is twelve **structural** smells (Mysterious Name, Duplicated Code, Feature
Envy, Data Clumps, Primitive Obsession, Repeated Switches, Shotgun Surgery, Divergent
Change, Speculative Generality, Message Chains, Middle Man, Refused Bequest);
`REVIEW_LENSES.md`'s six lenses are entirely **runtime failure modes** (error
propagation, swallowed errors, denominators, shared state, untrusted input, secrets).
Subject-matter overlap is essentially nil — they are complementary. The strongest
argument against adoption was the one that evaporated on reading, and §23.6 should be
read with that correction attached.

**The real blocker was the plumbing, not the checklist.** The upstream reaches its Spec
axis through `docs/agents/issue-tracker.md` and issue references in commit messages. The
kit has no issue tracker and should not gain one: its unit of work is the **slice**, and
`spec/` plus `PROJECT_INDEX.md` supply intent directly and more reliably than the
upstream's hunt through `docs/`, `specs/`, `.scratch/` by branch-name match. Adoption
meant four permanent divergences on day one — spec source, standards address, subagent
type, issue-tracker excision — against a file carrying no `license:` frontmatter to
vendor from. A vendor diverged in four places is a fork with extra bookkeeping.

**What the kit genuinely lacked** was the Spec axis itself: `REVIEW_LENSES.md` asks
whether code is sound, `/end-slice`'s gate asks whether it is green, and **nothing asked
whether the slice implemented what it said it would.** That hole is what PORT.2 fills.

### 28.2 What shipped

**`skills/diff-review/SKILL.md`** (new, kit-written) — two axes that fail independently
and are reported side by side, never merged:

- **Spec** — does the change implement the slice's (or, at phase end, the phase's) exit
  criteria, and only those? Intent is located in a fixed order, and **"no spec located"
  is a legitimate axis result**: the prime directive is *never invent the spec*, because
  an inferred spec reviews the diff against itself and always passes. It also asks the
  two questions a criteria list cannot ask itself — **scope creep** (work no criterion
  requested) and **silent narrowing** (a criterion met in a weaker form, which is the
  failure a green gate cannot catch).
- **Standards** — `CLAUDE.md` *Runtime Conventions* first, other convention files next,
  a structural-smell baseline only if neither exists. **A documented project standard
  always wins over the baseline**, stated explicitly so the reviewer does not file a
  finding it already knows is wrong.

It names **no CLI-specific agent, tool, or model** by design, carries no `model:` pin
(§27.3), and defers runtime failure modes to `REVIEW_LENSES.md` rather than restating
them — keeping the three-way division clean and invariant 2 satisfied.

**The wiring**, in the order authority flows: `SDLC.template.md` steps 6 and phase-4
(the file that wins), then `end-slice.md` §3 and `end-phase.md` §5, then
`sdlc-setup.md`'s preflight and install list, `sdlc-update.md`'s 0.14.0 transition,
`SKILLS.md`, `COPILOT.md`, and both READMEs.

**One build decision, stated rather than taken silently:** `pr-review-toolkit` demotes
from **Required** to an optional Claude-Code-only deepening at phase end. It follows
necessarily — a kit that ships its own reviewer cannot keep a third-party one
load-bearing — and it is what removes the per-machine install from team onboarding
entirely. A Copilot project **gains** a per-slice review it never had; a Claude Code
project **loses nothing**, since the plugin stays installed and stays usable.

### 28.3 Acceptance evidence — run on Copilot, not asserted

The skill was exercised on the §27 bench before the wiring was written, which is the
point: the reviewer the commands name had to be shown to exist on the CLI that lacked
one.

1. **It loads.** `copilot skill list` reports it under *Project skills* from
   `.claude/skills/diff-review/` — confirming §24.6's skills-move rationale first-hand
   rather than from the docs.
2. **Its frontmatter clears §27.2's own hazard.** Checked for colon-space in unquoted
   values before shipping — the finding applied to the file the finding produced.
3. **Both axes work.** Against a fixture whose uncommitted diff removed a `TypeError`
   guard and added an exception swallow, with a three-criterion slice spec and a
   one-rule *Runtime Conventions*: Spec returned two criteria unmet and one met, with
   correct line citations, plus **silent narrowing** identified by name; Standards cited
   `CLAUDE.md` by line. Axes reported separately. Verdicts correct.
4. **A harness error, recorded because it looked like a skill defect.** An earlier run
   reported that it could not pin the scope. The cause was mine — `--available-tools`
   omitted `powershell`, so git was unreachable whatever `--allow-tool 'shell(git
   diff)'` said, and Copilot surfaces that as a reasoning limitation rather than a
   permission error. The skill's step-1 discipline is what made it visible: it *said*
   the scope was unpinned instead of reviewing on and calling it clean. That is the
   behaviour §15's theme asked for, caught working.

### 28.4 What PORT.2 fed forward

`COPILOT.md` gained a measured section it did not have — **three authoring hazards**
that bind anything the kit writes for both CLIs, all three silent: the colon-space
frontmatter drop (§27.2), the `model:` downgrade (§27.3), and the
`--available-tools`/`--allow-tool` interaction found in 28.3.4. The loss table lost its
largest row, with the deprecation caveat kept attached so a future batch does not read
"pr-review-toolkit works on Copilot" and rebuild the dependency.

## 29. Hand-off — state as of 2026-08-03, end of the PORT.2 session

**Done and committed** (five commits on `main`, tree clean, `VERSION` still `0.13.0`):
PORT.0 (§23), PORT.1 (§24), PORT.4 (§25), the C7 experiment (§27), PORT.2 (§28).

**Unreleased and deliberate:** `MANIFEST.sha256` is stale by exactly one file — 29
entries against 30 bundle files, `diff-review/SKILL.md` absent. §26's checklist
regenerates it *after* the version bump because `VERSION` is itself a bundle file.
Regenerating it now and bumping later just makes it stale again.

**Standing decisions a fresh session must not re-open:** all of PORT ships as one
release (§26); the kit owns its reviewer, and neither `pr-review-toolkit` nor
`mattpocock/skills` is adopted (§28); `pr-review-toolkit` is optional and Claude Code
only.

### 29.1 A fresh session opens on PORT.3

The scope, and what §27 already established for each so it is not re-derived:

1. **`/code-review` → GitHub Copilot code review on the phase PR**, steered by
   `.github/copilot-instructions.md`. **The placement is the actual decision, not the
   mapping.** §23.1 established that this file is merged into *every CLI session's*
   instructions with no precedence order against `CLAUDE.md` — so anything written there
   to steer the PR reviewer is also loaded into every interactive session, and the kit
   already prohibits emitting a second instructions file for exactly this reason. Decide
   deliberately whether the kit writes this file at all.
2. **`verify` and `simplify` as kit-written skills.** Both are Claude Code built-ins with
   no Copilot equivalent, and both currently sit in `SKILLS.md`'s *Recommended built-ins*
   table with `COPILOT.md` recording "none" as the substitute. Each enters the §16 audit
   regime **individually** — §26 was explicit about that. `diff-review` (§28.2) is the
   worked precedent for shape, frontmatter discipline, and the acceptance-evidence bar.
3. **`security-review`** is already covered by STD's lenses — no new artifact, just
   confirm the row says so.
4. **`update-config`** needs no equivalent; `COPILOT.md` already explains why (Copilot's
   config is plain JSON).
5. **The per-CLI availability column in `SKILLS.md`.** Today the *Recommended built-ins*
   table is Claude-Code-shaped with a paragraph underneath pointing at `COPILOT.md`'s
   loss table. Building the column is PORT.3's call — note that §28 already removed the
   review row from that loss table, so the two are currently in step and must stay so.

**Inputs §27.6 already gathered, so PORT.3 need not re-measure them:** Copilot exposes
exactly **one** builtin skill (`customize-cloud-agent`), so this list is mostly things
the kit must supply rather than map; its builtin tools are `powershell`, `view`,
`create`, `edit`, `grep`, `glob`, `skill`, `task`, `web_fetch`,
`fetch_copilot_cli_documentation`, `sql`, `session_store_sql`, `read_agent`,
`list_agents`, `write_agent`, plus a `github-mcp-server-*` subset.

**Three authoring hazards now recorded in `COPILOT.md`** bind anything PORT.3 writes,
and all three fail silently: no colon-space in an unquoted frontmatter value, no
`model:` pin, and `--available-tools` silently overriding `--allow-tool` when testing.

### 29.2 Then the release — §26's checklist, with one step already part-done

1. Reconcile `COPILOT.md`'s *What the kit loses on Copilot today* against what shipped.
   **The review row is already done** (§28.4) — PORT.3 owns the `verify` and `simplify`
   rows. The table must not outlive the gap.
2. `CHANGELOG.md` for 0.14.0, entries marked *[installable]* / *[adoption-only]*. Two
   that need their nature stated rather than listed: the skills move (§24.6) is a
   **move**, and `diff-review` (§28) is a **new required skill plus a demotion of
   `pr-review-toolkit` to optional** — an adopter reading a bare addition would not know
   the per-machine install is gone.
3. Bump `sdlc-kit/VERSION` to `0.14.0`.
4. **Regenerate `MANIFEST.sha256` after the bump.** Prove discrimination on a *copy*,
   never on a tracked file.
5. Full `/kit-check`. Budget for it: this batch moved install paths (invariant 7's whole
   surface), added a skill directory (invariant 5's file tree), and added a kit-written
   file to a directory whose provenance rules are invariant 3's. Expect findings against
   3, 5, 7 and 8 in particular.

### 29.3 The Copilot bench is still standing

`pr-review-toolkit` remains installed on the owner's Copilot CLI, and the test repo at
`D:\AICourse\copilot-ci-test` still holds the fixture, a three-criterion slice spec, a
one-rule `CLAUDE.md`, and a copy of `diff-review`. Neither is a kit artifact and neither
is tracked. The binary is at
`%LOCALAPPDATA%\Microsoft\WinGet\Packages\GitHub.Copilot_*\copilot.exe` and is **not on
the PATH of an already-running shell** — that cost this session twenty minutes. Reversal
when done: `copilot plugin uninstall pr-review-toolkit`.

**Standing kit inputs unchanged:** any sixth field report (TFit Phase 07); R3.8's aging
rule (§16 contingent keep); STD's four audit clocks (§22), deadline 0.15.0.

---

## 30. PORT.3 built — 2026-08-03; the last two built-ins become kit-owned passes

PORT.3 as §29.1 scoped it, with one item decided rather than asked and one owner
decision taken mid-batch.

### 30.1 Item 1 — the kit does not write `.github/copilot-instructions.md`

§29.1 called the placement "the actual decision, not the mapping" and left it open. It
resolves against a standing decision rather than owner taste, so it was taken, not
asked. §23.1 converted the `AGENTS.md` question into a **prohibition** — setup emits
exactly one instructions file, because Copilot merges `CLAUDE.md`, `AGENTS.md`, and both
`copilot-instructions.md` locations with no defined precedence. That file is the same
class of object.

What tipped it beyond the rule: measured against the tree, `/code-review` is named in
exactly two places — `end-slice.md` (to say it is *not* the review step) and
`end-phase.md` (an optional owner-typed deepening). The kit would have taken on a
permanent every-session instructions cost to steer an optional out-of-band pass no
command can launch. `COPILOT.md` now carries the decision, the three reasons, and the
note that an adopter wanting it should write it themselves — it is project-owned, and
`sdlc-update.md`'s ownership table gained a row saying so, since `COPILOT.md` asserts it.

### 30.2 Items 2 and 5 — `change-verify` and `change-simplify`, wired

**Named deliberately unlike the built-ins.** `SKILLS.md` already told adopters not to
recreate built-ins by hand; a project-scoped skill called `simplify` would shadow one and
read as exactly that. The kit's are `change-simplify` and `change-verify`, and the
provenance note records that the built-ins were not read, copied, or derived from — what
was portable was the idea of the pass, which is nobody's to license.

**Owner decision taken mid-batch: wire them, don't just ship them.** The fork was real
and was put to the owner with the evidence assembled. §21 ("skills *stating the pass each
performs*") and §29.1's narrow scoping of the `diff-review` precedent — "shape,
frontmatter discipline, and the acceptance-evidence bar", wiring conspicuously absent —
both read as recommendation-only. Against that: §16's clock kills a rule with no
confirmed catch by 0.15.0, and nothing invokes an unwired skill, so building them unwired
meant shipping two artifacts the plan's own regime predicted would die. Owner chose to
wire. Consequence: **`SDLC.template.md`'s slice loop gained a step**, so 6–10 renumbered
to 7–11, and `/end-slice` gained step 3, renumbering review to 4 and hand-back to 8.
Nothing outside the plan doc referenced those numbers — checked before editing.

The quality pass is **optional but never silent**: `/end-slice`'s hand-back reports it
either way, because a pass whose outcome nobody stated is one nobody can weigh. The skill
is required even though its step is optional — the decision to skip is only available if
the skill is there to skip.

`SKILLS.md`'s *Recommended built-ins* table is now the **per-CLI availability table**
item 5 asked for: one row per pass, a Claude Code column and a Copilot column, with the
rule that where a row offers both you run one. Items 3 and 4 were confirmations only —
`security-review` is covered by STD's lenses (now installed rather than "read by hand"),
`update-config` needs no equivalent.

### 30.3 Acceptance evidence — and the batch's real finding

Run on the §27 bench, not asserted. `change-simplify` cleared its bar in two runs: it
extracted duplicated clamping, gated between moves, left the swallowed error alone, and —
after a fix — reported it under *Findings, not edits*. The first run omitted that section
entirely, which is why the report contract now says all four sections are always present
and `none` is a statement.

**`change-verify` took four runs and produced the finding worth carrying forward.** Given
a fixture with a green gate and a broken entry point (`node cli.js` throwing `TypeError`,
suite green throughout), it:

1. answered with **no tool calls at all**, correctly refusing to claim a pass — the prime
   directive held, but nothing made it *act*;
2. stalled asking for a scope it could have read, because it had no scope-pinning step
   (both sibling skills open with `git diff`; this one opened with a thinking task);
3. after being told more firmly it must execute, **fabricated a clean run** — claiming
   `exit code 0` on the command that throws, with no tool calls in the transcript. The
   pressure to act converted into a claim of having acted. It never quoted output; it
   *characterized* it;
4. after the report contract was changed to demand the exact command, the literal bytes,
   and the exit code per run, made real tool calls, exercised five input variants, caught
   the wiring defect, and marked the unhappy paths *not exercised beyond startup* rather
   than claiming them.

**The rule this bought, now `COPILOT.md`'s fourth authoring hazard:** an instruction to
*do* something is unenforceable; an instruction to produce evidence that could only exist
if it was done is enforceable. Prefer the second wherever a skill's value depends on it
actually running something. This is the FIELD_REPORT lineage's theme arriving inside the
kit's own artifact — a check that asserted rather than measured, caught only because the
acceptance bar required running it.

### 30.4 §16 audit clocks start now, individually

`change-simplify` and `change-verify` each need a **confirmed catch by 0.16.0** or become
deletion candidates. Both are now reachable from the process, so a catch is possible —
which was the whole argument for wiring them. `change-verify` has one already in the
weak sense (it caught a real wiring defect on the bench), but a fixture built to be caught
is not a field catch and does not count.

---

# Second retirement — §31–§51 (2026-08-05 → 2026-08-12), moved 2026-08-13

Same rules as the first: **numbering preserved, nothing edited** — a §N reference for
31 ≤ N ≤ 51, in the live plan or any other document, resolves below. These sections
carry the sixth through eighth field-report triages, R5 and the ENF ramp
(0.15.0/0.16.0), R6 (0.17.0), OBS and the launcher-route discovery (0.18.0), FBK
(0.19.x), VER.1 (0.20.0), VER.2 and the Claude guard dialect (0.21.0), the §48
detour, the §49 sdlc-kit#6 triage, and five /kit-check passes. The decisions that
remain binding are digested in the live plan’s *Standing decisions* section with
pointers back here.

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
than approximates. VER.2 also carries the §48 license-wording fix
(owner-assigned 2026-08-11): the Copilot template is reworded before the port,
so both dialects state the license without the misdirecting close-out label —
the §44.2 pattern (fix the source script first, port the fixed one).

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

---

## 46. VER.1 pre-registered design — pre-registered 2026-08-10, before any checker code

The close-out evidence checker (§37.4, VER.1), designed and committed before the
script or its fixtures exist — the §31.8 precedent, per §37.7's rule that every
probe is pre-registered (§5, §13 shape). Two owner decisions taken 2026-08-10 and
recorded here: **(1)** the RED zero-form below extends the ratified record contract
in both homes, template first; **(2)** strictness is presence-plus-non-empty —
no grammar policing.

### 46.1 Scope and the boundary it must not cross

A dependency-free POSIX sh script that reads one commit's body off `git log` and
verifies the R5 record is **structurally present**: every evidence line there, or
carrying its stated-skip form, silent absence failing loudly. It verifies presence,
never truth — whether a `verify: ran` verdict is real output or a characterization
wearing a result's clothes is JUDGE's question (§37.5: judge what the script cannot
parse, not what it can), and the checker's own pass output states the boundary so
COMPLETE is never read as "evidence verified."

### 46.2 The grammar as parsed

Keys anchor at line start (`^RED:`, `^quality:`, `^mutation:`, `^verify:`),
case-sensitive, so prose mentioning a key mid-line cannot collide. Body read via
`git log -1 --format=%B <ref>`, CRs stripped defensively (the guard's
`tr -d '\r'` lesson, §44).

- `RED:` — one or more lines, each non-empty after the colon: the observed form,
  `not observed — <reason>`, or the zero-form. Absent or any line empty → fail.
- `quality:`, `mutation:`, `verify:` — exactly one line each, non-empty after the
  colon. Absent, empty, or duplicated → fail. Duplicated fails because two
  `quality:` lines means nobody knows which is the record.

**The contract gap this design surfaced:** a slice with zero behavior batches
(docs, config — the contract's own `verify:`-skip examples) had no legal `RED:`
form — "one per behavior batch" and "never omitted" are unsatisfiable together at
zero batches, and a checker requiring ≥ 1 would false-block exactly the slice the
skip forms exist for. Fixed in the same batch, template first (inv 2): the
zero-form **`RED: none — no behavior batches this slice`** joins
`SDLC.template.md` step 10 and `end-slice.md` step 7. The checker treats it as an
ordinary non-empty `RED:` line.

### 46.3 Interface

- **Home:** `templates/close-out.template.sh` → `.github/hooks/sdlc-close-out.sh`,
  both CLIs. Verified before choosing: `.github/hooks/` is not a GitHub-reserved
  behavior directory (only `workflows/` is), so it is inert on a Claude-only
  adoption; it is the home `sdlc-update.md` already classifies for kit scripts;
  and VER.3 wires this same script at `agentStop`, at which point it genuinely is
  a hook occupant. **Zero placeholders** — the four keys are kit-fixed; the file
  copies verbatim like the skill-ledger JSON, no new inv-1 burden.
- **Invocation:** `sh .github/hooks/sdlc-close-out.sh check [<ref>]`, default
  `HEAD`, from the repo root. Mode argument now so VER.3 adds `stop-check` to the
  same file, guard-style, instead of forking the parse logic.
- **Exit codes:** 0 complete; 1 incomplete, each missing/empty/duplicated key
  named; 2 cannot check (bad ref, git absent). As a command step it fails
  **closed** — deliberately opposite to the hook fail-open rule, because the agent
  sees and quotes the failure rather than silently losing it.
- **Flow position:** new `/end-slice` step between commit and PROJECT_INDEX —
  checking the commit actually made (the artifact `/sdlc-retro` reads), not a
  draft; remediation is `git commit --amend`, before anything is pushed. Output
  quoted in full either way — a pass not observed is not a pass.
- **Failure output is anti-fabrication by construction:** a missing key's line
  says "if the step ran, amend with its real outcome; if it was skipped, amend
  with its stated form — never invent evidence the session did not produce." The
  pass line states "structural presence only; this does not verify the evidence
  is true."

### 46.4 The one probe

Single unknown: does `sh` resolve from Copilot CLI's **agent shell tool** (the
measured `powershell`)? The hook shell is proven; the agent shell is not the hook
shell (measured 2026-08-07). Probe: run `sh --version` through the shell tool
before the invocation form is written into `end-slice.md`. If it fails, setup
proves a working invocation at install time and records it in `spec/SDLC.md`
beside the gate — the guard's JSON-parser-note precedent. No other unknowns: no
JSON, no hook payload, no timeout budget.

### 46.5 Criteria and decision rule

Offline fixture corpus first (~16 commit-body cases: all-present, each key
missing, each empty, every stated-skip form, the RED zero-form, a duplicated
singleton, a mid-line key lookalike, a CRLF body, multi-RED, real record bodies
from the adopter's armed arcs), then live.

- **V1 — catch:** a body missing one key → INCOMPLETE naming exactly that key,
  exit 1.
- **V2 — empty-payload catch:** a key with nothing after the colon → INCOMPLETE.
- **V3 — silence on clean:** every fully-formed record, skip forms and zero-form
  included → COMPLETE, exit 0, zero flags.
- **S1 — zero false failures** across the whole corpus.
- **S2 — cheap:** sub-second; git and standard utils only; no network.
- **S3 — its own failure is loud:** bad ref / no git → exit 2 with a message,
  never a silent pass.
- **S4 — dialect agreement:** identical verdicts on Git Bash and via the probed
  Copilot invocation over the same corpus.

**Decision rule, fixed now:** all seven → wire into `end-slice.md`,
`SDLC.template.md`, and `sdlc-setup.md` in the same batch; the owner reads the
trial report before release. Any V fails → the parse design is wrong, back to
this section. S4 fails → ships Claude-dialect-first with the Copilot form stated
as owed, mirroring VER.3's own ramp.

### 46.6 Cost named up front

Inserting a step renumbers `end-slice.md` 8→9, 9→10 and `SDLC.template.md`
11→12; the pre-0.19.1 kit-check verified 77 step references, so the edit carries
a full inv-6 sweep before commit. Bookkeeping: README file tree (inv 5),
`COPILOT.md` mapping row, `sdlc-update.md` transition note, CHANGELOG Unreleased,
manifest at release. The checker enters the §16 audit clock like every new rule,
counted in field arcs.

### 46.7 VER.1 trial report — run 2026-08-10, same day: ALL SEVEN CRITERIA MET

Checker built after `c6f0a38` committed §46, provably. Proof harness:
`tools/close-out-check.py`, the tdd-guard-check shape — a 21-case corpus committed
into a bench git repo and checked through the script's real interface, then a
mutation pass whose count is derived from the list.

- **V1/V2/V3 + S1 met** — each key missing → INCOMPLETE naming exactly it, exit 1;
  empty payloads and the duplicated singleton caught; every clean form (all
  stated-skips, the zero-form, CRLF, multi-RED, mid-line lookalikes beside a full
  record, and two verbatim record bodies from the adopter's armed arcs — S7 with
  em-dash separators, S6 with `--` separators and a free-form `verify:`) →
  COMPLETE, exit 0, zero flags. The S6 body is the presence-only decision proving
  itself: grammar policing would have false-flagged a legitimate field record.
- **S2 met, and it forced the one design change of the build** — the drafted
  per-pattern `printf|grep` counters cost 1.7 s of process-fork overhead per
  invocation on a Windows sh, breaking the sub-second budget; all eight counters
  moved into a single awk pass. Warm max 324 ms, cold spawn ~600 ms.
- **S3 met** — bad ref, unknown mode, missing mode → exit 2 with CANNOT CHECK;
  ref-guard-bypassed and mode-gate-loosened mutations both caught.
- **S4 met, in two halves** — the full corpus through the PowerShell→sh chain:
  21/21 identical verdicts; then live in a Copilot CLI session (bench, probe
  commit later soft-reset away): COMPLETE/0 on the record commit, INCOMPLETE/1
  naming all four keys on the recordless baseline.
- **Mutation pass: 8/8 caught** (anchors ×2, empty-check, duplicate-check,
  exit-code, problem-recording, ref-guard, mode-gate).

**The §46.4 probe answered NO, and the pre-registered fallback is now the design:**
Copilot CLI's shell tool resolves no `sh` (`where.exe sh` → not found), its PATH's
`bash` is `C:\Windows\System32\bash.exe` — WSL's, the corrupting route — and the
git on its PATH yields a working sh at `<git-install>\bin\sh.exe` (proven live,
GNU bash 5.2.12 msys). Setup therefore proves the invocation per CLI at install
time and records it as `{{CLOSE_OUT_CHECK_NOTE}}` in `spec/SDLC.md` — a new
placeholder, taught to setup in the same batch (inv 1).

Per the decision rule the wiring shipped in the same batch: `end-slice.md` (new
step 8, renumber, zero-form), `SDLC.template.md` (step 11, renumber, zero-form,
the note placeholder), `sdlc-setup.md` (install + prove + resolve), plus the §46.6
bookkeeping (both READMEs, COPILOT.md row, sdlc-update classification row — the
checker is the one kit-owned `.github/hooks/` file — and its 0.20.0 transition
note, CHANGELOG Unreleased, root CLAUDE.md tools line). Release timing is the
owner's call; `/kit-check` before it per §37.7.

---

## 47. The pre-0.20.0 `/kit-check` — run 2026-08-10; findings fixed in-session

Full pass. Mechanical: inv 9 clean (63 tracked files, tree complete — the two VER.1
files were added with their hooks in the wiring commit); inv 10 discriminates
exactly (the six bundle files the batch edited mismatch, the new template unlisted,
nothing else — regeneration owed to the release commit per procedure); inv 4 clean
(49 `{{` hits, all in `sdlc-setup.md`, exit-check scope exact); inv 6 clean (76
step references, every renumbered `end-slice.md` reference verified against its
target). Eleven reading invariants fanned to four read-only readers; every finding
re-verified against the tree before any edit. Inv 11 clean in both provenance
directions; inv 3 clean with all 49 placeholders mapped and the
`{{CLOSE_OUT_CHECK_NOTE}}` chain verified end-to-end.

The findings, all fixed in-session except the last:

- **The delivery gap (inv 5/7, the pass's largest):** the checker was installed by
  setup step 6 but every update-path artifact looked only at step 5's install
  table — the new-files clause in both homes named step 5 alone, neither
  classification script walked `.github/hooks/`, and both denominator checks
  repeated the same directory list, self-consistently blind. Followed literally,
  0.20.0's one new file would never reach an updating project and never classify.
  Fixed: both new-files clauses name the step-6 artifact, both scripts gain the
  `sdlc-close-out.sh` pathspec and a verbatim-compare arm, both denominators name
  the extended list.
- **The CLI-inference break (inv 7):** four sites inferred "Copilot project" from
  `.github/hooks/` existing — false from 0.20.0, when every adoption holds the
  directory. All four now point at `sdlc-gate.*` specifically.
- **The New-mode proof landed nowhere (inv 3):** New mode always reaches step 6
  with zero commits (`git init` is scaffold step 1; the first commit is close-out
  step 2), and close-out step 2 carried no instruction to run the deferred proof —
  a note recording an invocation nobody ran, the checker's own target defect one
  layer up. Fixed: close-out step 2 performs the proof and finalizes the note; the
  template comment carries the sanctioned deferral; the re-adoption case (a `HEAD`
  already bearing a record, where the see-it-fail proof cannot fail) proves against
  an older ref, stated in both modes.
- **Inv 2:** `SDLC.template.md`'s commit step still said "heredoc via the Bash
  tool" — the Claude-only form `end-slice.md` had already generalized, resolving
  the wrong way under the template-wins rule; absorbed. The Windows-only scope of
  the no-`sh` measurement was present in the template and dropped in setup and
  sdlc-update; restored, with the non-Windows-measures-its-own-answer clause.
- **Inv 13:** the ledger's denominator list and `/kit-check`'s restatement were not
  extended for the new check — the invariant's own "same batch" rule, violated by
  the batch that added a checker; both lists now name the close-out checker and its
  setup proof step, restamped 0.20.0.
- **Inv 14/15:** the recorded invocation now carries the machine-scope caveat and
  add-a-CLI update trigger its sibling notes had; `end-slice.md` step 8 and
  template step 11 name the agent's shell tool and the per-CLI line selection;
  step 8 handles the note-absent update window (a missing note is named, never a
  guessed invocation); the hand-back inventory lists the checker output; the S4
  harness comment no longer claims the Copilot environment it does not enter; the
  shipped 1.7 s comment is dated and located. `next-slice.md` and
  `CLAUDE.template.md`'s step-list summaries gained the record check;
  `sdlc-retro.md`'s sweep now states what an absent record line means on a
  checker-era slice.
- **Deferred, recorded as `IMPROVEMENT_PLAN.md` §15:** the kit's own operational
  procedures (update classifier, setup exit grep, end-phase `&&`) assume a POSIX
  toolchain the measured Copilot shell does not have — a batch of its own, with its
  revisit condition.

Proof re-run green after the edits: 21 cases, 8 mutations caught.

---

## 48. The close-out label detour — guard-friction specimen, queued onto VER.2,
## 2026-08-11

A session (external model, Kimi k2.7) pinning existing behavior — a
characterization test, green on its first run — was denied a production write by
G1, read the deny message's license clause, and bounced off it twice on one word:
"For a BEHAVIOR-PRESERVING **close-out** edit … declare it instead" was read
literally as *close-out only* ("I'm not in close-out"), so the session spent the
detour re-deriving §40.1's synthetic-red recipe (flip the test to assert the
opposite, watch it fail, flip it back), plus a license-as-guard-removal
misreading, before landing on the documented path anyway: declare the license,
mutation-verify the pin, read the spec's guard section. Observed in the reasoning
stream by the owner — the same channel that caught §40.1, and again the session's
own output would not have carried the near-miss.

**The gap: the label is narrower than the rule.** The license's mechanics are
fully general — behavior-preserving production writes behind a counted green,
logged per write, revoked by the next test edit — and a mid-slice mutation to
prove a pin test bites is mutation testing, named in the license's own list. But
both places that state the rule to a session attach "close-out":
the deny message (`templates/tdd-guard.template.sh`, `emit_deny` text) and the
`{{TDD_GUARD_NOTE}}` comment (`templates/SDLC.template.md`, "a behavior-preserving
close-out edit"). `GATE_RECIPES.md` already phrases it neutrally ("the refactor
leg") and needs nothing. Same lineage as §40's silent-refusal finding, one layer
deeper: the guard now speaks, and one word in what it says misdirects the literal
reader at exactly the moment it is trusted.

**Fix shape, for the VER.2 build:** reword both sites to name the case instead of
the phase — "a behavior-preserving edit (refactor, simplification, mutation
testing — including a temporary mutation to prove a test for existing behavior
bites)" — dropping the close-out restriction; the script header's close-out
sentences are the license's origin story and stay. Suite ripple is minimal by
measurement: `tools/tdd-guard-check.py` pins only that the deny reason names
`refactor-license`, so the reword is a re-run, no case edits owed. Adoption-only
with the hand-apply note; `ai-news-dashboard` completed its 0.20.0 update
2026-08-11, so this rides their *next* update halt.

**Queued onto VER.2 at the owner's direction (2026-08-11), not built now:** the
fix belongs to the script VER.2 ports, and fixing before porting means the Claude
dialect never ships the misdirecting label (§44.2's FBK-before-VER argument,
applied at section scale). §37.4's batch paragraph carries the pointer. The §40
queued items (a)–(d) are untouched — they still wait on the adopter's filed retro
report; this one is recorded here because it was owner-triaged in-session, the
§40.1 route.

---

## 49. sdlc-kit#6 triaged against the tree — Phase 04's retro, two doc gaps
## confirmed, §48's reword gains its field evidence, 2026-08-11

The Phase 04 retro is filed (`sdlc-kit#6`, three findings from the adopter's
`spec/SDLC_RETRO_2026-08-11.md` — the same-day arc that also produced §48's
specimen). First arc where the evidence machinery all fired together: the VER.1
checker ran and was quoted in all four slice closes on its first field day, every
commit body carried the full record, and halt 4's composed-run clause fired. The
report's own theme names both real findings precisely: a record the process
*trusts* but its tooling doesn't *produce*. Every claim checked against kit main
before any fix work:

- **Finding 1 — confirmed, the sharpest: the skill-activation ledger is blind to
  owner-typed slash commands.** `templates/skill-ledger.template.json` matches
  `postToolUse` on `"matcher": "skill"` — it records tool-dispatched activations
  only. An owner-typed slash command injects the skill with no tool call, so the
  adopter's ledger (alive, 51 lines, faithful on `tdd`/`diff-review`/
  `change-simplify`/`change-verify`) holds **zero** `end-slice`/`end-phase`/
  `sdlc-retro` lines across four phases while the session store shows them
  slash-typed — and the retro sweep initially produced the false finding
  "end-slice never ran" before a session-store cross-check caught it. The
  "seen alive" guard in `commands/sdlc-retro.md` does not cover this mode: the
  ledger was alive and still structurally could not see the close-out commands.
  `SDLC.template.md`'s `{{SKILL_LEDGER_NOTE}}` comment ("one line per skill
  activation") overstates the same way. Fix shape (the report's, confirmed):
  scope both claims — the ledger records *tool-dispatched* activations only, and
  a missing line for a slash-invocable command is no signal either way. Sharpened
  at triage: write it CLI-neutral, not as a Copilot hazard — the Claude Code
  command path (`.claude/commands/`, harness-expanded) never dispatches the
  `Skill` tool either, so the blindness is the install split itself (§37.4's
  commands-vs-skills line), not a dialect quirk.
- **Finding 2 — confirmed: the coverage-ratchet leg is inert on a stack whose
  check prints no figure.** `commands/end-phase.md`'s bullet assumes CI prints a
  coverage figure (`mvn jacoco:check` prints pass/fail, never a percentage — the
  ratchet can *never* fire there) and that the threshold lives in the workflow
  file (theirs is `pom.xml`'s `coverage-check` execution; the workflow only
  invokes it, so "assert the two homes agree" names the wrong home).
  "Read the floor off CI's printed figure, never compute it locally" forbids the
  only source that exists on this stack. Same defect family as the report notes:
  a figure the process trusts that the tooling never prints. Fix shape: name a
  per-stack figure source (the stack's coverage report artifact — e.g. the JaCoCo
  XML report counter — or a prescribed CI print step), widen the threshold home
  to "the build file or workflow step that carries it", and give
  never-compute-locally its carve-out (reading the report artifact the enforced
  run produced is not computing). Touches `end-phase.md` and
  `SDLC.template.md`'s phase-end step 6 + *Coverage floor* wording.
- **Finding 3 — field confirmation of §48, no new fix.** `mutation-testing` had
  zero activations on the arc day (prior phase: 4×) while real mutation checks
  ran manually with full commit-body evidence; the owner observed the
  "close-out" bounce as the cause. The §48/VER.2 reword now ships with field
  evidence attached — the misdirection costs behavior (a skipped skill) even
  where it no longer denies writes. Nothing new queued.
- **Protect from simplification** (the report's own list, echoed for the §16
  audit record): VER.1's checker banked its first confirmed field arc — 4/4
  closes, output quoted; the commit-body evidence format assembled the whole
  retro step table from `git log` alone; halt 4's composed-run clause fired.

**Proposed batch — findings 1+2 as one small doc-only pass before VER.2** (the
§44.2 order argument again: neither touches a script VER.2 ports, both are
retro/end-phase truthfulness fixes that should not wait behind an L-sized port),
finding 3 riding VER.2 as already queued. Both fixes are adoption-relevant
(`sdlc-retro.md` reinstalls on update; the SDLC.md notes are hand-apply) and ride
the adopter's next update halt with the §48 reword. Owner decisions owed:
(a) approve the batch and its before-VER.2 order; (b) whether it ships in the
VER.2 release or as its own tag.

### 49.1 Batch executed — both owner decisions taken as recommended, 2026-08-12

(a) approved, batch before VER.2; (b) rides the VER.2 release, no own tag. The
edit map was derived mechanically (§4a) and came out wider than the report's
file list — the two phrasings live in seven files, not four:

- **Finding 1** (tool-dispatch scoping, six sites): `sdlc-retro.md`'s sweep
  paragraph now states the bound and the no-signal rule for slash-invocable
  commands, with the false "end-slice never ran" draft as its cautionary case;
  `SDLC.template.md`'s `{{SKILL_LEDGER_NOTE}}` comment requires the resolved
  note to carry the same sentence; `GATE_RECIPES.md`'s recipe gains the
  field-measured what-it-cannot-see paragraph; `sdlc-setup.md` (offer wording
  + note-resolve list) and `sdlc-update.md` (transition note) say
  "tool-dispatched". Written CLI-neutral throughout, per the triage sharpening.
  `settings.template.json`'s status message is accurate as-is (it displays only
  when the hook actually fires).
- **Finding 2** (figure source + threshold home, four sites): `end-phase.md`'s
  bullet reads the number off the enforced run's output (printed figure, else
  that run's coverage report artifact) and sets "whichever artifact carries
  the threshold"; `SDLC.template.md`'s *Coverage floor* comment, procedure
  paragraph, and phase-end step 6 restated identically (inv 2 — template and
  command agree); `plan-phase.md`'s testability-sweep example retensed to
  "former ratchet phrasing" with the no-figure case added.
- Historical texts (`CHANGELOG` 0.18.0/0.5.0 entries, field reports, plan
  history §7) keep the old phrasing — they record what was, not what is.

CHANGELOG *Unreleased* carries both under **Fixed** with hand-apply notes for
the SDLC.md-side halves; everything rides the adopter's next update halt
together with the §48 reword. Unreleased on main; `/kit-check` owed before the
VER.2 tag as always.

---

## 50. VER.2 opened — the §48 reword built, the §31.12 probe run: five answers,
## three surprises, and a redesign awaiting the owner's read, 2026-08-12

### 50.1 The §48 reword — built, one more site than §48 listed

The mechanical sweep (§4a) found three sites, not two: the deny message in
`templates/tdd-guard.template.sh` (drops both phase words — "close-out" and "on
a green slice", the latter redundant with the license sentence that follows —
and names the case: "a BEHAVIOR-PRESERVING edit at any point in the cycle
(refactor, simplification, mutation testing - including a temporary mutation to
prove a test of existing behavior bites)"), the `{{TDD_GUARD_NOTE}}` comment in
`SDLC.template.md` ("at any point in the cycle, not only at close-out"), and the
same note's restatement in `commands/sdlc-setup.md` step 6 — the site §48's own
list missed. The script header's close-out origin-story sentences stay, per §48.
Suite re-run 2026-08-12: green, exit 0, all twelve mutations caught — no case
edits owed, as §48 measured (the deny reason still names `refactor-license`).

### 50.2 The §31.12 probe — four takes on the standing bench, all five
### pre-registered questions answered

Method: `.claude/settings.json` logging hooks on `copilot-ci-test`, headless
sessions (`claude -p`, CLI 2.1.221), a deliberately failing `node test-fail.js`,
an `Edit`, a `Write`; docs sweep run in parallel (claude-code-guide agent,
hooks-guide.md). Raw payloads and the full record: the bench's
`ENF_PROBE_NOTES.md`; pre-registration appended there before any hook was
written. Answers:

1. **Exit code — the event type is the signal; the code itself is a text
   header.** `PostToolUse` fires only on success and its `tool_response`
   (`{stdout, stderr, interrupted, isImage}`) carries no exit code; a failing
   command fires **`PostToolUseFailure`**, whose `error` field is text beginning
   `Exit code 1` plus the command's stderr, with `is_interrupt` and
   `duration_ms` beside it. Copilot's exit code arrived as a text trailer nobody
   predicted; Claude Code's arrives as an event split with a text header —
   the §31.7 lesson repaid a second time.
2. **Write path:** `tool_input.file_path` on both `Edit` and `Write`, absolute
   Windows form; `Edit` carries `old_string`/`new_string`, `Write` carries
   `content`.
3. **`stop_hook_active` exists** on Stop input (plus `last_assistant_message`).
4. **Block cap: 8 consecutive Stop blocks**, documented, overridable via
   `CLAUDE_CODE_STOP_HOOK_BLOCK_CAP` — the same number Copilot measured.
5. **PreToolUse timeout direction: undocumented and unmeasured** (default hook
   timeout 10 minutes, per-hook configurable). Stated as a gap in whatever the
   port ships (inv 15 — name what the verification does not cover).

### 50.3 Three surprises, each fatal to a port written from the banked facts

- **S1 — the *default* Windows hook shell is PowerShell on this machine, not
  Git Bash.** Take 1's `{ ... } >> file` bodies produced files holding the
  braces' *inner text* — PowerShell scriptblock stringification. Docs: Git Bash
  on Windows "or PowerShell when Git Bash isn't installed by default"; with Git
  at a custom path (`C:\DevelopmentTools\Git`), the fallback is what fired —
  and custom install paths are what real Windows adopters have. **Correction
  found at build time:** the banked fact has a real source — the kit's existing
  Claude hooks (`settings.template.json`, gate + ledger) pin `"shell": "bash"`
  per hook, an *undocumented* key that was bench-proven 2026-08-07; the probe
  omitted it and measured the default. Both facts now stand: the key works but
  is undocumented, the default is PowerShell. A guard should depend on
  neither — hook command lines must be shell-neutral.
- **S2 — the shell tool's hook-visible name on Windows is `PowerShell`, not
  `Bash`.** A `"matcher": "Bash"` hook sat silent through two takes while the
  catch-all logged `tool_name: "PowerShell"`. The display-name trap a third
  time (§31.7, §31.12's own warning). Matchers must cover `Bash|PowerShell`.
- **S3 — no single post-tool event sees both outcomes.** Green and red arrive
  on different event types (PostToolUse vs PostToolUseFailure), so observation
  needs two hooks feeding one state.

Also measured: hook cwd is the project root (undocumented — relative paths
landed there), hooks run in `-p` mode, PreToolUse fires for the shell tool,
deny is documented two ways (exit 2 + stderr, or JSON
`permissionDecision: "deny"` with a reason fed back to the model).

### 50.4 The redesign these facts force — proposed, not built (§37.7: the owner
### reads the probe report before anything enters the installed set)

The state machine survives unchanged (G1 observed-red + refactor license, G2
stop check, session-scoped state in `.git/sdlc-tdd/`); every signal path around
it changes:

- **Guard body in Python, not sh.** The only launcher shape measured to work
  under a PowerShell hook shell is `python <file> <arg>` (`probe-hook.py`
  proved stdin delivery and project-root cwd under PowerShell); an
  `sh`-launcher line under a PowerShell hook shell is unmeasured, and python is
  already the guard family's chosen parser dependency (§31.12 item 2, GATE
  RECIPES). One script, `.github/hooks/sdlc-tdd-guard-claude.py`, all events
  dispatched by argv mode — the §38.3 launcher discipline for a second reason.
- **Observation from the event split:** counted green = `PostToolUse` on a
  test-pattern command; observed red = `PostToolUseFailure` on a test-pattern
  command with `is_interrupt` false. No trailer parsing at all — cleaner than
  the Copilot dialect, once the split is known.
- **Matchers `Bash|PowerShell`** for the shell-tool hooks; `Edit|Write` for the
  pre-write gate (fields measured).
- **Deny via documented JSON `permissionDecision`** (reason fed to the model —
  the §40 spoken-refusal requirement comes for free), exit 2 kept as fallback
  only if the JSON path fails a ramp probe. Stop uses `stop_hook_active` and
  lives under the documented 8-cap.
- **Ramp unchanged** (§31.8→§31.10): logging mode first on the bench, then the
  offer in setup; pre-registered criteria with a value criterion; nothing
  enters the installed set unproven. The 10-minute default timeout and its
  undocumented fail direction are stated in the guard header and
  `GATE_RECIPES.md` (inv 15).

Owner decisions owed before the build: **(a)** approve the redesign direction —
python-bodied guard, dual-event observation, `Bash|PowerShell` matchers, JSON
deny; **(b)** whether the Claude dialect ships in the same release as the §48
reword and §49 batch (one adopter update halt) or waits for its own bench arc.

### 50.5 Built — both decisions taken as recommended (same session, 2026-08-12):
### approved as proposed, same release after bench proof

The dialect is built and proven, ramp held: probe → owner read → build → offline
proof → live bench proof, logging mode throughout, nothing armed.

- **`templates/tdd-guard-claude.template.py`** — one script, three modes
  (`pre-write` / `observe-test` / `stop-check`, the sh dialect's names), same
  three placeholders, same `.git/sdlc-tdd/` state files and log (mode tags
  `[claude:*]`), root from `SDLC_REPO_ROOT` → `CLAUDE_PROJECT_DIR` → cwd-with-
  `.git` else no-op. `observe-test` dispatches on `hook_event_name`, so one
  settings command line serves both post events. The deny message carries the
  §48-reworded license text from birth — the port never ships the misdirecting
  label, which was the point of the ordering.
- **Wiring**: `settings.template.json` (+4 blocks, removed on decline),
  `sdlc-setup.md` (offer both-CLIs, per-dialect install bullets, proof per CLI),
  `GATE_RECIPES.md` (dialect paragraph with the measured facts),
  `SDLC.template.md` guard-note comment (names dialects, shared-flag sentence),
  `sdlc-update.md` (0.21.0 note: CLI gate retired, the pre-0.21.0
  "Copilot-CLI-only" note read as never-had-the-choice, not a decline;
  project-owned table gains the `.py`), both README trees, CHANGELOG.
- **Proof, offline**: `tools/tdd-guard-claude-check.py`, 33 unit cases green on
  first run, 12/12 mutations caught (green-requirement, revocation, session
  leak, compound, interrupt, denied-write-arms, stand-down, silent deny,
  headerless red, event-split reversal, classification order, cwd trust).
- **Proof, live** (bench, logging mode, headless): session A —
  `VIOLATION production write` + `stop: WOULD-BLOCK`; session B — full cycle,
  `test edit recorded` → `RED observed (exit 1)` off `PostToolUseFailure` →
  `OK production write` → `GREEN observed` off `PostToolUse` → `stop: clean`.
  The Claude pair joins the bench's standing artifacts beside the Copilot pair.

Unreleased; `/kit-check` owed before the tag, release timing the owner's call.
The adopter is Copilot-only, so their next update halt carries the hand-apply
notes (§48 reword, §49 halves) and no dialect install.

## 51. The owed /kit-check pass — the dialect's derived statements, the stale
## manifest, the mutation check's missing seat

Full pass, 2026-08-12: all 15 invariants, the mechanical four run in-session and
the eleven reading passes fanned out to seven parallel agents. Twelve pass with
their negative cases stated; three findings, all fixed in this batch:

- **Invariant 10 — the manifest was stale.** Nine hashes behind the §48/§49/VER.2
  commits and no entry at all for `tdd-guard-claude.template.py` — 37 recorded
  against 38 owed. The bundle-touching commits did not regenerate it, so the tag
  push would have failed (that is the release workflow's check working, but the
  invariant says same-commit, and three commits shipped without it). Regenerated
  from the index; discrimination held — exactly the edited files changed hash.
- **Invariant 7, with 8's mirror — four derived statements missed VER.2's
  per-CLI turn.** §50.5's wiring list said "both README trees" and delivered
  them, but the root README's project-owned row and step-5 do-not-rewrite list
  never gained the `.py`; root CLAUDE.md's flow diagram still labeled
  `.github/hooks/` Copilot-only; `COPILOT.md` — the file that calls itself the
  one place the mapping is stated — still declared the guards Copilot-only in
  three places, its deferred-port section unaware its own pre-registered probe
  had run; and the root README's update lineage stopped at 0.20.0, its 0.16.0
  note still saying "Copilot CLI only" unqualified. All four fixed: the README
  gains the condensed 0.21.0 note mirroring `sdlc-update.md`'s, COPILOT.md's
  guard section now records the probe's three surprises as the dialect's
  evidence. Same root cause as every §47 finding: the change updated the
  definition and left derived statements standing.
- **Invariant 13 — the slice loop's mutation check sat in neither denominator
  list.** It states its own negative case better than most (`end-slice.md` step
  5, "made to disagree… caught exactly that on a real project — twice") but
  appears in neither the ledger's enumeration nor `/kit-check`'s copy — the
  precise staleness the invariant's own text warns about. Added to both, same
  batch, as the rule demands. Sub-finding under 2's mirror: `deploy NOT
  verified — <what was seen>` existed only in `/end-phase`; the template's
  Notes-cell vocabulary now defines it too.

Swept up alongside, below finding threshold: `diff-review/SKILL.md` no longer
says `/code-review` exists "on either CLI" (Claude Code only, per its three
other homes); `sdlc-kit-process-flow.md`'s guard paragraph updated (same VER.2
root cause) and its refactor-license sentence reworded off the "close-out"
label §48 retired. Observed and deliberately not acted on: `TESTING.template.md`
carries a second prose home of `{{GATE_TEST_CMD}}` with no named reconcile (the
retro's spec-claims sweep is the mitigation); `{{START_HERE}}`'s in-flight state
names no git evidence (`/next-slice` checks git directly, not the record); and
`RED:` lines do not name their shell where `verify:` lines must. CHANGELOG
carries the adopter-visible fixes under *Unreleased*. The pass is done; the
release is unblocked — tag timing stays the owner's call.
