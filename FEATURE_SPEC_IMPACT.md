# Feature Spec — Owner Change Impact Visualization

**Target:** `sdlc-kit`  
**Purpose:** Add an optional, owner-facing visualization of what changed in a slice or phase and what existing code may be affected.  
**Primary integration:** Understand Anything  
**Status:** Proposed feature for implementation and field trial

---

## 1. Problem

SDLC Kit is designed so that a capable developer can remain responsible for product intent, design decisions, acceptance, and merge/deploy decisions while delegating most implementation work to an AI coding agent.

That creates a deliberate asymmetry:

- the agent sees and edits the implementation in detail;
- the owner should not need to line-review every generated change;
- the owner still needs enough understanding to supervise the work responsibly.

The current hand-back summaries explain what the agent believes changed, but they do not give the owner an independent visual view of the structural footprint of the work.

A useful owner-facing view should answer:

1. **What components changed directly?**
2. **What existing components may be affected by those changes?**
3. **Which architectural layers or subsystems were touched?**
4. **Does the implementation footprint look plausible for the behavior the owner approved?**
5. **Is anything surprising enough that the owner should ask a question before allowing the lifecycle to continue?**

Understand Anything already maintains a code knowledge graph and its dashboard already supports a diff overlay containing changed and affected node IDs. The feature should use that capability as an optional comprehension surface.

---

## 2. Goal

Give the owner a visual, architecture-level understanding of a slice or phase without requiring them to read the implementation diff.

The feature should let an owner move from:

> “The agent says this slice changed authentication.”

to:

> “I can see that authentication service, login-attempt persistence, and audit integration changed, and that the admin unlock flow may be affected.”

This is intended to improve **human supervision bandwidth**, not replace code review or verification.

---

## 3. Non-goals

This feature is **not**:

- a correctness gate;
- verification evidence;
- a replacement for `diff-review`;
- a replacement for tests, mutation checks, or `change-verify`;
- proof that no unshown component is affected;
- an authoritative architecture model;
- a reason to trust an LLM-generated summary without source evidence;
- a requirement that every SDLC Kit adopter install Understand Anything;
- a generic code-graph subsystem owned by SDLC Kit;
- a reason to automatically refresh an LLM-generated knowledge graph on every slice;
- a reason to automatically open a browser or dashboard window.

The source tree, Git history, tests, CI, deployment records, and other enforcing artifacts remain authoritative.

The visualization is a **human comprehension aid**.

---

## 4. Core design principles

### 4.1 Optional capability

Understand Anything is optional.

An adopter without a usable Understand Anything graph must continue through the normal SDLC unchanged.

The feature must never turn absence of the visualizer into a failed gate or blocked close-out.

Absence must also never be silent. The owner-facing hand-back should say that the impact view was unavailable and why.

### 4.2 Deterministic impact selection

The set of directly changed and graph-connected affected nodes should be derived mechanically from:

1. a Git change set; and
2. the existing Understand Anything knowledge graph.

The SDLC agent may explain the result in plain English, but it should not decide from intuition which nodes belong in the visual overlay.

### 4.3 No second source of truth

Understand Anything graph data is derived.

Its summaries and architecture classifications may include LLM interpretation.

Therefore:

```text
source / config / git
        ↓
authoritative project state

Understand Anything graph
        ↓
derived structural model

diff overlay
        ↓
derived visualization

agent explanation
        ↓
human-readable interpretation
```

No SDLC decision may rely on the visualization as proof that an affected component does or does not exist.

### 4.4 Loud incompleteness

A partial graph must not produce a confident complete-looking result.

If changed files have no corresponding graph nodes, the output must report them explicitly.

If the graph is missing, invalid, or known to be stale, the output must say so.

A useful incomplete visualization is acceptable.

A visualization that hides its incompleteness is not.

### 4.5 Preserve the existing owner-control model

The feature must not create a new mandatory owner halt.

It should enrich existing hand-backs and halt surfaces.

The owner may choose to open and inspect the visualization, but the feature should not force a new approval ceremony merely because visualization is available.

---

## 5. Understand Anything integration contract

Understand Anything currently stores its graph in:

```text
.ua/knowledge-graph.json
```

with legacy projects potentially using:

```text
.understand-anything/knowledge-graph.json
```

Use the legacy directory when it already exists; otherwise use `.ua`.

The existing Understand Anything diff overlay format is:

