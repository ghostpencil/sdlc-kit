# SDLC

Reads and changes the **SDLC state** — the one file, `<git-dir>/sdlc-state`, that the
kit's hooks read to learn whether the process is in force right now. `spec/SDLC.md`
*Shape* is the canonical statement of the states and of the hook rule; this command is
the typed entry point and nothing more. The daily commands write the state themselves,
so this is for looking, for suspending the hooks on purpose, and for putting it right.

**Prime directive: pausing and turning off are owner acts — never run `pause` or `off`
to get past a denied write.** A denied write takes the TDD path or declares a licence.
Run those verbs only when the owner typed this command with them.

## How to use

- `/sdlc status` — the state, the derived TDD leg, whether deny is armed, and the
  index's Phase line.
- `/sdlc pause <reason>` — suspend the hooks for non-SDLC work in the middle of a phase
  or slice; the reason is required and is spoken back once per session.
- `/sdlc resume` — restore the state that was paused.
- `/sdlc off` — no arc in flight; refuses while one is, unless the owner repeats it
  with `--force`.

## Workflow

1. From the repository root run `python .github/hooks/sdlc-state.py <verb> …` with the
   arguments the owner gave. If the file is missing, the project predates this
   command: say so and stop.
2. Quote the block it prints, verbatim. An error line (exit 2) is quoted too and is the
   answer — never retried with another verb to get round it.
3. On `status`, add one line: whether the index's Phase line and the state agree
   (`BUILD — Phase 12` with state `off` is a disagreement the owner should see).
4. Report per the hand-back standard (`spec/SDLC.md`, *Owner halt points*), one screen.
