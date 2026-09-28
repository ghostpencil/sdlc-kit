# Feature Plan

Kit-development artifact. **Sections §1–§51 (2026-07-19 → 2026-08-12) are retired to
`FEATURE_PLAN_HISTORY.md`, numbering preserved** — a `§N` reference below 52, in this
file or any other document, points there (retired in two moves: §1–§30 on 2026-08-05,
§31–§51 on 2026-08-13). This file carries what is live: the standing decisions, the
running clocks, and the active work.

Where this plan and the discussion that produced it disagree, this plan wins. Each
batch is sized for one session. Run `/kit-check` before any release this plan produces.

## Standing decisions — do not re-litigate

A digest with pointers; the full record with each decision's evidence is the history
file. Restating a decision here in more detail than the pointer needs would create a
second source of truth, which is its own recurring hazard
(`CRITICAL_GAPS_ANALYSIS.md`).

- **Foundation decisions, 2026-07-19** (§1), and the rejected/reshaped list (§4) —
  notably: execution-model changes ship on evidence; the slice-runner trial closed
  without shipping (§14), and every trial since is pre-registered with a value
  criterion (§5's trial-protocol rule).
- **Ripple lists in plans are incomplete** (§4a) — derive edit maps mechanically at
  build time, never from the plan's own list.
- **SIMP, 2026-08-03** (§16): the surveyor is deleted and the bar for any future
  custom agent is high; the doubles lens stays; R3.7's archival bullet is the safety
  net. The §16 audit regime binds every rule since: **no confirmed catch after two
  field arcs makes it a deletion candidate** (re-denominated from "two releases" by
  owner ruling 2026-08-14 — the clocks preamble below records why; §16's original
  wording stands unedited in the history file, as retirement requires).
- **Brainstorm, 2026-08-03** (§18): batch order was LEG → COP → STD; secure coding
  ships as lenses, not a command; standards ship as interview + conventions + lenses +
  mechanical gate rules, not prose.
- **PORT, 2026-08-03** (§21, §26, §28, §30): build the translation layer; all of PORT
  ships as one release; the kit owns its reviewer — neither `pr-review-toolkit` nor
  `mattpocock/skills` adopted, `pr-review-toolkit` optional and Claude Code only;
  setup emits exactly one instructions file (§23.1's prohibition); `change-simplify`
  and `change-verify` ship **wired** (§30.2).
- **R5 and ENF, 2026-08-05** (§31): R5.1–R5.5 approved as defined; the Copilot
  enforcement machinery is **addressed trial-first, not declined**.
- **The ENF ramp discipline, 2026-08-05** (§31.8→§31.10): every enforcement feature
  runs probe → pre-registered criteria including a value criterion → logging trial →
  the owner reads the report → deny ramp; nothing enters the installed set unproven,
  and a surprising probe redesigns rather than approximates. Applied unchanged by
  VER.2 (§50) and VER.3 (§52).
- **Enforcement ships as an offer, 2026-08-05** (§31.14): two states, accepted or
  declined-with-date, recorded in `spec/SDLC.md`; never installed unasked, never
  re-asked once declined. Governs the guards, the skill ledger (§38), and the
  close-out backstop (§52).
- **Guard doctrine, 2026-08-08/09** (§40, §42, §44): refusals and counted
  observations are **spoken** in-context, never log-only; the stop guard is
  **session-scoped** (binds only a session that wrote production code or edited a
  test); hook feedback frames itself — hook named, file named, expectation stated.
- **Fail directions, 2026-08-10/13** (§46.3, §52.3): a command step fails **closed**
  (its failure is seen and quoted); a hook fails **open** (a hook that errors must
  not block real work). One artifact may carry both, each stated in its header.
- **Considered and held, 2026-08-07** (§37.6): `/fleet` for the kit's sweeps and
  plan-mode wrapping of `/plan-phase` — recorded with reasons so neither is
  rediscovered as a proposal.

## Standing clocks and inputs

**Clocks are counted in field arcs, not releases — owner decision 2026-08-05.** Both
clocks below were originally set in release numbers, and 0.15.0 and 0.16.0 then shipped
on the same day. Applied literally that would have deleted three pieces of machinery for
failing a test they were never given the chance to sit: the evidence each clock demands
is produced by steps that shipped hours earlier, and no adopter had run an arc under
them. A release is something this repo can do twice in an afternoon; an arc is the unit
that actually exercises a rule. The denominator was wrong, not the rule — this is the
same defect the field reports keep surfacing, found this time in the audit regime
itself. **The §16 audit regime is re-denominated to match — "no confirmed catch after
two field arcs" — by owner ruling 2026-08-14**, closing the flag that stood here since
2026-08-05 (put at two halts before being ruled; the digest above carries the
re-denominated form, and every clock in this section was already counted in arcs).

**Refreshed 2026-09-27, against the tree at 0.31.0.** Shipped machinery is listed by its
clock, not by its build state; the history of each entry lives in the section it cites.

**Clocks the next field arc reads** (both adopters are on 0.31.0, merged 2026-09-04):

- **The three STD lenses — one final ATTRIBUTED clock, two arcs, no further extension**
  (§54 (b), ruled 2026-08-14; restarted §70.7 (i) once the denominator became
  enumerable via the `lenses:` commit-body line). A lens with no lens-named catch is
  deleted, with the conventions' enforcement lines re-pointed in the same batch.
  **Arc one read (§76.5 (i)):** `secrets and exposure` (3 applications) and
  `untrusted input` (2) are at **zero catches** with a real denominator;
  `logging and swallowed errors` recorded **no application** and stays unreadable —
  not a reason to restart again. Arc two decides the two readable lenses.
- **`change-simplify` — final two-sided clock, two arcs** (§70.7 (ii); the
  no-extension commitment is spent and cannot be spent again). Positive: one arc records
  a **Reuse-axis move that names its search**. Negative, disqualifying: a reuse or
  duplication finding first raised by `diff-review` or the whole-arc review on a diff
  this pass already passed over. **Arc one counted as satisfying the positive half**
  (§76.7 ruling 3 — not an extension); negative half checked and not triggered. Arc two is
  read against 0.31.0's corrected `/end-slice` §3 record line.
- **CONTRACT — §16 clock, arc one spent** (§57.5; started under 0.26.0 per §70.7 (iii)).
  §56.2's second criterion — a phase touching a contract surface demonstrably encounters
  its entries — was **met on arc one** (§76.5 (iii): 9 pins, 4 surfaces). Arc two decides
  the first criterion; no confirmed catch after two arcs → deletion candidate.
- **IMPACT — shipped 0.28.0; clock NOT started** (§66.6). Arc one did not count: the
  graph was stale for the whole window (§76.7 ruling 4). 0.31.0 shipped the kit's own
  phase-boundary regeneration trigger and the `autoUpdate` offer with its measured limits
  (auto-remind, not auto-update); the clock starts at the first arc run with a graph
  regenerated under that trigger, and counts only arcs with a usable graph.
- **`stop-check` — two-arc clock from the release carrying the filter (0.29.0)** (§73.8).
  Catch: flags a genuine slice commit lacking its close-out record. A false candidate
  fails §52.2's arming bar, and the clock restarts once; a second false candidate is
  deletion. **Both arcs at a zero non-empty-window denominator is deletion, not
  extension.** The tenth report's arc (run under 0.30.0) has **not been read** against
  this clock — §76.5 is silent on it; read both arcs together at the next retro.
- **Bare-flagging arming bar (§52.2) — log-only.** Unmet at 4 false candidates
  (§70.7 (iv)). It re-opens at the first arc whose false count is zero under the 0.29.0
  filter, and not before (§73.8).
- **§76.9(d) — the two 0.31.0 record-line halves have no observer.** Ruled (α) then (β):
  read arc two's records first; build a log-only observer only if the restatement was not
  enough.

**Settled clocks and contingent keeps:**

- **`change-verify` — clock satisfied** (§30.4): confirmed field catch at slice level,
  arc one, 2026-08-06 (§32.3).
- **`mutation-testing` — kept as depth; the inlined rules are the operative path**
  (§70.7 ruling 4). Three consecutive arcs at zero dispatches, as that ruling predicted;
  §76.5 (v) records a **confirmed catch for the inlining** itself.
- **R3.8's aging rule — contingent keep, still unexercised** (§16): the retro sweep
  consumes friction entries in their own arc, so the older-than-one-phase carry has never
  had one to carry. That is the healthy state; the rule is its backstop.

**Held work — owed, not scheduled:**

- **§76 finding 4 — OUT of 0.31.0 and held for the next batch** (§76.7 ruling 1): its
  short-circuit must be one a code slice cannot take, which is its own design question.
- **§77's residue — the unit and docs perf passes still assert on `max()`** (§77.7).
  Apply the median treatment when either next breaches, not pre-emptively; a breach is
  this finding, not a new one. The cap-20 case's fallback, if it fires, is best-of-2 for
  that case alone, not a raised budget.
- **§78 — the hook launchers' silent not-at-root skip, filed 2026-09-27, not ruled.**
  Measured: every Copilot hook but the ledger is inert below the root on builds before
  1.0.88; a linked worktree disarms them on every build (measured, §78.2) and the Claude
  dialect's guard and backstop by reading. `/skills reload`/`info` confirmed working
  (§78.4). Launcher fix DESIGNED and bench-measured (§78.5: `"cwd": "."` + `[ -e .git ]`,
  state in `git rev-parse --git-dir`); all three rulings taken (§78.6); BUILT 2026-09-27
  (§78.7), which also found the 0.28.1 guard fix blind on the WSL route and fixed it.
  Claude Code worktree session run live (guard + backstop pass from PowerShell; a Git
  Bash launch cannot find Git Bash here — §78.7). `/kit-check` run, eleven findings fixed
  (§78.8); RELEASED as 0.31.1. A harness-contract regression it shipped, caught by
  TFit's own tests during its update, is fixed as 0.31.2 (§78.9).
- **§79 — Copilot runs the Claude-dialect hooks from `.claude/settings.json`, filed
  2026-09-27, not ruled.** Both-dialect projects only; neither adopter exposed. Owed:
  a design and a ruling.
- **JUDGE — queued, not scheduled** (§37.5): the LLM-assisted layer for contracts a
  script verifies structurally but not semantically. Precondition (VER.1) met; opens
  only when the owner schedules it.

**Standing inputs:** none pending. Every field report through the tenth
(`sdlc-kit#10`, §76) is triaged, ruled, and shipped (0.31.0); the #10 reply was posted
2026-09-04. The next input is either adopter's next arc retro.

**The Copilot bench is still standing** (§29.3): fixture repo
`D:\AICourse\copilot-ci-test`; `pr-review-toolkit` installed on the owner's Copilot CLI;
neither is tracked, reversal steps recorded there. The ENF, OBS, VER.2, and VER.3 trial
artifacts stand on it (§31.16, §50.5, §52.7), including the backstop trio in logging mode.

---

## 52. VER.3 opened — the stop-time backstop designed: the checker's reserved
## seat filled, a two-class binding rule, the ramp pre-registered, 2026-08-13

VER.3's two prerequisites cleared in 0.21.0: VER.1's checker owns the record
grammar and reserved the seat (§46.3's mode argument), and VER.2's dialect
proved Claude's `Stop` event live on the bench (`stop: WOULD-BLOCK` /
`stop: clean`, §50.5) — the gate the §37.4 table set on the Claude half. What
follows is the design, proposed not built: the owner reads before anything
enters the installed set (§37.7), and the ENF ramp discipline (§31.8→§31.10)
applies unchanged.

### 52.1 Scope — the escape it closes, and the one it honestly does not

`/end-slice` step 8 runs the checker cooperatively; the session that commits a
slice and ends without running it — or ends past an unresolved INCOMPLETE —
escapes. The stop hook is the backstop for exactly that session. It is not a
second gate on sessions the command flow already served: when step 8 ran and
passed, the stop hook re-parses the same commit with the same grammar and
agrees by construction — one parse function, two callers, no state between
them.

### 52.2 The binding crux, and the two-class rule proposed

A stop hook takes no ref argument; "the session's slice commit" (the §37.4
row's phrase) must be derived. The subject-line route is out — the commit
convention is the project's own where one is recorded (`end-slice.md` step 7),
so shape-matching subjects would bind on a convention the kit does not control.
The rule proposed instead classifies every **unpushed** commit by the record
grammar itself:

- **Candidates:** `git rev-list @{u}..HEAD`, capped at 20; no upstream → HEAD
  only, the narrowing stated in the log line. Unpushed is also the remediation
  boundary: the fix is `git commit --amend`, legal exactly while unpushed —
  the same boundary step 8's own fix line states.
- **Complete record** — all four keys valid → clean.
- **Defective record** — ≥ 1 key line present but the set incomplete, empty,
  or duplicated → **flag**. Partial presence proves close-out intent; this is
  VER.1's INCOMPLETE escaped past step 8, and the verdict is stateless — a
  defective record is defective whichever session looks at it, so this class
  needs no session baseline, no `sessionStart` hook, no new state machinery.
- **Bare commit** — zero keys → ambiguous: a slice commit with the
  silent-total absence the checker exists to catch, or a legitimate
  docs/bookkeeping commit. Flagged only when the TDD guard's state shows
  slice-loop evidence for *this* session — `prod-write-observed` or
  `last-test-edit` under `.git/sdlc-tdd/` beside a `session` marker matching
  the stop payload's id; the guard already resets that state per session
  (owner-decided 2026-08-08), so its scoping ruling does double duty here.
  Where the guard is absent or declined, bare commits log a note and never
  block — stated per inv 15: on a guard-less adoption the backstop catches
  defective records, not silent-total absence; step 8 and `/sdlc-retro`'s
  git-log sweep own that class there.

**Bare-flagging arms last, if ever:** it rides the whole ramp in log-only form
and arms only if the trial *and* the first field arc show zero false
candidates — a docs commit made in the same session as slice work is a real
false-block shape, and a block whose remedy is "assert this is not a slice
commit and stop again" is a worse rule than a log line. Pre-registered now so
the arming decision is evidence-bound, not mood-bound.

### 52.3 Interface

- **Home:** the reserved seat — `stop-check` joins `close-out.template.sh`,
  the check-mode awk extracted into a `parse_record <ref>` function both modes
  call (§46.3's point: share the parse, never fork it). State dir
  `.git/sdlc-close-out/` (log + arming flag), mirroring the guard's layout.
- **Fail direction inverts per mode, in one file:** `check` stays fail-closed
  (§46.3, unchanged); `stop-check` fails OPEN — its own errors log and exit 0,
  because a hook that errors must not block real work (§31.7 item 5 is the
  specimen). The header states both directions side by side, since one file
  now carries both.
- **Payload:** the only fields read are `stop_hook_active` (stand down
  unconditionally when true — never fight the cap, measured at 8 on both
  dialects) and the session id (bare-class matching only; `sessionId` /
  `session_id`, either casing). Both are machine-emitted fixed keys, so a
  fixed sed/grep extraction replaces the guard's python-or-node parser
  apparatus — the guard parses prose-valued fields (commands, patch text) and
  needs a real JSON parser; a literal boolean and a UUID do not. If the
  extraction misses, stop-check logs and stands down — fail-open again.
- **Copilot wiring:** its own hook file `close-out-hook.template.json` →
  `.github/hooks/sdlc-close-out.json`, `agentStop`, using the guard json's
  proven wrapper shape (`cat | sh .github/hooks/sdlc-close-out.sh stop-check`
  behind the `.git`-and-file existence test). Block schema measured §31.11:
  `{"decision":"block","reason":…}`.
- **Claude wiring:** a `Stop` block in `settings.template.json` behind the
  proven-but-undocumented `"shell": "bash"` pin — the same file already
  carries it twice (gate and ledger hooks, bench-proven 2026-08-07) — so the
  sh body runs without a python shim. Same block schema, documented on Claude;
  honored-in-practice is a ramp probe (P2), not an assumption — §31.10's rule,
  a denial that does not deny is the failure mode being hunted.
- **Install stance:** an offer, not unconditional — enforcement wiring falls
  under §31.14's two-state rule (accepted or declined-with-date, recorded in
  `spec/SDLC.md`), its own offer beside the guard's in setup and in
  `/sdlc-update`'s transition note. Independent of the guard decision; setup
  states the bare-class dependency when the guard is declined.

### 52.4 Probes pre-registered (before any build)

- **P1 — the Stop-with-bash-pin launch:** does a `"shell": "bash"` `Stop` hook
  deliver stdin and run an sh script on the Windows bench? The pin is proven
  on `PostToolUse`; `Stop` is unmeasured, and §50.3's S1 is the standing
  warning against assuming a hook shell. One logging hook, one bench session.
- **P2 — Claude stop-block honored** (a deny-ramp probe, not pre-build):
  VER.2's live proof ran logging mode only; the armed schema on Claude is
  documented, not measured.
- No Copilot probes owed: `agentStop` schema, block schema, wrapper shape, and
  `-p`-mode firing are all §31.9/§31.11 bench facts the guard ships on today.

### 52.5 Criteria and decision rule

Offline first against a fixture corpus (defective / complete / bare crossed
with guard state present / absent / stale-session; the no-upstream fallback;
CRLF bodies; the candidate cap), driven through `tools/close-out-check.py`
grown for the mode, mutation seats included; then live on the bench, both
dialects, logging mode throughout.

- **V1 — defective-catch:** a scripted run commits a slice missing one key,
  skips step 8, stops → WOULD-BLOCK naming the commit and the key.
- **V2 — bare-catch:** guard-armed bench, a slice-loop session commits with
  zero keys → WOULD-BLOCK via the discriminator.
- **V3 — silence on clean:** complete record → `stop: clean`; a guard-less
  docs session's bare commit → note only; a mid-slice session with no commit →
  clean.
- **S1 — zero false flags** across the corpus. **S2 — cheap:** capped walk,
  two forks per candidate (§46.2's fork-budget note applies per commit).
  **S3 — logging inert and fail-open verified:** errors never block, exit 0
  throughout. **S4 — stand-down** on `stop_hook_active`; the 8-cap never
  approached. **S5 — reversible:** hook files + state dir removed → clean
  session, no artifact recreated. **S6 — dialect agreement** on identical
  corpora.

**Decision rule, fixed now:** all → the owner reads the trial report; then the
deny-ramp (arming flag, D-criteria in §31.10's shape, P2 inside it) may be
proposed. Any V fails → the binding rule is wrong, back to 52.2. Any S fails →
ships log-only or not at all. Bare-flagging's arming has its own bar (52.2).
JUDGE stays queued behind this batch (§37.5), unchanged.

### 52.6 Cost named up front, and the owner decisions owed

Files: `close-out.template.sh`, new `close-out-hook.template.json`,
`settings.template.json`, `sdlc-setup.md` (offer, per-dialect install bullets,
proof step), `sdlc-update.md`, `GATE_RECIPES.md`, `SDLC.template.md`'s checker
note, both README trees (inv 5), `COPILOT.md` mapping row, CHANGELOG,
`tools/close-out-check.py`; manifest regenerated same-commit — §51's finding
is one release old, and the release workflow catches it late where the
invariant wants it never. New rules enter the §16 audit clock, counted in
field arcs.

Owner decisions owed before the build: **(a)** the binding rule — the
two-class design, bare-flagging log-only until its own bar clears; **(b)** the
install stance — its own offer, independent of the guard's; **(c)** ramp
scheduling — P1 plus the logging trial now, release timing decided at the
halt, or the whole batch held for its own bench arc.

**All three taken as recommended, 2026-08-13:** (a) approved as proposed;
(b) its own offer; (c) P1 plus the logging trial now, the owner reads the
trial report at the next halt and release timing is decided there. This
section is committed before any probe or guard code runs — pre-registration
proven by commit ordering, §31.9's `4928fa9` precedent.

### 52.7 Built and proven — same day: P1 one take, offline all green, every
### live criterion met on both dialects; the report awaits the owner's read

**P1 first, one take** (bench `probe-stop-pin.log`, session 851140ea): the
`"shell": "bash"` pin **holds on `Stop`** — the script ran under Git Bash
(`MINGW64`, not the S1 PowerShell default, not WSL), the full JSON payload
arrived on stdin (`session_id` snake_case, `stop_hook_active`, plus
unadvertised fields), hook cwd was the project root, and the exact ship shape
`sh .github/hooks/<file>.sh stop-check` ran verbatim with no wrapper and no
python shim. The Claude wiring ships that literal line.

**Built** per 52.3, no design deviations: `close-out.template.sh` grew
`count_record()` (one parse, two callers — check-mode output byte-identical,
proven before anything else was touched) and the fail-open `stop-check` flow;
new `close-out-hook.template.json` (Copilot `agentStop`, guard-wrapper shape);
the settings `Stop` block behind the pin; the offer in `sdlc-setup.md` step 6
recording into the existing `{{CLOSE_OUT_CHECK_NOTE}}` (no new placeholder —
inv 1's set is unchanged); the backstop recipe section in `GATE_RECIPES.md`;
the 0.22.0 transition in `sdlc-update.md` (the `.json` joins the kit-owned
classification row and pathspec, with the project row's `*.json` glob gaining
its exception); both README turns and root CLAUDE.md's "one kit-owned file"
phrase (now two — §51's derived-statement lesson applied at write time);
CHANGELOG Unreleased.

**Offline** (`tools/close-out-check.py`, now three passes): 21 unit cases
byte-identical green, **15 new stop cases** green on their first run
(defective/complete/bare × guard present/absent/stale-session, both session-id
casings, armed block JSON parsed, bare-never-blocks-even-armed, no-upstream
narrowing, pushed-out-of-scope, defective-below-HEAD, CRLF, cap-20,
empty-payload fail-open), **16 mutations all caught** — the 8 original plus 8
stop-mode seats (stand-down disabled, defective-counted-complete,
bare-ignores-guard, session-unmatched, block-regardless-of-flag,
cap-unbounded, scope-ignores-upstream, RED-treated-singleton). Timing: 255 ms
typical, 3.4 s at the pathological cap-20 bound (~85 ms per Windows sh fork ×
2 forks per candidate) against the 30 s hook timeout.

**Live** (bench, logging mode, seven sessions; record in the bench's
`ENF_PROBE_NOTES.md`, log kept as a standing artifact):

- **V1** — a Claude session committed a record missing `verify:` and stopped:
  `stop: WOULD-BLOCK - defective record on 11becd0( missing verify )`.
- **V2** — Write-tool production file (the guard logged the violation and the
  marker) then a bare commit: `stop: WOULD-BLOCK (bare, log-only by design)`.
- **V3** — no-commit session → `clean (no candidate commits)`; amend-to-
  complete → `clean (1 complete, 0 bare)`; and the load-bearing one: a
  shell-only session beside the *same two bare commits* V2 flagged →
  `clean (… 2 bare without slice-loop evidence)` — the discriminator is
  session-scoped, so the docs-session false-block shape cannot occur.
- **S6** — Copilot `agentStop` ran the identical script through the json
  wrapper: `WOULD-BLOCK - defective record on 53d303f( missing quality )`,
  then `clean (2 complete, 2 bare)` after the amend. Same grammar, same log,
  both dialects.
- **S1** zero false flags across all firings; **S2** every firing far inside
  the 30 s budget; **S3** nothing denied or blocked, stdout never carried a
  verdict; **S4** structurally satisfied in logging mode and pinned offline
  (the `stop_standdown` case and `standdown_disabled` mutation); **S5** hook
  files moved aside → zero new log lines → restored.

Bench reversed to its baseline; the backstop trio joins the standing bench
artifacts beside the guard pairs. Manifest regenerated same-commit (§51's
lesson, applied at write time this once). **Per the 52.5 decision rule the
deny-ramp may now be proposed — after the owner reads this report at the next
halt, where release timing is also decided.** Unreleased until then; the
adopter's next update halt would carry the offer, not an install. P2 (Claude
stop-block honored in practice) remains the deny-ramp's opening probe;
bare-flagging stays log-only with its arming bar untouched.

### 52.8 The halt — owner rulings 2026-08-14, and the deny-ramp protocol
### pre-registered before any deny run

Four rulings taken (the fifth item put at the halt — the §16 regime's
re-denomination wording — received no ruling at this halt; it was ruled later the
same day, after the 0.22.0 release — the clocks preamble records it):

1. **Release held.** 0.22.0 stays untagged; timing returns to the owner after
   this ramp.
2. **The deny ramp opens now** — against the recommendation to wait one
   adopter arc, recorded per the house rule that the disagreement is written
   down, not litigated. Protocol below, pre-registered before any armed run.
3. **`change-simplify`: ruling (b) plus a directed improvement pass** — §53.
4. **The STD per-lens audit is authorized** — §54.

**Deny-ramp protocol (the §31.10 shape, adapted).** Arming is the flag file
`.git/sdlc-close-out/deny-enabled`; absent = logging, unchanged. Scope: the
**defective class only** — bare stays log-only regardless of the flag, by
§52.2's untouched arming bar. The open unknown is P2: Claude Code's Stop-hook
block JSON (`{"decision":"block","reason":…}`) is documented but has never
been measured honored; a denial that does not deny is the failure mode being
hunted (§31.10's rule). The observable for "honored" is fixed now: the log
must show the pair **`stop: BLOCK` followed by `stop: stop_hook_active set -
standing down`** — `stop_hook_active` goes true only when the CLI actually
processed a block, so the pair is the CLI's own receipt — plus the session
visibly receiving the reason (its reply or a remediating action).

- **D1 — deny catches (P2 answered):** armed bench, a session commits a
  defective record and stops → the stop is actually blocked; the BLOCK/
  stand-down pair appears; the session reacts to the reason rather than
  silently ending.
- **D2 — zero false denials:** armed, a session leaving only complete records
  stops clean, no block.
- **D3 — bare stays log-only armed:** armed, bare commit + guard evidence →
  WOULD-BLOCK line only, no block (offline-proven; confirmed live).
- **D4 — no lockup:** every blocked session ends (the stand-down guarantees
  the cap is never fought); a hang is a timeout and fails this criterion.
- **D5 — reversible:** deleting the flag returns the bench to logging mode,
  re-proven by re-running the D1 prompt and seeing WOULD-BLOCK only.
- **D6 — Copilot dialect:** one armed `agentStop` run repeats D1 through the
  json wrapper (the guard's block schema was measured §31.11; this proves the
  backstop emits it correctly).

**Decision rule, fixed now:** all six → the armed mode may be offered — as
arming *instructions* in `GATE_RECIPES.md`'s backstop section (the flag is
per-clone owner action, exactly the guard's pattern; nothing in the installed
set changes), and the owner decides release timing. Any failure → the flag
path ships documented as logging-only-until-fixed, and the failure is the
finding. The bench is disarmed after the trial regardless.

**Ramp run same day — ALL SIX MET** (five sessions, record in the bench's
`ENF_PROBE_NOTES.md`; bench disarmed and reversed after):

- **D1 met, and P2 is answered:** the armed Claude session was actually
  blocked (`stop: BLOCK … 155ad0c( missing verify )`), received the reason,
  **amended with the stated-skip form rather than fabricating** — its own
  words: "rather than fabricating an outcome" — and the stand-down pair
  followed. The documented Stop block JSON is honored in practice; measured,
  no longer assumed.
- **D2, D3, D5 met:** armed-clean stopped clean; armed-bare stayed log-only;
  disarmed-defective logged WOULD-BLOCK only — and that session did *not*
  amend, the exact contrast proving the block (not the log line) is what
  drives remediation.
- **D6 met:** Copilot's armed `agentStop` blocked on the inherited defective
  HEAD, and that session inspected the body itself and amended to the **same
  stated-skip form** (checker: COMPLETE). Same schema, second model family.
- **D4 met throughout** — every session ended, the cap never approached.

Headline for the record: **both dialects, blocked, independently produced the
honest remediation** — the reason text's anti-fabrication framing steering
two model families to the same correct amend. Per the decision rule the
armed mode is offerable: `GATE_RECIPES.md`'s backstop section drops its
"stays a ramp question" caveat for the measured fact (the one edit this
result owes), and release timing for 0.22.0 — now carrying a proven armed
mode — returns to the owner.

## 53. `change-simplify` redirected — the owner's (b) ruling executed: the miss
## diagnosed, three direction defects fixed, one final clock — 2026-08-14

The field record carried its own diagnosis: **Phase 04 S4, the same diff, minutes
apart — this pass said "nothing to do"; `diff-review` caught a duplicated
`LogCaptor` test helper.** A textbook Reuse-axis catch, missed by the pass whose
first axis is Reuse. Three direction defects explain it, each fixed in
`skills/change-simplify/SKILL.md`:

1. **Nothing said test code was in scope.** The axes read as production-shaped; on
   a TDD process, tests are where most of a slice's new code lives — and the miss
   was in a test file. Fixed: a scope paragraph naming test files, duplicated
   setup, and copied fixtures as Reuse territory, with the founding miss cited.
2. **Reuse asked a question but prescribed no act.** "Does this repeat something?"
   invites an eyeball over the diff in isolation — and an unsearched "no
   duplication" spells exactly like a verified one. Fixed: for every symbol the
   diff adds, search the repo for an existing equivalent before concluding clean;
   workflow step 2 runs the search and notes what was searched.
3. **The report had no denominator.** One blanket "nothing to do" line cannot be
   told apart from "did not look" — the assumed-denominator defect every field
   report keeps finding, sitting in the kit's own skill. Fixed: a fifth report
   section, per-axis verdicts, the Reuse line naming its search; the done-when
   requires it.

No derived statements owed: no other file restates the report's section count
(checked — `end-slice.md`, `SDLC.template.md`, `SKILLS.md` describe the pass's
role, not its report shape), and the commit record's `quality:` line grammar is
untouched. CHANGELOG carries the entry as **[installable]** (the skill file
installs to `.claude/skills/`). **The clock is final and stated in the standing
section: one confirmed catch in the next two field arcs, or deletion — no further
extension, the impaired-arc argument spent with this ruling.**

## 54. The STD per-lens audit — owner-authorized 2026-08-14, run same day: the
## recipe keeps, all three lenses are deletion candidates, and the record could
## not have said otherwise

Method: the four §22 subjects (the three STD lenses — *logging and swallowed
errors*, *untrusted input*, *secrets and exposure* — and the runtime-standards
recipe section) matched against every banked catch in the three arcs of exposure:
the 2026-08-06 whole-tree audit (§33), the Phase 03 retro's evidence table
(2026-08-08), the Phase 04 retro's (2026-08-11), and the adopter's backlog and
phase specs, read directly.

**Runtime-standards recipe — CONFIRMED CATCHES, KEEPS.** The mechanical rules it
put into the adopter's gate held everywhere: §33's meta-result ("every mechanized
rule held — Checkstyle catches, no-stdout, SpotBugs"), the SpotBugs
`EI_EXPOSE_REP` catch banked in arc one's evidence table. The recipe is the
lineage's best-performing rule, and its thesis — mechanize what can be
mechanized — is the one every field report keeps re-proving.

**The three lenses — zero attributed catches in three arcs; deletion candidates.**
Not one catch in any retro, backlog entry, or evidence table names any of the
three. The near-misses were checked, not assumed: Phase 03's per-source exception
finding is *error propagation* territory (the pre-STD lens, not on this clock) —
propagation across a loop boundary, not a swallowed error; Phase 04's two
`diff-review` catches were mock-policy drift and a Reuse duplication, neither a
lens on this clock. Sharper than absence-of-catch: the lenses' own subject matter
**produced real defects in the same window and other machinery caught them** —
the level ladder bent and the external audit caught it, not the logging lens; the
malformed-URL key corruption (untrusted input, on an RSS-ingesting adopter —
maximal exposure) was the external audit's catch too; secrets had exposure (API
keys) and neither catch nor recorded activation.

**The caveat the verdict carries:** per-lens attribution is structurally
invisible — R5.6's evidence sweep records `diff-review` as one step, and
`diff-review`'s report does not name which lens produced a finding. A lens catch
in these arcs *could not have been credited* — the same assumed-denominator
defect §53 just fixed in `change-simplify`, one file over. The audit therefore
cannot distinguish "never catches" from "catch never attributable", and says so
rather than pretending the three arcs were a clean test.

**The coupling cost, checked before the halt:** the conventions section names
these lenses as its enforcement (inv 14 — the adopter's `CLAUDE.md` cites the
swallowed-errors lens twice), so deletion re-points those enforcement lines or
trims the conventions to their mechanized part; and the trigger summaries in
`SDLC.template.md` slice-loop step and `end-slice.md` §3 name all three (inv 2's
both-sides rule). Deletion is a multi-file batch, not a file removal.

**Dispositions put to the owner** (the §16 disposition is theirs, never
defaulted): **(a)** delete all three now — three arcs, zero attributed catches,
subject matter demonstrably served better by mechanical rules and audits; the
batch carries the re-pointing above; **(b)** one final *attributed* clock — fix
the denominator first (per-lens verdict lines in `diff-review`'s report, §53's
exact pattern), then two arcs in which a catch must arrive lens-named, no further
extension. (b) is not the impaired-arc argument respent: the claim is not that
exposure was impaired but that the recording instrument could not register a
catch at all. Owner's call; the clocks section holds the pending state.

**Ruled (b) same day, and executed:** the attribution contract now lives in
`REVIEW_LENSES.md`'s preamble (an applied lens reports by name,
`<lens>: <finding, file and line | clean>`; a review applying none writes
`no lens triggered`; a lens finding carries its lens name into wherever the
finding lands, because the hand-back is not retained)
and is mirrored at all three calling sites — `end-slice.md` §4, `end-phase.md`'s
arc review (the unconsumed-artifact verdict named), `SDLC.template.md` step 7's
trigger summary AND phase-end step 4 (inv 2, both sides — the phase-end half was
a §55 catch). **The final clock: two field arcs from the
next arc to run; a catch counts only lens-named; no further extension.** The
owner also ruled 0.22.0 releases now, carrying this batch — the pre-release
`/kit-check` is §55.

## 55. The pre-0.22.0 `/kit-check` — run 2026-08-14; sixteen findings, all fixed
## in-session, and the theme is the same-session batch leaving its own derived
## statements stale

Full pass: the mechanical four in-session, the eleven reading passes fanned to
seven parallel agents, every agent reporting the violation it hunted alongside
its verdict. Six invariants clean outright (3, 5 near-clean, 6, 8, 9, 10 — inv 3
confirmed all 49 placeholders resolved and both new close-out files
placeholder-free). Sixteen findings across the rest, all fixed before this
section was written, and all but three caused by the last 48 hours' own batches:

- **inv 4** — the 0.22.0 transition note in `sdlc-update.md` named
  `{{CLOSE_OUT_CHECK_NOTE}}` literally; only `sdlc-setup.md` may carry `{{`.
- **inv 7** — the root README's exception count went stale exactly as it did at
  0.16.1 ("three exceptions" enumerating four, with the insertion scar); setup's
  exit-check parenthetical said "none of the three" over five out-of-scope
  artifacts; the CHANGELOG's backstop entry was `[adoption-only]` while the
  kit-owned `.sh` reaches adopters automatically → `[installable]`.
- **inv 11** — the LEDGER ITSELF miscounted the vendored set ("five files";
  seven files across five directories) — the denominator slip its own specimen
  warns about, fixed in ledger and command copy.
- **inv 12** — three adopter-facing citations in `tdd-guard-claude.template.py`
  (two unqualified `FEATURE_PLAN.md` refs, one bench file no adopter can
  resolve); the `change-simplify` sentence exposing a kit-internal deletion
  clock.
- **inv 13** — the new backstop had NO SEAT in either denominator list (ledger
  + `/kit-check` copy, whose "As of 0.21.0" stamp was also stale): the check
  was proven but invisible to the next pass — the precise defect the invariant
  exists for, caught pre-release this time.
- **inv 14** — the lens clock as first written into the installed
  `REVIEW_LENSES.md` recorded kit-internal state with an unreachable enforcing
  artifact; reworded to the field fact plus a durable-home rule (a lens finding
  carries its name into the backlog/fix record). Also: arm/disarm asymmetry in
  the template comment; the update path's missing two-direction reconcile for
  the backstop record.
- **inv 15** — three of a kind: the backstop's fire-first proof under-named its
  environment in both homes (now binds the operator's launcher, with the
  Claude-side pin exemption stated), and the checker note did not require the
  fire-proof itself to be recorded (now does, both homes).
- **inv 2** — the attribution clause was missing from the template's phase-end
  step (the mirror obligation: `/end-phase` enforced a rule the canonical file
  did not state), and the lens grammar had drifted (`file and line` dropped in
  both commands); one grammar now stated identically in all four homes.
- **inv 1** — two borderline hedges tightened (`pr-review-toolkit` "stays
  installed **where it is**"; "may be available" at phase end).

Sub-threshold notes recorded, not actioned: inv 3's four (formatter/package-
manager answers feed scaffolding but nothing records them; PROJECT_INDEX's
gotchas section has no placeholder to catch a skipped write), inv 11's
mutation-testing entry carrying documented divergence but no re-datable
verification date, inv 15's credential-clearing checks passing vacuously on a
machine that never held credentials, and inv 1's observation that the update
classifier's POSIX loop is unrunnable from Copilot's Windows shell tool (an
executability gap, not a stated fact — future work, not this release).

Proof suites re-run after the comment-touching fixes: guard dialect 33 cases +
12/12 mutations, close-out 21 + 15 cases + 16/16 mutations, all green. The
release is unblocked; 0.22.0 tags with this section in the tree.

## 56. The sixth field report triaged — the whole-project review of
## ai-news-dashboard: the contract-erosion class is real, and the tree says the
## mechanism is worse than the report's — 2026-08-15

Ingested verbatim as `FIELD_REPORT_2026-08-15.md`. Unlike the five before it this is
not an arc retro: it is a whole-project review of the second adopter (four merged
phases, Copilot CLI) against 0.22.0 main, filed explicitly as planning input, and it
prescribes its own discipline (§13 there: re-verify everything against both trees,
mark each finding measured / suspected / already-addressed, collapse symptoms to root
causes). That discipline was applied before this section was written — two
verification sweeps, one per tree, plus targeted git archaeology on the adopter.

### 56.1 The verdicts, finding by finding

**Report §2 — cross-phase product-contract erosion: MEASURED, mechanism corrected.**
All five Phase 01 ratifications stand in the adopter's `spec/PHASE_01_*.md` and no
later spec, retro, or backlog entry amends any of them: D6 (empty state shows last
refresh status), D23 (per-source `OK`/`WARN` panel with reason), D22 (detail view
with authors/tags and full sanitized content), the B-rows and acceptance checklist
restating them, and the application-owned URL/content safety rule. All five absences
confirmed in the current tree: `DashboardController` depends only on the three item
repositories, neither template carries any status element, the empty state is bare
`No news items yet`, the detail view shows no authors or tags, and
`NewsItem.summaryBasis` hard-truncates at 4,096 characters with no marker — so
"full sanitized feed content" is structurally unsatisfiable. The correction: the
report tells a Phase-02-rewrote-it-away story, but `git log -S "status"` over the
templates directory is empty for the repo's entire history — **the status panel
never rendered in any commit**. Phase 01 was accepted at halt 4 with at least two
checklist items unmet and no recorded deviation (the 2026-08-05 retro, the later
specs, and every backlog revision are silent). Then the 2026-08-06 external audit
filed the orphaned `SourceRefreshStatus` entity as a dead artifact, and Phase 03 S6
(`523844e`) closed that backlog entry **by deleting the entity and its repository** —
a cleanup that moved the tree further from the ratified spec, while `end-phase.md`'s
one prior-phase reach ("an entry that contradicts a ratified spec decision is a spec
conflict — halt 3") never fired, because it relies on the entry naming the conflict
and nothing in context knew D6/D23 existed. So the class has **two entry paths, not
one**: ratified-but-never-delivered surviving acceptance, and
delivered-then-rewritten. Both end identically — ratified behavior absent, every
gate, test, and review green, no owner decision recorded anywhere — and a fix must
sit where both paths pass through: phase planning and phase close, not slice
implementation.

**Report §3 — tests do not preserve old ratified behavior: MEASURED.** The dashboard
tests pin the Phase 02 surface thoroughly (empty-state text, cards, tags, batch
loading, pagination bounds) and nothing pins refresh status; `RefreshOutcome`
appears only in the JSON `POST /refresh` path's tests. Kit-side, the sweep found
**no mechanism at all** for durable regression obligations or test retirement:
"retire" occurs only about kit files, the disposal-intent lens is within-slice
(added-then-deleted in the same slice), and `change-verify`'s neighbouring-behavior
step is per-change, code-path-scoped. Same root as §2 — the missing input is the
obligation, not more tests.

**Report §4 — trust-boundary decay: MEASURED, both halves.** Adopter: feed-provided
URLs flow verbatim (`HackerNewsAdapter` takes `node.get("url")` as-is; the RSS path
checks only non-blank) into persistence and out through raw `th:href` in both
templates; the only scheme check in the repo is test infrastructure
(`TestIsolationConfig`). Phase 01's ratified "application-owned URL and content
safety checks" exists as Jsoup text-sanitization of bodies only — URLs are never
touched. Kit: the untrusted-input lens triggers only when a slice adds or changes an
ingress point, and `/plan-phase`'s trust-boundary interview and sweep are scoped to
*this phase's* behaviors; the per-phase spec's Trust Boundaries section is never
re-read by later phases. A consumer-side rewrite of stored hostile data triggers
nothing. Real gap, same shape as §2: a ratified constraint with no durable home.

**Report §5 — arc review is phase-complete, not regression-complete: MEASURED.**
`/end-phase` checks the arc against the current phase's exit criteria and takes the
acceptance checklist from the current phase's spec; its stated blind spot is
inter-slice seams, not inter-phase ones. Confirmed a design limitation, and the §2
specimen is its negative case. Same root; folds into Investigation A below.

**Report §6 — historical dead artifacts: MEASURED example, minimal disposition.**
`SourceRegistry.enabled` is persisted, seeded `true`, and has **no getter at all** —
no consumer is possible without recompiling the entity. The report's own test
("would STABILIZATION naturally surface it?") answers **no**: `/plan-phase` contains
zero STABILIZATION content, and stabilization work flows only from the deferred
backlog and the red-gate baseline — both write-once channels an unused column never
enters. Even the 2026-08-06 whole-tree audit missed this one while catching its two
siblings. But one harmless column is thin evidence for new mandatory machinery, and
the report agrees. Disposition: **no new sweep.** The load-bearing half joins
Investigation A instead — the `523844e` specimen shows the dangerous case is not the
artifact that lingers but the one that gets *deleted* without checking ratified
decisions; the deletion path is where the check belongs.

**Report §7 — owner comprehension visualization: PREMISE REFUTED.** The report
treats a "planned Understand Anything integration" as an existing commitment. It
does not exist: zero occurrences in this plan, the history file, or any document in
this repo. The underlying observation (a structural CHANGED/REMOVED footprint could
surface surprises prose hand-backs miss) is recorded here as **considered and held**
(§37.6's shape) — with the report's own caveat adopted as the reason: a visualizer
can expose a surprise, but the process still needs an authoritative statement of
what must be preserved, which is Investigation A's job. Resolved at the §56.3
ruling: the plan exists in a separate file outside this repo (owner statement,
2026-08-15); it stays held until after the improvement batches, then gets its own
triage against whatever that file actually says.

**Report §8 — human onboarding: MEASURED, small.** `/sdlc-setup` neither creates
nor checks a project README in either mode — New mode's scaffold list has no README
entry, Existing mode reads one only as analysis evidence, and the close-out never
asks. The adopter's only human-facing run instructions sit in PROJECT_INDEX's
environment-gotchas section. Real gap, deliberately lightweight fix: a minimal
human entry point (what the app is, how to run it, where the process docs live) —
links, never a second home for process truth.

**Report §9 — harness-specific enforcement: ALREADY ADDRESSED in substance.** The
report itself concedes the specific failures were absorbed (0.19–0.22: guard
dialects, split events, shell pins, spoken refusals, the ledger's no-signal rule).
Its residue — "define required harness semantics before adding a harness" — is what
the §31.12 probe protocol and the bench already do de facto. Recorded as a standing
gate rather than built: **no third harness (Cursor or otherwise) gets an adapter
until its semantics are benched against the report's §9 checklist** (discovery,
shell, hook payloads, failed-command observability, stop behavior, deny mechanism,
instruction loading, owner-typed observability, model routing, MCP). No work now;
no Cursor work is planned.

**Report §10 — process cost: ALREADY THE STANDING REGIME.** Field-arc clocks,
deletion candidates, attributed catches, trial-first enforcement — all live in the
clocks section above; the report explicitly endorses the direction and asks for
nothing new. Its one usable pressure — "recurring human friction is a cost, not
user error" — is already R4.6's writer plus the retro sweep. Nothing to do.

**Report §11 — the non-weaknesses: ADOPTED AS CONSTRAINTS.** Fresh context per
slice, one-phase-one-PR, TDD/mutation rigor, the whole-arc review's existence, the
five-halt model (no sixth), and harness delegation are all load-bearing and stay.
Every mechanism below is bound by them.

### 56.2 The root cause, and Investigation A's design brief

Report §§2–5 collapse to one sentence: **no artifact states what the product
currently does, so nothing downstream can be obligated to preserve it.** Phase specs
are per-phase deltas and historical decision records — correctly so; PROJECT_INDEX
is a dashboard and carries phase status, not behavior; and every process step reads
the current phase only. The kit already owns the fix's pattern: invariant 14 ("a
recorded value names its enforcing artifact") is exactly this rule at process
altitude. Investigation A is that invariant applied at product altitude.

Proposed shape, to be designed and pre-registered as its own batch (CONTRACT)
before any build — proposed, not ruled:

- **One new artifact** — a compact, surface-grouped statement of owner-ratified,
  externally observable product truths (the report's §2 sketch, re-derived), one
  line per behavior, each line naming its enforcing test or marked claim-only
  (inv 14's grammar). Phase specs remain the decision record; this becomes the one
  authoritative statement of *current* behavior — today no artifact holds that
  role, so this adds a source of truth without duplicating one.
- **Four touchpoints, all inside existing steps and halts:** `/end-phase` phase
  close reconciles the arc against it (new behaviors enter; behaviors the arc
  removed or left undelivered become explicit halt-4/halt-3 questions — the §2
  specimen's both entry paths die here); `/plan-phase` checks candidate behaviors
  against entries on the surfaces the phase touches, so a planned rewrite
  *encounters* what it must preserve; the whole-arc review gains the preserved-
  contract question for rewritten surfaces; and any deletion of a record-shaped
  artifact (the unconsumed-artifact lens's fix path) first checks the contract and
  ratified decisions (`523844e`'s lesson). Trust-boundary invariants ride in the
  same artifact as their own short section (Investigation B folded in — no
  parallel security-contract system), re-read by `/plan-phase` whenever a touched
  surface consumes data an earlier phase classified untrusted.
- **Test linkage, not test inflation:** entries pin behaviors at contract altitude;
  retiring a named test is a contract edit, and a contract edit is an owner
  decision through the existing halt-3 channel. No one-test-per-sentence rule.
- **Bounded by construction:** entries are current truths only — superseded lines
  are replaced, not accumulated; the artifact is read at phase boundaries, never
  per-slice, so context minimization at slice level is untouched.
- **Setup and update:** New mode instantiates it empty (grown at each phase
  close); Existing mode seeds it in the interview like every other spec fact —
  never inferred silently. `sdlc-update` carries the transition note.

**Value criterion, pre-registered now (the §5 trial-protocol rule):** the report's
§14 scenario, live. Seeding the adopter's contract must force D6/D22/D23 to become
either scheduled work or an explicit owner retirement — outcome B or C of §14,
where today's outcome is the unacceptable D. Then, across the next two field arcs,
any phase touching a contract surface must demonstrably encounter the relevant
entries before implementation (outcome A/B/C). The §16 audit clock applies from day
one: no confirmed catch after two field arcs makes the mechanism a deletion
candidate like any other rule.

### 56.3 Dispositions put to the owner

- **(a) Open CONTRACT as the next kit batch** — design pre-registered in the §52
  shape (design section → owner rulings → build), covering the artifact, the four
  touchpoints, and the §14 validation scenario. Recommended.
- **(b) Trust boundaries ride in the contract artifact** (Investigation B folded
  into A), not a parallel system. Recommended.
- **(c) Report §6:** no new dead-artifact sweep; the deletion-side check ships
  inside CONTRACT. Recommended.
- **(d) Report §7:** held unless the owner names where the "Understand Anything"
  plan lives — nothing in this repo does.
- **(e) README:** approve as its own small batch (a `README.template.md` +
  New-mode scaffold entry + Existing-mode offer), independent of CONTRACT.
  Recommended, after CONTRACT.
- **(f) Adopter-side filings owed** (their backlog is the canonical record, the
  2026-08-06 convention): the URL-scheme gap (report §4 — a real, current
  rendering path for feed-controlled `href`s), the D6/D22/D23 absences (which for
  them are halt-3 spec conflicts, not mere backlog entries), and
  `SourceRegistry.enabled`. An adopter-session action, with each claim re-verified
  at filing time; it would also make their next STABILIZATION arc the CONTRACT
  seed case.

**Ruled 2026-08-15 — all six taken as recommended**, with (d) resolved rather than
held blind: the visualization plan lives in a separate file outside this repo and is
addressed after the improvement batches (the §56.1 entry records it). Order of work:
CONTRACT (design §57, then build on its rulings), then the README batch (e), with
the adopter filing session (f) scheduled against their STABILIZATION arc so the
contract seed case and the filings land together.

## 57. CONTRACT opened — the product-contract mechanism designed: one bounded
## statement of current truths, four touchpoints inside existing halts,
## pre-registered before any build — 2026-08-15

§56.3's rulings opened this batch. What follows is the design, proposed not
built: the owner rules on 57.6 before anything is written into the kit (§37.7's
rule), and the value criterion stands as pre-registered in §56.2, restated
operationally in 57.5. The §11 constraints from the report bind throughout:
context minimization per slice, five halts and no sixth, phase specs stay
historical decision records, one authoritative source per fact.

### 57.1 The artifact

`spec/PRODUCT_CONTRACT.md`, instantiated from
`templates/PRODUCT_CONTRACT.template.md` — placeholder-free (headers and inline
guidance only), so inv 3's placeholder set is untouched. Structure: one section
per user-facing surface (the report §2 sketch's shape, re-derived from the
verified evidence), one line per behavior, each line carrying inv 14's grammar
at product altitude:

    - <externally observable truth, one line> (P<NN> D<M>) —
      pinned: <test or mechanical check> | claim-only (<date>)

The decision pointer (`P01 D23`) keeps phase specs the sole decision record; the
contract states only what is currently true and ratified. A superseding decision
replaces the line and the superseding phase spec records why; a retirement
deletes it, same rule. History lives in specs, current truth lives here — a role
no artifact holds today (§56.2's finding), so this adds a source of truth
without duplicating one. A closing `## Trust boundaries` section carries
high-consequence invariants (data classifications, scheme/rendering policies,
authority rules) in the same grammar. Bounded by construction: current truths
only, contract altitude only — a truth a user could observe or an invariant the
owner ratified, never a restating of specs sentence-by-sentence — and read at
phase boundaries, never per-slice.

### 57.2 The four touchpoints — existing steps, existing halts

1. **`/plan-phase` — the contract pass.** Read the contract whole (it is
   bounded); list entries on surfaces the candidate phase touches; carry them
   into the phase spec under a new `## Preserved behaviors` section of the
   embedded spec template. Slices then inherit them from the current phase spec,
   so `/next-slice` and the context-minimization rule are untouched. An entry
   the phase would remove or alter is put to the owner at the phase-scope halt
   (halt 1) or as a design question (halt 3) — never decided by the plan. The
   existing trust-boundary sweep additionally re-reads the contract's trust
   section whenever a touched surface consumes data an earlier phase classified
   untrusted — the consumer-side blind spot §56.1's §4 names.
2. **`/end-phase` — per-item acceptance verdicts (halt 4).** Every acceptance-
   checklist item is recorded met or owner-dispositioned: deferred (backlog
   entry, does not enter the contract) or dropped (ratified in the spec). An
   unmet item can no longer pass silently — the never-delivered path (Phase
   01's D6/D23) dies at its source. Not a sixth halt: this sharpens what halt 4
   already is, and the verdicts land in the phase spec's checklist itself.
3. **`/end-phase` — the contract reconcile and the preserved-contract
   question.** After acceptance, met behaviors enter or update the contract
   with their pinning tests named (or claim-only, dated) — the inv 14 reconcile,
   performed in the same pass that writes the record. The whole-arc review asks,
   for every surface the arc rewrote, whether that surface's contract entries
   still hold: the named pins still exist and ran green in the arc's gate
   (environment named per inv 15 — the gate run, not a claim). Preserved
   behaviors the arc left unimplemented are checklist items like any other and
   meet touchpoint 2.
4. **The deletion path.** The unconsumed-artifact lens gains one rule on its fix
   path: before a record-shaped artifact is deleted as dead, search the contract
   and the ratifying specs for it — a hit is a spec conflict (halt 3), not a
   cleanup (`523844e` is the specimen). The disposal-intent lens gains the
   mirror clause: deleting, skipping, or gutting a test the contract names as a
   pin is a contract edit, and a contract edit is an owner decision.

### 57.3 Setup, update, and the adoption seam

New mode instantiates the template beside the other spec files; it grows at each
phase close. Existing mode and `/sdlc-update` seed it per owner decision (b)
below. `sdlc-update.md` and the root README's update section carry the same
transition note (inv 8); the install list, both file trees, and the ownership
tables gain the template's row (inv 5, 7, 9); `COPILOT.md` needs no new mapping
row — spec files are CLI-neutral.

### 57.4 Cost named up front

Files: new `templates/PRODUCT_CONTRACT.template.md`; `SDLC.template.md` (the
canonical statements — the artifact's role, the reconcile, per-item verdicts,
the deletion rule; inv 2's both-sides rule covers every command mirror below);
`commands/plan-phase.md` (contract pass + the spec template's `## Preserved
behaviors`); `commands/end-phase.md` (halt-4 verdicts, reconcile step,
arc-review question); `reference/REVIEW_LENSES.md` (two lens clauses);
`commands/sdlc-setup.md`; `commands/sdlc-update.md` + root README update
section; both README trees; CHANGELOG; manifest regenerated same-commit
(inv 10). The reconcile and the deletion-path search are checks: each joins
inv 13's denominator sentence in the same batch with a stated negative case.
Everything new enters the §16 audit clock, counted in field arcs.

### 57.5 Value criterion, operational — and the clock

Unchanged from §56.2: (1) seeding the adopter's contract must force D6/D22/D23
to become scheduled work or an explicit owner retirement — report §14's outcome
B or C, where today's outcome is the unacceptable D; (2) across the next two
field arcs, a phase touching a contract surface demonstrably encounters the
relevant entries before implementation (outcome A, B, or C). The §16 clock runs
from the first arc under the mechanism; a contract pass with no confirmed catch
after two field arcs is a deletion candidate like any other rule.

### 57.6 Owner decisions owed before the build

- **(a) Home and name:** `spec/PRODUCT_CONTRACT.md` from its own template
  (recommended — PROJECT_INDEX stays a bounded dashboard; the contract is
  slow-growing and load-bearing), or a PROJECT_INDEX section.
- **(b) Existing-adoption seeding:** seed empty with a scaffolded note — grown
  at the next phase close, with a one-time backfill offered as that close's
  first reconcile (recommended — no invented facts, cost lands at a halt that
  already exists), or a full backfill interview at update/setup time.
- **(c) Per-item acceptance verdicts at halt 4:** approve as designed
  (recommended — it is the existing halt sharpened, and the §2 specimen's first
  entry path closes nowhere else).

**All three taken as recommended, 2026-08-15** — home is
`spec/PRODUCT_CONTRACT.md` from its own template; existing adoptions seed empty
with the one-time backfill offered at their next phase-close reconcile; halt 4
gains per-item verdicts. This section is committed before the build (§31.9's
pre-registration-by-commit-ordering precedent); the edit map below is derived
mechanically at build time per §4a, with §57.4 as the floor, not the list.

### 57.7 Built — same day, all three rulings applied as taken

The edit map, derived mechanically at build time (§4a) — §57.4's floor held, plus
two walkthrough touches it had not named (`sdlc-kit-process-flow.md`'s sweep count
and phase-end steps) and the `CLAUDE.template.md` spec-loading row:

- **New:** `templates/PRODUCT_CONTRACT.template.md` — placeholder-free, seeds
  empty, entry grammar and trust-boundaries section per 57.1; inv 3's set
  unchanged (census re-run: `{{` hits in `sdlc-setup.md` only).
- **Canonical:** `SDLC.template.md` gains the *Product contract* section (read
  boundaries, write rule, retirement-only-by-ratification, pinned-test rule,
  deletion rule, mid-flight backfill) plus its five mirrors: phase-start sweep
  list and spec contents, halt-4 per-item verdicts, arc-review
  preserved-contract check, bookkeeping reconcile, slice-loop trigger line
  (inv 2, both sides in the same batch).
- **Commands:** `plan-phase.md` (preserved-contract sweep with the
  consumer-side trust re-read; spec template's *Preserved Behaviors*),
  `end-phase.md` (halt-4 verdicts with the field specimen cited; the
  preserved-contract check with its stated negative case — a renamed-away pin
  must flag; the reconcile bullet with its own — an entry naming a test the
  tree does not hold fails it; the one-time backfill offer, decline recorded
  with date), `end-slice.md` §4 trigger summary.
- **Lenses:** the unconsumed artifact gains rule 4 (the fix path searches the
  contract before deletion — negative case: a name the contract does contain
  must hit; `523844e` cited as specimen); the disposal-intent trigger and
  rule 4 cover contract-pinned tests.
- **Seams:** setup instantiates the contract in both modes (Existing mode
  seeds empty by design — backfill is `/end-phase`'s, never setup's);
  `sdlc-update.md` + root README carry the mirrored 0.23.0 transition note
  (inv 8); both README trees updated (inv 5/9, the bundle's verbatim count is
  now seven); CHANGELOG Unreleased; inv 13's denominator extended in ledger
  and `/kit-check` copy (stamp moved to 0.23.0); `COPILOT.md` needed nothing —
  its spec row is the `spec/*.md` glob.
- **Manifest:** regenerated from staged content, discrimination proven —
  exactly the nine edited bundle files changed hash plus the one new entry,
  nothing else; entry count 40 = `git ls-files sdlc-kit` − 1; `sha256sum -c`
  green in the working tree (the release workflow's own check).

No step renumbering anywhere — every insertion was designed into an existing
step's body, so no project notes go stale this release. Unreleased: the full
`/kit-check` runs pre-release per the plan's own rule, and release timing is
the owner's. The §16 clock on the whole mechanism starts with the first field
arc that runs under it; the adopter's pending STABILIZATION arc is the seed
case (§56.3 (f) — the filing session and contract seeding land together).

## 58. The pre-0.23.0 `/kit-check` — run 2026-08-15 on the CONTRACT batch:
## sixteen findings, all fixed in-session, one refuted — and the headline is the
## batch's own edit decapitating the coverage-floor bullet

Full pass, §55's shape: the mechanical four in-session (inv 10 — 40 hashes match
committed content, 40 = ls-files − 1; inv 4 — `{{` in `sdlc-setup.md` only, exit
check names its exact scope; inv 9 — both new files in the tree, no deletions
since the §55 pass; inv 6 — 84 refs, all 23 in batch-touched files verified, no
renumbering), the eleven reading passes fanned to seven parallel agents, each
reporting the violation it hunted. Clean outright: inv 3 (49/49 placeholders
resolved semantically — the denominator has grown from B0's 32; the new template
confirmed placeholder-free), inv 11 (7 vendored files / 5 directories, no
divergence introduced, kit-written never described as vendored). Passes with
findings: 1, 5, 7, 12. Fails, fixed: 2, 13, 14, 15.

**The headline (inv 2/13/14, blocking):** the CONTRACT build's reconcile edit
replaced the line it anchored on — `- **Coverage floor — bump the enforcement,
then reconcile:** if the coverage measured` — without re-emitting it, leaving the
ratchet's ~23 lines (two-homes assertion, prove-it-fires proof) headless and
unconditional inside the new bullet. The step the kit's own inv-14 specimen is
about was itself un-stepped by the batch that cited it. Restored, with the §55
lesson re-sharpened: the same-session batch's wreckage is exactly what the
pre-release pass exists to catch, and it caught the same class twice running.

**The design gaps in the new text, all fixed in both homes (inv 14/15):**
`claim-only` defined where introduced (the explicit unenforced state — halt-4
evidence only, never reported clean, re-presented at each touching reconcile);
the check/reconcile population aligned to the sweep's (**touched**, not rewrote —
the narrowing was unstated and read-only consumer surfaces are where the trust
rationale says the risk lives); the pin predicate sharpened (**itself passed**,
not gate-green — a pin skipped or failing inside a recorded red baseline is a
finding); the deletion-path search got its method (entries are behavior prose,
so an identifier grep is the miss — read the bounded contract whole for the
artifact's surface, say what was read, *verify the denominator* applies); and
the three-site contradiction between the slice-level pin trigger and
"read at phase boundaries only" resolved by a stated narrow exception (the
disposal-intent lens opens the contract only when a test was deleted, skipped,
or gutted — *Preserved Behaviors* is a strict subset, so pointing the trigger
there would blind it to untouched-surface pins), with the absence branch added
(a project predating the file says so rather than reporting `no lens
triggered`). The deletion rule now also names its second caller — a cleanup
slice acting on a backlog entry — and `next-slice.md`'s re-derivation carries
the search, closing the reverse-direction gap (the rule's own specimen was a
stabilization slice no arc lens ever saw).

**The rest:** inv 1 — the pin trigger's missing absence clause (fixed above);
inv 5 — same contradiction from the pointer side, plus two pre-existing citation
notes recorded, not actioned; inv 7 — the bundle README's kit-owned list omitted
`.github/agents/explore.agent.md` (pre-existing; added); inv 12 — the shipped
checker's bare-flagging comment gated on the kit's own arming clock ("kit
FEATURE_PLAN 52.2…"), converted to the plain field fact per §55's precedent;
inv 13 — the retro's spec-claims-against-the-tree sweep was on neither
denominator list (added to ledger and command copy, which also re-aligned their
one wording divergence); inv 3's mirror image — the exit check named the guard's
`.sh` dialect but not the instantiated `.py`, so a Claude-only guard acceptance
shipped three placeholders no grep covered (per-dialect scope now stated); and
`sdlc-update.md`'s exhaustive write clause gained the contract file as its
second stated exception. One reported finding refuted on verification: the
"backslash path" in `REVIEW_LENSES.md` does not exist in the tree — the
reporter's own rendering.

Sub-threshold notes recorded, not actioned: the *Coverage floor* citation
resolves to a bold lead-in rather than a heading (self-consistent house form);
setup's closing handoff names a kit-folder path with the durable fallback beside
it; the preserved-contract check's evidence predates the arc's post-batch gate
(the reconcile re-checks pin-exists, not pin-green); both new checks state
negative cases no step schedules (consistent with several standing checks); the
met-verdict → entry direction has no second home to drift; inv 3's standing
sub-threshold set unchanged.

Proof suite re-run after the checker's comment fix: 21 unit + 15 stop cases, 16
mutations all caught. Manifest regenerated, discrimination proven — exactly the
eleven fix-touched files changed hash. The release is unblocked; 0.23.0 tags
with this section in the tree.

## 59. CONTEXT — two pre-release evaluations owner-directed 2026-08-15, both
## grounded against the adopter trees, shipped into the untagged 0.23.0: the
## index gets an exit path, the SDLC file gets a Records section

The owner asked two questions before tagging: does PROJECT_INDEX need a
retire-to-history rule, and is the kit's installed markdown doing smart context
engineering. Both answered by measurement, not reading: TFit's index
(kit 0.11.0) is 143.6 KB / 1,820 lines with the Deferred backlog at 1,257 lines
(69%) — read by every fresh session, ~36k tokens of bookkeeping before any work
— while ai-news-dashboard (0.22.0) sits at 13.7 KB after four phases: the
0.22.0-era discipline prose flattens the curve but nothing removes a closed
item, so the curve is the same. Root cause ruled: growing sections gain entries
at every slice close and closed items have no destination — the one archival
rule (`/end-phase` → phase spec) targets per-slice write-ups, and a done
backlog entry belongs to no phase spec. On the second question the layering
verified sound (instantiation strips template comments — measured zero in both
adopters; skills expose frontmatter only; REVIEW_LENSES trigger-gated) with one
structural defect: every daily command reads a handful of one-line facts out of
`spec/SDLC.md` (gate commands ~l.120, baseline l.128, floor l.160, checker note
l.267, model policy l.305 pre-restructure), so "read the baseline" loads the
whole 676-line file — ~8–10k tokens per command invocation for five lines of
record. Third finding, smaller: `/next-slice` reads the phase spec whole every
slice and the kit said nothing about spec size (TFit Phase 06: 172.8 KB).

Shipped as three deliverables, one recommendation explicitly held. (1) The
retirement rule: closed items only (done/dropped backlog entries, friction
lines `absorbed` >1 phase, verified-fixed gotchas) move verbatim at `/end-phase`
post-merge bookkeeping to `spec/PROJECT_INDEX_HISTORY.md` — single file over
the owner-floated dated-files folder, mirroring the kit's own
FEATURE_PLAN → FEATURE_PLAN_HISTORY precedent (numbering preserved, one
load-table row), dated sections per close giving both shapes at once. Open
items never retire. Denominator rulings taken with the rule (the lineage's own
lesson — a retirement splits a population): `/sdlc-retro`'s orient step now
reads the history file for the window; the deletion-rule search and the
unactioned sweep verified unaffected (they read contract/specs and `open`
lines respectively). (2) The Records section: `SDLC.template.md` restructured
so every per-project value (scope, gate commands, baseline + single-place
sentence, coverage floor, CI line, hook/environment, the three notes, model
policy as a `###` under it) sits in one bounded leading section; doctrine
unchanged below under its old headings (*The Gate*, *Gate baseline*,
*Coverage floor* — the latter promoted from bold lead-in to real heading,
resolving §58's sub-threshold citation note). Executed as a move-the-doctrine
restructure so the three high-density instantiation comments never left their
lines. The four daily commands, retro, setup (model-policy pointer), and
GATE_RECIPES point at *Records*; pointers degrade soft on an unfolded spec
(same lines, old positions — the 0.15.0 disagreement direction, stated in the
transition note). (3) `/plan-phase` step 5 + phase-start step 3: the spec stays
lean enough to read whole per slice; bulk research to a linked appendix file
with its own spec-loading row. Held: the template↔command dedup (the slice
loop's ~40-line review paragraph exists in both homes) — real, but it thins
the canon invariant 2 arbitrates by, and it is a batch of its own if ever;
recorded here so the decision is a ruling, not an omission. Transition notes
extended in both mirrored homes (`sdlc-update.md` 0.23.0 bullet + root README):
the Records fold MOVES recorded values verbatim, never re-derives; the history
file is `/end-phase`'s to create; `CLAUDE.md`'s table diff arrives by hand.
CHANGELOG's Unreleased now carries two labeled batches (CONTRACT, CONTEXT).
Manifest regenerated same-commit. 0.23.0 tags with both batches.

## 60. The second pre-0.23.0 `/kit-check` — run 2026-08-15 on the CONTEXT batch:
## the pass catches the batch's own §58-class regression a third time running,
## and the retirement rule is redesigned on four of its findings

Full pass, §58's shape: the mechanical four in-session (inv 10 — 40 hashes match
committed content, 40 = ls-files − 1; inv 4 — `{{` in `sdlc-setup.md` only (51),
exit check names its exact scope; inv 6 — 83 refs, multiset byte-identical to the
§58-verified state, zero renumbering (§58's "84" was a case-insensitive count);
inv 9 — all 68 tracked files enumerated, one stale annotation), the eleven
reading passes fanned to seven parallel agents. Clean outright: inv 7 (every
derived mapping statement verified, both classifiers, both denominators), inv 11
(seven vendored files all R100-only since verification; kit-written never
described as vendored; notices exact), inv 3 (census 49, byte-identical across
the commit, 49/49 resolved). Passes with findings: 1, 5, 8, 9, 12, 15. Fails,
fixed: 2, 13, 14.

**The headline (inv 2, blocking):** the retirement bullet's edit replaced the
line it anchored on — `- Trim/align the phase spec…` — without re-emitting it,
leaving phase-end's spec-cleanup step canonical in the template and executed
nowhere. Third consecutive batch caught replacing its own anchor (§55, §58, now
§59's edit); restored. **The design findings (inv 13/14/15, the retirement rule
rebuilt on them):** the "done or dropped" predicate read a marker no step wrote
— the backlog presentation now records each verdict on the entry line (`— done
(<fix commit>)` / `— dropped (owner, <date>)`) and retirement keys on the
marker; Environment gotchas were claimed as a growing section while marked
*bounded* with their own delete-when-fixed rule — dropped from the population,
which now names exactly the two growing record sections; "open items never
move" was an assertion nothing could observe — the step now re-reads what it
moved and pulls back any entry lacking its marker, the visible failure, added
to inv 13's denominator in both homes; the retro's history read was
window-scoped while repeat counts are cross-phase — rescoped to all sections.
**The Records preamble overclaimed** ("every value" — while `{{RUN_COMMAND}}`,
`{{DEPLOY_NOTE}}`, `{{ACCEPTANCE_SURFACE}}`, `{{MAIN_BRANCH}}`, kit version
legitimately live at the steps that use them): scoped honestly in all four
homes (template preamble, CLAUDE row, both transition notes), with the
stay-put values named where they stay. **Inv 1 on the new text:** the "only
trigger" sentence asserted the adopter's CLAUDE.md content — now a
check-and-add step in the same docs commit; the `backlog #N` rationale assumed
numbering the template never produces — softened to any-numbering-preserved;
"installed by /sdlc-setup" (false for updated projects) → "installed at" ×5.
**Pre-existing findings fixed the same session:** six stale "gate section"
pointers → *Records* (setup ×2, GATE_RECIPES ×2, template, end-slice — the
end-slice one a write target aimed at the value-free doctrine section);
"(Phase, START HERE, the gate baseline)" named an index section the template
forbids; the archive bullet's "which already exists" false for STABILIZATION
arcs; REVIEW_LENSES' deletion-path search was the one contract caller with no
absence clause; PROJECT_INDEX's coverage-floor tri-home line not widened for
build-file enforcers; the retro's citation enumeration missing
`spec/PRODUCT_CONTRACT.md`; the mirror homes' 0.23.0 notes diverging on five
facts (aligned, README side); README step-5 enumeration missing the history
file; the tree's "§1–§30" → "§1–§51"; and the inv-12 purity sweep's seven
pre-existing kit-development leaks in shipped files — `kit FEATURE_PLAN`
citations in `tdd-guard-claude.template.py` (×3), `close-out.template.sh`
(×2, incl. the §52.2 arming clock — now "log-only by design on every
install"), `GATE_RECIPES` §50, the "kit's own field bar" clauses (setup,
GATE_RECIPES), and Dungeon Daddy named in SKILLS.md — all converted to plain
field facts per §55's precedent. Sub-threshold, recorded not actioned: setup's
kit-folder SKILLS.md pointer (§58's standing note), the floor comment's
phrasing divergence from its doctrine (substance agrees), sdlc-update's
classifier naming no shell (POSIX assumed — real, larger than this pass), the
2,400-line vs 1,820-line history figures (different snapshots, both real).
One agent finding refuted in triage: extending the deletion-rule search to the
history file — the search's population is the contract and ratifying specs,
which retirement never touches; the template's parenthetical naming it was the
defect and is gone. Proof suites re-run after the two hook-template comment
fixes; manifest regenerated, discrimination proven. 0.23.0 tags with §59 and
this section in the tree.

## 61. PIN opened — the Claude hook-pin finding: `"shell": "bash"` hooks never
## fire on Claude Code 2.1.231, the TFit gate hook was silently inert, and the
## Claude dialect gets the 0.18.0 launcher split — 2026-08-15

Owner-directed 2026-08-15, same day as the finding ("I do want to address any
Claude Code friction in the next kit release"), during the TFit 0.11.0 → 0.23.0
update (their PR #17, merged 0ae7005 with CI green).

### 61.1 The finding, with routes named

Instantiating the 0.23.0 `settings.template.json` on TFit, the new Stop backstop
block never wrote a log line while the guard's Stop block (a shell-neutral
`python …` launcher) fired in the same sessions. Bench-isolated on a scratch repo,
Claude Code 2.1.231, Windows, headless (`claude -p`) route, two probes:

- **Stop:** a `"shell": "bash"` hook wrote nothing; an unpinned twin fired.
- **PostToolUse:** same split — the pinned probe never ran, the unpinned
  `sh -c` twin fired, `shutil.which('sh')` from the hook shell resolved
  `C:\DevelopmentTools\Git\usr\bin\sh.EXE`, and stdin delivered the payload
  (636 bytes measured).

Consequence on the adopter: their edit-time gate hook — pinned `"shell": "bash"`
since adoption, per the then-current template — **had been silently inert**, with
no way to say since when: a pinned hook that never runs produces no error, no log,
and no feedback, which is the 0.16.0 silent-failure shape recurring one layer up,
in the dispatch layer no hook body can see. Their `spec/SDLC.md` hook-environment
note and Kit friction log carry the field record; every TFit hook now runs
launcher-neutral (logic in `.github/hooks/`, bare `sh <script>` / `python
<script>` command lines, no `shell` key), and under that wiring every proof
passed on the real dispatch route — gate framed exit-2 on a deliberate lint
error, ledger line read back from a real `Skill` dispatch, backstop and guard
stop lines from real session stops.

**The contradiction to reconcile honestly:** `reference/GATE_RECIPES.md` records
the pin as *"load-bearing and measured (2026-08-13: the pin holds on `Stop`, runs
Git Bash … delivers the payload on stdin)"*, and the 2026-08-14 deny ramp
exercised that block live. Both statements can be true: the 08-13/08-14 bench ran
the interactive route, the 08-15 bench ran headless — or the CLI moved underneath
(2.1.231 measured on 08-15; the bench version was not recorded, which is itself a
finding for the bench discipline). The batch does not need the tiebreak: the fix
is route-independent, and the recipe's claims get re-stated as two dated
measurements with their routes named (inv 15's form) instead of one
"measured, holds".

### 61.2 The design, pre-registered — the 0.18.0 split, applied to the dialect
### that skipped it

The kit already learned this lesson on the Copilot side (0.18.0: "bare launcher
lines in JSON, logic in script files that never cross the boundary") and the
Claude guard dialect already ships it (`python <file> <mode>`, chosen in §50
"the shell being unknowable"). The gate hook, ledger block, and stop backstop
are the three Claude-side bodies that still depend on the pin. The batch:

1. **`templates/claude-gate.template.sh`** (new) — the gate-hook body, verbatim
   from today's `settings.template.json` command string, carrying
   `{{SOURCE_GLOB}}`, `{{HOOK_LINT_CMD}}`, `{{HOOK_TYPECHECK_BLOCK}}` →
   installed as project-owned `.github/hooks/sdlc-gate-claude.sh`;
   `settings.template.json`'s block becomes the bare launcher
   `sh .github/hooks/sdlc-gate-claude.sh` (`{{HOOK_STATUS_MESSAGE}}` stays in
   the JSON).
2. **`templates/skill-ledger-claude.template.sh`** (new, no placeholders) — the
   ledger body → `.github/hooks/sdlc-skill-ledger.sh`, launcher
   `sh .github/hooks/sdlc-skill-ledger.sh`; same offer/decline handling as
   today (setup removes the block on decline; the script is not installed on a
   decline).
3. **The Stop backstop block** — inline rewrap, no new file (the body takes no
   project values): `sh -c "if [ -d .git ] && [ -f
   .github/hooks/sdlc-close-out.sh ]; then sh .github/hooks/sdlc-close-out.sh
   stop-check; fi"`. Field-proven at TFit in exactly this form.
4. **All three `"shell"` keys deleted** from `settings.template.json`; the proof
   suite pins the launcher lines bare (the 0.18.0 "cannot be silently
   re-cleverified" discipline), and `tools/gate-hook-check.py` reads the Claude
   body from its new template home.
5. **`GATE_RECIPES.md`**: the pin claims at the backstop wiring, the ledger
   Claude paragraph, and the hook-environment section are re-stated as dated
   per-route measurements (08-13/14 interactive-bench, 08-15 headless 2.1.231);
   the hook-environment probe gains the dispatch check — a pinned-vs-unpinned
   probe pair, since a hook that never fires is invisible to every body-level
   probe the recipe has; bench runs record the CLI version from now on.
6. **`sdlc-setup.md`** step 6: instantiate/copy the new script(s) per CLI;
   install-list, README file trees, MANIFEST, THIRD_PARTY_NOTICES untouched
   otherwise; placeholder census moves with the body (inv 4: the three hook
   placeholders' template home changes; GATE_RECIPES documents them — keep in
   step).
7. **`sdlc-update.md` + root README** (mirrored, the two-statement rule): the
   0.24.0 transition note — `.claude/settings.json` is project-owned, so
   existing Claude adoptions get the rewire only by hand: three blocks
   re-wired, two script files arriving, and the plain consequence stated: until
   they land, on any CLI version/route where the pin does not fire, the gate
   hook, ledger, and backstop have never been running. TFit already carries the
   shape (field-proven 2026-08-15); ai-news is Copilot-side and unaffected.

Everything new enters the §16 audit clock, counted in field arcs, as ever.

### 61.3 Owner decisions owed before the build

- **(a) The split shape.** Recommended: script files for the two bodies with
  content (gate, ledger) + inline `sh -c` for the value-free backstop — the
  0.18.0 precedent, and byte-for-byte what TFit now runs. Alternative: inline
  `sh -c` wrapping for all three (no new files, but the gate body carries both
  quote types and the wrap is exactly the "clever quoting" the 0.18.0 suite
  pins against).
- **(b) The interactive-route re-measure.** The 08-13 claim may be
  route-specific. Not blocking (the new wiring works on both measured routes),
  but a two-minute owner-shell check — one interactive session in the bench
  repo with a pinned probe, read the marker — would settle whether the pin
  regressed with a CLI version or never held headless. Recommended: run it
  once before the release notes state the reconciliation.

### 61.4 Rulings and the build — same day: both recommendations approved, the
### batch built, and the proof tool's own decay caught in the doing

Owner rulings 2026-08-15: **(a) the split shape as recommended** (script files for
the gate and ledger bodies, inline `sh -c` for the value-free backstop); **(b) the
interactive re-measure as recommended** — one owner-shell probe run, owed before
the release notes state the reconciliation; the bench sits ready (below).

Built the same day, per §61.2, all seven items: the two new templates
(`claude-gate.template.sh` carrying the three hook placeholders,
`skill-ledger-claude.template.sh` value-free), `settings.template.json` down to
bare launchers with zero `"shell"` keys, GATE_RECIPES re-stated per-route with the
probe's new item 4 (the dispatch check: a pinned-vs-unpinned probe pair, markers
read back, CLI version recorded from now on), setup's per-CLI pair install +
widened exit-check scope, the mirrored 0.24.0 transition notes (update command +
root README, with the 0.22.0 notes' pin sentence pointed forward — the
0.16.0→0.18.0 crossing precedent), COPILOT.md's three mapping rows, both READMEs'
trees (root: two new template rows; bundle: verbatim-copy count 7→8, ownership
sentence naming the new pair), MANIFEST regenerated (42 entries, 42/42 verified,
python-hashed — the Git Bash `*`-prefix trap sidestepped again).

**The build's own catch (inv 13 class):** `tools/gate-hook-check.py`'s Claude
suite read `PostToolUse[0]` — an index 0.21.0's guard blocks silently re-pointed
at the observe-test launcher, so from 0.21.0 until today the suite passed while
driving the wrong block and **the Claude gate hook was unproven** — the software
twin of the field finding (a proof that certifies the wrong artifact is a hook
that never fires, one meta-level up). The suite now locates every block by
matcher, reads the body from the new template home, and pins the bare-launcher
and no-`"shell"`-key properties; run after the change: both dialects green under
both parsers, wiring cases included.

Adopter state: TFit already carries the exact shipped shape (field-proven at
their update — the wiring this batch canonizes); ai-news is Copilot-side and
unaffected. Release: the CHANGELOG entry is written; the tag waits on the owner's
(b) probe and the pre-release `/kit-check`. The probe bench is staged at the
scratch `stopbench` repo — a pinned Stop hook and an unpinned twin, each writing
a marker — and the owner's two-minute part is: open Claude Code interactively in
that directory, send one message, exit, and hand back the marker listing.

### 61.5 The (b) probe run — the pin is dead on the interactive route too, and
### the verdict is version drift, 2026-08-15

The owner delegated the interactive re-measure to the session; it ran as a driven
interactive TUI (winpty `-Xallow-non-tty`, real console, the trust dialog and
welcome screen observed — not headless `-p`). Result: on a real turn's Stop, the
unpinned probe wrote its marker and the pinned probe did not — **and the capture
showed v2.1.233, the CLI having auto-updated between the morning's headless bench
(2.1.231) and the afternoon's interactive one.** So the 2026-08-13 "pin holds"
measurement was version drift, not a route artifact: the pin is dead on both
routes on current versions, and a dispatch behavior the config depended on moved
underneath an auto-updating CLI silently — twice-in-one-day version churn being
its own exhibit for the probe's new record-the-CLI-version rule. All four hedged
homes sharpened to the verdict (GATE_RECIPES ×3 + probe item 4, setup's
fire-proof clause, the update note, the README mirror, the CHANGELOG preamble).
Remaining before the tag: the pre-release `/kit-check`.

### 61.6 The pre-0.24.0 `/kit-check` — run 2026-08-15 on the PIN batch: the
### mechanical four plus eleven reading passes fanned to seven agents; ten
### findings, all fixed in-session, and the theme is §58's a third time with a
### new twist — the batch left its own ledger stale

Mechanical: inv 9 clean (70 tracked, all covered); inv 6 step-ref multiset
byte-identical to the 0.23.0-verified state, semantic read clean (84 refs); inv 4
one FAIL — the 0.24.0 transition note wrote a literal `{{HOOK_ENVIRONMENT}}` into
the installed `sdlc-update.md` (fixed; and the fix was then eaten by a `git stash`
the inv-6 check itself ran and never popped — caught because the census was re-run
after the manifest regen, re-fixed, stash dropped); inv 10 one FAIL — the §61.5
commit edited three bundle files without regenerating the manifest (regenerated;
42/42, discrimination shown on exactly the edited files). Clean outright: inv 1
(the PIN text the best-behaved: every claim dated and versioned), inv 3 (49/49
placeholders, the moved trio's resolver and exit-check both moved with them), inv
5 (377 pointers, 0 dangling), inv 8, inv 9, inv 11 (all seven vendored R100-only).

**Inv 7 FAIL (three findings, one lineage):** the batch updated the bundle README,
COPILOT.md, and the file trees but not the two ownership tables (both homes'
project rows now name `sdlc-gate-claude.sh` and `sdlc-skill-ledger.sh`), the
"unlike its two `.sh` neighbors" claims (three homes reworded — the checker is now
"the one `.sh` the kit owns"), or root CLAUDE.md's flow diagram (Claude column
rebuilt, and its universal `.claude/settings.json` line scoped per-CLI — the
pre-existing note fixed in passing). **Inv 13 FAIL:** the dispatch check is a new
check and the ledger's denominator sentence did not name it — extended in both
homes (ledger + kit-check.md, now "as of 0.24.0"), the invariant's own named
failure mode, caught by its own rule. **Inv 14 FAIL (two):** the probe's new
records had no writer — setup's `{{HOOK_ENVIRONMENT}}` enumeration gains the
dispatch verdict and the CLI version with its source named (the CLI's own version
output), and the template's preamble now names all six record fields; the
`{{SKILL_LEDGER_NOTE}}` comment named half the Claude artifact — now the
block-plus-script pair with the why (launcher without script errors; script
without block never fires). **Inv 12 (one):** the claude-gate template header
named `tools/gate-hook-check.py` — the first kit-repo `tools/` path ever in a
shipped file — converted to the GATE_RECIPES generic form. **Inv 15 (four
minor):** the batch's own routes-and-versions standard applied to its stragglers
(template header now routed, setup's early citation versioned, the 08-14 deny-ramp
entry marked version-unrecorded, the 8-cap likewise). **Inv 2 (one borderline):**
end-phase's CLAUDE.md-row check at retirement had no echo in the canonical
template — one clause added to the retirement bullet. Proof suite re-run OK after
the template-header edit; manifest 42/42 against staged content. The tree is
release-ready pending the tag.

## 62. README built — the §56.3 (e) ruling executed: one template, zero new
## placeholders, and an offer that reads before it writes

Built 2026-08-15, same day as the 0.24.0 release and both adopter updates; the
ruling ("after CONTRACT") was satisfied at 0.23.0. Scope exactly as ruled:
`templates/README.template.md` + New-mode scaffold entry + Existing-mode offer.
The report-§8 measurement is the design bound — links, never a second home for
process truth — so the template carries only Round 1's identity, Round 3's
owner-verified run block, and the three spec links, with the precedence comment
(spec wins; run detail longer than a command belongs in Environment gotchas).

Decisions worth recording:

- **Zero new placeholders** (inv 3 at zero cost): `{{PROJECT_NAME}}`,
  `{{PROJECT_ONE_LINER}}`, `{{RUN_COMMAND}}`, `{{STOP_COMMAND}}` — all already
  interviewed, resolved with the same values as `CLAUDE.md`'s Commands block, the
  stop line deleted under the same rule.
- **The exit check's scope extension is conditional** (inv 4, ledger + root
  CLAUDE.md + setup all restated): `README.md` joins the `{{` grep only when this
  setup instantiated it. A pre-existing README is project prose the check has no
  business scanning — the same scoping logic that keeps the installed
  `sdlc-setup.md` out.
- **The present-README case writes nothing but reads one thing**: the documented
  run command against the one the owner just verified in their own shell. A
  disagreement is an owner finding at the feedback halt — the specimen (a
  documented run command that died at import for the owner while every agent-side
  run passed) is the exact defect class. New check → inv 13's denominator list
  extended in both homes (ledger + `/kit-check`, now "as of 0.25.0") in the same
  batch, per the §61.6 lesson.
- **The instantiated `README.md` is project-owned from the moment it exists**:
  both ownership tables (root README + `sdlc-update.md`, inv 8 mirrored) gain it
  in the project row; the flow diagram and the root file tree carry the template
  (inv 7's §61.6 lesson — trees updated *and* ownership tables, same batch). The
  update classifier is untouched: README.md appears in no pathspec, which is the
  correct shape for a never-classified project file.
- **No update-time offer, by scope discipline**: the ruling named New-mode entry +
  Existing-mode offer only. An already-adopted project without a README reaches
  the template through `sdlc-update.md`'s standing adoption-only rule (raise as a
  manual follow-up where it matters) — no 0.25.0 transition note, because nothing
  arrives by hand and no process loop changed.

MANIFEST 43/43 regenerated same-commit. Unreleased pending the next tag; the
CHANGELOG entry is dated 2026-08-15 — re-date if the release slips.

---

## 63. The seventh and eighth field reports triaged — two adopters, two arcs, ten
## findings, and one class under all three of the high ones: every step verifies that
## an act occurred, and none verifies that a number still holds — 2026-08-17

Both arrived the same day and are ingested verbatim: `FIELD_REPORT_2026-08-17.md`
(the **seventh** — [sdlc-kit#7](https://github.com/ghostpencil/sdlc-kit/issues/7),
the first adopter's Phase 07, BUILD, 7 slices, anonymized copy) and
`FIELD_REPORT_2026-08-17b.md` (the **eighth** —
[sdlc-kit#8](https://github.com/ghostpencil/sdlc-kit/issues/8), the second adopter's
Phase 05, STABILIZATION cleanup, 4 slices, Copilot CLI). Both are written against
**0.24.0**: they are the first two arcs run anywhere under the PIN release, and the
first two under CONTRACT.

Every finding below was verified against the kit tree at HEAD (`0c5f588`, the
unreleased 0.25.0) before this section was written, per §56's discipline. **Line
numbers cited here are the kit's own**, not the adopters' installed copies — the
reports quote the installed files, which is correct for them and not directly usable
here.

**All ten stand.** Three carry corrections, and two of those come out *worse* than
reported: the guard defect exists in both dialects rather than one, and the
contract-adjudication gap is permanent rather than per-arc.

### 63.1 Report seven, finding by finding

**7.1 — the backlog is counted without being reconciled against the arc that closed
it: CONFIRMED, and the two homes are asymmetric.** `commands/end-phase.md:249-255`
matches the report's quotation word for word: the bullet is correct about the
mechanism (record `— done (<fix commit>)` / `— dropped (owner, <date>)` on the
entry's own line) and silent about the population — it says to write a verdict *"as
it is taken"*, and for an entry a slice closed three days ago no verdict is being
taken at that moment. The canonical twin is **thinner and lives in two places**:
`templates/SDLC.template.md:667` carries only *"the backlog surfaced with severity
counts for an owner decision (convert / defer / drop)"*, and the marker rule the
retirement step keys on sits separately in *Bookkeeping rules* at `:709-711`. So a
fix touches three anchors, not two, and the template's phase-end bullet is the one
that currently says least. The half-delivered case the owner raised (their #68) is
real grammar debt: today an entry is `— done`, `— dropped`, or unmarked, and
half-done silently takes the *unmarked* branch, which is indistinguishable from
untouched.

**7.2 — "status only, one line" has no observer: CONFIRMED, and the proposed home
exists.** The rule stands in both places the report names (`commands/end-slice.md`
§9 and the template's *Bookkeeping rules*), and the measurement — 404 index lines
across seven close-outs against a rule that says one, net +225 after both mitigations
fired correctly — is the strongest single number in either report. The fix's cheapest
form is available: `templates/close-out.template.sh` already has a `stop-check` mode
(`:30`, `:44`, `:72`) and an established log-only class, so a docs-diff budget check
has a shipped mechanism to join rather than a new artifact to invent. The second
option the report offers — restate "one line" as a *number* a checker can compare —
is the part that makes the first one possible, and should be decided first.

**7.3 — the guard classifies writes by path and the path class is wrong: CONFIRMED,
and it is BOTH dialects, with Copilot's worse.** Claude:
`templates/tdd-guard-claude.template.py:194-199` is exactly as quoted — a path
outside `ROOT` falls to `else: rel = n`, keeps its absolute form, fails
`TEST_PATH_PATTERN`, matches the extension-only `SOURCE_GLOB`, and is charged as
production source. Copilot: `templates/tdd-guard.template.sh:216-222` never attempts
ROOT-relativization **at all** — it classifies on the normalized full path and the
basename, so the same scratchpad file is production source there too, by a shorter
route. The second adopter did not feel it only because their `SOURCE_GLOB` is
`*.java` and their scratch files are not; that is luck, not scope. The owner's ruling
in the report — *a file outside the repository cannot be production source* — is the
right shape and lands in both templates. **This is not a Claude-dialect fix**, and
treating it as one would repeat the defect §61 was built to stop.

**7.3b — `/end-phase` never mentions the refactor license: CONFIRMED, zero
occurrences.** `grep -ic licen commands/end-phase.md` returns `0`. Step 1 mandates the
`change-verify` pass on the arc, `change-verify` §3 requires driving the thing
through its own front door, and on a real project that means throwaway scripts —
every one of which the guard denies, with no license concept anywhere in the command
that mandated the work. Note the dependency: **if 7.3 lands, most of 7.3b evaporates**
(the scratchpad class is what was being licensed), and what remains is the narrower
question of in-repo verification scripts. Order matters here; do not build both
independently.

**7.4a — `mutation-testing`'s revert step names no mechanism: CONFIRMED, and the file
is VENDORED.** `skills/mutation-testing/SKILL.md:68` is mechanism-free as quoted, and
`:43` (*"revert the mutation before doing anything else"*) has the same shape. The
constraint the report cannot see: `reference/SKILLS.md:116-121` records this file as
an MIT-licensed condensed derivative of an upstream repo — so editing it **diverges
it from upstream and invariant 3 requires the divergence be recorded in
`reference/SKILLS.md` in the same batch**, not silently. Four working-tree
corruptions in one arc, all from `write_text(read_text())` on Windows, is ample
justification; the bookkeeping is what must not be forgotten.

**7.4b — the skill was never dispatched: ACCEPTED as reported, not independently
verifiable here.** The evidence is the adopter's own ledger (33 activations in the
window, siblings recording faithfully, `mutation-testing` at zero) against ~100
mutations actually run. That is as strong as a negative gets and it is theirs to
measure, not this repo's. The kit-side fact is confirmed:
`commands/end-slice.md:162-163` names the skill in prose and nothing observes whether
it ran. The report's own framing is the right decision to put — **is this a skill to
dispatch or a recipe to inline?** — and it interacts with 7.4a: if the byte-safe
revert is what matters, inlining the recipe delivers it without depending on
relevance-based activation.

**7.5 — RED has no shape for a characterization slice: CONFIRMED.**
`commands/next-slice.md:115-120` is quoted exactly, and `commands/end-slice.md` step
5's mutation trigger is scoped to *"every new guard, branch, or error path this slice
added"* — which a characterization slice also has none of. So both steps point away
from the one check that carries signal, and the arc's highest-risk slice (129 tests
pinning the module that guards a non-regenerable database) recorded the same evidence
class a README edit would. The report's fix names both anchors correctly.

**7.6 — `change-verify` records the environment without constraining it: CONFIRMED,
including the ordering.** §3 (*"Reach it the way something real does"*) precedes §5
(*"Record the environment the result came from"*), so the only environment step is
post-hoc, exactly as reported. The specimen — a verification run minting a live OAuth
token and reading the real calendar because the data dir was redirected and the
credentials were not — is the same half-built-isolation defect that adopter had
already solved for its test suite in July. `change-verify` is **kit-written**
(invariant 3), so this edit carries no provenance cost.

**7.7 — the Records table drifted again: CONFIRMED as a class, PREMISE CORRECTED.**
The kit ships **no test-count row**. `{{GATE_BASELINE}}` is resolved by
`commands/sdlc-setup.md:211` and `:677-684` as a *failure-count* line (`green — 0
lint / 0 type / 0 test failures (measured <date>, <shell>)`), and
`templates/SDLC.template.md:136` is its single home. The drifted `676 tests` row is
the adopter's own elaboration of that record. **This makes the finding stronger, not
weaker**: the kit invites projects to write numbers into *Records* and then supplies
row-by-row reconcile procedures naming only the rows it shipped (the coverage floor
at `commands/end-phase.md:281`, the red baseline in step 6), so any row an adoption
adds is structurally unreconciled from birth. The report's fix — reconcile the *whole*
table against a fresh measurement rather than two named rows — is the only form that
covers rows the kit never authored.

### 63.2 Report eight, finding by finding

**8.1 — ratified-but-absent behaviors have no adjudication step: CONFIRMED, and the
mechanism is worse than reported. This is §56's unbuilt half, now field-measured.**
The backfill bullet at `commands/end-phase.md:275-281` walks prior ratified decisions
and enters *"only what they confirm as still-current, never an inference"* — one
direction only, exactly as reported. Two facts sharpen it:

1. **The backfill is one-time.** It is offered at the first close after adoption and a
   decline is recorded so it is never re-made. A behavior omitted from that single
   pass is therefore invisible **permanently** — no later step re-walks prior phase
   specs.
2. **The preserved-contract check cannot cover the gap**, because its population is
   (entries already in the contract) × (surfaces this arc touched) —
   `commands/end-phase.md:144-160` and `templates/SDLC.template.md:626-632`. A
   behavior that never became an entry is outside both factors.

So the erosion path §56 diagnosed ("a fix must sit where both paths pass through:
phase planning and phase close") got its **storage** in CONTRACT and never got its
**adjudication**, and the first arc to run the backfill demonstrated precisely that:
the draft omitted P01 D6/D22/D23, the owner confirmed the draft, and only a
co-development read of `FIELD_REPORT_2026-08-15.md` — a kit document no adopter
process reads — stopped ratification-by-omission. Owner ruling in-report: restore.
This is the highest-value finding in either report and the one with the longest paper
trail.

**8.2 — the test-command matcher fires on any command text mentioning the runner:
CONFIRMED, and it is not Java-specific.** `reference/GATE_RECIPES.md:407` is exactly
`*mvn*test*|*gradlew*test*`, instantiated at `templates/tdd-guard.template.sh:271` as
`{{TEST_CMD_PATTERN}}) ;;` — substring-anywhere against the whole command string.
**Every row of that table has the same shape, including the default `*pytest*` at
`:44`**, so a `git commit -m` whose body quotes the RED command counts as a test run
on any stack, not just Java. Three spurious notices in one phase is the measured cost;
the real cost is message fatigue against a control whose refusals must be believed.
The fix (anchor to the first token, or strip quoted-string content before matching)
belongs in the recipe table and in both guard templates.

**8.3 — acceptance items can be unexercisable live: CONFIRMED, and the sweep's own
escape hatch creates the class.** `commands/plan-phase.md:122-126` requires every
behavior to be *"pinnable by a deterministic test, **or explicitly assigned to the
acceptance-review checklist**"* — and that assignment is **terminal**. Nothing
downstream asks how an assigned item is reached by a real caller; `:172-175` then
cites the sweep as the check that exit criteria have an observer, which closes the
loop on paper. The specimen (a malformed-feed-item behavior with no fixture seam,
which passed on three adapter pins plus an owner ruling and was honestly reported
"not exercised live" at halt 3) is the escape hatch working as written. The fix is one
line at the point of assignment: name the path a real caller reaches it by, or flag it
test-only **at plan time**, not at the halt.

### 63.3 The convergence — two classes, not ten findings

**Class A: no step re-derives a recorded number.** 7.1 (the backlog said 101 when at
least one entry was shipped and deployed), 7.7 (the baseline said 676 when the suite
was 678), 7.2 (the rule said one line when the arc wrote fifty-eight), and 8.1 (the
contract said current when three ratified behaviors were absent) are all one defect.
The seventh report names it exactly: *every step in the kit verifies that an act
occurred — was the test watched to fail, was the guard mutated, did the reviewer
return — and no step verifies that a count still holds.* The lineage supports it: the
kit has patched this class **four** times, always one row at a time and always after
the damage — the coverage-floor reconcile (2026-07-22), the type-ceiling procedure
(0.9.0), the marker-keyed retirement (0.23.0, which this arc promptly starved of
markers), and CONTRACT's storage (0.23.0, whose first run is 8.1). A fifth row-shaped
patch is the wrong answer; the shape that fits is **one reconcile pass at phase close
whose subject is every recorded number and every carried claim, reported as
recorded-vs-measured, before the owner is asked to decide anything on the strength of
one.**

**Class B: the guard's classifiers match text, not the artifact.** 7.3 (a path string
that is not a repo path is treated as one) and 8.2 (command text that merely mentions
the runner is treated as a run) are the same error twice, in the two classifiers that
decide when the guard speaks. Both are S-effort, both land in both dialects, and both
directly reduce the false-positive load that trains operators to route around the
control. This is the cheapest real safety win in either report.

The remainder (7.4a/b, 7.5, 7.6, 8.3) are independent single-anchor fixes, each with a
named home and a specimen.

### 63.4 What these two arcs say about machinery already on the clock

The arcs are field evidence against the standing clocks; each of these is an owner
ruling, not a fact this section settles.

- **PIN (0.24.0) — held.** The first adopter's guard log carries 656 lines across the
  window and the second reports the edit-time hook running all phase. No inert-hook
  symptom in either report. The launcher-neutral rewiring works in the field.
- **The three STD lenses (`logging and swallowed errors`, `untrusted input`, `secrets
  and exposure`) — arc one of two, no catch.** The seventh report's only lens-named
  catch is `unconsumed artifact` (it found a `close()` with no production consumer),
  which is **not one of the three on the clock**. The eighth report's evidence table
  has **no lens row at all**, so whether that arc counts toward the denominator is a
  ruling owed. On the strict reading the clock is at 1 of 2 with zero catches, and one
  more clean arc deletes all three with their conventions' enforcement lines
  re-pointed in the same batch.
- **`change-simplify` — catches on both arcs.** 12 moves applied on the first (10 more
  proposed and dropped with reasons), 6 on the second across three slices. Whether
  "moves applied" clears a clock worded as *one confirmed catch in the next two field
  arcs* is the ruling owed; the §53 redirect's founding miss was a duplicated test
  helper, and the second adopter's `diff-review` — not `change-simplify` — is again
  what caught a test-helper defect this arc (S1's `LogCaptor` level-restore
  narrowing). That is the same division of labour the redirect was built to end, and
  it argues for reading the moves conservatively.
- **CONTRACT — first arc under it, and its pre-registered value criterion was NOT met
  by the mechanism.** §57.5/§56.2 pre-registered: *seeding the adopter's contract must
  surface P01's D6/D22/D23 as scheduled work or explicit owner retirement.* They were
  surfaced — by a human reading the kit's own field report mid-close, against a draft
  that had omitted them. The mechanism produced the draft that omitted them. The
  honest reading is that the criterion failed on its first arc **and named its own
  repair** (8.1), which is a better outcome than a silent pass; the ruling owed is
  whether that counts as the clock's first arc spent or as a defect to fix before the
  clock starts.
- **R3.8's aging rule — still unexercised, but no longer starved on both sides.** The
  first adopter closed the arc with 3 friction entries left open; those are the first
  that can age past one phase, so the carry rule finally has a population coming.
- **The bare-flagging arming bar (§52.2)** — needs the false-candidate count from both
  arcs' close-out logs, which neither report states. Unresolved; ask before arming.

### 63.5 Decisions owed

1. **Sequencing — RULED 2026-08-17: fold Class B into 0.25.0.** The release carries
   the README batch (§62) plus CLASSIFY; `/kit-check` runs on the combined scope before
   the tag.
2. **Batch shape — RULED 2026-08-17: RECON + CLASSIFY + independents**, as proposed.
   **CLASSIFY** (Class B — 7.3, 8.2, with 7.3b resolved as a consequence rather than
   built) is built: §64. **RECON** (Class A — 7.1, 7.2, 7.7, 8.1 — one reconcile pass
   at phase close plus the half-done marker grammar and the contract's absent-behavior
   direction) is next and unopened. The four independents (7.4a+b, 7.5, 7.6, 8.3)
   follow, distributed by effort.
3. **7.4b's question** — dispatch or inline — must be answered before 7.4a is built,
   because inlining a byte-safe recipe into `end-slice.md` and editing the vendored
   skill are alternative deliveries of the same fix, and only one of them incurs the
   invariant-3 divergence note.
4. **The clock rulings in 63.4**, each on its own evidence.

---

## 64. CLASSIFY built — the guard's two classifiers stop matching text and start
## matching the artifact: out-of-repo writes, and runners named inside quotes

Owner-ruled 2026-08-17 at the §63.5 halt: Class B folds into 0.25.0 beside the README
batch; RECON and the four independents follow. Built the same day. Both fixes land in
**both dialects** — the §61 version-and-route standard, and §63.1 measured that the
Copilot dialect had the path defect too, by a shorter route than the Claude one.
⚠️ **The out-of-repo half of the Copilot fix did not actually work in the field** and
was repaired at 0.28.1 — see the correction at the end of this section and §72.

**(a) A file outside the repository is not production source.** Claude
(`tdd-guard-claude.template.py`): the `else: rel = n` fall-through becomes a
containment test — an **absolute** path not under `ROOT` logs and exits 0. Copilot
(`tdd-guard.template.sh`): the dialect never attempted the reduction at all, so it
gains one — lowercased prefix compare (Windows hands back either case), `cut` to the
relative form, and the same skip for an absolute path outside.

**(b) The test-command pattern is matched with quoted arguments stripped.** One line
in each dialect (`re.sub` / `sed -e 's/"[^"]*"/ /g' -e "s/'[^']*'/ /g"`), matching on
the stripped probe while every message still quotes the real command.

Decisions worth recording:

- **Quote-stripping was chosen over the report's other option, first-token
  anchoring** — both were offered in `FIELD_REPORT_2026-08-17b.md` finding 2. Anchoring
  means rewriting the pattern grammar (`*mvn*test*` → something that spans a first
  token and a later word), which invalidates **every instantiated guard already in the
  field**: those files are project-owned and never rewritten by an update, so the
  pattern an adopter holds would have to be hand-edited before the guard worked at
  all. Stripping leaves the table's substring shape exactly as written, needs no
  pattern change anywhere, and states the same idea more directly: quoted text is
  data, never what the shell runs. It is also the same sentence as fix (a) — match
  the artifact, not the text — which is what made them one batch.
- **The known cost is documented rather than hidden**, in both guards, the recipe, and
  both transition notes: a runner reachable **only** inside a quoted argument
  (`bash -c "pytest"`) no longer counts. It is a real regression in coverage and it is
  small, because the compound-command rule already requires bare invocations.
- **The compound check deliberately still reads the RAW command.** Feeding it the
  stripped probe would be more precise (a quoted `;` inside a `-k` expression is not a
  compound), but a stripping bug there would admit a genuine compound and record a
  **false GREEN** — the exact hazard that rule exists for. Precision on the deny side,
  conservatism on the counting side; the direction is stated in both guards' comments
  so a later session does not "fix" it.
- **Relative paths stay in scope, and that is a containment test rather than a bare
  else.** A relative path can only be relative to the root the guard resolved, so
  skipping it would open a hole in the guard while wearing the costume of a scoping
  fix. Both suites pin it, and one of the six new mutations is exactly that mistake.
- **7.3b (`/end-phase` never mentions the refactor license) is resolved as a
  consequence, not built** — per §63.5's ruling and §63.1's dependency note. The
  scratchpad class *was* the 12 licensed writes; with (a) in, a mandated
  `change-verify` pass that drives the app through throwaway scripts needs no license
  at all. **The residue, recorded so it is not lost:** an in-repo verification script
  (a fixture, a seeded harness committed under the repo) is still a production write
  under an `/end-phase` step that mentions no license. That is a RECON-adjacent
  question about what `/end-phase` step 1 owes the operator, and it is deliberately
  left open rather than half-answered here.

**An extra catch the fix produced, not predicted by either report.** Reducing the path
in the shell dialect closed a live misclassification: an absolute path to a test file
whose **basename** does not look like a test — `tests/conftest.py` is the specimen —
matched neither `TEST_PATH_PATTERN` form (`tests/*` cannot match a full Windows path;
the basename matches no `test_*.py`/`*_test.py`) and fell through to the
extension-only `SOURCE_GLOB`. So a **test** edit was charged as a production write and
licensed nothing. Pinned as its own case (`2d`) and its own mutation. Adopters on that
dialect may have friction already logged that this release explains, which is why the
transition note says so at the halt rather than only in the changelog.

**Proof coverage — six new mutations, and every fix has its negative case.** The rule
this repo holds itself to is that a suite surviving its own mutations is not testing
what it claims (invariant 13), so each fix ships with the mistake that would undo it:

| Dialect | New cases | New mutations |
|---|---|---|
| Claude (`tools/tdd-guard-claude-check.py`) | `3b` out-of-repo not production, `3c` not denied when armed, `3d` relative still in scope, `7c` quoted-only counts nothing, `7d` quoted argument still counts | charge out-of-repo as production; skip relative paths (the hole); match the raw command text |
| Copilot (`tools/tdd-guard-check.py`) | `2b` out-of-repo not production, `2c` absolute-inside still production, `2d` `tests/conftest.py` is a test edit, `5c` quoted-only counts nothing, `5d` quoted argument still counts | drop the out-of-repo skip; drop the reduction (the `conftest.py` regression); match the raw command text |

⚠️ **Corrected 2026-08-27 (§72): the Copilot row above overstates what was proven.**
Its `2c` case — *absolute-inside still production* — passed on a body where the
reduction was broken, because the bench **pins** `SDLC_REPO_ROOT` to its own root, so
both sides of the comparison agreed by construction. No adopter sets that variable.
The shell dialect's out-of-repo classifier therefore **never worked in the
configuration adopters actually run**, from 0.25.0 until the 0.28.1 fix; the Claude
dialect's did, and still does. Read the table as *the Claude fix was proven; the
Copilot fix was proven only against a fixture that could not fail.* §72 has the
measurement and the repair (cases `24b`/`24c`, run with the variable unset).

Both suites green, both dialects, unit and mutation passes, **measured not assumed**:
the shell suite reports 110 unit cases (55 × two parser dialects), 0 failures, **20
mutations, 20 caught, 0 survivors, 0 stale**; the Claude suite likewise, with each of
its three new mutations caught by the case written for it. The Claude suite runs in
seconds; **the shell suite takes ~35 minutes on this machine** — every case spawns
`sh`, measured at ~1.5–2 s per spawn under Windows, across 22 suite runs (2 parser
dialects + 20 mutations). That is not a hang, and a 120-second tool timeout reads
exactly like one; run it in the background and let it finish.

**Homes touched beyond the two guards:** `reference/GATE_RECIPES.md` (both rules
beneath the pattern table, each with its measured specimen and its stated cost);
`commands/sdlc-setup.md` (the guard note's rule list goes from three to four — scope
is a user-visible rule, and the note exists precisely to state the rules proactively
rather than let a session meet them as an unexplained refusal); `commands/sdlc-update.md`
and the root README (the 0.25.0 transition note, mirrored — the instantiated guard is
project-owned, so neither fix arrives by updating); `CHANGELOG.md` (0.25.0 restructured as two
batches and re-dated **twice** under §62's re-date instruction — 2026-08-15 →
2026-08-17 when CLASSIFY joined the release, then → **2026-08-18**, the day the tag
actually went out; the build dates in this section and §65 are 2026-08-17 and stay
that way, because they record when the work happened, not when it shipped).

---

## 65. The pre-0.25.0 `/kit-check` — run 2026-08-17 on the combined README+CLASSIFY
## scope: two findings, both fixed in-session, and both are the batch's own derived
## statements going stale for the fourth pass running

Scope, stated because a scoped run must say what it skipped: the **full** mechanical
set (invariants 4, 6, 9, 10) plus reading passes over this release's two batches —
§62's README work, which shipped after the last pass and had never been checked, and
§64's CLASSIFY — and over every statement derived from them. The full-corpus reading
of invariants 1, 2, 14 and 15 across all seven commands and every template is carried
forward from the pre-0.24.0 pass (§61.6); nothing in this release touched the process
steps those passes read.

**Mechanical results, with denominators rather than "matches":** `{{` census — hits in
`sdlc-setup.md` only (53), and setup's close-out check names `CLAUDE.md spec/
.claude/settings.json` plus the conditional `README.md`, the conditional gate-hook
script, and the accepted guard dialects. Step references — 88 across `commands/`, none
renumbered by either batch (both edits landed inside existing steps). README tree — 71
tracked files, every one present, the two new field reports added, no tree entry
without a file. Manifest — 43 entries against 43 tracked bundle files minus the
manifest, every hash matching **index** content, no missing and no extra.

### The two findings

**1 — `SDLC.template.md`'s guard-note comment still said "the three rules"
(invariant 2).** CLASSIFY gave the guards a fourth user-visible rule (a file outside
the repository is not production source) and taught `sdlc-setup.md` to write it into
`{{TDD_GUARD_NOTE}}` — and left the template's comment, which is the *canonical*
specification of what that note must contain, enumerating three. The template wins on
disagreement, so for the duration of the batch the kit's canonical file and its setup
command contradicted each other about how many rules the guard imposes. Fixed: four,
with the scope rule written into the enumeration in the same words setup uses.

**2 — `sdlc-kit-process-flow.md` described both classifiers in their pre-0.25.0 form
(invariant 1, derived-statement half).** The root walkthrough's G1 bullet defined a
production-source write without the containment test, and its observe-test bullet
described the matcher without the quote-stripping. Not a shipped file, and exactly the
kind of derived statement §61.6 made a standing check. Fixed: both bullets carry the
new behavior with its release stamp.

**Both findings are the same defect, and it is the fourth consecutive pass to find
it** — §55, §58, §60 and §61.6 each caught a batch leaving its own derived statements
stale, and §58's was the sharpest (the batch's own edit decapitated the coverage-floor
bullet). The pattern is now stable enough to name as a rule rather than a recurring
surprise: **a batch that changes a behavior must enumerate every file that describes
that behavior before it enumerates the files that implement it.** CLASSIFY's edit map
was derived mechanically for the *implementing* files (§4a, and it found the second
dialect that way) and by memory for the *describing* ones — which is precisely where
both findings landed.

### Passes worth recording with what they looked for

- **Invariant 8** — the two 0.25.0 transition notes (`sdlc-update.md` and the root
  README's *Updating an adopted project*) agree claim for claim: both fixes named,
  both template files named, `.json` launchers unchanged in both, the shell dialect's
  `tests/conftest.py` consequence in both, the `guard.log` confirmation step in both,
  the relative-path caveat in both. The violation looked for was the one the
  invariant was created for — a note stated in one home and not the other.
- **Invariant 13** — both denominator homes (ledger and `/kit-check`) carry the same
  21 items, both stamped "as of 0.25.0". CLASSIFY adds **no new check**: it fixes two
  classifiers inside an already-enumerated one (the TDD-guard proof step), whose
  suites gained six mutations. The violation looked for was a check added without
  being added to the list — the failure mode this invariant says goes stale silently.
- **Invariant 10** — the manifest matched the index, which is the trap rather than the
  all-clear: six bundle files are edited in the working tree, so the manifest is stale
  the moment they are committed. Regeneration from index content is a release step
  below, and the release workflow *verifies* rather than regenerates — a stale manifest
  fails the tag push after the tag is public.
- **Invariant 11** — no `skills/` file touched, so both provenance regimes are
  untouched. Recorded forward because it will not stay true: **7.4a proposes editing
  `mutation-testing/SKILL.md`, which `reference/SKILLS.md:116-121` records as an MIT
  condensed derivative.** That edit diverges it from upstream and the divergence must
  be recorded in `reference/SKILLS.md` in the same batch — or the alternative delivery
  (inline the byte-safe recipe into `end-slice.md`) avoids the provenance cost
  entirely, which is §63.5's decision 3 and why it must be answered first.

## 66. IMPACT opened — the §56.3 (d) hold resolved: the owner's visualization spec
## arrives and is triaged; a deterministic impact adapter for Understand Anything,
## proposed not built — 2026-08-18

§56.3 (d) held the owner-comprehension visualization until after the improvement
batches, "then gets its own triage against whatever that file actually says." The
file arrived 2026-08-18 (`FEATURE_OWNER_CHANGE_IMPACT_VISUALIZATION.md`) and is
ingested verbatim at the root as `FEATURE_SPEC_IMPACT.md` — the field-report
convention: the source document is never edited; this section records the triage
and the deltas. The design below is proposed, not built: the owner rules on 66.7
before anything is written into the kit (§37.7's rule). The report-§11 constraints
bind throughout, and the spec's own §25 restates them — five halts and no sixth,
context minimization per slice, no second source of truth, TDD and gate semantics
untouched.

### 66.1 What the spec proposes, and what stands as proposed

One kit-owned adapter (`sdlc-impact`) that derives, mechanically, the architecture
footprint of a slice or phase: git change set → Understand Anything knowledge
graph → changed nodes → one-hop affected nodes → UA's own `diff-overlay.json`,
plus a compact printed summary (`SDLC IMPACT: COMPLETE | PARTIAL | UNAVAILABLE |
ERROR`) that the daily commands quote at surfaces that already exist — the
slice-ready hand-back, the end-slice hand-back, and `/end-phase`'s acceptance and
merge hand-backs. A comprehension aid for the owner, explicitly not verification;
nothing about it enters gate truth.

Triaged against the kit's own lineage, the spec's core is sound in exactly the
places the field reports punish:

- **Deterministic selection** (spec §4.2, §6) — the adapter computes the overlay;
  the model only quotes it. No LLM decides what belongs in the picture.
- **Loud incompleteness with denominators** (spec §4.4, §12) — changed / mapped /
  unmatched counts printed together; the second report's lesson applied correctly.
- **The four-state taxonomy** satisfies inv 13, and "a check that cannot run must
  not appear to have passed" is the spec's own §14.
- **No new halt, runtime discovery, no placeholders** (spec §4.5, §19) — inv 1, 3
  and 4 untouched; ships verbatim like the close-out checker.
- **Trial-first with a pre-registered failure criterion** (spec §24) — the §16
  regime, arriving already in the kit's grammar.
- **No provider abstraction before a second provider exists** (spec §18) — §37.6's
  restraint, self-applied.

### 66.2 The triage — eight findings, adopted as deltas to the spec

Two are blockers, six are corrections. The spec file stays verbatim; these deltas
are the build's authority wherever they and the spec disagree.

**(a) BLOCKER — the schema contract is asserted, not verified.** The spec asserts
the graph location, node `filePath`, `edge.source`/`edge.target`, layer and
freshness metadata, the overlay schema, and the dashboard's read path — and
Understand Anything exists nowhere findable on this machine (searched 2026-08-18:
the course tree to depth four, the common dev directories, both drive roots).
CLASSIFY (§64) is one release old and its whole lesson is that a checker matches
the artifact, not the prose describing it. The adapter's read path is not frozen
until a real `knowledge-graph.json` and one observed dashboard read of a
`diff-overlay.json` have been inspected; the proof fixtures derive from that real
artifact, never invented. The owner has offered to install Understand Anything
(2026-08-18) — ruling (b) names what the build needs from that.

**(b) BLOCKER — the trial population is currently empty.** Spec §24's own bar: "a
trial that only proves the integration is safe is insufficient." Neither adopter
carries a `.ua/` graph today; without a designated project the feature ships inert
in every adopter and its clock starts with zero possible catches — the SIMP
precedent argues against shipping that. Resolved by ruling (c).

**(c) The overlay write collides with the kit's clean-tree rules.** `/end-phase`
step 1 requires a clean tree and step 5 re-asserts it as load-bearing; writing
`<UA_DIR>/diff-overlay.json` between the gate and the merge dirties the tree at
exactly the checked moments unless the UA directory is git-ignored. The spec says
"respect ignored files" but never handles this interaction. Delta: the adapter
runs `git check-ignore` on the UA directory first; not ignored → the summary still
prints but the overlay is not written, stated explicitly (`overlay: not written —
.ua/ is not git-ignored`). The same path rule excludes UA's own files from the
changed-file denominator mechanically (spec §7.2 asks for the exclusion; the delta
names the mechanism).

**(d) One verbatim script, no dialect fork.** The adapter is command-invoked, not
a hook — the PIN class (§61) never applies. One stdlib-only Python file, shipped
verbatim with zero placeholders, launched shell-neutrally (`python`, the same
rationale the settings template records for the guard launchers). The real cost is
the install surface (66.5), which is the strongest argument for exactly one file.

**(e) Slice-base capture is conditional, worktree-safe, and self-checking.** Spec
§7.1 captures unconditionally; delta: `/next-slice` records the base only when a
UA graph is detected, so the footprint is exactly zero for a non-UA adopter — a
stronger reading of the spec's own §4.1, at the honest cost that a graph installed
mid-slice waits one slice. The path comes from `git rev-parse --git-dir`, never a
literal `.git/` (worktrees), and the record is branch name + SHA, so a base
recorded on a different branch is detectably the "ambiguous or stale" case the
spec's §8.3 requires to fail loudly.

**(f) A missing interpreter is UNAVAILABLE, not ERROR.** Spec §21 records ERROR as
kit friction; an adopter without a `python` launcher is absence of an optional
capability's environment, not adapter failure. The message names the environment
(inv 15's grammar). Only a crash given a readable graph and a working interpreter
is ERROR.

**(g) Freshness is v1-simplified.** Spec §13's monorepo distinction needs a
project path scope nothing in the contract supplies. v1: graph metadata carries a
build commit → diff it against the slice/phase base and report `may be stale — N
project files changed since graph commit`; no metadata → `freshness unknown —
<reason>`. The monorepo refinement waits for a monorepo adopter — spec §18's
restraint applied to its own §13.

**(h) End-slice ordering, and the checker's key set is untouched.** The final
regeneration runs after the slice commit and the record check (steps 7–8), lands
in the step-10 hand-back beside the changed-from-preview statement, and clears the
slice base in the same pass. The impact summary never enters the commit body's
evidence keys — it is explicitly not evidence, and the close-out checker's
denominator does not change.

### 66.3 The adapter

`templates/sdlc-impact.template.py` → installed verbatim (ruling (d) of 66.7 names
the path). Modes `slice` and `phase <base-ref>`; stdlib only. Responsibilities, in
order: resolve the UA directory (legacy `.understand-anything/` when present, else
`.ua/`); establish the change set (committed since base + staged + unstaged +
untracked non-ignored, UA directory excluded by path); map changed files to every
node carrying them; one hop through edges, deduplicated, changed nodes never
re-listed as affected (spec §23's cases 5–7); layer report where the graph carries
membership; unmatched files listed with the full denominator; v1 freshness per
(g); overlay written behind the check-ignore guard per (c); the spec-§15 output
contract printed last. The dashboard is never launched (spec §16).

### 66.4 The touchpoints — existing steps, existing hand-backs

`SDLC.template.md` gains one short *Architecture impact view (optional)* section —
the canonical statement (inv 2), with three command mirrors as its automation,
each a few lines that run the adapter and quote its printed output rather than
restating its behavior:

1. **`/next-slice`** — step 3, after branch preparation: if a UA graph is
   detected, record branch + SHA per (e). Step 5: run `slice` mode; the summary
   joins the slice-ready hand-back, absence stated when absent (spec §4.1's
   non-silent rule).
2. **`/end-slice`** — after steps 7–8 per (h): regenerate, state whether the
   footprint changed from the preview, clear the base, report in step 10.
3. **`/end-phase`** — after step 2: run `phase <main>` (the branch the project's
   own records name — never assumed); the summary joins the acceptance hand-back.
   After step 5's fix commits: regenerate before the merge halt, any
   post-acceptance footprint change stated. No new halt anywhere — spec §4.5 and
   the five-halt constraint hold.

### 66.5 Cost named up front

Files: new `templates/sdlc-impact.template.py`; new `tools/impact-check.py` (every
shipped script artifact has its proof; fixtures derived per 66.2 (a), covering
spec §23's thirteen negative cases plus (c)'s not-ignored case and (e)'s
wrong-branch case); `SDLC.template.md` + the three command mirrors;
`sdlc-setup.md` New-mode step 5 (the inv 7 single source — install unconditional
and verbatim, inert without a graph, like the close-out checker) and the
Existing-mode column; `sdlc-update.md` + the root README's update section (inv 8,
same note both homes); `reference/COPILOT.md` mapping row; both README trees
(inv 9); `CHANGELOG.md`; `VERSION`; manifest regenerated same-commit with
discrimination proven (inv 10 — the text-mode trap is on record). The adapter's
proof joins inv 13's denominator in ledger and `/kit-check` copy in the same
batch. And per the §65 rule — the describing files are enumerated before the
implementing ones — the derived-statement sweep at build time covers
`sdlc-kit-process-flow.md` and both READMEs' prose, not only the trees.

### 66.6 Value criterion, pre-registered — spec §24 adopted with the kit's
### denominator

Hypothesis (spec §24): a deterministic visual map of changed and graph-connected
components lets the owner understand and challenge AI-generated work with less
line-level inspection. Evidence collected per arc, in the retro/field-report
channel that already exists: did the owner open the dashboard; did the view cause
a question that would not otherwise have been asked; did it surface an unexpected
subsystem; unmatched-file and staleness rates; generation friction; any ERROR
state (kit friction per spec §21, R4.6's writer). **The clock: across the next
two field arcs run with a usable graph, at least one owner-reported comprehension
event — a question asked, a surprise surfaced, or an owner-stated faster read of
the change. None → the integration is a deletion candidate like any rule; spec
§24's own failure criterion, in the §16 grammar. An arc without a usable graph
cannot exercise the feature and does not count against it.**

### 66.7 Owner decisions owed before the build

All five ruled 2026-08-18, each as recommended:

- **(a) Queue position — RULED: RECON first, IMPACT immediately after.** §63.5's
  ruling stands un-re-ruled; IMPACT's owner-side blockers resolved in parallel
  (see (b) and (c)) and the build slots in behind RECON's.
- **(b) The real artifact — RULED: adopted as stated. SATISFIED 2026-08-19.**
  At ruling time `TFit-Foundation/.ua/knowledge-graph.json` existed and was
  verified against the tree (with `config.json`, `fingerprints.json`,
  `meta.json` beside it); the next day the owner ran `/understand-diff` (UA
  plugin 2.9.4), it wrote `.ua/diff-overlay.json` (base `main`, 11 changed
  files, 8 changed nodes, ~80 one-hop affected), and the owner confirmed the
  dashboard rendered it. The overlay matches the spec's schema field-for-field.
  The adapter's read path is frozen against that observed pair, snapshotted
  with provenance in the git-ignored `impact-fixture-source/` (adopter
  internals — never committed; build-time fixtures derive from it, minimized).
  The real instance carries the build's best test case: seven changed files
  (incl. `usage_pricing.py`, new tests, `.claude/settings.json`) have no
  matching node because the graph predates them — spec responsibilities 6
  (unmatched files) and 7 (freshness) observed in the wild, not invented.
  This was blocker 66.2 (a)'s only exit.
- **(c) Trial project — RULED: TFit-Foundation.** Its graph already sits on
  disk, so the trial costs no new graph generation; ai-news-dashboard (Copilot
  CLI) joins later only if the owner elects to pay for a second graph.
- **(d) Install path — RULED: `.github/hooks/sdlc-impact.py`.** The directory
  is already the kit's script home in adopter repos despite its name; a new
  directory would widen every mapping for no gain.
- **(e) The eight deltas of 66.2 — RULED: adopted.** They are the build's
  authority wherever they and `FEATURE_SPEC_IMPACT.md` disagree.

What still gates the build, post-rulings: RECON ships first (a) — nothing else.
The `diff-overlay.json` observed read landed 2026-08-19; (b) is fully satisfied
and every other decision is taken.

---

## 67. RECON opened — one reconcile pass at phase close: every recorded number and
## carried claim, recorded-vs-measured, before any owner decision reads one

Opened 2026-08-19 per §63.5's ruling (RECON next) and §66.7 (a) (IMPACT builds
immediately after). Scope is Class A — findings 7.1, 7.2, 7.7, 8.1 — plus the two
riders §63.5 named with it: the half-done marker grammar and the contract's
absent-behavior direction. §63.3's diagnosis is the design's spine: the kit has
patched this class four times, always one row at a time, always after the damage;
the fifth patch must be the pass, not another row.

### 67.1 The reconcile pass (7.1 + 7.7 + 8.1's per-close direction)

A new opening bullet for `/end-phase` step 7 (post-merge bookkeeping), run **before
any bullet that asks the owner anything**: re-derive every recorded number and
carried claim from the tree and this close's own gate evidence, and report each as
`recorded X / measured Y` — divergences first, agreements collapsed to one line.
Its subjects, in order:

1. **The backlog, reconciled before it is counted.** Walk this arc's slice commits
   and the phase spec; mark `— done (<commit>)` on every entry they closed; only
   then report the open count, stating how many the pass itself just closed. The
   convert/defer/drop question is asked of the *reconciled* number. (Report 7's fix
   verbatim — the count describes the future instead of mixing it with the past.)
2. **The whole Records table, not two named rows.** Every row the table holds —
   including rows the adoption authored, which are structurally unreconciled from
   birth (7.7's sharpened premise) — checked against this close's gate run, each
   reported recorded-vs-measured. The coverage-floor and red-baseline bullets keep
   their decision procedures; this pass is the *detector* they and every unnamed
   row now share. No new gate run: step 2's evidence is the measurement, the merge
   having come from a clean tree.
3. **The contract's absent direction (8.1).** For every ratified decision in prior
   phase specs that has neither a contract entry nor a recorded drop, ask: is the
   behavior in the tree? Absent → surface for an explicit restore/drop ruling; a
   drop amends the source phase spec, so every decision reaches a terminal state
   and later walks shrink toward zero. This is per-close, not one-time — the §63.2
   sharpening (backfill runs once; the preserved-contract check's population can
   never reach a behavior that never became an entry) is exactly what this closes.
   The one-time backfill bullet gains the same direction for its single run.

### 67.2 The marker grammar rider (7.1's second shape)

Owner already ruled it in-report: **split it**. A half-delivered entry closes its
delivered half with the ordinary `— done (<commit>)` marker so it retires, and
opens a new numbered entry for the remainder with fresh provenance. One sentence in
the backlog-presentation bullet and one in *Bookkeeping rules*; the grammar stays
three-valued (done / dropped / unmarked) with unmarked now meaning only untouched.

### 67.3 The one-line observer (7.2)

The rule stays "one line" as the norm; the checker compares a **number** (report
7's second option is what makes its first possible). `close-out.template.sh` gains
a `docs-check` reading `git show --numstat` for the index file on close-out docs
commits, flagging when added lines exceed a stated budget — log-only, joining the
established bare-commit class. The file stays **verbatim** (no new placeholder;
invariant 1 untouched): the index path is canonical (`spec/PROJECT_INDEX.md`) and
the budget is an in-file constant. The budget must accommodate what legitimately
lands at slice close — one status line plus new backlog/friction entries — while
flagging the measured 44–87-line pattern; proposed default **25**. Proof rows join
`tools/close-out-check.py` (corpus + mutations, per the shipped-script rule).

### 67.4 Cost named up front

`commands/end-phase.md` (step 7 opening bullet; backfill direction; split
sentence); `templates/SDLC.template.md` (*Phase end* step 6 mirror, *Bookkeeping
rules* ×2 — invariant 2 says template first); `commands/end-slice.md` §9 (budget
number named beside the rule); `templates/close-out.template.sh` + its transition
note in `sdlc-update.md` + `tools/close-out-check.py` fixtures;
`templates/PRODUCT_CONTRACT.template.md` (entry-grammar comment gains the absent
direction); both READMEs untouched (no new files) unless (c) below adds one.

### 67.5 Clock, pre-registered

RECON's confirmed catch is a reconcile pass whose recorded-vs-measured report
shows a divergence that **changes an owner decision at that close** (a count
corrected before convert/defer/drop, a Records row caught drifted, an absent
behavior ruled restore/drop). Two field arcs with no catch and no divergence →
the pass earns its keep as cheap insurance only if it stays under ~10 lines of
hand-back; otherwise it is a SIMP candidate like any rule.

### 67.6 Owner decisions owed before the build

- **(a) The budget number.** 25 added index lines per close-out docs commit,
  log-only (recommended — accommodates status + legitimate entries, flags the
  measured 44–87 pattern), or another number, or refuse the checker and keep
  prose-only.
- **(b) The absent-direction population.** Full walk of all prior phase specs'
  ratified decisions, filtered to those with no contract entry and no drop record
  (recommended — converges to near-zero per close as decisions reach terminal
  states), or scope it to phases whose surfaces the arc touched (cheaper per
  close, permanently blind to untouched-surface erosion — the class 8.1 measured).
- **(c) The §64 residue.** In-repo verification scripts under `/end-phase` step 5
  still have no license. Fold into RECON as one sentence — verification scripts
  belong outside the repo (the 7.3 (a) class, already free); an in-repo
  verification artifact is a production write and takes the ordinary TDD path —
  (recommended), or hold it for the independents batch.
- **(d) Release shape.** RECON ships alone as 0.26.0 with the four independents
  following (recommended — matches §63.5's "follow, distributed by effort"), or
  one combined release.

### 67.7 Ruled 2026-08-19 — all four, plus the question the fourth pulled forward

- **(a) Budget — RULED: 25**, log-only, as recommended.
- **(b) Population — RULED: full walk, filtered**, as recommended.
- **(c) §64 residue — RULED: fold**, the one-sentence license as recommended.
- **(d) Release shape — RULED: COMBINED, against the recommendation.** 0.26.0
  carries RECON **and** the four independents (7.4a+b, 7.5, 7.6, 8.3) in one
  release. The consequence §63.5 decision 3 named was taken in the same sitting:
  **7.4b — RULED: inline the recipe.** The byte-safe revert goes into
  `end-slice.md`'s mutation step directly; the vendored `mutation-testing` skill
  stays untouched, so no invariant-3 divergence note is owed. The zero-activation
  ledger measurement is the evidence: a fix delivered by relevance-based dispatch
  is a fix delivered never.

Combined scope adds to 67.4's cost list: `commands/end-slice.md` (7.4a's inlined
recipe beside §67.3's budget line; 7.5's mutation-trigger scope),
`commands/next-slice.md` (7.5's RED shape for characterization slices),
`skills/change-verify/SKILL.md` (7.6 — kit-written, constraint before §3's drive,
no provenance cost), `commands/plan-phase.md` (8.3 — the assignment names the
path a real caller reaches it by, or flags test-only at plan time). Nothing else
is open; the build can start. **Built 2026-08-19 — see §68**, with the pre-tag
`/kit-check` at §69.


---

## 68. RECON built, combined with the four independents and the §64 residue —
## 0.26.0's whole scope in one pass, 2026-08-19

Built the same day §67 was opened and ruled. The owner's (d) ruling — COMBINED,
against the recommendation — is what makes this one section rather than two: RECON
plus 7.4a/7.4b, 7.5, 7.6, 8.3, plus the license sentence §64 left recorded and open.

### 68.1 The reconcile pass, as designed

`/end-phase` step 7 opens with it, before any bullet asks the owner anything, and the
canonical statement went into `SDLC.template.md` *Phase end* step 6 first (invariant
2). Its report shape is `recorded X / measured Y` — divergences first, each named with
the file that holds it, agreements collapsed to one line. Two decisions worth
recording beyond §67.1's design:

- **No new gate run, stated as a reason rather than a saving.** Step 2's run is the
  measurement because the merge came from a clean tree; re-running at step 7 would
  measure a *different* tree than the one the records describe. That is the same
  environment discipline invariant 15 asks for, pointed at a step that could easily
  have been written as "re-measure".
- **A row this close produces no evidence about reports `recorded X / not measured
  this close`, never as agreement.** Without that third verdict the pass would report
  a clean sweep over rows it never actually looked at — the all-`UNCHANGED`
  classification specimen (invariant 10), one layer up.

### 68.2 The observer (7.2)

`close-out.template.sh` gained a third mode, `docs-check`, and the file stays verbatim
— no new placeholder, the index path canonical, `BUDGET=25` an in-file constant. Its
seat is deliberate: **log-only on every install**, exiting 0 even on its own errors,
which puts it in the bare-commit class rather than the check mode's. The reason is the
rule it watches, not timidity — a close-out docs commit legitimately carries one
status line *plus* however many backlog and friction entries the slice really
produced, so a number cannot distinguish an honest heavy close from a write-up. `OVER`
is a question for the hand-back; "more entries than usual, here is why" is a complete
answer to it.

**Invariant 14 caught a defect in the first draft**, at the `/kit-check` below: the
budget had four prose homes (`end-slice.md`, the template, `sdlc-update.md`, the
README) and one enforcing constant, with nothing naming which was authoritative —
the exact shape 7.7 filed. Both process homes now say the number is a copy and the
script's `BUDGET` is the enforcing home, adding that the mode's own output quotes the
budget it used, so the value to believe is the one that was actually applied.

**Proof:** seven docs cases and six mutations joined `tools/close-out-check.py`
(under budget, exactly at it — 25 is not over — over it, an untouched index, a
retirement commit that only deletes, an explicit ref, and a bad ref that still exits
0). Full suite measured, not assumed: **21 unit + 7 docs + 15 stop cases, 22
mutations, 22 caught, 0 survivors**, slowest docs invocation 427 ms against the 1000 ms
budget. Each docs mutation is caught by a docs case, which is what makes the seven
cases evidence rather than decoration.

### 68.3 The four independents and the residue

- **7.4a + 7.4b — inlined, per §67.7's ruling.** The byte-safe revert is stated in
  `end-slice.md` §5 and the template's step 8: `git checkout -- <path>`, then
  `git status --short` clean, never a whole-file read-then-write (which normalizes
  line endings, trailing newline, and encoding — four corrupted working trees in one
  arc). The vendored `mutation-testing` skill is **untouched**, verified against the
  diff, so no invariant-3 divergence note is owed and `reference/SKILLS.md` needed no
  edit.
- **7.5 — both anchors, and the trigger inverts rather than widening.** A slice that
  added tests but no guard mutates *the production code each new test pins*. Sampling
  is allowed and must be stated (`mutation: 6 of 129 characterization pins`) — an
  unstated sample is the same blank the exemption left. RED gets the matching shape:
  manufactured and still observed (assert the wrong value first, watch it fail, then
  assert what the code does), never the zero-form, which belongs to a slice with no
  behavior batches at all.
- **7.6 — the constraint goes *before* §3's drive**, which was the whole finding: the
  only environment step ran after the run. Enumerate what the path reaches on its way
  out — credentials, data directory, outbound calls, queue, clock — point each
  somewhere disposable or confirm it inert, and state the isolation with the result.
  The sentence that carries it: **half-isolated is not isolated**, because the half
  nobody redirected is the half that reaches production.
- **8.3 — the assignment stops being terminal** (`plan-phase.md`, mirrored into the
  template's *Phase start* step 3): name the path a real caller reaches the behavior
  by, or flag it test-only **at plan time**, with what would create the seam.
- **The §64 residue folded in**, one sentence at `end-phase.md` step 2 and the
  template's *Phase end* step 1 — a verification script's license depends on where it
  lives, and the default is outside. Note the correction: §67.6 (c) placed it at
  "step 5" and §64 at "step 1"; the phase-level verification it is about is
  **`end-phase.md` step 2** (the template's *Phase end* step 1), which is where it
  went. The ruling's substance was unambiguous; only the step number was wrong.

### 68.4 Cost, measured against §67.4's estimate

Eleven bundle files (VERSION, four commands touched by RECON, two more by the
independents, `change-verify`, and three templates), plus `tools/close-out-check.py`,
the root README, `CHANGELOG.md`, `KIT_INVARIANTS.md`, and `.claude/commands/kit-check.md`
— the last two from the `/kit-check` findings below. §67.4 predicted every bundle file
correctly and named neither ledger file, which is the standing lesson (§55, §58, §60,
§65) landing for a **fifth** pass: a batch's cost estimate covers what it implements
and misses what *describes* what it implements.

**Dates.** The build and the `/kit-check` both happened **2026-08-19** and those dates
stay, because they record when the work happened; the `CHANGELOG.md` entry carries
**2026-08-21**, the day the tag went out, under §62's re-date instruction — the same
split §64 recorded for 0.25.0.

---

## 69. The pre-0.26.0 `/kit-check` — run 2026-08-19 on the combined RECON +
## independents scope: six findings, all fixed in-session, and for the first time in
## five passes the stale-description class was caught by an invariant rather than by
## a reader

Mechanical checks first, then the reading passes, then the fixes. The pass ran against
the full ledger; nothing was scoped out.

### The six findings

1. **Invariant 2, mirror direction — the §64 license sentence lived only in
   `end-phase.md`.** A rule a command enforces must appear in `SDLC.template.md`, and
   this one did not. Fixed: *Phase end* step 1 carries it.
2. **Invariant 2 — 8.3's rule lived only in `plan-phase.md`.** The template's *Phase
   start* step 3 described exit criteria naming their observer and said nothing about
   an acceptance assignment naming its caller path. Fixed.
3. **Invariant 2 — `change-verify`'s isolation constraint had no template home.** The
   skill carries the method, but *constrain before you drive* is a process rule and
   the template describes the step twice. Fixed at slice-loop step 9.
4. **Invariant 14 — the budget number named no enforcing artifact.** Four prose homes,
   one constant, nothing saying which wins. Fixed in both process homes (see §68.2) —
   and this is the finding the batch would most have deserved, since 7.7 is *exactly*
   this defect and RECON is its fix.
5. **Invariant 15 — `docs-check` did not name the shell it runs in.** Every sibling
   step does (`the agent's shell tool`, the gate's own scope). Fixed in the command
   and the template.
6. **Invariant 13 — the new observer was not in the denominator.** A check added
   without being added to invariant 13's enumeration is one the next pass will not
   think to look for; the invariant says so about itself. Fixed in `KIT_INVARIANTS.md`
   and `.claude/commands/kit-check.md`, whose "As of 0.25.0 that list is" also moved
   to 0.26.0. The entry states the observer's negative case honestly: **log-only, so
   it has no arming ramp and no fire-proof at setup** — its negative case is the docs
   corpus and its six mutations, which is where a budget that stopped discriminating
   would show.

Findings 4, 5 and 6 are the interesting ones: all three were caught by invariants the
kit wrote for itself after earlier misses, and none by re-reading the prose. That is
the first pass where the stale-description class was caught **mechanically-in-spirit**
rather than by a careful reader noticing.

### Passes worth recording with what they looked for

- **Invariant 9 (README tree):** every tracked file's basename located in the root
  README. No new files this batch, so the negative case (an added file absent from the
  tree) had nothing to fire on — recorded as such rather than as a pass with evidence.
- **Invariant 10 (manifest):** regenerated from the **index**, not the working tree,
  and verified twice — 43 entries against `git ls-files sdlc-kit` minus one, `sha256sum
  -c` 43/43, **zero `*` prefixes** (the text-mode trap that has now bitten twice), and
  the discrimination check reporting **exactly 11** changed rows, matching the eleven
  edited bundle files and nothing else.
- **Invariant 4 (`{{` census):** hits in `sdlc-setup.md` only (53). The verbatim
  close-out script was re-checked at zero, which the proof harness also asserts on
  every run.
- **Invariant 6 (step references):** all six references added by this batch read and
  confirmed against their targets — `end-phase` steps 2 and 5, `end-slice` steps 8
  (×3) and 9.
- **Invariant 11 (provenance, two regimes):** the diff confirms `mutation-testing/` is
  untouched, which is what the 7.4b ruling was for; `change-verify` is kit-written, so
  its edit carries no provenance cost and `reference/SKILLS.md` needed nothing.
- **Invariant 1 (no project facts):** one softening — *the guards see only files
  inside the repository* became *where the guards are installed, they see only…*,
  since a project can decline them.

---

## 70. The ninth field report triaged — six findings stand, three do not survive as
## filed, and one of the three is a hazard 0.26.0 shipped five days ago — 2026-08-26

`FIELD_REPORT_2026-08-21.md` (`sdlc-kit#9`, filed 2026-08-21) is the **ninth** field
report and the **sixth** from the first adopter, covering their Phase 08 — 5 slices, 1
PR, 27 owner decisions — written against **0.24.0**, which is genuinely what they run
(`spec/SDLC.md:13`, and a kept `sdlc-kit/` folder at 0.24.0). Nine findings, a priority
table, and an owner-posted correction that reproduces the report's own finding 1.

It arrived **five days after 0.26.0 released** and describes an arc that closed on
0.24.0 one day after the eighth report's batch was designed. That overlap is most of
the triage: three findings collide with work already shipped, and one collides with it
head-on.

**Its theme, one step past the eighth report's:** *this kit verifies that a step ran; it
does not verify that a step could have caught anything, or that a decision it recorded
ever reached a terminal state.* The eighth report said the kit is bad at making a number
reconcile and the kit answered with RECON; this one says a reconcile pass over the rows
the kit names cannot see a number written somewhere the kit does not name.

### 70.1 The arc, as measured

Every enforced thing green and agreeing with CI — lint 0, typecheck 0 over 18 source
files, **762** tests (the report says 761; see the correction), coverage floor 63, 0 fix
commits, close-out records **8/8 COMPLETE**, 53 observed REDs. At that same moment two
recorded numbers were wrong on disk and the backlog held 106 entries under 104
identifiers. None of the nine findings is about the work.

### 70.2 The three that do not survive as filed

**Finding 7 — the `"shell": "bash"` pin — DOES NOT STAND. It was fixed in 0.24.0, the
release the report is written against.** `templates/settings.template.json` carries no
`"shell"` key anywhere; read the file. 0.24.0's PIN batch (§61) removed it, and
`tools/gate-hook-check.py` gained wiring cases pinning the no-`shell`-key property "so
the measured-dead pin cannot be silently reintroduced". The corrected template was
sitting in the adopter's own tree the whole time, in the `sdlc-kit/` folder they keep at
0.24.0. **How it got in is the interesting part, and it is finding 3's mechanism:** the
entry reached the report through `sdlc-retro.md` step 2's *age rule* — carry any friction
entry older than one phase into the report automatically — which asks nothing about
whether the upstream artifact still holds the defect. A recorded claim was carried
forward without being re-derived against the artifact, inside a report whose theme is
that recorded claims are not re-derived against artifacts. Nothing owed kit-side beyond
the age-rule clause below; the adopter should be told, so the entry can close as
*implemented in 0.24.0* rather than age a third phase.

**Finding 4 — "no workflow command dispatches `mutation-testing`" — PREMISE FALSE, and
its suggested fix was ruled against seven days ago on this same evidence.** Verified
against **0.24.0 itself** (`git show v0.24.0:sdlc-kit/commands/end-slice.md`): §5 reads
*"Use the mutation-testing skill (`mutation-testing`, installed at
`.claude/skills/mutation-testing/`) for anything beyond a quick delete-and-run"* — the
skill by identifier, its install path, and a trigger condition. The claim that the step
"never names the installed skill" is wrong about the text it quotes. `end-phase.md` §5
is wrong in the other direction: the whole-arc review has no mutation step at all, so
"likewise" describes nothing there — adding one is a different proposal from fixing one.
And the suggested fix — dispatch by name instead of paraphrasing — is exactly the option
**§67.7 ruled against on 2026-08-19**, on this adopter's own ledger measurement: *a fix
delivered by relevance-based dispatch is a fix delivered never*, which is why 0.26.0
inlined the byte-safe recipe (7.4a) rather than pointing at the skill.

What survives is real and is not a naming problem: **0 dispatches against ~40 mutations
actually run, second consecutive arc at zero**, while mutation produced *both* of the
arc's defect findings including one that had survived two arcs with a fully green suite.
Naming has now been tried and measured. The live question is whether a skill file nothing
ever dispatches earns its place, or whether the rest of it follows 7.4a into the command
text — a delete-or-inline question, on a **vendored** file, so invariant 3 attaches
either way. See the decision owed below.

**Finding 9's first half — the mutation revert mechanism — is INVERTED, and this is the
one to act on first.** 0.26.0's 7.4a inlined this into `end-slice.md` §5 five days ago:

> **Restore by reverting the file, never by rewriting it.** The mutation is a tracked
> edit, so the tracked original is the byte-exact copy: undo it with
> `git checkout -- <path>` […] Never restore by writing the file's text back through a
> whole-file read-then-write

Finding 9's specimen is that exact command destroying a slice: *"the mutation was
reverted with `git checkout -- <file>`, which reverted the **uncommitted implementation
along with the mutant** — the file had no committed version of the slice's work behind
it."* **Both specimens are real, and the shipped text is wrong at the step that invokes
it.** §5 runs at end-slice; **§7 is where the slice commits**. So at §5 the slice's
implementation is uncommitted by construction, and §5's own justification — *the mutation
is a tracked edit, so the tracked original is the byte-exact copy* — is false there: the
tracked original is HEAD's version, not the pre-mutation working tree.
`git checkout -- <path>` at §5 reverts the mutation **and the slice**. The parked-stash
alternative the same sentence offers parks the slice too.

This is the only finding on the list getting worse with time: it is **[installable]**, it
is canonical as of 0.26.0, and it has not yet reached either adopter. A resolution
satisfying both specimens exists and is three lines — **a targeted single-hunk edit back**
(the mutating edit, inverted) is neither a whole-file read-then-write nor a VCS restore:
it normalizes nothing and discards nothing. `git checkout --` stays correct only where
the file carries no uncommitted work behind it, which §5 must **test for** rather than
assume.

### 70.3 The six that stand

**1 — the floor reconcile names homes by document, and a document holds the number
twice. STANDS, with two corrections that sharpen the fix.** Verified: `end-phase.md` step
7's Coverage-floor bullet reads *"the floor recorded in `spec/PROJECT_INDEX.md` (and
`spec/SDLC.md`)"*, and §68's reconcile pass is defined over *"Every row of `spec/SDLC.md`
Records"* — so a second home 300 lines away in the same file, and the index's ceiling
line, are outside its population. **The report's warning is correct: 0.26.0 would have
reported this instance clean.**

- *Correction A.* The report names `templates/SDLC.template.md` as seeding both homes.
  It does not. The template's *Coverage floor* section is procedural prose carrying **no
  number**, and `git log -S"Current:"` over that file's entire history returns nothing.
  The second home is **adopter-authored**. The fix cannot be "fix the template's second
  home"; there is none. What the template lacks is the prohibition.
- *Correction B, and it is the finding's real shape.* **The kit already has that
  prohibition** — for a different number, in `PROJECT_INDEX.template.md`: *"Gate
  baseline: recorded in spec/SDLC.md (its single home — do not restate the counts here,
  they would go stale silently when the baseline moves)."* The doctrine exists. It is an
  instantiation-time comment, addressed to setup, covering one number in one file, and
  nothing ever re-reads it. The adoption restated the count in two files anyway. This is
  not a missing rule — it is **a rule with no observer**, which is the shape §68 built
  `docs-check` for.

The adopter has already fixed their side: all four homes now read 63/762, with the
incident recorded in place (`spec/SDLC.md:568`, `PROJECT_INDEX.md:265`).

**The correction comment — STANDS, and its second cause collides with a 0.26.0 rule.**
Cause 1 (a `-q` runner that emits no count, so "read the count" yields silence and the
gap gets filled from the document under review) is unaddressed: the red-baseline bullet
says *report this arc's count beside the recorded one* and never says where the count
comes from. Cause 2 is the one to weigh: the baseline was re-derived correctly from the
PR's CI run, then a close-out commit **after the merge** added a test, so the freshly
re-derived number was already wrong when the close finished. **§68's reconcile pass
forbids the proposed fix** — *"No new gate run — step 2's run is the measurement […]
re-running here measures a different tree than the one these records describe."* Step 2
runs pre-merge on the arc branch; step 7 then commits docs, contract pins and bookkeeping
on main. 0.26.0 says the record describes the *measured* tree; the correction says it
must describe the *final* tree. Both are coherent, they cannot both be the rule, and the
correction is right that most closes under this kit commit after merging. Owner decision.

**2 — nothing allocates a backlog identifier. STANDS, unqualified, and it is the cheapest
item on the table.** `end-slice.md` §9's append bullet prescribes rationale, provenance
and cause marker and never mentions the number every downstream step addresses entries
by. §68's reconcile walks the backlog and reports the open count but asserts nothing
about uniqueness. And `end-phase.md`'s retirement bullet makes a promise a collision
silently breaks — *move the entries verbatim […] so an old reference to an entry still
resolves* — into a file no session reads at start. Measured: 106 entries, 104
identifiers, all four collisions minted the same day by two slice reviews writing into
different regions of a 1,500-line list. One clause plus one `sort | uniq -d`.

**3 — "absorbed" is a third state that reads as closure. STANDS, and it is load-bearing
for two other findings.** `sdlc-retro.md` step 2: *"entries a previous retro absorbed
carry a marker, so report the ones that do not"* — absorbed is excluded from the sweep.
Step 6's flip is a bare `absorbed by retro <date>` with no disposition. `end-slice.md` §9
and the template name only two closed states and never mention absorption. That is how a
hazard reached **eleven recurrences** with two retros and two owner rulings in between.
**Add a fourth part to the report's three:** the age rule in the same step-2 sentence
must ask whether the upstream artifact still holds the defect — that is how finding 7 got
here.

*Note against §63.3:* the guard ergonomics behind those eleven recurrences **were**
fixed, in 0.25.0/CLASSIFY — out-of-repo writes and quoted-argument matching, both
dialects. The adopter cannot see it: neither fix arrives by updating (the instantiated
guard is project-owned), which is the standing transition note. Their *compound-command*
half (40 uncounted `cd "<path>" && pytest` runs) is **not** covered — 0.25.0 deliberately
left the compound check reading the raw command — so that half is new and open.

**5 — the stop-time backstop watches a window the workflow empties. STANDS.**
`close-out.template.sh:105–107` scopes `stop-check` to `git rev-list -n 20 '@{u}..HEAD'`,
and `end-slice.md` step 7 commits **and pushes**, so the range is empty at every ordinary
stop: 121 log lines, ~100 vacuous `clean`, 4 false positives, **0 real catches** across
an arc. The transferable half is the sharpest sentence in the report and generalizes past
this hook: **a fire-proof and a catch-proof are different tests.** The kit already makes
exactly that demand of the coverage floor (*prove it fires — once*) and makes it of none
of its own controls.

**6 — a ratified *method* and a *Risks* entry reach no terminal state. STANDS, both
halves.** `next-slice.md` §2 re-derives the entry's **cause** and an **estimated
number**; a ratified method the slice implements *through* is uncovered, and the arc's
specimen cost a real conclusion (going straight to the bisect passed §2 cleanly; running
the prescribed byte-diff proved the region byte-identical and named a difference the
bisect had only eliminated by inference). §68's reconcile has three subjects — backlog,
*Records*, contract-absent — and never re-reads the phase spec's own *Risks & Deferred*,
so an obligation the spec attached to the arc lapses by silence while the arc makes the
question larger. **Cheapest medium item on the list, because it is not a new mechanism:**
Risks is a fourth subject for the pass 0.26.0 already built.

**8 — `change-verify` §3 has no shape for a process that never returns. STANDS.** §3
gained the environment-constraint opening in 0.26.0 (7.6) and still carries nothing for
the commonest front door there is: `subprocess.run(timeout=…)` discards the output it was
about to prove the pass with, a pipe-attached child buffers stdout so the banner never
arrives, and on Windows printing the captured UTF-8 to a cp1252 console raises after the
run succeeded. Cost it twice this arc, once **with the skill dispatched**, which makes it
a text gap rather than an operator lapse. Kit-written file; XS.

**9's second half — `change-simplify` §3 prices the gate at zero. STANDS.** *"Apply them
one at a time, gate between"* is right, and its cost scales with suite runtime, which is
the one thing a maturing project reliably grows: two moves cost three backgrounded
full-gate runs and a poll loop each at a ~100-second suite. Say what the intermediate
gate may be trimmed to. Kit-written; XS.

### 70.4 What the report confirms about shipped work

Recorded because a simplification pass should not have to rediscover it. The arc ran on
0.24.0 and independently exercised two things 0.26.0 built:

- **The half-delivered split (§68) has field confirmation before the release reaches
  them.** *"The retirement bullet's own re-read check fired for the first time and
  produced its designed failure: a half-delivered entry was pulled back out of the
  history file rather than retired on a marker it only half-earned."* That is exactly the
  case §68's split rule addresses, observed independently.
- **The preserved-contract check's negative case was proven to fire**, and the
  product-contract reconcile ran to 12 new entries with one claim-only promoted to
  pinned.

### 70.5 Clock evidence this report supplies

The four §63.4 rulings are still owed, and **three of them now have another arc of
evidence** — which is the argument for taking them alongside this triage rather than
before it:

- **The three STD lenses.** This arc: *unconsumed artifact* one genuine hit, *preserved
  contract* clean with its negative case proven to fire. That is a second named catch
  from the same adopter, and it bears directly on the ruling about whether ai-news's
  lens-less evidence table counted as an arc.
- **`change-simplify`.** Ran 4/5 slices, 2/2/3/1 moves, one skip with a stated reason — a
  third arc of moves-applied and still no *confirmed catch* in the clock's wording. The
  ruling (does "moves applied" clear it?) is now three arcs old.
- **CONTRACT's value criterion.** The reconcile ran and the negative case fired. Whether
  that is the clock's first arc or a repair of the mechanism is the ruling.
- **Bare-flagging arming bar.** Still no false-candidate count in any report. Ask.

### 70.6 Decisions owed

1. **Sequencing against IMPACT.** IMPACT (§66) is build-ready and was next in the queue.
   This report's finding 9a is an installable hazard the kit shipped five days ago and
   neither adopter has yet. Recommendation: **a small batch first** — 9a, plus the XS/S
   items that need no design (2, 8, 9b, and finding 3's four-part fix) — then IMPACT,
   then the medium items (1, 5, 6). The alternative is folding everything into one batch
   behind IMPACT, which leaves 9a canonical-and-wrong for however long that takes.
2. **Finding 1's fix shape.** Search-for-the-old-value until it cannot be found, as
   filed — or the stronger form corrections A and B point at: *a number has one home and
   the others link to it*, with the existing `PROJECT_INDEX.template.md` prohibition
   generalized and given an observer. The second is more work and is the fix that does
   not go stale the next time someone writes the number somewhere new.
3. **The correction's cause 2, against §68's "no new gate run".** Does a recorded
   baseline describe the tree that was measured, or the tree the close leaves behind? The
   two rules cannot both stand.
4. **Finding 4's real question.** `mutation-testing` is dispatched zero times across two
   arcs while being the step with the best defect record on this adoption. Inline the
   rest of it (7.4a's precedent), delete it, or leave it and accept that it is
   documentation? A vendored file either way — invariant 3 attaches.
5. **The four §63.4 clock rulings**, on the evidence in 70.5.

### 70.7 Ruled 2026-08-26 — all five, plus the two clock questions the fifth answered
### from evidence rather than judgement

1. **Sequencing — RULED (a): a small batch now, then IMPACT, then the medium items.**
   The batch is 9a, finding 2, finding 8, finding 9b, finding 3's four-part fix, ruling
   4's inlining, and the lens-denominator line ruling 5 (i) requires. All text, all
   installable, no design owed. The deciding fact is that 9a is a defect the kit
   shipped rather than one it inherited. Findings 1, 5 and 6, and ruling 3's baseline
   stamp, follow IMPACT.
2. **Finding 1 — RULED (b): search-for-the-old-value *and* the structural rule.** The
   reconcile pass gains the value search (the enforcement artifact's number, then no
   occurrence of the old value anywhere in the spec set — failure is a file list), and
   the `PROJECT_INDEX.template.md` prohibition is generalized: a number has one home
   and everything else links to it. The two halves do different jobs and the ruling
   takes both — the search is what works on day one and on trees the kit never seeded;
   the prohibition is what stops the class being re-created. Scheduled after IMPACT.
3. **The correction's cause 2 — RULED (a): stamp the baseline with the commit it was
   measured at.** §68's *no new gate run* stands. Verified before the ruling: the kit
   stamps no baseline with a commit anywhere, and nothing in `GATE_RECIPES.md`
   establishes that a project runs CI on pushes to main — so the correction's own
   proposal (re-derive from the first main-branch CI run after merge) is correct for
   the adopter who filed it and inert for any project without that topology. Stamping
   concedes the correction's point — the number was already wrong when the close
   finished — without making the fix depend on a CI shape the kit cannot require. The
   number stops claiming to describe a tree and starts describing a commit; the next
   close's reconcile reads the drift. Scheduled with finding 1.
4. **`mutation-testing` — RULED (a): inline the standing rules, keep the skill as
   depth, correct the claim in `reference/SKILLS.md`.** Verified: 119 lines, an
   MIT-derived condensation, and beyond what §5 already carries it holds the 3–8 sample
   size, never-stack, the escape workflow and the mutation score. Deleting it would
   lose those; leaving it produces a third arc at zero. So §5 takes the rules that bite
   when the loop is hand-rolled — sample size, never-stack, and the safe revert 9a is
   fixing — and the skill stays for depth. `SKILLS.md` currently claims the skill is
   *required since 0.5.0 because `/end-slice`'s mutation-check step invokes it*; two
   arcs of ledger say otherwise, and the row is corrected to what is true. **The
   vendored file is untouched, so no invariant-3 divergence note is owed** — the same
   reasoning that decided 7.4b, and the reason this ruling puts the mechanism in the
   command rather than in the skill that states `Always revert` and names nothing.
5. **The four §63.4 clocks — RULED, two of them from evidence.**

**(i) The three STD lenses — NOT deleted; the clock could not be read, and the reason
is a defect.** The strict reading said delete: arc one (Phase 07) and arc two (Phase
08) both close with no catch named by any of the three. The denominator was then
checked against the adopter's own records and **is not there.** Across both arcs the
phase specs carry **one** lens line in total — Phase 08's arc-level
`unconsumed artifact: clean` / `preserved contract: clean`; Phase 07 has none — while
`end-slice.md` §4 and `REVIEW_LENSES.md`'s preamble both require every review to write
a lens line **including `no lens triggered`** when none applied.

The absence is structural, not an operator lapse. The preamble retires the review
hand-back and carries only a lens **finding** onward ("into wherever the finding
lands"); a `clean` verdict and a `no lens triggered` verdict have **no durable home by
construction**. 0.22.0's instrument fixed attribution for catches and left the
denominator invisible, which is the same half-fix the ninth report names at the hook
level: a fire-proof standing in for a catch-proof. So the two arcs cannot distinguish
*the three lenses ran and found nothing* from *their triggers never matched a slice*,
and three lenses cannot be deleted on a number nobody has.

**Ruled: fix the missing half, then restart the two-arc clock from the first arc whose
denominator is enumerable.** The slice commit body already carries `mutation:` and
`verify:` lines; the lens verdict joins them as a `lenses:` line, which is where every
other per-slice evidence line already survives the session. In the small batch. This
also **retires the ai-news question** — whether that arc counted toward the denominator
never has to be ruled, because the denominator itself was unmeasured on every arc.

**(ii) `change-simplify` — RULED: the criterion was mis-specified, and it is re-written
once, knowingly spending the "no further extension" commitment.** Three arcs of applied
moves (12 / 6 / 2+2+3+1 with one stated skip) and zero *confirmed catches* under a
clock worded for a defect-finding instrument. A pass whose output is **quality** rather
than defects cannot produce a catch in the sense that wording means, so the clock spent
two arcs measuring the wrong property. Re-specifying is an extension in effect and is
recorded as one: the commitment is spent here and cannot be spent again.

**The new clock — two field arcs, final, and two-sided, because it tests the §53
redirect rather than the pass in general.** The redirect exists to end one specific
division of labour — the founding miss was Phase 04 S4's duplicated `LogCaptor` helper,
"nothing to do" from this pass and caught by `diff-review` on the same diff, and the
eighth report recorded the same shape again. So:

- **Positive:** at least one arc records a **Reuse-axis move that names its search** —
  the redirect's own deliverable, and evidence the pass is searching rather than
  eyeballing.
- **Negative, and it is the failure condition:** any arc in which a reuse or
  duplication finding is first raised by `diff-review` or the whole-arc review on a
  diff this pass had already passed over **fails the clock outright**, whatever the
  move count. That is the founding miss recurring, and a third recurrence is the
  answer.

Both halves read off artifacts the kit already requires — per-axis verdicts with the
Reuse search named, and `diff-review` findings carrying step provenance. No catch and
no failure across two arcs → deletion, no further extension, and this time the
criterion measures what the instrument does.

**(iii) CONTRACT — RULED: arc one was not spent.** The pre-registered criterion failed
on its first arc, but the mechanism **named its own repair** (8.1) and that repair
shipped in 0.26.0, so the arc measured a defective mechanism rather than the one on the
clock. Phase 08 adds evidence the rest of it works — the reconcile ran to 12 new
entries, one claim-only promoted to pinned, and the preserved-contract check's negative
case was **proven to fire** — but that is the mechanism functioning, not a catch. The
clock starts at the first field arc run under **0.26.0**, which is neither adopter yet:
both are on 0.24.0. **The adopter update offer is therefore what starts this clock**,
which is a second reason it comes next.

**(iv) The bare-flagging arming bar — RULED from the report's own measurement: the bar
is unmet and the backstop stays log-only.** §52.2 requires **zero** false candidates
across the logging trial and the first field arc. Phase 08's close-out log supplies the
count that was missing from the seventh and eighth reports: 121 lines, and the only
non-clean firings in the entire arc were **4 WOULD-BLOCK lines on a single
documentation commit**, which the adopter names as a false positive. Four, not zero. No
question to either adopter is needed. It is moot twice over: finding 5 shows the window
`stop-check` watches is empty by construction, so arming a control over an empty window
would have armed nothing — the arming question cannot be re-opened until finding 5's
scope fix lands.

**(v) R3.8's aging rule** — untouched by this report as a rule, but note it is the
mechanism that carried finding 7 into the report, and ruling 5's batch item for finding
3 adds the missing clause: an aged entry is re-checked against the upstream artifact
before it is carried.

---

## 71. A perf gate that disables the mutation pass — `tools/close-out-check.py`'s S2
## budgets fail the released kit on this machine, and a timing wobble costs the
## strongest check in the suite — filed 2026-08-26

Found while building 0.27.0 (§70), and filed rather than fixed because it is the
tooling's own defect and not part of that batch's ruled scope.

### 71.1 What was measured

The suite has three S2 timing budgets — unit 1000 ms, docs 1000 ms, stop 1500 ms with
a 5000 ms cap-20 walk — each checked with `if slowest >= …: sys.exit(1)` immediately
after its pass. Measured on this machine over six runs:

| run | unit warm | docs | stop typical | outcome |
|---|---|---|---|---|
| **v0.26.0, released tag, throwaway worktree** | 436 ms | 535 ms | **1918 ms** | **S2 FAILED**, exit 1 |
| 0.27.0 A | 368 ms | **5503 ms** | — | S2 FAILED (docs) |
| 0.27.0 B | 368 ms | ok | **6289 ms** | S2 FAILED (stop) |
| 0.27.0 C | — | — | **6120 ms**, cap-20 **8977 ms** | S2 FAILED (stop) |
| 0.27.0 D | **5328 ms** | — | — | S2 FAILED (unit) |
| 0.27.0 E | ok | ok | ok | **all green**, 22 mutations caught |
| 0.27.0 F | — | — | **6099 ms** | S2 FAILED (stop) |

Two things follow, and only the second is interesting.

**The budgets do not hold on this machine, and that is not a 0.27.0 regression.** The
**released** v0.26.0 fails the stop budget here (1918 ms against 1500 ms) — measured
against the tag in a throwaway worktree rather than argued. And the decisive control:
the **docs** pass is untouched by everything 0.27.0 changed (`docs-check` never calls
`count_record`) and still swung **535 ms → 5503 ms**, a 10× move on identical code.
Same code measured 368 ms and 5328 ms on the unit pass in consecutive runs. This is
machine state, not cost.

### 71.2 The finding, which is the ordering and not the numbers

**A timing wobble silently costs the mutation pass.** Each budget check exits
immediately, and the mutation pass runs *last* — so on any loaded machine the run
ends after the functional passes and **before the only pass that tests whether the
corpus can detect a defect at all.** Invariant 13's instrument is the one a flaky
gate switches off.

That is not hypothetical. It happened three times during this batch, and it mattered:
0.27.0 added a fifth key whose corpus turned out **not to pin its anchor** —
`anchor_dropped_lenses` SURVIVED. The only run that revealed it was the one that got
past S2; four runs before it reported green functional passes and told nobody. The
gap was then closed and verified by driving the mutated and real scripts by hand,
because the suite could not be made to complete.

**This is the ninth report's own finding 5, in the kit's own tooling, one turn
sharper:** there, a control's reach was unmeasured; here, a control *disables another
control*, and the log reads like a failure of the thing being tested rather than a
pass that never ran. A functional-plus-mutation result and a perf result are
different verdicts, and one must not be able to suppress the other.

### 71.3 Options, none ruled

1. **Collect perf, never short-circuit on it.** Run every functional pass and the
   mutation pass unconditionally; accumulate perf breaches and apply them to the exit
   code at the end, so a slow machine still yields the complete correctness signal.
   Cheapest, and it keeps the budget's teeth. **Recommended.**
2. **Reorder** so the mutation pass precedes the budget checks. Fixes this instance,
   leaves the general shape (an early gate hiding a later pass) in place.
3. **Re-calibrate** — median or best-of-N per invocation rather than the slowest
   single one, which is what a background antivirus scan lands on. Worth doing beside
   1 or 2; on its own it only moves the threshold at which the hiding starts.

The budgets exist for a real reason — the stop path runs inside a 30 s hook timeout —
so none of these proposes dropping them.

**Scope checked, not assumed: this is the only suite affected.** `close-out-check.py`
is the sole `tools/` proof with timing budgets; `gate-hook-check.py` and
`skill-ledger-check.py` contain no timing code at all, and the two guard suites' only
use of `time` is `sleep(1.1)` for 1-second-granular mtime ordering, which is a
correctness device rather than a gate. So the fix is one file, and no sweep is owed.

---

## 72. The 0.25.0 guard fix disarms the shell dialect on Windows — found while
## updating the adopter it was written for, and held out of their update — 2026-08-26

Found 2026-08-26 during the ai-news-dashboard update to 0.28.0, by running the fix
against **that project's own recorded payloads** before trusting it. The guard was
reverted to its 0.24.0 body there and the divergence recorded in their `spec/SDLC.md`;
the rest of the update shipped. This section is the kit-side half.

**Severity: high, and it is live in three releases.** 0.25.0, 0.26.0, 0.27.0 and
0.28.0 all carry it. Any Copilot-CLI adopter on Windows running 0.25.0+ has a TDD
guard that **stops guarding every write the CLI reports by absolute path** — which is
how that CLI reports them.

### 72.1 What was measured

`templates/tdd-guard.template.sh`, the relativization added by §64/CLASSIFY:

```sh
nl=$(printf '%s' "$n" | tr '[:upper:]' '[:lower:]')
rr=$(printf '%s' "$SDLC_REPO_ROOT" | tr '\\' '/'); rr=${rr%/}
rl=$(printf '%s' "$rr" | tr '[:upper:]' '[:lower:]')
case "$nl" in
  "$rl"/*) n=$(printf '%s' "$n" | cut -c $((${#rr} + 2))-) ;;
  /*|?:/*)
    log "write outside the repository - not production source: $p"
    continue ;;
```

**Corrected 2026-08-26 while building the fix — this filing claimed two causes and
there is one.** The incoming path *is* backslash-normalized, six lines above
(`n=$(printf '%s' "$p" | tr` ... `)`); I misread its absence. The single cause is the
flavour mismatch:

**The root and the paths are in different flavours.** `SDLC_REPO_ROOT=$(pwd)` in the
hook's MSYS shell yields `/d/aicourse/ai-news-dashboard`; the CLI reports a path that
normalizes to `d:/aicourse/...`. `/d/...` never prefixes `d:/...`, so the match cannot
succeed however the separators are written.

**And it is broader than "backslash paths".** Measured on a bench where `pwd` answers
`/tmp/...` and `pwd -W` answers `C:/Users/...`: the 0.28.0 body also fails on a
**forward-slash** absolute in-repo path (3/5 against the fixed body's 5/5). Any
absolute path fails whenever the two flavours differ; the adopter's backslashes were
how it surfaced, not what caused it.

So `nl` matches neither arm's intent: it falls through to `?:/*`, is logged as
*outside the repository*, and `continue` **skips the write entirely**.

**Measured on a real path from the adopter's own `guard.log`** —
`D:\AICourse\ai-news-dashboard\src\main\java\com\ainews\dashboard\refresh\RefreshOrchestrationService.java`,
a path their guard had genuinely denied before:

| guard body | verdict |
|---|---|
| 0.24.0 (pre-fix) | **DENY** production write without observed red |
| 0.25.0–0.28.0 | *"write outside the repository - not production source"*, **allowed** |

A fix written to *narrow* the guard's scope opened a hole in it. That is the worst
shape a control change can take, because the log line reads like correct behavior.

### 72.2 Scope, checked rather than assumed

- **The Claude/Python dialect is CORRECT and needs no change.**
  `templates/tdd-guard-claude.template.py` normalizes **both** sides
  (`n = p.replace("\\", "/")` beside `root_n = ROOT.replace("\\", "/")`), and its
  root comes from `CLAUDE_PROJECT_DIR` or `os.getcwd()`, which under Windows Python is
  already `D:\...`. Verified empirically on the first adopter 2026-08-26: an in-repo
  absolute path relativizes to `usage_store.py` and is denied.
- **The shell dialect is broken only where the hook shell's `pwd` flavour differs from
  the CLI's path flavour** — i.e. Windows. On a POSIX host `pwd` gives `/home/x/repo`
  and paths arrive `/home/x/repo/...`, so the prefix matches and the fix works as
  designed. The defect is Copilot-CLI-on-Windows, which is exactly the adopter the fix
  was written for.

### 72.3 WITHDRAWN — the "log corruption" was my probe, not the guard

**Filed 2026-08-26, withdrawn 2026-08-27 after measurement.** This section claimed the
guard corrupted backslash paths in its own log and deny text (`` becoming a BEL, so
`cominews` rendered `cominews`). That is **false**, and the claim should never have
been filed on the evidence I had.

What the measurement shows, run in the adopter's own tree with a payload built by
`json.dumps` rather than by hand:

- sent `D:\AICoursei-news-dashboard\src\main\java\cominews\dashboard
efresh\RefreshOrchestrationService.java`
- logged **byte-exact**, `` and `
` intact.

And the decisive check — the only two corrupted lines in that project's entire
`guard.log` are timestamped `2026-08-26T18:03:53Z` and `18:04:15Z`: **both are my own
probes from the day before.** Every line from a genuine session carries
`D:\AICoursei-news-dashboard` uncorrupted.

`log()` was never suspect on inspection either — it is
`printf '%s [%s] %s
' … "$1"`, with the path as an **argument** to `%s`, which
performs no escape interpretation. I wrote the section anyway, from a log line I had
produced myself.

**The actual cause:** my probe's payload was constructed inside a shell-quoted
`python -c` string, and the backslashes were consumed one layer before Python saw
them, so the guard was *sent* an already-mangled path and logged it faithfully. The
guard did exactly the right thing with exactly the wrong input.

**The lesson is the section's own theme pointed at me.** Four times that day a check
passed or failed for a reason other than the one intended, and each time the log told
the truth where the exit code lied. Here the log told the truth and I read my own
corruption back out of it as the tool's. *Evidence produced by the instrument you are
testing, through a harness you wrote minutes earlier, is not independent.* Build
payloads programmatically and confirm a defect against traffic you did not generate —
in this case, the session lines that were sitting in the same file.

Withdrawn with no fix owed. The correction is propagated to the adopter's `spec/SDLC.md`
and to their merged PR, both of which carried the false claim.

### 72.4 Why the kit's own proofs did not catch it

**Corrected: the corpus does have an in-repo absolute case — the bench neutralizes
it.** Case 2c is exactly *"absolute path INSIDE the repo is still production source"*.
It passes on the broken body because `Bench.run` **pins** `SDLC_REPO_ROOT` to the
bench's own Python-flavoured root (`e["SDLC_REPO_ROOT"] = self.root`), so both sides of
the comparison are in the same flavour **by construction** and can never diverge.

No adopter sets that variable. Every one of them takes the `SDLC_REPO_ROOT=$(pwd)`
fallback — the one path the corpus never exercised for classification. A case existed,
a fixture defeated it, and the pass was green for a reason unrelated to the property it
names. That is a sharper and more uncomfortable finding than "the corpus lacked a
case": a fixture convenience silently deleted a control's only coverage.
This is invariant 15 turned on the kit's own tooling: the proof verifies the artifact
and is silent about the environment it will run in. The ninth field report's finding 5
is the same shape — *a fire-proof and a catch-proof are different tests* — one level
further in.

It is also the third instance today of a check passing for a reason other than the one
intended (§70's unpinned `lenses:` anchor, IMPACT's git-ignored fixture bench, this).

### 72.5 Ruled and resolved 2026-08-26/27 — shipped as 0.28.1

1. **Fix shape — the root is resolved in BOTH flavours** (`$SDLC_REPO_ROOT` as given,
   and `pwd -W`), tried in turn, matching on either. One subshell; it cannot regress a
   POSIX host, where the two answers are identical. Proven on a bench where they
   genuinely differ: **3/5 broken, 5/5 fixed**, across backslash-absolute,
   slash-absolute, repo-relative, in-repo test and out-of-repo paths.
2. **Proof-corpus gap — closed, and it was worse than "a missing case".** Case `2c` is
   literally *absolute path INSIDE the repo is still production source*, and it passed
   on the broken body because `Bench.run` **pins** `SDLC_REPO_ROOT` to the bench's own
   root: both sides agree by construction and can never diverge. No adopter sets that
   variable. New cases `24b`/`24c` run with it **unset**, in both path flavours, and a
   mutation dropping the second candidate root is caught **by them**. *A case existed
   and a fixture convenience deleted its coverage* — a sharper failure than absence,
   because the suite named the property and still could not see it.
3. **Release urgency — shipped as its own patch, 0.28.1**, ahead of any further batch.
   Published tarball verified: checksum matches, 44/44, and the shipped guard scores
   **5/5 run out of the downloaded tarball**. The affected adopter re-took the guard
   only after re-proving in their own tree (3/5 → 5/5, deny-armed), which was the
   condition their own spec recorded.
4. **RULED 2026-08-27: the "both dialects" claim needed re-reading, and §64 is now
   corrected.** The Claude dialect's out-of-repo fix was genuinely proven and still
   holds. The Copilot dialect's was proven only against a fixture that could not fail,
   so it **never worked in the configuration adopters run** — 0.25.0 to 0.28.0. §64's
   proof table and its opening claim both carry the correction; nothing else in the
   kit rests on that sentence.

**Two mutations went STALE when the fix restructured their anchor** — *charge
out-of-repo writes as production* and *drop the repo-relative reduction*. The suite
reported them as stale rather than counting them caught, which is the only reason
those two defect classes did not silently lose coverage **inside the patch that
exists because coverage was silently lost**. Both re-pointed; final run 57 cases on
each parser dialect, 21 mutations, 0 stale, exit 0.

**Nothing further is open from this section.** §72.3 was withdrawn on 2026-08-27:
the "log corruption" was my own probe's mangled payload, not a guard defect — see
that section for the measurement and the lesson.

### 72.6 Superseded — the decisions as originally owed

1. **Fix shape.** Normalize the incoming path (`tr '\\' '/'`) **and** resolve the root
   in the same flavour the CLI uses — `pwd -W` where available, falling back to `pwd`,
   or derive it from `git rev-parse --show-toplevel` and normalize both. The fix must
   be proven against a **backslash** path, not a POSIX one.
2. **Proof-corpus gap.** `tdd-guard-check.py` gains Windows-flavoured absolute paths —
   in-repo and out-of-repo, both dialects — and a mutation that deletes the
   normalization must be caught. Without this the fix is unfalsifiable in the same way
   the defect was.
3. **Release urgency.** This is live in four releases and disarms a deny-armed control
   for one of the two adopters. Ship as its own patch release before any further batch,
   or fold into the next? The adopter is holding at 0.24.0's guard body until it is
   fixed **and** re-proven against their path shape, so nothing reaches them until it is.
4. **Whether CLASSIFY's §64 clock is affected.** The out-of-repo classifier was
   field-measured as working on the Claude dialect; on the shell dialect it has never
   worked at all. Any claim resting on "both dialects fixed" needs re-reading.

---

## 73. The medium batch opened — the ninth report's remainder, and its one unruled
## item needs the opposite of the fix it was filed with: narrow the candidates, do not
## widen the window — 2026-08-27

§70.7 ruling 1 sequenced this batch behind the small one and IMPACT. Both shipped
(0.27.0, 0.28.0), the guard re-arm shipped beside them (0.28.1), and both adopters
merged on 2026-08-26 — so this is the last ruled work from the ninth report.

Four items. Three are ruled and need only building; the fourth (finding 5) had no fix
shape, and measuring it before designing one changed the answer.

### 73.1 The three that are ruled, as build notes

- **Finding 1 + ruling 2 — the floor's homes.** `end-phase.md`'s *Coverage floor*
  bullet (line 373) asserts two homes agree — `spec/PROJECT_INDEX.md` **and**
  `spec/SDLC.md` — against the enforcing threshold, while §68's reconcile pass is
  defined over *"Every row of `spec/SDLC.md` Records"*, so a second home elsewhere in
  the same file is outside its population. Ruled (b): the reconcile gains **the value
  search** (find the enforcement artifact's number, then assert no occurrence of the
  old value anywhere in the spec set; failure is a file list), and
  `PROJECT_INDEX.template.md`'s existing one-home prohibition — today one instantiation
  comment about one number, at line 38 — is **generalized to a rule with an observer**.
- **Ruling 3 — stamp the baseline with the commit it was measured at.** §68's *no new
  gate run* stands; the number stops claiming to describe a tree and starts describing a
  commit, and the next close's reconcile reads the drift.
- **Finding 6 — *Risks & Deferred* becomes the reconcile's fourth subject**, beside the
  backlog, *Records*, and the contract-absent direction. Not a new mechanism: the pass
  built in 0.26.0 gains a fourth walk.

Nothing below changes any of those three. They are XS/S and mechanical.

### 73.2 Finding 5, measured over the control's whole installed life

The report measured its own arc. The log is still on disk in the adopter's tree and
covers install-to-date, so the population is enumerable rather than sampled —
`.git/sdlc-close-out/log`, **126 lines** (125 `stop:` lines plus one `docs budget:`
line from the 0.26.0 observer):

| class | lines | what it means |
|---|---|---|
| `clean (no candidate commits)` | **96** (77%) | the window was **empty** — nothing was inspected |
| `clean (0 complete, N bare ...)` | 10 | the window held 1–2 commits, **none carrying a record** |
| `WOULD-BLOCK (bare, log-only)` | **19** | fired — on **2 distinct commits** |
| real catches | **0** | across the control's entire life |

Three facts follow, and the first two are not in the report.

**1. `0 complete`, every single time.** In all 29 stops where the window was *not*
empty, the count of commits carrying a close-out record was zero. The window is not
merely usually empty — **it has never once contained the artifact the mode exists to
inspect.** That is a stronger statement than "the workflow empties it", and it is the
one that decides the fix: `/end-slice` step 7 commits, step 8 runs the fail-closed
`check` on that commit, step 10 pushes. A slice commit is therefore *recorded before it
is pushed and pushed before the session stops*, so it can be in this window only in the
seconds between step 7 and step 10.

**2. The report undercounts its own log by 15 lines and one commit.** It reports *"4
WOULD-BLOCK lines on a single documentation commit."* The log carries **19**, on
**two**: `f419114` x4 and `a5fc4dd` x15, all logged 2026-08-19, both inside the reported
arc. This is the lineage's own theme landing on the report that names it — a number read
off a reading of the artifact rather than off the artifact. It **strengthens** the
finding rather than weakening it.

**3. The 19 lines are 2 events.** `a5fc4dd` is re-flagged at all 15 stops of the session
that made it: there is no de-dup, so the log inflates events roughly 10:1, and a reader
counting lines overstates the false-positive rate by the same factor.

**What the two flagged commits are, checked rather than inferred:**

```
a5fc4dd  docs(sdlc): Phase 08 planned - prompt cache and the real cost per question
         CLAUDE.md | spec/PHASE_08_*.md | spec/PHASE_08_*_NOTES.md | spec/PROJECT_INDEX.md
f419114  docs(phase-08): acceptance 8.1 read the cache - D14 withdrawn, S3 re-scoped
         spec/PHASE_08_*.md | spec/PHASE_08_*_NOTES.md | spec/PROJECT_INDEX.md
```

**Neither touches a single code file.** Both are bookkeeping commits, and the false
positive is the exact shape the script's own comment predicted at build time — *"a docs
commit made in the same session as slice work is a real false-block shape, so this class
logs until proven never to flag one."* The design anticipated it; the field supplied the
count; nothing ever closed the loop.

**4.** Five lines took the `HEAD only, no upstream configured` narrowing. That path is
exercised in the field, not theoretical, and any change must keep it.

### 73.3 What the measurement does to the report's suggested fix

The report proposes: *"Scope `stop-check` to the arc branch's recent commits rather than
to unpushed ones."* On the numbers above that is the wrong direction, for two reasons
that are independent.

**It multiplies the only firings the control has ever produced.** Every firing to date
is a bookkeeping commit. An arc branch contains *more* of them than `@{u}..HEAD` does —
the phase plan, every acceptance record, every close-out docs commit — and none of them
will ever carry a close-out record, because they are not slices. Widening the window
grows the numerator of a control whose numerator is 100% false.

**It breaks the remediation the control prints.** The block reason says *"amend that
commit ... Fix the body before pushing (`git commit --amend` while it is HEAD)"*, and the
comment above the range says so outright: *"unpushed commits - also the remediation
boundary, since the fix is amending a body, legal exactly while unpushed."* On the arc
branch most candidates are already pushed and are not `HEAD`; the instruction becomes
either impossible or a force-push. **The window is unpushed because the remedy is only
legal there.** A fix that widens the window owes a new remedy, and the report does not
supply one.

The measurement points the other way: the window is right and **the candidate set is
wrong.**

### 73.4 Options for finding 5, none ruled

**A. Filter the candidates; keep the window. Recommended.** Skip any candidate whose
changed paths lie entirely inside `spec/` or are the root kit documents (`CLAUDE.md`,
`README.md`) — a bookkeeping commit, never a slice. Verified against the two specimens:
**19 of 19 lines and 2 of 2 commits are eliminated**, driving the false count to zero
without touching the window or the remedy. Two things make this cheap rather than
speculative: the script is copied **verbatim** and carries **zero placeholders**, so a
filter may only use paths the kit itself owns — and `spec/` is exactly that, already
hard-coded in the same file by the 0.26.0 `docs-check` mode (`IDX=spec/PROJECT_INDEX.md`).
The precedent exists. Pair it with the de-dup from 73.2's fact 3 and with a log line
that distinguishes *inspected N, all clean* from *nothing to inspect* — today both print
the word `clean`, which is the finding's opening sentence.

**B. Move the check to pre-push.** Non-empty by construction, and the remedy stays legal
because nothing is pushed yet. But it needs a **git** hook in `.git/hooks/`, which is a
new install surface: not committed, per-clone, invisible to `git clone`, and outside
`.github/hooks/` where every kit-owned hook lives. It also largely duplicates step 8's
fail-closed `check`. High cost for the same target population A already covers.

**C. Widen to the arc branch, and rewrite the remedy** (amend while unpushed and `HEAD`;
otherwise a follow-up correction commit, or defer to the phase-close reconcile). This is
the report's fix made coherent. It is strictly more work than A, and per 73.3 it is only
safe *combined* with A's filter — so it is A plus a remedy rewrite, not an alternative
to it.

**D. Delete `stop-check`.** Defensible on the kit's own clock discipline: 125 stops, zero
catches, every firing false, and §52.2's arming bar (**zero** false candidates) is unmet
by 2 events. The report considered deletion and declined it at interview because the
command-step `check` is fail-closed and separate and went 8/8. The counter-argument the
numbers now supply: the target population — a session that stops between step 7 and step
10 — **has never been observed to occur**, so what would be deleted is a control with no
demonstrated demand as well as no demonstrated reach.

**The recommendation is A, plus the honest log line, plus the de-dup — and then a
pre-registered clock rather than a verdict**, because A is what makes the clock readable
at all: with the false count at zero the bare class becomes armable for the first time,
and a control that goes two more field arcs with no catch gets D applied on evidence
instead of on argument. That sequencing also unblocks §70.7 (5)(iv), which ruled the
arming question closed until finding 5's scope fix lands.

**One property worth stating because it does not hold for the guard:**
`.github/hooks/sdlc-close-out.sh` is **kit-owned and copied verbatim**, so unlike the
TDD guard's instantiated body this fix *does* reach both adopters by ordinary
`/sdlc-update`. No hand-application, no transition note.

### 73.5 The catch-proof half, which is not finding 5's and is the larger half

The report's transferable sentence — **a fire-proof and a catch-proof are different
tests** — is about *Records*, not about `stop-check`. The adoption's row reads *"a fresh
headless session's stop executed the block fail-open and wrote its classification to the
log"*: proof the hook **ran**, recorded as though it settled whether the hook could ever
**catch**. `SDLC.template.md` seeds that wording (line 257: *"Installed: which CLIs, the
fire-proof actually ..."*).

**Corrected while building, and the correction makes the finding sharper rather than
smaller.** The draft of this section claimed the kit demands a catch-proof only for the
coverage floor and for none of its own controls. **That is false, and reading
`sdlc-setup.md` before writing the fix is what caught it.** Every install proof in the
kit is already a catch-proof, and each says so in the same words — *"Prove them the way
every other check is proven — by making them fail"*: the TDD guard's is a production
write with no failing test, seen to be named in the log; the checker's is a commit with
no record, seen to exit 1 INCOMPLETE naming all five keys; and the backstop's is *"end a
session in a repo whose HEAD is an unpushed commit missing a record key and confirm the
log holds `stop: WOULD-BLOCK - defective record` naming the commit."*

So the adopter's row did not follow a weak rule — **it under-recorded a strong one**, and
`SDLC.template.md` invited that by calling the result *the fire-proof* (line 257) when
what it demands is a catch. That much is a naming fix.

**The real gap is the one neither word covers, and the backstop is its perfect
specimen.** Its install proof genuinely catches — because the operator *constructs* an
unpushed commit missing a key. In ordinary operation `/end-slice` commits, checks and
pushes in one step, so that state essentially never arises: 96 of 125 stops had nothing
in the window at all. **The proof builds the very population whose natural occurrence is
the open question.** That is §72's lesson one level up — there a fixture pinned
`SDLC_REPO_ROOT` so both sides agreed by construction; here a proof constructs the
violation it then catches. A catch-proof establishes the control *can* fire; it says
nothing about *reach*.

So the batch's portable change is a third thing recorded beside the other two — a
**reach note**: whether the flagged state arises in ordinary operation, or was built for
the proof. *"Constructed for the proof; not yet observed arising on its own"* is a
legitimate answer, and unlike the two proofs it is a claim the next close can check. It
is prose in *Records* plus one clause in each install step, not a mechanism.

### 73.6 Cost, named up front

| item | where | size |
|---|---|---|
| Finding 1 — value search + generalized one-home rule | `end-phase.md`, `PROJECT_INDEX.template.md` | S |
| Ruling 3 — baseline commit stamp | `SDLC.template.md`, `end-phase.md` | XS |
| Finding 6 — *Risks* as the reconcile's 4th subject | `end-phase.md` | XS |
| Finding 5 (option A) — filter + de-dup + honest log | `close-out.template.sh` | S |
| Finding 5's proof — a **catch** case, not a fire case | `tools/close-out-check.py` | S |
| The reach note in *Records* (+ catch-proof naming) | `SDLC.template.md`, `sdlc-setup.md` | S |

The proof row is not optional and is the reason finding 5 is S rather than XS: a filter
that silently skips too much is the same defect one layer down, and §72's lesson is that
a fixture which cannot fail is worse than a missing case.

**Checked rather than assumed, and it inverts the expected gap.** The suite's 15 stop
cases *do* prove the mode catches — `stop_defective_logs_wouldblock`,
`stop_bare_with_guard_flagged`, `stop_defective_armed_blocks`,
`stop_defective_below_head_flagged` all assert a flag on a commit that earned one. What
the corpus contains **no case of** is the thing the field produced 19 times: **a
bookkeeping commit present in the window that must NOT be flagged.** Every case pins
what the mode fires on; not one pins what it must stay silent about. That is the same
shape as §72's case `2c` — the corpus names the property and cannot see the failure —
and it is why the filter's proof must be a **negative** case (`spec/`-only commit in the
window, `WOULD-BLOCK` absent, alongside a code commit in the same window that is still
flagged), not another firing case.

### 73.7 Decisions owed

1. **Finding 5's shape** — A (recommended), B, C, or D. A is measured to eliminate 19/19
   false lines with a discriminator the file already uses.
2. **Clock or verdict.** With A, does `stop-check` go on a pre-registered two-arc clock
   (no catch → delete, per D), or is it simply kept? The recommendation is the clock,
   pre-registered here.
3. **Does the catch-proof requirement generalize** to every installed control in
   *Records*, or only to the close-out hook? Recommended: generalize — it is the
   report's own transferable sentence, and the coverage floor already proves the shape
   works.
4. **Release shape** — one 0.29.0 carrying all four items, or the three ruled ones now
   and finding 5 behind its decision.

### 73.8 Ruled 2026-08-27 — all four, each as recommended

1. **Finding 5 — option A: narrow the candidates, keep the window and the remedy.** A
   candidate whose changed paths lie entirely inside `spec/` or are the root kit
   documents (`CLAUDE.md`, `README.md`) is a bookkeeping commit and is skipped before
   classification. With it: de-dup, so a commit already logged in this session is not
   re-logged (73.2's fact 3, measured at 15 lines for one commit); and the log line
   splits, so *inspected N, all clean* and *nothing to inspect* stop printing the same
   word — which is the sentence the finding opens with.
2. **A pre-registered two-arc clock, not a verdict.** Written out below, because a clock
   whose denominator is unstated is the defect §70.7 (5)(i) had to rule around.
3. **The catch-proof generalizes to every installed control.** *Records* carries a
   catch-proof beside the fire-proof for each control it lists — the report's own
   transferable sentence, and the coverage floor's *prove it fires — once* is the
   working precedent.
4. **One release, 0.29.0**, carrying all four items plus the catch-proof half, with the
   pre-tag `/kit-check` over the combined scope.

**The clock, pre-registered.** Two field arcs run under the release carrying the filter.

- **Denominator, and it is now readable, which is the point of the split log line:** an
  arc's denominator is the number of stops whose window was **non-empty**. The old log
  could not supply this — 96 empty and 29 inspected stops printed the same verdict.
- **Positive (the catch):** at least one arc in which `stop-check` flags a commit that
  genuinely lacked its close-out record and was a slice commit rather than bookkeeping.
- **Failure by falsity:** a false candidate in either arc fails §52.2's arming bar. The
  filter is incomplete, gets fixed, and the clock **restarts once**. A second false
  candidate after that is deletion — the same evidence D rests on, arrived at honestly.
- **Failure by unreadability, and it is deliberate:** if both arcs close with a
  denominator of **zero**, the clock is not extended — it is **deletion**. A window that
  never contains anything is precisely the finding, and letting an unreadable clock run
  forever is how this control reached 125 stops without a verdict.
- **No catch across two readable arcs → delete `stop-check`** (option D). The
  fail-closed `check` at `/end-slice` step 8 is untouched by any outcome here; it is a
  separate control and went 8/8 in the field.

**Not ruled here, because it is not owed yet:** whether the bare class arms. §70.7
(5)(iv) closed that question until this fix lands; it re-opens at the first arc whose
false count is zero, and not before.

### 73.9 Built 2026-08-27 — and three things the building found

All four items plus the reach note, shipped as 0.29.0. The parts that went as ruled are
in the CHANGELOG; what follows is only what the build learned that the design did not
know.

**1. The first cut of the filter cost 3.5 seconds, and the measurement is the only
reason it is not in the release.** Reading each candidate's paths took a second `git
show` beside the body's `git log`, i.e. **two processes per candidate** — and this file
already carries a warning about exactly that, from 2026-08-10: a grep-per-counter draft
cost ~1.7 s per invocation on Windows, which is why the ten counters share one awk pass.
Measured on a purpose-built 20-candidate repo, five runs each:

| variant | 20-candidate walk |
|---|---|
| no filter at all | 4188 ms |
| filter as first written (two processes per candidate) | **6868 ms** |
| filter folded into the body read (one process) | **4186 ms** |

The stop path runs inside a **30 s hook timeout** and the cap is 20 candidates, so this
was real and not noise. The fix reads body and paths from **one** `git show
--name-only --format='%B%n<marker>'` and classifies both in the existing awk, which
also means the filter now costs *nothing measurable* — 4186 against 4188. §71's ruling
was that a timing wobble must not suppress a correctness pass; it was never that timing
stops mattering, and the S2 budgets are what surfaced this.

**2. It was caught by measuring, not by reviewing.** The suite went green with the slow
version — every case passed, all 28 mutations caught — and the only signal was an S2
budget this repo has documented as unreliable on this machine. Had §71's fix not landed
first, the run would have exited at the budget **before the mutation pass**, and the
slow version would have shipped with a weaker result than the fast one. §71 paid for
itself inside one batch.

**3. A `git show --name-only` on a merge commit prints no paths**, so a merge falls to
"not bookkeeping" and stays a candidate — the safe direction, and the same one an empty
commit takes. Every existing stop case in the corpus commits `--allow-empty`, so **all
fifteen of them are pathless**, which is why the filter had to grow `commit_files`
before its own cases could exist. That is the same shape as §72's case `2c`: the bench
could not construct the input the defect needed.

**On the corpus gap, corrected from 73.6.** The expectation was that the suite would
lack a catch case. It had four. What it lacked was any case pinning what the mode must
stay **silent** about — the exact configuration behind 19 of 19 field firings. Five
cases and five mutations close it, and three of those mutations had to be re-pointed
when the one-process refactor moved the lines they targeted, which is 0.28.1's lesson
arriving on schedule.

---

## 74. LENS opened — mechanical counterparts for the review lenses: what a linter can
## decide, what needs a reference index, and what the code graph must never be asked —
## 2026-08-29

Opened on the owner's question of 2026-08-29: give the review lenses concrete checks to
work with, with Language Server Protocol named as the vehicle and Understand Anything's
knowledge graph raised as the cheaper follow-up. Both were **measured before anything
was designed**, and the measurement reorders the work: the substrate the question
started from cannot produce a check at all, the substrate nobody proposed is the
strongest and is already in the tree, and the third is disqualified for this use by its
own edge census. The theme continues §73's — *a control's proof constructs the state it
catches* — one step earlier: **an instrument's input is not its denominator, and
improving what a lens can see does nothing about a lens nobody can tell whether it
ran.**

### 74.1 The three substrates, measured

**(a) Linter rules — deterministic, already installed, already the best performer.**
`reference/GATE_RECIPES.md`'s *Runtime-standards rules* already names per-language rule
IDs whose subject matter is three of the eight lenses': ruff `E722`/`BLE001`/`B904` and
the bandit `S` family; ESLint `no-empty`, `no-eval`,
`@typescript-eslint/no-floating-promises`; `CA1031` with `-warnaserror`; checkstyle
`EmptyCatchBlock` + `IllegalCatch` with find-sec-bugs. Deterministic, versioned, same
input to same output, and enforced by the gate and the edit-time hook with no new
command.

**(b) LSP — real on both CLIs as of 2026-08, and asymmetric.** Claude Code configures
servers by plugin: `.lsp.json` at the plugin root or an inline `lspServers` object in
`plugin.json`, `command` + `extensionToLanguage` required, and a `diagnostics` field
(default `true`) that pushes diagnostics into context after edits. Project scope exists
— `claude plugin install <name> --scope project` writes `enabledPlugins` into
`.claude/settings.json`, so it travels with a clone — but **servers start only after the
workspace is trusted**. Copilot CLI takes `.github/lsp.json` (project, travels with a
clone) or `~/.copilot/lsp-config.json` (user): an `lspServers` map of `command`, `args`,
`fileExtensions`, with `/lsp show`, `/lsp test <name>`, `/lsp reload` to verify. Its
documented capability set is **navigation** — definition, references, hover, rename,
document and workspace symbols, implementation, incoming/outgoing calls — and **lists no
diagnostics**.

Neither CLI bundles servers. Of the owner's four languages, Python (pyright) and JS/TS
(typescript-language-server) are turnkey on both sides; **Java (jdtls) and C# (Roslyn LS
/ OmniSharp) are custom configuration on both sides and pull a JDK or a .NET SDK onto
every adopter machine.** The kit's entire runtime dependency list today is git, `sh`,
python, and a JSON parser.

Decisive for the question as asked: **neither CLI exposes a non-interactive LSP query.**
GitHub's documentation describes no programmatic interface; Claude's is a model-facing
tool. An LSP-backed lens yields no exit code, no countable denominator, and nothing
`tools/` can drive — invariant 13 gets no purchase on it and §73.8's catch-proof cannot
be satisfied. LSP improves what a reviewer sees; it is not a check.

**(c) The Understand Anything graph — disqualified for reference resolution, measured.**
Measured on the frozen real pair (`impact-fixture-source/knowledge-graph.json`, UA
2.9.4, TFit at `d75d9cf`, 116 files): 331 nodes, 544 edges. Edge census: `contains` 215,
`exports` 90, `imports` 76, `tested_by` 38, `related` 37, `documents` 33, **`calls`
31**, `depends_on` 9, `inherits` 6, `configures` 6, `deploys` 2, `triggers` 1.

- 183 function nodes; **17 (9%) are ever the target of a `calls` edge**; 7 are the
  source of one.
- 210 symbol nodes (function + class); **116 (55%) carry no incoming edge other than the
  structural `contains`.**

Ask that graph whether anything consumes a given function and it answers **no** for
roughly nine functions in ten that are in fact called. The *unconsumed artifact* lens's
failure mode is precisely a false "no consumer" claim, and the lens's own recorded
specimen is one: a status entity with no production writer, filed as dead and deleted.
Wiring the graph in as the authority would industrialize the defect the lens exists to
catch.

It is also the wrong *kind* of artifact. Nodes carry `summary`, `tags`, `complexity`,
`languageNotes` — prose — and import edges carry `"weight": 0.7`, a heuristic. It is a
model-authored architectural narrative pinned to a commit hash, not a resolved index, so
two regenerations of one tree need not agree and a check built on it has **no stable
denominator** — the exact defect §54 put three lenses on a clock for. Staleness
compounds it where it matters most: `SOURCE.md` preserves the quirk deliberately —
`usage_pricing.py`, four new test files, the Phase 08 spec and `.claude/settings.json`
all in `changedFiles` with no matching node. The unconsumed-artifact lens asks about
artifacts *the arc just introduced*, which are by construction the nodes a pre-arc graph
cannot hold.

**§66 already ruled this correctly and proved it.** The adapter walks *any* edge type
one hop rather than trusting `calls`; responsibilities 6 and 7 make unmatched files and
staleness loud; `tools/impact-check.py` carries a mutation named
`partial_reported_as_complete`. Promoting the graph to a reference authority for a lens
would contradict a decision the kit has already proof-tested.

### 74.2 What §54 already measured, and why it sets the order

> **Runtime-standards recipe — CONFIRMED CATCHES, KEEPS.** … The recipe is the
> lineage's best-performing rule, and its thesis — mechanize what can be mechanized —
> is the one every field report keeps re-proving.
>
> **The three lenses — zero attributed catches in three arcs; deletion candidates.**

The three lenses on that clock are *logging and swallowed errors*, *untrusted input*,
and *secrets and exposure* — and GATE_RECIPES already names mechanical rules covering
all three subjects in every language the kit carries a gate recipe for. For the three
lenses closest to deletion, the mechanical counterpart lives in the same repository,
covers the same subject matter, and is the artifact that actually caught things. That
reframes the question this section opened with: not *how do we feed these lenses better
data*, but **what is the residue a rule cannot express, and has anyone written it
down?**

### 74.3 Step 1 — the lens↔rule map

For each of the eight lenses × each language carrying a gate recipe (Python, TS/JS, C#,
Go, Java, Rust), state which part of the lens mechanizes, name the rule ID, and state
what is left over for the reader. Expected shape from the current lens text — to be
derived at build time, not from this list (§4a):

- **fully mechanizable:** logging and swallowed errors; secrets and exposure
- **partly:** error propagation; untrusted input
- **not:** verify the denominator; shared state under concurrency beyond what SpotBugs
  and the Roslyn analyzers already offer; the disposal-intent test and the unconsumed
  artifact — the last two for the reason step 2 addresses

It lands in *Runtime-standards rules*, which is **adoption-only** — read at
`/sdlc-setup`, never re-applied — so it cannot disturb an arc in flight. Setup already
consumes that section in both modes (New mode's Round 2; Existing mode's measured
violation-count delta), so the plumbing exists and the cost is the table plus at most
one sentence. The recipe's existing fire-proof — "one deliberate violation must fail the
lint run" — stays as written.

### 74.4 Step 2 — LSP find-references, as a pre-registered trial

Both kit-written reference lenses turn on *does anything still reference this?*, and
`REVIEW_LENSES.md` already concedes that its own recommended method is unreliable:

> a caller-grep undercounts — a framework-wired reader is a consumer the grep never sees

That is the one question grep structurally cannot answer, and it is where the confirmed
catches are: the seventh report's only lens-named catch was `unconsumed artifact`.

Scope: those two lenses only; Python and JS/TS only; Java and C# held pending a measured
startup cost, since jdtls and the Roslyn server are the two that add a language runtime
to the adopter's machine and the two with no official plugin on either side. Honest
bound, stated before the trial rather than after: **LSP narrows the framework-wiring gap
and does not close it** — Spring annotation wiring, DI by configuration, and reflection
stay invisible. The claim under trial is *fewer false "no consumer" calls*, never *a
correct denominator*.

This runs under §5's trial-protocol rule (pre-registered value criterion), **not** the
ENF ramp: nothing here is enforcement, so there is no logging trial, no arming bar, and
no deny ramp. Delivery asymmetry is the build's main cost and its main hazard — Copilot
takes a `.github/lsp.json` the kit writes into a directory it already owns; Claude Code
takes a plugin install plus a workspace-trust gate whose failure mode is the server
simply not starting, which is the silent-inertness shape §61 and §72 both paid for. Any
offer must state how the adopter checks it is live (`/lsp show`, `/lsp test`, the
`/plugin` Errors tab).

### 74.5 Step 3 — the UA graph as lens triage, never as verdict

74.1 (c) disqualifies the graph as an authority. It has a cheaper role the adapter's
existing read already pays for: choosing *where to look*.

- **`tested_by` (38 edges)** is a signal LSP does not supply at all — production symbols
  with no test edge, as a place to look first.
- **File-level `imports`** (76 edges over 67 file nodes) is the densest and most
  trustworthy layer, and is already what blast radius uses.
- **`tags`** (`entry-point`, `api-handler`, `tested`) can inform *which lenses are worth
  running on this diff* — a triggering question, not a concluding one.

The rule, and it must appear in any text that ships: **the graph chooses where to look;
a deterministic check decides what is true.** Sparsity is survivable for ranking and
fatal for verdicts, and an unqualified sentence here is one the next reader promotes.

### 74.6 The clock collision, and why step 1 clears it

The three STD lenses sit on a final two-arc clock, re-started 2026-08-26 (§70.7 (i))
from the first arc whose denominator is enumerable; the instrument that makes it
enumerable — the `lenses:` close-out key — shipped in 0.27.0 and no arc has closed under
it yet. Editing those three lenses now would restart that clock a third time, which is
the failure the re-start was itself a response to.

Step 1 does not touch them. It lands in an adoption-only reference doc;
`REVIEW_LENSES.md` — the one installed reference file — is untouched; and an existing
adoption's linter config is unaffected, because rules are adopted per project at setup
or gate time and never re-applied. The map can therefore be built now and the clock
still reads on schedule.

The map also improves the ruling when the clock does read: "delete or keep" becomes "is
the residue this rule cannot express worth a lens?" — a question with an artifact behind
it.

### 74.7 Cost named up front

**Step 1:** `reference/GATE_RECIPES.md` (*Runtime-standards rules* — the map); at most
one sentence in `commands/sdlc-setup.md`, both modes already reading the section; a
`/kit-check` consistency rule (every lens with a mechanizable half names a rule for each
language carrying a gate recipe, and no rule is named for a language with no recipe). No
new files, both READMEs untouched, `[adoption-only]`.

**Step 2:** a new offer and decline record in `commands/sdlc-setup.md`; a
`.github/lsp.json` template plus the Claude-side plugin instruction;
`reference/COPILOT.md` mapping rows; both READMEs' trees; MANIFEST regenerated.
`[installable]`, and the first kit feature ever to require a per-language binary the kit
does not ship.

**Step 3:** text only, inside the lens hand-back `/end-phase` already prints.

### 74.8 Value criteria, pre-registered

- **Step 1:** a field arc in which a rule adopted from the map fires on a defect whose
  lens would have been the only other detector. Failure: two arcs in which the map's
  rules add violations but no arc records a catch attributable to a rule the map added —
  the map is then documentation, and documentation of rules is what GATE_RECIPES already
  was.
- **Step 2:** an `unconsumed artifact` or `disposal-intent` finding in a field arc that
  names find-references as its method **and** records that a caller-grep would have
  missed it. Failure by falsity, and it is the one that matters: any arc in which an
  LSP-sourced "no consumer" claim proves wrong closes the trial. A reference index that
  produces a confident wrong answer is worse than a grep that produces an admittedly
  uncertain one — that is the whole of 74.1 (c), turned on the replacement.
- **Step 3:** an arc whose lens hand-back names a graph-sourced starting point for a
  finding something else then confirmed. Explicitly the weakest of the three: "helped
  the reviewer look in the right place" is the unfalsifiable claim §54 went looking for
  and could not find, so this gets **one** arc and is dropped if the record cannot carry
  it.

### 74.9 Owner decisions owed before the build

- **(a) Sequencing.** Step 1 now with steps 2 and 3 behind it (recommended — step 1 is
  deterministic, dependency-free, adoption-only and clock-safe, and it is the only one
  of the three that answers the question as the owner posed it); or all three as one
  batch; or step 2 first, on the grounds that the two reference lenses are where the
  confirmed catches already are.
- **(b) Map breadth.** All six languages carrying gate recipes (recommended — Go and
  Rust rows already exist in the runtime-standards list, and omitting them creates the
  asymmetry the next reader files as a finding); or the owner's four (Java, Python, C#,
  JavaScript); or only the two step 2 would also cover.
- **(c) The catch-proof question.** Does §73.8's generalization require anything beyond
  the recipe's existing fire-proof for a lint rule? Recommended: **no, and say so in one
  sentence** — for a rule the deliberate violation is both proofs at once, and leaving
  it unstated invites a later reader to invent a second ritual.
- **(d) Step 2's scope if it runs.** Python + JS/TS only, Java and C# held pending a
  measured jdtls/Roslyn startup cost (recommended); or all four at once; or decline the
  LSP direction and keep steps 1 and 3.
- **(e) Whether step 3 ships at all.** Its criterion is the weakest by construction. One
  arc and drop (recommended), or hold it entirely until step 1's criterion reads.

### 74.10 Ruled 2026-08-29 — all five; step 1 builds now and the other two stay filed

1. **Sequencing — RULED (a): step 1 now, steps 2 and 3 behind it.** The lens↔rule map
   is deterministic, dependency-free, adoption-only, and the only one of the three that
   answers the question as it was posed. It is also the clock-safe move: it lands in
   `reference/GATE_RECIPES.md` and leaves `REVIEW_LENSES.md` — the installed file
   carrying the three STD lenses on their final two-arc clock — untouched, so the clock
   re-started 2026-08-26 still reads on schedule under the `lenses:` key that shipped in
   0.27.0 and has not yet had an arc close under it.
2. **Map breadth — RULED (a): all six languages carrying a gate recipe.** Python,
   TypeScript/JavaScript, C#, Go, Java, Rust. Go and Rust rows already exist in the
   runtime-standards list; a map that skipped them would be the asymmetry the next
   reader files as a finding, and the marginal cost is two columns of rule IDs.
3. **The catch-proof question — RULED (c): no new ritual, said in one sentence.** For a
   lint rule the deliberate violation is the fire-proof and the catch-proof at once —
   the state it flags is the state that was constructed — so §73.8's generalization is
   already satisfied by the section's existing *prove the adopted set* paragraph. Saying
   so explicitly is what stops a later reader inventing a second ceremony for it.
4. **Step 2's scope if it runs — RULED (d), and it is now moot until step 1's criterion
   reads.** Recorded so the answer is not re-derived: Python + JS/TS only, with Java and
   C# held pending a measured jdtls/Roslyn startup cost, because those two add a JDK or
   a .NET SDK to every adopter machine and the kit's whole runtime dependency set today
   is git, `sh`, python, and a JSON parser.
5. **Step 3 — RULED (e): one arc, then dropped if the record cannot carry it.** Held
   with step 2. Its criterion is the weakest by construction and 74.1 (c) is the reason:
   a graph that answers "does anything consume this?" with *no* for nine called
   functions in ten cannot be promoted past triage on a claim as unfalsifiable as
   "it helped the reviewer look in the right place."

**Built by this batch:** the map itself in `reference/GATE_RECIPES.md`; one sentence in
`commands/sdlc-setup.md` pointing both modes at it; and a `/kit-check` consistency rule.
Nothing installed changes shape, no new placeholder, no new file.

---

## 75. The skill-ledger proof has been dead since 0.24.0 — the batch that caught one
## proof rotted by the launcher split introduced the same rot in the tool beside it,
## and six releases of `/kit-check` read it as sound — filed 2026-08-29

Found 2026-08-29 by running the `tools/` suites during a readiness review, which is the
first time all six have been run in one sitting. Five hold. The sixth has not completed
a run since 0.24.0 shipped on 2026-08-15. The artifact it proves is sound — that was
established separately, and 75.2 says how — so this is an instance of the class §61.4
named at its own meta-level: *a proof that certifies the wrong artifact is a hook that
never fires, one level up.* Here it is one level up again, because the reading pass that
should have noticed cannot notice this kind of failure at all.

### 75.1 What was measured

`python tools/skill-ledger-check.py`, run at `d014dc2`. The six Copilot cases pass. Then:

```
FAIL  claude: valid payload appends an ISO-stamped line, exit 0
        - rc=127 err=sh: .github/hooks/sdlc-skill-ledger.sh: No such file or directory
Traceback (most recent call last):
  File "tools/skill-ledger-check.py", line 121, in main
    n = io.open(ledger_of(repo2), encoding="utf-8").read().count("\n")
FileNotFoundError: ... proj2/.git/sdlc-skill-ledger.jsonl
```

The mechanism: `load_bodies()` returns `blocks[0]["hooks"][0]["command"]` from
`settings.template.json`'s `Skill` block, and `run()` executes that string as the hook
**body**. Since 0.24.0 the string is a bare launcher — `sh
.github/hooks/sdlc-skill-ledger.sh` — and the body it used to hold moved to
`templates/skill-ledger-claude.template.sh`. The suite now drives a path that does not
exist in its own bench, and the uncaught `FileNotFoundError` **aborts the run**, so the
three Claude cases after the failure — second-line append, unset `CLAUDE_PROJECT_DIR`,
`CLAUDE_PROJECT_DIR` without `.git` — have not executed since either. One dialect of one
control has been entirely unexercised for two weeks and six releases: 0.25.0, 0.26.0,
0.27.0, 0.28.0, 0.28.1, 0.29.0.

### 75.2 The shipped artifact is sound, established separately

`templates/skill-ledger-claude.template.sh` was driven directly against the same
measured payload rather than inferred from reading it. With `CLAUDE_PROJECT_DIR` set to
a repo root it appends one ISO-stamped line carrying the payload verbatim and exits 0;
with it unset it prints `SDLC skill ledger did NOT record this activation: ...` on stderr
and exits 2. Both branches behave as the artifact's header claims.

And the artifact has not moved: `git log v0.24.0..HEAD` over both
`skill-ledger-claude.template.sh` and `skill-ledger.template.json` is empty. So the
exposure is **six releases shipped with a control unproven**, not a defect that slipped
past a dead proof. That is the §72 distinction landing the other way this time, and it
is the reason this is filed rather than hot-fixed: the loss is coverage, not
correctness.

### 75.3 Why the kit's own checks did not catch it, which is the larger half

**(1) `/kit-check` reads; it does not run.** The command opens by declaring itself "an
agent **reading pass**, not a grep suite", and invariant 13's enumerated population
explicitly includes "the `tools/` proof suites". Reading a suite establishes that it
*states* its negative cases. It cannot establish that it *executes*. And
`skill-ledger-check.py` still reads as a model proof: payload fixtures measured on the
bench rather than invented, both dialects' loud branches exercised, a newline assertion
carrying its own reason. Every pre-tag pass since 0.24.0 would have read it and passed
it — §65, §69, and the 0.27.0 and 0.28.0 passes among them. This is the command's own
prime directive — *an all-clear from a check that cannot fail proves nothing* — turned
on the command itself.

**(2) The commit that broke it is titled for catching the same defect next door.**
`19a2a7a` (PIN, §61) reads "…the proof tool's index decay caught with it": it found
`gate-hook-check.py` driving a `PostToolUse` index that 0.21.0 had silently re-pointed,
and repaired it to locate blocks by matcher and read the body from its new template
home. That tool's docstring now documents the split verbatim ("split 2026-08-15"). The
suite sitting beside it in the same directory, reading the same file for the same
reason, was never opened. §4a's rule — derive the edit map mechanically, never from the
plan's own list — was applied to the batch's **product** and not to its **proofs**, and
the batch's own finding was the strongest available signal that the proofs were in
scope.

### 75.4 Scope, checked rather than assumed

Two suites read `settings.template.json`: `gate-hook-check.py` (fixed in 0.24.0) and
`skill-ledger-check.py` (this defect). The other four each read a single-body template
that was never split — `close-out.template.sh`, `sdlc-impact.template.py`,
`tdd-guard.template.sh` + `.json`, `tdd-guard-claude.template.py`. **There is no third
instance of this defect.**

The general defect in 75.3 (1) covers all six, and the other five were run the same day
to bound it: `gate-hook-check` OK; `tdd-guard-claude-check` OK, mutations caught;
`tdd-guard-check` 57 cases under each of two parsers, all passed, mutations caught;
`impact-check` 17 cases and 13/13 mutations; `close-out-check` 53 cases (26 unit, 7
docs, 20 stop) with 18/18 mutations, 0 survivors, 0 stale, correctness green and only
the §71 timing budgets breached — under three concurrent suites, which is the load §71
described. That run is also the first field exercise of §71's fix: the budgets were
missed and the mutation pass still completed, which under the pre-§71 code it would not
have.

### 75.5 The fix, and the open half

The artifact fix has one shape, and it is the sibling's:

- read the Claude **body** from `templates/skill-ledger-claude.template.sh`;
- keep locating the `Skill` block by matcher (already done) and **assert the block's
  command is a bare launcher naming that file** — the property `gate-hook-check.py`
  already pins for the gate, so the split cannot silently reverse;
- keep the launcher itself under test rather than merely unused: assert the path it
  names is the file `sdlc-setup.md` installs.

The open half is what makes a dead suite loud. Options:

1. **`/kit-check` runs the suites and quotes their exit codes.** One step; invariant
   13's population already names them; it closes exactly the measured failure mode.
   Cheapest. **Recommended.**
2. **A release-step gate.** Stronger — it cannot be skipped by scoping `/kit-check` to
   selected entries — but there is no release script to hang it on today, so it would
   ship as prose, which is the thing this repo keeps concluding does not work.
3. **Both**, 1 as the routine pass and 2 as the tag-time backstop.
4. **Neither; re-run by habit.** Recorded so it is not rediscovered as an option: it is
   what has been in force since 0.14.0, and it produced this section.

### 75.6 Decisions owed

- **(a) Fix shape.** All three bullets above (recommended — the middle one is what
  prevents the recurrence, and it costs one assertion); or minimal, re-pointing at the
  body file and leaving the launcher unpinned.
- **(b) Loudness.** Option 1 (recommended), 2, 3, or 4.
- **(c) Does §71's accumulate-don't-short-circuit fix generalize?** This suite *aborted*
  on an exception rather than reporting and continuing, which is why three cases
  vanished silently rather than failing visibly. Recommended: **generalize the crash
  half only** — an unexpected exception in one case reports and the run continues; the
  timing-budget half stays with `close-out-check.py`, the only suite that has budgets.
- **(d) Release shape.** `tools/` is kit-development only, so a fix there carries **no
  VERSION bump** (the `b6a81a9` precedent, which said so explicitly). Recommended: fold
  into whatever ships next; nothing installed changes.
- **(e) Does the unproven window need a note where adopters read?** Recommended: **no.**
  The artifact never changed and never failed, and the CHANGELOG's entry classes are
  `[installable]` and `[adoption-only]` — both defined by what an adopted project holds.
  A note about a kit-development proof would be the first entry in that file about
  something no adopter has.

### 75.7 Ruled 2026-08-29 — all five; the fix and its loudness ship together

1. **Fix shape — RULED (a): all three bullets.** The suite reads the Claude body from
   `templates/skill-ledger-claude.template.sh`; it asserts the `Skill` block's command
   is the bare launcher naming that file — the property `gate-hook-check.py` already
   pins for the gate, so the split cannot silently reverse a second time; and it asserts
   the launcher's path is the one `commands/sdlc-setup.md` installs, so the launcher
   stays under test rather than merely unused. The middle bullet is the one that
   prevents the recurrence and it costs a single assertion.
2. **Loudness — RULED (b), option 1: `/kit-check` runs the suites and quotes their exit
   codes.** Invariant 13's population already names the `tools/` proof suites, so this
   is the population's own check finally executing rather than a new obligation. It
   closes exactly the measured failure mode: a suite that cannot complete now reports a
   nonzero code into the pass that has been reading it as sound for six releases. The
   step carries the runtime facts measured 2026-08-29 — the guard suites sleep 1.1 s per
   case, `close-out-check.py` ran ~70 minutes under concurrent load, and all six buffer
   stdout, so they run with `python -u` — because a step whose cost surprises the runner
   is a step that gets skipped, and skipping is what option 4 already proved.
   Option 2 stays refused for the reason it was filed with: there is no release script
   to hang a gate on, so it would ship as prose.
3. **The crash half — RULED (c): generalize it, and only it.** An unexpected exception
   in one section now reports as a `CRASHED` line and the run continues to the next,
   with the exit code carrying it; the run no longer ends at the first traceback taking
   every later case with it silently. This is §71's accumulate-don't-short-circuit
   applied to the failure shape that produced §75, and it goes into **all six** suites,
   because the property that made this invisible — cases that never ran also never
   printed — is a property of the harness, not of this suite. The timing-budget half
   stays where it is: `close-out-check.py` is the only suite with budgets.
4. **Release shape — RULED (d): no VERSION bump for the `tools/` half.** `tools/` is
   kit-development only (invariant 12), so the suite fix and the crash guard change
   nothing an adopter holds — the `b6a81a9` precedent, which said so explicitly. They
   fold into whatever ships next, which is this batch's §74 step 1.
5. **A note where adopters read — RULED (e): no.** The artifact never changed and never
   failed across the unproven window, and both CHANGELOG entry classes are defined by
   what an adopted project holds. An entry about a kit-development proof would be the
   first in that file about something no adopter has.

---

## 76. The tenth field report triaged — all six stand, three need their fix re-aimed,
## and a seventh finding the report did not make sits on a final clock — 2026-09-01

`FIELD_REPORT_2026-09-01.md` (`sdlc-kit#10`, filed 2026-09-01) is the **tenth** field
report and the **seventh** from the first adopter, covering their Phase 09 — 7 slices, 23
commits, 1 PR — written against **0.30.0**, which is genuinely what they run: the 0.30.0
update landed, was re-stamped when the first attempt did not take, and the whole arc ran
under it. Six findings, a priority table, two findings withdrawn by the report itself.

**This is the first report in the lineage with no collision.** Every prior report since
the seventh arrived against a release two or more behind and spent most of its triage on
findings already fixed. This one is current: nothing in it is closed by shipped work, no
premise is false against the text it quotes, and no suggested fix is an option already
ruled against. What the triage owes instead is **aim** — three findings name the wrong
file, the wrong trigger, or claim more damage than the artifact allows — plus one finding
the report missed.

**Its theme, and it is the sharpest statement of the lineage so far:** *a rule that lives
in only one artifact erodes silently, and the kit's own controls are now the main source
of that erosion.* The eighth report said the kit never makes a number reconcile; the
ninth said the kit never verifies a step could have caught anything; this one says the
kit **splits contracts across artifacts and only the restated half survives** — and for
the first time the ledger can prove it, per skill, per session.

### 76.1 The arc, as measured

762 → **845** tests, coverage floor 63 → **67** (measured 67.87%), mypy 0 errors over 18
→ 19 files, `[tool.mypy]` flags 2 → **11**, backlog 128 → **121**. Close-out records
**7/7 complete** on all five keys. Three new controls shipped, each made to fail. Two
ratified owner decisions re-derived mid-arc and found **wrong** before either did damage.
Eleven friction entries — the largest harvest of any arc, and three of the six findings
exist only because of it.

**None of the six findings is about the work**, which is now the fifth consecutive report
where that is true. All six are about the process taxing or under-specifying itself.

### 76.2 The three corrections — each one changes what the fix is

**Finding 3 — the F841 collision — STANDS, but its cited trigger is wrong and its named
home is the wrong file.**

- *Correction A, and it is the useful half.* The report says `end-slice.md` §5
  *"prescribe[s] adding throwaway statements"*. It does not. Read at HEAD, §5 prescribes
  taking a **new guard, branch, or error path** and *"delet[ing] or invert[ing] it once"* —
  a *removal*, which never produces an unused local. The 53 × `F841` construction came
  from mutating a **size ratchet**: a check whose only way to disagree is to make the
  counted thing **bigger**, so the mutation must *add* statements. That is not a bad
  choice of mutation; it is the only available one for a counting check. So the collision
  is narrower and more interesting than filed — it fires exactly where the artifact under
  mutation is a **counting or sweeping check**, which is **finding 5's third case**.
  Findings 3 and 5 are one slice's two halves and the fix should be one edit, not two.
  (The S6 recurrence — inverting a condition — is the same shape: the inverted branch
  orphans the local the live branch consumed.)
- *Correction B.* The priority table names `settings.template.json` for the
  licence-honouring option. That file wires the launcher and carries no linter
  invocation. `{{HOOK_LINT_CMD}}` lives in `templates/claude-gate.template.sh` and
  `templates/copilot-hook.template.sh`, with the recipe in `reference/GATE_RECIPES.md`.
  A licence-honouring gate hook is a **two-dialect** change plus a recipe change plus
  `tools/gate-hook-check.py` cases — which is why the cheap half of the fix (name the
  collision and the module-level form in §5) is the one to take first.

**Finding 6 — the stale graph — STANDS, reduced to its small half; the damage claim does
not survive the template's own text.** The report says the view *"degrades into a
plausible-looking wrong answer rather than an absent one"*. `templates/SDLC.template.md`
→ *Architecture impact view* already says the opposite, in the artifact the adopter is
quoting from: **PARTIAL** is defined as *"the footprint was computed and something is
missing **and named**: files the graph does not know, **or a graph that may predate the
work**. The counts are printed with their denominators … so incompleteness is loud rather
than inferred"*, and *"A `COMPLETE` summary says the picture was drawn, never that the
change is correct."* The adapter reported `PARTIAL` with the reason on every run of the
arc. That is the designed behavior, working, and it is exactly the fire-proof/catch-proof
distinction the ninth report taught: the staleness was **loud**. What is genuinely
missing is one sentence — **no artifact anywhere names a regeneration trigger** — and
that is an S, in the template plus the two `end-phase.md` sites.

**Finding 2's *Homes* line is right and incomplete, and the omission is the whole of
§76.3.** The report names `commands/end-slice.md` §6 and `skills/change-verify/SKILL.md`.
The same split exists one step earlier, in `change-simplify`, where it is measurable and
where it lands on a **final, no-extension clock**.

### 76.3 The seventh finding — the report's own mechanism, found in `change-simplify`,
### where it threatens a clock that cannot be extended again

The report proves finding 2 with a differential: the part `end-slice.md` §6 **restates**
survived into all four records; the part living only in the skill did not. Run that same
differential on step 3 and it fails harder — **and this time the skill was dispatched.**

`commands/end-slice.md` §3's prescribed record line is:

> `quality: <N moves applied | nothing to do | skipped — reason>`

`skills/change-simplify/SKILL.md` requires considerably more (lines 139–140, 158–159):

> - **Per-axis verdicts** — one line per axis, even when the answer is clean, and for
>   Reuse the line names what was searched (the added symbols checked, and against
>   what) […] the Reuse axis line naming its search.

Measured against the arc's seven `quality:` lines, read off the slice commit bodies:

| | recorded |
|---|---|
| slices recording a `quality:` line | **7 / 7** |
| lines matching §3's prescribed form | **7 / 7** |
| lines carrying **per-axis verdicts** | **0 / 7** |
| Reuse-axis moves applied and named as such | **2** (S4, S6) |
| Reuse lines **naming their search** | **0** |

S4 records `1 move applied (Reuse — extracted the comment-strip the diff duplicated …)`
and S6 records `3 moves applied (1 reuse: duplicate repo-root expr …)`. Both name the
axis and the duplicate. Neither names **what was searched, and against what** — which is
the entire point of the §53 redirect, whose founding miss was a duplicated test helper
this pass eyeballed and `diff-review` then caught on the same diff.

**Why this is worse than finding 2, not a milder version of it.** Finding 2's mechanism
is *the skill was never loaded*, and the ledger supports it — one dispatch in five
sessions. Here the ledger shows **five dispatches in five sessions**. The skill was
loaded, run, and produced real moves; the half of its contract that had no home in the
command **still did not reach the record**. So "dispatch the skill" is not the fix for
this class. The durable record line is, and only the command specifies that.

**And it is load-bearing.** The `change-simplify` clock (§70.7 (ii)) is *two field arcs,
final, two-sided, and the no-further-extension commitment is already spent.* Its
**positive** criterion is, verbatim: *"at least one arc records a Reuse-axis move that
names its search."* Arc one of that clock has now run, and it records two Reuse-axis
moves and **zero named searches**. On a strict reading the positive half is unmet — but
what the arc actually measured is a record line that never asked for a search, which is
the same instrument defect that forced ruling (i) to restart the lens clock in the first
place. **The kit is about to delete a pass for failing a criterion its own record line
made unrecordable.** See the decision owed.

**Home:** `commands/end-slice.md` §3, alongside finding 2's §6 — one edit, both steps,
because they are the same defect and a fix to one leaves the other as the counter-example.

### 76.4 The six that stand, as build notes

**1 — the refactor licence, seventh recurrence. STANDS in full; both homes verified.**
`templates/tdd-guard-claude.template.py:223-225` and `templates/tdd-guard.template.sh:300-307`
both revoke on any test edit, in both dialects. `commands/end-slice.md` §§3/5/6 name the
licence **nowhere** — verified by grep across the file. `templates/SDLC.template.md:196`
states *"revoked by the next test edit"* as flat truth with no close-out qualification.
The report's claim that §5's mandated order cannot be executed without re-declaring is
correct and is the new half: §4 fixes tests → §5 writes production → and §5's own restore
touches tests again. Three declarations in one slice is what that costs. **Option (a) —
a close-out-scoped licence — is the one that removes the tax; option (b) only prices it.**
(a) is a two-dialect guard change with proof cases in both suites; (b) is three sentences.
Ruling owed.

**2 — `change-verify`'s missing third verdict. STANDS, verified end to end.**
`skills/change-verify/SKILL.md:184` carries the three-way verdict with *"must never be
folded into the first"*; §6's record line asks only for a verdict per behavior naming the
shell. Read off the four `verify: ran` records: **all four name the shell, none contains
a "not exercised"**, and S6's records three passes over a slice whose IMAP path was
deferred behind a seam by a ratified decision in the same arc. The report's inference —
followed from memory of the command, not loaded — is supported by the ledger and is the
right one. **Take the suggested fix as filed**, and take §76.3's alongside it.

**3 — the F841 collision. STANDS as corrected** (§76.2). Fix the cheap half in §5 with
finding 5.

**4 — the docs-only slice through the full loop. STANDS.** `commands/next-slice.md` §4
opens with *"Read `spec/TESTING.md` — fresh, every time"* before a loop with nothing in
it, and §2 — the one owner halt, where scope is already settled — has no docs-only branch
to declare. Note that §4 **already knows this class exists**: its characterization
paragraph warns against a slice that *"quietly takes the zero-form a docs edit takes"*.
The kit has the concept and no declaration point for it. The suggested fix is the right
shape; the M is real, because the short-circuit must not become an escape hatch a code
slice can take.

**5 — step 5's zero-form on a sweep. STANDS, and the adopter already invented the form.**
S7's record reads `mutation: 1 check seen to fail — the exit-criteria sweep, fed an
injected line anchor in a scratch copy, fired on exactly that line`. §5 has two branches
(a new guard; a characterization slice) and this is neither. The fix is to name the third
case in the language the arc already used. **Merge with finding 3** per §76.2.

**6 — the stale graph. STANDS, reduced** (§76.2). One sentence in the template naming a
regeneration trigger, echoed at the two `end-phase.md` sites.

### 76.5 The arc read against the standing clocks — three move for the first time

**(i) The three STD lenses — the restarted clock is READABLE for two of three, and arc
one is spent for those two.** §70.7 (i) restarted the clock *"from the first arc whose
denominator is enumerable"* and shipped the `lenses:` commit-body line to make it so.
That line is present **7/7** this arc — the instrument works. Read across the seven
records:

| lens | applications recorded | catches |
|---|---|---|
| `secrets and exposure` | **3** (S3, S4, S6) — all `clean` | 0 |
| `untrusted input` | **2** (S3, S4) — all `clean` | 0 |
| `logging and swallowed errors` | **0** | 0 |

So `secrets and exposure` and `untrusted input` are on **arc one of two, at zero
catches**, with a real denominator for the first time in the clock's life. The third is
still unreadable, and the reason is structural in the same way ruling (i) found: the
preamble requires *"one line per lens **applied**"*, so a lens whose trigger never matched
writes nothing, and *never triggered* remains indistinguishable from *never considered*.
**Do not restart the clock again for that** — two of three are now measurable, and a lens
whose trigger has not matched a slice in nine phases is answering the deletion question
by a different route. Recorded here so the next arc's read is against a stated baseline.

**(ii) `change-simplify` — arc one of the final clock has run, and it is ambiguous by the
kit's own fault.** Positive half: two Reuse-axis moves, zero named searches (§76.3) —
unmet as worded. Negative half: **not triggered, verified.** The two candidate backlog
entries minted by `diff-review` on diffs this pass had passed over are a comment-accuracy
finding about two allowlists that are *deliberately* different (it argues **against**
unification) and a duplicated-hazard finding in a file **outside the slice's diff**, which
is outside `change-simplify`'s stated scope. Neither is the founding miss recurring. So:
**no disqualifying event, and a positive half the record line could not carry.** Ruling
owed — and the honest options are to count the two moves as satisfying it, or to fix the
record line and read arc one again next arc.

**(iii) CONTRACT — arc one IS spent, and the mechanism demonstrably engaged.** §70.7
(iii) started the clock *"at the first field arc run under 0.26.0"*; this arc ran under
0.30.0, so it counts. The adopter completed the backfill walk before the arc (32
confirmed entries across eight surfaces), and the arc's preserved-contract check ran on
**9 pins across 4 touched surfaces, each verified present and passing**. §56.2's second
criterion — *"within two arcs a phase touching a contract surface must demonstrably
encounter its entries"* — is **met on arc one**. No catch, which is not required by that
half. Arc two decides the first half.

**(iv) IMPACT — arc one ran with a graph that was stale for the entire window; my read is
it does NOT count, and finding 6 is why.** §66.6 pre-registers *"an arc without a usable
graph cannot exercise the feature and does not count against it"*, and asks for at least
one owner-reported comprehension event across two such arcs. This arc: adapter ran at
every prescribed site, `PARTIAL` every time, graph built before the *previous* phase
merged, **zero comprehension events reported**. A graph that predates the previous arc
cannot show this arc's neighborhood, so the feature was never actually exercised — the
same reasoning ruling (i) used for the lenses. **Fix the instrument (finding 6), then
start the clock.** This is the third clock in a row whose first reading was blocked by a
missing half of its own instrument, which is itself worth saying out loud.

**(v) `mutation-testing` — third consecutive arc at zero dispatches, and §70.7 ruling 4
already priced it.** That ruling inlined the standing rules into §5 and kept the skill as
depth, saying in terms that *"leaving it produces a third arc at zero"*. It has. **The
report's corroboration is already-ruled and owes nothing.** What is new is the other
direction, and it is a **confirmed catch for the 0.26.0/0.29.0 inlining**: the arc's
records show every inlined rule being followed by sessions that never opened the skill —
S6 records a stated sample (`5 of 64 characterization pins`), S3 records
*"restored by inverted edit, never git checkout — both paths carried uncommitted slice
work"*, and S5 records *"path verified clean beforehand, restored by git checkout, tree
confirmed clean"*. That is §5's safe-revert rule and its `git status --short` precondition
being executed exactly as written, on their first field arc, by an operator who never
loaded the skill. **The 9a fix works, measured.** Record it against §70.7 ruling 4.

### 76.6 Decisions owed

1. **Sequencing.** The natural batch is small and text-only: finding 2 + §76.3 (one edit
   across §3 and §6), findings 3+5 merged (one edit in §5), finding 6 (one sentence, two
   echoes). That is four files and no design. Findings 1(a) and 4 are the two that carry
   design and both are M. Ship the text batch first, or hold for finding 1?
2. **Finding 1 — (a) or (b)?** (a) a close-out-scoped licence the guard honours, in both
   dialects with proof cases in both suites — removes a tax now at seven recurrences in
   one arc. (b) name the licence in §§3/5/6 — three sentences, makes the cost predictable
   and does not reduce it. The adopter explicitly declined to close this by absorption a
   third time. Recommend (a), with (b)'s sentences shipped alongside it, since the
   template's unqualified "revoked by the next test edit" has to change either way.
3. **§76.3's clock question, and it is the one that cannot wait.** The
   `change-simplify` positive criterion asks for a named search that the record line
   never asked for. Options: (α) count arc one's two Reuse-axis moves as satisfying the
   positive half and let the clock run to arc two on the corrected record line;
   (β) fix the record line and re-read arc one against arc two and three — an extension
   in effect, on a commitment already spent once; (γ) hold the criterion strictly and
   let arc two decide alone. Recommend (α): the redirect's *deliverable* — a Reuse move
   found on a diff, twice — is on the record, and only its *evidence-of-search* wording
   is unmet, for a reason that is the kit's defect and not the pass's.
4. **§76.5 (iv) — does an arc with a whole-arc-stale graph count against IMPACT?**
   Recommend **no**, consistent with (i) and (iii): fix the instrument first.
5. **Tell the adopter what is already ruled.** `mutation-testing`'s zero-dispatch
   corroboration was ruled 2026-08-26 and needs no third recurrence; their friction entry
   can close as *ruled upstream* rather than age another phase — the same courtesy §70.2
   extended for finding 7.

### 76.7 Ruled 2026-09-01 — all five, and ruling 4's second half needed a measurement
### before it could be built

1. **Sequencing — RULED: finding 1 first, then the text batch, all in one release.**
   The owner inverted the recommendation deliberately: the licence hazard is at seven
   recurrences in one arc and has been deferred behind a text batch twice already, so it
   leads. Everything else rides the same release. **Finding 4 is OUT** and holds for the
   next one — this release already carries a two-dialect guard change with proof cases in
   both suites, two record-line fixes, the §5 merge, and the impact-view work; finding
   4's short-circuit has to be one a code slice cannot take, which is its own design
   question, and it would interleave with the same three `end-slice.md` steps everything
   else is already editing.
2. **Finding 1 — RULED (a), with (b)'s sentences shipped alongside**, as recommended. A
   close-out-scoped licence the guard honours, in both dialects, with proof cases in
   `tools/tdd-guard-check.py` and `tools/tdd-guard-claude-check.py`; and §§3/5/6 name the
   licence as a precondition regardless, because `templates/SDLC.template.md:196`'s
   unqualified *"revoked by the next test edit"* has to change either way and a guard
   change that leaves the prose asserting the old rule is the §63 defect exactly.
3. **§76.3's clock question — RULED (α).** Arc one's two Reuse-axis moves count as
   satisfying the `change-simplify` positive criterion. The redirect's *deliverable* — a
   Reuse move found on a diff, twice — is on the record; only its *evidence-of-search*
   wording is unmet, and that is unmet because `end-slice.md` §3's record line never
   asked for a search. **This is not an extension**: the no-further-extension commitment
   stays unspent, the clock's two arcs still run, and arc two is read against the
   corrected record line this release ships. The negative half was checked and is **not
   triggered** (§76.5 (ii)).
4. **IMPACT — RULED: no, a whole-arc-stale graph does not count against the clock.** As
   recommended, and consistent with rulings (i) and (iii): fix the instrument, then start
   the clock.

   **Its second half — "help adopters turn auto-update on" — was ruled on a premise that
   does not hold, and the measurement changes what gets built.** Verified directly
   against the plugin source at
   `~/.claude/plugins/marketplaces/understand-anything/understand-anything-plugin`,
   independently of the adopter's own account of it (which it confirms):

   - `autoUpdate` **defaults to `false`** (`packages/core/src/persistence/index.ts:148`).
   - Setting it `true` enables exactly two things, and **neither writes the graph**.
     `hooks/hooks.json`'s `PostToolUse` entry runs
     `hooks/post-tool-use-auto-update.mjs`, whose entire output is a
     `hookSpecificOutput.additionalContext` string telling **the model** to read
     `hooks/auto-update-prompt.md` and do the merge by hand. The `SessionStart` entry is
     a staleness comparison that `echo`s the same instruction.
   - The `PostToolUse` entry carries **`"matcher": "Bash"`**. A commit issued through the
     PowerShell tool is a different tool and matches nothing, so on a PowerShell-primary
     project the commit trigger never fires at all — the adopter measured this both ways
     (a probe commit through Bash fired the reminder; their real arc commits did not).
   - `hooks/auto-update-prompt.md:3` describes itself as *"triggered automatically by the
     post-commit hook"*. **There is no post-commit hook anywhere in the plugin.**

   So `autoUpdate: true` is **auto-remind, not auto-update** — necessary, not sufficient,
   and on Windows/PowerShell close to session-start-only. Telling adopters to flip it and
   stopping there would put the kit in the position its own field reports keep catching:
   prose asserting a mechanism the artifact does not have.

   **RULED (owner, on the measurement): offer the flag AND own the trigger.** Two halves:
   `commands/sdlc-setup.md` detects a `.ua/` or `.understand-anything/` config, offers to
   set `autoUpdate: true`, and states in one place what it does and does not do; and the
   kit names its **own** regeneration trigger at the phase boundary, which is finding 6's
   actual ask and is independent of whether the plugin's reminder ever arrives. The third
   option — shipping a deterministic baseline-advancer of the kit's own, as the adopter
   built for themselves — is **refused**: it would put the kit in the business of
   maintaining a vendor's graph format, and the adopter's own version needed a
   tree-sitter-fidelity self-test to be safe (it caught two real extractor bugs before
   shipping). That is a vendor's job.

   **The vendor defect itself is not the kit's to fix** and is correctly filed against
   that plugin's repository, as the report says. What the kit owes is not depending on it.
5. **Tell the adopter what is already ruled — RULED: yes.** `mutation-testing`'s
   zero-dispatch corroboration was ruled 2026-08-26 (§70.7 ruling 4), which anticipated a
   third arc at zero in terms. Their friction entry closes as *ruled upstream* rather than
   ageing another phase — the same courtesy §70.2 extended for the ninth report's finding
   7. Goes in the issue reply alongside the §76.2 corrections and the §76.5 clock
   readings, since three of those readings are about their arc and they cannot derive them
   from their own tree.

### 76.8 The batch, as scoped

**LIC — the tenth report's batch.** One release. In order:

1. **Finding 1** — the close-out licence. `templates/tdd-guard-claude.template.py` and
   `templates/tdd-guard.template.sh`; proof cases in both `tools/` suites;
   `commands/end-slice.md` §§3/5/6 naming it; `templates/SDLC.template.md`'s Records
   paragraph qualified.
2. **Finding 2 + §76.3** — the two record lines. `commands/end-slice.md` §3 (per-axis
   verdicts, the Reuse search) and §6 (`not exercised: <what, or "nothing">`), each
   restating the half of its skill's contract that has been measured not to survive
   otherwise.
3. **Findings 3 + 5, merged** — `commands/end-slice.md` §5's third case (a slice whose
   deliverable is a sweep or a check owes a made-to-disagree run of *that*), carrying the
   `F841` collision and the module-level form, since a counting check is exactly where
   both bite.
4. **Finding 6 + ruling 4's second half** — `templates/SDLC.template.md`'s *Architecture
   impact view* names a regeneration trigger; `commands/end-phase.md` steps 2 and 6 echo
   it; `commands/sdlc-setup.md` offers `autoUpdate` with its measured limits stated.

Out: finding 4. Also out: any kit-owned graph writer (ruling 4).

### 76.9 Built 2026-09-01 — and the one thing the build found that the ruling did not
### cover

**Built as scoped in §76.8**, in the ruled order. Four things worth recording beyond the
edit list.

**(a) The close-out licence's shape, decided at build time.** The ruling said "a
close-out-scoped licence the guard honours"; it did not say what bounds it. A licence
that survives every test edit is, on its face, a session-long bypass of G1 — so the
design keeps every bound the refactor licence has (a counted green behind it, session
scope, the declaration line logged on every write) and adds one the refactor licence
does not need: **every test edit it survives is counted, and the count is logged.**
`close-out license SURVIVED a test edit (N this session)`. No cap, because a cap that
denies mid-close-out re-creates the defect being fixed and no evidence exists for a
number; the count is what makes a licence held open past its step **visible in review**
rather than silent. That is deliberately a catch-proof rather than a fire-proof, which
is the ninth report's lesson applied to the fix for the tenth's.

**(b) The build invalidated a pinned property, and it was re-pointed rather than
dropped.** `tools/tdd-guard-claude-check.py` case 4b pins §48/§50.1: the deny message
names the behavior-preserving route **by case**, never narrowed by a phase word, because
operators who read "close-out" concluded the licence was close-out-only. The new deny
sentence necessarily contains "close-out". The pin's *premise* changed — there is now a
genuinely close-out-scoped licence — but the defect it guards is still available, so 4b
was re-pointed to the property that actually protects it: the unqualified case sentence
must be present **and must precede** any occurrence of "close-out". A matching `32b` was
added to the shell suite, which had no equivalent. Deleting 4b because the change broke
it is exactly what the disposal-intent lens exists to catch.

**(c) Two mutation anchors went stale and were re-pointed, in both suites.** The licence
condition line changed in both dialects, and both suites' *"drop the green requirement"*
anchors pointed at the old text; the shell suite's session-clear anchor went stale the
same way. Both suites report a stale anchor rather than passing over it (§75.7), which is
how these surfaced immediately — the third time that reporting has paid for itself.
**Four new mutations** cover the new behavior in each dialect: revoke the close-out
licence on a test edit; stop counting the survivals; let it write without a green; and
(shell) log a close-out write as a refactor one.

**(d) The open half the ruling did not reach: the new record lines have no observer.**
`tools/close-out-check.py` is **structural presence only** by design — it asserts the
five keys are present and non-empty and says so in its own output (*"this does not verify
the evidence is true"*). So the `not exercised:` half of `verify:` and the `reuse:` half
of `quality:` are, today, rules with no observer — which is the exact shape §76.3
criticised and the report's own cross-cutting theme. **Not built, deliberately**, because
making the checker require a sub-key inside `verify: ran` would fail every existing
adopter record and every fixture in the suite, and a migration is a design question the
sequencing ruling did not open. The honest options for the next batch are (α) leave it as
prose and read arc two's records to see whether restating in the command was sufficient —
which is the measurement §76.3 says the command line alone *does* determine, and the
cheapest way to find out; (β) a **log-only** observer on the `docs-check` precedent
(§68), which breaks nothing and makes the omission visible; (γ) a hard requirement with a
stated cutover commit. **Recommend (α) then (β):** arc two is already going to be read
against the corrected line for the `change-simplify` clock, so the measurement is free,
and (β) only earns its place if that reading shows the restatement was not enough.
Recorded as the batch's known limit rather than discovered later as a gap.

**(e) Finding 3 is sharper than the report knew: the colliding rule is one the kit
itself recommends.** The build went looking for where a project decides to enable
`F841`, and found it in the kit's own **lens↔rule map**, shipped six days ago in 0.30.0
— the *unconsumed artifact* row recommends exactly that rule family in all six languages
(`F401`/`F811`/`ARG`, `@typescript-eslint/no-unused-vars`, `IDE0051`, `U1000`,
`UnusedPrivateMethod`, `dead_code`) as the mechanical half of a review lens. So this is
not a project's linter choice colliding with the kit; it is **two sections of the kit
colliding**, one recommending a rule and the other mandating a step the rule blocks,
neither aware of the other. That is the report's cross-cutting theme found inside the
kit's own reference file, and it is the strongest single instance of it. Cross-referenced
both ways: `GATE_RECIPES.md`'s row now names the collision and the module-level form at
the point a project turns the rules on, and §5 names the row so the step's reader knows
the rule is recommended rather than incidental. Neither is weakened — enabling the rules
is still right.

---

## 77. §71's stop budget fails on an IDLE machine at the same number it fails under
## load — the "timing wobble" explanation has been carrying a stable 3× step change
## since 0.27.0 — filed 2026-09-01

Found while running `/kit-check` before the 0.31.0 release (§76.8's batch). Filed
rather than fixed: `tools/close-out-check.py` is outside that batch's ruled scope, and
this is the tooling's own defect — the same reason §71 was filed rather than fixed.

### 77.1 What was measured

The 0.31.0 pre-release run of `tools/close-out-check.py` breached the stop budget
**twice**, and the second run is the one that matters:

| run | conditions | stop typical | verdict |
|---|---|---|---|
| A | three other proof suites running concurrently | **6399 ms** | S2 PERF, exit 1 |
| B | **nothing else running** — every other python killed first | **6344 ms** | S2 PERF, exit 1 |

Run B was made specifically to remove load as the explanation, expecting a large drop.
It moved **55 ms, under 1%.** Correctness in run B was complete and clean: 26 unit
cases, 7 docs cases, 20 stop cases, **28/28 mutations caught, 0 survivors, 0 stale, 0
crashes** — the suite's own closing line, *"the correctness results above are
unaffected"*, is true and is the reason this is not a release blocker.

### 77.2 The finding, which is not the number but the explanation attached to it

**The suite prints, and this repo has twice accepted, that these budgets are
*"unreliable under load"* — and run B has no load.** Set the five measurements this
repo holds side by side:

| source | stop typical |
|---|---|
| §71, **released v0.26.0**, throwaway worktree | **1918 ms** |
| §71, 0.27.0 run B | 6289 ms |
| §71, 0.27.0 run C | 6120 ms |
| §71, 0.27.0 run F | 6099 ms |
| §77 run A (0.31.0, loaded) | 6399 ms |
| §77 run B (0.31.0, **idle**) | 6344 ms |

Five of the six cluster inside **300 ms of each other**, across three releases, on
loaded and idle machines alike. That is not a wobble; that is a **stable ~3.3× step
change between v0.26.0 and 0.27.0** that has never been attributed to a cause. §71's
own decisive control — the docs pass swinging 535 ms → 5503 ms on identical code — is
real evidence of wobble, and it is what made *wobble* the standing explanation. It has
since been doing duty for a second phenomenon it does not explain.

**Why this matters beyond a red exit code.** The budgets are not arbitrary: §71 records
that they exist because *"the stop path runs inside a 30 s hook timeout."* At 6.3 s the
control still fits — comfortably, and nothing observed in the field suggests otherwise
— but the margin has quietly gone from ~16× to ~5×, and the artifact that would have
said so is the one being explained away. A budget that fails every run teaches its
reader to skip the line, which is how the skill-ledger proof stayed dead for six
releases (§75).

### 77.3 What is NOT claimed

- **Not a 0.31.0 regression.** `templates/close-out.template.sh` and
  `tools/close-out-check.py` are both untouched by §76.8's batch — verified by
  `git diff --stat`, empty for both.
- **Not attributed.** 0.27.0 added the fifth record key and 0.29.0 added the
  bookkeeping filter, whose own measurement (§73.9) reported 4186 ms against 4188 ms
  for the filtered-vs-unfiltered pair — itself well over the 1500 ms budget and
  recorded at the time as costing "nothing measurable", which was true of the *filter*
  and silent about the *baseline it sat on*. That is a lead, not a cause. Bisecting the
  step change is the work this section asks for and does not do.
- **Not a claim that the budget number is wrong.** It may be right and the code slower;
  it may be miscalibrated. Deciding that is §71.3 option 3, still unruled.

### 77.4 Decisions owed

1. **Rule §71.3 option 3 (re-calibrate), which has been open since 2026-08-26.**
   Median or best-of-N per invocation rather than the slowest single one. Option 1
   shipped and works — the mutation pass now completes and reported all 28 — so the
   only thing still broken is the verdict.
2. **Attribute the step change before re-calibrating, not after.** Re-calibrating first
   would set the new threshold from a number nobody has explained, which is the
   *recorded-value-with-no-enforcing-artifact* defect (invariant 14) committed against
   the kit's own tooling. One bisect across v0.26.0 → 0.27.0 → 0.29.0 → HEAD, in a
   throwaway worktree, answers it.
3. **Until both are done, a release note is owed on every run**: `/kit-check` should
   report this suite as **correctness-green / perf-red (§77)** rather than as a pass or
   a failure, because it is currently neither and both prior releases resolved the
   ambiguity by informal judgement. 0.30.0 shipped over this same breach (§75, recorded
   as "under three concurrent suites"); 0.31.0 does the same, now with the load
   explanation withdrawn.

### 77.5 The bisect, run 2026-09-04 — there is no step change to bisect

§77.4's first two items asked for a bisect across v0.26.0 → 0.27.0 → 0.29.0 → HEAD before
any re-calibration. It was run in six throwaway worktrees, one per tag, with a harness
that loads each tree's own `tools/close-out-check.py` and runs **only** its `stop_pass` —
no unit pass, no docs pass, no mutations — so each release is measured as it shipped, and
the per-case times are kept rather than collapsed to a max.

| tag | n (excl. cap) | median | p90 | max | cap-20 walk |
|---|---|---|---|---|---|
| v0.26.0 | 14 | **1129 ms** | 1301 | 1312 | 4177 ms |
| v0.27.0 | 14 | **1131 ms** | 1266 | 1303 | 4187 ms |
| v0.28.1 | 14 | **1142 ms** | 1286 | 1307 | 4190 ms |
| v0.29.0 | 19 | **1133 ms** | 1300 | 6168 | 4203 ms |
| v0.30.0 | 19 | **1163 ms** | 1324 | 1370 | 4226 ms |
| v0.31.0 | 19 | **1132 ms** | 1454 | 1465 | 4285 ms |

**The median does not move: 1129 ms at v0.26.0, 1132 ms at HEAD, across six releases and
the two changes §77.3 named as leads.** The 0.27.0 fifth record key and the 0.29.0
bookkeeping filter cost nothing measurable — 0.29.0's own §73.9 reading was right. The
only real growth in the whole window is the cap-20 walk, 4177 → 4285 ms (**+2.6% over six
releases**), which is nowhere near its 5000 ms budget. Every isolated run is **under**
both budgets, including HEAD's.

### 77.6 What the number actually is: `max()` over a distribution with one ~5 s stall

The full suite reports ~6300 ms for the same code these worktrees measure at ~1450 ms, so
the difference is a property of the run, not of the release. Three measurements, all on
HEAD, all on the same machine within minutes of each other:

1. **Stop pass alone, twice in one process:** typical **1467 ms**, then **1420 ms**. Run
   the unit and docs passes in between and the third stop pass reports **5560 ms** — with
   its wall time essentially unchanged (51 s → 55 s). The time did not spread; it landed
   somewhere.
2. **Where it lands is random.** Printing every case in run order: in one run the stall
   fell on `stop_complete_clean` (case 3 of 20) at **6156 ms** with all nineteen others
   between 1.08 and 1.46 s; in another it fell on `stop_repeat_flag_dedups` (case 19) at
   **6469 ms**. Same code, same order, different victim.
3. **The same case, run 40 times in one process:** min 1076, **median 1132**, p90 1263 —
   and **exactly one** invocation at **6203 ms**. One outlier in forty, about +5.0 s, on a
   distribution otherwise tight to ±200 ms.

So the reported statistic is `max()` over ~19 samples of a ~1.1 s distribution that
carries roughly one +5 s OS stall per suite run. It catches the outlier nearly every time,
which is exactly why it looked *stable* across releases and *identical* on a loaded and an
idle machine (§77.2's run A vs run B, 6399 vs 6344): both runs were measuring the stall,
not the script. §71's 1918 ms at v0.26.0 was not a faster release — it was a run whose
stall happened to miss.

**This retires the finding as filed and answers §77.4 items 1 and 2 together.** There is
no step change, so there is nothing to attribute before re-calibrating, and the
*"unreliable under load"* line was wrong in a second way: the stall is real but it is not
load. What remains is that **`max()` is the wrong statistic for a budget** — which is
§71.3 option 3, now supported by a cause rather than by an unexplained number.

**What the fix should be, for the owner's ruling.** The budgets exist because the stop
path runs inside a 30 s hook timeout, and the honest measurement of that risk is the
typical invocation, not the worst sample the OS happened to interrupt. Options, in the
order they are worth taking: **(α)** report the **median** of the stop invocations against
the 1500 ms budget and print the max beside it as an observation, not a verdict —
one-line change, immune to a single stall, and it would have read green at every tag in
the table above; **(β)** best-of-3 per case, which costs three times the stop pass's 51 s
for the same answer; **(γ)** raise the budget number, which is the one option the
measurement argues against — the median has not moved in six releases, so a raised budget
would be calibrated to an artifact of the sampling rather than to the script. **Recommend
(α).** The cap-20 budget needs nothing: it is measured on a single case, it is stable, and
it has 700 ms of headroom.

Not done here, because it is a change to the tooling rather than a measurement: §77.4
item 3's release note, and the `/kit-check` line that reports this suite as
**correctness-green / perf-red**. With (α) ruled, neither is needed — the suite would
simply be green — so both wait on the ruling rather than being written first.

### 77.7 Ruled 2026-09-04 — (α), and built the same day

**RULED (α): the typical verdict reads the median.** `tools/close-out-check.py` now
prints `median stop invocation: N ms (budget: 1500 ms; slowest of 19: M ms, observed not
asserted - FEATURE_PLAN 77)` and asserts on the median alone. Three things about the
shape, decided at build time:

- **The slowest is still printed.** A real regression moves the median *and* shows up
  there, so dropping it would trade one blind spot for another. It is an observation, and
  the line says so in its own text rather than in a comment.
- **The cap-20 walk keeps its max**, because it is a single case: with one sample there
  is no median to take. It has moved 4177 → 4285 ms in six releases *in isolation* — but
  **it is exposed to the same stall, and that was measured, not assumed**: the in-suite
  runs of §77.6 read it at **9367 ms** once and **4840 ms** on the verifying run, against
  a 5000 ms budget. So the last spurious-red path left in the suite runs through this one
  case. The cheap fix if it ever fires is **best-of-2 for the cap case alone** (~4 s), not
  a raised budget; not built now, on the same evidence rule applied to the unit and docs
  passes below — it has not breached yet.
- **The footer changed too.** *"this machine's are unreliable under load: FEATURE_PLAN
  71"* was wrong twice over — the stall is real but it is not load, and the sentence
  taught its reader to skip the line, which is exactly how the skill-ledger proof stayed
  dead for six releases (§75). It now states what a breach means under the median.

**§77.4's items 1 and 2 are answered and item 3 is withdrawn.** There was no step change
to attribute, so nothing had to be attributed before re-calibrating; and with the median
in place the suite is simply green, so the `correctness-green / perf-red` release note
`/kit-check` was owed has nothing left to report. §71.3 option 3 closes with it.

**The one thing this does NOT fix, stated rather than left to be rediscovered.** The unit
and docs passes still assert on `max()` — 26 and 7 samples against 1000 ms budgets — so
the same one-per-run stall can breach either of them on identical code. That is not
hypothetical: §71's own decisive control was the docs pass swinging **535 ms → 5503 ms**
between two runs of the same tree, which was read at the time as evidence of *wobble* and
is better read now as the same stall landing in a different pass. Both return only their
slowest invocation, so fixing them means returning per-case times from `unit_pass` and
`docs_pass` — a slightly larger change than this one, and outside what was ruled.
**Recommend the same treatment when either next breaches**, rather than pre-emptively:
the stop budget breached every run and these two have breached once between them, so the
evidence does not yet support the edit. Recorded here so the next breach is read as this
finding rather than as a new one.

---

## 78. The hook launchers read "not at the root" as "not a repo" — every Copilot hook but
## the ledger has been silently inert in any session launched below the root, on every
## CLI build before 1.0.88, and a linked worktree disarms both dialects by construction —
## filed 2026-09-27

**How it was found.** A sanity check of Copilot CLI against the kit (installed 1.0.86,
latest 1.0.88; `reference/COPILOT.md` last verified on 1.0.78). The 1.0.88 changelog
reads: *"Hook commands without an explicit `cwd` again run in the project root instead of
the session's current directory."* Every Copilot launcher the kit ships starts with the
same guard, and the guard's failure branch is an exit 0:

```
if [ -d .git ] && [ -f .github/hooks/<script> ]; then cat | sh .github/hooks/<script> …; fi
```

That is `copilot-hook.template.json` (gate), `tdd-guard.template.json` (all three events),
and `close-out-hook.template.json` (backstop). `skill-ledger.template.json` is the only
launcher whose not-at-root branch is loud (`exit 1` with a named message).

### 78.1 Measured — the bench, 2026-09-27

A probe hook (logs `pwd`, `[ -d .git ]`, `[ -e .git ]`) beside a copy of the kit-shaped
launcher, on the trusted bench `copilot-ci-test`, one shell-tool turn per run. Builds run
side by side from the release zips, SHA256-checked, `--no-auto-update`.

**A labelling trap, caught the same day and corrected here.** The WinGet-installed
`copilot.exe` is itself a **1.0.83** binary: a plain launch loads a newer self-downloaded
build (`--version` said 1.0.86, later 1.0.88), but `--no-auto-update` pins the build
bundled in the binary. The first pass ran that exe with the flag and labelled the rows
"1.0.86"; they were **1.0.83**. The genuine 1.0.86 zip was then measured separately. The
conclusion did not move — every pre-1.0.88 build measured skips — but a version claim
from this bench is only as good as `--version --no-auto-update` **on the exe that ran**.

| build | launched from | route | hook cwd | `.git` dir | kit launcher |
|---|---|---|---|---|---|
| 1.0.88 | root (control) | Git Bash | root | y | **ran** |
| 1.0.78 | `spec/` | Git Bash | `spec/` | n | **silent skip** |
| 1.0.83 | `spec/` | Git Bash | `spec/` | n | **silent skip** |
| 1.0.83 | root (control) | PowerShell → WSL | root | — | **ran** |
| 1.0.83 | `spec/` | PowerShell → WSL | `/mnt/d/…/spec` | n | **silent skip** |
| 1.0.86 | `spec/` | Git Bash | `spec/` | n | **silent skip** |
| 1.0.86 | `spec/` | PowerShell → WSL | `/mnt/d/…/spec` | n | **silent skip** |
| 1.0.88 | `spec/` | Git Bash | root | y | **ran** |
| 1.0.88 | `spec/` | PowerShell → WSL | root | y | **ran** |

The hook configuration *is* discovered from the repo root in every case — the hooks
fire; they fire in the wrong directory, and the launcher reads that as "no repo here".
So through 1.0.87, a Copilot session started anywhere below the root ran with **no gate,
no TDD guard, and no close-out backstop**, and said nothing. 1.0.78 is affected, so this
is not a recent regression: it is the whole of the kit's measured Copilot history, and
the 2026-08-07 record (*"the hook process's working directory is the session's cwd"*) was
the fact, measured, with its consequence for the guard never drawn. One unexplained
detail, recorded rather than smoothed: one 1.0.83 WSL-route subfolder run logged the
`agentStop` probe but not the `preToolUse` one; every other run logged both.

Whether either adopter ever launched below the root is **unknown**; both habitually
start at the root, which may be why no arc surfaced it.

### 78.2 The worktree case — by construction, and in both dialects

In a linked worktree `.git` is a **file** (`gitdir: …`), so `[ -d .git ]` is false at the
worktree's own root, and every launcher above skips there on any build. The Claude Code
dialect has the same test in two places: the close-out `Stop` block
(`settings.template.json`, `sh -c "if [ -d .git ] && …"`) and the TDD guard's
`repo_root()` (`tdd-guard-claude.template.py`, `os.path.isdir(".git")` for both the
`CLAUDE_PROJECT_DIR` and the cwd branch), which returns `None` and does nothing. The
subfolder case (78.1) is Copilot-only; Claude Code runs hooks at the project root.

This got more pressing, not less: Copilot 1.0.85 took `/worktree`, `/move`, and
`--worktree` out of experimental mode, and 1.0.87 added `worktreePathTemplate`. The kit
already solved this once — IMPACT's slice-base capture is worktree-safe (§66.2 (e)) —
and the hooks never got the same treatment.

**Measured end to end, 2026-09-27 — owner-approved probe inside the trusted bench.**
Copilot loads repo hooks only from `trustedFolders`, and adding a scratch folder to that
list was refused by the session's permission policy (config verified restored,
byte-identical), so the probe ran in a linked worktree created *inside* the bench
(`copilot-ci-test/.wt-probe`, branch `wt-probe`, both removed after), probe hooks copied
in, launched from the worktree root:

| build | route | hook cwd | `.git` dir | `.git` exists | kit launcher |
|---|---|---|---|---|---|
| 1.0.78 | Git Bash | worktree root | n | y | **silent skip** |
| 1.0.83 | Git Bash | worktree root | n | y | **silent skip** |
| 1.0.83 | PowerShell → WSL | `/mnt/d/…/.wt-probe` | n | y | **silent skip** |
| 1.0.88 | Git Bash | worktree root | n | y | **silent skip** |
| 1.0.88 | PowerShell → WSL | `/mnt/d/…/.wt-probe` | n | y | **silent skip** |

(The 1.0.83 rows were first recorded as 1.0.88 — the §78.1 labelling trap; the genuine
1.0.88 rows are from the release zip, re-run in a recreated probe worktree.)

The worktree's hooks load and fire at the worktree's own root on every build and route;
the launcher skips because `.git` is a file. **Updating the CLI does not fix this case**
— 1.0.88 skips exactly as 1.0.78 does. The Claude-dialect half (the `Stop` block and
`repo_root()`) is established by reading, not yet by a Claude Code run.

### 78.3 Fix direction — not ruled

- **Resolve the root, don't test the cwd.** `git rev-parse --show-toplevel` answers both
  cases (subfolder and worktree). **The hard part is the launcher, not the script:** from
  a subfolder the relative `.github/hooks/<script>` path does not resolve either, so the
  launcher must find its script without the root — and it must stay `$`-free for the
  WSL route (re-measured 2026-09-27: that route expands `$var` to empty before the hook
  shell runs, on top of the known backslash and `$(cat)` corruption), while keeping
  stdin for the payload. That is a bench design question, not a text edit; the Claude
  dialect (`CLAUDE_PROJECT_DIR`, Python) has the easier half.
- **A not-at-root outcome must be loud**, the skill ledger's shape: a hook that cannot
  find its repo says so on stderr rather than exiting 0. A silent skip is the §61 PIN
  defect and the 0.28.1 guard defect, a third time.
- **Proof cases in both guard suites** for a subfolder cwd and a `.git` file, with a
  mutation that restores `[ -d .git ]` — so the proof can fail on the old launcher.
- **The version floor.** 1.0.63 stays the hard floor (the matcher); 1.0.88 becomes the
  *recommended* floor, stated with this section's reason. **Withdrawn in §78.5** — the
  `cwd` fix holds from 1.0.63, and 1.0.88 does not fix the worktree case. The launcher fix is what makes
  older builds safe; the floor is not the fix.

### 78.4 Two re-verification items the same check raised

- **`/skills reload` and `/skills info`** — named by `sdlc-setup.md:801` and
  `SKILLS.md:24` as the install check. `/skills` became a dashboard in 1.0.81, and
  neither subcommand can be confirmed without an interactive session (not greppable in
  the binaries; GitHub's command reference is too incomplete to show absence — it omits
  `/plugin` too). **CONFIRMED 2026-09-27, both still work, on 1.0.83 and on 1.0.88**, in
  ai-news-dashboard: `/skills reload` prints *"Skills reloaded. Found 26 skills."* and
  `/skills info diff-review` prints Source (Project), Location
  (`.claude\skills\diff-review\SKILL.md`), and Description. The setup step stands as
  written. **Method, because the first attempt was void:** `copilot -p "/skills reload"`
  does **not** run the slash command — the text goes to the model, which answered
  *"Skills reloaded"* itself (20.8k tokens) and, for `info`, searched for and read the
  SKILL.md and summarized it: authoring hazard 4, a report of the action instead of the
  action. The confirmation came from a real interactive session driven through a
  pseudo-terminal (`pywinpty` + `pyte` in a scratch venv), the rendered screen read back,
  `0 AIC used`. The same screen shows a vendor defect worth knowing: the Understand
  Anything plugin's `understand` skill **fails to load** on Copilot (*"argument-hint must
  be a string"*).
- **`COPILOT.md` has not been re-verified since 1.0.78.** Stale as of this date:
  `/rubber-duck`'s Claude/GPT-only constraint (every family since 1.0.87); the
  `/plugins` dashboard (removed 1.0.81) and `copilot plugins install --skill` (now
  `copilot skill add [--project]`, 1.0.85). New evidence for the `/fleet` question: hook
  lifecycle events inside a subagent are recorded since 1.0.81, so hooks do run there —
  still a bench question before any use.

### 78.5 The launcher fix designed — four shapes measured, one survives every build and
### route, and "loud" turned out to mean something narrower than the kit assumed —
### 2026-09-27

**The candidates, measured before choosing.** One probe JSON carrying four launcher
shapes side by side, each calling a script that logs its cwd, `[ -d .git ]`,
`[ -e .git ]`, the stdin byte count, and `uname -s`. Run on the trusted bench from `spec/`
and from a linked worktree created inside it (owner-approved, removed after), on the
genuine release zips:

- **V0** — today: `if [ -d .git ] && [ -f .github/hooks/<s> ]; then cat | sh …; fi`
- **V1** — `"cwd": "."` on the entry (documented: *"relative to repository root or
  absolute"*), test `[ -e .git ]`, body otherwise unchanged and `$`-free
- **V2** — `cd "$(git rev-parse --show-toplevel)" && if [ -f … ]; then cat | sh …; fi`
- **V3** — `"exec": "sh"`, `"args": [".github/hooks/<s>", …]`, `"cwd": "."` (no shell)

| build | route | from `spec/` | from a worktree |
|---|---|---|---|
| 1.0.63 | Git Bash | V0 V1 V2 V3 all ran at root | V1 V2 V3 ran; V0 skipped |
| 1.0.78 | Git Bash | V1 V2 V3 ran; V0 skipped | V1 V2 V3 ran; V0 skipped |
| 1.0.86 | Git Bash | V1 V2 V3 ran; V0 skipped | V1 V2 V3 ran; V0 skipped |
| 1.0.86 | PowerShell → WSL | V1 V2 ran; V0 skipped; **V3 never fired** | V1 V2 ran; V0 V3 did not |
| 1.0.88 | Git Bash | all four ran | V1 V2 V3 ran; V0 skipped |
| 1.0.88 | PowerShell → WSL | V0 V1 V2 ran; **V3 never fired** | V1 V2 ran; V0 V3 did not |

Every firing variant received the full payload on stdin. Three facts fall out:

1. **V1 is the fix: declarative, `$`-free, and correct on every supported build and
   both routes**, subfolder and worktree alike — from the kit's floor (1.0.63) to the
   latest. `"cwd": "."` resolves to the *worktree's* root in a worktree, which is what
   the hooks need.
2. **The subfolder defect was a regression, not the original behaviour:** on 1.0.63 V0
   ran at the root from `spec/`. Somewhere in 1.0.64–1.0.77 hooks started inheriting the
   session cwd; 1.0.88 restored the root. So a "recommended floor of 1.0.88" (§78.3) is
   **withdrawn** — V1 makes every build from 1.0.63 safe, and 1.0.88 does not fix the
   worktree case anyway.
3. **V2 survived the WSL route** — `$(git rev-parse …)` evaluates to the same path in
   whichever layer expands it, unlike a `$var` defined in the body. It works, but it
   leans on a re-parse the kit has measured misbehaving three ways; V1 needs nothing
   from it. **V3 is out:** on a PowerShell launch there is no `sh` on the path it
   resolves, and it fails without a trace.

**"Loud" measured (1.0.88, 2026-09-27).** A `preToolUse` hook writing stderr and
exiting 0, and `postToolUse` / `agentStop` hooks writing stderr and exiting 1:

| hook outcome | reached the agent or the `-p` output | recorded |
|---|---|---|
| `preToolUse`, stderr, exit 0 | no | **nowhere** |
| `postToolUse`, stderr, exit 1 | no — the agent reported *"no hook messages appeared"* | session `events.jsonl`, process log |
| `agentStop`, stderr, exit 1 | no | session `events.jsonl`, process log |

So an exit-code failure is a log line nobody reads. That includes **the skill ledger's
not-at-root branch**, which the kit describes as its one loud launcher: it is loud to
`~/.copilot/session-state/<id>/events.jsonl` and nowhere else. The channels measured to
reach the agent are a `preToolUse` **deny** (the reference: exit 2 or any other non-zero
denies the call — it blocks work) and an `agentStop` **block** with a reason (the
close-out backstop's schema, bench-measured in §52; the CLI ends a turn after 8
consecutive blocks and passes `stop_hook_active`).

**The design, as proposed:**

- **D1 — every Copilot launcher gains `"cwd": "."` and tests `[ -e .git ]`.** Four JSON
  templates (gate, TDD guard ×3, close-out, skill ledger). The bodies stay `$`-free.
- **D2 — state lives in the per-worktree git directory, `git rev-parse --git-dir`** —
  the IMPACT precedent (§66.2 (e), `sdlc-impact.template.py:272`). In an ordinary
  checkout that *is* `.git`, so every existing path, licence, and log resolves exactly
  as today: **no migration for either adopter.** Touches the three script templates'
  root/state lines (`tdd-guard.template.sh:76–79`, `close-out.template.sh:106–107,
  150–151, 309–312`), `tdd-guard-claude.template.py`'s `repo_root()` and `S`, and the
  skill ledger, whose Copilot body writes `.git/sdlc-skill-ledger.jsonl` inline — it moves
  to a script file on the Claude dialect's `skill-ledger-claude.template.sh` pattern
  rather than growing a `$(…)` in a launcher.
- **D3 — the prose names the location once, and the ~30 `.git/sdlc-*` references
  stand.** `SDLC.template.md` states that `.git/` in every kit path means the repository's
  git directory — `git rev-parse --git-dir`, which is `.git/` except in a linked worktree.
  The licence-writing sites (`end-slice.md` §3/§5/§6, `SDLC.template.md:196–203`) name
  the command, because those are the paths an agent *writes*; in a worktree the literal
  path fails with an error rather than silently, which is the right failure but not a
  usable instruction.
- **D4 — the one loud branch sits on the stop hooks.** A stop-bearing launcher (TDD
  guard's `agentStop`, close-out's) whose `[ -e .git ] && [ -f … ]` test fails emits
  `{"decision":"block","reason":"SDLC hooks did not run: …"}` instead of falling through
  — reaching the agent, which reports it. Pre and post launchers stay exit-0 on that
  branch: a deny there would block every write on a broken install, and the stop hook of
  the same family reports the same fault a turn later. With D1 in place this branch
  fires only on a broken install (script missing), so its cost is paid only where it is
  deserved; the 8-block cap bounds it. The ledger's exit-1 branch gets its description
  corrected (loud to the session log, not to anyone reading) in the same batch.
- **D5 — the Claude dialect:** the close-out `Stop` block's `sh -c "if [ -d .git ] …"`
  becomes `[ -e .git ]`; `repo_root()` accepts a `.git` file; `sdlc-gate-claude.sh` and
  `skill-ledger-claude.template.sh`'s `-d "$CLAUDE_PROJECT_DIR/.git"` become `-e`. No cwd
  change — Claude Code runs hooks at the project root (measured), so it was never
  exposed to the subfolder half. **Its worktree behaviour is read, not run** — a Claude
  Code worktree session is owed as a live proof.

**Proofs, pre-registered.** In each of the four suites (`tdd-guard-check.py`,
`close-out-check.py`, `gate-hook-check.py`, `skill-ledger-check.py`): a template-shape
assertion that every Copilot launcher carries `"cwd": "."` and no `[ -d .git ]`; a
fixture where `.git` is a *file* from a real `git worktree add`, driving each body and
script and asserting state lands in the per-worktree git dir; a mutation restoring
`[ -d .git ]` that the fixture must kill. Then live, on the bench: 1.0.63 and 1.0.88,
both routes, from `spec/` and from a worktree, with the real templates rather than a
probe — the guard denying (in deny mode) and the ledger recording, not merely firing.

**Cost.** Six template files, four proof suites, three prose sites with real edits
(the definition in `SDLC.template.md`, the licence lines, the ledger's loudness claim),
`GATE_RECIPES.md`'s launcher description (lines 273, 380, 517) and `COPILOT.md`'s
hooks section. `sdlc-update.md` classifies the hook JSONs as kit-owned verbatim files, so
the fix reaches both adopters by an ordinary update; the instantiated guard body is the
one piece that needs the re-instantiation path the 0.28.1 fix used.

**Rulings owed:**

1. **Worktree scope — full support (D2 + D3), or a loud refusal?** The refusal is
   cheaper in prose but not in scripts: detecting a worktree and saying so needs the same
   root and state lines touched, and leaves `/worktree` sessions — standard on Copilot
   since 1.0.85, and the isolation mode Claude Code's own subagents use — running
   unguarded, loudly. **Recommend full support.** No adopter is known to use worktrees,
   but a silent disarm is exactly the defect whose absence of evidence is its signature.
2. **D4's loud channel — `agentStop` block, as proposed, or log-only?** Recommend the
   block: it is the one channel measured to reach anyone, and it fires only on a broken
   install.
3. **Release shape — a patch (0.31.1), on the 0.28.1 precedent for a silent disarm of
   the guard,** or folded into the next minor with whatever the adopters' next arcs
   bring. Recommend the patch.

### 78.6 Ruled 2026-09-27 — all three, as recommended

1. **Worktree scope — RULED: full support.** D2 (state in `git rev-parse --git-dir`) and
   D3 (the location named once; the licence-writing sites name the command) are built,
   not a refusal.
2. **Loud channel — RULED: the `agentStop` block (D4).** Pre and post launchers stay
   exit-0 on the broken-install branch; the stop hooks of the same family report it.
3. **Release — RULED: patch 0.31.1**, on the 0.28.1 precedent, then an ordinary adopter
   update (the instantiated guard body re-instantiated as in 0.28.1).

Build order, as §78.5 pre-registered it: proofs first in the four suites (the worktree
fixture and the `[ -d .git ]` mutation must fail on today's templates), then D1, D2,
D5, D4, D3, then the live bench pass (1.0.63 and 1.0.88, both routes, subfolder and
worktree, real templates) and a Claude Code worktree session, then `/kit-check`
pre-tag.

### 78.7 Built 2026-09-27 — and four things the build found that the design did not

**Built as ruled (§78.6), proofs first.** Every new case was run against the committed
templates before the fix and failed there, then passed after: the Copilot guard (21b,
26a–26c, 26e, 27), the Claude guard (28–28d), the close-out worktree pass (four cases),
and the gate launcher (two cases, under both JSON parsers). D1–D5 are in the templates;
the ledger body moved to `templates/skill-ledger.template.sh` (renamed from
`skill-ledger-claude.template.sh`), shared by both CLIs.

**1. Path flavour inside a worktree — a design gap, measured before it was coded.** A
worktree made by Windows git writes `gitdir: D:/…` into its `.git` file. Under WSL bash
that path does not exist as written, and **WSL's own git cannot follow it either** —
`fatal: not a git repository: …/.wt-probe/D:/AICourse/…` on `rev-parse` and `rev-list`
alike — while the same git works when `GIT_DIR` points at the translated `/mnt/d/…`
path and `GIT_WORK_TREE` at the worktree. So §78.5's "use `git rev-parse --git-dir`"
could not be taken literally on the adopters' route. The scripts read the `.git` file
themselves, with the gate's drive-letter translation, and the close-out script exports
`GIT_DIR`/`GIT_WORK_TREE` when — and only when — it is in a worktree git cannot resolve.

**2. Quotes in a launcher — measured, and the suites' rule narrowed to match.** Three
suites banned quote characters from launcher bodies "as a precaution"; the 2026-08-07
measurements were backslashes and `$(cat)`, and 2026-09-27 added a `$var` defined in the
body. D4's else-branch has to print JSON. Probed first on both routes (1.0.88) with the
exact branch: the block reached the agent (`D4-SEEN`), once, standing down on
`stop_hook_active` via `grep -q 'stop_hook_active.: *true'`.
The guard suite's case 21 now asserts what was measured — no backslash, no `$`. The gate
and ledger launchers still carry no quotes at all.

**3. The 0.28.1 guard fix was blind on the WSL route — found by the pre-registered live
pass, and the most serious thing in this batch.** Under WSL bash the guard's root reads
`/mnt/d/…`, the second candidate root comes from `pwd -W`, which is MSYS-only and
prints nothing, and the CLI still reports `D:\…`. So every absolute-path write matched
neither candidate and fell to *"write outside the repository - not production source"* —
**the §72 defect, live on exactly the route the adopters launch by**, since 0.25.0.
0.28.1's re-arm was proven on Git Bash. Measured 2026-09-27 on the real templates, deny
armed: the Git Bash launch denied, the PowerShell launch of the same build logged
*outside the repository* and **let the write through** (three bench edits, reverted).
Fixed with a third candidate — the mount form translated back to drive form — behind a
harness knob, `SDLC_WSL_MOUNT`, because the suite's host has no `/mnt` to build a
fixture in; proof case 24d fails on the committed guard and passes on the fix, and a
mutation dropping the candidate is caught by it.

**4. The licence path the refusal names must be one the agent can write.** Live under
WSL in a worktree, the fixed guard's refusal named
`/mnt/d/…/worktrees/-wt-probe/sdlc-tdd/refactor-license` — correct for the hook shell,
unusable for the agent, whose tools take drive paths. The display path now translates
back to drive form; case 24e pins it, with a mutation.

**The live pass (pre-registered in §78.5), on the real templates, deny armed:**

| build | route | from | verdict | where logged | licence path named |
|---|---|---|---|---|---|
| 1.0.63 | Git Bash | `spec/` | DENY | main git dir | `.git/sdlc-tdd/…` |
| 1.0.63 | Git Bash | worktree | DENY | worktree git dir | worktree git dir, drive form |
| 1.0.86 | Git Bash | `spec/` | DENY | main git dir | `.git/sdlc-tdd/…` |
| 1.0.88 | Git Bash | `spec/` | DENY | main git dir | `.git/sdlc-tdd/…` |
| 1.0.88 | Git Bash | worktree | DENY | worktree git dir | worktree git dir, drive form |
| 1.0.86 | PowerShell → WSL | `spec/` | DENY (after fix 3) | main git dir | `.git/sdlc-tdd/…` |
| 1.0.86 | PowerShell → WSL | worktree | DENY (after fix 3) | worktree git dir | `/mnt/…` → fix 4 |
| 1.0.88 | PowerShell → WSL | `spec/` | DENY (after fix 3) | main git dir | `.git/sdlc-tdd/…` |
| 1.0.88 | PowerShell → WSL | worktree | DENY (after fix 3) | worktree git dir | `/mnt/…` → fix 4 |

1.0.86 from `spec/` is the row that exercises `"cwd": "."` itself — 1.0.63 and 1.0.88
start hooks at the root either way. The skill ledger recorded into the main git dir from
`spec/` and into the worktree's from the worktree, on 1.0.63 and 1.0.88. Two method notes:
a run from `spec/` needs `--allow-all-paths`, or Copilot's own path sandbox refuses to
read `../payments.js` and the guard never sees an edit (the first `spec/` pass was void
for that reason, not a guard miss); and the probe skill's own text ("do not run any
tools") suppressed the edit in the first combined run — a fixture defeating its own case,
the §72 lesson again.

**The Claude Code worktree session (D5's live proof, owed by §78.5).** Claude Code
2.1.283, a real headless session in the probe worktree, the new Python guard and the new
`Stop` launcher installed there, deny armed in the worktree's git dir: the guard
**denied** the edit, logged `[claude:pre-write] DENY` in the worktree's own git dir, and
its refusal named `D:/AICourse/copilot-ci-test/.git/worktrees/-wt-probe/sdlc-tdd/
refactor-license`. The close-out `Stop` hook logged `stop: clean` in the same git dir —
**but only when the session was launched from PowerShell.** Launched from Git Bash it
never ran: *"requires bash but Git Bash was not found"*, visible only under `--debug`.
Git for Windows is at a non-default path on this machine; the plausible mechanism is
Claude Code deriving Git Bash from the `git.exe` on `PATH`, which is `cmd\git.exe` from
PowerShell and `mingw64\bin\git.exe` inside Git Bash. **Every `sh`-form Claude hook the
kit ships — gate, ledger, backstop — fails the same way on that route**, while the
`python …` guard commands run. Not a 0.31.1 regression (the old `sh -c` form needs bash
too), and TFit-Foundation lives on this machine — whether its operator ever launches
from Git Bash is unknown. Recorded in `GATE_RECIPES.md` with the documented remedy
(`CLAUDE_CODE_GIT_BASH_PATH`) and the standing prove-from-the-real-route rule; not
otherwise acted on.

**Shipped-citation check.** The build first wrote eight `FEATURE_PLAN.md` citations into
shipped templates and one into `GATE_RECIPES.md`; invariant 5 (pointers in installed
files must resolve in the installed world) and the 0.29.0/d014dc2 cleanup rule them out.
Replaced with the release tag or the measurement date before commit; the bundle carries
none.

## 79. Copilot CLI runs the Claude-dialect hooks too — `.claude/settings.json` is
## Copilot repo config, so a project carrying both dialects runs both in every Copilot
## session — filed 2026-09-27, not ruled

**Found during §78's bench work.** A Copilot session's `agentStop` record showed a
failure from `"source": "repo settings"`: the kit's Claude-dialect close-out `Stop`
command, run by Copilot **through PowerShell**, which cannot parse `if [ … ]` —
*"ParserError: Missing '(' after 'if' in if statement"*. The changelog is explicit:
1.0.12 (2026-03-26) — *"Read .claude/settings.json and .claude/settings.local.json as
additional repo config sources."* `COPILOT.md` never recorded it.

**Measured consequences on the bench (1.0.88):** the Claude guard's Python body runs in
Copilot sessions — `[claude:pre-write] no path parsed from the write payload`,
`[claude:stop-check] stop: clean` lines appear beside the Copilot guard's own — against
a payload shape it was not written for, sharing the same `sdlc-tdd/` state directory;
and the shell-form Claude launchers fail to parse under PowerShell, adding a failed hook
record to every stop. Nothing observed was *harmful* on the bench — the Python guard
found no path and did nothing; the shell ones failed — but "harmless by accident" is not
a design, and the two guards writing one state directory in one session is exactly where
an accident would stop being harmless.

**Exposure:** projects that installed **both** dialects' hooks and run Copilot there.
Neither adopter is exposed today: ai-news-dashboard has no `.claude/settings.json`, and
TFit-Foundation runs Claude Code only. The bench is exposed by construction.

**Not designed yet** — the options are real and not obvious: make each Claude-dialect
command a no-op under a Copilot payload; move the Claude hooks to a file Copilot does not
read (`.claude/settings.local.json` is also read, so not that one); or state in setup
that a both-CLIs project should expect the doubling. Recorded in `COPILOT.md`'s
2026-09-27 re-verification; owed a design and a ruling.

### 78.8 The pre-0.31.1 `/kit-check` — run 2026-09-27: eleven findings, all fixed
### in-session, and the full suite run caught four mutations the new cases could not see

The reading passes ran as three parallel read-only agents (invariants 7/8/12,
1/2/5/6/14/15/16, 3/4/11/13 plus the lens↔rule map); the mechanical checks and the six
suites ran here.

**Findings, by where they came from:**

- **Introduced by 0.31.1 and fixed:** (2) setup's guard-note list restated the note's
  contents without the new `.git/`-in-a-worktree definition, so a fresh setup would omit
  it — the §76.3 "command restates half the contract" class, a fourth time; (2) two
  licence-declaring sites (end-slice step 5, the SDLC template) still named the bare
  path; (8) the README's 0.31.1 note lacked the update note's record step; (14) Copilot
  adopters' ledger note would name only the JSON after the body moved to a script; (14/15)
  **per-worktree state was an unstated consequence of D2** — deny armed in the main
  checkout does not arm a worktree — now said wherever a mode is recorded; (15) the
  re-prove step named no launch route, although finding (c) lived on the PowerShell
  route only and a Git Bash re-prove would pass over it; (7) the bundle README still
  called the ledger script Claude-side.
- **Pre-existing, fixed:** (7) `sdlc-impact.py` (0.28.0) was missing from the bundle
  README's kit-owned list and verbatim-copy count, from the "four exceptions" (five), and
  from **both** update-procedure denominator checks — so on any project with the adapter
  the classifier loop printed one line more than its check expected; the README's loop
  had also lost a line continuation.
- **Invariant 13:** the ledger's denominator list named none of the three new checks
  (extended); no case ran a stop launcher **with** its script present (37d and two
  close-out cases added — a typo in the launcher's `-f` path would have blocked every
  stop); case labels 26/27 were duplicated (the new blocks moved to 36/37).

**The full suite run** — the first with `-u`, sequential, ~80 minutes — exited 1 on three
suites, and every one was a real gap in this batch's own proofs rather than a product
defect: two guard mutations survived (removing the no-`.git` early exit; resolving a
relative gitdir against the cwd), one Claude mutation went stale (the `isdir` → `exists`
change moved its anchor — reported STALE by design, not counted), and one close-out
mutation survived (it mutated a `mkdir` whose directory an earlier case had already
made). The two "trust any cwd" mutants were not equivalent: git-dir resolution now
absorbs the non-repo *pre-write*, but at *stop* the early exit is what keeps a session
started outside any repository from being blocked with "did not run" — cases 25b
(Copilot) and 24b (Claude) pin that. 36f pins root-relative gitdir resolution; the
close-out mutation was re-aimed at the write. Each re-verified caught before the final
run. Passing on the first full run were `gate-hook-check`, `skill-ledger-check` and
`impact-check` (rc 0), and every unit case in the other three.

**The final run, after the repairs — all six exit 0.** `close-out-check`: 26 unit + 7
docs + 20 stop cases plus the 13-case worktree/launcher pass, 32 mutations caught, median
stop 886 ms against 1500 (cap-20 walk 3179 ms against 5000). `tdd-guard-check`: 80 cases
under each of python and node, 30 mutations caught. `tdd-guard-claude-check`: 51/51, 22
mutations caught. From the first run, unchanged since: `gate-hook-check` OK (both
parsers), `skill-ledger-check` 17/17, `impact-check` 17 cases and 13 mutations caught.
Manifest regenerated and verified 44/44 against the working tree and the git index (the
binary-mode `*` trap recurred on the first attempt and was caught before install).

### 78.9 A regression 0.31.1 shipped, caught by an adopter's own tests — 0.31.2, same day

During TFit-Foundation's 0.31.1 update the project's gate went red: **8 of its own
`tests/test_tdd_guard.py` cases** failed, every one with the guard printing nothing. Their
harness pins `SDLC_REPO_ROOT` to a bare `tmp_path` with no `.git` — the kit's own stated
contract ("an explicit SDLC_REPO_ROOT wins so a harness can pin it"), and through 0.31.0 the
guard created `ROOT/.git/sdlc-tdd/` there. 0.31.1's git-dir resolution (D2) returns nothing
when `.git` does not exist at all, so a pinned bare root now exited before guarding — in
both dialects. **Real hook invocations were never affected**: no CLI pins the root, and
every 0.31.1 live proof passed. It is a harness-contract regression, and invisible to the
kit's suites for one reason: **every fixture they build creates a `.git`**. The same
blind spot §78 itself was about — a fixture shaped like the one configuration that cannot
exhibit the defect — one level down, in this batch's own proofs.

**Fixed as 0.31.2**: a pinned root with no `.git` at all falls back to `ROOT/.git` (created
on demand, as before); a `.git` file naming no git directory still guards nothing and says
so at stop; the close-out checker and the ledger keep their stricter behavior (neither has a
pin, and the ledger must stay loud outside a repository). Case 25c in both guard suites pins
a bare directory — it fails on the published 0.31.1 templates and passes now — and a
mutation dropping the fallback is caught by it in each. **Acceptance: TFit's full suite
with the fix applied as a hunk (its amendments kept) — 845 passed, its recorded baseline.**

The lesson worth keeping is procedural, not technical: the adopter's gate is a proof suite
the kit does not own, and it ran a configuration no kit fixture did. An update's gate run
is therefore not a formality to skip on a hook-only release — it is the one place a
project's own tests exercise the kit's contracts.
