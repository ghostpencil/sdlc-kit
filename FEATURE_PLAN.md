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
