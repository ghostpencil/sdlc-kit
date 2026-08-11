# End Slice

Close out the current slice: gate → quality pass → review → fix → mutation check →
verification → commit → record check → record. Runs without asking except for
owner-facing design questions. Process reference: `spec/SDLC.md`.

## How to use

`/end-slice` — after the slice's exit criteria are met, before `/clear`. **Owner-typed
only**: `/next-slice` ends at the slice-ready hand-back and never chains into this
command — close-out commits and pushes without asking, and the hand-back is the owner's
moment to inspect the work first. If this command was reached without the owner asking
for it, stop.

The review (step 4) is the analysis-heavy part; check the model policy recorded in
`spec/SDLC.md` (`/model` to switch — on a CLI where routing is operator-performed, the
policy names the moment to set it).

## Workflow

### 1. Sanity check

- `git status` + `git diff --stat`. If the working tree is clean and nothing is
  uncommitted, report that there is no slice to close and stop.
- Confirm you are NOT on the main branch. If you are, stop and say so — slices live on
  a phase or cleanup branch.

### 2. Run the gate

Run the gate exactly as defined in `spec/SDLC.md` — the steps recorded there, in order.

All steps must be green. If not, fix the failures first (TDD skill rules apply if tests
change), then re-run. Do not proceed on red.

Green means green **against the gate baseline recorded in `spec/SDLC.md`** — zero for a
clean adoption, the recorded counts for a project adopted with a red baseline. Any
increase is a regression and is fixed in this slice. Read the baseline from `spec/SDLC.md`;
never assume it is zero. And green here is green **in this session's shell** — where
local and CI disagree about a measurement, CI is authoritative and the disagreement is
itself a finding (`spec/SDLC.md` states the rule).

### 3. Quality pass — optional, and never silent

Run the `change-simplify` skill on the working diff: reuse, simplification, efficiency,
and altitude, applied only where this slice introduced or worsened the condition. It is
installed by `/sdlc-setup` into `.claude/skills/change-simplify/` and is available on
both CLIs.

It runs **here, before the review**, so the reviewer reads the code that will actually
be committed — a quality pass run afterwards invalidates the review it follows.

Three rules make it safe to run automatically:

- **Behavior is frozen.** Every move is behavior-preserving. An improvement that would
  change what the code does is a **finding**, not an edit — including one that would fix
  something obviously wrong. A behavior change smuggled in under a refactor is invisible
  to step 4, because a reviewer reads a refactor as behavior-preserving by definition.
- **One move at a time, gate between.** Not a batch then the gate. A batch that goes red
  says only that the batch broke something; one at a time makes every failure
  self-locating.
- **Read-only about the tree's shape**, exactly as the review is: no `git checkout`,
  `git restore`, or `git stash`. The code being improved is uncommitted, so there is no
  restore point behind it.

**Skipping it is legitimate; skipping it silently is not.** On a small or mechanical
slice there may be nothing to do — say that in the hand-back (step 10), along with what
was applied if it ran. A pass whose outcome nobody stated is one nobody can weigh.
Either way the one-line outcome also goes into the slice commit body (step 7) —
`quality: <N moves applied | nothing to do | skipped — reason>` — so the record
outlives the session.

### 4. Slice code review

Run the `diff-review` skill on the working diff (uncommitted changes, plus any commits
this slice has already made on the branch — `git diff <main>...HEAD` if the slice spans
commits). It reviews along two axes that fail independently and are reported side by
side, never merged: **Spec** — does this implement the slice's exit criteria, and only
those — and **Standards** — does it follow the conventions recorded in `CLAUDE.md`
*Runtime Conventions*. The skill is installed by `/sdlc-setup` into
`.claude/skills/diff-review/` and is available on both CLIs; it names no CLI-specific
agent or model.

The built-in `/code-review` (Claude Code only — like the fan-out below, it does not
exist on Copilot CLI) is the owner-typed, billed escalation — it is not this
step, and this command cannot launch it. On Claude Code a deeper specialist fan-out
(`pr-review-toolkit`) may be available; it is **optional**, and if it ran, say so in
the hand-back (step 10). The same rule binds any substitution: a review whose depth is
not stated is one nobody can weigh, and a good substitute review is exactly the kind
nobody thinks to question.

