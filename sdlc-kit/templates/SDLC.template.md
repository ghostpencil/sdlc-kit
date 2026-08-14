# {{PROJECT_NAME}} — SDLC

**Scope: {{SDLC_SCOPE}}**
<!-- What this process governs and what is explicitly out of scope. "The whole repo" is
     the common answer; a mixed repo (app + docs, app + infra, monorepo packages) names
     the boundary here so no session has to guess it. -->

Canonical description of the development process. The commands `/plan-phase`,
`/next-slice`, `/end-slice`, and `/end-phase` (installed project-scoped by
`/sdlc-setup`, so they travel with the repo) automate it; if
this file and a command disagree, this file wins — fix the command.

Commands state nothing project-specific; every project fact lives in this file. Anything
here that a command would need to know — the gate commands, the gate baseline, the scope
of this process — is recorded below and read from here.

**Kit version:** {{KIT_VERSION}} (adopted {{ADOPTION_DATE}} — a claim whose evidencing
artifact is the adoption commit; on disagreement the commit wins). Update procedure:
`/sdlc-update` (installed with the commands; the kit's home repository README states the
same procedure). **Kit home repository:** {{KIT_HOME_REPO}} — the URL `/sdlc-retro`
submits upstream reports to, recorded here so acting on a submit decision never needs
a second question.

---

## Shape

Work is organized as **phases → slices → TDD cycles**.

- A **phase** delivers one feature or a set of related features. It lives on one branch
  (`feat/phase-NN-<slug>`), has a spec (`spec/PHASE_NN_*.md`) that breaks it into slices,
  and ends in a single PR to `{{MAIN_BRANCH}}`.
- A **slice** is one coherent behavior within a phase — small enough for a single session.
  Each slice is built test-first, reviewed, committed, and recorded before context is cleared.
- A **TDD cycle** is one red–green–refactor step inside a slice.

During **STABILIZATION** there are no feature phases; the same slice loop applies to
bug-fix/cleanup slices on a cleanup branch named for the arc's theme
(`chore/cleanup-<arc-theme>` — not for whichever slice happens first).

**One arc, one branch, one PR — in both modes.** Slices accumulate on the arc branch
until `/end-phase`; only `/end-phase` opens a PR. Work arising from a slice's own
review stays on the same branch. Splitting an arc across branches forfeits the single
whole-arc review — the stage that catches what slice reviews structurally cannot.

**The hotfix exception — the only sanctioned second unmerged branch.** An urgent
production fix that cannot wait for the open arc branches `fix/<slug>` off
`{{MAIN_BRANCH}}`, gets its own minimal PR (gate green against the recorded baseline,
review scaled to the diff, merge approval as ever), and its own Phase History row — it
is not a slice of the arc. After it merges, the arc branch merges `{{MAIN_BRANCH}}`
and re-runs the gate before its next slice, so the arc never drifts silently from what
production runs.

**Parallelism is read-only fan-out only.** Slices are strictly sequential — their order
is set at planning time and inter-slice dependencies are the norm. Subagents may run in
parallel only for read-only work *within* a step (analysis sweeps, repo surveys, review
lenses), made safe by tool restriction; never for implementation, never across slices.
Findings return to the main session, and every owner interaction happens there —
subagents cannot ask the owner anything, so no halt point ever moves into one.
Where the CLI in use cannot fan out in parallel, the same sweeps run one after another:
the coverage is identical, only the wall-clock differs. A sweep dropped for time is a
sweep that did not run, and is reported that way — never as a sweep that found nothing.

## Owner halt points

The process runs autonomously except at these five points. Everything else (gates, reviews,
fix application, bookkeeping, commits) proceeds without asking. Autonomy runs *within*
a command, never across the boundary between commands: each command in the daily loop
is owner-typed, and `/next-slice` in particular ends at the slice-ready hand-back
rather than chaining into `/end-slice` (see *Slice loop*).

1. **Phase scope** — the owner decides what the next phase (or cleanup slice) covers.
   Recorded as OWNER-DECIDED in `spec/PROJECT_INDEX.md` START HERE.
2. **Slice scope confirmation** — one question at the start of `/next-slice`. Skipped
   when the slice is already recorded as OWNER-DECIDED with its scope spelled out;
   re-asking a decided question is ceremony, and the halt exists for the undecided case.
   The skip lapses when the slice's re-derivation contradicts what was decided — a
   backlog cause that does not hold, or an **estimated** number that derives differently
   — because what was decided is no longer what is true.
