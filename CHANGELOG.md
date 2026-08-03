# Changelog

Kit-scoped, semver-ish. Versions describe **the kit**, not any project that adopted it.
This file is repo documentation and is not shipped inside `sdlc-kit/`; the bundle carries
its version in `sdlc-kit/VERSION`.

An entry marked **[installable]** changes a file an adopted project holds
(`commands/**`, `skills/**`, `agents/**`, `reference/REVIEW_LENSES.md`) and therefore
matters at update time. Entries marked **[adoption-only]** change `templates/**` or the
non-installed reference docs, which are read at `/sdlc-setup` time and never re-applied
to an already-adopted project.

## 0.13.0 — 2026-08-03

The STD batch: the kit's first product-quality standards — logging, error handling,
secure coding — last of the owner-ordered LEG → COP → STD queue (`FEATURE_PLAN.md`
§18, built as §22), in the shape the first field report taught: checks that fail
loudly, not prose rules. Owner decisions honored: secure coding ships as review
lenses, not a command; conventions ship as setup interview + project-owned record +
lenses + gate rules where mechanical. Two new template placeholders
(`{{LOGGING_CONVENTIONS}}`, `{{ERROR_CONVENTIONS}}`), taught to setup in the same
release; no new files; no halt-point changes.

### Added
- **[adoption-only]** `CLAUDE.template.md` gains a *Runtime Conventions* section —
  how the project's code logs and fails, recorded at setup, each bullet noting which
  parts are mechanically enforced (linter rule IDs) versus review-only. A convention
  changed without its linter rule is a claim, not a control.
- **[installable]** `sdlc-setup.md`: the **runtime-conventions ask** (New mode
  Round 3) — how the software logs (framework, level meanings, what may never be
  logged) and how it fails (fail fast or degrade, wrapping at boundaries, whether
  blind catches are ever acceptable), then the matching gate rules proposed for the
  chosen toolchain, with one adopted rule's violation included in the hook
  verification. Existing mode **discovers first** (frameworks imported, level usage,
  bare/blind-catch count, which rules the linter config already enables) and
  proposes with each rule's measured current violation count — new-rule violations
  land in the measured gate baseline, never a setup-time fix spree.
- **[installable]** `reference/REVIEW_LENSES.md`: three lenses — **logging and
  swallowed errors** (every new handler names where the signal goes; the level is a
  routing decision checked against the recorded conventions; one failure, one
  ERROR), **untrusted input** (name every interpreter the input reaches and the
  mechanism neutralizing it there; canonicalize-then-prefix-check paths built from
  input; deserializers that can execute are not for untrusted data), and **secrets
  and exposure** (a secret has exactly one home; a new surface names its enforcing
  control as configured where the code actually runs; error output to a caller is a
  disclosure decision). The file states their provenance: shipped as standards, not
  from a field catch — each enters the audit regime individually.
- **[adoption-only]** `reference/GATE_RECIPES.md` gains **Runtime-standards rules**:
  per-linter rule sets (ruff `E722`/`BLE001`/`B904`/`T20` + the bandit `S` family;
  eslint `no-console`/`no-empty`/`no-eval` kin + `no-floating-promises`; .NET
  `latest-recommended` analyzers; golangci-lint `errcheck` + `gosec`; checkstyle
  `EmptyCatchBlock`/`IllegalCatch`; clippy `unwrap_used`/`expect_used`/
  `print_stdout`). Rules live in the linter's own config, so the existing gate and
  edit-time hook enforce them with no new command, proven the way the hook is
  proven: one deliberate violation must fail the lint run.

### Changed
- **[adoption-only]** `SDLC.template.md` slice-loop step 6 and **[installable]**
  `end-slice.md` §3: the lens-trigger summary now also fires when the slice added a
  catch or failure path, took in outside data or passed it to an interpreter, or
  touched credentials or an externally reachable surface.

### Fixed
Seven pre-existing defects caught by the release `/kit-check` (all older than this
batch; invariants 2, 3, and 5):
- **[installable]** `end-phase.md` acceptance-review note told the session to fix a
  run command proven broken in the owner's shell in `CLAUDE.md` only, leaving
  `spec/SDLC.md`'s halt-4 line naming the broken command — it now names both homes.
- **[adoption-only]** `SDLC.template.md` halt 5 now carries the reviewer-routing
  clause `end-phase.md` already shipped (a team may route merge approval through a
  human PR reviewer, recorded in the project's `spec/SDLC.md`) — the rule existed
  only in the command, and the template is canonical.
- **[adoption-only]** `PROJECT_INDEX.template.md`: the Phase block now carries a
  coverage-floor line. `/end-phase` and `SDLC.template.md` both assert the floor
  recorded in `spec/PROJECT_INDEX.md` matches the workflow value — against a
  template that had no such field, making a "not done until they are" step
  unsatisfiable on a clean adoption.
- **[installable]** `sdlc-retro.md`: the read-the-citation-off-the-file rule now
  names the copy an adopted project actually holds (installed command / instantiated
  template) — the kit-repo paths it required do not exist where the kit folder was
  deleted, which the rule's own hard gate turned into an unsatisfiable requirement.
- **[installable]** `sdlc-setup.md` now resolves two placeholders it never named:
  the integration-vs-unit boundary in `spec/TESTING.md` (both modes), and
  `{{EXTRA_SPEC_ROWS}}` in `CLAUDE.md`'s spec-loading table (empty for a new
  project; one row per on-demand doc discovered on an existing one).
- **[adoption-only]** `GATE_RECIPES.md`: the hook table now states that `CLAUDE.md`'s
  prose restatement (`{{HOOK_TOOLS}}`, `{{SOURCE_EXT}}`) resolves from the same
  values, so the prose and the hook cannot disagree.

## 0.12.0 — 2026-08-03

The LEG batch: owner-led legibility work from the `FEATURE_PLAN.md` §18 brainstorm,
first of the owner-ordered LEG → COP → STD queue. Input-side and output-side
legibility in one batch: LEG.1 adds the owner hand-back standard (words in), LEG.2 is
the measured token pass over the bundle (words out), baselined on the tree that
includes LEG.1 so the tension stays honest. No new files, no new placeholders, no
halt-point changes.

### Added
- **[adoption-only]** `SDLC.template.md` *Owner halt points* (LEG.1): **the hand-back
  standard** — every owner-facing moment (each of the five halts, and the hand-back
  that ends each command) opens with an executive summary in plain-English bullets;
  every decision the owner is being asked to make is **numbered and explicitly
  marked** (`Decision 1: …`) with options and a recommendation; supporting detail
  follows the summary and never interleaves with it. Motivation: five generations of
  rigor fixes made the agent's output correct, and none asked whether the owner
  could follow it — the owner reports phase/slice output too detailed to follow.
