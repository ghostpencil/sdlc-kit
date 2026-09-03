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
`spec/SDLC.md` (*Records*; `/model` to switch — on a CLI where routing is
operator-performed, the policy names the moment to set it).

## Workflow

### 1. Sanity check

- `git status` + `git diff --stat`. If the working tree is clean and nothing is
  uncommitted, report that there is no slice to close and stop.
- Confirm you are NOT on the main branch. If you are, stop and say so — slices live on
  a phase or cleanup branch.

### 2. Run the gate

Run the gate exactly as recorded in `spec/SDLC.md` (*Records*) — the steps recorded
there, in order.

All steps must be green. If not, fix the failures first (TDD skill rules apply if tests
change), then re-run. Do not proceed on red.

Green means green **against the gate baseline recorded in `spec/SDLC.md`** (*Records*)
— zero for a clean adoption, the recorded counts for a project adopted with a red
baseline. Any increase is a regression and is fixed in this slice. Read the baseline;
never assume it is zero. And green here is green **in this session's shell** — where
local and CI disagree about a measurement, CI is authoritative and the disagreement is
itself a finding (`spec/SDLC.md` states the rule).

### 3. Quality pass — optional, and never silent

Run the `change-simplify` skill on the working diff: reuse, simplification, efficiency,
and altitude, applied only where this slice introduced or worsened the condition. It is
installed at `.claude/skills/change-simplify/` and is available on
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
Either way the one-line outcome also goes into the slice commit body (step 7) — so the
record outlives the session:

```
quality: <N moves applied | nothing to do | skipped — reason>; reuse: <what was
         searched, and against what | not searched — reason>
```

**The `reuse:` half is not decoration, and it is here because the record line without it
was measured.** The skill's own contract requires per-axis verdicts and, for Reuse, a
line naming *what was searched and against what* — because *"an unsearched 'no
duplication' is not a verdict, it is a guess with the same spelling."* On a real arc the
skill was dispatched in **every one of five slice sessions** and the durable record still
carried **zero** named searches, because this line asked only for a move count: the half
the command restated survived into the commit bodies and the half only the skill carried
did not (field, 2026-09-01). Dispatching the skill is therefore *not* what preserves its
contract — the record line is. A move that names the duplicate but not the search does
not satisfy this; naming the search is what distinguishes a pass that looked from one
that glanced.

**This is the first close-out step that writes production code, so it is where the
licence is declared — and it is the close-out licence, not the refactor one.** Where the
TDD guards are installed, before the first edit here: write one line naming the step and
move it to `.git/sdlc-tdd/close-out-license`, behind a counted green, exactly as a
refactor licence is declared. **One declaration covers steps 3 through 6.** Use the
close-out licence because a test edit revokes the refactor one, and close-out's own
mandated order puts test edits between its production writes — step 4's review fixes
tests, step 5's mutation restores them, and a refactor licence declared here is revoked
by the method it was declared for. On a real arc that cost seven re-declarations in a
single phase, three of them inside one slice, across three consecutive retros (field,
2026-09-01). Every test edit the close-out licence survives is counted in the guard log,
so a licence left open past step 6 is visible in review; it ends with the session either
way. Declaring it is not a formality here — this step edits production code after the
gate has run, so the write is behavior-preserving by construction and the licence is its
precondition.

### 4. Slice code review

