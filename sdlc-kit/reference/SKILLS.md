# Skills — Required, Recommended, and How to Install

The SDLC leans on Claude Code **skills**. They come from three places, and knowing
which is which matters — only one of them travels with a `git clone`:

1. **Built into Claude Code** — ship with the tool itself; nothing to install, just
   keep Claude Code current (`claude update`).
2. **Shipped in this kit** (`sdlc-kit/skills/`) — the TDD skill set, vendored from
   public repos, plus the kit-written `diff-review`, `change-simplify`, and
   `change-verify`. **Not** part of either CLI.
   `/sdlc-setup` copies these into the target project's `.claude/skills/`, so once
   committed, every teammate gets them via `git clone` — no per-machine step. That
   directory is read by Claude Code *and* Copilot CLI, so one copy serves both
   (`reference/COPILOT.md`).
3. **Official plugin** — `pr-review-toolkit`, installed once per machine. **Optional
   since 0.14.0**, and Claude Code only; nothing in the process requires it.

## How to verify

In a session in the target project, available skills appear in the session's skill
listing (a user can type `/` to browse) — on either CLI. A skill is "available" if it
appears there. `/sdlc-setup` verifies the **source files and the installed copies** —
it cannot verify the listing itself. On Copilot CLI the owner can confirm it without
leaving the session: type `/skills reload`, then check the listing (`/skills info
<name>` prints a skill's resolved location — the fastest check that the right copy is
the one listed; both subcommands documented, verified 2026-08-07). On Claude Code the
listing is fixed for the session that wrote the files, so availability is confirmed in
a **fresh** session (checklist item 5 below). Either way: `tdd` must appear or the
install failed.

## How kit skills must NOT be updated: `gh skill`

