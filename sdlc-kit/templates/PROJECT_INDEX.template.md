# {{PROJECT_NAME}} — Project Index

Single source of truth for phase/slice status, the deferred backlog, and what to do
next. Updated at every `/end-slice` and `/end-phase` — never left for "later".

**Agent CLI:** {{TARGET_CLI}}
<!-- Recorded at setup: `Claude Code`, `Copilot CLI`, or `both`. It is not a preference —
     it is which install mapping this project holds, and /sdlc-update reads it to know
     which directories are kit-owned here. Changing CLI means re-running /sdlc-setup,
     not editing this line. -->


<!-- Sections below are marked **bounded** or **growing**. Bounded sections answer "what
     do I do next" and are what a fresh session reads first: they stay short, and stale
     content leaves them rather than accumulating. Growing sections are records and may
     get long — they live below the bounded ones for that reason. Per-slice close-outs
     record status only — one line; detail belongs in the phase spec and the commit
     message, not here. If detail collects here anyway, /end-phase archives it into
     that phase's own spec file at the close — a safety net, not the plan; nothing is
     deleted, but this file is a dashboard first and an archive never. A single source
     of truth nobody can find the answer in has stopped being one.
     The two growing record sections (Deferred backlog, Kit friction log) also have an
     exit path: at every phase close, /end-phase retires items whose line carries a
     closing marker — "— done (<fix commit>)" / "— dropped (owner, <date>)" on a
     backlog entry, the absorbed form on a friction line more than a phase old — into
     spec/PROJECT_INDEX_HISTORY.md, one dated section per close, numbering and
     provenance preserved. An entry without its marker never retires. -->

## Phase — *bounded*

**{{INITIAL_PHASE_STATUS}}**
<!-- New Project mode:  "PRE-PHASE-1. Project scaffolded <date> via /sdlc-setup.
     No feature phases yet — run /plan-phase to define Phase 1.
     Coverage floor: TBD from first CI run."
     Existing Project mode: either
     "STABILIZATION. SDLC adopted <date> via /sdlc-setup on an existing codebase.
      Gate baseline: recorded in spec/SDLC.md (its single home — do not restate the
      counts here, they would go stale silently when the baseline moves).
      Coverage floor: <TBD from first CI run | the CI-enforced figure>."
     or "BUILD — Phase NN <title> (spec/PHASE_NN_*.md)" if adopting mid-feature.
     In every mode this block carries the coverage-floor line: /end-phase's post-merge
     bookkeeping asserts it, spec/SDLC.md's recorded floor, and the enforced threshold
     value (the CI workflow file, or the build file's check rule where the workflow
     only invokes the check) are identical at every phase close. -->

## START HERE — Next work — *bounded*

{{START_HERE}}
<!-- One short block a fresh session can act on: what is in flight (branch names,
     uncommitted state), what the next slice is, and what decision (if any) is the
     owner's. Anything OWNER-DECIDED is recorded here with the date. -->

## Deferred backlog — *growing*

<!-- Review findings and small follow-ups deferred at /end-slice / /end-phase.
     One line each: what, where, why deferred — and where it came from, e.g.
     "(slice review, 2026-07-19)" or "(whole-arc review, PR #2)". Provenance is what
     makes the pile triageable months later. Each entry also marks its stated cause
     "measured" (reproduced/observed) or "suspected" (inferred) — an entry is a
     hypothesis with a timestamp, not a finding, and /next-slice re-derives the cause
     before fixing. This is a menu, not a mandate — a big enough pile becomes a cleanup
     slice by owner decision at the next phase boundary, where /end-phase presents it. -->

- (empty)

## Phase History — *growing*

| Phase | Title | PR | Merged | Notes |
|---|---|---|---|---|
{{PHASE_HISTORY_ROWS}}
<!-- Existing Project mode: seed an adoption marker —
       | — | **SDLC adopted** | pre-SDLC | <date> | via /sdlc-setup |
     — plus a few back-filled pre-SDLC rows from git history, recorded so the arc of
     the project is visible, not because they followed this process ("pre-SDLC" is a
     fine PR value). New Project mode: leave empty. Deploying projects: /end-phase
     bookkeeping records the deploy outcome in Notes (`deployed+verified <date>` /
     `deploy pending — <where tracked>` / `n/a — no deploy`). -->

## Kit friction log — *growing*

<!-- Process friction, not code findings: a step that cost more than it returned, a
     rule worked around, tooling noise (stderr warnings, phantom diffs), a moment the
     process was silent. One line each, in exactly this shape:
       - <YYYY-MM-DD> — <the friction, one sentence> — open
     flipped in place when a retro absorbs the entry into a report:
       - <YYYY-MM-DD> — <the friction, one sentence> — absorbed by retro <YYYY-MM-DD>
     /end-slice's close-out writes the `open` form here, at the moment the friction is
     still accurate; /sdlc-retro's sweep reads the status word, reports every entry
     still `open` with its age, and carries anything older than one phase into the
     next report. One shape for writer and sweep — an entry without a status word is
     one the sweep has to infer about, which is how two entries in a real adoption
     sat statusless until a retro guessed. This is /sdlc-retro's raw material — its
     recorded-but-unactioned sweep mines this section first, because friction that
     produces no backlog entry, no commit, and no gate movement is invisible to every
     other sweep. -->

- (none yet)

## Environment gotchas — *bounded*

<!-- Machine/OS/tooling facts that bite a fresh session or a new contributor: toolchain
     or venv paths, OS-specific behavior, services that must be running for the gate,
     where credentials live, "CI is authoritative because local runtime differs" and
     why, and the toolchain paths the OWNER's shell resolves (which can differ from an
     agent's). One line each; delete when fixed. An entry recorded in three consecutive
     slices is escalated at /end-slice — it becomes a gate step, a hook, or a test, or
     is ratified unpreventable and says so with its recurrence count. -->

- (none)

## Notes & gotchas — *bounded*

{{NOTES}}
<!-- Durable, non-obvious facts a fresh session needs and cannot derive from code:
     data-compatibility rules, seeds/fixtures, decisions too small for a spec.
     Environment facts go in Environment gotchas above. Keep each to 1–3 lines.
     New Project mode starts this as "- (none)". -->
