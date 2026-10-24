# The Agentic SDLC Kit

A reusable, language-agnostic software development lifecycle for AI-assisted development
with Claude Code. Extracted and generalized from the process battle-tested on the
Dungeon Daddy project (50+ phases shipped with it).

It works for any programming language and any type of application — CLI tools, web
services, GUI apps, libraries. The process is the constant; the tooling (linter, type
checker, test runner) is configured per project during setup. It runs on **Claude Code**
and **GitHub Copilot CLI**, and a project may use both.

Since that first extraction the kit has shipped 51 releases, nearly all shaped by real use:
three adopting projects (Python, Java/Spring Boot, TypeScript) have run it across both
CLIs, and eleven field reports from them sit at the root of this repo. The theme of that
work is in the next sections: the process no longer only *describes* the steps, it
*checks* them, and every check ships with proof that it can fail.

---

## The process in one paragraph

Work is organized as **phases → slices → TDD cycles**. A *phase* is one feature (one
branch, one spec, one PR). A *slice* is one coherent behavior, small enough for a single
fresh-context session, built test-first and committed before context is cleared. A *TDD
cycle* is one red–green–refactor step. The agent runs autonomously between five **owner
halt points** (phase scope, slice scope, design questions, acceptance review, merge
approval). Every slice must pass **the gate** — lint + typecheck + tests, all green —
before it is committed. A single file, `spec/PROJECT_INDEX.md`, is the source of truth
for status, so every fresh session can orient itself in seconds.

Full process: see `templates/SDLC.template.md` (becomes `spec/SDLC.md` in your project).

## Why it works (the short version for the team)

- **Context is a budget.** Sessions read only `CLAUDE.md` + `spec/PROJECT_INDEX.md` at
  start and load other specs on demand. Small context = sharper agent.
- **Fresh session per slice.** Long conversations degrade. Each slice starts clean and
  ends with everything recorded on disk, so nothing lives only in chat history.
- **TDD keeps the agent honest.** A failing test written first is a contract the agent
  can't quietly reinterpret. The vendored TDD skill teaches the loop, and the TDD guards
  watch it at edit time (below).
- **The gate is non-negotiable.** Lint + typecheck + tests green before every commit.
  A file-edit hook surfaces most failures at edit time, not at slice end.
- **You stay in charge at exactly five points.** Everything else runs without asking, so
  you're not rubber-stamping trivia — and the five halts are never skipped, so the agent
  never decides scope, design, or merges for you.
- **Specs are interrogated, not assumed.** `/plan-phase` interviews you and then
  adversarially attacks its own understanding before writing a build-ready spec.

## What the kit checks for you

Prose rules erode; the field reports showed it again and again. So the kit turns its
load-bearing steps into hooks and scripts that leave evidence, and keeps the prose for
judgement calls.

- **The gate at edit time.** A hook runs your lint, typecheck, or tests on the file just
  edited, so most failures surface while the agent is still in context.
- **TDD guards.** Hooks watch the editor tools: a production write with no failing test
  observed first is logged, or denied once you arm deny mode. A RED counts only when the
  test runner's own report shows the failure. Comment- and layout-only edits are exempt,
  decided by a parser rather than by a guess. The guards are a cooperative backstop, not
  a security boundary.
- **A close-out evidence record.** Every slice commit carries four lines: its RED
  evidence, the review's lens verdicts, the mutation check, and the verification result.
  A checker script fails loudly when one is missing or empty. It checks that the record
  exists, not that it is true, and that alone catches the steps that silently vanish.
- **Review lenses.** The kit's own reviewer applies focused lenses such as concurrency,
  untrusted input, and disposal. Each lens maps to the linter rules that cover its
  mechanical half in every language with a gate recipe.
- **A product contract.** `spec/PRODUCT_CONTRACT.md` states what the product currently
  does, as the owner ratified it. Each phase end checks that those behaviors still exist,
  so a later cleanup cannot delete one with every test green.
- **An SDLC state switch.** `/sdlc` shows whether the process is in force, and lets the
  owner or the agent pause the hooks for work that isn't the slice's. Every pause needs a
  reason and is logged with who asked, and `/sdlc-retro` reads that log.
- **Architecture impact, optional.** Where a project keeps an Understand Anything
  knowledge graph, each slice and each phase gets a picture of what its changes touched,
  and the graph refreshes itself at slice end.
- **A retro that feeds the kit.** `/sdlc-retro` turns a finished phase into lessons for
  the project and a field report for the kit. `/sdlc-update` brings an adopted project
  forward to a new release without overwriting what the project owns.

The kit holds itself to the same rule. Every control states how it is proven to fail,
and the scripts under `tools/` prove it: each one breaks the hooks on purpose and must
see its tests catch every mutation before a release ships.

---

## Quick start

### Prerequisites

