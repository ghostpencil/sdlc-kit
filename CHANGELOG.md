# Changelog

Kit-scoped, semver-ish. Versions describe **the kit**, not any project that adopted it.
This file is repo documentation and is not shipped inside `sdlc-kit/`; the bundle carries
its version in `sdlc-kit/VERSION`.

An entry marked **[installable]** changes a file an adopted project holds
(`commands/**`, `skills/**`, `reference/REVIEW_LENSES.md`) and therefore matters at
update time. Entries marked **[adoption-only]** change `templates/**` or the
non-installed reference docs, which are read at `/sdlc-setup` time and never re-applied
to an already-adopted project.

## Unreleased

### Fixed
- **[installable]** `sdlc-update.md` step 5 now says explicitly that files **new in the
  target version's install set** are copied in — classification never sees them (the
  project does not hold them yet), and the command's first real run (TFit,
  0.2.0 → 0.3.0, which introduced two new installed files) had to infer this from the
  source list rather than being told.

## 0.3.0 — 2026-07-19

Everything the field report asked for that 0.2.0 did not ship — and the kit's own
self-check, whose first run found 15 more defects, all fixed here.

### Fixed
- The *Updating an adopted project* procedure hashed the **working tree**, which reports
  every file as drifted for any Windows adopter whose project does not pin line endings —
  the kit stores LF, their checkout holds CRLF. The check looked like it worked and was
  uniformly wrong. It now hashes committed content (`git cat-file -p :path`), which is LF
  on every platform. Found by running the documented procedure against a real adopted
  project rather than a synthetic one.
- The retroactive path for projects adopted before 0.2.0 is now a complete script, and
  notes that `v0.1.0` predates the restructure (kit files at `commands/`, not
  `sdlc-kit/commands/`).
- Both scripts now avoid a trap that produced confident wrong answers: probing for a path
  with `git cat-file … | sha256sum` reports the *pipeline's* status, so a missing path
  yields the hash of empty input and silently matches the wrong entry. Documented, along
  with a denominator check, since the failure mode is a plausible result rather than an
  error.

The three fixes above changed no file inside `sdlc-kit/`. The entries below do, and reach
adopters at the next release; the bundle manifest is regenerated in the same commits (the
release workflow *verifies* the manifest rather than regenerating it, so a stale one
fails the next tag push).

### Added
- **[adoption-only]** `{{SDLC_SCOPE}}` in `SDLC.template.md`, directly below the title,
  and **[installable]** `/sdlc-setup` now asks in both modes whether the process governs
  the whole repo or a subset, and what is explicitly out of scope. Mixed repos are
  common; the first adoption had to record this decision in three files by hand.
- **[adoption-only]** `SDLC.template.md`, CI section: when local and CI disagree about a
  measurement, CI is authoritative — and the disagreement is itself a finding to explain
  before any threshold moves. The kit previously never contemplated the two disagreeing.
- **[installable]** `end-slice.md` §5 (and the matching bookkeeping rule in
  `SDLC.template.md`): a slice that adds a tool, runtime, or service the gate now
  requires records it and adds it to CI in the same commit — a gate dependency
  discovered by a contributor's red run is a documentation bug.
- **[installable]** `end-phase.md` §3: to exercise failure paths during acceptance
  without risking authoritative data, prefer breaking the connection over corrupting
  the data — stop the server; the failure paths are identical and no real data moves.
- **[adoption-only]** `PROJECT_INDEX.template.md`: a dedicated *Environment gotchas*
  section (previously these facts had no home of their own inside *Notes & gotchas*);
  the Existing-mode adoption-row convention for Phase History
  (`| — | **SDLC adopted** | pre-SDLC | … |`, back-filled rows marked as recorded for
  the arc, not as process history); and backlog provenance tags
  (`"(slice review, <date>)"`) — the practice the field report's own retrospective
  called the most useful part of the run.