The reviewer reviews the **uncommitted working diff by design**, so a clean-tree rule
cannot protect it; the discipline binds to the agent instead: **the review is read-only
in the shared tree.** No `git checkout`, `git restore`, or `git stash`; fixes come back
as findings, never as edits. A reviewer that "helpfully" reverts or rewrites a file is
destroying the very diff it was asked to review — a real arc lost two uncommitted fixes
to exactly that.

Two lenses the diff-shaped review structurally lacks — apply them explicitly:

- **Consumers of changed behavior.** For every error/return path this slice changed
  (raises, handlers, status codes, return shapes), name each **consumer** of that path
  and state what it did with the *old* behavior. The defects that survive clean slice
  reviews live one layer away, in a consumer written against behavior that just
  changed — nothing in the diff itself looks wrong.
- **Test doubles.** Does any double in this slice omit a side effect or simplify the
  error surface of what it replaces? A double one field simpler than reality makes the
  defect it hides structurally unreachable in tests (`spec/TESTING.md`, mock policy).

If the slice changed error propagation, added a catch or failure path or logging
around one, swept the codebase for a pattern or wrote a script or check whose output
will be trusted, touched an object that outlives a request or is reachable
from more than one, took in outside data or passed it to an interpreter, touched
credentials or an externally reachable surface or added logging or error output near
either, or added a test the slice itself then deleted, skipped, or gutted (or ran
under armed TDD-ordering guards and a new test reaches into internals the mock
policy fences off), also apply the matching lens from
`.claude/commands/REVIEW_LENSES.md`; otherwise skip that file.

Triage findings — **verify each one against the source before it enters any pile.** A
finding is a claim about the code; severity is asserted by the reviewer, not measured,
and a false premise survives review at CRITICAL just as easily as at LOW. Findings that
did not survive verification are reported in the hand-back (step 10) alongside the ones
that did, never dropped silently.

- **Fix now:** correctness bugs, silent failures, trust-boundary violations, anything
  CRITICAL/HIGH.
- **Defer:** style/structure improvements, latent issues with no current trigger. Each
  deferred item gets a one-line entry with rationale (step 9), its stated cause marked
  **measured** (you reproduced or observed it) or **suspected** (you inferred it) — the
  reader of that entry needs to know what still needs checking, because a backlog entry
  is a hypothesis with a timestamp, not a finding.
- **Owner question:** anything that is a design decision, not a defect — HALT and ask,
  per the hand-back standard (`spec/SDLC.md`, *Owner halt points*): plain English, the
  decision numbered and marked, options with a recommendation.

One finding class overrides the buckets: a finding that contradicts a **ratified spec
decision** (`diff-review` names these as spec conflicts, CRITICAL). It is neither
fixed silently under Fix-now nor deferred — it takes halt 3 (`spec/SDLC.md`): fix the
code now, or amend the decision it contradicts, and which one yields is the owner's
call, not the review's.

If fixes were applied, re-run the gate.

The review step is done when every finding is dispatched — fixed, deferred with its
marker, discarded with its reason, or raised to the owner — and the hand-back names
the discards. A finding still sitting in none of those states is the step not finished,
however far the conversation has moved on.

### 5. Mutation check — a new guard must be seen to fail

For every **new guard, branch, or error path** this slice added (review fixes
included): delete or invert it once, run the suite, and watch it fail on exactly the
test that claims to pin it — then restore and confirm green. Use the mutation-testing
skill (`mutation-testing`, installed by `/sdlc-setup`) for anything beyond a quick
delete-and-run. A check is only trustworthy once it has been made to disagree; a guard
whose deletion leaves the suite green is untested code wearing a test's name, and this
practice caught exactly that on a real project — twice — in guards whose tests could
not have failed. The runs happen in this session's shell — the same scope, and the
same local-vs-CI caveat, as the gate (step 2). The step is done when every new guard has been seen to fail on
exactly its own test; a guard not yet seen to fail is not yet closed. The one-line
outcome goes into the slice commit body (step 7) —
`mutation: <N guards, each seen to fail | none — no new guards>`.

### 6. Slice verification — optional, and never silent

