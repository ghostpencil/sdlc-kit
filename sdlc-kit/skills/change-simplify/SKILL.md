---
name: change-simplify
description: Post-green quality pass on a change set — reuse, simplification, efficiency, and altitude — applied as edits and taken back through the gate. Use after the slice is green and before the review. Quality only; it does not hunt for bugs, and it never changes behavior.
---

# Change Simplify

Improve the shape of code that already works, without changing what it does.
Process reference: `spec/SDLC.md`.

This is the refactor leg, run across the whole slice rather than inside one cycle. TDD's
refactor step sees one test's worth of code at a time; the duplication that matters is
usually only visible once the slice is done, between things written an hour apart.

**Prime directive: behavior is frozen.** Every edit here must leave the observable
behavior identical. If an improvement would change what the code does — even to fix
something obviously wrong — it is **a finding, not an edit**. Report it and leave the
code alone. A behavior change smuggled in under a refactor is invisible to review,
because review reads a refactor as behavior-preserving by definition.

## How to use

Run after the slice is green and before the slice review, so the reviewer reads the code
that will actually be committed. It can also be run directly on any range.

Arguments, all optional:

- **A scope** — `working` (uncommitted changes, the default), `<main>...HEAD`, or any
  git range.
- **An axis** — one of the four below, to run alone. Default is all four.

## Preconditions

- **The gate is green.** Refactoring red code is debugging, and this pass has no way to
  tell an improvement from a fix. If the gate is not green, stop and say so.
- **The suite covers what you are about to move.** Behavior preservation is checked by
  the gate, so a refactor of code the suite does not exercise is unverified by
  construction. Where that is the case, say which edits rest on nothing and let the
  caller decide — do not quietly proceed as though the gate covered them.

## What this skill is not

- **Not a bug hunt.** Quality only. A suspected defect is a finding for `diff-review` or
  a lens in `.claude/commands/REVIEW_LENSES.md`, never a fix applied here.
- **Not `diff-review`.** That pass is **read-only** and reports; this one **edits**.
  They are deliberately different contracts and must not be merged — a reviewer that
  edits cannot be trusted to report what it chose to change instead.
- **Not a rewrite.** The unit of work is a named, behavior-preserving move on code this
  change set introduced or worsened. Restructuring code the slice merely stood next to
  is scope creep, and it lands in the diff with no criterion asking for it.
- **Not licensed to rearrange the tree.** No `git checkout`, `git restore`, or
  `git stash`: at slice end the code being improved is *uncommitted*, so there is no
  restore point behind it and a "clean up first" reflex destroys the slice.

## The four axes

Applied only where the change set introduced or worsened the condition.

| Axis | The question |
|---|---|
| **Reuse** | Does this repeat something the project already has? Prefer the existing helper, type, or convention over a second expression of the same decision. |
| **Simplification** | Can this say the same thing with less structure — a branch that cannot be taken, a flag only ever passed one way, an indirection with one caller, a name that needs the body read? |
| **Efficiency** | Is there work done repeatedly that could be done once, or a pass over data that could be one pass instead of three? Only where it is *also* clearer; a faster version nobody can read is a different kind of debt. |
| **Altitude** | Is this written at the right level? A function mixing a policy decision with the mechanics of carrying it out reads as two things, and the mechanics usually belong one level down. |

**Test code is in scope.** The change set is the whole diff — test files included.
Duplicated setup, a copied helper, a fixture re-derived beside an existing one: all
Reuse territory, and on a TDD process tests are where most of every slice's new code
lives. The founding miss is on record: a duplicated `LogCaptor` test helper sailed
through this pass as "nothing to do" and was caught by `diff-review` minutes later on
the same diff (field, 2026-08-11) — a reviewer had to report what this pass exists to
fix.

