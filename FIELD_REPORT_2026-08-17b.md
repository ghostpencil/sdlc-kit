# Field report: `ai-news-dashboard` Phase 05 retro (2026-08-17) — backfill adjudication gap, guard matcher misfires

**Source:** [sdlc-kit#8](https://github.com/ghostpencil/sdlc-kit/issues/8), filed
2026-08-17 — the **eighth** field report, from the second adopter (Copilot CLI, Java/Spring
Boot), whose earlier findings came in as issues #3–#6 and as the whole-project review filed
as `FIELD_REPORT_2026-08-15.md`. Written against **0.24.0** at the Phase 05 boundary; the
first arc anywhere to run the 0.23.0 product-contract backfill. Reproduced verbatim (this
adopter is the owner's own project and is not anonymized). Two reports arrived the same
day; the seventh is `FIELD_REPORT_2026-08-17.md`. The triage lives in `FEATURE_PLAN.md`
§63.

Project: ai-news-dashboard — kit adopted 2026-08-03 (existing mode), currently kit
0.24.0. Window: Phase 05, 2026-08-15 → 2026-08-17 — four slices (S1 shared test
helpers, S2 seed pin, S3 per-item log demotion, S4 backfill marker + ruleset hash),
one PR (#13, merged `8e98917`). Headline numbers: 104 tests / 0 failures; gate
baseline held at 0 for a 5th consecutive arc; coverage floor ratcheted 83% → 88%
(first successful ratchet, measured 88.9% off the enforced run's JaCoCo report);
`spec/PRODUCT_CONTRACT.md` backfilled for the first time (20 behavior entries +
2 trust-boundary entries, owner-confirmed). Interview: owner reported the phase was
smooth, no overrides, nothing to delete.

## 1. Ratified-but-absent behaviors have no adjudication step

**HIGH.** The one-time contract backfill in `/end-phase` walks prior ratified
decisions and enters "only what they confirm as still-current, never an inference"
(`commands/end-phase.md`, step 7 *Product-contract reconcile* — quoted from the
installed copy `.github/skills/end-phase/SKILL.md`). Nothing in that step — or
anywhere — asks the complementary question: **which ratified behaviors are absent
from the tree, and are they restored or formally dropped?**

Evidence: the kit's own field report (`FIELD_REPORT_2026-08-15.md` §2–3, written
against this project) lists Phase 01 behaviors missing from the app today — the
per-source `OK/WARN` status panel (P01 D23), last-refresh status in the empty state
(P01 D6), authors/tags and full sanitized feed content in the detail view (P01 D22,
with `summaryBasis` truncated at 4,096 chars). During this close's backfill, the
draft contract simply omitted those decisions and the owner confirmed the draft —
the erosion came within one question of being ratified by omission. Only the
co-development read of the kit-side field report surfaced it. Owner ruling this
session: **restore** (backlog entry added).

Fix: the backfill (and the per-close reconcile) gains a second direction — for each
ratified decision in prior phase specs, if the behavior is absent from the tree,
surface it for an explicit restore/drop ruling; a drop ruling amends the source
phase spec. Homes: `commands/end-phase.md` (the backfill bullet) and
`templates/PRODUCT_CONTRACT.template.md` (the backfill note in its entry-grammar
comment).

## 2. TDD guard's test-command matcher fires on any command text mentioning mvn+test

**LOW.** The Java `{{TEST_CMD_PATTERN}}` is `*mvn*test*|*gradlew*test*`
(`sdlc-kit/reference/GATE_RECIPES.md`, recipe table — line 407 at kit 0.25.0),
instantiated at `.github/hooks/sdlc-tdd-guard.sh:271` as `*mvn*test*) ;;`. The net
catches any shell command whose *text* mentions both words: this phase it fired on a
`git commit -m` whose body quoted the RED run commands (S3 close, 2026-08-17) and
twice on `Add-Content` appends to a RED-record file quoting the same (S4 close).
Harmless — the notice admits the run is unaffected — but three spurious notices in
one phase trains message fatigue against the guard's real refusals.

Fix: anchor the match to the command's first token (`mvn`, `mvnw`, `./mvnw` at
start) rather than substring-anywhere, or strip quoted-string content before
matching. Homes: `sdlc-kit/reference/GATE_RECIPES.md` (the pattern table and the
"keyed on the runner" note beneath it) and every instantiated
`sdlc-tdd-guard.sh`.

## 3. Acceptance-checklist items can be unexercisable live

**LOW.** Phase 05 acceptance item 4 (malformed feed item → DEBUG-only logging) could
not be driven through a real caller path at slice close *or* phase end — feed URLs
are hardcoded, so no fixture seam exists. It passed on three adapter test pins plus
the owner's ruling, and `/end-phase` step 3 honestly reported it "not exercised
live". But nothing at plan time asks whether each acceptance item *can* be exercised
through a real path — the silence sits between `commands/plan-phase.md`'s
acceptance-checklist authorship and `commands/end-phase.md` halt 3's exercise. Fix:
`/plan-phase` gains a one-line check per acceptance item — name the path a real
caller reaches it by, or flag it test-only at plan time rather than discovering it
at the halt. Project half (the fixture seam) is backlogged.

## What worked well

- **S4's live-boot verification caught the arc's worst defect pre-PR**: the
  `@Modifying` bulk updates threw `TransactionRequiredException` at real boot,
  masked by test transactions — found by `FileBackedSchemaBootTest` and the live
  boot, exactly the startup/wiring gap change-verify exists for. Fixed in
  `ec3b119`; disposition: closed.
- **The 0.24.0 coverage-ratchet procedure worked on first use**: measured figure
  read from the JaCoCo report artifact of the enforced `mvn test` run (88.9%),
  threshold set in `pom.xml` `coverage-check`, both homes (SDLC Records, index)
  reconciled, CI green on the push. This closes retro 2026-08-11 finding 2's
  practical question.
- **Zero guard denials all phase** — after Phases 03–04's thrash, the bare-command
  discipline plus the refactor license held without a single recorded denial.
- **Slice commit bodies carried complete step evidence** (`RED:` / `quality:` /
  `mutation:` / `verify:` lines, skips stated with reasons) on all four slices.
- **The contract backfill landed at all** — the P0 mechanism from the field report
  exercised within two days of adoption.

## Step evidence

| Step | Evidence this window |
|---|---|
| Gate (4 steps) | ran every slice + phase end; caught: SpotBugs `UNSAFE_HASH_EQUALS` in S4 close (fixed `ec3b119`) |
| TDD observed-RED | ran — 8 recorded reds in S4, 3 in S3, pin-style noted where the assertion passed immediately (S2, two S4 pins) |
| change-simplify | ran all 4 slices; caught: 4 moves (S4), 1 (S3), 1 (S1) |
| diff-review | ran all 4 slices + whole-arc; caught: S1 `LogCaptor` level-restore narrowing (slice review, fixed in `802df95`) |
| mutation check | ran per commit bodies (6/1/4 guards, each seen to fail); the `mutation-testing` skill tool was not dispatched in the window — checks performed inline |
| change-verify | S1/S2/S3 skipped with stated reasons in commit bodies; S4 ran (caught the `TransactionRequiredException`); end-phase ran (boots A–F, live refresh, off switch, rule-edit cycle) |
| Owner acceptance | ran — checklist items 1–4 ruled met 2026-08-17 |
| Edit-time hook | ran all phase (advisory feedback present); two matcher-misfire notices (finding 2) |
| Skill ledger | alive all window (`.git/sdlc-skill-ledger.jsonl`, this clone); slash-typed closes leave no line, as documented |

## Suggested priority

| # | Change | File(s) | Effort |
|---|---|---|---|
| 1 | Backfill/reconcile gains the ratified-but-absent adjudication direction | `commands/end-phase.md`, `templates/PRODUCT_CONTRACT.template.md` | S |
| 2 | Anchor the test-command matcher to the first token | `sdlc-kit/reference/GATE_RECIPES.md`, instantiated `sdlc-tdd-guard.sh` | S |
| 3 | Plan-time "how is each acceptance item exercised" check | `commands/plan-phase.md` | S |

## Cross-cutting theme

The process's weak direction is longitudinal: it supervises the work in front of it
well, but the past→present check (ratified behavior still present?) only got storage
this phase (the contract), not yet the adjudication step that makes drift an owner
decision. Finding 1 is that gap's sharp edge.
