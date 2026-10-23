# Gate & Hook Recipes

Per-language commands for the two places tooling is configured during `/sdlc-setup`:

1. **The gate** (`spec/SDLC.md`) — lint, typecheck, full test suite; run at every
   `/end-slice` and `/end-phase`.
2. **The edit-time hook** — the same lint/typecheck run on the single file just edited,
   so failures surface immediately. Two dialects, one per target CLI, both split the
   same way — logic in a script file, a bare launcher line in the config: Claude
   Code's pair (`.github/hooks/sdlc-gate-claude.sh` holding the logic, from
   `templates/claude-gate.template.sh`, launched by the `Edit|Write` block in
   `.claude/settings.json`, from `templates/settings.template.json`) and Copilot
   CLI's pair (`.github/hooks/sdlc-gate.sh` holding the logic, from
   `templates/copilot-hook.template.sh`, plus `sdlc-gate.json` as its bare launcher,
   from `templates/copilot-hook.template.json`). The Copilot split (2026-08-07)
   exists because nothing rich survives the WSL launcher boundary; the Claude split
   (2026-08-15) because the per-hook `"shell"` pin its inline body depended on was
   measured never firing — both in *the hook environment* below. The
   owner confirms the target CLI at setup; *Hook dialects* below states what differs.

A third section, *Runtime-standards rules*, lists per-linter rule sets for the
runtime-conventions interview — those land inside the linter's own config, so both
places above enforce them without a new command. It closes with *The lens↔rule
map*: which half of each review lens those rules already decide, and which half no
rule in any of the six languages can express.

These are starting points. Always prefer the commands the project **already uses**
(check CI workflows, `Makefile`, `package.json` scripts) over these defaults — the gate
must match CI, or the gate lies. That includes security checks CI already runs
(dependency audit, secret scan, static analysis): fast ones join the local gate; slow
or credentialed ones stay CI-only but are listed in `spec/SDLC.md` (*Records*, beside
the gate) so merge readiness includes them knowingly — the same placement logic as the
coverage floor below, enforced in CI and recorded locally.

## Hook template placeholders

| Placeholder | Meaning | Example (Python) |
|---|---|---|
| `{{SOURCE_GLOB}}` | case-pattern for source files; `\|`-separate alternatives | `*.py` |
| `{{HOOK_LINT_CMD}}` | lints the single file `$f`, plus its format check where the gate formats | `python -m ruff check "$f"` |
| `{{HOOK_TYPECHECK_BLOCK}}` | optional typecheck of `$f`, often scoped to the app dir | see below |
| `{{HOOK_STATUS_MESSAGE}}` | spinner text (Claude Code hook only) | `ruff + mypy on edited file` |
| `{{HOOK_CONFIG_PATH}}` | where the hook is configured, named in the generated prose | `.claude/settings.json` |
| `{{HOOK_FEEDBACK_NOTE}}` | what this CLI's hook feedback does — see *Hook dialects* | `its feedback is blocking — fix it before moving on.` |
| `{{TEST_PATH_PATTERN}}` | case-pattern for test files; `\|`-separate alternatives | `tests/*\|test_*.py\|*_test.py` |
| `{{TEST_CMD_PATTERN}}` | case-pattern matching a test-suite invocation | `*pytest*` |
| `{{TEST_REPORT_PATTERN}}` | regular expression found in the runner's own failure report | `=+ (FAILURES\|ERRORS) =+` |
| `{{GUARD_EXEMPT_PATTERN}}` | case-pattern for repo-relative paths that are neither production nor tests; never empty | `*.config.*\|.*\|tools/*` |

The last four belong to the TDD-ordering guards below and are asked for only when those
are installed. They are separate from `{{SOURCE_GLOB}}` for a measured reason: every
`SOURCE_GLOB` in this file is extension-only, so `*.py` matches `tests/test_x.py` as
readily as `src/x.py`. `SOURCE_GLOB` answers "should the edit hook fire," where matching
a test file is harmless; the guard needs the one question that pattern cannot answer, so
it tests `{{TEST_PATH_PATTERN}}` **first** and treats only the remainder as production —
after `{{GUARD_EXEMPT_PATTERN}}` has taken out what is neither (*Code is `SOURCE_GLOB`
minus the exempt pattern*, below).

`{{HOOK_TYPECHECK_BLOCK}}` is a bash fragment ending in `;` that sets `t` (output) and
`trc` (exit code), and may set `tn` (a non-blocking note, below). It may read `$f` (the
file as the hook found it) and `$r` (the same file, repo-relative, `/`-separated), and
runs from the project root. To scope it to application code only (skip tests/tools):

```bash
case "$f" in *<app_dir>*) t=$(<typecheck cmd> "$f" 2>&1); trc=$? ;; esac;
```

If the language has no separate typecheck step, replace the whole block with a single
space and leave `trc=0`.

**What the hook checks, and what it says** (0.35.0, sdlc-kit#14, #15, #17 — two
adopters on two stacks hit all three independently):

- **Only files inside the project.** An absolute path outside the repository root — a
  session scratchpad, a temp file, another checkout — is skipped, by the same root test
  the TDD guards use. Linting it against this project's config failed for reasons that
  were not the edit's, and a throwaway close-out script had to satisfy the project's
  lint rules before it could even be saved.
