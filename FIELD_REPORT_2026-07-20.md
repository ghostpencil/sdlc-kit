# Field Report — second arc, and the first run of `/sdlc-retro`

> **Anonymized.** This is the kit-bound copy of a retro run on a real project. Organization
> identity, hosting details, repository and PR links are removed; engineering detail,
> measurements and commit SHAs are intact, because the kit's own rule is *evidence before
> findings* and a finding that cannot name a file is not yet a finding. **Kit file paths
> are exact and unmodified** — they are what each finding implicates. The project retains
> an unredacted copy.
>
> ### Status — submitted
>
> **Placed in the kit's home repository 2026-07-20.** Per the twin-copy rule this file was
> created with, this copy is now the canonical submitted version; the adopting project
> retains the unredacted original (`spec/SDLC_RETRO_2026-07-20.md` in its own repo) as its
> record, and its project-side kit-bound twin can be deleted.
>
> Companion: [`FIELD_REPORT.md`](FIELD_REPORT.md) at this repo's root is the **first**
> run's field report. The adopting project restored its own vendored copy from git after a
> kit update deleted it (see finding 1) and audited its 14 findings against the installed
> 0.4.0 files: 9 absorbed, 4 open, 2 unverified.

**Project:** a live Python web app, ~240 KB of app code, serving a small nonprofit's
document archive. Single-maintainer.
**Kit adopted:** 2026-07-19 at 0.1.0, in **Existing Project** mode on an ungated
codebase. Now at 0.4.0.
**Window:** the second arc run fully through the process — hermetic test suite plus a
complete HTTP dispatch net, merged 2026-07-20.

**This is also `/sdlc-retro`'s own first real run**, so it doubles as F1 acceptance
evidence: the command was built to turn recorded history into kit findings, and the
findings below are what it produced. Section *What worked well* and finding 4 are the
parts most directly about the command itself.

**Headline numbers — measured at retro time, not remembered:**

| | Adoption | After PR #2 | After PR #4 |
|---|---|---|---|
| `ruff check .` | 0 (cleaned during adoption) | 0 | **0 — green** |
| `mypy .` | 175 | 171 | **171 — unmoved across four slices** |
| `pytest` | 7 | 34 | **85 passing** |
| CI coverage floor | 12 | 26 | **28** (CI printed 29.02%) |

Four code commits, five docs commits, three kit-update commits. Slice cadence ran roughly
30 minutes apart; the arc-review fix batch (`bb759b9`, 577 insertions across 8 files) was
larger than two of the three slices it corrected.

---

## 1. `/sdlc-update` silently deletes un-manifested files, and reports that it has not

**Severity: medium.** No data was lost. Zero signal, discovered only by a retro sweep
reading the diff of a commit nobody had reason to re-read.

> ⚠️ **Corrected 2026-07-20, after this report was first committed.** The original text
> rated this **high** and called it data loss — *"486 lines destroyed", "two commits' worth
> of authored work"*. That was wrong. The kit's home repository holds a **byte-identical**
> `FIELD_REPORT.md` at its top level (`diff` clean against
> `0ff6645^:sdlc-kit/FIELD_REPORT.md`); what was deleted was the project's **vendored
> copy**. The claim was asserted from a diff showing a deletion, without enumerating where
> the file lived — **the verify-the-denominator failure, in the report that names it as the
> cross-cutting theme.** The defect below is real and unchanged; its blast radius is not.
> Recorded rather than quietly edited, because a retro that hides its own corrections is
> worth less than one that carries them.

**Evidence.** Commit `0ff6645` ("chore: update sdlc-kit 0.2.0 -> 0.3.0") includes the line:

```
 sdlc-kit/FIELD_REPORT.md | 486 ---------------------------
```

