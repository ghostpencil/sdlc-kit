# Skills — Required, Recommended, and How to Install

The SDLC leans on Claude Code **skills**. They come from three places, and knowing
which is which matters — only one of them travels with a `git clone`:

1. **Built into Claude Code** — ship with the tool itself; nothing to install, just
   keep Claude Code current (`claude update`).
2. **Shipped in this kit** (`sdlc-kit/skills/`) — the TDD skill set, vendored from
   public repos, plus the kit-written `diff-review`. **Not** part of either CLI.
   `/sdlc-setup` copies these into the target project's `.claude/skills/`, so once
   committed, every teammate gets them via `git clone` — no per-machine step. That
   directory is read by Claude Code *and* Copilot CLI, so one copy serves both
   (`reference/COPILOT.md`).
3. **Official plugin** — `pr-review-toolkit`, installed once per machine. **Optional
   since 0.14.0**, and Claude Code only; nothing in the process requires it.

## How to verify

In a session in the target project, available skills appear in the session's skill
listing (a user can type `/` to browse) — on either CLI. A skill is "available" if it
appears there. `/sdlc-setup` checks this; after setup, `tdd` must appear or the
install failed.

## Required

| Skill | Source | Role in the SDLC |
|---|---|---|
| `tdd` (+ `tdd-references/`) | **kit-vendored** → project `.claude/skills/tdd/` | The red–green–refactor loop for every slice; the vertical-slicing mandate and mock policy it enforces. `/next-slice` invokes it after reading `spec/TESTING.md`. **Setup must install this and halt if the copy fails.** |
| `diff-review` | **kit-vendored** → project `.claude/skills/diff-review/` | The reviewer both `/end-slice` (step 3, working diff) and `/end-phase` (step 5, arc range) name. Two axes reported side by side and never merged: **Spec** — does the change implement the slice's or phase's exit criteria, and only those — and **Standards** — does it follow `CLAUDE.md` *Runtime Conventions*, falling back to a structural-smell baseline. Names no CLI-specific agent or model, so it works on both CLIs. The built-in `/code-review` is the owner-typed, billed escalation — agents cannot launch it, and it is not what any command means by "review". |
| kit commands | this kit | `sdlc-setup`, `plan-phase`, `next-slice`, `end-slice`, `end-phase`, `sdlc-retro`, `sdlc-update` → copied into `<project>/.claude/commands/`; travel with the repo. The install list in `commands/sdlc-setup.md` (New mode step 5) is the source of truth for this set. |

## Shipped in `sdlc-kit/skills/` — what gets installed when

Five are vendored from upstreams; `diff-review/` is kit-written. The install mechanics
are identical, but the *provenance regime* is not — see the note below the table.

Each is a skill directory holding a `SKILL.md`, copied whole into
`.claude/skills/<name>/`. The six `SKILL.md` files share a basename — only the parent
directory tells them apart, so they are copied as directories, never as files.

| Directory | Install when | What it is |
|---|---|---|
| `tdd/` (`SKILL.md` + `tdd-references/{tests,mocking}.md`) | **always** | Core TDD skill: tracer-bullet vertical slicing, behavior-over-implementation testing, mock policy. `SKILL.md` links into `tdd-references/` relatively, so the subfolder travels with it. |
| `tdd-guide/` | optional | Broader multi-framework TDD guide (test generation, coverage analysis) — useful for teams new to TDD. |
| `mutation-testing/` | **always** | Test-suite strength assessment by injecting deliberate bugs. Required since 0.5.0: `/end-slice`'s mutation-check step invokes it, so it installs with the core set. |
| `diff-review/` | **always** | The two-axis reviewer (Spec + Standards) named by `/end-slice` step 3 and `/end-phase` step 5. Required since 0.14.0 — without it both commands name a reviewer that does not exist. **Kit-written, not vendored:** see the provenance note below. |
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

| Skill | When |
|---|---|
| `verify` | Before committing nontrivial changes — exercises the change end-to-end, not just tests. |
| `simplify` | Post-green refactor pass on the slice diff. |
| `security-review` | Phases touching auth, secrets, user input, or the network. |
| `update-config` | Editing `.claude/settings.json` (hooks, permissions) safely. |

If a built-in listed here is missing from the skill listing, the Claude Code install is
outdated — run `claude update`; do not try to recreate built-ins by hand.

**These are Claude Code built-ins.** On Copilot CLI none of the four exists. What that
costs, and what stands in for each, is in `reference/COPILOT.md` — *What the kit loses
on Copilot today*. Do not read this table as a promise on that CLI.

**The review apparatus is no longer on that list.** Until 0.14.0 the per-slice and
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
2. Clone the project repo — the kit commands, the TDD skill set, `diff-review`, the
   hook, and the specs all come with it (they were installed project-scoped by
   `/sdlc-setup`). **Nothing per-machine is required for review** — which was not the
   case before 0.14.0.
3. Optional, Claude Code only:
   `/plugin install pr-review-toolkit@claude-plugins-official` — a deeper specialist
   fan-out at phase end. Skipping it costs depth, not correctness.
4. Install the project toolchain so **the gate runs locally** (right language version —
   a wrong local runtime makes the local gate lie; CI is authoritative when they differ).
5. Open the CLI in the repo, type `/` and confirm `tdd`, `diff-review`, and the seven
   SDLC commands appear, then run `/next-slice` and confirm it orients correctly.
   `diff-review` missing is the one worth catching early — `/end-slice` names it, so a
   session finds out at slice close rather than at setup. Nothing appearing
   is an install-path problem, not a missing skill — check where they landed against
   the install list in `commands/sdlc-setup.md`.