3. **Design questions** — any spec conflict or owner-facing design decision surfaced
   during the work, mid-slice or by a review, halts with a question; it is never
   resolved silently. A review finding that contradicts a **ratified spec decision**
   is a spec conflict and takes this halt — fix the code now, or amend the decision
   it contradicts — never a backlog line by default: a decision the owner ratified
   does not get un-decided by deferral.
4. **Acceptance review** — the owner personally exercises the phase's visible behavior at
   phase end ({{ACCEPTANCE_SURFACE}}). The agent does not perform this review on the
   owner's behalf. When no slice's exit criteria required running the application — an
   arc behavior-neutral by construction — `/end-phase` first runs the composed system
   locally against real data before the PR: the halt otherwise passes vacuously on a
   phase with no visible behavior yet, which is exactly when nothing has ever run
   outside the test suite. **The run's log output is part of the acceptance
   surface**: read it against the logging conventions recorded in `CLAUDE.md` —
   silence at a boundary the conventions promise (a run that starts, finishes, or
   fails without the log saying so) is a finding, because absence never appears in
   any diff and this halt is the only step that watches the system speak.
5. **Merge approval** — the owner approves the PR merge. A team that routes merge
   approval through a human PR reviewer instead of the owner-in-session records that
   routing here; the reviewer's approval then satisfies this halt, and the merge still
   waits for it.

### The hand-back standard

Every owner-facing moment — each of the five halts above, and the hand-back that ends
each command — opens with an executive summary the owner can act on without reading
further: **plain English, bullet form, a few lines** — what happened, what state the
work is in, what happens next. Every decision the owner is being asked to make is
**numbered and explicitly marked** (`Decision 1: …`), with its options and a
recommendation where one exists — a question buried in a paragraph is a question the
owner was never asked, and an answer to it is a decision that was never made.
Supporting detail (evidence, per-finding dispositions, counts, logs) follows the
summary; it never replaces it and never interleaves with it. The rules elsewhere in
this file make the *agent's* output correct; this is the one that makes it possible
for the *owner* to follow.

## The Gate

"The gate" means all of the following, in order, all green:

```
{{GATE_LINT_CMD}}        # lint
{{GATE_TYPECHECK_CMD}}   # typecheck / compile check — omit only if the language has neither
{{GATE_TEST_CMD}}        # full test suite
```

### Gate baseline

**Baseline: {{GATE_BASELINE}}**

Green means green **against that baseline** — zero for a clean adoption, the recorded
counts for a project adopted mid-flight. Any *increase* is a regression and is fixed in
the slice that caused it, never accepted as a cost. The baseline only ever moves down, as
the STABILIZATION backlog burns it toward zero; when it changes, it is re-recorded here in
the same commit.

A count can also hold still because the checker stopped looking: suppressions, skipped
tests, and constructs that hide code from analysis (an unannotated decorator can type
everything it wraps as `Any`) freeze the number while shrinking what it measures. A
ceiling that stops measuring is worse than a high one — when the count will not move,
check what the checker still reaches, not only what it reports.

**The baseline moves by procedure, not by ambition.** At every phase close, post-merge
bookkeeping reports the current count beside the recorded one and does one of three
things: lowers the baseline here in the same docs commit, records an owner decision to
lower it via a stabilization slice in the next phase, or records that the owner
**ratified holding it** — with how many arcs it has been unchanged. A ceiling nobody is
ever asked about is not a ratchet, and *"drive it down through the backlog"* is a wish
until a step serves it.

**Rendering:** an unchanged red baseline is reported as `N (unchanged for K arcs)`,
never as `N (ceiling held)` or any other phrasing where a stall reads as an
achievement. The same number twelve times is the finding, and it has to look like one.

This is the single place the baseline is defined. Commands read it from here.

The same checks run in CI ({{CI_DESCRIPTION}}). Merges to `{{MAIN_BRANCH}}` require the
CI check green — via branch protection where it is configured, and as a process rule
regardless.

**Coverage floor:** {{COVERAGE_FLOOR}}
<!-- "TBD from first CI run" until one exists. Set just below the first green CI run's
     observed figure (printed, or read from that run's coverage report artifact where
     the check prints only pass/fail), using CI's exact invocation; it only ever
     raises. Lowering it to pass a build defeats its only purpose — existing coverage
     debt is a backlog item, not a merge blocker. -->