**Reuse is searched, not eyeballed.** For each helper, fixture, private method,
constant, or type the diff *adds*, look for an existing equivalent before concluding
there is none — search the repo for the name, the shape, or the thing it wraps
(`grep`/IDE lookup; on a fanned-out review, the project's own conventions file first).
An unsearched "no duplication" is not a verdict, it is a guess with the same spelling.

**The project's documented conventions win over every axis.** `CLAUDE.md` *Runtime
Conventions* first, then any other convention file the repo carries. If the repo says to
do something an axis above would undo, the repo is right and the axis is silent — say so
rather than making an edit you already know will be reverted.

## Workflow

### 1. Pin the scope and confirm the preconditions

State the range and the file count. Confirm the gate is green and say so. If either
precondition above fails, stop here and report why — a quality pass that ran on red is
not a weaker result, it is an unrelated one.

If the range is empty, that is the result — report it and stop. Check *why* before you
do: an empty `git diff` on a slice that plainly changed something usually means the work
is staged or already committed, not that there is nothing there. Say which you found, so
the caller can re-scope rather than read "nothing to simplify" as a verdict on the code.

### 2. Propose, in writing, before editing

Walk each axis against the change set — tests included — and for Reuse, run the
search the axis section requires, noting what was searched. Then list the candidate
moves: the file and line, the axis, the move, and — the part that
does the work — **what makes it behavior-preserving**. A move you cannot say that about
is a move you have not finished thinking about.

Then drop the ones that are taste. The bar is that a reader is measurably better off, not
that the code now matches how you would have written it. A diff full of neutral
rewordings hides the two edits that mattered and costs the review its attention.

### 3. Apply them one at a time, gate between

One named move, then the gate. Not a batch, then the gate.

A batch that goes red tells you the batch broke something, and finding which edit did it
means unpicking work already tangled together. One at a time makes every failure
self-locating, and the moves are individually small by construction. If a move goes red,
revert **that move** and record it — a refactor you believed was behavior-preserving and
was not is worth more as a note than as a silent retry.

### 4. Report

**All five sections are always present, including when one is empty.** "Findings: none"
is a statement; an omitted section is indistinguishable from a section nobody filled in,
and the reader cannot tell which they are looking at.

- **Applied** — per move: file and line, axis, what changed, and the gate result after.
- **Proposed and dropped** — with the reason. A move rejected as taste, as too large, or
  as resting on untested code is information; a vanished one is a pass nobody can audit.
- **Per-axis verdicts** — one line per axis, even when the answer is clean, and for
  Reuse the line names what was searched (the added symbols checked, and against
  what). A blanket "nothing to do" is indistinguishable from "did not look" — the same
  defect this kit's field reports keep finding in checks whose denominator was assumed
  — so the axis line is the denominator, written down. Three arcs of blanket
  "nothing to do" is what put this pass on a deletion clock.
- **Findings, not edits** — anything the prime directive stopped, and nothing you went
  looking for. This is not a bug hunt: you will pass directly over behavior you are
  forbidden to change, and what you noticed *while doing the work* is owed to the caller.
  A swallowed error you declined to fix, a branch that cannot be reached, a convention
  in `CLAUDE.md` the code contradicts — name it, say you did not touch it, and move on.
  Write **none** if there were none.
- **The final gate result** for the whole scope.

## Done when

Every proposed move is either applied with a green gate behind it or recorded as dropped
with its reason, the final gate is green, every behavior-changing improvement noticed
along the way is left as a finding rather than an edit, and **all five report sections
have been written — `none` where that is the answer, and the Reuse axis line naming
its search**. A pass that ends with an
unexplained diff is not done, whatever the gate says.

## Notes

- **Both CLIs.** This skill installs to `.claude/skills/change-simplify/`, which Claude
  Code and Copilot CLI both read. It names no CLI-specific agent, tool, or model on
  purpose: a pinned model is silently downgraded on one CLI, and a named subagent type
  does not exist on it at all. Keep it that way when editing.
- **On the Claude Code built-in.** Claude Code ships a `simplify` skill of its own. This
  one is the kit's portable equivalent, so the pass exists on both CLIs and the process
  can name it without knowing which CLI is running. Where both are present, either
  serves; do not run both over the same range.
