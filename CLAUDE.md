# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This repo contains **no application code** — it is a distributable kit of Claude Code
prompt files (commands, skills, templates, reference docs) that describes and automates a
software development lifecycle. There is nothing to build, lint, or test. The only
verification available is reading for internal consistency: `/kit-check` runs that
reading pass against the canonical ledger in `KIT_INVARIANTS.md` (see *Invariants*
below for the working summary).

The kit is **not applied to itself**: there is no `spec/`, no gate, no phase branches
here. Work on this repo is ordinary editing plus careful cross-file consistency.

## Repo layout: product vs. docs about the product

The repo root is **not** the kit. `sdlc-kit/` is the shippable product — the only folder
that is copied into an adopting project, and the unit that gets packaged as a release
artifact. Everything at the root (`README.md`, `CLAUDE.md`, `FIELD_REPORT.md`,
`FIELD_REPORT_2026-07-20.md`, `FIELD_REPORT_2026-07-22.md`, `IMPROVEMENT_PLAN.md`, `FEATURE_PLAN.md`,
`FEATURE_PLAN_HISTORY.md`, `KIT_INVARIANTS.md`, `LICENSE`, the root `.claude/commands/`,
the root `tools/` — re-runnable proofs for the two shipped hook artifacts, which are
kit-development checks and not part of the process the kit installs)
is documentation *about* the kit and must never end up in an adopter's repo.
`FEATURE_PLAN.md` carries only the standing decisions, running clocks, and active work;
its retired sections (§1–§30) live in `FEATURE_PLAN_HISTORY.md` with numbering
preserved, so a `FEATURE_PLAN.md §N` reference with N ≤ 30 — here or in any older
document — resolves there.

When adding a file, the question is always: does an adopting project need this at setup or
slice time? Yes → `sdlc-kit/`. No → root.

Paths below written as `commands/…`, `templates/…` are relative to `sdlc-kit/` — the same
way they read once the folder is sitting in a target project.

## Architecture: three layers, one direction of flow

```
sdlc-kit/ (the product)  ──/sdlc-setup──▶  target project
  templates/*.template.*                     CLAUDE.md, spec/*.md, .claude/settings.json
                                             (Copilot: .github/hooks/, .github/agents/)
  commands/*.md                              .claude/commands/*.md
                                             (Copilot: .github/skills/<name>/SKILL.md)
  skills/<name>/SKILL.md                     .claude/skills/<name>/SKILL.md
                                             (project-scoped; both CLIs read it)
  reference/*.md                             (stays put — consulted by setup, not installed,
                                              EXCEPT REVIEW_LENSES.md → .claude/commands/)
```

`commands/sdlc-setup.md` is the entry point and the only file that reads the others. It
runs in two modes — **New Project** (interview → scaffold → establish a green gate) and
**Existing Project** (analyze → propose → confirm → generate, merging never overwriting) —
and it instantiates every template, installs the four daily commands, `sdlc-retro.md`,
`sdlc-update.md`, the vendored TDD skill set, and the three kit-written change passes
(`diff-review`, `change-simplify`, `change-verify`), and writes the edit-time hook.
`commands/sdlc-update.md`
brings an adopted project forward to a newer kit release; it and the root README's
*Updating an adopted project* section state the same procedure and must agree.

The process the kit installs is **phases → slices → TDD cycles**, gated by lint +
typecheck + tests, with exactly five owner halt points. `templates/SDLC.template.md` is
the canonical statement of that process; the four daily commands (`plan-phase`,
`next-slice`, `end-slice`, `end-phase`) are its automation. `spec/PROJECT_INDEX.md` (from
`PROJECT_INDEX.template.md`) is the single source of truth in an adopted project — the
load-bearing piece that lets a fresh session orient in seconds.

**The install split is by how a file is invoked, not by what it contains.** The seven
commands are user-typed entry points and go to `.claude/commands/`; the eight skills —
five vendored, three kit-written since 0.14.0 — are model-invocable and go to
`.claude/skills/<name>/SKILL.md`. Both are
project-scoped, so both travel with a `git clone` — that was always the point, and until
0.14.0 it was served by putting everything in `.claude/commands/`. The move happened
because `.claude/skills/` is read by Copilot CLI as well, so one copy now serves both
CLIs; the commands stayed put for the opposite reason, since a command sitting in a
skills directory can be invoked by the model unbidden. The Copilot column of every
mapping is in `sdlc-kit/reference/COPILOT.md`, and `commands/sdlc-setup.md`'s install
list (New mode step 5) is the definition both READMEs and `sdlc-update.md` derive from —
keep them in step if you touch install paths. (An `agents/` → `.claude/agents/`
mapping existed on kits 0.6.0–0.9.0 and was retired in 0.10.0 with its only occupant,
the surveyor; `sdlc-update.md` still classifies `.claude/agents/` for the transition,
and now also handles the 0.14.0 skills move as a removal-and-re-add.)

## Invariants to preserve when editing

The canonical, full ledger is `KIT_INVARIANTS.md` at the root — 15 invariants, each with
the real defect that motivated it — and `/kit-check` is the reading pass that verifies
them. The six below are the working summary; on disagreement the ledger wins.

