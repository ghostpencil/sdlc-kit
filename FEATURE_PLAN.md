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
| Slice-runner straight into the kit | **Reshaped** into a gated trial (F3). Execution-model changes ship on evidence, not on design confidence. |

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
- **Acceptance, plan-phase half — open.** "A plan-phase run on a real spec with
  sweeps delegated and every owner interaction in the main session" needs a real
  owner interview; it runs on the next real phase planned on an adopted project
  (TFit), same shape as F1's acceptance. Until then the delegation is
  design-verified, not field-verified.

### Resume here

1. **Migrate TFit to 0.6.0** (`/sdlc-update` — owner-halting, so run it with the
   owner). Note for that run: `{{MODEL_POLICY}}` and the friction-log seed are
   [adoption-only] — TFit's project-owned `spec/SDLC.md` and `PROJECT_INDEX.md` do
   not receive them automatically; the changelog flags both as manual follow-ups,
   and TFit already has its own friction log (the section the seed generalizes).
2. **F2's open acceptance half** rides the next `/plan-phase` on TFit.
3. **Then F3** (slice-runner TRIAL, §3) — on TFit or Dungeon Daddy, kit untouched
   until the trial passes. Ships as `v0.7.0` only if it does.
