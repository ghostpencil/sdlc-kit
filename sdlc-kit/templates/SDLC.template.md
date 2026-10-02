# {{PROJECT_NAME}} — SDLC

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

## Records

The per-project record the close-outs run on: the scope, the gate and its baseline
and floor, the CI line, the hook and guard notes, and the model policy live in this
one section — a command session reading those values loads these lines, not the rest
of the file. Each record names the section whose rules govern it. A few values live
at the step that uses them instead: the run command and acceptance surface (*Phase
end*, halt 4), the deploy note (*Phase end*, step 6), the main branch (*Shape*), the
kit version (the header) — each read where it is used, never re-derived.

**Every row that records a control records what its proof could *see*.** The install
proofs this kit prescribes are already catch-proofs — each one says *prove it by making
it fail*, and a control seen only to run is not one of them. But a catch-proof
**constructs** the state it catches, and that leaves the question nobody asks: does the
workflow ever produce that state on its own? So a control row states three things, not
two — installed (where, and in which mode), the **catch** seen (what was flagged, named),
and the **reach note**: whether the flagged state arises in ordinary operation, or was
built for the proof. *"Constructed for the proof; not yet observed arising on its own"*
is a legitimate answer and a useful one — it is a claim the next close can check. What is
not legitimate is a row that records only that the control executed: one adoption carried
a stop-time backstop as installed and proven on exactly such a line, and its window was
empty at 96 of the 125 stops it ever took, with zero catches in its whole life.

**Scope: {{SDLC_SCOPE}}**
<!-- What this process governs and what is explicitly out of scope. "The whole repo" is
     the common answer; a mixed repo (app + docs, app + infra, monorepo packages) names
     the boundary here so no session has to guess it. -->

### The gate

All of the following, in order, all green (rules: *The Gate*):

```
{{GATE_LINT_CMD}}        # lint
{{GATE_TYPECHECK_CMD}}   # typecheck / compile check — omit only if the language has neither
{{GATE_TEST_CMD}}        # full test suite
```

**Baseline: {{GATE_BASELINE}}** — the single place the baseline is defined; commands
read it from here (rules: *Gate baseline*). The value carries the commit it was measured
at (`N @ <short-sha>`); *Gate baseline* says why.

The same checks run in CI ({{CI_DESCRIPTION}}). Merges to `{{MAIN_BRANCH}}` require the
CI check green — via branch protection where it is configured, and as a process rule
regardless (rules: *The Gate*).

**Coverage floor:** {{COVERAGE_FLOOR}} (rules: *Coverage floor*)
<!-- "TBD from first CI run" until one exists. Set just below the first green CI run's
     observed figure (printed, or read from that run's coverage report artifact where
     the check prints only pass/fail), using CI's exact invocation; it only ever
     raises. Lowering it to pass a build defeats its only purpose — existing coverage
     debt is a backlog item, not a merge blocker. -->

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
hook that checks nothing still reads as a gate; and the dispatch layer itself can
change under an auto-updating CLI, so the record below names the CLI version it
measured and is a dated claim about that version, re-proven at every hook-touching
update. What the hook environment measured at
setup (launch route, shell, JSON parser, lint reachability, the dispatch check's
verdict, CLI version), the **catch** its proof saw (the hook's report on the deliberate
lint error, naming the file), and the **reach note** the rule above requires:
{{HOOK_ENVIRONMENT}}

