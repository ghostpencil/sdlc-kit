# Changelog

Kit-scoped, semver-ish. Versions describe **the kit**, not any project that adopted it.
This file is repo documentation and is not shipped inside `sdlc-kit/`; the bundle carries
its version in `sdlc-kit/VERSION`.

An entry marked **[installable]** changes a file an adopted project holds
(`commands/**`, `skills/**`, `reference/REVIEW_LENSES.md`) and therefore matters at
update time. Entries marked **[adoption-only]** change `templates/**` or the
non-installed reference docs, which are read at `/sdlc-setup` time and never re-applied
to an already-adopted project.

## 0.5.0 — 2026-07-20

The retro-fix batch: all 15 priority rows of `FIELD_REPORT_2026-07-20.md` — the first
real run of `/sdlc-retro`, on the same adoption that produced the first field report.
Cut ahead of the planned agents batch because the report's top rows are a live defect
class in the update path itself. The report's cross-cutting theme — checks whose
denominator was assumed rather than enumerated — is the thread through nearly every
entry below.

### Fixed
- **[installable]** `sdlc-update.md` step 5 no longer replaces a kept `sdlc-kit/`
  folder blind: it enumerates the folder's **actual contents** against the manifest
  first, reports anything un-manifested, and HALTs — a project put that file there, and
  one real update silently deleted a project's only local copy of two commits of
  authored work while reporting "nothing project-owned touched". Step 6 now permits
  that reassurance only when the final diff was actually read (report finding 1).
- **[installable]** `sdlc-update.md` step 4 reports **content-changed counts separately
  from touched counts**, so "5 changed, 19 touched" replaces the flat "24 modified"
  whose known-meaningless noise is exactly where the deletion above went unread
  (finding 12, the mechanism of finding 1).
- The root README's update section mirrors both changes plus the arc-boundary rule —
  the command and the section state the same procedure by definition.
- **[installable]** `end-slice.md` §3 named a review tool that does not exist ("the
  code-review skill"); a real run substituted silently and well, which is why nobody
  looked. The per-slice reviewer is now `pr-review-toolkit:code-reviewer`, the built-in
  `/code-review` is identified as the owner-typed escalation, and any substituted tool
  must be named in the hand-back (finding 6; `reference/SKILLS.md` and setup's step 1.2
  check follow).

### Added
- **[installable]** `end-slice.md` gains a **mutation-check step**: every new guard,
  branch, or error path is deleted or inverted once and the suite watched to fail on
  exactly the intended test. The kit shipped `mutation-testing.md` and no workflow step
  ever invoked it; used by habit on a real project, it caught a test that could not
  have failed and proved a production defect's root cause — the single
  highest-yield check in the kit, previously reachable only by memory (finding 4).
  `mutation-testing.md` accordingly flips from offered to always-installed
  (`sdlc-setup.md` step 5, `reference/SKILLS.md`) — updaters who declined it at
  adoption receive it as a new-in-install-set file.
- **[installable]** `end-slice.md` §3 gains the two lenses slice review structurally
  lacked, both paid for in production: name each **consumer** of a changed error/return
  path and what it did with the old behavior (finding 2 — two arcs, two defects that
  survived every slice review, one live in production); and ask whether any **test
  double** omits a side effect or simplifies the error surface of what it replaces
  (finding 5 — a recorder that dropped one flag assignment hid a live bug through four
  reviews).
- **[installable]** `next-slice.md` §2: **re-derive a backlog entry's stated cause
  before writing any fix** — 3 of 3 entries checked on a real project stated a wrong
  cause, and a fix aimed at a fictional trigger can be right anyway, pass every test,
  and teach the next reader a false fact (finding 3). Deferred entries now mark their
  cause **measured** or **suspected** at the writing end (`end-slice.md` §3,
  `templates/PROJECT_INDEX.template.md`).
- **[installable]** `next-slice.md` §3 states the branch rule mode-independently —
  slices accumulate on one arc branch until `/end-phase`; only `/end-phase` opens a
  PR — and checks for **any unmerged arc branch**, not just "am I on main".
  STABILIZATION branches are named for the arc's theme, not their first slice
  (finding 7; `end-slice.md` notes state the accumulation rule its PR prohibition
  always assumed).
- **[installable]** `end-phase.md` post-merge bookkeeping asks the **deploy question**
  (merging is not shipping — a production fix once sat unshipped behind exactly this
  missing step) and **surfaces the backlog** with severity counts for one owner
  decision: convert, defer, or drop (findings 9, 10). Neither is a new halt; the
  five-halt-point invariant stands.
- **[installable]** `sdlc-update.md` states *when* to update: at a phase/arc boundary,
  never with an arc in flight — three updates once landed in the three hours before an
  arc's first slice, and which kit version governed which slice is now
  unreconstructable (finding 8).
- **[installable]** `sdlc-setup.md`: warns that a kept `sdlc-kit/` folder is kit-owned
  and **volatile** (project notes go to a project-owned path); checks `.gitattributes`
  defines an `eol` for `*.md` and offers `*.md text eol=lf` in both modes (findings 1,
  12 — the one-line fix for the phantom-modified noise).
- **[installable]** `sdlc-retro.md` step 1 gains the co-development clause — when the
  kit's own repo is at hand, orientation reads the kit-side planning docs too — and
  step 2 sweeps for **recorded-but-unactioned friction** on both sides. The first real
  retro missed a friction item the kit's plan had already recorded and labeled as retro
  material; the command could only mine what the project wrote down (finding 12's
  method note).
- **[adoption-only]** `templates/SDLC.template.md` carries the canonical statement of
  every process change above: the one-arc-one-branch-one-PR rule in *Shape*, halt 2
  narrowed to skip owner-decided slices (finding 11 — the owner's instinct was to
  delete it; the retro narrowed it instead), the re-derive rule, the renamed reviewer
  and its two lenses, the mutation-check step, and the deploy question + backlog
  presentation at phase end. New placeholder `{{DEPLOY_NOTE}}`, resolved by a new
  deploy-procedure question in both setup interviews — the placeholder contract holds.
- **[adoption-only]** `templates/TESTING.template.md` mock policy: a double that stands
  in for production code must reproduce its **side effects and error surface**, or the
  test drives the real thing (finding 5).
- **[adoption-only]** `templates/CLAUDE.template.md` command summaries follow
  (mutation check; deploy question).

## 0.4.0 — 2026-07-19

The improvement loop gets its input side: `/sdlc-retro` turns a finished phase into
evidence, so the next plan rests on what a run actually taught rather than on what
someone remembered to write down. Cut ahead of the feature plan's schedule (which put
0.4.0 after the agents batch) so the command can be exercised on a real adoption —
the same reason the last two releases were cut, and the same reason they found defects.

