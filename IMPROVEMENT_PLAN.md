# Improvement Plan — acting on the field report

Kit-development artifact (like `FIELD_REPORT.md`), not something an adopting project uses.

**Source:** `FIELD_REPORT.md` — 14 findings from the first external adoption (TFit
Foundation Q&A App, Python, Existing Project mode, 3 slices, 1 PR merged).

**This plan is not a transcription of that report.** The report's diagnoses are strong;
several of its proposed fixes were rejected or reshaped after review. Where this plan and
`FIELD_REPORT.md` disagree, **this plan wins** — §6 records why, so a future session does
not re-litigate settled calls.

Each batch below is sized for one fresh session. Read this file plus the batch you're
working; you should not need to read the whole field report.

---

## 1. Decisions already made

**Versioning.** Semver-ish, kit-scoped. `v0.1.0` = the current shipped state, tagged
retroactively at `bdc0ba1` (verified: the only commit after the initial one added
`FIELD_REPORT.md` and touched no installable file, so the installable surface is identical
across both commits — this is what makes the retroactive tag honest).

**File ownership** — the rule an update tool needs, and the rule that decides every
"where does this go" question below:

| Path | Owner | Update behavior |
|---|---|---|
| `sdlc-kit/commands/`, `sdlc-kit/skills/` | kit | tracks upstream; overwrite when unmodified, owner decides when drifted |
| `sdlc-kit/reference/` | kit | tracks upstream; not installed into projects, consulted at setup |
| `sdlc-kit/templates/` | kit | only matters at adoption; never re-applied to an adopted project |
| instantiated `spec/*.md`, `CLAUDE.md`, `.claude/settings.json` | **project** | **never overwritten** — these hold recorded baselines, owner decisions, gotchas |

**Repo layout (changed after v0.1.0).** `sdlc-kit/` is now the shippable product and the
unit that gets packaged as a release artifact; the root holds docs *about* the kit
(`README.md`, `CLAUDE.md`, `FIELD_REPORT.md`, this plan, `LICENSE`). Kit-relative paths in
this plan — `commands/end-slice.md` and so on — mean `sdlc-kit/commands/end-slice.md`.
Manifest hashes are keyed **relative to the kit root**, so the restructure does not break
continuity with `v0.1.0`.

> **Correction (B0, verified against the tag).** An earlier draft of this section claimed
> the restructure left *every* installable file byte-identical. It did not:
> `commands/sdlc-setup.md` changed, because its close-out step pointed at a kit-local
> `README.md` that the restructure deleted. The change is a doc pointer with no behavioral
> effect, and it does **not** affect §4 — TFit holds the `v0.1.0` content and is compared
> against the `v0.1.0` manifest. The general rule stands and is now load-bearing:
> **a manifest is only ever compared against the version the project claims to be on.**

**Command files may not state facts about the adopting project.** This is the root-cause
rule behind finding #1 and it is now a kit invariant. Commands defer to `spec/SDLC.md`;
anything project-variable lives in a template placeholder, never in command prose.

**The kit ships no application code.** Enforcement mechanisms are specified as *a check
plus its acceptance test*, and `/sdlc-setup` — which is an agent, not a copy script —
authors the implementation for the detected stack and proves it works. This keeps the kit
language-agnostic while still making rules fail loudly. See B3; it is the pattern that
makes finding #3 affordable.

**Context budget.** `end-slice.md` is 75 lines and is read at every slice close. Review
lenses and conditional checklists go in `reference/`, pointed at conditionally — not
inlined. The kit's own Core Rule is *minimize context*; these fixes must not violate it.

---

## 2. Batch order and rationale

```
B0  version identity + manifest        ← DONE (2026-07-19)
B1  the two shipped defects            ← DONE (2026-07-19) → v0.2.0 ready to tag
     └─ MIGRATE TFit to v0.2.0         ← prove the update path on a small, safe diff
B2  cheap general wins
B3  enforceable checks (the reframe)
B4  reference/REVIEW_LENSES.md
B5  remainder
B6  kit self-check invariants
     └─ cut v0.3.0 → migrate TFit again
```

