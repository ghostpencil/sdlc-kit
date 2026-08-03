---
name: change-verify
description: Exercise a change through the path its real caller takes, before committing, and report what was actually observed rather than what should follow. Use before committing a nontrivial slice and at phase end for the phase-level verification. A green gate is evidence about the test suite, not about the behavior.
---

# Change Verify

Exercise a change the way something real reaches it, and report what you observed.
Process reference: `spec/SDLC.md`.

The gate proves the suite agrees with the code. It cannot prove the behavior happens,
because a suite exercises the code through the harness rather than through the path a
caller takes — and the two differ in exactly the places that break: startup, wiring,
configuration, the environment. This skill covers that gap and nothing else.

**Prime directive: never report a pass you did not observe.** "This should work" is a
prediction, not a verification, and a prediction recorded as a result is worse than no
verification at all — it spends the credibility of a check that never ran. If the
behavior could not be exercised, that is the finding.

**This skill runs commands. It has no read-only mode, and reasoning is not a
substitute.** Do not write any part of the report before the runs have happened — not a
summary, not a heading, not a provisional verdict. Drafting the report first is how a
run gets described instead of performed, and the description is always more confident
than the run would have been. If you are about to report "not exercised" because you
have not tried yet, that is not a finding — **go and try.** The finding is reserved for
a path you attempted and could not reach.

## How to use

Invoked before committing a nontrivial slice, and at phase end for the phase-level
verification `/end-phase` step 2 calls for. It can also be run directly on any change.

Arguments, all optional:

- **What to exercise** — a behavior, an entry point, or a criterion. Default is what the
  current slice's exit criteria describe.
- **A run command** — defaults to the one `CLAUDE.md` records for the project.

## What this skill is not

- **Not the gate.** Lint, typecheck, and tests are `/end-slice` step 2 and have already
  run. Do not re-run them and report the result here; a green gate is the precondition
  for this pass, not its outcome.
- **Not `diff-review`.** That reads the change against the spec and the project's
  conventions. This one runs it. A change can review clean and not work.
- **Not owner acceptance.** Phase end *(halt 4)* has the owner run the project
  themselves, in their own shell. That halt exists because the agent's environment and
  the owner's differ, and this skill cannot stand in for it — at most it makes the
  halt likelier to pass by finding the breakage first.
- **Not a fixer.** What you find comes back as findings. The calling command or the
  session applies them, then the gate runs again.

## Workflow

### 1. Pin what changed

Establish the change set before anything else: `git status` and `git diff` for the
working tree, `git diff <main>...HEAD` for an arc. State the range and the file count.

**Never ask the caller what the change was — read it.** The diff is on disk, and a
verification that begins by requesting a scope it could have looked up has already
failed to do the one thing it exists to do, which is go and find out.

If the range is empty, check whether the work is staged or already committed before
concluding there is nothing to verify, and say which you found.

### 2. State what would count as the behavior happening

Before running anything, write down the observable: what you expect to see, where you
expect to see it, and what would distinguish it from the behavior *not* happening. Do
this first, in writing.

Deciding after the fact whether an output looks right is how a broken change gets
verified — the result arrives, it is plausible, and the standard quietly reshapes itself
around it. A criterion written before the run cannot do that.

If the behavior has no observable — nothing in the output, the logs, the filesystem, the
database, or the exit code changes — say so and stop. **That is a finding**, and usually
a real one about the change rather than about the verification.

### 3. Reach it the way something real does — by actually running it

**Execute.** Start the thing and drive it through its own front door: the CLI's argv,
the HTTP route, the queue message, the UI. Not the test harness, not the internal
function. Capture the command, its output, and its exit code as you go — that captured
text is the only thing the report is allowed to be built from.

The failures this step exists to catch live in the wiring — a module that imports
cleanly in the test process and not at startup, a config key read from an environment
the suite fakes, a route registered nowhere, a dependency the tests inject and
production never constructs. Every one of those is invisible from inside the suite by
construction.

Where the real path genuinely cannot be driven here — it needs credentials, a deploy, a
device, another service — **do not substitute the nearest reachable thing and report a
pass.** Say which path was exercised, which was not, and what remains unverified. A
partial verification named as partial is useful; one presented as complete is a false
negative with a signature on it.

### 4. Watch for the failure the change could still have

Exercise the unhappy paths the change touched, not only the one it was written for: the
error branch, the empty input, the second call, the missing file. A change verified only
along its happy path has been verified against its author's intent rather than against
the system.

Then check what the change was **not** supposed to move. Run the neighbouring behavior
that shares its code path and confirm it still does what it did. Regression is the
failure mode that no criterion in the slice spec is written to catch, because nobody
writes a criterion for the thing that already worked.

### 5. Record the environment the result came from

A verification result is a claim about a system, and the system includes the machine.
Record what would let someone else get the same result or explain a different one: the
command as actually run, the interpreter or runtime and its version, and any
environment variable, config file, or service the run depended on.

This is the step that pays at phase end. When halt 4 fails in the owner's shell after
passing here, the difference between the two environments is the defect, and it is only
findable if this run wrote down what its own was. Anything resolved that way belongs in
`CLAUDE.md` *Environment gotchas*.

## Report

**Every claimed run appears as a transcript block, or it did not happen.** For each one,
in this shape — the exact command on one line, then the literal bytes it printed in a
fenced block, then the exit code:

```
$ <the exact command, copy-pasteable>
<the output, verbatim — the real bytes, not a description of them>
exit: <code>
```

**Characterizing output is the tell.** "Observed the expected result", "clean exit",
"produced correct output" are all things a report says when no command was run — they
are what a prediction sounds like when it is wearing a result's clothes. If you cannot
paste the literal bytes, you did not run it, and the honest verdict is *not exercised*.
A verification whose evidence is its own confidence is the failure this skill exists to
prevent, and it fails silently by construction: the report reads better than a real one.

Then:

- **What was exercised** — the entry point and the inputs, once per transcript block.
- **Verdict per behavior** — observed working / observed broken / **not exercised, and
  why**. The third is a first-class result and must never be folded into the first.
- **The environment** — from step 5.

## Done when

Every behavior in scope has one of the three verdicts, each observed verdict is backed
by something quoted from the run rather than described, and everything not exercised is
named along with what stopped it. A behavior with no verdict is the verification
unfinished, however convincing the ones above it look.

**The self-check that catches the common failure: a report containing no quoted command
output is not a report, it is a plan.** If nothing in it was copied out of a run, no
verification happened — go back to step 2 and run something. Likewise, a "not exercised"
verdict must name the obstacle that stopped an attempt; "I have not run it yet" is not
an obstacle.

## Notes

- **Both CLIs.** This skill installs to `.claude/skills/change-verify/`, which Claude
  Code and Copilot CLI both read. It names no CLI-specific agent, tool, or model on
  purpose — see `reference/COPILOT.md`.
- **On the Claude Code built-in.** Claude Code ships a `verify` skill of its own. This
  one is the kit's portable equivalent, so the pass exists on both CLIs and the process
  can name it without knowing which CLI is running. Where both are present, either
  serves; do not run both and report the pass twice.
