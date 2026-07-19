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
`IMPROVEMENT_PLAN.md`, `KIT_INVARIANTS.md`, `LICENSE`, the root `.claude/commands/`) is
documentation *about* the kit and must never end up in an adopter's repo.

When adding a file, the question is always: does an adopting project need this at setup or
slice time? Yes → `sdlc-kit/`. No → root.

Paths below written as `commands/…`, `templates/…` are relative to `sdlc-kit/` — the same
way they read once the folder is sitting in a target project.

## Architecture: three layers, one direction of flow

```
sdlc-kit/ (the product)  ──/sdlc-setup──▶  target project
  templates/*.template.*                     CLAUDE.md, spec/*.md, .claude/settings.json
  commands/*.md                              .claude/commands/*.md
  skills/** (incl. tdd-references/)          .claude/commands/**   (project-scoped)
  reference/*.md                             (stays put — consulted by setup, not installed,
                                              EXCEPT REVIEW_LENSES.md → .claude/commands/)
```

`commands/sdlc-setup.md` is the entry point and the only file that reads the others. It
runs in two modes — **New Project** (interview → scaffold → establish a green gate) and
**Existing Project** (analyze → propose → confirm → generate, merging never overwriting) —
and it instantiates every template, installs the four daily commands, `sdlc-update.md`,
and the vendored TDD skill set, and writes the edit-time hook. `commands/sdlc-update.md`
brings an adopted project forward to a newer kit release; it and the root README's
*Updating an adopted project* section state the same procedure and must agree.

The process the kit installs is **phases → slices → TDD cycles**, gated by lint +
typecheck + tests, with exactly five owner halt points. `templates/SDLC.template.md` is
the canonical statement of that process; the four daily commands (`plan-phase`,
`next-slice`, `end-slice`, `end-phase`) are its automation. `spec/PROJECT_INDEX.md` (from
`PROJECT_INDEX.template.md`) is the single source of truth in an adopted project — the
load-bearing piece that lets a fresh session orient in seconds.

Note that **skills install into `.claude/commands/`, not `.claude/skills/`** — that is
deliberate (project-scoped, so they travel with a `git clone`) and is stated in several
files; keep it consistent if you touch install paths.

## Invariants to preserve when editing

The canonical, full ledger is `KIT_INVARIANTS.md` at the root — 13 invariants, each with
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
3. **Vendored skills are third-party.** Everything in `skills/` came from an upstream MIT
   repo. `reference/SKILLS.md` records per-file provenance and verification dates, and
   `THIRD_PARTY_NOTICES.md` carries the attributions. Editing a vendored skill diverges it
   from upstream — note that in `reference/SKILLS.md` rather than silently drifting.
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

## Writing conventions for these files

Command files are prompts, not documentation. The established shape is: a title, a
one-paragraph statement of what the command does plus its process reference, a **prime
directive** line where one applies (`sdlc-setup`: never assume, never overwrite;
`plan-phase`: never fill a gap with an assumption), a *How to use* section with the
invocation and optional arguments, then *Workflow* as numbered steps. Owner halt points
are called out inline and explicitly (*halt 2*, "— HALT", "the ONE owner halt"). Prose is
hard-wrapped near 90 characters.