- **[installable]** the six installed commands enforce the standard at their
  halt/hand-back steps, each restating the format inline so it survives in an
  adoption whose project-owned `spec/SDLC.md` predates it: `plan-phase.md` steps
  2 and 6 (the spec presentation opens with a summary; everything being ratified is
  numbered), `next-slice.md` steps 2, 4, and 5 (a derived number that differs from
  the ratified one returns as its own marked decision), `end-slice.md` steps 3 and 7
  (the hand-back restructured: summary first, dispositions as detail), `end-phase.md`
  steps 3, 5, 6, and 7 (post-merge bookkeeping presents its several owner decisions
  together, numbered — never one at a time buried in the bullet that raised each),
  `sdlc-retro.md` steps 2 and 6 (the submit-upstream call is a marked decision),
  `sdlc-update.md` steps 4 and 5 (per-file DRIFTED calls and un-manifested-file
  halts are numbered decisions).

### Changed
- **[installable]** LEG.2, the measured token pass — wording-only trims, no rule,
  halt, or completion condition touched: `plan-phase.md`, `end-slice.md`,
  `end-phase.md`, `sdlc-retro.md`, `sdlc-setup.md` (largest win: Existing mode
  restated New-mode asks verbatim; now cross-references). **[adoption-only]** two
  trims in `SDLC.template.md`. Bundle counts, `wc -w` / bytes÷4 over
  `git ls-files`: 27,882 → 27,765 words, ~46,677 → ~46,487 estimated tokens
  against the post-LEG.1 baseline. The measured finding: SIMP (0.10.0) already
  took the wording fat; what remains is rules, negative cases, and
  confirmed-catch evidence the §16 audit protects. Vendored `skills/**`
  untouched.
- Root-side, no marker: README's field-report count corrected to five (was four)
  — caught by `/kit-check` inv 9 during the batch's closing pass.

## 0.11.0 — 2026-08-03

The R4 batch: the fix batch of the fifth field report (`FIELD_REPORT_2026-08-02.md`,
filed as `sdlc-kit#2`), triaged in `FEATURE_PLAN.md` §15 — ten rules in the report's
damage order, run after SIMP by owner decision. The report's theme shapes the heaviest
rows: **the kit specified what each step must produce and almost never what makes it
done** — R4 gives the phase-boundary steps the completion conditions SIMP deliberately
left to it. No new files, no new placeholders, no halt-point changes.

### Added
- **[installable]** `end-phase.md` §5 (R4.1, R4.3): spawning the review fan-out
  re-asserts the §1 clean-tree precondition where it is load-bearing — the reviewers
  share the session's tree, and a real arc lost two uncommitted fixes to a reviewer's
  `git checkout` while the fix-batch commit claimed both. The corollary travels with
  it: a commit message may not claim a fix that has no test pinning it. And the
  review's completion condition: done only when **every** reviewer has returned — the
  fix batch is assembled after the last return, goes through the gate as one unit, and
  a later-arriving finding re-opens the review rather than starting a second batch.
- **[installable]** `end-slice.md` §3 (R4.1): the slice reviewer reviews the
  uncommitted working diff by design, so the discipline binds to the agent — the
  review is **read-only in the shared tree**: no `git checkout/restore/stash`; fixes
  come back as findings, never as edits.
- **[installable]** `end-phase.md` §3 (R4.2): when no slice's exit criteria required
  running the application — an arc behavior-neutral by construction — the composed
  system runs **locally against real data before the PR opens**. The acceptance halt
  passes vacuously on exactly those arcs; the arc that bought this rule found its
  worst defect in that pass, three commits before the PR, with 474 hermetic tests
  green throughout. `plan-phase.md` step 4 flags the all-slices-behavior-neutral
  condition at planning time.
- **[installable]** `plan-phase.md` steps 4–5 (R4.5): each slice's exit criteria name
  **what observes them and when** — a local command, the gate, CI on the main branch,
  or the owner; a criterion naming an observer that does not run at that point is a
  planning defect, not a slice problem. The kit's own ratchet phrasing is the standing
  exposure for every adopter whose CI runs only on the main branch — a real arc wrote
  the unsatisfiable criterion twice in one planning session.
- **[installable]** `reference/REVIEW_LENSES.md` (R4.4): third lens — **shared state
  under concurrency**: for every object that outlives a request or is reachable from
  more than one, name the runtime's concurrency model and state what serializes
  access. Specimen measured rather than asserted: 410 of 600 concurrent selects
  returned the wrong question's passages under the stdlib threading server — two
  browser tabs is enough. `end-slice.md` §3's trigger enumeration gains the matching
  third trigger.
- **[installable]** `end-slice.md` step 6 (R4.6): the friction log gets its writer —
  friction with the *process* is written to the Kit friction log at slice close, or
  never (one adoption's retros produced 23 findings across three arcs while the log
  gained zero entries). This is the writer R3.8's contingent keep waits on (§16).
- **[installable]** `end-slice.md` step 6 (R4.7): slice close-outs record **status
  only — one line**; detail lives in the phase spec and the commit message (already
  the better record). A real adoption wrote 83–163 lines per slice into its index
  five times and corrected it once per arc. R3.7's phase-close archival bullet stays
  as the safety net by owner decision (§16). **[adoption-only]**
  `PROJECT_INDEX.template.md`'s section comments state the write rule and name the
  friction log's writer.
- **[installable]** `end-slice.md` §6 (R4.8): a control that hands the operator a
  remediation command must scope that command to the population the control actually
  flags — an unscoped fix-everything one-liner corrupted two PNGs whose magic bytes
  legitimately contain CR LF. The *verify the denominator* lens applies to the
  control's own output.
- **[installable]** `sdlc-retro.md` step 5 (R4.10): the citation gate — a finding
  quotes the implicated text at a section number **read off the file at writing
  time** (or, for a silence finding, locates the silence between two named steps that
  do exist), and names **every home** of the quoted wording. Two consecutive reports
  shipped citations written from memory of the process — step numbers for steps that
  do not exist — every one caught only maintainer-side.
- **[adoption-only]** `SDLC.template.md` mirrors every command-side rule above
  canonically (inv 2): halt 4, phase-start item 3, slice-loop items 6 and 9,
  phase-end item 4, and the bookkeeping gotcha rule.
- Root-side, no marker: `FEATURE_PLAN.md` §5 gains the trial-protocol rule (R4.9) — a
  trial pre-registers **what the change is supposed to buy and how that is measured**,
  alongside its safety criteria. F3's four criteria all measured safety, and a trial
  that cannot fail on value cannot justify shipping.

## 0.10.0 — 2026-08-03

The SIMP batch: the simplification pass the fifth field report ranked first (finding 7,
`sdlc-kit#2`) and the kit's own §12 standing note had already called for — run as its
own batch, **before** the R4 fix batch, by owner decision. The audit behind it is
`FEATURE_PLAN.md` §16: 38 adopter-facing rules enumerated from the 0.5.0–0.9.0
releases, each asked *what did you catch, in which adopter, when* — 24 carry confirmed
post-ship catches, and the verdict is the report's own prediction: a pruning, not a
retreat. **This batch adds no new process rules.**

