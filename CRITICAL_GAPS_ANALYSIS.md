# Critical Gap Analysis — Five Priorities Before Broader Expansion

**Repository reviewed:** `ghostpencil/sdlc-kit`  
**Kit version at review:** 0.7.0  
**Purpose:** Analytical input for evaluating the next evolution of the kit. This document describes the gaps, why they matter, and the properties an eventual remedy would need to preserve. It deliberately does **not** prescribe an implementation.

The kit is already unusually strong at controlling agent scope, preserving context across sessions, enforcing TDD habits, challenging requirements, and converting field failures into durable process improvements. The five gaps below are not evidence that the core model is weak. They are the boundaries that become visible because the core model is now mature enough to expose them.

They should be addressed before expanding toward team-scale development or additional agent platforms. Otherwise, broader adoption would multiply the cost of changing the underlying process later.

---

## Executive summary

| # | Gap | Current strength that exposes it | Principal risk |
|---|---|---|---|
| 1 | The workflow state machine is interpreted rather than mechanically enforced | Commands, invariants, halt points, gates, and evidence rules are exceptionally explicit | The agent can still skip, misread, or inaccurately record a required transition while producing a plausible account of compliance |
| 2 | One arc, one branch, one PR delays integration | Whole-arc review has repeatedly found defects invisible to slice reviews | Integration feedback, mergeability, rollback granularity, and delivery cadence degrade as arcs grow |
| 3 | The process is not risk-adaptive | The standard workflow is rigorous and coherent | Low-risk work may carry unnecessary ceremony while high-risk work receives no materially stronger assurance model |
| 4 | Security is treated as a design concern, not a complete secure-development lifecycle | Trust boundaries, isolation, test doubles, release checks, and provenance awareness are already present | Functionally correct software may still ship with dependency, secret, supply-chain, privacy, or threat-model failures |
| 5 | The modeled lifecycle largely ends at merge | `/end-phase` correctly recognizes that merging is not shipping | Production deployment, verification, rollback, observability, and incident learning remain outside the evidence chain |

A common theme runs through all five:

> The kit is strongest when it converts a written claim into something that can be observed failing. Its next maturity step is to apply that principle to the lifecycle itself.

---

# 1. The workflow state machine is interpreted rather than mechanically enforced

## Current strength

The kit defines its development state with unusual clarity:

- phases, slices, and TDD cycles;
- five owner halt points;
- one arc branch and one final PR;
- mandatory gate, review, mutation check, commit, and bookkeeping steps;
- `spec/PROJECT_INDEX.md` as the durable orientation point;
- a canonical SDLC document that wins over commands;
- explicit kit invariants and negative cases;
- release-time manifest and bundle verification.

The command files are more precise than most executable workflows. They state not only what should happen, but also why a tempting alternative is unsafe. The field reports show that this precision has repeatedly prevented or exposed real defects.

## The gap

The process is nevertheless executed primarily by a language model interpreting Markdown.

The model decides whether:

- the current state was read correctly;
- a halt is required;
- the owner has already decided a question;
- all phase behaviors map to slices;
- the correct arc branch is active;
- the gate result satisfies the recorded baseline;
- a review substitution was disclosed;
- every applicable mutation check was actually performed;
- deferred findings were recorded with correct provenance and cause markers;
- the next state written to `PROJECT_INDEX.md` accurately reflects repository reality.

The repository contains deterministic checks around portions of this process, but not a deterministic authority over the process transitions themselves. The human-readable index is both a valuable orientation artifact and an agent-authored claim about state.

This creates a distinction between two kinds of enforcement:

1. **Local technical enforcement** — lint, type checking, tests, hook behavior, manifest integrity, file counts.
2. **Lifecycle enforcement** — whether the work was allowed to move from one SDLC state to another.

The first category is increasingly strong. The second still depends on compliant interpretation.

## Why it matters

The kit’s own field evidence repeatedly demonstrates the danger of a plausible claim that is not reconciled against the enforcing artifact:

- a coverage floor was recorded as raised while CI still enforced the old value;
- a mock policy existed while tests reached a live Google API;
- a command asserted a green baseline while the project’s canonical SDLC recorded a red one;
- update classifiers produced confident but incorrect classifications until their denominator and negative cases were tested.

A lifecycle transition can fail in the same way. An agent can report:

- “all slices complete” while one behavior has no evidence;
- “mutation checks passed” without a durable record of which guards were mutated;
- “safe to clear” while bookkeeping is incomplete;
- “ready to merge” while the acceptance decision or CI status is ambiguous;
- “next slice S4” while repository history or the phase spec implies another state.

