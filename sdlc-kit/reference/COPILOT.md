# GitHub Copilot CLI — the translation layer

The process this kit installs is CLI-neutral: phases → slices → TDD cycles, gated by
lint + typecheck + tests, with five owner halt points. What is *not* neutral is where
files go, what the gate hook is called, and which supporting tools exist. This file is
the one place that mapping is stated. `/sdlc-setup` reads it after the owner confirms
the target CLI; nothing else in the kit restates it.

**Everything below is dated evidence, not a durable fact.** Copilot CLI moves fast —
capabilities named here were verified on the dates in *Provenance* at the end, against
GitHub's own docs unless another source is named. Where a claim is unverified or
third-party, it says so in place. Treat an undated claim in this file as a bug.

## Which files this affects

| Concern | Claude Code | Copilot CLI |
|---|---|---|
| Agent instructions | `CLAUDE.md` | `CLAUDE.md` — **read directly, no translation** |
| Kit commands (7) | `.claude/commands/*.md`, user-typed `/name` | `.github/skills/<name>/SKILL.md`, invoked `/name` |
| Kit skills (8: 5 vendored, 3 kit-written) | `.claude/skills/<name>/SKILL.md` | the same path — a directory both CLIs read, so one copy serves both |
| Review lenses | `.claude/commands/REVIEW_LENSES.md` | same path — a document, not an executable |
| Gate hook | `.claude/settings.json`, `PostToolUse` | `.github/hooks/sdlc-gate.json`, `postToolUse` |
| TDD-ordering guards | **not installed** — see *The TDD-ordering guards* below | `.github/hooks/sdlc-tdd-guard.json` + `.sh` (optional) |
| Session model pin | `.claude/settings.json` `"model"` | `/model`, or `COPILOT_MODEL` in the environment |
| Read-only sweep agent | built-in `Explore` subagent | `.github/agents/explore.agent.md` |
| Specs | `spec/*.md` | `spec/*.md` — plain files, no mechanism involved |

A repo that answers **both** at the interview gets both columns. Nothing is written
twice: the seven commands exist once per CLI in different formats, and the eight skill
directories exist once in a shared directory. Three rows are Copilot-only by nature —
the guards, the sweep agent, and the model pin — and the table says so in place rather
than letting a dual-CLI project assume symmetry.

### Why `CLAUDE.md` is not translated — and why `AGENTS.md` is prohibited

Copilot CLI reads `CLAUDE.md` alongside `AGENTS.md`,
`.github/copilot-instructions.md`, and `$HOME/.copilot/copilot-instructions.md`. When
several are present it **combines** them, and the docs state plainly that there is no
general precedence order between them.

So the instantiated `CLAUDE.md` — including its *Runtime Conventions* section — needs
no Copilot equivalent, and setup must **not** write one. A project carrying both
`CLAUDE.md` and a kit-written `AGENTS.md` would load two copies of the same
instructions with no rule for which wins, and the first edit to one of them makes the
project's own instructions self-contradicting in a way nothing reports. Setup emits
exactly one instructions file on either CLI.

This is a prohibition, not an omission. A future batch that "helpfully" adds
`AGENTS.md` for cross-agent compatibility is reintroducing the defect.

### Why the skills live under `.claude/skills/` even on Copilot

`.claude/skills` is one of the three project skill directories Copilot CLI reads
(`.github/skills`, `.claude/skills`, `.agents/skills`) — confirmed first-hand against
1.0.77, where a kit skill placed there is listed under *Project skills*. Installing the
eight skill directories there means a dual-CLI repo carries **one** copy of each skill
rather than two that can drift apart. The Claude-flavoured directory name on a Copilot-only project is
the accepted cost of that; it is a name, and the alternative is a sync surface.

The seven kit commands are the deliberate exception, and go to `.github/skills/` —
which Copilot reads and Claude Code does not. They are user-typed workflow entry
points, not model-invocable skills: installing them where Claude Code lists them as
skills would let `/end-phase` or `/plan-phase` fire unbidden mid-slice. Owner decision,
2026-08-03.

Packaging a command as a skill is mechanical: `.github/skills/<command-name>/SKILL.md`,
the command's markdown body unchanged, with frontmatter added —

```yaml
---
name: end-slice
description: "Close a slice — gate, code review, mutation check, commit, PROJECT_INDEX."
---
```