- **An agent CLI** — **Claude Code** (CLI, desktop app, or IDE extension) or **GitHub
  Copilot CLI** (1.0.63 or newer, below which the gate hook's matcher may never fire).
  The kit is prompt files; both CLIs read them, and a project may adopt both.
- **git** — the target project must be a git repository; the process commits per slice
  and lands each phase as a PR.
- A **POSIX shell with `sha256sum`** for the verify and update scripts — standard on
  Linux, `shasum -a 256` on macOS, Git Bash on Windows (it ships with Git for Windows).
- **Either `python` or `node`**, for the edit-time hook only — it parses a JSON payload
  to find the file that was just edited, and ships both dialects so whichever you have
  is enough. This is the kit's one dependency beyond the agent CLI itself, it is
  unrelated to your project's language, and the hook reports loudly rather than passing
  quietly if it finds neither. What matters is that the interpreter is on the `PATH` of
  the shell **your CLI runs hooks in**, which is not always the shell you type in —
  setup measures that rather than assuming it.

### Both modes

1. Get the `sdlc-kit/` folder into the root of the target repository. It must keep that
   name — `/sdlc-setup` looks for it by name.

   **Download a release** (recommended — no git surgery, and the bundle is checksummed):

   ```bash
   cd /path/to/target-project
   curl -sL https://github.com/ghostpencil/sdlc-kit/releases/latest/download/sdlc-kit.tar.gz | tar -xz
   cd sdlc-kit && sha256sum -c MANIFEST.sha256 && cd ..   # verify; shasum -a 256 -c on macOS
   ```

   Releases: <https://github.com/ghostpencil/sdlc-kit/releases>. A specific version is
   `releases/download/vX.Y.Z/sdlc-kit.tar.gz` (releases up to v0.6.0 embed the version
   in the asset name instead: `sdlc-kit-<version>.tar.gz`).

   **Or clone this repo** and lift the kit folder out of it:

   ```bash
   cd /path/to/target-project
   git clone --depth 1 https://github.com/ghostpencil/sdlc-kit /tmp/sdlc-kit-src
   cp -r /tmp/sdlc-kit-src/sdlc-kit ./sdlc-kit    # the kit only — not the repo's own docs
   ```

   Either way you end up with plain files (not a nested git repo) that you commit
   alongside your project.
2. Put `sdlc-setup` where your CLI will find it. **This is the one file you install by
   hand** — setup installs the other seven commands itself, but it cannot install its own
   entry point.

   **Claude Code** — copy it into the target's `.claude/commands/`:

   ```bash
   mkdir -p .claude/commands && cp sdlc-kit/commands/sdlc-setup.md .claude/commands/
   ```

   **Copilot CLI** — it does not read `.claude/commands/`, and markdown slash commands
   do not exist there (`github/copilot-cli#618`), so the command ships as a skill: a
   frontmatter block, one blank line, then the kit file unchanged.

   ```bash
   mkdir -p .github/skills/sdlc-setup
   { printf -- '---\nname: sdlc-setup\ndescription: "Bootstrap the Agentic SDLC into this project."\n---\n\n'
     cat sdlc-kit/commands/sdlc-setup.md
   } > .github/skills/sdlc-setup/SKILL.md
   ```

   Keep the body byte-for-byte and the description quoted. `/sdlc-update` classifies
   these files by stripping the frontmatter and comparing the remainder against the
   manifest, so a tidy-up in the body makes an untouched command read as drifted — and
   an unquoted `: ` anywhere in the frontmatter makes Copilot drop the file silently.
   `sdlc-kit/reference/COPILOT.md` carries the mapping for every other file, which
   setup handles.
3. Open your CLI in the target repo and run **`/sdlc-setup`**. On Copilot, confirm
   `/skills` lists `sdlc-setup` under *Project skills* before you do — a frontmatter
   parse failure produces no error, and absence is the only symptom.

Setup auto-detects the mode and confirms it with you:

- **New Project mode** — an empty or nearly-empty repo. Setup interviews you (language,
  app type, tooling, test framework, run command…), scaffolds the toolchain and spec
  files from the templates, installs the commands and the edit-time gate hook, and
  leaves you ready to run `/plan-phase` for Phase 1.
- **Existing Project mode** — a repo with real code in it. Setup analyzes the codebase
  (language, build system, how tests actually run, CI, existing docs), proposes a gate
  and a spec set, and confirms everything with you before writing anything. Existing
  files are merged, never overwritten. It then baselines the gate honestly — a red gate
  becomes your initial STABILIZATION backlog, not a blocker.

Either way, setup **installs the required skills**. Neither the TDD skill nor the
reviewer is built into either CLI — the kit ships both in `skills/` and setup copies
them into the target project's `.claude/skills/`, so the whole team inherits them via
`git clone` with no per-machine step. Setup verifies the kit skills' source files and
installed copies; on Copilot CLI it also shows you what the kit loses there.
`pr-review-toolkit` is optional as of 0.14.0 — a deeper Claude-Code-only pass at phase
end, required by nothing. See `reference/SKILLS.md` and `reference/COPILOT.md`.

### After setup, the daily loop

| Command | When |
|---|---|
| `/plan-phase` | At a phase boundary — turn an idea into a build-ready spec |
| `/next-slice` | First command of every fresh session — orient, confirm scope, TDD |
| `/end-slice` | Slice done — gate, code review, commit, record, then `/clear` |
| `/end-phase` | Last slice done — gate, acceptance review, PR, review, merge |
| `/sdlc` | Any time — `status`, or `pause`/`resume`/`off` the kit's hooks for non-SDLC work (any caller, with a reason; who asked is logged) |

One slice per session. `/clear` after every `/end-slice`. That's the rhythm.

---

## What's in the kit

This repository is split in two: **`sdlc-kit/` is the product** — the only folder that
goes into your project — and everything at the root is documentation *about* the kit,
which you do not need to install.

```
sdlc-kit/                            ← THE KIT — copy this folder into your project
├── VERSION                          ← the kit version this bundle is
├── MANIFEST.sha256                  ← checksums of every file in the bundle
├── README.md                        ← install + verify, for people who only have the bundle
├── commands/                        ← installed into <project>/.claude/commands/ (Copilot: .github/skills/)
│   ├── sdlc-setup.md                ← the two-mode setup command (start here)
│   ├── plan-phase.md
│   ├── next-slice.md
│   ├── end-slice.md
│   ├── end-phase.md
│   ├── sdlc-retro.md                ← lessons-learned extraction at a phase boundary
│   ├── sdlc.md                      ← /sdlc: read or change the SDLC state the hooks obey
│   └── sdlc-update.md               ← brings an adopted project to a newer kit release
├── skills/                          ← skills → <project>/.claude/skills/ (both CLIs read it)
│   ├── tdd/                         ← THE TDD skill (not built into either CLI)
│   │   ├── SKILL.md
│   │   └── tdd-references/          ← tests.md + mocking.md (linked from SKILL.md)
│   ├── mutation-testing/            ← always installed — reference depth for /end-slice's mutation check
│   ├── diff-review/                 ← always installed — kit-written; the reviewer /end-slice
│   │                                   and /end-phase name (Spec + Standards axes, both CLIs)
│   ├── change-verify/               ← always installed — kit-written; the verification
│   │                                   /end-slice step 6 and /end-phase step 2 name
│   ├── python-pro/                  ← Python projects only
│   └── hypothesis-tests/            ← Python projects only
├── templates/                       ← instantiated into the project by /sdlc-setup
│   ├── SDLC.template.md             → spec/SDLC.md        (the canonical process)
│   ├── CLAUDE.template.md           → CLAUDE.md           (agent instructions)
│   ├── PROJECT_INDEX.template.md    → spec/PROJECT_INDEX.md (source of truth)
│   ├── TESTING.template.md          → spec/TESTING.md     (TDD + mock policy)
│   ├── PRODUCT_CONTRACT.template.md → spec/PRODUCT_CONTRACT.md (current-truth product
│   │                                   contract — seeds empty, placeholder-free)
│   ├── README.template.md           → README.md            (human entry point: what the
│   │                                   app is, how to run it, where the process docs
│   │                                   live; New mode when absent, offered in Existing)
│   ├── settings.template.json       → .claude/settings.json (Claude Code hook config: bare
│   │                                   launcher lines only — no "shell" keys, measured 2026-08-15)
│   ├── claude-gate.template.sh      → .github/hooks/sdlc-gate-claude.sh (edit-time gate hook,
│   │                                   Claude Code dialect: the logic, holding its placeholders)
│   ├── copilot-hook.template.sh     → .github/hooks/sdlc-gate.sh (the same hook, Copilot dialect:
│   │                                   the logic, holding every placeholder)
│   ├── copilot-hook.template.json   → .github/hooks/sdlc-gate.json (its bare launcher; no values)
│   ├── tdd-guard.template.sh        → .github/hooks/sdlc-tdd-guard.sh (optional: the observed-RED
│   │                                   write guard and the premature-stop guard, Copilot dialect)
│   ├── tdd-guard.template.json      → .github/hooks/sdlc-tdd-guard.json (their hook config; no values)
│   ├── tdd-guard-claude.template.py → .github/hooks/sdlc-tdd-guard.py (the same guards, Claude Code
│   │                                   dialect: event-split observation, shell-neutral launcher)
│   ├── skill-ledger.template.sh     → .github/hooks/sdlc-skill-ledger.sh (optional, logging-only:
│   │                                   the skill-activation ledger's body, both CLIs; no values)
│   ├── skill-ledger.template.json   → .github/hooks/sdlc-skill-ledger.json (its Copilot launcher;
│   │                                   no values)
│   ├── close-out.template.sh        → .github/hooks/sdlc-close-out.sh (both CLIs, always: the
│   │                                   close-out evidence checker /end-slice runs; no values)
│   ├── sdlc-impact.template.py      → .github/hooks/sdlc-impact.py (both CLIs, always: the
│   │                                   architecture-impact adapter; inert without an
│   │                                   Understand Anything graph; no values)
│   ├── sdlc-cosmetic.template.py    → .github/hooks/sdlc-cosmetic.py (both CLIs, always: the
│   │                                   comment/format-only classifier the TDD guards and
│   │                                   /end-slice ask — Python, TS/JS, Java, C#; no values)
│   ├── sdlc-state.template.py       → .github/hooks/sdlc-state.py (both CLIs, always: the
│   │                                   helper behind /sdlc and the daily commands' state
│   │                                   writes; a command step, never a hook; no values)
│   └── explore.agent.template.md    → .github/agents/explore.agent.md (Copilot only: read-only sweeps)
├── reference/                       ← consulted by /sdlc-setup
│   ├── GATE_RECIPES.md              ← gate + hook commands per language, both hook dialects
│   ├── COPILOT.md                   ← the Copilot CLI mapping: install paths, hook, detection
│   ├── SKILLS.md                    ← required/recommended skills and how to install
│   ├── UPDATE_NOTES.md              ← /sdlc-update's notes for 0.14.0–0.31.3 (read at update time)
│   └── REVIEW_LENSES.md             → <project>/.claude/commands/ (the one installed reference file)
├── THIRD_PARTY_NOTICES.md           ← attributions for the vendored skills (MIT; python-pro's
│                                       redistribution status unverified — the notices say so)
└── LICENSE                          ← MIT (must travel with the bundle)

.github/workflows/release.yml        ← packages the kit as a release asset on tag push
.github/ISSUE_TEMPLATE/bug-report.md   ← issue template: one quick finding
.github/ISSUE_TEMPLATE/field-report.md ← issue template: adoption findings, retro-shaped
.claude/commands/kit-check.md        ← /kit-check: kit self-check (development-only, never installed)
tools/gate-hook-check.py             ← proves the gate hooks (script + launcher) against measured payloads
tools/skill-ledger-check.py          ← proves the skill-activation ledger, both dialects
tools/tdd-guard-check.py             ← proves the TDD guards, then mutates them to prove the proof
tools/tdd-guard-claude-check.py      ← proves the Claude Code guard dialect the same two-pass way
tools/close-out-check.py             ← proves the close-out evidence checker, corpus + mutations
tools/impact-check.py                ← proves the architecture-impact adapter, cases + mutations
tools/sdlc-state-check.py            ← proves the SDLC state helper, every verb + mutations
tools/cosmetic-check.py              ← proves the cosmetic-edit classifier, corpus + mutations
                                       (TypeScript installs passed in with --ts; not vendored)
tools/shipped-lint-check.py          ← lints every shipped .py with stock ruff, + mutations
tools/rederive-check.py              ← proves /sdlc-update's hook re-derive helper, extracted
                                       from the command, cases + mutations
tools/impact-fixtures/               ← the IMPACT proof's seed pair, minimized from a real
                                       Understand Anything graph + overlay, a real scanner
                                       output for coverage, and the plugin's hooks.json
                                       verbatim for plugin-fix (SEED.md has provenance)
tools/cosmetic-prototypes/           ← COSMETIC's measurement prototypes (FEATURE_PLAN §82.8):
                                       the difftastic/ast probes, the TS/Java/C# comparators,
                                       fixtures — the seed for the build's cosmetic-check proof
.gitattributes                       ← pins LF — the manifest hashes depend on it (one
                                       verbatim CRLF fixture is exempt)
.gitignore
README.md                            ← you are here
CLAUDE.md                            ← instructions for agents working ON the kit
CHANGELOG.md                         ← kit version history
FIELD_REPORT.md                      ← findings from the first external adoption
FIELD_REPORT_2026-07-20.md           ← findings from the second arc — /sdlc-retro's first real run
FIELD_REPORT_2026-07-22.md           ← findings from the third arc — first full arc on kit 0.6.0
FIELD_REPORT_2026-08-01.md           ← findings from a 5th phase (sdlc-kit#1) — triaged in FEATURE_PLAN_HISTORY.md §12
FIELD_REPORT_2026-08-02.md           ← findings from the 6th phase (sdlc-kit#2) — triaged in FEATURE_PLAN_HISTORY.md §15
FIELD_REPORT_2026-08-15.md           ← whole-project review of ai-news-dashboard — triaged in FEATURE_PLAN.md §56
FIELD_REPORT_2026-08-17.md           ← findings from a 7th phase (sdlc-kit#7) — triaged in FEATURE_PLAN.md §63
FIELD_REPORT_2026-08-17b.md          ← ai-news-dashboard Phase 05 (sdlc-kit#8) — triaged in FEATURE_PLAN.md §63
FIELD_REPORT_2026-08-21.md           ← findings from an 8th phase (sdlc-kit#9) — triaged in FEATURE_PLAN.md §70
FIELD_REPORT_2026-09-01.md           ← findings from a 9th phase (sdlc-kit#10) — triaged in FEATURE_PLAN.md §76
FIELD_REPORT_2026-10-19.md           ← a third adopter's Phase 01 (sdlc-kit#17) — triaged in FEATURE_PLAN.md §84
CRITICAL_GAPS_ANALYSIS.md            ← external gap review at 0.7.0 — triaged in FEATURE_PLAN_HISTORY.md §11
IMPROVEMENT_PLAN.md                  ← what was done about them (closed at v0.3.0)
FEATURE_PLAN.md                      ← the live plan: standing decisions, clocks, active work
FEATURE_PLAN_HISTORY.md              ← its retired sections §1–§51, numbering preserved
KIT_INVARIANTS.md                    ← the invariant ledger /kit-check verifies
FEATURE_SPEC_IMPACT.md               ← owner's impact-visualization spec, ingested verbatim — triaged in FEATURE_PLAN.md §66
sdlc-kit-process-flow.md             ← the process walkthrough: setup, the four daily
                                        commands, the halts, and where the hook guards fire
LICENSE                              ← MIT
```

Paths written as `commands/…` or `templates/…` elsewhere in the docs are relative to
`sdlc-kit/`, which is also how they read once the folder is inside your project.

Templates use `{{PLACEHOLDER}}` markers; `/sdlc-setup` resolves every one of them with
you before finishing (and greps for leftover `{{` as its own exit check).

---

## Updating an adopted project

Adopting the kit copies files into your project. Later kit releases do not reach them on
their own — this is the procedure that brings them forward without destroying what your
project has recorded.

Setup installs this procedure as a command: run **`/sdlc-update`** in the adopted
project and it walks these same steps, halting once for drifted files. This section is
the human-readable statement of the same procedure — the command and this section must
agree, and a disagreement between them is a kit bug. Projects adopted before the command
existed follow this section by hand once; the update itself installs the command.

**Update at a phase/arc boundary, never with an arc in flight.** A mid-arc update
changes the rules governing slices already scoped, and which kit version governed which
slice becomes unreconstructable afterward. If one is truly unavoidable, record the
version change against the affected slices in `spec/PROJECT_INDEX.md`.

### Who owns what

The whole procedure rests on this split:

| Path in your project | Owner | Update behavior |
|---|---|---|
| `.claude/commands/*.md` (from `commands/` and `reference/REVIEW_LENSES.md` — and from `skills/` too on kits ≤ 0.13.0) | **kit** | Tracks upstream. Overwritten when provably unmodified; you decide when drifted. |
| `.claude/skills/*/SKILL.md` (+ `tdd/tdd-references/`, from `skills/`; this mapping starts at 0.14.0) | **kit** | Same rule — and copy skill **directories**, not lone files: the six `SKILL.md` files share a basename. Coming from ≤ 0.13.0 these are new files and their `.claude/commands/` originals are removed — one move, not two unrelated changes. |
| `.claude/agents/*.md` (from kits 0.6.0–0.9.0; the `agents/` mapping was retired in 0.10.0) | **kit** | Classified for the transition — removed when provably unmodified; you decide when drifted. |
| `.github/skills/*/SKILL.md`, `.github/agents/explore.agent.md` (Copilot CLI projects) | **kit** | Same rule. The packaged skills are compared with their frontmatter block stripped — see the script below. |
| `.github/hooks/sdlc-close-out.sh` (both CLIs, from 0.20.0: the close-out evidence checker) | **kit** | Same rule — compared against `templates/close-out.template.sh`, which it copies verbatim; one of the four kit-owned files in that directory (with `sdlc-impact.py`, `sdlc-cosmetic.py` and `sdlc-state.py`; a fifth, `sdlc-close-out.json`, is retired) — every other file there is project-owned. |
| `.github/hooks/sdlc-close-out.json` (Copilot, 0.22.0–0.37.1: the retired stop-time backstop's wiring — present only where accepted) | **kit** | Classified for the transition — compared against `templates/close-out-hook.template.json` in your old manifest and removed when provably unmodified; you decide when drifted. |
| `.github/hooks/sdlc-impact.py` (both CLIs, from 0.28.0: the architecture-impact adapter) | **kit** | Same rule — compared against `templates/sdlc-impact.template.py`, which it copies verbatim. Installed unconditionally and inert without an Understand Anything graph, so it is never offered or declined. |
| `.github/hooks/sdlc-cosmetic.py` (both CLIs, from 0.34.0: the cosmetic-edit classifier) | **kit** | Same rule — compared against `templates/sdlc-cosmetic.template.py`, which it copies verbatim. Installed unconditionally — it can only grant an exemption — so it is never offered or declined. |
| `.github/hooks/sdlc-state.py` (both CLIs, from 0.39.0: the SDLC state helper) | **kit** | Same rule — compared against `templates/sdlc-state.template.py`, which it copies verbatim. Installed unconditionally — it is a command step the hooks never run — so it is never offered or declined. |
| `CLAUDE.md`, `README.md` (where setup instantiated it — from 0.25.0), `spec/*.md`, `.claude/settings.json`, `.github/hooks/*.json` other than `sdlc-close-out.json`, `.github/hooks/sdlc-gate.sh`, `.github/hooks/sdlc-gate-claude.sh`, `.github/hooks/sdlc-tdd-guard.sh`, `.github/hooks/sdlc-tdd-guard.py`, `.github/hooks/sdlc-skill-ledger.sh` | **project** | **Never overwritten.** These hold your gate baseline, your own gate commands, your TDD-guard patterns, owner decisions, backlog, and gotchas. A fix to a hook script's template therefore reaches you only through `/sdlc-update`'s hook-script walk-through, which shows you the full diff and writes only on your yes — it cannot arrive silently; a spec-file change is handed to you as a diff to fold in. |
| `.github/copilot-instructions.md`, `AGENTS.md` | **project** | Never written, never overwritten, never removed. `/sdlc-setup` creates neither — if one is in your repo, you put it there. |

Which rows apply to your project is recorded, not guessed: `spec/PROJECT_INDEX.md` names
your agent CLI. A project set up for both holds the eight commands twice — once
user-typed under `.claude/commands/`, once packaged under `.github/skills/` — and both
copies update.

`templates/` and `reference/` are read only at `/sdlc-setup` time (and
`reference/UPDATE_NOTES.md` at `/sdlc-update` time, from the kit clone) and are never
re-applied to an already-adopted project — with six exceptions, all of which track
upstream like the commands: `reference/REVIEW_LENSES.md`, installed into
`.claude/commands/` (so `/end-slice`'s pointer to it resolves after the kit folder is
gone); on Copilot projects `templates/explore.agent.template.md`, which is copied verbatim
rather than instantiated because it carries no placeholders; from 0.20.0, on both CLIs,
`templates/close-out.template.sh`, copied verbatim to `.github/hooks/sdlc-close-out.sh`
for the same reason; and — from 0.28.0, on both CLIs —
`templates/sdlc-impact.template.py`, copied verbatim to `.github/hooks/sdlc-impact.py`;
and — from 0.34.0, on both CLIs — `templates/sdlc-cosmetic.template.py`, copied verbatim
to `.github/hooks/sdlc-cosmetic.py`; and — from 0.39.0, on both CLIs —
`templates/sdlc-state.template.py`, copied verbatim to `.github/hooks/sdlc-state.py`.
A kit release that changes only the non-installed
templates and reference docs is an adoption-only change — it affects new adoptions, not
yours, **with one standing exception**: a template change to a project-owned file you
instantiated reaches you only with your review — a hook script through the update's
walk-through, which offers to apply it and shows the full diff; a spec file as a diff
handed to you to fold in — and the per-version transition notes name each one.
`CHANGELOG.md` marks each entry accordingly.

### The procedure

1. **Find the version you are on.** `spec/SDLC.md` records it (*Kit version: X.Y.Z*).
   Projects adopted before 0.2.0 have no stamp; see *No version stamp* below.
   **And your agent CLI:** `spec/PROJECT_INDEX.md` records it (*Agent CLI:*), which
   decides which directories step 3 enumerates. Projects adopted before 0.14.0 have no
   such line — infer it from what the repo holds (`.claude/settings.json` versus the
   Copilot gate pair `.github/hooks/sdlc-gate.*` — the directory alone proves nothing
   from 0.20.0, when the both-CLIs `sdlc-close-out.sh` moves in), state the
   inference to the owner and have them confirm it, then
   write the line as part of this update, so the next one reads it instead of
   inferring. When the line is present, glance at the same evidence anyway: a
   recorded CLI the repo's own artifacts contradict is a finding for the owner
   before anything is copied, never a value to proceed on — every later step trusts
   this line.

2. **Get both versions of the kit.**

   ```bash
   git clone https://github.com/ghostpencil/sdlc-kit /tmp/kit
   git -C /tmp/kit worktree add /tmp/kit-old vX.Y.Z    # the version you are on
   ```

3. **Classify every installed file** against the manifest of the version you are *on* —
   not the new one. That is what makes the answer provable rather than hopeful.

   > **Hash committed content, not the working tree.** The kit stores text as LF, but if
   > your project does not pin line endings (`.gitattributes`) and you are on Windows,
   > your checkout holds CRLF. Hashing those files directly reports **every file as
   > drifted** — the check appears to work and is uniformly wrong. `git cat-file -p :path`
   > reads the committed bytes, which are LF on every platform. This applies only to files
   > inside your repo; a downloaded release archive is already LF and verifies with plain
   > `sha256sum -c MANIFEST.sha256`.

   ```bash
   cd /path/to/your-project
   MAN=/tmp/kit-old/sdlc-kit/MANIFEST.sha256

   for f in $(git ls-files .claude/commands .claude/skills .claude/agents \
                           .github/skills .github/agents \
                           .github/hooks/sdlc-close-out.sh \
                           .github/hooks/sdlc-close-out.json \
                           .github/hooks/sdlc-impact.py \
                           .github/hooks/sdlc-cosmetic.py \
                           .github/hooks/sdlc-state.py); do
     have=""
     case "$f" in
       .github/hooks/sdlc-close-out.sh)
         # one of the FOUR kit-owned files in .github/hooks/ — copied verbatim, no
         # project values. Their neighbors are project-owned and deliberately NOT in
         # the pathspec above: this loop must never classify the gate, guard, or ledger scripts.
         base=sdlc-close-out.sh
         want=$(awk '$2 == "templates/close-out.template.sh" {print $1}' "$MAN") ;;
       .github/hooks/sdlc-close-out.json)
         # the retired stop-time backstop's Copilot wiring (0.22.0-0.37.1), present
         # only where the offer was accepted; classified so it can be removed.
         base=sdlc-close-out.json
         want=$(awk '$2 == "templates/close-out-hook.template.json" {print $1}' "$MAN") ;;
       .github/hooks/sdlc-impact.py)
         # the second: the architecture-impact adapter (0.28.0), verbatim on both CLIs.
         # A project coming from a pre-0.28.0 kit has no such file yet — git ls-files
         # skips it and it arrives as a new install like any other.
         base=sdlc-impact.py
         want=$(awk '$2 == "templates/sdlc-impact.template.py" {print $1}' "$MAN") ;;
       .github/hooks/sdlc-cosmetic.py)
         # the third: the cosmetic-edit classifier (0.34.0), verbatim on both CLIs;
         # absent before 0.34.0, so it arrives as a new install the first time.
         base=sdlc-cosmetic.py
         want=$(awk '$2 == "templates/sdlc-cosmetic.template.py" {print $1}' "$MAN") ;;
       .github/hooks/sdlc-state.py)
         # the fourth: the SDLC state helper (0.39.0), verbatim on both CLIs;
         # absent before 0.39.0, so it arrives as a new install the first time.
         base=sdlc-state.py
         want=$(awk '$2 == "templates/sdlc-state.template.py" {print $1}' "$MAN") ;;
       .claude/skills/*)
         base=${f#.claude/skills/}
         # skills/ installs one directory per skill here from 0.14.0 on.
         want=$(awk -v b="$base" '$2 == "skills/" b {print $1}' "$MAN") ;;
       .claude/commands/*)
         base=${f#.claude/commands/}
         # commands/ and reference/REVIEW_LENSES.md install here — and skills/ did too
         # on kits <= 0.13.0, so that prefix stays for projects still on one.
         want=$(awk -v b="$base" \
           '$2 == "commands/" b || $2 == "skills/" b || $2 == "reference/" b {print $1}' "$MAN") ;;
       .claude/agents/*)
         base=${f#.claude/agents/}
         # agents/ installed into .claude/agents/ on kits 0.6.0–0.9.0; the mapping was
         # retired in 0.10.0, so these classify here for the removed-files step below.
         # (Against a pre-0.6.0 manifest they classify UNKNOWN — the denominator
         # below still counts them).
         want=$(awk -v b="$base" '$2 == "agents/" b {print $1}' "$MAN") ;;
       .github/skills/*/SKILL.md)
         # Copilot packaging: a frontmatter block, one blank line, then the kit command
         # verbatim. Strip the block and it must hash to commands/<name>.md.
         base=${f#.github/skills/}; base=${base%/SKILL.md}
         want=$(awk -v b="commands/$base.md" '$2 == b {print $1}' "$MAN")
         have=$(git cat-file -p ":$f" | awk \
           'NR==1 && $0=="---" {fm=1; next} fm && $0=="---" {fm=0; blank=1; next}
            fm {next} blank && $0=="" {blank=0; next} {blank=0; print}' |
           sha256sum | cut -d' ' -f1)
         base="$base (packaged skill)" ;;
       .github/agents/explore.agent.md)
         # copied verbatim from the template — it carries no placeholders.
         base=explore.agent.md
         want=$(awk '$2 == "templates/explore.agent.template.md" {print $1}' "$MAN") ;;
       *) base=$f; want="" ;;
     esac
     [ -n "$have" ] || have=$(git cat-file -p ":$f" | sha256sum | cut -d' ' -f1)
     if   [ -z "$want" ];        then echo "UNKNOWN   $base  (not from the kit — yours)"
     elif [ "$want" = "$have" ]; then echo "UNCHANGED $base  (safe to overwrite)"
     else                             echo "DRIFTED   $base  (review the diff — your call)"
     fi
   done
   ```

   Three traps worth knowing, because each produces a confident wrong answer rather
   than an error:

   - **Never write `git cat-file … | sha256sum` as the test of whether a path exists.** A
     pipeline reports the *last* command's status, so a missing path yields the hash of
     empty input and silently "matches" the wrong entry. Look the path up in the manifest,
     as above, rather than probing for it.
   - **Check the denominator.** The loop should report exactly as many files as
     `git ls-files` over the same pathspec list the loop walks (the five directories
     plus `.github/hooks/sdlc-close-out.sh`, `.github/hooks/sdlc-close-out.json`,
     `.github/hooks/sdlc-impact.py`, `.github/hooks/sdlc-cosmetic.py` and
     `.github/hooks/sdlc-state.py`).
     If it reports fewer,
     your prefix matching is dropping files — `tdd-references/` lives two directories
     down and is the usual casualty. A Copilot project counts files under `.github/`
     too, and a project set up for both counts the eight commands twice, once per copy.
   - **The frontmatter strip fails safe.** If it breaks it hashes nothing, which matches
     no manifest entry, so the file lands in `DRIFTED` in front of you rather than in
     `UNCHANGED` behind your back. Eight packaged skills all going `DRIFTED` at once
     means the strip, not eight edits.

4. **Act on the classification.**
   - `UNCHANGED` → provably untouched since adoption. Copy the new version over it.
     On a Copilot project the packaged skills (`.github/skills/<name>/SKILL.md`) are
     re-packaged, not copied: keep the existing frontmatter block and replace only the
     body below it with the new `commands/<name>.md`; `.github/agents/explore.agent.md`
     is the new template copied verbatim.
   - `DRIFTED` → you or setup edited it. Diff it against both versions and decide, file
     by file. **Never auto-overwrite a drifted file** — `spec/SDLC.md` explicitly invites
     you to fix a command that disagrees with it, so drift is often deliberate.
   - `UNKNOWN` → not a kit file. Leave it alone.

   Then list **every** live entry in `spec/PROJECT_INDEX.md` *Kit friction log* —
   `open`, or absorbed as `RULING OPEN` — beside the changelog entry in the update range
   that addresses it, or `nothing in range`. The log names no implicated file, so there
   is nothing to filter on; one adopter's two entries stayed `RULING OPEN` for seven
   weeks after the update that fixed them. A matched `RULING OPEN` entry is proposed for
   closure in step 6; an `open` one is left for the next retro.

   Then look for every process rule an earlier update missed. The command's step 4
   carries a table of marker phrases, one per rule `SDLC.template.md` gained from 0.15.0
   on; each absent from your `spec/SDLC.md` is put to you as a numbered decision: fold
   the rule now, or record it as reworded on purpose (`Fold marker answered:` in
   *Records*), so it is not asked again.

   Then read each optional hook's record against its artifact — the TDD guards and the
   skill ledger, for each CLI you run — on every update, not
   only the one that introduced it. A recorded decline is settled. No record line at all
   means you never had the choice, so the offer is made now, as setup would make it, with
   its proof. A record that disagrees with the files, either way round, is reported to
   you rather than fixed. The command's step 5 states the full check.

   Then copy in any files **new in the target version's install set**. Classification
   never saw them — it enumerates what your project already holds, and your project does
   not hold them yet — so they appear in no category above and are the one class of
   update a purely classification-driven pass silently skips. Take the install set from
   the new version's `sdlc-kit/commands/sdlc-setup.md` (New mode step 5 — plus step 6's
   kit-owned artifacts, `templates/close-out.template.sh` →
   `.github/hooks/sdlc-close-out.sh`, both CLIs; and, both CLIs, verbatim,
   `templates/sdlc-impact.template.py` → `.github/hooks/sdlc-impact.py` (from 0.28.0)
   `templates/sdlc-cosmetic.template.py` → `.github/hooks/sdlc-cosmetic.py` (from
   0.34.0) and `templates/sdlc-state.template.py` → `.github/hooks/sdlc-state.py` (from
   0.39.0); they live outside the step-5 table because they install beside the hooks).

   The symmetric case: files **removed from the target's install set** — listed in your
   old version's manifest under an install mapping but absent from the target's. An
   `UNCHANGED` one is provably the kit's and is deleted; a `DRIFTED` one is yours to
   keep (move it to a project-owned path outside the kit-managed directories) or delete.
   First instance: `agents/sdlc-surveyor.md` and the
   whole `agents/` → `.claude/agents/` mapping (0.6.0–0.9.0), retired in 0.10.0.

   The second instance is the 0.14.0 skills move, and it is a removal and a re-add of
   the same content: the five vendored skills leave `.claude/commands/<name>.md` and
   arrive at `.claude/skills/<name>/SKILL.md`. Both halves run in the same update. When
   it is done, check that no skill is left at both paths — two copies of `tdd` with
   different content is the one outcome to avoid.

   The third is 0.37.0's removal of the optional `tdd-guide/` skill. An unchanged copy
   is deleted; to keep one, move it out of `.claude/skills/` to a path your project
   owns.

   The fourth is 0.38.0's: the `change-simplify/` skill and, on a Copilot project that
   accepted the backstop, `.github/hooks/sdlc-close-out.json`. The Claude Code half of
   that release's change is in its note (`commands/sdlc-update.md`, step 5).

   Before copying anything, read the per-version *[installable]* transition notes in
   the update command itself (`commands/sdlc-update.md`, step 5 — and, for a version
   older than 0.32.0, `reference/UPDATE_NOTES.md`) for every version you are
   crossing — they carry what no classification can infer. The one with teeth: if
   your `spec/SDLC.md` predates the target's template, it still describes the old
   slice loop, and by its own first paragraph it **wins** over the updated commands —
   until you fold the template diff in, the file that outranks the new steps is the
   file disabling them.

   If you kept a `sdlc-kit/` folder from adoption, replace it with the new version's
   bundle — but **list its actual contents against the old version's manifest first**,
   and note both counts (N files on disk, M in the manifest), so an empty listing reads
   as the error it is rather than as a clean result.
   Anything in that folder the manifest does not list was put there by your project, and
   a wholesale replace deletes it silently — that is how one project lost its only local
   copy of an authored field report. Move any such file to a project-owned path (`spec/`
   is the usual home) before replacing. Left stale instead, the folder sits beside a
   re-stamped `spec/SDLC.md` claiming a version it does not hold.

   Replace **by copy-over-in-place, never by removing the directory**: delete only the
   files the old version's manifest lists, then `cp -r <new-kit>/. sdlc-kit/`. An
   `rm -rf sdlc-kit` can fail half-done on Windows (`Device or resource busy` after
   every file is already unlinked), and even where it works it opens a window in which
   your project holds no bundle at all if the copy then fails.

   When you present (or read) the update's plan, count files whose *committed content*
   actually changes separately from files merely touched — line-ending churn on an
   unpinned checkout can make two dozen files report modified when four differ. The
   short list is the one to read closely; the long one is the noise deletions hide in.

   **A project-owned file can still hold a kit defect.** Your gate hook, guards and
   ledger script hold *your* values, so no update may overwrite them, and a kit fix to
   one of them reaches you only by hand or through the walk-through below. The version
   notes say which releases carry such a fix and what it means; they are not restated
   here, because two copies of every note, each edited at every release, went stale at
   least once. Read them in the update command: step 5 of `commands/sdlc-update.md`
   for 0.32.0 onward, and `reference/UPDATE_NOTES.md` for 0.14.0 through 0.31.3.

   **Every project-owned hook script gets a walk-through, and an offer to apply it for
   you.** The five scripts instantiated from templates — `sdlc-gate.sh`,
   `sdlc-gate-claude.sh`, `sdlc-tdd-guard.sh`, `sdlc-tdd-guard.py`,
   `sdlc-skill-ledger.sh` — are yours, so a kit fix to one reaches you only this way, and
   the update does it for each one you have, whether or not a version note names it. It
   reads your values out of the installed file, finds the release the script was
   derived from (not always the version you are on: an earlier update may have offered
   a change you declined), and merges the new template into your file three ways, so
   your own local edits carry over; a value a version note offers to change goes in a
   second, target-only values file, so the merge applies it. It refuses a script with
   uncommitted changes, since a failed proof restores from `HEAD`. Then it walks you
   through it, one numbered decision per script: what changes in behavior, each local
   edit and whether it is carried, each merge conflict with both sides and a
   recommended resolution, what keeping the script costs, and the full diff of the file
   it would write. On your yes it writes that file, checks its syntax, runs the proof
   setup runs for it and records the catch, named, with its reach note; a failing proof
   puts the committed script back and reports. On your no it records the decline in
   `spec/SDLC.md`, one dated line per declined offer, so it is not re-asked until the
   template changes again; a later yes marks the line superseded. The command carries
   the helper script that does the reading and merging; it writes nothing in your tree
   until you say yes — its working files go under the git directory.

5. **Touch nothing project-owned.** Do not let an update rewrite `spec/SDLC.md`,
   `spec/PROJECT_INDEX.md`, `spec/PROJECT_INDEX_HISTORY.md`, `spec/TESTING.md`,
   `spec/PRODUCT_CONTRACT.md`,
   `CLAUDE.md`, `.claude/settings.json`,
   `.github/hooks/*.json` (other than the retired `sdlc-close-out.json`, which is
   kit-owned and removed),
   `.github/hooks/sdlc-gate.sh`, `.github/hooks/sdlc-gate-claude.sh`,
   `.github/hooks/sdlc-tdd-guard.sh`, `.github/hooks/sdlc-tdd-guard.py`, or
   `.github/hooks/sdlc-skill-ledger.sh`. They hold
   your recorded
   baseline, your gate commands, your TDD-guard patterns, and
   your decisions; the kit cannot regenerate them. The only exceptions are the
   writes named in step 6.
   And claim only what was checked: "nothing project-owned touched" may be said once
   the final diff has been read against the ownership table — not asserted from the
   manifest, which structurally cannot see files it never listed. An unverified
   reassurance is worse than silence, because it stops the reader looking.

6. **Verify, then re-record the version.** Re-run step 3 against the **new** version's
   manifest: every file you copied must now classify `UNCHANGED`, and the only `DRIFTED`
   entries are files you chose to keep. The two runs disagreeing about the copied files
   is what proves the classifier discriminates — an all-clear it could not fail to
   produce proves nothing. Then re-record the version in `spec/SDLC.md`
   (*Kit version: X.Y.Z*, dated), and — each only if it was missing — write the
   *Agent CLI:* line into `spec/PROJECT_INDEX.md` and the *Kit home repository:* line
   into `spec/SDLC.md`, the latter taken from the URL step 2 cloned the kit from.
   When the *Kit home repository* line is already present, compare it against the URL
   this update actually cloned — a mismatch goes to you as a finding, never a silent
   overwrite.
   Those lines are the only project-owned content
   an update writes, and the absent-only ones never overwrite an answer already there.
   More
   join them **only when this update actually put an offer to you** — the TDD-guard
   offer, the skill-ledger offer and each declined hook-script re-derive record your
   answer in `spec/SDLC.md`, a decline included, so no later update re-asks
   it — and an **accepted** offer also installs its artifacts (the guard pair, the
   ledger hook, a hook script re-derived at the walk-through, with its proof's record),
   each written only on your word at that halt. The empty `spec/PRODUCT_CONTRACT.md`
   the 0.23.0 note (`reference/UPDATE_NOTES.md`) creates is the
   other: a verbatim template copy, only when absent. An update that did not
   ask does not record an answer. And each `RULING OPEN` friction entry you confirm the
   release fixed — checked against the installed file — is flipped in place to
   `implemented in kit vX.Y.Z` (the release tag that shipped the fix); one you do not
   confirm stays as it is. Do these writes last, so an aborted update never
   claims a version it does not hold. From here
   every later update is mechanical.

7. **Land it as a normal PR** (`chore/update-sdlc-kit-X.Y.Z`) — the same way the adoption
   landed. Read `CHANGELOG.md` for the versions you skipped; entries marked
   *[installable]* are the ones that changed what you just copied.

### No version stamp (adopted before 0.2.0)

Manifests did not exist before 0.2.0, so there is no `MANIFEST.sha256` to compare against.
Hash the tag's contents directly instead — the result is exactly as provable, since the
manifest is only ever a cache of those same hashes.

Note that `v0.1.0` predates the repo restructure: its kit files live at `commands/` and
`skills/`, without the `sdlc-kit/` prefix that later versions use.

```bash
cd /path/to/your-project
KIT=/tmp/kit                       # a clone of the kit repo
OLD=v0.1.0                         # the version you believe you are on
PRE=""                             # use PRE=sdlc-kit/ for v0.2.0 and later

for f in $(git ls-files .claude/commands); do
  base=${f#.claude/commands/}
  want=""
  for cand in "${PRE}commands/$base" "${PRE}skills/$base" "${PRE}reference/$base"; do
    # -e tests existence and sets a real exit status; never probe with a pipeline.
    if git -C "$KIT" cat-file -e "$OLD:$cand" 2>/dev/null; then
      want=$(git -C "$KIT" cat-file -p "$OLD:$cand" | sha256sum | cut -d' ' -f1)
      break
    fi
  done
  have=$(git cat-file -p ":$f" | sha256sum | cut -d' ' -f1)
  if   [ -z "$want" ];        then echo "UNKNOWN   $base"
  elif [ "$want" = "$have" ]; then echo "UNCHANGED $base"
  else                             echo "DRIFTED   $base"
  fi
done
```

If every file matches a released version, you are provably on that version and step 3
applies unchanged from there. If they match nothing, treat every file as `DRIFTED` and
reconcile by hand — once. After this update you will have a version stamp and never need
this section again.

## Reporting problems and field reports

GitHub issues are the channel; two templates are provided:

- **Bug report** — one finding, quick to file: what happened, what you expected, and
  the kit file implicated.
- **Field report** — the gold-standard input: structured findings from a real adoption,
  in the shape `/sdlc-retro` produces at a phase boundary. If you ran the retro, its
  output already *is* the report — paste it in.

Either way, a finding is most useful when it names the kit file(s) that would have to
change and separates what was observed from what is suspected. That loop is how the kit
improves: every `FIELD_REPORT*.md` file at the repo root (the tree above lists them) is a
real report from an adopting project, and the fix batches in `CHANGELOG.md` were triaged
directly out of them.

## FAQ

**Does my project have to be a Python project?** No. The process is language-agnostic.
The gate commands are configured per project — `reference/GATE_RECIPES.md` has recipes
for Python, TypeScript/JavaScript, C#/.NET, Go, Java, and Rust, and the pattern extends
to anything with a linter and a test runner.

**Does the kit itself need Python installed?** It needs **either `python` or `node`** —
one of them, on the machine, for the edit-time hook only. The hook is handed its payload
as JSON and has to read a file path out of it, which needs a real parser; it ships both
dialects and picks whichever it finds at run time. Nearly every developer machine
already has one, and if yours has neither, the hook says so on every edit instead of
passing quietly. Nothing else in the kit needs either one, and this is independent of
what your project is written in. (Until 0.16.0 this answer read "No", which was wrong:
the hook has always shelled out to `python`.)

**What if my language has no type checker?** The gate's typecheck step is optional —
setup drops it (or substitutes a compile step) where it doesn't apply.

**Can I adopt this mid-flight on a messy codebase?** Yes — that's what Existing Project
mode is for. It documents reality (including a red gate) rather than pretending, and
starts you in STABILIZATION until the gate is green.

**Where do the skills come from?** Two provenances inside the kit, plus one optional
plugin. Six `skills/` files in four directories are **vendored** (third-party,
MIT-attributed — the TDD skill set, `tdd` with its two references,
mutation-testing, hypothesis-tests, and python-pro, whose license is
self-declared with no identified upstream, as `THIRD_PARTY_NOTICES.md` states rather
than settles; NOT part of either CLI); two are
**kit-written** (`diff-review`, `change-verify` — the review and verification passes
the close-out commands name). All six install
project-scoped so they travel with the repo. `pr-review-toolkit`
is an official plugin installed once per machine with one command, optional and
Claude Code only. Details in
`reference/SKILLS.md` — `/sdlc-setup` handles all of this.

**Do I have to use every part?** The load-bearing parts are: the gate, TDD-first
slices, fresh session per slice, and PROJECT_INDEX as the single source of truth. The
five halt points assume a single owner; for a team, map them onto your review process
(e.g. merge approval = normal PR review).
