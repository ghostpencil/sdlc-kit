# The Agentic SDLC Kit — bundle

This folder is the kit itself: a language-agnostic software development lifecycle for
AI-assisted development with Claude Code, delivered as Claude Code prompt files. There is
no application code here and nothing to build.

Version: see `VERSION`. Full documentation, the field report, and the changelog live in
the kit's home repository: <https://github.com/ghostpencil/sdlc-kit>

---

## Install

1. Make sure this folder sits at the root of your project and is named `sdlc-kit` —
   `/sdlc-setup` looks for it by name.
2. Copy `commands/sdlc-setup.md` into your project's `.claude/commands/`.
3. Open Claude Code in your project and run **`/sdlc-setup`**.

Setup auto-detects **New Project** mode (interview → scaffold → establish a green gate)
or **Existing Project** mode (analyze → propose → confirm → generate, merging and never
overwriting), instantiates every template, installs the daily commands and the vendored
TDD skill set, and writes the edit-time gate hook.

After setup the daily loop is `/plan-phase` → `/next-slice` → `/end-slice` → `/end-phase`,
one slice per session, `/clear` between slices.

## What is in here

```
VERSION                  ← the kit version this bundle is
MANIFEST.sha256          ← checksums of every file below (see "Verifying" and "Updating")
commands/                ← installed into <project>/.claude/commands/
skills/                  ← vendored TDD skill set → <project>/.claude/commands/
templates/               ← instantiated into the project by /sdlc-setup
reference/               ← consulted by /sdlc-setup; REVIEW_LENSES.md is also installed
LICENSE                  ← MIT
THIRD_PARTY_NOTICES.md   ← attributions for the vendored skills (all MIT)
```

`commands/`, `skills/`, and the installed `reference/REVIEW_LENSES.md` are **kit-owned**:
they track upstream and an update may overwrite them when they are unmodified. Everything `/sdlc-setup` writes into your project
(`CLAUDE.md`, `spec/*.md`, `.claude/settings.json`) is **project-owned** and is never
overwritten by an update — it holds your recorded gate baseline, owner decisions, and
gotchas.

## Verifying this bundle

```bash
cd sdlc-kit && sha256sum -c MANIFEST.sha256      # shasum -a 256 -c on macOS
```

## Updating an already-adopted project

See the *Updating an adopted project* section of the home repository's README. The short
version: compare your installed `.claude/commands/*.md` against the `MANIFEST.sha256` of
the version you are currently on (recorded in your `spec/SDLC.md`). Files that match are
provably unmodified and safe to overwrite; files that differ are yours to reconcile.
