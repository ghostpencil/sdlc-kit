# SDLC Setup

Bootstrap the Agentic SDLC (phases → slices → TDD, owner halt points, the gate) into
this project. Two modes: **New Project** (interview → scaffold) and **Existing Project**
(analyze → propose → confirm → generate). Kit reference: the `sdlc-kit/` folder
(README, `templates/`, `reference/GATE_RECIPES.md`, `reference/SKILLS.md`).

Prime directive: **never fill a gap with an assumption, and never overwrite what
exists.** Every unclear choice becomes a question to the owner; every collision with an
existing file becomes a shown merge plan, not a silent clobber.

## How to use

`/sdlc-setup` — auto-detects the mode and confirms it. Force with `/sdlc-setup new` or
`/sdlc-setup existing`. Optional kit path if `sdlc-kit/` is not at the repo root:
`/sdlc-setup existing ../sdlc-kit`.

## Workflow

### 1. Preflight (both modes)

1. Locate the kit folder; halt if its `templates/`, `skills/`, and `reference/` are
   missing. Read `sdlc-kit/VERSION` — this resolves `{{KIT_VERSION}}`, and today's date
   resolves `{{ADOPTION_DATE}}`. If `VERSION` is absent the kit predates version
   stamping: record `{{KIT_VERSION}}` as `unknown (pre-0.2.0)` rather than guessing.
2. **Verify skills** (see `reference/SKILLS.md`): the TDD skill is NOT built into
   Claude Code — it is vendored in `sdlc-kit/skills/` and installed in step 2a/2b
   below; HALT if `sdlc-kit/skills/tdd.md` is missing. The built-in `code-review`
   skill must appear in the available-skills listing — if missing, tell the owner to
   update Claude Code; do not improvise a substitute. Check for the
   `pr-review-toolkit` plugin; if absent, tell the owner to run
   `/plugin install pr-review-toolkit@claude-plugins-official` (setup can continue —
   it is needed by `/end-phase`, not today).
3. `git status` / `git rev-parse`. Not a git repo → note that New mode will `git init`.
   Dirty working tree in an existing repo → ask the owner to commit/stash first.
4. Detect the mode: no source files beyond scaffolding/docs → **New Project**;
   otherwise **Existing Project**. Confirm the detection with the owner in the same
   question round as step 2's findings (AskUserQuestion). A forced-mode argument skips
   only the detection, not the confirmation of anything else.

### 2a. New Project mode — interview, then scaffold

Interview in rounds (AskUserQuestion, ≤4 questions per round; prefer concrete options
with trade-offs). Later rounds depend on earlier answers — do not front-load one giant
questionnaire.

- **Round 1 — identity:** project name + one-line purpose; language + minimum version;
  application type (CLI / web service / GUI / library / other); main branch name
  (default `main`).
- **Round 2 — toolchain** (offer the language's conventional defaults from
  `reference/GATE_RECIPES.md` as the recommended option): linter, type checker (or
  compile step, or none), test framework, package/build manager, formatter.
- **Round 3 — process fit:** does this process govern the whole repo, or a subset — and
  what is explicitly out of scope (default: the whole repo; mixed repos — app + docs,
  app + infra — name the boundary); how the owner will run the app for acceptance
  review (the run command); CI provider (default GitHub Actions); any always-active
  rules for CLAUDE.md (portability, serialization, DI seams for external services);
  anything the owner already knows about Phase 1 (recorded for `/plan-phase`, not
  acted on now).

  **Do not ask for a coverage floor and do not propose a number.** No CI run exists yet,
  so any figure would be invented. Record `coverage floor: TBD from first CI run` and
  follow the procedure in `reference/GATE_RECIPES.md`.

Keep interviewing until a round surfaces nothing new. Then scaffold, in order:

1. `git init` (if needed) + language scaffolding: package manifest, `src`/package dir,
   tests dir, tool configs (linter/typechecker/test runner), `.gitignore`.
2. **Establish the gate green on the walking skeleton:** one trivial module + one real
   test; run lint + typecheck + tests per `GATE_RECIPES.md`. Do not proceed red.
3. Instantiate templates (resolve every `{{PLACEHOLDER}}`): `CLAUDE.md`,
   `spec/SDLC.md`, `spec/PROJECT_INDEX.md` (status: PRE-PHASE-1), `spec/TESTING.md`
   (layer strategy + mandatory-mock table for THIS stack). `{{GATE_BASELINE}}` is
   `green — 0 lint / 0 type / 0 test failures (established <date> on the walking
   skeleton)`, which step 2 just proved. Never write a baseline you have not measured.
4. Install commands and skills into `.claude/commands/` (project-scoped, so the team
   inherits them via git):
   - the kit's `plan-phase.md`, `next-slice.md`, `end-slice.md`, `end-phase.md`
     (and this file);
   - the TDD skill set from `sdlc-kit/skills/`: `tdd.md` + `tdd-references/`
     (always), `tdd-guide.md` + `mutation-testing.md` (offer), `python-pro.md` +
     `hypothesis-tests.md` (Python projects only — offer). Preserve the
     `tdd-references/` subfolder; `tdd.md` links into it relatively.
   - If a same-named skill already exists on this machine in `~/.claude/commands/`,
     note that the project copy and user copy will both be listed; recommend the
     owner keep the project copy authoritative (it is versioned with the repo).
