# The IMPACT proof's seed fixture — derived, never invented

`FEATURE_PLAN.md` §66.2 (a) is a blocker ruling: the adapter's read path is frozen
against a **real** Understand Anything pair, and *"the proof fixtures derive from that
real artifact, never invented."* This directory is that derivation.

## Provenance

Extracted 2026-08-26 from the git-ignored `impact-fixture-source/` snapshot at the repo
root — the pair captured 2026-08-19 from the ruled trial project's `.ua/` directory,
immediately after the owner's observed dashboard read (UA plugin 2.9.4, graph analyzed
2026-08-18T08:53:22Z, overlay written 2026-08-19T09:19:49Z against base `main`). That
snapshot is adopter internals and is never committed; this minimized derivative is.

**What the minimization did, and did not do.** It keeps the nodes whose `filePath` is
one of eight real files, every edge between them, and every layer that still has a
member. Node and layer prose is truncated (`summary` to 80 chars, `description` to 70)
and `languageNotes` dropped, so the fixture stays diffable. The project name is
replaced with `FixtureProject`. **No id, path, type, edge, weight, direction, or
overlay count was altered or synthesized** — the schema and the structure are the
observed ones. 331 nodes / 544 edges became 44 / 59.

## What each observed case is here to preserve

Every one of these is real structure from the trial project's graph, not a shape
constructed to make a test pass:

| Spec §23 case | The real instance kept here |
|---|---|
| 5 — changed file has multiple function/class nodes | `usage_store.py` carries 5 nodes; `tfit_qa_server.py` 20; `tools/build_golden_set.py` 9 |
| 6 — same pair connected by multiple edges | `file:usage_store.py` → `class:usage_store.py:UsageStore` exists **twice**, once `contains` and once `exports`. The affected node must be emitted once |
| 7 — node both directly changed and connected to another changed node | `file:usage_store.py` and `class:usage_store.py:UsageStore` are **both** in `changedNodeIds` **and** adjacent; likewise the `tfit_qa_server.py` and `build_golden_set.py` pairs. They must stay in `changedNodeIds` and never appear in `affectedNodeIds` |
| 2, 8 — file absent from the graph | `usage_pricing.py` and `.claude/settings.json` are in `changedFiles` with **no** matching node — the in-the-wild quirk `SOURCE.md` records, and the reason the snapshot must not be re-frozen from a later, internally-consistent pair |
| layers | five real layers survive with their real membership |

The observed overlay's own invariant also survives and is asserted by the proof:
`changedNodeIds` and `affectedNodeIds` are **disjoint** — true in the real artifact
(0 overlap across 8 and 81 ids) and true here.

## Rules for editing

- Variants for the other negative cases (malformed JSON, missing graph, stale
  metadata, not-ignored UA directory, wrong-branch base) are **mutations of this base
  built by the proof at run time**, not extra files here. A negative case is a
  transformation of the real thing; that is what keeps it honest.
- If Understand Anything's schema changes, re-observe on the trial project and
  re-derive — do not hand-edit these files to match a new schema. `SOURCE.md` in the
  snapshot directory names the frozen pair as the ruling authority.
- Do not "fix" the unmatched files or the freshness gap. They are the only surviving
  real instance of spec responsibilities 6 and 7.