- **[adoption-only]** `TESTING.template.md` §*Test Isolation — Enforced, Not Promised*:
  the field report's near-miss (a suite calling the live Google Calendar API for three
  slices, green the whole time) as a headline rule — *partial isolation is worse than
  none, because it reads as complete* — plus three checks the kit specifies without
  shipping code: outbound network blocked, credentials unreachable, every home/data-dir
  seam isolated. A new `{{ISOLATION_HARNESS}}` placeholder records where the harness
  lives and the proof that each check has been made to fail.
- **[installable]** `reference/REVIEW_LENSES.md` — deep-dive review lenses behind a
  conditional pointer in `end-slice.md` §3, read only when the slice's diff matches a
  trigger (error-propagation changes; pattern sweeps or trusted check-scripts), so
  ordinary slices pay no context for them. The error-propagation lens: a new raise is
  done when every caller has been re-read; the mirror question *what did I stop seeing?*;
  a status code is a claim about fault. The verify-the-denominator lens takes its worked
  examples from the 0.2.0 session's three confidently-wrong checks rather than the field
  report's miscount — in each, the check returned a *plausible* answer, so nothing
  prompted a second look — paired with the rule that a check is only trustworthy once it
  has been made to disagree. Unlike the rest of `reference/`, this file is **installed**
  (`→ .claude/commands/REVIEW_LENSES.md`, both setup modes) so the pointer resolves in
  projects that removed the kit folder after setup; it is kit-owned, joins the
  manifest/update path, and the README's classification scripts now try the `reference/`
  prefix alongside `commands/` and `skills/`.
- **[adoption-only]** `TESTING.template.md`: a *Skip discipline* subsection beside the
  mock policy — a test must **fail**, not skip, when a tool it requires is absent; a
  silently-skipped test is the same false green as one that reached the real service —
  and *What a test may assert about errors* in §Test Isolation: asserting "returns empty
  on error" is usually pinning a bug (assert that the error propagates instead), and a
  new invariant is checked against what the system already does, not what sounds right.
- **[installable]** `/sdlc-setup` authors the isolation harness for the detected stack
  (New mode step 4; Existing mode proposes it at the feedback halt) and **proves each
  check by its negative case** — a deliberate violation must fail the suite loudly,
  naming what was attempted, before the check is described as enforced. If the owner
  defers it, the gap goes to the backlog and `{{ISOLATION_HARNESS}}` records what is
  actually enforced today — never enforcement that does not exist. Acceptance was run
  for real in a non-Python stack (Node): the harness authored from the spec alone
  failed loudly on a deliberate `fetch` (naming the address) and a credential-path
  read, then ran 3/3 green with a shell-set token provably not reaching tests.
- **[installable]** `commands/sdlc-update.md` — the update procedure as an installed
  command, closing the field report's #14 outright. It classifies every installed file
  against the manifest of the version the project is **on**, hashes committed content
  (never the working tree), tries all three install prefixes with a denominator check,
  halts exactly once (per-file owner decision on drifted files — never auto-overwritten),
  touches nothing project-owned, and re-stamps `spec/SDLC.md` last so an aborted update
  never claims a version it does not hold. The command and the root README's *Updating an
  adopted project* section deliberately state the same procedure twice — they are
  cross-pointed, a disagreement between them is defined as a kit bug, and keeping them in
  agreement is a `/kit-check` invariant candidate. `SDLC.template.md`'s update pointer
  now names `/sdlc-update` instead of the home-repo README, which an adopted project may
  not hold.
- **[installable]** `/sdlc-setup` Existing mode: the analysis step now globs for
  pre-existing `PROJECT_INDEX.md` / `INDEX.md` / `STATUS.md` anywhere in the tree and
  surfaces hits at the feedback halt with an offered rename of the pre-existing file —
  the kit is about to make `spec/PROJECT_INDEX.md` the single source of truth, and a
  same-named neighbor is how a session reads the wrong file. If the owner keeps both
  names, the disambiguation is recorded in project-owned files (Environment gotchas), not
  in command prose. Scoped to Existing mode, as planned; renaming the kit's own file
  remains deferred until the update path has been exercised at scale.
- **[installable]** `end-phase.md` §5: one sentence on why the whole-arc review exists —
  slice reviews each see one layer, so arc-level bugs live in the seams between slices
  and are invisible to every per-slice review by construction.
