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

Run the code-review skill on the working diff (uncommitted changes, plus any commits this
slice has already made on the branch — `git diff <main>...HEAD` if the slice spans
commits).

If the slice changed error propagation (raises, handlers, error status codes) or swept
the codebase for a pattern, also apply the matching lens from
`.claude/commands/REVIEW_LENSES.md`; otherwise skip that file.

Triage findings:
- **Fix now:** correctness bugs, silent failures, trust-boundary violations, anything
  CRITICAL/HIGH.
- **Defer:** style/structure improvements, latent issues with no current trigger. Each
  deferred item gets a one-line entry with rationale (step 5).
- **Owner question:** anything that is a design decision, not a defect — HALT and ask.

If fixes were applied, re-run the gate.

### 4. Commit the slice

Use the Bash tool with a heredoc for the message (never shell-specific here-strings):

```
git add <files>   # add the slice's files explicitly; never git add -A blindly
git commit -m "$(cat <<'EOF'
<type>(<area>): <slice summary>

<what and why, briefly>
EOF
)"
```

### 5. Record in PROJECT_INDEX

Update `spec/PROJECT_INDEX.md`:
- Mark the slice done in the current phase's status/START HERE section.
- Append deferred review findings to the backlog with rationale and provenance
  (e.g. "(slice review, <date>)").
- If this slice added a tool, runtime, or service the gate now requires, record it (gate
  section of `spec/SDLC.md`; Environment gotchas in PROJECT_INDEX) and add it to CI in
  the same commit — a gate dependency discovered by a contributor's red run is a
  documentation bug.
- Note the next slice up, so `/next-slice` in a fresh session can orient without help.

Commit the docs change separately (`docs: PROJECT_INDEX — <slice> done; next up <next>`).

### 6. Hand back

Report in one short block: gate results (test count), review outcome (N fixed / N
deferred), commit hashes, and the next slice. End with: **safe to `/clear`**.

## Notes

- Never mark the slice done if the gate is red or the review left unfixed CRITICAL items.
- Do not start the next slice in this session — fresh context per slice is the rule.
- Push the branch (`git push`) so work is not stranded locally, but never open a PR here —
  that is `/end-phase`.