### Removed
- **[installable]** The `sdlc-surveyor` agent and with it the entire `agents/` →
  `.claude/agents/` install mapping (the surveyor was its only occupant since 0.6.0).
  Four releases, zero observed uses across four real arcs — the analysis sweeps absorb
  the fact-fetching it was designed for, and §12 had already recorded that continued
  non-use would be a signal about the step, not noise. Owner-decided 2026-08-03.
  Ripples: `plan-phase.md`'s feasibility check keeps the practice (verify seams by
  quoting the codebase) without the agent; `sdlc-setup.md` no longer installs agents;
  the model-policy Low tier loses its "kit-set" instance; `reference/SKILLS.md` loses
  the kit-agents row; both READMEs and the flow diagram lose the mapping.
- **[installable]** `sdlc-update.md` step 5 gains the mapping's retirement mechanism —
  the first **removed-from-install-set** clause, symmetric to the new-files clause: a
  file in the old manifest's install mapping but absent from the target's is deleted
  when it classified `UNCHANGED`, and goes to the owner when `DRIFTED`. The
  classification script still enumerates `.claude/agents/` so projects on 0.6.0–0.9.0
  can transition. The root README's update section states the same clause (inv 8).
  Machinery the deletion needs to reach adopters — not a new process rule.

### Changed
- **[installable]** Six "do this" rules converted toward "this is done when" — the
  fifth report's cross-cutting theme (the gate, the only step with a completion
  condition, was the only step that never failed) applied to the survivors that admit
  one in a single clause: slice-review triage (`end-slice.md` §3 — done when every
  finding is dispatched and the hand-back names the discards), the mutation check
  (`end-slice.md` §4 — done when every new guard has been seen to fail on exactly its
  own test), re-derivation (`next-slice.md` §2 — done when every marker had its
  proportional check and every `estimated` number carries a derivation), the
  coverage-floor reconcile (`end-phase.md` step 7 — not done until the homes are
  identical), gotcha escalation (`end-slice.md` §6 — exactly two closed states; a
  sharper note is neither), and the friction sweep (`sdlc-retro.md` §2 — done when no
  unabsorbed entry is left unreported). **[adoption-only]** `SDLC.template.md` mirrors
  the first five canonically (inv 2). The whole-arc review and the acceptance pass are
  deliberately untouched — their completion conditions are R4 additions, not
  conversions.

### Audited, kept, on the record (§16)
- The doubles lens (five releases, no attributed catch, failure class demonstrably
  alive) — owner-decided keep. R3.7's archival bullet — kept as the safety net behind
  R4's coming prevention. R3.8's aging rule — kept contingent on R4 giving the friction
  log a writer. Kit-development invariants (14, 15) out of audit scope.

## 0.9.0 — 2026-08-01

The R3 batch: the eight findings of `FIELD_REPORT_2026-08-01.md` (the fourth field
report — a different adopter's fifth phase, a three-slice security arc, filed as
`sdlc-kit#1`). Every claim was verified against the tree at 0.8.0 before triage rather
than accepted: seven stood, one was already fixed in 0.7.0, and three had their scope
or attribution corrected — recorded in `FEATURE_PLAN.md` §12. The report's theme is the
kit's widest yet and now carries invariant 15: **the process verifies the artifact and
is silent about the environment it will run in.** Four of the eight findings are
instances of that one gap. Same shape as R2 and G1 — markdown-only, no new placeholders,
no tooling, no new halt point.

### Added
- **[installable]** `plan-phase.md` step 4: the consequence sweep's hits must now answer
  two questions. **Is it actually inert?** — a claim that a consequence is neutralized
  by configuration ("ships dormant", "off in prod", "merging changes nothing") names
  the variable and **quotes its value from the artifact that configures production**,
  never from the test environment, which is usually configured to make the claim true.
  **What is the independent off switch?** — a control whose only lever also disables an
  unrelated system has no rollback. A real arc called a spend cap dormant in its spec,
  its PR body, and its index while the deployment manifest committed the variable that
  made it enforce from the first request; the test conftest neutralized that same
  variable suite-wide, so every in-repo signal agreed with the wrong conclusion.
  **[installable]** `end-phase.md` step 7 asks the question the deploy outcome does not
  — *what did this deploy turn on*, and what disables each newly-live control by itself.
- **[installable]** `plan-phase.md` steps 3/5/6 + `next-slice.md` §2: a decision
  carrying a number is tagged **`measured`** (naming the run, count, or query behind it)
  or **`estimated`**, and the slice that implements an `estimated` one derives it
  *before* starting — a differing result goes back to the owner as a question and the
  decision is re-tagged. Extends the `measured`/`suspected` vocabulary the backlog
  already uses to where numbers are first ratified. Seven of forty-four decisions on one
  arc were corrected on contact with code, one of them a cap whose approved value
  implied roughly two orders of magnitude more spend than intended.
- **[installable]** `end-phase.md` step 7: the red gate baseline gets the mechanism the
  coverage floor already had — report the count beside the recorded one, then lower it,
  schedule lowering it, or have the owner **ratify holding it** with the number of arcs
  it has been unchanged. One adoption held a typecheck count across four arcs and twelve
  recorded gate runs while its `SDLC.md` called it a ceiling to drive down.
  **[adoption-only]** `SDLC.template.md` states the procedure and the rendering rule: an
  unchanged baseline reads `N (unchanged for K arcs)`, never `held` — a stall must not
  look like an achievement.
- **[installable]** `end-slice.md` §6: a gotcha recorded in **three consecutive slices**
  becomes a gate step, a hook, or a test — or is ratified unpreventable and says so with
  its recurrence count. One adoption recorded the same line-ending hazard four times,
  each note sharper than the last, each one followed, and it recurred every time.
  **[adoption-only]** `SDLC.template.md` bookkeeping rules state it canonically;
  `PROJECT_INDEX.template.md`'s Environment gotchas comment points at it.
- Kit-development (not shipped): **invariant 15** — every verification step names the
  environment it verifies against — added to `KIT_INVARIANTS.md` with its specimen and
  to `/kit-check`'s reading passes.

### Fixed
- **[installable]** `end-phase.md` §5 and `end-slice.md` §3: **verify each review
  finding against the source before it enters a fix batch, and report the findings that
  did not survive alongside those that did.** Nothing previously sat between "run the
  review" and "apply fix batches". Two of five reviewers on one arc produced CRITICALs
  whose stated trigger was factually false; followed literally, the step would have
  taken both fixes into a live authorization path. The reporting half is not optional —
  a discarded finding is evidence about the reviewer.
- **[installable]** `sdlc-setup.md` (both modes) and `end-phase.md` §3: a command the
  **owner** will execute is verified in the **owner's shell**, not an agent's — the
  owner runs the acceptance command during setup and pastes the result, and the resolved
  interpreter path is recorded in Environment gotchas. A documented run command was
  broken for one owner (a conda `base` interpreter their profile put on `PATH`) and
  verified working by agents, whose tool-shells never load that profile, for four
  phases of green gates. **[adoption-only]** `SDLC.template.md` states it at the
  acceptance-review step.
