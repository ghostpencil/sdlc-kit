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
| Vendored skills (5) | `.claude/skills/<name>/SKILL.md` | the same path — a directory both CLIs read, so one copy serves both |
| Review lenses | `.claude/commands/REVIEW_LENSES.md` | same path — a document, not an executable |
| Gate hook | `.claude/settings.json`, `PostToolUse` | `.github/hooks/sdlc-gate.json`, `postToolUse` |
| Session model pin | `.claude/settings.json` `"model"` | `/model`, or `COPILOT_MODEL` in the environment |
| Read-only sweep agent | built-in `Explore` subagent | `.github/agents/explore.agent.md` |
| Specs | `spec/*.md` | `spec/*.md` — plain files, no mechanism involved |

A repo that answers **both** at the interview gets both columns. Nothing is written
twice: the seven commands exist once per CLI in different formats, the six skill
directories exist once in a shared directory, and every other row is already shared.

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
six skill directories there means a dual-CLI repo carries **one** copy of each skill
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
description: Close a slice — gate, code review, mutation check, commit, PROJECT_INDEX.
---
```

`name` and `description` are required; `license` and `allowed-tools` are optional.
Markdown custom slash commands do not exist on Copilot CLI — the near-miss is real and
tracked upstream (`github/copilot-cli#1113`, closed as a duplicate of `#618`, which is
open), so this packaging step is what a future release deletes if `#618` ships.

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
   and the failure mode is a silently green gate — invariant 15 exactly. The recipe
   therefore sets `timeoutSec` explicitly and states the basis for the number, and the
   generated `spec/SDLC.md` says that a timeout reads as a pass.
3. **The matcher is anchored.** It is compiled as `^(?:PATTERN)$` and must match the
   whole tool name, so the Claude-side `Edit|Write` does not port as a substring match
   — and the tool vocabulary differs anyway (below).
4. **`preToolUse` is the stronger event** — it *can* deny, is fail-closed on error and
   on exit 2, and takes `permissionDecision: allow|deny|ask`. The kit does not use it:
   its gate is a post-edit check, not a pre-approval. Recorded so a later batch does not
   rediscover it and assume it was overlooked.

### Tool names — what is documented, and how to find the rest

The hook matcher tests against `toolName`, and Copilot CLI's tool vocabulary is
under-documented (`github/copilot-cli#3820` asks for exactly this). Provenance of each
name the recipe ships with:

| Name | Evidence | Confidence |
|---|---|---|
| `bash` | the hooks reference's own matcher example, `"bash\|edit"` | documented |
| `edit` | same example | documented |
| `create` | third-party cookbook and an SDK example filtering on it | plausible, unofficial |
| `apply_patch` | same cookbook's post-edit hook | plausible, unofficial |

The recipe ships `edit|create|apply_patch` as a **starting** matcher and proves it the
way the kit proves every other check (invariant 13): a deliberate lint error must
produce hook feedback before the hook is trusted. A wrong matcher therefore fails
loudly at setup time instead of becoming a gate that never fires.

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

## Models and tiers

The kit's vocabulary stays High / Medium / Low by task shape; only the concrete models
differ. On Copilot CLI the available set comes from `/model` (or `/models`), and
`COPILOT_MODEL` sets one from the environment. Setup **asks** the owner to map the
three tiers against that listing rather than proposing model names — the same rule the
gate recipes follow, for the same reason.

**Per-agent model pinning is supported** — the custom-agents *configuration reference*
documents a `model` field ("Model to use when this custom agent executes. If unset,
inherits the default model"), applying to GitHub.com, the Copilot CLI, and supported
IDEs. This corrects an earlier reading of the CLI's how-to page, which lists only
`name`, `description`, and `tools`: the how-to is a subset of the reference, not a
narrower contract. The kit still ships no pinned model in any file it installs — a model
name is a project fact, so if the owner wants the sweep agent pinned to their Low tier,
setup adds `model:` from the recorded policy.

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

### Three authoring hazards, measured on 1.0.77

These bind anything the kit writes that must run on both CLIs, and all three fail
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
| `/code-review` | the owner-typed, billed escalation | GitHub Copilot code review requested on the phase PR |
| `verify` | end-to-end exercise before committing | none |
| `simplify` | post-green refactor pass on the slice diff | none |
| `security-review` | phases touching auth, secrets, input, network | the secure-coding lenses in `REVIEW_LENSES.md`, read by hand |
| `update-config` | editing hook/permission config safely | not needed — see below |

Copilot's own review path is worth knowing: **GitHub Copilot code review** can be
requested on a pull request from the Reviewers sidebar, configured to run
automatically, and — the part that matters here — steered by
`.github/copilot-instructions.md`. Note the interaction with the instructions rule
above: that same file is merged into the CLI's instructions, so anything written there
to steer the PR reviewer is also loaded into every CLI session. Placement is a
deliberate choice, not a free one.

`update-config` needs no equivalent: Copilot's configuration is plain JSON
(`.github/hooks/*.json`, `.github/copilot/settings.json`) that any editor can open
safely.

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
as a silent overwrite.

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

Upstream issues tracked, open as of 2026-08-03: `github/copilot-cli#618` (markdown
prompt files), `github/copilot-cli#3820` (matcher / tool-name documentation).

When any of this is re-verified, update the date and say what moved. A capability table
whose date never changes is a table nobody rechecked.