```json
{
  "version": "1.0.0",
  "baseBranch": "<base ref or descriptive base>",
  "generatedAt": "<ISO timestamp>",
  "changedFiles": [
    "<path>"
  ],
  "changedNodeIds": [
    "<node id>"
  ],
  "affectedNodeIds": [
    "<node id>"
  ]
}
```

The dashboard reads this from:

```text
<UA_DIR>/diff-overlay.json
```

SDLC Kit should generate that overlay directly rather than requiring the AI to invoke the `/understand-diff` skill and reason its way through the graph.

The existing Understand Anything skill may remain available to the owner or agent for deeper exploration, but it is not the execution mechanism for this feature.

---

## 6. Proposed SDLC Kit component

Introduce one small kit-owned adapter conceptually named:

```text
sdlc-impact
```

The exact implementation language and installed path should follow the kit's existing portability rules and be chosen during implementation.

The adapter should support two logical modes:

```text
sdlc-impact slice
sdlc-impact phase <base-ref>
```

The adapter's responsibilities are intentionally narrow:

1. establish the correct Git change set;
2. load the existing Understand Anything graph;
3. map changed files to graph nodes;
4. traverse one graph hop to connected nodes;
5. identify affected architectural layers where available;
6. detect unmatched changed files;
7. assess graph freshness using graph metadata where available;
8. write `diff-overlay.json`;
9. print a compact result the SDLC command can include in its hand-back.

It should not generate architectural prose using an LLM.

---

## 7. Slice change boundary

### 7.1 Capture the slice base

A slice needs its own base because all slices accumulate on the same phase branch.

`main...HEAD` would represent the whole phase, not the current slice.

After `/next-slice` has:

- oriented;
- completed scope confirmation/re-derivation;
- checked out or created the correct arc branch;
- integrated a moved main branch if required;

but **before the TDD implementation begins**, record:

```text
git rev-parse HEAD
```

as the slice base.

This state is transient and should live under `.git`, for example:

```text
.git/sdlc-impact/slice-base
```

The exact path is implementation-owned, but it must not become committed project state.

### 7.2 Slice change set

At slice-ready time, the adapter should derive all project files changed since the captured slice base, including:

- committed changes created during the slice;
- staged tracked changes;
- unstaged tracked changes;
- untracked non-ignored project files.

Generated Understand Anything files must be excluded from the change set.

The change set is the denominator for the slice visualization.

---

## 8. Slice lifecycle integration

There are two distinct useful views of a slice.

### 8.1 Slice preview — before owner authorizes close-out

Current `/next-slice` deliberately stops when the slice is ready and lets the owner decide whether to invoke `/end-slice`.

Before that hand-back, when Understand Anything data is available:

1. generate the slice impact overlay from the captured slice base to the current working state;
2. print the impact summary;
3. include that summary in the normal slice-ready hand-back;
4. tell the owner that the Understand Anything dashboard can visualize the changed and affected components;
5. stop exactly where `/next-slice` stops today.

Example hand-back addition:

```text
Architecture impact:
- 6 changed files mapped to 9 graph components
- 14 existing components are one hop from those changes
- Layers touched: API, Service, Persistence
- 1 changed file is not represented in the current graph
- Impact visualization is ready in Understand Anything
```

This is a **preview** because `/end-slice` may still apply quality, review, mutation, or verification fixes.

### 8.2 Final slice impact — after close-out changes

`/end-slice` may legitimately modify the slice after the owner viewed the preview.

Therefore the final visualization must not silently remain the preview.

After all close-out fixes are complete and immediately before or after the final slice commit, regenerate the slice impact from the same captured slice base.

The end-slice hand-back should state the final impact result.

If the final graph footprint differs materially from the preview, state that explicitly.

Examples:

```text
Impact view unchanged from the owner preview.
```

or:

```text
Impact view changed during close-out:
- review fix added AuditService to the affected set
- no new architectural layer was introduced
```

This is informational, not a new owner halt.

If a close-out finding creates a genuine owner-facing design decision, the existing design-question halt still applies independently.

### 8.3 Clear slice state

Once the slice is closed successfully, clear the transient slice-base state so a future session cannot accidentally reuse it.

A missing, ambiguous, or stale slice base must fail the visualization attempt loudly but must not block normal SDLC close-out.

---

## 9. Phase lifecycle integration

The phase view represents the whole arc.

Its change set should be derived from the configured base branch to the current phase branch.

The base branch must come from project SDLC state or be passed explicitly. Do not assume the branch is named `main`.

### 9.1 Before owner acceptance

In `/end-phase`, after:

- phase preconditions;
- the full gate;
- phase-level verification;
- any fixes those steps required;

