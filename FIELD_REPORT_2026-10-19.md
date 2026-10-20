# Field report (kit 0.33.0, Phase 01 of a TypeScript adoption): 9 findings — the controls observe proxies, not the facts they guard

**Source:** [sdlc-kit#17](https://github.com/ghostpencil/sdlc-kit/issues/17), filed
2026-10-19 — the **eleventh** field report, and the first from the third adopter: their
first feature phase, produced by `/sdlc-retro`. Written against **0.33.0**, which is what
the arc ran on. It cites issues #13–#16 (filed mid-arc by the same adopter) as its own
field data, and #11 and #15 from the first adopter. **Generalized here**, as the first
adopter's reports are: the findings, evidence and numbers are as measured, but the
project name, its paths, its commit SHAs, its PR and CI run numbers, its library names,
and its backlog and decision identifiers are removed. The issue body itself is
un-anonymized; where the two disagree the issue is right. `#N` below always means a kit
issue. The triage lives in `FEATURE_PLAN.md` §84, together with #11–#16.

**Read the triage before acting on the priority table.** Two fixes would break something
as filed: finding 1's "classify on the leading executable" breaks every wrapper (`uv run
pytest`, `npx vitest`), and finding 3's launcher prefix (from #13) denies every edit on
Copilot, which runs the same `.claude/settings.json` through PowerShell. Finding 5's
first fix is closed by §83 GRAPH, finding 6 needs its reason restated, and finding 8's
alternative has no CI template to edit. The triage also adds the guard's **worse**
direction, which this report's theme predicts but its examples miss: a read-only command
naming the runner records a false GREEN. §84.2 and §84.4 have each one.

---

**Adopter profile.** A multi-tenant website generator: a TypeScript 6 pnpm monorepo on
Next.js 16, Claude Code only, developed on Windows 11 with Git Bash hooks.
**Adoption:** kit 0.33.0, New Project mode, 2026-10-15. Every guard was armed at
setup, ahead of the recommended ramp. 0.33.0 is still the latest kit release. Upstream
`main` is 3 commits ahead with planning only (§82 COSMETIC), so every finding below stands
against the current kit.
**Window:** the first feature phase. It produced 11 slices (S1–S11, as planned), one
hook-fix commit, one hook patch, one CI-only test fix and the whole-arc fix batch. It
merged as one PR: 116 files, +7,228/−125, 29 commits.

**Headline numbers, measured today:**
- **Gate:** green on `main`: 0 lint / 0 type / 0 test failures, 216 tests in
  18 files. The recorded baseline is `0` at the fix batch, so it is unchanged and was zero
  throughout.
- **CI:** green on `main`.
- **Coverage floor:** set at the close to 99/97/99/90 (lines/statements/functions/branches),
  just under CI's 99.45/97.64/99.05/90.95.
- **Records:** 11/11 slice commits carry all five evidence lines.
- **Backlog:** 18 entries were opened in the phase and 10 are closed.
- **Friction log:** 12 entries were opened and none were absorbed before this retro.

Evidence sources:
- `git log` (slice commit bodies)
- `spec/PROJECT_INDEX.md` and `spec/PROJECT_INDEX_HISTORY.md`
- `.git/sdlc-skill-ledger.jsonl`, `.git/sdlc-tdd/guard.log` and `.git/sdlc-close-out/log`.
  All three were read from the **owner's clone**, which is the
  only clone the arc ran on.
- The session transcripts
- The kit's open issues #11 and #13–#16, and `FEATURE_PLAN.md` §81 and §82 on `main`.
  The co-development clause applies because §82.9 names this project.

---

## 1. The TDD guard decides what ran from the command's text and what happened from the exit code

**Severity: HIGH.** A licence-granting RED was recorded with no test running. The owner
rates this the top issue of the phase.

**What happened.** The guard classifies a Bash call as a test run by substring-matching
the command (`TEST_CMD_PATTERN = "*vitest*|*pnpm*test*|*npm*test*"`). Once a call is
classified, it counts **any** failing exit as a RED. Five recorded failure shapes in one
phase:

- **False RED that licensed a write (S6).** pnpm's deps-status check failed
  (`ERR_PNPM_IGNORED_BUILDS`) before Vitest started. The friction log says it "was counted
  as a licence-granting RED". Filed as ghostpencil/sdlc-kit#16.
- **False RED from wrong arguments (S4).** A bare `pnpm --dir <path> vitest run …` failed on
  its arguments ("Command not found", exit 1) and "an environment failure registers as
  test evidence". The slice re-observed the real red by hand.
- **False RED from a crash (S9).** A config-less `playwright test` "crashed collecting
  Vitest files and was counted as RED". This was recorded as an environment failure.
- **Text misreads, refused only because the command was compound.** These were a `git commit`
  heredoc naming "pnpm … test-isolation", `gh api repos/pnpm/action-setup/releases/latest`,
  `cat … vitest.config.ts`, and the S11 commit body naming `pnpm test:e2e`. **It recurred
  twice in this retro session:** two read-only `sed`/`grep` calls naming
  `vitest.config.ts` were announced as "that test run was NOT counted". They were saved only
  because each command also happened to contain a `;` or `|`.
- **A quoted `|` read as a pipe (S10).** `pnpm vitest run <file> -t "gallery|About"` was
  refused as compound.

**Evidence.**
- Kit friction log entries 2026-10-15, 2026-10-18 (two) and 2026-10-19 in
  `spec/PROJECT_INDEX.md`.
- `guard.log`: 1,167 lines and 76 `compound` refusals.
- The guard source (installed copy, identical to the template apart from its resolved
  placeholders), `observe-test` branch:

  > `probe = re.sub(r'"[^"]*"|\'[^\']*\'', " ", cmd)` / `if not cmd or not match_any(probe, TEST_CMD_PATTERN):`

  and in the failure branch, once an exit-code header is found:

  > `code = m.group(1)` / `mark("red-observed")` / `log("RED observed (exit %s): %s" % (code, cmd))`

The quote-stripping fixed quoted commit messages. It does not cover heredoc bodies, file
*names* such as `vitest.config.ts`, or a `|` inside quotes, which the compound check still
reads raw by design. Nothing distinguishes "the runner ran and a test failed" from "the
wrapper failed before the runner started". A RED is the event that licenses production
writes, so this is the guard's highest-stakes signal, and its evidence is the weakest the
hook has: a non-zero exit from anything whose text mentions the runner.

**Kit text implicated (every home):**
- `templates/tdd-guard-claude.template.py`: the `observe-test` mode, quoted above.
- `templates/tdd-guard.template.sh`: the Copilot dialect. It shares the pattern variable and
  should be checked for the same exit-code rule.
- `templates/SDLC.template.md` *Records*, TDD_GUARD_NOTE rule 1. Quoted from the
  instantiated `spec/SDLC.md`: "A test run registers only as a **single bare command** — no
  `;`, `&` or `|` (flags and single-test selectors are fine)". The rule says nothing about
  what makes a failing run a RED.

**Fix.**
1. Classify on the command's **leading executable and sub-command**, not on a substring
   anywhere in the text. `cat`, `sed`, `grep`, `gh` and `git` never run tests.
2. Count a RED only when the runner's **own** output shows it ran (Vitest's `Test Files`
   / `FAIL` summary, pytest's `failed`/`error` summary line). A failing exit without it is
   logged as "environment failure, not counted" and said out loud.
3. Parse quotes before the compound check, so that `-t "a|b"` is one argument.

#16 already carries finding 2's field data. This report adds the S4/S9 recurrences and the
retro-session misreads.

## 2. Writes through the shell tool bypass the TDD guard and the edit-time hook, and no kit rule forbids them

**Severity: HIGH.** One slice's TDD ordering could not be verified. The owner calls it "a
real risk: it didn't trigger the TDD hooks at all".

**What happened.** In S6 the agent made about **13 production writes and about 15 test
edits through shell scripts** (python, sed, heredoc). The guard and the edit-time
lint/format/typecheck hook saw none of them. The owner caught it, not a control.

**Evidence.**
- Kit friction log, 2026-10-18 entry: "The kit states no file-editing rule, and auto-mode
  guidance permits shell edits. Filed as a comment on ghostpencil/sdlc-kit#16; agent
  memory now forbids it".
- The only defence since is an agent-memory file (`no-shell-edits-to-repo-files.md`),
  which is a per-machine claim and not a control.
- **The harness actively pulls the other way.** Claude Code's auto-mode system text tells
  the agent it may "make small, mechanical file changes with sed, heredocs, or short
  scripts instead of the dedicated Read, Edit, or Write tools". A kit that stays silent
  loses to an instruction that speaks.

**Kit text implicated.**
- `reference/GATE_RECIPES.md`, *What these guards are not*: "the generated `spec/SDLC.md`
  must say so: writes made through the shell tool are invisible to G1". The kit
  **documents** the hole and stops there.
- Its instantiated home, `templates/SDLC.template.md` TDD_GUARD_NOTE. Quoted from
  `spec/SDLC.md` *Records*: "What they are not: a cooperative backstop, not a security
  boundary — writes through the shell tool are invisible to G1".
- `templates/CLAUDE.template.md` *Always-Active Rules*: no rule about how files are edited.
  The silence sits between "TDD required (tests first)" and "Small steps only".
- `commands/next-slice.md` §4 (the TDD loop) does not name the edit tools either.

**Fix.**
1. Add a rule to `templates/CLAUDE.template.md` *Always-Active Rules* and to the
   TDD_GUARD_NOTE: "Repository files are edited only through the agent's edit tools
   (Edit/Write, or Copilot's edit/create). A shell write is invisible to the guard and to
   the edit-time gate hook". Say in the same rule that it **overrides** harness guidance
   permitting shell edits.
2. Detection. On PostToolUse `Bash|PowerShell`, compare a cheap tree fingerprint (the
   `git status --porcelain` hash, or #15's mtime walk) before and after the call. Log a
   change to a `SOURCE_GLOB` or test path as `VIOLATION shell write`, and say it out loud.
   The guard cannot stop it, but it can stop being blind to it.

## 3. The shipped hook launchers and edit-time gate hook generate false blocks: both patched locally, both still in 0.33.0

**Severity: MEDIUM.** It cost dozens of false blocks across S1–S4 and two local patches. It
has not recurred since the patches.

**What happened.** There were three defects:

- **Launchers resolve their path from the session's working directory.** A Bash `cd`
  into a subdirectory made every hook fail with a blocking "can't open file". It recurred 5×
  in S1, including a false "close-out script is missing" Stop message. Fixed locally
  with a `cd "${CLAUDE_PROJECT_DIR:-.}" || exit 2;` prefix on all seven launchers.
  Filed as #13.
- **The gate hook type-checked the whole project after every write.** In S4 it blocked 20
  times in about 35 edits and none was a defect. 11 came from the TDD red itself (8 of those
  named the wrong file) and 9 from editing a consumer before its provider. The hook also
  **missed** the session's one real gate failure, a Prettier failure. Fixed locally: a
  per-tsconfig `tsc`, blocking only on errors in the edited file, plus
  `prettier --check`. Filed as #14 with a 13-case proof.
- **The hook lints files outside the repository.** A scratchpad probe failed with "ESLint
  couldn't find an eslint.config". This is the same scope gap as #15 finding 2b.

**Evidence.** Kit friction log entries 2026-10-16, 2026-10-17 and 2026-10-18 (scratchpad
lint), and the `spec/SDLC.md` *Records* "Project patch 2026-10-18" paragraph. The patch's
reach note: "observed catching ordinary edits 2026-10-19 … a Prettier violation … and a
`prefer-const` error, both real".

**Kit text implicated:** `templates/settings.template.json` (the launcher shape) and
`templates/claude-gate.template.sh` (the hook body).

**Fix.** Adopt the two local patches, whose proofs are on #13 and #14, and skip any edited
path outside the repository root. This adoption confirms what #13–#15 report from another
project. Two adopters and two operating systems have now hit the same three defects.

## 4. The edit-time hook and the TDD guard pull against each other on a formatting-only test edit

**Severity: MEDIUM.** It happened once, at the phase close, and cost one denial plus a
re-observed red.

**What happened.** Right after an observed red, the edit-time hook demanded a Prettier
re-wrap of the test file. The guard reads any test edit as a new cycle and reset the red,
so the next production write was denied (`guard.log` lines 1064–1065). The friction log
puts it this way: "the hook's own fix and the guard's rule pull against each other".

**Kit text implicated.** `templates/tdd-guard-claude.template.py`: a `pre-write` on a
test path clears the red with no notion of a cosmetic edit. `commands/end-slice.md`
step 5 already warns about one hook-vs-guard collision ("The two controls have no
knowledge of each other by design"), but only for unused-variable mutations.

**Fix.** Kit plan §82 (COSMETIC) has ruled the direction and names this project as its
TypeScript canary (§82.9), but the build has not started. This report is field data for
it, not a new design. Until it ships, add one line to `/end-slice` step 5's collision
paragraph. It should say that a formatting fix the hook demands on a test file after its
red resets the red, so the fix belongs **before** the red run, not after it.

## 5. The per-slice graph refresh is written as mandatory, was skipped at all 11 slice closes, and the skip never reached the friction log

**Severity: MEDIUM-LOW.** The owner ruled the skip fine for this project, so no damage
was felt. A mandatory step bypassed every single time is still either wrong or
unenforceable.

**What happened.**
- The Understand Anything graph was built at setup (33 files) and refreshed
  next after the merge (122 files). That is 0 refreshes in 11 slice closes.
- Every hand-back stated the skip with a cost reason. Session transcripts, in order of
  growing debt: "15 files behind", "67 files stale", "76 files stale", "95 files", "99
  files", "102 files stale", "107 files behind", "115 files behind". One added: "a plain
  incremental `/understand` can't add files (kit issue #11). Only `/understand --full`
  would, and that spends a lot of tokens".
- At the phase boundary the tool's planner returned `FULL_UPDATE` (104 of 122 files
  changed).
- The impact view read `PARTIAL` at every site that draws it for the whole phase (for
  example, `changed-files: 12 / mapped-files: 6` at one close).
- The owner's ruling at this retro: **fine to skip**. The view was not worth a
  multi-agent run per slice here.

Each skip was a legitimate stated skip. But the **same skip for the same reason, 11 times
in a row, never became a friction line**. `/end-slice` step 9's prompt ("Was anything in
this slice friction with the *process*…?") was answered no each time, because a stated skip
does not read as friction from inside one slice.

**Kit text implicated (every home):**
- `commands/end-slice.md` step 10: "**Then refresh the graph — last, and only after the
  base is cleared.**"
- `templates/SDLC.template.md` *Architecture impact view*, quoted from `spec/SDLC.md`:
  "**Regenerate the graph at every slice end and at the phase boundary — those are the
  triggers, and they are this process's, not the graph tool's.**" The same section prices
  it as cheap: "An incremental run re-analyses only changed files … about 160 s".
  `FEATURE_PLAN.md` §81 rests on the same assumption. It holds only for a graph that is
  already current **and** only for files the graph already knows, which issue #11 shows is
  not true for new files.
- `commands/end-slice.md` step 9, *Kit friction gets written now or never*: the silence
  is that it has no rule turning a **repeated** stated skip into friction.

**Fix.**
1. Make the slice-end trigger an owner choice recorded at setup ("slice end" or "phase
   boundary only"), with the PARTIAL consequence stated next to the choice.
2. When `/next-slice` finds the graph more than a threshold of files behind, say so once
   and halt for the owner's choice, instead of re-deferring at every close.
3. Mirror the Environment-gotchas escalation in step 9: **a step skipped for the same
   reason in three consecutive slices is friction** and gets a line, whatever the
   per-slice verdict was.

## 6. `/end-slice` step 5 says "confirm green" without saying the gate is not a counted green

**Severity: LOW.** It blocked Stop twice (S2, S3). The cause was re-derived and measured
on 2026-10-18 as the session's fault, not the guard's.

**What happened.** After mutation checks, the session restored the mutation and confirmed
green with `pnpm gate`. Rule 1 says the gate is not counted, so the stop guard had no
green and blocked.

**Evidence.** Kit friction log, 2026-10-16 entry (re-derived 2026-10-18 from `guard.log`
lines 300–326): "The guard behaved as specified, so don't change it … Fix: confirm every
manufactured red with a counted bare run".

**Kit text implicated.** `commands/end-slice.md` step 5: "delete or invert it once, run
the suite, and watch it fail on exactly the test that claims to pin it — then restore and
confirm green". The rule that makes the obvious confirmation not count lives in a
different file: `templates/SDLC.template.md` *Records*, TDD_GUARD_NOTE rule 1, "`pnpm
gate` is not counted" (instantiated wording).

**Fix.** In step 5, change "confirm green" to "confirm green with a counted bare test run
(where the TDD guards are installed, a gate run is not counted)".

## 7. The process is silent on library approval: where it is asked, and where the answer is recorded

**Severity: LOW.** No damage. The owner names it as the phase's one place where a
decision was made with nothing to go on.

**What happened.** Six libraries were approved during the phase (a schema validator, a browser test runner and its accessibility plugin, a dependency
linter, a logger and a TS script runner, approved 2026-10-16/18). The
approvals went into the phase spec's decisions and an ad-hoc line in
`spec/PROJECT_INDEX.md` *START HERE*: "Approved libraries so far: …". One slice deferred a
verification because "no TS script runner is installed (adding one needs library
approval)" (S4's `verify:` line). That is the cost of having no defined moment to ask.

**Kit text implicated.** `templates/CLAUDE.template.md` *Always-Active Rules*: "No new
libraries without approval". This is the only mention anywhere in the kit's commands and
templates (`grep -i librar` over `.claude/commands/` and the templates finds no other).
The silence sits between `commands/plan-phase.md` (which settles the phase's decisions)
and `commands/next-slice.md` §4 (where the need surfaces).

**Fix.**
1. `/plan-phase` lists the libraries the phase needs as ratified decisions.
2. `/next-slice` halts (as an owner question) when a slice needs one that is not listed.
3. Give the approved list one home: a *Records* line, per the index's own one-number-one-home
   rule.

## 8. The draft-PR-for-CI case has no wording; only "never open a PR here"

**Severity: LOW.** It was a one-time deviation, and the phase decision was followed.

**What happened.** A ratified Phase 01 decision required a draft PR right after S1's first
push, so that CI ran on the arc. The kit forbids opening a PR at slice close and does not
mention a draft opened for CI.

**Evidence.** Kit friction log, 2026-10-16 entry: "the phase decision was followed, with
no kit wording for a draft-PR-for-CI exception".

**Kit text implicated (both homes):**
- `commands/end-slice.md` *Notes*: "Push the branch (`git push`) so work is not stranded
  locally, but never open a PR here — that is `/end-phase`."
- `templates/SDLC.template.md` *Slice loop* (line 856 of the template; 990 of the
  instantiated copy): "Push the branch (no PR — that is phase end)."

**Fix.** Allow the draft PR in both homes: "a **draft** PR opened only so CI runs on the
arc is not this; `/end-phase` marks it ready". Alternatively, run CI on `feat/**` pushes
in the CI template so no draft is needed.

## 9. The phase-scope impact view counts untracked files

**Severity: LOW.** One manual reconcile at the merge halt.

**What happened.** `sdlc-impact.py phase` read `changed-files: 133` against a committed arc
of 116 files, because untracked `.idea/` and `sh.exe.stackdump` were counted.

**Kit text implicated.** `templates/sdlc-impact.template.py`, `change_set()` (the installed
copy is byte-identical): "Committed since base, staged, unstaged, and
untracked-but-not-ignored. A slice that committed mid-way is covered by the first; a slice
mid-flight by the rest." That is right for a slice in flight. At phase scope, the arc is
committed and sits at the merge halt, so untracked files are not part of it.

**Fix.** At `phase` scope, either drop the untracked source or report it as a separate
`untracked-files:` line outside the denominator.

---

## What worked well

Every catch cited here has its disposition attached.

- **Mutation check (end-slice step 5).** It ran in all 10 code slices and caught weak
  tests three times:
  - **S2:** a `missingProperty` path suffix "survived until a field-path pin
    was added". Fixed.
  - **S6:** the path allow-list mutant "survived first; test strengthened, then caught".
    Fixed.
  - **S7:** 2 survivors were dead branches and were removed. Fixed.

  This happened with **zero** `mutation-testing` skill dispatches. The rules restated in
  step 5 carried it, exactly as step 5's own note predicts.
- **Review lenses.** They produced six backlog entries, five of them fixed:
  - Verify-the-denominator: one entry (cross-package layering not enforced). Fixed.
  - Untrusted input: two entries (raw tenant strings echoed). Fixed.
  - Logging: one entry (two failure signals reached no log). Fixed.
  - Consumers: one entry (ENOENT crash instead of a coded error). Fixed.
  - **Untrusted input: one entry (the schema validator's `allErrors` over unbounded
    input) is still open**. See open
    damage below.
- **Whole-arc review.** It produced 10 findings: a spec conflict (the build log
  carried no ids), one MEDIUM (SVG shipped through two media tables) and 8 LOW. All were
  fixed in the fix commit by owner ruling, with 0 deferred.
- **Evidence lines plus the close-out checker.** All 11 slice commits carry `RED:`,
  `quality:`, `lenses:`, `mutation:` and `verify:`. Every `quality:` line names its `reuse:`
  search and every `verify:` line carries `not exercised:`, which are the two halves a
  previous adopter lost. This retro's step-evidence sweep could be done from `git log`
  alone.
- **Owner workaround that paid off: patching the kit hooks locally**
  instead of waiting for upstream. Both patches are proven, and neither defect has recurred.

**Open damage:** that one backlog entry. The untrusted-input lens caught it in S2 and it is still open,
deferred by owner ruling until tenant-authored input reach the validator.

## Step evidence

The ledger was read from the owner's clone. It is alive: 42 lines, 2026-10-16 → 2026-10-19.

| Named step | State |
|---|---|
| TDD loop (`tdd` skill) | **ran**. 11 ledger lines: S1–S10 and the phase-end fix batch. S11 was docs-only. |
| Observed RED | **ran**: `RED:` lines in 11/11 slices (S11 uses the zero-form). **Caught:** the guard counting wrapper failures as RED in S4 and S9, each recorded and re-observed (finding 1). |
| Quality pass (`change-simplify`) | **ran**: 10/10 code slices (10 ledger lines), with moves applied in 8. S11 **skipped with reason** (docs-only). |
| Slice review (`diff-review`) | **ran**: 12 ledger lines (11 slices plus the whole arc). **Caught:** twelve backlog entries. |
| Review lenses (`REVIEW_LENSES.md`) | **ran**: a `lenses:` line in 11/11, read as a file per `/end-slice` step 4. The only ledger line is setup's proof, which is expected. **Caught:** six backlog entries. |
| Mutation check | **ran**: 10 code slices. S11 used `none — no new guards`. **Caught:** the S2, S6 and S7 weak tests. The `mutation-testing` skill has **no ledger line**, which the kit expects (rules restated in step 5). |
| Slice verification (`change-verify`) | **ran** in 8 slices and **skipped with reason** in 3 (S3–S5: "no production caller until S6"). The skill was dispatched in only 4 of the 8 runs (S6, S7, S9, S10). S1, S2, S8 and S11 wrote contract-shaped lines, including `not exercised:`, without it. **Caught:** S8's pre-fix `depcruise` exit 9 on real violations. |
| Close-out record check | **ran**. Every slice record is complete. `check` mode writes no log line, so this rests on the records themselves and the hand-backs. |
| Docs budget observer (`docs-check`) | **ran**: 13 log lines. **Caught:** one `OVER` (S6, 28/25). |
| Stop-time backstop | **ran**: 110 stop lines. Only 4 were WOULD-BLOCK, all of the log-only bare class (setup, graph and hook chore commits) and none on a slice commit. The reach note is still "constructed". |
| Edit-time gate hook | **ran**. **Caught:** a real Prettier violation and a `prefer-const` error at the close. There were also about 35 false blocks before the patch (finding 3). |
| Architecture impact view | **ran**: `sdlc-impact.py` appears in 17 session transcripts. It read PARTIAL throughout because the graph was stale (finding 5). |
| Graph refresh at slice end | **skipped with reason**: 11/11, cost. The owner ruled the skip fine at this retro. It **ran** once at the phase boundary. |
| Phase-level verification | **ran**: `change-verify` ledger line at 2026-10-19T11:34Z, after the S11 commit. |
| Owner acceptance (halt 4) | **ran**: items 1–10 met. |
| Whole-arc review | **ran**. **Caught:** 10 findings, all fixed in the fix batch. |

## Suggested priority

| # | Change | File(s) | Effort |
|---|---|---|---|
| 1 | Classify test runs by leading executable, count RED only on runner-produced output, and parse quotes before the compound check | `templates/tdd-guard-claude.template.py`, `templates/tdd-guard.template.sh`, `templates/SDLC.template.md` (rule 1) | M |
| 2 | Add an "edit repo files only with edit tools" rule that overrides harness guidance, and detect shell writes post-hoc | `templates/CLAUDE.template.md`, `templates/SDLC.template.md` (TDD_GUARD_NOTE), `reference/GATE_RECIPES.md`, `templates/tdd-guard-claude.template.py` | S (rule) + M (detection) |
| 3 | Ship the cwd-anchored launchers and the per-file gate hook (#13, #14), and skip out-of-repo paths | `templates/settings.template.json`, `templates/claude-gate.template.sh` | S (patches exist) |
| 4 | Build §82 COSMETIC. Meanwhile, one line in step 5's collision paragraph | `templates/tdd-guard-claude.template.py`, `commands/end-slice.md` | L / S |
| 5 | Make the slice-end graph refresh an owner choice at setup, halt once when the graph is far behind, and turn a repeated skip into friction | `commands/end-slice.md` (steps 9, 10), `commands/next-slice.md`, `templates/SDLC.template.md` (*Architecture impact view*), `commands/sdlc-setup.md` | S |
| 6 | "Confirm green with a counted bare run" in step 5 | `commands/end-slice.md` | XS |
| 7 | Library approval: ratified at `/plan-phase`, halted on at `/next-slice`, one home for the list | `commands/plan-phase.md`, `commands/next-slice.md`, `templates/CLAUDE.template.md` | S |
| 8 | Draft-PR-for-CI wording in both homes | `commands/end-slice.md`, `templates/SDLC.template.md` | XS |
| 9 | Phase-scope `change_set()` excludes untracked files, or reports them separately | `templates/sdlc-impact.template.py` | XS |

## Cross-cutting theme

**The controls observe proxies instead of the facts they guard.**
- The TDD guard infers "a test ran" from the command's spelling and "it failed" from any
  non-zero exit (finding 1).
- It infers "nothing was written" from the absence of an Edit/Write call (finding 2).
- It infers "a new cycle began" from any test-file write, including a formatting fix
  (finding 4).
- The impact view infers "the arc's files" from the working tree (finding 9).

Each proxy holds on the happy path, and each one failed this phase in exactly the case a
control exists for. If only one thing is taken: **have the guard observe effects** (the
runner's own output, the tree's actual change), not the agent's description of what it did.



