# Kit Invariants

The canonical ledger of what must stay true across this repository's files, and the
specification for `/kit-check` (root `.claude/commands/kit-check.md`), which verifies it.
Kit-development artifact: it lives at the root, beside `FIELD_REPORT.md`, because
invariant 12 forbids kit-development-only files inside `sdlc-kit/` — which is also why
`/kit-check` is a root-repo command that `/sdlc-setup` never installs.

Root `CLAUDE.md` carries a working summary for sessions editing the kit. If the two
disagree, this file wins and the disagreement is itself a finding.

Every invariant below carries a **specimen**: the real defect that motivated it. The
specimen is not decoration — it is the check's negative case. A verification pass for an
invariant is trusted only if it can say what a violation looks like, and the specimen is
that statement (invariant 13 makes this rule an invariant of its own).

---

## 1. Command files state no facts about the adopting project

Commands defer to `spec/SDLC.md`; anything project-variable lives in a template
placeholder, never in command prose. Commands are kit-owned and identical across every
adopting project, so any project fact they state is false somewhere.

**Check:** reading pass over `commands/` (and `skills/`, though vendored
files rarely offend). **Specimen:** `v0.1.0`'s `end-slice.md` asserted *"the typecheck baseline is
green"* — false at every slice close of every red-baseline adoption, shipped and
unnoticed for three slices (field report #1).

**One sanctioned exception: the kit is GitHub-focused, owner-decided 2026-08-05.**
`gh pr create` / `gh pr merge` in `end-phase.md` and `SDLC.template.md`'s phase-end
steps are a tool fact that a GitLab or Bitbucket project would find false. It is a
deliberate scope choice, not drift — the arc-to-PR shape, the release workflow, the
issue templates, and `/sdlc-retro`'s submit-upstream offer are all built on GitHub.
`/kit-check` reports it as a note, not a finding, until the owner widens the scope.

## 2. `SDLC.template.md` is canonical; no command contradicts it

The template's own first paragraph says so: if a command and the SDLC file disagree, the
file is right and the command is the bug. The mirror obligation: any process rule a
command enforces must be stated in the template (see §8 of `IMPROVEMENT_PLAN.md`, note
on #9).

**Check:** reading pass, commands against the template. **Specimen:** the same #1
assertion — it contradicted the template's recorded-baseline rule, and the contradiction
was found by a human noticing two files disagreed.

## 3. Every template placeholder is resolved by setup — semantically

Every `{{PLACEHOLDER}}` in `templates/` (plus the hook and guard ones documented in
`reference/GATE_RECIPES.md` — `{{HOOK_*}}`, `{{SOURCE_GLOB}}`, `{{TEST_PATH_PATTERN}}`,
`{{TEST_CMD_PATTERN}}`, `{{TEST_REPORT_PATTERN}}`, `{{GUARD_EXEMPT_PATTERN}}`) must be
resolved by a question or step in `sdlc-setup.md`. This is **not** a name match: when this was measured at B0, only 8 of
the 32 placeholders then present were named verbatim in setup; the rest are asked for in
other words (`{{GATE_LINT_CMD}}` comes from "linter", `{{RUN_COMMAND}}` from "how the
owner will run the app").

**Check:** reading pass that maps each placeholder to the setup step resolving it.
**Specimen:** the literal name-match implementation was tried and produced 24 false
positives out of 32 — a plausible-looking check that was uniformly wrong.

## 4. The exit check covers exactly the instantiated files

Setup's close-out check is `grep -r '{{' CLAUDE.md spec/ .claude/settings.json` — plus
`README.md` when setup instantiated it (the 0.25.0 human entry point; a pre-existing
README is not setup's to scan), plus the instantiated gate-hook script and guard
dialect(s) for the target CLI, which carry hook placeholders — the files setup
instantiates, no more. The installed `sdlc-setup.md` is the **only**
installed file permitted to carry literal `{{` (it must name placeholders to teach their
resolution); every other installed file stays `{{`-free.

**Check:** `grep -rc '{{' sdlc-kit/commands sdlc-kit/skills
sdlc-kit/reference/REVIEW_LENSES.md` → hits in `sdlc-setup.md` only.
**Specimen:** the check as first shipped grepped all of `.claude/`, which contains the
installed `sdlc-setup.md` — a false positive on every single adoption (plan §8.11).

## 5. Pointers in installed files resolve in the installed world

Every file-and-section pointer in an installed file must name a path and section that
exist in what setup actually installs — not in the kit repo, whose folder is explicitly
optional after setup, and not in a template that instantiates without the named section.

**Check:** reading pass; enumerate pointers, verify each target exists post-setup.
**Specimens:** the plan's own #9 said "add it to the gate section of `CLAUDE.md`" — the
instantiated CLAUDE.md has no gate section (plan §8.1); B4's first draft pointed
`end-slice.md` at `reference/REVIEW_LENSES.md`, a path most adopted repos would not have
had (plan, B4 hand-off).

## 6. Numbered step cross-references stay correct

A "step N" reference between workflow steps is as fragile as a file pointer: inserting a
step renumbers everything after it, silently.

**Check:** `grep -nE 'step [0-9]' sdlc-kit/commands/*.md`, then verify each reference by
reading the target. **Specimen:** B3 inserted New-mode step 4 and stale-ified Existing
mode's "same rules as New mode step 4" — caught only by this grep (plan §8.5).

## 7. The install mapping has one source of truth

The kit-path → installed-path mapping is **defined** by `sdlc-setup.md`'s install list
(New mode step 5; Existing mode step 3 inherits it). Since 0.14.0 the mapping is
**per-CLI and has two destinations**: `commands/` and `reference/REVIEW_LENSES.md` →
`.claude/commands/`, `skills/<name>/` → `.claude/skills/<name>/`, and on Copilot CLI the
commands are packaged instead as `.github/skills/<name>/SKILL.md`. (Before 0.14.0
`skills/` also landed in `.claude/commands/`, which is why the classifiers keep that
prefix; an `agents/` → `.claude/agents/` mapping existed 0.6.0–0.9.0 and was retired with
its only occupant, and the update path still classifies `.claude/agents/`
so the transition can remove it.) Every other statement of the
mapping is derived and must be verified against it: the root README's ownership table
and file tree, the bundle README, root `CLAUDE.md`'s flow diagram, `sdlc-update.md`'s
ownership table, `reference/COPILOT.md`'s mapping table, and — the ones with teeth — the
prefix lists in **both**
classification scripts (`sdlc-update.md` step 3 and the README's update section),
including their denominator checks, which must enumerate every destination directory.
A derived statement that names one CLI's path as though it were universal is a
violation, not a simplification.

**Check:** reading pass; diff each derived statement against the install list.
**Specimen:** installing `REVIEW_LENSES.md` (B4) falsified five derived statements at
once; both classification scripts tried only `commands/` and `skills/` prefixes and
would have classified the installed file `UNKNOWN` — "not from the kit, yours" —
silently exempting it from every future update (plan §8.6).

## 8. The update procedure's two statements agree

The procedure exists twice by design: `commands/sdlc-update.md` (what an adopted project
runs) and the root README's *Updating an adopted project* (what a human reads). Both
define disagreement as a kit bug. They must state the same classification rules, the
same ownership table, and the same traps (hash committed content; never probe with a
pipeline; check the denominator). **The per-release version notes are the exception, and
are not duplicated:** they have one home — step 5 of the command for 0.32.0 onward,
`reference/UPDATE_NOTES.md` for 0.14.0 through 0.31.3 — and the README points there.

**Check:** reading pass, side by side, plus: the README carries no per-release note of
its own. **Specimen:** the README's copy of the 0.31.0 note kept a regeneration-trigger
claim the command's had dropped, fixed in `405a3aa`; 0.37.0 then removed the README's
whole copy of the notes, about 500 lines (`FEATURE_PLAN.md` §86.3). The procedure's
duplication was created knowingly in B5 as drift-by-construction, and this invariant is
the mitigation it was created with (plan §8.8).

## 9. The README file tree matches the filesystem

The root README's tree enumerates every tracked file in the repo; adding, renaming, or
removing one means updating it.

**Check:** compare the tree against `git ls-files` (directory-level entries expand).
**Specimen:** the commit adding `.gitignore` did not update the tree — found by this
check's first real run, in B6 itself.

## 10. `MANIFEST.sha256` is current, and provably discriminates

Every hash matches the **committed** content (LF, `git cat-file -p`) of its file; the
entry count equals `git ls-files sdlc-kit` minus the manifest itself; any commit
touching the bundle regenerates it in the same commit — the release workflow *verifies*
the manifest rather than regenerating it, so a stale one fails the tag push.
Regeneration is proven by discrimination: exactly the edited files change hash, nothing
else does.

**Check:** recompute and diff; count entries. **Specimen:** an all-`UNCHANGED`
classification is exactly what a broken classifier prints — the update script was
trusted only after it flagged the 3 genuinely changed files at `v0.2.0` and no others
(plan §7.2).

## 11. Vendored skills match their recorded provenance

`skills/` holds **two provenance regimes, and the check must not conflate them.** The
six vendored files (across four vendored directories — `tdd/` and its two
`tdd-references/` files count per file, which is the point: the specimen below is one
of them) are third-party MIT content: each either matches the upstream
verification recorded in `reference/SKILLS.md`, or its divergence is documented there,
and `THIRD_PARTY_NOTICES.md` carries the attributions. The two kit-written files
(`diff-review`, `change-verify`, both 2026-08-03) have **no upstream to
verify against** — for them the invariant is the opposite one: they must not be described
as vendored, and `THIRD_PARTY_NOTICES.md` must say the notices do not apply to them.
Attributing kit-written work to a third party is as much a provenance defect as the
reverse.

**Check:** diff against the provenance claims; confirm any edit is noted. **Specimen:**
none yet — the field report's #11 proposed editing `skills/tdd/tdd-references/tests.md`
(then at `skills/tdd-references/tests.md`) and
was rejected precisely because it would have silently invalidated the certification.

## 12. Nothing kit-development-only lives under `sdlc-kit/`

That folder ships verbatim to every adopter and is packaged as the release artifact. The
field report, improvement plan, changelog, this file, and `/kit-check` stay at the root.

**Check:** reading pass over `git ls-files sdlc-kit` — would an adopter be confused or
burdened by this file? **Specimen:** B6 as first written placed this ledger in
`sdlc-kit/reference/` and `/kit-check` in `sdlc-kit/commands/` — setup would have
installed a kit-development command into every adopting project (plan, B6 hand-off).

## 13. Every check states its negative case

Any check this kit specifies or ships — the isolation harness, the edit-time hook, the
hook-environment probe and its dispatch check (the pinned-vs-unpinned probe pair,
CLI version recorded — added 0.24.0 after a wiring shape was measured silently never
firing), the TDD-ordering guards' proof step and their logging-to-deny
ramp, the skill-activation ledger's proof step, the close-out evidence checker and its
setup proof step (four keys as of 0.38.0: `lenses:` joined RED/quality/mutation/verify
fail-closed in 0.27.0, because a lens verdict of `clean` or `no lens triggered`
previously had no durable home — the review hand-back is not retained and only a lens
*finding* travelled onward, so two field arcs could not distinguish a lens that ran clean
from one that never triggered — and `quality:` left with its pass in 0.38.0, its negative
case now a pre-0.38.0 `quality:` line seen to be ignored, single or doubled; the
retired `stop-check` mode's negative case is its stub seen to stay silent at exit 0), the
checker's docs-budget observer (0.26.0 — log-only by
design, so it has no arming ramp and no fire-proof at setup; its negative case is
`tools/close-out-check.py`'s docs corpus and its six mutations, which is where a
budget that stopped discriminating would show), the retro's ledger-alive precheck and its
spec-claims-against-the-tree sweep, the
skills-listing check, the exit
checks, the Existing-mode README run-command read (0.25.0 — a present README's
documented run command read against the owner-verified one; the disagreement surfaced
at the halt is its visible failure), the slice loop's mutation check, the
coverage-floor establishment proof, the
deploy verification, the preserved-contract check and the product-contract
reconcile, the unconsumed-artifact lens's deletion-path contract search, the
retirement step's closing-marker re-read (an entry moved to
`spec/PROJECT_INDEX_HISTORY.md` without its closing marker is pulled back — the
visible failure; as of 0.27.0 it reads a friction line's **disposition** too, so an
entry absorbed with `RULING OPEN` must be seen NOT to retire however old it is), the
backlog's **uniqueness assert** at the phase close (negative case: a duplicated
identifier surfaced by `sort | uniq -d` instead of folded into a silent count), the
retro's **open-ruling sweep** (an absorbed entry with nothing built must be seen to be
reported beside the unabsorbed ones) and its **age-rule upstream re-check** (an aged
entry whose defect the current kit release already fixed must be seen to be
reclassified rather than re-filed), the update
classifier, the release workflow's manifest
verification, the architecture-impact adapter's four-state taxonomy (0.28.0 — its
negative cases live in `tools/impact-check.py`: a graph that will not parse must be
seen to report ERROR rather than a silent COMPLETE, and an un-ignored UA directory
must be seen to write no overlay; 0.33.0 — a graph built inside the change set must be
seen to read current, one built on a sibling branch to read stale, and a tracked
graph directory's own refresh commit must be seen not to count; 0.35.0 — a scan that
fails or cannot run must be seen to report "cannot check" rather than a COMPLETE read
off an empty list, a missing doc must be seen NOT to call for a full rebuild, and a
graph already at HEAD must be seen to skip the slice-end refresh, and `plugin-fix` must
be seen to leave a Claude Code install and every line past the frontmatter
byte-identical, and the hooks it installs on Copilot must be seen to deliver top-level
`additionalContext` from the project's directory, not the plugin's), the hook launchers'
**missing-script stop block**
(0.31.1 — a stop launcher whose script is absent must be seen to block once naming it,
and must be seen NOT to block when `stop_hook_active` is true or when the script is
present; pre- and post-tool launchers must be seen to stay silent), the hooks'
**git-directory resolution through a linked worktree's `.git` file** (0.31.1 — a real
`git worktree add` fixture must be seen to keep state in the worktree's own git
directory, and a `.git` naming no git directory must be seen to guard nothing at
pre-write and to block at stop), the guard's **WSL mount candidate root** (0.31.1 — a
drive-form path under a `/mnt/<drive>/` root must be seen to be production, not
"outside the repository"), the Claude-dialect hooks' **Copilot-payload stand-down**
(0.31.3 — a Copilot-translated payload must be seen to stand down silently on a case
that would otherwise log, gate, or block, and a native Copilot payload and a Claude
payload carrying `timestamp` must be seen still to act), the **docs-only slice's
confirmation** at `/end-slice` step 1 and its verification's docs form (0.32.0 — a
source or test file in the diff must be seen to void the declaration, and a documented
command that fails must be reported broken, never folded into a skip; since 0.34.0 a
source file voids it unless the cosmetic classifier answers exit 0), the **cosmetic
classifier** (0.34.0, `tools/cosmetic-check.py` — a code change, a moved directive, a
parse error, a missing toolchain, a timeout and a broken cache must each be seen to
answer "not cosmetic", and both guard suites must see a real edit still denied and a
crashing classifier still exit 0), the guard patterns' **shell-case-pattern check**
(0.34.0 — `sh -n` on the instantiated shell guard at setup and update;
`tools/tdd-guard-check.py` P2: a spaced `TEST_CMD_PATTERN` must be seen to fail it, and
P1: every row of the recipe's table must be seen to pass it), the **shipped-Python lint
check** (0.34.1, `tools/shipped-lint-check.py` — the 0.34.0 classifier as tagged must be
seen to fail stock ruff, and a planted E741, unused import, malformed `noqa`, syntax
error and unresolvable placeholder must each be seen to fail every shipped file), the
0.35.0 controls — the guards' **runner-report RED rule** (`{{TEST_REPORT_PATTERN}}`:
setup's proof must see one real red counted and one wrapper failure logged "NOT
counted", and both guard suites must see a cut-off report and an invalid pattern
refused), the **never-runs commands** (a reader, `git`, an install or a heredoc that
names the runner must be seen to record nothing either way), the **guard-exempt
pattern** (an exempt write must be seen logged and allowed, and an empty value must be
seen to fail `sh -n`, `tools/tdd-guard-check.py` P3), the **edit-time hook's file scope**
(`tools/gate-hook-check.py` — a dirty file outside the project must be seen silent
beside its checked in-project twin, each check's label seen alone with only its own
output, and the non-blocking note seen at exit 0), the **Copilot commit detector**
(`tools/impact-check.py` — seven commands that only mention a commit must be seen not to
fire), the **scripted mutation runner** (its sha256 assert must fail on bytes not
restored, and the `git diff` after the run stays mandatory because a killed runner
restores nothing), and `/sdlc-update`'s
**friction enumeration** (an entry the release does not address must be seen listed as
`nothing in range`, never dropped), and `/sdlc-update`'s **hook-script walk-through**
(0.35.1 — its helper must be seen to stop, never propose, with `UNRESOLVED` on a
placeholder the target template adds, `NO TARGET` on a tag that is not a release,
`UNCOMMITTED` on a script with local changes, and `NO BASE` on values no release's
template fills; a value read wrong must be seen as a local amendment on its line, a
local patch as a merge conflict, and an unchanged script as `CURRENT`; a re-derived
script whose setup proof fails is restored from `HEAD`. Proven on two adopters' real
0.34.1 scripts, one run with a deliberately wrong values file — not by a `tools/`
suite), the 0.36.0 controls — the helper's **amendment retirement** (`--drop`,
`tools/rederive-check.py`, which runs the helper's text extracted from the command: a
proposal with two of three amendments dropped must be seen to equal the target
template, filled, plus the kept one, a drop the target does not cover must be seen
named `BEHAVIOR CHANGE`, and an unprinted number must be seen to stop it), the
guards' **cosmetic test edit** (both guard suites: a comment-only test edit under a live
red must be seen to keep the red and a refactor licence, and a real one must still be
seen to stale it), and the impact adapter's **phase-scope untracked line**, **gone
files** and **refresh-check count** (`tools/impact-check.py` — an untracked file must be
seen outside the phase denominator, a gone file named and triggering nothing, and the
graph directory's own commit left out of the count), the guards' **outside-the-editor
report** (both guard suites, on a real git repository: a code file written by the shell
must be seen named at the stop and, armed, blocked once, while a file already dirty at
the session's start, a mutation restored to its start content, and a commit dated
before the session must be seen not charged), `/sdlc-update`'s **fold markers**
(`tools/rederive-check.py`: every marker must be seen exactly once in the template, and
a template with one removed must be seen to fail), and the Claude Code launchers' **root
anchor** (`tools/skill-ledger-check.py` since 0.38.0, `tools/close-out-check.py` before
it: from a subdirectory of a linked worktree the ledger launcher must be seen to reach its
script; the case was seen to fail with the anchor removed, exit 127 — once by hand,
2026-10-23, Git Bash on Windows; the suite's exact-launcher case pins it thereafter;
`tools/gate-hook-check.py` pins the anchor on every launcher), the **SDLC state**
(0.39.0: each of the four hook bodies' stand-down, proven in `tools/tdd-guard-claude-check.py`,
`tools/tdd-guard-check.py` and both suites of `tools/gate-hook-check.py` by four cases —
an absent state file guards, `off` stands down silently, `paused` stands down and logs
the unguarded production write, an unknown word guards — and two mutations each, the
stand-down removed and the stand-down widened to an absent file; the helper's own
transitions, `status`, worktree resolution and `off`-while-in-flight refusal in
`tools/sdlc-state-check.py`, with a `set` that does not log and a `resume` that ignores
`stage:` as its mutations) — the
`tools/` proof suites, and `/kit-check` itself — must state how it is
proven to **fail**, and is trusted only once it has been made to disagree.
**This list is the check's denominator and goes stale silently**: a check added without
being added here is one the pass will not think to look for. Adding a check means
extending this sentence in the same batch. A check that cannot fail visibly is indistinguishable from
one that passes.

**Check:** reading pass over every specified check — **except the `tools/` proof
suites, which are RUN and their exit codes quoted.** Reading a suite establishes that
it *states* its negative cases; only running it establishes that it executes, and the
difference is not hypothetical: `tools/skill-ledger-check.py` read as a model proof
through five pre-tag passes while crashing on its first Claude case, leaving one
dialect of one control unexercised across six releases (`FEATURE_PLAN.md` §75, fixed
2026-08-29). **Specimen:** three checks written
in one session returned confident, plausible, wrong answers without erroring — working-tree
hashing (CRLF made all 12 files "drift"), a pipeline probe (missing paths hashed empty
input and "matched"), and the name-match placeholder check (24 false positives). None
prompted a second look, because each produced a plausible result (plan §7.1).

## 14. A recorded value names its enforcing artifact

Any value or state the process records in prose — a floor, a baseline, a status, a
deploy outcome — must name the artifact that enforces or evidences it, and the step
that writes the record must reconcile the two in the same pass (or the record must
state explicitly that it is claim-only). A number in prose is not the number the
machine enforces; writing one without the other is how the two drift.

**One number, one home, and the record names the commit it was measured at** (both
0.29.0). A value restated in a second document is a second thing to update, and it goes
stale in the reader's favour because a stale copy still looks like a record — so the
reconcile searches the whole spec set for the **old** value rather than checking the one
home a bullet happens to name. And a record and its measurement are never simultaneous:
the gate baseline is written `N @ <short-sha>` so the next close can read the drift
instead of assuming there is none.

**Check:** reading pass over `commands/` and `templates/` for every step that records
a value or state; each names its enforcing artifact and its reconcile step, or is
marked claim-only. **Specimen:** TFit's coverage floor — `/end-phase` bookkeeping
recorded 28 → 32 in two prose homes while `gate.yml` silently kept enforcing 28 for
two days (`FIELD_REPORT_2026-07-22.md` finding 1); R2 added that one reconcile, and
this invariant generalizes it (plan §11, G1.5).

## 15. Every verification step names the environment it verifies against

Any step in a shipped command or template that checks, proves, confirms, or accepts
something must name **where** the check runs and whether that place is the one the
claim is about. A claim about production is checked against production configuration;
a command the owner will type is checked in the owner's shell; a number is checked
against the run that produced it. "Verified" without a named environment is a claim
about the checker, not about the thing.

**Check:** reading pass over `commands/` and `templates/` for verbs of verification
(verify, confirm, check, prove, green, accept, ratify). Each occurrence names its
environment, or is one the environment cannot vary for. **Specimen:** an arc that
described a spend cap as dormant in three documents and shipped it enforcing — the
gate was green, and green meant *green in the test environment*, whose conftest
neutralized the very variable the dormancy claim rested on while the deployment
manifest committed it (`FIELD_REPORT_2026-08-01.md` finding 1). Every in-repo signal
agreed with the wrong conclusion because every one of them was measured somewhere
other than production. Four of that report's eight findings are instances of this one
invariant (plan §12, R3.9).

---

## 16. A control's record says whether its trigger occurs on its own

Every install proof this kit prescribes is a **catch**-proof — each says *prove it by
making it fail* — and each one therefore **constructs** the state it catches. That
leaves a question none of them asks: does the workflow ever produce that state by
itself? So the record of a control states three things, not two — installed (where and
in which mode), the catch actually seen (naming what was flagged), and the **reach
note**: whether the flagged state arises in ordinary operation, or was built for the
proof. *"Constructed for the proof; not yet observed arising on its own"* is a
legitimate answer and the useful one, because unlike the two proofs it is a claim a
later close can check. A row recording only that the control executed is not a proof of
anything and must not read as one.

This is invariant 13 pointed one step further out. 13 asks whether a check can be made
to fail; 16 asks whether anything will ever make it.

**Check:** reading pass over every control record `templates/SDLC.template.md` seeds and
every `commands/sdlc-setup.md` step that writes one — each demands the catch by name and
a reach note. A threshold with a prove-it-fires rule is a control too: the coverage
floor's row was a number with no catch until 0.37.1, though its proof was mandatory. **Specimen:** the close-out checker's stop-time backstop. Its setup proof
genuinely catches, because the operator constructs an unpushed commit missing a record
key — but `/end-slice` commits, checks and pushes in one step, so that state essentially
never arises: **96 of 125 stops had an empty window, every one of the other 29 held zero
commits carrying a record, and all 19 flag lines were two bookkeeping commits.** Zero
real catches across the control's entire life, recorded the whole time as installed and
proven (`FIELD_REPORT_2026-08-21.md` finding 5; plan §73.2, fixed in 0.29.0). Recording
its reach made it readable, and the reading retired it: five more field arcs with no catch
and five false candidates (plan §87.3 (iv), retired in 0.38.0).

**The SDLC state stand-down inverts the question (0.39.0, plan §89.9).** Its trigger is
not a rare state the workflow might never produce — it is ordinary operation: every
between-phase session reads `off`, so the stand-down fires constantly and "does the
flagged state arise on its own" is answered yes by construction. What the reach note
must carry instead is whether a stand-down ever **replaced a denial or a licence** — a
`paused:` or `off` window in `guard.log` covering a write the previous release would
have denied or charged, read mechanically from the logs. Until one is seen, the row says
so: *constructed for the proof; value measured against the §89.11 baseline only*.
