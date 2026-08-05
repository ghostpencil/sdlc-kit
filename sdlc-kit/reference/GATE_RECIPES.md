# Gate & Hook Recipes

Per-language commands for the two places tooling is configured during `/sdlc-setup`:

1. **The gate** (`spec/SDLC.md`) — lint, typecheck, full test suite; run at every
   `/end-slice` and `/end-phase`.
2. **The edit-time hook** — the same lint/typecheck run on the single file just edited,
   so failures surface immediately. Two dialects, one per target CLI: Claude Code's
   (`.claude/settings.json`, from `templates/settings.template.json`) and Copilot CLI's
   (`.github/hooks/sdlc-gate.json`, from `templates/copilot-hook.template.json`). The
   owner confirms the target CLI at setup; *Hook dialects* below states what differs.

A third section, *Runtime-standards rules*, lists per-linter rule sets for the
runtime-conventions interview — those land inside the linter's own config, so both
places above enforce them without a new command.

These are starting points. Always prefer the commands the project **already uses**
(check CI workflows, `Makefile`, `package.json` scripts) over these defaults — the gate
must match CI, or the gate lies. That includes security checks CI already runs
(dependency audit, secret scan, static analysis): fast ones join the local gate; slow
or credentialed ones stay CI-only but are listed in the gate section of `spec/SDLC.md`
so merge readiness includes them knowingly — the same placement logic as the coverage
floor below, enforced in CI and recorded locally.

## Hook template placeholders

| Placeholder | Meaning | Example (Python) |
|---|---|---|
| `{{SOURCE_GLOB}}` | case-pattern for source files; `\|`-separate alternatives | `*.py` |
| `{{HOOK_LINT_CMD}}` | lints the single file `$f` | `python -m ruff check "$f"` |
| `{{HOOK_TYPECHECK_BLOCK}}` | optional typecheck of `$f`, often scoped to the app dir | see below |
| `{{HOOK_STATUS_MESSAGE}}` | spinner text (Claude Code hook only) | `ruff + mypy on edited file` |
| `{{HOOK_CONFIG_PATH}}` | where the hook is configured, named in the generated prose | `.claude/settings.json` |
| `{{HOOK_FEEDBACK_NOTE}}` | what this CLI's hook feedback does — see *Hook dialects* | `its feedback is blocking — fix it before moving on.` |

`{{HOOK_TYPECHECK_BLOCK}}` is a bash fragment ending in `;` that sets `t` (output) and
`trc` (exit code). To scope it to application code only (skip tests/tools):

```bash
case "$f" in *<app_dir>*) t=$(<typecheck cmd> "$f" 2>&1); trc=$? ;; esac;
```

If the language has no separate typecheck step, replace the whole block with a single
space and leave `trc=0`.

The instantiated `CLAUDE.md` restates the same facts in prose (`{{HOOK_TOOLS}}`,
`{{SOURCE_EXT}}`); resolve both from this table's values, so the prose and the hook
cannot disagree. `{{HOOK_CONFIG_PATH}}` and `{{HOOK_FEEDBACK_NOTE}}` appear in both
`CLAUDE.template.md` and `SDLC.template.md` and are resolved from the dialect below —
the same value in both files.

Note: the hook's file-path extraction uses `python -c` for JSON parsing. On machines
without Python, substitute `jq`: `f=$(jq -r '.tool_input.file_path // empty' 2>/dev/null)`.
Python is the default deliberately — it is the more commonly present of the two (the
machine this kit is developed on has Python and no `jq`).

---

## Hook dialects

The per-language lint and typecheck commands below are CLI-neutral; only the hook's
wrapper differs. Resolve the same `{{HOOK_*}}` placeholders either way.

| | Claude Code | Copilot CLI |
|---|---|---|
| Template | `templates/settings.template.json` | `templates/copilot-hook.template.json` |
| Instantiates to | `.claude/settings.json` | `.github/hooks/sdlc-gate.json` |
| Event | `PostToolUse` | `postToolUse` |
| Matcher | `Edit\|Write` (substring) | `edit\|create\|apply_patch` (anchored `^(?:…)$`) |
| Failure channel | stderr + `exit 2` | JSON `additionalContext` on stdout |
| Timeout key | `"timeout": 120` (ms-free seconds) | `"timeoutSec": 120` |
| `{{HOOK_STATUS_MESSAGE}}` | used | no such key — the placeholder does not occur in the Copilot template, so it is not asked for on that path |