`name` and `description` are required; `license` and `allowed-tools` are optional. The
description is quoted here deliberately — see authoring hazard 1 below; an unquoted
value that later grows a `: ` drops the whole file with no error.
Markdown custom slash commands do not exist on Copilot CLI — the near-miss is real and
tracked upstream (`github/copilot-cli#1113`, closed as a duplicate of `#618`, which is
open), so this packaging step is what a future release deletes if `#618` ships.

**One command is packaged by hand: `sdlc-setup` itself.** Setup packages the other six
at install time, but it cannot install its own entry point, so the adopter does that one
before the first session — a single file copy on Claude Code, this `SKILL.md` shape
here. Both READMEs carry the procedure; this file is why the two CLIs differ at all.

## The gate hook

The recipe — matcher, payload parsing, timeout, and the proof step — is in
`GATE_RECIPES.md` beside the Claude Code one, and the template it instantiates is
`templates/copilot-hook.template.json`. It is stated there, not here. Four Copilot-only
hazards belong to this file, because they change what the *process* can claim:

1. **`postToolUse` cannot block.** Its only outputs are `modifiedResult` and
   `additionalContext`; the latter is injected as a prepended user message. The kit's
   Claude-side hook exits 2 with stderr, which is also advice to the model rather than
   a hard stop — so the gate is not weakened — but no generated file may say the
   hook's feedback is *blocking* on Copilot. That is what `{{HOOK_FEEDBACK_NOTE}}`
   exists to keep honest.
2. **A hook that times out is treated as a pass.** `timeoutSec` defaults to 30, and a
   timed-out hook surfaces a warning and lets the tool call proceed. The kit's hook
   runs lint *and* typecheck; 30 seconds is not a generous budget for a cold typecheck,
   and the failure mode is a silently green gate — a check that verifies nothing while
   reading as one that passed. The recipe
   therefore sets `timeoutSec` explicitly and states the basis for the number, and the
   generated `spec/SDLC.md` says that a timeout reads as a pass.
3. **The matcher is anchored.** It is compiled as `^(?:PATTERN)$` and must match the
   whole tool name, so the Claude-side `Edit|Write` does not port as a substring match
   — and the tool vocabulary differs anyway (below).
4. **`preToolUse` is the stronger event** — it *can* deny, is fail-closed on error and
   on exit 2, and takes `permissionDecision: allow|deny|ask`. The **gate hook** does not
   use it: the gate is a post-edit check, not a pre-approval, and that is deliberate.
   The optional TDD-ordering guards below are the one thing in the kit that does, which
   is exactly why they are optional, ramped, and proven before they are trusted.

### Hook capabilities on record — and the two the guards now build on

Verified against the hooks reference 2026-08-05, recorded so a later batch starts from
dated facts instead of re-research. The first two stopped being reference material that
day: the TDD-ordering guards below are built on them, and their **output schemas were
measured on the bench** rather than taken from the docs, which do not state them —

- **`preToolUse` denies with**
  `{"permissionDecision":"deny","permissionDecisionReason":"…"}` on stdout. Observed:
  the write did not happen and the session was shown the reason verbatim.
- **`agentStop` blocks with** `{"decision":"block","reason":"…"}`. Observed: the session
  continued under a forced continuation, and the next stop arrived carrying
  `stop_hook_active: true` (snake_case, as sent).

A denial that does not deny is the failure mode worth naming here, because nothing
reports it: the hook exits 0, the CLI ignores an unrecognised payload, and the guard's
log says it denied while the write went through. Both schemas above were confirmed by
reading the transcript for the *effect*, not by the hook's own claim.

- **`preToolUse`'s fail behavior is asymmetric: closed on a command error, open on a
  timeout.** The reference is explicit that a timed-out hook lets the tool call
  proceed *even for `preToolUse`*. Hazard 2's arithmetic therefore applies to any
  future pre-hook too: a guard that outruns its `timeoutSec` silently stops guarding,
  which is why a guard script must stay cheap — state reads and writes, never running
  a suite inline.
- **`agentStop` can block a session from stopping**, with a documented cap of eight
  consecutive blocks. Its input carries a `stop_hook_active` flag telling the hook it
  is already inside a forced continuation — a well-behaved hook reads the flag rather
  than fighting the cap.
- **`userPromptTransformed` can rewrite the model-facing prompt** — mutation only; it
  cannot block.

### Tool names — what is documented, and how to find the rest