but before the existing owner acceptance halt:

1. generate the phase impact overlay;
2. provide the compact architectural impact summary to the owner;
3. tell the owner how to open the Understand Anything dashboard;
4. continue into the existing acceptance halt.

This lets the owner evaluate both:

- the product's observed behavior; and
- the structural footprint of the implementation.

### 9.2 After whole-arc review fixes

Whole-arc review occurs after owner acceptance and may create fix commits.

If the phase branch changes after the acceptance-time visualization, regenerate the phase overlay before merge approval.

The merge hand-back should use the current visualization, not one based on the pre-review branch state.

If the structural footprint changed after acceptance, state that in the merge hand-back.

No new halt is introduced.

---

## 10. Graph mapping behavior

Given:

```text
changedFiles
```

load the Understand Anything graph and identify all nodes whose `filePath` matches a changed file.

Those nodes form:

```text
changedNodeIds
```

For every changed node, inspect graph edges where the node appears as either:

```text
edge.source
```

or:

```text
edge.target
```

Every directly connected node that is not itself changed forms:

```text
affectedNodeIds
```

The initial implementation should use **one-hop traversal only**.

Do not expand recursively in v1.

A large recursive neighborhood is likely to make the visualization less useful to the owner and increases the chance that the graph appears to claim more certainty than it has.

The owner or agent can use Understand Anything's deeper exploration tools when they want to follow a relationship farther.

---

## 11. Architectural layers

When the knowledge graph contains layer membership, report which layers contain directly changed nodes.

Optionally report a second set for affected-only nodes if the distinction remains readable.

Example:

```text
Changed layers:
- API
- Service
- Persistence

Affected-only layers:
- Audit
- Notifications
```

Layer classification is derived graph metadata and must be described as such.

---

## 12. Unmatched changed files

Every changed project file must end in one of two states:

```text
mapped to one or more graph nodes
```

or:

```text
unmatched
```

The tool must print the denominator:

```text
Changed project files: 8
Mapped changed files: 6
Unmatched changed files: 2
```

Then list the unmatched paths.

Do not allow:

```text
Changed components: 6
```

to stand alone when 2 changed files were never represented.

Unmatched files are an incompleteness warning, not an SDLC defect.

---

## 13. Graph freshness

Understand Anything graph metadata includes the commit used to build the graph where available.

Use that metadata to assess whether the graph predates project changes.

The freshness check must distinguish:

- repository commit movement that changed this project;
- unrelated commit movement in a monorepo;
- working-tree changes;
- generated Understand Anything data.

The implementation should follow the same principle as Understand Anything's own diff tooling:

> A hash mismatch alone is not enough to call a project graph stale. Determine whether project files actually changed.

The hand-back should report one of:

```text
graph basis current for the project before this slice
graph may be stale — <reason>
graph freshness unknown — <reason>
```

The feature should still produce best-effort mapped output when safe to do so.

---

## 14. Missing or unavailable Understand Anything

Expected non-use states include:

- no `.ua/knowledge-graph.json`;
- no legacy graph;
- graph cannot be parsed;
- graph schema is not recognizable;
- no changed files map to graph nodes.

These must be visible but non-blocking.

Example:

```text
Architecture impact view unavailable:
Understand Anything graph not found. SDLC close-out is unaffected.
```

or:

```text
Architecture impact view partial:
3 of 7 changed files are not represented in the graph.
```

An internal failure in the SDLC-owned adapter itself should be distinguishable from normal absence of the optional capability.

---

## 15. Output contract

The adapter should produce a short, stable textual result suitable for hand-back.

Suggested shape:

```text
SDLC IMPACT: COMPLETE
scope: slice
changed-files: 8
mapped-files: 8
changed-nodes: 12
affected-nodes: 19
changed-layers: API, Service, Persistence
unmatched-files: 0
graph-freshness: current-before-slice
overlay: .ua/diff-overlay.json
```

Partial example:

```text
SDLC IMPACT: PARTIAL
scope: slice
changed-files: 8
mapped-files: 6
changed-nodes: 9
affected-nodes: 14
changed-layers: Service, Persistence
unmatched-files: 2
graph-freshness: stale — 3 project files changed since graph commit
overlay: .ua/diff-overlay.json
```

Unavailable example:

```text
SDLC IMPACT: UNAVAILABLE
scope: slice
reason: Understand Anything knowledge graph not found
```

The exact syntax may change if implementation reveals a better format, but the result must be:

