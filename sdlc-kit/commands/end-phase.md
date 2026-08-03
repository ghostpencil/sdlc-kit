# End Phase

Close out the phase: gate → owner acceptance review → PR → whole-arc review → merge
approval → bookkeeping. Halts exactly twice: acceptance review and merge approval.
Process reference: `spec/SDLC.md`.

## How to use

`/end-phase` — after the last slice of the phase has been through `/end-slice`.

## Workflow

### 1. Preconditions

- Read `spec/PROJECT_INDEX.md`; confirm every slice of the phase is marked done. If not,
  say which is open and stop — finish it via `/next-slice` + `/end-slice` first.
- On the phase branch, working tree clean, branch pushed.

### 2. Run the gate

Run the gate exactly as defined in `spec/SDLC.md` (lint → typecheck → full test suite).

Green means green **against the gate baseline recorded in `spec/SDLC.md`** — zero for a
clean adoption, the recorded counts for a project adopted with a red baseline. Any
increase is a regression. Read the baseline from `spec/SDLC.md`; never assume it is zero.

Also run whatever phase-level verification the phase spec calls for (smoke test,
end-to-end run, manual script). Fix and re-run until green.

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
command in CLAUDE.md) — do not perform this review on the owner's behalf.

If that command fails in the owner's shell, treat it as a defect in the instructions,
not as the owner's problem: the shell an agent runs commands in and the shell the owner
types into are different environments (different `PATH`, different interpreter, a
profile the agent never loads), and only the owner's is authoritative for anything the
owner executes. Fix the command in `CLAUDE.md` and record the resolved interpreter or
toolchain path in PROJECT_INDEX's Environment gotchas — this step is the only one in the
whole process that exercises that environment, so what it finds has been wrong since
setup.

If the checklist includes failure paths, prefer breaking the connection over corrupting
the data: stopping the server (or the backing service) leaves the product up while its
writes go nowhere — the failure paths exercised are identical, and authoritative data is
never at risk.

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

Spawning the fan-out has a precondition, re-asserted from §1 because this is where it
is load-bearing: **the working tree is clean and every fix so far is committed.** The
reviewers run concurrently with this session in the same tree, and an uncommitted fix
is a fix a reviewer's `git checkout` can silently revert — a real arc lost two that
way, and the fix-batch commit's message claimed both. The corollary generalizes past
the fan-out: **a fix with no test pinning it can silently leave, so a commit message
may not claim one.**

Run `pr-review-toolkit:review-pr` on the PR. **Verify each finding against the source
before it enters a fix batch, and report the findings that did not survive verification
alongside those that did** — a review finding is a claim about the code, and a claim
with a false premise can be CRITICAL-severity and still wrong. On a real arc, two of
five reviewers produced CRITICALs whose stated trigger was factually false; followed
literally, this step would have taken both fixes into a live authorization path. The
reporting half is not optional: a discarded finding is evidence about the reviewer, and
dropping it silently teaches nobody anything.

**The review is done only when every reviewer has returned.** With a fan-out, "done" is
whenever the last reviewer comes back, and nothing else holds the batch: assemble the
fix batch only after the last return, and take it through the gate as one unit. A
finding that arrives after the batch is committed re-opens the review rather than
starting a second batch — on a real arc the batch closed while the slowest reviewer was
still out; that reviewer returned with the arc's worst gap (nine surviving mutations at
100% line coverage), and the interim batch had shipped its own regression. Then apply
the surviving batch, re-run the gate, push, and update the PR body with what changed.
If the phase was large or high-risk, suggest `/code-review ultra <PR#>` to the owner as
an optional deeper pass (owner-triggered, paid).

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
gh pr merge <PR#> --merge
git checkout <main> && git pull
```

### 7. Post-merge bookkeeping (on the main branch)

This step asks the owner several decisions inside one conversation — the deploy
question, the backlog disposition, the red-baseline call, the retro offer. Per the
hand-back standard, present them **together, each numbered and explicitly marked**
(`Decision 1: …`), after a plain-English summary of where the phase landed — never
one at a time buried in the bullet that raised it.

- **Ask the deploy question, then record the verified outcome:** does this phase need
  a deploy for its changes to reach users, and has it happened? Merging is not
  shipping — a production fix sat unshipped behind exactly this missing question once.
  The kit cannot know the project's deploy procedure, but the question is mandatory:
  point at wherever the project recorded the answer (`spec/SDLC.md` is the usual home;
  if nothing is recorded, that is a gap to record now). When the project deploys, do
  not stop at "yes": **verify the deployed artifact is the merged commit against the
  platform's own record** — the deploy run's SHA, the hosting dashboard's
  deployed-commit field, wherever the deploy note in `spec/SDLC.md` says it is exposed
  — an artifact this session did not author. Record the outcome in the Phase History
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
  cleanup slice or the next phase's scope), defer knowingly, or drop. "A big enough
  pile becomes a cleanup slice" defers indefinitely when nothing ever presents the
  pile; this is the presentation point.
- **Coverage floor — bump the enforcement, then reconcile:** if CI's printed coverage
  for the merged branch rose this arc, set the floor in the CI workflow file (the
  `--cov-fail-under` value or its equivalent) to just under CI's printed number, in the
  same docs commit as the bookkeeping below. Then **assert the two homes agree**: the
  floor recorded in `spec/PROJECT_INDEX.md` (and `spec/SDLC.md`) and the value in the
  workflow file must be identical — the bullet is not done until they are. The
  recorded number is a claim; the workflow value
  is the enforcement — a mismatch means the ratchet is not actually ratcheting. Read
  the floor off CI's printed figure, never compute it locally; a real arc recorded a
  raise in the index twice while CI silently kept enforcing the old floor.
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
  in PROJECT_INDEX during the arc, move them into that phase's own spec file — which
  already exists and is already the historical home — leaving the Phase History row and
  a short paragraph behind. The index's bounded sections (Phase, START HERE, the gate
  baseline) are what a fresh session reads first; they stop working as an answer to
  "what do I do next" once closed history sits above them, and one real adoption reached
  2,400 lines with the answer buried under five phases of merged detail. Nothing is
  deleted — the detail is simply not this file's job past the phase close.
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
