# Plan Phase

Turn a phase idea into a build-ready `spec/PHASE_NN_*.md` by **interrogating the owner**
and **adversarially attacking the requirements** until no material gaps remain. The spec
is written last, not first. Process reference: `spec/SDLC.md`.

Prime directive: **never fill a gap with an assumption.** Every gap, ambiguity, or
contradiction becomes a question to the owner. If the owner answers "you decide," record
your choice as a numbered decision marked *(proposed)* and get it approved with the final
spec — silence is never approval.

## How to use

`/plan-phase` — at a phase boundary, or when `/next-slice` finds nothing to slice.
Optional argument to skip candidate selection: `/plan-phase 12` or
`/plan-phase user accounts`.

This command is analysis-heavy; check the model policy recorded in `spec/SDLC.md`
(*Records*; `/model` to switch).

## Workflow

### 1. Orient

Read `spec/PROJECT_INDEX.md` (Notes + deferred backlog). Then, only
as needed: any roadmap file, any design doc named for the candidate, and the project's
scope/feature spec if one exists. Context-minimization rule applies.

### 2. Candidate selection — owner halt 1

Present the candidate phases (roadmap order, deferred backlog pressure, anything the
owner raised) with a recommendation and a one-line value statement each — plain-English
bullets per the hand-back standard (`spec/SDLC.md`, *Owner halt points*).
AskUserQuestion (on Claude Code; plain chat where the CLI lacks it).
Record the choice as OWNER-DECIDED with the date.

### 3. Requirements interview — grill in rounds

Interview the owner with AskUserQuestion in batches (≤4 questions per round). Prefer
concrete options with trade-offs over open-ended questions; use previews (mock output,
ASCII UI sketches, sample API payloads) when the difference is visual. Keep going until
a full round surfaces nothing new. Cover, minimum:

- **User-visible value** — what does the user actually see or do differently?
  Ask for a worked example: "walk me through one concrete use of this."
- **Scope edges** — for each borderline capability: in or out? Everything cut goes to
  Non-Goals by name, so it can't creep back silently.
- **Behavior specifics** — for each behavior: trigger, inputs, rule, output, and what
  the user sees. Vague verbs ("handles", "manages", "supports") are not answers — push
  for the rule.
- **Trust boundaries** — for anything an external or non-deterministic system touches
  (LLM, third-party API, user-supplied data): may it mutate authoritative state
  directly, propose-and-validate, or read-only? "The <external system> decides X" is a
  red flag to resolve, not record.
- **Failure & emptiness** — what happens when the dependency call fails, the list is
  empty, the target is missing, the action repeats, existing data predates the feature?
- **Tuning** — which numbers are adjustable parameters (name where they live) vs
  structural rules? For every number that ends up in a decision, ask where it came
  from: a run, a count, or a query (**measured** — record which) or a guess, an
  analogy, or a round figure that felt right (**estimated**). Ask for the measurement
  when it is cheap to take now; a cap, a limit, a batch size, or a budget approved
  without one is approved against nothing.

### 4. Adversarial gap analysis — attack the requirements

After the interview, actively try to break the requirements. The sweeps are this
command's heaviest context load, and they are read-only — run each applicable sweep as
its own **parallel read-only subagent** (give it the phase idea, the interview's
answers, and the relevant spec pointers) — the CLI's own read-only agent type where it
has one, otherwise the `explore` profile `/sdlc-setup` installed. Where the CLI cannot
fan out, run the sweeps one after another; dropping a sweep for time is a gap in the
analysis, not a saving, and is reported as one.
Sweep agents analyze, so they inherit the session model. Findings come
back to **this** session: each becomes a new interview question (back to
step 3) or a recorded decision, and every question goes to the owner from here — no
subagent ever interacts with the owner.

- **Walkthrough** — write a short end-to-end usage script exercising the feature.
  Every moment the script forces you to invent something unspecified is a gap.
- **Trust-boundary sweep** — scan for any behavior where an external system, model, or
  untrusted input mutates authoritative state. The application disposes; violations get
  redesigned as proposal + validator or an application-owned rule.
- **Preserved-contract sweep** — read `spec/PRODUCT_CONTRACT.md` whole (it is bounded
  by design; if it is absent, the project predates it — say so, and the phase-close
  reconcile owns the backfill offer). List the entries on surfaces this phase
  touches and carry them into the spec's *Preserved Behaviors* section verbatim,
  pins included; slices then inherit them from the phase spec, which is what keeps
  the contract out of the per-slice read. **An entry the phase would remove or alter
  is an owner question** — at this halt or halt 3, never a decision the plan makes:
  a rewrite that drops a ratified behavior is indistinguishable from an
  implementation simplification unless someone is made to say which it is, and one
  passed silently exactly that way on a real adoption. When a touched surface
  **consumes** data the contract's *Trust boundaries* section classifies untrusted,
  re-read those invariants and carry the applicable ones the same way — the
  producer's boundary rules were ratified in a phase spec no later phase reads, and
  a consumer-side rewrite can expose stored hostile data without touching any
  ingestion point.