- compact;
- deterministic;
- easy for the agent to quote;
- explicit about incompleteness;
- not phrased as verification.

---

## 16. Dashboard behavior

The feature should generate the overlay automatically when possible.

It should **not automatically launch the dashboard**.

The hand-back may tell the owner how to open the installed Understand Anything dashboard using the platform-appropriate invocation.

Reasons not to auto-launch:

- CLI and desktop environments differ;
- browser launching is a side effect unrelated to correctness;
- the owner may not want to inspect every slice visually;
- generation is cheap enough to automate, viewing is a human choice.

If no known dashboard invocation is available for the active harness, say that the overlay was generated and leave opening it to the owner.

---

## 17. Relationship to review

The visualization and `diff-review` have different responsibilities.

### Visualization

Answers:

> What did the change structurally touch?

### Review

Answers:

> Is the change correct, appropriately scoped, and consistent with project standards?

The visualizer must not replace the existing explicit consumer review lens.

A one-hop graph can help an owner notice relationships but can miss:

- reflection;
- framework wiring;
- dynamic configuration;
- generated bindings;
- database relationships;
- runtime-only consumers;
- relationships absent from the graph index.

The current source-verification and denominator rules continue to govern review findings.

---

## 18. Relationship to CodeGraphContext or future providers

Do not design this feature around a universal code-intelligence abstraction yet.

The first implementation is an **Understand Anything integration** because it directly supplies the owner-facing dashboard and diff overlay needed for this trial.

If later field evidence shows value in multiple graph providers, the impact adapter can be generalized behind a provider interface.

Do not add that abstraction before a second provider exists.

---

## 19. Installation / adoption behavior

Prefer runtime discovery over a new setup questionnaire in v1.

The feature can discover Understand Anything by looking for:

```text
.ua/knowledge-graph.json
```

or the legacy graph location.

This avoids adding setup ceremony for an optional capability.

If later implementation proves that additional project-specific configuration is required, record only the minimum required project fact in the project-owned SDLC state.

Do not add tool-specific configuration to kit-owned generic commands when runtime discovery is sufficient.

---

## 20. Security and repository hygiene

The adapter must:

- read project source paths and Understand Anything graph data only;
- write only the Understand Anything diff overlay and transient `.git` state required for the slice base;
- never send code to an external service;
- never modify the knowledge graph itself;
- never commit transient slice state;
- respect the project's ignored files;
- avoid adding generated dashboard scratch data to commits accidentally.

If Understand Anything itself requires additional external/model access for graph generation, that remains outside this feature's deterministic overlay-generation path.

---

## 21. Failure behavior

Expected feature states:

### COMPLETE

- graph readable;
- changed file denominator established;
- every changed file either mapped or explicitly classified;
- overlay written;
- summary printed.

### PARTIAL

- graph readable;
- overlay usable;
- one or more changed files unmatched or graph known/potentially stale;
- incompleteness printed explicitly.

### UNAVAILABLE

- Understand Anything not installed/configured for this project;
- graph not present;
- feature skipped honestly.

### ERROR

- the kit-owned impact adapter itself failed in a way that should have been supported;
- output explains the failure.

`ERROR` should be recorded as kit friction during field trials.

None of these states changes gate truth.

---

## 22. Acceptance criteria

### Core adapter

- [ ] Resolves `.ua` versus legacy Understand Anything data directory correctly.
- [ ] Reads an existing Understand Anything knowledge graph without modifying it.
- [ ] Accepts a deterministic change boundary for slice and phase modes.
- [ ] Includes tracked, staged, unstaged, and untracked non-ignored changed project files in the denominator.
- [ ] Excludes generated Understand Anything artifacts from the change set.
- [ ] Maps changed files to all graph nodes carrying those file paths.
- [ ] Computes one-hop affected nodes through graph edges.
- [ ] Excludes directly changed nodes from the affected-only list.
- [ ] Reports changed architectural layers where graph metadata permits.
- [ ] Lists every unmatched changed file.
- [ ] Reports graph freshness or freshness uncertainty.
- [ ] Writes a valid Understand Anything `diff-overlay.json`.
- [ ] Produces a compact COMPLETE / PARTIAL / UNAVAILABLE / ERROR summary.

### Slice workflow

- [ ] `/next-slice` captures the slice base after branch preparation and before implementation.
- [ ] Slice-ready hand-back generates a preview impact overlay when available.
- [ ] Slice-ready hand-back preserves the existing stop before `/end-slice`.
- [ ] Absence of Understand Anything does not add a halt or block the slice.
- [ ] `/end-slice` regenerates the final impact after close-out fixes.
- [ ] `/end-slice` states whether the final structural footprint differs materially from the preview.
- [ ] Successful close-out clears transient slice-base state.