The hook matcher tests against `toolName`, and Copilot CLI's tool vocabulary is
under-documented (`github/copilot-cli#3820` asks for exactly this). **Measured on the
bench 2026-08-05 against 1.0.77 on Windows 11**, by the discovery procedure below —
these observations supersede the documentation and the third-party sources for every
name they cover:

| Name | Evidence | Confidence |
|---|---|---|
| `apply_patch` | **measured** — fires for both the create and the edit flow | observed 2026-08-05 |
| `powershell` | **measured** — the shell tool on Windows | observed 2026-08-05 |
| `view` | **measured** — the read tool | observed 2026-08-05 |
| `bash` | the hooks reference's own matcher example, `"bash\|edit"` | documented, **not observed** |
| `edit` | same example | documented, **did not fire** on the tested flows |
| `create` | third-party cookbook and an SDK example filtering on it | plausible, **did not fire** |

Three traps this measurement exposed, each of which would have shipped silently:

1. **The UI label is not the tool name.** Copilot displays "Edit" while the hook name is
   `apply_patch`. A matcher written from what the session shows you never fires.
2. **The documented names are the ones that did not fire.** `edit` and `create` come
   from GitHub's own example; on 1.0.77 neither appeared for any file write. The recipe's
   `edit|create|apply_patch` worked by its third alternative only — it would have looked
   deliberate and been accidental.
3. **`apply_patch` does not deliver JSON.** Its `toolArgs` is raw patch text
   (`*** Begin Patch` / `*** Add File: <path>`), not the JSON-encoded string every other
   tool sends. The 0.15.0 hook body JSON-parsed `toolArgs` unconditionally, so on the
   only write tool that actually fires it fell to its no-path branch and **never ran the
   gate on any edit**. Fixed in 0.16.0 by parsing the patch text for its touched paths;
   the instantiated hook is project-owned, so adopted projects need the changelog fix
   applied by hand.

A fourth thing this section used to get wrong by omission: **the loud-when-it-cannot-run
behaviour was never a Copilot property**, it was just the only dialect that had it. The
Claude Code hook exited 0 and checked nothing whenever it could not find a path — a
silently green gate in the kit's own file. 0.16.0 gives that dialect the same loudness
(stderr + exit 2). Both are now proven by the same suite, and neither can go quiet
without saying so.

The recipe still proves the matcher the way the kit proves every other check — trusted
only once made to fail: a deliberate lint error must produce hook feedback. That proof
is what caught trap 3, and it is why a wrong matcher fails loudly at setup time instead
of becoming a gate that never fires.

**Discovery procedure, for when the proof fails.** Register a matcher-less
`postToolUse` hook that appends its input to a file, edit one source file, then read
the real vocabulary off the log:

```json
{ "version": 1, "hooks": { "postToolUse": [
  { "type": "command", "bash": "cat >> /tmp/copilot-hook-probe.jsonl", "timeoutSec": 10 }
] } }
```

The same log answers the second unknown: **which field of `toolArgs` holds the edited
file path**. `toolArgs` is delivered as a JSON-encoded *string* (the docs' own example
is `"toolArgs":"{\"command\":\"ls\"}"`), so it is parsed in two steps, and the key
inside it is documented for no tool. The recipe tries the plausible keys and reports
loudly when none matches, rather than exiting quietly — a hook that cannot find the
file it was called about is indistinguishable from a clean edit, and that is the
failure this kit's field reports keep finding.

### Version floor

Post-tool-use matcher support is reported fixed in Copilot CLI **v1.0.63** — a
third-party source, uncorroborated by GitHub's docs, and the only version claim in this
file. Setup reads `copilot --version` and says plainly if the installed CLI is older,
rather than installing a gate that cannot fire. Same treatment as any other
environment-dependent claim: state where it was checked, or do not make it.

## The TDD-ordering guards, and why they are Copilot-only

The field finding that motivated them is a Copilot property: **on Copilot CLI a skill is
a prompt, so presence is not process.** The kit's highest-risk steps — write the test
first, do not stop while red — were specified in files the model may or may not honour.
The guards give those two steps a deterministic backstop. The recipe, the placeholders,
the ramp and the proof step are in `GATE_RECIPES.md`; what belongs here is the dialect
decision and its evidence.

