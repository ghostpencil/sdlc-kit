# End Slice

Close out the current slice: gate → review → fix → commit → record. Runs without asking
except for owner-facing design questions. Process reference: `spec/SDLC.md`.

## How to use

`/end-slice` — after the slice's exit criteria are met, before `/clear`.

## Workflow

### 1. Sanity check

- `git status` + `git diff --stat`. If the working tree is clean and nothing is
  uncommitted, report that there is no slice to close and stop.
- Confirm you are NOT on the main branch. If you are, stop and say so — slices live on
  a phase or cleanup branch.

### 2. Run the gate

Run the gate exactly as defined in `spec/SDLC.md` (lint → typecheck → full test suite).

All steps must be green. If not, fix the failures first (TDD skill rules apply if tests
change), then re-run. Do not proceed on red.

Green means green **against the gate baseline recorded in `spec/SDLC.md`** — zero for a
clean adoption, the recorded counts for a project adopted with a red baseline. Any
increase is a regression and is fixed in this slice. Read the baseline from `spec/SDLC.md`;
never assume it is zero.

### 3. Slice code review

Run the `diff-review` skill on the working diff (uncommitted changes, plus any commits
this slice has already made on the branch — `git diff <main>...HEAD` if the slice spans
commits). It reviews along two axes that fail independently and are reported side by
side, never merged: **Spec** — does this implement the slice's exit criteria, and only
those — and **Standards** — does it follow the conventions recorded in `CLAUDE.md`
*Runtime Conventions*. The skill is installed by `/sdlc-setup` into
`.claude/skills/diff-review/` and is available on both CLIs; it names no CLI-specific
agent or model.

The built-in `/code-review` is the owner-typed, billed escalation — it is not this
step, and this command cannot launch it. On Claude Code a deeper specialist fan-out
(`pr-review-toolkit`) may be available; it is **optional**, and if it ran, say so in
the hand-back (step 7). The same rule binds any substitution: a review whose depth is
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

If the slice changed error propagation or added a catch or failure path, swept the
codebase for a pattern, touched an object that outlives a request or is reachable
from more than one, took in outside data or passed it to an interpreter, or touched
credentials or an externally reachable surface, also apply the matching lens from
`.claude/commands/REVIEW_LENSES.md`; otherwise skip that file.

Triage findings — **verify each one against the source before it enters any pile.** A
finding is a claim about the code; severity is asserted by the reviewer, not measured,
and a false premise survives review at CRITICAL just as easily as at LOW. Findings that
did not survive verification are reported in the hand-back (step 7) alongside the ones
that did, never dropped silently.

- **Fix now:** correctness bugs, silent failures, trust-boundary violations, anything
  CRITICAL/HIGH.
- **Defer:** style/structure improvements, latent issues with no current trigger. Each
  deferred item gets a one-line entry with rationale (step 6), its stated cause marked
  **measured** (you reproduced or observed it) or **suspected** (you inferred it) — the
  reader of that entry needs to know what still needs checking, because a backlog entry
  is a hypothesis with a timestamp, not a finding.
- **Owner question:** anything that is a design decision, not a defect — HALT and ask,
  per the hand-back standard (`spec/SDLC.md`, *Owner halt points*): plain English, the
  decision numbered and marked, options with a recommendation.

If fixes were applied, re-run the gate.

The review step is done when every finding is dispatched — fixed, deferred with its
marker, discarded with its reason, or raised to the owner — and the hand-back names
the discards. A finding still sitting in none of those states is the step not finished,
however far the conversation has moved on.

### 4. Mutation check — a new guard must be seen to fail

For every **new guard, branch, or error path** this slice added (review fixes
included): delete or invert it once, run the suite, and watch it fail on exactly the
test that claims to pin it — then restore and confirm green. Use the mutation-testing
skill (`mutation-testing`, installed by `/sdlc-setup`) for anything beyond a quick
delete-and-run. A check is only trustworthy once it has been made to disagree; a guard
whose deletion leaves the suite green is untested code wearing a test's name, and this
practice caught exactly that on a real project — twice — in guards whose tests could
not have failed. The step is done when every new guard has been seen to fail on
exactly its own test; a guard not yet seen to fail is not yet closed.

### 5. Commit the slice

Use the Bash tool with a heredoc for the message (never shell-specific here-strings):

```
git add <files>   # add the slice's files explicitly; never git add -A blindly
git commit -m "$(cat <<'EOF'
<type>(<area>): <slice summary>

<what and why, briefly>
EOF
)"
```

### 6. Record in PROJECT_INDEX

Update `spec/PROJECT_INDEX.md`:
- Mark the slice done in the current phase's status/START HERE section. **Status only —
  one line.** The close-out records that the slice is done and what is next; the detail
  goes where it will live anyway — the phase spec — and the commit message is already
  the better record. A real adoption wrote 83–163 lines of per-slice detail into the
  index five times and paid an archiving step once per arc to move it back out; the
  phase-close archival bullet stays as the safety net, not the plan.
- Append deferred review findings to the backlog with rationale, provenance
  (e.g. "(slice review, <date>)"), and the cause marker from step 3's triage
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
  PROJECT_INDEX, dated, now. Slice close is the last moment the evidence is still
  accurate; the retro reads this log and cannot reconstruct what was never recorded —
  one adoption's retros produced 23 findings across three arcs while the log gained
  zero entries, because no step ever prompted the writing.
- Note the next slice up, so `/next-slice` in a fresh session can orient without help.

Commit the docs change separately (`docs: PROJECT_INDEX — <slice> done; next up <next>`).

### 7. Hand back

Report per the hand-back standard (`spec/SDLC.md`, *Owner halt points*). Open with a
plain-English executive summary in bullets: what the slice now does, gate green (test
count), and what is next — with any decision the owner still owes **numbered and
explicitly marked** (usually there is none; an open design question is the exception).
Then the detail, after the summary and never mixed into it: review outcome (N fixed /
N deferred / N discarded as unverified, naming those), mutation-check outcome (N
guards checked, each seen to fail), any tool substituted for one this file names, and
commit hashes. End with: **safe to `/clear`**.

## Notes

- Never mark the slice done if the gate is red or the review left unfixed CRITICAL items.
- Do not start the next slice in this session — fresh context per slice is the rule.
- Push the branch (`git push`) so work is not stranded locally, but never open a PR here —
  that is `/end-phase`. The rule behind the prohibition: **slices accumulate on one arc
  branch until `/end-phase`**, in BUILD and STABILIZATION alike, so the whole-arc review
  sees everything the arc changed. Follow-on work arising from this slice's own review
  belongs on this same branch, not on a fresh one.