The floor raises by procedure, not by rule alone — at phase end, where coverage is
known: if the coverage measured for the merged branch rose over the arc, post-merge
bookkeeping sets the threshold — in whichever artifact carries it: the CI workflow
file, or the build file's check rule where the workflow only invokes the check — to
just under the measured figure (in the same docs commit as the PROJECT_INDEX update),
then asserts that the floor recorded here and in `spec/PROJECT_INDEX.md` is identical
to that threshold value — the bookkeeping is not done until they are. The measured
figure is read off the enforced run's own output: CI's printed number where the check
prints one, else the coverage report artifact the same run produced — a check that
prints only pass/fail yields no printed figure ever, and waiting for one leaves this
leg inert. Reading that artifact is not computing the number locally; re-running
coverage outside the enforced invocation to produce a different number is. The
recorded number is a claim; the threshold value is the enforcement — a mismatch means
the ratchet is not ratcheting, which is the only regression the floor exists to
prevent.

**When the floor is first established, prove it fires — once.** Set it above the
observed number, run the gate's own commands (and CI's, if they differ), and watch
the failure; then set the real value. Two homes agreeing on a number proves nothing
about whether the enforcing step ever *runs* in the commands the gate executes — a
floor bound to a build phase the gate never reaches passes every reconcile and
enforces nothing. Same discipline as the edit-time hook's install proof: a check
that has never been seen to fail is not yet a check.

If local and CI disagree about a measurement — a pass/fail, an error count, a coverage
figure — CI is authoritative. And the disagreement is itself a finding: work out *why*
before adjusting any threshold, because the gap is usually a symptom (a git-ignored
file, an environment difference, a test reaching a real service), not noise to average
away.

An edit-time hook ({{HOOK_CONFIG_PATH}}) runs the lint/typecheck steps on every edited
source file, so most gate failures surface at edit time rather than at slice end.
{{HOOK_FEEDBACK_NOTE}}
<!-- If setup found the hook could not work in this project's hook shell and the owner
     chose not to install one, the two lines above are replaced with that fact and its
     date, and {{HOOK_CONFIG_PATH}} names no file. A process file claiming a hook that
     does not exist is worse than one admitting there is none: the gate is then the only
     check, and every slice close has to carry that weight knowingly. -->

A hook runs in the shell the agent CLI resolves, which is not necessarily the one you
type in — if it cannot reach this project's toolchain it cannot check anything, and a
hook that checks nothing still reads as a gate. What the hook environment measured at
setup: {{HOOK_ENVIRONMENT}}

{{TDD_GUARD_NOTE}}
<!-- Setup resolves {{TDD_GUARD_NOTE}} to a statement of whether the TDD-ordering guards
     are installed, which CLI they run on, and whether they are in logging or deny mode.
     When installed, the note also states the three rules the guards impose on a coding
     session — the note is the proactive statement; the guard's own messages state them
     only reactively, at a refusal or a counted run (field, 2026-08-08 — before the
     guard spoke, a session that met them first as unexplained refusals thrashed and
     probed the guard instead of complying): a test run registers only as a single bare
     command — no `;`, `&` or `|`; flags and single-test selectors are fine; the
     stop guard's green is ANY counted green, full-suite assurance being the end-slice
     gate's job, not the backstop's; and a behavior-preserving edit — refactor,
     simplification, mutation testing, including a temporary mutation to prove a
     test of existing behavior bites, at any point in the cycle, not only at
     close-out — is licensed without a fresh red by declaring it:
     one line naming the step and move to `.git/sdlc-tdd/refactor-license`, valid only
     behind a counted green, revoked by the next test edit, every write under it
     logged. The stop guard is session-scoped (owner-decided
     2026-08-08): it binds only a session that wrote production code or edited a test,
     so a planning, docs, or bookkeeping session stops clean by construction. The note
     also names the artifact that decides the mode (`.git/sdlc-tdd/deny-enabled`,
     present means deny — arming or disarming means updating the line), records the
     proof run that was made to fail, and says `.git/` is per-clone: the flag, state,
     and log describe the machine that wrote the note, not this checkout.
     If they were declined, it says so WITH THE DATE — it does not delete this line. A
     missing line and a declined offer are different facts: /sdlc-update re-offers the
     guards when this project never had the choice, and must not badger an owner who
     already made it. Deleting the record erases the difference.
     The note names the dialect(s) installed — Copilot (`.github/hooks/
     sdlc-tdd-guard.sh` + `.json`), Claude Code (`.github/hooks/sdlc-tdd-guard.py`
     plus the four hook blocks in `.claude/settings.json`) — and on a project running
     both CLIs says which sides are covered; the deny flag and state are shared, so
     arming deny arms every installed dialect. Never describe a guard this project
     does not have. -->