**They ship for Copilot CLI only, and the Claude Code port is deferred, not declined.**
Claude Code has the matching events — a `PreToolUse` hook can deny, a `Stop` hook can
block — so the port looks like a translation exercise. It is not, and the reason is the
same one that made the Copilot guards take a bench run: **the guard's whole mechanism
rests on two payload facts, and Claude Code's documentation settles neither** (checked
against the hooks reference, 2026-08-05):

1. **Whether a shell command's exit code is available to `PostToolUse`, and in what
   form.** The docs give no `PostToolUse` input example and do not state what
   `tool_response` carries for the Bash tool. G1 and G2 both turn on observing a test
   run's exit status; on Copilot this resolved into a *text trailer* parse, which no one
   predicted from the docs.
2. **Which field of a file-write's `tool_input` holds the path.** The docs document no
   input schema for `Edit` or `Write`. On Copilot the equivalent assumption — that the
   write tool sends JSON — is exactly what broke the gate hook for a whole release.

Two more are unstated: whether Claude Code's Stop input carries a `stop_hook_active`
flag (the guard's stand-down depends on it) and whether a consecutive-block cap exists.
And the timeout semantics are ambiguous in the one direction that matters — the docs do
not say whether a timed-out `PreToolUse` fails open or closed.

Writing the port from those gaps would mean shipping a guard whose failure mode is
silence, into the CLI where the kit's users would trust it most. The kit's own rule
applies unchanged: **only a bench answers this.** A Claude Code port is a future batch
whose first step is a probe run, pre-registered before any code is written: log a real
`PostToolUse` payload for a deliberately failing test command, and a real `PreToolUse`
payload for an `Edit` and a `Write`, and design the state machine from what they
actually contain rather than from what the documentation implies.

Two Claude-side facts *are* documented and worth carrying into that batch: hooks get
`$CLAUDE_PROJECT_DIR` for portable path resolution, and the Windows shell is stated
(Git Bash, with a per-hook `"shell"` key) rather than left to `PATH` — so the WSL hazard
in `GATE_RECIPES.md` is a Copilot-side problem specifically, and the Claude port would
not need the self-locating prelude.

The generated `spec/SDLC.md` says which CLI the guards run on — a verification step has
to name the environment it verifies against, and a dual-CLI project must not read a
Copilot-only backstop as covering both.

## Models and tiers

The kit's vocabulary stays High / Medium / Low by task shape; only the concrete models
differ. On Copilot CLI the available set comes from `/model` (or `/models`), and
`COPILOT_MODEL` sets one from the environment. Setup **asks** the owner to map the
three tiers against that listing rather than proposing model names — the same rule the
gate recipes follow, for the same reason.

**Routing is operator-performed on Copilot.** No file the kit installs can set the
model for a session or a command: kit files carry no `model:` (authoring hazard 2 — a
Claude model name is downgraded to `auto` with a warning, and a model name is a
project fact besides), and skill frontmatter has no documented `model` field at all —
the CLI skills page documents `name`, `description`, `license`, and `allowed-tools`
only (checked 2026-08-05); only custom agents document `model` (below). The levers are
therefore the operator's three: `/model` in-session, `COPILOT_MODEL` in the
environment for a scripted run, and a per-agent `model:` pin on
`.github/agents/explore.agent.md` if the owner wants the sweep agent held to the Low
tier. The generated `spec/SDLC.md` names which commands run at which tier and
instructs the operator to set the model **before** a High-tier command —
`/plan-phase`, `/end-phase`, and `/end-slice`'s review at minimum; the escalation is
manual, and the CLI's low execution visibility (a session does not announce which
model served each turn) is a CLI property the kit can report around but not fix. A
field run on 0.14.0 paid for the un-named version of this in manual mid-arc
overrides; the recorded tier mapping, the setup question that states what `auto`
forfeits, and the operator step in `SDLC.md` are the response.