- **[adoption-only]** `SDLC.template.md`, gate-baseline section: a count can also hold
  still because the checker stopped looking — suppressions, skipped tests, and constructs
  that hide code from analysis freeze the number while shrinking what it measures.
  **Flagged unsolved:** this is a prose warning, which the field report's own thesis says
  is the weak form of a fix. The real mechanism records *checker reach* (suppression
  count, `Any`-expression share) alongside the error count so a flat count with degrading
  reach becomes visible; designing that is deliberately deferred — it is placeholder- and
  setup-work sized like a batch of its own.
- **Kit self-check** (root-only; nothing an adopter receives): `KIT_INVARIANTS.md`, the
  canonical ledger of 13 invariants — each carrying the real shipped defect that
  motivated it, as the check's negative case — and `/kit-check`
  (root `.claude/commands/kit-check.md`), an agent reading pass over the ledger, not a
  grep suite: the greppable checks (README tree, manifest currency, `{{` census, step
  references) run as commands inside it, but the invariants that have actually shipped
  defects (a false project fact in prose, a semantically-resolved placeholder, a pointer
  that dangles only post-setup) are invisible to pattern matching — the literal
  placeholder name-match was tried and produced 24 false positives out of 32. Both live
  at the root because invariant 12 forbids kit-development-only files in the bundle —
  the batch as first planned put them *in* the bundle, which would have installed a
  kit-development command into every adopting project.

### Fixed — by /kit-check's first real run

The pass was run before shipping it and disagreed immediately: 15 findings, all fixed
in this release. The ones with teeth:

- **[installable]** `end-phase.md` asserted *"branch protection requires the CI check"*
  — a repo-configuration fact that is false for any adopter without branch protection,
  the same defect class as 0.2.0's baseline assertion (nothing in setup configures or
  verifies branch protection). The command now states the rule without asserting the
  enforcement; **[adoption-only]** `SDLC.template.md`'s CI section softened to match.
- **This changelog's own marker definition classified all of `reference/**` as
  adoption-only** — contradicting the install mapping (and its own entries):
  `reference/REVIEW_LENSES.md` is installed and tracks upstream, so a future change to
  it filed per the old definition would have been tagged *[adoption-only]* and never
  routed to adopters by `/sdlc-update`, which reads these markers. Header fixed;
  **[installable]** `sdlc-update.md`'s Notes no longer repeat the stale generalization.
- The README's manual update procedure **had no verification step**: `/sdlc-update` §6
  re-classifies against the target manifest to prove the classifier discriminates, and
  the README — the stated path for pre-command adopters — went straight from copy to
  re-stamp. Added, along with the command's replace-a-kept-`sdlc-kit/`-folder-wholesale
  step, which the README also lacked (a stale kept folder sits beside a re-stamped
  `spec/SDLC.md` claiming a version it does not hold). Both were disagreements between
  the procedure's two statements — found by the invariant recorded when the second
  statement was written.
- **[installable]** `sdlc-setup.md` Existing mode installed the edit-time hook with no
  proof it blocks — the deliberate-lint-error verification existed only in New mode,
  and Existing mode is both the field-tested path and the riskier install (hook
  *merging*). The proof is now required in both modes.
- **[installable]** `skills/python-pro.md` carried a "Reference Guide" table pointing
  at five `references/*.md` companion files that exist nowhere — not in the kit, not
  installed — so a Python session was instructed to load five dangling paths. Table
  removed; the divergence from upstream is recorded in `reference/SKILLS.md`, whose
  provenance note (with `THIRD_PARTY_NOTICES.md`) now also states plainly that
  `python-pro.md` has no identified upstream license, rather than implying blanket MIT.
- **[installable]** `sdlc-setup.md`'s close-out exit check grepped all of `.claude/`,
  which contains the installed copy of `sdlc-setup.md` itself — a file that
  legitimately names placeholders — so the check false-positived on every adoption
  (plan §8.11, left for this batch deliberately). Scoped to exactly the instantiated
  files: `CLAUDE.md spec/ .claude/settings.json`.
