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
| `{{TEST_PATH_PATTERN}}` | case-pattern for test files; `\|`-separate alternatives | `tests/*\|test_*.py\|*_test.py` |
| `{{TEST_CMD_PATTERN}}` | case-pattern matching a test-suite invocation | `*pytest*` |

The last two belong to the TDD-ordering guards below and are asked for only when those
are installed. They are separate from `{{SOURCE_GLOB}}` for a measured reason: every
`SOURCE_GLOB` in this file is extension-only, so `*.py` matches `tests/test_x.py` as
readily as `src/x.py`. `SOURCE_GLOB` answers "should the edit hook fire," where matching
a test file is harmless; the guard needs the one question that pattern cannot answer, so
it tests `{{TEST_PATH_PATTERN}}` **first** and treats only the remainder as production.

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

### The hook's one dependency: a JSON parser

The hook is handed its payload as JSON and must read a file path out of it, so it needs
a real parser — hand-rolled `sed` extraction of JSON is how a check starts returning
confident wrong answers. Both hook dialects therefore **carry two implementations of
that parse, python and node, and choose between them at run time**:

```sh
JP=""; JN=""
for c in python python3; do command -v "$c" >/dev/null 2>&1 && { JP=$c; break; }; done
[ -z "$JP" ] && command -v node >/dev/null 2>&1 && JN=node
```

Three reasons it detects rather than being configured, each of which cost something to
learn:

1. **Only the hook's own shell can answer.** Ask the owner and they answer for the shell
   they type in; the hook runs somewhere else (see *The hook environment* below). A
   configured interpreter is a claim about the wrong environment, which is no claim at
   all.
2. **Neither interpreter is implied by the CLI.** Copilot CLI's own prerequisites are a
   subscription and, on Windows, PowerShell 6+; four of its five install methods are
   standalone binaries that bundle their runtime and expose no `node` on the `PATH`. So
   "they'll have node, it's a Node app" is false.
3. **Windows python writes CRLF.** `print()` emits `\r\n`, and a stray `\r` falsifies
   every downstream string comparison — `[ "$st" = "ok" ]` is false when `$st` is
   `ok\r`. Git Bash hides this because MSYS `sed` silently strips CR; WSL bash does not,
   and WSL exposes Windows `python.exe` through `PATH` interop. Both hook bodies pipe
   the interpreter's output through `tr -d '\r'` for that reason. Node writes LF
   everywhere and never had the problem.

**With neither interpreter present, both hooks say so on every edit** — `additionalContext`
on Copilot, stderr and exit 2 on Claude Code — rather than exiting quietly. That is the
same rule as everywhere else: a check that cannot run must not be indistinguishable from
one that passed.

`jq` is no longer suggested as a substitute. It was only ever a note telling an adopter
to hand-edit the body, it was never a shipped path, and it was never tested. The two
dialects that replace it need no editing and were both exercised by the 44-case pass
recorded under *Hook dialects* below.

## The hook environment — measure it, do not assume it

**A hook does not run in the shell you type in.** It runs in whatever shell the CLI
resolves, with that shell's `PATH`, that shell's idea of what a path looks like, and
that shell's view of whether the project's toolchain exists at all. None of that is
implied by the gate passing in your terminal, and a hook that cannot run its checks is
the silently-green gate this file's *timeout is a pass* warning is already about.

**Measured 2026-08-05, Copilot CLI 1.0.77 on Windows 11:** a hook's `bash` command
resolves against the **system** `PATH`, and on a Windows machine with WSL installed that
is WSL's bash (`system32\bash.exe`) — a Linux environment in which `D:\…` does not
exist, and in which the project's Windows-installed linter, type checker and test runner
are all absent. Both documented failure modes were observed in one run: a cold WSL start
blew the 10-second `timeoutSec` and **failed open** (the tool call proceeded unguarded),
and a warm run errored and, on `preToolUse`, **failed closed** (the call was denied).
Claude Code states its own answer instead of leaving it to `PATH` — its docs specify Git
Bash on Windows, with a per-hook `"shell"` key — so this is a Copilot-side hazard, not a
universal one.