Run the `diff-review` skill on the working diff (uncommitted changes, plus any commits
this slice has already made on the branch — `git diff <main>...HEAD` if the slice spans
commits). It reviews along two axes that fail independently and are reported side by
side, never merged: **Spec** — does this implement the slice's exit criteria, and only
those — and **Standards** — does it follow the conventions recorded in `CLAUDE.md`
*Runtime Conventions*. The skill is installed at
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
either, deleted, skipped, or gutted a test `spec/PRODUCT_CONTRACT.md` names as a
pin (opening the contract to check that is the disposal-intent lens's sanctioned
exception to its read-at-phase-boundaries rule; a project without the file
predates it — say so rather than silently not firing), or added a test the slice
itself then deleted, skipped, or gutted (or ran
under armed TDD-ordering guards and a new test reaches into internals the mock
policy fences off), also apply the matching lens from
`.claude/commands/REVIEW_LENSES.md`; otherwise skip that file. **Each applied lens
reports by name with its verdict** — `<lens>: <finding, file and line | clean>` —
and a review that
applied none writes `no lens triggered`; an unnamed lens verdict cannot be credited
to the lens (the file's own preamble states the contract). **That verdict goes into
the slice commit body as the `lenses:` line (step 7), where the other per-slice
evidence lines already outlive the session.** The review hand-back is not retained,
and only a lens *finding* travels onward under its own name — so before this line
existed, a lens that ran and found nothing left no trace anywhere, and two field arcs
of lens evidence could not distinguish *ran and clean* from *never triggered*. A clock
that deletes a lens for having no catch needs the second number, not the first.

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
skill (`mutation-testing`, installed at `.claude/skills/mutation-testing/`) for anything beyond a quick
delete-and-run. A check is only trustworthy once it has been made to disagree; a guard
whose deletion leaves the suite green is untested code wearing a test's name, and this
practice caught exactly that on a real project — twice — in guards whose tests could
not have failed. The runs happen in this session's shell — the same scope, and the
same local-vs-CI caveat, as the gate (step 2). The step is done when every new guard has been seen to fail on
exactly its own test; a guard not yet seen to fail is not yet closed. The one-line
outcome goes into the slice commit body (step 7) —
`mutation: <N guards, each seen to fail | none — no new guards>`.

**A characterization slice has no new guard, and is not exempt — its trigger reads the
other way round.** When this slice's tests pin behavior that already existed — a
characterization pass, a coverage backfill, a regression net thrown around code nobody
wrote this week — what is new is the **tests**, so mutate the production code each one
claims to pin and watch that test fail. Read the trigger this way whenever the slice
added tests but no guard: nothing else in the close-out carries any signal about such
a slice, and the exemption runs exactly opposite to the risk — on a real arc the
highest-stakes slice of the phase, 129 tests pinning the module that guards a
non-regenerable database, recorded the evidence a README edit would have recorded.
Where the count is large, **sample instead of exhausting**: take the tests pinning the
behaviors whose silent loss would cost most, and say in the record how many were
checked out of how many (`mutation: 6 of 129 characterization pins, each seen to
fail`) — a stated sample is evidence; an unstated one is the same blank the exemption
left.

**A slice whose deliverable is a sweep, a ratchet, or a check is the third case, and
`mutation: none` is wrong for it.** When the slice ships no guard and adds no test but
its exit criterion *is* a check — "no entry cites a line number", "no module exceeds N
statements", "every declared floor agrees" — then that check is the artifact this step
exists to distrust, and it owes a made-to-disagree run of **itself**. Feed it a planted
violation in a scratch copy and watch it fire on exactly that, then confirm it is clean
on the real tree. This is not pedantry: on a real arc such a sweep needed **five passes
to enumerate its own population** (13 → 15 → 16 → 17 → 18) and one of its patterns
reported a **false clean**, and the slice only caught it by injecting an anchor —
*despite* this step's zero-form rather than because of it (field, 2026-09-01). Record it
in the same shape: `mutation: 1 check seen to fail — <the check>, fed <the planted
violation>, fired on exactly that`.

**One collision to know about before you write the mutation, because it will block you
otherwise.** A counting or sweeping check can only be made to disagree by making the
counted thing **bigger** — you must *add* statements, not delete a guard — and a
throwaway local added inside a function is exactly what a linter's unused-variable rule
exists to flag (`F841` in ruff, `no-unused-vars` in ESLint, and their equivalents).
**Where this project runs an edit-time gate hook** — check `spec/SDLC.md` (*Records*) for
whether one is installed — that hook lints the file just edited and rejects the write
**before the test suite ever runs**, which reads as the mutation being wrong when it is
the only mutation available. On a real arc this cost two blocked attempts in one
slice, 53 findings on the first (field, 2026-09-01). **Write the mutation at module
level**, where an unused-variable rule does not apply, or use a form the project's linter
already tolerates. The two controls have no knowledge of each other by design — the lint
hook has no notion of a mutation in progress — so the workaround is stated here rather
than left to be rediscovered by being blocked. Note that this project may well have
enabled those rules **on the kit's own recommendation** — they are the mechanical half
of the *unconsumed artifact* lens. Both rules are right; they simply had no knowledge of
each other until an arc ran into it, so do not read the block as a sign the linter
config is wrong.

**The close-out licence declared at step 3 covers this step — and this is the step that
most needs it.** Where the TDD guards are installed and step 3 was skipped (so nothing
was declared), declare `.git/sdlc-tdd/close-out-license` here before the first mutation.
Do not fall back to the refactor licence: this step's own prescribed *restore* touches
test files between its production writes, so a refactor licence declared here is revoked
by the method it was declared for — which is what cost one arc three re-declarations
inside a single slice.

**Restore by undoing the edit, not by restoring the file.** This step runs *before*
step 7 commits, so the slice's own implementation is sitting uncommitted in the
working tree underneath the mutation — which makes the obvious mechanism the
destructive one. `git checkout -- <path>` restores the path to **HEAD**, not to its
pre-mutation state: on a file whose slice work is not yet committed it reverts the
mutation *and the slice*, and one arc lost a slice's uncommitted implementation
exactly that way, recoverable only because the code was still in the session's
context. `git stash` parks the slice for the same reason. So:

- **Undo the mutation the way you made it — a targeted edit of the same hunk,
  inverted.** The mutating edit changed specific characters; change exactly those
  back. This is the default, and it is safe whether or not anything is committed.
- **A VCS restore is available only when the path carries no uncommitted work
  behind it** — and that is a thing to *check*, with `git status --short <path>`
  before mutating, not to assume. Clean before the mutation means
  `git checkout -- <path>` is a true inverse; dirty means it is not.
- **Never restore by writing the file's text back through a whole-file
  read-then-write.** One arc corrupted its working tree four times doing exactly
  that, because a read-modify-write normalizes whatever it round-trips (line
  endings, the trailing newline, an encoding a BOM implied) and a restore that
  should have been a no-op silently rewrote every line of the file. A targeted hunk
  edit is not a whole-file rewrite and normalizes nothing.

Either way, confirm the file is back — `git diff -- <path>` empty of the mutation —
before re-running the suite. A mutation left in the tree is the worst outcome
available here, and it is what a failed restore looks like.

**Two more rules that only bite when the loop is hand-rolled, which is how it is
actually run:** mutate **one thing at a time and revert between** — stacked mutations
make a red suite unattributable, and the second mutation's evidence is worthless.
And where a file offers more targets than are worth exhausting, take **a sample of
three to eight** rather than every branch, and say in the record how many of how
many. All of this is stated here rather than left to the skill: `mutation-testing`
carries the same rules at more length and is worth reading when a mutation pass gets
difficult, but two arcs of ledger measured **zero** activations against roughly a
hundred mutations actually run, and a rule that arrives only when a skill happens to
be dispatched is a rule that arrives never.

### 6. Slice verification — optional, and never silent

Run the `change-verify` skill on a nontrivial slice: exercise the changed behavior
through the path its real caller takes — the CLI's argv, the HTTP route, the queue
message — not the test harness. The gate (step 2) is evidence about the suite; this is
the only slice-level evidence about the **behavior**, and without it the first time
anything runs the change outside the harness is phase end — a real adoption's ingestion
break survived its slice's close-out exactly that way and surfaced at phase end, four
fix commits later. The skill is installed at
`.claude/skills/change-verify/` and is available on both CLIs; its own report contract
applies (a transcript block per run — a pass not observed is not a pass).

Same contract as step 3: **skipping is legitimate; skipping silently is not.** On a
small or mechanical slice — docs, config, a change the gate fully pins — state the skip
and its reason in the hand-back (step 10). Either way the one-line outcome goes into the
slice commit body (step 7), so the record outlives the session:

```
verify: ran — <verdict per behavior, naming the shell it ran in>;
        not exercised: <what could not be reached, and why | nothing>
or
verify: skipped — <reason>
```

**The `not exercised:` half is required, and `nothing` is a real answer that must be
written out.** The skill's contract has three verdicts — observed working, observed
broken, and *not exercised, and why* — and says the third *"is a first-class result and
must never be folded into the first."* Only the first two survived into the record on a
real arc: four slices recorded `verify: ran` with credible detail, **all four naming the
shell this line asked for and none containing a single "not exercised"**, including one
whose unreachable path had been deferred behind a seam by a ratified decision in that
same arc (field, 2026-09-01). The ledger showed the skill was not dispatched in any of
those five sessions — so a run that skipped the skill could still produce a
contract-satisfying line from memory of this command alone. It no longer can: a run that
reached everything has to say `nothing`, and a run that did not has to name what it
missed. The
shell matters because this step runs in the **agent's** shell: a pass here does not
stand in for halt 4's owner acceptance, which is the same exercise in the owner's —
and a documented run command once died at import for the owner while passing cleanly
for every agent.

If it observed a break, fixes go through the loop the review's fixes do: apply, re-run
the gate, and any new guard joins step 5's mutation obligation.

Where this step writes a harness or a probe into the repository, it is production source
to the guards and is covered by the close-out licence step 3 declares — which is what the
one declaration spanning steps 3 through 6 is scoped for.

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
lenses: <lens: finding | lens: clean, …  | no lens triggered>
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
the same scope as the gate — with the invocation recorded in `spec/SDLC.md`
(*Records*), taking the close-out checker note's line **for the CLI running this
session** — the note's line is the record, never a guessed form, however common
(`sh .github/hooks/sdlc-close-out.sh check` is typical but measured wrong on some
shells) — and quote its output in full in the
hand-back — a pass not observed is not a pass. If `spec/SDLC.md` carries **no**
such note, this project's process file predates the checker (`/sdlc-update`'s
transition note names exactly this window): say so in the hand-back and have the
note resolved per that procedure — never guess an invocation, because on a shell
without `sh` the guess dies as a shell error, not as the checker's own CANNOT
CHECK.