5. Install the edit-time hook: instantiate `settings.template.json` →
   `.claude/settings.json` using the hook recipe for the language; verify by editing a
   scratch source file with a deliberate lint error and confirming the hook blocks.
6. Offer to scaffold CI (a workflow running the same gate). Report coverage; do not
   enforce a floor yet — the floor is set from the first green CI run
   (`reference/GATE_RECIPES.md`).

### 2b. Existing Project mode — analyze, then propose, then generate

1. **Analyze before asking.** Survey the repo (spawn an Explore agent for large ones):
   languages + versions; build system; how tests are actually run (CI config is the
   best witness); lint/typecheck config present or absent; existing CLAUDE.md /
   README / docs / ADRs; branch + PR conventions from `git log`; app entry point / run
   command; test layout and any existing mocking conventions; whether the repo holds
   more than the app (docs site, infra, data pipelines — anything the process might
   not govern).
2. **Present findings + proposal — the feedback halt.** Show: detected stack, proposed
   gate commands (prefer what CI already runs), proposed hook, spec set to generate,
   and how existing docs will be treated (merge plan for an existing CLAUDE.md —
   preserve-and-extend, shown as a diff before writing). Interview in rounds for what
   analysis could not determine: whether this process governs the whole repo or a
   subset, and what is explicitly out of scope (step 1's survey of what else the repo
   holds seeds this question); acceptance-review surface and run command, in-flight
   work (open branches/PRs to record in START HERE), known trouble spots for the
   backlog, always-active rules worth encoding. If CI already enforces a coverage floor,
   record the existing number as-is; if it does not, record
   `coverage floor: TBD from first CI run` and do not propose one.
3. **Generate** (same placeholder-resolution rules as New mode):
   - `CLAUDE.md` — merge, never replace; existing instructions win on conflict and
     conflicts are surfaced to the owner.
   - `spec/SDLC.md`, `spec/TESTING.md` — document the conventions the project
     *actually* follows today (test layout, real mock seams), not aspirations.
   - `spec/PROJECT_INDEX.md` — seeded with reality: current status, a few Phase
     History rows from git history (pre-SDLC is fine), in-flight work in START HERE,
     known issues in the backlog.
   - Commands and the vendored TDD skill set into `.claude/commands/` (same rules as
     New mode step 4); hook into `.claude/settings.json` (merge with any existing
     hooks).
4. **Baseline the gate honestly.** Run it, then resolve `{{GATE_BASELINE}}` in
   `spec/SDLC.md` with what you measured — this is the placeholder step 3 could not fill,
   because the measurement did not exist yet. Leave it unresolved until now rather than
   guessing; the close-out `{{` check in step 3.1 is what catches you forgetting.
   - Green → `green — 0 lint / 0 type / 0 test failures (measured <date>)`.
   - Red → do NOT block setup and do NOT fix code now. Record the exact counts
     (`N lint / N type / N test failures (measured <date>)`) as the baseline in
     `spec/SDLC.md`, mirror them in PROJECT_INDEX, and set status STABILIZATION. The
     surrounding template text already says an increase is a regression — do not restate
     it, and do not edit any command file to match these numbers. Commands read the
     baseline from `spec/SDLC.md`; that is the whole point of recording it there.

   If the local runtime differs from CI's, record "CI is authoritative" (and why) in
   Environment gotchas — and treat the disagreement itself as worth understanding, not
   as a number to split the difference on.

### 3. Close-out (both modes)

1. Exit check: `grep -r '{{' CLAUDE.md spec/ .claude/` → must be empty. Re-run the
   gate one final time (New mode: must be green).
2. Ask the owner: commit the setup? If yes — New mode: initial commit; Existing mode:
   a `chore/adopt-sdlc` branch and a normal PR (the team should see this land like any
   change). Never commit without asking.
3. Report: what was generated, skill/plugin verification results, gate baseline, and
   the handoff — **`/clear`, then `/plan-phase`** (New, or Existing with a green gate)
   or **`/clear`, then `/next-slice`** on the STABILIZATION backlog (Existing, red
   gate). Point the team at the onboarding checklist in `sdlc-kit/reference/SKILLS.md`,
   and at the kit's home repo (<https://github.com/ghostpencil/sdlc-kit>) for the full
   process overview.

## Notes

- The kit folder itself need not stay in the target repo once setup is done — the
  installed files are self-sufficient. Keeping it (or a pointer to its home repo) helps
  future re-setup; owner's call, default keep.
- If the repo already has a partial SDLC install (some commands, older specs), treat it
  as Existing mode with the installed files as "existing docs": diff, merge, upgrade —
  never duplicate.
- Multi-language monorepos: one gate that runs every language's checks; hook matches
  the union of source globs. If that gets slow, scope the hook to the fast checks and
  keep the gate complete.
