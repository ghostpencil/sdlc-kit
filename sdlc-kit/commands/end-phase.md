# End Phase

Close out the phase: gate → owner acceptance review → PR → whole-arc review → merge
approval → bookkeeping. Halts twice by schedule — acceptance review and merge
approval — plus any owner-facing design question the work or the review surfaces,
which halts like everywhere else. Process reference: `spec/SDLC.md`.

## How to use

`/end-phase` — after the last slice of the phase has been through `/end-slice`.

This command is review-heavy; check the model policy recorded in `spec/SDLC.md`
(*Records*; `/model` to switch — on a CLI where routing is operator-performed, the
policy names the moment to set it).

## Workflow

### 1. Preconditions

- Read `spec/PROJECT_INDEX.md`; confirm every slice of the phase is marked done. If not,
  say which is open and stop — finish it via `/next-slice` + `/end-slice` first.
- On the phase branch, working tree clean, branch pushed.

### 2. Run the gate

Run the gate exactly as recorded in `spec/SDLC.md` (*Records*) — the steps recorded
there, in order.

Green means green **against the gate baseline recorded in `spec/SDLC.md`** (*Records*)
— zero for a clean adoption, the recorded counts for a project adopted with a red
baseline. Any increase is a regression. Read the baseline; never assume it is zero.
Green here is green **in this session's shell**; where local and CI disagree about a
measurement, CI is authoritative and the disagreement is itself a finding
(`spec/SDLC.md` states the rule) — step 6's merge halt reads CI's own checks.

Also run whatever phase-level verification the phase spec calls for: the
`change-verify` skill on the arc, plus any smoke test, end-to-end run, or manual script
the spec names. Fix and re-run until green.

**A verification script's license depends on where it lives, and the default is
outside.** A throwaway driver written under a session temp directory is not a
production write at all — where the TDD guards are installed they see only files
inside the repository — so it needs no refactor license and nothing about it is owed
here. Committing one under the
repo makes it production source like any other file, and it takes the ordinary
red-green path: a test first, then the script. Neither case is a special exemption,
and reaching for one is the signal that the script wanted to be outside the repo.

`change-verify` is installed at `.claude/skills/change-verify/` and
is available on both CLIs. It exercises the arc through the path a real caller takes
rather than through the harness, which is the gap the gate cannot cover — a suite
reaches the code through the test process, and the failures that survive a green suite
live in startup, wiring, and configuration. Its discipline is that **a pass not
observed is not a pass**: anything it could not exercise is reported as unverified, not
assumed. Same caveat as its slice-level twin: this runs in the agent's shell and does
not stand in for halt 4, the one step in this loop that runs in the owner's.

This is what step 3 draws on. An arc that reaches the acceptance halt with nothing
observed puts the owner in front of a system no one has run, and the halt passes
vacuously.

### 3. Owner acceptance review — HALT

**First, check what this arc has actually run.** If no slice's exit criteria required
running the application — every slice behavior-neutral by construction, e.g. new code
behind a default-off flag — then the composed system has never run outside the test
suite, and this halt would pass vacuously: a flag-gated arc has no visible behavior by
design, so the process is at its most confident exactly where it has observed least.
In that case, **run the composed system locally against real data before the PR
opens**, and put what it shows in front of the owner with the acceptance pass. On the
arc that bought this rule, the local pass found the arc's worst defect three commits
before the PR — 474 hermetic tests green throughout, the defect in the composition,
invisible to every unit.