The checker verifies **structural presence only**: every evidence line of step 7's
record present, or carrying its stated-skip form — one line per key for
`quality:`/`lenses:`/`mutation:`/`verify:` (a duplicate fails: nobody knows which
line is the record), each key at the start of its line — with silent absence failing
loudly. It never verifies truth — its own output says so — and COMPLETE is not
evidence the work behind a line happened; the steps that produced the lines remain
the record of that.

**COMPLETE therefore does not mean the two sub-keys are there.** The checker asserts
presence of the five keys and nothing inside them, so a `verify: ran` line missing
`not exercised:` and a `quality:` line missing `reuse:` both pass it. Read those two
lines yourself before accepting COMPLETE — they are the halves a real arc lost while
every key was present and the record read as complete (field, 2026-09-01), which is
precisely the class a structural check cannot see.

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
  phase-close archival bullet stays as the safety net, not the plan. **The rule now
  carries a number: 25 lines added to the index by this close-out's docs commit**,
  counting the status line plus whatever backlog, gotcha, and friction entries the
  slice genuinely produced. It is a budget, not a limit — see the observer below. The
  number stated here is a copy: the enforcing home is the `BUDGET` constant in
  `.github/hooks/sdlc-close-out.sh`, and that file is kit-owned and copied verbatim,
  so the two can only diverge across kit releases and never per project — the
  observer's own output quotes the budget it actually used, which is the value to
  believe.