**Copilot specifics, each of which changed the recipe** (full evidence and dates in
`reference/COPILOT.md`):

- **It cannot block.** `postToolUse` returns `modifiedResult` or `additionalContext`
  and nothing else; the text is injected as a prepended user message. Resolve
  `{{HOOK_FEEDBACK_NOTE}}` accordingly — *advisory*, not blocking. Claude Code's exit-2
  stderr is also advice to the model, so the gate is no weaker; the generated files just
  may not claim a stop that does not happen.
- **A timeout is a pass.** The documented default is 30 seconds and a timed-out hook
  surfaces a warning and lets the tool call proceed — a silently green gate: a check
  that stops checking without saying where it stopped. The template ships `timeoutSec: 120` to match the
  Claude-side value; **setup must time one real hook run during the verification below
  and raise the number to at least 3× what it measured**, then state the measured basis
  in `spec/SDLC.md` alongside the timeout-reads-as-a-pass warning.
- **It reports loudly when it cannot do its job.** The tool vocabulary and the field of
  `toolArgs` holding the edited path are under-documented upstream, so the body tries
  the plausible keys and, when none matches — or when the file cannot be found from the
  hook's working directory — emits `additionalContext` saying the gate did **not** run.
  A hook that quietly exits 0 because it could not find its file is indistinguishable
  from a clean edit; that is the whole hazard.
- **`toolArgs` arrives as a JSON-encoded string**, not an object, so it is parsed in two
  steps. The body accepts the camelCase payload (`toolArgs`, `cwd`) and the VS Code
  compatible one (`tool_input`), because both are documented and which one arrives is
  not stated.
- **Output is capped at 8000 characters** — the documented cap is 10 KB across all
  returning hooks — and decoded with `errors='replace'`, because a Windows locale codec
  mangles any non-ASCII in lint output on the way through. For the same reason the
  hook's own messages are ASCII only.

**Verified 2026-08-03** against the instantiated body, six cases: both payload dialects
with a failing linter (loud), a non-source file (silent), a clean source file (silent),
a payload with no path (loud), a path whose file is missing (loud), and unparseable
input (loud). That is the negative-case proof for the recipe itself; the per-project
proof below is separate and still required.

**Proving the hook in the project — a check is trusted only once it has been made to
fail.** Same standard as the Claude side:
edit a scratch source file with a deliberate lint error and confirm the hook reports it.
On Copilot this proof does double duty — it is also what catches a wrong `matcher`,
since a matcher that never fires and a clean file look identical. If the proof produces
nothing, run the tool-name discovery procedure in `reference/COPILOT.md` before
adjusting anything else, and check `copilot --version` against the version floor
recorded there.

---

## Python

```
python -m ruff check .            # lint
python -m mypy <package>          # typecheck (strict; keep the baseline green)
python -m pytest -q               # tests
```

Hook: `SOURCE_GLOB` = `*.py`; lint = `python -m ruff check "$f"`;
typecheck block = `case "$f" in *<package>*) m=$(python -m mypy "$f" 2>&1); trc=$? ;; esac;`

## TypeScript / JavaScript (Node)

```
npx eslint .                      # lint
npx tsc --noEmit                  # typecheck (omit for plain JS)
npm test                          # tests (vitest/jest — whatever package.json says)
```

Hook: `SOURCE_GLOB` = `*.ts|*.tsx|*.js|*.jsx`; lint = `npx eslint "$f"`;
typecheck: per-file `tsc` is unreliable — run project-wide `npx tsc --noEmit` in the
block if the project is small, otherwise leave typecheck to the gate.

## C# / .NET

```
dotnet format --verify-no-changes         # lint/format
dotnet build --nologo -warnaserror        # compile = typecheck
dotnet test --nologo                      # tests
```

