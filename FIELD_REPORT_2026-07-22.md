# Retro — Arc 3 / PR #7 (Response correctness & durable crash trail)

**Project:** TFit Foundation Q&A app (Python 3.11, stdlib-first HTTP server + DuckDB).
**Adoption:** Agentic SDLC adopted 2026-07-19 on an existing ungated codebase, mode
**STABILIZATION** (bug-fix/cleanup arcs, no feature phases). Kit version **0.6.0**.
**Window:** the third STABILIZATION arc — `d0b8dec..bec0154`, merged as PR #7 (`bec0154`)
on 2026-07-22. Slices S1–S4: #44 (`/ask` double response, the arc's only *live* defect),
#33 (non-dict JSON body), #45 (blank citation page), #38/#50 (durable `action="crash"`
audit trail); #39 cut after an adversarial sweep measured its premise false.

**Headline result, measured against the tree at retro time (not remembered):**

| Metric | Start of arc | End of arc | Note |
|---|---|---|---|
| Tests | 85 | **125** | `pytest --co` sum, verified 2026-07-22 |
| mypy | 171 | **171** | held (ceiling); owner ruling "tests first, types later" stands |
| ruff | green | **green** | |
| CI coverage | 29.02% | **32.78%** | CI-printed |
| CI floor (`gate.yml`) | 28 | **28 → 32** | ⚠️ recorded 32 at close-out but **not applied to `gate.yml`** until this retro — see Finding 1 |

The whole-arc review earned its keep for the **third arc in a row**: it found two
mutation-confirmed test gaps that all four slice reviews missed (S3 and S4 slice reviews
each returned zero findings), fixed in `fa76e5b`. That track record is now 3-for-3 and is
the strongest *worked-well* signal in the window.

This report holds the **kit** findings — evidence the process was wrong, unclear, or
silent. Project-specific lessons were applied to `spec/PROJECT_INDEX.md` and are not
repeated here. Submitting this upstream to the kit repo is the owner's call; nothing has
been copied there.

---

## 1. `/end-phase` records a coverage-floor raise it never applies, and nothing reconciles the two homes of the number

**Severity: medium-high.** Silent, and it defeats the one guarantee the ratchet exists to
give — that coverage cannot regress.

**What happened.** PR #7's close-out recorded the floor raise in **two** places:
`spec/PROJECT_INDEX.md` START HERE (*"CI floor **28 → 32** (CI printed 32.78%)"*) and its
Phase History row (*"CI floor 28 → 32 (CI printed 32.78%)"*). But
`.github/workflows/gate.yml` was **never touched anywhere in the arc** — `git log
d0b8dec..bec0154 -- .github/workflows/gate.yml` is empty — and still read
`--cov-fail-under=28`, last changed at `bb759b9` on 2026-07-19 (the *previous* arc). So for
two days CI enforced **28** while every reader of the index was told **32**. The ratchet was
~4.8 points loose: coverage could have dropped from 32.78% toward 28% and CI would have
stayed green — exactly the regression the ratchet is the sole defense against.

**Why the process let it through.** `commands/end-phase.md` step 7 ("Post-merge
bookkeeping") enumerates: the deploy question, surface-the-backlog, *"`spec/PROJECT_INDEX.md`:
add the Phase History row, flip the Phase section … refresh START HERE,"* trim the spec,
commit docs, suggest memories, offer `/sdlc-retro`. **There is no bullet that says: read
CI's printed coverage for the merged branch, set `--cov-fail-under` in `gate.yml` to just
under it, and confirm the number recorded in the index matches the file.** The floor lives
in two places — a workflow file (what CI *enforces*) and index prose (what the history
*claims*) — and no step reconciles them. The agent wrote the prose the bookkeeping list
asked for and never edited the file the list never mentioned. Owner confirmed at interview:
*"process was silent — kit finding."*

**Implicates:** `commands/end-phase.md` step 7 (bookkeeping list), and
`templates/SDLC.template.md` wherever it describes the coverage ratchet — the ratchet is
documented as a rule ("raise as slices land, never lower it") with no procedure that
actually performs the raise at the boundary where coverage is known.

**Fix.** Add a bookkeeping bullet to step 7: *"Coverage floor — if CI's coverage rose this
arc, set `--cov-fail-under` in the CI workflow to just under CI's printed number, in the
same docs commit; then confirm the floor recorded in `PROJECT_INDEX.md` and the value in
the workflow file are identical. The recorded number is a claim; the workflow value is the
enforcement — a mismatch means the ratchet is not actually ratcheting."* The reconcile step
is the load-bearing half: this project's own history warns three times "never *compute* the
floor," but the failure here was subtler — the floor was read off CI correctly and then
written to the wrong artifact.

**Generalizes?** Yes. Any adopter using the kit's ratchet pattern (a `--cov-fail-under`
in CI + a recorded floor in the index) can record a raise into the prose and never apply it
to the file, with zero signal, because the two are never checked against each other.

---

## 2. `/next-slice` §2 re-derivation has no lighter path for entries whose cause is already `measured`

**Severity: low-medium.** Ceremony that returns nothing on the entries the kit's own
marker already vouches for.