- Append deferred review findings to the backlog with an identifier, rationale,
  provenance (e.g. "(slice review, <date>)"), and the cause marker from step 4's
  triage (**measured** / **suspected**). **The identifier is the next integer above
  the file's current maximum, read from the file at the moment of the append** — not
  carried from earlier in the session, and not guessed from the entry count, which
  drifts the moment anything retires. Every step downstream addresses entries by
  number and none of them can detect a collision: one arc minted two pairs of
  duplicates on a single day, two slice reviews writing into different regions of the
  same unordered list, and the document that scoped the next phase then named one of
  the numbers — resolving by content to one entry and by number to two, the other a
  legitimately open finding a scoping pass could have discarded on sight.
- If this slice added a tool, runtime, or service the gate now requires, record it
  (*Records* → *The gate* in `spec/SDLC.md`; Environment gotchas in PROJECT_INDEX) and add it to CI in
  the same commit — a gate dependency discovered by a contributor's red run is a
  documentation bug.
- **Escalate a recurring gotcha instead of re-describing it.** Before appending to
  Environment gotchas, read what is already there: if this slice is the **third
  consecutive** one to record the same hazard, it stops being a note and becomes a
  check — a gate step, a hook, or a test — or the owner ratifies it as unpreventable and
  the entry says so, with the recurrence count. Those are the hazard's only two closed
  states; a sharper note is neither — **and neither is having been absorbed by a
  retro.** A retro that reads the hazard, files it upstream, and even takes an owner
  ruling on it has recorded that the finding was *transmitted*; the hazard is closed
  when something changed, not when someone was told. Count the recurrences past
  absorption, and where a hazard has been absorbed with nothing built, say so in the
  entry with the date it was absorbed — one adoption's guard-ergonomics hazard reached
  **eleven** recorded recurrences with two retros and two owner rulings inside that
  span, because each absorption reset the count to zero. Prose in a status document is
  not a control: a real adoption recorded an editor silently rewriting line endings four
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
  later flips to `absorbed by retro <date> — <disposition>`; an entry without the
  status word is one
  the sweep has to guess about. Slice close is the last moment the evidence is still
  accurate; the retro reads this log and cannot reconstruct what was never recorded —
  one adoption's retros produced 23 findings across three arcs while the log gained
  zero entries, because no step ever prompted the writing.