1. **The placeholder contract.** Templates carry `{{PLACEHOLDER}}` markers; setup must
   resolve every one, and its exit check is
   `grep -r '{{' CLAUDE.md spec/ .claude/settings.json` — scoped to the instantiated
   files, because the installed `sdlc-setup.md` legitimately names placeholders.
   Adding a placeholder to a template without teaching `sdlc-setup.md` to ask for it
   breaks that check. Current set spans `templates/` and the hook recipe in
   `reference/GATE_RECIPES.md` (which documents the four `{{HOOK_*}}`/`{{SOURCE_GLOB}}`
   ones).
2. **`SDLC.template.md` wins.** It says so itself: if a command and the SDLC file
   disagree, the file is right and the command is the bug. A process change therefore
   usually touches the template *and* one or more commands — check both.
3. **`skills/` has two provenance regimes.** Five files came from upstream MIT repos;
   three (`diff-review`, `change-simplify`, `change-verify`) are kit-written with no
   upstream. `reference/SKILLS.md` records per-file provenance and verification dates,
   and `THIRD_PARTY_NOTICES.md` carries the attributions *and* says which files it does
   not cover. Editing a vendored skill diverges it from upstream — note that in
   `reference/SKILLS.md` rather than silently drifting. Describing a kit-written skill
   as vendored is the same defect pointed the other way.
4. **Gate recipes must match reality, not defaults.** `reference/GATE_RECIPES.md`
   repeatedly instructs setup to prefer the commands a project already runs in CI over the
   kit's suggested ones — "the gate must match CI, or the gate lies."
5. **The README's file tree** enumerates every file in the repo; adding or renaming one
   means updating it.
6. **Nothing kit-development-only may live under `sdlc-kit/`.** That folder is shipped
   verbatim to adopters and packaged as a release artifact; the field report, this file,
   and the improvement plan stay at the root.

## FIELD_REPORT.md is the open backlog

`FIELD_REPORT.md` documents the first external adoption (a Python project, Existing
Project mode) and lists 14 numbered gaps, each naming the file(s) that need to change,
with a prioritized table at the end. Treat it as the issue tracker — but check
`IMPROVEMENT_PLAN.md` §2 for what is already done before acting on it. The two findings
that were load-bearing context for any edit are both resolved: **#1** (a command
asserting a project fact) was fixed in v0.2.0 and became the invariant that commands
state no project facts; **#14** (no update path) is closed by `commands/sdlc-update.md`
plus the root README's update procedure — the two state the same procedure and must
agree.

Its cross-cutting conclusion is worth applying to new work: the kit is strong at
*specifying* process and weak at making it *self-checking*. Prefer changes that fail
loudly (scaffolded blockers, commands that read a recorded baseline) over changes that add
more prose rules.

`FIELD_REPORT_2026-07-20.md` is the second report from the same adoption — the first real
run of `/sdlc-retro` (F1's acceptance evidence), with 12 findings and a 15-row priority
table, all 15 rows actioned by R1 (`FEATURE_PLAN_HISTORY.md` §7, shipped as v0.5.0). Its
cross-cutting theme extends the first report's: checks whose *denominator* was assumed
rather than enumerated — including inside the kit's own `/sdlc-update`.

`FIELD_REPORT_2026-07-22.md` is the third — the first full arc run on kit 0.6.0, with 3
findings and a 3-row priority table. Its theme sharpens the lineage again: a number
recorded in prose is not the number the machine enforces, and the kit's bookkeeping
updates the prose without reconciling against the enforcing artifact. `FEATURE_PLAN_HISTORY.md`
§10 records how it was triaged.

`FIELD_REPORT_2026-08-01.md` is the fourth — a different adopter's fifth phase, filed as
`sdlc-kit#1`, with 8 findings and a priority table. Its theme is the widest yet and now
carries an invariant of its own (15): **the process verifies the artifact and is silent
about the environment it will run in** — a gate green in the test environment said
nothing about a control that was live in production, and four of its eight findings are
instances of that one gap. `FEATURE_PLAN_HISTORY.md` §12 records the triage, including the three
claims that did not survive verification against the tree and the one already fixed in
0.7.0.

`FIELD_REPORT_2026-08-02.md` is the fifth — the same adopter's sixth phase (its first
BUILD arc, and the first report written against the then-current release, 0.9.0), filed
as `sdlc-kit#2`, with 10 findings and a priority table whose top row is owner-ranked:
finding 7, a simplification pass auditing every rule added since 0.5.0 against a
confirmed catch, runs **as its own batch before any R4 fix batch**. Its theme completes
the lineage: **the kit specifies what each step must produce and almost never what makes
it done** — the gate is the only step with a completion condition and the only step that
never failed. `FEATURE_PLAN_HISTORY.md` §15 records the triage: nine of ten findings stood
(three with step-number or scope corrections), and the work shipped as two batches —
SIMP, the simplification pass (v0.10.0), then R4, the ten-rule fix batch (v0.11.0,
§17).

## Writing conventions for these files

Command files are prompts, not documentation. The established shape is: a title, a
one-paragraph statement of what the command does plus its process reference, a **prime
directive** line where one applies (`sdlc-setup`: never assume, never overwrite;
`plan-phase`: never fill a gap with an assumption), a *How to use* section with the
invocation and optional arguments, then *Workflow* as numbered steps. Owner halt points
are called out inline and explicitly (*halt 2*, "— HALT", "the ONE owner halt"). Prose is
hard-wrapped near 90 characters.
