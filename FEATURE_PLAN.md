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

- **The three STD lenses — RULED 2026-08-14, §54's (b): one final ATTRIBUTED
  clock.** The audit ran (§54): the runtime-standards recipe KEEPS on confirmed
  catches; the lenses had zero attributed catches in three arcs, with the recorded
  caveat that attribution was structurally invisible. The instrument is now fixed
  (lens verdicts report by name — `REVIEW_LENSES.md` preamble + all three calling
  sites, shipped with 0.22.0). **The clock: two field arcs from the next arc to
  run; only a lens-named catch counts; no further extension — a lens with none is
  deleted, with the conventions' enforcement lines re-pointed in the same batch.**
- **`change-verify` — clock satisfied** (§30.4): confirmed field catch at slice
  level, arc one, 2026-08-06 (§32.3).
- **`change-simplify` — RULED 2026-08-14: kept on a final clock, redirected first**
  (§30.4 expiry reconciled 2026-08-13; owner ruling (b) at the §52.8 halt; the
  improvement pass is §53). **The new clock: one confirmed catch in the next two
  field arcs, no further extension** — the impaired-arc argument (arc two's
  unlicensed guard) is spent with this ruling and cannot be re-used. The redirect
  shipped 2026-08-14: test code named in scope, Reuse searched not eyeballed,
  per-axis verdicts with the Reuse search named — built from the founding miss
  (Phase 04 S4's duplicated `LogCaptor` helper, "nothing to do" from this pass,
  caught by `diff-review` on the same diff).
- **R3.8's aging rule — no longer starved, still unexercised** (§16 contingent
  keep; reconciled 2026-08-13): R4.6's writer has produced real friction entries
  since 2026-08-08 (the adopter's guard-friction specimens), and the retro sweep
  consumed them in both later retros — but every entry so far was absorbed in its
  own arc, so the carry rule for entries **older than one phase** has never had one
  to carry. That is the healthy state, and the rule is its backstop; stays on the
  contingent keep.
- **Bare-flagging arming bar (§52.2)** — the backstop's bare-commit class stays
  log-only until **zero false candidates across the logging trial (banked
  2026-08-13, §52.7) and the first field arc**; the arming decision is
  evidence-bound, taken at a halt, never by default.
- **JUDGE — queued, not scheduled** (§37.5): the LLM-assisted layer for contracts a
  script verifies structurally but not semantically. Its design constraints are
  recorded there (never inside a timeout-bound tool hook; headless invocation on
  both CLIs; fixed rubric, forced verdict-plus-quotation; logging ramp; §16 clock
  from day one). VER.1 exists, so its precondition is met; it opens only when the
  owner schedules it.
- **CONTRACT — built 2026-08-15, unreleased; clock armed, not started** (§57.5):
  the product-contract mechanism runs the §16 clock from the first field arc under
  it. Value criterion pre-registered in §56.2: seeding the adopter's contract must
  surface P01's D6/D22/D23 as scheduled work or explicit owner retirement, and
  within two arcs a phase touching a contract surface must demonstrably encounter
  its entries. No confirmed catch after two field arcs → deletion candidate like
  any rule.
- **PIN — opened 2026-08-15, owner-directed, targeted at the next release** (§61):
  the Claude-dialect hook rewiring. Field-measured at the TFit 0.23.0 update: hooks
  behind `"shell": "bash"` never fire on Claude Code 2.1.231 — the adopter's gate
  hook had been silently inert. Design pre-registered in §61; decisions owed there.
- **IMPACT — opened 2026-08-18, design §66; ruled same day, queued behind
  RECON.** The §56.3 (d) hold resolved: the owner's visualization spec is
  ingested at the root (`FEATURE_SPEC_IMPACT.md`) and triaged — a deterministic
  Understand Anything impact adapter, eight deltas adopted. All five §66.7
  rulings taken 2026-08-18: RECON builds first, TFit-Foundation is the trial
  project (its `.ua/knowledge-graph.json` verified on disk), install path
  `.github/hooks/sdlc-impact.py`. The observed dashboard read landed
  2026-08-19 — (b) fully satisfied, the read path frozen against the real
  TFit pair (snapshotted, git-ignored `impact-fixture-source/`). Only RECON
  gates the build now. Its clock is pre-registered in §66.6 and counts only
  field arcs run with a usable graph.
- **Standing input — ARRIVED 2026-08-17, triaged in §63.** Both adopters closed a
  phase the same day and filed: the first adopter's Phase 07 (`sdlc-kit#7`, the
  seventh report) and the second's Phase 05 (`sdlc-kit#8`, the eighth). Ten findings,
  all standing; the clock evidence each arc carries is read in §63.4 and the rulings
  are owed there.
- **The Copilot bench is still standing** (§29.3): fixture repo
  `D:\AICourse\copilot-ci-test`; `pr-review-toolkit` installed on the owner's Copilot
  CLI; neither is tracked, reversal steps recorded there. The ENF, OBS, VER.2, and
  VER.3 trial artifacts stand on it (§31.16, §50.5, §52.7), including the backstop
  trio in logging mode.

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
