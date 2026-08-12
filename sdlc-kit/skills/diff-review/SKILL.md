---
name: diff-review
description: Two-axis review of a change set — Spec (does it implement what the slice or phase spec asked, and only that) and Standards (does it follow the project's documented conventions). Use at /end-slice on the working diff and at /end-phase on the whole arc. Runs the axes independently and reports them side by side without merging them.
---

# Diff Review

Review a change set along two axes that fail independently, and report them that way.
A change can be flawless code that implements the wrong thing, or the right thing built
against no convention at all — merging the two verdicts hides exactly that. Process
reference: `spec/SDLC.md`.

**Prime directive: never invent the spec.** If the change set has no stated intent you
can locate, say so and skip the Spec axis. An inferred spec reviews the diff against
itself and always passes.

## How to use

Invoked by `/end-slice` (step 4, the working diff) and `/end-phase` (step 5, the whole
arc). It can also be run directly on any range.

Arguments, all optional:

- **A scope** — `working` (uncommitted changes, the default at slice end),
  `<main>...HEAD` (the arc, the default at phase end), or any git range.
- **An axis** — `spec` or `standards` to run one alone. Default is both.

## What this skill is not

- **Not `/code-review`.** That is the owner-typed, billed escalation (Claude Code
  only); a session cannot launch it, and no kit command means it by "review".
- **Not the review lenses.** `.claude/commands/REVIEW_LENSES.md` covers runtime failure
  modes — error propagation, swallowed errors, denominators, shared state, untrusted
  input, secrets — each behind its own trigger. This skill does not restate them, and
  the calling command decides whether a lens applies. If a finding here is really a
  lens finding, name the lens and stop; do not re-derive it.
- **Not a fixer.** The review is **read-only in the shared tree.** No `git checkout`,
  `git restore`, or `git stash` — at slice end the diff under review is *uncommitted*,
  so a "helpful" revert destroys the very thing being reviewed. Fixes come back as
  findings. The calling command applies them.

## Workflow

### 1. Pin the fixed point, and say what it is

Establish the exact range before reading anything: `git status` and `git diff` for
`working`, `git diff <main>...HEAD` for an arc. State the range and the file count in
the report. A review whose scope was never stated cannot be checked for coverage later,
and "reviewed the changes" is the claim that hides a missed file.

If the range is empty, that is the finding — report it and stop. An empty diff silently
reviewed as clean is how a review passes without reading anything.

### 2. Axis A — Spec

**The question: does this change set implement what was asked, and only that?**

Find the intent, in this order, and stop at the first that exists:

1. The **current slice's exit criteria** in the phase spec under `spec/` — the normal
   case at slice end. `spec/PROJECT_INDEX.md` names the active phase and slice.
2. The **phase's exit criteria** in the same phase spec — the normal case at phase end.
3. A path the caller passed explicitly.
4. Nothing. **Then report "no spec located" as the axis result and skip to Axis B.**
   Do not substitute the commit messages or the branch name; those describe what was
   done, and reviewing the work against its own account of itself is not a check.

Report, per criterion, one of:

- **Met** — name the file and symbol that satisfies it.
- **Not met** — the criterion and what is missing.
- **Unverifiable from the diff** — say why. A criterion about behavior nobody can see
  in the change set is a real answer, not a failure of the review.

Then two questions the criteria list cannot ask itself:

- **Scope creep.** Is there anything in the diff that no criterion asked for? Name it.
  Unasked-for work is not automatically wrong — it is automatically *undiscussed*, and
  it rides into the arc without ever having been planned.
- **Silent narrowing.** Did a criterion get satisfied in a weaker form than written —
  the happy path only, one caller of three, a stub where behavior was specified? This
  is the failure the gate cannot catch, because a narrowed implementation is still
  green.

### 3. Axis B — Standards

**The question: does this change set follow the conventions this project documented?**

Find the standards, in this order:

1. **`CLAUDE.md`, *Runtime Conventions*** — the project's own recorded rules (logging
   levels, error handling, config access, whatever it wrote down). This is the kit's
   home for them.
2. Any other convention file the repo carries (`CONTRIBUTING.md`, a style guide).
3. The baseline below, if neither exists.

**A documented project standard always wins over the baseline.** If the repo says to do
something the baseline calls a smell, the repo is right and the baseline is silent —
say so explicitly in the report rather than filing a finding you already know is wrong.

**The baseline** — structural smells, applied only where the diff introduced or worsened
one. Never file a smell that the change set merely stood next to.

| Smell | What it looks like |
|---|---|
| Mysterious name | A name that needs the implementation read to understand |
| Duplicated code | The same decision expressed in more than one place |
| Long function | A function doing several things, none of them nameable alone |
| Feature envy | A function more interested in another object's data than its own |
| Data clumps | The same group of values passed together everywhere, unnamed |
| Primitive obsession | A domain concept carried as a bare string, int, or dict |
| Repeated switches | The same conditional over the same type in several places |
| Shotgun surgery | One conceptual change forcing edits across many files |
| Divergent change | One file edited for several unrelated reasons |
| Speculative generality | Abstraction serving a caller that does not exist |
| Message chains | A reaching through a chain of objects to get at a fourth |
| Middle man | A class or module that only forwards |

The baseline is a **prompt to look**, not a defect list. A smell is a question about
design, and "this is fine here, because —" is a complete and frequent answer.

### 4. Report the axes side by side — never merged

Two sections, both always present, each with its own verdict. Do **not** rank findings
across axes, and do not collapse them into one severity list. A Spec miss and a
Standards smell are different kinds of wrong, and the reader acts on them differently.

Per finding: the file and line, what is wrong, and why it matters — in that order, one
finding per claim.

**Every finding is a claim about the code, and severity is asserted rather than
measured.** Verify each against the source before reporting it. Findings that do not
survive verification are reported as such, never dropped silently — a discarded finding
with its reason is information; a vanished one is a review that cannot be audited.

One severity rule is fixed: **a finding that contradicts a ratified spec decision —
a decision the phase spec records the owner approving — is CRITICAL and is named as
a spec conflict**, whatever its mechanical size. It is the one finding class the
close-out may not defer by default (`spec/SDLC.md`, halt 3): the code and a ratified
decision cannot both stand, and which one yields is the owner's call, not the
review's.

Close with the range reviewed, the file count, and the axis verdicts. If either axis was
skipped, say which and why.

## Done when

Both axes have returned a verdict — including "no spec located" or "no documented
standards, baseline applied" — every finding names a file and line and has been verified
against the source, and the report states the range it covered. An axis with no verdict
is the review unfinished, however complete the other one looks.

## Notes

- **Both CLIs.** This skill installs to `.claude/skills/diff-review/`, which Claude Code
  and Copilot CLI both read. It names no CLI-specific agent, tool, or model on purpose:
  a pinned model is silently downgraded on one CLI, and a named subagent type does not
  exist on it at all. Keep it that way when editing.
- **On fan-out.** Running the two axes as parallel sub-agents is a legitimate
  optimization where the CLI supports it, and it is how the design this skill borrows
  from works. It is not required, and the axes must stay unmerged either way. Where a
  sub-agent is spawned, it is read-only in the shared tree like everything else here.
