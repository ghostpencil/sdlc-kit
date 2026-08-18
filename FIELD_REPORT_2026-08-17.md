# Field report (kit 0.24.0, 7th phase of a real adoption): 7 findings — the kit makes every step produce evidence and never makes a number reconcile

**Source:** [sdlc-kit#7](https://github.com/ghostpencil/sdlc-kit/issues/7), filed
2026-08-17 — the **seventh** field report, and the fifth from this adopter (their count;
it covers their seventh phase since adoption). Written against **0.24.0** at the Phase 07
boundary. Reproduced verbatim from the **anonymized** issue body — the adopter keeps the
unredacted copy deliberately as the only one, and where the two disagree theirs is right,
so nothing here should be de-anonymized by a later edit (that includes this file's name).
Two reports arrived the same day; the eighth is `FIELD_REPORT_2026-08-17b.md`. The triage
lives in `FEATURE_PLAN.md` §63.

Field report from a real adoption, produced by `/sdlc-retro` at a phase boundary. Project
details are generalized; the findings, evidence and numbers are as measured.

**Adopter profile.** A small nonprofit's internal Q&A + task web app, deployed behind an SSO
proxy. Python, stdlib-first, single-maintainer, Windows, Claude Code. Kit **0.24.0**, adopted
at 0.1.0 on an existing ungated codebase. **Same adopter as the four prior reports**; this is
the **fifth** report and covers the **seventh** phase since adoption.

**The arc.** 7 slices, 1 PR, 19 numbered owner decisions plus 4 taken mid-arc. It drove the
typecheck leg from 171 errors to zero over application code and removed `continue-on-error`
from the CI type step, then added per-call token accounting so that spend decisions resting
on estimates could finally be checked against a measurement.

**The arc itself went well**, which is why this report is worth reading — none of the seven
findings is about the work:

| | previous phase close | this phase close | how measured |
|---|---|---|---|
| lint | 0 | **0 — green** | re-run during the retro |
| typecheck | 171 errors in 9 files | **0 in 17 source files** | re-run during the retro |
| tests | 474 | **678, all passing** | re-run during the retro |
| CI coverage floor | 52 | **61** | read from the CI workflow |
| typecheck `continue-on-error` | on | **removed** | read from the CI workflow |
| fix commits in the arc | 4 | **0** | `git log <arc range>` |
| close-out records COMPLETE | — | **7 / 7** | `sh hooks/sdlc-close-out.sh check` per slice |

Seven slices. Whole-arc review found no code defect and said so, with three candidate
findings verified against source, discarded, and reported as discarded.

---

## 1. `/end-phase` counts the backlog without reconciling it against the arc that just closed

**Severity: high.** It corrupts the one owner decision the phase close exists to produce.

At the close, the owner was presented with **101 open backlog entries** and asked the
convert/defer/drop question, choosing *convert into the next phase* — the first time that
trigger ever fired on this adoption.

But **the arc's own headline deliverable was one of the 101.** That entry was the reason
the phase existed; it shipped across two slices, merged, and was verified in production
from the container's own startup banner. It carries **no closing marker**:

```
entry A (arc's deliverable, shipped): closing-markers=[]
entry B (half shipped):               closing-markers=[]
```

So it counted toward the pile, and — because the retirement step keys on that marker — **it
could never have retired.** The retirement step itself worked correctly and moved 20 other
entries out; it simply had nothing to key on for these.

**The text implicated**, `commands/end-phase.md`, the *Surface the backlog* bullet (read
off the installed copy):

> - **Surface the backlog:** report the open deferred-entry count with a severity
>   breakdown, flag the oldest untouched entries, and ask the owner once — convert (a
>   cleanup slice or the next phase's scope), defer knowingly, or drop. **Record each
>   verdict on the entry's own line as it is taken** — `— done (<fix commit>)` when a
>   slice closed it, `— dropped (owner, <date>)` on a drop ruling; a deferral leaves
>   the line unmarked. The line's marker is what the retirement bullet below reads;
>   a verdict that lives only in this conversation is one no later step can act on.

The bullet is right about the *mechanism* and silent about the *population*. It says to
record a verdict **"as it is taken"** — but for an entry a slice closed three days ago, no
verdict is being taken at this moment, and nothing tells the step to ask *which of these
did this arc close?* before reporting a number. The same wording is the canonical statement
in `templates/SDLC.template.md` → *Phase end* step 6 (*"open-entry count with a severity
breakdown … with each verdict written onto the entry line as it is taken"*), so **both
homes need the fix** or they disagree.

**Proposed fix.** A reconcile pass ahead of the count, in both homes: *before reporting the
open-entry count, walk this arc's slice commits and phase spec and mark `— done
(<commit>)` on every entry they closed; report the count after that pass, and state how
many the pass just closed.* The count then describes the future instead of mixing it with
the past.

**A second shape the step has no answer for: the half-delivered entry.** One entry here
shipped half its scope and still opens with a sentence asserting the very absence the
delivered half removed — in the entry someone would read to find out whether that thing
exists. The kit offers only done / dropped / unmarked, and a half-done entry silently takes
the *unmarked* branch, which is indistinguishable from untouched. The owner's ruling at
this retro was **split it**: close the delivered half with its marker so it retires, open a
new numbered entry for the remainder with fresh provenance. Worth stating in the kit.

**Generalizes?** Yes. Any adoption whose phase is scoped from its own backlog hits this the
first time a phase closes an entry it was scoped from — which is the normal case.

---

## 2. "Status only — one line" has no observer, and the very next arc broke it 7 times out of 7

**Severity: high.** A rule the owner ratified at the *previous* retro, written into two
files, followed zero times, detected by nothing.

The previous retro produced this owner decision, now in `templates/SDLC.template.md` →
*Bookkeeping rules*:

> - ⚠️ **A slice close-out records STATUS ONLY in the project index** *(owner decision …
>   supersedes the per-slice detail blocks the previous five arcs wrote).* One line per
>   slice; the detail goes into the phase spec or stays in the commit message, which is
>   already the better record.

and in `commands/end-slice.md` §9:

> - Mark the slice done in the current phase's status/START HERE section. **Status only —
>   one line.** … A real adoption wrote 83–163 lines of per-slice detail into the
>   index five times and paid an archiving step once per arc to move it back out; the
>   phase-close archival bullet stays as the safety net, not the plan.

**Measured**, `git show --numstat` on each of the seven close-out docs commits, index file
only:

| slice | lines added |
|---|---|
| S1 | 75 |
| S2 | 44 |
| S3 | 53 |
| S4 | 44 |
| S5 | 87 |
| S6 | 51 |
| S7 | 50 |
| **total** | **404 (avg 58)** |

The rule says *one*. The previous arc's five close-outs averaged ~107, so the decision
halved the write and enforced nothing — and **the file ended up bigger**:

```
project index @ previous phase close:      1,678 lines
              @ just before /end-phase:    2,322 lines
              @ after archive + retirement: 1,903 lines
retired-items file:                           361 lines
```

**Net +225 lines in the index, after the archiving bullet *and* the first-ever
closed-item retirement both fired correctly.** Both mitigations did their jobs and the
number still moved the wrong way. The kit's own hedge — *"the phase-close archival bullet
stays as the safety net, not the plan"* — describes exactly what happened for the seventh
consecutive arc.

The owner's read: **the rule is right; it needs an observer.** That is the finding. This kit
already knows the pattern — an earlier retro on this adoption found a CI coverage floor
recorded in the index that the workflow file never received, and the answer was a
bump-and-reconcile bullet plus a test that reads the workflow. Here the same class recurs
with no equivalent.

**Proposed fix.** Make it observable where it is broken. Cheapest form matching existing
machinery: extend `hooks/sdlc-close-out.sh` (`stop-check`, or a new `docs-check`) to read
`git show --numstat HEAD -- <index path>` on a close-out docs commit and flag when the diff
exceeds a stated budget — log-only by default, like its bare-commit class. Second-cheapest:
state a **number** instead of "one line", so there is something a checker can compare
against. "One line" is the specification that seven consecutive sessions read and did not
follow.

**Generalizes?** Yes — and note the shape: the kit's own answer to over-writing was a
*cleanup* step, and a cleanup step cannot enforce a budget, only pay for exceeding it.

---

## 3. The TDD-ordering guard classifies writes by path, and the path class it uses is wrong

**Severity: high, chronic.** Five consecutive close-outs paid it; this arc it escaped the
slice loop entirely and made a mandated `/end-phase` step unexecutable as written. Prior
adoptions of this project logged it four times as four separate notes; it is one finding.

**Measured**, from `.git/sdlc-tdd/guard.log` on the machine the arc ran on (`.git/` is
per-clone, so this is one clone's record), 656 lines over the window:

| | count |
|---|---|
| DENY production write without observed red | **13** |
| …where the target was **outside the repository** (session scratchpad) | **5** |
| refactor licenses declared (distinct) | **15** |
| licenses revoked by a subsequent test edit | **9** |
| production writes admitted under a license | **104** |
| …under a license declared for `/end-phase`'s verification step | **12** |

**The classification, read from the guard itself** (`hooks/sdlc-tdd-guard.py`):

```python
TEST_PATH_PATTERN = "tests/*|test_*.py|*_test.py"     # :68
SOURCE_GLOB = "*.py"                                   # :69
```

and the pre-write path handling:

```python
    n = p.replace("\\", "/")
    root_n = ROOT.replace("\\", "/").rstrip("/")
    if n.lower().startswith(root_n.lower() + "/"):
        rel = n[len(root_n) + 1:]
    else:
        rel = n
```

**That `else` is the defect.** A path outside `ROOT` keeps its absolute form as `rel`,
fails `TEST_PATH_PATTERN`, matches the extension-only `SOURCE_GLOB`, and is therefore
classified **production source**. So a throwaway mutation runner in the session scratchpad
— never committed, never on the gate's path, applying its mutations to a copy — costs the
same license as an edit to the module guarding this project's authoritative,
non-regenerable database. The control cannot distinguish the two acts, so it charges the
same price for both, which is how a license stops meaning anything.

**And it now bites outside the slice loop.** `commands/end-phase.md` step 1 mandates:

> run whatever phase-level verification the phase spec calls for (the `change-verify`
> skill on the arc, plus any smoke test, end-to-end run, or manual script the spec names)

`skills/change-verify/SKILL.md` §3 then requires *"Start the thing and drive it through its
own front door"* — which here meant throwaway scripts to spawn the server, drive HTTP, and
aggregate rows. Every one is a scratchpad write; every one was denied; and **`end-phase.md`
mentions no license anywhere** (grep for `licen` in the installed copy returns nothing). The
12 licensed writes in the table above are the measured cost. **A command that cannot be
executed as written trains the operator to route around the control rather than respect
it** — which is the opposite of what an armed guard is for.

**Proposed fix (the owner's ruling here).** Scope the guard to **tracked repo paths**. A
file outside the repository cannot be production source. That removes the whole scratchpad
class in one change, keeps the license meaningful for real source edits, and introduces no
new concept. If a deeper fix is wanted later, scope by *intent*: the mandated
behavior-preserving steps (`end-slice` 3 and 5, `end-phase` 1) grant the license implicitly,
since they are behavior-preserving **by definition** and editing tests between mutations is
the method rather than a bypass.

**Related, same guard, lower cost — and it fired against the retro itself.** The
compound-command rule counts a test run only as a single bare command. `/sdlc-retro` step 2
mandates re-running the gate; run from an agent shell with a `cd` prefix or a pipe it
produced *"that test run was NOT counted"* **four times in one retro session**. The rule is
right for a TDD cycle; it does not know that some commands are mandated by a step whose
purpose is *measurement*, not development. Also note the recorded gate is three commands
joined by `&&`, so the documented gate and the armed guard disagree about the same command.

**Generalizes?** Yes, strongly, and most on Windows adoptions where an absolute scratchpad
path is the normal place for a throwaway script.

---

## 4. `mutation-testing`'s revert step names no mechanism — and the skill was never activated

**Severity: medium-high.** It caused four working-tree corruptions in one arc.

**The text**, `skills/mutation-testing/SKILL.md:68`:

> - **Always revert:** after each test run, restore the original code

Correct, and mechanism-free. The mechanism a session reaches for on Windows —
`path.write_text(path.read_text())` — silently rewrites the whole file to CRLF. This arc
recorded **four** such corruptions, every one from a hand-rolled mutation or bookkeeping
runner rather than from an editor: two in one slice, one in another, and one from the
`/end-phase` bookkeeping script itself. Each was caught within one run by a project-owned
gate test that asserts working-tree line endings — but that test is this adoption's own
invention, escalated after the hazard recurred five times as prose notes. **The kit ships
the instruction that causes the corruption and nothing that catches it.**

**And the skill was never dispatched.** The skill-activation ledger
(`.git/sdlc-skill-ledger.jsonl`, this clone) carries **33 activations, all inside the
window**, so it is provably alive and faithful:

```
   8  diff-review
   7  tdd
   7  change-simplify
   7  change-verify
   2  (unrelated)
   1  end-phase
   1  (unrelated)
```

`mutation-testing`: **zero lines** — against `commands/end-slice.md`, which says

> Use the mutation-testing skill (`mutation-testing`, installed at
> `.claude/skills/mutation-testing/`) for anything beyond a quick delete-and-run

and against roughly **100 mutations actually run** this arc, recorded in the commit bodies
(6 / 28 / 28 / 9 / 7 / 13 / 15 across seven slices). Every one hand-rolled. On a CLI where
skill activation is relevance-based, **presence is not activation** — and this is the
sharpest "no evidence" the step-evidence sweep can produce, precisely because the ledger is
recording the skill's siblings in the same sessions.

**Proposed fix, two parts.** (a) Give the revert step a mechanism: *restore with
`git checkout -- <path>`, or by bytes (`write_bytes(read_bytes())`) — never by
round-tripping the file as text.* One sentence, and it removes a whole corruption class on
every Windows adoption. (b) Decide what the skill is for: either have `end-slice` step 5
record **which mechanism** was used in its `mutation:` line, or accept that hand-rolling is
the norm and put the byte-safe recipe in the step itself. A skill named in prose that
nothing observes is a step that can silently never run — which is the thing
`/sdlc-retro`'s step-evidence sweep exists to detect, here detecting one of the kit's own.

**Generalizes?** Yes for (a) on any Windows adoption. (b) generalizes to any
relevance-activated CLI.

---

## 5. RED has no shape for a characterization slice — a slice class the process itself mandates

**Severity: medium.** The highest-risk slice of the arc recorded the weakest evidence in it.

**The text**, `commands/next-slice.md`:

> **RED is observed, not assumed:** run each behavior's new test and watch it fail
> before writing the code, and record the observation **as it happens** — the exact
> test command, the failing test's line, the exit code — in a running record kept for
> `/end-slice` … and the close-out states `not observed` rather than omitting the line.

The arc's second slice was **129 characterization tests** pinning all 33 methods of the
module that the next two slices were about to rewrite in ~106 places — the safety net for a
rewrite of the code guarding an authoritative, non-regenerable database. A characterization
suite passes on first run **by construction**; a red can only be manufactured by asserting
something false, which proves the file executes and nothing about whether it would catch a
real change. So the record reads:

```
RED: none — no behavior batches this slice. Characterization tests pin EXISTING …
```

— byte-for-byte the evidence class a README edit produces. The zero-form exists and is
worded for docs and config commits; **nothing distinguishes "this slice added no behavior"
from "this slice's entire product is a net whose strength is the open question."**

The honest observer is **mutation**, and `end-slice.md` step 5 asks only about *"every new
guard, branch, or error path this slice added"* — which a characterization slice also has
none of. So neither step points at the one check carrying signal. **The slice ran 28
mutations plus a 6-case attribution re-check on its own initiative** (28/28 killed); nothing
in the process asked for it, and had the session not thought of it, the riskiest slice of
the arc would have shipped with no evidence at all that its net had holes.

**Proposed fix.** Name the class. A slice whose product is characterization records
`RED: characterization — <N> mutations, <M> killed` in place of the zero-form, and
`end-slice.md` step 5 gains a second trigger: *a slice that pins existing behavior mutates
the code it pins, not the guards it added.*

**A neighbouring gap, same step:** step 5's contract assumes a new branch is *reachable*
("delete it and watch the suite fail"). This arc added 27 narrowings that are unreachable
by construction, where **deletion leaving the suite green is the correct result** and the
step as written reads that as a test gap. Inversion is the mutation that carries signal
there. The step needs a sanctioned form for a guard whose only observer is the typechecker.

**Generalizes?** Yes. Characterization-before-rewrite is a technique the kit's own risk
guidance pushes toward, and its evidence shape is unspecified.

---

## 6. `change-verify` records the environment but never asks that it be constrained

**Severity: medium.** A verification run reached a third-party service holding the
organization's real records.

**The text.** `skills/change-verify/SKILL.md` §3:

> **Execute.** Start the thing and drive it through its own front door: the CLI's argv,
> the HTTP route, the queue message, the UI.

and §5 — the only step that mentions the environment at all:

> ### 5. Record the environment the result came from
> … Record what would let someone else get the same result or explain a different one: the
> command as actually run, the interpreter or runtime and its version, and any
> environment variable, config file, or service the run depended on.

**Record**, not constrain — and the ordering is wrong for the risk: §5 runs *after* §3.

**What happened.** During a slice verification pass, a route returned a real empty result
instead of the expected "not configured" short-circuit. The data-directory variable had
been pointed at a scratch directory, which isolates the databases and the corpus — and
**not the credentials**, which come from a dotenv file and a service-account key in the
repo root. The server minted a live OAuth token and read the organization's real
third-party calendar. Read-only as it happened; the write route is one route away.

This adoption had already solved the identical problem for its **test suite** months
earlier — its conftest neutralizes credentials *separately* from redirecting the data
directory, after a slice found that redirecting the data directory alone is "a half-built
isolation that reads as complete". The lesson did not transfer to manual runs **because
nothing prompted it to**: the skill's only environment step is a post-hoc record.

**Proposed fix.** A pre-run bullet in §3: *before executing, name every credential, account
and third-party service the run could reach, and state how each is isolated or why it is
safe to reach. A run that will touch a real external service is an owner question, not a
footnote in the report.* The information is already required by §5 — it is simply being
collected one step too late to act as a control.

**Generalizes?** Yes. §3's whole point is that the run reaches things the test harness
fakes; credentials are one of those things, and the skill treats reaching them as a
reporting detail.

---

## 7. The gate baseline table drifts one row at a time, and only two rows have a procedure

**Severity: low individually, structural cumulatively.** Third instance of one class in four
retros on this adoption.

**Measured during the retro:** the suite collects and passes **678**.

| home | reads |
|---|---|
| *Records* baseline table — **the enforcement home** | **676** |
| *Coverage floor* prose, same file | 678 |
| project index ceiling line | 678 |

`templates/SDLC.template.md` → *Records* → *The gate*:

> | `pytest` | **7 passing at adoption; suite now 676 tests, 0 failing** | must stay green — no failing test may be committed |

The kit has answered this class twice, both times for a **different row of the same
table**: the coverage floor got a bump-and-reconcile bullet after a retro found CI enforcing
28 while the index claimed 32 for two days; the type ceiling got the
lower-it / schedule-it / ratify-it procedure in 0.9.0 after reading the same number for five
arcs — and it then drifted *again inside this arc*, the index reading a stale figure with 38
errors of slack for two slices while the enforcement table read the real one. **The
test-count row sits in the same table and has neither procedure.**

**Proposed fix.** At `/end-phase` step 6, reconcile the **whole Records table** against a
fresh gate run — every row reported recorded-vs-measured — rather than naming two rows and
leaving the rest to whoever remembers. A table with two procedural rows and one wish is
exactly how the type leg sat unchanged for five arcs.

**Generalizes?** Yes. The template seeds the table; the commands walk two of its rows.

---

## What worked well

Named so a future simplification pass leaves them alone. Each with its disposition attached
— a catch is not a fix.

- **Re-derivation before the slice** (`next-slice` §2). Fired three times this arc and
  changed the work each time: one slice re-derived a ratified count and confirmed it
  exactly; another found a ratified decision's site count was 11, not 7; a third found that
  a decision's **cited precedent route does not exist** — a ratified decision resting on
  something that was never there. **Disposition: all three fixed in the slice that found
  them, spec amended in the same commit.** Five arcs running.
- **Verify-before-apply in review** (`end-slice` step 4 / `end-phase` step 4). The whole-arc
  review produced **three candidate findings that did not survive verification** and
  reported them as discarded — one about an exception escaping a guard that the dispatch net
  actually catches by documented intent, one about a field being `None` that the source sets
  two lines earlier, and one "stale citation" that was the reviewer's own miscount.
  **Disposition: all three discarded, none entered a fix batch, zero fix commits in the
  arc.** Second arc where the review found no code defect; the discipline of *saying so*
  rather than manufacturing a finding is what makes that read as a result instead of a
  skipped step.
- **The three-recurrences-buys-a-control rule** (`templates/SDLC.template.md`, *Bookkeeping
  rules*). This adoption's line-ending hazard was recorded as prose **five times**, each
  note sharper than the last, each one followed, and it recurred every time. Escalated to a
  gate test under this rule, it then caught **all four** recurrences this arc within one run
  each — against a cause (helper scripts, not editors) nobody had anticipated when it was
  written. **Disposition: all four fixed in the run that caught them.** The rule is the
  reason the control exists; finding 4 above is what keeps feeding it.
- **The close-out evidence record** (`end-slice` step 8 + `hooks/sdlc-close-out.sh`). All
  seven slice commits pass the structural checker, re-run during the retro:

  ```
  COMPLETE - RED(7)  quality mutation verify
  COMPLETE - RED(1)  quality mutation verify
  COMPLETE - RED(1)  quality mutation verify
  COMPLETE - RED(9)  quality mutation verify
  COMPLETE - RED(4)  quality mutation verify
  COMPLETE - RED(14) quality mutation verify
  COMPLETE - RED(15) quality mutation verify
  ```

  **Disposition: 7/7, no amend needed.** This is the single highest-value thing 0.23.0
  added: it is why findings 4 and 5 above are *provable* rather than remembered, and why
  the step-evidence sweep below could be built from artifacts instead of recollection.

**One more, unprompted.** The kit friction log went from **no new entry in three arcs** —
the previous retro's finding 6 — to **ten entries in one arc**, all written at the moment of
friction, and **four of this report's seven findings are built on them**. `/end-slice` step
9's explicit prompt is what did it. That fix worked, and it is the reason this report has
evidence for a chronic ergonomics problem instead of a vague complaint about it.

⚠️ One caveat on the log worth passing back: entries are inserted **worst-first by hand**,
and during this arc one insertion **overwrote the head of the entry below it** — leaving an
orphaned body with no date and no opening clause, in a log whose entire purpose is not
losing records. Recovered verbatim from git. If the kit wants the worst-first ordering, the
log may need append-then-sort rather than insert-in-place.

---

## Step evidence

Every named step, with its state in this window. Sources: slice commit bodies, backlog
provenance tags, the skill ledger (**this clone only** — an activation on another machine
leaves no line), the close-out checker, and the guard log.

| named step | state | evidence |
|---|---|---|
| Observed RED (`next-slice` §4) | **ran** | 51 `RED:` lines over 7 commits, each with command, failing line and exit code; 4 explicit `not observed — <reason>` |
| RED on a characterization slice | **no shape** | zero-form on a 129-test net; **finding 5** |
| TDD skill | **ran** | ledger ×7 |
| Quality pass (`change-simplify`) | **ran, and caught** | ledger ×7; `quality:` 7/7 — 12 moves applied, 10 proposed and dropped with stated reasons |
| Slice review (`diff-review`) | **ran, and caught** | ledger ×8; 10 new backlog entries, all tagged `measured` with the anchor read at source; one slice's review caught a missing observability line that two acceptance items were written against |
| Review lenses | **ran** | per-lens verdicts in each hand-back; the arc lens *unconsumed artifact* found a `close()` with no production consumer |
| Mutation check (`end-slice` 5) | **ran, and caught** | `mutation:` 7/7, ~100 mutations. Caught a probe that left the suite **green** because a broad `except` let substring assertions pass through either handler — assertion made exact before the guard was pinned; a later slice found **3 survivors** and closed them |
| — the `mutation-testing` **skill** | **no evidence** | **zero ledger lines** in a window with 33; **finding 4** |
| Slice verification (`change-verify`) | **ran, and caught** | ledger ×7; `verify:` 7/7, each naming shell, interpreter, and **what was not exercised**. Caught the live third-party call → **finding 6** |
| Close-out record check (`end-slice` 8) | **ran** | 7/7 COMPLETE, re-run during the retro |
| Index bookkeeping, status-only (`end-slice` 9) | **ran, rule not followed** | 404 lines added over 7 close-outs; **finding 2** |
| Friction log write (`end-slice` 9) | **ran** | 10 entries, all in window — the previous retro's fix working |
| Phase-level verification (`end-phase` 1) | **ran** | needed 12 licensed scratchpad writes → **finding 3** |
| Owner acceptance, halt 4 | **ran, and caught** | per-item verdicts recorded; one item closed a **two-arc-old** acceptance item from a previous phase on a real measurement and discharged a re-tune obligation deferred three times. The same measurement **disproved a claim made while presenting it** — a plausible "warm cache" steady state was offered, the owner ran the test, and the cache-read counter was **0 across every paid call**. One item recorded **half met** rather than waved through |
| Whole-arc review | **ran** | both axes clean, no fix batch, 3 findings discarded on verification and reported as discarded |
| Preserved-contract check | **ran** | `n/a — no entries` (contract seeded empty at 0.23.0) |
| Deploy + what-did-it-turn-on (`end-phase` 6) | **ran, and caught** | deploy verified against the platform's own record *and* the container's banner; caught that a new subsystem **went live with no configuration action** (unset means enabled), named with its independent off switch |
| Type-ceiling reconcile | **ran** | outcome 1 — fell to 0, lowered in both homes |
| Coverage-floor reconcile | **ran** | raised from CI's own printed figure; both homes agree, re-verified during the retro |
| Product-contract reconcile | **ran** | 7 entries seeded + 1 deliberately `claim-only`, each pin checked to exist; the one-time backfill offered and **accepted as outstanding** |
| Backlog surfaced | **ran, count wrong** | **finding 1** |
| Closed-item retirement | **ran** | first ever — 20 entries moved verbatim; the step's own re-read correctly **left behind** one entry lacking a marker |

---

## Suggested priority

| # | change | file(s) | effort |
|---|---|---|---|
| 3 | Scope the TDD guard to tracked repo paths — a file outside `ROOT` is not production source | `hooks/sdlc-tdd-guard.py` (the pre-write `else: rel = n` branch) | S |
| 4a | Give `mutation-testing`'s revert step a mechanism: `git checkout` or bytes, never a text round-trip | `skills/mutation-testing/SKILL.md:68` | S |
| 1 | Reconcile the backlog against the arc **before** counting it; add a half-done marker | `commands/end-phase.md` + `templates/SDLC.template.md` *Phase end* 6 | S |
| 3b | Mention the refactor license in `/end-phase` step 1, or exempt mandated verification steps | `commands/end-phase.md` step 1 | S |
| 6 | Move credential isolation from a post-run record to a pre-run prompt | `skills/change-verify/SKILL.md` §3 | S |
| 7 | Reconcile the **whole** Records table at phase close, not two named rows | `templates/SDLC.template.md` *Records* + `commands/end-phase.md` 6 | S |
| 5 | Name the characterization-slice class in RED and in the mutation step; sanction inversion for unreachable guards | `commands/next-slice.md` §4 + `commands/end-slice.md` 5 | M |
| 2 | Give "status only — one line" an observer, or restate it as a checkable budget | `commands/end-slice.md` §9 + `hooks/sdlc-close-out.sh` | M |
| 4b | Decide whether `mutation-testing` is a skill to dispatch or a recipe to inline | `commands/end-slice.md` 5 | M |

---

## Cross-cutting theme

**This kit is good at making a step produce evidence, and bad at making a number
reconcile.**

Every step the process names ran this arc and left a durable artifact: 7/7 close-out records
COMPLETE, 33 logged skill activations, 51 observed reds with commands and exit codes, ~100
mutations, a deploy verified from the container's own log, three review findings discarded
on verification and named. That is a genuinely strong result, and it is why this report could
be written from artifacts rather than from memory. **0.23.0's evidence machinery is the
reason** — nearly every finding above is provable only because something wrote a line at the
moment of the act.

And at that same moment, **three separately ratified numbers were wrong in the record**: the
backlog said 101 open when at least one was finished and shipped; the gate baseline said 676
tests when it was 678; the bookkeeping rule said one line per close-out when it was
fifty-eight. None was caught by any step, because every step in the kit verifies that an
**act** occurred — was the test watched to fail, was the guard mutated, did the reviewer
return — and no step verifies that a **count** still holds.

The kit has patched this three times now, always one row at a time and always after the
damage: a reconcile bullet for the coverage floor, a three-outcome procedure for the type
ceiling, and a marker-keyed retirement step in 0.23.0 that this arc promptly starved of
markers. It will keep recurring one number at a time until the phase close gains a single
reconcile pass whose job is *every recorded number in the process files, re-derived against
the tree*, reported as recorded-vs-measured. **That one pass would have caught all three of
this arc's — in one place, before the owner was asked to make a decision on the first of
them.**
