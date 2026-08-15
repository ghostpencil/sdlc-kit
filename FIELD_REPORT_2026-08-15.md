# SDLC Kit — Field Weaknesses Revealed by `ai-news-dashboard`

**Purpose:** Planning input for Claude Code.  
**Field project:** `ai-news-dashboard` (four completed phases, Copilot CLI adoption).  
**Kit baseline reviewed:** current `sdlc-kit` main as of 2026-08-14 (0.22.0).  
**Intent:** Identify weaknesses exposed by the field project before deciding what to change in the kit.

---

## 1. Executive summary

The `ai-news-dashboard` field project is strong evidence that SDLC Kit can produce a maintainable, well-tested application while an agent performs most implementation work. The repository has meaningful behavioral tests, CI/static-analysis gates, explicit specs, durable retrospectives, and several examples where the process caught defects that ordinary slice implementation would have missed.

The largest weakness exposed by the project is **not implementation quality**. It is **longitudinal product-contract preservation**.

The kit is currently very strong at supervising the work directly in front of it:

```text
current phase → current slice → TDD → gate → review → mutation → verification → owner acceptance
```

It is weaker at guaranteeing that a later phase does not accidentally erase an owner-ratified behavior from an earlier phase:

```text
Phase 01 contract
      ↓
Phase 02 rewrite
      ↓
current-phase tests/review all green
      ↓
old product behavior can nevertheless disappear
```

The current context-minimization rule contributes to this risk: `/next-slice` intentionally reads the current phase spec and avoids loading older specs unless needed. `/end-phase` reviews the arc against the current phase's exit criteria and acceptance checklist. That is good for context discipline, but there is no compact authoritative artifact containing the **surviving product behaviors later phases must preserve**.

The field project also exposed secondary weaknesses around trust-boundary persistence, historical dead artifacts, human onboarding, harness-specific enforcement complexity, and process cost. Several harness/enforcement problems were already absorbed into later kit releases; they remain useful architectural lessons rather than necessarily requiring new features.

---

# 2. Priority 0 — Cross-phase product-contract erosion

**Status:** CONFIRMED FIELD GAP  
**Severity:** HIGH  
**Root question:** Where do product behaviors live after the phase that introduced them is closed?

## Evidence from `ai-news-dashboard`

Phase 01 contains explicit owner-decided requirements including:

- an empty dashboard showing the **last refresh status**;
- a dashboard **status panel** showing per-source `OK/WARN` and failure reasons;
- refresh results being visible to the user through that status surface;
- a feed-only detail view showing required metadata and **full sanitized feed content**;
- application-owned URL/content safety checks.

The current application does not fully represent that contract:

- `DashboardController` has no refresh-status dependency or status model;
- `dashboard.html` renders the item list, pagination, source name and tags, but no per-source refresh status panel;
- the empty state says `No news items yet`, but does not show the last refresh status;
- the feed detail view does not show authors or tags;
- `NewsItem.summaryBasis` is truncated to 4,096 characters, so the detail surface cannot necessarily display the full original sanitized feed content promised by Phase 01.

The current test suite can remain green while these older ratified behaviors are absent.

## Likely process mechanism

The current process deliberately minimizes context:

- `/next-slice` reads `PROJECT_INDEX`, the **current phase spec**, and only other specs needed by the current slice;
- old phase specs become historical records;
- `/end-phase` reviews the arc against the **current phase's** exit criteria;
- the owner acceptance checklist is taken from the **current phase's** user-visible behaviors.

This creates a blind spot when a later phase rewrites a surface created by an earlier phase.

Example:

```text
Phase 01:
Dashboard must show refresh health

Phase 02:
Rewrite dashboard as cards + pagination

Phase 02 implementation:
passes Phase 02 acceptance

Result:
card dashboard is correct
refresh-health behavior silently disappears
```

No individual step is necessarily malfunctioning. The missing input is the durable contract that Phase 02 was obligated to preserve.

## Planning objective

