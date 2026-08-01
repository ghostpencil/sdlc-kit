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

1. Locate the kit folder; halt if its `templates/`, `skills/`, `agents/`, and
   `reference/` are missing. Read `sdlc-kit/VERSION` — this resolves `{{KIT_VERSION}}`, and today's date
   resolves `{{ADOPTION_DATE}}`. If `VERSION` is absent the kit predates version
   stamping: record `{{KIT_VERSION}}` as `unknown (pre-0.2.0)` rather than guessing.
2. **Verify skills** (see `reference/SKILLS.md`): the TDD skill is NOT built into
   Claude Code — it is vendored in `sdlc-kit/skills/` and installed in step 2a/2b
   below; HALT if `sdlc-kit/skills/tdd.md` is missing. Check for the
   `pr-review-toolkit` plugin; if absent, tell the owner to run
   `/plugin install pr-review-toolkit@claude-plugins-official` (setup can continue,
   but the plugin is needed by both `/end-slice` — its per-slice reviewer is the
   `pr-review-toolkit:code-reviewer` agent — and `/end-phase`, so it must be installed
   before the first slice closes, not just before the first phase does).
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
  review (the run command — and how to stop it, if Ctrl+C or closing the window does
  not suffice — **verified in the owner's own shell**, see below); how a merged phase
  reaches users — the deploy procedure, or "none" for
  a library/local tool, and for a deploying project also how a deploy is **verified**:
  where the platform exposes the deployed commit (the deploy run's SHA, a dashboard
  field) and the URL or command for a post-deploy smoke check (all of it resolves
  `{{DEPLOY_NOTE}}` in `spec/SDLC.md`'s phase-end step, which asks the deploy question
  and records its verified outcome at every phase close); CI provider (default GitHub
  Actions); any always-active
  rules for CLAUDE.md (portability, serialization, DI seams for external services);
  the **model policy** (see below); anything the owner already knows about Phase 1
  (recorded for `/plan-phase`, not acted on now).

  **The model-policy poll.** Present this three-tier recommendation as the default and
  ask the owner to confirm or adjust (aliases only, never model IDs — IDs go stale):

  | Tier | Alias | Used for |
  |---|---|---|
  | High | `opus` | planning, analysis, adversarial review |
  | Medium | `sonnet` | writing code to an existing plan/spec |
  | Low | `haiku` | mechanical collection — hard-coded on the kit's read-only agents |

  Record the confirmed policy as `{{MODEL_POLICY}}` (*Model policy* section of
  `spec/SDLC.md`). Then ask whether to pin a session default: if yes, resolve
  `{{DEFAULT_MODEL}}` in `.claude/settings.json` (`"model"` key) with the chosen
  alias; if the owner keeps the harness default, **delete that line** from the
  instantiated settings rather than inventing a value. Never write a model into any
  installed command file — the poll lands in project-owned files only.

  **The owner's shell — verify the run command there, not here.** Anything the *owner*
  will execute has to work in the owner's terminal, which is not the shell this session
  runs commands in: different `PATH`, a shell profile no agent tool-shell loads, and
  often a different interpreter of the same name. Ask the owner to run the acceptance
  command themselves now and paste what happened, plus the resolver for the toolchain
  it uses (`which <tool>` / `(Get-Command <tool>).Source`, or the language's
  equivalent). If it fails, fix the command against **their** result — never against a
  run of your own — before it becomes `{{RUN_COMMAND}}`. Record the resolved path in
  PROJECT_INDEX's Environment gotchas when it differs from the bare name, because the
  next session will otherwise verify it in the wrong environment too. A command an
  agent verifies and an owner executes has two environments, and only the owner's is
  authoritative: one adoption shipped a documented run command that died at import for
  the owner and passed cleanly for every agent, and four phases of green gates said
  nothing.

  **Do not ask for a coverage floor and do not propose a number.** No CI run exists yet,
  so any figure would be invented. Resolve `{{COVERAGE_FLOOR}}` (gate section of
  `spec/SDLC.md`) as `TBD from first CI run` and follow the procedure in
  `reference/GATE_RECIPES.md`.

Keep interviewing until a round surfaces nothing new. Then scaffold, in order:

1. `git init` (if needed) + language scaffolding: package manifest, `src`/package dir,
   tests dir, tool configs (linter/typechecker/test runner/formatter), `.gitignore`,
   and a `.gitattributes` that pins `* text=auto eol=lf` — the kit ships every text
   file as LF, and on a checkout with no eol policy (Windows, `core.autocrlf`) every
   later kit update reports a page of phantom-modified files, which is the noise a
   real deletion hides in. The repo-wide pin is the kit repo's own choice and covers
   the kit's non-markdown files (`LICENSE`, `VERSION`, `MANIFEST.sha256`, JSON) that a
   `*.md`-only pin was measured to miss; a project that must keep CRLF for some path
   carves the exception (`*.bat text eol=crlf`) rather than dropping the default.
2. **Establish the gate green on the walking skeleton:** one trivial module + one real
   test; run lint + typecheck + tests per `GATE_RECIPES.md`. Do not proceed red.
3. Instantiate templates (resolve every `{{PLACEHOLDER}}`): `CLAUDE.md`,
   `spec/SDLC.md`, `spec/PROJECT_INDEX.md` (status: PRE-PHASE-1), `spec/TESTING.md`
   (layer strategy + mandatory-mock table for THIS stack; leave
   `{{ISOLATION_HARNESS}}` for step 4, which authors what it describes).
   `{{GATE_BASELINE}}` is `green — 0 lint / 0 type / 0 test failures (established
   <date> on the walking skeleton)`, which step 2 just proved. Never write a baseline
   you have not measured.
4. **Author and prove the test-isolation harness.** `spec/TESTING.md` §Test Isolation
   specifies the checks; implement them for this stack in the test harness: outbound
   network blocked, credential env vars cleared and credential paths pointed at
   nonexistent files, every home/data-dir seam isolated. Then **prove each check by
   its negative case**: add a deliberate violation (a real outbound call; a read of a
   real credential path), confirm the suite fails loudly naming what was attempted,
   remove the violation, confirm green. Resolve `{{ISOLATION_HARNESS}}` with where the
   harness lives and each recorded proof. An unproven blocker is partial isolation
   that reads as complete — the proof step is not optional.
5. Install commands and skills into `.claude/commands/` (project-scoped, so the team
   inherits them via git):
   - the kit's `plan-phase.md`, `next-slice.md`, `end-slice.md`, `end-phase.md`,
     `sdlc-retro.md`, `sdlc-update.md` (and this file);
   - the TDD skill set from `sdlc-kit/skills/`: `tdd.md` + `tdd-references/` +
     `mutation-testing.md` (always — `/end-slice`'s mutation-check step invokes it, so
     it is not optional), `tdd-guide.md` (offer), `python-pro.md` +
     `hypothesis-tests.md` (Python projects only — offer). Preserve the
     `tdd-references/` subfolder; `tdd.md` links into it relatively.
   - `reference/REVIEW_LENSES.md` → `.claude/commands/REVIEW_LENSES.md` (always) —
     `end-slice.md` §3 points at that installed path, so skipping this breaks the
     pointer. The rest of `reference/` stays uninstalled.
   - If a same-named skill already exists on this machine in `~/.claude/commands/`,
     note that the project copy and user copy will both be listed; recommend the
     owner keep the project copy authoritative (it is versioned with the repo).
   Then install the kit's agent definitions from `sdlc-kit/agents/` into
   `.claude/agents/` (project-scoped, inherited on clone the same way): currently
   `sdlc-surveyor.md`, the read-only mechanical-collection agent `/plan-phase` names.
   Its `model: haiku` is kit-set and stays — no project has a reason to burn a bigger
   model on file search; everything else about models is the owner's poll above.
6. Install the edit-time hook: instantiate `settings.template.json` →
   `.claude/settings.json` using the hook recipe for the language; verify by editing a
   scratch source file with a deliberate lint error and confirming the hook blocks.
7. Offer to scaffold CI (a workflow running the same gate). Report coverage; do not
   enforce a floor yet — the floor is set from the first green CI run
   (`reference/GATE_RECIPES.md`).

### 2b. Existing Project mode — analyze, then propose, then generate

1. **Analyze before asking.** Survey the repo — for large ones, fan the survey out to
   parallel read-only subagents (the same pattern `/plan-phase` uses for its sweeps:
   read-only by tool restriction, findings return here, every owner question stays in
   this session; the built-in Explore type serves, since the kit's own surveyor agent
   is not installed yet at this point). Collect:
   languages + versions; build system; how tests are actually run (CI config is the
   best witness); lint/typecheck config present or absent; existing CLAUDE.md /
   README / docs / ADRs; branch + PR conventions from `git log`; app entry point / run
   command; how the app is deployed, if it is (CD workflows, hosting config,
   Dockerfiles); any security scanning CI already runs (dependency audit, secret
   scanning, static analysis — the proposed gate folds these in per
   `reference/GATE_RECIPES.md`); test layout and any existing mocking conventions; any existing
   test-isolation enforcement (network blockers, sanitized env vars) and the seams it
   misses; whether the repo holds more than the app (docs site, infra, data pipelines
   — anything the process might not govern); and whether any file named
   `PROJECT_INDEX.md`, `INDEX.md`, or `STATUS.md` already exists anywhere in the tree —
   the kit is about to make `spec/PROJECT_INDEX.md` the single source of truth, and a
   same-named neighbor is how a session ends up reading the wrong file. Same class of
   check as the leftover-`{{` exit grep.
2. **Present findings + proposal — the feedback halt.** Show: detected stack, proposed
   gate commands (prefer what CI already runs), proposed hook, whether `.gitattributes`
   defines an eol policy — if not, offer `* text=auto eol=lf` (recommended: one line
   that permanently removes the phantom-modified noise every kit update otherwise
   produces on an autocrlf checkout, including on the kit's non-markdown files, which
   a `*.md`-only pin was measured to miss); an owner wary of a repo-wide change can
   take the scoped fallback instead (`*.md text eol=lf` plus `sdlc-kit/** text eol=lf`
   if the kit folder stays) — the test-isolation
   harness to author or extend (`spec/TESTING.md` §Test Isolation — what step 1 found,
   what is missing), any name collision step 1 found with `spec/PROJECT_INDEX.md`
   (offer to rename the pre-existing file; if the owner keeps both names, record the
   disambiguation in PROJECT_INDEX's Environment gotchas — the command decides nothing
   here), spec set to generate, and how existing docs will be treated (merge plan for an existing CLAUDE.md —
   preserve-and-extend, shown as a diff before writing). Interview in rounds for what
   analysis could not determine: whether this process governs the whole repo or a
   subset, and what is explicitly out of scope (step 1's survey of what else the repo
   holds seeds this question); acceptance-review surface and run command (and stop
   command, if Ctrl+C does not suffice) — **verified in the owner's own shell, by the
   owner, per New mode Round 3's *The owner's shell*: they run it now and paste the
   result, and the resolved interpreter path goes in Environment gotchas.** An existing
   project makes this more likely to bite, not less: the run command already exists, so
   nothing prompts anyone to test it, and it has usually only ever been run by the owner
   or only ever by tooling — never both; how a merged phase reaches users — the deploy
   procedure, or "none", and for a deploying project also how a deploy is **verified**:
   where the platform exposes the deployed commit and the URL or command for a
   post-deploy smoke check (resolves `{{DEPLOY_NOTE}}` in `spec/SDLC.md`'s phase-end
   step; step 1's survey of CI/CD config seeds the proposed answer); in-flight
   work (open branches/PRs to record in START HERE), known trouble spots for the
   backlog, always-active rules worth encoding, and the **model policy** — same poll,
   same recording rules as New mode Round 3 (`{{MODEL_POLICY}}` in `spec/SDLC.md`;
   `{{DEFAULT_MODEL}}` in `.claude/settings.json` or the line deleted; never into a
   command file). If CI already enforces a coverage floor,
   resolve `{{COVERAGE_FLOOR}}` (gate section of `spec/SDLC.md`) with the existing
   number as-is; if it does not, resolve it as `TBD from first CI run` and do not
   propose one.
3. **Generate** (same placeholder-resolution rules as New mode):
   - `CLAUDE.md` — merge, never replace; existing instructions win on conflict and
     conflicts are surfaced to the owner.
   - `spec/SDLC.md`, `spec/TESTING.md` — document the conventions the project
     *actually* follows today (test layout, real mock seams), not aspirations.
   - The test-isolation harness (`spec/TESTING.md` §Test Isolation): author it — or
     extend what step 1 found — and prove each check by its negative case (deliberate
     violation → loud failure naming the attempt → remove → green). If the owner
     defers it, record the gap as a backlog item and resolve `{{ISOLATION_HARNESS}}`
     with what is actually enforced today — never describe enforcement that does not
     exist.
   - `spec/PROJECT_INDEX.md` — seeded with reality: current status, a few Phase
     History rows from git history (pre-SDLC is fine), in-flight work in START HERE,
     known issues in the backlog.
   - Commands, the vendored TDD skill set, and `reference/REVIEW_LENSES.md` into
     `.claude/commands/`, plus the agent definitions from `sdlc-kit/agents/` into
     `.claude/agents/` (same rules as New mode step 5); hook into
     `.claude/settings.json` (merge with any existing hooks), verified the same way as
     New mode step 6 — a deliberate lint error in a scratch source file must be
     blocked. An unverified hook is enforcement that reads as complete.
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

1. Exit check: `grep -r '{{' CLAUDE.md spec/ .claude/settings.json` → must be empty.
   The scope is exactly the files setup instantiates — a blanket `.claude/` grep would
   trip on the installed copy of this command, which legitimately names placeholders.
   Every other installed file is `{{`-free and stays that way. Re-run the gate one
   final time (New mode: must be green).
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
  future re-setup; owner's call, default keep. If it stays, tell the owner plainly:
  **`sdlc-kit/` is kit-owned and volatile** — `/sdlc-update` replaces it wholesale, so
  nothing project-authored may live there. Process notes, field reports, and anything
  else the project writes belong at a project-owned path (`spec/` is the usual home); a
  file parked in `sdlc-kit/` is one update away from silent deletion.
- If the repo already has a partial SDLC install (some commands, older specs), treat it
  as Existing mode with the installed files as "existing docs": diff, merge, upgrade —
  never duplicate.
- Multi-language monorepos: one gate that runs every language's checks; hook matches
  the union of source globs. If that gets slow, scope the hook to the fast checks and
  keep the gate complete.