{{TDD_GUARD_NOTE}}
<!-- Setup resolves {{TDD_GUARD_NOTE}} to a statement of whether the TDD-ordering guards
     are installed, which CLI they run on, and whether they are in logging or deny mode.
     When installed, the note also states the four rules the guards impose on a coding
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
     one line naming the step and move to `.git/sdlc-tdd/refactor-license` (the git
     directory's — see below for a linked worktree), valid only
     behind a counted green, revoked by the next test edit, every write under it
     logged — **except during `/end-slice`, which has its own licence and needs one**:
     close-out's mandated order edits tests *between* its production writes (the review
     fixes tests, the mutation step writes production and restores tests, the
     verification step writes a harness), so a licence a test edit revokes cannot
     survive the step it was declared for, and one real arc paid the re-declaration
     seven times in a single phase. `.git/sdlc-tdd/close-out-license` is the same
     licence with that one difference, still behind a counted green, still ending with
     the session, and every test edit it survives is COUNTED in the log so a licence
     held open past close-out is visible rather than silent; and the guards see only
     files INSIDE the repository — an absolute path
     outside the repo root is neither licensed nor denied (0.25.0), so a scratch
     script under a session temp directory is not a production write and costs no
     license, while a relative path always is one. The stop guard is session-scoped (owner-decided
     2026-08-08): it binds only a session that wrote production code or edited a test,
     so a planning, docs, or bookkeeping session stops clean by construction. The note
     also names the artifact that decides the mode (`.git/sdlc-tdd/deny-enabled`,
     present means deny — arming or disarming means updating the line), records the
     proof run that was made to fail, and says `.git/` is per-clone: the flag, state,
     and log describe the machine that wrote the note, not this checkout. It also says
     what `.git/` MEANS in every kit path — the licences, the flag, the state, the logs:
     the repository's git directory, which is `.git/` itself in an ordinary checkout
     and, in a linked worktree, where `.git` is a file, the directory
     `git rev-parse --git-dir` prints. A licence declared at the literal `.git/...` path
     in a worktree fails to write; the guard's own refusal names the real path
     (0.31.1). And the flag, the state and the log are per-WORKTREE too: a linked
     worktree keeps its own git directory, so arming deny in one checkout does not arm
     another, and a note that says "deny" is a claim about the checkout it was armed in.
     If they were declined, it says so WITH THE DATE — it does not delete this line. A
     missing line and a declined offer are different facts: /sdlc-update re-offers the
     guards when this project never had the choice, and must not badger an owner who
     already made it. Deleting the record erases the difference.
     The note names the dialect(s) installed — Copilot (`.github/hooks/
     sdlc-tdd-guard.sh` + `.json`), Claude Code (`.github/hooks/sdlc-tdd-guard.py`
     plus the four hook blocks in `.claude/settings.json`) — and on a project running
     both CLIs says which sides are covered; the deny flag and state are shared, so
     arming deny arms every installed dialect. With both dialects installed it also
     says a Copilot contributor needs `python` on PATH: Copilot runs the Claude
     dialect's launchers too, and one that cannot start denies the edit. Never describe a guard this project
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
     artifact that makes "installed" true (on each CLI a pair: that CLI's launcher —
     the Copilot hook JSON, or the Claude Code settings-file block — AND the body
     script both share since 0.31.1, `.github/hooks/sdlc-skill-ledger.sh`, since a
     launcher with no script errors and a script with no launcher never fires — adding
     or removing any of them later means
     updating this line,
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
     discipline as the hook environment note above — and carrying the catch that run
     printed (the INCOMPLETE line naming the missing keys) and its reach note: the proof
     runs on a commit with no record by construction, so say whether a real slice commit
     has yet come up INCOMPLETE on its own. `sh .github/hooks/sdlc-close-out.sh
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
     THE SAME NOTE's invocation serves the script's `docs-check` mode too — same
     line, `docs-check` in place of `check` — so nothing extra is proven or
     recorded for it. That mode is log-only on every install, exits 0 even on its
     own errors, and is read at slice step 12; it is not part of what the note
     proves, because a mode that cannot fail a step cannot lie about one.
     THE SAME NOTE also records the stop-time backstop's state — the same script's
     `stop-check` mode wired at agentStop (Copilot, `.github/hooks/sdlc-close-out.json`)
     / Stop (Claude Code, the settings-file block), offered separately and OPTIONAL
     where the checker itself is not. Installed: which CLIs, the catch-proof
     actually seen (which CLI and launcher, the would-block line read back NAMING
     THE COMMIT — a recorded install whose proof never ran is the silent absence
     this family catches, one layer up), THE REACH NOTE the rule above requires
     (the proof constructs an unpushed commit missing a key, while /end-slice
     commits, checks and pushes in one step — so say whether that state has been
     seen to arise on its own), logging or armed
     (the flag file `.git/sdlc-close-out/deny-enabled`, present means armed — arming
     or disarming means updating this line, because nothing else will), and that the log lives at
     `.git/sdlc-close-out/log`, per-clone like everything under `.git/` — and
     per-worktree, as the guard note says. Declined:
     say so WITH THE DATE — never delete the line; /sdlc-update reads it exactly as
     it reads the guard note's decline. Unlike the command step above, the backstop
     fails OPEN (a hook that errors must not block work), and its bare-commit class
     is log-only by design regardless of the flag. -->



### Model policy

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

## The Gate

The gate's commands, its baseline, and the coverage floor are *Records* entries above;
this section carries the rules that govern them.

Green means green **against the recorded baseline** — zero for a clean adoption, the
recorded counts for a project adopted mid-flight. Any *increase* is a regression and is
fixed in the slice that caused it, never accepted as a cost. The baseline only ever
moves down, as the STABILIZATION backlog burns it toward zero; when it changes, it is
re-recorded in *Records* in the same commit.

A count can also hold still because the checker stopped looking: suppressions, skipped
tests, and constructs that hide code from analysis (an unannotated decorator can type
everything it wraps as `Any`) freeze the number while shrinking what it measures. A
ceiling that stops measuring is worse than a high one — when the count will not move,
check what the checker still reaches, not only what it reports.

### Gate baseline

**The baseline moves by procedure, not by ambition.** At every phase close, post-merge
bookkeeping reports the current count beside the recorded one and does one of three
things: lowers the baseline in *Records* in the same docs commit, records an owner
decision to lower it via a stabilization slice in the next phase, or records that the
owner **ratified holding it** — with how many arcs it has been unchanged. A ceiling
nobody is ever asked about is not a ratchet, and *"drive it down through the backlog"*
is a wish until a step serves it.

**The number describes a commit, not a tree.** Every recorded baseline carries the
commit it was measured at — `N @ <short-sha>` — because the measurement and the record
are never simultaneous. The count comes from the arc branch's gate run — *Phase end*
step 1, before the merge; the close then commits docs, pins and bookkeeping on top of
it. One arc
re-derived its baseline correctly and a later close-out commit added a test, so the
freshly derived number was already wrong by the time the close finished. The stamp does
not make the number current — it makes it **checkable**, which is strictly better than a
number that silently claims to describe whatever the tree holds now. The next close's
reconcile reads the drift between the stamp and the tree instead of assuming there is
none. Re-running the gate at close to refresh the number stays forbidden, for the reason
*Phase end*'s reconcile gives.

**Rendering:** an unchanged red baseline is reported as `N (unchanged for K arcs)`,
never as `N (ceiling held)` or any other phrasing where a stall reads as an
achievement. The same number twelve times is the finding, and it has to look like one.

### Coverage floor

The floor raises by procedure, not by rule alone — at phase end, where coverage is
known: if the coverage measured for the merged branch rose over the arc, post-merge
bookkeeping sets the threshold — in whichever artifact carries it: the CI workflow
file, or the build file's check rule where the workflow only invokes the check — to
just under the measured figure (in the same docs commit as the PROJECT_INDEX update),
then asserts that the floor recorded in *Records* and in `spec/PROJECT_INDEX.md` is
identical to that threshold value — the bookkeeping is not done until they are. The
measured figure is read off the enforced run's own output: CI's printed number where
the check prints one, else the coverage report artifact the same run produced — a
check that prints only pass/fail yields no printed figure ever, and waiting for one
leaves this leg inert. Reading that artifact is not computing the number locally;
re-running coverage outside the enforced invocation to produce a different number is.
The recorded number is a claim; the threshold value is the enforcement — a mismatch
means the ratchet is not ratcheting, which is the only regression the floor exists to
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

## Product contract

`spec/PRODUCT_CONTRACT.md` is the current-truth statement of owner-ratified,
externally observable behavior — one line per behavior, grouped by user-facing
surface, each line naming the decision that ratified it (`P<NN> D<M>`) and its
enforcement: `pinned: <test or mechanical check>` or `claim-only (<date>)`. Phase
specs remain the decision record and stay historical; this file states what is
currently true — the role that otherwise belongs to no artifact, which is how a
ratified behavior can vanish with every gate, test, and review green.

- **Read at phase boundaries only.** `/plan-phase` carries the entries on surfaces
  the phase touches into the phase spec (*Preserved Behaviors*), so slices inherit
  them from the spec they already read — the context-minimization rule is untouched.
  One narrow exception: a slice review that saw a test deleted, skipped, or gutted
  opens this file to ask whether that test is a pin (the disposal-intent lens) —
  *Preserved Behaviors* carries only this phase's touched surfaces, and a deleted
  pin can belong to an untouched one.
- **Written at phase close.** `/end-phase`'s contract reconcile enters each
  acceptance-checklist behavior recorded **met**, with its pinning test named (or
  `claim-only`, dated). Anywhere else, the file changes only by owner decision.
- **`claim-only` is the explicit unenforced state.** The entry has no pinning
  test: its only evidence is the owner exercising the behavior at halt 4, nothing
  reconciles it between phases, and the preserved-contract check never reports it
  clean. The date shows the debt's age; each phase-close reconcile that touches
  its surface re-asks whether it can now be pinned.
- **A behavior leaves only by ratified retirement.** A superseding decision replaces
  its line and the superseding phase spec records why; omission is never retirement.
- **And it never stays out by omission either — the absent direction.** Every phase
  close, the reconcile pass at the head of post-merge bookkeeping walks prior phase
  specs for ratified decisions holding **neither** an entry here **nor** a recorded
  drop, and asks whether the behavior is in the tree. Each absent one takes an
  explicit owner ruling — restore, or drop and amend the ratifying decision in its
  source spec — so every decision reaches a terminal state and the walk shrinks close
  by close. Every other check on this file reads entries that exist: the
  preserved-contract check's population is (entries here) × (surfaces this arc
  touched), and the backfill below runs once. A behavior that never became an entry
  is outside all of them, which is how three ratified behaviors left a real product
  with every gate, test, and review green.
  A planned change that would remove or alter an entry is an owner question at
  planning (halt 1 or halt 3), never a decision the plan makes on its own.
- **A pinned test is contract-bound.** Deleting, skipping, or gutting a test this
  file names as a pin is a contract edit, and a contract edit is an owner decision
  (halt 3) — never a quiet suite cleanup.
- **The deletion rule.** A record-shaped artifact (an entity, a column, a config key)
  is not deleted as dead until this file and the ratifying phase specs have been
  searched for it — a hit is a spec conflict (halt 3: build the consumer, or retire
  the decision), not a cleanup. The search's method matters: entries here are
  behavior prose, not symbol names, so a grep for the artifact's identifier is the
  miss — read this file whole (it is bounded) for the surface the artifact serves,
  then that surface's ratifying specs, and say what was read (a search-absence
  claim, so the *verify the denominator* lens applies). The rule binds whichever
  step decides the deletion — the whole-arc unconsumed-artifact lens, or a cleanup
  slice acting on a backlog entry, where the search joins the entry's
  re-derivation. It exists because a real cleanup deleted the
  only remnant of a ratified-but-undelivered behavior, closing a backlog entry while
  moving the tree further from the spec that required it.
- **Trust boundaries ride here.** The file's closing section carries high-consequence
  invariants (untrusted-data classifications, scheme/rendering policies, authority
  rules). `/plan-phase` re-reads it whenever a touched surface **consumes** data
  classified untrusted there — the consumer side inherits the producer's boundary
  rules, which otherwise live in a phase spec no later phase reads.
- **Adopted mid-flight:** a contract still empty — or missing outright, on a
  project updated from a pre-contract kit that has not yet created it (the update
  procedure names the window) — while Phase History shows merged
  phases gets a **one-time backfill
  offer** at the next phase close — an owner-confirmed pass over the prior phase
  specs' ratified decisions, never an inference; a decline is recorded in the file
  with the date, so the offer is not re-made at every close. That single run takes
  the **absent direction** above as well: a decision confirmed still-current whose
  behavior is not actually in the tree is put up for a restore/drop ruling, never
  entered as current and never silently left out — the first real backfill omitted
  three, and only a human reading a document no adopter process reads caught it.

## Architecture impact view — *optional*

A project that carries an **Understand Anything** knowledge graph gets a mechanical
picture of what each slice and each arc touched: the git change set mapped onto the
graph's nodes, one hop out through its edges, written back as UA's own
`diff-overlay.json` and summarized in a few printed lines the daily commands quote.
The adapter is `.github/hooks/sdlc-impact.py`, installed verbatim and launched
`python <path>`; it is command-invoked, never a hook.

**It is a comprehension aid, and it is not verification.** Nothing it prints enters
gate truth, no step passes or fails on it, and it adds no owner halt — the five in
*Owner halt points* are still the five. A `COMPLETE` summary says the picture was
drawn, never that the change is correct. Read it the way you would read a map, not a
test result, and note that its own summary is **not** part of the slice commit's
evidence record: the close-out checker's keys are unchanged, because a picture is not
evidence.

**A project without the graph loses nothing.** With no UA directory the adapter prints
`UNAVAILABLE` with the reason and every step continues exactly as written — an
optional capability that is not installed has nothing to report. `/next-slice` records
the slice base only when a graph is present, so a non-adopting project pays no
footprint at all; the honest cost is that a graph installed mid-slice waits one slice
before the view works.

Its four states are worth knowing apart:

- **COMPLETE** — every changed project file mapped to a node.
- **PARTIAL** — the footprint was computed and something is missing *and named*:
  files the graph does not know, or a graph that may predate the work. The counts are
  printed with their denominators (`changed-files` beside `mapped-files`) so
  incompleteness is loud rather than inferred.
- **UNAVAILABLE** — the capability's environment is absent. Not a failure.
- **ERROR** — the adapter itself broke on a readable graph. That is kit friction and
  belongs in the friction log; a graph that exists and will not parse reports here and
  never as a silent COMPLETE.

**Regenerate the graph at the phase boundary — that is the trigger, and it is this
process's, not the graph tool's.** Run the tool's own analysis after `/end-phase`'s
post-merge bookkeeping, before the next `/plan-phase`. That is the only moment in the
loop where the tree is settled, the branch is merged, and no slice is mid-flight, so it
is the one place a regeneration cannot invalidate work in progress. Without a stated
trigger the graph ages silently and every run of the view reports `PARTIAL` for the whole
arc: one real adoption ran a seven-slice phase against a graph built before the
*previous* phase merged, so the view was degraded at every site that draws it and the
freshness line was the only thing that said so (field, 2026-09-01).

**Do not rely on the graph tool's own auto-update to do this.** Where the tool offers
such a setting, turn it on — it is strictly better than nothing — but treat it as a
reminder, not a refresh. Measured against the Understand Anything plugin at kit 0.31.0:
its `autoUpdate` flag defaults to off, and turning it on enables two hooks that both only
*print a message asking the agent* to merge the graph by hand — neither writes it. One of
those hooks matches the **Bash** tool only, so on a project whose primary shell is
PowerShell a commit fires nothing at all, and the plugin's own prompt describes itself as
triggered by a post-commit hook the plugin does not ship. A setting named auto-update
that reminds rather than updates is exactly the kind of claim this process re-derives
rather than trusts. The phase-boundary regeneration above is what makes the view's
freshness a property of this process instead of a property of a vendor's hook matcher.

**Freshness answers one question only:** had the tree already moved on from the graph
*before this work began*? It compares the graph's build commit against the slice or
phase **base**, never against the working tree — this change set's own edits are unseen
by the graph by definition, and measuring against the tree would call every slice stale
and make COMPLETE unreachable. No build metadata means `freshness unknown` with the
reason, never "current".

**The overlay is written only where the UA directory is git-ignored.** *Phase end*
requires a clean tree and re-asserts it before the merge, so writing into a tracked UA
directory would dirty the tree at exactly the moments this process checks it. Where the
directory is not ignored the summary still prints and the file is not written, said
plainly (`overlay: not written — .ua is not git-ignored`). The same path rule keeps
UA's own generated files out of the project's changed-file denominator.

Where the view fits: `/next-slice` records the slice base once the branch is settled and
previews the footprint into the slice-ready hand-back; `/end-slice` regenerates after
the record check, states **whether the footprint changed from that preview**, and clears
the spent base in the same pass, so the next slice can never compute against an old one;
`/end-phase` runs it against the main branch the project's own records name for the
acceptance hand-back, and regenerates before the merge halt, stating any change since
acceptance. The two changed-from statements are the ones that earn the view its place:
a close-out review that adds a file the owner never saw, or a whole-arc review that adds
one after acceptance, is invisible to every other step. The dashboard is never launched
automatically.

## Phase start

Run `/plan-phase` at a phase boundary (after `/end-phase` post-merge bookkeeping, or when
`/next-slice` finds nothing to slice):

1. Candidate phases presented with a recommendation; owner picks the scope *(halt 1)*.
2. Requirements interview in rounds (≤4 questions each) until a round surfaces nothing
   new, then an adversarial gap analysis (walkthrough, trust-boundary sweep,
   preserved-contract sweep — the product contract's entries on touched surfaces,
   carried into the spec — consequence sweep, cross-system sweep,
   persistence/compatibility sweep, testability
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
   boundaries (what the consequence sweep found, recorded), preserved behaviors (the
   product-contract entries on surfaces this phase touches, carried with their pins —
   see *Product contract* above), user-visible
   surface + acceptance-review checklist, slices with exit criteria that name **what
   observes them and when** (a criterion naming an observer that does not run at that
   point — CI on an arc branch, typically — is a planning defect) and a test approach
   (`none` is reserved for a slice touching no production source and no test file — the
   docs-only slice of *Slice loop* step 4), risks. A behavior
   assigned to the acceptance checklist rather than pinned by a test **names the path
   a real caller reaches it by, or is flagged test-only here** — the assignment is not
   terminal, and an item nothing downstream asks about reaches halt 4 as a checklist
   line nobody can exercise. Any decision
   carrying a number is tagged **measured** (naming the run, count, or query behind it)
   or **estimated** — the same distinction the deferred backlog draws about causes,
   applied where a number is first ratified. The spec stays lean enough to be read
   whole at every slice — decisions, behaviors, slices, and checklists are the spec;
   bulk research and interview detail go to an appendix file the spec links, with
   its own spec-loading row in `CLAUDE.md` naming its trigger, loaded
   only when a slice needs it (`/next-slice` reads the phase spec at every slice).
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
   and re-tag the decision measured with what you ran. **And it covers a ratified
   *method* the slice implements through** — where the phase spec ratified not only an
   outcome but how it would be established, the slice owes that method or an explicit
   substitution presented at the halt, because a different route answers a different
   question even when it satisfies the same one. The re-derivation is done when every
   marker has had its proportional check, every estimated number carries a recorded
   derivation, and every ratified method has been run or explicitly substituted.
3. Ensure the arc branch is checked out (create it if phase start was skipped; check for
   any unmerged arc branch before creating a new one — see *Shape*).
4. Read `spec/TESTING.md`, invoke the TDD skill, implement the slice in small
   red–green–refactor steps. **RED is observed, not assumed:** each behavior's new test
   is run and watched to fail before the code is written, and the observation is
   recorded as it happens — the exact test command, the failing test's line, the exit
   code — in a running record the session keeps for `/end-slice`, which writes it into
   the slice commit body. An observed red cannot be reconstructed at close-out; a red
   never recorded reads later as a red never run. **A characterization test — one
   written against behavior that already exists — has no natural red, and passing on
   its first run is not evidence that it pins anything.** Its red is manufactured and
   still observed: assert the wrong value first (or break the behavior for one run),
   watch it fail for the expected reason, then assert what the code actually does.
   It is recorded in the ordinary shape, marked as characterization — never with the
   zero-form, which belongs to a slice with no behavior batches at all. Design
   questions halt *(halt 3)*.

   **A docs-only slice is declared here, not discovered at close-out.** When the phase
   spec ratified the slice's test approach as `none` and the slice plans to touch no
   production source and no test file, say so in one line citing the ratified
   approach, and skip `spec/TESTING.md`, the TDD skill, and the loop: the record is the
   zero-form `RED: none — no behavior batches this slice`, and `/end-slice` writes
   steps 6 and 8 as their stated skips directly (`quality: skipped — docs-only slice;
   reuse: not searched — docs-only slice`, `mutation: none — no new guards`) rather
   than walking them to find nothing. Step 9 still runs, in its docs form. **A
   docstring or comment inside a source file is not docs-only** — it is a
   behavior-preserving production write, taken in the loop under the refactor licence
   where the TDD guards are installed. The short-circuit needs no guard of its own — a
   slice declared docs-only that writes source meets the guard and the gate exactly as
   any production write does — and `/end-slice` confirms the declaration against
   everything the slice will commit before writing a skip (`git status --short`, so an
   untracked file counts, plus any commit the slice already made): a production source
   or test file there voids it, and every step runs.

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
   (`quality: <N moves applied | nothing to do | skipped — reason>; reuse: <what was
   searched, and against what | not searched — reason>`) is recorded in the slice
   commit body. **The `reuse:` half is required**, because the skill's rule that Reuse
   is *searched, not eyeballed* has no other durable home: one arc dispatched the skill
   in every one of five slice sessions and recorded zero named searches, since the line
   asked only for a move count. This is also the first close-out step that writes
   production code, so where the TDD guards are installed it is where the **close-out
   licence** is declared — one declaration covering steps 6 through 9.
7. Slice code review (the `diff-review` skill on the diff — its Spec and Standards axes
   reported side by side, never merged; plus the matching
   lens from `.claude/commands/REVIEW_LENSES.md` when the slice changed error
   propagation, added a catch or failure path or logging around one, swept for a
   pattern or wrote a script or check whose output will be trusted, touched an
   object that outlives a request or is reachable from more than one, took in outside
   data or passed it to an interpreter, touched credentials or an externally
   reachable surface or added logging or error output near either, or added a test
   the slice itself then deleted, skipped, or gutted — or deleted, skipped, or
   gutted a test `spec/PRODUCT_CONTRACT.md` names as a pin — or, under armed
   TDD-ordering guards, added a test reaching into internals the mock policy fences
   off — each applied lens reporting by name with its verdict,
   `<lens>: <finding, file and line | clean>`, and `no lens triggered`
   when none did — the verdict recorded on the slice commit's `lenses:` line, since
   the review hand-back is not retained and only a lens *finding* otherwise travels
   under its own name). The review is **read-only in the shared tree** —
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
   guard has been seen to fail on exactly its own test. **A slice that added tests but
   no guard — a characterization pass, a coverage backfill — reads the trigger the
   other way round rather than skipping the step:** what is new is the tests, so the
   production code each one pins is what gets mutated, sampled where the count is
   large and the sample stated. Nothing else in the close-out carries signal about
   such a slice. **And a slice whose deliverable is a sweep, a ratchet, or a check is
   the third case, for which `mutation: none` is wrong:** that check is the artifact
   this step exists to distrust, so it owes a made-to-disagree run of *itself* — a
   planted violation in a scratch copy, seen to fire on exactly that, then confirmed
   clean on the real tree. One arc's sweep needed five passes to enumerate its own
   population and one of its patterns reported a false clean. **One collision to know
   before writing the mutation:** a counting or sweeping check can only be made to
   disagree by *adding* statements, and an unused local inside a function is what the
   linter's unused-variable rule flags — the edit-time hook rejects the write before
   the suite runs. Write the mutation at **module level**, where that rule does not
   apply. **The mutation is undone by inverting the edit that made it** — a
   targeted edit of the same hunk, which is safe whether or not anything is committed.
   This step runs before the slice commits, so the implementation is uncommitted
   underneath the mutation and `git checkout -- <path>` restores the path to HEAD,
   taking the slice with it — one arc lost a slice's work that way. A VCS restore is
   available only where `git status --short <path>` was clean before the mutation, and
   that is checked rather than assumed. Never write the file's text back through a
   whole-file read-then-write either: that normalizes line endings, trailing newline,
   and encoding, and it corrupted one arc's working tree four times. Mutate one thing
   at a time, reverting between, so a red suite stays attributable. The one-line outcome
   (`mutation: <N guards, each seen to fail | N of M characterization pins, each seen
   to fail | none — no new guards>`) is recorded in the slice commit body.
9. Slice verification, **optional** (the `change-verify` skill on a nontrivial slice):
   exercise the changed behavior through the path its real caller takes rather than
   through the test harness — the gate is evidence about the suite; this is the only
   slice-level evidence about the behavior, and without it nothing runs the change
   outside the harness before phase end. **Constrain the run before starting it, not
   after:** it drives production code paths with production wiring, so everything the
   path reaches on its way out — credentials, the data directory, outbound calls, the
   queue, the clock — is pointed somewhere disposable or confirmed inert first, and
   the isolation established is stated with the result. Redirecting some of them is
   the failure mode: one run redirected the data directory, left the credentials
   alone, and minted a live token against a real account.
   Skipping it is a legitimate choice on a small
   or mechanical slice; skipping it silently is not — the skip and its reason are
   stated in the hand-back, and the one-line outcome (`verify: ran — <verdicts,
   naming the shell they ran in>; not exercised: <what could not be reached, and why |
   nothing>` / `verify: skipped — <reason>`) is recorded in the
   slice commit body either way. **The `not exercised:` half is required and `nothing`
   is a real answer**: the skill's third verdict — *not exercised, and why* — is a
   first-class result that must never be folded into the first, and it is the half that
   disappeared on a real arc while all five keys stayed present and the record read as
   complete. The step runs in the agent's shell, and a pass there
   does not stand in for halt 4's owner acceptance.
   A break it observes is fixed through the same loop as a review fix: apply, re-run
   the gate, and any new guard joins step 8's mutation obligation.
   **On a docs-only slice (step 4) the step runs in a narrower form and is not
   optional:** every command the diff adds or changes is run once and every file path
   it adds is opened, each result quoted like any run — a documented command that does
   not work is a docs slice's characteristic defect, and this is the one moment it is
   cheap to catch. A command that would reach anything not disposable (a deploy, a data
   reset, an outbound call) is not run; it goes under `not exercised:` with that reason.
   A diff that adds neither records `verify: skipped — no command or path added`.
10. Commit — the multi-line message written in the shell tool's own literal form: a
    heredoc on a POSIX shell tool (Claude Code's Bash), a single-quoted here-string
    on a PowerShell one (Copilot CLI's measured shell tool). Subject line in the
    project's own convention where one is recorded; the kit's default shape is
    `<type>(<area>): <summary>` with `docs:` for bookkeeping commits. The commit body
    carries the slice's evidence record: the observed-RED lines from step 4's running
    record (one per behavior batch — command, failing line, exit code, with
    `not observed — <reason>` stated rather than omitted, and a slice with no
    behavior batches writing the zero-form `RED: none — no behavior batches this
    slice`), the `quality:`, `mutation:`, and `verify:` lines from steps 6, 8, and 9,
    and the `lenses:` line from step 7's review.
11. Verify the record: run the close-out checker on the commit just made — **in the
    agent's shell tool**, the same scope as steps 5–9, using the invocation line the
    close-out checker note in this file's *Records* section records **for the CLI
    running this session** (on a both-CLIs project the note carries one line each) — and
    quote its output in full — a pass not observed is not a pass. The
    checker verifies **structural presence only** — every evidence line there or
    carrying its stated-skip form, one line per key for `quality:`/`lenses:`/
    `mutation:`/`verify:` (a duplicate fails — nobody knows which line is the
    record), each key at the start of its line — never truth; its own output says so. On
    INCOMPLETE, `git commit --amend` with the real outcome or the stated-skip form —
    never with invented evidence — and re-run; on CANNOT CHECK, fix what it names
    and re-run. The step is done only at COMPLETE, and it exists because the record
    is what `/sdlc-retro`'s step-evidence sweep reads off `git log`: a silently
    absent line there is a step nobody can later weigh.
12. Update `spec/PROJECT_INDEX.md` — slice marked done (**status only, one line**;
    detail lives in the phase spec and the commit message), deferred items appended,
    and any friction with the process itself written to the Kit friction log now,
    while the evidence is still accurate, in the log's one-line shape
    (`- <date> — <friction> — open`) — then commit the docs change. That rule
    carries a **budget of 25 added index lines** for this commit — the status line
    plus whatever backlog, gotcha, and friction entries the slice genuinely produced
    — and the close-out checker's `docs-check` mode counts them and reports against
    it: run it on the docs commit, in the agent's shell like the record check above,
    and quote its line. The number here is a copy; the enforcing home is that
    script's own `BUDGET` constant, and the mode's output quotes the budget it used.
    **Log-only**, always: it
    never fails the step and never blocks, because a number cannot tell a heavy but
    honest close from a per-slice write-up, so `OVER` is a question the hand-back
    answers rather than a verdict. It exists because *status only, one line* was in
    force the whole time an adoption wrote 404 index lines across seven close-outs;
    a rule with no observer is a wish. Push the branch (no PR — that is phase end).
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
   is the next step, and it is the one that runs in the owner's shell. **A
   verification script's license depends on where it lives, and the default is
   outside:** a throwaway driver under a session temp directory is not a production
   write at all (where the guards are installed, they see only files inside the
   repository), so it needs no
   refactor license; committing one under the repo makes it production source, and it
   takes the ordinary red-green path. Neither is an exemption, and wanting one is the
   signal the script belonged outside the repo.
2. **Owner acceptance review** *(halt 4)* — owner runs `{{RUN_COMMAND}}` and verifies the
   phase's visible behavior against the spec's checklist. **Every checklist item —
   the phase's own and any *Preserved Behaviors* entry — gets a recorded per-item
   verdict in the spec's checklist: met, deferred (a backlog entry; the behavior does
   not enter the product contract), or dropped (the ratifying decision amended — an
   owner ruling).** An unmet item with no recorded disposition is this halt not
   finished; an acceptance that waves one through silently is how a ratified behavior
   first goes missing. Findings become fix commits
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
   contract: an unnamed lens verdict cannot be credited to the lens. Beside it runs
   the **preserved-contract check**: for every surface the arc touched (the
   preserved-contract sweep's own population), the product
   contract's entries on that surface still hold — each named pin exists and
   **itself passed** in this arc's gate run (a pin skipped or failing inside a
   recorded red baseline is a finding, not green), a claim-only entry reporting
   `claim-only — halt 4 evidence only` rather than clean — reported as
   `preserved contract: <finding, file and
   line | clean | n/a — no entries on touched surfaces>`; a violation that turns out
   deliberate is halt 3, because a ratified behavior is retired by the owner or not
   at all. Verify each finding against the source
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
6. Post-merge bookkeeping on `{{MAIN_BRANCH}}`. It **opens with the reconcile pass**,
   which runs before any bullet below asks the owner anything: every recorded number
   and carried claim re-derived from the tree and from this close's own gate evidence,
   each reported as `recorded X / measured Y` — divergences first, agreements collapsed
   to one line. A decision taken against a stale number is taken twice. No new gate run
   is needed: step 1's evidence **is** the measurement, the merge having come from a
   clean tree. Four subjects, in order:
   - **The backlog, reconciled before it is counted.** Walk this arc's slice commits
     and the phase spec; mark `— done (<commit>)` on every entry they closed; only
     then report the open count, stating how many the pass itself just closed. The
     convert/defer/drop question below is asked of the **reconciled** number — a count
     still carrying entries this arc delivered describes the future instead of mixing
     it with the past.
   - **The whole *Records* table, not the two rows that have bullets of their own.**
     Every row the table holds is checked against this close's gate run and reported
     recorded-vs-measured — including rows the adoption authored, which are
     structurally unreconciled from birth, nothing having ever been written to
     reconcile them. The coverage-floor and red-baseline bullets below keep their own
     decision procedures; this pass is the **detector** they and every unnamed row now
     share. **Where a row's number is enforced somewhere, the value is searched for,
     not just the row:** take the number from the enforcing artifact, then search the
     whole spec set for the **old** value and report every file still carrying it.
     Reconciling one home says nothing about a second one three hundred lines away in
     the same file.
   - **The contract's absent direction.** For every ratified decision in prior phase
     specs that has neither a contract entry nor a recorded drop, ask the question no
     other check asks: is the behavior in the tree? Absent → surface it for an explicit
     restore/drop ruling; a drop amends the source phase spec, so every decision
     reaches a terminal state and later walks shrink toward zero. This runs at **every**
     close, not once: the one-time backfill runs once by definition, and the
     preserved-contract check's population — entries on touched surfaces — can never
     reach a behavior that never became an entry.
   - **The phase spec's own *Risks & Deferred*.** Every entry the spec opened is driven
     to a terminal state — discharged (naming what discharged it), carried (with the
     identifier it was given), or withdrawn (with the reason) — and anything ending in
     none of the three is reported. No other walk reads that section, so without this
     one an obligation the spec attached to the arc lapses by silence while the arc
     closes green.

   Then the decisions and the records themselves: the deploy question (does this phase
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
   independent off switch goes to the backlog as a risk); the **product-contract
   reconcile** (halt 4's met behaviors enter `spec/PRODUCT_CONTRACT.md` with their
   pins named; entries on touched surfaces re-affirmed against pins that exist —
   the record is not done until entry and pin agree; claim-only entries on touched
   surfaces re-presented — can one now be pinned?; the one-time backfill offered
   where the *Product contract* section above says it is owed); the coverage-floor ratchet
   (set the threshold where it lives — workflow file or build-file check rule — from
   the enforced run's figure, then reconcile
   it against the recorded floor — see *Coverage floor* above); the red-baseline
   decision (lower it here, schedule it, or ratify holding it with the arc count — see
   *Gate baseline* above); the backlog surfaced
   with severity counts for an owner decision (convert / defer / drop), PROJECT_INDEX
   Phase History row + status flip, deferred-pile consolidation, **closed-phase detail
   archived out of PROJECT_INDEX into the phase spec**, **closed items retired to
   `spec/PROJECT_INDEX_HISTORY.md`** (see *Bookkeeping rules*), spec cleanup, memory
   updates worth keeping.
7. `/sdlc-retro` is **offered**, not required — it extracts the phase's lessons while
   the evidence is fresh, sorting each into a project lesson (into PROJECT_INDEX) or a
   kit lesson (into a report). Declining is the right answer when the phase has nothing
   to teach, and the command refuses to run on too little evidence.

## Bookkeeping rules

- `spec/PROJECT_INDEX.md` is the single source of truth for phase/slice status, the
  deferred backlog, and START HERE. It is updated at every slice end and phase end —
  never left for "later".
- **A recorded number is reconciled before it is read.** Every number and carried
  claim in these records — the backlog count, each row of the *Records* table, the
  floor, the baseline, the contract's coverage — is re-derived from the tree at phase
  close and reported `recorded X / measured Y` **before** any decision reads it
  (*Phase end*, step 6). Recording a number is an act, and the act does not keep the
  number true; a rule that fires when a number is *written* is silent for every close
  afterwards, which is why each number here has its own writing rule and none of them
  caught a stale value. The detector is one pass over all of them, not another rule
  per row.
- Owner decisions are recorded where they were made (PROJECT_INDEX or the phase spec)
  with the date.
- Deferred review findings go to the backlog, not into scope creep; a big enough pile
  becomes a cleanup slice by owner decision. **A backlog entry's identifier is the next
  integer above the file's current maximum, read from the file at the moment of the
  append** — every other step addresses entries by number, and nothing downstream can
  detect a collision. The phase close asserts the identifiers are unique before it
  counts them.
- **A check records its verdict whether or not it found anything.** A lens that ran
  clean, a sweep that triggered on nothing — each writes its negative result where the
  result outlives the session, because a check with no durable negative record cannot
  be told apart from one that never ran, and every judgement about whether a check
  earns its place needs that denominator.
- A slice that adds a tool, runtime, or service the gate now requires records it
  (*Records* → *The gate*; Environment gotchas in PROJECT_INDEX) and adds it to CI in
  the same commit. A gate dependency discovered by a contributor's red run is a
  documentation bug.
- **A gotcha recorded in three consecutive slices becomes a check, or is ratified
  unpreventable.** The third recurrence of the same environmental hazard buys a gate
  step, a hook, or a test — not a fourth, better-worded note. If nothing can prevent
  it, the entry says so explicitly and carries its recurrence count. Those are the
  hazard's only two closed states; a sharper note is neither, **and neither is having
  been absorbed by a retro** — absorption records that the finding was transmitted
  upstream, and the recurrence count keeps running until something changed. Prose in a
  status document is not a control; describing a hazard more sharply each time is what a
  process does instead of stopping it. A control that hands the operator a remediation
  command scopes that command to the population the control actually flags — the
  failure message is the part acted on under time pressure.
- `spec/PROJECT_INDEX.md` has **bounded** sections and **growing** ones (marked in the
  file). The bounded ones are what a fresh session reads first and are kept short;
  per-slice detail is archived into the phase spec at phase close rather than
  accumulating above them.
- **Closed items retire out of the index at phase close.** The two growing record
  sections — the deferred backlog and the Kit friction log — gain entries at every
  slice close, and without an exit path they only grow: a real
  adoption's index reached 1,820 lines, 69% of it deferred backlog, read by every
  fresh session at start. At `/end-phase` post-merge bookkeeping, items whose line
  carries closing evidence — a backlog entry marked `— done (<fix commit>)` or
  `— dropped (owner, <date>)` (the backlog presentation writes the marker as the
  verdict is taken), a Kit-friction line flipped to a **closed** absorbed form
  (`- <date> — <friction> — absorbed by retro <date> — implemented in <commit>`
  or `— ruled unpreventable`) more
  than one phase ago — move verbatim to
  `spec/PROJECT_INDEX_HISTORY.md` (created on first retirement), one dated section
  per phase close, any numbering and all provenance preserved so an old reference
  to an entry still resolves. **A half-delivered entry is split, never half-marked:**
  when an arc closes part of an entry and leaves the rest, the delivered part takes the
  ordinary `— done (<commit>)` marker so it retires, and the remainder opens as a
  **new numbered entry** whose provenance names the entry it came from. The grammar
  stays three-valued — done, dropped, unmarked — and unmarked now means only
  *untouched*; an entry partly delivered and left unmarked is counted as open work in
  full, retires never, and describes neither what shipped nor what remains.
  (Environment gotchas are bounded — delete when fixed
  — and never retire; Phase History stays, one row per phase.) An item without its
  closing marker never retires — an open entry in the history file is work hidden
  from every session that acts on the index, so the retirement step re-reads what
  it just moved and pulls back any entry lacking the marker. The step also checks
  that `CLAUDE.md`'s spec-loading table carries the history file's row (its
  never-at-session-start trigger — canonical in the CLAUDE template's table); on a
  project updated rather than re-instantiated the row can be missing, and it is
  added in the same docs commit, because a retired item nothing points at is
  unfindable by the rule that made retiring it safe. Nothing is deleted;
  and a retro's sweep over **closed** items (repeat counts, oldest-unaddressed)
  reads the history file too — retirement splits that population across two
  files, and a sweep that reads only the index has a denominator it did not
  enumerate.