Find the smallest mechanism that preserves **current externally observable product truths** across phases without forcing every fresh agent session to load all historical phase specifications.

A likely shape worth investigating is a compact artifact such as:

```text
CURRENT PRODUCT CONTRACT

Dashboard
- shows newest items
- shows refresh health/status
- empty state includes last refresh state
- external links follow safety policy
- pagination exposes at most 100 items

Refresh
- only one refresh runs at a time
- source failures degrade rather than abort the run
- manual refresh requires admin token

Persistence
- stable-key ingest is idempotent
- canonical duplicates merge provenance
- firstSeenAt is immutable
```

**Do not adopt this shape without re-deriving it.** The important requirement is the behavior, not the filename or document format.

## Constraints on any solution

Any fix must preserve:

- context minimization;
- one authoritative source per fact;
- phase specs as historical decision records;
- current phase specs as build plans;
- bounded `PROJECT_INDEX` size;
- owner authority over behavior changes;
- no requirement to load every old phase into each session.

Avoid solving the problem by simply saying "read all previous phase specs."

## Success criteria for a solution

A later phase that rewrites a previously implemented surface must mechanically or procedurally encounter the surviving behavior contract before implementation and before phase acceptance.

A deliberate behavior removal must become an owner decision rather than silently looking like an implementation simplification.

---

# 3. Priority 0 — Tests do not necessarily preserve old owner-ratified behavior

**Status:** CONFIRMED FIELD GAP  
**Severity:** HIGH  
**Related to:** Cross-phase contract erosion, but not identical.

The current dashboard tests thoroughly verify the Phase 02 card/pagination behavior, including:

- empty-state text;
- title/summary/external links;
- internal detail fallback;
- source display;
- tag badges;
- batch loading rather than N+1 behavior;
- pagination bounds.

They do **not** pin the Phase 01 refresh-status behavior that is no longer present.

This means the kit's strong testing discipline can produce an important false sense of longitudinal safety:

> Every current test can be legitimate, test-first, mutation-sensitive, and green while a behavior ratified three phases ago has disappeared because no current test represents it anymore.

## Planning objective

Determine how durable product behaviors become durable regression obligations.

Questions Claude Code should investigate:

1. Should an owner-ratified externally observable behavior require at least one durable acceptance/regression test?
2. If a later phase intentionally removes that behavior, how is the corresponding test retirement tied to an owner decision?
3. Can `/plan-phase` perform a consequence sweep against the current product contract and identify existing tests that should remain green?
4. Can `/end-phase` verify not only the new phase contract but also that the relevant retained contract still has test coverage?
5. How do we avoid turning the suite into brittle UI snapshot tests?

The desired property is:

```text
ratified behavior
      ↓
implementation
      ↓
durable behavioral pin
      ↓
later rewrite
      ↓
old behavior either survives
OR owner explicitly retires/amends it
```

Do not solve this by requiring one test per sentence in a spec. Preserve behavioral altitude.

---

# 4. Priority 1 — Trust-boundary decisions can decay after the phase that created them

**Status:** CONFIRMED PROCESS GAP / SECURITY IMPACT REQUIRES RUNTIME VALIDATION  
**Severity:** HIGH for high-consequence systems

Phase 01 explicitly states that external feeds are untrusted and that **application-owned URL and content safety checks** are responsible for normalization/safety.

The current code sanitizes textual feed content effectively, but canonical URLs flow from feed adapters into persistence and then into Thymeleaf `href` attributes without an obvious application-owned allow-list for safe external schemes.

For example, the Hacker News adapter accepts the feed-provided `url` when present and the dashboard/detail templates render `canonicalUrl` as a link.

The important kit weakness is broader than this specific possible bug:

> A trust-boundary rule can be ratified in an old phase, then become invisible to later phases that modify the same data path.

The current secure review lenses are strong when triggered by the **current change**, but a later UI rewrite can expose pre-existing unsafe data without introducing the original ingestion code.

## Planning objective

Determine how high-consequence/trust-boundary decisions survive as active constraints rather than historical prose.

Potential questions:

