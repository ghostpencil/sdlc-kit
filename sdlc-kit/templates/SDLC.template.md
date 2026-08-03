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

**Kit version:** {{KIT_VERSION}} (adopted {{ADOPTION_DATE}}). Update procedure:
`/sdlc-update` (installed with the commands; the kit's home repository README states the
same procedure).

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

## Owner halt points

The process runs autonomously except at these five points. Everything else (gates, reviews,
fix application, bookkeeping, commits) proceeds without asking.

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
   resolved silently.
4. **Acceptance review** — the owner personally exercises the phase's visible behavior at
   phase end ({{ACCEPTANCE_SURFACE}}). The agent does not perform this review on the
   owner's behalf. When no slice's exit criteria required running the application — an
   arc behavior-neutral by construction — `/end-phase` first runs the composed system
   locally against real data before the PR: the halt otherwise passes vacuously on a
   phase with no visible behavior yet, which is exactly when nothing has ever run
   outside the test suite.
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
     observed figure, using CI's exact invocation; it only ever raises. Lowering it to
     pass a build defeats its only purpose — existing coverage debt is a backlog item,
     not a merge blocker. -->

The floor raises by procedure, not by rule alone — at phase end, where coverage is
known: if CI's printed coverage rose over the arc, post-merge bookkeeping sets the
floor in the CI workflow file to just under CI's printed figure (in the same docs
commit as the PROJECT_INDEX update), then asserts that the floor recorded here and in
`spec/PROJECT_INDEX.md` is identical to the value in the workflow file — the
bookkeeping is not done until they are. The recorded
number is a claim; the workflow value is the enforcement — a mismatch means the ratchet
is not ratcheting, which is the only regression the floor exists to prevent.

If local and CI disagree about a measurement — a pass/fail, an error count, a coverage
figure — CI is authoritative. And the disagreement is itself a finding: work out *why*
before adjusting any threshold, because the gap is usually a symptom (a git-ignored
file, an environment difference, a test reaching a real service), not noise to average
away.

An edit-time hook ({{HOOK_CONFIG_PATH}}) runs the lint/typecheck steps on every edited
source file, so most gate failures surface at edit time rather than at slice end.
{{HOOK_FEEDBACK_NOTE}}

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
     Copilot CLI, and this section says which. -->

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
   numbered owner decisions, behaviors, non-goals, data/migration impact, user-visible
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
   reproduce-or-disprove (and is re-tagged). A backlog entry is a hypothesis with a
   timestamp, not a finding; when the cause does not hold, correct the entry in place
   and re-scope. The same rule covers an **estimated** number the slice implements:
   derive it before starting, take a differing result back to the owner as a question,
   and re-tag the decision measured with what you ran. The re-derivation is done when
   every marker has had its proportional check and every estimated number carries a
   recorded derivation.
3. Ensure the arc branch is checked out (create it if phase start was skipped; check for
   any unmerged arc branch before creating a new one — see *Shape*).
4. Read `spec/TESTING.md`, invoke the TDD skill, implement the slice in small
   red–green–refactor steps. Design questions halt *(halt 3)*.

Run `/end-slice` when the slice's exit criteria are met:

5. Run the gate.
6. Slice code review (`pr-review-toolkit:code-reviewer` on the diff; plus the matching
   lens from `.claude/commands/REVIEW_LENSES.md` when the slice changed error
   propagation or added a catch or failure path, swept for a pattern, touched an
   object that outlives a request or is reachable from more than one, took in outside
   data or passed it to an interpreter, or touched credentials or an externally
   reachable surface). The review is **read-only in the shared tree** —
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
7. Mutation check: every new guard, branch, or error path this slice added is deleted
   or inverted once and the suite watched to fail on exactly the intended test
   (mutation-testing skill for anything beyond a quick delete-and-run). A check is
   trustworthy only once it has been made to disagree; the step is done when every new
   guard has been seen to fail on exactly its own test.
8. Commit (heredoc for multi-line messages, via the Bash tool).
9. Update `spec/PROJECT_INDEX.md` — slice marked done (**status only, one line**;
   detail lives in the phase spec and the commit message), deferred items appended,
   and any friction with the process itself written to the Kit friction log now,
   while the evidence is still accurate — then commit the docs change. Push the
   branch (no PR — that is phase end).
10. Owner clears context (`/clear`). Every slice starts from a fresh window.

## Phase end

Run `/end-phase` when the last slice is done:

1. Run the gate; run whatever phase-level verification the phase spec calls for
   (smoke test, end-to-end run, manual script).
2. **Owner acceptance review** *(halt 4)* — owner runs `{{RUN_COMMAND}}` and verifies the
   phase's visible behavior against the spec's checklist. Findings become fix commits
   (back to the slice loop if large). This is the one step in the whole process that
   runs in the **owner's** shell rather than an agent's, and the two are different
   environments — different `PATH`, an unloaded profile, sometimes a different
   interpreter of the same name. A command that fails here is a defect in the
   instructions: fix `{{RUN_COMMAND}}` against the owner's result and record the
   resolved toolchain path in Environment gotchas.
3. Push and open the PR (`gh`), body summarizing the phase against its exit criteria.
4. Whole-arc review: `pr-review-toolkit:review-pr` on the PR — spawned only from a
   clean tree with every fix committed, since the fan-out shares the tree with the
   session; and a commit message may not claim a fix that has no test pinning it,
   because an untested fix can silently leave. Verify each finding against the source
   before it enters a fix batch, and report the ones that did not survive alongside
   the ones that did. The review is done only when **every** reviewer has returned:
   the fix batch is assembled after the last return and goes through the gate as one
   unit — a later-arriving finding re-opens the review rather than starting a second
   batch. Then apply, re-run the gate, push. Deeper option when warranted:
   `/code-review ultra <PR#>` (owner-triggered).
5. **Merge approval** *(halt 5)*, then merge.
6. Post-merge bookkeeping on `{{MAIN_BRANCH}}`: the deploy question (does this phase
   need a deploy to reach users, and has it happened — merging is not shipping;
   {{DEPLOY_NOTE}}) closed with a **verified outcome** — when the project deploys, the
   deployed artifact is checked against the platform's own record (the deploy run's
   SHA or deployed-commit field, per the deploy note) and the result recorded in the
   Phase History row's Notes cell (`deployed+verified <date>` / `deploy pending —
   <where tracked>` / `n/a — no deploy`), with a pending deploy carried in START HERE
   until verified, and followed by the question the deploy outcome does not answer —
   **what did this deploy turn on**, and what disables each newly-live control by
   itself; the coverage-floor ratchet (set the workflow value, then reconcile
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