Because the report can be coherent and detailed, the failure may look more trustworthy than a simple script error.

This risk increases as the kit grows. More profiles, security checks, deployment states, or team roles would add more transitions for the model to remember and reconcile. Without a firmer state boundary, every new capability expands the semantic surface that must remain mutually consistent across command prose and project-authored records.

## Important tension

Not everything should become deterministic.

The kit depends on model judgment for legitimate analytical work:

- identifying ambiguity;
- deciding whether a question is owner-facing;
- adversarially examining requirements;
- evaluating consumer behavior;
- assessing whether a test double matches reality;
- interpreting retrospective evidence.

Mechanizing these judgments would either be impossible or would reduce the kit to shallow checklist compliance.

The real boundary is therefore not “replace Markdown with code.” It is the distinction between:

- **judgment about the work**, which belongs to the agent and owner; and
- **proof that required lifecycle transitions and evidence exist**, which can potentially be validated more mechanically.

## Failure modes exposed by the gap

- A required halt is skipped because the model treats a decision as already resolved.
- A command advances despite a missing or stale artifact.
- Two files describe different current states.
- Evidence is summarized in prose but cannot be reconstructed later.
- A review or mutation check is claimed without a durable denominator.
- A resumed session enters through an invalid state because `START HERE` was written incorrectly.
- Future command changes introduce transitions that older project-owned files cannot represent.

## Questions an eventual remedy must resolve

These are design questions, not proposed answers:

- What is the minimum lifecycle state that must be machine-readable?
- Which transitions are important enough to reject when their evidence is absent?
- Does `PROJECT_INDEX.md` remain canonical, become a rendered view of another state artifact, or coexist with one under a strict reconciliation rule?
- What evidence must be durable versus merely reported at hand-back?
- How are qualitative findings represented without pretending they are deterministic facts?
- How does an adopted project upgrade its state representation without losing history?
- How is manual owner intervention recorded when GitHub approval or another external event supplies the halt decision?
- How does the system avoid creating a second source of truth—the exact class of problem the kit has repeatedly learned to eliminate?

## Conceptual closure condition

This gap would be substantially closed when a lifecycle transition cannot be represented as complete unless the required predecessor state and evidence are present, while analytical decisions remain human- and agent-readable rather than reduced to a rigid workflow DSL.

The decisive property is not the existence of a CLI or schema. It is that the kit can distinguish:

> “The agent says this step happened” from “the repository contains reconstructable evidence that allows this state transition.”

---

# 2. One arc, one branch, one PR delays integration

## Current strength

The rule is deliberate:

> One arc, one branch, one PR.

Slices remain small and independently reviewed, but accumulate on a single branch until `/end-phase`. The final PR then receives a whole-arc review that examines interactions no individual slice review can see.

The field reports strongly validate the whole-arc review. Across three recorded arcs, it found defects missed by all slice reviews. These were not style concerns; they included data-integrity and mutation-confirmed test gaps located in seams between layers and slices.

The final review is therefore load-bearing. Any change that merely replaces the arc PR with independent slice PRs risks removing one of the kit’s best-supported practices.

## The gap

A small implementation slice is not necessarily a small integration batch.

Even though work is decomposed into narrow slices, the code remains outside the main integration line until the entire arc closes. As an arc grows, this can produce:

- delayed detection of conflicts with main;
- delayed CI feedback against the current integration state;
- a final PR containing many commits and behaviors;
- a larger rollback unit;
- increased branch drift;
- later discovery of environment or deployment interactions;
- reduced ability to release completed safe behavior independently;
- pressure to shorten or skip final review because the PR is large.

The process optimizes implementation cognition and final seam review, but not necessarily integration frequency.

## Why it matters

The difference between **slice size** and **integration batch size** can remain invisible on a solo project with short arcs. It becomes significant when:

- a phase grows beyond the expected number of slices;
- main changes during the arc;
- a dependency update lands elsewhere;
- an urgent fix must be made while the arc is open;
- one completed behavior would be valuable to ship before the rest;
- a defect appears after merge and the arc contains several unrelated changes;
- the final PR becomes too large for a reviewer to reason about effectively.

Large delayed integration also changes the meaning of the gate. A slice can be green on the arc branch while the arc as a whole moves farther from the current main branch. The final whole-arc gate and review catch this eventually, but the cost of correction rises with the age and width of the branch.

