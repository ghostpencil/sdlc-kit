# Field report (kit 0.40.1, Phase 30 of the first adopter): 7 findings — the defects that mattered lived outside any single diff

**Source:** [sdlc-kit#20](https://github.com/ghostpencil/sdlc-kit/issues/20), filed
2026-11-19 — the **thirteenth** field report, from the first adopter: their Phase 30,
produced by `/sdlc-retro` one week after the twelfth. Written against **0.40.1**, which
is what the arc ran on. **Generalized here**, as the first adopter's earlier reports are:
the findings, evidence, quoted kit text and numbers are as measured, but the project
name, its paths and module and test names, its commit SHAs, its PR and CI run numbers,
its environment variable and library and product names, and its backlog, decision,
behavior and acceptance identifiers are removed. The issue body itself is un-anonymized;
where the two disagree the issue is right. `#N` below always means a kit issue. The
triage lives in `FEATURE_PLAN.md` §93, together with #18 and #19.

**Read the triage before acting on the priority table.** Finding 6's fix, "accept a
failure summary line (`N failed`)", collides with `reference/GATE_RECIPES.md`'s measured
rule that the report pattern is a marker the runner prints first, never its closing
summary; only one of that finding's three parts is a fix, and not as filed. Finding 5's
mutation half is closed by §70.7 ruling 4 (the inline rules are the operative path, so
zero ledger dispatches is the expected reading); it stands for `verify:` only. Finding 1
must be designed together with #18's "always run it for real" suggestion, which pulls the
other way — this finding is what a real run costs when nobody asked what it writes.
Finding 2 has two legs of different weight: the cheaper one is the Spec axis reading the
decisions a slice cites, and the plan-time clause map is its own section. §93.1 and §93.2
have each one.

---

Field report from a real adoption, produced by `/sdlc-retro` at a phase boundary. Project
details are generalized; the findings, evidence and numbers are as measured. Citations
were read off the project's installed copies of the kit files (kit 0.40.1); upstream paths
are given. Where the issue names the phase spec's decision, behavior, acceptance and
backlog identifiers, each finding here says what they were instead. The labels F1–F7 are
the whole-arc review's own finding numbers.

**Adopter profile.** The first adopter: a Python web application on Claude Code. Agentic
SDLC adopted 2026-07-19 (kit 0.1.0, onto an existing ungated codebase); kit **0.40.1**
since 2026-11-02.

**Window.** Phase 30 — an intake pipeline that triages a shared mailbox, with owner
review. From the Phase 29 merge to the Phase 30 merge (one PR, merged 2026-11-19). That is
57 commits and 17 slices: S0 to S16, with S0b dropped by the owner and S13 docs-only.
Inert in production; the cutover is an activation step after the phase.

**Headline numbers** (measured from the PR's CI run):

| Measure | Before | After |
|---|---|---|
| Tests | 3,834 | 4,166 (4,164 passed + 2 skipped) |
| Coverage | 92.47% | 93.18%, floor raised 92 → 93 |
| mypy | 0 over 92 files | 0 over 111 files |
| ruff | green | green |
| Local chunked suite | 21.6 min | 2.7 min (S0) |

**Defects that escaped every slice review:**
- One found at the `/end-phase` real-data run. It cost slice S16.
- Three found by the whole-arc review: F1 (the cutover is now blocked behind a backlog
  entry), F2 (a ratified decision amended) and F3 (fixed).

**Evidence read:**
- Slice commit bodies.
- `spec/PROJECT_INDEX.md`: the backlog entries opened in the window, and Phase History.
- `spec/SDLC.md`: *Records* and the Kit friction log.
- `.git/sdlc-state.log`, `.git/sdlc-tdd/guard.log` and `.git/sdlc-skill-ledger.jsonl`, all
  read in this clone, the arc's only one.
- An owner interview of two rounds.

---

## 1. A ratified acceptance step had a destructive side effect, and no sweep looks at acceptance steps

**Severity: HIGH.** It caused real damage: a new slice, and a cutover that would have
promoted nothing.

**What happened:**
- An acceptance item prescribed a rehearsal of the pipeline's promotion command with the
  project's data-directory setting pointed at a copy of the archive. The phase spec's
  risk list named "the rehearsal" as the verification for the irreversible cutover.
- The project's intake store lives in a per-user application-data directory, whatever
  that setting says. So the rehearsal's confirmed promotion marked 35 items `promoted` in
  the **real** store.
- `/end-phase` step 2's real-data run read the promotion command's dry run as "0 to
  promote", where the acceptance item had read 35. Had nobody looked, the cutover would
  have promoted nothing.
- Every slice review was clean, because the defect was in the procedure, not in a diff.
- Kit friction line (`spec/SDLC.md`, 2026-11-18, P30 S16): "no slice-level check covers a
  ratified acceptance procedure's side effects, and only running the real CLI at
  `/end-phase` step 2 found it."
- Owner: this is what they fought most this phase, and it should have been caught at
  `/plan-phase`.

**Kit text implicated:** `commands/plan-phase.md`, step 4, *Consequence sweep*. Quoted
from the installed `.claude/commands/plan-phase.md`:

> "scan the behaviors for changes to authentication or authorization, money or financial calculation, destructive or irreversible data operations … Each hit names its extra verification in the spec — in the slice's exit criteria or the acceptance-review checklist"

The sweep scans *behaviors* and asks each hit to name a verification. It never sweeps the
verification itself. Here the named verification (the rehearsal) was the thing with the
irreversible side effect. The canonical statement is a second home:
`templates/SDLC.template.md`, *Phase end* → planning (instantiated `spec/SDLC.md` ~line
1333, "The consequence sweep *(kit 0.8.0)* scans the phase's behaviors…").

**Fix:** extend the consequence sweep to every acceptance-checklist step and every
verification a hit names. For each one, ask what it writes, and where, when run against
real data. In particular, ask whether "point X at a copy" redirects every store the
command touches. Make the same change in both homes.

## 2. Promised behaviors fell between slices: traceability works at item level, not clause level

**Severity: HIGH.** It blocks activation: the backlog entry it produced is HIGH and blocks
the cutover, and a ratified decision had to be amended.

**What happened:**
- **F1:** a ratified decision promises that after the cutover, an *original* message
  written to one named officer is triaged like any other sent mail.
  - S3's slice-time owner ruling defined the set-aside as any message carrying the mail
    provider's sent label whose To/Cc recipients are exactly that officer, "forward or
    original".
  - Nothing reconciled that ruling with the decision, and S11, which cites the decision,
    implemented only the promotion command.
- **F2:** a ratified behavior promised that an owner-only listing command shows which
  items were missed, and that a ruling command records one of two named verdicts on each.
  - S9's row cites two decisions under that behavior, but its exit criteria name only
    "tests for each match kind".
  - Sixteen clean slice reviews could not see either gap, because the Spec axis reviews
    each slice against *its own* exit criteria. The whole-arc review found both.
- Owner: a planning gap, to be fixed by a `/plan-phase` check.

**Kit text implicated:**
- `commands/plan-phase.md`, the spec skeleton note after *Slices* (installed copy, line
  ~196): "Behaviors map onto slices — no behavior left unassigned."
  - The check passes at item granularity: the behavior maps to S9 through its decisions,
    while two of its clauses map nowhere.
- `commands/next-slice.md`, step 2. It re-derives causes, numbers and methods. It does not
  check a ruling made *inside* the slice against the phase's other ratified decisions; the
  S3 ruling was such a ruling.
- `skills/diff-review/SKILL.md`, §2, Axis A. It takes "the current slice's exit criteria"
  as the intent at slice end, which by construction cannot see a clause no slice owns.

**Fix:**
- At `/plan-phase`, map every clause of each Behavior and each Decision, not each item, to
  a named slice exit criterion, or to the acceptance checklist, or mark it explicitly as
  post-phase activation. List any unmapped clause as a finding.
- At `/next-slice`, when the owner rules on an interpretation, grep the spec for other
  decisions that use the same term (here, the two terms the ruling and the decision
  shared) and present any conflict inside the same halt.

## 3. The graph-refresh skip was logged at every slice close, about 15 near-identical lines, with no action possible

**Severity: MEDIUM.** It cost time and buried the real friction.

**What happened:**
- Every Phase 30 slice close wrote a friction line beginning "the slice-end graph refresh
  is skipped again". That was S0–S16, with S4, S12 and S13 folded into neighbours.
- The graph was past the full-rebuild threshold for the whole arc. `refresh-check` read
  from 242 up to 394 files behind the graph's one recorded commit, and the only remedy was
  the owner's `/understand --full`, owed since Phase 19.
- The plugin's SessionStart and post-commit hooks said "you MUST update the graph" each
  time, sometimes after a non-commit command.
- The genuine second items (heredoc writes, a duplicated backlog number, the rehearsal
  side effect) sat behind the repeated lead in every line.
- Owner ruling: **record it once, then stay quiet until the owner rebuilds.**

**Kit text implicated:** `commands/end-slice.md`, step 9 (installed lines ~515–523):

> "A stated skip counts too: a step this file or `/next-slice` prescribes, skipped for the same reason in this slice and the two before it, is friction whatever each slice's own verdict was. Write one line…"

And step 10's refresh, which says "A needed refresh that is not run anyway … is stated
with that count, so a repeated skip reads as growing debt."

The rule was written for a graph that falls behind unnoticed. Once the debt is a recorded
owner action, re-stating it at every close records nothing new. The process rule also
lives in `templates/SDLC.template.md`, *Architecture impact view* / the `Graph refresh:`
line (instantiated `spec/SDLC.md` line 1253).

**Fix:** once a close records `OWNER: /understand --full` past the threshold, later slice
closes state one line ("graph rebuild owed, recorded <date>") and write no friction line.
Re-raise it only at `/end-phase`'s coverage check. Ideally `refresh-check` reports this
state itself.

## 4. Shell writes to test files keep recurring, and the TDD guards did not stop them

**Severity: MEDIUM.** It happens often and the damage is small: each one was caught and
redone through Edit before a test counted.

**What happened:**
- Three times this arc, a test `.py` was written through a shell heredoc or inline Python:
  - S6: one test file.
  - S8: the same file.
  - S10: two tests appended.
- Each time, Claude Code's auto-mode classifier refused the run or the next one. The
  friction lines say "the TDD guards did not" stop it.
- The log records the same route at P11 S3 (2026-10-12), P13 S0 and S1 (2026-10-24), P13
  S2, and P14 S3 (2026-10-25, "fifth recorded recurrence"). That makes this arc's three
  the sixth to eighth.
- Owner: they noticed it as a workaround this phase.

**Kit text implicated:**
- `templates/CLAUDE.template.md`, *Always-active code rules* ("Code changes only through
  the editor tools … the guard reports it at the stop, after the fact (kit 0.36.0)").
- `.github/hooks/sdlc-tdd-guard.py`. Its own comment at line ~306 says a shell write "was
  invisible to it", and at ~317 that "a shell write in that very call is missed".

**Fix:** a PreToolUse check on Bash that refuses, before running, a command which
redirects into, heredoc-writes or `write_text`/`write_bytes`-writes a path matching the
source or test globs. Auto mode currently provides this by accident; an adoption without
auto mode has nothing.

## 5. The skill ledger shows far fewer skill runs than the commit bodies claim

**Severity: LOW.** It is about evidence, not damage.

**What happened:** in the window, the ledger records:

| Skill | Ledger runs | Closes that claim the step |
|---|---|---|
| `diff-review` | 9 | 17 |
| `change-verify` | 3 | 16 slice commits carry a `verify:` line |
| `mutation-testing` | 0 | 16 carry a `mutation:` line |
| `tdd` | 15 | — |

- The ledger is alive, so this is not a dead hook. The verify and mutation steps were
  mostly performed inline: real runs, described in the commit lines, but without the
  skill.
- `/end-slice` allows the inline mutation form ("Use the mutation-testing skill … for
  anything beyond a quick delete-and-run"). Step 6 names `change-verify` without that
  allowance: "Run the `change-verify` skill on a nontrivial slice".
- The commit-body `verify:` line is therefore the only evidence for 13 of 16
  verifications, and it is self-reported.

**Kit text implicated:** `commands/end-slice.md`, step 6 (installed line ~326).

**Fix:** either state that an inline verification carrying the skill's report contract
counts, or have the `verify:` line say `(inline)` versus `(change-verify)`, so the retro's
ledger cross-check can read it.

## 6. The TDD guard's run counting cost repeated re-runs

**Severity: LOW.**

**What happened:**
- A compound mutation-check run was not counted until it was re-run bare (S7, and again at
  this close).
- A seven-failure parametrized run with `--tb=no` was "not counted as a red" (S5).
- A test edit between a manufactured red and its production write made the red stale and
  cost three denied writes (S5).
- This is all recorded in the S5 and S7 friction lines. Each one is correct by the guard's
  rules, but together they read as noise.

**Kit text implicated:** `.github/hooks/sdlc-tdd-guard.py`, the single-bare-command rule.
Its home statement is `templates/SDLC.template.md`, the guard note in *Records*.

**Fix:** accept a failure summary line (`N failed`) as a red's report, so `--tb=no` and
`-q` runs count. And state in `/next-slice` step 4 that a manufactured red's correction is
its own red–green pair.

## 7. Nothing checks backlog numbers for duplicates during an arc

**Severity: LOW.** It was caught by procedure, at the close.

**What happened:**
- Two backlog entries were given the same number, written on adjacent days in different
  regions of the index. A third entry recorded this at the S3 close.
- `/end-phase` step 7's uniqueness assertion renumbered one at the close.
- In between, every reference to that number was ambiguous for 13 slices.

**Kit text implicated:** `commands/end-slice.md`, step 9's read-the-max rule. It is the
only mid-arc guard, and it is prose.

**Fix:** have `/end-slice` step 9 run the same `sort | uniq -d` that `/end-phase` step 7
runs.

## What worked well

All four are owner-confirmed, each with its outcome:

- **Whole-arc review.**
  - It found F1, F2, F3 and F5 after 16 clean slice reviews.
  - F3 and F5 were fixed in the review's fix batch. F1 is open as a backlog entry, a HIGH
    that blocks the cutover. F2 was resolved by an owner amendment of the decision it
    touched.
- **The real-data acceptance pass and the real CLI at `/end-phase` step 2.**
  - They found finding 1, which was fixed in S16.
  - With 4,161 hermetic tests green, the real dry run's "0 to promote" was the only
    signal.
- **Mutation check.**
  - At S16 it killed two surviving mutants (that slice's own first two findings) by adding
    tests, both in the S16 commit.
  - At this close it pinned both review fixes.
- **A project-owned sample gate on the pipeline's redaction step.**
  - The owner's four 50-sample reads drove the surviving-name rate from 18% to 10%, 12%
    and finally 4%. That was accepted with a stated residual risk.
  - The digest-bound gate reopened correctly whenever the redaction step changed.

## Step evidence

| Named step | Evidence in the window |
|---|---|
| Observed RED | **ran**: a `RED:` line on all 16 code-slice commits and on the review batch (3 to 25 lines each). |
| Slice review (`diff-review`) and lenses | **ran and caught**: a `lenses:` line on 16 commits, and 9 slice-review backlog entries. The ledger shows 9 `diff-review` runs (finding 5). |
| Mutation check | **ran and caught**: a `mutation:` line on 16 commits. It caught S16's two survivors. 0 `mutation-testing` ledger lines: inline runs. |
| Verification (`change-verify`) | **ran**: a `verify:` line on 16 commits. 3 ledger runs; the rest inline (finding 5). The review batch has no `verify:` line: it was verified by its tests and the real CLI was not re-run, so **skipped: tests only**. |
| Close-out record check | **ran**: COMPLETE at S16; every code commit carries all four lines. |
| Docs-only path (S13) | **ran**: S13 committed as docs-only. |
| Graph refresh (slice end) | **skipped with a stated reason** at every close: past the full-rebuild threshold (finding 3). |
| `/end-phase` real-data run | **ran and caught**: finding 1. |
| Whole-arc review | **ran and caught**: F1 to F7, F1 open as a backlog entry. |
| Preserved-contract check | **ran**: clean, 99 pins. |
| Phase-end graph coverage | **ran**: `full-rebuild: needed` (180 code files missing); deferred to the owner (an owner decision at the close). |
| Paused writes | **none**: 0 `paused: unguarded` lines; no pause or off in the window except plan-phase → phase and phase-end → off. |

## Suggested priority

| # | Change | File(s) | Effort |
|---|---|---|---|
| 1 | Sweep acceptance steps and named verifications for side effects, including "a copy" redirecting every store | `commands/plan-phase.md` step 4; `templates/SDLC.template.md` consequence sweep | S |
| 2 | Clause-level Behavior/Decision → exit-criterion mapping; a conflict check on in-slice owner rulings | `commands/plan-phase.md` (spec skeleton note); `commands/next-slice.md` step 2 | M |
| 3 | Record a past-threshold graph debt once, then stay quiet until `/end-phase` | `commands/end-slice.md` steps 9–10; `templates/SDLC.template.md` *Architecture impact view* | S |
| 4 | PreToolUse refusal of shell writes to source and test globs | `.github/hooks/sdlc-tdd-guard.py` (or a new hook); `templates/CLAUDE.template.md` | M |
| 5 | Mark verify lines `(inline)` or `(change-verify)`, or bless inline verification | `commands/end-slice.md` step 6 | S |
| 6 | Count a summary-only failing run as a red | `.github/hooks/sdlc-tdd-guard.py` | S |
| 7 | Duplicate-id check at every slice close | `commands/end-slice.md` step 9 | S |

## Cross-cutting theme

**The defects that mattered lived outside any single diff:** in a procedure (the
rehearsal), in a clause no slice owned (one of a ratified decision, one of a ratified
behavior), and in a ruling made mid-arc (the S3 slice-time ruling).

The slice loop reviewed each change well, and the cost landed at the boundaries between
artifacts. If only one change is taken, make `/plan-phase` trace every clause and every
verification step to an owner, and ask of each verification step what it writes and where.
