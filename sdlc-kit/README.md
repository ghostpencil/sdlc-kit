# The Agentic SDLC Kit — bundle

This folder is the kit itself: a language-agnostic software development lifecycle for
AI-assisted development with Claude Code or GitHub Copilot CLI, delivered as prompt
files. There is no application code here and nothing to build.

Version: see `VERSION`. Full documentation, the field report, and the changelog live in
the kit's home repository: <https://github.com/ghostpencil/sdlc-kit>

---

## Install

Prerequisites: an agent CLI — Claude Code (CLI, desktop app, or IDE extension) or GitHub
Copilot CLI 1.0.63 or newer — plus `git`, and — for the verify and update scripts — a
POSIX shell with `sha256sum` (standard on Linux, `shasum -a 256` on macOS, Git Bash on
Windows).

1. Make sure this folder sits at the root of your project and is named `sdlc-kit` —
   `/sdlc-setup` looks for it by name.
2. Install `sdlc-setup` by hand. It is the only one: setup installs the other six
   commands itself, but it cannot install its own entry point.
   - **Claude Code:** copy `commands/sdlc-setup.md` into your project's
     `.claude/commands/`.
   - **Copilot CLI:** write `.github/skills/sdlc-setup/SKILL.md` — a `---` block
     carrying `name: sdlc-setup` and a **quoted** one-line `description`, then one blank
     line, then `commands/sdlc-setup.md` byte-for-byte. Copilot reads no
     `.claude/commands/` and has no markdown slash commands. Keeping the body unchanged
     is what lets `/sdlc-update` recognize the file later; quoting the description is
     what stops an unquoted `: ` from making Copilot drop it silently.
     `reference/COPILOT.md` has the mapping for every other file.
3. Open your CLI in the project and run **`/sdlc-setup`** — on Copilot, confirm
   `/skills` lists it under *Project skills* first, since a frontmatter error is silent.

Setup auto-detects **New Project** mode (interview → scaffold → establish a green gate)
or **Existing Project** mode (analyze → propose → confirm → generate, merging and never
overwriting), instantiates every template, installs the daily commands and the eight
skills (five vendored, three kit-written), and writes the edit-time gate hook.

After setup the daily loop is `/plan-phase` → `/next-slice` → `/end-slice` → `/end-phase`,
one slice per session, `/clear` between slices.

## What is in here

```
VERSION                  ← the kit version this bundle is
MANIFEST.sha256          ← checksums of every file below (see "Verifying" and "Updating")
commands/                ← installed into <project>/.claude/commands/
                           (Copilot CLI: .github/skills/<name>/SKILL.md)
skills/                  ← TDD skill set + the three kit-written passes
                           (diff-review, change-simplify, change-verify)
                           → <project>/.claude/skills/
                           (one directory per skill; both CLIs read that path)
templates/               ← instantiated into the project by /sdlc-setup
reference/               ← consulted by /sdlc-setup; REVIEW_LENSES.md is also installed
LICENSE                  ← MIT
THIRD_PARTY_NOTICES.md   ← attributions for the vendored skills (all MIT)
```

`commands/`, `skills/`, and the installed `reference/REVIEW_LENSES.md` are
**kit-owned**:
they track upstream and an update may overwrite them when they are unmodified. Everything `/sdlc-setup` writes into your project
(`CLAUDE.md`, `spec/*.md`, `.claude/settings.json`) is **project-owned** and is never
overwritten by an update — it holds your recorded gate baseline, owner decisions, and
gotchas.

## Verifying this bundle

```bash
cd sdlc-kit && sha256sum -c MANIFEST.sha256      # shasum -a 256 -c on macOS
```

## Updating an already-adopted project

Run `/sdlc-update` in the adopted project (setup installs it alongside the daily
commands), or see the *Updating an adopted project* section of the home repository's
README — both state the same procedure. The short version: compare your installed
`.claude/commands/*.md` and `.claude/skills/*/SKILL.md` (plus `.github/skills/` and
`.github/agents/` on a Copilot CLI project, and `.claude/agents/*.md` on kits
0.6.0–0.9.0) against the
`MANIFEST.sha256` of the version you are currently
on (recorded in your `spec/SDLC.md`). Files that match are provably unmodified and safe
to overwrite; files that differ are yours to reconcile.