**Per-agent model pinning is supported** — the custom-agents *configuration reference*
documents a `model` field ("Model to use when this custom agent executes. If unset,
inherits the default model"), applying to GitHub.com, the Copilot CLI, and supported
IDEs. This corrects an earlier reading of the CLI's how-to page, which lists only
`name`, `description`, and `tools`: the how-to is a subset of the reference, not a
narrower contract. The kit still ships no pinned model in any file it installs — a model
name is a project fact, so if the owner wants the sweep agent pinned to their Low tier,
setup adds `model:` from the recorded policy. **Measured on the bench 2026-08-05, and
the two halves differ:** an agent pinned `model: claude-sonnet-4.5` **executed on that
model** while the session default was `gpt-5.3-codex` (the CLI's own transcript labelled
the turn `Pin-probe(claude-sonnet-4.5)`) — so per-agent pinning is honoured in practice,
not merely documented. A skill carrying `model:` **loads and fires normally but the turn
stays on the session model**: the undocumented field is silently ignored rather than
rejected, which is the worst of the three possible behaviours, because the file looks
like it is routing and is not.

So a Copilot-only project may pin `.github/agents/explore.agent.md` to the owner's Low
tier if they ask. Skills remain off the table because the field does nothing there, and
dual-CLI projects remain off the table regardless, since one CLI's model name is the
other's downgrade warning. The operator levers above are still the load-bearing
mechanism for everything else.

## Subagents and sweeps

Custom agents are `.github/agents/*.agent.md` (project) or `~/.copilot/agents/`
(personal, wins on a name collision), invocable via `/agent`, by name, by inference
from the description, or `copilot --agent NAME --prompt`. Hooks exist for
`subagentStart` / `subagentStop`, so subagents are first-class.

The kit's read-only sweep agent — used by `/plan-phase`'s gap analysis and
`/sdlc-setup`'s Existing-mode survey, where Claude Code uses its built-in `Explore` —
ships as `templates/explore.agent.template.md` → `.github/agents/explore.agent.md`.

**Frontmatter, from the custom-agents configuration reference.** `tools` takes a YAML
array or a comma-separated string; omitted (or `["*"]`) means every tool, and `[]` means
none. The built-in aliases are `execute` (run a shell command), `read`, `edit`, `search`,
`agent` (invoke another custom agent), `web`, and `todo`. Read-only is therefore
`tools: ["read", "search"]` — the restriction the kit's profile ships with. Also
available: `model` (above), `target` (`vscode` / `github-copilot`, defaulting to both),
`user-invocable`, and `disable-model-invocation` — the last of which is described in
cloud-agent terms, so do not assume it governs the CLI.

**A trap worth naming: these aliases are not the hook's tool names.** The agent
reference calls the shell tool `execute`; the hooks reference's matcher example calls it
`bash`. `edit` appears in both, which is what makes the mismatch easy to miss. Do not
derive a hook matcher from this list — use the provenance table and discovery procedure
above.

**Parallel fan-out is still undocumented.** Where the kit's sweeps would fan out, they
run serially on Copilot. The generated `spec/SDLC.md` says so — a sweep that quietly
became serial is a sweep whose coverage nobody re-checked. Measured against 1.0.77, the
raw capability *is* present — `task`, `list_agents`, `read_agent` and `write_agent` are
builtin tools, and delegation to a named custom agent succeeds — but no *subagent type*
equivalent to Claude Code's `general-purpose` exists; only agents defined in
`.github/agents/` or supplied by a plugin can be named. A skill that spawns
`general-purpose` by name does nothing here.

### Four authoring hazards, measured on 1.0.77

These bind anything the kit writes that must run on both CLIs, and all four fail
**silently** — which is what makes them worth a section rather than a footnote.

1. **A `: ` inside an unquoted frontmatter value drops the whole file.** Copilot's YAML
   frontmatter parser is stricter than Claude Code's. A plain scalar containing a
   colon-space — easily introduced by an embedded example like `user: "do the thing"` —
   makes the document unparseable, and the agent or skill simply does not appear. There
   is no install warning and no listing error; the loss is visible only by asking for a
   name that does not exist and reading which names *do*. Specimen: of
   `pr-review-toolkit`'s six agents, exactly the one with a colon-space in its
   description failed to load. **Quote the value or use a block scalar**, and check new
   frontmatter with `copilot skill list` before shipping it.
2. **`model:` naming a Claude model is downgraded, not honoured.** Copilot warns that
   the model "is not available" and proceeds on `auto`. Kit files that must run on both
   CLIs carry no `model:` at all; the model policy is recorded in `spec/SDLC.md` and
   applied by the owner.
3. **Tool names differ, and `--available-tools` silently overrides `--allow-tool`.**
   Copilot's builtins are `powershell` (not `bash`), `view` / `create` / `edit` (not
   `Read` / `Write` / `Edit`), plus `grep`, `glob`, `skill`, `task`, `web_fetch`, and a
   `github-mcp-server-*` subset. Restricting `--available-tools` without including
   `powershell` removes shell access no matter what `--allow-tool 'shell(git diff)'`
   says, and the session reports a *reasoning* limitation rather than a permission
   error — the failure looks like a bad answer, not a bad flag.
