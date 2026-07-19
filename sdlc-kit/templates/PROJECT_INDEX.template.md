# {{PROJECT_NAME}} — Project Index

Single source of truth for phase/slice status, the deferred backlog, and what to do
next. Updated at every `/end-slice` and `/end-phase` — never left for "later".

## Phase

**{{INITIAL_PHASE_STATUS}}**
<!-- New Project mode:  "PRE-PHASE-1. Project scaffolded <date> via /sdlc-setup.
     No feature phases yet — run /plan-phase to define Phase 1."
     Existing Project mode: either
     "STABILIZATION. SDLC adopted <date> via /sdlc-setup on an existing codebase.
      Gate baseline: <green | N lint / N type / N test failures — see backlog>."
     or "BUILD — Phase NN <title> (spec/PHASE_NN_*.md)" if adopting mid-feature. -->

## START HERE — Next work

{{START_HERE}}
<!-- One short block a fresh session can act on: what is in flight (branch names,
     uncommitted state), what the next slice is, and what decision (if any) is the
     owner's. Anything OWNER-DECIDED is recorded here with the date. -->

## Deferred backlog

<!-- Review findings and small follow-ups deferred at /end-slice / /end-phase.
     One line each: what, where, why deferred. This is a menu, not a mandate — a big
     enough pile becomes a cleanup slice by owner decision at the next phase boundary. -->

- (empty)

## Phase History

| Phase | Title | PR | Merged | Notes |
|---|---|---|---|---|
{{PHASE_HISTORY_ROWS}}
<!-- Existing Project mode: seed a few rows from git history so the arc of the project
     is visible ("pre-SDLC" is a fine PR value). New Project mode: leave empty. -->

## Notes & gotchas

{{NOTES}}
<!-- Durable, non-obvious facts a fresh session needs and cannot derive from code:
     environment quirks, data-compatibility rules, seeds/fixtures, "CI is authoritative
     because local runtime differs", etc. Keep each to 1–3 lines. -->
