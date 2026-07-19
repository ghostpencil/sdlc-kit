# The Agentic SDLC Kit

A reusable, language-agnostic software development lifecycle for AI-assisted development
with Claude Code. Extracted and generalized from the process battle-tested on the
Dungeon Daddy project (50+ phases shipped with it).

It works for any programming language and any type of application — CLI tools, web
services, GUI apps, libraries. The process is the constant; the tooling (linter, type
checker, test runner) is configured per project during setup.

---

## The process in one paragraph

Work is organized as **phases → slices → TDD cycles**. A *phase* is one feature (one
branch, one spec, one PR). A *slice* is one coherent behavior, small enough for a single
fresh-context session, built test-first and committed before context is cleared. A *TDD
cycle* is one red–green–refactor step. The agent runs autonomously between five **owner
halt points** (phase scope, slice scope, design questions, acceptance review, merge
approval). Every slice must pass **the gate** — lint + typecheck + tests, all green —
before it is committed. A single file, `spec/PROJECT_INDEX.md`, is the source of truth
for status, so every fresh session can orient itself in seconds.

Full process: see `templates/SDLC.template.md` (becomes `spec/SDLC.md` in your project).

## Why it works (the short version for the team)

- **Context is a budget.** Sessions read only `CLAUDE.md` + `spec/PROJECT_INDEX.md` at
  start and load other specs on demand. Small context = sharper agent.
- **Fresh session per slice.** Long conversations degrade. Each slice starts clean and
  ends with everything recorded on disk, so nothing lives only in chat history.
- **TDD keeps the agent honest.** A failing test written first is a contract the agent
  can't quietly reinterpret. The kit's vendored TDD skill enforces the loop.
- **The gate is non-negotiable.** Lint + typecheck + tests green before every commit.
  A file-edit hook surfaces most failures at edit time, not at slice end.
- **You stay in charge at exactly five points.** Everything else runs without asking, so
  you're not rubber-stamping trivia — and the five halts are never skipped, so the agent
  never decides scope, design, or merges for you.
- **Specs are interrogated, not assumed.** `/plan-phase` interviews you and then
  adversarially attacks its own understanding before writing a build-ready spec.

---

## Quick start

### Both modes

1. Get the `sdlc-kit/` folder into the root of the target repository. It must keep that
   name — `/sdlc-setup` looks for it by name.

   **Download a release** (recommended — no git surgery, and the bundle is checksummed):

   ```bash
   cd /path/to/target-project
   curl -sL https://github.com/ghostpencil/sdlc-kit/releases/latest/download/sdlc-kit-<version>.tar.gz | tar -xz
   cd sdlc-kit && sha256sum -c MANIFEST.sha256 && cd ..   # verify; shasum -a 256 -c on macOS
   ```

   Releases: <https://github.com/ghostpencil/sdlc-kit/releases>

   **Or clone this repo** and lift the kit folder out of it:

   ```bash
   cd /path/to/target-project
   git clone --depth 1 https://github.com/ghostpencil/sdlc-kit /tmp/sdlc-kit-src
   cp -r /tmp/sdlc-kit-src/sdlc-kit ./sdlc-kit    # the kit only — not the repo's own docs
   ```

   Either way you end up with plain files (not a nested git repo) that you commit
   alongside your project.
2. Copy `sdlc-kit/commands/sdlc-setup.md` into the target's `.claude/commands/`
   (create the folder if needed).
3. Open Claude Code in the target repo and run **`/sdlc-setup`**.

Setup auto-detects the mode and confirms it with you:

- **New Project mode** — an empty or nearly-empty repo. Setup interviews you (language,
  app type, tooling, test framework, run command…), scaffolds the toolchain and spec
  files from the templates, installs the commands and the edit-time gate hook, and
  leaves you ready to run `/plan-phase` for Phase 1.
- **Existing Project mode** — a repo with real code in it. Setup analyzes the codebase
  (language, build system, how tests actually run, CI, existing docs), proposes a gate
  and a spec set, and confirms everything with you before writing anything. Existing
  files are merged, never overwritten. It then baselines the gate honestly — a red gate
  becomes your initial STABILIZATION backlog, not a blocker.

