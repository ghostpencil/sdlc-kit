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
│   ├── end-phase.md
│   ├── sdlc-retro.md                ← lessons-learned extraction at a phase boundary
│   └── sdlc-update.md               ← brings an adopted project to a newer kit release
├── skills/                          ← vendored skills → <project>/.claude/commands/
│   ├── tdd.md                       ← THE TDD skill (not built into Claude Code)
│   ├── tdd-references/              ← tests.md + mocking.md (linked from tdd.md)
│   ├── tdd-guide.md                 ← optional: broader TDD guide for teams new to it
│   ├── mutation-testing.md          ← always installed — /end-slice's mutation check invokes it
│   ├── python-pro.md                ← Python projects only
│   └── hypothesis-tests.md          ← Python projects only
├── agents/                          ← installed into <project>/.claude/agents/
│   └── sdlc-surveyor.md             ← read-only mechanical-collection agent (haiku)
├── templates/                       ← instantiated into the project by /sdlc-setup
│   ├── SDLC.template.md             → spec/SDLC.md        (the canonical process)
│   ├── CLAUDE.template.md           → CLAUDE.md           (agent instructions)
│   ├── PROJECT_INDEX.template.md    → spec/PROJECT_INDEX.md (source of truth)
│   ├── TESTING.template.md          → spec/TESTING.md     (TDD + mock policy)
│   └── settings.template.json       → .claude/settings.json (edit-time gate hook)
├── reference/                       ← consulted by /sdlc-setup
│   ├── GATE_RECIPES.md              ← gate + hook commands per language
│   ├── SKILLS.md                    ← required/recommended skills and how to install
│   └── REVIEW_LENSES.md             → <project>/.claude/commands/ (the one installed reference file)
├── THIRD_PARTY_NOTICES.md           ← attributions for the vendored skills (all MIT)
└── LICENSE                          ← MIT (must travel with the bundle)

.github/workflows/release.yml        ← packages the kit as a release asset on tag push
.claude/commands/kit-check.md        ← /kit-check: kit self-check (development-only, never installed)
.gitattributes                       ← pins LF — the manifest hashes depend on it
.gitignore
README.md                            ← you are here
CLAUDE.md                            ← instructions for agents working ON the kit
CHANGELOG.md                         ← kit version history
FIELD_REPORT.md                      ← findings from the first external adoption
FIELD_REPORT_2026-07-20.md           ← findings from the second arc — /sdlc-retro's first real run
IMPROVEMENT_PLAN.md                  ← what was done about them (closed at v0.3.0)
FEATURE_PLAN.md                      ← post-field-report feature work (retro, agents, model tiers)
KIT_INVARIANTS.md                    ← the invariant ledger /kit-check verifies
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

Setup installs this procedure as a command: run **`/sdlc-update`** in the adopted
project and it walks these same steps, halting once for drifted files. This section is
the human-readable statement of the same procedure — the command and this section must
agree, and a disagreement between them is a kit bug. Projects adopted before the command
existed follow this section by hand once; the update itself installs the command.

**Update at a phase/arc boundary, never with an arc in flight.** A mid-arc update
changes the rules governing slices already scoped, and which kit version governed which
slice becomes unreconstructable afterward. If one is truly unavoidable, record the
version change against the affected slices in `spec/PROJECT_INDEX.md`.

### Who owns what

The whole procedure rests on this split:

| Path in your project | Owner | Update behavior |
|---|---|---|
| `.claude/commands/*.md` (from `commands/`, `skills/`, `reference/REVIEW_LENSES.md`) | **kit** | Tracks upstream. Overwritten when provably unmodified; you decide when drifted. |
| `.claude/agents/*.md` (from `agents/`) | **kit** | Same rule — overwritten when provably unmodified; you decide when drifted. |
| `CLAUDE.md`, `spec/*.md`, `.claude/settings.json` | **project** | **Never overwritten.** These hold your gate baseline, owner decisions, backlog, and gotchas. |

`templates/` and `reference/` are read only at `/sdlc-setup` time and are never
re-applied to an already-adopted project — with one exception: `reference/REVIEW_LENSES.md`
is installed into `.claude/commands/` (so `/end-slice`'s pointer to it resolves after the
kit folder is gone) and tracks upstream like the commands. A kit release that changes only
the non-installed templates and reference docs is an adoption-only change — it affects new
adoptions, not yours. `CHANGELOG.md` marks each entry accordingly.

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

   > **Hash committed content, not the working tree.** The kit stores text as LF, but if
   > your project does not pin line endings (`.gitattributes`) and you are on Windows,
   > your checkout holds CRLF. Hashing those files directly reports **every file as
   > drifted** — the check appears to work and is uniformly wrong. `git cat-file -p :path`
   > reads the committed bytes, which are LF on every platform. This applies only to files
   > inside your repo; a downloaded release archive is already LF and verifies with plain
   > `sha256sum -c MANIFEST.sha256`.

   ```bash
   cd /path/to/your-project
   MAN=/tmp/kit-old/sdlc-kit/MANIFEST.sha256

   for f in $(git ls-files .claude/commands .claude/agents); do
     case "$f" in
       .claude/commands/*)
         base=${f#.claude/commands/}
         # commands/, skills/, and reference/REVIEW_LENSES.md all install into
         # .claude/commands/, so try all three prefixes.
         want=$(awk -v b="$base" \
           '$2 == "commands/" b || $2 == "skills/" b || $2 == "reference/" b {print $1}' "$MAN") ;;
       .claude/agents/*)
         base=${f#.claude/agents/}
         # agents/ installs into .claude/agents/ (mapping added in kit 0.6.0; an older
         # manifest has no agents/ entries, so these classify UNKNOWN — the denominator
         # below still counts them).
         want=$(awk -v b="$base" '$2 == "agents/" b {print $1}' "$MAN") ;;
     esac
     have=$(git cat-file -p ":$f" | sha256sum | cut -d' ' -f1)
     if   [ -z "$want" ];        then echo "UNKNOWN   $base  (not from the kit — yours)"
     elif [ "$want" = "$have" ]; then echo "UNCHANGED $base  (safe to overwrite)"
     else                             echo "DRIFTED   $base  (review the diff — your call)"
     fi
   done
   ```

   Two traps worth knowing, because both produce confident wrong answers rather than
   errors:

   - **Never write `git cat-file … | sha256sum` as the test of whether a path exists.** A
     pipeline reports the *last* command's status, so a missing path yields the hash of
     empty input and silently "matches" the wrong entry. Look the path up in the manifest,
     as above, rather than probing for it.
   - **Check the denominator.** The loop should report exactly as many files as
     `git ls-files .claude/commands .claude/agents | wc -l`. If it reports fewer, your
     prefix matching is dropping files — `tdd-references/` lives in a subdirectory and is
     the usual casualty.

