# Next Slice

Bootstrap a fresh session onto the next slice of the current phase: orient → confirm scope
(one question) → branch → TDD. Process reference: `spec/SDLC.md`.

## How to use

`/next-slice` — first command in a fresh session. Optional argument to name a specific
slice: `/next-slice S3` or `/next-slice the retry-backoff item`.

## Workflow

### 1. Orient

Read `spec/PROJECT_INDEX.md` (CLAUDE.md is already loaded). From its Phase section and
START HERE, determine:
- Phase mode (BUILD vs STABILIZATION) — phase discipline in CLAUDE.md applies.
- The current phase spec (`spec/PHASE_NN_*.md`); read it if one exists for this phase.
- The next unstarted slice and its exit criteria. If an argument named a slice, use that
  instead — but flag it if PROJECT_INDEX suggests a different order.

Load no other spec files yet (context-minimization rule); pull them in later only when the
slice touches their area.

### 2. Confirm scope — the ONE owner halt

Ask one question (AskUserQuestion on Claude Code; plain chat where the CLI lacks
it): the slice you propose to do, its exit criteria in a
sentence or two, and what it deliberately does NOT include — plain-English bullets per
the hand-back standard (`spec/SDLC.md`, *Owner halt points*), the decision explicitly
marked. Offer the next-best alternative
slice as a second option. Do not proceed until answered; do not ask anything else unless a
genuine design question surfaces later.

**Skip the question when the slice is already owner-decided.** If PROJECT_INDEX records
this slice as OWNER-DECIDED with its scope and constraints spelled out, re-asking "is
this the scope?" is ceremony — state in one line that you are proceeding on the recorded
decision, and go. The halt exists for unscoped or ambiguous slices; keep it for those.

**Re-derive the entry's stated cause before writing any fix — proportionally to its
marker.** A backlog entry is a hypothesis with a timestamp, not a finding — of the first
three entries a real project checked at slice start, all three stated a wrong cause, and
a fix aimed at a fictional trigger can be right anyway, pass every test, and silently
teach the next reader a false fact. The `measured` / `suspected` marker records how much
evidence the entry already carries; read it and scale the work to it:

- **`measured`** — spot-check that the cited evidence still holds: the `:NNNN` anchors
  point where they did, the named behavior still reproduces the obvious way. Minutes,
  not a re-investigation.
- **`suspected`** — full re-derivation: reproduce or disprove the claimed cause before
  any fix. (Every wrong-cause catch on record came from this class.)
- A `measured` entry whose anchors have drifted, or whose spot-check surprises you in
  any way, falls back to full re-derivation — and is re-tagged with what you find.

The reproduction runs where the cause was observed — the entry's provenance names the
stage. An owner-shell or CI-observed cause cannot be disproved from this session's
shell; a failed reproduction from a different environment downgrades the entry to
"could not reproduce here", never to a corrected cause.

Either way, when the cause does not hold where it was claimed to hold, correct the
entry in place and re-scope the slice against what is actually true.

**An entry whose fix deletes a record-shaped artifact adds one check to its
re-derivation:** the deletion rule's contract-and-specs search (`spec/SDLC.md`,
*Product contract*) runs before the slice is scoped — a hit is a spec conflict
(halt 3), not a cleanup, and a real cleanup slice once deleted the only remnant of
a ratified behavior on the strength of a dead-artifact entry alone.

**The same rule covers an `estimated` number this slice implements.** If the slice
builds to a decision in the phase spec whose number is tagged **estimated**, derive it
before starting: run the count, the query, or the measurement the plan could not take
yet. Cheap now, and the plan was ratified against reasoning rather than a figure — on a
real project seven of forty-four decisions changed on contact with code, one of them a
cap whose approved value implied roughly two orders of magnitude more spend than
intended. A derived number that differs from the ratified one goes back to the owner
**inside this halt** — it is a scope question, not a new halt, and it un-skips the
recorded-OWNER-DECIDED shortcut above, because what was decided is no longer what is
true. Never absorb the difference quietly — present it as its own numbered, marked
decision (`Decision 2: the derived value differs — keep the ratified number or adopt
the derived one?`), with both numbers and the derivation. When the derivation confirms
the number, re-tag the decision **measured** in the spec with what you ran.