Either way, setup **installs the required skills**. The TDD skill is *not* built into
Claude Code — the kit vendors it in `skills/` and setup copies it into the target
project's `.claude/commands/`, so the whole team inherits it via `git clone`. Built-in
skills (code-review, verify, …) are verified, and the one plugin (`pr-review-toolkit`)
gets a one-line install instruction if absent. See `reference/SKILLS.md`.

### After setup, the daily loop

| Command | When |
|---|---|
| `/plan-phase` | At a phase boundary — turn an idea into a build-ready spec |
| `/next-slice` | First command of every fresh session — orient, confirm scope, TDD |
| `/end-slice` | Slice done — gate, code review, commit, record, then `/clear` |
| `/end-phase` | Last slice done — gate, acceptance review, PR, review, merge |

One slice per session. `/clear` after every `/end-slice`. That's the rhythm.

---

## What's in the kit

This repository is split in two: **`sdlc-kit/` is the product** — the only folder that
goes into your project — and everything at the root is documentation *about* the kit,
which you do not need to install.

```
sdlc-kit/                            ← THE KIT — copy this folder into your project
├── VERSION                          ← the kit version this bundle is
├── MANIFEST.sha256                  ← checksums of every file in the bundle
├── README.md                        ← install + verify, for people who only have the bundle
├── commands/                        ← installed into <project>/.claude/commands/
│   ├── sdlc-setup.md                ← the two-mode setup command (start here)
│   ├── plan-phase.md
│   ├── next-slice.md
│   ├── end-slice.md
│   └── end-phase.md
├── skills/                          ← vendored skills → <project>/.claude/commands/
│   ├── tdd.md                       ← THE TDD skill (not built into Claude Code)
│   ├── tdd-references/              ← tests.md + mocking.md (linked from tdd.md)
│   ├── tdd-guide.md                 ← optional: broader TDD guide for teams new to it
│   ├── mutation-testing.md          ← optional: test-suite strength assessment
│   ├── python-pro.md                ← Python projects only
│   └── hypothesis-tests.md          ← Python projects only
├── templates/                       ← instantiated into the project by /sdlc-setup
│   ├── SDLC.template.md             → spec/SDLC.md        (the canonical process)
│   ├── CLAUDE.template.md           → CLAUDE.md           (agent instructions)
│   ├── PROJECT_INDEX.template.md    → spec/PROJECT_INDEX.md (source of truth)
│   ├── TESTING.template.md          → spec/TESTING.md     (TDD + mock policy)
│   └── settings.template.json       → .claude/settings.json (edit-time gate hook)
├── reference/                       ← consulted by /sdlc-setup; not installed
│   ├── GATE_RECIPES.md              ← gate + hook commands per language
│   └── SKILLS.md                    ← required/recommended skills and how to install
├── THIRD_PARTY_NOTICES.md           ← attributions for the vendored skills (all MIT)
└── LICENSE                          ← MIT (must travel with the bundle)

.github/workflows/release.yml        ← packages the kit as a release asset on tag push
README.md                            ← you are here
CLAUDE.md                            ← instructions for agents working ON the kit
CHANGELOG.md                         ← kit version history
FIELD_REPORT.md                      ← findings from the first external adoption
IMPROVEMENT_PLAN.md                  ← what is being done about them
LICENSE                              ← MIT
```

Paths written as `commands/…` or `templates/…` elsewhere in the docs are relative to
`sdlc-kit/`, which is also how they read once the folder is inside your project.

Templates use `{{PLACEHOLDER}}` markers; `/sdlc-setup` resolves every one of them with
you before finishing (and greps for leftover `{{` as its own exit check).

---

## Updating an adopted project

Adopting the kit copies files into your project. Later kit releases do not reach them on
their own — this is the procedure that brings them forward without destroying what your
project has recorded.

### Who owns what

The whole procedure rests on this split:

| Path in your project | Owner | Update behavior |
|---|---|---|
| `.claude/commands/*.md` (from `commands/`, `skills/`) | **kit** | Tracks upstream. Overwritten when provably unmodified; you decide when drifted. |
| `CLAUDE.md`, `spec/*.md`, `.claude/settings.json` | **project** | **Never overwritten.** These hold your gate baseline, owner decisions, backlog, and gotchas. |

