# Changelog

Kit-scoped, semver-ish. Versions describe **the kit**, not any project that adopted it.
This file is repo documentation and is not shipped inside `sdlc-kit/`; the bundle carries
its version in `sdlc-kit/VERSION`.

An entry marked **[installable]** changes a file an adopted project holds
(`commands/**`, `skills/**`, `agents/**`, `reference/REVIEW_LENSES.md`) and therefore
matters at update time. Entries marked **[adoption-only]** change `templates/**` or the
non-installed reference docs, which are read at `/sdlc-setup` time and never re-applied
to an already-adopted project.

## 0.21.0 — 2026-08-12

The sdlc-kit#6 doc batch (`FEATURE_PLAN.md` §49, owner-approved 2026-08-12): the
Phase 04 retro's two confirmed findings, each a check trusting a record its tooling
never produces. Plus VER.2 (`FEATURE_PLAN.md` §50): the §48 deny-message reword and
the Claude Code TDD-guard dialect, built from the §31.12 probe run and proven
offline and live before entering the tree. Closed out by the pre-release
`/kit-check` pass (§51), whose fixes ride along below.

### Added
- **[adoption-only]** **The TDD-ordering guards gain a Claude Code dialect —
  `templates/tdd-guard-claude.template.py` → `.github/hooks/sdlc-tdd-guard.py`,
  offered per CLI, logging mode first.** Same state machine as the Copilot pair
  (G1 observed-red + refactor license, G2 stop check), shared `.git/sdlc-tdd/`
  state and deny flag; every signal path rebuilt from the 2026-08-12 probe
  (§50): observation reads the **event split** (`PostToolUse` fires only on
  success; failures arrive as `PostToolUseFailure` with the exit code as a text
  header of `error`), matchers cover **`Bash|PowerShell`** (the shell tool's
  hook-visible Windows name is `PowerShell` — the display-name trap a third
  time), hook command lines are shell-neutral `python` launchers (the default
  Windows hook shell is PowerShell; the undocumented per-hook `"shell"` key is
  deliberately not relied on), deny uses the documented JSON
  `permissionDecision` form, Stop honors `stop_hook_active` under the
  documented 8-cap. `settings.template.json` carries the four hook blocks
  (setup removes them on decline, ledger-style); `sdlc-setup.md`'s offer is now
  both-CLIs; `sdlc-update.md` re-offers to Claude-Code-only projects whose
  guard note recorded the old CLI fact rather than a decline. Proof:
  `tools/tdd-guard-claude-check.py` — 33 cases, 12 mutations, all caught — and
  live logging-mode bench sessions on both guard paths (violation + full
  red-green cycle), recorded in the bench's `ENF_PROBE_NOTES.md`. Timeout fail
  direction is undocumented and stated as such (inv 15).

### Fixed
- **[adoption-only]** **The refactor license no longer says "close-out"
  (FEATURE_PLAN §48, field-confirmed by sdlc-kit#6 finding 3).** The guard's deny
  message and the `{{TDD_GUARD_NOTE}}` text named the license's cases under a
  "close-out" label, and a literal reader mid-slice bounced off the word — twice
  observed, once at the cost of a whole skill going unused. Both now name the case,
  not the phase: "a behavior-preserving edit at any point in the cycle (refactor,
  simplification, mutation testing — including a temporary mutation to prove a test
  of existing behavior bites)". The script header's origin-story sentences stay.
  **[installable]** half: `sdlc-setup.md`'s note-resolve wording (the third site the
  §48 list missed) states the same. Hand-apply: reword the deny message in
  `.github/hooks/sdlc-tdd-guard.sh` and the guard note in `spec/SDLC.md` to the new
  template text.
