# {{PROJECT_NAME}} — SDLC

**Scope: {{SDLC_SCOPE}}**
<!-- What this process governs and what is explicitly out of scope. "The whole repo" is
     the common answer; a mixed repo (app + docs, app + infra, monorepo packages) names
     the boundary here so no session has to guess it. -->

Canonical description of the development process. The commands `/plan-phase`,
`/next-slice`, `/end-slice`, and `/end-phase` (in `.claude/commands/`) automate it; if
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
bug-fix/cleanup slices on a cleanup branch (`chore/cleanup-<slug>`).

## Owner halt points

The process runs autonomously except at these five points. Everything else (gates, reviews,
fix application, bookkeeping, commits) proceeds without asking.

1. **Phase scope** — the owner decides what the next phase (or cleanup slice) covers.
   Recorded as OWNER-DECIDED in `spec/PROJECT_INDEX.md` START HERE.
2. **Slice scope confirmation** — one question at the start of `/next-slice`.
3. **Design questions** — any spec conflict or owner-facing design decision surfaced
   mid-slice halts with a question; it is never resolved silently.
4. **Acceptance review** — the owner personally exercises the phase's visible behavior at
   phase end ({{ACCEPTANCE_SURFACE}}). The agent does not perform this review on the
   owner's behalf.
5. **Merge approval** — the owner approves the PR merge.

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

This is the single place the baseline is defined. Commands read it from here.

The same checks run in CI ({{CI_DESCRIPTION}}). Merges to `{{MAIN_BRANCH}}` require the
CI check green — via branch protection where it is configured, and as a process rule
regardless.

**Coverage floor:** {{COVERAGE_FLOOR}}
<!-- "TBD from first CI run" until one exists. Set just below the first green CI run's
     observed figure, using CI's exact invocation; it only ever raises. Lowering it to
     pass a build defeats its only purpose — existing coverage debt is a backlog item,
     not a merge blocker. -->

If local and CI disagree about a measurement — a pass/fail, an error count, a coverage
figure — CI is authoritative. And the disagreement is itself a finding: work out *why*
before adjusting any threshold, because the gap is usually a symptom (a git-ignored
file, an environment difference, a test reaching a real service), not noise to average
away.

A PostToolUse hook (`.claude/settings.json`) runs the lint/typecheck steps on every
edited source file, so most gate failures surface at edit time rather than at slice end.

## Phase start

Run `/plan-phase` at a phase boundary (after `/end-phase` post-merge bookkeeping, or when
`/next-slice` finds nothing to slice):

1. Candidate phases presented with a recommendation; owner picks the scope *(halt 1)*.
2. Requirements interview in rounds (≤4 questions each) until a round surfaces nothing
   new, then an adversarial gap analysis (walkthrough, trust-boundary sweep, cross-system
   sweep, persistence/compatibility sweep, testability sweep, contradiction sweep,
   minimal-version attack). Every gap becomes a question or a numbered decision — never
   an assumption.
3. Spec written to `spec/PHASE_NN_*.md` only once open questions are resolved: goal,
   numbered owner decisions, behaviors, non-goals, data/migration impact, user-visible
   surface + acceptance-review checklist, slices with exit criteria, risks.
4. Owner approves the decisions + slice breakdown *(same halt, second checkpoint)*.
5. Branch `feat/phase-NN-<slug>` created off `{{MAIN_BRANCH}}`; `spec/PROJECT_INDEX.md`
   flipped to BUILD with the spec pointer; docs committed. Then `/clear` and `/next-slice`.

## Slice loop (repeat per slice)

Run `/next-slice` in a **fresh session**:

1. Read `CLAUDE.md` + `spec/PROJECT_INDEX.md`, then the phase spec. Load no other specs
   until needed (context-minimization rule).
2. Identify the next unstarted slice and its exit criteria; confirm scope with the owner
   in one question *(halt 2)*.
3. Ensure the phase branch is checked out (create it if phase start was skipped).
4. Read `spec/TESTING.md`, invoke the TDD skill, implement the slice in small
   red–green–refactor steps. Design questions halt *(halt 3)*.

Run `/end-slice` when the slice's exit criteria are met:

5. Run the gate.
6. Slice code review (code-review skill on the diff; plus the matching lens from
   `.claude/commands/REVIEW_LENSES.md` when the slice changed error propagation or swept
   for a pattern). Apply CRITICAL/HIGH fixes now; defer the rest to the PROJECT_INDEX
   backlog with a one-line rationale each. Re-run the gate if anything changed.
7. Commit (heredoc for multi-line messages, via the Bash tool).
8. Update `spec/PROJECT_INDEX.md` — slice marked done, deferred items appended — and
   commit the docs change. Push the branch (no PR — that is phase end).
9. Owner clears context (`/clear`). Every slice starts from a fresh window.

## Phase end

Run `/end-phase` when the last slice is done:

1. Run the gate; run whatever phase-level verification the phase spec calls for
   (smoke test, end-to-end run, manual script).
2. **Owner acceptance review** *(halt 4)* — owner runs `{{RUN_COMMAND}}` and verifies the
   phase's visible behavior against the spec's checklist. Findings become fix commits
   (back to the slice loop if large).
3. Push and open the PR (`gh`), body summarizing the phase against its exit criteria.
4. Whole-arc review: `pr-review-toolkit:review-pr` on the PR. Apply fix batches, re-run
   the gate, push. Deeper option when warranted: `/code-review ultra <PR#>`
   (owner-triggered).
5. **Merge approval** *(halt 5)*, then merge.
6. Post-merge bookkeeping on `{{MAIN_BRANCH}}`: PROJECT_INDEX Phase History row + status
   flip, deferred-pile consolidation, spec cleanup, memory updates worth keeping.

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
