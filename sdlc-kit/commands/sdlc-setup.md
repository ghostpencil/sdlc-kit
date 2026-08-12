# SDLC Setup

Bootstrap the Agentic SDLC (phases → slices → TDD, owner halt points, the gate) into
this project. Two modes: **New Project** (interview → scaffold) and **Existing Project**
(analyze → propose → confirm → generate). Kit reference: the `sdlc-kit/` folder
(README, `templates/`, `reference/GATE_RECIPES.md`, `reference/SKILLS.md`, and
`reference/COPILOT.md` when the target CLI is Copilot).

Prime directive: **never fill a gap with an assumption, and never overwrite what
exists.** Every unclear choice becomes a question to the owner; every collision with an
existing file becomes a shown merge plan, not a silent clobber.

## How to use

`/sdlc-setup` — auto-detects the mode and confirms it. Force with `/sdlc-setup new` or
`/sdlc-setup existing`. Optional kit path if `sdlc-kit/` is not at the repo root:
`/sdlc-setup existing ../sdlc-kit`.

## Workflow

### 1. Preflight (both modes)

1. Locate the kit folder; halt if its `templates/`, `skills/`, and
   `reference/` are missing. Read `sdlc-kit/VERSION` — this resolves `{{KIT_VERSION}}`, and today's date
   resolves `{{ADOPTION_DATE}}`. If `VERSION` is absent the kit predates version
   stamping: record `{{KIT_VERSION}}` as `unknown (pre-0.2.0)` rather than guessing.
   The kit README's opening names the kit's home repository URL — this resolves
   `{{KIT_HOME_REPO}}`; if that line is absent, the clone URL in the kit's
   `commands/sdlc-update.md` procedure states the same fact. Only when both are missing
   does this become a question for the owner — never guess a URL.
2. **Detect the target CLI** — which agent CLI this project's team will run the process
   in. It decides where commands, skills, and the gate hook are installed, and nothing
   downstream can be written until it is settled. `reference/COPILOT.md` holds the
   signal table and the full mapping; read it and follow it rather than reasoning about
   the signals here. Three rules bind this step:
   - **Signals are positive-only.** The absence of one CLI's marker is never evidence
     of the other — Copilot CLI stamps no session marker at all, so a Copilot project
     is detected from repo artifacts and `PATH`, or not at all.
   - **Detection sets the proposed answer, never the answer.** Unambiguous evidence →
     carry it into step 5's confirmation round as the default, one confirm, no new
     question. Conflicting or absent evidence → ask open-ended. The prime directive
     applies here like everywhere else.
   - **"Both" is a valid answer** and changes only install paths, never the process.
   If the answer includes Copilot, run `copilot --version` and compare it against the
   version floor in `reference/COPILOT.md`; an older CLI means the gate hook's matcher
   may never fire, so say that plainly now rather than installing a hook that cannot
   report anything. That run resolves in **this session's** shell — if the owner runs
   Copilot from a different shell or machine, have them run it there (the same
   two-environments rule as the run command below); step 6's live hook proof is the
   backstop either way.
   The confirmed answer resolves `{{TARGET_CLI}}` in `spec/PROJECT_INDEX.md`
   (`Claude Code` / `Copilot CLI` / `both`) — `/sdlc-update` reads it to know which
   directories are kit-owned in this project, so an unrecorded answer is one a later
   update has to guess at.
3. **Verify skills** (see `reference/SKILLS.md`): none of the TDD skill, the reviewer,
   or the two change passes is built into either CLI — all are in `sdlc-kit/skills/`
   and installed in step 2a/2b below. HALT if any of `sdlc-kit/skills/tdd/SKILL.md`,
   `sdlc-kit/skills/diff-review/SKILL.md`, `sdlc-kit/skills/change-simplify/SKILL.md`,
   or `sdlc-kit/skills/change-verify/SKILL.md` is missing; `/end-slice` and
   `/end-phase` name all four between them, so a missing copy is a process that cannot
   close a slice or a phase. `change-simplify` counts even though its step is optional
   — a step that may run needs the skill present in order to decide against it.
   On Copilot the built-ins the kit leans on are absent, each with its own consequence:
   show the owner *What the kit loses on Copilot today* from `reference/COPILOT.md` —
   that table is the answer, not a count repeated here — and let them decide knowing
   it. Do not describe a substitute the kit does not install. `pr-review-toolkit` is
   **optional** and Claude Code only; mention it as an available deepening at phase end
   if the owner is on that CLI, and do not make setup contingent on it.
4. `git status` / `git rev-parse`. Not a git repo → note that New mode will `git init`.
   Dirty working tree in an existing repo → ask the owner to commit/stash first.
