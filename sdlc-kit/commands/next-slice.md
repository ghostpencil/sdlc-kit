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

Ask one question (AskUserQuestion): the slice you propose to do, its exit criteria in a
sentence or two, and what it deliberately does NOT include. Offer the next-best alternative
slice as a second option. Do not proceed until answered; do not ask anything else unless a
genuine design question surfaces later.

**Skip the question when the slice is already owner-decided.** If PROJECT_INDEX records
this slice as OWNER-DECIDED with its scope and constraints spelled out, re-asking "is
this the scope?" is ceremony — state in one line that you are proceeding on the recorded
decision, and go. The halt exists for unscoped or ambiguous slices; keep it for those.

**Re-derive the entry's stated cause before writing any fix.** A backlog entry is a
hypothesis with a timestamp, not a finding — of the first three entries a real project
checked at slice start, all three stated a wrong cause, and a fix aimed at a fictional
trigger can be right anyway, pass every test, and silently teach the next reader a false
fact. Check the marker (`measured` / `suspected`), reproduce or disprove the claimed
cause — this is usually minutes — and when it does not hold, correct the entry in place
and re-scope the slice against what is actually true.

### 3. Ensure the branch

The rule, mode-independent: **slices accumulate on one arc branch until `/end-phase`;
only `/end-phase` opens a PR.** One arc, one branch, one whole-arc review.

- Check for **any unmerged arc branch** (`git branch --no-merged <main>`), not just
  whether you are on the main branch. If one exists, this slice almost certainly
  belongs on it — check it out and `git pull`. Starting a second branch mid-arc splits
  the arc into two PRs and forfeits the single whole-arc review, which is the stage
  with the best defect track record; do it only if the owner confirms this work is
  genuinely a separate arc.
- If there is no arc branch yet, create one off the up-to-date main branch:
  `feat/phase-NN-<slug>` (BUILD) or `chore/cleanup-<arc-theme>` (STABILIZATION — name
  it for the **arc's theme**, not for this first slice, because later slices accumulate
  onto it and a branch named for its first slice misdescribes everything after).
- Never implement a slice directly on the main branch.

### 4. Enter the TDD loop

1. Read `spec/TESTING.md` — fresh, every time; do not rely on memory.
2. Invoke the TDD skill.
3. Implement the slice in small red–green–refactor cycles, one behavior at a time.
4. A spec conflict or owner-facing design decision HALTS with a question — never resolve
   one silently.

### 5. Finish

When the slice's exit criteria are met, tell the owner the slice is ready for close-out
and run `/end-slice` (gate, review, commit, PROJECT_INDEX, then `/clear`).

## Notes

- One slice per session. If the confirmed slice turns out to hide two behaviors, finish
  the first, note the second in PROJECT_INDEX via `/end-slice`, and take it next session.
- If PROJECT_INDEX and the phase spec disagree about what is next, PROJECT_INDEX is newer
  — trust it, and fix the spec as part of the slice's docs commit.
