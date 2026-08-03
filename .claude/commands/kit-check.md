# Kit Check

Verify this repository against the invariant ledger in `KIT_INVARIANTS.md`. This is an
agent **reading pass**, not a grep suite: most invariants are semantic — a false project
fact in command prose, a placeholder asked for in different words than its name, a
pointer to a section that exists in the kit repo but not in an adopted project — and
pattern matching has been tried against them and failed (the literal placeholder
name-match produced 24 false positives out of 32). The greppable minority run as
commands inside the pass. This command is kit-development tooling; `/sdlc-setup` never
installs it.

Prime directive: **an all-clear from a check that cannot fail proves nothing.** For
every invariant, report not just the verdict but what a violation would have looked
like — each ledger entry's specimen is that statement. Run the full pass before cutting
any release.

## How to use

`/kit-check` — full pass. `/kit-check 5 7` — scope to specific ledger entries, e.g.
after an edit that only moved pointers. A scoped run must say what it skipped.

## Workflow

### 1. Load the ledger

Read `KIT_INVARIANTS.md` (canonical — it wins over any summary) and root `CLAUDE.md`.
The numbering below is the ledger's.

### 2. Mechanical checks first

Run these as commands; each states its negative case in the ledger.

- **9 — README tree:** `git ls-files` versus the root README's file tree. Every tracked
  file appears (directory-level entries like `tdd-references/` cover their contents);
  every tree entry exists on disk.
- **10 — manifest:** recompute SHA-256 from committed content
  (`git cat-file -p :sdlc-kit/<path>`) for every bundle file; diff against
  `MANIFEST.sha256`. Entry count must equal `git ls-files sdlc-kit | wc -l` minus one
  (the manifest itself). Report the denominator, not just "matches".
- **4 — `{{` census:** `grep -rc '{{' sdlc-kit/commands sdlc-kit/skills
  sdlc-kit/reference/REVIEW_LENSES.md` → hits in `sdlc-setup.md` only,
  and setup's close-out check names exactly `CLAUDE.md spec/ .claude/settings.json`.
- **6 — step references:** `grep -nE 'step [0-9]' sdlc-kit/commands/*.md`, then read
  each referenced step and confirm it is the one the sentence means.

### 3. Reading passes

For each, read the named files in full — do not sample — and cite evidence per verdict.

- **1 — no project facts:** every declarative sentence in `commands/*.md`
  that could be false for *some* adopting project (a baseline state, a
  stack, a number, a tool) is a finding. Commands may only point at where the project
  records the fact.
- **2 — no contradiction with `SDLC.template.md`:** compare each command's process
  claims (gate, halt points, baseline handling, bookkeeping) against the template; also
  the mirror — any rule a command enforces must appear in the template.
- **3 — placeholder mapping:** enumerate every `{{PLACEHOLDER}}` in `templates/` and
  `reference/GATE_RECIPES.md`; for each, name the `sdlc-setup.md` step or interview
  round that resolves it, matching **semantically**. Unresolvable → finding; a setup
  question with no placeholder to fill is worth a note.
- **5 — pointers resolve post-setup:** enumerate file-and-section pointers in installed
  files (`commands/`, `skills/`, `reference/REVIEW_LENSES.md`); verify each
  target exists in what setup installs or instantiates, not merely in this repo.
- **7 — install mapping:** take `sdlc-setup.md`'s install list (New mode step 5) as the
  definition; verify every derived statement against it — both READMEs, root
  `CLAUDE.md`'s flow diagram, `sdlc-update.md`'s table, `reference/COPILOT.md`'s mapping
  table, and the prefix lists in **both**
  classification scripts, including their denominator checks (`.claude/agents/` stays
  enumerated there for the 0.6.0–0.9.0 transition, though the mapping is retired).
  The definition is now per-CLI: verify each derived statement against the column that
  applies to it, and treat a statement that names one CLI's path as universal as a
  finding.
- **8 — update procedure agrees:** `sdlc-update.md` beside the root README's *Updating
  an adopted project*: same classification rules, same ownership table, same traps.
- **11 — vendored provenance:** each `skills/` file matches `reference/SKILLS.md`'s
  verification claims, or its divergence is documented there.
- **12 — bundle purity:** scan `git ls-files sdlc-kit` for anything an adopter should
  not receive.
- **13 — negative cases:** every check the kit specifies (isolation harness spec, hook
  verification, exit checks, update classifier, release workflow, this command) states
  how it is proven to fail.
- **14 — recorded values name their enforcement:** enumerate every step in `commands/`
  and `templates/` that records a value or state (floors, baselines, statuses, deploy
  outcomes); each names the artifact that enforces or evidences it and the step that
  reconciles the two, or is explicitly claim-only.
- **15 — verification names its environment:** enumerate every verification verb in
  `commands/` and `templates/` (verify, confirm, check, prove, accept, ratify, and
  "green"); each names where the check runs and whether that place is what the claim is
  about — production configuration for a claim about production, the owner's shell for
  a command the owner types, the run that produced a number. An unqualified "verified"
  over a claim whose truth is environment-dependent is the finding.

### 4. Report

One table: invariant / verdict (**pass** / **finding** / **skipped**) / evidence — where
a pass's evidence includes the violation it looked for and did not find. Findings are
fixed as ordinary edits in the session (or recorded in `IMPROVEMENT_PLAN.md` if larger);
this command itself changes nothing.