5. Detect the mode: no source files beyond scaffolding/docs → **New Project**;
   otherwise **Existing Project**. Confirm the detection with the owner in the same
   question round as steps 2–3's findings (AskUserQuestion on Claude Code; plain
   chat where the CLI lacks it). A forced-mode argument
   skips only the mode detection, not the confirmation of anything else — the target
   CLI is confirmed in this round whether or not the mode was forced.

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
  review — the run command (and how to stop it, if Ctrl+C or closing the window does
  not suffice — **verified in the owner's own shell**, see below) and **what they will
  exercise** when it runs, which resolves `{{ACCEPTANCE_SURFACE}}`; how a merged phase
  reaches users — the deploy procedure, or "none" for
  a library/local tool, and for a deploying project also how a deploy is **verified**:
  where the platform exposes the deployed commit (the deploy run's SHA, a dashboard
  field) and the URL or command for a post-deploy smoke check (all of it resolves
  `{{DEPLOY_NOTE}}` in `spec/SDLC.md`'s phase-end step); CI provider (default GitHub
  Actions); any always-active
  rules for CLAUDE.md (portability, serialization, DI seams for external services);
  the **runtime conventions** — how the software logs and fails (see below); the
  **model policy** (see below); anything the owner already knows about Phase 1
  (recorded for `/plan-phase`, not acted on now).

  **The runtime-conventions ask.** Two questions, recorded as the *Runtime
  Conventions* section of `CLAUDE.md`: how the software **logs** — framework or
  mechanism, what each level means here, what may never be logged (secrets, PII) —
  resolving `{{LOGGING_CONVENTIONS}}`; and how it **fails** — fail fast or degrade,
  any error taxonomy or wrapping at boundaries, whether blind catches are ever
  acceptable and where — resolving `{{ERROR_CONVENTIONS}}`. Then propose the matching
  *Runtime-standards rules* from `reference/GATE_RECIPES.md` for the Round 2
  toolchain; adopted rules go into the linter config with the other tool configs at
  scaffold step 1, so the gate and hook enforce them from the first slice. Note in
  each conventions bullet which parts are mechanically enforced (rule IDs) and which
  are review-only, and include one adopted rule's violation in step 6's hook
  verification — a rule proposed and never seen to fire is configuration that reads
  as enforcement.

  **The model-policy poll.** The three tiers are the kit's vocabulary on either CLI;
  only the models filling them differ. Present this as the default and ask the owner to
  confirm or adjust (aliases only, never model IDs — IDs go stale):

  | Tier | Alias (Claude Code) | Used for |
  |---|---|---|
  | High | `opus` | planning, analysis, adversarial review |
  | Medium | `sonnet` | writing code to an existing plan/spec |
  | Low | `haiku` | mechanical collection — file search, enumeration, verbatim gathering |

  On Copilot CLI the alias column is **asked, not proposed**: the available models come
  from that CLI's own `/model` listing, so show the owner the listing and have them map
  the three tiers against it — each tier gets a named model from that listing, **or the
  owner ratifies `auto` for that tier, and the question itself states what `auto`
  forfeits**: on Copilot no installed file routes models (`reference/COPILOT.md`,
  *Models and tiers*), so under `auto` the process-heavy commands — `/plan-phase`,
  `/end-phase`, `/end-slice`'s review — may run below the work's tier, and a field run
  has already paid for that in manual mid-arc overrides. A dated record of the choice
  is not the fix — a record cannot show whether the consequence was understood; the
  question must carry it. Proposing names from memory is the same mistake as proposing
  gate commands the project does not run: the mapping must match an **informed**
  decision, or the mapping lies. Do not build the policy on per-agent model pinning —
  `COPILOT.md` records what is and is not verified about `model:` frontmatter there.

  Record the confirmed policy as `{{MODEL_POLICY}}` (*Model policy* section of
  `spec/SDLC.md`). On Copilot CLI the policy text is **operator-facing** — the
  template's comment states the shape: it names which commands run at which tier and
  the moment the routing is executed (set `/model` in-session, or `COPILOT_MODEL` for
  a scripted run, **before** a High-tier command), because a tier policy nobody
  executes is prose. Then ask whether to pin a session default: on Claude Code, if yes,
  resolve `{{DEFAULT_MODEL}}` in `.claude/settings.json` (`"model"` key) with the chosen
  alias, and if the owner keeps the harness default, **delete that line** from the
  instantiated settings rather than inventing a value. On Copilot there is no such
  settings key — the pin is `/model` per session or `COPILOT_MODEL` in the environment,
  so record which the owner chose in the policy text itself. Never write a model into
  any installed command file — the poll lands in project-owned files only.

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
   real deletion hides in. The repo-wide pin covers
   the kit's non-markdown files (`LICENSE`, `VERSION`, `MANIFEST.sha256`, JSON) that a
   `*.md`-only pin was measured to miss; a project that must keep CRLF for some path
   carves the exception (`*.bat text eol=crlf`) rather than dropping the default.
2. **Establish the gate green on the walking skeleton:** one trivial module + one real
   test; run lint + typecheck + tests per `GATE_RECIPES.md`. Do not proceed red.
3. Instantiate templates (resolve every `{{PLACEHOLDER}}`): `CLAUDE.md` (the
   spec-loading table's `{{EXTRA_SPEC_ROWS}}` resolves empty for a new project —
   delete the placeholder line), `spec/SDLC.md`, `spec/PROJECT_INDEX.md` (status:
   PRE-PHASE-1; START HERE points at `/plan-phase` for the first phase; Phase History
   has no rows yet and Notes starts `- (none)` — empty is a resolved value, stated,
   never a placeholder left behind), `spec/TESTING.md`
   (test layout — step 6's guard patterns derive from it — layer strategy,
   mandatory-mock table, and the integration-vs-unit boundary —
   where integration tests live and what they may touch — for THIS stack; leave
   `{{ISOLATION_HARNESS}}` for step 4, which authors what it describes).
   `{{HOOK_ENVIRONMENT}}`, `{{TDD_GUARD_NOTE}}`, `{{SKILL_LEDGER_NOTE}}`, and
   `{{CLOSE_OUT_CHECK_NOTE}}` are all left for step 6, which measures the first,
   decides the middle two, and proves the last.
   `{{GATE_BASELINE}}` is `green — 0 lint / 0 type / 0 test failures (established
   <date> on the walking skeleton, <this session's shell>)`, which step 2 just proved.
   The record names where it was measured, because a later session comparing against
   it needs to know whether it is comparing like with like. Never write a baseline
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
5. Install commands and skills — always project-scoped, so the team inherits them via
   git. **Where they go depends on the target CLI from preflight step 2**; this list is
   the definition, and `reference/COPILOT.md` carries the evidence and the reasoning
   behind the Copilot column.

   The seven kit commands are user-typed workflow entry points; the eight kit skills
   (five vendored, three kit-written) are model-invocable capabilities. They install
   to different places for that reason:

   | | Claude Code | Copilot CLI |
   |---|---|---|
   | the 7 commands | `.claude/commands/<name>.md` | `.github/skills/<name>/SKILL.md` |
   | the 8 skill directories | `.claude/skills/<name>/SKILL.md` | the same path — both CLIs read it |
   | `REVIEW_LENSES.md` | `.claude/commands/REVIEW_LENSES.md` | the same path — it is a document, not an executable |

   Packaging a command as a Copilot skill is mechanical, and the shape is **exact**: a
   `---` fenced block carrying `name` (the command's filename without `.md`) and
   `description` (one sentence, from the command's own opening paragraph), then one
   blank line, then the kit file byte-for-byte. Nothing else is inserted and nothing in
   the body is reworded — `/sdlc-update` classifies these files by stripping that block
   and comparing the remainder against the manifest, so a tidy-up at the top of the body
   makes an untouched command read as drifted. A project answering "both" gets both
   columns, and the seven commands are the only files that exist twice — deliberately
   not in a directory where Claude Code would list them as model-invocable skills. The
   list:
   - the kit's `plan-phase.md`, `next-slice.md`, `end-slice.md`, `end-phase.md`,
     `sdlc-retro.md`, `sdlc-update.md` (and this file);
   - the skill directories from `sdlc-kit/skills/`, each already a skill directory that
     is copied whole: `tdd/` (with its `tdd-references/` subfolder, which `SKILL.md`
     links into relatively), `mutation-testing/` (always — `/end-slice`'s mutation-check
     step invokes it, so it is not optional), `diff-review/` (always — `/end-slice`
     step 4 and `/end-phase` step 5 both name it, and it is the only reviewer that
     exists on both CLIs), `change-simplify/` (always — `/end-slice` step 3 names it;
     the step is optional, the skill is not, because a step that may run needs the
     skill present to decide against), and `change-verify/` (always — `/end-slice`
     step 6 and `/end-phase` step 2 name it); then `tdd-guide/` (offer), `python-pro/` +
     `hypothesis-tests/` (Python projects only — offer). Copy directories, not files:
     the eight `SKILL.md` files share a basename and only their parent directory tells
     them apart.
   - `reference/REVIEW_LENSES.md` → `.claude/commands/REVIEW_LENSES.md` (always) —
     `end-slice.md` §4 points at that installed path, so skipping this breaks the
     pointer. The rest of `reference/` stays uninstalled.
   - Copilot CLI only: `templates/explore.agent.template.md` →
     `.github/agents/explore.agent.md`, the read-only sweep profile the surveys in step
     2b and `/plan-phase` delegate to (Claude Code uses its built-in `Explore` instead,
     so nothing is installed there). It ships restricted to `read` and `search` and
     carries no model — add `model:` from the recorded policy only if the owner asks,
     and never a model name of your own choosing.
   - If a same-named skill already exists on this machine (`~/.claude/skills/`,
     `~/.claude/commands/`, or the Copilot personal directories), note that the project
     copy and user copy will both be listed; recommend the owner keep the project copy
     authoritative (it is versioned with the repo).
6. Install the edit-time hook, in the dialect the target CLI speaks — *Hook dialects*
   in `reference/GATE_RECIPES.md` names the templates, the destinations, and what
   differs.
   Claude Code: `settings.template.json` → `.claude/settings.json`. Copilot CLI, a
   pair: `copilot-hook.template.sh` → `.github/hooks/sdlc-gate.sh` (instantiated —
   every placeholder lives here) and `copilot-hook.template.json` →
   `.github/hooks/sdlc-gate.json` (the bare launcher — it takes no values; copy it
   verbatim and edit nothing but, later in this step, its `timeoutSec` number). The
   same
   `{{HOOK_*}}` values (plus `{{SOURCE_GLOB}}`) fill either dialect, and four of them are
   the dialect's own facts restated in prose — `{{HOOK_CONFIG_PATH}}` and
   `{{HOOK_FEEDBACK_NOTE}}` in `CLAUDE.md` and `spec/SDLC.md`, `{{HOOK_TOOLS}}` and
   `{{SOURCE_EXT}}` in `CLAUDE.md`'s hook sentence — so take all four from that table
   when step 3 instantiates
   those files, never invented at instantiation time. On Copilot, `{{HOOK_FEEDBACK_NOTE}}` must not claim the feedback blocks,
   and must carry the warning that a timed-out hook is reported as a pass.

   **Measure the hook's environment first** — *The hook environment* in
   `reference/GATE_RECIPES.md` carries the one-line probe and how to read it. A hook runs
   in the shell the CLI resolves, not the one you type in — and the answer is
   **per-launcher, not per-machine**: the hook shell follows the PATH of the shell the
   CLI was started from (measured: WSL bash from a PowerShell launch, Git Bash from a
   Git Bash launch, same repo, same day — and the WSL route additionally corrupts rich
   hook bodies). Run the probe from the CLI's own session, **launched the way this
   project's operator actually launches it** — a probe run from another launcher
   measures the wrong environment, and a team with two launch habits probes both. What it reports resolves `{{HOOK_ENVIRONMENT}}` in
   `spec/SDLC.md` — **which launcher the probe ran from**, which shell answered,
   **which JSON parser it offers (`python` or
   `node`; the hook needs one and picks it at run time)**, and whether the project's own
   lint command runs there. Record what that shell offered, not what the machine has
   installed: they are different questions, and only the first one governs the hook. Do
   not ask the owner which interpreter to use — a preference cannot answer a question
   about an environment neither of you is standing in. If the parser or the toolchain is
   unreachable there, say so plainly and do not leave a hook installed that reads as
   enforcement and checks nothing — that decision is the owner's to make knowingly, and
   `{{HOOK_ENVIRONMENT}}` is where they will read it back.
   **If no hook ends up installed, say so in `spec/SDLC.md` rather than leaving its
   sentence standing:** replace the edit-time-hook paragraph with that fact and its
   date, and resolve `{{HOOK_CONFIG_PATH}}` to name no file — the template's comment
   there says the same. `CLAUDE.md`'s hook sentence (the one carrying
   `{{HOOK_TOOLS}}`, `{{SOURCE_EXT}}`, and `{{HOOK_FEEDBACK_NOTE}}`) is replaced with
   the same fact — and so is the *Runtime Conventions* Enforcement sentence's "and
   the edit-time hook" clause, the third home of the claim, which carries no
   placeholder and so nothing else will flag: the three statements fall together; a
   CLAUDE.md describing a hook the project declined is the exact defect this branch
   exists to prevent, one file over. The canonical process file must never describe a check this
   project does not have; the gate then carries the whole load, and every slice close
   should know it.

   Then verify: edit a scratch source file with a deliberate lint error and confirm the
   hook reports it — blocking on Claude Code, as injected feedback on Copilot, and in a
   session launched the operator's way, since the hook shell is per-launcher. On
   Copilot, **time that run** and raise `timeoutSec` to at least 3× the measurement,
   recording the basis **and the launch route it was timed on** (a budget measured on
   the fast route is a budget for the wrong environment); a hook whose budget was never measured against a real run is
   a gate that goes quiet on the first cold typecheck. If nothing is reported at all,
   the matcher is the first suspect — `reference/COPILOT.md` has the discovery
   procedure.

   **Resolve `{{TDD_GUARD_NOTE}}` on every adoption.**
   The placeholder lives in `spec/SDLC.md`, which is instantiated on both CLIs, so a
   path that declines the offer below still has to fill it or the close-out `{{`
   check fires with nothing to write.

   **Then offer the TDD-ordering guards — both CLIs, per dialect, and optional.** *The
   TDD-ordering guards* in `reference/GATE_RECIPES.md` is the recipe for both
   dialects; `COPILOT.md` records the Copilot-side history. Put the choice to the
   owner with its trade-off stated: the guards make TDD ordering mechanical rather
   than advisory (deny a production write outside TDD's two licenses — an observed
   fresh red, or a declared behavior-preserving refactor edit behind a counted green;
   refuse a stop from a coding session that has no counted green or ended red), at
   the cost of the hook artifacts below and a guard that can be wrong about which
   commands are test runs. Default to offering, not to installing. If accepted:
   - Copilot CLI: `tdd-guard.template.sh` → `.github/hooks/sdlc-tdd-guard.sh` and
     `tdd-guard.template.json` → `.github/hooks/sdlc-tdd-guard.json`. The JSON takes no
     values — do not edit it.
   - Claude Code: `tdd-guard-claude.template.py` → `.github/hooks/sdlc-tdd-guard.py`,
     and the four `sdlc-tdd-guard.py` hook blocks already in the instantiated
     `.claude/settings.json` stay (PreToolUse `Edit|Write`, PostToolUse and
     PostToolUseFailure `Bash|PowerShell` — the shell tool's hook-visible name on
     Windows is `PowerShell`, measured 2026-08-12 — and Stop). Their command lines
     are shell-neutral `python` launchers on purpose: the default Windows hook shell
     is PowerShell, so nothing POSIX may live in a hook command. **If the guards are
     declined, or the project runs no Claude Code, REMOVE those four blocks** — the
     same two-state handling as the skill ledger's block, recorded the same way.
   - Both dialect scripts take `{{TEST_PATH_PATTERN}}`, `{{TEST_CMD_PATTERN}}` and
     `{{SOURCE_GLOB}}` — resolve them identically in both. **Do not ask for these cold and do not invent them from the
     language.** You already know the answers: the test framework came from Round 2, and
     the test layout is the one you are writing into `spec/TESTING.md` at step 3. Derive
     both patterns from those, show the owner the two literal patterns you resolved, and
     have them confirm — the recipe's per-language table is the starting point, the
     project's actual layout wins. A project whose layout no case-pattern can express is
     a finding to report, not a pattern to approximate.
   - They install in **logging mode** and stay there. Never create the
     `.git/sdlc-tdd/deny-enabled` flag during setup: deny is armed by the owner after
     reading a few sessions of `.git/sdlc-tdd/guard.log` and confirming the guard
     recognises the project's own test runs. A guard armed before that blocks every
     production write in the repo.
   - Prove them the way every other check is proven — by making them fail. In a scratch
     session **of each CLI a dialect was installed for** — the guards fire only from
     that CLI's hooks, and they execute in the hook shell the environment probe above
     measured, so a proof run anywhere else proves nothing about them —
     write a production file with no failing test first and confirm the log
     names it; then end a session with no green run and confirm the stop guard logs a
     would-block. An unproven guard is a file that reads as enforcement. If neither
     line appears, the guard is not firing: re-check the matcher and the hook
     environment above before adjusting anything else.
   - Record the outcome as `{{TDD_GUARD_NOTE}}` in `spec/SDLC.md`: installed or not,
     which CLI they run on, logging or deny mode, and the proof you just ran. **When
     installed, the note also states the three rules the guards impose on a coding
     session** — a test run registers only as a single bare command (no `;`, `&` or
     `|`; flags and single-test selectors are fine); the stop guard's green is
     any counted green, full-suite assurance being the end-slice gate's job; and a
     behavior-preserving edit (refactor, simplification, mutation testing — including
     a temporary mutation to prove a test of existing behavior bites, at any point in
     the cycle, not only at close-out)
     is licensed without a fresh red by declaring it, one line naming the step and
     move to `.git/sdlc-tdd/refactor-license`, valid only behind a counted green and
     revoked by the next test edit (*The TDD-ordering guards* in
     `reference/GATE_RECIPES.md` is the full recipe) — because the note is the
     proactive statement of them: the guard's own messages say them only reactively,
     at the refusal or counted run itself, and a session that meets them first as an
     unexplained refusal probes the guard instead of complying
     (field, 2026-08-08). The note also says the stop guard is **session-scoped**
     (owner-decided 2026-08-08): it binds only a session that wrote production code
     or edited a test, so a planning, docs, or bookkeeping session stops clean by
     construction. **Name the
     artifact that decides the mode** — the flag file `.git/sdlc-tdd/deny-enabled`,
     present means deny — and say in the same breath that arming or disarming deny means
     updating this line, because nothing else will. The note is written at the one moment
     it can only say "logging", and the ramp exists to change that later; a mode recorded
     without its flag file is a number in prose drifting from the thing that enforces it.
     State the other half too: `.git/` is **not** committed, so the flag, the state and
     the log live in one clone only. This line is repo-wide and is therefore a claim
     about the machine setup ran on — say whose, and let a teammate check their own. **A
     decline is recorded too, with the date — never delete the line.** `/sdlc-update`
     re-offers the guards to a project that never had the choice, and reads this to tell
     that apart from an owner who considered them and said no; deleting the record
     erases the difference and turns a decision into a recurring question. Never
     describe guards the project does not have. On a project answering **both** CLIs,
     the note must say the backstop covers the Copilot side only — an unqualified "TDD
     ordering is enforced" is false in half the sessions the team will run.

   **Then offer the skill-activation ledger — both CLIs, optional, logging-only.** *The
   skill-activation ledger* in `reference/GATE_RECIPES.md` is the recipe and carries the
   measured facts. Put the choice plainly: one hook appending one line per
   tool-dispatched skill activation to `.git/sdlc-skill-ledger.jsonl`, so
   `/sdlc-retro`'s step-evidence sweep reads which skills actually ran instead of
   trusting that presence meant activation (slash-typed commands dispatch no tool and
   leave no line — the recipe states the bound); the cost is one more hook and a
   per-clone log file. It never blocks anything.
   Default to offering, not to installing. If accepted:
   - Copilot side: `skill-ledger.template.json` → `.github/hooks/sdlc-skill-ledger.json`,
     copied verbatim — it takes no values; do not edit it.
   - Claude Code side: the `"Skill"`-matcher block already in the instantiated
     `.claude/settings.json` stays (Copilot-only adoptions have no such file and skip
     this bullet).
   - Prove it per the recipe: invoke any installed skill in a session of each installed
     CLI — launched the way this project's operator actually launches it — and read the
     ledger's last line back. No line → the hook is not firing; check
     the matcher spelling and the hook environment before trusting it.

   **On a decline, the artifacts must actually be absent**: do not write the Copilot
   ledger JSON, and remove the `"Skill"`-matcher block from the settings file you
   write — the record of the decline lives in the note below, never as dead config; a
   removed hook with an "installed" note, or the reverse, is exactly the contradiction
   `/sdlc-update` is told to report.

   **Resolve `{{SKILL_LEDGER_NOTE}}` on every adoption — accepted, declined, either
   CLI.** The placeholder lives in `spec/SDLC.md`, which is instantiated on every path,
   so a decline still has to fill it or the close-out `{{` check fires with nothing to
   write (this sentence sits outside the accepted-only list above for exactly that
   reason). Installed: which CLIs, **the hook artifact that makes it true** —
   `.github/hooks/sdlc-skill-ledger.json` on Copilot, the `"Skill"`-matcher block in
   `.claude/settings.json` on Claude Code — the ledger path, that `.git/` is
   per-clone so the ledger describes one machine, and that it records
   tool-dispatched activations only, so a missing line for a slash-invocable
   command is no signal either way. Say in the same breath that adding
   or removing the hook later means updating this line, because nothing else will. Declined: say so **with the date — never delete
   the line**. `/sdlc-update` reads it exactly as it reads the TDD-guard note: a
   recorded decline is settled; a missing line is a project that never had the choice.

   **Install the close-out evidence checker — both CLIs, always, not an offer.**
   `close-out.template.sh` → `.github/hooks/sdlc-close-out.sh`, copied verbatim — it
   takes no values (the record's four keys are fixed by the process); do not edit it.
   It is not a hook despite its address: `/end-slice`'s verify-the-record step runs
   it as a command step in the agent's shell, and it fails closed there on purpose.
   Prove it the way every other check is proven — by seeing it fail: run it against
   `HEAD` (`sh .github/hooks/sdlc-close-out.sh check` wherever `sh` resolves in the
   agent's shell — Claude Code's Bash tool does, measured 2026-08-10), and a pre-kit
   commit carries no record, so the proof is INCOMPLETE naming all four keys,
   exit 1. Two branches, neither assumed: a repo whose `HEAD` **does** carry a
   record (a re-adoption from kit ≥ 0.15.0 — the partial-install case in the Notes)
   proves against a commit predating the record instead, because a COMPLETE is the
   proof not failing; and a repo with **no commits yet** — every New-mode run, since
   `git init` is scaffold step 1 and the first commit is close-out step 2 — defers
   the proof to that step, where it is actually performed (close-out step 2 says
   so), and the note is finalized there, still inside setup.
   **On Copilot CLI the invocation itself is the thing to measure**: its shell tool
   is not the shell you type in, and measured 2026-08-10 **on Windows** it resolves
   no `sh` — while the `bash` on its PATH is WSL's, the route that corrupts hook
   bodies; never substitute it. There the working form derives sh from the git on
   its PATH — `bin\sh.exe` beside the `cmd` directory that holds `git.exe` — so
   resolve that literal path,
   run the proof through it **from a session of the CLI itself**, and record the
   exact form that ran (a non-Windows Copilot project measures its own answer —
   `sh` may simply resolve; the probe, not the platform lore, decides). Then
   resolve `{{CLOSE_OUT_CHECK_NOTE}}` in `spec/SDLC.md`:
   one invocation line per installed CLI, each one actually run against a real
   commit — a recorded invocation that was never run is exactly the silent absence
   the checker exists to catch, one layer up. The note is a claim about this
   machine and these CLIs: a teammate's clone re-proves before trusting it, and
   adding a CLI later means adding its proven line, because nothing else will.
7. Offer to scaffold CI (a workflow running the same gate). Report coverage; do not
   enforce a floor yet — the floor is set from the first green CI run
   (`reference/GATE_RECIPES.md`).

### 2b. Existing Project mode — analyze, then propose, then generate

1. **Analyze before asking.** Survey the repo — for large ones, fan the survey out to
   parallel read-only subagents (the same pattern `/plan-phase` uses for its sweeps:
   read-only by tool restriction, findings return here, every owner question stays in
   this session; Claude Code's built-in `Explore` type serves. On Copilot nothing is
   installed yet — the `explore` profile arrives at step 5, for `/plan-phase` and after
   — so this survey runs in this session, and serially if fan-out is unavailable rather
   than being trimmed to fit). Collect:
   languages + versions; build system; how tests are actually run (CI config is the
   best witness); lint/typecheck config present or absent; which agent CLI the repo is
   already set up for, if either — the artifact signals in `reference/COPILOT.md`, which
   is the evidence preflight step 2 proposes its answer from, and note that `CLAUDE.md`,
   `AGENTS.md`, and `.claude/skills/` are read by both CLIs and so discriminate nothing;
   existing CLAUDE.md /
   README / docs / ADRs; branch + PR conventions from `git log`; app entry point / run
   command; how the app is deployed, if it is (CD workflows, hosting config,
   Dockerfiles); any security scanning CI already runs (dependency audit, secret
   scanning, static analysis — the proposed gate folds these in per
   `reference/GATE_RECIPES.md`); test layout and any existing mocking conventions; the
   runtime conventions the code actually follows — logging framework(s) imported and
   how levels are used, error-handling patterns (custom exception types, wrapping at
   boundaries) and the count of bare/blind catches — plus which *Runtime-standards
   rules* (`reference/GATE_RECIPES.md`) the linter config already enables; any existing
   test-isolation enforcement (network blockers, sanitized env vars) and the seams it
   misses; whether the repo holds more than the app (docs site, infra, data pipelines
   — anything the process might not govern); and whether any file named
   `PROJECT_INDEX.md`, `INDEX.md`, or `STATUS.md` already exists anywhere in the tree —
   the kit is about to make `spec/PROJECT_INDEX.md` the single source of truth, and a
   same-named neighbor is how a session ends up reading the wrong file. Same class of
   check as the leftover-`{{` exit grep.
2. **Present findings + proposal — the feedback halt.** Show: detected stack, proposed
   gate commands (prefer what CI already runs), proposed hook, whether `.gitattributes`
   defines an eol policy — if not, offer `* text=auto eol=lf` (recommended; the
   rationale and the non-markdown evidence are in §2a scaffold step 1); an owner wary
   of a repo-wide change can
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
   or only ever by tooling — never both; how a merged phase reaches users and how a
   deploy is **verified** — the same asks as New mode Round 3, resolving
   `{{DEPLOY_NOTE}}` (step 1's survey of CI/CD config seeds the proposed answer); in-flight
   work (open branches/PRs to record in START HERE), known trouble spots for the
   backlog, always-active rules worth encoding, the **runtime conventions** — propose
   what step 1 *discovered* (framework, level usage, wrapping) as the recorded
   conventions, resolving `{{LOGGING_CONVENTIONS}}`/`{{ERROR_CONVENTIONS}}` in the
   merged `CLAUDE.md` per New mode Round 3's *runtime-conventions ask*, and propose
   the *Runtime-standards rules* delta with each rule's **measured** current violation
   count, the shell it was measured in stated beside it — the owner adopts a rule
   knowing its cost, and the violations a newly
   adopted rule surfaces land in step 4's measured baseline, never in a setup-time fix
   spree — and the **model policy** — same poll,
   same recording rules as New mode Round 3 (`{{MODEL_POLICY}}` in `spec/SDLC.md`;
   `{{DEFAULT_MODEL}}` in `.claude/settings.json` or the line deleted; never into a
   command file). If CI already enforces a coverage floor,
   resolve `{{COVERAGE_FLOOR}}` (gate section of `spec/SDLC.md`) with the existing
   number as-is — **after proving the claim**: confirm the enforcing step actually
   runs in the commands CI executes (a threshold bound to a build phase CI never
   reaches enforces nothing — `spec/SDLC.md`, *Coverage floor*, states the
   prove-it-fires rule). A floor that turns out to be recorded but not wired is an
   owner finding at setup, not a number to copy. If CI enforces none, resolve it as
   `TBD from first CI run` and do not
   propose one.
3. **Generate** (same placeholder-resolution rules as New mode):
   - `CLAUDE.md` — merge, never replace; existing instructions win on conflict and
     conflicts are surfaced to the owner. `{{EXTRA_SPEC_ROWS}}`: one spec-loading row
     with a precise trigger per existing doc step 1 found worth loading on demand
     (ARCHITECTURE.md, DATA_MODEL.md, …); none found → delete the placeholder line.
   - `spec/SDLC.md`, `spec/TESTING.md` — document the conventions the project
     *actually* follows today (test layout, real mock seams, the integration-vs-unit
     boundary as the tests actually draw it), not aspirations.
   - The test-isolation harness (`spec/TESTING.md` §Test Isolation): author it — or
     extend what step 1 found — and prove each check by its negative case (deliberate
     violation → loud failure naming the attempt → remove → green). If the owner
     defers it, record the gap as a backlog item and resolve `{{ISOLATION_HARNESS}}`
     with what is actually enforced today — never describe enforcement that does not
     exist.
   - `spec/PROJECT_INDEX.md` — seeded with reality: current status, a few Phase
     History rows from git history (pre-SDLC is fine), in-flight work in START HERE,
     known issues in the backlog.
   - Commands, the eight kit skills (five vendored, three kit-written), and
     `reference/REVIEW_LENSES.md` installed
     per New mode step 5 — the destinations depend on the confirmed target CLI; hook
     installed and verified per New mode step 6, merged with any existing hooks rather
     than replacing them (Copilot's live in `.github/hooks/*.json` or inline in
     `.github/copilot/settings.json`, so look in both); the close-out evidence
     checker installed and proven per the same step — an adopted repo has commits to
     prove against, and when `HEAD` itself already carries a record (a re-adoption
     from kit ≥ 0.15.0), the proof runs against a commit predating it, because a
     COMPLETE is the proof not failing. A deliberate lint error in a
     scratch source file must produce the hook's feedback. An unverified hook is
     enforcement that reads as complete.
4. **Baseline the gate honestly.** Run it, then resolve `{{GATE_BASELINE}}` in
   `spec/SDLC.md` with what you measured — this is the placeholder step 3 could not fill,
   because the measurement did not exist yet. Leave it unresolved until now rather than
   guessing; the close-out `{{` check in step 3.1 is what catches you forgetting.
   - Green → `green — 0 lint / 0 type / 0 test failures (measured <date>, <this
     session's shell>)`.
   - Red → do NOT block setup and do NOT fix code now. Record the exact counts
     (`N lint / N type / N test failures (measured <date>, <this session's shell>)`)
     as the baseline in
     `spec/SDLC.md` — its single home; PROJECT_INDEX's phase block points there rather
     than restating the counts — and set status STABILIZATION. The
     surrounding template text already says an increase is a regression — do not restate
     it, and do not edit any command file to match these numbers. Commands read the
     baseline from `spec/SDLC.md`; that is the whole point of recording it there.

   If the local runtime differs from CI's, record "CI is authoritative" (and why) in
   Environment gotchas — and treat the disagreement itself as worth understanding, not
   as a number to split the difference on.

### 3. Close-out (both modes)

1. Exit check: `grep -r '{{' CLAUDE.md spec/ .claude/settings.json` → must be empty,
   plus `.github/hooks/sdlc-gate.sh` when the target CLI is Copilot, and
   `.github/hooks/sdlc-tdd-guard.sh` when step 6's guards were accepted (the gate's
   and the guard's `.json` launchers take no values, and neither does
   `.github/hooks/sdlc-close-out.sh` — copied verbatim — so none of the three is in
   scope). The scope is
   exactly the files setup instantiates — a blanket `.claude/` grep would
   trip on the installed copy of this command, which legitimately names placeholders,
   and on Copilot the same is true of `.github/skills/sdlc-setup/SKILL.md`. Name the
   instantiated files explicitly; a check whose scope drifted with the install path is
   a check that stopped covering the file it was written for.
   Every other installed file is `{{`-free and stays that way. Re-run the gate one
   final time (New mode: must be green in this session's shell — the scope the
   baseline record names).
2. Ask the owner: commit the setup? If yes — New mode: initial commit; Existing mode:
   a `chore/adopt-sdlc` branch and a normal PR (the team should see this land like any
   change). Never commit without asking. **New mode: the close-out checker proof
   deferred from step 6 runs now, against the initial commit just made** — it carries
   no slice record, so the checker must report INCOMPLETE naming all four keys,
   exit 1; quote that output and finalize the `{{CLOSE_OUT_CHECK_NOTE}}` line in
   `spec/SDLC.md` from deferred to proven, in this same commit (amend it). If the
   owner declines the commit, the note keeps saying the proof is owed — a note
   claiming a proof that never ran is the exact defect the checker exists to catch.
3. Report: what was generated, skill/plugin verification results — **file-level only:
   source and installed copies checked; the listing check is still owed, and the report
   says how per CLI: on Copilot the owner types `/skills reload` and checks it now, on
   Claude Code it needs a fresh session** (`reference/SKILLS.md` *How to verify*) — gate
   baseline, and
   the handoff — **`/clear`, then `/plan-phase`** (New, or Existing with a green gate)
   or **`/clear`, then `/next-slice`** on the STABILIZATION backlog (Existing, red
   gate). Point the team at the onboarding checklist in `sdlc-kit/reference/SKILLS.md`,
   and at the kit's home repository — the *Kit home repository* line just written into
   `spec/SDLC.md`, never a guessed URL — for the full process overview.

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