- **[installable]** `sdlc-retro.md` §2: the friction-log sweep now reads the log for
  **status and age**, not only content — unabsorbed entries are reported with how many
  phases they have survived, and anything older than one phase is carried into the new
  report automatically. The absorbed-marker convention existed; nothing read it.
- **[installable]** `end-phase.md` step 7 + **[adoption-only]**
  `PROJECT_INDEX.template.md`: index sections are marked **bounded** or **growing**, and
  closed-phase per-slice detail is archived into that phase's own spec file at the phase
  close. One adoption's single source of truth reached 2,400 lines with the answer to
  "what do I do next" buried above five phases of merged history. Nothing is deleted —
  the file is a dashboard first and an archive never.

## 0.8.0 — 2026-07-22

The G1 batch: the five accepted kernels of `CRITICAL_GAPS_ANALYSIS.md`, an external
review of the kit at 0.7.0 that was challenged before acceptance — the verdict, the
owner answers that re-weighted it, and the rejected remainder (enforcement engine, risk
profiles, full secure-development lifecycle, slice PRs, deployment lifecycle states)
are recorded in `FEATURE_PLAN.md` §11. Every accepted change follows R2's shape: small,
reconcile-shaped, markdown-only — no new files, no new placeholders, no tooling.

### Added
- **[installable]** `end-phase.md` step 7: the deploy question now ends in a
  **verified, recorded outcome** — the deployed artifact is checked against the
  platform's own record (the deploy run's SHA, the dashboard's deployed-commit field)
  and the result lands in the Phase History row's Notes cell (`deployed+verified
  <date>` / `deploy pending — <where tracked>` / `n/a — no deploy`), with a pending
  deploy carried in START HERE until verified. **[installable]** `sdlc-setup.md`'s two
  deploy questions also capture how a deploy is verified (same `{{DEPLOY_NOTE}}`
  placeholder, richer resolution). **[adoption-only]** `SDLC.template.md` phase-end
  step 6 states it canonically; `PROJECT_INDEX.template.md`'s Phase History comment
  and `CLAUDE.template.md`'s `/end-phase` summary mention the outcome.
- **[installable]** `next-slice.md` §3 + **[adoption-only]** `SDLC.template.md` Shape:
  the **hotfix exception** — an urgent production fix while an arc is open branches
  `fix/<slug>` off main with its own minimal PR and Phase History row, the only
  sanctioned second unmerged branch; afterward the arc branch merges main and re-runs
  the gate before its next slice, so the arc never drifts silently from production.
- **[adoption-only]** `GATE_RECIPES.md`: security checks CI already runs (dependency
  audit, secret scan, static analysis) are part of "the gate must match CI" — fast
  ones join the local gate, slow or credentialed ones stay CI-only but are listed in
  the gate section of `spec/SDLC.md`. **[installable]** `sdlc-setup.md`'s Existing-mode
  survey collects them.
- **[installable]** `plan-phase.md` step 4 + **[adoption-only]** `SDLC.template.md`
  phase-start step 2: the **consequence sweep** — behaviors touching auth, money,
  irreversible data operations, credentials, or regulated data must name their extra
  verification in the spec and appear in Risks & Deferred; consequence and size are
  different axes, and smallness is no exemption.
- Kit-development (not shipped): **invariant 14** — a recorded value names its
  enforcing artifact and the step that writes it reconciles the two — added to
  `KIT_INVARIANTS.md` with its specimen (the third field report's floor drift) and to
  `/kit-check`'s reading passes.

## 0.7.0 — 2026-07-22

The R2 batch: all three priority rows of `FIELD_REPORT_2026-07-22.md` (the third field
report — the first full arc run on kit 0.6.0), plus the distribution-readiness work
ahead of opening the repository to a general audience. The report's cross-cutting theme
runs through every fix: a number recorded in prose is not the number the machine
enforces — wherever a value lives in two places, bump both, then assert they agree.

### Fixed
- **[installable]** `end-phase.md` step 7 gains the coverage-floor bullet the ratchet
  was missing: if CI's printed coverage rose this arc, set the floor in the CI workflow
  file to just under CI's printed number in the same docs commit, then **assert** that
  the floor recorded in the index and the value in the workflow file are identical —
  the record is a claim, the workflow value is the enforcement. A real arc recorded
  "28 → 32" in two prose homes while CI silently enforced 28 (finding 1).
  **[adoption-only]** `SDLC.template.md` states the boundary procedure canonically
  (*Coverage floor* section + *Phase end* step 6).
- **[installable]** `next-slice.md` §2 re-derivation is now proportional to the
  `measured`/`suspected` marker it previously read and then ignored: `measured` →
  spot-check that the cited anchors and behavior still hold; `suspected`, or a
  `measured` entry whose anchors drifted or whose spot-check surprises → full
  reproduce-or-disprove, re-tagged with what it finds. Every wrong-cause catch on
  record stays in the full-treatment class (finding 2). **[adoption-only]**
  `SDLC.template.md` slice-loop step 2 mirrors the rule.
- **[installable]** `sdlc-update.md` step 5 now prescribes the bundle-replacement
  mechanism instead of leaving it to improvisation: copy-over-in-place — remove only
  the files the old version's manifest lists, then `cp -r $K/. sdlc-kit/`, never
  `rm -rf` the directory. The improvised `rm -rf` failed half-done on a real Windows
  update (directory busy after every file was unlinked) and on any platform opens a
  window with no bundle at all (finding 3). The root README's update section states
  the same mechanism.
- `reference/SKILLS.md` no longer claims `python-pro.md` carries "no license text" —
  the file's frontmatter self-declares `license: MIT`; the record now says so while
  keeping its redistribution status unverified (no locatable upstream). Found by this
  release's `/kit-check` pass.

### Changed
- Release assets now use stable, version-free names (`sdlc-kit.tar.gz`, `sdlc-kit.zip`,
  `sdlc-kit.CHECKSUMS.txt`) so the README's `releases/latest/download/…` one-liner
  works verbatim. The version still travels in the tag, the release title, and
  `sdlc-kit/VERSION` inside the archive. Applies from the next tag; releases up to
  v0.6.0 keep their `sdlc-kit-<version>.*` names, and the README says so.
- Root README: prerequisites stated (Claude Code, git, a POSIX shell with `sha256sum`),
  the download one-liner fixed, and a new *Reporting problems and field reports*
  section. The bundle README states the same prerequisites (manifest regenerated).

### Added
- `.github/ISSUE_TEMPLATE/` — a one-finding bug-report template and a field-report
  template mirroring the shape `/sdlc-retro` emits, so submitted reports arrive in the
  form the triage process already consumes.

## 0.6.0 — 2026-07-20

The agents-and-model-tiers batch (`FEATURE_PLAN.md` F2), plus two residues from the
0.5.0 migration. Two governing rules, both now stated in `SDLC.template.md`:
parallelism is **read-only fan-out within a step only** (never implementation, never
across slices), and every owner interaction stays in the main session — subagents
cannot ask, so no halt point moves. The five-halt-point invariant stands.

### Added
- **[installable]** New install mapping — the first new destination since
  `REVIEW_LENSES.md`: `agents/` → `.claude/agents/`, project-scoped agent definitions
  inherited on clone like the commands. Initial set is one file, deliberately:
  `sdlc-surveyor.md`, a read-only mechanical-collection agent (`tools: Read, Grep,
  Glob`; `model: haiku` — kit-set, because collection gains nothing from a bigger
  model). It collects and reports verbatim, with denominators; it never analyzes.
  Both classification scripts (`sdlc-update.md` step 3 and the root README's update
  section) now enumerate `.claude/agents/` with an `agents/` prefix match, and their
  denominator checks count both destination directories. Updaters from ≤0.5.0 receive
  the agent via the new-in-install-set clause, not classification.
- **[installable]** `plan-phase.md` step 4: the seven adversarial sweeps run as
  **parallel read-only subagents** — the command's heaviest context load, delegated;
  findings return to the main session, where every question and decision stays with
  the owner. Sweep agents analyze and therefore inherit the session model — the haiku
  surveyor is explicitly excluded from this step. The feasibility check names
  `sdlc-surveyor` (it locates seams; it does not judge them).
- **[installable]** `sdlc-setup.md` gains the **model-policy poll** (both modes, the
  process-fit round): a three-tier recommendation (High `opus` — planning, analysis,
  adversarial review; Medium `sonnet` — code to an existing spec; Low `haiku` —
  mechanical collection) confirmed or adjusted by the owner. Recorded in
  project-owned homes only: the policy as `{{MODEL_POLICY}}` in `spec/SDLC.md`, the
  optional pinned session default as `{{DEFAULT_MODEL}}` in `.claude/settings.json`
  (`"model"` key; line deleted when the owner keeps the harness default). Aliases
  only, never model IDs. Setup never writes a model into an installed command file —
  the rejected shape of field-report #1. `opusplan` on `plan-phase.md` remains
  deferred for lack of field evidence. `plan-phase.md` opens with a one-line pointer
  to the recorded policy.
- **[adoption-only]** `SDLC.template.md`: the read-only fan-out rule and the model
  policy section (`{{MODEL_POLICY}}`); `settings.template.json`: the `"model"` line
  (`{{DEFAULT_MODEL}}`). Placeholders #35 and #36, both resolved by the poll.
- **[adoption-only]** `PROJECT_INDEX.template.md` seeds a **Kit friction log**
  section — process friction (tooling noise, workarounds, silent moments) gets a
  dated one-line home the moment it is felt. `/sdlc-retro`'s recorded-but-unactioned
  sweep mines this section first **[that half installable]** and treats its absence
  on an older adoption as a small finding. Residue of the 0.5.0 migration: TFit's
  friction log had no kit-side counterpart for other adopters.
- **[adoption-only]** Setup's `.gitattributes` guidance widens from `*.md text eol=lf`
  to `* text=auto eol=lf` (New mode writes it; Existing mode offers it, with a scoped
  fallback for owners wary of repo-wide policy). The `*.md`-only pin was measured to
  miss four non-markdown bundle files (`LICENSE`, `MANIFEST.sha256`, `VERSION`,
  `settings.template.json`) on the 0.5.0 TFit update — same phantom-modification
  noise class, one size smaller. The repo-wide form is what this kit's own
  `.gitattributes` uses.

### Fixed
- **[adoption-only]** `reference/SKILLS.md` onboarding checklist said "the five SDLC
  commands"; the set has been seven since 0.4.0 (`sdlc-retro`, `sdlc-update`). Its
  Required table gains the kit-agents row.
- **[adoption-only]** Halt 3's template wording scoped design questions "mid-slice";
  `end-phase.md` has always (correctly) halted on design questions found by the
  whole-arc review too. The template now owns that scope — "mid-slice or by a
  review" (this release's `/kit-check`, invariant 2).
- Root README: the file tree still marked `mutation-testing.md` optional (always
  installed since 0.5.0), and the update section lacked the command's "claim only
  what was checked" rule — both brought back into agreement (invariants 7, 8).

## 0.5.0 — 2026-07-20

The retro-fix batch: all 15 priority rows of `FIELD_REPORT_2026-07-20.md` — the first
real run of `/sdlc-retro`, on the same adoption that produced the first field report.
Cut ahead of the planned agents batch because the report's top rows are a live defect
class in the update path itself. The report's cross-cutting theme — checks whose
denominator was assumed rather than enumerated — is the thread through nearly every
entry below.

### Fixed
- **[installable]** `sdlc-update.md` step 5 no longer replaces a kept `sdlc-kit/`
  folder blind: it enumerates the folder's **actual contents** against the manifest
  first, reports anything un-manifested, and HALTs — a project put that file there, and
  one real update silently deleted a project's only local copy of two commits of
  authored work while reporting "nothing project-owned touched". Step 6 now permits
  that reassurance only when the final diff was actually read (report finding 1).
- **[installable]** `sdlc-update.md` step 4 reports **content-changed counts separately
  from touched counts**, so "5 changed, 19 touched" replaces the flat "24 modified"
  whose known-meaningless noise is exactly where the deletion above went unread
  (finding 12, the mechanism of finding 1).
- The root README's update section mirrors both changes plus the arc-boundary rule —
  the command and the section state the same procedure by definition.
- **[installable]** `end-slice.md` §3 named a review tool that does not exist ("the
  code-review skill"); a real run substituted silently and well, which is why nobody
  looked. The per-slice reviewer is now `pr-review-toolkit:code-reviewer`, the built-in
  `/code-review` is identified as the owner-typed escalation, and any substituted tool
  must be named in the hand-back (finding 6; `reference/SKILLS.md` and setup's step 1.2
  check follow).

### Added
- **[installable]** `end-slice.md` gains a **mutation-check step**: every new guard,
  branch, or error path is deleted or inverted once and the suite watched to fail on
  exactly the intended test. The kit shipped `mutation-testing.md` and no workflow step
  ever invoked it; used by habit on a real project, it caught a test that could not
  have failed and proved a production defect's root cause — the single
  highest-yield check in the kit, previously reachable only by memory (finding 4).
  `mutation-testing.md` accordingly flips from offered to always-installed
  (`sdlc-setup.md` step 5, `reference/SKILLS.md`) — updaters who declined it at
  adoption receive it as a new-in-install-set file.
- **[installable]** `end-slice.md` §3 gains the two lenses slice review structurally
  lacked, both paid for in production: name each **consumer** of a changed error/return
  path and what it did with the old behavior (finding 2 — two arcs, two defects that
  survived every slice review, one live in production); and ask whether any **test
  double** omits a side effect or simplifies the error surface of what it replaces
  (finding 5 — a recorder that dropped one flag assignment hid a live bug through four
  reviews).
- **[installable]** `next-slice.md` §2: **re-derive a backlog entry's stated cause
  before writing any fix** — 3 of 3 entries checked on a real project stated a wrong
  cause, and a fix aimed at a fictional trigger can be right anyway, pass every test,
  and teach the next reader a false fact (finding 3). Deferred entries now mark their
  cause **measured** or **suspected** at the writing end (`end-slice.md` §3,
  `templates/PROJECT_INDEX.template.md`).
- **[installable]** `next-slice.md` §3 states the branch rule mode-independently —
  slices accumulate on one arc branch until `/end-phase`; only `/end-phase` opens a
  PR — and checks for **any unmerged arc branch**, not just "am I on main".
  STABILIZATION branches are named for the arc's theme, not their first slice
  (finding 7; `end-slice.md` notes state the accumulation rule its PR prohibition
  always assumed).
- **[installable]** `end-phase.md` post-merge bookkeeping asks the **deploy question**
  (merging is not shipping — a production fix once sat unshipped behind exactly this
  missing step) and **surfaces the backlog** with severity counts for one owner
  decision: convert, defer, or drop (findings 9, 10). Neither is a new halt; the
  five-halt-point invariant stands.
- **[installable]** `sdlc-update.md` states *when* to update: at a phase/arc boundary,
  never with an arc in flight — three updates once landed in the three hours before an
  arc's first slice, and which kit version governed which slice is now
  unreconstructable (finding 8).
- **[installable]** `sdlc-setup.md`: warns that a kept `sdlc-kit/` folder is kit-owned
  and **volatile** (project notes go to a project-owned path); checks `.gitattributes`
  defines an `eol` for `*.md` and offers `*.md text eol=lf` in both modes (findings 1,
  12 — the one-line fix for the phantom-modified noise).
- **[installable]** `sdlc-retro.md` step 1 gains the co-development clause — when the
  kit's own repo is at hand, orientation reads the kit-side planning docs too — and
  step 2 sweeps for **recorded-but-unactioned friction** on both sides. The first real
  retro missed a friction item the kit's plan had already recorded and labeled as retro
  material; the command could only mine what the project wrote down (finding 12's
  method note).
- **[adoption-only]** `templates/SDLC.template.md` carries the canonical statement of
  every process change above: the one-arc-one-branch-one-PR rule in *Shape*, halt 2
  narrowed to skip owner-decided slices (finding 11 — the owner's instinct was to
  delete it; the retro narrowed it instead), the re-derive rule, the renamed reviewer
  and its two lenses, the mutation-check step, and the deploy question + backlog
  presentation at phase end. New placeholder `{{DEPLOY_NOTE}}`, resolved by a new
  deploy-procedure question in both setup interviews — the placeholder contract holds.
- **[adoption-only]** `templates/TESTING.template.md` mock policy: a double that stands
  in for production code must reproduce its **side effects and error surface**, or the
  test drives the real thing (finding 5).
- **[adoption-only]** `templates/CLAUDE.template.md` command summaries follow
  (mutation check; deploy question).

## 0.4.0 — 2026-07-19

The improvement loop gets its input side: `/sdlc-retro` turns a finished phase into
evidence, so the next plan rests on what a run actually taught rather than on what
someone remembered to write down. Cut ahead of the feature plan's schedule (which put
0.4.0 after the agents batch) so the command can be exercised on a real adoption —
the same reason the last two releases were cut, and the same reason they found defects.

### Added
- **[installable]** `commands/sdlc-retro.md` — `/sdlc-retro`, lessons-learned extraction
  at a phase boundary. The improvement loop had a proven output side (field report →
  plan → batches → release → migrate) and a manual input side: `FIELD_REPORT.md` was
  written by hand, so the kit's evidence supply depended on someone volunteering a
  retrospective. The command mines what the process already forces onto disk —
  deferred-backlog provenance tags, the gate-baseline trajectory in `spec/SDLC.md`,
  Phase History, `git log` friction signals — then interviews the owner and sorts every
  lesson into exactly two piles: project facts into the project's own files, process
  findings into `spec/SDLC_RETRO_<date>.md` in the shape of `FIELD_REPORT.md`. It never
  submits anything; whether a finding reaches the kit is the owner's call. Refuses to
  run on a project with too little history rather than manufacturing findings.
- **[adoption-only]** `templates/CLAUDE.template.md` lists `/sdlc-retro` alongside the
  four daily commands, so an adopting project learns the command exists. A command
  installed and named nowhere the project reads is a command nobody runs.
- **[installable]** `end-phase.md` step 7 offers `/sdlc-retro` after the phase closes.
  Every other kit command is reachable from the process — `SDLC.md` names `/plan-phase`,
  `/plan-phase` hands off to `/next-slice`, `/end-slice` to `/clear`. The retro had no
  caller, which for *this* command is self-defeating: it exists because the evidence
  supply depended on someone volunteering a retrospective. It is offered rather than
  required, and stays out of `SDLC.template.md` deliberately — a mandatory retro after
  every phase is the ceremony the retro's own "what would you delete?" question exists
  to catch. The failure it prevents is silent: no error, no drift, no `/kit-check`
  finding, just a command that ships in every bundle and never runs.

### Fixed
- The root README's *Updating an adopted project* section was missing the
  **new-files-in-the-target** clause that `sdlc-update.md` step 5 already had — so the
  two statements of the procedure disagreed, which the kit defines as a bug. A human
  following the README by hand would finish step 4 with no instruction that would ever
  create a newly-installed file, and step 6's verification checks only files you copied,
  so the omission verified clean. Found by `/kit-check` invariant 8 while adding
  `sdlc-retro.md` — the first new installed file since the clause was written, and
  exactly the case it exists for.
- **[adoption-only]** `reference/SKILLS.md`'s kit-command row listed five commands,
  omitting `sdlc-update` (shipped in 0.3.0) and `sdlc-retro`. It is a derived statement
  of the install mapping, so it now names its source of truth instead of quietly drifting
  from it a third time.
- **[installable]** `sdlc-update.md` step 5 now says explicitly that files **new in the
  target version's install set** are copied in — classification never sees them (the
  project does not hold them yet), and the command's first real run (TFit,
  0.2.0 → 0.3.0, which introduced two new installed files) had to infer this from the
  source list rather than being told.

## 0.3.0 — 2026-07-19

Everything the field report asked for that 0.2.0 did not ship — and the kit's own
self-check, whose first run found 15 more defects, all fixed here.

### Fixed
- The *Updating an adopted project* procedure hashed the **working tree**, which reports
  every file as drifted for any Windows adopter whose project does not pin line endings —
  the kit stores LF, their checkout holds CRLF. The check looked like it worked and was
  uniformly wrong. It now hashes committed content (`git cat-file -p :path`), which is LF
  on every platform. Found by running the documented procedure against a real adopted
  project rather than a synthetic one.
- The retroactive path for projects adopted before 0.2.0 is now a complete script, and
  notes that `v0.1.0` predates the restructure (kit files at `commands/`, not
  `sdlc-kit/commands/`).
- Both scripts now avoid a trap that produced confident wrong answers: probing for a path
  with `git cat-file … | sha256sum` reports the *pipeline's* status, so a missing path
  yields the hash of empty input and silently matches the wrong entry. Documented, along
  with a denominator check, since the failure mode is a plausible result rather than an
  error.

The three fixes above changed no file inside `sdlc-kit/`. The entries below do, and reach
adopters at the next release; the bundle manifest is regenerated in the same commits (the
release workflow *verifies* the manifest rather than regenerating it, so a stale one
fails the next tag push).

### Added
- **[adoption-only]** `{{SDLC_SCOPE}}` in `SDLC.template.md`, directly below the title,
  and **[installable]** `/sdlc-setup` now asks in both modes whether the process governs
  the whole repo or a subset, and what is explicitly out of scope. Mixed repos are
  common; the first adoption had to record this decision in three files by hand.
- **[adoption-only]** `SDLC.template.md`, CI section: when local and CI disagree about a
  measurement, CI is authoritative — and the disagreement is itself a finding to explain
  before any threshold moves. The kit previously never contemplated the two disagreeing.
- **[installable]** `end-slice.md` §5 (and the matching bookkeeping rule in
  `SDLC.template.md`): a slice that adds a tool, runtime, or service the gate now
  requires records it and adds it to CI in the same commit — a gate dependency
  discovered by a contributor's red run is a documentation bug.
- **[installable]** `end-phase.md` §3: to exercise failure paths during acceptance
  without risking authoritative data, prefer breaking the connection over corrupting
  the data — stop the server; the failure paths are identical and no real data moves.
- **[adoption-only]** `PROJECT_INDEX.template.md`: a dedicated *Environment gotchas*
  section (previously these facts had no home of their own inside *Notes & gotchas*);
  the Existing-mode adoption-row convention for Phase History
  (`| — | **SDLC adopted** | pre-SDLC | … |`, back-filled rows marked as recorded for
  the arc, not as process history); and backlog provenance tags
  (`"(slice review, <date>)"`) — the practice the field report's own retrospective
  called the most useful part of the run.
- **[adoption-only]** `TESTING.template.md` §*Test Isolation — Enforced, Not Promised*:
  the field report's near-miss (a suite calling the live Google Calendar API for three
  slices, green the whole time) as a headline rule — *partial isolation is worse than
  none, because it reads as complete* — plus three checks the kit specifies without
  shipping code: outbound network blocked, credentials unreachable, every home/data-dir
  seam isolated. A new `{{ISOLATION_HARNESS}}` placeholder records where the harness
  lives and the proof that each check has been made to fail.
- **[installable]** `reference/REVIEW_LENSES.md` — deep-dive review lenses behind a
  conditional pointer in `end-slice.md` §3, read only when the slice's diff matches a
  trigger (error-propagation changes; pattern sweeps or trusted check-scripts), so
  ordinary slices pay no context for them. The error-propagation lens: a new raise is
  done when every caller has been re-read; the mirror question *what did I stop seeing?*;
  a status code is a claim about fault. The verify-the-denominator lens takes its worked
  examples from the 0.2.0 session's three confidently-wrong checks rather than the field
  report's miscount — in each, the check returned a *plausible* answer, so nothing
  prompted a second look — paired with the rule that a check is only trustworthy once it
  has been made to disagree. Unlike the rest of `reference/`, this file is **installed**
  (`→ .claude/commands/REVIEW_LENSES.md`, both setup modes) so the pointer resolves in
  projects that removed the kit folder after setup; it is kit-owned, joins the
  manifest/update path, and the README's classification scripts now try the `reference/`
  prefix alongside `commands/` and `skills/`.
- **[adoption-only]** `TESTING.template.md`: a *Skip discipline* subsection beside the
  mock policy — a test must **fail**, not skip, when a tool it requires is absent; a
  silently-skipped test is the same false green as one that reached the real service —
  and *What a test may assert about errors* in §Test Isolation: asserting "returns empty
  on error" is usually pinning a bug (assert that the error propagates instead), and a
  new invariant is checked against what the system already does, not what sounds right.
- **[installable]** `/sdlc-setup` authors the isolation harness for the detected stack
  (New mode step 4; Existing mode proposes it at the feedback halt) and **proves each
  check by its negative case** — a deliberate violation must fail the suite loudly,
  naming what was attempted, before the check is described as enforced. If the owner
  defers it, the gap goes to the backlog and `{{ISOLATION_HARNESS}}` records what is
  actually enforced today — never enforcement that does not exist. Acceptance was run
  for real in a non-Python stack (Node): the harness authored from the spec alone
  failed loudly on a deliberate `fetch` (naming the address) and a credential-path
  read, then ran 3/3 green with a shell-set token provably not reaching tests.
- **[installable]** `commands/sdlc-update.md` — the update procedure as an installed
  command, closing the field report's #14 outright. It classifies every installed file
  against the manifest of the version the project is **on**, hashes committed content
  (never the working tree), tries all three install prefixes with a denominator check,
  halts exactly once (per-file owner decision on drifted files — never auto-overwritten),
  touches nothing project-owned, and re-stamps `spec/SDLC.md` last so an aborted update
  never claims a version it does not hold. The command and the root README's *Updating an
  adopted project* section deliberately state the same procedure twice — they are
  cross-pointed, a disagreement between them is defined as a kit bug, and keeping them in
  agreement is a `/kit-check` invariant candidate. `SDLC.template.md`'s update pointer
  now names `/sdlc-update` instead of the home-repo README, which an adopted project may
  not hold.
- **[installable]** `/sdlc-setup` Existing mode: the analysis step now globs for
  pre-existing `PROJECT_INDEX.md` / `INDEX.md` / `STATUS.md` anywhere in the tree and
  surfaces hits at the feedback halt with an offered rename of the pre-existing file —
  the kit is about to make `spec/PROJECT_INDEX.md` the single source of truth, and a
  same-named neighbor is how a session reads the wrong file. If the owner keeps both
  names, the disambiguation is recorded in project-owned files (Environment gotchas), not
  in command prose. Scoped to Existing mode, as planned; renaming the kit's own file
  remains deferred until the update path has been exercised at scale.
- **[installable]** `end-phase.md` §5: one sentence on why the whole-arc review exists —
  slice reviews each see one layer, so arc-level bugs live in the seams between slices
  and are invisible to every per-slice review by construction.
- **[adoption-only]** `SDLC.template.md`, gate-baseline section: a count can also hold
  still because the checker stopped looking — suppressions, skipped tests, and constructs
  that hide code from analysis freeze the number while shrinking what it measures.
  **Flagged unsolved:** this is a prose warning, which the field report's own thesis says
  is the weak form of a fix. The real mechanism records *checker reach* (suppression
  count, `Any`-expression share) alongside the error count so a flat count with degrading
  reach becomes visible; designing that is deliberately deferred — it is placeholder- and
  setup-work sized like a batch of its own.
- **Kit self-check** (root-only; nothing an adopter receives): `KIT_INVARIANTS.md`, the
  canonical ledger of 13 invariants — each carrying the real shipped defect that
  motivated it, as the check's negative case — and `/kit-check`
  (root `.claude/commands/kit-check.md`), an agent reading pass over the ledger, not a
  grep suite: the greppable checks (README tree, manifest currency, `{{` census, step
  references) run as commands inside it, but the invariants that have actually shipped
  defects (a false project fact in prose, a semantically-resolved placeholder, a pointer
  that dangles only post-setup) are invisible to pattern matching — the literal
  placeholder name-match was tried and produced 24 false positives out of 32. Both live
  at the root because invariant 12 forbids kit-development-only files in the bundle —
  the batch as first planned put them *in* the bundle, which would have installed a
  kit-development command into every adopting project.

### Fixed — by /kit-check's first real run

The pass was run before shipping it and disagreed immediately: 15 findings, all fixed
in this release. The ones with teeth:

- **[installable]** `end-phase.md` asserted *"branch protection requires the CI check"*
  — a repo-configuration fact that is false for any adopter without branch protection,
  the same defect class as 0.2.0's baseline assertion (nothing in setup configures or
  verifies branch protection). The command now states the rule without asserting the
  enforcement; **[adoption-only]** `SDLC.template.md`'s CI section softened to match.
- **This changelog's own marker definition classified all of `reference/**` as
  adoption-only** — contradicting the install mapping (and its own entries):
  `reference/REVIEW_LENSES.md` is installed and tracks upstream, so a future change to
  it filed per the old definition would have been tagged *[adoption-only]* and never
  routed to adopters by `/sdlc-update`, which reads these markers. Header fixed;
  **[installable]** `sdlc-update.md`'s Notes no longer repeat the stale generalization.
- The README's manual update procedure **had no verification step**: `/sdlc-update` §6
  re-classifies against the target manifest to prove the classifier discriminates, and
  the README — the stated path for pre-command adopters — went straight from copy to
  re-stamp. Added, along with the command's replace-a-kept-`sdlc-kit/`-folder-wholesale
  step, which the README also lacked (a stale kept folder sits beside a re-stamped
  `spec/SDLC.md` claiming a version it does not hold). Both were disagreements between
  the procedure's two statements — found by the invariant recorded when the second
  statement was written.
- **[installable]** `sdlc-setup.md` Existing mode installed the edit-time hook with no
  proof it blocks — the deliberate-lint-error verification existed only in New mode,
  and Existing mode is both the field-tested path and the riskier install (hook
  *merging*). The proof is now required in both modes.
- **[installable]** `skills/python-pro.md` carried a "Reference Guide" table pointing
  at five `references/*.md` companion files that exist nowhere — not in the kit, not
  installed — so a Python session was instructed to load five dangling paths. Table
  removed; the divergence from upstream is recorded in `reference/SKILLS.md`, whose
  provenance note (with `THIRD_PARTY_NOTICES.md`) now also states plainly that
  `python-pro.md` has no identified upstream license, rather than implying blanket MIT.
- **[installable]** `sdlc-setup.md`'s close-out exit check grepped all of `.claude/`,
  which contains the installed copy of `sdlc-setup.md` itself — a file that
  legitimately names placeholders — so the check false-positived on every adoption
  (plan §8.11, left for this batch deliberately). Scoped to exactly the instantiated
  files: `CLAUDE.md spec/ .claude/settings.json`.
- **[adoption-only]** `SDLC.template.md` + **[installable]** `sdlc-setup.md` +
  `reference/GATE_RECIPES.md`: the coverage floor now has a recorded home — a
  `{{COVERAGE_FLOOR}}` line in the gate section (`TBD from first CI run` until one
  exists), resolved by both setup modes, enforcement staying in CI. Previously the
  "record TBD" instruction named no destination.
- Smaller finds, same pass: the canonical template never stated two rules the installed
  commands enforce (push at slice end; the conditional review lenses) — both added
  **[adoption-only]**; `{{STOP_COMMAND}}` had no producing interview question (now
  asked with the run command, both modes, **[installable]**); the formatter was asked
  for and never routed anywhere (now in scaffold step 1); `plan-phase.md` read a
  "product direction" section `PROJECT_INDEX.template.md` does not scaffold (pointer
  trimmed, **[installable]**); the root file tree was missing `.gitattributes` and
  `.gitignore` (invariant 5's first mechanical catch).

## 0.2.0 — 2026-07-19

Version identity, an update path, and the two defects the first field report found in the
shipped kit.

### Fixed
- **[installable]** `commands/end-slice.md` asserted *"The typecheck baseline is green"*
  unconditionally, which is false on any project adopted with a red baseline — a mode the
  kit advertises as supported. Both `end-slice.md` and `end-phase.md` now read the gate
  baseline from `spec/SDLC.md` instead of assuming it. Root cause, now a kit invariant:
  **a command file may not state a fact about the adopting project.**
- **[installable]** `/sdlc-setup` asked for a coverage floor defaulting to **70%**, and
  **[adoption-only]** `reference/GATE_RECIPES.md` justified that number as "Dungeon Daddy
  uses ≥70%" — a constant imported from another project and never measured. Both removed.
  The floor is now set from the first green CI run using CI's exact invocation, and only
  ever raises. *A remembered constant is not a measurement.*

### Added
- `sdlc-kit/VERSION`, `sdlc-kit/MANIFEST.sha256`, `sdlc-kit/LICENSE`, and a bundle-local
  `sdlc-kit/README.md`, so a downloaded artifact is self-describing, verifiable, and
  carries its MIT license text as redistribution requires.
- This changelog.
- Root README: *Updating an adopted project* — the manual update procedure and the
  file-ownership table.
- Release workflow (`.github/workflows/release.yml`): packages `sdlc-kit/` as
  `sdlc-kit-<version>.tar.gz` and `.zip` on tag push and attaches them to the release.
- **[adoption-only]** `{{KIT_VERSION}}`/`{{ADOPTION_DATE}}` in `SDLC.template.md`, so a
  later update knows its baseline without guessing, and `{{GATE_BASELINE}}`, which gives
  the measured gate baseline one definite home for the commands to read. **[installable]**
  `/sdlc-setup` resolves all three — the baseline only after it has actually measured it.

- `.gitattributes` pinning text files to LF. Checksums are only meaningful if the bytes
  are identical on every platform; without this a Windows checkout hashes CRLF and a
  Linux one hashes LF, so the same kit version would report drift on every file.

### Changed
- Repo restructured: `sdlc-kit/` is now the shippable product; the root holds
  documentation *about* the kit. **[installable]** — the only installable file this
  touched is `commands/sdlc-setup.md`, whose close-out step pointed at a kit-local README
  that the restructure removed; it now points at the home repo. No behavior change.

## 0.1.0 — 2026-07-19

Initial extraction of the Agentic SDLC kit from the Dungeon Daddy project: the two-mode
`/sdlc-setup` command, the four daily commands (`plan-phase`, `next-slice`, `end-slice`,
`end-phase`), the vendored MIT TDD skill set, five templates, and the gate/skills
reference docs.

Tagged retroactively at `bdc0ba1`. The commit after the initial one added only
`FIELD_REPORT.md` and touched no installable file, so the installable surface is identical
across both commits — which is what makes the retroactive tag honest.