## Important tension

The whole-arc review should not be treated as duplicate review or optional ceremony. The evidence says the opposite.

The design problem is therefore not simply “merge slices sooner.” It is:

> How can the project receive continuous integration feedback and smaller delivery units without losing a final review over the complete behavioral arc?

Several concepts are related but not identical:

- the unit of planning;
- the unit of implementation context;
- the unit of commit;
- the unit of code review;
- the unit of integration;
- the unit of release;
- the unit of rollback;
- the range inspected by the final seam review.

The current kit aligns most of those units at the arc boundary. A future model may separate them, but each separation creates new state and evidence requirements.

## Failure modes exposed by the gap

- A long-running arc becomes difficult to merge despite every slice being locally green.
- A large final PR receives shallower human or agent review because of review fatigue.
- A defect requires reverting the entire arc rather than one independently safe change.
- A completed slice remains unshipped behind unrelated unfinished behavior.
- Main changes invalidate assumptions made several slices earlier.
- A hotfix creates a competing branch and makes the current “one unmerged arc branch” rule ambiguous.
- More frequent integration accidentally removes the only review that sees cross-slice seams.

## Questions an eventual remedy must resolve

- Is the arc the unit of product intent, integration, release, or only final acceptance?
- Can a complete slice exist on main without exposing incomplete behavior to users?
- If intermediate PRs exist, what commit range or artifact defines the final whole-arc review?
- How is an arc reconstructed after some slices have already merged?
- What prevents a sequence of individually correct slice merges from producing an incoherent feature?
- How do feature flags, dormant wiring, or compatibility layers affect acceptance and test obligations?
- What is the recovery path when an arc must pause while an unrelated urgent change lands?
- Does continuous integration mean merging code, opening an always-current draft PR, or simply running the arc branch against the latest main after every slice?

## Conceptual closure condition

This gap would be substantially closed when the kit can obtain early integration feedback and reduce final batch risk while preserving a review that evaluates the complete arc and the seams between slices.

A remedy that improves merge frequency but loses whole-arc reasoning would be a regression. A remedy that preserves the final review but still permits branch drift and oversized rollback units would only partially address the gap.

---

# 3. The process is not risk-adaptive

## Current strength

The standard workflow is coherent and high assurance:

- requirements interrogation;
- adversarial planning;
- TDD;
- gate enforcement;
- slice review;
- mutation checks;
- owner acceptance;
- whole-arc review;
- merge approval;
- retrospective learning.

This is a strong default for meaningful feature and stabilization work. The process also avoids arbitrary exceptions: a red baseline is recorded honestly, design questions halt, and deferred work remains visible.

## The gap

The assurance model changes little based on the risk profile of the change.

A low-impact internal cleanup, a routine feature, an authentication change, a destructive migration, and a production hotfix all pass through substantially the same conceptual lifecycle. The phase spec can add verification, and `/end-phase` may suggest a deeper review for a large or high-risk phase, but risk does not currently drive a distinct set of mandatory controls.

This creates risk in both directions:

- **Over-processing:** trivial or reversible work may pay the full cost of a feature arc.
- **Under-processing:** high-consequence changes may receive the same controls as ordinary application behavior.

## Why it matters

Size and risk are not the same.

A change can be small in lines of code but high in consequence:

- changing an authorization condition;
- modifying a payment or financial calculation;
- changing data-retention behavior;
- altering migration rollback behavior;
- introducing a new external service or dependency;
- changing credential handling;
- modifying audit or compliance records;
- changing a destructive command default.

Conversely, a large generated UI or refactor may be highly reversible and isolated.

Without an explicit risk model, the agent or owner must improvise what “high risk” means at planning time. That makes stronger controls dependent on memory—the class of process weakness the kit generally works to eliminate.

Uniform ceremony also threatens adoption. If every tiny corrective change requires the full phase lifecycle, users may begin bypassing the process. Once bypass becomes normal for “small” work, the boundary between sensible exception and ungoverned change erodes.

## Important tension

Risk adaptation can easily become either bureaucratic or cosmetic.

A profile named “high assurance” has no value unless it changes actual evidence, approval, verification, or release requirements. A “quick” path is unsafe if it merely removes steps without defining the narrow conditions under which those steps add little value.

The classification itself can also become a weak point:

- If the agent assigns the profile, it may minimize risk to reduce work.
- If the owner always assigns it, risk recognition depends entirely on owner expertise.
- If a checklist assigns it mechanically, the checklist may miss contextual consequences.