Two ordering constraints that matter:

1. **Tag `v0.1.0` before any batch lands.** The tag must point at the pre-improvement
   state or the retroactive migration in §4 loses its basis. This is step 1 of B0.
2. **Migrate TFit after B1, not after everything.** B1 is a two-line-ish diff to two
   command files. Exercising the update machinery on that is how you find out whether the
   machinery works before betting a large diff on it. The field report's #14 argues the
   update path is the blocker for everything else; proving it early is the cheap version
   of that argument.

---

## 3. The batches

### B0 — version identity and the drift manifest *(unblocks everything)*

Report #14, reduced. The report proposes a full `commands/sdlc-update.md`. The missing
primitive is not a command — it is **version identity**: the kit currently has no
`VERSION`, no changelog, and nothing stamped into installed files, so "diff against
upstream" means diffing against whatever the user happened to clone. Ship the primitive;
the command becomes a convenience.

1. ~~`git tag -a v0.1.0 bdc0ba1`~~ — **done**, tagged and pushed before the restructure.
2. Add `sdlc-kit/VERSION` containing `0.1.0` — **inside** the kit folder, so the version
   ships with the bundle and an adopter can read what they are on.
3. Add `CHANGELOG.md` at the **root** — repo history, not something adopters need.
   `0.1.0` = initial extraction; start an `Unreleased` section covering the restructure.
4. Add `sdlc-kit/MANIFEST.sha256` — SHA-256 of every kit-owned installable file
   (`commands/**`, `skills/**`), keyed relative to the kit root. Ships with the bundle so
   a downloaded artifact can be verified, and so §4's drift check works offline.
   Regenerated as part of every release.
5. Add an `UPDATING.md` section to the root README documenting the manual update
   procedure: get the current kit → compare the adopting project's installed files against
   the manifest **of the version it claims to be on** → files that match are provably
   unmodified and safe to overwrite → files that differ are reported and the owner decides
   per file. Include the ownership table from §1.
6. `sdlc-setup.md`: record the adopted kit version in `spec/SDLC.md` (new
   `{{KIT_VERSION}}` placeholder, read from `sdlc-kit/VERSION`) — so the next update knows
   the baseline without guessing.
7. **Release packaging.** Decide and document how `sdlc-kit/` becomes a downloadable
   artifact at each tag — a `sdlc-kit-<version>.zip`/`.tar.gz` attached to a GitHub
   release, ideally produced by a CI job on tag push so the archive can never drift from
   the tag. Link it from the README quick start (which currently points at the releases
   page and needs a real asset behind it), and publish the manifest checksum alongside.
   **The bundle must contain `LICENSE`** — MIT requires the license text to travel with
   redistributed copies, and `LICENSE` currently lives at the repo root, outside the
   packaged folder. `THIRD_PARTY_NOTICES.md` is already inside and must stay there.
   The bundle should also carry a short README of its own, since `sdlc-setup.md` used to
   point adopters at a kit-local README that no longer exists.
8. Update the README file tree (kit invariant: the tree enumerates every file).

**Acceptance:** from a clean clone of a hypothetical adopting project, the procedure in
`UPDATING.md` correctly classifies at least one unmodified file and one deliberately
modified file. `grep -c '{{' ` on templates still balances against setup's question list.

**Deliberately deferred:** `commands/sdlc-update.md` itself. Write it in B5 or later, once
the manual procedure has been run for real (§4) and its rough edges are known.

---

### B1 — the two shipped defects *(cut `v0.2.0` after this)*

Both are live and wrong in the shipped kit today.

**#1 — `end-slice.md` asserts a false project fact.** `commands/end-slice.md` §2 says
*"Run the gate exactly as defined in `spec/SDLC.md`"* and then, one line later, asserts
*"The typecheck baseline is green — any new error is a regression, never an accepted
cost."* On any project adopted with a red baseline — which the README advertises as
supported — that assertion is false at every slice close.

