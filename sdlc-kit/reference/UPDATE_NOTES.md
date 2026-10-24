# Update notes, 0.14.0 – 0.31.3

The transition notes `/sdlc-update` carried for kits 0.14.0 through 0.31.3. They moved
out of the command at 0.37.0, once every known adopter had passed 0.35.1. **A project
updating from a version older than 0.32.0 reads every note here for each version it
crosses, before anything is copied.** They belong to step 5 of `commands/sdlc-update.md`
and read exactly as if they still sat there: "this step", "above" and "below" mean that
step (or the command's opening ownership table, above every step), and "the removal
clause" and "the new-files clause" are step 5's first two bullets.
Notes for 0.32.0 onward stay in the command, and so does the standing check the 0.16.0,
0.18.0, 0.21.0 and 0.22.0 notes introduced — each optional hook's record read against
its artifact on every update — which step 5 states in full; the notes here add only
their version-specific readings. This file is these notes' only home;
nothing else restates them.

**An update that also crosses 0.38.0 skips two of these folds:** the 0.22.0 backstop
offer and the 0.31.0 `quality:` `reuse:` rule. 0.38.0 retired both, and its note in the
command says what replaces them.

Not installed into a project, like the rest of `reference/`: an update reads it from the
target kit (`/tmp/kit/sdlc-kit/reference/UPDATE_NOTES.md` in the command's own steps).

- **The 0.14.0 skills move is the second instance, and it is a removal and a re-add of
  the same content.** A project coming from ≤ 0.13.0 holds the five vendored skills at
  `.claude/commands/<name>.md`; the target installs them at
  `.claude/skills/<name>/SKILL.md`. Both halves run: the old paths leave by the removal
  clause above (`UNCHANGED` → deleted; `DRIFTED` → the owner's call, and a drifted
  vendored skill is worth keeping deliberately — see `reference/SKILLS.md` on
  divergence), and the new paths arrive as files new in the target's install set. Say
  this to the owner as one move rather than as a column of unrelated deletions and
  additions, and check
  afterwards that no skill is left at **both** paths — two copies of `tdd` with
  different content is the one outcome this step must not produce.
- **0.14.0 also adds a skill the process now requires: `diff-review/`.** It arrives by
  the new-files clause like any other addition, but say what it means rather than
  listing it: `/end-slice` step 4 and `/end-phase` step 5 previously named
  `pr-review-toolkit`, a per-machine Claude Code plugin, and now name this skill, which
  travels with the repo and runs on both CLIs. Two consequences for the owner, both
  worth stating at the halt. **A Copilot project gains a per-slice review it never
  had** — the commands used to name a reviewer that did not exist there. **A Claude
  Code project loses nothing**: `pr-review-toolkit` stays installed where it is and
  stays usable as
  an optional deepening at phase end, it simply stops being required, so no one needs
  to uninstall anything. If the project's onboarding docs tell new developers to
  install that plugin, that instruction is now optional — flag it, but do not edit
  project-owned docs.
- **0.14.0 adds two more kit-written skills, and one of them changes the slice loop:
  `change-simplify/` and `change-verify/`.** Both arrive by the new-files clause, but
  the owner needs the process change stated, not the filenames. `/end-slice` gains a
  **new step 3**, an optional post-green quality pass, which renumbers every step after
  it — review became step 4 (the 0.14.0 commit/hand-back numbers were 6 and 8; 0.15.0
  renumbers again — next bullet). `/end-phase` step 2 now
  names `change-verify` for the phase-level verification it previously described only
  as "smoke test, end-to-end run, manual script" (0.15.0 adds a slice-close naming
  too — next bullet). Two things to say plainly: the
  quality-pass step is **optional but never silent**, so the hand-back gains a line
  either way; and on Claude Code these do **not** replace the `verify` and `simplify`
  built-ins, which remain available — the kit ships its own so the passes exist on
  Copilot too, and running both over the same range is waste, not rigour.
  A project whose own notes cite `/end-slice` step numbers will be stale after this
  update. Flag that; do not edit project-owned docs to fix it.
- **0.15.0 changes the slice loop again, and prescribes two record formats.**
  `/end-slice` gains a **new step 6** — slice verification via `change-verify`,
  optional but never silent, same contract as the quality pass — renumbering commit to
  7, PROJECT_INDEX to 8, hand-back to 9. The TDD loop's RED becomes evidence-bearing:
  the failing run is observed and recorded as it happens, and the slice commit body
  now carries the `RED:` lines and a `verify:` outcome line. The Kit friction log gets
  one prescribed entry shape (`- <date> — <friction> — open`, flipped by the retro to
  `absorbed by retro <date>`). The catch to state at the halt: those rules live in the
  target's `templates/SDLC.template.md`, `templates/TESTING.template.md`, and
  `templates/PROJECT_INDEX.template.md`, which an update never re-instantiates — so
  the project's `spec/SDLC.md` and `spec/TESTING.md` still describe the old loop, and
  `spec/SDLC.md` **wins over the commands by its own first paragraph**. Until the
  owner folds the template diff into their spec files, the updated commands and the
  project's process file disagree, in the direction that disables the new steps. Hand
  the owner the diff of the three templates between the two versions; do not edit
  project-owned files. Step-number citations in project notes go stale again — flag,
  do not fix.
- **0.16.0 changes BOTH edit-time hook recipes, and both are project-owned — so this
  update delivers neither.** Two changes affect every adopted project on either CLI.
  (a) The hooks now carry **two JSON-parser dialects, python and node, and detect which
  is available at run time**; previously they hard-coded `python`, which was an
  undocumented dependency and simply failed on a machine without it. (b) They pipe the
  parser's output through `tr -d '\r'`, because Windows python writes CRLF and a stray
  carriage return falsifies the hook's own string comparisons — invisible under Git Bash,
  which strips it, and fatal under WSL bash, which does not. On the **Claude Code** side
  there is a third: the hook used to `exit 0` silently whenever it could not find the
  edited file's path, so a broken hook was indistinguishable from a clean edit; it now
  reports on stderr and exits 2, matching the Copilot dialect. Hand the owner the diff of
  `templates/settings.template.json` and/or `templates/copilot-hook.template.json` against
  the values their instantiated hook carries, and let them re-apply. Do not rewrite either
  file. **Re-run the hook-environment probe while you are here** (`reference/GATE_RECIPES.md`,
  *The hook environment*) and compare it against what `spec/SDLC.md` recorded at setup: a
  machine that has gained WSL, or lost the JSON parser the hook picks at run time, moves
  that answer, and nothing else in the process ever looks again. Where it has moved, that
  is a finding for the halt — not a line to update silently.
- **0.16.0 fixes a defect in the Copilot gate hook that this update cannot deliver.**
  On Copilot CLI the write tool is `apply_patch`, and its `toolArgs` is raw patch text
  rather than the JSON every other tool sends. The hook body through 0.15.0 JSON-parsed
  it unconditionally, so on the only write tool that actually fires it fell to its
  "could not find the file" branch **on every edit** and never once ran lint or
  typecheck. On a Copilot project, `.github/hooks/sdlc-gate.json` is where to look: the
  symptom is the hook reporting on every edit that it did not run. Read it with the
  owner rather than assuming its state — it is project-owned, this command never
  classified it, and it may have been hand-patched, replaced, or never installed.
  0.16.0's `templates/copilot-hook.template.json` is the fix to compare against —
  though a project crossing 0.18.0 in the same update should skip straight to that
  release's restructured pair (its note below) rather than re-applying 0.16.0's
  single-JSON body only to replace it again.
  The instantiated `.github/hooks/sdlc-gate.json` is **project-owned** — it holds this
  project's own lint and typecheck commands — so an update must not rewrite it. Hand the
  owner the diff between the two template versions and the values their current hook
  carries, and let them re-instantiate. State the consequence plainly at the halt: until
  they do, the hook stays broken, and this is one of the few defects an update cannot
  fix for them. Claude Code projects are unaffected.
- **0.16.0 adds the optional TDD-ordering guards, Copilot CLI only until 0.21.0 — and
  every update from here on checks whether this project was ever offered them.** Two hook files
  (`.github/hooks/sdlc-tdd-guard.sh` and `.json`) that deny a production write outside
  TDD's two licenses (an observed fresh red since the last test edit, or a declared
  behavior-preserving refactor edit behind a counted green) and refuse a stop from a
  coding session while no counted green has been observed or the latest observed run
  is red. They are
  **not** part of the automatic new-files clause: they are project-owned, optional, and
  carry this project's own test patterns, so nothing is installed without the owner's
  word. Decide from two pieces of evidence, in this order:
  1. **Does this project run Copilot CLI?** The *Agent CLI:* line in
     `spec/PROJECT_INDEX.md` says so (`Copilot CLI` or `both`) — the same line step 1
     already reads. A Claude-Code-only project gets
     no offer and no mention at this version — the guards do not exist for it until
     0.21.0's dialect (that note, below, makes the offer), and saying otherwise
     describes a backstop it cannot have.
  2. **Is `.github/hooks/sdlc-tdd-guard.sh` present?** If yes, nothing to do: it is
     project-owned and this update leaves it alone. If no, read the TDD-guard line in
     `spec/SDLC.md` — the one `/sdlc-setup` writes whether the guards were taken *or*
     declined:
     - **It records a decline** → the owner already decided. One sentence in the report,
       then move on; do not re-open a settled question at every update.
     - **There is no such line at all** → this project predates the offer, or setup
       never made it. **Offer the guards now, as a first setup would.** This is the case
       the re-offer exists for, and it is invisible unless you look: the guards being
       absent looks identical either way from the filesystem, which is why the decision
       is recorded in prose rather than inferred from the tree.
     - **The line says "installed" but the files are gone** → do not re-offer as though
       nothing happened. Report the contradiction: the record and the repository
       disagree, and only the owner knows which is right (a removal on purpose, or a
       file lost in a merge). This is the reconcile step — you are holding the record
       and its artifact at the same instant, and comparing them is the whole point of
       having both.
  **Reconcile the other direction too, in the "nothing to do" case above**: when the
  guard files *are* present, still read the line. Present-but-recorded-as-declined is
  the same contradiction pointing the other way, and the branch that skips reading the
  record is exactly the branch that can never notice. Where the line claims **deny mode**,
  say plainly that the flag file deciding it (`.git/sdlc-tdd/deny-enabled`) is inside
  `.git` and therefore per-clone — the line describes the machine that wrote it, not
  this checkout.
  Taking them up means following `sdlc-setup.md` step 6 in full — test patterns derived
  and confirmed, the logging-mode ramp, and the proof step — none of it skippable
  because this is an update rather than a first setup. A guard armed before the log
  shows it recognising the project's own test runs blocks every production write in the
  repo. Record the outcome, **including a decline**, in `spec/SDLC.md` the way setup
  does, so the next update can still tell the two apart. Say which CLI they cover, too:
  a project running both CLIs gets the backstop on the Copilot side only.
- **0.17.0 adds six process rules whose canonical statements live in the templates —
  so this update delivers the commands that point at them, not the rules themselves.**
  Halt 4's acceptance surface now includes the run's log, read against the recorded
  logging conventions; a review finding that contradicts a **ratified spec decision**
  is CRITICAL, named a spec conflict, and takes halt 3 instead of the backlog; a
  coverage floor is **proven to fire** when first established or inherited; the
  whole-arc review gains *the unconsumed artifact* lens (that file updates by
  classification, so the lens itself arrives); the retro cites catches only with
  their disposition attached and sweeps every artifact the spec files name against
  the tree. The catch to state at the halt, same shape as 0.15.0's: the updated
  commands point at sections of `spec/SDLC.md` — halt 3's spec-conflict sentence,
  *Coverage floor*'s prove-it-fires rule, halt 4's log sentence — **that the
  project's un-re-instantiated copy does not yet carry**, and `spec/SDLC.md` wins
  over the commands by its own first paragraph. Hand the owner the template diff of
  `SDLC.template.md` (and `PROJECT_INDEX.template.md`'s phase-block comment) between
  the two versions; do not edit project-owned files. 0.17.0 also widens the
  slice-review lens triggers and requires a backlog entry's cause to be reproduced
  **in the environment it was observed in** — those arrive with the commands and need
  no spec change.
- **0.18.0 adds the optional skill-activation ledger, both CLIs — and every update from
  here on checks whether this project was ever offered it.** A logging-only hook
  appending one line per tool-dispatched skill activation to
  `.git/sdlc-skill-ledger.jsonl`, read by
  `/sdlc-retro`'s step-evidence sweep (*The skill-activation ledger* in
  `reference/GATE_RECIPES.md` is the recipe). It is **not** part of the automatic
  new-files clause: hooks are project-owned and nothing is installed without the
  owner's word. Same two-state check as the TDD guards, but with no CLI gate — the
  ledger exists for both: is the ledger artifact present (`.github/hooks/
  sdlc-skill-ledger.json` on Copilot, the `"Skill"`-matcher block in
  `.claude/settings.json` on Claude Code — check the artifact for the CLI the *Agent
  CLI:* line records)? If yes, leave the artifact alone — **but still read the
  skill-ledger line in `spec/SDLC.md`**: present-but-recorded-as-declined is a
  contradiction only that read can notice, and the branch that skips reading the
  record is exactly the branch that can never notice. If no, read the same line: a recorded decline is a settled decision that gets one sentence; no
  line at all is a project that never had the choice — offer it now, as a first setup
  would, with the proof step (invoke a skill, read the last ledger line back)
  non-skippable because this is an update. Record the outcome, including a decline
  with its date, the way setup does. Present-but-recorded-as-declined, or a line
  claiming installed with the artifact gone, is a contradiction to report, not to
  silently fix.
  **0.18.0 also fixes the TDD-guard hook config for machines where the CLI's hook
  shell is the WSL launcher** — the old config's prelude was silently corrupted on
  that route and the guards never ran there. Both guard files are project-owned, so
  a project that has them gets this only by hand: `.github/hooks/sdlc-tdd-guard.json`
  is a verbatim template copy — replacing it with the 0.18.0 template inherits the
  offline proof — and `sdlc-tdd-guard.sh` carries the project's patterns, so its
  change (the root-defaulting block at the top, per the changelog) is applied as a
  template diff, the way the G1 fix was in 0.16.1. State the consequence at the halt:
  until both land, the guards may be silently inert in some launch environments even
  though the log looked healthy from others.
  **And 0.18.0 restructures the Copilot gate hook the same way, for the same
  boundary** — `.github/hooks/sdlc-gate.json` becomes a bare launcher (verbatim
  template copy, no values, only `timeoutSec` ever edited) and the logic moves to a
  new project-owned `.github/hooks/sdlc-gate.sh`, instantiated from
  `templates/copilot-hook.template.sh` with the project's existing hook values — the
  source glob, the lint command, and the typecheck block, read out of the current
  `sdlc-gate.json` before replacing it, per the changelog. On the affected machines the old single-JSON hook reported a **false**
  "no JSON parser" on every edit; a project that has been seeing that message gets
  its explanation and its fix in the same motion. Hand-apply both files, then re-run
  the proof step (a deliberate lint error must produce hook feedback), in a session
  launched the way this project's operator actually launches the CLI — the hook shell
  is per-launcher, and the proof certifies only the route it ran on. Re-run the
  hook-environment probe here too: the 0.16.0 note's probe instruction is standing at
  every hook-touching crossing, not a one-release step, and this restructure exists
  because the probe's answer is per-launcher.
- **0.19.0 and 0.19.1 change hook-script behavior, and every change arrives by hand —
  the files are project-owned.** 0.19.0 carries four TDD-guard fixes in
  `sdlc-tdd-guard.sh`, each named in the CHANGELOG with its reason: the declared
  refactor license (G1's second license — without it, armed close-out passes force
  synthetic test-edit/red cycles), the spoken refusal (an uncounted run says so
  in-context instead of only logging), the single-`&` separator fix (a single-`&`
  compound could record a false observation), and G2's session scoping (a session
  with no production write and no test edit stops clean). 0.19.1 adds three more,
  one per hook: `sdlc-tdd-guard.sh` speaks counted RED/GREEN observations as state
  facts; `sdlc-gate.sh` marks truncated output so clipped lint feedback cannot read
  as complete; and — Claude Code — `.claude/settings.json`'s gate hook frames its
  lint failure (hook named, file named, expectation stated) instead of emitting raw
  linter output. Apply each as a template diff against the project's instantiated
  copy, the way the G1 fix was in 0.16.1; the `.json` launchers are unchanged
  throughout. State at the halt which of these are still pending — a guard note
  describing 0.19.x semantics over a script still running 0.18.0 behavior
  misdescribes the project in the direction that hides fixes.