The kit’s existing owner-control philosophy suggests that risk classification would need both analytical input and explicit accountability, but the exact boundary remains open.

## Failure modes exposed by the gap

- High-impact changes receive no threat model, rollback proof, or stronger approval.
- Low-risk changes accumulate outside the process because the default feels too heavy.
- “Large” is used as a proxy for “risky,” missing small high-consequence changes.
- Emergency fixes either violate the process or move too slowly for the incident.
- A change begins as ordinary work but becomes high-risk mid-slice with no defined escalation path.
- A high-assurance label adds prose but no extra machine-enforced evidence.
- Different adopters interpret risk levels inconsistently, making field evidence difficult to compare.

## Questions an eventual remedy must resolve

- Which dimensions define risk: reversibility, blast radius, data authority, privacy, money, authentication, availability, migration complexity, external systems, or regulatory consequence?
- Is risk declared at phase planning, slice start, or both?
- Can risk escalate during implementation, and what happens to work already completed under a lower profile?
- Which controls vary by profile: planning depth, reviewers, mutation scope, security checks, deployment method, rollback evidence, acceptance surface, or owner halts?
- What is the minimum safe path for a production emergency?
- How does a quick path prove that it is genuinely low risk rather than merely small?
- How are project-specific risk rules recorded without embedding project facts into kit-owned commands?
- What evidence would show that profiles reduce cost or defects rather than only adding categories?

## Conceptual closure condition

This gap would be substantially closed when the rigor of the workflow is proportional to the consequence and reversibility of the change, with explicit evidence showing why a lighter or stronger path applied.

The closure criterion is not the number of profiles. It is whether the process can answer:

> “Why was this amount of assurance appropriate for this change?”

without relying on hindsight or an unrecorded judgment.

---

# 4. Security is a design concern, not yet a complete secure-development lifecycle

## Current strength

The kit already contains meaningful security-related thinking:

- explicit trust-boundary analysis during planning;
- suspicion of external or nondeterministic systems mutating authoritative state;
- enforced test isolation;
- outbound network blocking;
- credential sterilization;
- test-double fidelity rules;
- failure-path testing;
- release manifests and checksums;
- third-party notices and provenance checks for vendored skills;
- concern for data compatibility and authoritative stores.

These are stronger controls than many development frameworks provide by default. The field reports also demonstrate that they arose from real near misses, including tests reaching a live organizational service.

## The gap

The security controls do not yet form a complete secure-development lifecycle.

The kit does not systematically define when or how a project should address areas such as:

- security requirements;
- threat modeling;
- authentication and authorization review;
- secret detection;
- dependency and vulnerability scanning;
- static or dynamic security analysis;
- software bills of materials;
- build provenance and artifact signing;
- license policy;
- privacy and data classification;
- vulnerability intake and remediation;
- security incident handling;
- separation of duties for high-consequence changes;
- production security verification.

Trust boundaries are necessary, but they do not cover the full security problem. Test isolation protects the test environment, but not necessarily the deployed system or dependency chain. Bundle checksums protect the kit archive from accidental drift, but do not by themselves establish trusted build provenance for adopting projects.

## Why it matters

Functional correctness and security correctness overlap, but they are not equivalent.

A change can satisfy all specified behavior and pass strong tests while still:

- exposing data to an unauthorized caller;
- introducing a vulnerable dependency;
- logging secrets or personal information;
- trusting an unsafe deserialization path;
- weakening transport or storage protections;
- creating a supply-chain exposure;
- violating retention or consent requirements;
- producing an unsigned or unverifiable release artifact;
- leaving a known vulnerability without an ownership or response path.

AI-assisted development increases some of these risks because an agent can introduce dependencies, configuration, generated workflows, or security-sensitive defaults as incidental implementation choices. A strong behavioral spec may not mention them because they are not user-visible behavior.

This gap also limits the meaning of “enterprise-ready.” Enterprise adoption typically requires evidence that secure-development practices exist across governance, design, implementation, verification, release, and vulnerability response—not only that the code was tested carefully.

## Important tension

Security requirements can overwhelm small projects if every possible control becomes mandatory.

The kit’s strength is that it remains understandable and usable. Turning the standard workflow into a compliance encyclopedia would damage that strength and encourage bypass.

The likely conceptual boundary is between:

- a minimal security baseline that applies broadly;
- risk-triggered controls for sensitive changes;
- project-specific tooling and regulatory obligations;
- external standards used as coverage maps rather than copied wholesale into every phase.