- Delete the assertion from `end-slice.md` §2. Replace with: *"Green means green **against
  the baseline recorded in `spec/SDLC.md`** — zero for a clean adoption, the recorded count
  for an adopted baseline. Any increase is a regression and is fixed in this slice."*
- Apply the same to `end-phase.md` §2 (it already defers correctly; it just says nothing
  about counts).
- **Do NOT** implement the report's proposed fix of having `sdlc-setup.md` rewrite command
  files to match the measured baseline. That makes `commands/` project-mutated, which
  contradicts the ownership split in §1 and would make every adopted project show permanent
  phantom drift against the manifest. The report's own #14 says commands are kit-owned; its
  #1 fix violates that. The correct reading of its "templates are parameterized, commands
  are not" lesson is the inverse of the one it drew: commands should assert *nothing*
  project-specific.
- Record the "no project facts in command files" invariant (§1) wherever kit contribution
  rules end up living — B6 gives it a home.

**#2 — the kit ships the harmful coverage default.** The field report claims *"there is no
coverage concept anywhere."* **That claim is false** and the truth is more damning:

- `commands/sdlc-setup.md:52` asks for a coverage floor with **default 70%** — the exact
  aspirational number the adopting project set first and had to back out, with the recorded
  lesson *"a 70% floor would fail every build from day one and would be switched off within
  a week."*
- `reference/GATE_RECIPES.md:111` justifies it as *"Dungeon Daddy uses ≥70%"* — a
  remembered constant imported from another project and trusted without measurement, which
  is **precisely the failure mode finding #2 exists to name.** The kit's own reference doc
  is an instance of the bug.

So the fix is a deletion plus a procedure, not a new feature:

- Remove the `70%` default from `sdlc-setup.md` (both modes) and the Dungeon Daddy anchor
  from `GATE_RECIPES.md`.
- Encode, in `GATE_RECIPES.md` and `SDLC.template.md`: **never compute the floor.** Set it
  from the first green CI run, using CI's *exact* invocation (scoping flags moved the
  number 9 points on the reporting project), just below the observed figure. It only ever
  raises. Lowering it to pass a build defeats its only purpose. Existing coverage debt is a
  backlog item, not a merge blocker.
- Keep the report's meta-rule verbatim; it is the best sentence in it: *"A remembered
  constant is not a measurement."*
- Setup must not ask for a floor before a CI run exists — it should record "floor: TBD from
  first CI run" instead.

**Acceptance:** no numeric coverage default survives anywhere in the kit; `grep -rn "70%"`
returns nothing outside `FIELD_REPORT.md` and this plan.

**Then:** bump `VERSION`/`CHANGELOG`/`MANIFEST.sha256`, tag `v0.2.0`, and go do §4.

---

### B2 — cheap, general, uncontested

All small; all survive the "would a Go team on a greenfield service hit this?" test.

- **#4 — environments disagreeing is the finding.** `SDLC.template.md`, CI section. Two
  rules: *when two environments disagree about a measurement, find out why before adjusting
  the threshold* (on the reporting project the disagreement was reporting live API calls in
  tests — the gap was the symptom, not the disease); and *if local and CI diverge, CI is
  authoritative.* The kit currently says "the same checks run in CI" and never contemplates
  them disagreeing, which on any repo with git-ignored local files is a matter of when.
- **#8 — the kit assumes it governs the whole repo.** `sdlc-setup.md`, both modes: ask
  *"does this process govern the whole repo, or a subset? What is explicitly out of scope?"*
  New `{{SDLC_SCOPE}}` placeholder in `SDLC.template.md`, directly below the title. Mixed
  repos (app+docs, app+infra, app+data-pipeline, monorepo packages) are common; the
  reporting project had to record this decision in three files by hand.