- **0.20.0 adds the close-out evidence checker, and the file arrives automatically
  but its wiring does not.** `.github/hooks/sdlc-close-out.sh` is kit-owned and
  verbatim (the classification table above), so the new-files clause delivers it —
  but three things live in project-owned files and arrive only by hand. (a)
  `spec/SDLC.md` needs the close-out checker note beside the gate: the proven
  invocation per installed CLI, each form actually run against a real commit before
  being recorded. On Claude Code that is typically
  `sh .github/hooks/sdlc-close-out.sh check` — the proven line is what the note records;
  on Copilot CLI the shell tool on Windows resolves no `sh` (measured 2026-08-10 —
  and its PATH's `bash` is WSL's, the corrupting route), so there the working form
  derives sh from
  the git on its PATH (`bin\sh.exe` beside `git.exe`'s `cmd` directory) and the note
  carries that literal proven path; a non-Windows Copilot project measures its own
  answer. Prove it the way setup does: run it against a
  pre-record commit and watch it fail INCOMPLETE naming all five keys. (b) The
  slice loop in `spec/SDLC.md` gains the verify-the-record step after the commit
  step and the `RED:` zero-form (`RED: none — no behavior batches this slice`) in
  the commit step's record contract — hand the owner the template diff, do not edit
  the spec. (c) `/end-slice` renumbers again: PROJECT_INDEX 8→9, hand-back 9→10.
  Project notes citing those numbers go stale — flag, do not fix. Until (a) and (b)
  land, the updated command names a checker invocation and a record form the
  project's process file does not know — the same disagreement direction as the
  0.15.0 note, and the same resolution: the spec wins until the owner folds the
  diff.
- **0.21.0 adds the Claude Code TDD-guard dialect, and it retires the 0.16.0 CLI
  gate: the guard offer is now per-CLI, per dialect.** The new artifacts — a
  project-owned `.github/hooks/sdlc-tdd-guard.py` (instantiated from
  `templates/tdd-guard-claude.template.py` with the same three patterns as the sh
  dialect) plus four hook blocks in `.claude/settings.json` (PreToolUse
  `Edit|Write`; PostToolUse and PostToolUseFailure `Bash|PowerShell`; Stop) — are
  **not** part of the automatic new-files clause, for the same reason as ever:
  project-owned, optional, patterned. Run the 0.16.0 two-state check per CLI the
  project runs, with one 0.21.0-specific reading: a `spec/SDLC.md` guard line that
  says the guards are *Copilot-CLI-only and this project does not run that CLI* was
  setup's pre-0.21.0 statement about the kit, **not an owner decline** — that
  project never had the choice, so offer the Claude dialect now, as a first setup
  would (instantiate, keep or add the settings blocks, logging mode, fail-first
  proof in a Claude Code session). On acceptance the four settings blocks arrive by
  hand — `.claude/settings.json` is project-owned and the update never edits it.
  0.21.0 also rewords the guard deny message and the guard note (the refactor
  license names the case, not "close-out") — hand-applied as template diffs per the
  CHANGELOG, alongside its other hand-apply notes (the skill-ledger scope sentence,
  the coverage-floor procedure text).
- **0.22.0 adds the close-out checker's stop-time backstop, as an offer.** The
  checker script itself updates automatically (kit-owned; its new `stop-check`
  mode arrives with the file), but the *wiring* is optional and per-CLI:
  `.github/hooks/sdlc-close-out.json` on Copilot (kit-owned verbatim, present only
  where accepted), a `Stop` block in `.claude/settings.json` on Claude Code
  (project-owned, arrives by hand — **a project crossing 0.24.0 in the same update
  installs that block in the 0.24.0 launcher-neutral form, not this release's
  pinned one**: the `"shell": "bash"` key this note originally called load-bearing
  was later measured never firing on Claude Code 2.1.231 — the 0.24.0 note below).
  Read the backstop half of the close-out checker note
  line in `spec/SDLC.md` with the 0.16.0 two-state rule: a recorded decline is
  settled; a line that predates 0.22.0 says nothing about the backstop, so put the
  choice now as setup would (logging mode, never create
  `.git/sdlc-close-out/deny-enabled`, fire-first proof per `sdlc-setup.md` step 6,
  outcome recorded in that same note line). Its bare-commit class is log-only by
  design on every install — say so when offering. Reconcile both directions, as the
  guard check does: a note saying installed beside no artifact, or the artifact
  present beside a recorded decline, is a contradiction to report — and on Copilot
  the artifact whose presence encodes the accept is
  `.github/hooks/sdlc-close-out.json`.
- **0.23.0 adds the product contract, and the artifact arrives only by hand — it is
  project-owned.** A new spec file, `spec/PRODUCT_CONTRACT.md` (from
  `templates/PRODUCT_CONTRACT.template.md`, placeholder-free, seeds empty), holds
  the current-truth statement of owner-ratified externally observable behavior —
  the file `/plan-phase`'s new preserved-contract sweep and `/end-phase`'s new
  per-item acceptance verdicts, preserved-contract check, and contract reconcile
  all read or write. Those commands arrive by classification, but they point at
  this file and at `spec/SDLC.md` sections (*Product contract*; the phase-start,
  halt-4, arc-review, and bookkeeping additions; the slice-loop trigger line) that
  the project's un-re-instantiated spec does not yet carry — the 0.15.0
  disagreement direction, same resolution: the spec wins until the owner folds the
  template diff. Create the file by copying the template as-is, hand the owner the
  `SDLC.template.md` diff, and say plainly: **the contract starts empty on
  purpose** — the one-time backfill over prior phases' ratified decisions is
  offered at the next `/end-phase`, owner-confirmed there, never inferred at
  update time.
- **0.23.0 also restructures `spec/SDLC.md` and gives the index an exit path — both
  arrive only by the owner folding the `SDLC.template.md` diff.** The restructure: a
  *Records* section now holds the per-project values the close-outs read (scope, gate
  commands, baseline, coverage floor, CI line, the hook/environment line, the
  guard/ledger/close-out notes, model policy — a handful of others stay at the step
  that uses them, and the section's preamble names each), with the doctrine sections
  below referencing it — so a command session loads one bounded section, not the
  whole
  file. Folding it **moves the project's recorded values verbatim**: the baseline
  counts, the proven invocations, the measured hook environments are project facts
  this update must never re-derive or re-type from the template. Until the diff is
  folded, the updated commands' *(Records)* pointers degrade soft — the facts are
  the same lines at their old positions, and the spec wins as ever. The exit path:
  `/end-phase` now retires closed items from the two growing record sections —
  backlog entries whose line carries a closing marker (`— done (<fix commit>)` /
  `— dropped (owner, <date>)`), friction lines absorbed more than a phase ago —
  to `spec/PROJECT_INDEX_HISTORY.md`,
  created by that command on first retirement — nothing to create at update time.
  `CLAUDE.md`'s spec-loading table changes arrive by hand the same way (its
  `spec/SDLC.md` row now names *Records*; a new `spec/PROJECT_INDEX_HISTORY.md` row
  carrying its never-at-session-start trigger), and `CLAUDE.md` is project-owned —
  hand the owner the
  `CLAUDE.template.md` table diff, never edit it; `/end-phase`'s retirement bullet
  checks for the row at each close and has the owner's session add it if absent.
- **0.24.0 rewires every Claude-dialect hook launcher-neutral, and none of it
  arrives by updating — `.claude/settings.json` and the hook scripts are
  project-owned.** The finding (measured 2026-08-15, Claude Code 2.1.231, an
  adopter's update bench): a hook carrying the per-hook `"shell": "bash"` key
  **never fired** — on `Stop` and on `PostToolUse` alike, no error, no log — while
  an unpinned twin fired; the interactive route re-measured dead the same day (on
  2.1.233 — the CLI auto-updated between the benches), and the same pinned block
  had measured working 2026-08-13 on an unrecorded version: version drift under an
  auto-updating CLI, and no shipped wiring depends on the pin anymore. On a Claude Code
  project, state the consequence plainly at the halt: **until the rewire lands by
  hand, the gate hook, the skill ledger, and the stop backstop may never have been
  running on some routes — a pinned hook that does not fire looks exactly like a
  clean edit.** The hand-applies, per the 0.18.0 shape (logic in scripts, bare
  launchers in JSON): (a) `templates/claude-gate.template.sh` →
  `.github/hooks/sdlc-gate-claude.sh`, instantiated with the values read out of the
  current settings-file hook body before replacing it; the `Edit|Write` block
  becomes the bare launcher `sh .github/hooks/sdlc-gate-claude.sh`. (b) Where the
  ledger is installed: `templates/skill-ledger.template.sh` (named
  `skill-ledger-claude.template.sh` through 0.31.0) →
  `.github/hooks/sdlc-skill-ledger.sh` (verbatim), the `"Skill"` block becomes
  `sh .github/hooks/sdlc-skill-ledger.sh`. (c) Where the backstop is installed: the
  `Stop` block becomes the launcher-neutral
  `sh -c "if [ -d .git ] && [ -f .github/hooks/sdlc-close-out.sh ]; then sh
  .github/hooks/sdlc-close-out.sh stop-check; fi"`. (d) Every `"shell"` key in the
  settings file is removed — the guard blocks' `python …` lines were always
  neutral and are untouched. Then re-run the hook proof (a deliberate lint error
  must produce the framed exit-2 feedback) **and the hook-environment probe with
  its new dispatch check** (`reference/GATE_RECIPES.md`, *The hook environment*,
  item 4: a pinned-vs-unpinned probe pair, markers read back, CLI version
  recorded) — the standing at-every-hook-crossing rule, and this release is why it
  now asks whether the hook fires at all. Update the hook line and
  the hook-environment record in `spec/SDLC.md` with the owner as the
  facts move — never silently.
- **0.25.0 fixes both of the TDD guard's classifiers, in both dialects, and neither
  fix arrives by updating — the instantiated guard is project-owned.** Both are
  false-positive fixes: the guard was speaking about acts that never happened, which
  is the failure mode that teaches an operator to route around a control rather than
  respect it. (a) **A file outside the repository is no longer production source.**
  An absolute path not under the repo root kept its absolute form, failed
  `TEST_PATH_PATTERN`, matched the extension-only `SOURCE_GLOB`, and was charged the
  same refactor license as an edit to the project's most sensitive module — measured
  over one arc as 13 denials, 5 of them on a session scratchpad, and 12 writes
  licensed for a mandated `/end-phase` verification step whose own text never
  mentions a license. Relative paths still count: they can only be relative to the
  resolved root. (b) **The test-command
  pattern is matched with quoted arguments stripped**, so a `git commit -m` whose
  body quotes the RED command no longer registers as a test run — three spurious
  notices in one phase on a Java adoption.
  Apply each as a template diff against the project's instantiated copy, the way the
  0.19.x fixes were — `templates/tdd-guard-claude.template.py` (pre-write path
  handling and the `observe-test` match) or `templates/tdd-guard.template.sh` (the
  same two), keeping the project's three placeholder values. The `.json` launchers and
  the settings blocks are unchanged. **The shell dialect carries one extra
  consequence worth stating at the halt:** it never reduced the path at all, so an
  absolute path to a file like `tests/conftest.py` was being charged as a production
  write — a *test* edit that licensed nothing. A project on that dialect may have
  friction in its log that this release explains. After applying, confirm from
  `guard.log` on the next real session that scratchpad writes no longer appear and
  that the project's own test runs still register.
- **0.26.0 adds a third mode to the close-out checker, and that half arrives
  automatically — the invocation line in `spec/SDLC.md` does not.** The script is
  kit-owned and copied verbatim, so `docs-check` lands with the file: it counts the
  lines a close-out docs commit added to `spec/PROJECT_INDEX.md` and reports them
  against an in-file budget of 25. It is **log-only on every install** — it exits 0
  even on its own errors and can never fail a step, which is why it is not offered,
  armed, or declined like the stop-time backstop. Nothing in `.git/` and no new
  placeholder is involved. What the project must do is one line of bookkeeping:
  `/end-slice` now runs it after the docs commit, using the **close-out checker
  note's own invocation with `docs-check` where it says `check`** — so a project
  whose note predates the mode has a note that reads correctly but has never been
  proven for it. It needs no separate proof (a log-only mode cannot lie about a step
  it cannot fail); just confirm at the halt that the note's line exists, and if the
  project has no such note at all, resolve it per the 0.20.0 entry above before the
  new step can run. **The rule the mode observes is also newly numbered:** *status
  only, one line* now carries a budget of 25 added index lines, which is a budget and
  not a limit — a close with a genuinely large entry count answers `OVER` in the
  hand-back rather than trimming the record to fit.
- **0.26.0 also adds the phase-close reconcile pass, and it changes what
  `/end-phase` asks before it asks anything else.** Post-merge bookkeeping now opens
  by re-deriving every recorded number and carried claim — the backlog count, every
  row of *Records* (not only the two the kit shipped procedures for), and every
  ratified decision in prior phase specs with neither a contract entry nor a recorded
  drop — reporting each `recorded X / measured Y` before any bullet asks the owner
  for a decision. Two consequences worth stating at the halt: the **first** close
  after updating will usually surface divergences that accumulated under earlier
  releases (a backlog entry already shipped, an adoption-authored *Records* row
  nothing ever reconciled, a ratified behavior absent from the tree) — that backlog
  is the pass working, not a defect it introduced; and rulings it produces are
  ordinary owner decisions, recorded where they are made. The command file carries
  all of it, so this half arrives by updating with nothing to hand-apply.
- **0.27.0 adds a fifth key to the close-out record, and the first slice closed
  after updating will fail on it once.** The slice commit body now carries a
  `lenses:` line beside `RED:`/`quality:`/`mutation:`/`verify:` — the slice review's
  lens verdicts, or the zero-form `no lens triggered` when none applied. Both halves
  arrive automatically: `end-slice.md` prescribes the line and the verbatim
  close-out script enforces it. **That is the point to state at the halt** — the
  checker's `check` mode is fail-closed, so a slice closed out of old habit reports
  `INCOMPLETE - problems: lenses` and the fix is `git commit --amend` with the real
  verdict, exactly as for any other missing key. It is a one-time relearning, not a
  defect, and it is narrow: nothing else about the record changed. Why it was worth
  a fail-closed key rather than a prose rule: a lens that ran and found nothing
  previously left no trace anywhere, because the review hand-back is not retained
  and only a lens *finding* travelled onward under its own name — so two field arcs
  of lens evidence could not distinguish *ran and clean* from *never triggered*, and
  a standing decision to delete three lenses for finding nothing could not be read.
  A check with no durable negative record cannot be told apart from one that never
  ran.
- **0.27.0 also changes how a mutation is undone, and the old recipe could destroy
  a slice.** `end-slice.md` §5 shipped `git checkout -- <path>` as the canonical
  restore in 0.26.0. That step runs *before* the slice commits, so the
  implementation sits uncommitted underneath the mutation and the command restores
  the path to **HEAD** — reverting the mutation and the slice together. A real arc
  lost a slice's work that way. The step now inverts the mutating edit instead (a
  targeted edit of the same hunk, safe whether or not anything is committed), and
  keeps a VCS restore only where `git status --short <path>` was clean *before* the
  mutation. **A project that took 0.26.0 has the dangerous wording installed**;
  updating replaces it, and until then do not run the §5 recipe on a file whose
  slice work is uncommitted.
- **0.28.0 installs one new file and asks nothing of a project without a graph.**
  `.github/hooks/sdlc-impact.py` — the architecture-impact adapter — is kit-owned and
  copied verbatim, so it arrives with the update like the close-out checker. It is
  **inert unless the project carries an Understand Anything knowledge graph**: every
  command that quotes it prints `UNAVAILABLE` and one stated line, and nothing gates,
  fails, or halts on it. That is why it is installed unconditionally rather than
  offered — most projects will never install a graph, the cost is one file, and a
  graph added later works with no re-run of setup, since discovery happens at run
  time. Add the file and the three command mirrors arrive with it; there is nothing to
  prove and nothing to arm. Two things to say at the halt for a project that **does**
  carry a graph: the adapter writes its overlay only into a **git-ignored** UA
  directory (the phase close requires a clean tree and re-asserts it before the merge,
  so a tracked UA directory gets the summary and no overlay, stated); and the view is
  a **comprehension aid, never verification** — nothing it prints enters gate truth,
  and its summary is deliberately not one of the close-out record's keys, so the
  checker's five-key denominator is unchanged.
- **0.28.1 re-arms the TDD guard's shell dialect on Windows, and it arrives only by
  hand.** 0.25.0 through 0.28.0 shipped a relativization that compared the incoming
  path against a root taken from `$(pwd)`; on Windows the hook shell answers `/d/foo`
  while Copilot CLI sends `D:\foo`, so **every absolute path fell to the *outside the
  repository* arm and was skipped rather than guarded** — logging a line that reads
  like correct behavior. Measured against an adopter's own recorded path: 0.24.0
  denies, 0.25.0–0.28.0 allow. Apply `templates/tdd-guard.template.sh` as a template
  diff keeping the project's three placeholder values, together with the 0.25.0 fixes
  if those are not taken yet. **The Claude/Python dialect is correct and needs
  nothing.** Re-prove the deny afterwards against a path shape from the project's own
  `guard.log`, and read the verdict from the log rather than the probe's exit code — a
  malformed payload makes the guard log a parse error and exit 0, which looks exactly
  like an allow.
- **0.29.0 changes the close-out backstop's log vocabulary, and the change arrives with
  the update.** `.github/hooks/sdlc-close-out.sh` is kit-owned and copied verbatim, so
  unlike either TDD-guard fix this one needs no hand-application. Three behaviour
  changes to state at the halt, all in `stop-check`: commits touching only `spec/` and
  the root kit documents are **skipped before classification** (bookkeeping, never a
  slice — and they were 100% of one adoption's measured firing history); a flag is
  logged **once per commit per session**, with repeats logged as `stop: repeat`; and a
  stop with nothing in its window now logs **`stop: n/a`** rather than `stop: clean`,
  because a control with no reach and a control that found nothing were previously the
  same word. Expect the log to get quieter and more informative at once. **If the
  project's close-out checker note in `spec/SDLC.md` records a fire-proof**, this is the
  close to upgrade that line: 0.29.0's *Records* rule asks for the catch actually seen
  (naming the commit) **and a reach note** — whether the flagged state arises in ordinary
  operation or was constructed for the proof. Hand-fold both, as with every
  `spec/SDLC.md` change; never 3-way-merge that file.
- **0.29.0 also stamps the gate baseline with the commit it was measured at.** The
  recorded value becomes `N @ <short-sha>`. Nothing recomputes it here: the stamp is
  applied at the next `/end-phase`, from that close's own step-2 run. An unstamped
  baseline is not a defect to fix during the update.
- **0.31.0 adds a third TDD-guard licence, and it arrives with the guard's own update.**
  `.git/sdlc-tdd/close-out-license` is the refactor licence scoped to `/end-slice`,
  differing in one way: a test edit does **not** revoke it. It reaches the project
  through the ordinary hook comparison above, in whichever dialect is installed, and it
  requires **no project decision** — nothing changes for a project that never declares
  it, and the refactor licence behaves exactly as before. Two things are worth saying in
  the update summary. First, `/end-slice` §§3, 5 and 6 now name the licence as a
  precondition, so a close-out that used to rediscover it by being denied will not:
  that is the point of the change, and one real arc paid seven re-declarations in a
  single phase without it. Second, **every test edit the close-out licence survives is
  counted in the guard log** — a licence held open past close-out shows up as a large
  count rather than as silence, which is what a review should look for.
- **0.31.0 also changes what `/end-slice`'s `quality:` and `verify:` record lines must
  carry**, and the change is not enforced by the close-out checker. `verify: ran` now
  carries `not exercised: <what, or "nothing">`, and `quality:` carries
  `reuse: <what was searched, and against what>`. The checker is structural-presence-only
  and is unchanged, so **existing records stay valid and nothing fails** — but slices
  closed after this update should carry the new halves. Do not retrofit old commit
  bodies; the record describes the session that wrote it.
- **0.31.1 re-arms every hook launcher that read "not at the root" as "not a repo", and
  most of it arrives only by hand.** Two measured ways to be there, both silent — the
  launchers tested for a `.git` *directory* and exited 0 otherwise. (a) **A Copilot
  session started below the repository root**, on CLI builds 1.0.64 through 1.0.87,
  ran every hook in the session's cwd: no gate, no TDD guard, no backstop, no ledger
  line. 1.0.63 and 1.0.88 start hooks at the root, but the fix does not depend on the
  build. (b) **A linked worktree**, on every build and in both dialects: its `.git` is a
  file, and the guard and backstop kept their state under a `.git/` that is not a
  directory there. (c) **Found while proving the fix, and the most serious of the
  three: the Copilot TDD guard has waved through every absolute-path write on the WSL
  route since 0.25.0.** When Copilot is launched from PowerShell its hooks run under WSL
  bash, where the guard's root reads `/mnt/d/…`; 0.28.1's second candidate root comes
  from `pwd -W`, which exists only in Git Bash — so a `D:\…` path matched neither and
  was logged *"write outside the repository - not production source"*. Measured live
  2026-09-27, deny armed: the Git Bash launch denied, the PowerShell launch of the same
  build let the write through. Read the project's `guard.log` for that line against an
  in-repository path: each one is a write the guard should have judged. State the
  consequence plainly at the halt: **on an affected route,
  those controls may never have run, and nothing said so.** What changed: every Copilot
  entry carries `"cwd": "."`; every test is `[ -e .git ]`; the scripts resolve the git
  directory from a worktree's `.git` file themselves (translating a Windows `D:/` path
  under WSL, where WSL's own git cannot follow it); each stop launcher blocks once,
  naming a missing script, where it used to exit 0 — a hook's exit code reaches only
  Copilot's session log, never the agent (measured); and the skill ledger's body moved
  out of the Copilot JSON into `.github/hooks/sdlc-skill-ledger.sh`, which both CLIs now
  share. **Arrives with the update:** `.github/hooks/sdlc-close-out.sh` and
  `sdlc-close-out.json` (kit-owned). **By hand, all project-owned:** on Copilot, replace
  `sdlc-gate.json` and `sdlc-tdd-guard.json` from their templates (no values), apply
  `templates/tdd-guard.template.sh` as a template diff keeping the three placeholder
  values, and — where the ledger is installed — install `templates/skill-ledger.template.sh`
  → `.github/hooks/sdlc-skill-ledger.sh` **before** replacing `sdlc-skill-ledger.json`,
  because the new JSON is only a launcher for that script and says so, loudly, when it
  is missing. On Claude Code, apply `templates/tdd-guard-claude.template.py` as a
  template diff keeping the three values, replace the `Stop` block's close-out command
  from `templates/settings.template.json`, and replace `sdlc-skill-ledger.sh` with the
  shared body (it now falls back to its working directory when `CLAUDE_PROJECT_DIR` is
  unset). **No state moves**: in an ordinary checkout every path — licences, deny
  flags, logs, the ledger — resolves exactly where it did. **But state is per-worktree**:
  a linked worktree has its own git directory, so deny armed in the main checkout does
  not arm a worktree. Re-prove afterwards the way the defect hid, **from each launch
  route the team uses** — on Windows both Git Bash and PowerShell, since (c) existed on
  the PowerShell route only: with deny armed, start a Copilot session in a
  subdirectory, ask for an edit to an in-repository production file by its **absolute**
  path, and read the verdict from `guard.log`; where the team uses worktrees, repeat in
  one (armed there); on Claude Code, repeat from the operator's own launch route. Then
  fold into `spec/SDLC.md` by hand: the guard note says what `.git/` means in a worktree
  and that the flag is per-worktree (the template's guidance now asks for both), and —
  where the ledger is installed on Copilot — the ledger note names the shared body
  `.github/hooks/sdlc-skill-ledger.sh` beside the JSON, since that pair is now what
  makes "installed" true.
- **0.31.2 fixes a regression 0.31.1 put into both TDD-guard dialects, and it arrives only
  by hand — the instantiated guard is project-owned.** A harness that pins
  `SDLC_REPO_ROOT` to a directory with no `.git` (a project's own guard tests typically
  do, with a bare temp directory) got **no guarding at all** under 0.31.1, silently;
  0.31.2 restores the pre-0.31.1 behavior. Real hook invocations were never affected. Apply
  the 0.31.1 → 0.31.2 template diff to the installed guard, keeping the three placeholder
  values and any local amendments; a project taking 0.31.1 and 0.31.2 in one hop applies
  the combined diff. **If the project has its own guard tests, run them** — that is how this
  was found.
- **0.31.3 makes the Claude-dialect hooks stand down under Copilot, which also reads
  `.claude/settings.json`.** It matters only to a project with both dialects' hooks
  installed; a single-CLI project applies it for currency and sees no change. The
  close-out checker is kit-owned and replaced as usual. The Claude guard
  (`.github/hooks/sdlc-tdd-guard.py`) and the Claude gate body
  (`.github/hooks/sdlc-gate-claude.sh`) are instantiated, so their change arrives **by
  hand**: apply the 0.31.2 → 0.31.3 template diff to each, keeping the placeholder values
  and any local amendments. **Then re-prove both from a Claude Code session** — a
  deliberate lint error must still be refused by the gate, and the guard's proof step
  must still catch — because a hand-apply that drops the `permission_mode` clause
  silences both controls in every Claude Code session. On a both-dialect project, also
  make one edit from a Copilot session and confirm `guard.log` holds the Copilot guard's
  line and no Claude-guard line; and tell the owner the one thing no script can fix — a
  Copilot contributor needs `python` on PATH, because an erroring PreToolUse launcher
  denies the edit under Copilot — handing them the line to fold into `spec/SDLC.md`
  beside the guards' installed note.