4. **Act on the classification.**
   - `UNCHANGED` → provably untouched since adoption. Copy the new version over it.
   - `DRIFTED` → you or setup edited it. Diff it against both versions and decide, file
     by file. **Never auto-overwrite a drifted file** — `spec/SDLC.md` explicitly invites
     you to fix a command that disagrees with it, so drift is often deliberate.
   - `UNKNOWN` → not a kit file. Leave it alone.

   Then copy in any files **new in the target version's install set**. Classification
   never saw them — it enumerates what your project already holds, and your project does
   not hold them yet — so they appear in no category above and are the one class of
   update a purely classification-driven pass silently skips. Take the install set from
   the new version's `sdlc-kit/commands/sdlc-setup.md` (New mode step 5). The agent
   definitions (`agents/` → `.claude/agents/`, new in 0.6.0) arrive this way on any
   project updating from an older version.

   If you kept a `sdlc-kit/` folder from adoption, replace it with the new version's
   bundle — but **list its actual contents against the old version's manifest first**,
   and note both counts (N files on disk, M in the manifest), so an empty listing reads
   as the error it is rather than as a clean result.
   Anything in that folder the manifest does not list was put there by your project, and
   a wholesale replace deletes it silently — that is how one project lost its only local
   copy of an authored field report. Move any such file to a project-owned path (`spec/`
   is the usual home) before replacing. Left stale instead, the folder sits beside a
   re-stamped `spec/SDLC.md` claiming a version it does not hold.

   When you present (or read) the update's plan, count files whose *committed content*
   actually changes separately from files merely touched — line-ending churn on an
   unpinned checkout can make two dozen files report modified when four differ. The
   short list is the one to read closely; the long one is the noise deletions hide in.

5. **Touch nothing project-owned.** Do not let an update rewrite `spec/SDLC.md`,
   `spec/PROJECT_INDEX.md`, `spec/TESTING.md`, `CLAUDE.md`, or `.claude/settings.json`.
   They hold your recorded baseline and decisions; the kit cannot regenerate them.
   And claim only what was checked: "nothing project-owned touched" may be said once
   the final diff has been read against the ownership table — not asserted from the
   manifest, which structurally cannot see files it never listed. An unverified
   reassurance is worse than silence, because it stops the reader looking.

6. **Verify, then re-record the version.** Re-run step 3 against the **new** version's
   manifest: every file you copied must now classify `UNCHANGED`, and the only `DRIFTED`
   entries are files you chose to keep. The two runs disagreeing about the copied files
   is what proves the classifier discriminates — an all-clear it could not fail to
   produce proves nothing. Then re-record the version in `spec/SDLC.md`
   (*Kit version: X.Y.Z*, dated). From here every later update is mechanical.

7. **Land it as a normal PR** (`chore/update-sdlc-kit-X.Y.Z`) — the same way the adoption
   landed. Read `CHANGELOG.md` for the versions you skipped; entries marked
   *[installable]* are the ones that changed what you just copied.

### No version stamp (adopted before 0.2.0)

Manifests did not exist before 0.2.0, so there is no `MANIFEST.sha256` to compare against.
Hash the tag's contents directly instead — the result is exactly as provable, since the
manifest is only ever a cache of those same hashes.

Note that `v0.1.0` predates the repo restructure: its kit files live at `commands/` and
`skills/`, without the `sdlc-kit/` prefix that later versions use.

```bash
cd /path/to/your-project
KIT=/tmp/kit                       # a clone of the kit repo
OLD=v0.1.0                         # the version you believe you are on
PRE=""                             # use PRE=sdlc-kit/ for v0.2.0 and later

for f in $(git ls-files .claude/commands); do
  base=${f#.claude/commands/}
  want=""
  for cand in "${PRE}commands/$base" "${PRE}skills/$base" "${PRE}reference/$base"; do
    # -e tests existence and sets a real exit status; never probe with a pipeline.
    if git -C "$KIT" cat-file -e "$OLD:$cand" 2>/dev/null; then
      want=$(git -C "$KIT" cat-file -p "$OLD:$cand" | sha256sum | cut -d' ' -f1)
      break
    fi
  done
  have=$(git cat-file -p ":$f" | sha256sum | cut -d' ' -f1)
  if   [ -z "$want" ];        then echo "UNKNOWN   $base"
  elif [ "$want" = "$have" ]; then echo "UNCHANGED $base"
  else                             echo "DRIFTED   $base"
  fi
done
```

If every file matches a released version, you are provably on that version and step 3
applies unchanged from there. If they match nothing, treat every file as `DRIFTED` and
reconcile by hand — once. After this update you will have a version stamp and never need
this section again.

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