- **#9 — new gate dependencies go unrecorded.** `end-slice.md` §5: *"If this slice added a
  tool, runtime, or service the gate now requires, add it to the gate section of `CLAUDE.md`
  and to CI in the same commit. A gate dependency discovered by a contributor's red run is a
  documentation bug."* One line; keep it one line (context budget).
- **#13a — safe acceptance-testing of error paths.** `end-phase.md` §3: to exercise failure
  paths without risking authoritative data, **stop the server** — the page stays live, its
  writes go nowhere, identical failure paths, zero data risk. Generalize as *prefer breaking
  the connection over corrupting the data.*
- **#13b — environment gotchas have no home.** Add an "Environment gotchas" section to
  `PROJECT_INDEX.template.md`.
- **#13c — adoption row convention.** Document the Existing-mode phase-history convention:
  an `| — | **SDLC adopted** | pre-SDLC | … |` row plus back-filled pre-SDLC rows from git
  history, explicitly marked as *recorded so the arc of the project is visible, not because
  they followed this process.*
- **Backlog provenance tags** — *not in the field report's priority table, and it should
  have been.* Its "what worked well" section notes that tagging each deferred backlog item
  with its origin (`"Slice review 2026-07-19"`, `"Whole-arc review, PR #2"`) was an
  unplanned local addition that *"turned out to be the most useful part."* Make it the
  documented convention in `PROJECT_INDEX.template.md`. S effort, positive field evidence.

---

### B3 — enforceable checks, without shipping code *(the reframe)*

Report #3 is the most valuable finding in the report: a test suite was calling the **live
Google Calendar API** the entire time — minting real OAuth tokens locally, passing in CI
only because credentials were absent there, so the same green covered two different code
paths. The `spec/TESTING.md` mock policy said *"never call the real service in a test"* and
nothing enforced it. The near-miss: the same seam covers `insert_event`, one route away
from writing to a real 501(c)(3)'s calendar.

The lesson to encode in `TESTING.template.md`, as a headline rule:

> **Partial isolation is worse than none, because it reads as complete.** A mock policy
> that lives only in prose will be violated, and the violation will not be visible.