- Should the durable product/system contract include a compact **trust-boundary invariant** section?
- When a phase touches a consumer of untrusted data, should `/plan-phase` re-load applicable trust-boundary invariants even when the producer was built in an older phase?
- Can the consequence sweep derive relevant invariants from changed surfaces without loading historical specs wholesale?
- Should security-sensitive owner decisions require named tests or mechanical checks that survive refactors?

Do not add a generic enterprise threat-modeling framework unless field evidence requires it.

---

# 5. Priority 1 — Whole-arc review is phase-complete, not necessarily product-regression-complete

**Status:** CONFIRMED DESIGN LIMITATION  
**Severity:** MEDIUM-HIGH

Current `/end-phase` whole-arc review correctly asks whether the arc delivered the **current phase** and applies the unconsumed-artifact lens to things introduced by the arc.

That is valuable and should remain.

But the `ai-news-dashboard` example shows a different review question is also needed somewhere:

> Did this arc accidentally invalidate a surviving behavior or invariant from the product that existed before the arc?

This is not the same as reviewing the current phase against its own exit criteria.

## Planning objective

Investigate whether phase planning/review needs a narrowly bounded **regression contract** input.

The likely sequence is:

```text
current phase spec       retained product contract
        \                      /
         \                    /
          → implementation ←
                 ↓
           whole-arc review
                 ↓
     new behavior + preserved behavior
```

Avoid making the reviewer compare every phase against every historical decision.

---

# 6. Priority 1 — Historical unconsumed artifacts can survive indefinitely

**Status:** CONFIRMED EXAMPLE  
**Severity:** MEDIUM

`SourceRegistry` persists an `enabled` column and initializes it to `true`, but the current production code has no reader/getter or behavior that consumes the field.

The current whole-arc **unconsumed artifact** lens is intentionally scoped to entities, columns, endpoints, config keys, or public APIs introduced by the current arc.

That means it is good at preventing **new** unconsumed artifacts but is not a general detector for old artifacts that survived from prior phases.

## Planning objective

Decide whether this needs any new kit mechanism at all.

Possible existing homes to evaluate first:

- STABILIZATION phase discovery;
- recurring cleanup/backlog process;
- code-intelligence/visualization tooling;
- periodic dead-artifact sweep rather than every phase.

Do not expand every whole-arc review into a whole-repository dead-code audit.

A useful test is whether an artifact like `SourceRegistry.enabled` would naturally surface during the existing stabilization workflow. If yes, improve that path instead of inventing a new mandatory step.

---

# 7. Priority 1 — Owner hand-back is behavior-rich but structurally thin

**Status:** OBSERVED OPPORTUNITY  
**Severity:** MEDIUM

The existing owner hand-back gives a concise plain-English description of what a slice or phase now does. That is appropriate and should remain the default human altitude.

However, the dashboard regression illustrates a class of surprise that may be easier for a human to notice structurally than textually:

```text
expected change:
Dashboard UI rewrite

actual structural footprint:
DashboardController        CHANGED
Dashboard template          CHANGED
Refresh-status consumer     REMOVED / NO LONGER CONNECTED
```

The planned Understand Anything integration is a promising fit because it addresses a **supervision/comprehension problem**, not a harness-execution problem.

## Planning objective

Continue the visual-impact experiment, but preserve these boundaries:

- optional capability;
- deterministic Git denominator;
- graph is derived evidence, not source truth;
- visualization is not a gate;
- unmatched/stale graph coverage must be loud;
- no claim that unshown nodes are unaffected;
- no mandatory sixth owner halt.

The visualizer should be evaluated on one question:

> Did it help the owner identify a useful question or surprising structural consequence they would otherwise have missed?

It should **not** be presented as the primary fix for cross-phase contract preservation. A visualizer can expose a surprise; the process still needs an authoritative definition of what must be preserved.

---

# 8. Priority 1 — Human onboarding is weaker than agent onboarding

**Status:** CONFIRMED PROJECT SYMPTOM  
**Severity:** MEDIUM-LOW