- **[adoption-only]** `SDLC.template.md` + **[installable]** `sdlc-setup.md` +
  `reference/GATE_RECIPES.md`: the coverage floor now has a recorded home — a
  `{{COVERAGE_FLOOR}}` line in the gate section (`TBD from first CI run` until one
  exists), resolved by both setup modes, enforcement staying in CI. Previously the
  "record TBD" instruction named no destination.
- Smaller finds, same pass: the canonical template never stated two rules the installed
  commands enforce (push at slice end; the conditional review lenses) — both added
  **[adoption-only]**; `{{STOP_COMMAND}}` had no producing interview question (now
  asked with the run command, both modes, **[installable]**); the formatter was asked
  for and never routed anywhere (now in scaffold step 1); `plan-phase.md` read a
  "product direction" section `PROJECT_INDEX.template.md` does not scaffold (pointer
  trimmed, **[installable]**); the root file tree was missing `.gitattributes` and
  `.gitignore` (invariant 5's first mechanical catch).

## 0.2.0 — 2026-07-19

Version identity, an update path, and the two defects the first field report found in the
shipped kit.

### Fixed
- **[installable]** `commands/end-slice.md` asserted *"The typecheck baseline is green"*
  unconditionally, which is false on any project adopted with a red baseline — a mode the
  kit advertises as supported. Both `end-slice.md` and `end-phase.md` now read the gate
  baseline from `spec/SDLC.md` instead of assuming it. Root cause, now a kit invariant:
  **a command file may not state a fact about the adopting project.**
- **[installable]** `/sdlc-setup` asked for a coverage floor defaulting to **70%**, and
  **[adoption-only]** `reference/GATE_RECIPES.md` justified that number as "Dungeon Daddy
  uses ≥70%" — a constant imported from another project and never measured. Both removed.
  The floor is now set from the first green CI run using CI's exact invocation, and only
  ever raises. *A remembered constant is not a measurement.*

### Added
- `sdlc-kit/VERSION`, `sdlc-kit/MANIFEST.sha256`, `sdlc-kit/LICENSE`, and a bundle-local
  `sdlc-kit/README.md`, so a downloaded artifact is self-describing, verifiable, and
  carries its MIT license text as redistribution requires.
- This changelog.
- Root README: *Updating an adopted project* — the manual update procedure and the
  file-ownership table.
- Release workflow (`.github/workflows/release.yml`): packages `sdlc-kit/` as
  `sdlc-kit-<version>.tar.gz` and `.zip` on tag push and attaches them to the release.
- **[adoption-only]** `{{KIT_VERSION}}`/`{{ADOPTION_DATE}}` in `SDLC.template.md`, so a
  later update knows its baseline without guessing, and `{{GATE_BASELINE}}`, which gives
  the measured gate baseline one definite home for the commands to read. **[installable]**
  `/sdlc-setup` resolves all three — the baseline only after it has actually measured it.

- `.gitattributes` pinning text files to LF. Checksums are only meaningful if the bytes
  are identical on every platform; without this a Windows checkout hashes CRLF and a
  Linux one hashes LF, so the same kit version would report drift on every file.

### Changed
- Repo restructured: `sdlc-kit/` is now the shippable product; the root holds
  documentation *about* the kit. **[installable]** — the only installable file this
  touched is `commands/sdlc-setup.md`, whose close-out step pointed at a kit-local README
  that the restructure removed; it now points at the home repo. No behavior change.

## 0.1.0 — 2026-07-19

Initial extraction of the Agentic SDLC kit from the Dungeon Daddy project: the two-mode
`/sdlc-setup` command, the four daily commands (`plan-phase`, `next-slice`, `end-slice`,
`end-phase`), the vendored MIT TDD skill set, five templates, and the gate/skills
reference docs.

Tagged retroactively at `bdc0ba1`. The commit after the initial one added only
`FIELD_REPORT.md` and touched no installable file, so the installable surface is identical
across both commits — which is what makes the retroactive tag honest.
