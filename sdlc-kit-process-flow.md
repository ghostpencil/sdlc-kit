# SDLC Kit — Process Flow

A walkthrough of the process the kit installs: what `/sdlc-setup` puts in place, what
each of the four daily commands does, where the five owner halt points fall, and —
because they are the least visible part — where the hook guards fire.

**This document is descriptive, not canonical.** In an adopted project the canonical
statement of the process is `spec/SDLC.md` (instantiated from
`sdlc-kit/templates/SDLC.template.md`), and that file says so itself: if it and a
command disagree, the file is right and the command is the bug. The same rule binds
this walkthrough — on disagreement, the template and the command files win, and the
mismatch here is the defect to fix.

---

## Activation: what `/sdlc-setup` installs

`/sdlc-setup` runs in two modes — **New Project** (interview → scaffold → establish a
green gate) and **Existing Project** (analyze → propose → confirm → generate, merging
never overwriting). Either way it leaves the project with:

- **Instantiated documents** — `CLAUDE.md`, `spec/SDLC.md` (the process),
  `spec/PROJECT_INDEX.md` (the single source of truth a fresh session orients from),
  `spec/TESTING.md` (TDD + mock policy). Every `{{PLACEHOLDER}}` is resolved; setup's
  exit check greps the instantiated files for any `{{` left behind.
- **The seven commands** — `sdlc-setup`, `plan-phase`, `next-slice`, `end-slice`,
  `end-phase`, `sdlc-retro`, `sdlc-update` — into `.claude/commands/` (Copilot CLI:
  `.github/skills/<name>/SKILL.md`). User-typed entry points.
- **The skills** — five vendored (`tdd`, `tdd-guide`, `mutation-testing`,
  `python-pro`, `hypothesis-tests`) and three kit-written (`diff-review`,
  `change-simplify`, `change-verify`) — into `.claude/skills/`, which both CLIs read.
  Model-invocable; the daily commands name them by step. `python-pro` and
  `hypothesis-tests` install on Python projects only; `tdd-guide` is optional.
- **The hook guards** — the edit-time gate hook (always offered), the TDD-ordering
  guards (Copilot CLI only, optional, logging mode first), and the skill-activation
  ledger (optional, logging-only, both CLIs). Detailed below.
- **A green gate** — the lint / typecheck / test commands recorded in `spec/SDLC.md`
  with their baseline (zero for a clean adoption, the measured counts for a project
  adopted red). The gate must match what CI already runs, or the gate lies.

## The shape

Work is organized as **phases → slices → TDD cycles**.

- A **phase** delivers one feature or a set of related features, lives on one branch
  (`feat/phase-NN-<slug>`), has a spec (`spec/PHASE_NN_*.md`) breaking it into slices,
  and ends in a single PR.
- A **slice** is one coherent behavior, small enough for a single session — built
  test-first, reviewed, committed, and recorded before context is cleared.
- A **TDD cycle** is one red–green–refactor step inside a slice.

**One arc, one branch, one PR.** Slices accumulate on the arc branch until
`/end-phase`; only `/end-phase` opens a PR, so the whole-arc review sees everything
the arc changed. The only sanctioned second branch is an urgent hotfix. During
STABILIZATION the same slice loop runs on `chore/cleanup-<arc-theme>`.

The process runs autonomously except at **five owner halt points**:

1. **Phase scope** — the owner picks what the next phase covers.
2. **Slice scope confirmation** — one question at the start of `/next-slice` (skipped
   when the slice is already recorded OWNER-DECIDED with its scope spelled out).
3. **Design questions** — any spec conflict or owner-facing design decision, whenever
   it surfaces, halts with a question; it is never resolved silently.
4. **Acceptance review** — the owner personally exercises the phase's visible
   behavior at phase end, in the owner's own shell.
5. **Merge approval** — the owner approves the PR merge.

Every halt and every hand-back follows the same standard: a plain-English executive
summary first, every decision numbered and explicitly marked, detail after.

## The daily loop

```
/plan-phase ──▶ (/clear) ──▶ /next-slice ──▶ owner runs /end-slice ──▶ (/clear)
   halt 1                       halt 2              │    ▲
                                                    ▼    │ more slices
                                              last slice done
                                                    │
                                                    ▼
                                               /end-phase ──▶ merge ──▶ /sdlc-retro
                                              halts 4 + 5                (offered)
```

### `/plan-phase` — turn an idea into a build-ready spec

1. **Orient** — read `spec/PROJECT_INDEX.md`, then only what the candidate needs.
2. **Candidate selection** — *halt 1*: candidates presented with a recommendation;
   the choice recorded OWNER-DECIDED.