Run the `change-verify` skill on a nontrivial slice: exercise the changed behavior
through the path its real caller takes — the CLI's argv, the HTTP route, the queue
message — not the test harness. The gate (step 2) is evidence about the suite; this is
the only slice-level evidence about the **behavior**, and without it the first time
anything runs the change outside the harness is phase end — a real adoption's ingestion
break survived its slice's close-out exactly that way and surfaced at phase end, four
fix commits later. The skill is installed by `/sdlc-setup` into
`.claude/skills/change-verify/` and is available on both CLIs; its own report contract
applies (a transcript block per run — a pass not observed is not a pass).

Same contract as step 3: **skipping is legitimate; skipping silently is not.** On a
small or mechanical slice — docs, config, a change the gate fully pins — state the skip
and its reason in the hand-back (step 10). Either way the one-line outcome goes into the
slice commit body (step 7): `verify: ran — <verdict per behavior, naming the shell it
ran in>` or `verify: skipped — <reason>`, so the record outlives the session. The
shell matters because this step runs in the **agent's** shell: a pass here does not
stand in for halt 4's owner acceptance, which is the same exercise in the owner's —
and a documented run command once died at import for the owner while passing cleanly
for every agent.

If it observed a break, fixes go through the loop the review's fixes do: apply, re-run
the gate, and any new guard joins step 5's mutation obligation.

### 7. Commit the slice