Tell the owner the phase is gate-green and ready for their acceptance pass, per the
hand-back standard (`spec/SDLC.md`, *Owner halt points*): a plain-English executive
summary in bullets — what the phase delivers, what to exercise, the exact command to
run — with the checklist as detail below it. List what to
look at: the phase's user-visible behaviors from the spec's acceptance checklist, plus
any live-data notes from PROJECT_INDEX. The owner exercises the product themselves (run
command in CLAUDE.md) — do not perform this review on the owner's behalf. **The run's
log output is part of the acceptance surface**: point the owner at it (or read the
composed run's log yourself, when this step ran one) and check it against the logging
conventions recorded in `CLAUDE.md` — a run that starts, finishes, or fails without
the log saying so is a finding. Absence never appears in a diff, so no review before
this halt can catch a promised log line that was never written.

If that command fails in the owner's shell, treat it as a defect in the instructions,
not as the owner's problem: the shell an agent runs commands in and the shell the owner
types into are different environments (different `PATH`, different interpreter, a
profile the agent never loads), and only the owner's is authoritative for anything the
owner executes. Fix the command in **both its homes** — `CLAUDE.md` (*Commands*) and
`spec/SDLC.md` (halt 4) — and record the resolved interpreter or
toolchain path in PROJECT_INDEX's Environment gotchas — in the slice and phase loop this
step is the only one that exercises that environment, so what it finds has been wrong
since setup (which has its own owner-shell asks, for the same reason).

If the checklist includes failure paths, prefer breaking the connection over corrupting
the data: stopping the server (or the backing service) leaves the product up while its
writes go nowhere — the failure paths exercised are identical, and authoritative data is
never at risk.

**Record a per-item verdict as the owner goes** — in the spec's acceptance checklist
itself, item by item, covering the phase's own items and any *Preserved Behaviors*
entries the spec carries: **met**, **deferred** (becomes a backlog entry, and the
behavior does not enter the product contract), or **dropped** (the ratifying decision
is amended in the spec — an owner ruling, halt-3 shaped, taken here). An unmet item
with no recorded disposition is this halt not finished. The rule exists because a
real phase was accepted with two checklist items unmet and nothing recorded; the
absence surfaced three phases later, by external review, with every intervening
gate green — and by then the only schema remnant of the behavior had been deleted
as dead code.

Findings become fix commits (through the gate again). Large findings mean a new slice —
stop and say so. Proceed only on explicit owner OK.

### 4. Open the PR

```
gh pr create --title "<Phase NN — title>" --body "$(cat <<'EOF'
## Summary
<phase summary against its exit criteria, slice by slice>

## Test plan
<gate results, phase-level verification, owner acceptance review done>
EOF
)"
```

### 5. Whole-arc review

Reviewing at this scope has a precondition, re-asserted from §1 because this is where
it is load-bearing: **the working tree is clean and every fix so far is committed.**
The arc review reads a committed range, so an uncommitted fix is simply invisible to
it; and if a fan-out is spawned, its reviewers also run concurrently with this session
in the same tree, where an uncommitted fix is a fix a reviewer's `git checkout` can
silently revert — a real arc lost two that way, and the fix-batch commit's message
claimed both. The corollary generalizes past
the fan-out: **a fix with no test pinning it can silently leave, so a commit message
may not claim one.**

Run the `diff-review` skill on the arc range (`git diff <main>...HEAD`), checked
against the **phase's** exit criteria rather than any single slice's — at this scope
its Spec axis is asking whether the arc delivered the phase it promised, which no
slice-level review was ever positioned to see. Apply the arc-triggered lens from
`.claude/commands/REVIEW_LENSES.md` — *the unconsumed artifact*: every entity,
column, endpoint, config key, or public API the arc introduced names its production
consumer, or becomes a finding. Report it by name with its verdict
(`unconsumed artifact: <finding, file and line | clean>`), per the lens file's
contract — an
unnamed lens verdict cannot be credited to the lens.

Beside it runs the **preserved-contract check** (its subject is the contract, not
the diff): for every surface the arc touched — the sweep's own population, so the
carried set and the checked set cannot drift apart — read
`spec/PRODUCT_CONTRACT.md`'s
entries on that surface and confirm each still holds — the named pin exists in the
tree and **itself passed** in this arc's gate run (step 2's run; that is the
environment the claim is about — and passed as a test, not merely inside a gate
green against a recorded baseline: on a red-baseline adoption a pin skipped or
failing inside the baseline is a finding, not clean). A **claim-only** entry has
no pin to run and is never reported clean on the strength of a test that does not
exist — report it `claim-only — halt 4 evidence only`; its verification is the
owner's acceptance pass, not the gate. Report
`preserved contract: <finding, file and line | clean |
n/a — no entries on touched surfaces>`. Its negative case: pointed at an entry
whose pinning test was renamed or deleted, it must flag that entry — a run that
cannot fail that way is not this check. A violation that turns out deliberate is
halt 3, not a finding to fix quietly: a ratified behavior is retired by the owner
or not at all. A missing contract file means the project predates it
(`/sdlc-update`'s transition note names the window) — say so in the hand-back
rather than skipping silently.

On Claude Code a deeper specialist fan-out may be available
(`pr-review-toolkit:review-pr` — a per-machine plugin the kit never installs); it is
not required, and the paragraphs below about
concurrent reviewers bind **only if one ran**. Whether a deepening ran is stated in
the hand-back either way.

**Verify each finding against the source
before it enters a fix batch, and report the findings that did not survive verification
alongside those that did** — a review finding is a claim about the code, and a claim
with a false premise can be CRITICAL-severity and still wrong. On a real arc, two of
five reviewers produced CRITICALs whose stated trigger was factually false; followed
literally, this step would have taken both fixes into a live authorization path. The
reporting half is not optional: a discarded finding is evidence about the reviewer, and
dropping it silently teaches nobody anything.

**The review is done only when every reviewer has returned** — trivially true of the
single-reviewer default, and the trap only when a fan-out ran. With a fan-out, "done" is
whenever the last reviewer comes back, and nothing else holds the batch: assemble the
fix batch only after the last return, and take it through the gate as one unit. A
finding that arrives after the batch is committed re-opens the review rather than
starting a second batch — on a real arc the batch closed while the slowest reviewer was
still out; that reviewer returned with the arc's worst gap (nine surviving mutations at
100% line coverage), and the interim batch had shipped its own regression. Then apply
the surviving batch, re-run the gate, push, and update the PR body with what changed.
If the phase was large or high-risk, suggest `/code-review ultra <PR#>` to the owner as
an optional deeper pass (owner-triggered, paid, and Claude Code only — like
`pr-review-toolkit` above, it does not exist on Copilot CLI).

