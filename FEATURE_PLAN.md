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
6. **Then F3** (slice-runner TRIAL, §3, unchanged in shape). Phase 06 (#64, retrieval
   redesign) is the natural arc to trial it on — and it is the first close that must
   answer for TFit's 171, unchanged for four arcs, under R3.3's new rule.

**Standing note for the next retro** (raised 2026-08-01, not yet field-tested): R3 is
the fourth batch of process rules added on field evidence with no simplification pass
between them. The next `/sdlc-retro` is the place to ask which earned their keep —
finding 6's escalation threshold and finding 2's re-derivation are the two most likely
to read as ceremony if they never catch anything. A rule that costs and returns nothing
is a finding too.