Kit skills arrive by `/sdlc-setup` copying directories and move forward by
`/sdlc-update` — never by the `gh skill` extension. `gh skill install` **injects
provenance fields into `SKILL.md` frontmatter** — repository, ref, and git tree SHA —
and `gh skill update` compares those tree SHAs against the upstream repository.
(Confirmed against GitHub's changelog, 2026-04-16 entry; verified 2026-08-05.) Run
against a kit-installed skill, that mutates a file `/sdlc-update`'s enumeration and
this file's provenance regime expect byte-stable: the skill reads as drifted, or —
worse — gets "updated" to an upstream that is not the kit's version at all. This is
CLI-neutral, not a Copilot hazard: the extension targets six agents **including Claude
Code**. If a kit skill was already touched this way, strip the injected frontmatter
fields and let `/sdlc-update` re-verify the file against its manifest.

## Required

| Skill | Source | Role in the SDLC |
|---|---|---|
| `tdd` (+ `tdd-references/`) | **kit-vendored** → project `.claude/skills/tdd/` | The red–green–refactor loop for every slice; the vertical-slicing mandate and mock policy it enforces. `/next-slice` invokes it after reading `spec/TESTING.md`. **Setup must install this and halt if the copy fails.** |
| `diff-review` | **kit-written** → project `.claude/skills/diff-review/` | The reviewer both `/end-slice` (step 4, working diff) and `/end-phase` (step 5, arc range) name. Two axes reported side by side and never merged: **Spec** — does the change implement the slice's or phase's exit criteria, and only those — and **Standards** — does it follow `CLAUDE.md` *Runtime Conventions*, falling back to a structural-smell baseline. Names no CLI-specific agent or model, so it works on both CLIs. The built-in `/code-review` is the owner-typed, billed escalation — agents cannot launch it, and it is not what any command means by "review". |
| `change-simplify` | **kit-written** → project `.claude/skills/change-simplify/` | The post-green quality pass `/end-slice` step 3 names — reuse, simplification, efficiency, altitude, applied only where the slice introduced or worsened the condition. **The step is optional; the skill is not**, because a step that may run needs the skill present to decide against. Unlike `diff-review` it **edits**, so its prime directive is that behavior is frozen: an improvement that would change behavior is a finding, not an edit. |
| `change-verify` | **kit-written** → project `.claude/skills/change-verify/` | The verification pass named at **both** closes: `/end-slice` step 6 (slice close — optional but never silent, same contract as the quality pass) and `/end-phase` step 2 (phase level, on the arc). Exercises the change through the path a real caller takes rather than through the test harness — the gap a green gate structurally cannot cover. Its rule is that **a pass not observed is not a pass**: anything it could not exercise is reported unverified, so halt 4 is not spent on a check that never ran. |
| kit commands | this kit | `sdlc-setup`, `plan-phase`, `next-slice`, `end-slice`, `end-phase`, `sdlc-retro`, `sdlc-update` → copied into `<project>/.claude/commands/`, or packaged into `<project>/.github/skills/<name>/SKILL.md` on Copilot CLI; either way they travel with the repo. `sdlc-setup` is installed by hand — it cannot install its own entry point. The install list in `commands/sdlc-setup.md` (New mode step 5) is the source of truth for this set. |

## Shipped in `sdlc-kit/skills/` — what gets installed when

Five are vendored from upstreams; `diff-review/`, `change-simplify/`, and
`change-verify/` are kit-written. The install mechanics are identical, but the
*provenance regime* is not — see the note below the table.

Each is a skill directory holding a `SKILL.md`, copied whole into
`.claude/skills/<name>/`. The eight `SKILL.md` files share a basename — only the parent
directory tells them apart, so they are copied as directories, never as files.

| Directory | Install when | What it is |
|---|---|---|
| `tdd/` (`SKILL.md` + `tdd-references/{tests,mocking}.md`) | **always** | Core TDD skill: tracer-bullet vertical slicing, behavior-over-implementation testing, mock policy. `SKILL.md` links into `tdd-references/` relatively, so the subfolder travels with it. |
| `tdd-guide/` | optional | Broader multi-framework TDD guide (test generation, coverage analysis) — useful for teams new to TDD. |
| `mutation-testing/` | **always** | Test-suite strength assessment by injecting deliberate bugs. Required since 0.5.0: `/end-slice`'s mutation-check step invokes it, so it installs with the core set. |
| `diff-review/` | **always** | The two-axis reviewer (Spec + Standards) named by `/end-slice` step 4 and `/end-phase` step 5. Required since 0.14.0 — without it both commands name a reviewer that does not exist. **Kit-written, not vendored:** see the provenance note below. |
| `change-simplify/` | **always** | The post-green quality pass named by `/end-slice` step 3. Required since 0.14.0 even though the step is optional — the decision to skip it is only available if the skill is there to skip. **Kit-written, not vendored.** |
| `change-verify/` | **always** | The verification pass named by `/end-slice` step 6 (since 0.15.0) and `/end-phase` step 2. Required since 0.14.0 — without it the commands name a pass that does not exist. **Kit-written, not vendored.** |
| `python-pro/` | Python projects only | Typed, strict-mypy Python idioms (attribution: github.com/Jeffallan). |
| `hypothesis-tests/` | Python projects only | Property-based test authoring with Hypothesis. |

**Provenance & licensing:**

- `diff-review/SKILL.md` — **kit-written, 2026-08-03. No upstream, nothing vendored.**
  Its *design* is owed to [mattpocock/skills](https://github.com/mattpocock/skills)
  (`skills/engineering/code-review/`, MIT): the two-axis Spec/Standards split, running
  the axes independently, and reporting them side by side without merging or reranking
  are that skill's ideas, and the structural-smell baseline is the familiar Fowler set
  it also draws on. **The text is not copied and the file is not a derivative** — the
  upstream reaches its Spec axis through a `docs/agents/issue-tracker.md` and issue
  references in commit messages, which this kit has no equivalent for by design; its
  unit of work is the slice, and `spec/` plus `PROJECT_INDEX.md` supply the intent
  directly. Adopting the file would have meant four permanent divergences on day one
  (spec source, standards location, subagent type, issue-tracker excision) against an
  upstream carrying no `license:` frontmatter to vendor from, so the idea was taken and
  the plumbing was not. Recorded here because the debt is real even though the licence
  obligation is not.
- `change-simplify/SKILL.md`, `change-verify/SKILL.md` — **kit-written, 2026-08-03. No
  upstream, nothing vendored.** Each carries a pass Claude Code ships as a built-in
  (`simplify`, `verify`) and Copilot CLI has no equivalent for, so the kit writes its
  own and the process can name the pass without knowing which CLI is running. **The
  built-ins were not read, copied, or derived from** — what was portable was the idea of
  the pass, which is not anyone's to license. The names deliberately differ from the
  built-ins': a project-scoped skill named `simplify` or `verify` would shadow one, and
  this file already tells adopters not to recreate built-ins by hand.
- `tdd/SKILL.md`, `tdd/tdd-references/tests.md`, `tdd/tdd-references/mocking.md` — from
  [mattpocock/skills](https://github.com/mattpocock/skills)
  (`skills/engineering/tdd/`), **MIT license** — redistribution is fine; keep this
  attribution. Verified 2026-07-19 against the repo's pre-2026-06-30 revision
  (word-for-word match; our copies have install-layout link paths and, in the two
  reference files, examples localized per project). The upstream skill was later
  reshaped ("reference-only with pre-agreed seams", red→green without a refactor
  stage) — worth a look when next refreshing the kit.
- `hypothesis-tests/SKILL.md` — verbatim from
  [honnibal/claude-skills](https://github.com/honnibal/claude-skills)
  (`hypothesis-tests.md.txt`), **MIT license**. Verified 2026-07-19 (one-word diff).
  The frontmatter carries `disable-model-invocation: true`, present since vendoring
  (in-tree history, checked 2026-08-09) — on Claude Code that documented field makes
  the skill user-typed-only; on Copilot CLI it is undocumented and expected to be
  silently ignored (`reference/COPILOT.md`, which also states the kit adopts the
  field as no mechanism of its own).
- `mutation-testing/SKILL.md` — condensed derivative of the same repo's
  `mutation-testing.md.txt` (**MIT**): same structure, terminology ("3–8 mutations",
  never-stack/always-revert rules, diagnostic-quality ratings, mutation score), and
  `argument-hint` frontmatter, at roughly half the length; the upstream long form is
  worth consulting when refreshing the kit. The condensed text itself has no public
  GitHub match — it appears to be a local adaptation.
- `tdd-guide/SKILL.md` — from
  [alirezarezvani/claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory)
  (`generated-skills/tdd-guide/SKILL.md`), **MIT license**. Verified 2026-07-19: our
  copy is the upstream's first ~120 lines with invocation syntax and one example
  adapted; the dropped tail documents companion Python scripts that were never
  installed.
- `python-pro/SKILL.md` — carries `author: https://github.com/Jeffallan`. **Diverged
  2026-07-19:** the "Reference Guide" table was removed — it pointed at five
  `references/*.md` companion files that were never part of the kit, so every path
  dangled after install.

All identified upstreams are MIT — team and external distribution are fine with these
attributions kept intact. The exception to note: `python-pro/SKILL.md` has no identified
upstream repository; its frontmatter self-declares `license: MIT` with an author
attribution, but a self-declaration with no locatable upstream cannot be checked
against anything — treat its redistribution status as unverified rather than settled.

## Recommended built-ins (nothing to install)

The passes below are not required by any command; they are worth reaching for anyway.
**Read the availability columns before relying on one** — a recommendation that holds on
one CLI and not the other is exactly how an adopter ends up told to run something they
do not have.

| Pass | When | Claude Code | Copilot CLI |
|---|---|---|---|
| exercise a change end-to-end | before committing nontrivial changes | `verify` (built-in) **or** the kit's `change-verify` | `change-verify` (kit-shipped) |
| post-green quality pass | on the slice diff, before review | `simplify` (built-in) **or** the kit's `change-simplify` | `change-simplify` (kit-shipped) |
| secure-coding review | phases touching auth, secrets, user input, or the network | `security-review` (built-in) **or** the lenses | the secure-coding lenses in `.claude/commands/REVIEW_LENSES.md` |
| edit hook/permission config safely | changing the gate hook or permissions | `update-config` (built-in) | **not needed** — Copilot's config is plain JSON any editor can open |

Two rules for reading that table:

- **Where a row offers both, run one.** The kit's version exists so the pass is
  available on Copilot, not to double up on Claude Code. Running both over the same
  range is waste, not rigour.
- **A missing built-in is an outdated install, not a gap to fill.** If a built-in named
  here is absent from the Claude Code skill listing, run `claude update`; do not
  recreate it by hand. The kit's own equivalents are deliberately named differently
  (`change-verify`, `change-simplify`) so that installing them shadows nothing.

Rows one and two used to read "none" on the Copilot side. `change-verify` and
`change-simplify` closed them in 0.14.0, and both are now named by the process rather
than merely recommended — `change-verify` at `/end-slice` step 6 and `/end-phase`
step 2, `change-simplify` at `/end-slice` step 3. Row three was closed by the review
lenses in 0.13.0.

**The review apparatus left this list entirely.** Until 0.14.0 the per-slice and
whole-arc reviews named `pr-review-toolkit`, which does not exist on Copilot, so an
adopter there was told to run a reviewer they did not have. `diff-review` is kit-owned
and installs to `.claude/skills/`, which both CLIs read — so the reviewer the commands
name now exists wherever the kit is installed. `pr-review-toolkit` remains available as
an optional Claude-Code-only deepening at phase end and is required by nothing.

## Custom skills

Project-specific additions (Dungeon Daddy has `/ui-test` and `/assess-tests`) follow
the same split the kit's own files do: something the owner *types* is a command in
`.claude/commands/`; something a session should reach for on its own is a skill
directory in `.claude/skills/<name>/SKILL.md`. Both are project-scoped and shared via
git. The machine-scoped equivalents (`~/.claude/commands/`, `~/.claude/skills/`) do NOT
travel with the repo. Pattern to copy: a markdown file stating *when to use it*, *the
workflow as numbered steps*, and *what halts for the owner*. **Prefer project-scoped** —
anything a teammate needs must be in the repo, not on your machine.

## Team onboarding checklist (per developer machine)

1. Install the CLI this project adopted — ask, or look at what it holds: a
   `.github/hooks/` gate is a Copilot project, a `.claude/settings.json` one is Claude
   Code, and a repo may hold both. On Claude Code, run `claude update` to current.
2. Clone the project repo — the kit commands, the TDD skill set, `diff-review`,
   `change-simplify`, `change-verify`, the hook, and the specs all come with it (they
   were installed project-scoped by `/sdlc-setup`). **Nothing per-machine is required
   for review** — which was not the case before 0.14.0.
3. Optional, Claude Code only:
   `/plugin install pr-review-toolkit@claude-plugins-official` — a deeper specialist
   fan-out at phase end. Skipping it costs depth, not correctness.
4. Install the project toolchain so **the gate runs locally** (right language version —
   a wrong local runtime makes the local gate lie; CI is authoritative when they differ).
5. Open the CLI in the repo, type `/` and confirm `tdd`, `diff-review`,
   `change-simplify`, `change-verify`, and the seven SDLC commands appear, then run
   `/next-slice` and confirm it orients correctly. The three kit-written skills are the
   ones worth catching early — the commands name them, so a session otherwise finds out
   at slice or phase close rather than at setup. Nothing appearing
   is an install-path problem, not a missing skill — check where they landed against
   the install list in `commands/sdlc-setup.md`.