This is not a repeat of the slice reviews: each of those saw one layer, so arc-level bugs
live in the seams between slices and are invisible to every per-slice review by construction.

Owner-facing design questions found by review HALT — they go to the owner, not into the
fix batch, each per the hand-back standard: plain English, numbered and marked, options
with a recommendation.

### 6. Merge approval — HALT

Present per the hand-back standard: a plain-English executive summary in bullets — PR
link, review outcome (N fixed / N deferred-to-backlog), final gate results, CI status
(`gh pr checks`) — then the merge approval as an explicitly marked decision
(`Decision 1: merge?`). On approval:

```
gh pr merge <PR#> --merge   # or --squash / --rebase: use the strategy the repo's
                            # settings allow; if several do, the owner's call at this halt
git checkout <main> && git pull
```

### 7. Post-merge bookkeeping (on the main branch)

This step asks the owner several decisions inside one conversation — the deploy
question, the backlog disposition, the red-baseline call, the retro offer. Per the
hand-back standard, present them **together, each numbered and explicitly marked**
(`Decision 1: …`), after a plain-English summary of where the phase landed — never
one at a time buried in the bullet that raised it. **The reconcile pass below runs
first**, because every one of those decisions reads a recorded number, and a number
read before it is reconciled is a decision taken twice.