### Phase workflow

- [ ] `/end-phase` generates the phase impact after gate/phase verification and before owner acceptance.
- [ ] The phase base ref comes from project state or an explicit argument rather than assuming `main`.
- [ ] If whole-arc review changes the branch afterward, the impact overlay is regenerated before merge approval.
- [ ] The merge hand-back does not present a stale pre-review visualization as current.

### Owner semantics

- [ ] Hand-backs call the visualization an architecture/impact view, not verification.
- [ ] The owner is told when the view is partial or unavailable.
- [ ] The dashboard is not auto-launched.
- [ ] No new mandatory owner halt is added.
- [ ] Existing owner decision boundaries remain unchanged.

---

## 23. Negative cases that must be exercised

The feature is not complete until these cases have been observed:

1. **No Understand Anything graph**
   - normal SDLC continues;
   - hand-back says visualization unavailable.

2. **One new source file absent from the graph**
   - file appears in `unmatched-files`;
   - overlay may still contain mapped existing files;
   - result is PARTIAL, not COMPLETE.

3. **Graph commit is older, but only unrelated monorepo files changed**
   - graph is not called stale solely from commit hash mismatch.

4. **Graph is genuinely stale for project files**
   - result says so explicitly.

5. **Changed file has multiple function/class nodes**
   - all matching changed nodes are included.

6. **Changed node connects to the same affected node through multiple edges**
   - affected node is emitted once.

7. **A node is both directly changed and graph-connected to another changed node**
   - it remains in `changedNodeIds`, not duplicated in `affectedNodeIds`.

8. **Untracked new source file**
   - included in the changed-file denominator;
   - unmatched if absent from graph.

9. **Slice contains an intermediate commit**
   - captured slice base still produces the complete slice change set.

10. **Close-out review adds a file not present in the owner preview**
    - final slice impact reports the structural footprint changed.

11. **Whole-arc review adds a phase file after acceptance**
    - phase overlay is refreshed before merge approval.

12. **Understand Anything overlay directory exists but graph JSON is malformed**
    - clear PARTIAL/UNAVAILABLE/ERROR classification;
    - no false COMPLETE.

13. **Generated `.ua` files change**
    - they do not enter the project's changed-file denominator.

---

## 24. Field-trial hypothesis

This feature should ship initially as an optional, measured trial.

### Value hypothesis

> Showing the owner a deterministic visual map of directly changed and graph-connected components lets them understand and challenge AI-generated work with less line-level code inspection.

### What would count as value

Across real slices/phases, record:

- whether the owner opened the dashboard;
- whether the visualization caused the owner to ask a question they would not otherwise have asked;
- whether it revealed an unexpected subsystem/layer;
- whether the owner reports faster or clearer understanding of the change;
- whether the graph produced misleading relationships;
- how often changed files were unmatched;
- how often graph staleness reduced usefulness;
- generation latency;
- any process friction caused by the feature.

### Failure criterion

The feature should be reconsidered or simplified if, after enough real exposure to make a judgment:

- owners rarely inspect it;
- it produces no new useful questions;
- staleness makes the result routinely incomplete;
- the graph misleads more often than it informs;
- maintaining the adapter costs more than the supervision value it produces.

A trial that only proves the integration is safe is insufficient.

The trial must test whether it improves human understanding.

---

## 25. Preserve these invariants

Implementation must not weaken:

- one slice per fresh implementation session;
- the owner-controlled transition from slice-ready to `/end-slice`;
- existing five owner halt semantics;
- TDD ordering and evidence;
- full gate semantics;
- slice and whole-arc review;
- mutation checks;
- `change-verify`;
- source verification of review findings;
- the rule that a check which cannot run must not appear to have passed;
- the separation between kit-owned rules and project-owned facts;
- the rule against creating duplicate sources of truth.

---

## 26. Implementation posture

Prefer the smallest implementation that can test the value hypothesis.

Do not use this feature as a reason to:

- introduce a general workflow engine;
- create a universal graph-provider abstraction;
- add a new persisted project-state system;
- vendor Understand Anything;
- automatically regenerate its LLM knowledge graph;
- expand the correctness gate;
- add a sixth owner halt.

The implementation is successful when the owner receives a trustworthy **map of the change surface** at the moments they already supervise the work, while every correctness claim continues to come from the existing SDLC evidence chain.