**What happened.** `commands/next-slice.md` §2 requires re-deriving every backlog entry's
stated cause before writing any fix — a step this project's history strongly vindicates
(3-of-3 wrong causes caught at slice start). But the kit *also* introduced a
`measured`/`suspected` marker on each deferred entry (`end-slice.md` §6, "Bookkeeping
rules"), precisely to tell a future reader which causes carry an untested claim. §2 does
**not** use that marker to scale effort: a cause freshly **measured** at last arc's review
gets the same full re-derivation as one marked **suspected** since adoption.

Arc 3's four scoped entries (#44, #33, #45, #38/#50) were each characterized in detail by
PR #4's whole-arc review only days earlier and tagged accordingly, yet each took a full
re-derivation pass. The owner flagged the uniform re-derivation as the arc's felt friction
and, asked what specifically felt heavy, chose *"no lighter path for 'measured' entries."*
The step is correct; its cost is not proportioned to the evidence the kit already records.

**Implicates:** `commands/next-slice.md` §2 (re-derivation), which does not read the
`measured`/`suspected` marker that `end-slice.md` §6 writes.

**Fix.** Make §2 proportional: for an entry marked **`measured`**, a spot-check that its
cited line/behavior still holds (anchors haven't drifted, the branch still exists) is
sufficient; reserve the full re-derivation for **`suspected`** entries and for any
`measured` entry whose cited `:NNNN` anchors have moved. Keep the escape hatch explicit —
if the spot-check surprises you, fall back to full re-derivation and re-tag. This preserves
the 3-of-3 win (all three wrong-cause catches were on entries that would still get full
treatment) while removing the dead weight on well-characterized ones.

**Generalizes?** Yes — any adopter with a `measured`/`suspected`-tagged backlog inherits a
re-derivation step blind to the tag.

---

## 3. `/sdlc-update` step 5's Windows `rm -rf` — carried, still open

**Severity: low, recurring.** Recorded in this window and not yet actioned upstream.

**What happened.** During this arc's opening (the 0.5.0 → 0.6.0 kit update, commit
`bc9db7e`, inside the window), `commands/sdlc-update.md` step 5's bundle replacement
`rm -rf sdlc-kit && cp -r $K sdlc-kit` failed on Windows: `rm: cannot remove 'sdlc-kit':
Device or resource busy` after it had already unlinked all 26 files, leaving the tree empty
but git-tracked. Benign only because the `&&` blocked the `cp` and the bundle is committed —
neither guaranteed by the procedure. Full write-up is `spec/SDLC.md` → Kit friction log
entry #4; it is reproduced here because `/sdlc-retro`'s sweep is supposed to surface
recorded-but-unactioned friction, and this is the window's one such item.

**Implicates:** `commands/sdlc-update.md` step 5 — prescribes replacement without
prescribing *how*, and every worked example in the kit is POSIX-shaped.

**Fix.** Copy-over-in-place: `cp -r $K/. sdlc-kit/` after removing only the *files* the old
manifest lists, never the directory — strictly better on POSIX too (no window where the
bundle is absent). Full rationale in friction log #4.

**Generalizes?** Yes, for any Windows adopter — a platform the kit otherwise supports.

---

## What worked well

- **The whole-arc review is 3-for-3.** S3 and S4 slice reviews each returned zero findings,
  yet the arc review found two mutation-confirmed test gaps in the seams *between* slices
  (`/subtasks/suggest` success-path audit; `do_POST`'s post-response non-`ConnectionError`
  else-arm), both fixed in `fa76e5b`. The kit's insistence on running the arc review "even
  when every slice passed" (SDLC.md Shape) has now paid on all three arcs this project has
  run. Protect this from any future simplification.
- **Mutation-testing by habit continued to pay.** Every new guard in the arc was
  deleted/inverted and watched to fail on exactly its test — S4 alone ran five such checks
  (per-site isolation on the `audit=False` flips). The kit ships `mutation-testing.md` but
  no command invokes it; this project's habit is what caught the gaps. (This reinforces the
  standing open finding from earlier retros that the kit should wire mutation-testing into
  `/end-slice`.)
- **The adversarial planning sweep cut #39.** Round 1 of arc planning chose to make the
  POST error messages generic "for consistency"; the sweep measured that premise false and
  the decision was reversed before any code was written. The gap analysis in `/plan-phase`
  did its job.
- **The re-derivation step, where it fired, still earns its keep** — this is why Finding 2
  proposes proportioning it, not removing it.

## Suggested priority

| # | Change | File(s) | Effort |
|---|---|---|---|
| 1 | Add a coverage-floor bookkeeping bullet that edits the workflow *and* reconciles it against the recorded number | `commands/end-phase.md` step 7; `templates/SDLC.template.md` (ratchet) | S |
| 2 | Make §2 re-derivation proportional to the `measured`/`suspected` marker | `commands/next-slice.md` §2 | S |
| 3 | Copy-over-in-place instead of `rm -rf` in the update | `commands/sdlc-update.md` step 5 | S |

## Cross-cutting theme

**A number (or a rule) recorded in prose is not the same as the number the machine
enforces — and the kit's bookkeeping steps update the prose without a step that touches, or
reconciles against, the enforcing artifact.** Finding 1 is the sharp case: the floor was
read off CI correctly, written into two prose locations, and left un-applied to the one file
CI actually reads. Finding 2 is the mirror: the kit *records* a `measured`/`suspected`
judgement about each backlog cause but the step that consumes those causes ignores the
record. In both, the kit writes a fact down and then acts as if it hadn't. The single
highest-leverage habit for this kit is a **reconcile step** wherever a value lives in two
places — bump both, then assert they agree.