4. **A skill that asks for an action can get a report of that action instead — so
   demand the artifact, not the action.** Measured while building `change-verify`
   (2026-08-03), across four runs on the same fixture. Told to exercise a change, the
   session answered without a single tool call; told more firmly that it *must* execute,
   it produced a confident report claiming `exit code 0` on a command that in fact
   throws `TypeError` — the pressure to act converted into a claim of having acted. What
   fixed it was not more insistence but a **checkable output contract**: require the
   exact command, the literal bytes it printed, and the exit code, in a fenced block per
   run, and say that characterizing output ("clean exit", "expected result") is itself
   the tell. The next run made real tool calls and caught the defect. The general rule
   for kit skills: **an instruction to do something is unenforceable; an instruction to
   produce evidence that could only exist if it was done is enforceable.** Prefer the
   second wherever a skill's value depends on it actually running something.

## What the kit loses on Copilot today

Stated plainly, because a translation layer that hides its gaps is worse than one that
does not exist. As of this file's date, no Copilot equivalent is installed for:

**The review apparatus left this table in 0.14.0.** It was the largest entry: the kit's
per-slice and whole-arc reviews named `pr-review-toolkit`, a Claude Code plugin, so a
Copilot adopter was instructed to run a reviewer that did not exist for them. The kit
now ships its own — `diff-review`, installed to `.claude/skills/`, which both CLIs read
— and it names no CLI-specific agent, tool, or model, so both CLIs run the same
reviewer. `pr-review-toolkit` survives only as an optional Claude-Code-only deepening
at phase end, and nothing requires it.

The measured caveat behind that decision is worth keeping: `pr-review-toolkit` *can*
be made to install and run on Copilot CLI, but only via `copilot plugin install
<owner>/<repo>:<path>`, which Copilot's own output announces as deprecated in favour of
marketplace installs — and the marketplace route currently fails on the Claude
marketplace's manifest. A capability reachable only through a path its vendor has
announced it is removing is not one to build a process on.

| Missing | What the kit uses it for | Available substitute today |
|---|---|---|
| `/code-review` | the owner-typed, billed escalation | GitHub Copilot code review requested on the phase PR — owner-driven, and the kit does not configure it; see below |
| `verify` | end-to-end exercise before committing | **closed in 0.14.0** — the kit-written `change-verify`, named by `/end-slice` step 6 and `/end-phase` step 2 |
| `simplify` | post-green refactor pass on the slice diff | **closed in 0.14.0** — the kit-written `change-simplify`, named by `/end-slice` step 3 |
| `security-review` | phases touching auth, secrets, input, network | the secure-coding lenses in `REVIEW_LENSES.md`, installed to `.claude/commands/` and named by `/end-slice` — no longer read by hand |
| `update-config` | editing hook/permission config safely | not needed — see below |

Only the first row is still a real loss, and it is the one the kit never required. Two
rows closed in 0.14.0 the way the review row did: the kit wrote its own portable
version rather than describing a substitute it does not install. Those two are
kit-written and named nowhere in Claude Code's built-in set — deliberately, so that
installing them shadows no built-in (`reference/SKILLS.md`, provenance).

`update-config` needs no equivalent: Copilot's configuration is plain JSON
(`.github/hooks/*.json`, `.github/copilot/settings.json`) that any editor can open
safely.

### `/code-review`, and why setup does not write `.github/copilot-instructions.md`

Copilot's own review path is worth knowing: **GitHub Copilot code review** can be
requested on a pull request from the Reviewers sidebar, configured to run
automatically, and — the part that would matter here — steered by
`.github/copilot-instructions.md`.

**`/sdlc-setup` does not write that file. This is decided, not pending.** The reasoning,
recorded so a later batch does not helpfully add it:

1. **It is a second instructions file, which the kit prohibits.** Copilot CLI merges
   `CLAUDE.md`, `AGENTS.md`, `.github/copilot-instructions.md`, and
   `$HOME/.copilot/copilot-instructions.md` with **no defined precedence order** — the
   same finding that made setup emit exactly one instructions file and decline to emit
   `AGENTS.md`. Anything written there to steer a PR reviewer is also loaded into every
   interactive session, unranked against `CLAUDE.md`.
