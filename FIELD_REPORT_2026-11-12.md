# Field report (kit 0.40.1, Phase 27 of the first adopter): 6 findings — rules the agent must remember fail; checks that run do not

**Source:** [sdlc-kit#19](https://github.com/ghostpencil/sdlc-kit/issues/19), filed
2026-11-12 — the **twelfth** field report, from the first adopter: their Phase 27,
produced by `/sdlc-retro`, and their first retro since 2026-09-01. The issue names no kit
version and says its citations were read off the installed files at the time of writing;
the adopter merged **0.40.1** on 2026-11-02, so that is what the arc ran on.
**Generalized here**, as the first adopter's earlier reports are: the findings, evidence,
quoted kit text and numbers are as measured, but the project name, its paths and module
and test names, its commit SHAs, its PR, CI run and deploy identifiers, its library names,
and its backlog, decision and contract identifiers are removed. The issue body itself is
un-anonymized; where the two disagree the issue is right. `#N` below always means a kit
issue. The triage lives in `FEATURE_PLAN.md` §93, together with #18 and #20 — #18 is a
single finding from the same adopter's Phase 18 close (the test double that mirrored the
code) and stays an issue only.

**Read the triage before acting on the priority table.** Finding 1's premise, "no lens
fires", is half false: an always-on doubles question already exists in
`commands/end-slice.md` step 4, and the gap is its wording and that the kit asks for no `lenses:`
verdict on it — so the fix is to move and widen that question, not to add a lens beside it.
Finding 2's shell-write detector **is** installed and armed there; it saw one of seven
writes because it skips any file later touched through the editor, which is the commonest
route, and the prevention the finding asks for is held one arc behind that fix. Finding
3's first fix adds a second prose rule for a rule that already exists. Finding 4's cause
is not a hand search skipped but a sequencing defect nobody filed: the old-value search
runs **before** the write that makes a value old (§93.4). §93.1 and §93.2 have each one.

---

Field report from a real adoption, produced by `/sdlc-retro` at a phase boundary. Project
details are generalized; the findings, evidence and numbers are as measured. Citations
were read off the project's installed copies of the kit files at the time of writing.

**Adopter profile.** The first adopter: a Python web application (stdlib-first, over an
embedded analytical index) on Claude Code. Agentic SDLC adopted 2026-07-19 on an existing
ungated codebase (red type baseline 175, now 0).

**Window.** Phase 27 — a history view in a side panel, a pinned header, and follow-ups to
the phone layout. From the plan's approval (2026-11-10) to the merge (2026-11-12, one PR):
12 slices plus the close, 30 commits. First retro since 2026-09-01 (seventeen phase closes
offered one and it was declined each time).

**Measured**, from CI on the arc's last commit: ruff 0, mypy 0 over 86 files (unchanged
for 23 arcs), **3,430 → 3,574 tests** (3,572 passed + 2 skipped), coverage 92.31% → 92.36%
(floor 92). Deployed and verified the same day. Backlog: 6 closed and retired, 12 opened,
167 open.

---

## 1. No lens fires when a slice builds or changes a test double, and a keyboard trap shipped through one