- **[installable]** **The skill-activation ledger's evidence claim is scoped to what
  the hook can see.** The ledger records **tool-dispatched** activations only: an
  owner-typed slash command is injected by the CLI with no tool call and writes no
  line — on both CLIs, since Claude Code's `.claude/commands/` are harness-expanded
  and never dispatch the `Skill` tool either. Field evidence (sdlc-kit#6 finding 1):
  a four-phase ledger, alive and faithful for every tool-dispatched skill, held zero
  lines for its slash-typed slice closes, and the retro sweep's first draft read
  that absence as "end-slice never ran". `/sdlc-retro`'s step-evidence sweep now
  states the bound and rules a missing line for a slash-invocable command **no
  signal either way**; the offer/record wording in `sdlc-setup.md`, `sdlc-update.md`,
  and `GATE_RECIPES.md` says "tool-dispatched" wherever it said "skill activation".
  **[adoption-only]** half: the `{{SKILL_LEDGER_NOTE}}` comment in
  `SDLC.template.md` requires the resolved note to carry the same bound —
  hand-apply: add the sentence to the skill-ledger note in `spec/SDLC.md` (one
  sentence: the ledger records tool-dispatched activations only; a missing line for
  a slash-invocable command is no signal either way).
- **[installable]** **The coverage-floor ratchet works on stacks whose check prints
  no figure and whose threshold lives outside the workflow file.** The old bullet
  assumed CI prints a coverage percentage and the threshold lives in the CI workflow
  file; on a Maven/JaCoCo adoption `jacoco:check` prints only pass/fail — the
  ratchet could never fire — and the threshold lives in the build file, so "assert
  the two homes agree" named the wrong home (sdlc-kit#6 finding 2). `/end-phase` now
  reads the measured number off the enforced run's own output — CI's printed figure
  where one exists, else the coverage report artifact the same run produced — and
  sets the threshold "in whichever artifact carries it"; re-running coverage outside
  the enforced invocation stays forbidden. `/plan-phase`'s testability-sweep example
  updated to match. **[adoption-only]** half: `SDLC.template.md`'s *Coverage floor*
  paragraph and phase-end step 6 restated the same way — hand-apply: replace the
  *Coverage floor* procedure paragraph in `spec/SDLC.md` with this release's
  template text (or fold the two changes: figure source and threshold home).
- **[adoption-only]** **The pre-release `/kit-check` pass: the Claude-guard dialect's
  derived statements catch up (invariant 7).** `reference/COPILOT.md` still declared
  the TDD guards Copilot-only in three places after the dialect entered the tree —
  the mapping-table row, the "Copilot-only by nature" sentence, and the guard
  section, whose deferred-port rationale is now recorded as resolved by the
  2026-08-12 probe. And `SDLC.template.md`'s phase-end Notes-cell vocabulary gains
  the failure form `/end-phase` already records — hand-apply: add
  `deploy NOT verified — <what was seen>` to the deploy bullet's Notes-cell forms in
  `spec/SDLC.md`. **[installable]** half: `skills/diff-review/SKILL.md` no longer
  implies `/code-review` exists on both CLIs (it is Claude Code only, as
  `/end-slice`, `/end-phase`, and the process file already said).

## 0.20.0 — 2026-08-10

VER.1 (`FEATURE_PLAN.md` §37.4, design pre-registered as §46 before any code,
owner-approved 2026-08-10): the close-out evidence record stops being prose-only —
a script now fails loudly when a slice commit's record is silently absent. Includes
the pre-0.20.0 `/kit-check` fixes (§47) — the largest being the delivery gap: the
update path's new-files clause, both classification scripts, and both denominator
checks were blind to the one file this release adds; all now name it.

### Added
- **[installable]** **The close-out evidence checker: `templates/close-out.template.sh`
  → `.github/hooks/sdlc-close-out.sh`, both CLIs, always, verbatim.** A dependency-free
  POSIX sh script that reads the slice commit body off `git log` and verifies the
  R5 record **structurally**: `RED:` at least once, `quality:` / `mutation:` /
  `verify:` exactly once each, every line non-empty after the colon — presence or
  stated-skip form, never omitted, with duplicates of the singletons failing because
  nobody knows which line is the record. Presence only, never truth — its own pass
  output says so — and its failure message steers to the true record ("never invent
  evidence the session did not produce"), not to manufacturing one. Exit 0/1/2
  (complete / incomplete / cannot check); it **fails closed** as a command step, the
  deliberate opposite of the hook fail-open rule. Kit-owned at update time: it takes
  no project values (the sole `.github/hooks/` file that doesn't). Proof:
  `tools/close-out-check.py`, a 21-case corpus (every skip form, each key
  missing/empty/duplicated, mid-line lookalikes, CRLF, two verbatim adopter record
  bodies) plus 8 mutations, all caught; S4 dialect agreement proven through the
  PowerShell→sh chain and live in a Copilot CLI session.
- **[installable]** **`/end-slice` gains step 8, "Verify the record" — and renumbers
  again**: PROJECT_INDEX 8→9, hand-back 9→10. The step runs the checker on the commit
  just made — the artifact `/sdlc-retro` reads, not a draft — in the agent's shell
  tool, taking the recorded invocation for the CLI running the session, quotes its
  output in full either way, and remediates INCOMPLETE by `git commit --amend` with
  the real outcome or the stated-skip form, before anything is pushed. The same file
  gains the `RED:` zero-form in its step-7 record contract (next entry), and the
  hand-back inventory now lists the record check's quoted output.
- **[adoption-only]** **The `RED:` zero-form closes a contract gap the checker design
  surfaced**: a slice with no behavior batches (docs, config — the contract's own
  `verify:`-skip examples) had no legal `RED:` line, since "one per behavior batch"
  and "never omitted" are unsatisfiable together at zero. `SDLC.template.md` step 10
  and `end-slice.md` step 7 now name `RED: none — no behavior batches this slice`.
  `SDLC.template.md` also gains slice-loop step 11 (verify the record; 11→12, 12→13)
  and the `{{CLOSE_OUT_CHECK_NOTE}}` placeholder beside the gate — the proven checker
  invocation per installed CLI, each form run before recorded, machine-scoped like
  its sibling notes, resolved by setup's step 6, which now installs the
  checker and proves it by watching it fail INCOMPLETE against a pre-record commit
  (a New-mode repo defers that proof to setup's own close-out commit; a re-adoption
  whose `HEAD` already carries a record proves against an older ref).
  Measured 2026-08-10 and recorded where setup will need it: Copilot CLI's shell
  tool on Windows resolves no `sh` (and its PATH's `bash` is WSL's, the corrupting
  route); there the
  working invocation derives sh from the git on its PATH, and the note carries the
  literal proven form.

## 0.19.1 — 2026-08-09

The FBK batch (`FEATURE_PLAN.md` §44, owner-approved 2026-08-09): every hook's
feedback audited against one criterion — usable context for the model, on failure
*and* on success. Plus the pre-0.19.1 `/kit-check` fixes below.

### Added
- **[adoption-only]** **Counted test observations are spoken, completing the 0.19.0
  spoken-refusal fix.** That fix left counted runs silent, so the guard's state
  machine stayed invisible on the success side: a session learned its run counted
  only by the next deny not arriving. `observe-test` now echoes each counted run as
  postToolUse `additionalContext` — the state fact it produced, never an
  instruction. GREEN: the stop guard is satisfied, with the reminder that full-suite
  assurance stays the end-slice gate's job (the any-counted-green ruling, spoken
  where it applies). RED: the write license it earned — or, when no test file has
  been edited this session, that it licenses nothing yet, because a message claiming
  a license G1 would refuse is confidently wrong at the exact moment it is trusted.
  Refused runs speak as before. Suite grows to 50 cases and two new mutations
  (re-silencing the counted GREEN, and the counted REDs, must both be caught —
  seventeen total). `sdlc-tdd-guard.sh` is project-owned: existing projects get this
  as a hand-apply; the `.json` launcher is unchanged.

### Fixed
- **[adoption-only]** **The Claude Code gate hook frames its lint failure instead of
  dumping raw linter output.** Through 0.19.0 the failure branch emitted the linter's
  output alone — no statement of which hook fired, which file it checked, or what is
  expected — while the Copilot dialect always framed. Both dialects now open with
  "SDLC gate hook: lint/typecheck failed on the file just edited. Fix it before
  continuing: \<file\>", and the empty-typecheck echo (a stray blank line) is gone.
  `.claude/settings.json` is project-owned: hand-apply for existing Claude Code
  adoptions.
- **[adoption-only]** **The Copilot gate hook says when it truncates.** `emit()` caps
  `additionalContext` at 8000 characters; through 0.19.0 the cut was silent, so lint
  output clipped mid-error read as complete — the silent-failure shape the hook
  exists to refuse, in its own output. The capped text now ends with
  `…[truncated by the gate hook at 8000 chars]`, inside the cap. `sdlc-gate.sh` is
  project-owned: hand-apply; the `.json` launcher is unchanged.

### Fixed (pre-0.19.1 `/kit-check`)
- **[installable]** **The update procedure now names the 0.19.0 and 0.19.1
  hand-applies.** Neither release had a transition note despite seven
  hand-apply-bearing changes between them — the first hook-changing releases to
  skip the 0.16.x/0.18.0 precedent. `sdlc-update.md` step 5 and the root README's
  update section now carry a combined note (four 0.19.0 guard fixes, three 0.19.1
  hook-feedback fixes, all template-diff hand-applies, launchers unchanged), and
  the README's "adoption-only… affects new adoptions, not yours" claim now states
  the standing exception: template changes to project-owned files reach existing
  projects only by hand.
- **[installable]** **CLI-specific tools are no longer asserted as universal.**
  `AskUserQuestion` (a Claude Code tool, absent from `COPILOT.md`'s mapping) is
  qualified per-CLI at its six sites in four commands; `end-slice.md`'s commit
  step names both CLIs' multi-line literal forms (heredoc on a POSIX shell tool,
  here-string on PowerShell) instead of prescribing "the Bash tool with a
  heredoc"; `sdlc-setup.md`'s no-hook branch now names the third home of the
  edit-time-hook claim (`CLAUDE.md`'s *Runtime Conventions* Enforcement clause),
  which carries no placeholder and so nothing else flags — a declined-hook
  adoption would otherwise ship a CLAUDE.md asserting edit-time enforcement that
  does not exist.
- **[adoption-only]** **Reference-doc reconciliations.** `COPILOT.md`'s
  unresolvable "R5.3" batch reference removed; the `disable-model-invocation`
  tension settled from in-tree history (the field arrived with the vendored
  `hypothesis-tests` copy — `SKILLS.md` now records it and its per-CLI meaning,
  `COPILOT.md` scopes "deliberately not adopted" to kit mechanism);
  `GATE_RECIPES.md`'s dated proof paragraph re-stamped 2026-08-09 count-free (it
  certified a body 0.19.1 rewrote — the 0.16.0 specimen recurring) and the bench
  anchored at first use; the guard-note rationale in `SDLC.template.md` and setup
  updated for a guard that now speaks (the note is proactive, the guard's
  messages reactive); the guard suite's hardcoded "fifteen ways" corrected to
  derived-only.

## 0.19.0 — 2026-08-08

### Fixed (pre-0.19.0 `/kit-check` batch)
- **[installable]** **The guard descriptions sessions actually read caught up with
  the guard.** `sdlc-update.md`'s re-offer bullet still described the 0.16.0
  semantics ("deny a production write when no failing test has been observed, and
  block a stop while the suite is red") — wrong on the refactor license, the
  any-counted-green denominator, and session scoping, and it is the text an owner
  reads when deciding the re-offer. Also in the same batch: `end-slice.md` qualifies
  `/code-review` as Claude Code only (its `end-phase.md` sibling always did) and
  states the project-convention-wins rule at the commit recipe; `next-slice.md`'s
  merge-drift gate run points at the recorded definition and baseline;
  `sdlc-update.md` and the root README now treat a recorded *Agent CLI:* line the
  repo's own artifacts contradict as a finding, not a value to proceed on;
  `sdlc-setup.md`'s close-out points at the recorded *Kit home repository* line
  instead of a hardcoded URL, qualifies its final gate run and measured violation
  counts with the shell they ran in; `change-verify`'s re-entry pointer names the
  step that runs (3), not just the one that specifies (2).
### Changed (pre-0.19.0 `/kit-check` batch)
- **[adoption-only]** **The guard note's required content now states all three
  licenses-and-rules, and the disposal-intent trigger reached the canonical file.**
  Three findings converged on the same gap: the refactor license was documented
  only in GATE_RECIPES (not installed) and the guard's own deny message, while the
  `{{TDD_GUARD_NOTE}}` required content — whose stated purpose is "nowhere else the
  session reads at slice time says them" — never mentioned it, and the
  disposal-intent lens pointed reviewers at the note for exactly that content. The
  note's required content (template comment + setup bullet) now carries the third
  rule, the mode-deciding flag file, the per-clone caveat, and the proof record;
  `SDLC.template.md`'s slice-loop lens-trigger list gains the §41 disposal-intent
  trigger `end-slice.md` already had (the direction that mattered: the canonical
  file wins, and it was the one missing the newest lens); the mutation check names
  its environment (the session's shell, the gate's own scope) in both homes.
  Root-doc side, not shipped: the stale "four `{{HOOK_*}}`" count in `CLAUDE.md` and
  `KIT_INVARIANTS.md` (GATE_RECIPES documents eight plus two prose ones), the
  retro's ledger-alive precheck added to invariant 13's denominator list, the root
  README's update step 6 acknowledging accepted-offer artifact writes with the
  do-them-last rule, and the bundle README's project-owned enumeration gaining the
  0.18.0 ledger hook. Three design-shaped findings deferred with revisit conditions
  (`IMPROVEMENT_PLAN.md` §13); five discarded with reasons recorded in
  `FEATURE_PLAN.md` §43.

### Added
- **[adoption-only]** **The TDD guard's declared refactor license — the second TDD
  license G1 was missing.** Through 0.18.0 G1 licensed a production write only through
  a fresh red, so the behavior-preserving close-out passes the kit itself installs
  (`change-simplify`, mutation testing) had no lawful path once the slice was green.
  Measured in the field (ai-news-dashboard Phase 03, 2026-08-08): three consecutive
  slices ran synthetic test-edit/red cycles at close-out, and one legitimate
  simplification was dropped as not worth the dance — the session was observed
  deriving the full bypass recipe before declining on effort, not principle. A
  production write is now also allowed while `.git/sdlc-tdd/refactor-license` exists
  **and** a green run has been observed this session. The file is the session's own
  one-line declaration (step and move); every write under it is logged with that line
  so `diff-review` can audit the window, a test edit revokes it, a new session clears
  it, and it survives reds on purpose — mutation testing's expected reds and the
  revert of a failed refactor move are production writes too, with G2 still refusing
  a red stop. The deny message names both ways out. Suite grows to 42 cases and three
  new mutations (a bare declaration must not license, the revocation must not be
  dropped, the license must not leak across sessions). Like the entry below, this is
  a hand-apply for existing projects; the `.json` launcher is unchanged.

### Fixed
- **[adoption-only]** **The TDD guard speaks when it refuses to count a test run.**
  Through 0.18.0 the observe hook wrote a refusal (compound command, or a payload with
  no exit-code trailer) only to `.git/sdlc-tdd/guard.log` and emitted nothing, so the
  session learned about it at its next unexplained deny. Measured in the field
  (ai-news-dashboard Phase 03, 2026-08-08): three thrash episodes, misattributed
  beliefs that compile-failure reds and `-Dtest=` selectors do not count (both false —
  the guard reads exit codes only), and a probe of the separator list, all downstream
  of the silent refusal. Both refusal shapes now emit the reason and what IS allowed
  ("flags and single-test selectors are fine; use the runner's quiet flag, not a
  pipe") as postToolUse `additionalContext` — the same measured schema the gate hook
  uses; counted runs stay silent. Suite grows to 35 cases and a ninth mutation
  (re-silencing the refusal must be caught). `sdlc-tdd-guard.sh` is project-owned:
  existing projects get this as a hand-apply; the `.json` launcher is unchanged.
- **[adoption-only]** **A single `&` now refuses to count, like every other
  separator.** Through 0.18.0 the guard's compound-command list caught only the
  doubled forms (`&&`, `||`) plus `;` and `|`, so a single-`&` compound's exit code
  could record a false observation; the field's `cmd /c "… & …"` probe (2026-08-08)
  was refused only by the `;` inside its expanded `PATH` value — luck, not design.
  The separator classes are now single-character (`;`, `&`, `|`), which covers the
  doubled forms by containment. Suite grows to 44 cases and a thirteenth mutation
  (regressing to the doubled-only list must be caught). Hand-apply, same file as
  above; the `.json` launcher is unchanged.
- **[adoption-only]** **The stop guard is session-scoped: no writes, nothing to
  guard** (owner-decided 2026-08-08). Through 0.18.0 G2 fired on every `agentStop`
  unconditionally, so a session with no production write and no test edit —
  `/plan-phase`, docs, bookkeeping, `/sdlc-retro` — could not stop clean in deny
  mode, refused with "no green test run has been observed" against work that runs
  no tests by design (masked so far by logging mode, where it only wrote
  WOULD-BLOCK lines). G1 now records when a production write actually goes through
  (`.git/sdlc-tdd/prod-write-observed`, cleared per session like every other
  observation), and stop-check stands down when neither that marker nor a test
  edit exists. A denied write arms nothing — the tree never changed — while a test
  edit alone still arms the guard, because a written test never run is exactly the
  never-ran stop G2 exists to refuse. Suite grows to 48 cases and two new
  mutations (dropping the stand-down, and arming from a denied write, must both be
  caught — fifteen total). Hand-apply, same file as above; the `.json` launcher is
  unchanged.
- **The stop guard's green is documented as any counted green — division of labor,
  not a gap** (sdlc-kit#5 finding 4, owner-decided 2026-08-08). A targeted
  single-test green satisfies G2 by design: full-suite assurance is the end-slice
  gate's job, and the backstop never runs tests inline. Stated in the guard header
  and required content for the `spec/SDLC.md` guard note (template comment + setup),
  so the boundary is written where sessions and owners actually read.

### Changed
- **The guard note now states the two rules the guards impose on every session**
  (sdlc-kit#5 finding 5): a test run registers only as a single bare command (flags
  and single-test selectors are fine), and the stop guard's green is any counted
  green. Nowhere else a session reads at slice time said either — the vendored TDD
  skill stays un-diverged (inv 3); the coordination lives in the note that exists
  exactly when the guards do. Existing guard-running adoptions extend their note by
  hand.
- **New review lens: the disposal-intent test** (`REVIEW_LENSES.md`, trigger added
  to `/end-slice`). A test added and then deleted, skipped, or gutted by the same
  slice — or a new test reaching into mock-policy-fenced internals under armed
  guards — is a key, not a test: the write it licensed merged having been "tested"
  by nothing that survives. Derived in the field before it was ever executed
  (2026-08-08); the refactor license removed the price advantage, this lens covers
  the residue.

## 0.18.0 — 2026-08-07

The observability release, plus a discovery that reshaped every Copilot-dialect hook
the kit ships. The OBS batch (`FEATURE_PLAN.md` §38) added the skill-activation
ledger — machine evidence of which skills actually ran, closing the gap where
presence is not activation — and re-verified `COPILOT.md` against live sources
(two tracked upstream issues had moved: prompt files are declined-for-skills, so the
command packaging is permanent; the hook tool-name vocabulary is now documented).
Building the ledger surfaced the release's biggest fact: **the hook shell follows the
launching shell's PATH, and the WSL launcher route re-parses hook command lines**,
corrupting backslashes and `$(cat)` — which had silently disabled the TDD guards on
that route and made the gate hook report a *false* "no JSON parser" on every edit.
All three hooks are now boundary-proof by construction: bare launcher lines in JSON,
logic in script files that never cross the boundary, each pinned by its proof suite
and proven live on both launcher routes.

**Updating an adopted project — three hand-applies, all project-owned:**
(1) the TDD-guard pair: replace `.github/hooks/sdlc-tdd-guard.json` with the 0.18.0
template verbatim (it inherits the offline proof) and apply the small root-defaulting
diff at the top of `sdlc-tdd-guard.sh`; (2) the gate hook: `.github/hooks/
sdlc-gate.json` becomes a bare launcher you replace verbatim, and the logic moves to
a new `.github/hooks/sdlc-gate.sh` instantiated from `templates/copilot-hook.
template.sh` with the source glob, lint command, and typecheck block read out of your
current JSON before replacing it; (3) re-run the hook proof (a deliberate lint error
must produce feedback) and the hook-environment probe, **launched the way your
operator actually launches the CLI** — the hook shell is per-launcher, and a proof
certifies only the route it ran on. `/sdlc-update` step 5 carries the full notes,
including the offer-when-absent path for the new ledger.

### Added
- **[adoption-only]** **The skill-activation ledger** — an optional, logging-only
  hook on both CLIs appending one timestamped line per skill activation to
  `.git/sdlc-skill-ledger.jsonl` (`templates/skill-ledger.template.json` on Copilot;
  a `"Skill"`-matcher block in `settings.template.json` on Claude Code). Offered at
  setup, never imposed; declines recorded with their date under the two-state rule.
  Probe-proven first: skill invocation fires the post-tool-use event under
  `toolName: "skill"` / `tool_name: "Skill"`, relevance-based activation logging
  identically to explicit (`FEATURE_PLAN.md` §38.2).
- **[installable]** `/sdlc-retro`'s step-evidence sweep reads the ledger as machine
  evidence, with its negative case stated: a silent ledger reports "hook health
  unknown", never per-skill no-evidence. `/sdlc-update` gains the ledger
  offer-when-absent branch with both contradiction directions reachable.
- **[adoption-only]** `templates/copilot-hook.template.sh` — the gate hook's logic
  as a script file (all placeholders live here; the JSON is a bare launcher), with
  `resolve_path` translating absolute-Windows patch-header paths so the gate lints
  the real file on either launcher route.
- **[installable]** Operator levers recorded in `COPILOT.md`: `/rubber-duck` (a
  lever, not a step — conversation-only output cannot satisfy an evidence-shaped
  step) and plan mode (session-folder artifact; press-sourced hard-block with the
  MCP-connected exception). Plus the re-verified capability record: `/fleet`, the
  fourteen-event hooks reference, the exit-2 deny channel, `policy.d`, the
  documented tool-name list, `/skills reload`.

### Changed
- **[adoption-only]** **Every Copilot-dialect hook body is launcher-boundary-proof**:
  `tdd-guard.template.json` and `copilot-hook.template.json` carry bare launchers
  (no backslash, no `$`, no quotes — pinned by suite cases so they cannot be
  silently re-cleverified); the guard script trusts a repo-root cwd when
  `SDLC_REPO_ROOT` is unset.
- **[installable]** Every hook proof and the hook-environment probe name their
  launch route; `{{HOOK_ENVIRONMENT}}` records the route first; the `timeoutSec`
  basis records the route it was timed on.
- **[installable]** The skills-listing check is per-CLI: `/skills reload` confirms
  in-session on Copilot; Claude Code still needs a fresh session.
- Twenty-four findings from the pre-release `/kit-check` fixed in-session
  (`FEATURE_PLAN.md` §38.8) — headline: invariant 13's denominator extended (the
  ledger proof step, the skills-listing check, the deploy verification), the
  `{{SKILL_LEDGER_NOTE}}` resolver made unconditional (the §31.15 no-resolver
  specimen, recurring), the deploy verification's negative case stated, and
  python-pro's self-declared-MIT status no longer flattened to "all MIT".

## 0.17.0 — 2026-08-06

Six process rules extracted from a whole-tree audit of the second adopter after two
merged phases (`FEATURE_PLAN.md` §33, the R6 batch), plus eighteen findings from the
pre-release `/kit-check` (§34). The audit's meta-result restates the enforcement
lineage's thesis on fresh evidence — every mechanized rule held, every prose-only rule
bent — but the six rules answer a narrower gap: the checks that existed were
diff-shaped or claim-shaped, and none could see absence. An artifact nothing consumes,
a promised log line never written, a floor that never fires, a spec claim the tree
does not back, a finding that contradicts a ratified decision, a catch cited as if it
were a fix — each shipped through every existing check, and each now has the one step
positioned to notice it.

**Updating an adopted project:** the canonical statements live in `SDLC.template.md`,
which an update never re-instantiates — the updated commands point at spec sections
your project's copy does not yet carry, and `spec/SDLC.md` wins over the commands by
its own first paragraph. `/sdlc-update` step 5 carries the 0.17.0 transition note;
fold the template diff into your spec files with your owner.

### Added
- **[installable]** **Halt 4 reads the log.** The acceptance run's log output is part
  of the acceptance surface, read against the recorded logging conventions
  (`CLAUDE.md`, *Runtime Conventions*); silence at a boundary the conventions promise
  is a finding. Absence appears in no diff, so no review-shaped step could catch it —
  the founding case promised INFO at run boundaries and ERROR on failure and had
  neither after two merged phases, with no logging config at all.
  (`SDLC.template.md` halt 4; `/end-phase` §3.)
- **[installable]** **A finding that contradicts a ratified spec decision is a spec
  conflict, not a backlog line.** `diff-review` names it as such at CRITICAL — the one
  finding class the close-outs may not defer *or fix* by default: it takes halt 3, and
  whether the code or the decision yields is the owner's call. Founding case: an N+1
  merged into a backlog directly against the phase spec's own "single JOIN FETCH to
  avoid N+1" decision. (`SDLC.template.md` halt 3; `diff-review/SKILL.md`;
  `/end-phase` backlog presentation; `/end-slice` triage carries the carve-out.)
- **[installable]** **A coverage floor is proven to fire when established.** Set it
  above the observed number, run the commands the gate and CI actually execute, watch
  the failure, then set the real value — once, at establishment or inheritance, and
  now also at Existing-mode setup when CI already claims a floor. Two homes agreeing
  on a number proves nothing about whether the enforcing step ever runs: the founding
  case recorded "enforced in pom.xml" while `jacoco:check` bound to a phase neither
  the gate nor CI ever reached. (`SDLC.template.md` *Coverage floor*; `/end-phase`;
  `/sdlc-setup` Existing mode; `GATE_RECIPES.md` *Coverage*.)
- **[installable]** **The unconsumed-artifact lens, at arc review.** Every artifact
  the arc introduced — entity, table/column, endpoint, config key, public API — names
  its production consumer; "next phase will use it" is acceptable only said out loud,
  as a deferred-backlog entry. Slice reviews see changed paths; none of the three
  founding catches (an entity with no production writer, a seeded column with no
  accessor, factory overloads only tests called) ever appeared as a changed path.
  (`REVIEW_LENSES.md`; `/end-phase` §5; `SDLC.template.md` phase-end review.)
- **[installable]** **The retro attaches dispositions and sweeps spec claims against
  the tree.** A catch may be cited as evidence a practice worked only with its
  disposition attached — fixed in `<commit>`, or open in the backlog — and an open one
  lists under damage, never wins alone (the founding retro cited two still-open
  defects as wins). And every concrete artifact the spec files name — paths,
  harnesses, configs, floors — is stat-checked, absences reported with their age (a
  named isolation config had never existed across two phases and two retros).
  (`/sdlc-retro` §2 and the interview.)

### Changed
- **[installable]** **Eighteen pre-release `/kit-check` findings fixed.** The ones an
  adopter can observe: `/end-slice`'s lens-routing (and the template's) now carries
  the three trigger clauses the lens file always stated — a trusted check script,
  logging added around a failure path, logging near credentials — which could
  previously never fire through the routing; a backlog entry's cause is reproduced in
  the environment it was observed in, and a failed reproduction elsewhere downgrades
  to "could not reproduce here" instead of rewriting the entry; the retro's
  gate-trajectory comparison names its shell with CI authoritative; the retro's
  citation read is per-CLI (it named `.claude/commands/` as universal, false on a
  Copilot-only adoption); the gate-baseline record names the shell it was measured
  in, and lives in `spec/SDLC.md` only — `PROJECT_INDEX`'s phase block now points
  there instead of restating counts that went stale silently; the model-policy pin is
  marked claim-only between edits; `/sdlc-setup` names all four hook facts restated
  in prose (`{{HOOK_TOOLS}}`/`{{SOURCE_EXT}}` were resolved only generically);
  `/sdlc-update`'s Notes name `explore.agent.template.md` as installable-on-Copilot.
- **[adoption-only]** `GATE_RECIPES.md` anchors "the bench" at first use and its
  *Coverage* procedure gains the prove-it-fires step; the kit-development invariant
  ledger and `/kit-check` extend invariant 13's denominator with the coverage-floor
  establishment proof — the second consecutive release where that list went stale,
  and the first where it was caught before the tag.

## 0.16.1 — 2026-08-06

One field arc on 0.16.0 produced all three fixes (`FEATURE_PLAN.md` §31.18 and §32; the
seventh field report, filed as `sdlc-kit#4`): the guards' first real defect — found by
arming them — and the two findings of the report. The theme is the arc's own: the
process executed faithfully, and the vulnerabilities were in the seams — a red accepted
without asking what produced it, a hand-back delivered in the same breath as the commit
it described.

### Fixed
- **[adoption-only]** **G1 could be satisfied without writing any test.** Armed for
  deny, a session was denied twice, then ran `mvn test -Dtest=ThisTestDoesNotExist` —
  non-zero because nothing matched — and the guard recorded `RED observed (exit 1)` and
  licensed the write. The denial mechanism was not at fault; the broken step was the
  inference that a red implies a test. G1 now requires both halves of "you changed a
  test this session, then watched it fail": the test-file edit must exist and the red
  must be newer than it. The offline suite gained this exact case first and the case
  was **watched to fail against the 0.16.0 guard before the fix landed**, plus a
  mutation that reverts the fix so the suite keeps enforcing it. The known cost: a
  **resumed** session's first production write is denied until a test file is touched
  (state is session-scoped, so the old branch's leniency for that case was the hole);
  the deny message names the way out. **Installed guards are project-owned — apply by
  hand**: replace the G1 licensing line in `.github/hooks/sdlc-tdd-guard.sh` with the
  0.16.1 template's (one `if` line), or re-instantiate keeping your three patterns.
- **[installable]** **`/next-slice` chained into `/end-slice`, committing and pushing
  with no inspection moment.** §5 said "tell the owner the slice is ready … and run
  `/end-slice`" — one instruction, and close-out runs without asking, so the summary
  and the commit it described arrived in the same turn. The fix is a **command
  boundary, not a sixth halt**: `/next-slice` now stops at the slice-ready hand-back
  and the owner runs `/end-slice`; `/end-slice` carries the mirror guard (owner-typed
  only — reached without the owner asking, it stops); `SDLC.template.md` states the
  rule — autonomy runs *within* a command, never across the boundary between commands
  — in the slice loop and in the halt-points preamble. The five halt points stand
  unchanged.
- **[installable]** **`/sdlc-retro` offered to submit upstream with no path to the
  kit's repository URL.** The retro had to ask the owner for the URL before it could
  act on an approved submission. `spec/SDLC.md` now records it at adoption
  (`{{KIT_HOME_REPO}}` in the template; setup resolves it from the kit README's opening
  — a step, not a new question), retro §6 resolves it *before* presenting the submit
  decision (fallback: the clone URL in the installed `sdlc-update`, written into
  `spec/SDLC.md` when used), and `/sdlc-update` backfills the line on update from the
  URL it actually cloned — never overwriting one already recorded.

### Changed
- **[installable]** **Ten pre-release `/kit-check` findings fixed** (the pass is
  recorded in the kit repo's planning docs). The ones an adopter can observe:
  `/sdlc-setup` no longer describes the three kit-written skills as vendored (both
  modes); `/sdlc-update`'s copy rule states sources and destinations per-CLI instead
  of naming `.claude/commands/` as universal, and — new — when the *Kit home
  repository:* line is already present it is **compared against the URL the update
  actually cloned from**, a mismatch going to the owner as a finding; the gate steps
  in `/end-slice` and `/end-phase` name the shell "green" was observed in, CI
  authoritative on disagreement; the slice `verify:` record names the shell it ran
  in, template and command in step, with the explicit rule that an agent-shell pass
  does not stand in for the owner's acceptance halt; `reference/SKILLS.md` no longer
  claims setup checks the session skill listing (setup verifies files and installed
  copies; the listing is confirmed in a fresh session); `/end-phase`'s coverage-floor
  bullet is stack-neutral; three placeholder-mapping gaps in `/sdlc-setup` closed
  (New-mode test layout, the empty-but-stated PROJECT_INDEX values, `{{SOURCE_GLOB}}`
  named beside the `{{HOOK_*}}` set).

## 0.16.0 — 2026-08-05

The ENF batch (`FEATURE_PLAN.md` §31.5–§31.14): Copilot CLI gets a deterministic
backstop for the two steps the field kept losing — write the test first, do not stop
while red — and the edit-time hook gets three defects fixed, two of which meant it was
never actually running. The batch's theme is the one the bench kept proving: **the
process verified the artifact and was silent about the environment the check itself
would run in.** Every hook fact below was measured on a bench against Copilot CLI
1.0.77, not read out of documentation; where the docs and the bench disagreed, the bench
won and the reference says so.

### Added
- **[adoption-only]** **The TDD-ordering guards — optional, Copilot CLI only.** Two hook
  files (`templates/tdd-guard.template.sh` + `.json` → `.github/hooks/sdlc-tdd-guard.*`)
  that make TDD ordering mechanical rather than advisory: **G1** denies a production
  write when no failing test run has been observed in this session since the last test
  edit, **G2** blocks a stop while no green run has been observed or the latest is red.
  They install in **logging mode** and stay there — deny is armed by the owner, by
  creating `.git/sdlc-tdd/deny-enabled`, after reading enough of the log to confirm the
  guard recognises the project's own test runs. Trial-first, per the pre-registered
  protocol in §31.8/§31.10: a logging trial met all seven criteria, then a deny ramp met
  five of six and the sixth failed, was fixed, and re-passed. State is session-scoped, so
  yesterday's red cannot license today's write. A **cooperative backstop, not a security
  boundary** — shell-tool writes are invisible to it, and a bench session was observed
  reading the guard's own source.
- **[installable]** **`/sdlc-setup` offers the guards** at New-mode step 6, deriving the
  test-path and test-command patterns from answers it already has rather than asking
  cold, and requiring the proof step (make each guard fail once) before they are trusted.
  A decline is **recorded with its date**, never deleted — see the update rule below.
- **[installable]** **The hook-environment probe.** A hook runs in the shell the agent
  CLI resolves, not the one you type in; on a Windows machine with WSL installed that was
  measured to be WSL bash, where neither the project's paths nor its toolchain exist.
  Setup now measures that shell from the CLI's own session and records what it found in
  `spec/SDLC.md` (`{{HOOK_ENVIRONMENT}}`) — which shell answered, which JSON parser it
  offers, and whether the project's own lint command runs there.

### Fixed
- **[adoption-only]** **The Copilot gate hook never ran — on any edit.** On 1.0.77 the
  write tool is `apply_patch`, whose `toolArgs` is raw patch text rather than the
  JSON-encoded string every other tool sends. The hook body JSON-parsed it
  unconditionally, so on the only write tool that fires it fell to its "could not find
  the file" branch every single time. It now parses the patch text, handles multi-file
  patches, and skips `Delete` headers.
- **[adoption-only]** **The Claude Code gate hook failed *silently*.** Where it could not
  find the edited file's path it ran `exit 0` and checked nothing — a silently green
  gate, in the kit's own file, indistinguishable from a clean edit. It now reports on
  stderr and exits 2 for every case it cannot handle: no parser, no path, file missing,
  unusable `CLAUDE_PROJECT_DIR`. Loud-when-it-cannot-run was never a Copilot property;
  that dialect was just the only one that had it.
- **[adoption-only]** **The hooks' undocumented `python` dependency is gone.** Both
  dialects shelled out to `python` while Prerequisites never mentioned it and the FAQ
  answered *"Does this require Python? No."* Both hooks and the guard now carry **two
  parser implementations, python and node, and detect which is present at run time** —
  detection rather than a setup question, because an owner answers for the shell they
  type in while the hook runs in a different one. With neither present, all three say so
  on every edit instead of passing quietly. `node` is not implied by Copilot CLI, which
  is why both ship: four of its five install methods are standalone binaries.
- **[adoption-only]** **Windows CRLF could silently disable both hooks.** Python's
  `print()` emits `\r\n`; the hooks split that output and compare fields to literals, so
  a stray `\r` makes `[ "$st" = "ok" ]` false and sends the hook down its "did not run"
  branch on every edit. Git Bash masks it (MSYS `sed` strips CR); WSL bash does not, and
  WSL exposes Windows `python.exe` through `PATH` interop. All three bodies now strip it.
- **[installable]** **The README's Prerequisites and FAQ told the truth's opposite.**
  Prerequisites now lists "either `python` or `node`, for the edit-time hook only", and
  the FAQ is split into *must my project be Python* (no) and *does the kit need it* (one
  of the two, for the hook), saying plainly that the old answer was wrong.

### Changed
- **[installable]** **`/sdlc-update` re-offers the guards to a project that never had the
  choice.** It reads the *Agent CLI:* line to skip Claude-Code-only projects, then checks
  whether the guard files exist; absent-with-a-recorded-decline is a settled decision that
  gets one sentence, while absent-with-no-record means the project predates the offer and
  gets the full one. Absent guards look identical on disk either way, which is why the
  decision is recorded in prose rather than inferred from the tree.
- **[installable]** **Both statements of the update procedure carry the same warning:**
  the instantiated hooks are **project-owned**, so none of the hook fixes above reach an
  adopted project by updating. They arrive as a changelog entry the owner re-applies by
  hand — and until they do, a Copilot project's edit-time gate has never run.
- **[adoption-only]** `reference/COPILOT.md`'s tool-name provenance table is replaced by
  measurements: `apply_patch`, `powershell` and `view` observed; the **documented**
  `edit` and `create` did not fire on any tested flow. Per-agent `model:` pinning is
  confirmed honoured and skill `model:` confirmed ignored, closing the pending-bench note
  from 0.15.0. `jq` is dropped as a suggested hook substitute — it was never a shipped
  path and never tested, and two proven dialects replace it.

### Fixed by the pre-release `/kit-check` pass
Fifteen findings from the full invariant pass, all fixed before the tag. The ones that
would have shipped: `{{TDD_GUARD_NOTE}}` had no resolver on a Claude-Code-only adoption,
so setup's close-out `{{` check would have fired on the commonest adoption shape with
nothing to write; `spec/SDLC.md` asserted an edit-time hook exists while the new step 6
sanctions declining one; the guard's recorded logging-vs-deny mode named no enforcing
artifact and went stale by design the moment deny was armed, and `/sdlc-update` held that
record and the flag file in the same step without ever comparing them; the recipe's dated
"verified, six cases" certified a hook body that had been replaced; and "never denies on
its own failure" was true of the guard script but not of the hook layer above it, which
this same file had measured failing closed on `preToolUse`. Also: a project-fact
assertion in `sdlc-update.md`, kit-development pointers (`FEATURE_PLAN.md §31.7`, bare
invariant numbers) inside files an adopter receives, and invariant 13's own enumeration
of checks — stale, and therefore unable to lead anyone to the checks this release added.

### Repo (not shipped in the bundle)
- `tools/gate-hook-check.py` and `tools/tdd-guard-check.py` — re-runnable proofs for the
  three shipped hook artifacts, covering both dialects under both parsers, with every
  silent case also run dirty. The guard tool additionally **mutates the guard six ways
  and requires its own suite to catch each**; during this batch it caught its own decay,
  reporting `STALE mutation no longer applies` rather than passing while testing nothing.

## 0.15.0 — 2026-08-05

The R5 batch (`FEATURE_PLAN.md` §31): the sixth field report — the first from a second
adopter, and the first from a Copilot CLI adoption — triaged and fixed. Its theme is
the kit's own hazard-4 rule arrived at independently: *an instruction to do is
unenforceable; an instruction to produce evidence that could only exist if it was done
is enforceable.* Every substantive change here converts a written step into an
evidenced one.

### Added
- **[installable]** **`/end-slice` gains step 6, slice verification** — the
  `change-verify` skill run at slice close, in exactly the shape the quality pass
  already uses: **optional, and never silent**. The skill's own description always said
  "before committing a nontrivial slice", but no slice-level step fired it — on Copilot
  CLI, where skill activation is relevance-based, it demonstrably never ran, and an
  ingestion break survived a slice close-out to surface at phase end, four fix commits
  later. Commit, PROJECT_INDEX, and hand-back renumber to 7/8/9.
  (`templates/SDLC.template.md` slice loop gains the matching step 9;
  `skills/change-verify/SKILL.md` *How to use* now names the step, so skill and
  process state one trigger.)
- **[installable]** **Observed-RED evidence.** RED was written, never evidenced: the
  template said "write one test", not "run it and watch it fail". Now
  `templates/TESTING.template.md`'s RED step demands the observed failing run;
  `/next-slice` §4 records each observation **as it happens** (command, failing line,
  exit code — it cannot be reconstructed at close-out); the slice commit body carries
  the `RED:` lines and the `verify:` outcome as the durable record; `/end-slice`'s
  hand-back states them per behavior batch, with **"not observed" stated, never
  omitted**. The mutation check proves test *sensitivity*; this is the first artifact
  proving red-before-green *ordering*.
- **[installable]** **`/sdlc-retro` gains a step-evidence enumeration sweep** — reads
  the steps `spec/SDLC.md` names and reports each as ran / caught / skipped-with-reason
  / no evidence, off the records the two changes above create. Silent non-activation
  surfaces by enumeration instead of by damage; the report skeleton gains a *Step
  evidence* table.
- **[adoption-only]** **Copilot model routing is operator-performed, and now says so.**
  Setup's tier question states what ratifying `auto` forfeits (process-heavy commands
  may route below the work's tier — a field run paid for this in manual overrides);
  the `spec/SDLC.md` model-policy shape names which commands run at which tier and the
  moment the operator sets the model (`/model` / `COPILOT_MODEL`, before a High-tier
  command); `reference/COPILOT.md` records the three operator levers and marks the
  Copilot-model `model:` pin **unverified pending a bench run** — no per-file pins
  ship until the bench answers.

### Changed
- **[installable]** **Friction-log entries get one prescribed shape** —
  `- <date> — <friction> — open`, flipped by the retro to `absorbed by retro <date>`.
  `templates/PROJECT_INDEX.template.md` prescribes it, `/end-slice` writes it,
  `/sdlc-retro` flips it: one format for writer and sweep, so status is read, not
  inferred.
- **[adoption-only]** `reference/SKILLS.md` — new section: kit skills must never be
  updated via `gh skill install`/`update`, which inject provenance frontmatter
  (repository, ref, tree SHA) into `SKILL.md` and compare against an upstream that is
  not the kit. CLI-neutral: the extension targets six agents including Claude Code.
  `reference/COPILOT.md` cross-references it, and records three dated hook facts for
  any future enforcement batch (`preToolUse` fails open on timeout, `agentStop`'s
  eight-block cap and `stop_hook_active`, `userPromptTransformed` is mutation-only).

### Fixed
- **[installable]** `reference/REVIEW_LENSES.md` — its header still said "`/end-slice`
  §3 points here"; the lens pointer has lived in §4 since the 0.14.0 renumber.

## 0.14.1 — 2026-08-05

A patch release: the Copilot bootstrap becomes documented, plus three findings from a
full `/kit-check` over the 15 invariants. No process change and no new rule — nothing
here alters what a slice or a phase must do.

### Fixed
- **[installable]** `skills/change-verify/SKILL.md` — step 5 told the operator to record
  a resolved toolchain path in `CLAUDE.md` *Environment gotchas*. That section lives in
  `spec/PROJECT_INDEX.md`; the instantiated `CLAUDE.md` has no such section, so the
  pointer resolved nowhere in an adopted project (invariant 5).
- **[installable]** `commands/sdlc-update.md` — said "the six `SKILL.md` files share a
  basename" where the kit ships **eight**. Written when six was correct and not updated
  when `change-simplify` and `change-verify` arrived in 0.14.0 (invariant 7).
- **[installable]** `commands/sdlc-retro.md` — the citation rule covered "a vendored
  skill", silently excluding the three kit-written ones from the rule about which copy
  of a file a report quotes (invariant 11).

### Changed
- **[adoption-only]** **Both READMEs now document how to bootstrap `/sdlc-setup` on
  Copilot CLI**, which neither did. Both said to copy `commands/sdlc-setup.md` into
  `.claude/commands/` and open Claude Code — on Copilot that does nothing: it reads no
  `.claude/commands/` and has no markdown slash commands (`github/copilot-cli#618`).
  The mapping existed in `reference/COPILOT.md` and in setup's own install list, but
  never as an install instruction, and setup cannot install its own entry point — so a
  Copilot adopter had no way in. Both READMEs now carry the packaging step, and say to
  confirm `/skills` lists it before running, since a frontmatter parse failure is
  silent.
- **[adoption-only]** `reference/COPILOT.md` — records why `sdlc-setup` is the one
  hand-packaged command, and quotes the description in its example frontmatter, since an
  unquoted example is what later grows a `: ` and drops the file silently.
- **[adoption-only]** `reference/SKILLS.md` — the kit-commands row named only
  `.claude/commands/`; it now carries both CLIs' destinations and the bootstrap
  exception.
- **[adoption-only]** `sdlc-kit/README.md` — dropped two claims 0.14.0 falsified
  elsewhere but left standing here: "delivered as Claude Code prompt files", and that
  setup installs "the vendored TDD skill set" (it installs eight skills, five vendored
  and three kit-written).

## 0.14.0 — 2026-08-03

The PORT batch: the kit runs on **GitHub Copilot CLI** as well as Claude Code
(`FEATURE_PLAN.md` §21, built as §23–§30, shipped as one release per §26). The process
itself does not change shape — same phases, slices, TDD cycles, five halts — but the kit
stops assuming which CLI is reading it. Three things made that possible and each is a
change an adopter can feel: skills move to a directory **both** CLIs read, the kit stops
depending on a Claude-Code-only review plugin and ships its own reviewer, and the two
remaining Claude Code built-ins the kit leaned on are replaced by portable equivalents.

**Read the two *Changed* entries before updating** — one is a file move and one renumbers
`/end-slice`'s steps. Neither is visible as a plain addition.

### Added
- **[installable]** `skills/diff-review/` — the kit's own two-axis reviewer, **required**,
  named by `/end-slice` step 4 and `/end-phase` step 5. **Spec** (does the change
  implement the slice's or phase's exit criteria, and only those — including scope creep
  and *silent narrowing*, the failure a green gate cannot catch) and **Standards**
  (`CLAUDE.md` *Runtime Conventions* first, a structural-smell baseline only if the
  project documented nothing), reported side by side and never merged. Its prime
  directive is **never invent the spec**: an inferred spec reviews the diff against
  itself and always passes, so "no spec located" is a legitimate axis result. Names no
  CLI-specific agent, tool, or model, so both CLIs run the same reviewer. Kit-written,
  not vendored — see `reference/SKILLS.md` for the design debt to `mattpocock/skills`.
- **[installable]** `skills/change-simplify/` — the post-green quality pass named by
  `/end-slice` step 3 (reuse, simplification, efficiency, altitude). Unlike the reviewer
  it **edits**, so **behavior is frozen**: one behavior-preserving move at a time with
  the gate between, and an improvement that would change behavior is a finding rather
  than an edit. The step is optional; the skill is not, because the decision to skip is
  only available if the skill is there to skip.
- **[installable]** `skills/change-verify/` — the phase-level verification named by
  `/end-phase` step 2. Exercises the arc through the path a real caller takes rather than
  through the test harness, which is the gap a green gate structurally cannot cover.
  **A pass not observed is not a pass**: every claimed run must appear as the exact
  command, the literal bytes it printed, and the exit code, and anything that could not
  be exercised is reported *not exercised* rather than assumed.
- **[adoption-only]** `reference/COPILOT.md` — the Copilot CLI mapping: install paths per
  artifact, the hook dialect, target-CLI detection, what the kit loses there and what
  stands in, four measured authoring hazards, and the alternatives considered and
  declined (shipping the kit as a plugin; emitting `AGENTS.md`).
- **[adoption-only]** `templates/copilot-hook.template.json` — the edit-time gate hook in
  Copilot's dialect. Records that `postToolUse` **cannot block** (it advises, like Claude
  Code's exit-2), that `timeoutSec` defaults to 30 and **timeouts fail open** — a
  timed-out hook reads as a pass, which the generated `spec/SDLC.md` now says out loud —
  and that the `matcher` regex is anchored, so tool names must be exact.
- **[adoption-only]** `templates/explore.agent.template.md` — a read-only sweep profile
  for Copilot's `.github/agents/`, used by `/plan-phase` and the Existing-mode surveys.
- **[installable]** `sdlc-setup.md`: **target-CLI detection**, proposed from positive-only
  signals and confirmed by the owner. The absence of one CLI's marker is never evidence
  of the other — Copilot CLI stamps no session marker at all, so its detection rests on
  repo artifacts and `PATH`, and `CLAUDE.md`/`AGENTS.md`/`.claude/skills/` discriminate
  nothing because both CLIs read them. The answer is recorded in `spec/PROJECT_INDEX.md`
  so `/sdlc-update` reads it rather than sniffing.
- **[installable]** `sdlc-update.md` classifies the Copilot-side artifacts
  (`.github/skills/`, `.github/hooks/`, `.github/agents/`) and handles the 0.14.0 skills
  move as a removal-and-re-add. `.github/copilot-instructions.md` and `AGENTS.md` are
  recorded as **project-owned** — setup writes neither.
- **[adoption-only]** `PROJECT_INDEX.template.md` records the project's agent CLI.

### Changed
- **[installable] The five vendored skills MOVED, they were not re-added.** They lived in
  `.claude/commands/<name>.md` through 0.13.0 and now live in
  `.claude/skills/<name>/SKILL.md`, one directory per skill. **An update removes the old
  path and adds the new one; do not end up holding both** — two copies of `tdd` with
  different content is the one outcome the update must not produce, and `/sdlc-update`
  checks for it. The reason for the move is the whole batch: `.claude/skills/` is read by
  Copilot CLI too, so one copy now serves both. The seven commands deliberately did *not*
  move — a command sitting in a skills directory can be invoked by the model unbidden.
- **[installable] `pr-review-toolkit` is demoted from required to optional**, and Claude
  Code only. This is the other half of the `diff-review` entry above and an adopter
  reading a bare addition would miss it: the per-slice and whole-arc reviews used to name
  a per-machine plugin, so a Copilot adopter was told to run a reviewer that did not
  exist for them and every new developer owed an install step. **Nothing requires it
  now.** It stays installed and stays usable as an optional deepening at phase end;
  nobody needs to uninstall anything, and team onboarding loses the per-machine step
  entirely. (Measured caveat kept in `reference/COPILOT.md`: it *can* be made to run on
  Copilot, but only through an install path its vendor has announced as deprecated.)
- **[installable] `/end-slice` gained a step, so its later steps renumbered.** The new
  optional quality pass is step 3; review is now step 4, commit 6, record 7, hand-back 8.
  A project whose own notes cite `/end-slice` step numbers will be stale after updating —
  `/sdlc-update` flags this and does not edit project-owned docs to fix it.
- **[adoption-only]** `SDLC.template.md`: the matching slice-loop step (old 6–10 became
  7–11), `change-verify` named in phase-end step 1, and both review steps now name
  `diff-review` instead of the plugin.
- **[installable]** `end-phase.md` step 2 names `change-verify` for the phase-level
  verification it previously described only as "smoke test, end-to-end run, manual
  script", and step 3 draws on it — an arc reaching the acceptance halt with nothing
  observed puts the owner in front of a system no one has run.
- **[adoption-only]** `reference/SKILLS.md`'s *Recommended built-ins* table is now a
  **per-CLI availability table**: one row per pass, a Claude Code column and a Copilot
  column, and the rule that where a row offers both you run one. The kit's equivalents
  are deliberately named unlike the built-ins (`change-verify`, `change-simplify`) so
  installing them shadows nothing.
- **[adoption-only]** `reference/COPILOT.md`'s loss table: of five rows, four are closed.
  Only `/code-review` remains a real loss, and it is the one the kit never required.

## 0.13.0 — 2026-08-03

The STD batch: the kit's first product-quality standards — logging, error handling,
secure coding — last of the owner-ordered LEG → COP → STD queue (`FEATURE_PLAN.md`
§18, built as §22), in the shape the first field report taught: checks that fail
loudly, not prose rules. Owner decisions honored: secure coding ships as review
lenses, not a command; conventions ship as setup interview + project-owned record +
lenses + gate rules where mechanical. Two new template placeholders
(`{{LOGGING_CONVENTIONS}}`, `{{ERROR_CONVENTIONS}}`), taught to setup in the same
release; no new files; no halt-point changes.

### Added
- **[adoption-only]** `CLAUDE.template.md` gains a *Runtime Conventions* section —
  how the project's code logs and fails, recorded at setup, each bullet noting which
  parts are mechanically enforced (linter rule IDs) versus review-only. A convention
  changed without its linter rule is a claim, not a control.
- **[installable]** `sdlc-setup.md`: the **runtime-conventions ask** (New mode
  Round 3) — how the software logs (framework, level meanings, what may never be
  logged) and how it fails (fail fast or degrade, wrapping at boundaries, whether
  blind catches are ever acceptable), then the matching gate rules proposed for the
  chosen toolchain, with one adopted rule's violation included in the hook
  verification. Existing mode **discovers first** (frameworks imported, level usage,
  bare/blind-catch count, which rules the linter config already enables) and
  proposes with each rule's measured current violation count — new-rule violations
  land in the measured gate baseline, never a setup-time fix spree.
- **[installable]** `reference/REVIEW_LENSES.md`: three lenses — **logging and
  swallowed errors** (every new handler names where the signal goes; the level is a
  routing decision checked against the recorded conventions; one failure, one
  ERROR), **untrusted input** (name every interpreter the input reaches and the
  mechanism neutralizing it there; canonicalize-then-prefix-check paths built from
  input; deserializers that can execute are not for untrusted data), and **secrets
  and exposure** (a secret has exactly one home; a new surface names its enforcing
  control as configured where the code actually runs; error output to a caller is a
  disclosure decision). The file states their provenance: shipped as standards, not
  from a field catch — each enters the audit regime individually.
- **[adoption-only]** `reference/GATE_RECIPES.md` gains **Runtime-standards rules**:
  per-linter rule sets (ruff `E722`/`BLE001`/`B904`/`T20` + the bandit `S` family;
  eslint `no-console`/`no-empty`/`no-eval` kin + `no-floating-promises`; .NET
  `latest-recommended` analyzers; golangci-lint `errcheck` + `gosec`; checkstyle
  `EmptyCatchBlock`/`IllegalCatch`; clippy `unwrap_used`/`expect_used`/
  `print_stdout`). Rules live in the linter's own config, so the existing gate and
  edit-time hook enforce them with no new command, proven the way the hook is
  proven: one deliberate violation must fail the lint run.

### Changed
- **[adoption-only]** `SDLC.template.md` slice-loop step 6 and **[installable]**
  `end-slice.md` §3: the lens-trigger summary now also fires when the slice added a
  catch or failure path, took in outside data or passed it to an interpreter, or
  touched credentials or an externally reachable surface.

### Fixed
Seven pre-existing defects caught by the release `/kit-check` (all older than this
batch; invariants 2, 3, and 5):
- **[installable]** `end-phase.md` acceptance-review note told the session to fix a
  run command proven broken in the owner's shell in `CLAUDE.md` only, leaving
  `spec/SDLC.md`'s halt-4 line naming the broken command — it now names both homes.
- **[adoption-only]** `SDLC.template.md` halt 5 now carries the reviewer-routing
  clause `end-phase.md` already shipped (a team may route merge approval through a
  human PR reviewer, recorded in the project's `spec/SDLC.md`) — the rule existed
  only in the command, and the template is canonical.
- **[adoption-only]** `PROJECT_INDEX.template.md`: the Phase block now carries a
  coverage-floor line. `/end-phase` and `SDLC.template.md` both assert the floor
  recorded in `spec/PROJECT_INDEX.md` matches the workflow value — against a
  template that had no such field, making a "not done until they are" step
  unsatisfiable on a clean adoption.
- **[installable]** `sdlc-retro.md`: the read-the-citation-off-the-file rule now
  names the copy an adopted project actually holds (installed command / instantiated
  template) — the kit-repo paths it required do not exist where the kit folder was
  deleted, which the rule's own hard gate turned into an unsatisfiable requirement.
- **[installable]** `sdlc-setup.md` now resolves two placeholders it never named:
  the integration-vs-unit boundary in `spec/TESTING.md` (both modes), and
  `{{EXTRA_SPEC_ROWS}}` in `CLAUDE.md`'s spec-loading table (empty for a new
  project; one row per on-demand doc discovered on an existing one).
- **[adoption-only]** `GATE_RECIPES.md`: the hook table now states that `CLAUDE.md`'s
  prose restatement (`{{HOOK_TOOLS}}`, `{{SOURCE_EXT}}`) resolves from the same
  values, so the prose and the hook cannot disagree.

## 0.12.0 — 2026-08-03

The LEG batch: owner-led legibility work from the `FEATURE_PLAN.md` §18 brainstorm,
first of the owner-ordered LEG → COP → STD queue. Input-side and output-side
legibility in one batch: LEG.1 adds the owner hand-back standard (words in), LEG.2 is
the measured token pass over the bundle (words out), baselined on the tree that
includes LEG.1 so the tension stays honest. No new files, no new placeholders, no
halt-point changes.

### Added
- **[adoption-only]** `SDLC.template.md` *Owner halt points* (LEG.1): **the hand-back
  standard** — every owner-facing moment (each of the five halts, and the hand-back
  that ends each command) opens with an executive summary in plain-English bullets;
  every decision the owner is being asked to make is **numbered and explicitly
  marked** (`Decision 1: …`) with options and a recommendation; supporting detail
  follows the summary and never interleaves with it. Motivation: five generations of
  rigor fixes made the agent's output correct, and none asked whether the owner
  could follow it — the owner reports phase/slice output too detailed to follow.
- **[installable]** the six installed commands enforce the standard at their
  halt/hand-back steps, each restating the format inline so it survives in an
  adoption whose project-owned `spec/SDLC.md` predates it: `plan-phase.md` steps
  2 and 6 (the spec presentation opens with a summary; everything being ratified is
  numbered), `next-slice.md` steps 2, 4, and 5 (a derived number that differs from
  the ratified one returns as its own marked decision), `end-slice.md` steps 3 and 7
  (the hand-back restructured: summary first, dispositions as detail), `end-phase.md`
  steps 3, 5, 6, and 7 (post-merge bookkeeping presents its several owner decisions
  together, numbered — never one at a time buried in the bullet that raised each),
  `sdlc-retro.md` steps 2 and 6 (the submit-upstream call is a marked decision),
  `sdlc-update.md` steps 4 and 5 (per-file DRIFTED calls and un-manifested-file
  halts are numbered decisions).

### Changed
- **[installable]** LEG.2, the measured token pass — wording-only trims, no rule,
  halt, or completion condition touched: `plan-phase.md`, `end-slice.md`,
  `end-phase.md`, `sdlc-retro.md`, `sdlc-setup.md` (largest win: Existing mode
  restated New-mode asks verbatim; now cross-references). **[adoption-only]** two
  trims in `SDLC.template.md`. Bundle counts, `wc -w` / bytes÷4 over
  `git ls-files`: 27,882 → 27,765 words, ~46,677 → ~46,487 estimated tokens
  against the post-LEG.1 baseline. The measured finding: SIMP (0.10.0) already
  took the wording fat; what remains is rules, negative cases, and
  confirmed-catch evidence the §16 audit protects. Vendored `skills/**`
  untouched.
- Root-side, no marker: README's field-report count corrected to five (was four)
  — caught by `/kit-check` inv 9 during the batch's closing pass.

## 0.11.0 — 2026-08-03

The R4 batch: the fix batch of the fifth field report (`FIELD_REPORT_2026-08-02.md`,
filed as `sdlc-kit#2`), triaged in `FEATURE_PLAN.md` §15 — ten rules in the report's
damage order, run after SIMP by owner decision. The report's theme shapes the heaviest
rows: **the kit specified what each step must produce and almost never what makes it
done** — R4 gives the phase-boundary steps the completion conditions SIMP deliberately
left to it. No new files, no new placeholders, no halt-point changes.

### Added
- **[installable]** `end-phase.md` §5 (R4.1, R4.3): spawning the review fan-out
  re-asserts the §1 clean-tree precondition where it is load-bearing — the reviewers
  share the session's tree, and a real arc lost two uncommitted fixes to a reviewer's
  `git checkout` while the fix-batch commit claimed both. The corollary travels with
  it: a commit message may not claim a fix that has no test pinning it. And the
  review's completion condition: done only when **every** reviewer has returned — the
  fix batch is assembled after the last return, goes through the gate as one unit, and
  a later-arriving finding re-opens the review rather than starting a second batch.
- **[installable]** `end-slice.md` §3 (R4.1): the slice reviewer reviews the
  uncommitted working diff by design, so the discipline binds to the agent — the
  review is **read-only in the shared tree**: no `git checkout/restore/stash`; fixes
  come back as findings, never as edits.
- **[installable]** `end-phase.md` §3 (R4.2): when no slice's exit criteria required
  running the application — an arc behavior-neutral by construction — the composed
  system runs **locally against real data before the PR opens**. The acceptance halt
  passes vacuously on exactly those arcs; the arc that bought this rule found its
  worst defect in that pass, three commits before the PR, with 474 hermetic tests
  green throughout. `plan-phase.md` step 4 flags the all-slices-behavior-neutral
  condition at planning time.
- **[installable]** `plan-phase.md` steps 4–5 (R4.5): each slice's exit criteria name
  **what observes them and when** — a local command, the gate, CI on the main branch,
  or the owner; a criterion naming an observer that does not run at that point is a
  planning defect, not a slice problem. The kit's own ratchet phrasing is the standing
  exposure for every adopter whose CI runs only on the main branch — a real arc wrote
  the unsatisfiable criterion twice in one planning session.
- **[installable]** `reference/REVIEW_LENSES.md` (R4.4): third lens — **shared state
  under concurrency**: for every object that outlives a request or is reachable from
  more than one, name the runtime's concurrency model and state what serializes
  access. Specimen measured rather than asserted: 410 of 600 concurrent selects
  returned the wrong question's passages under the stdlib threading server — two
  browser tabs is enough. `end-slice.md` §3's trigger enumeration gains the matching
  third trigger.
- **[installable]** `end-slice.md` step 6 (R4.6): the friction log gets its writer —
  friction with the *process* is written to the Kit friction log at slice close, or
  never (one adoption's retros produced 23 findings across three arcs while the log
  gained zero entries). This is the writer R3.8's contingent keep waits on (§16).
- **[installable]** `end-slice.md` step 6 (R4.7): slice close-outs record **status
  only — one line**; detail lives in the phase spec and the commit message (already
  the better record). A real adoption wrote 83–163 lines per slice into its index
  five times and corrected it once per arc. R3.7's phase-close archival bullet stays
  as the safety net by owner decision (§16). **[adoption-only]**
  `PROJECT_INDEX.template.md`'s section comments state the write rule and name the
  friction log's writer.
- **[installable]** `end-slice.md` §6 (R4.8): a control that hands the operator a
  remediation command must scope that command to the population the control actually
  flags — an unscoped fix-everything one-liner corrupted two PNGs whose magic bytes
  legitimately contain CR LF. The *verify the denominator* lens applies to the
  control's own output.
- **[installable]** `sdlc-retro.md` step 5 (R4.10): the citation gate — a finding
  quotes the implicated text at a section number **read off the file at writing
  time** (or, for a silence finding, locates the silence between two named steps that
  do exist), and names **every home** of the quoted wording. Two consecutive reports
  shipped citations written from memory of the process — step numbers for steps that
  do not exist — every one caught only maintainer-side.
- **[adoption-only]** `SDLC.template.md` mirrors every command-side rule above
  canonically (inv 2): halt 4, phase-start item 3, slice-loop items 6 and 9,
  phase-end item 4, and the bookkeeping gotcha rule.
- Root-side, no marker: `FEATURE_PLAN.md` §5 gains the trial-protocol rule (R4.9) — a
  trial pre-registers **what the change is supposed to buy and how that is measured**,
  alongside its safety criteria. F3's four criteria all measured safety, and a trial
  that cannot fail on value cannot justify shipping.

## 0.10.0 — 2026-08-03

The SIMP batch: the simplification pass the fifth field report ranked first (finding 7,
`sdlc-kit#2`) and the kit's own §12 standing note had already called for — run as its
own batch, **before** the R4 fix batch, by owner decision. The audit behind it is
`FEATURE_PLAN.md` §16: 38 adopter-facing rules enumerated from the 0.5.0–0.9.0
releases, each asked *what did you catch, in which adopter, when* — 24 carry confirmed
post-ship catches, and the verdict is the report's own prediction: a pruning, not a
retreat. **This batch adds no new process rules.**

### Removed
- **[installable]** The `sdlc-surveyor` agent and with it the entire `agents/` →
  `.claude/agents/` install mapping (the surveyor was its only occupant since 0.6.0).
  Four releases, zero observed uses across four real arcs — the analysis sweeps absorb
  the fact-fetching it was designed for, and §12 had already recorded that continued
  non-use would be a signal about the step, not noise. Owner-decided 2026-08-03.
  Ripples: `plan-phase.md`'s feasibility check keeps the practice (verify seams by
  quoting the codebase) without the agent; `sdlc-setup.md` no longer installs agents;
  the model-policy Low tier loses its "kit-set" instance; `reference/SKILLS.md` loses
  the kit-agents row; both READMEs and the flow diagram lose the mapping.
- **[installable]** `sdlc-update.md` step 5 gains the mapping's retirement mechanism —
  the first **removed-from-install-set** clause, symmetric to the new-files clause: a
  file in the old manifest's install mapping but absent from the target's is deleted
  when it classified `UNCHANGED`, and goes to the owner when `DRIFTED`. The
  classification script still enumerates `.claude/agents/` so projects on 0.6.0–0.9.0
  can transition. The root README's update section states the same clause (inv 8).
  Machinery the deletion needs to reach adopters — not a new process rule.

### Changed
- **[installable]** Six "do this" rules converted toward "this is done when" — the
  fifth report's cross-cutting theme (the gate, the only step with a completion
  condition, was the only step that never failed) applied to the survivors that admit
  one in a single clause: slice-review triage (`end-slice.md` §3 — done when every
  finding is dispatched and the hand-back names the discards), the mutation check
  (`end-slice.md` §4 — done when every new guard has been seen to fail on exactly its
  own test), re-derivation (`next-slice.md` §2 — done when every marker had its
  proportional check and every `estimated` number carries a derivation), the
  coverage-floor reconcile (`end-phase.md` step 7 — not done until the homes are
  identical), gotcha escalation (`end-slice.md` §6 — exactly two closed states; a
  sharper note is neither), and the friction sweep (`sdlc-retro.md` §2 — done when no
  unabsorbed entry is left unreported). **[adoption-only]** `SDLC.template.md` mirrors
  the first five canonically (inv 2). The whole-arc review and the acceptance pass are
  deliberately untouched — their completion conditions are R4 additions, not
  conversions.

### Audited, kept, on the record (§16)
- The doubles lens (five releases, no attributed catch, failure class demonstrably
  alive) — owner-decided keep. R3.7's archival bullet — kept as the safety net behind
  R4's coming prevention. R3.8's aging rule — kept contingent on R4 giving the friction
  log a writer. Kit-development invariants (14, 15) out of audit scope.

## 0.9.0 — 2026-08-01

The R3 batch: the eight findings of `FIELD_REPORT_2026-08-01.md` (the fourth field
report — a different adopter's fifth phase, a three-slice security arc, filed as
`sdlc-kit#1`). Every claim was verified against the tree at 0.8.0 before triage rather
than accepted: seven stood, one was already fixed in 0.7.0, and three had their scope
or attribution corrected — recorded in `FEATURE_PLAN.md` §12. The report's theme is the
kit's widest yet and now carries invariant 15: **the process verifies the artifact and
is silent about the environment it will run in.** Four of the eight findings are
instances of that one gap. Same shape as R2 and G1 — markdown-only, no new placeholders,
no tooling, no new halt point.

### Added
- **[installable]** `plan-phase.md` step 4: the consequence sweep's hits must now answer
  two questions. **Is it actually inert?** — a claim that a consequence is neutralized
  by configuration ("ships dormant", "off in prod", "merging changes nothing") names
  the variable and **quotes its value from the artifact that configures production**,
  never from the test environment, which is usually configured to make the claim true.
  **What is the independent off switch?** — a control whose only lever also disables an
  unrelated system has no rollback. A real arc called a spend cap dormant in its spec,
  its PR body, and its index while the deployment manifest committed the variable that
  made it enforce from the first request; the test conftest neutralized that same
  variable suite-wide, so every in-repo signal agreed with the wrong conclusion.
  **[installable]** `end-phase.md` step 7 asks the question the deploy outcome does not
  — *what did this deploy turn on*, and what disables each newly-live control by itself.
- **[installable]** `plan-phase.md` steps 3/5/6 + `next-slice.md` §2: a decision
  carrying a number is tagged **`measured`** (naming the run, count, or query behind it)
  or **`estimated`**, and the slice that implements an `estimated` one derives it
  *before* starting — a differing result goes back to the owner as a question and the
  decision is re-tagged. Extends the `measured`/`suspected` vocabulary the backlog
  already uses to where numbers are first ratified. Seven of forty-four decisions on one
  arc were corrected on contact with code, one of them a cap whose approved value
  implied roughly two orders of magnitude more spend than intended.
- **[installable]** `end-phase.md` step 7: the red gate baseline gets the mechanism the
  coverage floor already had — report the count beside the recorded one, then lower it,
  schedule lowering it, or have the owner **ratify holding it** with the number of arcs
  it has been unchanged. One adoption held a typecheck count across four arcs and twelve
  recorded gate runs while its `SDLC.md` called it a ceiling to drive down.
  **[adoption-only]** `SDLC.template.md` states the procedure and the rendering rule: an
  unchanged baseline reads `N (unchanged for K arcs)`, never `held` — a stall must not
  look like an achievement.
- **[installable]** `end-slice.md` §6: a gotcha recorded in **three consecutive slices**
  becomes a gate step, a hook, or a test — or is ratified unpreventable and says so with
  its recurrence count. One adoption recorded the same line-ending hazard four times,
  each note sharper than the last, each one followed, and it recurred every time.
  **[adoption-only]** `SDLC.template.md` bookkeeping rules state it canonically;
  `PROJECT_INDEX.template.md`'s Environment gotchas comment points at it.
- Kit-development (not shipped): **invariant 15** — every verification step names the
  environment it verifies against — added to `KIT_INVARIANTS.md` with its specimen and
  to `/kit-check`'s reading passes.

### Fixed
- **[installable]** `end-phase.md` §5 and `end-slice.md` §3: **verify each review
  finding against the source before it enters a fix batch, and report the findings that
  did not survive alongside those that did.** Nothing previously sat between "run the
  review" and "apply fix batches". Two of five reviewers on one arc produced CRITICALs
  whose stated trigger was factually false; followed literally, the step would have
  taken both fixes into a live authorization path. The reporting half is not optional —
  a discarded finding is evidence about the reviewer.
- **[installable]** `sdlc-setup.md` (both modes) and `end-phase.md` §3: a command the
  **owner** will execute is verified in the **owner's shell**, not an agent's — the
  owner runs the acceptance command during setup and pastes the result, and the resolved
  interpreter path is recorded in Environment gotchas. A documented run command was
  broken for one owner (a conda `base` interpreter their profile put on `PATH`) and
  verified working by agents, whose tool-shells never load that profile, for four
  phases of green gates. **[adoption-only]** `SDLC.template.md` states it at the
  acceptance-review step.
- **[installable]** `sdlc-retro.md` §2: the friction-log sweep now reads the log for
  **status and age**, not only content — unabsorbed entries are reported with how many
  phases they have survived, and anything older than one phase is carried into the new
  report automatically. The absorbed-marker convention existed; nothing read it.
- **[installable]** `end-phase.md` step 7 + **[adoption-only]**
  `PROJECT_INDEX.template.md`: index sections are marked **bounded** or **growing**, and
  closed-phase per-slice detail is archived into that phase's own spec file at the phase
  close. One adoption's single source of truth reached 2,400 lines with the answer to
  "what do I do next" buried above five phases of merged history. Nothing is deleted —
  the file is a dashboard first and an archive never.

## 0.8.0 — 2026-07-22

The G1 batch: the five accepted kernels of `CRITICAL_GAPS_ANALYSIS.md`, an external
review of the kit at 0.7.0 that was challenged before acceptance — the verdict, the
owner answers that re-weighted it, and the rejected remainder (enforcement engine, risk
profiles, full secure-development lifecycle, slice PRs, deployment lifecycle states)
are recorded in `FEATURE_PLAN.md` §11. Every accepted change follows R2's shape: small,
reconcile-shaped, markdown-only — no new files, no new placeholders, no tooling.

### Added
- **[installable]** `end-phase.md` step 7: the deploy question now ends in a
  **verified, recorded outcome** — the deployed artifact is checked against the
  platform's own record (the deploy run's SHA, the dashboard's deployed-commit field)
  and the result lands in the Phase History row's Notes cell (`deployed+verified
  <date>` / `deploy pending — <where tracked>` / `n/a — no deploy`), with a pending
  deploy carried in START HERE until verified. **[installable]** `sdlc-setup.md`'s two
  deploy questions also capture how a deploy is verified (same `{{DEPLOY_NOTE}}`
  placeholder, richer resolution). **[adoption-only]** `SDLC.template.md` phase-end
  step 6 states it canonically; `PROJECT_INDEX.template.md`'s Phase History comment
  and `CLAUDE.template.md`'s `/end-phase` summary mention the outcome.
- **[installable]** `next-slice.md` §3 + **[adoption-only]** `SDLC.template.md` Shape:
  the **hotfix exception** — an urgent production fix while an arc is open branches
  `fix/<slug>` off main with its own minimal PR and Phase History row, the only
  sanctioned second unmerged branch; afterward the arc branch merges main and re-runs
  the gate before its next slice, so the arc never drifts silently from production.
- **[adoption-only]** `GATE_RECIPES.md`: security checks CI already runs (dependency
  audit, secret scan, static analysis) are part of "the gate must match CI" — fast
  ones join the local gate, slow or credentialed ones stay CI-only but are listed in
  the gate section of `spec/SDLC.md`. **[installable]** `sdlc-setup.md`'s Existing-mode
  survey collects them.
- **[installable]** `plan-phase.md` step 4 + **[adoption-only]** `SDLC.template.md`
  phase-start step 2: the **consequence sweep** — behaviors touching auth, money,
  irreversible data operations, credentials, or regulated data must name their extra
  verification in the spec and appear in Risks & Deferred; consequence and size are
  different axes, and smallness is no exemption.
- Kit-development (not shipped): **invariant 14** — a recorded value names its
  enforcing artifact and the step that writes it reconciles the two — added to
  `KIT_INVARIANTS.md` with its specimen (the third field report's floor drift) and to
  `/kit-check`'s reading passes.

## 0.7.0 — 2026-07-22

The R2 batch: all three priority rows of `FIELD_REPORT_2026-07-22.md` (the third field
report — the first full arc run on kit 0.6.0), plus the distribution-readiness work
ahead of opening the repository to a general audience. The report's cross-cutting theme
runs through every fix: a number recorded in prose is not the number the machine
enforces — wherever a value lives in two places, bump both, then assert they agree.

### Fixed
- **[installable]** `end-phase.md` step 7 gains the coverage-floor bullet the ratchet
  was missing: if CI's printed coverage rose this arc, set the floor in the CI workflow
  file to just under CI's printed number in the same docs commit, then **assert** that
  the floor recorded in the index and the value in the workflow file are identical —
  the record is a claim, the workflow value is the enforcement. A real arc recorded
  "28 → 32" in two prose homes while CI silently enforced 28 (finding 1).
  **[adoption-only]** `SDLC.template.md` states the boundary procedure canonically
  (*Coverage floor* section + *Phase end* step 6).
- **[installable]** `next-slice.md` §2 re-derivation is now proportional to the
  `measured`/`suspected` marker it previously read and then ignored: `measured` →
  spot-check that the cited anchors and behavior still hold; `suspected`, or a
  `measured` entry whose anchors drifted or whose spot-check surprises → full
  reproduce-or-disprove, re-tagged with what it finds. Every wrong-cause catch on
  record stays in the full-treatment class (finding 2). **[adoption-only]**
  `SDLC.template.md` slice-loop step 2 mirrors the rule.
- **[installable]** `sdlc-update.md` step 5 now prescribes the bundle-replacement
  mechanism instead of leaving it to improvisation: copy-over-in-place — remove only
  the files the old version's manifest lists, then `cp -r $K/. sdlc-kit/`, never
  `rm -rf` the directory. The improvised `rm -rf` failed half-done on a real Windows
  update (directory busy after every file was unlinked) and on any platform opens a
  window with no bundle at all (finding 3). The root README's update section states
  the same mechanism.
- `reference/SKILLS.md` no longer claims `python-pro.md` carries "no license text" —
  the file's frontmatter self-declares `license: MIT`; the record now says so while
  keeping its redistribution status unverified (no locatable upstream). Found by this
  release's `/kit-check` pass.

### Changed
- Release assets now use stable, version-free names (`sdlc-kit.tar.gz`, `sdlc-kit.zip`,
  `sdlc-kit.CHECKSUMS.txt`) so the README's `releases/latest/download/…` one-liner
  works verbatim. The version still travels in the tag, the release title, and
  `sdlc-kit/VERSION` inside the archive. Applies from the next tag; releases up to
  v0.6.0 keep their `sdlc-kit-<version>.*` names, and the README says so.
- Root README: prerequisites stated (Claude Code, git, a POSIX shell with `sha256sum`),
  the download one-liner fixed, and a new *Reporting problems and field reports*
  section. The bundle README states the same prerequisites (manifest regenerated).

### Added
- `.github/ISSUE_TEMPLATE/` — a one-finding bug-report template and a field-report
  template mirroring the shape `/sdlc-retro` emits, so submitted reports arrive in the
  form the triage process already consumes.

## 0.6.0 — 2026-07-20

The agents-and-model-tiers batch (`FEATURE_PLAN.md` F2), plus two residues from the
0.5.0 migration. Two governing rules, both now stated in `SDLC.template.md`:
parallelism is **read-only fan-out within a step only** (never implementation, never
across slices), and every owner interaction stays in the main session — subagents
cannot ask, so no halt point moves. The five-halt-point invariant stands.

### Added
- **[installable]** New install mapping — the first new destination since
  `REVIEW_LENSES.md`: `agents/` → `.claude/agents/`, project-scoped agent definitions
  inherited on clone like the commands. Initial set is one file, deliberately:
  `sdlc-surveyor.md`, a read-only mechanical-collection agent (`tools: Read, Grep,
  Glob`; `model: haiku` — kit-set, because collection gains nothing from a bigger
  model). It collects and reports verbatim, with denominators; it never analyzes.
  Both classification scripts (`sdlc-update.md` step 3 and the root README's update
  section) now enumerate `.claude/agents/` with an `agents/` prefix match, and their
  denominator checks count both destination directories. Updaters from ≤0.5.0 receive
  the agent via the new-in-install-set clause, not classification.
- **[installable]** `plan-phase.md` step 4: the seven adversarial sweeps run as
  **parallel read-only subagents** — the command's heaviest context load, delegated;
  findings return to the main session, where every question and decision stays with
  the owner. Sweep agents analyze and therefore inherit the session model — the haiku
  surveyor is explicitly excluded from this step. The feasibility check names
  `sdlc-surveyor` (it locates seams; it does not judge them).
- **[installable]** `sdlc-setup.md` gains the **model-policy poll** (both modes, the
  process-fit round): a three-tier recommendation (High `opus` — planning, analysis,
  adversarial review; Medium `sonnet` — code to an existing spec; Low `haiku` —
  mechanical collection) confirmed or adjusted by the owner. Recorded in
  project-owned homes only: the policy as `{{MODEL_POLICY}}` in `spec/SDLC.md`, the
  optional pinned session default as `{{DEFAULT_MODEL}}` in `.claude/settings.json`
  (`"model"` key; line deleted when the owner keeps the harness default). Aliases
  only, never model IDs. Setup never writes a model into an installed command file —
  the rejected shape of field-report #1. `opusplan` on `plan-phase.md` remains
  deferred for lack of field evidence. `plan-phase.md` opens with a one-line pointer
  to the recorded policy.
- **[adoption-only]** `SDLC.template.md`: the read-only fan-out rule and the model
  policy section (`{{MODEL_POLICY}}`); `settings.template.json`: the `"model"` line
  (`{{DEFAULT_MODEL}}`). Placeholders #35 and #36, both resolved by the poll.
- **[adoption-only]** `PROJECT_INDEX.template.md` seeds a **Kit friction log**
  section — process friction (tooling noise, workarounds, silent moments) gets a
  dated one-line home the moment it is felt. `/sdlc-retro`'s recorded-but-unactioned
  sweep mines this section first **[that half installable]** and treats its absence
  on an older adoption as a small finding. Residue of the 0.5.0 migration: TFit's
  friction log had no kit-side counterpart for other adopters.
- **[adoption-only]** Setup's `.gitattributes` guidance widens from `*.md text eol=lf`
  to `* text=auto eol=lf` (New mode writes it; Existing mode offers it, with a scoped
  fallback for owners wary of repo-wide policy). The `*.md`-only pin was measured to
  miss four non-markdown bundle files (`LICENSE`, `MANIFEST.sha256`, `VERSION`,
  `settings.template.json`) on the 0.5.0 TFit update — same phantom-modification
  noise class, one size smaller. The repo-wide form is what this kit's own
  `.gitattributes` uses.

### Fixed
- **[adoption-only]** `reference/SKILLS.md` onboarding checklist said "the five SDLC
  commands"; the set has been seven since 0.4.0 (`sdlc-retro`, `sdlc-update`). Its
  Required table gains the kit-agents row.
- **[adoption-only]** Halt 3's template wording scoped design questions "mid-slice";
  `end-phase.md` has always (correctly) halted on design questions found by the
  whole-arc review too. The template now owns that scope — "mid-slice or by a
  review" (this release's `/kit-check`, invariant 2).
- Root README: the file tree still marked `mutation-testing.md` optional (always
  installed since 0.5.0), and the update section lacked the command's "claim only
  what was checked" rule — both brought back into agreement (invariants 7, 8).

## 0.5.0 — 2026-07-20

The retro-fix batch: all 15 priority rows of `FIELD_REPORT_2026-07-20.md` — the first
real run of `/sdlc-retro`, on the same adoption that produced the first field report.
Cut ahead of the planned agents batch because the report's top rows are a live defect
class in the update path itself. The report's cross-cutting theme — checks whose
denominator was assumed rather than enumerated — is the thread through nearly every
entry below.

### Fixed
- **[installable]** `sdlc-update.md` step 5 no longer replaces a kept `sdlc-kit/`
  folder blind: it enumerates the folder's **actual contents** against the manifest
  first, reports anything un-manifested, and HALTs — a project put that file there, and
  one real update silently deleted a project's only local copy of two commits of
  authored work while reporting "nothing project-owned touched". Step 6 now permits
  that reassurance only when the final diff was actually read (report finding 1).
- **[installable]** `sdlc-update.md` step 4 reports **content-changed counts separately
  from touched counts**, so "5 changed, 19 touched" replaces the flat "24 modified"
  whose known-meaningless noise is exactly where the deletion above went unread
  (finding 12, the mechanism of finding 1).
- The root README's update section mirrors both changes plus the arc-boundary rule —
  the command and the section state the same procedure by definition.
- **[installable]** `end-slice.md` §3 named a review tool that does not exist ("the
  code-review skill"); a real run substituted silently and well, which is why nobody
  looked. The per-slice reviewer is now `pr-review-toolkit:code-reviewer`, the built-in
  `/code-review` is identified as the owner-typed escalation, and any substituted tool
  must be named in the hand-back (finding 6; `reference/SKILLS.md` and setup's step 1.2
  check follow).

### Added
- **[installable]** `end-slice.md` gains a **mutation-check step**: every new guard,
  branch, or error path is deleted or inverted once and the suite watched to fail on
  exactly the intended test. The kit shipped `mutation-testing.md` and no workflow step
  ever invoked it; used by habit on a real project, it caught a test that could not
  have failed and proved a production defect's root cause — the single
  highest-yield check in the kit, previously reachable only by memory (finding 4).
  `mutation-testing.md` accordingly flips from offered to always-installed
  (`sdlc-setup.md` step 5, `reference/SKILLS.md`) — updaters who declined it at
  adoption receive it as a new-in-install-set file.
- **[installable]** `end-slice.md` §3 gains the two lenses slice review structurally
  lacked, both paid for in production: name each **consumer** of a changed error/return
  path and what it did with the old behavior (finding 2 — two arcs, two defects that
  survived every slice review, one live in production); and ask whether any **test
  double** omits a side effect or simplifies the error surface of what it replaces
  (finding 5 — a recorder that dropped one flag assignment hid a live bug through four
  reviews).
- **[installable]** `next-slice.md` §2: **re-derive a backlog entry's stated cause
  before writing any fix** — 3 of 3 entries checked on a real project stated a wrong
  cause, and a fix aimed at a fictional trigger can be right anyway, pass every test,
  and teach the next reader a false fact (finding 3). Deferred entries now mark their
  cause **measured** or **suspected** at the writing end (`end-slice.md` §3,
  `templates/PROJECT_INDEX.template.md`).
- **[installable]** `next-slice.md` §3 states the branch rule mode-independently —
  slices accumulate on one arc branch until `/end-phase`; only `/end-phase` opens a
  PR — and checks for **any unmerged arc branch**, not just "am I on main".
  STABILIZATION branches are named for the arc's theme, not their first slice
  (finding 7; `end-slice.md` notes state the accumulation rule its PR prohibition
  always assumed).
- **[installable]** `end-phase.md` post-merge bookkeeping asks the **deploy question**
  (merging is not shipping — a production fix once sat unshipped behind exactly this
  missing step) and **surfaces the backlog** with severity counts for one owner
  decision: convert, defer, or drop (findings 9, 10). Neither is a new halt; the
  five-halt-point invariant stands.
- **[installable]** `sdlc-update.md` states *when* to update: at a phase/arc boundary,
  never with an arc in flight — three updates once landed in the three hours before an
  arc's first slice, and which kit version governed which slice is now
  unreconstructable (finding 8).
- **[installable]** `sdlc-setup.md`: warns that a kept `sdlc-kit/` folder is kit-owned
  and **volatile** (project notes go to a project-owned path); checks `.gitattributes`
  defines an `eol` for `*.md` and offers `*.md text eol=lf` in both modes (findings 1,
  12 — the one-line fix for the phantom-modified noise).
- **[installable]** `sdlc-retro.md` step 1 gains the co-development clause — when the
  kit's own repo is at hand, orientation reads the kit-side planning docs too — and
  step 2 sweeps for **recorded-but-unactioned friction** on both sides. The first real
  retro missed a friction item the kit's plan had already recorded and labeled as retro
  material; the command could only mine what the project wrote down (finding 12's
  method note).
- **[adoption-only]** `templates/SDLC.template.md` carries the canonical statement of
  every process change above: the one-arc-one-branch-one-PR rule in *Shape*, halt 2
  narrowed to skip owner-decided slices (finding 11 — the owner's instinct was to
  delete it; the retro narrowed it instead), the re-derive rule, the renamed reviewer
  and its two lenses, the mutation-check step, and the deploy question + backlog
  presentation at phase end. New placeholder `{{DEPLOY_NOTE}}`, resolved by a new
  deploy-procedure question in both setup interviews — the placeholder contract holds.
- **[adoption-only]** `templates/TESTING.template.md` mock policy: a double that stands
  in for production code must reproduce its **side effects and error surface**, or the
  test drives the real thing (finding 5).
- **[adoption-only]** `templates/CLAUDE.template.md` command summaries follow
  (mutation check; deploy question).

## 0.4.0 — 2026-07-19

The improvement loop gets its input side: `/sdlc-retro` turns a finished phase into
evidence, so the next plan rests on what a run actually taught rather than on what
someone remembered to write down. Cut ahead of the feature plan's schedule (which put
0.4.0 after the agents batch) so the command can be exercised on a real adoption —
the same reason the last two releases were cut, and the same reason they found defects.

### Added
- **[installable]** `commands/sdlc-retro.md` — `/sdlc-retro`, lessons-learned extraction
  at a phase boundary. The improvement loop had a proven output side (field report →
  plan → batches → release → migrate) and a manual input side: `FIELD_REPORT.md` was
  written by hand, so the kit's evidence supply depended on someone volunteering a
  retrospective. The command mines what the process already forces onto disk —
  deferred-backlog provenance tags, the gate-baseline trajectory in `spec/SDLC.md`,
  Phase History, `git log` friction signals — then interviews the owner and sorts every
  lesson into exactly two piles: project facts into the project's own files, process
  findings into `spec/SDLC_RETRO_<date>.md` in the shape of `FIELD_REPORT.md`. It never
  submits anything; whether a finding reaches the kit is the owner's call. Refuses to
  run on a project with too little history rather than manufacturing findings.
- **[adoption-only]** `templates/CLAUDE.template.md` lists `/sdlc-retro` alongside the
  four daily commands, so an adopting project learns the command exists. A command
  installed and named nowhere the project reads is a command nobody runs.
- **[installable]** `end-phase.md` step 7 offers `/sdlc-retro` after the phase closes.
  Every other kit command is reachable from the process — `SDLC.md` names `/plan-phase`,
  `/plan-phase` hands off to `/next-slice`, `/end-slice` to `/clear`. The retro had no
  caller, which for *this* command is self-defeating: it exists because the evidence
  supply depended on someone volunteering a retrospective. It is offered rather than
  required, and stays out of `SDLC.template.md` deliberately — a mandatory retro after
  every phase is the ceremony the retro's own "what would you delete?" question exists
  to catch. The failure it prevents is silent: no error, no drift, no `/kit-check`
  finding, just a command that ships in every bundle and never runs.

### Fixed
- The root README's *Updating an adopted project* section was missing the
  **new-files-in-the-target** clause that `sdlc-update.md` step 5 already had — so the
  two statements of the procedure disagreed, which the kit defines as a bug. A human
  following the README by hand would finish step 4 with no instruction that would ever
  create a newly-installed file, and step 6's verification checks only files you copied,
  so the omission verified clean. Found by `/kit-check` invariant 8 while adding
  `sdlc-retro.md` — the first new installed file since the clause was written, and
  exactly the case it exists for.
- **[adoption-only]** `reference/SKILLS.md`'s kit-command row listed five commands,
  omitting `sdlc-update` (shipped in 0.3.0) and `sdlc-retro`. It is a derived statement
  of the install mapping, so it now names its source of truth instead of quietly drifting
  from it a third time.
- **[installable]** `sdlc-update.md` step 5 now says explicitly that files **new in the
  target version's install set** are copied in — classification never sees them (the
  project does not hold them yet), and the command's first real run (TFit,
  0.2.0 → 0.3.0, which introduced two new installed files) had to infer this from the
  source list rather than being told.

## 0.3.0 — 2026-07-19

Everything the field report asked for that 0.2.0 did not ship — and the kit's own
self-check, whose first run found 15 more defects, all fixed here.

### Fixed
- The *Updating an adopted project* procedure hashed the **working tree**, which reports
  every file as drifted for any Windows adopter whose project does not pin line endings —
  the kit stores LF, their checkout holds CRLF. The check looked like it worked and was
  uniformly wrong. It now hashes committed content (`git cat-file -p :path`), which is LF
  on every platform. Found by running the documented procedure against a real adopted
  project rather than a synthetic one.
- The retroactive path for projects adopted before 0.2.0 is now a complete script, and
  notes that `v0.1.0` predates the restructure (kit files at `commands/`, not
  `sdlc-kit/commands/`).
- Both scripts now avoid a trap that produced confident wrong answers: probing for a path
  with `git cat-file … | sha256sum` reports the *pipeline's* status, so a missing path
  yields the hash of empty input and silently matches the wrong entry. Documented, along
  with a denominator check, since the failure mode is a plausible result rather than an
  error.

The three fixes above changed no file inside `sdlc-kit/`. The entries below do, and reach
adopters at the next release; the bundle manifest is regenerated in the same commits (the
release workflow *verifies* the manifest rather than regenerating it, so a stale one
fails the next tag push).

### Added
- **[adoption-only]** `{{SDLC_SCOPE}}` in `SDLC.template.md`, directly below the title,
  and **[installable]** `/sdlc-setup` now asks in both modes whether the process governs
  the whole repo or a subset, and what is explicitly out of scope. Mixed repos are
  common; the first adoption had to record this decision in three files by hand.
- **[adoption-only]** `SDLC.template.md`, CI section: when local and CI disagree about a
  measurement, CI is authoritative — and the disagreement is itself a finding to explain
  before any threshold moves. The kit previously never contemplated the two disagreeing.
- **[installable]** `end-slice.md` §5 (and the matching bookkeeping rule in
  `SDLC.template.md`): a slice that adds a tool, runtime, or service the gate now
  requires records it and adds it to CI in the same commit — a gate dependency
  discovered by a contributor's red run is a documentation bug.
- **[installable]** `end-phase.md` §3: to exercise failure paths during acceptance
  without risking authoritative data, prefer breaking the connection over corrupting
  the data — stop the server; the failure paths are identical and no real data moves.
- **[adoption-only]** `PROJECT_INDEX.template.md`: a dedicated *Environment gotchas*
  section (previously these facts had no home of their own inside *Notes & gotchas*);
  the Existing-mode adoption-row convention for Phase History
  (`| — | **SDLC adopted** | pre-SDLC | … |`, back-filled rows marked as recorded for
  the arc, not as process history); and backlog provenance tags
  (`"(slice review, <date>)"`) — the practice the field report's own retrospective
  called the most useful part of the run.
- **[adoption-only]** `TESTING.template.md` §*Test Isolation — Enforced, Not Promised*:
  the field report's near-miss (a suite calling the live Google Calendar API for three
  slices, green the whole time) as a headline rule — *partial isolation is worse than
  none, because it reads as complete* — plus three checks the kit specifies without
  shipping code: outbound network blocked, credentials unreachable, every home/data-dir
  seam isolated. A new `{{ISOLATION_HARNESS}}` placeholder records where the harness
  lives and the proof that each check has been made to fail.
- **[installable]** `reference/REVIEW_LENSES.md` — deep-dive review lenses behind a
  conditional pointer in `end-slice.md` §3, read only when the slice's diff matches a
  trigger (error-propagation changes; pattern sweeps or trusted check-scripts), so
  ordinary slices pay no context for them. The error-propagation lens: a new raise is
  done when every caller has been re-read; the mirror question *what did I stop seeing?*;
  a status code is a claim about fault. The verify-the-denominator lens takes its worked
  examples from the 0.2.0 session's three confidently-wrong checks rather than the field
  report's miscount — in each, the check returned a *plausible* answer, so nothing
  prompted a second look — paired with the rule that a check is only trustworthy once it
  has been made to disagree. Unlike the rest of `reference/`, this file is **installed**
  (`→ .claude/commands/REVIEW_LENSES.md`, both setup modes) so the pointer resolves in
  projects that removed the kit folder after setup; it is kit-owned, joins the
  manifest/update path, and the README's classification scripts now try the `reference/`
  prefix alongside `commands/` and `skills/`.
- **[adoption-only]** `TESTING.template.md`: a *Skip discipline* subsection beside the
  mock policy — a test must **fail**, not skip, when a tool it requires is absent; a
  silently-skipped test is the same false green as one that reached the real service —
  and *What a test may assert about errors* in §Test Isolation: asserting "returns empty
  on error" is usually pinning a bug (assert that the error propagates instead), and a
  new invariant is checked against what the system already does, not what sounds right.
- **[installable]** `/sdlc-setup` authors the isolation harness for the detected stack
  (New mode step 4; Existing mode proposes it at the feedback halt) and **proves each
  check by its negative case** — a deliberate violation must fail the suite loudly,
  naming what was attempted, before the check is described as enforced. If the owner
  defers it, the gap goes to the backlog and `{{ISOLATION_HARNESS}}` records what is
  actually enforced today — never enforcement that does not exist. Acceptance was run
  for real in a non-Python stack (Node): the harness authored from the spec alone
  failed loudly on a deliberate `fetch` (naming the address) and a credential-path
  read, then ran 3/3 green with a shell-set token provably not reaching tests.
- **[installable]** `commands/sdlc-update.md` — the update procedure as an installed
  command, closing the field report's #14 outright. It classifies every installed file
  against the manifest of the version the project is **on**, hashes committed content
  (never the working tree), tries all three install prefixes with a denominator check,
  halts exactly once (per-file owner decision on drifted files — never auto-overwritten),
  touches nothing project-owned, and re-stamps `spec/SDLC.md` last so an aborted update
  never claims a version it does not hold. The command and the root README's *Updating an
  adopted project* section deliberately state the same procedure twice — they are
  cross-pointed, a disagreement between them is defined as a kit bug, and keeping them in
  agreement is a `/kit-check` invariant candidate. `SDLC.template.md`'s update pointer
  now names `/sdlc-update` instead of the home-repo README, which an adopted project may
  not hold.
- **[installable]** `/sdlc-setup` Existing mode: the analysis step now globs for
  pre-existing `PROJECT_INDEX.md` / `INDEX.md` / `STATUS.md` anywhere in the tree and
  surfaces hits at the feedback halt with an offered rename of the pre-existing file —
  the kit is about to make `spec/PROJECT_INDEX.md` the single source of truth, and a
  same-named neighbor is how a session reads the wrong file. If the owner keeps both
  names, the disambiguation is recorded in project-owned files (Environment gotchas), not
  in command prose. Scoped to Existing mode, as planned; renaming the kit's own file
  remains deferred until the update path has been exercised at scale.
- **[installable]** `end-phase.md` §5: one sentence on why the whole-arc review exists —
  slice reviews each see one layer, so arc-level bugs live in the seams between slices
  and are invisible to every per-slice review by construction.
- **[adoption-only]** `SDLC.template.md`, gate-baseline section: a count can also hold
  still because the checker stopped looking — suppressions, skipped tests, and constructs
  that hide code from analysis freeze the number while shrinking what it measures.
  **Flagged unsolved:** this is a prose warning, which the field report's own thesis says
  is the weak form of a fix. The real mechanism records *checker reach* (suppression
  count, `Any`-expression share) alongside the error count so a flat count with degrading
  reach becomes visible; designing that is deliberately deferred — it is placeholder- and
  setup-work sized like a batch of its own.
- **Kit self-check** (root-only; nothing an adopter receives): `KIT_INVARIANTS.md`, the
  canonical ledger of 13 invariants — each carrying the real shipped defect that
  motivated it, as the check's negative case — and `/kit-check`
  (root `.claude/commands/kit-check.md`), an agent reading pass over the ledger, not a
  grep suite: the greppable checks (README tree, manifest currency, `{{` census, step
  references) run as commands inside it, but the invariants that have actually shipped
  defects (a false project fact in prose, a semantically-resolved placeholder, a pointer
  that dangles only post-setup) are invisible to pattern matching — the literal
  placeholder name-match was tried and produced 24 false positives out of 32. Both live
  at the root because invariant 12 forbids kit-development-only files in the bundle —
  the batch as first planned put them *in* the bundle, which would have installed a
  kit-development command into every adopting project.

### Fixed — by /kit-check's first real run

The pass was run before shipping it and disagreed immediately: 15 findings, all fixed
in this release. The ones with teeth:

- **[installable]** `end-phase.md` asserted *"branch protection requires the CI check"*
  — a repo-configuration fact that is false for any adopter without branch protection,
  the same defect class as 0.2.0's baseline assertion (nothing in setup configures or
  verifies branch protection). The command now states the rule without asserting the
  enforcement; **[adoption-only]** `SDLC.template.md`'s CI section softened to match.
- **This changelog's own marker definition classified all of `reference/**` as
  adoption-only** — contradicting the install mapping (and its own entries):
  `reference/REVIEW_LENSES.md` is installed and tracks upstream, so a future change to
  it filed per the old definition would have been tagged *[adoption-only]* and never
  routed to adopters by `/sdlc-update`, which reads these markers. Header fixed;
  **[installable]** `sdlc-update.md`'s Notes no longer repeat the stale generalization.
- The README's manual update procedure **had no verification step**: `/sdlc-update` §6
  re-classifies against the target manifest to prove the classifier discriminates, and
  the README — the stated path for pre-command adopters — went straight from copy to
  re-stamp. Added, along with the command's replace-a-kept-`sdlc-kit/`-folder-wholesale
  step, which the README also lacked (a stale kept folder sits beside a re-stamped
  `spec/SDLC.md` claiming a version it does not hold). Both were disagreements between
  the procedure's two statements — found by the invariant recorded when the second
  statement was written.
- **[installable]** `sdlc-setup.md` Existing mode installed the edit-time hook with no
  proof it blocks — the deliberate-lint-error verification existed only in New mode,
  and Existing mode is both the field-tested path and the riskier install (hook
  *merging*). The proof is now required in both modes.
- **[installable]** `skills/python-pro.md` carried a "Reference Guide" table pointing
  at five `references/*.md` companion files that exist nowhere — not in the kit, not
  installed — so a Python session was instructed to load five dangling paths. Table
  removed; the divergence from upstream is recorded in `reference/SKILLS.md`, whose
  provenance note (with `THIRD_PARTY_NOTICES.md`) now also states plainly that
  `python-pro.md` has no identified upstream license, rather than implying blanket MIT.
- **[installable]** `sdlc-setup.md`'s close-out exit check grepped all of `.claude/`,
  which contains the installed copy of `sdlc-setup.md` itself — a file that
  legitimately names placeholders — so the check false-positived on every adoption
  (plan §8.11, left for this batch deliberately). Scoped to exactly the instantiated
  files: `CLAUDE.md spec/ .claude/settings.json`.
- **[adoption-only]** `SDLC.template.md` + **[installable]** `sdlc-setup.md` +
  `reference/GATE_RECIPES.md`: the coverage floor now has a recorded home — a
  `{{COVERAGE_FLOOR}}` line in the gate section (`TBD from first CI run` until one
  exists), resolved by both setup modes, enforcement staying in CI. Previously the
  "record TBD" instruction named no destination.
- Smaller finds, same pass: the canonical template never stated two rules the installed
  commands enforce (push at slice end; the conditional review lenses) — both added
  **[adoption-only]**; `{{STOP_COMMAND}}` had no producing interview question (now
  asked with the run command, both modes, **[installable]**); the formatter was asked
  for and never routed anywhere (now in scaffold step 1); `plan-phase.md` read a
  "product direction" section `PROJECT_INDEX.template.md` does not scaffold (pointer
  trimmed, **[installable]**); the root file tree was missing `.gitattributes` and
  `.gitignore` (invariant 5's first mechanical catch).

## 0.2.0 — 2026-07-19

Version identity, an update path, and the two defects the first field report found in the
shipped kit.

### Fixed
- **[installable]** `commands/end-slice.md` asserted *"The typecheck baseline is green"*
  unconditionally, which is false on any project adopted with a red baseline — a mode the
  kit advertises as supported. Both `end-slice.md` and `end-phase.md` now read the gate
  baseline from `spec/SDLC.md` instead of assuming it. Root cause, now a kit invariant:
  **a command file may not state a fact about the adopting project.**
- **[installable]** `/sdlc-setup` asked for a coverage floor defaulting to **70%**, and
  **[adoption-only]** `reference/GATE_RECIPES.md` justified that number as "Dungeon Daddy
  uses ≥70%" — a constant imported from another project and never measured. Both removed.
  The floor is now set from the first green CI run using CI's exact invocation, and only
  ever raises. *A remembered constant is not a measurement.*

### Added
- `sdlc-kit/VERSION`, `sdlc-kit/MANIFEST.sha256`, `sdlc-kit/LICENSE`, and a bundle-local
  `sdlc-kit/README.md`, so a downloaded artifact is self-describing, verifiable, and
  carries its MIT license text as redistribution requires.
- This changelog.
- Root README: *Updating an adopted project* — the manual update procedure and the
  file-ownership table.
- Release workflow (`.github/workflows/release.yml`): packages `sdlc-kit/` as
  `sdlc-kit-<version>.tar.gz` and `.zip` on tag push and attaches them to the release.
- **[adoption-only]** `{{KIT_VERSION}}`/`{{ADOPTION_DATE}}` in `SDLC.template.md`, so a
  later update knows its baseline without guessing, and `{{GATE_BASELINE}}`, which gives
  the measured gate baseline one definite home for the commands to read. **[installable]**
  `/sdlc-setup` resolves all three — the baseline only after it has actually measured it.

- `.gitattributes` pinning text files to LF. Checksums are only meaningful if the bytes
  are identical on every platform; without this a Windows checkout hashes CRLF and a
  Linux one hashes LF, so the same kit version would report drift on every file.

### Changed
- Repo restructured: `sdlc-kit/` is now the shippable product; the root holds
  documentation *about* the kit. **[installable]** — the only installable file this
  touched is `commands/sdlc-setup.md`, whose close-out step pointed at a kit-local README
  that the restructure removed; it now points at the home repo. No behavior change.

## 0.1.0 — 2026-07-19

Initial extraction of the Agentic SDLC kit from the Dungeon Daddy project: the two-mode
`/sdlc-setup` command, the four daily commands (`plan-phase`, `next-slice`, `end-slice`,
`end-phase`), the vendored MIT TDD skill set, five templates, and the gate/skills
reference docs.

Tagged retroactively at `bdc0ba1`. The commit after the initial one added only
`FIELD_REPORT.md` and touched no installable file, so the installable surface is identical
across both commits — which is what makes the retroactive tag honest.