{{SKILL_LEDGER_NOTE}}
<!-- Setup resolves {{SKILL_LEDGER_NOTE}} to a statement of whether the skill-activation
     ledger is installed — a logging-only hook that appends one line per
     TOOL-DISPATCHED skill activation to `.git/sdlc-skill-ledger.jsonl`, so the
     retro's step-evidence sweep can read which named skills actually ran instead of
     trusting that presence meant activation. It runs on both CLIs (the hook fires on
     the skill tool: `skill` on Copilot, `Skill` on Claude Code — measured
     2026-08-07), and the dispatch scoping bounds it: a command the owner types as a
     slash command is injected with no tool call and writes no line (field-measured
     2026-08-11 — four phases of slash-typed slice closes, zero ledger lines), so the
     note must also say that a missing line for a slash-invocable command is no
     signal either way. The note names the hook
     artifact that makes "installed" true (the Copilot hook JSON, the settings-file
     block on Claude Code — adding or removing either later means updating this line,
     because nothing else will), names the ledger
     file, and says in the same breath that `.git/` is per-clone: the ledger records
     this machine's sessions only, and a retro citing it must say whose clone it read.
     If the ledger was declined, the note says so WITH THE DATE — it does not delete
     this line. A missing line and a declined offer are different facts: /sdlc-update
     offers the ledger when this project never had the choice, and must not badger an
     owner who already made it. -->