The security model must also respect the kit’s project-fact boundary. The kit can define categories and evidence expectations, but scanners, identity models, data classifications, deployment platforms, and regulatory obligations are project-specific.

## Failure modes exposed by the gap

- A high-risk phase passes the ordinary gate without any security analysis.
- Security remains a prose reminder with no failing check or evidence artifact.
- Dependency scanning is added locally but omitted from CI.
- A project claims supply-chain integrity based only on source checksums.
- Secrets are absent from source but exposed in logs, fixtures, generated artifacts, or CI output.
- A vulnerability is detected but has no lifecycle state, owner, severity rule, or remediation clock.
- The security profile becomes so broad that adopters disable it.
- A standards mapping creates documentation confidence without actual control coverage.

## Questions an eventual remedy must resolve

- What security baseline should apply to every adopting project?
- Which risk factors activate stronger security requirements?
- Which security evidence belongs in the phase spec, project index, CI, release artifacts, or a separate project-owned security document?
- How are controls proven by negative cases where feasible?
- How are accepted risks recorded and revisited?
- What constitutes a blocking security finding versus a deferred one?
- How are dependency and build provenance handled without binding the kit to one ecosystem?
- How does the kit distinguish application security, supply-chain security, privacy, and operational security?
- What part of vulnerability response belongs after merge, and how does it reconnect to stabilization work?
- How can established frameworks such as NIST SSDF, OWASP SAMM, and SLSA serve as coverage references without turning the kit into a certification claim?

## Conceptual closure condition

This gap would be substantially closed when security requirements and evidence become part of the same traceable lifecycle as functional behavior, scaled to the project’s risk, rather than remaining an optional design concern or a collection of unrelated tools.

The decisive property is that a project can explain:

> what security risks were considered, which controls applied, what evidence passed, what risk remains, and who accepted it.

---

# 5. The modeled lifecycle largely ends at merge

## Current strength

The kit explicitly learned that merging is not shipping.

`/end-phase` asks whether deployment is required and whether it happened. It also requires owner acceptance before merge, checks CI, surfaces deferred work, reconciles the coverage floor, updates project history, and offers a retrospective while evidence is fresh.

That is a meaningful improvement over development processes that treat an approved PR as delivered value.

## The gap

Deployment is currently represented primarily as a required question and a project-specific note, not as a fully modeled lifecycle state with evidence.

The kit does not yet provide a general structure for:

- deployment readiness;
- environment promotion;
- deployment execution evidence;
- post-deployment smoke or acceptance checks;
- production health verification;
- feature enablement;
- rollback criteria and proof;
- canary or phased release;
- monitoring and observability changes;
- incident response;
- runtime feedback returning to the backlog;
- delivery-performance measurement.

For projects that do not deploy—libraries, local tools, or some internal scripts—this may be appropriate. For production services and applications, however, the lifecycle’s strongest evidence chain stops before the environment where the software creates real value and real risk.

## Why it matters

A green repository does not prove a successful production change.

Many failures arise only from:

- environment configuration;
- production permissions;
- real data shape or volume;
- migration order;
- service dependencies;
- deployment packaging;
- infrastructure differences;
- feature-flag state;
- concurrency or load;
- monitoring blind spots;
- rollback behavior.

The current acceptance review occurs before merge and may exercise a local or test environment. That is valuable but cannot establish that the deployed artifact is the reviewed artifact or that production behaves the same way.

A merge can therefore be fully compliant with the development process while users receive nothing, receive the wrong artifact, or receive a change that immediately requires rollback.

This also limits evaluation of the kit itself. Test counts, coverage, review findings, and baseline movement show engineering improvement, but they do not reveal:

- how long changes take to reach users;
- how often deployments fail;
- how quickly failures recover;
- how much rework follows release;
- whether the process improves operational stability.

Without production feedback, the retrospective sees only repository evidence and owner memory about runtime outcomes.

## Important tension

The kit should not become a deployment platform.

Adopting projects may use GitHub Actions, Azure DevOps, manual desktop packaging, cloud-native deployment systems, app stores, container platforms, or no deployment at all. A language- and platform-agnostic kit cannot prescribe one mechanism.

The relevant gap is not missing deployment automation code. It is missing lifecycle semantics around delivery:

- when a phase is considered merged versus delivered;
- what project-specific evidence proves delivery;
- what verification is required afterward;
- what happens when verification fails;
- how runtime findings return to stabilization.

