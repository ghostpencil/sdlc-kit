# Changelog

Kit-scoped, semver-ish. Versions describe **the kit**, not any project that adopted it.
This file is repo documentation and is not shipped inside `sdlc-kit/`; the bundle carries
its version in `sdlc-kit/VERSION`.

An entry marked **[installable]** changes a file an adopted project holds
(`commands/**`, `skills/**`) and therefore matters at update time. Entries marked
**[adoption-only]** change `templates/**` or `reference/**`, which are read at
`/sdlc-setup` time and never re-applied to an already-adopted project.

## Unreleased

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
- **[installable]** `/sdlc-setup` authors the isolation harness for the detected stack
  (New mode step 4; Existing mode proposes it at the feedback halt) and **proves each
  check by its negative case** — a deliberate violation must fail the suite loudly,
  naming what was attempted, before the check is described as enforced. If the owner
  defers it, the gap goes to the backlog and `{{ISOLATION_HARNESS}}` records what is
  actually enforced today — never enforcement that does not exist. Acceptance was run
  for real in a non-Python stack (Node): the harness authored from the spec alone
  failed loudly on a deliberate `fetch` (naming the address) and a credential-path
  read, then ran 3/3 green with a shell-set token provably not reaching tests.

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