- Note the next slice up, so `/next-slice` in a fresh session can orient without help.

Commit the docs change separately (`docs: PROJECT_INDEX — <slice> done; next up <next>`).

Then run the close-out checker's **`docs-check`** mode on that commit — in **the
agent's shell tool**, the same scope as step 8 and the gate, using the invocation
recorded in `spec/SDLC.md` (*Records*) with `docs-check` where step 8's line says
`check` — and quote its line in the hand-back. It counts the lines the commit added to
`spec/PROJECT_INDEX.md` and reports them against the budget. It is **log-only**: it
never fails this step, never blocks, and exits 0 even on its own errors, because the
payload it watches legitimately varies and a number cannot tell a genuine six-entry
close from a write-up. `OVER` is a question for the hand-back — which shape was it? —
and "more entries than usual, here is why" is a complete answer to it. What it exists
to catch is the other shape, and the reason it exists at all is that the prose rule
above said *one line* the whole time one adoption wrote 404 index lines across seven
close-outs: a rule with no observer is a wish. A project whose `spec/SDLC.md` predates
the mode (`/sdlc-update`'s transition note names the window) has no line to run — say
so in the hand-back rather than guessing an invocation.

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
(step 8 — COMPLETE, or how an INCOMPLETE was remediated), **the docs budget line**
(step 9 — quoted, and an `OVER` answered rather than merely reported), **the final
architecture footprint** (below, where the project has one), any tool substituted for
one this file names, and commit hashes. End with: **safe to `/clear`**.

**Regenerate the architecture impact view before handing back**, where the project
carries one — after the record check and the docs commit, so it describes the slice as
it actually landed rather than as it looked at the preview:

```
python .github/hooks/sdlc-impact.py slice        # quote the block it prints
python .github/hooks/sdlc-impact.py clear-base   # the slice's base is spent
```

Quote the block, then say **whether the footprint changed from the preview**
`/next-slice` handed back — a close-out review that added a file the owner never saw in
the preview is exactly the case worth naming, and it is invisible unless someone
compares the two. Clearing the base in the same pass is what keeps the next slice from
computing against a spent one. None of this gates the step: it is a comprehension aid,
not verification (`spec/SDLC.md`, *Architecture impact view*), its summary never enters
the commit body's evidence keys, and an `UNAVAILABLE` is one stated line. A project
whose `spec/SDLC.md` has no such section predates the adapter — say so rather than
guessing an invocation.

## Notes

- Never mark the slice done if the gate is red or the review left unfixed CRITICAL items.
- Do not start the next slice in this session — fresh context per slice is the rule.
- Push the branch (`git push`) so work is not stranded locally, but never open a PR here —
  that is `/end-phase`. The rule behind the prohibition: **slices accumulate on one arc
  branch until `/end-phase`**, in BUILD and STABILIZATION alike, so the whole-arc review
  sees everything the arc changed. Follow-on work arising from this slice's own review
  belongs on this same branch, not on a fresh one.