### Added
- **[installable]** `commands/sdlc-retro.md` — `/sdlc-retro`, lessons-learned extraction
  at a phase boundary. The improvement loop had a proven output side (field report →
  plan → batches → release → migrate) and a manual input side: `FIELD_REPORT.md` was
  written by hand, so the kit's evidence supply depended on someone volunteering a
  retrospective. The command mines what the process already forces onto disk —
  deferred-backlog provenance tags, the gate-baseline trajectory in `spec/SDLC.md`,
  Phase History, `git log` friction signals — then interviews the owner and sorts every
  lesson into exactly two piles: project facts into the project's own files, process
  findings into `spec/SDLC_RETRO_<date>.md` in the shape of `FIELD_REPORT.md`. It never
  submits anything; whether a finding reaches the kit is the owner's call. Refuses to
  run on a project with too little history rather than manufacturing findings.
- **[adoption-only]** `templates/CLAUDE.template.md` lists `/sdlc-retro` alongside the
  four daily commands, so an adopting project learns the command exists. A command
  installed and named nowhere the project reads is a command nobody runs.
- **[installable]** `end-phase.md` step 7 offers `/sdlc-retro` after the phase closes.
  Every other kit command is reachable from the process — `SDLC.md` names `/plan-phase`,
  `/plan-phase` hands off to `/next-slice`, `/end-slice` to `/clear`. The retro had no
  caller, which for *this* command is self-defeating: it exists because the evidence
  supply depended on someone volunteering a retrospective. It is offered rather than
  required, and stays out of `SDLC.template.md` deliberately — a mandatory retro after
  every phase is the ceremony the retro's own "what would you delete?" question exists
  to catch. The failure it prevents is silent: no error, no drift, no `/kit-check`
  finding, just a command that ships in every bundle and never runs.

### Fixed
- The root README's *Updating an adopted project* section was missing the
  **new-files-in-the-target** clause that `sdlc-update.md` step 5 already had — so the
  two statements of the procedure disagreed, which the kit defines as a bug. A human
  following the README by hand would finish step 4 with no instruction that would ever
  create a newly-installed file, and step 6's verification checks only files you copied,
  so the omission verified clean. Found by `/kit-check` invariant 8 while adding
  `sdlc-retro.md` — the first new installed file since the clause was written, and
  exactly the case it exists for.
- **[adoption-only]** `reference/SKILLS.md`'s kit-command row listed five commands,
  omitting `sdlc-update` (shipped in 0.3.0) and `sdlc-retro`. It is a derived statement
  of the install mapping, so it now names its source of truth instead of quietly drifting
  from it a third time.
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
