# SDLC

Reads and changes the **SDLC state** — the one file, `<git-dir>/sdlc-state`, that the
kit's hooks read to learn whether the process is in force right now. `spec/SDLC.md`
*Shape* is the canonical statement of the states and of the hook rule; this command is
the typed entry point and nothing more. The daily commands write the state themselves,
so this is for looking, for suspending the hooks on purpose, and for putting it right.

**Prime directive: every change of state says who asked and why.** Any caller may
pause or turn the state off — the owner, this session on its own judgement, a harness
script — for work that is not the slice's; `pause` and `off` require a reason, and the
log keeps the caller beside it (`/sdlc-retro` reads it). A denied write of the slice's
own work is not that case: it takes the TDD path or declares a licence, and a pause
whose reason is a denial is exactly what the retro looks for.

## How to use

- `/sdlc status` — the state, the derived TDD leg, whether deny is armed, and the
  index's Phase line.
- `/sdlc pause <reason>` — suspend the hooks for work that is not the slice's, in the
  middle of a phase or slice; the reason is required, logged, and spoken back once per
  session.
- `/sdlc resume` — restore the state that was paused.
- `/sdlc off <reason>` — no arc in flight; the reason is required. While an arc is in
  flight the helper refuses once and names `pause` as the usual verb; repeating with
  `--force` goes through, and the log line records the stage that was abandoned.
- **Who asked travels with every change.** Pass `--by owner` when the owner typed this
  command, `--by agent` when this session invokes it on its own judgement; a hook or
  launcher script passes `--by harness`. The daily commands pass their own names.

## Workflow

1. From the repository root run `python .github/hooks/sdlc-state.py <verb> …` with the
   arguments given and the `--by` that is true (above). If the file is missing, the
   project predates this command: say so and stop.
2. Quote the block it prints, verbatim. An error line (exit 2) is quoted too and is the
   answer — never retried with another verb to get round it.
3. On `status`, add one line: whether the index's Phase line and the state agree
   (`BUILD — Phase 12` with state `off` is a disagreement the owner should see).
4. Report per the hand-back standard (`spec/SDLC.md`, *Owner halt points*), one screen.