Hook: `SOURCE_GLOB` = `*.cs`; lint = `dotnet format --verify-no-changes --include "$f"`;
typecheck: leave to the gate (per-file compile isn't meaningful).

## Go

```
golangci-lint run ./...           # lint (or: go vet ./...)
go build ./...                    # compile = typecheck
go test ./...                     # tests
```

Hook: `SOURCE_GLOB` = `*.go`; lint = `golangci-lint run "$f"` (or `gofmt -l "$f"` +
`go vet` on the file's package).

## Java (Maven / Gradle)

```
mvn -q checkstyle:check           # lint            (gradle: ./gradlew checkstyleMain)
mvn -q compile                    # compile = typecheck (gradle: ./gradlew compileJava)
mvn -q test                       # tests           (gradle: ./gradlew test)
```

Hook: `SOURCE_GLOB` = `*.java`; per-file tooling is weak — a compile-only hook via the
build tool is usually too slow; consider lint-only (`checkstyle -c config "$f"`) or no
hook, relying on the gate.

## Rust

```
cargo clippy --all-targets -- -D warnings   # lint
cargo check                                  # typecheck
cargo test                                   # tests
```

Hook: `SOURCE_GLOB` = `*.rs`; per-file clippy isn't supported — use `cargo clippy` on
the whole crate if it's fast, otherwise rely on the gate.

---

## Runtime-standards rules (logging, error handling, secure coding)

Mechanical enforcement for the conventions recorded in the project's `CLAUDE.md`
*Runtime Conventions* section: where the linter can state the rule, the rule goes in
the **linter's own config**, so the gate and the edit-time hook enforce it with no new
command. The match-reality rule above applies here too: check what the project's
linter config already enables before proposing anything, and on an existing project
measure each proposed rule's current violation count first — the owner adopts a rule
knowing its cost, and the violations a newly adopted rule surfaces land in the
recorded gate baseline, never in a setup-time fix spree.

Starting points per linter (rule IDs current at kit release; IDs drift — the linter's
own docs win over this table):

- **Python (ruff):** `E722` (bare `except`), `BLE001` (blind `except Exception`),
  `B904` (`raise … from` inside handlers), `T201`/`T203` (stray `print`), and the `S`
  family (bandit: hardcoded credentials S105–S107, `pickle` S301, shell/SQL injection
  S602–S609). Exempt tests via `per-file-ignores` (`tests/*: S101, T201`) rather than
  weakening a rule globally.
- **TypeScript / JavaScript (eslint):** `no-console` (or scope the allowed methods),
  `no-empty` (flags an empty `catch`), `no-eval` / `no-implied-eval` / `no-new-func`;
  with typed linting, `@typescript-eslint/no-floating-promises` — an unawaited promise
  is the ecosystem's bare except.
- **C# (.NET analyzers):** `<AnalysisLevel>latest-recommended</AnalysisLevel>` in the
  project file, plus explicit severities in `.editorconfig` for the rules that set
  leaves off — `dotnet_diagnostic.CA1031.severity = warning` (catch-general-
  exceptions) is the one to name; the gate's `-warnaserror` promotes them to failures.
- **Go (golangci-lint):** `errcheck` is on by default — keep it on; enable `gosec`;
  `forbidigo` for stray `fmt.Print*`.
- **Java:** checkstyle `EmptyCatchBlock` + `IllegalCatch`; where the project already
  runs SpotBugs, add `find-sec-bugs`.
- **Rust (clippy):** promote the allow-by-default `unwrap_used`, `expect_used`, and
  `print_stdout` for library code (tests and bins as the project decides); the gate's
  `-D warnings` makes them binding.

Prove the adopted set the way the hook is proven: one deliberate violation (a bare
`except:`, a stray `print`) must fail the lint run before the rules are trusted — a
rule proposed and never seen to fire is configuration that reads as enforcement.

---

## Coverage

Keep the floor in CI, not in the local gate — local runs stay fast, CI stays
authoritative. Record the current figure in the gate section of `spec/SDLC.md`
(`{{COVERAGE_FLOOR}}`, `TBD from first CI run` until one exists) so sessions know it
without reading CI config.

**Never compute the floor, and never carry one over from another project.** *A remembered
constant is not a measurement.* An aspirational floor fails every build from day one and
gets switched off within a week, which is strictly worse than having none: it trains the
team to route around the gate.

The procedure:

1. Ship without a floor. Let CI run and report coverage.
2. Set the floor from the **first green CI run**, just below the observed figure — using
   CI's *exact* invocation. Scoping flags matter: on one project the same suite reported
   figures 9 points apart depending on what was included, so a floor copied from a local
   run would have been meaningless.
3. It only ever raises. Lowering the floor to make a build pass defeats its only purpose;
   if a change drops coverage, that is the finding.

Existing coverage debt is a backlog item, not a merge blocker. Adopting a project at 34%
means the floor starts near 34%.

Two environments disagreeing about coverage is itself a finding — find out why before
adjusting the threshold. The gap is a symptom, not the disease.

## No tooling at all?

If the project has no linter/test runner yet (New Project mode), setting them up IS the
first act of `/sdlc-setup` — a gate that runs green on an empty project is the walking
skeleton everything else builds on. Never defer "we'll add tests later"; the process
does not work without the gate.