**So setup measures it, before trusting either hook.** Run this from the CLI's own
session (`copilot -p '…'`, not from your terminal), which is the only place the answer is
authoritative:

```
bash -c 'echo "shell: $0"; uname -a; pwd; command -v python || command -v python3 || echo NO-PYTHON; command -v node || echo NO-NODE; ls "$PWD" >/dev/null 2>&1 && echo CWD-OK || echo CWD-UNREACHABLE'
```

Read three things off it, and record them in `spec/SDLC.md` beside the gate:

1. **Which shell answered** — `uname` naming WSL/Linux on a Windows project is the
   hazard above, and means the hooks are running somewhere the project does not exist.
2. **Whether `python` or `node` resolves there.** The hooks need one of the two to parse
   their payload, and they pick whichever is present at run time. Record which one *this
   shell* offers — not which one is installed on the machine, which is a different
   question with a different answer. Neither present is a real finding: the hooks will
   report it on every edit, which is honest but useless, so install one or accept that
   the edit-time check does not run here.
3. **Whether the project's own gate commands resolve there** — run the actual
   `{{HOOK_LINT_CMD}}`. A hook that finds its file and then cannot run the linter is
   the same silent pass by a different route.

If the answer is the WSL one, the honest options are to install the toolchain inside
that environment, or to accept that the Copilot-side hooks do not run on this machine
and say so in `spec/SDLC.md` — never to leave a hook installed that reads as enforcement
and checks nothing. The rule behind this is the one the kit applies everywhere else and
had never applied here: **a check must name the environment it runs in.** The process
verified the artifact and was silent about the environment the check itself would run
in.

**Adopters on 0.15.0 and earlier are affected and will not get this by updating.** The
instantiated hook is project-owned, so `/sdlc-update` never rewrites it; the fix reaches
an adopted project as a changelog entry the owner applies by hand.

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

**Verified 2026-08-05** against the instantiated body of both dialects, 44 cases —
every case run once under `python` and once under `node`, with `PATH` pinned to one at a
time, because a dialect that is never exercised is not a dialect that was proven. The
cases: `apply_patch`'s raw patch text, multi-file and delete-only patches, both payload
shapes (`toolArgs` and `tool_input`), absolute-Windows and repo-relative paths, a path
containing a space, a non-source file, a payload with no path, a missing file,
unparseable input, and neither interpreter present. Every silent case was also run
dirty, so silence means something. That is the negative-case proof for the recipe
itself; the per-project proof below is separate and still required. (The suite lives
with the kit's development tooling, not in the bundle — an adopter runs the per-project
proof, not this one.)

**Proving the hook in the project — a check is trusted only once it has been made to
fail.** Same standard as the Claude side:
edit a scratch source file with a deliberate lint error and confirm the hook reports it.
On Copilot this proof does double duty — it is also what catches a wrong `matcher`,
since a matcher that never fires and a clean file look identical. If the proof produces
nothing, run the tool-name discovery procedure in `reference/COPILOT.md` before
adjusting anything else, and check `copilot --version` against the version floor
recorded there.

---

## The TDD-ordering guards — optional, Copilot CLI only

The edit-time hook checks *what* was written. These two guards check **when**, and they
are the only mechanism in the kit that can refuse an action rather than comment on it:

- **G1, the observed-RED write guard** (`preToolUse`) — a write to a production source
  file is a violation unless a test file has been edited **in this session** and a
  **failing** test run has been observed since that edit. Both halves are required: a
  red alone proves nothing, since any test-shaped command that exits non-zero (a
  pattern matching no tests) manufactures one — found in the field on the first armed
  arc. The corollary: a **resumed** session must touch a test file before its first
  production write, because guard state is session-scoped.
- **G2, the premature-stop guard** (`agentStop`) — stopping is a violation while no
  green test run has been observed, or the latest observed run is red.