2. **What it would steer is the one thing the kit deliberately does not own.**
   `/code-review` is the owner-typed, billed escalation on either CLI. No command
   invokes it, `/end-slice` names it only to say it is *not* the review step, and
   `/end-phase` offers it as an optional deepening. Taking on a permanent every-session
   instructions cost to tune an optional out-of-band pass is a bad trade in the one
   direction that is hard to reverse.
3. **The kit's reviewers already carry the standards that file would restate.**
   `diff-review`'s Standards axis reads `CLAUDE.md` *Runtime Conventions* directly. A
   `copilot-instructions.md` written by setup would be a second copy of rules that
   already exist in the file both CLIs read — and a second copy with no precedence rule
   is the failure this whole section is about.

**An adopter who wants it should write it themselves.** It is a project-owned file, the
kit will not create or overwrite it, and `/sdlc-update` treats it as project-owned like
`.claude/settings.json`. Worth knowing before you do: keep it to PR-review guidance that
is harmless when loaded into an interactive session, because it will be.

## Updating a Copilot project

`/sdlc-update` treats the Copilot-side artifacts exactly as it treats the `.claude/`
set — with one adjustment the packaging forces. The seven packaged skills are *not*
byte-identical to any bundle file: each is a frontmatter block plus the kit command
verbatim. So the update strips that block and compares the remainder against the
manifest's `commands/<name>.md` entry, which is why setup's packaging shape is specified
exactly and inserts nothing else. `.github/agents/explore.agent.md` needs no such
handling — it copies its template verbatim, placeholders being absent.

The gate hook is **project-owned**, like `.claude/settings.json`: it holds the project's
own lint and typecheck commands, so an update never rewrites it. A release that changes
the hook recipe reaches an adopted project as a changelog entry the owner applies, not
as a silent overwrite. The two TDD-guard files are project-owned for the same reason and
on the same terms — `sdlc-tdd-guard.sh` carries the project's test patterns, and its
`.json` is left alone with it.

That ownership has a cost worth stating plainly, because 0.16.0 is the first release to
pay it: the `apply_patch` fix to the gate-hook recipe is a **real defect fix that no
adopted project receives by updating**. `/sdlc-update` reports the recipe changed and
the owner re-applies it by hand; until they do, a Copilot project's gate hook has never
run on a single edit.

One more way a skill file can mutate outside `/sdlc-update`: the `gh skill` extension
injects provenance frontmatter into `SKILL.md` on install, and its `update` compares
tree SHAs against an upstream that is not the kit. The full note is in
`reference/SKILLS.md` — it is CLI-neutral (the extension targets six agents including
Claude Code), not a Copilot hazard; it is named here only because this file is where
update expectations live. (Verified 2026-08-05.)

Which of this applies is recorded rather than sniffed: `/sdlc-setup` writes the project's
agent CLI into `spec/PROJECT_INDEX.md`, and `/sdlc-update` reads it there.

## Considered and declined: shipping the kit as a plugin

Copilot CLI reads a `marketplace.json` from `.github/plugin/` **or `.claude-plugin/`**,
`copilot plugin install` accepts a marketplace, a GitHub repo, a Git URL, or a local
path, and `plugin.json` can declare `agents`, `skills`, `commands`, `hooks`,
`mcpServers`, `lspServers`, and `extensions`. The whole kit could therefore ship as one
installable plugin instead of files that `/sdlc-setup` copies into place.

Declined: it is a second install path to maintain and to keep in step with
`/sdlc-update`, and copying files into the repo is what makes the installed process
travel with a `git clone`. Recorded because the option is not obvious and someone will
otherwise rediscover it as a proposal.

The same finding has a second edge worth stating: that `.claude-plugin/` is a
documented Copilot location does **not** mean a Claude Code plugin runs on Copilot.
Reading a manifest layout is not executing its contents.

## Detecting the target CLI

`/sdlc-setup` proposes an answer and the owner confirms it; this table is what the
proposal is built from. Signals are **positive-only**: the absence of one CLI's marker
is never evidence of the other.

