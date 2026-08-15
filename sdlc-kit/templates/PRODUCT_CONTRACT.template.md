# Product Contract

The current-truth statement of this product's owner-ratified, externally observable
behavior. `spec/SDLC.md` (*Product contract*) states the rules; the short form:

- **One line per behavior, grouped by user-facing surface.** Each line names the
  decision that ratified it (`P01 D23` — phase spec 01, decision 23) and its
  enforcement: `pinned: <test or mechanical check>` or `claim-only (<date>)`.
- **Current truths only.** Phase specs are the decision record and stay historical; this
  file states what the product does now. A superseding decision replaces a line; a
  ratified retirement deletes it. A behavior never leaves this file by omission.
- **Written at phase close** by `/end-phase`'s contract reconcile, and by owner decision
  anywhere else. **Read at phase boundaries only** — `/plan-phase` carries the relevant
  entries into the phase spec's *Preserved Behaviors*, so slices never load this file.
- **Contract altitude.** An entry is a truth a user could observe or an invariant the
  owner ratified — never a restating of a spec sentence-by-sentence.

<!-- Entry grammar (one line, wrapped as needed):
       - <externally observable truth> (P<NN> D<M>) — pinned: <test> | claim-only (<date>)
     Surfaces become `## <Surface>` sections as entries arrive (Dashboard, Refresh,
     Persistence, CLI, …). Example, delete when the first real entry lands:
       - Dashboard lists newest items first, paginated (P01 D4) — pinned:
         DashboardControllerTest#rendersNewestFirst
-->

- (no entries yet — they arrive at each phase close via `/end-phase`'s contract
  reconcile; on a project adopted mid-flight, the one-time owner-confirmed backfill is
  offered at the first phase close after adoption)

## Trust boundaries

<!-- High-consequence invariants, same grammar: which inputs are untrusted, what
     neutralizes them where they are rendered or interpreted (scheme allow-lists,
     sanitizers), and authority rules (what external systems may never mutate).
     /plan-phase re-reads this section whenever a phase touches a surface that
     CONSUMES data classified untrusted here — the consumer side inherits the
     producer's boundary rules, which otherwise live in a phase spec no later phase
     reads. -->

- (no entries yet)