The field repository has excellent agent-facing orientation:

- `CLAUDE.md`;
- `PROJECT_INDEX`;
- `SDLC.md`;
- `TESTING.md`;
- phase specs;
- retrospectives.

It has no simple root project README explaining to a human:

- what the application is;
- prerequisites;
- how to run it;
- how to trigger refresh;
- where data is stored;
- how to run the gate/tests;
- how the SDLC Kit is used in this repository.

The project is easier for a fresh AI session to orient into than for a fresh human developer.

## Planning objective

Determine whether `/sdlc-setup` or phase-one planning should ensure a minimal human README exists for projects that lack one.

Keep this lightweight. Do not duplicate `CLAUDE.md` or `spec/SDLC.md`.

A README should be a human entry point with links to deeper process docs, not another source of process truth.

---

# 9. Priority 2 — Harness-specific enforcement is effective but expensive and brittle

**Status:** FIELD-CONFIRMED THEME; MANY SPECIFIC FAILURES ALREADY ADDRESSED IN 0.19–0.22  
**Severity:** MEDIUM architectural concern

`ai-news-dashboard` produced unusually useful evidence about enforcement portability:

- TDD guards could initially be satisfied by the wrong kind of failing command;
- compound commands were misclassified;
- refusal feedback was initially invisible at the moment it mattered;
- guard behavior incentivized synthetic/test-theater workarounds;
- legitimate close-out refactor/mutation edits conflicted with the write guard;
- hook shells used a different JDK from the project shell;
- skill activation evidence could not observe owner-typed slash commands;
- coverage checks differed in where they exposed the measured number;
- Copilot model routing required operator intervention.

Many of these findings were correctly absorbed into later kit releases. The remaining weakness is the **maintenance shape**:

> every harness adapter can become a small platform with its own event semantics, shell behavior, failure direction, permissions and blind spots.

## Planning objective

Prefer an explicit harness-conformance strategy over more ad hoc adapter code.

Before adding a new harness such as Cursor, define the minimum semantics the kit requires and bench them:

```text
Required harness semantics
- command/skill discovery
- shell execution semantics
- pre/post tool hook payloads
- failed-command observability
- stop-hook behavior
- deny/block mechanism
- project instruction loading
- owner-typed command observability (or known absence)
- model-routing control
- MCP/tool invocation
```

Then implement only the adapter needed to express kit invariants using those primitives.

The kit should own **engineering semantics**, not recreate harness capabilities.

---

# 10. Priority 2 — Process cost is substantial and needs continued value auditing

**Status:** OBSERVED TRADEOFF  
**Severity:** MEDIUM for adoption

For a relatively small application, the repository contains a large amount of SDLC/process material relative to production code. That was appropriate for a field laboratory, but it is still adoption evidence.

The risk is not simply "too much Markdown." The real risk is:

> a step may survive because it sounds prudent rather than because it produces useful catches or supervision value.

The kit has already moved in the right direction with field-arc clocks, deletion candidates, attributed lens catches, and trial-first enforcement.

## Planning objective

Continue applying the existing evidence standard aggressively:

- every optional quality/review mechanism should have a measurable value hypothesis;
- steps with no confirmed catches after their agreed exposure should be simplified, redirected, or deleted;
- recurring human friction should be measured as a cost, not dismissed as user error;
- do not introduce "Quick / Standard / High" process profiles without field evidence that the standard process is materially harming low-risk work;
- avoid making `ai-news-dashboard`'s laboratory-level instrumentation mandatory for every adopter unless the evidence justifies it.

This is a pressure to **simplify**, not a recommendation for a new feature.

---

# 11. Important non-weaknesses — do not “fix” these

The field project supports keeping these properties:

## 11.1 Fresh context per slice

This appears valuable. The cross-phase contract problem should not be solved by abandoning context hygiene.

## 11.2 One phase / one branch / one PR

Nothing in this project demonstrates that the arc shape is a problem for the intended single-owner workflow.

## 11.3 Strong TDD / mutation / real-path verification