- **Reconcile every recorded number and carried claim — before any bullet below asks
  the owner anything.** Re-derive each from the tree and from this close's own gate
  evidence, and report it as `recorded X / measured Y`: divergences first, each named
  with the file that holds it, then the agreements collapsed to one line (`N rows
  reconciled, no divergence`). **No new gate run** — step 2's run is the measurement,
  the merge having come from a clean tree; re-running here measures a different tree
  than the one these records describe. Three subjects, in order:
  1. **The backlog, reconciled before it is counted.** Walk this arc's slice commits
     and the phase spec, and mark `— done (<fix commit>)` on every backlog entry they
     closed. **Only then** report the open count — and say how many entries this pass
     itself just closed. The backlog bullet below asks convert/defer/drop of that
     reconciled number: a count still carrying entries this arc delivered describes
     the future mixed together with the past, and one was measured at 101 with a
     shipped entry sitting inside it.
  2. **Every row of `spec/SDLC.md` *Records*, not only the two rows that have bullets
     of their own.** Check each against this close's gate run and report it
     recorded-vs-measured — the gate baseline and the coverage floor, which keep their
     decision procedures in the bullets below, **and** every other row: the gate
     commands, the CI line, the hook and guard notes, the model policy, and any row
     this adoption authored. Adoption-authored rows are structurally unreconciled from
     birth, nothing having ever been written to reconcile them, which is why this pass
     is defined over the table rather than over a list of row names. A row this close
     produces no evidence about is reported `recorded X / not measured this close` —
     never as agreement.
  3. **Ratified decisions the contract never received.** For every ratified decision in
     prior phase specs that has **neither** a contract entry **nor** a recorded drop,
     ask the question no other check asks: is the behavior in the tree? Present each
     absent one for an explicit owner ruling — restore (a backlog entry or next-phase
     scope) or drop, a drop amending the ratifying decision in its own phase spec
     exactly as halt 4 does. Every decision then reaches a terminal state, so this walk
     shrinks toward zero close by close. It runs at **every** close, not once: the
     backfill below runs once by definition, and step 5's preserved-contract check
     reads entries on touched surfaces, so neither can ever reach a behavior that never
     became an entry. That is the gap three owner-ratified behaviors went missing
     through, with every gate, test, and review green the whole way.
- **Ask the deploy question, then record the verified outcome:** does this phase need
  a deploy for its changes to reach users, and has it happened? Merging is not
  shipping — a production fix sat unshipped behind exactly this missing question once.
  The kit cannot know the project's deploy procedure, but the question is mandatory:
  point at wherever the project recorded the answer (`spec/SDLC.md` is the usual home;
  if nothing is recorded, that is a gap to record now). When the project deploys, do
  not stop at "yes": **verify the deployed artifact is the merged commit against the
  platform's own record** — the deploy run's SHA, the hosting dashboard's
  deployed-commit field, wherever the deploy note in `spec/SDLC.md` says it is exposed
  — an artifact this session did not author. The check's failure is stated, never
  smoothed over: the platform's field showing a different SHA, or no such field being
  found where the deploy note says it is exposed, records as `deploy NOT verified —
  <what was seen>` — a halt-5 fact for the owner, not a silent downgrade to "probably
  fine". Record the outcome in the Phase History
  row's Notes cell: `deployed+verified <date>`, `deploy pending — <where tracked>`, or
  `n/a — no deploy`; a pending deploy also stays in START HERE until verified, so a
  merged-but-unshipped phase can never read as complete. Not a new halt — the owner
  answers it inside the bookkeeping conversation.