That file was **project-authored**, across two deliberate commits — `4aa078b` ("field
report from the first real run of the kit", 437 lines) and `4c88278` ("field report
addendum — the kit has no upgrade path", 49 lines). It held **14 numbered process
findings** plus a *What worked well* section and a suggested-priority table for the kit
authors — precisely the artifact this command exists to produce.

The same commit message states both of these:

> the kept `sdlc-kit/` folder was replaced wholesale with the v0.3.0 bundle.

> Nothing project-owned touched except the version re-stamp in `spec/SDLC.md`.

Both are true of the **manifest** and false of the **repository**. The classifier verified
12/12 files UNCHANGED against v0.2.0 and 14/14 against v0.3.0 — a denominator drawn from
the manifest, which never contained `FIELD_REPORT.md`, so the file was invisible to every
check the procedure ran. "Replaced wholesale" is doing the damage and the verification
step cannot see it, because it only ever asks about files it already knows about.

**This is the same failure this project has now hit three separate times** — building a
list by enumerating what you already assumed rather than what is actually there. The
project's own `spec/PROJECT_INDEX.md` names it the "verify the denominator" lens after it
caused the hermetic-tests slice to miss ten environment variables including all six auth
ones. Here it is inside the kit's own update tooling.

**Cost — real, but bounded.** The canonical copy survives in the kit repo, so the findings
were never at risk. What the deletion cost is *local* continuity: the `Kit friction log`
created two hours later (`296526c`) **restarts numbering at 1** rather than continuing from
14, and the owner did not know the deletion had happened until this retro.

The severity is what a silent, unverified deletion deserves rather than what this instance
happened to cost. The next un-manifested file in that directory may be the only copy —
nothing in the procedure distinguishes the two cases, and nothing tells the reader which
one they are in. The reassurance is the defect: *"Nothing project-owned touched"* is
asserted from a manifest that structurally cannot see the file it just removed.

**Recovered 2026-07-20** to `spec/SDLC_FIELD_REPORT_2026-07-19.md` — project-owned, so
outside anything a kit update replaces. The genuinely new work is the audit attached to it:
its 14 findings checked against the installed 0.4.0 files show **9 absorbed**, 4 open, 2
unverified. Two of the open four — *a written rule that nothing enforces will be violated
silently* (#3) and *run the whole-arc review even when every slice passed* (#5) — were
independently re-derived as findings 4 and 2 below, which is corroboration across two
runs rather than recovery of anything lost.

**Implicates:** `commands/sdlc-update.md` (the classifier's denominator and the
"replaced wholesale" step), `commands/sdlc-setup.md` (which creates `sdlc-kit/` without
warning that its contents are destroyable).

**Proposed fix.** Three parts, cheapest first. (a) Before overwriting, enumerate the
**actual directory contents** and refuse to delete anything not in the incoming or
outgoing manifest — report it and halt. (b) State in `sdlc-setup.md` that `sdlc-kit/` is
kit-owned and volatile, and that project-authored process notes belong at a
project-owned path. (c) Stop asserting "nothing project-owned touched" unless the
procedure actually checked; an unverified reassurance is worse than silence, because it
stops the reader looking.

**Generalizes?** Yes, entirely. Any project that writes anything into `sdlc-kit/` — which
the kit's own field-report convention *invites* — loses it at the next update, silently.

## 2. Slice review is structurally too narrow, and the evidence is now two for two

**Severity: high.** One instance shipped a defect to production.

**Evidence.** Both arcs run under this process ended with the whole-arc review finding a
serious defect that every slice review had passed clean.

- **PR #2:** two data-integrity defects survived three slice reviews. Both were the same
  shape — a partial write reported as total failure, inviting a retry that duplicates rows
  in the authoritative store. One could have put a second row for a single regulatory
  filing cycle into a regulated nonprofit's statutory filing history.
- **PR #4:** three of four reviewers independently converged on a defect four clean slice
  reviews missed, and it was **live in production**. The GET net's guard read
  `isinstance(e, ConnectionError) and self._response_started` — keying on exception type
  as well as the flag, when the flag alone answers "may I still send?". Any
  non-`ConnectionError` raised after the response began framed a second response into the
  first one's unflushed header block. Live trigger, measured: `_send_file`'s
  `Content-Disposition` encodes latin-1/strict, and two files in the live `public/` mirror
  contain U+2019 (Word's automatic right quote). Clicking either citation raised
  `UnicodeEncodeError` mid-response and returned a well-formed **HTTP 200 carrying 13
  bytes of JSON as the PDF**. The arc's stated purpose was to stop failures the frontend
  cannot report; it produced one the frontend reported as *success*.

Meanwhile the ~17 backlog entries slice review produced in this arc skew markedly
cosmetic — a missing `return` before end-of-method (#40), an asymmetric audit summary
(#42), an `Error:` prefix in an alert (#19). The high-severity entries it did not catch
came from arc review: #44 (🔴, live today) and the eight PR #4 deferrals.

The reason is structural, not effort: slice review looks at one diff in one layer, and
these defects live in the interaction between a change and a consumer written against the
old behavior. PR #4's finding 1 is the clean example — nothing about the server change
looked wrong; the damage was one layer away.

**Implicates:** `commands/end-slice.md` §3 (scope of the per-slice review), and
`templates/SDLC.template.md` `Slice loop` step 6.

**Proposed fix.** Do not weaken the arc review to save time — it is the stage with the
track record. Instead give slice review the one lens it structurally lacks: require it to
name each **consumer** of any changed error/return path and state what that consumer did
with the old behavior. PR #4's finding 1, PR #2's refresh-inside-the-try bug and backlog
#45 are all the same question unasked.

**Generalizes?** Yes. The two-stage split is the kit's design; the evidence says stage one
is scoped below the defect class that matters.

## 3. Backlog entries are written as findings when they are hypotheses — 3 of 3 checked were wrong

**Severity: high.** Owner-confirmed as real rework, not noise.

**Evidence.** Every backlog entry whose stated cause was checked at slice start turned out
to be wrong, and all three were written *by slice review*:

- **#21** claimed a Claude 429/529 aborts the connection on `/suggest`. It does not — both
  functions already caught `HTTPError` and bare `Exception` around `call_claude`. The real
  escapes were the unguarded work *before* that try. The fix as specified would have been
  aimed at a path that was already safe.
- **#21** also claimed to be "the smallest remaining one". `do_GET` had **no net at all**,
  reached `get_calendar()` by a *shorter* path, and became #34.
- **#34** claimed the Windows hidden-attribute `PermissionError` was a live trigger for
  `_send_file`'s `read_bytes()`. It is write-path only — Windows refuses `CREATE_ALWAYS`
  on a hidden file, so `open(path,'w')` fails while `'rb'` succeeds every time. Measured in
  about thirty seconds. The net was still correct, for TOCTOU and ACL denial.

`commands/next-slice.md` contains **no instruction to re-derive** — `grep -i
'derive\|hypothes\|cause\|verify'` returns nothing. §2 says to "identify the next unstarted
slice and its exit criteria", which reads as *adopt the entry*, not *test it*. The
project's own index eventually wrote the missing rule itself: *"A backlog entry is a
hypothesis with a timestamp, not a finding."* That sentence should not have had to be
discovered by a project.

Note the failure mode #34 demonstrates: a fix aimed at a fictional trigger that is
**right anyway for a different reason** passes every test you can write for it. It is
invisible to the gate, invisible to review, and it silently teaches the next reader a
false fact about the system.

**Implicates:** `commands/next-slice.md` §2, and `commands/end-slice.md` §3 (where entries
are *written*).

**Proposed fix.** Both ends. Writing: require each deferred entry to mark its cause
**measured** or **suspected**, so the reader knows what needs checking. Reading: add one
line to `/next-slice` §2 — re-derive the entry's stated cause before writing any fix, and
correct the entry in place when it does not hold. Owner initially judged that
mutation-testing (finding 4) subsumed this; on the #34 evidence above it does not, and the
owner revised to recommending both.

## 4. The kit ships mutation-testing and no workflow command ever invokes it

**Severity: medium-high.** A capability installed, paid for, and reachable only by habit.

**Evidence.** `.claude/commands/mutation-testing.md` is installed. `grep -rl -i mutation
.claude/commands/` matches exactly two files: the skill itself, and `sdlc-setup.md` —
which *installs* it. `end-slice.md` does not mention it. Neither does `next-slice.md` or
`end-phase.md`. Nothing in the slice loop calls the thing.

This project used it anyway, by habit, and it repeatedly did work nothing else did:

- It caught **a test that could not have failed**. Slice #34's status-guard test originally
  sent an error envelope, which trips `!m.error` as well as `!r.ok` — so it would have
  passed with the guard deleted. Sending a *map-shaped* body with a 500 status is what
  makes the two disagree.
- In PR #4's arc review it proved the root cause of finding 2: **deleting either production
  `_response_started` assignment left the whole suite green.**
- `print_exc` survived the first mutation pass and needed a purpose-built test calling
  `_dispatch_failed` outside any `except` block before the two implementations disagreed.

The project's own summary — *"a check is only trustworthy once it has been made to
disagree"* — applies to the tests you just wrote, not only to old ones. That is a kit-level
rule discovered by a project because the kit never stated it.

**Implicates:** `commands/end-slice.md` (no step invokes it), `templates/SDLC.template.md`
(`Slice loop` does not mention it), `commands/mutation-testing.md` (nothing routes to it).

**Proposed fix.** Make it a step, not a skill sitting on a shelf: every **new guard,
branch, or error path** added in a slice must be deleted or inverted once, and the suite
watched to fail on exactly the intended test. It is cheap, it is already written, and on
this evidence it is the single highest-yield check in the kit.

## 5. Test doubles simpler than production hid real defects — twice in one arc

**Severity: medium.** Both instances produced a green suite over a real bug.

**Evidence.**

- `DispatchRecorder._send` overrode production `_send` and **dropped its one side effect**
  (`_response_started = True`). The flag was therefore *simulated everywhere and produced
  nowhere*, making "route sends, then raises" — the exact shape of finding 2 above —
  structurally unreachable in tests. Four slice reviews missed the production defect for
  this reason.
- Slice #34's information-disclosure test constructed `PermissionError(13, "Permission
  denied")` **without a filename**. `OSError` stringifies *with* its filename, which is how
  `/file` came to publish absolute server paths. A double one field simpler than reality
  made the leak invisible.

**Implicates:** `reference/TESTING.template.md` / the kit's mock policy, and
`commands/end-slice.md` (review has no prompt for it).

**Proposed fix.** State the rule in the testing reference: a double that replaces
production code must reproduce its **side effects and its error surface**, or the test
must drive the real thing. Add "does any double omit a side effect of what it replaces?"
to the review prompts. `spec/TESTING.md` in this project already warns that *"a test that
asserts 'returns empty on error' is usually pinning a bug"* — this is the same class one
level up, at the double rather than the assertion.

## 6. `/end-slice` names a review tool that does not exist

**Severity: medium.** Carried from `Kit friction log` #1, unresolved at 0.4.0.

**Evidence.** `.claude/commands/end-slice.md` §3: *"Run the code-review skill on the
working diff"*. No `code-review` skill is installed — not in `.claude/commands/`, not in
`~/.claude/commands/`, not in the agent's skill listing. The built-in `/code-review` is
owner-typed and billed; an agent cannot launch it. `SDLC.md` `Phase end` step 4 names
`pr-review-toolkit:review-pr`, a real tool — so step 3 is the outlier, not the convention.

**What it caused.** During `chore/cleanup-hermetic-tests` the agent substituted
`pr-review-toolkit:code-reviewer` and **did not surface the substitution**. The review was
good, which is exactly why nothing prompted a second look; the owner found out by asking
why a "PR review" ran on a branch with no PR.

**Implicates:** `commands/end-slice.md` §3, `templates/SDLC.template.md`.

**Proposed fix.** Name a tool that exists, distinguish the agent-runnable per-slice
reviewer from the owner-typed `/code-review` escalation, and add the standing rule that a
substituted tool must be named in the hand-back.

## 7. The one-branch-per-arc rule is stated only in BUILD terms

**Severity: medium.** Getting it wrong silently forfeits the review stage with the best
track record.

**Evidence.** `Shape` defines the rule only for phases (*"lives on one branch
`feat/phase-NN-<slug>` … ends in a single PR"*). STABILIZATION has neither a numbered
phase nor a phase spec. `commands/next-slice.md` §3 says to create a branch "if a
phase/cleanup branch already exists **for this work**" — where "this work" reads naturally
as *this slice*, especially since the STABILIZATION slug is slice-specific
(`chore/cleanup-<slug>`) while the BUILD slug is phase-specific.

**What it caused.** The agent closed the hermetic-tests slice, then put a follow-on docs
finding *arising from that slice's own review* on a second branch cut from `main` — which
produces two arcs, two PRs, and **no single whole-arc review spanning both**. Given
finding 2, that forfeits the highest-value stage in the process. The owner caught it;
nothing in the kit would have.

**Implicates:** `commands/next-slice.md` §3, `templates/SDLC.template.md` (`Shape`),
`commands/end-slice.md` (its PR prohibition assumes an accumulation rule it never states).

**Proposed fix.** State it once, mode-independently: *slices accumulate on one arc branch
until `/end-phase`; only `/end-phase` opens a PR.* Have `/next-slice` §3 check for **any
unmerged arc branch**, not just "am I on `main`". Name the STABILIZATION branch for the
**arc** (`chore/cleanup-<arc-theme>`), not its first slice — PR #2 ended up named after its
*last* slice, which is the same drift showing from the other end.

## 8. Nothing says when it is safe to update the kit

**Severity: medium.** Owner-confirmed: it changed the rules under in-flight work.

**Evidence.** Three updates landed in a three-hour window on 2026-07-19 — `9fe4b1b`
(0.1.0→0.2.0, 16:57), `0ff6645` (0.2.0→0.3.0, 18:37), `463f26a` (0.3.0→0.4.0, 19:44) —
immediately before the arc's first slice commit at 20:43, with the arc already scoped. The
0.3.0 update alone rewrote 25 files (850 insertions, 739 deletions) and changed the
behavior of `end-slice`, `end-phase` and `sdlc-setup`. `commands/sdlc-update.md` states a
procedure but says nothing about *when* to run it.

Which kit version governed which slice of PR #4 is now unreconstructable from the record,
and finding 1 — the destroyed field report — was a direct consequence of updating without
a stated safe point.

**Implicates:** `commands/sdlc-update.md`.

**Proposed fix.** One sentence: update at a phase/arc boundary, never with an arc in
flight. If an update must happen mid-arc, record the version against the affected slices.

## 9. `/end-phase` says nothing about deploying

**Severity: medium.** In this arc a production fix sat unshipped behind a step the command
does not have.

**Evidence.** `grep -i 'deploy\|render\|restart' .claude/commands/end-phase.md` returns
**no match**. Step 6 ends at "post-merge bookkeeping". Yet PR #4's headline fix was the
U+2019 corrupted-200 defect, live in production, and merging does not ship it — the platform
redeploys code from `main`, but the fix reaches users only once that redeploy completes.
The project had to write the warning itself, as a ⚠️ block in `spec/PROJECT_INDEX.md`:
*"A production deploy is warranted but NOT automatic."*

`spec/SDLC.md` does carry a `Deploying a phase` section — but that is the project-owned
file, and no command routes to it, so it is documentation the process never enforces.

**Implicates:** `commands/end-phase.md` (step 6), `templates/SDLC.template.md`.

**Proposed fix.** Add a step 7: *does this phase require a deploy, and has it happened?*
The kit cannot know a given project's deploy procedure, but it can make the question
mandatory and point at wherever the project recorded the answer.

## 10. No rule converts a backlog pile into work

**Severity: low, compounding.**

**Evidence.** `spec/SDLC.md` `Bookkeeping rules`: *"a big enough pile becomes a cleanup
slice by owner decision."* The backlog now stands at roughly **30 open entries** and is
labelled in the project's own index as *"a menu, not a mandate"*. Three owner-flagged
entries (#2 the 193 KB monolith, #3 the open security items, #4 stale docs) have sat
untouched since adoption day while two full arcs were selected from elsewhere in the list.
"Big enough" is never defined, so the decision defers indefinitely by default.

**Implicates:** `templates/SDLC.template.md` (`Bookkeeping rules`), `commands/end-phase.md`
(the natural prompt point).

**Proposed fix.** Make `/end-phase` surface the backlog with counts by severity and ask the
owner once: convert, defer, or drop. A prompt at a boundary, not a threshold.

## 11. Halt 2 is ceremony when the slice is already owner-decided

**Severity: low.** Owner-nominated for deletion, then narrowed.

**Evidence.** `Owner halt points` #2 requires "one question at the start of `/next-slice`"
confirming slice scope. The next slice, #38/#50, is recorded in `spec/PROJECT_INDEX.md` as
**OWNER-DECIDED 2026-07-20**, with its implementation constraint (`action="crash"`,
distinguishable from `fail`), its test obligations, and its rationale for not folding into
PR #4 all specified in advance. Re-asking "is this the scope?" adds nothing.

**Implicates:** `commands/next-slice.md` §2, `templates/SDLC.template.md` (`Owner halt
points`).

**Proposed fix.** Narrow rather than remove: skip halt 2 when the slice is already recorded
as owner-decided with scope; keep it for anything unscoped or ambiguous. The owner's first
instinct was to delete it outright and revised to this on reflection.

---

## 12. Line-ending churn makes every update unreadable — and `/sdlc-retro` cannot see it

**Severity: medium**, and it is the probable *mechanism* of finding 1.

**Evidence.** The project's `.gitattributes` pins `eol=lf` for `*.sh`, `docker-entrypoint.sh`
and `Dockerfile` only — the files that run inside a Linux container, where CRLF breaks the
shebang. Nothing covers `*.md`, and `core.autocrlf` is `true`. The kit ships its markdown
with LF. So **every kit install rewrites the line endings of every `.md` file it touches**,
and `git status` reports them all as modified when most have no content change at all.

Measured on the 0.3.0→0.4.0 update (`463f26a`): **11 `.md` files in the commit, 5 with a
real content change** of more than four lines. The kit's own planning notes record the same
effect at larger scale — *"every kit update will report ~24 phantom-modified `.md` files
when only 4 differ in committed content."* It reproduced three times in the retro session
itself: every commit emitted `warning: LF will be replaced by CRLF`.

**Why this is not cosmetic.** It trains the operator to ignore `git status` and diff output
during **the one operation where reading them matters most** — a kit update, which
overwrites files wholesale. Finding 1 is a file deletion that went unnoticed inside a
25-file update commit. A changeset where two dozen entries are known-meaningless noise is
precisely the condition under which a single `486 ----------` line does not register. The
two findings are one story: **the update procedure generates the noise that hides its own
mistakes.**

**And every retro sweep is blind to it.** `commands/sdlc-retro.md` step 2 mines backlog
provenance tags, gate trajectory, Phase History, Environment gotchas, and `git log` friction
signals. A line-ending mismatch produces no backlog entry, no gate movement, no Phase
History row, and no commit — it lives in *stderr warnings*, which nothing records. Worse,
this instance **had already been written down** — in the kit's own planning document, which
explicitly called it *"decent `/sdlc-retro` material in its own right"* — and the retro
still missed it, because step 1's orientation reads the project's `spec/SDLC.md` and
`spec/PROJECT_INDEX.md` and never the kit's side. When the kit is developed alongside an
adopting project, half the friction record sits in a repository the command does not open.

This is friction log #2 (*nothing records process friction between retros*) recurring one
level up: the friction log fixed the project-side gap, and the kit-side gap is still open.

**Implicates:** `commands/sdlc-retro.md` steps 1 and 2 (orientation is project-only; no
sweep reaches tooling noise), `commands/sdlc-update.md` (does not normalize or warn about
line endings before overwriting), `commands/sdlc-setup.md` (adoption is the natural place
to check `.gitattributes` covers `*.md`).

**Proposed fix.** (a) At setup, check whether `*.md` has a defined `eol` and offer to add
`*.md text eol=lf`; a one-line `.gitattributes` change removes the noise permanently.
(b) Before an update overwrites anything, report *content-changed* file counts separately
from *touched* counts, so the operator sees `5 changed` rather than `24 modified` — this
also directly mitigates finding 1. (c) Give `/sdlc-retro` step 1 an instruction to read the
kit's own planning/field-report docs when the kit is co-developed, and step 2 a sweep for
recorded-but-unactioned friction on **both** sides.

**Generalizes?** Yes. Any adopting project on Windows, or any mixed-platform team, hits the
same churn; and the retro's project-only orientation is a fixed property of the command.

**Method note — this finding was a miss, and the miss is the point.** It was surfaced by
the owner pointing at the kit's plan, not by any sweep. The evidence discipline that makes
`/sdlc-retro` useful is the same discipline that bounds it: it can only mine what the
project wrote down, and the most accurate record of this particular friction was written
down somewhere the command never looks.

## What worked well

- **The whole-arc review is the most valuable stage in this process, and it is not close.**
  Two arcs, two serious defects that clean slice reviews passed — including one live in
  production. Protect it from any future simplification. Its cost is visible (`bb759b9`
  was 577 insertions of fixes) and that cost *is* the return.
- **Measuring instead of arguing, repeatedly and cheaply.** The hidden-attribute trigger
  (30 seconds to disprove), the local/CI coverage gap (2.1 points, not the remembered 0.3),
  the "last instance" claim, the U+2019 filenames in the live `public/` mirror. Every one
  overturned something plausible that had already been written down.
- **The `Kit friction log`**, created mid-arc to close the gap where a process finding had
  nowhere to live between retros. It fed three entries straight into this report,
  pre-formatted, with evidence captured at the moment of friction rather than
  reconstructed weeks later. Two became findings 6 and 7 above with no re-derivation.
- **`spec/PROJECT_INDEX.md` as narrative, not just status.** Recording *why* a fix was
  right — including assumptions that turned out false — is the only reason this retro could
  see repetition across slices. Findings 3 and 5 are visible only because someone wrote
  down that they had been wrong.
- **Bookkeeping discipline.** Every fix commit is followed by its docs commit within two
  minutes (`9158022`→`fe8a43b`, `9fddf7c`→`7f738c7`). The "never left for later" rule held
  under a fast slice cadence, which is when it usually breaks.
- **The coverage ratchet set from CI's printed number.** Set wrong three times (38 → 28 →
  26) by computing it; correct ever since it was read. The rule earned its scar tissue.

## Suggested priority

| # | Change | File(s) | Effort |
|---|---|---|---|
| 1 | Never delete un-manifested files; enumerate actual directory contents and halt | `commands/sdlc-update.md` | S |
| 2 | Warn that `sdlc-kit/` is volatile; project notes go to a project-owned path | `commands/sdlc-setup.md` | XS |
| 3 | Require mutation-testing every new guard as a slice-loop step | `commands/end-slice.md`, `templates/SDLC.template.md` | S |
| 4 | Re-derive a backlog entry's cause before fixing; mark causes measured/suspected | `commands/next-slice.md` §2, `commands/end-slice.md` §3 | S |
| 5 | Give slice review a consumer-of-changed-error-path lens | `commands/end-slice.md` §3 | S |
| 6 | Name a review tool that exists; require naming any substitution | `commands/end-slice.md` §3 | XS |
| 7 | State one-branch-per-arc mode-independently; check for any unmerged arc branch | `commands/next-slice.md` §3, `templates/SDLC.template.md` | S |
| 8 | Doubles must reproduce side effects and error surface of what they replace | `reference/TESTING.template.md` | XS |
| 9 | Update only at an arc boundary | `commands/sdlc-update.md` | XS |
| 10 | Add a deploy question to `/end-phase` | `commands/end-phase.md` | XS |
| 11 | Surface the backlog at phase end: convert / defer / drop | `commands/end-phase.md` | XS |
| 12 | Skip halt 2 when the slice is already owner-decided | `commands/next-slice.md` §2 | XS |
| 13 | Report content-changed counts separately from touched counts before overwriting | `commands/sdlc-update.md` | S |
| 14 | Check `*.md` has a defined `eol` at adoption; offer `*.md text eol=lf` | `commands/sdlc-setup.md` | XS |
| 15 | Retro reads the kit's own planning docs when the kit is co-developed | `commands/sdlc-retro.md` §1–2 | S |

Rows 13 and 14 pair with row 1: the same update procedure both generates the noise and
hides its own deletions inside it. Fixing either alone leaves the other half standing.

## Cross-cutting theme

**The kit tells you to verify things, and does not verify its own.** Every finding above is
the same shape: a check whose *denominator* was assumed rather than enumerated. The update
classifier verified 14/14 files it already knew about and deleted the one it did not
(finding 1). Slice review verifies the diff it was handed and cannot see the consumer one
layer away (finding 2). A backlog entry asserts a cause nobody re-measures (finding 3). A
test double reproduces the fields someone remembered (finding 5). A guard is trusted
without ever being made to disagree — by the one tool the kit ships and never calls
(finding 4).

This project learned the lens the hard way and named it: **verify the denominator** —
enumerate independently rather than matching against what you already assumed. It has now
paid for that lesson three times in three unrelated places, and a fourth time *inside this
report*: finding 1 was first written as data loss without checking whether a second copy
existed. One of them did. The lens is hard to apply precisely because the check feels
redundant right up until it isn't.

If only one thing is taken from this report: **a step that cannot see what it is deleting
must not report that it deleted nothing.** `/sdlc-update` is the live instance; the shape
is general.

> **Note on ordering.** Findings are numbered by the damage they appeared to cause when
> written. Finding 1 was subsequently corrected from high to medium (see its own note), so
> the true damage order now leads with **2** (slice review's scope — a production defect)
> and **3** (backlog entries as false findings — owner-confirmed rework). **Finding 12 was
> added last and is not lowest-priority** — it is the probable mechanism of finding 1 and
> should be read directly after it. Numbers were kept stable rather than resequenced,
> because the priority table and several cross-references cite them by ID.