**Severity: high (a blocking accessibility defect reached the arc review; fixed in the
review's fix batch).**

S1 built the page-test harness's new stubs and recorded, in its commit body,
`lenses: no lens triggered`. S3 then pinned the side panel's Tab trap through those stubs.
The stub's query returned a configured list of buttons and ignored the `[hidden]` ancestor
the real DOM would have excluded, so the test passed while the real panel treated a hidden
confirmation button as its first stop: Shift+Tab escaped the panel, Tab from the last row
went nowhere, and the search box was skipped. S3's `verify:` line records a run in a
headless browser — a real browser, in which each of the four ways of closing the panel was
seen to consume one history entry — but it did not walk Tab with the confirmation hidden.
Eleven slices of green later, the whole-arc review's Standards reviewer found it; the fix
was confirmed in a real browser at 390px.

Implicated text: `commands/REVIEW_LENSES.md`, the preamble: "each lens names its own
trigger. If no trigger matches the slice, close this file". The file's lenses are error
propagation, logging and swallowed errors, verify the denominator, shared state under
concurrency, untrusted input, the disposal-intent test and the unconsumed artifact. None
triggers on "the slice added or changed a test double, stub or harness". The closest text
is inside *the unconsumed artifact* ("the test double drifts from reality through the door
it opened"), which is arc-scoped and about consumers, not fidelity. Second home:
`spec/TESTING.md` (from `templates/TESTING.template.md`) owns the mock policy, which
governs *when* to use a double, not checking that a double keeps the semantics its caller
depends on.

Fix: a lens, *test-double fidelity*. **Trigger:** the slice added or changed a fake, stub,
harness method or fixture that stands in for a real dependency. **Question:** name each
behavior of the real thing that the code under test depends on (selector filtering,
visibility, ordering, side effects), and show one test where the double and the real thing
would disagree, or run that test once against the real thing.

## 2. The edit-tools rule is unenforced, and it was broken four times in one phase

**Severity: medium (the red-green order for three tests rests on observed runs, not the
guard).**

The friction log records shell writes to test files at P27 S3 (`sed -i`), S4 (heredoc), S6
(`sed -i`) and S7 (heredoc and `sed -i`; the last three tests of one test file "were
written by heredoc and only renamed through Edit"), after five earlier recurrences (P18
S4, P15 S3/S4, P24 S9, P26 S6b/S7/S8, P26 `/end-phase`). Each was caught by the agent
itself, sometimes after the write had counted.

Implicated text: `templates/CLAUDE.template.md` (quoted from the instantiated
`CLAUDE.md`), *Always-active code rules*: "Code changes only through the editor tools …
the guard reports it at the stop, after the fact (kit 0.36.0)". Second home:
`spec/SDLC.md` (from `templates/SDLC.template.md`), the guard note **(a4)**: "the guards
see ONLY the editor tools: a source or test file written through the shell is invisible to
them". The installed hook matcher is `"matcher": "Edit|Write"` (`.claude/settings.json`),
so the rule is instruction-only at write time.

Fix: ship a `PreToolUse` hook on the shell tool that denies a command writing a code path
(redirect or heredoc into, `sed -i`, `tee`, `cp`/`mv` onto `*.py` and test paths), with
the formatter and mutation-runner exceptions the rule already names. **Owner ruling
2026-11-12: block them** (recorded as a backlog entry in the project).

## 3. A slice's owner decision waits for the phase close

**Severity: medium (two owner calls reached the owner one and two days late, both at the
merge halt).**

The S7 slice review filed a backlog entry headed "**OWNER DECISION**" — the time a bulk
action's audit row records is not the time stamped on the rows it changed (2026-11-11) —
into the deferred backlog; the owner ruled it at `/end-phase` (2026-11-12), and the fix
then needed its own gate run inside the close. Separately, a ratified decision fixed a
count's display as "100+"; S4 built "N+" (the number of rows listed). No slice record
flagged the difference; it surfaced while the merge halt was being written, as the first
decision put to the owner there. The owner: "Decisions surfacing late"; ruling: **halt at
the slice**.

Implicated text: `commands/end-slice.md` §4: "**Owner question:** anything that is a
design decision, not a defect — HALT and ask", and "a finding that contradicts a
**ratified spec decision** … takes halt 3". Both rules exist; the failure is that a review
finding can be *labelled* an owner decision and still be routed to the backlog bucket, and
that diff-review's Spec axis checks criteria (`skills/diff-review/SKILL.md` §2, "Silent
narrowing") but not a decision's ratified *wording* against the built behavior. Second
home: `spec/SDLC.md` *Owner halt points* (halt 3).

Fix: in `/end-slice` §4, a backlog entry may not carry an owner-decision marker; such a
finding halts. And in the Spec axis, for every ratified decision the slice's row names,
quote the decision's observable wording beside the built behavior.

## 4. A record's second home was missed at three closes, by a check that is still manual

**Severity: low (no wrong enforcement; a stale claim in the canonical file).**

`spec/SDLC.md` *Coverage floor* "Current:" line was not updated at the Phase 21, 24 and 26
closes; each miss was found by the next close's old-value search ("this line was not
updated at that close, found by the Phase 22/25/27 close's old-value search"). The
project's test that holds the floor's homes together parses the contract and the CI
workflow file only.

Implicated text: `commands/end-phase.md` §7 subject 2: "search the whole spec set for the
**old** value and report every file and line that still carries it … an empty list is the
only pass." The rule works when run (it caught this one); it is a hand search, and a hand
search skipped once leaves the error for a whole arc.

Fix: name the mechanized form as the preferred one: where a number has more than one home,
a gate test asserting every home agrees. The project half is a backlog entry there.

## 5. The friction log has no ceiling and no reader

**Severity: low (nothing broke; the record stopped being read).**

`spec/SDLC.md` *Kit friction log* holds **154** entries; **118** end `— open`, one is
`RULING OPEN`. The last retro was 2026-09-01. Each close's offer was declined (Phase 26's
close records "`/sdlc-retro`: declined" as one of its owner decisions). The graph-refresh
line alone recurs at eight P27 closes.

Implicated text: `commands/end-phase.md` §7: "Offer `/sdlc-retro` … An offer, not a step;
declining is the right answer whenever the phase has nothing to teach". The offer carries
no evidence, so "nothing to teach" is never tested against the log.

Fix: the offer states the friction log's open count and oldest open entry's age, and
recommends the retro when either passes a threshold.

## 6. The graph plugin's prompts and the project's refresh rule contradict each other at every slice

**Severity: low (noise; the rule was followed every time).**

The plugin's SessionStart and post-commit hooks said "you MUST update the graph" at every
P27 session and commit (the graph sat at one commit, 175 → 193 structural files behind);
`spec/SDLC.md` `Graph refresh: slice-end incremental on · phase-end full-when-code-missing
on` routes a gap that size to the owner, so each slice logged a friction line instead.
Implicated: `templates/SDLC.template.md`, *Architecture impact view*. Fix: when the
coverage check reads `full-rebuild: needed`, record the owner action once and suppress the
slice-end refresh line until the rebuild. **Owner: will run `/understand --full`.**

## What worked well

- **The whole-arc review** caught the Tab trap (finding 1) and nine more defects, all
  fixed test-first in one fix batch; one deferred (a backlog entry, open). Owner: "Review
  earned it; cut nothing."
- **The composed local run on real data** caught a 3 s skew between a bulk action's audit
  row and the time stamped on the rows it changed (the owner decision of finding 3, since
  fixed) and a clipped card in the side panel (fixed); one more logged to the backlog,
  open.
- **Mutation per slice**: every slice records guards seen to fail; survivors became tests
  at S3 (one guard), S6 (one) and S8 (four).
- **The contract pin sweep in both forms** (a lesson from the Phase 26 close) found no
  orphan this time and repointed one contract entry's two retired pins at bookkeeping.
- **The old-value search** found the stale coverage line (finding 4; corrected at the
  close).
- **Step-evidence lines** were present on all 12 slice commits; the close-out checker
  held.

## Step evidence

| Named step | Window evidence |
|---|---|
| Observed RED (`RED:`) | ran: all 12 slice commits |
| Review lenses (`lenses:`) | ran: 12 of 12; caught at S3 (error routing), S10 (an unconsumed constant); `no lens triggered` at S1, S4, S6, S7, S11 (S1 is finding 1) |
| Mutation check (`mutation:`) | ran and caught: 12 of 12; survivors turned into tests at S3, S6, S8 |
| Verification pass (`verify:`) | ran at 9; **skipped with a reason** at S4, S6, S7 (page pinned under a script runtime; identity not verifiable locally); ledger shows 1 `change-verify` dispatch in the window, the rest inline headless-browser runs |
| `diff-review` (slice and arc) | ran: 8 ledger dispatches; arc review caught 13 findings |
| Unconsumed-artifact lens (arc) | ran: clean |
| Preserved-contract check | ran: clean; 2 retired pins repointed at bookkeeping |
| Composed local run on real data | ran and caught: the audit-time skew, the clipped card |
| TDD guard | ran; blind to the shell writes of finding 2 |
| SDLC state | no pauses, no `off` mid-arc; every transition by a command |
| Graph refresh | skipped at every slice with the rule's reason (finding 6) |

## Suggested priority

| # | Change | File(s) | Effort |
|---|---|---|---|
| 1 | Test-double fidelity lens | `commands/REVIEW_LENSES.md`, `templates/TESTING.template.md` | S |
| 2 | Shell-write deny hook for code paths | `hooks/` (new pre-tool script), settings template, `templates/CLAUDE.template.md`, `templates/SDLC.template.md` (a4) | M |
| 3 | Owner-decision findings halt; ratified wording quoted in the Spec axis | `commands/end-slice.md` §4, `skills/diff-review/SKILL.md` §2, `templates/SDLC.template.md` halt 3 | S |
| 4 | Prefer a gate test for multi-home numbers | `commands/end-phase.md` §7 subject 2 | S |
| 5 | Retro offer carries the friction-log count and age | `commands/end-phase.md` §7 | XS |
| 6 | One owner action instead of a per-slice graph line | `templates/SDLC.template.md` *Architecture impact view*, `commands/end-slice.md` | S |

## Cross-cutting theme

**Rules the agent must remember fail; checks that run do not.** Every finding above is a
rule that already exists in prose (use a faithful double, write only through the editor,
halt on an owner decision, search every home, read the friction log) and was skipped
exactly when nobody executed it. The catches this phase came from things that ran on their
own: the arc review, the composed local run, mutation, the pin sweep. Move each rule that
can be mechanized into something that runs.
