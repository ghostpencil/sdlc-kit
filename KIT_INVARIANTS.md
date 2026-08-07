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

Every `{{PLACEHOLDER}}` in `templates/` (plus the four `{{HOOK_*}}`/`{{SOURCE_GLOB}}`
ones documented in `reference/GATE_RECIPES.md`) must be resolved by a question or step in
`sdlc-setup.md`. This is **not** a name match: when this was measured at B0, only 8 of
the 32 placeholders then present were named verbatim in setup; the rest are asked for in
other words (`{{GATE_LINT_CMD}}` comes from "linter", `{{RUN_COMMAND}}` from "how the
owner will run the app").

**Check:** reading pass that maps each placeholder to the setup step resolving it.
**Specimen:** the literal name-match implementation was tried and produced 24 false
positives out of 32 — a plausible-looking check that was uniformly wrong.

## 4. The exit check covers exactly the instantiated files

Setup's close-out check is `grep -r '{{' CLAUDE.md spec/ .claude/settings.json` — the
files setup instantiates, no more. The installed `sdlc-setup.md` is the **only**
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
pipeline; check the denominator).

**Check:** reading pass, side by side. **Specimen:** none yet — the duplication was
created knowingly in B5 as drift-by-construction, and this invariant is the mitigation
it was created with (plan §8.8).

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
five vendored files are third-party MIT content: each either matches the upstream
verification recorded in `reference/SKILLS.md`, or its divergence is documented there,
and `THIRD_PARTY_NOTICES.md` carries the attributions. The three kit-written files
(`diff-review`, `change-simplify`, `change-verify`, all 2026-08-03) have **no upstream to
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
hook-environment probe, the TDD-ordering guards' proof step and their logging-to-deny
ramp, the exit checks, the coverage-floor establishment proof, the update classifier,
the release workflow's manifest
verification, the `tools/` proof suites, and `/kit-check` itself — must state how it is
proven to **fail**, and is trusted only once it has been made to disagree.
**This list is the check's denominator and goes stale silently**: a check added without
being added here is one the pass will not think to look for. Adding a check means
extending this sentence in the same batch. A check that cannot fail visibly is indistinguishable from
one that passes.

**Check:** reading pass over every specified check. **Specimen:** three checks written
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