- **A check wider than the file blocks only on errors located in the edited file, or in
  a config it could not load; the rest is a non-blocking note.** A project-wide
  typecheck run after every edit blocked 20 times in about 35 edits on one adopter and
  none of the blocks was a defect: 11 were the TDD red itself (a test importing a module
  that does not exist yet is a type error, and *is* the red), 8 of them named a
  production file for an error in the test, and the run also stopped at the first
  failing workspace package and hid the edited file's own error. A block that filters
  sets `trc` only for the edited file's errors and puts a count of the others in `tn`,
  which the hook hands back as context at exit 0 on Claude Code and as a "Not blocking"
  line on Copilot. **A wider check that cannot be filtered leaves the hook for the
  gate** — and so does one that stops at the first failure (`pnpm -r`, a workspace
  runner), since filtering its output turns a hidden error into a silent pass. Which
  recipe checks are wider than the file: TypeScript's `tsc` (filtered block below),
  mypy (it follows the file's imports and reports what it finds there; unfiltered),
  `cargo clippy` on the crate and `go vet` on the package.
- **Each check under its own name, with only its own output.** The failure line says
  `lint failed`, `typecheck failed`, or both, and prints only what failed — never a
  clean check's text under a failure it did not cause.
- **The format check rides in the lint slot, where the gate formats.** If the gate runs
  a formatter check that takes a single file, `{{HOOK_LINT_CMD}}` is
  `<lint> "$f" && <format check> "$f"` (the hook runs the value as one group, so both
  commands' output is captured); otherwise the recipe says the format check stays with
  the gate. Whether the gate formats is a project fact — Prettier in a TypeScript gate is
  the project's choice, not the recipe's — so setup reads the gate before folding one
  in. One adopter's hook passed three files that then failed the gate's
  `prettier --check`.

Half-way states are the remaining source of blocks no edit caused: an import in one edit
and its use in the next, a type member used before it is added. `/next-slice` step 4
asks for providers before consumers and one edit per file, which costs nothing in any
language. Python has an opt-in recipe variant for the rest (below).

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
dialects that replace it need no editing and were both exercised by the proof pass
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
Claude Code documents its own answer — Git Bash on Windows, with a per-hook `"shell"`
key — **but the key cannot be trusted: measured 2026-08-15, Claude Code 2.1.231 on
Windows 11 (headless route, an adopter update's bench), a hook carrying
`"shell": "bash"` never fired at all, on `Stop` and on `PostToolUse` alike, while an
unpinned twin beside it fired** — no error, no log, no feedback, and the adopter's
pinned gate hook had been silently inert for an unknown span. **The interactive
route re-measured the same day: pin dead there too** (a driven interactive TUI
session on 2.1.233 — the CLI had auto-updated between the two same-day benches —
wrote the unpinned marker and not the pinned one on a real turn's Stop). The same
pinned block had measured working on this bench 2026-08-13 with the CLI version
unrecorded, so the verdict is **version drift, not a route artifact**: a dispatch
behavior the config depends on moved underneath an auto-updating CLI, silently —
which is why the probe below records the version. Every Claude-dialect hook the
kit ships is therefore launcher-neutral — bare `sh <script>` / `python <script>`
command lines, no `"shell"` key — and in the shell those resolve on the measured
machine, `sh` was Git's (`<git-install>\usr\bin\sh.EXE`) and stdin delivered the
payload intact (636 bytes measured). **The probe below includes the dispatch check —
a pinned probe hook and an unpinned twin, each writing a marker — and every bench
measurement records the CLI version from now on**: a hook that never fires is
invisible to every body-level probe, so no environment answer is complete without
asking whether the hook ran at all.

**Sharpened 2026-08-07, Copilot CLI 1.0.78, same machine — the answer is per-launcher,
not per-machine.** The `PATH` the hook resolves against is the **launching shell's**:
the same repo, same hooks, same day ran its hooks under WSL bash when the CLI was
started from PowerShell, and under **Git Bash** when the CLI was started from Git Bash
(where Git's `bash` precedes `system32` on `PATH`). Two consequences, both observed
live. A hook written for one route breaks on the other — a `/mnt/d/…` output path
worked from the PowerShell launch and made the same `preToolUse` hook **error and
fail closed** (a denied tool call) from the Git Bash launch. And the WSL route is
worse than a different filesystem view: the WSL launcher **re-parses the hook command
line** on the way in, and that re-parse corrupted every backslash-carrying hook body
it was given and returned empty for `$(cat)` — a bare `cat` still received the
payload. A body that is correct bash can therefore arrive as broken bash, and the
break is silent for any hook whose failure branch is quiet. Hook bodies that must
survive both routes avoid backslashes and stdin-into-`$(…)` entirely (the
skill-activation ledger below is the worked example), and the probe below is run
**from the CLI launched the way this project's operator actually launches it** — a
probe run from the other launcher measures the wrong environment.

**So setup measures it, before trusting either hook.** Run this from the CLI's own
session (`copilot -p '…'`, not from your terminal), which is the only place the answer is
authoritative:

```
bash -c 'echo "shell: $0"; uname -a; pwd; command -v python || command -v python3 || echo NO-PYTHON; command -v node || echo NO-NODE; ls "$PWD" >/dev/null 2>&1 && echo CWD-OK || echo CWD-UNREACHABLE'
```

Run it from the CLI **launched the way this project's operator actually launches
it** (the answer is per-launcher, above; a team with two launch habits probes both).
Read four things off it, and record them in `spec/SDLC.md`
(*Records*, beside the gate), the launch route first:

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
4. **Whether a hook fires at all — the dispatch check.** Everything above probes the
   shell a hook would run in; none of it proves the CLI dispatches the hook. Measured
   2026-08-15 (Claude Code 2.1.231 headless, 2.1.233 interactive — both routes): a
   hook carrying a per-hook `"shell"` key never
   fired while an unpinned twin beside it did — no error anywhere, invisible to every
   body-level probe. In a scratch repo, register two markers-only probe hooks on the
   event you depend on (one in the exact wiring shape you will ship, one minimal
   `sh -c "echo fired > probe.txt"` twin), trigger the event once, and read the
   markers back. A wiring shape whose probe never fires is not installed pending
   investigation — it is replaced with the shape whose probe fired. Record the CLI
   version beside the result: the same pinned shape measured working 2026-08-13 on
   an unrecorded version and dead two days later on both routes, and the CLI
   auto-updated twice inside the measuring day itself.

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
| Template | `templates/claude-gate.template.sh` (logic) + the `Edit\|Write` block in `settings.template.json` (launcher, takes only `{{HOOK_STATUS_MESSAGE}}`) | `templates/copilot-hook.template.sh` (logic) + `.json` (launcher, takes no values) |
| Instantiates to | `.github/hooks/sdlc-gate-claude.sh` + the block in `.claude/settings.json` | `.github/hooks/sdlc-gate.sh` + `sdlc-gate.json` |
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
  hook's own messages are ASCII only. When the cap bites, the capped text ends with a
  `…[truncated by the gate hook at 8000 chars]` marker (added 2026-08-09): lint output
  cut mid-error with no marker reads as complete, which is the silent-failure shape
  the loud-reporting rule above exists to refuse.

**Why the Copilot dialect is a script-plus-launcher pair, not one JSON (restructured
2026-08-07).** The hook config's command line crosses the CLI-to-shell boundary, and
when the hook shell is the WSL launcher that boundary re-parses the line (*the hook
environment* above) — the previous single-JSON body, whose logic was embedded as
backslash-dense parser sources, arrived corrupted there and reported a **false** "no
JSON parser (python or node) on the PATH" on every edit with python present. Now
`sdlc-gate.json` carries only the bare launcher
(`if [ -e .git ] && [ -f .github/hooks/sdlc-gate.sh ]; then cat | sh … ; fi`, on an
entry carrying `"cwd": "."` — no backslash, no `$`, no quotes, pinned by the proof
suite so it cannot be silently re-cleverified; the `cwd` and the `-e` are 0.31.1's, see
*Where the launchers start* below) and everything with teeth lives in `sdlc-gate.sh`, which is read from
disk by the executing shell and never crosses the boundary. The script also resolves
each touched path across path flavours (absolute-Windows headers arrive even when the
hook runs in WSL — the same both-forms fact the guards normalise for), so the gate
lints the real file on either route. Proven live on both launcher routes with real
lint output, and offline by the suite. One consequence for setup: the `.json` takes
**no values** and is copied verbatim (only its `timeoutSec` number is ever edited);
every placeholder now lives in the `.sh`.

**Verified 2026-08-09** against the instantiated body of both dialects — every case
run once under `python` and once under `node`, with `PATH` pinned to one at a time,
because a dialect that is never exercised is not a dialect that was proven; the case
count is derived by the suite at run time, never stated here. The case classes:
`apply_patch`'s raw patch text, multi-file and delete-only patches, both payload
shapes (`toolArgs` and `tool_input`), absolute-Windows and repo-relative paths, a path
containing a space, a non-source file, a payload with no path, a missing file,
unparseable input, neither interpreter present, output past the truncation cap, the
launcher's boundary shape, and the Claude dialect's framed failure — and since 0.35.0
a path outside the project (skipped, beside an in-project twin that is checked), each
check named with only its own output, a compound lint value's stderr, the non-blocking
note, and the TypeScript block above, extracted from this file and driven against a
stub `tsc`. Every silent case
was also run dirty, so silence means something. That is the negative-case proof for the recipe
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

## The TDD-ordering guards — optional, both CLIs, one dialect each

The edit-time hook checks *what* was written. These two guards check **when**, and they
are the only mechanism in the kit that can refuse an action rather than comment on it.
Two dialects, one state machine: the Copilot pair
(`tdd-guard.template.sh` + `.json`, described below in Copilot's event names) and the
Claude Code script (`tdd-guard-claude.template.py` →
`.github/hooks/sdlc-tdd-guard.py`, hook blocks in `.claude/settings.json`). They share
`.git/sdlc-tdd/` — state, log, and the `deny-enabled` flag, so arming deny arms every
installed dialect. The Claude dialect's measured facts (hook-payload probe,
2026-08-12): **green and red arrive on different events** — `PostToolUse` fires
only when a command succeeds and carries no exit code; a failing command fires
`PostToolUseFailure` with the code as a text header of its `error` field — so the
guard reads the event split instead of an exit-code trailer; the shell tool's
hook-visible name on Windows is **`PowerShell`, not `Bash`** (matchers cover both);
and the default Windows hook shell is PowerShell, so the hook command lines are
shell-neutral `python` launchers with every branch of logic in the script. Deny uses
the documented JSON `permissionDecision` form; Stop honors `stop_hook_active` under
the documented 8-block cap. Undocumented and unmeasured: whether a timed-out hook
fails open or closed (default timeout 10 minutes; the template sets 30 s). The guard
does state I/O only, plus — on a write it would otherwise refuse — the cosmetic
classifier's subprocesses, bounded at 12 s compile and 8 s compare.

- **G1, the observed-RED write guard** (`preToolUse`) — a write to a production source
  file is a violation unless a test file has been edited **in this session** and a
  **failing** test run has been observed since that edit. Both halves are required: a
  red alone proves nothing, since any test-shaped command that exits non-zero (a
  pattern matching no tests) manufactures one — found in the field on the first armed
  arc. The corollary: a **resumed** session must touch a test file before its first
  production write, because guard state is session-scoped. Since 2026-08-08 G1
  carries a **second license, for the refactor leg**: a production write is also
  allowed while `.git/sdlc-tdd/refactor-license` exists **and** a green run has been
  observed this session. The file is the session's own one-line declaration (step and
  move) that the edits are behavior-preserving; every write made under it is logged
  with that line so the review can audit the window, a test edit revokes it (a new
  test is a new cycle), and a new session clears it. It survives reds on purpose —
  mutation testing's expected reds and the revert of a failed refactor move are
  production writes too, and G2 still refuses to stop while the latest run is red.
  Since 0.31.0 there is a **third** license, `.git/sdlc-tdd/close-out-license`, which
  is the second one scoped to `/end-slice` and differs in exactly one way: a test edit
  does **not** revoke it. Close-out's mandated order edits tests between its
  production writes — the review fixes tests, the mutation step writes production and
  restores tests, the verification step writes a harness — so a license a test edit
  revokes cannot survive the step it exists for; one real arc paid the re-declaration
  seven times in a single phase (field, 2026-09-01). Every test edit it survives is
  **counted** in the log, so a license held open past close-out is visible in review
  rather than silent.
  Field-driven: with only the red license, armed close-out passes (`change-simplify`,
  mutation testing) forced synthetic test-edit/red cycles or suppressed legitimate
  quality moves.
- **G2, the premature-stop guard** (`agentStop`) — stopping is a violation while no
  green test run has been observed, or the latest observed run is red. The green is
  **any** counted green — a single-test selector run satisfies it. Division of
  labor, not a gap (owner-decided, 2026-08-08): full-suite assurance is the
  end-slice gate's job, and this backstop never runs tests inline. Session-scoped
  (owner-decided, 2026-08-08): it binds only a session that made a production write
  that went through, or edited a test — a planning, docs, or bookkeeping session
  runs no tests by design and stops clean, and a denied write arms nothing.

**The cosmetic exemption (owner-ruled, 2026-10-19).** A production write that G1
would deny is let through when it changes **comments or layout only**, and logged
`OK production write (cosmetic: <how it was told>)`. Both dialects ask one kit-owned
file, `.github/hooks/sdlc-cosmetic.py` (copied verbatim, both CLIs): the Claude script
imports it by path, the Copilot script runs `python .github/hooks/sdlc-cosmetic.py
write <file>` with the payload on stdin. It rebuilds the file as the write would leave
it and compares syntax trees with positions and comments ignored — Python in-process,
TypeScript and the JS family through the project's own `typescript` (resolved upward
from the edited file, so a workspace package's pin wins), Java through the JDK's
compiler API, C# through the .NET SDK's Roslyn — and then compares the **directive
lines** (`# noqa`, `// @ts-expect-error`, `#pragma`, every C# preprocessor line but
the `#region`/`#endregion` pair, …), which must keep their text, their order and their neighbouring code
lines. **It can only grant.** A missing toolchain, a parse error, an ambiguous or
missing match, a timeout, an extension it does not know, a classifier that crashes —
each is "not cosmetic", logged with the reason, and today's rule applies. A docstring
is a string in the tree, so a docstring edit is real. A cosmetic write arms nothing:
G2 does not bind a session for it. Stated limits: `apply_patch` and a Copilot project
with node and no python get no exemption; compiled comparators are cached under
`.git/sdlc-tdd/cosmetic/`, the first call per toolchain costs a compile (about 1.5 s
for Java or C#), later ones about half a second.

Every test-run observation is **spoken back as context, not only logged**. A refused
run (compound command, missing exit-code trailer) is refused out loud with what is
allowed stated — field-driven, 2026-08-08: a silently refused session thrashed and
probed the guard instead of complying. A counted run is spoken too (owner-directed,
2026-08-09, the same invisible-state reasoning on the success side): RED as the write
license it earned — or, when no test file has been edited this session, that it
licenses nothing yet — and GREEN as the stop guard satisfied, with the reminder that
full-suite assurance stays the end-slice gate's job. State facts, never instructions:
the messages report what is now true, and the process files say what to do about it.

Templates: `templates/tdd-guard.template.sh` → `.github/hooks/sdlc-tdd-guard.sh`, and
`templates/tdd-guard.template.json` → `.github/hooks/sdlc-tdd-guard.json`. The JSON
carries no project values, no absolute path — and since 2026-08-07 **no backslash and
no `$`**: each hook body is the bare
`if [ -e .git ] && [ -f .github/hooks/sdlc-tdd-guard.sh ]; then cat | sh … ; fi` on an
entry carrying `"cwd": "."` (the stop entry adds one quoted `else` branch, below),
because the launcher boundary above corrupts anything richer when the hook shell is
the WSL launcher — the previous prelude (`$(cat)` plus backslash-carrying `sed`/`tr`
deriving the root from the payload's `cwd`) came up empty on that route and **exited 0
without running the guard, silently**, which is exactly the failure mode it was built
to prevent. The natural experiment that confirmed the diagnosis: on one day on the
bench (the kit's pre-release test rig — `reference/COPILOT.md`, *Provenance*), the
only session that produced guard-log lines was the only one launched from Git Bash.
The root comes from the hook process's working directory, which the entry's
`"cwd": "."` pins to the repository root (*Where the launchers start*, below), and
which the script trusts only when a `.git` — directory or file — sits there. Proven on
both launcher routes live, and offline by the suite's boundary-property case, which
pins the no-backslash/no-`$` shape so it cannot be silently re-cleverified. The script
takes the five guard placeholders above. State lives in `.git/sdlc-tdd/` (inside the git
directory, so nothing to gitignore — in a linked worktree that is the worktree's own
git directory, read from its `.git` file) and is **session-scoped**: a red observed
yesterday does not license a write today.

**Where the launchers start, and what a broken install says (0.31.1).** Every Copilot hook entry the kit ships carries `"cwd": "."`, which the CLI
resolves against the repository root — the *worktree's* root in a linked worktree.
Without it, builds 1.0.64 through 1.0.87 ran hooks in the **session's** cwd, and a
session started below the root ran with no gate, no guard, and no backstop: the
launcher read "not at the root" as "not a repo" and exited 0 (measured on the bench,
2026-09-27, on 1.0.63, 1.0.78, 1.0.86 and 1.0.88, both launcher routes; 1.0.63 and
1.0.88 start hooks at the root either way). The test is `[ -e .git ]`, not `-d`,
because in a linked worktree `.git` is a file — on every build. The scripts read that
file themselves rather than asking git: a worktree made by Windows git names a `D:/`
path that neither WSL bash nor WSL's own git can follow, so they translate it the way
the gate script translates touched paths, and the close-out script points git at the
result. A consequence worth stating wherever a mode is recorded: state is therefore
**per-worktree** — deny armed in the main checkout does not arm a linked worktree. **Exit codes are not loud on Copilot**: a non-zero hook exit lands in the
session's own log (`~/.copilot/session-state/<id>/events.jsonl`) and nowhere the agent
or the operator reads (measured 2026-09-27). The one channel measured to reach the
agent without blocking work is a stop hook's block, so each stop-bearing launcher —
the guard's and the backstop's, in both dialects — carries an `else` branch that
blocks once, naming the missing script, and stands down on `stop_hook_active`. That
branch prints JSON, so it carries quotes; quotes were banned from launchers as a
precaution, and a quoted branch was measured surviving both launcher routes.

**Claude Code has no `"cwd"` key: its hooks start in the session's cwd, and a shell
`cd` moves that and keeps it moved.** Measured on an adoption 2026-10-16 (Claude Code
2.1.301, Git Bash, sdlc-kit#13; a second adopter hit it independently): after one `cd
<subdir> && …` in a shell call, every relative launcher looked for
`<subdir>/.github/hooks/…`. The guard's `python …` launchers failed with *can't open
file* and its test runs went unrecorded; the gate launcher exited 127, which PostToolUse
treats as non-blocking, so **the gate was skipped in silence**; and the close-out Stop
block's `-e`/`-f` test failed, which until 0.35.0 printed the same *is missing* message
a real missing script prints. That message now says *not found from `<pwd>`* and tells
the session to `cd` back to the root, so the two cases read differently. **Since
0.36.0 every launcher in `.claude/settings.json` starts with the root anchor
`cd "$(git rev-parse --show-toplevel)"; `**, so a moved session no longer moves its
hooks. Measured live 2026-10-23 on the bench, after a `cd spec` in the session's shell:
on Claude Code 2.1.309 (Git Bash) the unanchored launchers reproduced the defect — two
test runs unrecorded, the first edit **denied** by the guard's *can't open file* exit 2
until the model `cd`'d back by itself — and the anchored ones recorded the run GREEN,
let the edit through first time, and ran the gate, the guard's stop and the close-out
block from the root. On Copilot 1.0.103, which runs these launchers through PowerShell
7.6.8 from the root whatever its own shell did, every edit- and shell-path launcher
succeeded from both launch routes; the only failures were the ones `COPILOT.md`
already records for a both-dialect project (`sh` not found from a PowerShell launch;
the close-out block's quoting mangled from Git Bash), and the Claude-dialect scripts stand down under a Copilot
payload anyway. The anchor is `;`-joined, never `|| exit 2`: Windows PowerShell 5.1
cannot parse `||`, and on Copilot a PreToolUse launcher that fails to parse **denies
every edit**; in `sh` the `||` branch almost never fires, because `cd ""` succeeds.
The adopter's `cd "${CLAUDE_PROJECT_DIR:-.}"` form was rejected for the same reason —
PowerShell reads `${CLAUDE_PROJECT_DIR:-.}` as one variable name, expands it to empty
and lands in the home directory (measured 2026-10-20, pwsh 7). It also reaches a linked
worktree's own root. **What the anchor does not cover:** a project path containing `[`
or `]`, which PowerShell's `cd` reads as a wildcard and refuses (the launcher then runs
from wherever it started, as before); and a session where git cannot name the root, where
the close-out message above still says where it looked. Prefer `git -C <dir>` or a
subshell `( cd <dir> && … )` all the same: the anchor keeps the hooks at the root, but
the session's own relative paths still move with its cwd.

**Claude Code on Windows must find Git Bash, or every `sh` hook silently fails to run.**
Measured 2026-09-27 on Claude Code 2.1.283 with Git for Windows installed at a
non-default path: a session launched from **Git Bash** logged, for the `sh -c` close-out
`Stop` command, *"requires bash but Git Bash was not found … or add \"shell\":
\"powershell\""* — in the `--debug` log only; nothing reached the agent — while the
`python …` guard commands ran. Launched from **PowerShell** on the same machine, the
same hook ran. (Plausibly Claude Code derives Git Bash from the `git.exe` on `PATH`,
which is `…\cmd\git.exe` from PowerShell and `…\mingw64\bin\git.exe` inside Git Bash;
that is an inference, the behaviour is measured.) The kit's gate, ledger, and backstop
launchers on Claude Code are all `sh` commands. Where Git is not at its default path, set
`CLAUDE_CODE_GIT_BASH_PATH` to its `bin\bash.exe`, and prove the gate hook from the
launch route the operator actually uses — the standing rule of *the hook environment*. The guard reads its payload with the same dual python-or-node parser the gate
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

**Key the command pattern on the test runner, never on a filename.** The bench
version matched `node test…` as adjacent words and was blind to `node .\test-x.js`, because the
`.\` prefix sat between them. Wildcards spanning the runner and the word `test`
(`*node*test*`) match every invocation form; a pattern anchored on a path does not.

**Every pattern value must be a valid shell `case` pattern — no spaces, `|` between
alternatives — and the same in both dialects.** The Copilot script pastes the value
into a `case` arm unquoted, so a space is a **syntax error**: the script dies before it
logs anything, and Copilot reads the non-zero exit as deny — every write refused with
`hook exited with code 2` and an empty `guard.log` (measured on the bench, 2026-10-19,
with `*node *test*`). The Claude script matches with `fnmatch` and tolerates the
space, so a value that works in one dialect proves nothing about the other. Where a
space seems needed, a `*` spans it. Check the instantiated script with
`sh -n .github/hooks/sdlc-tdd-guard.sh` before the logging ramp, using an `sh` that
resolves — on Windows Git Bash's; Copilot's shell tool resolves none, and a shell error
there is not a syntax verdict.

**The patterns above are matched against the command with quoted arguments
removed** — both guard dialects strip `"…"` and `'…'` before the `case`, so the
table's substring shape stays as written and needs no anchoring. It exists because a
substring pattern matched against the raw string fires on any command whose *text*
mentions the runner: measured on a Java adoption, a `git commit -m` whose body quoted
the RED run commands, plus two appends writing a RED record — three spurious notices
in one phase, on a control whose refusals have to be believed. Quoted text is data,
never what the shell runs. **The known cost, stated rather than hidden:** a runner
reachable only inside a quoted argument (`bash -c "pytest"`) no longer counts — run it
bare, which the compound-command rule
already requires. The compound check deliberately still reads the raw command: a
stripping bug there would admit a genuine compound and record a false green, so that
check stays conservative.

**A command that names the runner without running it never counts** (0.35.0). The
substring pattern also matched `cat vitest.config.ts`, `grep pytest pyproject.toml`,
`pip install pytest`, and a heredoc whose body names the run — the kit's own commit
recipe (`git commit -F - <<'EOF'`) among them. A failure counted as a RED, and a success
counted as a **GREEN that satisfied the stop guard with no test run at all**. Both
dialects now drop, silently: any command containing a heredoc (`<<`); a command whose
leading executable — after any `env` and `NAME=value` prefix, with its directory and
`.exe`/`.cmd`/`.bat`/`.ps1` removed — is a reader or a tool that never runs tests (`cat`,
`type`, `more`, `less`, `head`, `tail`, `sed`, `awk`, `grep`, `egrep`, `fgrep`, `rg`,
`find`, `ls`, `dir`, `echo`, `printf`, `wc`, `diff`, `git`, `gh`, `jq`, `code`, `which`,
`where`, `file`, `stat`, `pip`, `pip3`, `pipx`, `conda`, `Get-Content`, `gc`,
`Select-String`, `sls`, `Get-ChildItem`, `gci`, `Test-Path`, `Write-Output`,
`Write-Host`); `python -m pip`; and `npm`, `pnpm`, `yarn`, `bun`, `uv` or `poetry` with
a subcommand that installs, removes, updates or lists (`install`, `i`, `add`, `ci`,
`remove`, `rm`, `uninstall`, `un`, `update`, `upgrade`, `up`, `list`, `ls`, `view`,
`info`, `show`, `outdated`, `audit`, `why`, `sync`, `lock`). A fixed list on purpose:
every mistake it makes lands on the not-counted side. `uv run pytest`, `npx vitest`,
`python -m pytest` and `env CI=1 pytest` still count.

**A RED needs the runner's own report** (0.35.0, `{{TEST_REPORT_PATTERN}}`). A failing
exit is the command's verdict; a RED is the test's. A wrapper that fails before the
runner starts — pnpm's install check (`ERR_PNPM_IGNORED_BUILDS`), a bad flag, a missing
binary, a filter matching no tests — exits with the code a failed test uses, and was
counted as the red that licenses a production write (one adoption, twice). So a failing
run counts only when the pattern is found in its output, matched with ANSI codes and
CRLF removed; otherwise the run is refused out loud. **The pattern must be a marker the
runner prints first, never its closing summary**, because neither CLI delivers the end of
a long output: measured 2026-10-20, Claude Code's `error` keeps about the first 10,000
characters, and Copilot replaces a very long result with *"Output too large…"* and the
first 500. Measured values (vitest 4.1.12, jest 30.5.2, pytest 9.0; each counts an
assertion red, a missing-module red and a syntax-error red, and refuses "no tests found",
a pass, a missing wrapper binary and a CLI usage error):

| Runner | `{{TEST_REPORT_PATTERN}}` | Quiet re-run when a noisy red is refused |
|---|---|---|
| pytest | `=+ (FAILURES\|ERRORS) =+` | not needed unless `-s`; drop it |
| vitest | `^\s*FAIL\s\|Test Files +\d+ failed` | `--silent=true --reporter=dot` (`--silent` alone keeps a failing test's console output in 4.1) |
| jest | `^\s*FAIL\s\|Test Suites: \d+ failed` | `--silent` |
| Maven (Surefire) | `<<< (FAILURE\|ERROR)!\|COMPILATION ERROR` | `-q` |

The Maven row was measured separately: Maven 3.9.2, Surefire 3.2.5 and JUnit 5.10.2,
with `mvn -q test`. An assertion red prints `<<< FAILURE!` at character 80. A test that
does not compile prints `[ERROR] COMPILATION ERROR :` at character 8. Neither marker
appears in a pass (quiet or not), an unrecognised flag, `-Dtest=` matching no test, or a
missing `mvn` (`bash` exit 127, PowerShell's *not recognized*). Its cost: a compile
error in **production** code also counts as a RED, just as pytest counts an import error.

vitest's ` RUN  v…` start line is **not** a marker: it prints on every run, a pass and
"No test files found" included. The value is a regular expression in the subset Python
and JavaScript share (the Copilot script runs either), with no quote and no backtick.
An invalid one is a `GUARD ERROR` in the log, and no failing run counts until it is
fixed. Copilot strips colour and trims leading whitespace off the whole output — hence
`^\s*`. For another runner, find the first line its failure report prints and that a
pass, a wrapper error and "no tests" never print; setup proves the value (below).

**Code is `SOURCE_GLOB` minus the exempt pattern** (0.35.0, `{{GUARD_EXEMPT_PATTERN}}`).
`SOURCE_GLOB` is extension-only, so a one-off tools script, a config written in the
source language and the graph tool's scratch each needed a red no test could produce —
measured on two adopters: writes to `tools/` scripts denied, `.dependency-cruiser.mjs`
denied, `playwright.config.ts` passed only on a licence, and three of Understand
Anything's `.ua/tmp/*.cjs` charged as production. A red no test can produce gets
manufactured or licensed around, and a licence that becomes routine stops meaning
anything. A repo-relative path matching the pattern is neither production nor a test,
checked before the test classification, and logged as exempt when `SOURCE_GLOB` would
have charged it. `.ua/*` and `.understand-anything/*` are exempt in the template itself,
whatever the value. `SOURCE_GLOB` is unchanged, so the edit-time hook still lints
exempt files. Setup proposes `*.config.*|.*` plus the tree's own script directories
(`tools/*`, `scripts/*`) and the owner confirms; a product script that has tests stays
code by leaving its directory out. **Never empty**: the Copilot script pastes it into a
`case` arm after the two built-in patterns, where an empty alternative is a syntax error
and Copilot reads that as deny-everything — a project that exempts nothing writes `.ua/*`.
The same definition of code is what the edit-tools rule in `spec/SDLC.md` covers.

**A file outside the repository is never production source.** Both dialects reduce
the write path to a repo-relative one and skip an absolute path that is not under the
root. `SOURCE_GLOB` is extension-only, so before this a session scratchpad —
`…/Temp/<session>/scratchpad/mutate_s5.py`, never committed, never on the gate's path
— was classified production and cost the same refactor license as an edit to the
module guarding an adoption's authoritative database. Measured over one arc: 13
denials, 5 of them on scratchpad files, 12 writes licensed for a mandated `/end-phase`
verification step that the command's own text never mentions a license for (owner
ruling: a control that cannot tell those two acts apart charges the same price for
both, which is how a license stops meaning anything). A **relative** path stays in
scope — it can only be relative to the root the guard resolved, and skipping it would
be a hole rather than a scoping fix. The reduction also fixed a live misclassification
in the shell dialect, which
never attempted it: an absolute path to `tests/conftest.py` matched neither
`TEST_PATH_PATTERN` form (`tests/*` cannot match a full Windows path, and the
basename looks nothing like a test) and fell through to `SOURCE_GLOB`, so a test edit
was charged as a production write and licensed nothing.

**The ramp is not optional.** The guards install in **logging mode**, where they write to
`.git/sdlc-tdd/guard.log` and never deny. Deny is armed by creating the flag file
`.git/sdlc-tdd/deny-enabled` and disarmed by deleting it. Read a few real sessions of the
log first and confirm the guard is recognising the project's own test runs: a guard that
does not see your test command will, the moment deny is armed, block every production
write in the repo. This ordering was pre-registered on the bench and it earned its
keep — the deny ramp found a defect (a compound test command reporting the wrong exit
code, recording a **false green**) that logging mode had not surfaced.

**Prove both guards the way the kit proves every check — by making them fail.** In a
scratch session **of the Copilot CLI itself, launched the operator's way** — the
guards fire only from its hooks, in the per-launcher hook shell the probe above
measured, so a proof run anywhere else proves nothing about them. Write a production
source file without a failing test first, and confirm
the log names it; then finish the session with no green run, and confirm the stop guard
logs a would-block. If nothing appears, the guard is not firing — check the tool-name
matcher against `reference/COPILOT.md`'s discovery procedure and the hook environment
above, and do not arm deny until the log speaks.

**What these guards are not.** A cooperative backstop, not a security boundary, and the
generated `spec/SDLC.md` must say so: writes made through the shell tool are invisible to
G1, and a session can read the guard's own source and state. On the bench a session did
exactly that — it read the script to learn the recognised command format. It complied,
but it could as easily have touched the state files. Since 0.35.0 the shell gap carries
a rule rather than only a disclaimer: **code changes only through the editor tools**
(`CLAUDE.template.md` *Always-Active Rules*, restated in the guard note), stated as
overriding any harness guidance that permits shell edits — one adopter's guard, armed
in deny mode, watched none of three production writes and a 16-mutation runner made
through the shell in a single slice, and another counted about 28 unseen writes while
armed (sdlc-kit#15, #16, #17). Code is `{{SOURCE_GLOB}}` minus the exempt pattern;
docs, configs and exempt scripts stay shell-writable. The exceptions are a tool's own
output (a formatter's `--write`, codegen) and `/end-slice` step 5's hash-verified
mutation runner. A test written through the shell does not license its red: once the
rule exists it is out of process, and counting it would reward the breach. **Since
0.36.0 the stop reports such writes.** At a session's first hook call the guard
records `HEAD` and the content of every code file already modified. At each stop it
names every code file whose content differs from that start and that no pre-write let
through. That covers the working tree and what the session committed, but not commits
dated before the session began (a pull, a merge). Armed, it blocks the stop once per
set of files and asks for the owner to be told; in logging mode it logs. Content,
never mtime, so the hash-verified runner, which puts the same bytes back, never trips
it; and a write the guard denied, then made through the shell, is caught. Its costs:
a formatter or generator writing into code nobody edited this session reads as a
breach (exempt generated directories), a commit pulled in mid-session reads as the
session's, and a shell write in the session's very first tool call predates the
snapshot. It detects, never prevents. Two more honest limits: G2 accepts
any green test run rather than a full gate run, and a session that satisfies the guard
can still delete the test afterwards — which is why the evidence lines in the slice
commit body, not the guard, are what make TDD ordering auditable after the fact, and
why an added-then-deleted test is a named review lens (`REVIEW_LENSES.md`, *the
disposal-intent test*) rather than guard territory.

---

## The close-out stop-time backstop — optional, both CLIs, one wiring each

The close-out evidence checker (`.github/hooks/sdlc-close-out.sh`, installed on
every adoption) carries a second mode, `stop-check`, wired as a stop hook where the
owner accepts the offer. At session end it classifies the **unpushed** commits
(`@{u}..HEAD`, capped at 20; `HEAD` only when no upstream is configured — the log
line states which) by the same record grammar `/end-slice`'s command step runs:

- a **defective** record — some evidence keys present, but one missing, empty, or
  duplicated — logs a would-block naming the commit and its problems. This is the
  escape the command step cannot catch: a session that committed a slice and ended
  without verifying, or past an unresolved INCOMPLETE. The verdict is stateless —
  a defective body is defective whichever session looks at it, and the remedy
  (amend before pushing) is legal exactly while the commit is unpushed.
- a **bare** commit — no record keys at all — is ambiguous (a silent slice commit,
  or a legitimate docs commit), so it flags only when the TDD guards are installed
  and their session state (`.git/sdlc-tdd/`) shows this session wrote production
  code or edited a test. **This class never blocks, armed or not** — log-only by
  design on every install — and on a guard-less adoption the
  generated `spec/SDLC.md` must say plainly: the backstop catches defective
  records, not silently absent ones.

**Wiring, measured per dialect.** Copilot CLI: `.github/hooks/sdlc-close-out.json`
(verbatim from `templates/close-out-hook.template.json`), `agentStop`, the same
`cat | sh …` wrapper shape as the guard JSON; the block schema
(`{"decision":"block","reason":…}`) was measured on the bench 2026-08-05. Claude
Code: a `Stop` block in `.claude/settings.json` carrying the **launcher-neutral**
form — `sh -c "if [ -e .git ] && [ -f .github/hooks/sdlc-close-out.sh ]; then sh
.github/hooks/sdlc-close-out.sh stop-check; elif …; else …; fi"`, no `"shell"` key
(the `-e` and the `else` branch that blocks once when the script is missing are
0.31.1's — *Where the launchers start*, above; the Copilot JSON carries the same
branch and `"cwd": "."`). Three dated
measurements sit behind that shape, routes and versions named: 2026-08-13
(interactive-route bench, CLI version unrecorded) the pinned `"shell": "bash"`
block fired and delivered the payload on stdin; 2026-08-15 (headless, Claude Code
2.1.231, an adopter update's bench) the same pinned block **never fired** while
the launcher-neutral form did, on a real session stop with the classification
line read back; 2026-08-15 again (interactive, 2.1.233 — the CLI auto-updated
between the same-day benches) the pin dead on that route too — version drift,
not a route artifact; see *The hook environment*, which is why no shipped hook
depends on the pin. The block schema (`{"decision":"block","reason":…}`) was measured
honored 2026-08-14 (the pre-registered deny ramp; CLI version unrecorded — the
record-the-version rule postdates it): the blocked session received
the reason, amended the commit with the stated-skip form rather than fabricating
evidence, and the next stop stood down on `stop_hook_active` — the same sequence
the Copilot dialect produced on the same bench.

**Fail direction — the inverse of the command step, on purpose.** `check` fails
closed because a command step's failure is seen and quoted; `stop-check` fails
open — its own errors log to `.git/sdlc-close-out/log` and exit 0 — because a
hook that errors must not block real work. It also stands down unconditionally
under `stop_hook_active` (the documented consecutive-block cap, measured at 8 on
both dialects — versions unrecorded; those benches predate the
record-the-version rule — is never fought).

**Logging first, always.** It installs logging-only: verdicts appear as
`stop: WOULD-BLOCK` lines in `.git/sdlc-close-out/log`, and nothing is blocked.
A flag is logged **once per commit per session** (a repeat stop logs `stop: repeat`),
so counting `WOULD-BLOCK` lines counts events: before 0.29.0 one session logged the
same commit fifteen times. Commits that touch only `spec/` and the root kit documents
are skipped before classification — bookkeeping, never a slice, and they were 100% of
this backstop's measured firing history.
Blocking the defective class is armed by creating `.git/sdlc-close-out/deny-enabled`
and disarmed by deleting it — the owner's call, after reading a few real sessions
of the log, and the `{{CLOSE_OUT_CHECK_NOTE}}` line in `spec/SDLC.md` is updated
in the same breath. Prove it by firing it — in a scratch session of each installed
CLI, **launched the way this project's operator actually launches it**, since the
Copilot hook shell is per-launcher and the Claude dispatch layer has been measured
moving under an auto-updating CLI (*The hook environment*: the pinned form worked
on one version and silently never fired on the next): end the session on an unpushed
commit missing one record key and read the would-block line back; no line means
the hook is not firing.

**What it is not.** A cooperative backstop with the guards' own honest limits: it
reads commit bodies, not truth — a fabricated record line passes it, which is why
the steps that produce the lines remain the evidence — and a session can read its
source and state. Scope is deliberately narrow: unpushed commits on the current
branch, this clone only (`.git/` is per-clone, like the guard state beside it).

---

## The skill-activation ledger — optional, logging-only, both CLIs

One hook, one line per tool-dispatched skill activation, appended to
`.git/sdlc-skill-ledger.jsonl`:
an ISO-8601 UTC timestamp, a space, then the hook payload verbatim. It exists because
**presence is not activation** — on Copilot CLI skill activation is relevance-based, a
skill can silently never run, and until this ledger the only detector was the damage a
skipped step eventually caused. With it, the retro's step-evidence sweep reads
activations off disk instead of trusting self-report.

The measured facts it is built on (bench, 2026-08-07 — Copilot CLI 1.0.78 and Claude
Code, one probe run each, explicit and relevance-based activation both logged):
invoking a skill fires the post-tool-use event on **both** CLIs, under `toolName:
"skill"` on Copilot (a name absent from the hooks reference's own tool-name list —
measured, not documented) and `tool_name: "Skill"` on Claude Code. What it cannot
see, field-measured 2026-08-11: a command the owner types as a slash command is
injected by the CLI with no tool call — no post-tool-use event, no line (a real
adoption's ledger ran four phases without a single line for its slash-typed slice
closes, while faithfully recording every tool-dispatched skill). The ledger is
evidence for tool-dispatched activations only; a missing line for a slash-invocable
command is no signal either way, and the retro sweep is told so. Copilot's payload
carries its own `timestamp`; Claude Code's does not, and neither payload ends with a
newline — so the hook stamps the time itself and appends the newline itself, or the
"JSONL" file becomes one unparseable line.

**Dialects — one body, two launchers (since 0.31.1).** The body is
`templates/skill-ledger.template.sh` → `.github/hooks/sdlc-skill-ledger.sh`, no
placeholders, shared by both CLIs. It takes the root from `CLAUDE_PROJECT_DIR` where
Claude Code sets it and from its working directory otherwise, resolves the git
directory from `.git` — a directory, or a linked worktree's `.git` file — and appends
there. It may use `$(cat)` and `\n` freely: it is read by `sh`, never re-parsed on a
launcher boundary. Copilot: `templates/skill-ledger.template.json` →
`.github/hooks/sdlc-skill-ledger.json`, copied verbatim — it takes no values, and is
now a bare launcher on an entry carrying `"cwd": "."`, like the other Copilot hooks
(*Where the launchers start*, above). Until 0.31.1 it carried the body inline —
deliberately primitive, no backslash, stdin piped straight to the file, because the WSL
launcher boundary (measured 2026-08-07) corrupted every backslash-carrying body and
returned empty for `$(cat)`. An inline body cannot follow a worktree's `.git` file
without a `$` that boundary also eats, so it moved into the script. Claude Code: the
`"Skill"`-matcher block in `.claude/settings.json` (part of `settings.template.json`)
is a bare launcher, `sh .github/hooks/sdlc-skill-ledger.sh` behind the root anchor
(*Where the launchers start*, above) — split 2026-08-15 with the
gate hook, because the per-hook `"shell": "bash"` pin the inline body depended on was
measured never firing (*The hook environment*). Setup removes the launcher(s) and skips
the script install if the ledger is declined — the *record* of the decline lives in
`spec/SDLC.md`, never here. Both dialects **report when they cannot write** —
stderr and a non-zero exit — but only one of them is loud: on Claude Code that reaches
the agent; on Copilot a post-tool-use exit reaches only the session's own log
(measured 2026-09-27), which is as far as that event lets a hook speak. A ledger that
silently stopped recording would read as "no skill ever activated", which is precisely
the false negative it exists to prevent.

**Prove it the way every check is proven.** In a session of each installed CLI —
launched the way this project's operator actually launches it, since the hook shell
is per-launcher — invoke
any installed skill explicitly (`/tdd` will do), then read the last line of
`.git/sdlc-skill-ledger.jsonl` and confirm it names that skill and this session. No
line means the hook is not firing — on Copilot check the matcher spelling (`skill`,
lowercase) and the hook environment above; on Claude Code check that
`$CLAUDE_PROJECT_DIR` resolves.

**Honest limits, for the note in `spec/SDLC.md`.** `.git/` is per-clone: the ledger
records the sessions of one machine, and a retro citing it says whose. It records
*activation*, not diligence — a skill that loaded and was ignored still logs a line;
the evidence lines in the slice commit body remain the record of what a step actually
did. And it is cooperative like every hook here: a timed-out hook fails open, so an
absent line is strong evidence but not proof of non-activation — the retro's
four-state vocabulary (ran / caught / skipped with reason / no evidence) already says
this correctly.

---

## Python

```
python -m ruff check .            # lint
python -m mypy <package>          # typecheck (strict; keep the baseline green)
python -m pytest -q               # tests
```

Hook: `SOURCE_GLOB` = `*.py`; lint = `python -m ruff check "$f"`, or
`python -m ruff check "$f" && python -m ruff format --check "$f"` where the gate runs
`ruff format --check`;
typecheck block = `case "$f" in *<package>*) t=$(python -m mypy "$f" 2>&1); trc=$? ;; esac;`
(through 0.34.x this read `m=`, and the hook prints `t`, so a mypy failure printed its
failure line with none of mypy's errors under it). mypy follows the file's imports, so
an error in an imported module blocks this file too; a project where that bites leaves
mypy to the gate.

Opt-in variant, offered and never the default: lint =
`python -m ruff check --ignore F401,F821,F841 "$f"`. An import before its use (F401), a
use before its import (F821) and a mutation's throwaway local (F841) are the states a
change passes through between two edits — one adopter logged about 21 such blocks over
two slices, all moot by the next edit. **The cost:** a misspelled name and a genuinely
dead import wait for the gate, which still runs all three.

## TypeScript / JavaScript (Node)

```
npx eslint .                      # lint
npx tsc --noEmit                  # typecheck (omit for plain JS)
npm test                          # tests (vitest/jest — whatever package.json says)
```

Hook: `SOURCE_GLOB` = `*.ts|*.tsx|*.js|*.jsx`; lint = `npx eslint "$f"`, or
`npx eslint "$f" && npx prettier --check "$f"` where the gate runs Prettier.
Typecheck: per-file `tsc` is unreliable, and a project-wide one blocks on every error
anywhere (*What the hook checks* above). The block below typechecks the one TypeScript
project that owns the file — the nearest `tsconfig.json` upward — from the root, and
blocks only on errors located in the file, in that tsconfig, or with no location at all
(a `tsc` that could not run checked nothing, so it never reads as clean); a count of
the other files' errors goes in the note. Proven on a pnpm workspace by the adopter who
wrote it (13 cases, two live), and by the kit's gate-hook suite against a stub `tsc`:

```sh
case "$f" in *.ts|*.tsx)
  d=$(dirname "$r"); while [ "$d" != "." ] && [ ! -f "$d/tsconfig.json" ]; do d=$(dirname "$d"); done
  cfg="$d/tsconfig.json"; if [ "$d" = "." ]; then cfg=tsconfig.json; fi
  a=$(npx tsc --noEmit --pretty false -p "$cfg" 2>&1); arc=$?
  if [ $arc -ne 0 ]; then
    t=$(printf '%s\n' "$a" | awk -v r="$r(" -v c="$cfg(" '/^[^ \t]/ { k = (index($0, r) == 1 || index($0, c) == 1 || $0 ~ /^error /) } k')
    if [ -n "$t" ]; then trc=1; else
      n=$(printf '%s\n' "$a" | grep -c ': error TS')
      if [ "$n" -gt 0 ]; then tn="$n type error(s) in other files of $cfg (the gate checks them)"; else t=$a; trc=$arc; fi
    fi
  fi ;;
esac;
```

Run `tsc` directly, never through the workspace's own `typecheck` script when that
script is `pnpm -r …` or another runner that stops at the first failing package: the
run then never reaches the package that owns the edited file, and the file's own error
is never printed (measured: the shipped hook blocked on another package's error and
reported the edited file's not at all). A file outside every tsconfig's `include` is
not typechecked by this block; typed ESLint reports it ("not found by the project
service"), and a project without typed linting leaves that case to the gate.

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

Hook: `SOURCE_GLOB` = `*.go`; lint = `golangci-lint run "$f"`. `gofmt -l` exits 0
whether or not it lists the file, so as a format check it needs a test of its output:
`golangci-lint run "$f" && { [ -z "$(gofmt -l "$f")" ] || { echo "not gofmt-formatted: $f"; false; }; }`.
`go vet` runs on the file's package, which is wider than the file — unfiltered, it
belongs to the gate.

## Java (Maven / Gradle)

```
mvn -q checkstyle:check           # lint            (gradle: ./gradlew checkstyleMain)
mvn -q compile                    # compile = typecheck (gradle: ./gradlew compileJava)
mvn -q test                       # tests           (gradle: ./gradlew test)
```

Hook: `SOURCE_GLOB` = `*.java`; per-file tooling is weak — a compile-only hook via the
build tool is usually too slow; consider lint-only (`checkstyle -c config "$f"`) or no
hook, relying on the gate. There is no standard per-file format check; a formatter the
gate runs stays with the gate.

## Rust

```
cargo clippy --all-targets -- -D warnings   # lint
cargo check                                  # typecheck
cargo test                                   # tests
```

Hook: `SOURCE_GLOB` = `*.rs`; lint = `rustfmt --check "$f"` where the gate checks
formatting. Per-file clippy isn't supported, and `cargo clippy` on the crate is wider
than the file: it blocks on any error in the crate, so unfiltered it belongs to the
gate.

---

## Runtime-standards rules (logging, error handling, secure coding)

Mechanical enforcement for the conventions recorded in the project's `CLAUDE.md`
*Runtime Conventions* section: where the linter can state the rule, the rule goes in
the **linter's own config**, so the gate and the edit-time hook enforce it with no new
command. The match-reality rule above applies here too: check what the project's
linter config already enables before proposing anything, and on an existing project
measure each proposed rule's current violation count first, stating the shell the
count was measured in beside it — the owner adopts a rule
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


### The lens↔rule map: what a rule decides, and the residue it cannot

`reference/REVIEW_LENSES.md` carries eight review lenses. Three of them
(*logging and swallowed errors*, *untrusted input*, *secrets and exposure*) have
subject matter the rules above already cover mechanically, and a rule is strictly
better than a lens where it applies: it is deterministic, it runs on every file rather
than on the ones a reviewer opened, and the gate already enforces it. This map says,
per lens, **which half a rule can decide** — adopt those rules for the project's
languages — and **which half no rule can express**, because that residue is the only
part a human review adds.

Read it when adopting rules (both setup modes) and when a lens comes up for its
retirement reading. It is a map of *coverage*, not a claim that any lens is redundant:
a lens whose mechanizable half is fully adopted is a lens whose value is now exactly
its residue, and that is the question its clock should be answering.

The rules named per language are drawn from the starting points above plus the additions
named here; where a language
has no equivalent the row says so, because an omission that reads as an oversight gets
filled in with an invented rule ID the next time someone edits this file.

**Lens: error propagation.** *Mechanized:* an exception raised without its cause
attached, a caught-and-rethrown error that loses the stack, an error return dropped on
the floor. Python `B904`, `E722`; JS/TS `no-useless-catch`, `no-throw-literal` (typed:
`@typescript-eslint/only-throw-error`, `@typescript-eslint/no-floating-promises`); C#
`CA2200`, `CA1031`; Go `errcheck`, `errorlint`; Java checkstyle `IllegalCatch`, PMD
`PreserveStackTrace`; Rust clippy `unwrap_used`, `expect_used`.
*Residue:* every caller's control flow re-read after a new raise travels, and whether a
status code can honestly make its claim about fault. No linter reads a 4xx and knows
whose fault it was.

**Lens: logging and swallowed errors.** *Mechanized:* the empty handler, the blind
catch, the stray `print`, the error logged without its exception. Python `E722`,
`BLE001`, `TRY400`, `T201`/`T203`; JS/TS `no-empty`, `no-console`; C# `CA1031` under
`-warnaserror`; Go `errcheck`, `forbidigo`; Java checkstyle `EmptyCatchBlock` +
`IllegalCatch`, PMD `EmptyCatchBlock`; Rust clippy `print_stdout`, `dbg_macro`.
*Residue:* the level as a routing decision — whether anyone watches the level chosen,
whether the line carries the operation and identifying inputs a reader needs to act,
and the one-failure-one-ERROR bound. A rule sees the logging call; it cannot see the
reader, and "swallowed with a receipt" passes every rule in this row.

**Lens: verify the denominator.** *Mechanized:* nothing, in any of the six languages.
The lens is about a claim made from a search — what was enumerated, and what the
enumeration could not reach — and no rule takes a search as its input.
*Residue:* all of it. This row exists so the absence is recorded rather than
rediscovered.

**Lens: shared state under concurrency.** *Mechanized:* thinly, and unevenly. Go is the
strongest — `go test -race` in CI (a gate command, not a rule) plus `go vet`'s
`copylocks` and `loopclosure`; Java SpotBugs' multithreaded-correctness detectors
(`IS2_INCONSISTENT_SYNC`); Rust's `Send`/`Sync` checking in the compiler itself, plus
clippy `await_holding_lock` and `mutex_atomic`; JS/TS `require-atomic-updates` and
`@typescript-eslint/no-misused-promises`. Python and C# have no rule that names the
model.
*Residue:* the lens's actual question — name the runtime's concurrency model and state
what serializes access — and its measurement requirement. "Nothing serializes access"
is a sentence a reviewer writes, not a diagnostic a linter emits.

**Lens: untrusted input.** *Mechanized:* the interpreter hops, by taint or by pattern.
Python ruff's bandit family — `S608` (SQL), `S602`–`S609` (shell), `S301` (`pickle`),
`S506` (unsafe YAML load), `S307` (`eval`); JS/TS `no-eval`, `no-implied-eval`,
`no-new-func`, plus eslint-plugin-security's `detect-child-process` and
`detect-non-literal-fs-filename`; C# `CA2100` and the taint rules `CA3001` (SQL),
`CA3003` (file path), `CA3006` (command); Go gosec `G201`/`G202` (SQL string building),
`G204` (subprocess), `G304` (file path from a variable); Java find-sec-bugs
`SQL_INJECTION_*`, `COMMAND_INJECTION`, `PATH_TRAVERSAL_IN`. Rust has no comparable
taint set in clippy — `cargo audit` covers dependencies, not data flow.
*Residue:* naming **every** interpreter the input reaches and the neutralizing
mechanism at each hop, and the canonicalize-then-prefix-check sequence. A rule sees the
`realpath` call; it does not see whether the *result* was checked against the intended
root, which is the near-miss the lens was written for.

**Lens: secrets and exposure.** *Mechanized:* the hardcoded credential, and committed
config. Python `S105`–`S107`; JS/TS eslint-plugin-no-secrets (`no-secrets/no-secrets`);
C# `CA5390`, plus `CA5350`/`CA5351` for the weak-crypto neighbours; Go gosec `G101`;
Java find-sec-bugs `HARD_CODE_PASSWORD`, `HARD_CODE_KEY`; Rust has no clippy rule here.
Across all six, repository-level secret scanning (the forge's push protection, or a
scanner in CI) is the rule that catches what a language linter never sees, because a
secret's usual home is a config file no linter reads.
*Residue:* the two halves that are about the deployment, not the file — who may call a
new surface and what enforces that **where the code will actually run**, and whether an
error path discloses internals to its caller. No rule running in the test environment
can answer either.

**Lens: the disposal-intent test.** *Mechanized:* nothing, in any language, and not for
want of a rule — the lens's subject is a property of the **diff** (a test added and then
deleted, skipped, or gutted within the same slice), and a linter reads a tree. Its
mechanical counterpart in the kit is the TDD-ordering guard plus `/end-slice`'s
close-out reading, not a linter rule.
*Residue:* all of it, plus the contract half — a test the product contract names as a
pin retires only by contract edit, at halt 3.

**Lens: the unconsumed artifact.** *Mechanized:* dead code, but only the local kind.
Python ruff `F401`, `F811`, the `ARG` family; JS/TS
`@typescript-eslint/no-unused-vars` and tsc's `noUnusedLocals`/`noUnusedParameters`;
C# `IDE0051` and compiler `CS0169`; Go staticcheck `U1000` (golangci-lint's `unused`) —
the widest of the six, since it reaches unexported identifiers across a module; Java
PMD `UnusedPrivateMethod` / `UnusedPrivateField`; Rust rustc `dead_code` and
`unused_imports`, binding under `-D warnings`.
*Residue:* **every rule in that row stops at the public surface**, and the lens's
subject starts there — an endpoint nothing calls, a column nothing queries, a factory
only tests construct. Worse, both a linter and a caller-grep undercount on stacks that
wire consumers by annotation, reflection, or configuration, so a clean run is not a
negative result; the lens's own denominator caveat applies to the rule exactly as it
applies to the grep. Treat these rules as the floor and the arc review as the check.

*One collision this row creates, and it is the kit's own:* every rule listed here fires
on a **deliberately** unused local, which is what a mutation against a counting or
sweeping check has to add — and the edit-time hook runs these rules on the file just
edited, so it rejects the write before the suite runs. Enabling them is still right; the
mutation is written at **module level** instead, where an unused-*variable* rule does not
apply. `commands/end-slice.md` §5 states this at the step that hits it. Recorded here
because this file is where a project decides to turn the rules on, and a rule this
document recommends should not silently block a step this process mandates (field,
2026-09-01 — two blocked attempts in one slice, 53 findings on the first).

**Adopting from this map needs no new proof step.** The *prove the adopted set*
paragraph above is already both proofs at once for a lint rule: the deliberate
violation *is* the state the rule must flag, so the run that shows it firing shows both
that the rule executes and that it catches something — there is no second ceremony to
perform here.

---

## Coverage

Keep the floor in CI, not in the local gate — local runs stay fast, CI stays
authoritative. Record the current figure in `spec/SDLC.md` (*Records*, the
`{{COVERAGE_FLOOR}}` line — `TBD from first CI run` until one exists) so sessions know
it without reading CI config.

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
4. When the floor is first set — or inherited from a project that already claims one —
   prove it fires: set it above the observed number, run the commands CI actually
   executes, and watch the failure, then set the real value (`spec/SDLC.md`,
   *Coverage floor*, states the rule). A threshold bound to a build phase those
   commands never reach passes every reconcile and enforces nothing.

Existing coverage debt is a backlog item, not a merge blocker. Adopting a project at 34%
means the floor starts near 34%.

Two environments disagreeing about coverage is itself a finding — find out why before
adjusting the threshold. The gap is a symptom, not the disease.

## No tooling at all?

If the project has no linter/test runner yet (New Project mode), setting them up IS the
first act of `/sdlc-setup` — a gate that runs green on an empty project is the walking
skeleton everything else builds on. Never defer "we'll add tests later"; the process
does not work without the gate.
