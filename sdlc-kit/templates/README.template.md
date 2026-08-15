# {{PROJECT_NAME}}

{{PROJECT_ONE_LINER}}

<!-- Human entry point only — what this is, how to run it, where the real docs live.
     Process truth stays in the spec files linked below, never here; run detail longer
     than a command (interpreter paths, env vars, quirks) belongs in
     spec/PROJECT_INDEX.md's Environment gotchas. If this file and a spec file disagree,
     the spec file is right. -->

## Run

```
{{RUN_COMMAND}}          # start the app
{{STOP_COMMAND}}         # stop it (omit if closing the window/Ctrl+C suffices)
```

## Development

Development follows an agentic SDLC — phases → slices → TDD cycles, gated by lint +
typecheck + tests:

- [`spec/PROJECT_INDEX.md`](spec/PROJECT_INDEX.md) — current status and what to do next
- [`spec/SDLC.md`](spec/SDLC.md) — the process: the gate, the slice loop, the owner halts
- [`CLAUDE.md`](CLAUDE.md) — the instructions agent sessions load