{{CLOSE_OUT_CHECK_NOTE}}
<!-- Setup resolves {{CLOSE_OUT_CHECK_NOTE}} to the proven invocation of the close-out
     evidence checker (`.github/hooks/sdlc-close-out.sh`, installed verbatim on every
     adoption — it takes no per-project values), one line per installed CLI, each form
     actually RUN at setup against a real commit before being recorded — the same
     discipline as the hook environment note above. `sh .github/hooks/sdlc-close-out.sh
     check` is the default wherever `sh` resolves in the agent's shell tool; measured
     2026-08-10, Copilot CLI's shell tool on Windows resolves no `sh` (and the `bash`
     on its PATH is WSL's, the route that corrupts hook bodies) — there the working
     form derives sh from the git on its PATH, e.g.
     `& '<git-install>\bin\sh.exe' .github/hooks/sdlc-close-out.sh check`, with the
     literal proven path written into the note. A recorded invocation that was never
     run is exactly the silent absence the checker exists to catch. (One sanctioned
     deferral: a brand-new repo has no commit to prove against until setup's own
     close-out makes the initial commit — the proof runs there, still inside setup,
     and the note is finalized in the same breath.) Like its two sibling notes above,
     this line is a claim about the machine and CLIs setup ran on: the proven path
     describes that machine (a teammate's clone re-proves before trusting it), and
     adding a CLI later means adding its proven line — nothing else will.
     THE SAME NOTE also records the stop-time backstop's state — the same script's
     `stop-check` mode wired at agentStop (Copilot, `.github/hooks/sdlc-close-out.json`)
     / Stop (Claude Code, the settings-file block), offered separately and OPTIONAL
     where the checker itself is not. Installed: which CLIs, the fire-proof actually
     seen (which CLI and launcher, the would-block line read back — a recorded
     install whose proof never ran is the silent absence this family catches,
     one layer up), logging or armed
     (the flag file `.git/sdlc-close-out/deny-enabled`, present means armed — arming
     or disarming means updating this line, because nothing else will), and that the log lives at
     `.git/sdlc-close-out/log`, per-clone like everything under `.git/`. Declined:
     say so WITH THE DATE — never delete the line; /sdlc-update reads it exactly as
     it reads the guard note's decline. Unlike the command step above, the backstop
     fails OPEN (a hook that errors must not block work), and its bare-commit class
     is log-only by design regardless of the flag. -->



## Model policy

{{MODEL_POLICY}}
<!-- Owner-confirmed at setup; adjust any time (re-record here when it changes). The
     kit's recommended default is three tiers by task shape: High (`opus`) for
     planning, analysis, and adversarial review; Medium (`sonnet`) for writing code to
     an existing plan/spec; Low (`haiku`) for mechanical collection. Aliases only,
     never model IDs — IDs go stale. On a CLI other than Claude Code the tiers are the
     same and the models are that CLI's own, mapped with the owner at setup.
     Switch any session with /model; the pinned session default, if one was chosen,
     lives in .claude/settings.json ("model") on Claude Code, or in COPILOT_MODEL on
     Copilot CLI, and this section says which. The pin statement here is claim-only
     between edits: nothing reconciles it against the settings file, so whoever
     changes the pin owns updating this line — a policy section describing a pin that
     no longer exists is exactly the drift it looks like.
     Copilot CLI dialect — routing is OPERATOR-PERFORMED: no file the kit installs can
     set the model, so the policy text above must name which commands run at which
     tier (/plan-phase, /end-phase, and /end-slice's review are High at minimum) and
     instruct the operator to set the model — /model in-session, or COPILOT_MODEL for
     a scripted run — BEFORE invoking a High-tier command. A tier policy nobody
     executes is prose; naming the moment it is executed is what makes it a step. A
     tier the owner left on `auto` is recorded as `auto (ratified <date>)` with what
     that forfeits stated beside it. -->

## Phase start

Run `/plan-phase` at a phase boundary (after `/end-phase` post-merge bookkeeping, or when
`/next-slice` finds nothing to slice):

1. Candidate phases presented with a recommendation; owner picks the scope *(halt 1)*.
2. Requirements interview in rounds (≤4 questions each) until a round surfaces nothing
   new, then an adversarial gap analysis (walkthrough, trust-boundary sweep,
   consequence sweep, cross-system sweep, persistence/compatibility sweep, testability
   sweep, contradiction sweep, minimal-version attack — the sweeps may fan out as
   parallel read-only subagents per the rule above). Every gap becomes
   a question or a numbered decision — never an assumption. Two rules bind the
   consequence sweep's hits: a claim that a consequence **ships inert** (flag, env var,
   "off in prod", "merging changes nothing") names the variable and quotes its value
   from the artifact that configures **production** — never from the test environment,
   which is usually configured to make the claim true — and each hit names the lever
   that disables it **alone**, since a control sharing its only off switch with an
   unrelated system has no rollback.
3. Spec written to `spec/PHASE_NN_*.md` only once open questions are resolved: goal,
   numbered owner decisions, behaviors, non-goals, data/migration impact, trust
   boundaries (what the consequence sweep found, recorded), user-visible
   surface + acceptance-review checklist, slices with exit criteria that name **what
   observes them and when** (a criterion naming an observer that does not run at that
   point — CI on an arc branch, typically — is a planning defect), risks. Any decision
   carrying a number is tagged **measured** (naming the run, count, or query behind it)
   or **estimated** — the same distinction the deferred backlog draws about causes,
   applied where a number is first ratified.
4. Owner approves the decisions + slice breakdown *(same halt, second checkpoint)*.
5. Branch `feat/phase-NN-<slug>` created off `{{MAIN_BRANCH}}`; `spec/PROJECT_INDEX.md`
   flipped to BUILD with the spec pointer; docs committed. Then `/clear` and `/next-slice`.

## Slice loop (repeat per slice)

Run `/next-slice` in a **fresh session**:

1. Read `CLAUDE.md` + `spec/PROJECT_INDEX.md`, then the phase spec. Load no other specs
   until needed (context-minimization rule).
2. Identify the next unstarted slice and its exit criteria; confirm scope with the owner
   in one question *(halt 2 — skipped when the slice is recorded OWNER-DECIDED with
   scope)*. If the slice comes from the backlog, **re-derive the entry's stated cause
   before writing any fix, proportionally to its marker** — a `measured` cause gets a
   spot-check that its cited anchors and behavior still hold; a `suspected` cause, or a
   `measured` one whose anchors drifted or whose spot-check surprises, gets the full
   reproduce-or-disprove (and is re-tagged). The reproduction runs where the cause was
   observed: an owner-shell or CI-observed cause cannot be disproved from the agent's
   shell, and a failed reproduction from a different environment downgrades the entry
   to "could not reproduce here", never to a corrected cause. A backlog entry is a
   hypothesis with a timestamp, not a finding; when the cause does not hold **where it
   was claimed to hold**, correct the entry in place
   and re-scope. The same rule covers an **estimated** number the slice implements:
   derive it before starting, take a differing result back to the owner as a question,
   and re-tag the decision measured with what you ran. The re-derivation is done when
   every marker has had its proportional check and every estimated number carries a
   recorded derivation.
3. Ensure the arc branch is checked out (create it if phase start was skipped; check for
   any unmerged arc branch before creating a new one — see *Shape*).
4. Read `spec/TESTING.md`, invoke the TDD skill, implement the slice in small
   red–green–refactor steps. **RED is observed, not assumed:** each behavior's new test
   is run and watched to fail before the code is written, and the observation is
   recorded as it happens — the exact test command, the failing test's line, the exit
   code — in a running record the session keeps for `/end-slice`, which writes it into
   the slice commit body. An observed red cannot be reconstructed at close-out; a red
   never recorded reads later as a red never run. Design questions halt *(halt 3)*.

`/next-slice` ends at the slice-ready hand-back — the executive summary per the
hand-back standard — and **the owner runs `/end-slice`**. Close-out is never chained
from the work session's own momentum: it commits and pushes without asking, so the
hand-back is the owner's one moment to inspect the work before it lands on the arc
branch, and a summary delivered in the same turn as the commit it describes is a
summary no one could act on. This stop is a command boundary like every other in the
daily loop, not a sixth halt.

Run `/end-slice` when the slice's exit criteria are met:

5. Run the gate.
6. Quality pass, **optional** (the `change-simplify` skill on the working diff — reuse,
   simplification, efficiency, altitude, applied only where this slice introduced or
   worsened the condition). It runs here and not later because the reviewer should read
   the code that will actually be committed. **Behavior is frozen**: every move is
   behavior-preserving, one move at a time with the gate between, and an improvement
   that would change behavior is a finding rather than an edit. It requires a green
   gate — a quality pass over red code cannot tell an improvement from a fix. It is
   **read-only about the tree's shape** exactly as the review is — no `git
   checkout/restore/stash` — because the code it improves is uncommitted and has no
   restore point behind it. Skipping
   it is a legitimate choice on a small or mechanical slice; skipping it silently is
   not, so say so in the hand-back either way — and the one-line outcome
   (`quality: <N moves applied | nothing to do | skipped — reason>`) is recorded in
   the slice commit body.
7. Slice code review (the `diff-review` skill on the diff — its Spec and Standards axes
   reported side by side, never merged; plus the matching
   lens from `.claude/commands/REVIEW_LENSES.md` when the slice changed error
   propagation, added a catch or failure path or logging around one, swept for a
   pattern or wrote a script or check whose output will be trusted, touched an
   object that outlives a request or is reachable from more than one, took in outside
   data or passed it to an interpreter, touched credentials or an externally
   reachable surface or added logging or error output near either, or added a test
   the slice itself then deleted, skipped, or gutted — or, under armed TDD-ordering
   guards, added a test reaching into internals the mock policy fences
   off — each applied lens reporting by name with its verdict,
   `<lens>: <finding, file and line | clean>`, and `no lens triggered`
   when none did). The review is **read-only in the shared tree** —
   the reviewer reviews the uncommitted working diff, so no `git checkout/restore/stash`;
   fixes come back as findings, never as edits. Two questions the diff alone cannot answer,
   asked explicitly: who **consumes** each changed error/return path, and what did that
   consumer do with the old behavior; and does any **test double** omit a side effect
   or simplify the error surface of what it replaces. **Every finding is verified
   against the source before it is fixed or deferred**, and the ones that do not survive
   verification are reported, not dropped — a finding is a claim about the code, and
   severity is asserted rather than measured. Apply CRITICAL/HIGH fixes now; defer the
   rest to the PROJECT_INDEX backlog with a one-line rationale each, cause marked
   measured or suspected. Re-run the gate if anything changed. The review is done when
   every finding is dispatched — fixed, deferred with its marker, discarded with its
   reason, or raised to the owner — and the hand-back names the discards.
8. Mutation check: every new guard, branch, or error path this slice added is deleted
   or inverted once and the suite watched to fail on exactly the intended test
   (mutation-testing skill for anything beyond a quick delete-and-run; the runs happen
   in the session's shell, the gate's own scope). A check is
   trustworthy only once it has been made to disagree; the step is done when every new
   guard has been seen to fail on exactly its own test. The one-line outcome
   (`mutation: <N guards, each seen to fail | none — no new guards>`) is recorded in
   the slice commit body.
9. Slice verification, **optional** (the `change-verify` skill on a nontrivial slice):
   exercise the changed behavior through the path its real caller takes rather than
   through the test harness — the gate is evidence about the suite; this is the only
   slice-level evidence about the behavior, and without it nothing runs the change
   outside the harness before phase end. Skipping it is a legitimate choice on a small
   or mechanical slice; skipping it silently is not — the skip and its reason are
   stated in the hand-back, and the one-line outcome (`verify: ran — <verdicts,
   naming the shell they ran in>` / `verify: skipped — <reason>`) is recorded in the
   slice commit body either way. The step runs in the agent's shell, and a pass there
   does not stand in for halt 4's owner acceptance.
   A break it observes is fixed through the same loop as a review fix: apply, re-run
   the gate, and any new guard joins step 8's mutation obligation.
10. Commit — the multi-line message written in the shell tool's own literal form: a
    heredoc on a POSIX shell tool (Claude Code's Bash), a single-quoted here-string
    on a PowerShell one (Copilot CLI's measured shell tool). Subject line in the
    project's own convention where one is recorded; the kit's default shape is
    `<type>(<area>): <summary>` with `docs:` for bookkeeping commits. The commit body
    carries the slice's evidence record: the observed-RED lines from step 4's running
    record (one per behavior batch — command, failing line, exit code, with
    `not observed — <reason>` stated rather than omitted, and a slice with no
    behavior batches writing the zero-form `RED: none — no behavior batches this
    slice`) and the `quality:`, `mutation:`, and `verify:` lines from steps 6, 8,
    and 9.
11. Verify the record: run the close-out checker on the commit just made — **in the
    agent's shell tool**, the same scope as steps 5–9, using the invocation line the
    close-out checker note beside the gate in this file records **for the CLI running
    this session** (on a both-CLIs project the note carries one line each) — and
    quote its output in full — a pass not observed is not a pass. The
    checker verifies **structural presence only** — every evidence line there or
    carrying its stated-skip form, one line per key for `quality:`/`mutation:`/
    `verify:` (a duplicate fails — nobody knows which line is the record), each key
    at the start of its line — never truth; its own output says so. On
    INCOMPLETE, `git commit --amend` with the real outcome or the stated-skip form —
    never with invented evidence — and re-run; on CANNOT CHECK, fix what it names
    and re-run. The step is done only at COMPLETE, and it exists because the record
    is what `/sdlc-retro`'s step-evidence sweep reads off `git log`: a silently
    absent line there is a step nobody can later weigh.
12. Update `spec/PROJECT_INDEX.md` — slice marked done (**status only, one line**;
    detail lives in the phase spec and the commit message), deferred items appended,
    and any friction with the process itself written to the Kit friction log now,
    while the evidence is still accurate, in the log's one-line shape
    (`- <date> — <friction> — open`) — then commit the docs change. Push the
    branch (no PR — that is phase end).
13. Owner clears context (`/clear`). Every slice starts from a fresh window.

## Phase end

Run `/end-phase` when the last slice is done:

1. Run the gate; run whatever phase-level verification the phase spec calls for
   (the `change-verify` skill on the arc, plus any smoke test, end-to-end run, or
   manual script the spec names). The gate is evidence about the suite; this step is
   the only one before halt 4 that produces evidence about the **behavior**, since a
   suite exercises code through the harness rather than through the path a caller
   takes. **A pass not observed is not a pass** — anything that could not be exercised
   here is reported as unverified rather than assumed, because the alternative spends
   halt 4's credibility on a check that never ran. Like its slice-level twin, this
   step runs in the agent's shell and does not stand in for halt 4 — the owner's run
   is the next step, and it is the one that runs in the owner's shell.
2. **Owner acceptance review** *(halt 4)* — owner runs `{{RUN_COMMAND}}` and verifies the
   phase's visible behavior against the spec's checklist. Findings become fix commits
   (back to the slice loop if large). This is the one step in the *slice and phase loop*
   that runs in the **owner's** shell rather than an agent's — setup has its own
   owner-shell asks, for the same reason — and the two are different
   environments: different `PATH`, an unloaded profile, sometimes a different
   interpreter of the same name. A command that fails here is a defect in the
   instructions: fix `{{RUN_COMMAND}}` against the owner's result and record the
   resolved toolchain path in Environment gotchas. The run command has **two homes** —
   here and `CLAUDE.md` (*Commands*) — so fix both in the same pass; fixing one and
   leaving the other is exactly how the two drift.
3. Push and open the PR (`gh`), body summarizing the phase against its exit criteria.
4. Whole-arc review: the `diff-review` skill on the arc range (`<main>...HEAD`),
   checked against the **phase's** exit criteria rather than a slice's — spawned only
   from a clean tree with every fix committed, since any fan-out shares the tree with
   the session; and a commit message may not claim a fix that has no test pinning it,
   because an untested fix can silently leave. The arc-triggered lens applies here:
   *the unconsumed artifact* (`.claude/commands/REVIEW_LENSES.md`) — every artifact the arc
   introduced names its production consumer, a question no slice-shaped review is
   positioned to ask — reported by name with its verdict
   (`unconsumed artifact: <finding, file and line | clean>`), per the lens file's
   contract: an unnamed lens verdict cannot be credited to the lens. Verify each finding against the source
   before it enters a fix batch, and report the ones that did not survive alongside
   the ones that did. The review is done only when **every** reviewer has returned:
   the fix batch is assembled after the last return and goes through the gate as one
   unit — a later-arriving finding re-opens the review rather than starting a second
   batch. Then apply, re-run the gate, push. Deeper options when warranted, both
   Claude Code only and neither required: `pr-review-toolkit:review-pr` for a
   specialist fan-out, and `/code-review ultra <PR#>` (owner-triggered). A deepening
   that ran is named in the hand-back, because a review nobody can tell the depth of
   is a review nobody can weigh.
5. **Merge approval** *(halt 5)*, then merge.
6. Post-merge bookkeeping on `{{MAIN_BRANCH}}`: the deploy question (does this phase
   need a deploy to reach users, and has it happened — merging is not shipping;
   {{DEPLOY_NOTE}}) closed with a **verified outcome** — when the project deploys, the
   deployed artifact is checked against the platform's own record (the deploy run's
   SHA or deployed-commit field, per the deploy note) and the result recorded in the
   Phase History row's Notes cell (`deployed+verified <date>` / `deploy pending —
   <where tracked>` / `deploy NOT verified — <what was seen>`, a halt-5 fact for the
   owner / `n/a — no deploy`), with a pending deploy carried in START HERE
   until verified, and followed by the question the deploy outcome does not answer —
   **what did this deploy turn on**, and what disables each newly-live control by
   itself (newly-live controls recorded in the same Notes cell; one without an
   independent off switch goes to the backlog as a risk); the coverage-floor ratchet
   (set the threshold where it lives — workflow file or build-file check rule — from
   the enforced run's figure, then reconcile
   it against the recorded floor — see *Coverage floor* above); the red-baseline
   decision (lower it here, schedule it, or ratify holding it with the arc count — see
   *Gate baseline* above); the backlog surfaced
   with severity counts for an owner decision (convert / defer / drop), PROJECT_INDEX
   Phase History row + status flip, deferred-pile consolidation, **closed-phase detail
   archived out of PROJECT_INDEX into the phase spec**, spec cleanup, memory
   updates worth keeping.
7. `/sdlc-retro` is **offered**, not required — it extracts the phase's lessons while
   the evidence is fresh, sorting each into a project lesson (into PROJECT_INDEX) or a
   kit lesson (into a report). Declining is the right answer when the phase has nothing
   to teach, and the command refuses to run on too little evidence.

## Bookkeeping rules

- `spec/PROJECT_INDEX.md` is the single source of truth for phase/slice status, the
  deferred backlog, and START HERE. It is updated at every slice end and phase end —
  never left for "later".
- Owner decisions are recorded where they were made (PROJECT_INDEX or the phase spec)
  with the date.
- Deferred review findings go to the backlog, not into scope creep; a big enough pile
  becomes a cleanup slice by owner decision.
- A slice that adds a tool, runtime, or service the gate now requires records it (the
  gate section above; Environment gotchas in PROJECT_INDEX) and adds it to CI in the
  same commit. A gate dependency discovered by a contributor's red run is a
  documentation bug.
- **A gotcha recorded in three consecutive slices becomes a check, or is ratified
  unpreventable.** The third recurrence of the same environmental hazard buys a gate
  step, a hook, or a test — not a fourth, better-worded note. If nothing can prevent
  it, the entry says so explicitly and carries its recurrence count. Those are the
  hazard's only two closed states; a sharper note is neither. Prose in a status
  document is not a control; describing a hazard more sharply each time is what a
  process does instead of stopping it. A control that hands the operator a remediation
  command scopes that command to the population the control actually flags — the
  failure message is the part acted on under time pressure.
- `spec/PROJECT_INDEX.md` has **bounded** sections and **growing** ones (marked in the
  file). The bounded ones are what a fresh session reads first and are kept short;
  per-slice detail is archived into the phase spec at phase close rather than
  accumulating above them.
