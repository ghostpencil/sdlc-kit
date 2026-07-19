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

Tell the owner the phase is gate-green and ready for their acceptance pass. List what to
look at: the phase's user-visible behaviors from the spec's acceptance checklist, plus
any live-data notes from PROJECT_INDEX. The owner exercises the product themselves (run
command in CLAUDE.md) — do not perform this review on the owner's behalf.

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

Run `pr-review-toolkit:review-pr` on the PR. Apply fix batches, re-run the gate, push,
and update the PR body with what changed. If the phase was large or high-risk, suggest
`/code-review ultra <PR#>` to the owner as an optional deeper pass (owner-triggered, paid).

This is not a repeat of the slice reviews: each of those saw one layer, so arc-level bugs
live in the seams between slices and are invisible to every per-slice review by construction.

Owner-facing design questions found by review HALT — they go to the owner, not into the
fix batch.

### 6. Merge approval — HALT

Present: PR link, review outcome (N fixed / N deferred-to-backlog), final gate results,
CI status (`gh pr checks`). Ask for merge approval. On approval:

```
gh pr merge <PR#> --merge
git checkout <main> && git pull
```

### 7. Post-merge bookkeeping (on the main branch)

- `spec/PROJECT_INDEX.md`: add the Phase History row, flip the Phase section to the next
  state (next phase or STABILIZATION), fold deferred review findings into the backlog,
  refresh START HERE.
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