Write the multi-line message in the shell tool's own literal form — a heredoc on a
POSIX shell tool (Claude Code's Bash), a single-quoted here-string on a PowerShell
one (Copilot's measured shell tool) — never a form the executing shell does not parse.
Subject line in the project's own convention where one is recorded; the shape below
is the kit's default (`spec/SDLC.md` states the rule):

```
git add <files>   # add the slice's files explicitly; never git add -A blindly
git commit -m "$(cat <<'EOF'
<type>(<area>): <slice summary>

<what and why, briefly>

RED: <test command> — <the failing line> — exit <code>   (one per behavior batch)
quality: <N moves applied | nothing to do | skipped — reason>
mutation: <N guards, each seen to fail | none — no new guards>
verify: <ran — verdicts | skipped — reason>
EOF
)"
```

The `RED:` lines are the slice's observed-red record, copied from the running record
`/next-slice` §4 keeps as each red is observed — the exact test command, the failing
test's line, the exit code. A behavior whose red was not observed is written
`RED: not observed — <reason>`, never omitted — and a slice with no behavior batches
at all (docs, config) writes the zero-form `RED: none — no behavior batches this
slice`, so the record line exists either way. The commit body is where this record
lives durably: `/sdlc-retro`'s step-evidence sweep reads it off `git log`, and an
observed red cannot be reconstructed at close-out — the commit only carries what the
loop already wrote down.

### 8. Verify the record — structural, and quoted

Run the close-out checker on the commit just made — in **the agent's shell tool**,
the same scope as the gate — with the invocation recorded beside the gate in
`spec/SDLC.md`, taking the close-out checker note's line **for the CLI running this
session** (where `sh` resolves in the agent's shell it is
`sh .github/hooks/sdlc-close-out.sh check`), and quote its output in full in the
hand-back — a pass not observed is not a pass. If `spec/SDLC.md` carries **no**
such note, this project's process file predates the checker (`/sdlc-update`'s
transition note names exactly this window): say so in the hand-back and have the
note resolved per that procedure — never guess an invocation, because on a shell
without `sh` the guess dies as a shell error, not as the checker's own CANNOT
CHECK.

The checker verifies **structural presence only**: every evidence line of step 7's
record present, or carrying its stated-skip form — one line per key for
`quality:`/`mutation:`/`verify:` (a duplicate fails: nobody knows which line is
the record), each key at the start of its line — with silent absence failing
loudly. It never verifies truth — its own output says so — and COMPLETE is not
evidence the work behind a line happened; the steps that produced the lines remain
the record of that.

- **INCOMPLETE** — `git commit --amend` the slice commit with the real outcome, or
  with the stated-skip form if the step was skipped. Never with invented evidence:
  a fabricated line is worse than a missing one, because the checker will believe it.
  Re-run until COMPLETE.
- **CANNOT CHECK** — fix what it names and re-run. Never proceed past it silently;
  the checker fails closed on purpose, the opposite of the hook rule, because a
  command step's failure is seen and quoted rather than silently swallowed.

### 9. Record in PROJECT_INDEX

Update `spec/PROJECT_INDEX.md`:
- Mark the slice done in the current phase's status/START HERE section. **Status only —
  one line.** The close-out records that the slice is done and what is next; the detail
  goes where it will live anyway — the phase spec — and the commit message is already
  the better record. A real adoption wrote 83–163 lines of per-slice detail into the
  index five times and paid an archiving step once per arc to move it back out; the
  phase-close archival bullet stays as the safety net, not the plan.
- Append deferred review findings to the backlog with rationale, provenance
  (e.g. "(slice review, <date>)"), and the cause marker from step 4's triage
  (**measured** / **suspected**).
- If this slice added a tool, runtime, or service the gate now requires, record it (gate
  section of `spec/SDLC.md`; Environment gotchas in PROJECT_INDEX) and add it to CI in
  the same commit — a gate dependency discovered by a contributor's red run is a
  documentation bug.
- **Escalate a recurring gotcha instead of re-describing it.** Before appending to
  Environment gotchas, read what is already there: if this slice is the **third
  consecutive** one to record the same hazard, it stops being a note and becomes a
  check — a gate step, a hook, or a test — or the owner ratifies it as unpreventable and
  the entry says so, with the recurrence count. Those are the hazard's only two closed
  states; a sharper note is neither. Prose in a status document is not a
  control: a real adoption recorded an editor silently rewriting line endings four
  times, each note sharper than the last, each one followed, and the hazard recurred
  every time. And when the check becomes a control: **a control that hands the operator a
  remediation command must scope that command to the population the control actually
  flags.** An operator acts on the failure message under time pressure — an unscoped
  fix-everything one-liner from a line-endings check, applied over the whole tracked
  tree, corrupted two PNGs whose magic bytes legitimately contain CR LF. The *verify
  the denominator* lens applies to the control's own output.
- **Kit friction gets written now or never.** Was anything in this slice friction with
  the *process* rather than with the code — a rule fought, worked around, or silent
  where a decision was needed? If so, one line to the Kit friction log in
  PROJECT_INDEX, now, in the log's prescribed shape —
  `- <YYYY-MM-DD> — <the friction, one sentence> — open` — the same shape the retro
  later flips to `absorbed by retro <date>`; an entry without the status word is one
  the sweep has to guess about. Slice close is the last moment the evidence is still
  accurate; the retro reads this log and cannot reconstruct what was never recorded —
  one adoption's retros produced 23 findings across three arcs while the log gained
  zero entries, because no step ever prompted the writing.
- Note the next slice up, so `/next-slice` in a fresh session can orient without help.

Commit the docs change separately (`docs: PROJECT_INDEX — <slice> done; next up <next>`).

### 10. Hand back

Report per the hand-back standard (`spec/SDLC.md`, *Owner halt points*). Open with a
plain-English executive summary in bullets: what the slice now does, gate green (test
count), and what is next — with any decision the owner still owes **numbered and
explicitly marked** (usually there is none; an open design question is the exception).
Then the detail, after the summary and never mixed into it: quality-pass outcome (N
moves applied / N dropped, or **skipped** with the reason — never omitted), review
outcome (N fixed / N deferred / N discarded as unverified, naming those),
mutation-check outcome (N guards checked, each seen to fail), **RED evidence per
behavior batch** (the command, the failing line, the exit code — with `not observed`
stated, never omitted, same contract as the quality pass), **verification outcome**
(the verdicts, or skipped with the reason), **the record check's quoted output**
(step 8 — COMPLETE, or how an INCOMPLETE was remediated), any tool substituted for
one this file names, and commit hashes. End with: **safe to `/clear`**.

## Notes

- Never mark the slice done if the gate is red or the review left unfixed CRITICAL items.
- Do not start the next slice in this session — fresh context per slice is the rule.
- Push the branch (`git push`) so work is not stranded locally, but never open a PR here —
  that is `/end-phase`. The rule behind the prohibition: **slices accumulate on one arc
  branch until `/end-phase`**, in BUILD and STABILIZATION alike, so the whole-arc review
  sees everything the arc changed. Follow-on work arising from this slice's own review
  belongs on this same branch, not on a fresh one.
