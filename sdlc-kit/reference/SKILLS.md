# Skills — Required, Recommended, and How to Install

The SDLC leans on Claude Code **skills**. They come from three places, and knowing
which is which matters — only one of them travels with a `git clone`:

1. **Built into Claude Code** — ship with the tool itself; nothing to install, just
   keep Claude Code current (`claude update`).
2. **Vendored in this kit** (`sdlc-kit/skills/`) — the TDD skill set, originally
   installed from a public repo. **Not** part of Claude Code. `/sdlc-setup` copies
   these into the target project's `.claude/commands/`, so once committed, every
   teammate gets them via `git clone` — no per-machine step.
3. **Official plugin** — `pr-review-toolkit`, installed once per machine.

## How to verify

In a Claude Code session in the target project, available skills appear in the
session's skill listing (a user can type `/` to browse). A skill is "available" if it
appears there. `/sdlc-setup` checks this; after setup, `tdd` must appear or the
install failed.

## Required

| Skill | Source | Role in the SDLC |
|---|---|---|
| `tdd` (+ `tdd-references/`) | **kit-vendored** → project `.claude/commands/` | The red–green–refactor loop for every slice; the vertical-slicing mandate and mock policy it enforces. `/next-slice` invokes it after reading `spec/TESTING.md`. **Setup must install this and halt if the copy fails.** |
| `pr-review-toolkit` | official plugin | The per-slice diff review in `/end-slice` (`pr-review-toolkit:code-reviewer`) and the whole-arc PR review in `/end-phase` (`pr-review-toolkit:review-pr` plus specialized reviewer agents). Once per machine: `/plugin install pr-review-toolkit@claude-plugins-official`. The built-in `/code-review` is the owner-typed, billed escalation — agents cannot launch it, and it is not what any command means by "review". |
| kit commands | this kit | `sdlc-setup`, `plan-phase`, `next-slice`, `end-slice`, `end-phase`, `sdlc-retro`, `sdlc-update` → copied into `<project>/.claude/commands/`; travel with the repo. The install list in `commands/sdlc-setup.md` (New mode step 5) is the source of truth for this set. |

## Vendored in `sdlc-kit/skills/` — what gets installed when

| File | Install when | What it is |
|---|---|---|
| `tdd.md` + `tdd-references/{tests,mocking}.md` | **always** | Core TDD skill: tracer-bullet vertical slicing, behavior-over-implementation testing, mock policy. |
| `tdd-guide.md` | optional | Broader multi-framework TDD guide (test generation, coverage analysis) — useful for teams new to TDD. |
| `mutation-testing.md` | **always** | Test-suite strength assessment by injecting deliberate bugs. Required since 0.5.0: `/end-slice`'s mutation-check step invokes it, so it installs with the core set. |
| `python-pro.md` | Python projects only | Typed, strict-mypy Python idioms (attribution: github.com/Jeffallan). |
| `hypothesis-tests.md` | Python projects only | Property-based test authoring with Hypothesis. |

**Provenance & licensing:**

- `tdd.md`, `tdd-references/tests.md`, `tdd-references/mocking.md` — from
  [mattpocock/skills](https://github.com/mattpocock/skills)
  (`skills/engineering/tdd/`), **MIT license** — redistribution is fine; keep this
  attribution. Verified 2026-07-19 against the repo's pre-2026-06-30 revision
  (word-for-word match; our copies have install-layout link paths and, in the two
  reference files, examples localized per project). The upstream skill was later
  reshaped ("reference-only with pre-agreed seams", red→green without a refactor
  stage) — worth a look when next refreshing the kit.
- `hypothesis-tests.md` — verbatim from
  [honnibal/claude-skills](https://github.com/honnibal/claude-skills)
  (`hypothesis-tests.md.txt`), **MIT license**. Verified 2026-07-19 (one-word diff).
- `mutation-testing.md` — condensed derivative of the same repo's
  `mutation-testing.md.txt` (**MIT**): same structure, terminology ("3–8 mutations",
  never-stack/always-revert rules, diagnostic-quality ratings, mutation score), and
  `argument-hint` frontmatter, at roughly half the length; the upstream long form is
  worth consulting when refreshing the kit. The condensed text itself has no public
  GitHub match — it appears to be a local adaptation.
- `tdd-guide.md` — from
  [alirezarezvani/claude-code-skill-factory](https://github.com/alirezarezvani/claude-code-skill-factory)
  (`generated-skills/tdd-guide/SKILL.md`), **MIT license**. Verified 2026-07-19: our
  copy is the upstream's first ~120 lines with invocation syntax and one example
  adapted; the dropped tail documents companion Python scripts that were never
  installed.
- `python-pro.md` — carries `author: https://github.com/Jeffallan`. **Diverged
  2026-07-19:** the "Reference Guide" table was removed — it pointed at five
  `references/*.md` companion files that were never part of the kit, so every path
  dangled after install.

All identified upstreams are MIT — team and external distribution are fine with these
attributions kept intact. The exception to note: `python-pro.md` has no identified
upstream repository or license text, only its in-file author attribution — treat its
redistribution status as unverified rather than settled.

## Recommended built-ins (nothing to install)

| Skill | When |
|---|---|
| `verify` | Before committing nontrivial changes — exercises the change end-to-end, not just tests. |
| `simplify` | Post-green refactor pass on the slice diff. |
| `security-review` | Phases touching auth, secrets, user input, or the network. |
| `update-config` | Editing `.claude/settings.json` (hooks, permissions) safely. |

If a built-in listed here is missing from the skill listing, the Claude Code install is
outdated — run `claude update`; do not try to recreate built-ins by hand.

## Custom skills

Project-specific commands beyond the five (Dungeon Daddy has `/ui-test` and
`/assess-tests`) live in `.claude/commands/` (project-scoped, shared via git) or
`~/.claude/commands/` / `~/.claude/skills/` (machine-scoped, does NOT travel with the
repo). Pattern to copy: a markdown file stating *when to use it*, *the workflow as
numbered steps*, and *what halts for the owner*. **Prefer project-scoped** — anything a
teammate needs must be in the repo, not on your machine.

## Team onboarding checklist (per developer machine)

1. Install Claude Code; run `claude update` to current.
2. `/plugin install pr-review-toolkit@claude-plugins-official`
3. Clone the project repo — the kit commands, TDD skill set, hook, and specs all come
   with it (they were installed project-scoped by `/sdlc-setup`).
4. Install the project toolchain so **the gate runs locally** (right language version —
   a wrong local runtime makes the local gate lie; CI is authoritative when they differ).
5. Open Claude Code in the repo, type `/` and confirm `tdd` and the five SDLC commands
   appear, then run `/next-slice` and confirm it orients correctly.
