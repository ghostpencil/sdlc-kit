# Field report (kit 0.30.0, 9th phase of a real adoption): 6 findings — a rule that lives in only one artifact erodes silently, and the kit's own controls are now the main source of that erosion

**Source:** [sdlc-kit#10](https://github.com/ghostpencil/sdlc-kit/issues/10), filed
2026-09-01 — the **tenth** field report, and the seventh from the first adopter (their
count; it covers their ninth phase since adoption). Written against **0.30.0**, which is
genuinely what they run — the 0.30.0 update landed, was re-stamped when the first attempt
did not take, and the arc ran under it. **Generalized here**, as the seventh and ninth
reports were: the findings, evidence and numbers are as measured, but the project name,
its source filenames, its commit SHAs, its PR number and its backlog identifiers are
removed. The issue body itself is un-anonymized; where the two disagree the issue is
right. The triage lives in `FEATURE_PLAN.md` §76.

**Read the triage before acting on the priority table.** Two findings need corrections
that change what the fix is (3's cited step does not prescribe what it is said to
prescribe, and its named home is the wrong file; 6's degradation claim is defused by text
already in the template), and the triage adds a **seventh finding the report did not
make** — the same mechanism as finding 2, found in `change-simplify` instead of
`change-verify`, where it threatens a final, no-extension clock. §76.2 has each one, and
§76.5 reads the arc against the standing clocks, three of which this arc is the first
ever able to move.

---

Field report from a real adoption, produced by `/sdlc-retro` at a phase boundary. Project
details are generalized; the findings, evidence and numbers are as measured.

**Adopter profile.** A small nonprofit's internal Q&A + task web app, deployed behind an
SSO proxy. Python, stdlib-first, single-maintainer, Windows, Claude Code. Kit **0.30.0**,
adopted at 0.1.0 on 2026-07-19 onto an existing ungated codebase with a **red** type
baseline (175 errors). **Same adopter as the seventh and ninth reports**; this is the
**seventh** report from them and covers the **ninth** phase since adoption.

**The arc.** Phase 09 — the four oldest open backlog entries (monolith split, stale doc
facts, `--strict` mypy, coverage). Seven slices, 23 commits, one PR, merged, deployed and
verified.

**Six findings, ordered by damage.** Every citation was read off the installed file at
writing time, not from memory of the process. Two findings that did not survive
verification are reported alongside those that did.

**The two worth reading first:** finding 1 (the refactor-licence hazard reached seven
recurrences in one arc, and the new half is that `/end-slice`'s own mandated step order
cannot be executed without re-declaring the licence) and finding 2 (`change-verify` was
never dispatched across five slice sessions, and the ledger shows exactly which half of
its contract went missing as a result).

**Measured result numbers** (from the CI run at the last commit of the close — not
remembered):

| | before | after |
|---|---|---|
| tests | 762 | **845** |
| coverage floor (CI-enforced) | 63 | **67** (measured 67.87%) |
| mypy errors / files checked | 0 / 18 | **0 / 19** |
| `[tool.mypy]` boolean flags | 2 | **11** (9 of `--strict`'s 13) |
| the sync script's coverage | 0% | **78%** |
| backlog open | 128 | **121** (7 closed, 6 remainders minted) |

Three new controls shipped, each **made to fail** rather than merely built. Two ratified
owner decisions were re-derived mid-arc and found **wrong**, both before they could do
damage.

---

## 1. The refactor-licence hazard: seven recurrences in one arc, two retros, an owner ruling, and nothing built — and the close-out's own mandated order is what breaks it

**Severity: high.** This is the arc's largest single tax and its third consecutive
appearance in a retro.

**Evidence.** The friction log records it at **S4 (three declarations in one slice)**,
**S5**, and **S6 (three more)** — plus the prior arc's S4/S5/S6 entries it was already
escalated from. The 2026-08-31 entry states the count explicitly: *"this hazard has now
been absorbed by two retros"*. The project even carries an auto-memory note written
solely to pre-empt it, and it still fired.

**The half that is new, and the reason "record it again" has stopped working.** Earlier
reports framed this as *"the first close-out write is denied"*. That is not the whole
defect. `commands/end-slice.md` mandates the order **step 4 (review, which fixes tests) →
step 5 (mutation, which writes production) → step 6 (verify, which writes a harness)**,
while the installed TDD guard revokes the licence on **any** test edit:

```
# A test edit invalidates any earlier red and revokes any refactor
if present("refactor-license"):
    clear("refactor-license")
    log("refactor license revoked (a test edit starts a new cycle)")
```

So the close-out sequence **cannot be executed without repeatedly re-declaring the
licence** — S6 paid it three times, each revocation caused by the mutation step's own
prescribed *restore* of a test file. The revocation rule is correct for a TDD cycle and
wrong for close-out, which is mandated, behavior-preserving by definition, and where
editing tests between mutations **is the method**.

**And step 5 never mentions the licence.** Read at writing time, the installed
`end-slice.md` §5 says:

> For every **new guard, branch, or error path** this slice added (review fixes
> included): delete or invert it once, run the suite, and watch it fail on exactly the
> test that claims to pin it — then restore and confirm green.

Nothing there, or in §3 or §6, names `.git/sdlc-tdd/refactor-license`. Every mutation
pass therefore rediscovers the requirement **by being denied**.

**Homes of the rule:** `commands/end-slice.md` §§3/5/6 (silent about the licence) and
`templates/SDLC.template.md` → *Records*, TDD-guards paragraph (states the revocation
rule as correct without qualifying it for close-out). A fix that touches only one leaves
them disagreeing.

**Suggested fix.** Either (a) exempt a close-out-scoped licence from test-edit
revocation — a `close-out` mode the guard honours between steps 3 and 6 — or (b) have
`end-slice.md` §§3/5/6 each name the licence as a precondition so the cost is at least
predictable. (a) removes the tax; (b) only makes it visible.

**Disposition: RULING OPEN** (owner, 2026-09-01). Explicitly *not* closed by this retro:
absorption twice has already been tried and the recurrence count kept climbing.

---

## 2. `change-verify` was never dispatched in the arc, and exactly the half of its contract that lives only in the skill file went missing

**Severity: high** — because it is silent, and because the step exists to catch what the
gate cannot.

**Evidence, machine-read from the skill ledger on the clone the arc ran on.** Five slice
sessions, each showing the same three dispatches and never a fourth:

| arc | `change-verify` | `change-simplify` | `diff-review` |
|---|---|---|---|
| Phase 07 | 7 | 7 | 8 |
| Phase 08 | 3 | 4 | 6 |
| **Phase 09** | **1** | 5 | 8 |

The single Phase 09 dispatch is `/end-phase`'s own. **This is a regression, not a
long-standing absence** — the skill has 11 all-time dispatches, first seen 2026-08-16.

Yet S2, S3, S4 and S6 all record `verify: ran` with substantive, checkable detail (a real
server on a named port, a byte count, a sha256, "off switch holds"). **The verification
work demonstrably happened** — one of S6's claims was independently re-verified at
`/end-phase` and held. So this is not fabrication.

**What was lost is specific, and the differential shows it.** `commands/end-slice.md` §6
restates part of the contract inline — *"`verify: ran — <verdict per behavior, naming the
shell it ran in>`"* — and **all four records name the shell**. The rest of the contract
lives only in `skills/change-verify/SKILL.md`, which requires:

> - **Verdict per behavior** — observed working / observed broken / **not exercised, and
>   why**. The third is a first-class result and must never be folded into the first.

**None of the four records contains a single "not exercised" verdict.** Every behavior is
reported as a pass. The one dispatched run in the window — `/end-phase`'s — named two
unexercised paths immediately.

**The clincher is S6.** It had a *known* unexercised path: the sync script's `main()` IMAP
body, which a ratified decision deferred behind a `_connect()` seam. Its verify record
reports three verdicts as three passes and says nothing about what it could not reach.
The gap is recorded elsewhere in the spec, so nothing was hidden — but the step whose job
is to say *"here is what I could not exercise"* did not say it.

**Inference, stated as an inference** (the owner left this to the records): the skill was
followed **from memory of `end-slice.md`, not loaded**. The parts the command restates
survived; the parts only the skill carries did not. A session that had opened the skill
file would most plausibly have dispatched it — its two siblings were dispatched in every
one of those same five sessions.

**Corroboration, already known upstream.** `mutation-testing` has **zero dispatches
all-time** on this clone against **~26 mutants actually run in Phase 09 alone**.
`commands/end-slice.md` already says exactly this:

> two arcs of ledger measured **zero** activations against roughly a hundred mutations
> actually run, and a rule that arrives only when a skill happens to be dispatched is a
> rule that arrives never.

Phase 09 is the second skill to show the pattern, and the first to show it as a
**regression from prior arcs**. That is the new information: a skill can be dispatched
faithfully for two arcs and silently stop, with the record contract still satisfied in
wording.

**Suggested fix.** The record contract is satisfiable without the skill, so make the
skill's non-obvious half unavoidable: have `end-slice.md` §6's prescribed record line
carry the third verdict explicitly — `verify: ran — <verdicts>; not exercised: <what, or
"nothing">` — so a run that reached everything must say so, and a run that skipped the
skill cannot produce the line from memory of the command alone.

**Homes:** `commands/end-slice.md` §6 and `skills/change-verify/SKILL.md` (*Report*).

---

## 3. Two kit-installed controls collide: the lint hook rejects the mutation step's own prescribed construction

**Severity: medium** — it blocks a mandated step, twice, in two different constructions.

**Evidence.** `end-slice.md` §5 (and this phase's acceptance item for the size ratchet)
prescribe making a check disagree, and watching it go red. Written the obvious way — dummy
locals in a throwaway function — the PostToolUse **ruff** hook blocked the edit with
**53 × `F841 Local variable is assigned to but never used`**, *before pytest could run at
all*. It recurred at S6 in a new construction (inverting a condition), so this is not one
bad choice of mutation.

The mutation is **by definition** temporary and unused — which is precisely what `F841`
exists to flag. The two controls have no knowledge of each other: the lint hook has no
notion of a mutation in progress, exactly as it has no notion of a refactor in progress
(the friction log already notes that asymmetry against the TDD guard, which at least has
a licence).

**Homes:** `commands/end-slice.md` §5 and the project's own gate-hook wiring, which the
kit's templates seed. The workaround this project found — write mutations at **module
level**, where `F841` does not apply — is real but undiscoverable, and it was found by
being blocked.

**Suggested fix.** `end-slice.md` §5 should name the collision and the module-level form,
or the lint hook should honour the same licence file the TDD guard does.

**Also filed as a project backlog entry** (owner decision, tagged `(retro, 2026-09-01)`),
because the hook wiring is this project's to change.

---

## 4. A docs-only slice is routed through the full TDD loop, and every evidence step resolves to a stated-empty form

**Severity: medium.** Recurrence count **2** in this arc alone (S1 and S7).

**Evidence.** S1 changed three markdown files and one Python *docstring*; S7 changed
markdown only. Both have phase-spec-ratified *"Test approach: none"*. Yet
`commands/next-slice.md` §4 (*Enter the TDD loop*) opens with:

> 1. Read `spec/TESTING.md` — fresh, every time; do not rely on memory.

…before a loop with nothing in it, and `end-slice.md` steps 3, 5 and 6 each resolve to a
stated-empty form (`quality: nothing to do`, `mutation: none — no new guards`,
`verify: skipped`). The forms are *correct* and the records are honest — the cost is
ceremony, and the risk is that a reader learns to write the empty form by reflex.

**Homes:** `commands/next-slice.md` §4 and `commands/end-slice.md` §§3/5/6.

**Suggested fix.** A docs-only branch declared once at `/next-slice` §2 (where scope is
already the one owner halt), which then legitimately short-circuits §4 and the three
empty steps — rather than each step discovering emptiness independently.

---

## 5. Step 5's zero-form hides owed evidence when a slice's correctness rests on a sweep rather than a guard

**Severity: medium**, and it nearly cost this arc a real check.

**Evidence.** S7 shipped no code, so `end-slice.md` §5's literal reading is
`mutation: none — no new guards`, and its characterization branch does not fit either (no
tests were added). But the slice's **entire exit criterion** — *"no backlog entry cites a
line number in the monolith"* — **is a check**, and the *verify the denominator* lens
holds that a check is trustworthy only once made to disagree.

That mattered: S7's sweep needed **five passes** to enumerate its own population
(13 → 15 → 16 → 17 → 18) and one pattern reported a **false clean**. The slice did
eventually feed an injected line anchor into a scratch copy and watch the sweep fire —
but it did that *despite* step 5's zero-form, not because of it.

**Home:** `commands/end-slice.md` §5. **Suggested fix:** name the third case — a slice
whose deliverable is a sweep or a check owes a made-to-disagree run of *that*, and
`mutation: none` is wrong for it.

---

## 6. The kit ships an architecture-impact adapter for a graph it does not own, does not refresh, and names no refresh trigger for

**Severity: low-medium**, and it degrades into a *plausible-looking wrong answer* rather
than an absent one.

**Evidence.** `/end-phase` step 2 and step 6 both invoke
`python .github/hooks/sdlc-impact.py phase <main>`. Every run this arc reported
`PARTIAL … graph-freshness: may be stale`, and `spec/SDLC.md`'s own *Architecture impact
view* section concedes the graph was last analyzed **2026-08-19**, before the prior phase
merged. Nothing in the process says when to regenerate it.

The boundary test says this one **is** the kit's: it is true for any adopter, with any
graph tool, on any shell. (The graph plugin's own `autoUpdate` matcher bug is a *vendor*
defect and is **not** filed here — it belongs to that plugin's repository, and this
project already worked around it with a real `post-commit` hook.)

**Home:** `templates/SDLC.template.md` → *Architecture impact view*, and
`commands/end-phase.md` steps 2 and 6.

---

## What worked well

- **The close-out record contract held perfectly: 7/7 slices carry all five keys**
  (`RED`, `quality`, `lenses`, `mutation`, `verify`), including the stated-empty forms on
  the two docs-only slices. The evidence checker is doing its job — this retro could
  reconstruct the entire arc from commit bodies alone.
- **The review lenses caught four times, and every catch was `verify the denominator`**
  (S1, S2, S4, S7). Two were consequential: S4 found a `noreferrer` guard's hardcoded
  population had silently fallen **6 → 5** and was passing on its floor; S7 found 29
  surviving line anchors. *Disposition: S4's fixed in the arc; S7's open in the backlog.*
- **Mutation testing found what reading could not, again.** S4's eight mutants surfaced
  **five defects the gate could not see — four of them pre-existing**, including a
  vacuous citation-page test and two functions with no coverage at all, all confirmed
  against pre-move `HEAD`. *Disposition: all fixed in the arc.*
- **Re-deriving ratified decisions caught two that were wrong, before either did damage.**
  One decision's seam would have left a query endpoint on a stale retriever after an admin
  reload — silent, production-only, unreachable by any hermetic test. Another's ~57%
  coverage ceiling was simply miscounted; the owner raised the target to ≥75% and the
  slice hit 78%. Neither was found by reading; both by re-measuring.
- **The kit 0.29.0 whole-*Records*-table walk earned its place on its first run.** It
  found the *Scope* row reading **18** against a measured **20** — stale for a whole arc,
  because a module was added at the prior phase's S1 and that close corrected only the
  *mypy* row, which had a bullet. The new rule is precisely what caught it.
- **11 friction entries — the largest harvest of any arc** (prior arcs: 3, 6, 1, 5).
  `/end-slice` step 9 is working, and three of this report's six findings exist only
  because of it.
- **Clean history:** exactly two commits per slice, no reverts, one fix batch (the arc
  review's), no red-gate-then-fix pattern.

---

## Step evidence

Read from slice commit bodies, the deferred backlog's provenance tags, and the skill
ledger — **this machine's clone only**; an activation elsewhere leaves no line here.

| named step | state in the window |
|---|---|
| observed RED | **ran** — S2–S6; `none, no behavior` with a stated reason on the two docs-only slices |
| `change-simplify` (quality) | **caught** — 8 moves applied across S2–S6; ledger confirms 5 dispatches |
| `diff-review` (review) | **caught** — 8 dispatches (7 slices + arc); produced most of the arc's backlog entries |
| review lenses | **caught ×4** — all `verify the denominator` (S1, S2, S4, S7) |
| mutation check | **caught** — ~26 mutants; S4's found 5 defects, 4 pre-existing |
| `mutation-testing` skill | **no evidence** — zero dispatches all-time, against ~26 mutants run |
| `change-verify` | **ran, skill not dispatched** — 4 slices record `verify: ran` with credible detail; ledger shows 0 dispatches in 5 slice sessions (finding 2) |
| `change-verify` (skip form) | **skipped with a stated reason** — S1, S5, S7 |
| preserved-contract check | **ran, clean** — 9 pins on 4 touched surfaces, each verified present and passing |
| unconsumed-artifact lens | **ran** — reached the extracted renderer's 4 consumerless shims independently, but a backlog entry had already recorded them at S4; credited as a confirmation, not a catch |
| close-out evidence checker | **ran** — 7/7 slices complete; no missing keys |
| architecture impact view | **ran, degraded** — `PARTIAL` every time, graph stale since 2026-08-19 (finding 6) |

---

## Findings that did not survive verification

Reported rather than dropped, because a discarded finding is evidence about the sweep.

- **A test helper named by a Phase 05 ratified decision does not exist** — flagged as a
  ratified decision unactioned across four closes. **False.** The decision's trigger is
  the **rule of three** (*"promoted … at the rule-of-three"*) and there are **two**
  consumers: the test module that defines it, and one that imports it. The decision is
  correctly waiting. *(Residual, noted not filed: the second consumer arrived by
  cross-test import, which is the coupling the promotion exists to remove — the counter
  is at 2, not 0.)*
- **19 spec-named paths appear absent from the tree** — the first sweep's denominator was
  wrong. It compared bare basenames against full paths and counted upstream kit citation
  paths (`commands/end-slice.md`) as project files. Re-derived against `git ls-files` with
  basename resolution, the genuine absences are all benign: git-ignored archive files,
  stdlib modules, hypothetical names used in prose, and kit-side field reports. **Zero
  real absences.** The sweep needed the same *verify the denominator* discipline it was
  looking for elsewhere.

---

## Suggested priority

| # | change | file(s) | effort |
|---|---|---|---|
| 1 | Exempt a close-out-scoped refactor licence from test-edit revocation, **or** name the licence in §§3/5/6 | the TDD guard templates, `commands/end-slice.md`, `templates/SDLC.template.md` | M / S |
| 2 | Make §6's record line carry the third verdict: `not exercised: <what, or "nothing">` | `commands/end-slice.md`, `skills/change-verify/SKILL.md` | S |
| 3 | Name the lint-hook/mutation collision and the module-level form, or extend the licence to the lint hook | `commands/end-slice.md`, the gate-hook templates | S / M |
| 4 | A docs-only branch declared once at `/next-slice` §2 that short-circuits §4 and the three empty steps | `commands/next-slice.md`, `commands/end-slice.md` | M |
| 5 | Name step 5's third case: a slice whose deliverable is a sweep owes a made-to-disagree run of the sweep | `commands/end-slice.md` | S |
| 6 | State a regeneration trigger for the architecture graph, or mark the view explicitly best-effort | `templates/SDLC.template.md`, `commands/end-phase.md` | S |

---

## Cross-cutting theme

**A rule that lives in only one artifact is a rule that erodes silently — and the kit's
own controls are now the main source of that erosion.**

Every finding here is one artifact assuming another. Findings 1 and 3 are two
kit-installed controls with no knowledge of each other, each individually correct.
Finding 2 is a contract split between a command and a skill, where **only the half the
command restated survived** — and the ledger can prove it. Finding 5 is a step whose
zero-form is right for guards and wrong for sweeps. Finding 6 is an adapter for a thing
the kit does not own.

The arc's own best moments have the same shape inverted: the whole-*Records*-table walk
caught a stale row precisely **because** kit 0.29.0 stopped trusting the two rows that
had bullets and started walking every row. **The fix pattern is the same everywhere:
enumerate the population instead of visiting the known members** — which is, exactly,
the *verify the denominator* lens that produced four of this arc's catches, turned on the
process instead of the code.