The model must also avoid blocking library or local-tool projects on meaningless production steps.

## Failure modes exposed by the gap

- A merged fix remains undeployed while the project index implies completion.
- The deployed artifact differs from the commit that passed review.
- A migration succeeds in CI but fails or partially applies in production.
- Post-deployment verification is informal and leaves no evidence.
- A rollback occurs but the project’s current state still reads as successfully delivered.
- Monitoring is insufficient to detect that a release failed semantically.
- Runtime incidents do not feed the same measured/suspected backlog discipline.
- Delivery metrics are guessed from memory rather than measured from repository and deployment evidence.

## Questions an eventual remedy must resolve

- Where does the kit’s definition of “done” end for deployable projects?
- Which lifecycle states distinguish merged, deploy-pending, deployed, verified, failed, and rolled back?
- What is the minimum project-specific deployment contract the kit needs to record?
- What evidence proves that the deployed artifact corresponds to the reviewed commit?
- Which post-deployment checks are required, and which remain project-specific?
- How are manual deployments represented honestly?
- How does a failed deployment re-enter the slice or stabilization lifecycle?
- How are rollback requirements scaled by risk?
- What observability changes belong in the phase itself?
- Which delivery metrics are useful without encouraging Goodhart-style threshold gaming?
- How does the lifecycle remain valid for libraries and tools with no production environment?

## Conceptual closure condition

This gap would be substantially closed when a deployable project cannot silently equate merge with delivered value, and when deployment outcome and post-deployment verification become reconstructable parts of the project history.

The kit does not need to own the deployment mechanism. It needs to own the truth about the lifecycle state:

> merged, delivered, verified, failed, or rolled back.

---

# Cross-cutting observations

## 1. Gap 1 is foundational to gaps 3–5

Risk profiles, security controls, and delivery states all add conditional transitions and required evidence. If those are introduced only as additional prose, the kit’s semantic burden will grow faster than its enforceability.

This does not mean the state-machine question must be solved completely before any other exploration. It means proposed remedies for risk, security, and deployment should be evaluated for whether they create new unenforced claims.

## 2. Gap 2 is a flow problem, not simply a branching preference

The current branch model protects whole-arc reasoning. Its weakness is delayed integration, not the existence of an arc. Any analysis that frames the choice as “arc PR versus slice PR” is probably too narrow.

The deeper question is which lifecycle units should remain aligned and which can safely separate.

## 3. The kit should preserve its strongest proven properties

A remedy to any gap should be treated skeptically if it weakens:

- the five meaningful owner halt points;
- fresh context per slice;
- adversarial requirement analysis;
- honest brownfield baselines;
- vertical TDD;
- negative-case proof of checks;
- mutation confirmation;
- consumer and test-double review lenses;
- whole-arc seam review;
- measured/suspected backlog causes;
- evidence-based retrospectives;
- the separation between kit-owned and project-owned files.

These are not stylistic preferences. Several have direct field evidence behind them.

## 4. A second source of truth is a recurring hazard

Many possible remedies naturally introduce structured state, evidence files, security reports, deployment records, and risk declarations. The kit’s history already shows how dangerous it is when a value lives in prose and an enforcing artifact without reconciliation.

Any new artifact should have a clear answer to:

- Is it authoritative, derived, or evidentiary?
- Who writes it?
- Who validates it?
- What other artifact must agree with it?
- What happens when they disagree?

## 5. The remedy should be judged through field evidence

The repository’s strongest improvements came from real adoption findings rather than speculative framework design. The same standard should apply here.

A proposed change is more credible when a trial can reveal:

- what defect or friction it detects;
- what false positive it creates;
- what ceremony it adds;
- whether its negative case is visible;
- whether an adopter can reconstruct what happened later;
- whether the feature is still useful when the agent behaves imperfectly.

---

# Overall conclusion

The five gaps do not undermine the kit’s current value. They define the transition from a highly disciplined agent-assisted coding process into a fuller agentic SDLC.

The kit already has the right philosophical foundation for addressing them:

- claims should be measured;
- rules should fail loudly;
- evidence should survive context loss;
- ambiguity belongs with the owner;
- defects in the process should become invariants or improved workflow;
- project facts and kit rules should not be mixed.

The challenge is to extend that philosophy without overbuilding the framework or replacing useful judgment with shallow mechanization.

The central design question across all five areas is:

> Which parts of the lifecycle require human or agent judgment, and which claims about lifecycle state should no longer be trusted unless the repository can prove them?