Templates: `templates/tdd-guard.template.sh` → `.github/hooks/sdlc-tdd-guard.sh`, and
`templates/tdd-guard.template.json` → `.github/hooks/sdlc-tdd-guard.json`. The JSON
carries no project values and no absolute path — it derives the repository root from the
payload's own `cwd`, translating path flavour, so the committed file works for every
clone of the repo rather than only the machine setup ran on. The script takes the three
placeholders below. State lives in `.git/sdlc-tdd/` (inside `.git`, so nothing to
gitignore) and is **session-scoped**: a red observed yesterday does not license a write
today. The guard reads its payload with the same dual python-or-node parser the gate
hooks use, detected the same way — so accepting the guards adds no dependency the gate
hook did not already impose. With neither interpreter present it writes `GUARD ERROR` to
its log and guards nothing: **the script never denies on its own failure**, because a
guard that blocks work because it is broken is worse than no guard at all.

That promise covers the script, and it stops where the script does. If the *hook* fails
before the script runs — a missing shell, a cold WSL start blowing `timeoutSec` — the
CLI decides, and this file has measured that decision going both ways on the same
machine: fail-open on timeout, and **fail-closed (the call denied) on a `preToolUse`
command error**. G1 is a `preToolUse` hook, so in that environment a broken hook can
deny a write no matter what the script would have done. That is the strongest argument
for the logging ramp: it exercises the whole path, not just the script, before anything
is armed. If denials appear in a session whose `guard.log` shows nothing, suspect the
hook layer and re-read *The hook environment* above.

| Language | `{{TEST_PATH_PATTERN}}` | `{{TEST_CMD_PATTERN}}` |
|---|---|---|
| Python | `tests/*\|test_*.py\|*_test.py` | `*pytest*` |
| TS / JS | `test/*\|tests/*\|*.test.*\|*.spec.*` | `*jest*\|*vitest*\|*npm*test*` |
| C# / .NET | `*Tests/*\|*Test.cs\|*Tests.cs` | `*dotnet*test*` |
| Go | `*_test.go` | `*go*test*` |
| Java | `src/test/*\|*Test.java\|*Tests.java` | `*mvn*test*\|*gradlew*test*` |
| Rust | `tests/*\|*_test.rs` | `*cargo*test*` |

**Key the command pattern on the test runner, never on a filename.** The bench version
matched `node test…` as adjacent words and was blind to `node .\test-x.js`, because the
`.\` prefix sat between them. Wildcards spanning the runner and the word `test`
(`*node*test*`) match every invocation form; a pattern anchored on a path does not.

**The ramp is not optional.** The guards install in **logging mode**, where they write to
`.git/sdlc-tdd/guard.log` and never deny. Deny is armed by creating the flag file
`.git/sdlc-tdd/deny-enabled` and disarmed by deleting it. Read a few real sessions of the
log first and confirm the guard is recognising the project's own test runs: a guard that
does not see your test command will, the moment deny is armed, block every production
write in the repo. This ordering was pre-registered on the bench and it earned its
keep — the deny ramp found a defect (a compound test command reporting the wrong exit
code, recording a **false green**) that logging mode had not surfaced.

**Prove both guards the way the kit proves every check — by making them fail.** In a
scratch session: write a production source file without a failing test first, and confirm
the log names it; then finish the session with no green run, and confirm the stop guard
logs a would-block. If nothing appears, the guard is not firing — check the tool-name
matcher against `reference/COPILOT.md`'s discovery procedure and the hook environment
above, and do not arm deny until the log speaks.

**What these guards are not.** A cooperative backstop, not a security boundary, and the
generated `spec/SDLC.md` must say so: writes made through the shell tool are invisible to
G1, and a session can read the guard's own source and state. On the bench a session did
exactly that — it read the script to learn the recognised command format. It complied,
but it could as easily have touched the state files. Two more honest limits: G2 accepts
any green test run rather than a full gate run, and a session that satisfies the guard
can still delete the test afterwards — which is why the evidence lines in the slice
commit body, not the guard, are what make TDD ordering auditable after the fact.

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