3. **Requirements interview** — rounds of ≤4 questions until a round surfaces nothing
   new. Every number in a decision is tagged **measured** (with the run behind it) or
   **estimated**. The prime directive: never fill a gap with an assumption.
4. **Adversarial gap analysis** — nine read-only sweeps (walkthrough, trust-boundary,
   preserved-contract — the product contract's entries on touched surfaces carried
   into the spec, removals owner-ruled — consequence, cross-system, persistence,
   testability, contradiction,
   minimal-version), fanned out as parallel read-only subagents where the CLI can.
   Findings become questions or decisions, never assumptions.
5. **Draft the spec** — `spec/PHASE_NN_*.md`: goal, numbered decisions, behaviors,
   non-goals, trust boundaries, preserved behaviors, data/migration, acceptance
   checklist, slices whose
   exit criteria name what observes them and when, risks.
6. **Approval** — on the owner's OK: branch created, PROJECT_INDEX flipped to BUILD,
   spec committed, then `/clear` and `/next-slice`.

A planning session writes specs and docs, not code — the write-path guards pass its
edits through untouched, and the stop guard does not bind it (see *Session scoping*).

### `/next-slice` — build one slice, fresh session

1. **Orient** — PROJECT_INDEX → phase spec → next unstarted slice.
2. **Confirm scope** — *halt 2*, one question. A backlog entry's stated cause is
   re-derived proportionally to its `measured` / `suspected` marker before any fix;
   an `estimated` number the slice implements is derived before starting, and a
   differing result goes back to the owner inside this halt.
3. **Ensure the arc branch** — check for any unmerged arc branch before creating one;
   never implement on the main branch.
4. **TDD loop** — read `spec/TESTING.md`, invoke the TDD skill, then red–green–
   refactor, one behavior at a time. **RED is observed, not assumed**: each new test
   is run and watched to fail before the code is written, and the observation (exact
   command, failing line, exit code) is recorded as it happens for the slice commit
   body. Design questions halt (*halt 3*).
5. **Finish** — a slice-ready hand-back, and **stop**. The owner runs `/end-slice`;
   the hand-back is the owner's one moment to inspect the work before close-out
   commits and pushes it.

### `/end-slice` — close out (owner-typed only)

1. **Sanity check** — something to commit, and not on the main branch.
2. **The gate** — lint, typecheck, full suite, green against the recorded baseline.
3. **Quality pass** — the `change-simplify` skill, optional and never silent: behavior
   frozen, one move at a time with the gate between, before the review so the
   reviewer reads what will actually be committed.
4. **Slice code review** — the `diff-review` skill: Spec and Standards axes reported
   side by side, plus the consumer-of-changed-behavior and test-double lenses, plus
   any matching lens from `REVIEW_LENSES.md`. Read-only in the shared tree. Every
   finding verified against the source before it is fixed, deferred (with a
   `measured` / `suspected` cause marker), discarded with its reason, or raised to
   the owner (spec conflicts take *halt 3*).
5. **Mutation check** — every new guard, branch, or error path is deleted or inverted
   once and the suite watched to fail on exactly its own test. A check is trustworthy
   only once it has been made to disagree.
6. **Slice verification** — the `change-verify` skill, optional and never silent:
   exercise the changed behavior through its real caller's path, not the harness.
7. **Commit** — the body carries the evidence: `RED:` lines per behavior, `quality:`,
   `mutation:`, `verify:` outcomes.
8. **Record** — PROJECT_INDEX updated (slice done in one line, backlog appended, kit
   friction logged now or never); docs committed separately; branch pushed, no PR.
9. **Hand back** — outcomes named, discards included, ending "safe to `/clear`".

### `/end-phase` — close the arc

1. **Preconditions + gate** — every slice done, tree clean; the gate plus whatever
   phase-level verification the spec names (`change-verify` on the arc). A pass not
   observed is not a pass. If every slice was behavior-neutral by construction, the
   composed system is run locally on real data before the PR.
2. **Owner acceptance review** — *halt 4*, in the owner's shell. Every checklist item
   gets a recorded per-item verdict (met / deferred / dropped) — an unmet item with
   no disposition is the halt not finished. The run's log output
   is part of the acceptance surface. A command that fails in the owner's shell is a
   defect in the instructions, fixed in both its homes.
