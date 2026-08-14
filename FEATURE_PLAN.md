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
- **Standing input:** a TFit field report (Phase 07), whenever it arrives.
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