- **Then ask what the deploy turns ON:** which controls, limits, or behaviors become
  live that were not live before, and the lever that disables each one *by itself*.
  "Has it deployed" and "what did deploying activate" are different questions, and only
  the second one catches a control the arc believed was dormant — the spec, the PR body,
  and the index all called one dormant on a real arc while the deployment manifest
  committed the variable that made it enforce from the first request. Answer it from the
  production configuration (the same artifact `/plan-phase`'s consequence sweep quotes),
  not from the test environment or the code. Anything newly live goes in the Notes cell
  beside the deploy outcome; anything without an independent off switch goes to the
  backlog as a risk, now that it is real rather than planned.
- **Surface the backlog:** report the open deferred-entry count with a severity
  breakdown, flag the oldest untouched entries, and ask the owner once — convert (a
  cleanup slice or the next phase's scope), defer knowingly, or drop. **Record each
  verdict on the entry's own line as it is taken** — `— done (<fix commit>)` when a
  slice closed it, `— dropped (owner, <date>)` on a drop ruling; a deferral leaves
  the line unmarked. The line's marker is what the retirement bullet below reads;
  a verdict that lives only in this conversation is one no later step can act on.
  **A half-delivered entry is split, never half-marked:** close the delivered part
  with its own `— done (<fix commit>)` so it retires, and open a **new numbered
  entry** for the remainder, its provenance naming the entry it came from. The
  grammar stays three-valued — done, dropped, unmarked — and unmarked now means only
  *untouched*; an entry left unmarked because only part of it shipped counts as open
  in full, retires never, and reports neither what shipped nor what remains.
  "A big enough
  pile becomes a cleanup slice" defers indefinitely when nothing ever presents the
  pile; this is the presentation point. One class is exempt from default deferral: an
  entry that contradicts a **ratified spec decision** is a spec conflict (halt 3),
  and it takes an explicit owner ruling — fix now, or amend the decision it
  contradicts — because a decision the owner ratified does not get un-decided by
  deferral.
- **Product-contract reconcile:** fold halt 4's verdicts into
  `spec/PRODUCT_CONTRACT.md`. Every item recorded **met** enters or updates its
  entry — decision pointer and enforcement named (`pinned: <test>` or `claim-only
  (<date>)`); **deferred** items go to the backlog, not the contract; **dropped**
  items leave it, with the amended decision recorded in the phase spec. Then
  reconcile the direction nothing else checks: every entry on a surface this arc
  touched still names a pin that exists in the tree — the preserved-contract check
  read that at review time; this is the write-side mirror, and the bullet is not
  done until entry and pin agree (an entry naming a test the tree does not hold
  fails this reconcile — that visible failure is the check's negative case).
  Re-present any **claim-only** entries on touched surfaces while here: can one
  now be pinned? An owner question, never a default — a dated claim-only line is
  a debt, and this is its only recurring presentation point.
  **One-time backfill:** if the contract is empty while Phase History shows merged
  phases — an adoption or update predating the file — offer the backfill now: walk
  the prior phase specs' ratified decisions with the owner and enter only what they
  confirm as still-current, never an inference. A decline is recorded in the
  contract file with the date, so the offer is not re-made at every close. The
  backfill's single run takes the **same absent direction** as the reconcile pass
  above: a decision the owner confirms as still-current whose behavior is not
  actually in the tree is put up for a restore/drop ruling — never entered as
  current on the owner's memory, and never quietly left out. A draft that omitted
  three such decisions, caught only because a human happened to read the phase spec
  beside it, is what bought this sentence.
- **Coverage floor — bump the enforcement, then reconcile:** if the coverage measured
  for the merged branch rose this arc, set the threshold — in whichever artifact
  carries it: the CI workflow file, or the build file's check rule where the workflow
  only invokes the check (a Maven adoption's number lives in the build file; the
  workflow never sees it) — to just under the measured number, in the
  same docs commit as the bookkeeping below. Then **assert the two homes agree**: the
  floor recorded in `spec/PROJECT_INDEX.md` (and `spec/SDLC.md`) and that threshold
  value must be identical — the bullet is not done until they are. **If this
  arc established the floor for the first time, prove it fires before recording it:**
  set it above the observed number, run the gate's own commands (and CI's, if they
  differ), watch the failure, then set the real value — two homes agreeing proves
  nothing about whether the enforcing step ever runs in the commands the gate
  executes (`spec/SDLC.md`, *Coverage floor*, states the rule). The
  recorded number is a claim; the threshold value
  is the enforcement — a mismatch means the ratchet is not actually ratcheting. Read
  the measured number off the enforced run's own output: CI's printed figure where
  the check prints one, else the coverage report artifact that same run produced —
  some check tools print only pass/fail, never a percentage, and waiting for a
  printed figure on such a stack leaves this leg inert forever (a real arc's
  `jacoco:check` recorded "no ratchet applied" for exactly that reason). Reading the
  enforced run's artifact is not computing locally; re-running coverage outside the
  enforced invocation to produce a different number is, and stays forbidden — a real
  arc recorded a raise in the index twice while CI silently kept enforcing the old
  floor.
- **Red baseline — lower it or ratify holding it:** for a project adopted with a red
  gate baseline (`spec/SDLC.md`), report this arc's count beside the recorded one. If it
  fell, lower the baseline in `spec/SDLC.md` in this same docs commit — that record *is*
  the enforcement, since the gate compares against it. If it did not fall, ask the owner
  once: lower it anyway (a stabilization slice in the next phase), or ratify holding it
  — and record which, with **how many arcs the number has now been unchanged**. The
  coverage floor ratchets by procedure; without this bullet the baseline ratchets by
  hope, and a real adoption held one typecheck count across four arcs and twelve
  recorded gate runs before anyone noticed the leg was inert. Never let an unchanged
  count be reported as "held" — see the rendering rule in `spec/SDLC.md`.
- `spec/PROJECT_INDEX.md`: add the Phase History row, flip the Phase section to the next
  state (next phase or STABILIZATION), fold deferred review findings into the backlog,
  refresh START HERE.
- **Archive the closed phase's detail.** If the project accumulated per-slice write-ups
  in PROJECT_INDEX during the arc, move them into that phase's own spec file where one
  exists — the historical home. A STABILIZATION cleanup arc has no phase spec; say so
  and leave its detail where the retirement bullet below can reach it. Leave the Phase
  History row and
  a short paragraph behind. The index's bounded sections (Phase, START HERE) are what
  a fresh session reads first; they stop working as an answer to
  "what do I do next" once closed history sits above them, and one real adoption reached
  2,400 lines with the answer buried under five phases of merged detail. Nothing is
  deleted — the detail is simply not this file's job past the phase close.
- **Retire closed items to `spec/PROJECT_INDEX_HISTORY.md`.** The archive bullet above
  moves this phase's detail; this one is the exit path for the two growing record
  sections (`spec/SDLC.md`, *Bookkeeping rules*, states the rule). Move out of the
  index: deferred-backlog entries whose line carries a closing marker — `— done
  (<fix commit>)` or `— dropped (owner, <date>)`, written by the backlog bullet
  above or by the slice that closed them — and Kit-friction lines flipped
  `absorbed` more than one phase ago. (Environment gotchas are a bounded section
  with their own rule — delete when fixed — and never retire; Phase History stays,
  one cheap row per phase.) On first retirement create the file with a one-line
  header — "Retired from
  `spec/PROJECT_INDEX.md` — closed items only." — then, this
  close and every close, append one dated section (`## Retired at Phase NN close —
  <date>`) and move the entries **verbatim** — any numbering, provenance tags, and
  markers intact, so an old reference to an entry still resolves. Then the step's
  own check, in the same pass: re-read the section just written — every entry moved
  must carry its closing marker, and one without is pulled back into the index,
  because an open entry in the history file is work hidden from every session that
  acts on the index; the check fails visibly by producing a pulled-back entry.
  Nothing is deleted, and no session reads the history file at start — its
  spec-loading trigger belongs in `CLAUDE.md`'s table (the `CLAUDE.template.md`
  row: never at session start, only tracing a retired item; `/sdlc-retro`'s
  closed-item sweeps are the other sanctioned read). **Check that table now**: if
  this project's `CLAUDE.md` lacks the row — an adoption updated rather than
  re-instantiated — add it in this docs commit, or every retired item becomes
  unfindable by the rule that was supposed to make retirement safe.
- Trim/align the phase spec if the review changed behavior described there.
- Commit the docs change (`docs: PROJECT_INDEX — Phase NN merged; next up <next>`).
- Suggest any durable lessons worth saving to auto-memory.
- Offer `/sdlc-retro` — it extracts lessons from the phase just closed, while the
  evidence is fresh: project facts into PROJECT_INDEX, process findings into a report.
  An offer, not a step; declining is the right answer whenever the phase has nothing to
  teach, and the command itself refuses to run on too little evidence.

## Notes

- Never merge with a red gate or failing CI — the rule holds whether or not branch
  protection enforces it on this repo.
- Deferred findings go to the PROJECT_INDEX backlog, not silently dropped — a big pile is
  grounds to propose a cleanup slice at the next phase-scope decision.
- If the team's process routes merge approval through a human PR reviewer instead of the
  owner-in-session, treat "reviewer approves on GitHub" as halt 5 and merge only after it.