3. **PR** — `gh pr create`, the body summarizing the phase against its exit criteria.
4. **Whole-arc review** — `diff-review` on `<main>...HEAD` against the *phase's* exit
   criteria, plus the unconsumed-artifact lens and the preserved-contract check
   (contract entries on rewritten surfaces still hold, their pins alive in this
   arc's gate). Findings verified before the fix
   batch; the batch is assembled only after the last reviewer returns and goes
   through the gate as one unit.
5. **Merge approval** — *halt 5*, then merge.
6. **Post-merge bookkeeping** — the deploy question closed with a verified outcome,
   what the deploy turned on (and each control's independent off switch), the
   product-contract reconcile (met behaviors enter `spec/PRODUCT_CONTRACT.md` with
   their pins), the backlog
   surfaced for an owner decision, the coverage-floor ratchet reconciled against the
   CI workflow file, the red baseline lowered or ratified held, Phase History row,
   closed-phase detail archived out of the index. `/sdlc-retro` is offered, not run.

## The hook guards

The guards are **never called by the commands**. They are installed once by
`/sdlc-setup` and fired by the CLI itself on tool events — every edit, every shell
run, every skill activation, every session stop — regardless of which command is
running. The commands run the *gate* explicitly; the hooks are the ambient tripwires
around it. All three fail loud rather than silent, and none denies on its own
failure.

**The edit-time gate hook** (both CLIs — `.claude/settings.json` on Claude Code,
`.github/hooks/sdlc-gate.sh` on Copilot). After every file edit it checks the path
against the project's source glob and, on a match, runs the recorded lint and
typecheck commands on that file — so most gate failures surface at edit time rather
than at slice end. Non-source files (specs, docs) pass through. If it cannot check
(no parser, no path, no project dir), it says "the gate did NOT run" instead of
passing vacuously.

**The TDD-ordering guards G1 + G2** (both CLIs, per dialect, optional —
`.github/hooks/sdlc-tdd-guard.sh` on Copilot, `.github/hooks/sdlc-tdd-guard.py` plus
four `.claude/settings.json` hook blocks on Claude Code). A cooperative backstop, not
a security boundary — shell-tool writes
are invisible to it, and it exists to make TDD ordering the path of least
resistance. **Logging mode is the default**; deny arms only when
`.git/sdlc-tdd/deny-enabled` exists, and only after the log shows the guards
recognizing the project's own test runs.

- **G1, the observed-RED write guard** (pre-write): a production-source write needs
  either a test edit this session followed by an observed failing run (the fresh-red
  license, for new behavior), or a declared `.git/sdlc-tdd/refactor-license` plus an
  observed green this session (the refactor license, for behavior-preserving edits at
  any point in the cycle — refactors, `change-simplify` moves, mutation-testing
  edits). The declaration
  is one line naming the step and move; every write under it is logged, a test edit
  revokes it, and it survives reds on purpose.
- **observe-test** (post-shell): records RED or GREEN from a test command's exit
  code — bare single commands only. A compound (`;`, `&`, `|`) is refused *out loud*,
  with what is allowed stated, because its exit code is not the test's. Counted runs
  are spoken too: each RED/GREEN observation is echoed back as the state fact it
  produced (the write license earned — or that the red licenses nothing yet, absent
  a test edit — and the stop guard satisfied), so the guard's state machine is
  visible at every transition, not only on refusal.
- **G2, the premature-stop guard** (agent stop): stopping is a violation while no
  green run has been observed or the latest observed run is red. The green is **any**
  counted green — a single-test selector satisfies it; full-suite assurance is
  `/end-slice`'s gate, not the backstop.

**Session scoping** (owner-decided 2026-08-08): G2 binds only a session that made a
production write that went through, or edited a test — a written test never run is
exactly a never-ran stop. A session that did neither (planning, docs, bookkeeping)
runs no tests by design and stops clean; a denied write arms nothing, because the
tree did not change. The write-path guards are scoped the same way by construction:
they classify by file kind, not by command, so spec and docs writes pass through
whatever session makes them.

**The skill-activation ledger** (optional, logging-only, both CLIs). One line per
skill activation into `.git/sdlc-skill-ledger.jsonl`, so `/sdlc-retro` can read
which named skills actually ran instead of trusting that presence meant activation.
`.git/` is per-clone, so the ledger describes one machine.

### Where each guard fires across the loop

| Event | Guard | Matters most during |
|---|---|---|
| File edit (post) | Edit-time gate hook | `/next-slice` TDD loop; every fix batch |
| File edit (pre, Copilot) | G1 write guard | TDD loop; `/end-slice` quality pass and fixes |
| Shell run (post, Copilot) | observe-test | Every test run: TDD loop, gate, mutation check |
| Skill activation (post) | Ledger | TDD skill and the three change passes |
| Session stop (Copilot) | G2 stop guard | Coding sessions only — ends each slice on green |

## After the arc

- **`/sdlc-retro`** — offered at phase close: extracts lessons while the evidence is
  fresh, sorting each into a project lesson (PROJECT_INDEX) or a kit lesson (a report
  for the kit's home repository). It refuses to run on too little evidence.
- **`/sdlc-update`** — brings an adopted project forward to a newer kit release; the
  kit README's *Updating an adopted project* section states the same procedure.