These repeatedly produced useful evidence. Refine enforcement, but do not weaken the underlying requirements because hooks were imperfect.

## 11.4 Whole-arc review

The arc review has caught composition defects that slice review could not. The problem is its **input scope**, not the existence of the review.

## 11.5 Owner halt model

The five owner halt points remain coherent. Do not add a new halt merely to support product contracts or visualization.

## 11.6 Harness delegation

Do not respond to Cursor/Kiro/Copilot capability by building competing execution infrastructure. The field project reinforces that the kit's durable value is the methodology/evidence layer.

---

# 12. Recommended Claude Code planning order

Do **not** implement every item above as separate features.

Start by asking Claude Code to re-derive and cluster the findings against the current 0.22.0 tree.

Recommended order:

### Investigation A — Longitudinal contract preservation

Treat items 2–5 as potentially one root problem:

```text
Where do surviving product truths live,
and how are later plans/tests/reviews forced to encounter them?
```

The desired result may be one small new artifact plus changes to `/plan-phase` and `/end-phase`, rather than multiple new mechanisms.

### Investigation B — Trust-boundary durability

Determine whether the same product-contract mechanism can carry high-consequence invariants such as external URL safety. Prefer reuse over a parallel security-contract system.

### Investigation C — Historical artifact cleanup

Test whether existing STABILIZATION machinery should catch dormant artifacts before adding a new step.

### Investigation D — Owner comprehension visualization

Proceed as an optional field trial. Measure owner questions/surprises, not merely successful overlay generation.

### Investigation E — Human onboarding

Decide whether a minimal README expectation belongs in setup or project planning. Keep it separate from lifecycle truth.

### Investigation F — Harness adapter contract

Before Cursor support, define and bench required harness semantics. Do not port by filename analogy.

---

# 13. Required implementation discipline for this improvement batch

When Claude Code turns this document into a feature plan:

1. **Re-verify every finding against the current kit tree and the field project.** This document is a field report, not an instruction to implement its suspected causes verbatim.
2. Mark each finding **measured**, **suspected**, or **already addressed**.
3. Collapse multiple symptoms into one root cause where possible.
4. Prefer modifying an existing lifecycle step over adding a new command/skill/hook.
5. Preserve context minimization and the five owner halts.
6. Do not introduce a second source of truth for project behavior.
7. Pre-register the value criterion for any new mechanism.
8. For deterministic checks, prove the failure mode before trusting the check.
9. Field-test the change on a project with at least one earlier-phase behavior that a later phase rewrites.
10. If a proposed mechanism adds ceremony but cannot name the defect class it prevents, reject it.

---

# 14. Suggested validation scenario

A useful fixture/trial should deliberately reproduce the failure class observed here.

Example:

## Phase 01

Ratify and implement:

```text
Dashboard displays:
- news cards
- a persistent last-refresh status panel
```

Pin both behaviors with appropriate tests.

## Phase 02

Plan:

```text
Rewrite dashboard cards and pagination.
```

Do **not** mention refresh status in the Phase 02 request.

The improved kit should force one of these outcomes before merge:

```text
A. Status behavior is preserved automatically because it is a retained contract.

B. Agent identifies the conflict and asks the owner whether the behavior should be removed.

C. A deterministic/behavioral check fails because the retained contract was violated.
```

The unacceptable outcome is the current failure mode:

```text
new phase requirements satisfied
+ current tests green
+ current review clean
+ old owner-ratified behavior silently gone
```

This scenario directly tests whether the fix solves the field failure rather than merely producing another document.

---

# 15. Bottom line

The `ai-news-dashboard` project does **not** suggest that SDLC Kit's core problem is poor AI-generated code. It suggests the opposite: the immediate implementation discipline is strong enough that the remaining weaknesses have moved up a level.

The most important open problem is now:

> **How does an owner preserve the accumulated product contract while agents work phase-by-phase with intentionally bounded context?**

That is a methodology problem worth owning.

Solve that before adding broader execution machinery.
