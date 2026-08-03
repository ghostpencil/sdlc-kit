# {{PROJECT_NAME}} — Agent Instructions

You are implementing **{{PROJECT_NAME}}**: {{PROJECT_ONE_LINER}}.

Language: {{LANGUAGE_AND_VERSION}}. Application type: {{APP_TYPE}}.

---

# Core Rule — Minimize Context

Do NOT load all spec files.

At start, read only:
- CLAUDE.md
- spec/PROJECT_INDEX.md

Load other files only when needed.

---

# SDLC

The development process (phases → slices → TDD, owner halt points, the Gate) is defined
in `spec/SDLC.md`. Session commands that drive it:

- `/plan-phase` — plan the next phase (requirements interrogation + adversarial gap
  analysis, then a build-ready spec with slices)
- `/next-slice` — start a slice in a fresh session (orient, confirm scope, branch, TDD)
- `/end-slice` — close a slice (gate, code review, mutation check, commit,
  PROJECT_INDEX, then `/clear`)
- `/end-phase` — close a phase (gate, owner acceptance review, PR, whole-arc review,
  merge, deploy question + recorded outcome)
- `/sdlc-retro` — extract lessons from a finished phase (project facts to this project's
  files; process findings to a report you decide whether to send upstream)

An edit-time hook ({{HOOK_CONFIG_PATH}}) runs {{HOOK_TOOLS}} on every edited
{{SOURCE_EXT}} file. {{HOOK_FEEDBACK_NOTE}}

---

# Phase Discipline

Phase and status are in spec/PROJECT_INDEX.md.

## If STABILIZATION
- Do not move to next phase
- No new features
- No architecture changes
- Only:
    - bug fixes
    - behavior fixes
    - UI fixes
    - test fixes
    - spec alignment

If unsure → ask

## If BUILD
- Work only within current phase
- Do not skip ahead

---

# Always-Active Rules

- TDD required (tests first)
- Small steps only (one behavior)
- No new libraries without approval
- {{LANGUAGE_AND_VERSION}}
{{PROJECT_SPECIFIC_RULES}}
<!-- Examples of project-specific rules worth adding here:
     - portability rules (no OS-specific paths)
     - serialization conventions (human-readable JSON, schema versions)
     - dependency-injection seams for external services (LLMs, APIs, clocks)
     - threading / async ownership rules -->

---

# Runtime Conventions

How this project's code logs and fails. Recorded at setup — owner-answered (New
Project) or discovered from the code and confirmed (Existing). Enforcement: the linter
rules named below run in the gate and the edit-time hook; the *logging and swallowed
errors*, *untrusted input*, and *secrets and exposure* lenses in
`.claude/commands/REVIEW_LENSES.md` cover what no rule can state. A convention changed
here without its linter rule is a claim, not a control — change both together.

- **Logging:** {{LOGGING_CONVENTIONS}}
- **Error handling:** {{ERROR_CONVENTIONS}}
<!-- Each bullet names: the framework or mechanism; the level or wrapping policy (what
     ERROR means here, where errors are wrapped, whether blind catches are ever
     acceptable and where); what may never appear (secrets, PII in logs; bare excepts);
     and which parts are mechanically enforced (linter rule IDs) versus review-only. -->

---

# Skills

## TDD Skill

When writing tests for a new phase or new feature, use the installed TDD skill
(`tdd` — installed project-scoped by `/sdlc-setup`, versioned with this repo).

**Before invoking the TDD skill, read `spec/TESTING.md`.** It defines the mock
policy, the integration vs. unit boundary, and the per-cycle checklist. Do not
rely on memory — load it fresh each time.

Use the TDD skill before:
- creating a new test file
- adding tests for a new module
- starting a new phase
- defining test strategy

Do not write phase tests from memory if the TDD skill applies.

For bug fixes during STABILIZATION:
- use the TDD skill only if adding or changing tests
- otherwise keep the fix minimal

---

## Commands

```
{{RUN_COMMAND}}          # start the app manually
{{STOP_COMMAND}}         # stop it (omit if closing the window/Ctrl+C suffices)
```

---

# Spec Loading Rules

Load a spec file ONLY for its trigger. If you open a spec, say which one.

| File | Load only when |
|---|---|
| `spec/SDLC.md` | process questions; a session command seems to conflict with process |
| `spec/TESTING.md` | invoking the TDD skill (always read first); writing/modifying tests |
| `spec/PHASE_NN_*.md` | working the current phase (pointer in PROJECT_INDEX) |
{{EXTRA_SPEC_ROWS}}
<!-- As the project grows, add one row per new spec (ARCHITECTURE.md, DATA_MODEL.md,
     UI_SPEC.md, …) with a precise trigger. Precise triggers are what keep context small. -->

- If spec conflicts with request → ask for override

---

# Workflow (TDD)

For each task:

1. Write failing test
2. Implement minimal code
3. Refactor
4. Repeat

No large batches.

---

# Output Rules

- Keep code minimal
- No unrelated changes
- No future features
- No assumptions