The report then proposes that `sdlc-setup.md` scaffold a socket blocker. **Reshape this.**
Shipping blockers means the kit acquires a per-language test-harness matrix (Python, TS,
Go, Rust, Java, C#) to maintain and version — trading away the language-agnosticism that is
its whole value proposition. Instead, apply the §1 pattern:

> The kit specifies **the check and its acceptance test**. `/sdlc-setup` authors the
> implementation for the detected stack and **proves it** — by making a deliberate outbound
> call and confirming the suite fails loudly with the address it tried to reach.

The proof step is not optional. An unverified blocker is another half-built isolation that
reads as complete — the finding recurring one level up.

Checks to specify this way: outbound network blocked; credential env vars cleared and
credential paths pointed at nonexistent files; **every** data-dir/home-dir seam isolated,
not just the obvious one (the reporting project's `conftest.py` sterilized one env var and
nothing else).

**Acceptance:** a New-mode setup run in a non-Python stack produces a working, *verified*
network blocker without the kit containing a line of that language.

---

### B4 — `reference/REVIEW_LENSES.md` *(new file)*

Findings #6, #11, and #12 are all review guidance. Two of them name "code-review guidance"
as the target file — **that file does not exist and cannot**: `code-review` is a Claude
Code built-in the kit does not own. And #11 targets `skills/tdd-references/tests.md`, which
is **vendored MIT content** that `reference/SKILLS.md` certifies as verified word-for-word
against upstream; editing it forks the kit and invalidates that certification.

So: one new kit-owned `reference/REVIEW_LENSES.md`, referenced *conditionally* from
`end-slice.md` §3 (*"if this slice changed error propagation, read …"*) so it costs no
context on slices that don't need it.

- **#6 — error-propagation lens.** Three formulations, all worth encoding: *making a call
  raise is not done when the raise is correct; it is done when every caller's control flow
  has been re-read*; **the mirror question** — when you stop something from raising, ask
  *what did I stop seeing?*, not just *who now crashes?*; and *a status code is a claim
  about fault* (400 was a claim the reporting code couldn't make — it parses data read from
  the database, so corrupt stored data raises on a perfectly valid request).
  Caveat to note in the file: this was 3-for-3 on the reporting project, but during a
  **STABILIZATION** phase — which is by definition when you go fix swallowed errors. Present
  it as a lens, not as a claim about universal defect rates.
- **#12 — verify the denominator.** A silent-except sweep matched `except duckdb.Error:`
  literally and missed 7 sites written `except (duckdb.Error, ValueError, TypeError):`,
  while reporting success — found 26, fixed 26, wrong denominator, no signal. Encode as
  *when auditing a pattern, enumerate by symbol or structure and verify the denominator* —
  **drop the report's "use AST" framing**, which implies tooling the kit doesn't ship and
  can't assume.
- **#11 — testing lessons → `TESTING.template.md`** (kit-owned), not the vendored file.
  (1) *A test asserting "returns empty on error" is usually pinning a bug, not a behavior* —
  prefer asserting the error propagates; a production outage on the reporting project was a
  missing dependency swallowed by `except duckdb.Error: return []`, and a mocked DB would
  have returned rows happily while the suite stayed green through the whole outage.
  (2) *Tests must fail, not skip, when a required tool is absent* — "a silently-skipped test
  is the same false green the slice removed"; conditional-skip is the default idiom in most
  frameworks and the kit says nothing about skip discipline. (3) Fold the narrower
  string-assertion lesson into (1), plus: *check a new invariant against what the system
  already does, not against what sounds right* (a review-written test asserted "no audit row
  on rejection" when the audit layer already mapped failures to `action="fail"` — it would
  have made one event produce two different histories).

---

### B5 — remainder

- **#7 — `PROJECT_INDEX.md` name collision.** `sdlc-setup.md`, Existing mode: glob for
  `PROJECT_INDEX.md` / `INDEX.md` / `STATUS.md` anywhere in the repo; on a hit, halt and
  offer a rename. Same class of check as the existing leftover-`{{` exit check.
  *Note for later:* the deeper fix is that the kit chose a generic name for its most
  load-bearing file, and renaming to `spec/SDLC_INDEX.md` would kill the collision class
  outright — but it breaks every adopted project and every cross-reference. Revisit once
  the update path (B0/§4) is proven; not before.
- **#10 — a baseline count can stop measuring.** The sharpest insight in the report:
  *"a ceiling that stops measuring is worse than a high one."* An unannotated decorator
  applied to 20 handlers typed them all as `Any`; the error count held at 175 because the
  checker had stopped looking. Generalizes past mypy to lint suppressions and skipped tests.
  Add the warning to the baseline section of `SDLC.template.md` — **and flag in the
  `CHANGELOG` that the mechanism is unsolved**, because a prose warning is exactly what the
  report's own thesis says doesn't work. The real fix records *checker reach* (untyped-defs
  or `Any`-expression percentage, suppression count) alongside the error count, so a flat
  count with degrading reach is visible. Design that when B3's pattern is established.
- **#5 — defend the arc review.** `end-phase.md` §5. Keep it to one line explaining the
  *mechanism*: slice reviews each see one layer, so arc-level bugs live in the seams between
  slices and are invisible to all of them. **Cut the anecdote** the report proposes ("on
  this kit's first production run…") — a general kit shouldn't carry another project's war
  story, it will read as stale within a year, and exhortation-by-testimonial is the thing
  the report's own thesis says doesn't work. Downgrade from the report's "high" severity:
  the arc review is step 5 of a linear command, not an option, so there is no skip to
  defend against beyond a human choosing not to run `/end-phase` at all.
- Optionally: `commands/sdlc-update.md`, now that §4 has exercised the manual procedure.

---

### B6 — kit self-check *(my addition; not in the field report)*

The report never proposes a regression check **for the kit itself** — yet finding #1 is a
shipped command contradicting the canonical process file, found by a human noticing two
files disagreed, after three slices of nobody noticing. The kit greps for leftover `{{` at
setup time but has no equivalent consistency check over its own files. This is the report's
own thesis applied one level up, and its absence is the report's biggest blind spot.

Add `reference/KIT_INVARIANTS.md` and a `/kit-check` command (or a documented pass) that
verifies:

1. No command file states a fact about the adopting project (the §1 invariant; this is what
   would have caught #1).
2. Every `{{PLACEHOLDER}}` in `templates/` has a corresponding question in `sdlc-setup.md`.
   **Note from B0 — do not implement this as a literal name match.** It was tried: of the
   32 placeholders in `templates/`, only 8 are named verbatim in `sdlc-setup.md`. The rest
   are asked for semantically (`{{GATE_LINT_CMD}}` comes from "linter", `{{RUN_COMMAND}}`
   from "how the owner will run the app"), so a name-matching check reports 24 false
   positives and is useless. The check has to be a reading pass — which is an argument for
   `/kit-check` being an agent-run command rather than a grep.
3. No command contradicts `SDLC.template.md` — which is canonical by its own first
   paragraph.
4. The README file tree matches the filesystem.
5. `MANIFEST.sha256` is current.
6. Vendored `skills/` files match their upstream verification claims in `reference/SKILLS.md`,
   or the divergence is documented there.

Then cut `v0.3.0` and run §4 again.

---

## 4. Migrating the adopting project (TFit) — retroactive v0

**The situation:** the project adopted the kit on 2026-07-19 with no version stamp, and its
installed files carry no provenance. It is nonetheless *provably* at `v0.1.0`, and here is
why that claim is safe rather than hopeful:

- The kit's installable surface is byte-identical at `5f2aae4` and `bdc0ba1` (verified —
  the second commit added only `FIELD_REPORT.md`). So "which commit did it adopt from" has
  no effect on what was installed.
- `FIELD_REPORT.md` §14 records that all three installed command files were byte-identical
  to the kit's at the time of the report.
- `MANIFEST.sha256` (B0) turns both of those from recollection into a check.

**Procedure** — run in the adopting repo, after B1 ships and `v0.2.0` is tagged:

1. Clone the kit at `v0.1.0` to a scratch path. Compute SHA-256 of the project's
   `.claude/commands/*.md` and compare against `v0.1.0`'s `MANIFEST.sha256`.
2. Classify every file:
   - **matches** → provably unmodified since adoption → safe to overwrite with `v0.2.0`.
   - **differs** → the owner edited it (which `spec/SDLC.md` explicitly invites: *"if this
     file and a command disagree, this file wins — fix the command"*), or setup modified it.
     Report the diff; the owner decides per file. **Never auto-overwrite.**
3. Copy the `v0.2.0` versions of the matching kit-owned files (`commands/`, `skills/`) into
   `.claude/commands/`.
4. **Touch nothing project-owned.** `spec/SDLC.md`, `spec/PROJECT_INDEX.md`,
   `spec/TESTING.md`, root `CLAUDE.md`, and `.claude/settings.json` stay exactly as they
   are. They hold the 171-error baseline, ~30 backlog items with provenance, the
   `PROJECT_INDEX` collision warnings, and the "governs the Python app only" scope decision
   — all of which are that project's, not the kit's.
5. Record the new kit version in `spec/SDLC.md` (`kit version: 0.2.0`, dated). From here on
   the project has a version stamp and every later update is mechanical.
6. Verify the fix actually landed: `.claude/commands/end-slice.md` no longer asserts "the
   typecheck baseline is green," and `spec/SDLC.md`'s recorded 171-error ceiling is now the
   single place the baseline is defined. That contradiction is the one that ran unnoticed
   for three slices.
7. Land it as a normal PR on that project (`chore/update-sdlc-kit-0.2.0`), consistent with
   how the kit was adopted there in the first place.

**Why migrate at v0.2.0 rather than waiting for everything:** the diff is two command files
and a handful of lines. If the procedure has a flaw, this is the cheapest possible way to
find it. Repeat the same procedure at `v0.3.0` after B6, when the diff is large — by which
point the machinery has been exercised once for real.

**Watch for:** B2's `{{SDLC_SCOPE}}` and B5's `PROJECT_INDEX` collision check are both
setup-time features, and that project already solved both by hand. Updating must not
undo the hand-written scope note or the three collision warnings. This is exactly why the
ownership split in §1 forbids touching `spec/*` — but it's worth confirming by eye on the
first run, since it's the failure mode that would do real damage.

---

## 5. Cross-cutting cautions for whoever executes this

- **Evidence is n=1, and a specific 1.** Python, Existing-mode, STABILIZATION, mixed
  app/content repo, Windows/NTFS, one owner, three slices. No New-Project run, no BUILD
  phase, no compiled language, no team — i.e. roughly half the kit's advertised surface is
  still untested. The *lessons* generalize well; the *fixes* are where the overfitting hides.
  Ask of each: would a Go team on a greenfield service hit this?
- **Prose bloat is the likeliest way these fixes make the kit worse.** The report proposes
  adding four separate things to `end-slice.md`, a 75-line file read at every slice close,
  in a kit whose Core Rule is *minimize context*. B4 exists specifically to prevent that.
- **Don't confuse "the kit is under-built as a product" with "the kit should ship more
  code."** The gap is version identity and self-consistency (B0, B6), not per-language
  harnesses. A prompt kit that starts shipping test scaffolding in six languages has traded
  its main advantage for someone else's maintenance problem.

---

## 6. Rejected or reshaped — do not re-litigate

| From the report | Disposition |
|---|---|
| #1: setup rewrites command files to match the measured baseline | **Rejected.** Makes `commands/` project-mutated; contradicts the ownership split and the report's own #14. Fix is to delete the assertion so commands state no project facts at all. |
| #2: "there is no coverage concept anywhere" | **Factually wrong.** `sdlc-setup.md:52` and `GATE_RECIPES.md:109-111` both cover it — and ship a 70% default sourced from another project by memory. Reframed as deleting a harmful default, not adding a feature. |
| #3: setup scaffolds a socket blocker | **Reshaped.** Kit specifies check + acceptance test; setup authors it per stack. Shipping blockers costs a per-language matrix. |
| #5: add the "two data-integrity bugs" anecdote to `end-phase.md` | **Trimmed** to the mechanism. Severity downgraded — there is no skip to defend against. |
| #6, #12: target "code-review guidance" | **Retargeted.** No such kit-owned file exists; `code-review` is a built-in. → new `reference/REVIEW_LENSES.md`. |
| #11: edit `skills/tdd-references/tests.md` | **Rejected.** Vendored MIT content certified against upstream in `reference/SKILLS.md`. → `TESTING.template.md` instead. |
| #12: "audit by AST" | **Reframed** to "verify the denominator." AST tooling isn't universally available and the kit can't assume it. |
| #14: `commands/sdlc-update.md` first | **Reduced.** Version identity is the missing primitive; the command is a convenience. Manual procedure first (§4), command later. |
| #7: rename `spec/PROJECT_INDEX.md` | **Deferred,** not rejected. Kills the collision class but breaks every adopted project — unshippable until the update path is proven. |
| #10: prose warning is the fix | **Accepted as interim,** flagged as unsolved. Real fix records checker reach, not just error count. |
| *(not in the report)* backlog provenance tags | **Promoted** into B2. Its own "what worked well" section calls this the most useful part of the run, and it never reached the priority table. |
| *(not in the report)* kit self-check | **Added** as B6. Finding #1 shipped because nothing checks the kit against itself. |
