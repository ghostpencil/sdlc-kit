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

Run the `pr-review-toolkit:code-reviewer` agent on the working diff (uncommitted
changes, plus any commits this slice has already made on the branch —
`git diff <main>...HEAD` if the slice spans commits). The built-in `/code-review` is
the owner-typed, billed escalation — it is not this step, and this command cannot
launch it. If the named agent is unavailable and something else must stand in, the
substitution is **named in the hand-back** (step 7) — a good substitute review is
exactly the kind nobody thinks to question.

Two lenses the diff-shaped review structurally lacks — apply them explicitly:

- **Consumers of changed behavior.** For every error/return path this slice changed
  (raises, handlers, status codes, return shapes), name each **consumer** of that path
  and state what it did with the *old* behavior. The defects that survive clean slice
  reviews live one layer away, in a consumer written against behavior that just
  changed — nothing in the diff itself looks wrong.
- **Test doubles.** Does any double in this slice omit a side effect or simplify the
  error surface of what it replaces? A double one field simpler than reality makes the
  defect it hides structurally unreachable in tests (`spec/TESTING.md`, mock policy).

If the slice changed error propagation or swept the codebase for a pattern, also apply
the matching lens from `.claude/commands/REVIEW_LENSES.md`; otherwise skip that file.

Triage findings:
- **Fix now:** correctness bugs, silent failures, trust-boundary violations, anything
  CRITICAL/HIGH.
- **Defer:** style/structure improvements, latent issues with no current trigger. Each
  deferred item gets a one-line entry with rationale (step 6), its stated cause marked
  **measured** (you reproduced or observed it) or **suspected** (you inferred it) — the
  reader of that entry needs to know what still needs checking, because a backlog entry
  is a hypothesis with a timestamp, not a finding.
- **Owner question:** anything that is a design decision, not a defect — HALT and ask.

If fixes were applied, re-run the gate.

### 4. Mutation check — a new guard must be seen to fail

For every **new guard, branch, or error path** this slice added (review fixes
included): delete or invert it once, run the suite, and watch it fail on exactly the
test that claims to pin it — then restore and confirm green. Use the mutation-testing
skill (`.claude/commands/mutation-testing.md`) for anything beyond a quick
delete-and-run. A check is only trustworthy once it has been made to disagree; a guard
whose deletion leaves the suite green is untested code wearing a test's name, and this
practice caught exactly that on a real project — twice — in guards whose tests could
not have failed.

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
- Mark the slice done in the current phase's status/START HERE section.
- Append deferred review findings to the backlog with rationale, provenance
  (e.g. "(slice review, <date>)"), and the cause marker from step 3's triage
  (**measured** / **suspected**).
- If this slice added a tool, runtime, or service the gate now requires, record it (gate
  section of `spec/SDLC.md`; Environment gotchas in PROJECT_INDEX) and add it to CI in
  the same commit — a gate dependency discovered by a contributor's red run is a
  documentation bug.
- Note the next slice up, so `/next-slice` in a fresh session can orient without help.

Commit the docs change separately (`docs: PROJECT_INDEX — <slice> done; next up <next>`).

### 7. Hand back

Report in one short block: gate results (test count), review outcome (N fixed / N
deferred), mutation-check outcome (N guards checked, each seen to fail), any tool
substituted for one this file names, commit hashes, and the next slice. End with:
**safe to `/clear`**.

## Notes

- Never mark the slice done if the gate is red or the review left unfixed CRITICAL items.
- Do not start the next slice in this session — fresh context per slice is the rule.
- Push the branch (`git push`) so work is not stranded locally, but never open a PR here —
  that is `/end-phase`. The rule behind the prohibition: **slices accumulate on one arc
  branch until `/end-phase`**, in BUILD and STABILIZATION alike, so the whole-arc review
  sees everything the arc changed. Follow-on work arising from this slice's own review
  belongs on this same branch, not on a fresh one.