- **Consequence sweep** — scan the behaviors for changes to authentication or
  authorization, money or financial calculation, destructive or irreversible data
  operations (migration, deletion, retention), credential handling, or regulated data.
  Each hit names its extra verification in the spec — in the slice's exit criteria or
  the acceptance-review checklist — and appears in Risks & Deferred. A hit absorbed
  silently is the finding; consequence and size are different axes, and smallness is
  no exemption. Two questions every hit must answer:
  - **Is it actually inert?** Any claim that a consequence is neutralized by
    configuration — a flag, an environment variable, "ships dormant", "off in prod",
    "merging changes nothing" — must name the variable **and quote its value from the
    artifact that configures production**: the deployment manifest, the platform's
    environment settings, the compose or workflow file. Never from the test
    environment, which is usually configured to make exactly this claim true, and
    never from the code that reads the variable. A dormancy claim that cannot be
    quoted from a production artifact is an open question, not a decision.
  - **What is the independent off switch?** Each hit names the lever that disables it
    alone. A control whose only lever also disables something unrelated — the identity
    layer, the whole feature set, the service — has no rollback, and that is a finding
    now rather than during the incident it causes.
- **Cross-system sweep** — list every existing subsystem the feature reads or writes.
  Each touched system needs a stated interaction rule (or an explicit "unaffected").
- **Persistence & compatibility sweep** — new/changed models → migration plan, seed/
  fixture data, and the live-data question: what happens to existing saves/databases/
  configs created before this feature? Preserve-and-extend; never break existing data.
- **Testability sweep** — every behavior must be pinnable by a deterministic test, or
  explicitly assigned to the acceptance-review checklist. "Feels right" is not an exit
  criterion. Each slice's exit criteria name **what observes them and when** — a local
  command, the gate, CI on the main branch, or the owner. A criterion naming an
  observer that does not run at that point is a planning defect, not a slice problem;
  the kit's own former ratchet phrasing is the recorded exposure — "raise the
  coverage floor from CI's printed number" is unsatisfiable on an arc branch whenever
  CI runs only on the main branch, and unsatisfiable everywhere on a stack whose
  check prints no figure (the phrasing now names the enforced run's report artifact
  as the fallback source) — and a real arc wrote that criterion twice in one planning
  session against a convention its own previous arc had recorded. Separately: if **every**
  slice comes out behavior-neutral by construction (nothing runs until an activation
  moment), flag it in the spec now — `/end-phase` will owe a local real-data pass of
  the composed system before the PR, and an acceptance checklist written entirely for
  the activation moment is the tell.
- **Contradiction sweep** — check the answers against each other, against product
  direction, and against locked decisions in prior specs. Surface conflicts; never
  quietly pick a side.
- **Minimal-version attack** — what is the smallest version that still delivers the
  value? Anything above that line must be justified or moved to a later phase.

Verify feasibility claims against the codebase (does the seam we're assuming exist?)
before locking decisions that depend on them — quote what is actually there, with its
path, rather than judging from memory of the code.

### 5. Draft the spec

Only when Open Questions is empty (or contains only *(proposed)* decisions awaiting the
step-6 approval), write `spec/PHASE_NN_<SLUG>.md`:

```
# Phase NN — Title
## Goal                 (user-visible value, 2–3 sentences)
## Owner Decisions      (D1… numbered, dated; (proposed) items flagged; any decision
                         carrying a number tagged measured — with the run, count, or
                         query behind it — or estimated)
## Behaviors            (B1… — trigger, rule, output, what the user sees)
## Non-Goals            (everything cut, by name)
## Trust Boundaries     (what external systems may propose/read; what only the app does
                         — omit if no external systems are touched)
## Preserved Behaviors  (product-contract entries on surfaces this phase touches,
                         carried verbatim with their pins — the preserved-contract
                         sweep fills it; omit if none)
## Data & Migration     (models, migration id, seed/fixtures, existing-data impact)
## User-Visible Surface (screens/endpoints/CLI touched + acceptance-review checklist
                         for /end-phase)
## Slices               (S1… in dependency order — scope, exit criteria, test approach)
## Risks & Deferred     (known risks, explicitly deferred items)
```

Slices must each be one-session-sized, with exit criteria a named observer can verify
at the point they are claimed — a test, the gate, CI on the main branch, or the
acceptance checklist (step 4's testability sweep is the check). Behaviors map onto
slices — no behavior left unassigned.

**Keep the spec lean enough to be read whole at every slice.** Decisions, behaviors,
slices, and checklists are the spec; interview transcripts, survey output, and other
bulk research go to an appendix file the spec links
(`spec/PHASE_NN_<SLUG>_NOTES.md`), loaded only when a slice needs it — add it a
spec-loading row in `CLAUDE.md` with that trigger. `/next-slice` reads the phase spec
at every slice: a real adoption's 173 KB phase spec taxed every session of its arc
with detail no single slice used.

### 6. Approval — owner halt

Present the spec per the hand-back standard (`spec/SDLC.md`, *Owner halt points*):
open with a plain-English executive summary in bullets — what the phase delivers, the
slice count, the top 3 risks — then everything the owner is being asked to ratify,
**numbered and explicitly marked** (`Decision 1: …`): each *(proposed)* decision, and
each number tagged **estimated** (the owner is ratifying those against no measurement,
and `/next-slice` re-derives each one before the slice that implements it). The full
decision list and slice breakdown follow as detail — the owner approves from the
summary; the spec file is where the detail lives. On approval: create
`feat/phase-NN-<slug>` off the up-to-date main branch,
flip `spec/PROJECT_INDEX.md` to BUILD with the spec pointer and OWNER-DECIDED note,
commit the spec + index (docs commit), and hand off: **`/clear`, then `/next-slice`.**

## Notes

- Rounds of ≤4 questions beat one giant questionnaire — later questions should depend
  on earlier answers.
- If interrogation stalls ("I don't know yet"), park the behavior in Risks & Deferred
  and shrink the phase rather than spec on guesses.
- A phase plan that survives step 4 unchanged is a smell — attack harder.