The re-derivation is done when every marker has had its proportional check and every
`estimated` number the slice implements carries a recorded derivation — any changed
cause corrected in place, any changed number back to the owner.

### 3. Ensure the branch

The rule, mode-independent: **slices accumulate on one arc branch until `/end-phase`;
only `/end-phase` opens a PR.** One arc, one branch, one whole-arc review.

- Check for **any unmerged arc branch** (`git branch --no-merged <main>`), not just
  whether you are on the main branch. If one exists, this slice almost certainly
  belongs on it — check it out and `git pull`. Starting a second branch mid-arc splits
  the arc into two PRs and forfeits the single whole-arc review, which is the stage
  with the best defect track record; do it only if the owner confirms this work is
  genuinely a separate arc or an urgent hotfix (the one sanctioned second branch —
  `spec/SDLC.md` *Shape* defines its path).
- If the main branch has moved since the arc branched (a hotfix landed), merge it into
  the arc branch and re-run the gate (as `spec/SDLC.md` *Records* defines it, against
  the recorded baseline — green in this session's shell, with CI authoritative on any
  disagreement, as ever) before starting the slice — drift is cheapest to
  absorb here, one slice at a time, not at phase end.
- If there is no arc branch yet, create one off the up-to-date main branch:
  `feat/phase-NN-<slug>` (BUILD) or `chore/cleanup-<arc-theme>` (STABILIZATION — name
  it for the **arc's theme**, not for this first slice, because later slices accumulate
  onto it and a branch named for its first slice misdescribes everything after).
- Never implement a slice directly on the main branch.

### 4. Enter the TDD loop

1. Read `spec/TESTING.md` — fresh, every time; do not rely on memory.
2. Invoke the TDD skill.
3. Implement the slice in small red–green–refactor cycles, one behavior at a time.
   **RED is observed, not assumed:** run each behavior's new test and watch it fail
   before writing the code, and record the observation **as it happens** — the exact
   test command, the failing test's line, the exit code — in a running record kept for
   `/end-slice`, which writes it into the slice commit body. An observed red cannot be
   reconstructed at close-out; a red never recorded reads later as a red never run,
   and the close-out states `not observed` rather than omitting the line.

   **A characterization test has no natural red, and "green on first run" is not
   evidence.** A test written against behavior that already exists passes
   immediately — and a test that passes immediately may be pinning nothing at all:
   the wrong object, a value the implementation never produces, an assertion that
   would hold against any implementation whatsoever. Its red is **manufactured, and
   still observed**: assert the wrong value first (or break the behavior under test
   for one run), watch it fail *for the reason you expect*, then set the assertion to
   what the code actually does and watch it pass. Record it in the ordinary shape,
   marked for what it is — `RED: <command> — <test>:<line> — exit 1 (characterization:
   asserted <wrong value> first)`. Without this the step has no shape for such a
   slice and quietly takes the zero-form a docs edit takes: a real arc's 129-test
   characterization slice, thrown around the module that guards a non-regenerable
   database, recorded exactly the evidence a README edit would have.
4. A spec conflict or owner-facing design decision HALTS with a question — never resolve
   one silently. State it per the hand-back standard: plain English, the decision
   numbered and marked, options with a recommendation.

### 5. Finish

When the slice's exit criteria are met, tell the owner the slice is ready for close-out
— an executive summary per the hand-back standard: what the slice now does, in plain
English — **and stop there. Do not run `/end-slice`; the owner runs it** (gate, quality
pass, review, mutation check, verification, commit, record check, PROJECT_INDEX,
then `/clear`).
Close-out commits and pushes without asking, so this hand-back is the owner's one
moment to look at the work before it lands on the arc branch — a summary delivered in
the same turn as the commit it describes is a summary no one could act on.

## Notes

- One slice per session. If the confirmed slice turns out to hide two behaviors, finish
  the first, note the second in PROJECT_INDEX via `/end-slice`, and take it next session.
- If PROJECT_INDEX and the phase spec disagree about what is next, PROJECT_INDEX is newer
  — trust it, and fix the spec as part of the slice's docs commit.