`templates/` and `reference/` are read only at `/sdlc-setup` time and are never
re-applied to an already-adopted project. A kit release that changes only those is an
adoption-only change — it affects new adoptions, not yours. `CHANGELOG.md` marks each
entry accordingly.

### The procedure

1. **Find the version you are on.** `spec/SDLC.md` records it (*Kit version: X.Y.Z*).
   Projects adopted before 0.2.0 have no stamp; see *No version stamp* below.

2. **Get both versions of the kit.**

   ```bash
   git clone https://github.com/ghostpencil/sdlc-kit /tmp/kit
   git -C /tmp/kit worktree add /tmp/kit-old vX.Y.Z    # the version you are on
   ```

3. **Classify every installed file** against the manifest of the version you are *on* —
   not the new one. That is what makes the answer provable rather than hopeful.

   ```bash
   cd /path/to/your-project/.claude/commands
   for f in *.md; do
     want=$(grep -E "(commands|skills)/(.*/)?$f\$" /tmp/kit-old/sdlc-kit/MANIFEST.sha256 | cut -d' ' -f1)
     have=$(sha256sum "$f" | cut -d' ' -f1)
     if   [ -z "$want" ];        then echo "UNKNOWN   $f  (not from the kit — yours)"
     elif [ "$want" = "$have" ]; then echo "UNCHANGED $f  (safe to overwrite)"
     else                             echo "DRIFTED   $f  (review the diff — your call)"
     fi
   done
   ```

4. **Act on the classification.**
   - `UNCHANGED` → provably untouched since adoption. Copy the new version over it.
   - `DRIFTED` → you or setup edited it. Diff it against both versions and decide, file
     by file. **Never auto-overwrite a drifted file** — `spec/SDLC.md` explicitly invites
     you to fix a command that disagrees with it, so drift is often deliberate.
   - `UNKNOWN` → not a kit file. Leave it alone.

5. **Touch nothing project-owned.** Do not let an update rewrite `spec/SDLC.md`,
   `spec/PROJECT_INDEX.md`, `spec/TESTING.md`, `CLAUDE.md`, or `.claude/settings.json`.
   They hold your recorded baseline and decisions; the kit cannot regenerate them.

6. **Re-record the version** in `spec/SDLC.md` (*Kit version: X.Y.Z*, dated). From here
   every later update is mechanical.

7. **Land it as a normal PR** (`chore/update-sdlc-kit-X.Y.Z`) — the same way the adoption
   landed. Read `CHANGELOG.md` for the versions you skipped; entries marked
   *[installable]* are the ones that changed what you just copied.

### No version stamp (adopted before 0.2.0)

Manifests did not exist before 0.2.0, but they can be reconstructed from any tag, which is
enough to make the same check work retroactively:

```bash
git -C /tmp/kit archive v0.1.0 | tar -tf - | grep -E '^(sdlc-kit/)?(commands|skills)/'
# hash each of those paths out of the tag and compare with your installed copies
```

If your files match a released version's contents, you are provably on that version and
step 3 applies unchanged. If they match nothing, treat every file as `DRIFTED`.

## FAQ

**Does this require Python?** No. The process is language-agnostic. The gate commands
are configured per project — `reference/GATE_RECIPES.md` has recipes for Python,
TypeScript/JavaScript, C#/.NET, Go, Java, and Rust, and the pattern extends to anything
with a linter and a test runner.

**What if my language has no type checker?** The gate's typecheck step is optional —
setup drops it (or substitutes a compile step) where it doesn't apply.

**Can I adopt this mid-flight on a messy codebase?** Yes — that's what Existing Project
mode is for. It documents reality (including a red gate) rather than pretending, and
starts you in STABILIZATION until the gate is green.

**Where do the skills come from?** Three places. The TDD skill set is **vendored in
this kit** (`skills/` — originally from a public community repo; it is NOT part of
Claude Code) and installed project-scoped so it travels with the repo. Skills like
code-review, verify, and simplify are built into Claude Code itself. `pr-review-toolkit`
is an official plugin installed once per machine with one command. Details in
`reference/SKILLS.md` — `/sdlc-setup` handles all of this.

**Do I have to use every part?** The load-bearing parts are: the gate, TDD-first
slices, fresh session per slice, and PROJECT_INDEX as the single source of truth. The
five halt points assume a single owner; for a team, map them onto your review process
(e.g. merge approval = normal PR review).