| Strength | Signal | Reads as |
|---|---|---|
| Strong | `CLAUDECODE=1` (also `CLAUDE_CODE_ENTRYPOINT`, `CLAUDE_CODE_SESSION_ID`) | setup is running inside Claude Code |
| Bonus | `AI_AGENT` — **prefix match only** | whichever CLI the prefix names |
| Medium | `.claude/settings.json`, `.claude/commands/` | repo already set up for Claude Code |
| Medium | `.github/hooks/`, `.github/agents/`, `.github/copilot-instructions.md`, `.github/copilot/settings.json` | repo already set up for Copilot CLI |
| Weak | `claude` / `copilot` on `PATH` | installed on this machine; says nothing about this repo |

Three traps, each of which has already caught someone:

- **Copilot CLI stamps no session marker.** Its documented environment variables —
  `COPILOT_GITHUB_TOKEN`, `GH_TOKEN`, `GITHUB_TOKEN`, `COPILOT_HOME`, `COPILOT_MODEL` —
  are every one of them user-set configuration or auth. A developer who exported
  `GITHUB_TOKEN` in a shell profile trips that test from inside Claude Code; a Copilot
  user who authenticated with `/login` may trip none of it. There is no strong signal
  for Copilot, so its detection rests on the repo artifacts and `PATH`.
- **`AI_AGENT` is a proposed convention, not an implemented standard**, promoted by a
  third-party detector that does not claim the tools set it. Match it by prefix: the
  value observed in the session that verified this was `claude-code_2-1-220_agent`,
  while the convention's documented form is `claude-code`. An equality test would have
  failed against the very session that produced it.
- **`CLAUDE.md`, `AGENTS.md`, and `.claude/skills/` discriminate nothing.** All three
  are read by both CLIs. Only the files in the table above are evidence.

Absent or conflicting evidence is not a tiebreak to guess at — setup asks open-ended.

## Provenance

GitHub documentation, fetched and verified **2026-08-03** unless noted: the hooks
reference (payload, output contract, config schema, matcher anchoring, `timeoutSec`);
*Using hooks with GitHub Copilot CLI* (`timeoutSec` default, the `toolArgs`-as-string
example); *Using hooks with Copilot CLI for predictable, policy-compliant execution*
(the two-step `jq` parse); CLI custom instructions; CLI add-skills; create custom agents
for the CLI **and the custom-agents configuration reference** (the frontmatter fields,
the `tools` syntax, and the built-in tool aliases — the reference is the fuller of the
two and corrects the how-to); the CLI command reference; the CLI plugin reference;
Copilot code review.

Named non-GitHub sources, each cited in place above and **not** corroborated by GitHub's
docs: a third-party Copilot CLI cookbook (the `create` / `apply_patch` tool names, the
v1.0.63 matcher floor) and `vercel/detect-agent`, MIT (the `AI_AGENT` convention and the
Copilot auth-variable detection this file declines to use).

Re-verified **2026-08-05**, same sources unless named: the hooks reference (the
`preToolUse` timeout asymmetry, `agentStop`'s eight-block cap and `stop_hook_active`,
`userPromptTransformed` — the *Hook capabilities on record* section above); the CLI
skills page (SKILL.md frontmatter documents no `model` field — *Models and tiers*);
GitHub's changelog, 2026-04-16 entry (`gh skill install`/`update` frontmatter
injection — repository, ref, tree SHA).

**Measured on the bench 2026-08-05** — Copilot CLI 1.0.77, Windows 11, fixture repo
`copilot-ci-test`, captured payloads retained. These are first-hand observations, and
where they disagree with a documented or third-party claim above, they win and the row
says so: the tool-name vocabulary (`apply_patch` / `powershell` / `view`, and the
non-firing of `edit` and `create`); `apply_patch`'s `toolArgs` being raw patch text;
`postToolUseFailure` **never firing** for a shell command that exits non-zero, which
instead arrives as `postToolUse` with `resultType: "success"` and a
`<shellId: N completed with exit code M>` text trailer; the `preToolUse` deny and
`agentStop` block output schemas; `agentStop` firing in `-p` mode with snake_case
`stop_hook_active`; hook `bash` resolving to WSL bash on a Windows machine, with both
the fail-open-on-timeout and fail-closed-on-error behaviours observed live; and
per-agent `model:` being honoured while skill `model:` is ignored.

Upstream issues tracked, open as of 2026-08-03: `github/copilot-cli#618` (markdown
prompt files), `github/copilot-cli#3820` (matcher / tool-name documentation).

When any of this is re-verified, update the date and say what moved. A capability table
whose date never changes is a table nobody rechecked.
