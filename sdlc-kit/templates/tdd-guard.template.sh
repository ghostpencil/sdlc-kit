#!/bin/sh
# SDLC TDD-ordering guards G1 + G2 (Copilot CLI dialect).
#
# G1 - observed-RED write guard: a production-source write is a violation unless a
#      test file has been edited this session AND a failing test run has been observed
#      since that edit. Both halves are required: a red alone proves nothing, because
#      any test-shaped command that exits non-zero (a pattern matching no tests)
#      manufactures one - found in the field on the first armed arc.
#      G1 carries a SECOND license for the refactor leg (field, 2026-08-08: with no
#      such license, armed close-out passes - change-simplify, mutation testing -
#      forced synthetic test-edit/red cycles or suppressed legitimate quality moves):
#      a production write is also allowed while .git/sdlc-tdd/refactor-license exists
#      AND a green run has been observed this session. The file is the session's own
#      explicit declaration that the edits are behavior-preserving; its first line
#      names the step and move, every write made under it is logged with that line so
#      review can audit the window, a test edit revokes it (a new test is a new
#      cycle), and it is cleared at session end. It survives reds on purpose:
#      mutation testing's expected reds and the revert of a failed refactor move are
#      production writes too, and G2 below still refuses to stop while the latest
#      observed run is red.
# G2 - premature-stop guard: stopping is a violation while no green test run has been
#      observed, or the latest observed run is red. The green is ANY counted green -
#      a single-test selector run satisfies it. That is division of labor, not a gap
#      (field, 2026-08-08): full-suite assurance is the end-slice gate's job, and this
#      backstop never runs tests inline. G2 exists to refuse red and never-ran stops.
#      G2 is SESSION-SCOPED to the work the ordering governs (owner-decided
#      2026-08-08): it binds only a session that made a production write that went
#      through, or edited a test (a written test never run is exactly a never-ran
#      stop). A session that did neither - planning, docs, bookkeeping - runs no
#      tests by design and stops clean; a denied write arms nothing, because the
#      tree did not change.
#
# Every observe-test outcome is SPOKEN back as context, not only logged: refusals
# with the reason and what is allowed (2026-08-08 - a silently refused session
# thrashed and probed the guard instead of complying), and counted RED/GREEN runs
# as the state fact each produced (2026-08-09, the same lesson pointed at the
# success side - a session otherwise learns its run counted only by the next deny
# not arriving). State facts, never instructions.
#
# LOGGING MODE IS THE DEFAULT. The guards only deny/block when the flag file
# .git/sdlc-tdd/deny-enabled exists; without it they log and always exit 0. Arm deny only
# once the log shows the guards recognizing the project's own test runs.
#
# This is a COOPERATIVE BACKSTOP, NOT A SECURITY BOUNDARY. Writes made through the
# shell tool are invisible to it, and the session can read or edit this script and its
# state. It exists to make TDD ordering the path of least resistance, not to make
# violating it impossible. (Both were observed in pre-release trials: a session read
# this script's own source to learn the recognized command format, complied with it,
# and could as easily have edited the state files instead.)
#
# Never runs the test suite inline: a hook that outruns timeoutSec fails open and
# silently stops guarding. State reads and writes only.
#
# JSON PARSER: needs python OR node - whichever is on the PATH of the shell the agent
# CLI runs hooks in, which is NOT necessarily the shell you type in. It detects that at
# run time rather than being told, because only the hook's own shell can answer it. With
# neither, the guard says so in its log and guards nothing; it never denies on its own
# failure. What that shell reported at setup is recorded in spec/SDLC.md beside the gate.

MODE=$1
# The hook config invokes this script from the repository root: the hook process's
# working directory is the session's cwd, in the executing shell's own path flavour
# (measured 2026-08-07 - and the reason the config passes nothing: anything richer
# than a bare command is corrupted when the CLI's hook shell is the WSL launcher,
# which re-parses the command line). An explicit SDLC_REPO_ROOT still wins so a
# harness can pin it. With no root given and no .git here, do nothing rather than
# write state to an unrelated directory.
if [ -z "$SDLC_REPO_ROOT" ]; then
  [ -d .git ] || exit 0
  SDLC_REPO_ROOT=$(pwd)
fi
S="$SDLC_REPO_ROOT/.git/sdlc-tdd"
mkdir -p "$S" 2>/dev/null
LOG="$S/guard.log"
IN=$(cat)

log() { printf '%s [%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$MODE" "$1" >> "$LOG" 2>/dev/null; }

# --- JSON parser: detect once, then run whichever dialect we found ------------------
# The two sources below are held in single-quoted shell strings, so neither may contain
# a single quote - both are written with double quotes throughout for that reason.
JP=""; JN=""
for c in python python3; do
  if command -v "$c" >/dev/null 2>&1; then JP=$c; break; fi
done
if [ -z "$JP" ] && command -v node >/dev/null 2>&1; then JN=node; fi

# jr <python-source> <node-source> - reads stdin, writes the same lines either way.
# `tr -d '\r'` is not optional: Windows python writes CRLF, and a stray CR turns every
# downstream string comparison false. Git Bash hides this (MSYS sed strips CR); WSL
# bash does not.
jr() {
  if   [ -n "$JP" ]; then "$JP" -c "$1" 2>/dev/null | tr -d '\r'
  elif [ -n "$JN" ]; then "$JN" -e "$2" 2>/dev/null | tr -d '\r'
  else return 127
  fi
}

PY_PARSE='
import sys,json,re
d=json.loads(sys.stdin.buffer.read().decode("utf-8","replace"))
o=[d.get("sessionId") or ""]
o.append(str(d.get("stop_hook_active") or d.get("stopHookActive") or "false").lower())
a=d.get("toolArgs") or d.get("tool_input") or {}
cmd=""
paths=[]
if isinstance(a,str) and a.lstrip()[:1] not in "{[":
    paths=[v.strip() for k,v in re.findall(r"^\*\*\* (Add|Update|Delete) File: (.+)$",a,re.M) if k!="Delete"]
else:
    a=json.loads(a) if isinstance(a,str) else a
    cmd=a.get("command") or ""
    p=a.get("path") or a.get("file_path") or a.get("filePath") or ""
    if p: paths=[p]
o.append(cmd.replace(chr(10)," "))
r=d.get("toolResult") or {}
t=(r.get("textResultForLlm") or "") if isinstance(r,dict) else ""
m=re.findall(r"completed with exit code (\d+)>",t)
o.append(m[-1] if m else "")
o.extend(paths)
sys.stdout.write("\n".join(o)+"\n")
'

JS_PARSE='
const d=JSON.parse(require("fs").readFileSync(0,"utf8"));
const o=[d.sessionId||""];
o.push(String(d.stop_hook_active||d.stopHookActive||"false").toLowerCase());
let a=d.toolArgs||d.tool_input||{},cmd="",paths=[];
if(typeof a==="string" && !"{[".includes(a.trimStart()[0]||"")){
  for(const m of a.matchAll(/^\*\*\* (Add|Update|Delete) File: (.+)$/gm)) if(m[1]!=="Delete") paths.push(m[2].trim());
}else{
  if(typeof a==="string") a=JSON.parse(a);
  cmd=a.command||"";
  const p=a.path||a.file_path||a.filePath||"";
  if(p) paths=[p];
}
o.push(cmd.replace(/\n/g," "));
const r=d.toolResult||{};
const t=(r&&typeof r==="object")?(r.textResultForLlm||""):"";
const mm=[...t.matchAll(/completed with exit code (\d+)>/g)];
o.push(mm.length?mm[mm.length-1][1]:"");
o.push(...paths);
process.stdout.write(o.join("\n")+"\n");
'

# Every field this guard reads, one per line:
#   1 sessionId  2 stop_hook_active  3 shell command  4 exit-code trailer
#   5+ patch paths (Add/Update only - a Delete has nothing to write-guard)
F=$(printf '%s' "$IN" | jr "$PY_PARSE" "$JS_PARSE")

if [ -z "$F" ]; then
  # No parser, or an unparseable payload. Say so; never deny on the guard's own failure
  # - a broken guard that denies reads as enforcement and blocks real work.
  if [ -z "$JP" ] && [ -z "$JN" ]; then
    log "GUARD ERROR: no JSON parser on this shell's PATH (needs python or node) - not guarding this call"
  else
    log "GUARD ERROR: could not parse the hook payload - not guarding this call"
  fi
  exit 0
fi

SID=$(printf  '%s' "$F" | sed -n 1p)
ACTIVE=$(printf '%s' "$F" | sed -n 2p)
CMD=$(printf   '%s' "$F" | sed -n 3p)
CODE=$(printf  '%s' "$F" | sed -n 4p)
PATHS=$(printf '%s\n' "$F" | tail -n +5)

# Observations are SESSION-scoped: a red observed in an earlier session does not
# license a production write in this one. A new sessionId resets them.
if [ -n "$SID" ] && [ "$SID" != "$(cat "$S/session" 2>/dev/null)" ]; then
  rm -f "$S/red-observed" "$S/green-observed" "$S/last-test-edit" "$S/refactor-license" "$S/prod-write-observed" 2>/dev/null
  printf '%s' "$SID" > "$S/session" 2>/dev/null
  log "new session $SID - previous observations cleared"
fi

# The output schemas below were measured against the CLI, not taken from documentation.
emit_deny() {
  printf '%s' "$1" | jr '
import sys,json
sys.stdout.write(json.dumps({"permissionDecision":"deny","permissionDecisionReason":sys.stdin.read()},separators=(",",":")))
' '
process.stdout.write(JSON.stringify({permissionDecision:"deny",permissionDecisionReason:require("fs").readFileSync(0,"utf8")}));
'
}
emit_block() {
  printf '%s' "$1" | jr '
import sys,json
sys.stdout.write(json.dumps({"decision":"block","reason":sys.stdin.read()},separators=(",",":")))
' '
process.stdout.write(JSON.stringify({decision:"block",reason:require("fs").readFileSync(0,"utf8")}));
'
}
# postToolUse context injection - the same measured schema the edit-time gate hook uses.
emit_context() {
  printf '%s' "$1" | jr '
import sys,json
sys.stdout.write(json.dumps({"additionalContext":sys.stdin.read()},separators=(",",":")))
' '
process.stdout.write(JSON.stringify({additionalContext:require("fs").readFileSync(0,"utf8")}));
'
}

case "$MODE" in

  pre-write)
    [ -n "$PATHS" ] || { log "no paths parsed from the write payload"; exit 0; }
    prod=""; test_touched=""
    # One path per line, read with IFS cleared: a path containing a space is one path,
    # not two. The heredoc (rather than a pipe) keeps the loop in this shell, so what it
    # accumulates survives it.
    while IFS= read -r p; do
      [ -n "$p" ] || continue
      # Paths arrive absolute-Windows AND repo-relative. Classify on the normalized
      # relative path and on the basename, so both `tests/*` and `test_*.py` shaped
      # patterns work. Test check runs FIRST: SOURCE_GLOB is extension-only, so it
      # matches test files just as readily as production ones.
      n=$(printf '%s' "$p" | tr '\\' '/')
      b=${n##*/}
      case "$n" in {{TEST_PATH_PATTERN}}) test_touched=1; continue ;; esac
      case "$b" in {{TEST_PATH_PATTERN}}) test_touched=1; continue ;; esac
      case "$b" in {{SOURCE_GLOB}})
        if [ -z "$prod" ]; then prod="$p"; else prod="$prod, $p"; fi ;;
      esac
    done <<PATHLIST
$PATHS
PATHLIST
    if [ -n "$prod" ]; then
      ok=""
      # "You changed a test this session, then watched it fail" - the red must have a
      # test edit before it, or it licenses nothing. The known cost: a resumed session
      # starts with cleared state, so its first production write is denied until a test
      # file is touched; the deny message names the way out.
      if [ -f "$S/red-observed" ] && [ -f "$S/last-test-edit" ] && [ "$S/red-observed" -nt "$S/last-test-edit" ]; then ok=red; fi
      # The refactor leg's declared license: behavior-preserving edits behind an
      # observed green. The declaration alone licenses nothing - without a counted
      # green this session there is no gate behind the claim.
      if [ -z "$ok" ] && [ -f "$S/refactor-license" ] && [ -f "$S/green-observed" ]; then ok=lic; fi
      # The marker below is what session-scopes G2: it records a production write that
      # actually WENT THROUGH. The deny branch sets nothing on purpose - a denied
      # write leaves the tree unchanged, and a stop guard armed by it would demand a
      # green for code that was never written.
      if [ "$ok" = "red" ]; then
        touch "$S/prod-write-observed" 2>/dev/null
        log "OK production write (red observed since last test edit): $prod"
      elif [ "$ok" = "lic" ]; then
        touch "$S/prod-write-observed" 2>/dev/null
        log "OK production write (refactor license: $(head -n 1 "$S/refactor-license" 2>/dev/null | tr -d '\r')): $prod"
      elif [ -f "$S/deny-enabled" ]; then
        log "DENY production write without observed red: $prod"
        emit_deny "TDD ordering: the write to $prod was denied because this session has not edited a test file and then observed a failing test run. For new behavior: write or edit one test, run it, watch it fail, then implement. Run the tests as a single bare command (no ';', '&' or '|' separators - the guard reads that run's own exit code, and a compound command's exit code is not the test's), then retry this edit. For a BEHAVIOR-PRESERVING edit at any point in the cycle (refactor, simplification, mutation testing - including a temporary mutation to prove a test of existing behavior bites): declare it instead - write one line naming the step and move to .git/sdlc-tdd/refactor-license, then retry. That license requires a counted green run this session, is revoked by the next test edit, ends with the session, and every write made under it is logged for review."
      else
        touch "$S/prod-write-observed" 2>/dev/null
        log "VIOLATION production write without observed red: $prod"
      fi
    fi
    # A test edit invalidates any earlier red: the new test needs its own observed red.
    # It also revokes any refactor license - a new test is a new cycle, and a window
    # declared for the last slice's close-out must not license this one's behavior.
    if [ -n "$test_touched" ]; then
      touch "$S/last-test-edit" 2>/dev/null
      log "test edit recorded (any earlier red is now stale)"
      if [ -f "$S/refactor-license" ]; then
        rm -f "$S/refactor-license" 2>/dev/null
        log "refactor license revoked (a test edit starts a new cycle)"
      fi
    fi
    exit 0 ;;

  observe-test)
    [ -n "$CMD" ] || exit 0
    case "$CMD" in
      {{TEST_CMD_PATTERN}}) ;;
      *) exit 0 ;;
    esac
    # The exit-code trailer reflects the WHOLE shell invocation, not the test. A
    # compound like `<test cmd>; echo done` reports the echo's status, so a red run
    # records a false GREEN - which both licenses a production write and un-blocks the
    # stop guard. Only bare single-command invocations count as observations.
    # A refusal is SPOKEN, never just logged: measured in the field (2026-08-08), a
    # session whose runs were refused silently learned about it only at the next
    # unexplained deny, then thrashed and probed the guard instead of complying -
    # and misattributed the refusals to rules the guard does not have.
    # Single-character classes on purpose: *"&"* catches & and &&, *"|"* catches | and
    # ||. The doubled-only forms were the 0.18.0 shape, and a single & slipped them -
    # the field's `cmd /c "... & ..."` probe (2026-08-08) was refused only by the `;`
    # inside its expanded PATH value, luck rather than design.
    case "$CMD" in
      *";"*|*"&"*|*"|"*)
        log "test run NOT counted (compound command - the exit code would be the compound's, not the test's): $CMD"
        emit_context "TDD ordering: that test run was NOT counted - the command is compound (contains ';', '&' or '|'), so its exit code is not the test's. The run itself is unaffected; it just registers nothing. Flags and single-test selectors are fine - to trim output use the runner's quiet flag, not a pipe. Re-run as one bare command to register the RED or GREEN."
        exit 0 ;;
    esac
    if [ -z "$CODE" ]; then
      log "test run seen but no exit-code trailer found: $CMD"
      emit_context "TDD ordering: that test run could not be counted - no exit code was found in the hook payload, so the guard cannot read the result. If this repeats on every run, the payload format has changed and the guard needs fixing before its ordering can be trusted."
    # Counted observations are SPOKEN, like the refusals above (owner-directed
    # 2026-08-09, the same invisible-state lesson pointed at the success side): the
    # session otherwise learns its run counted only by the next deny not arriving.
    # State facts only, never instructions - and the RED message claims a license
    # only when G1 would actually grant one, because a red with no test edit this
    # session is counted yet licenses nothing, and a message that says otherwise is
    # confidently wrong at the exact moment it is trusted.
    elif [ "$CODE" = "0" ]; then
      touch "$S/green-observed" 2>/dev/null; log "GREEN observed: $CMD"
      emit_context "TDD ordering: GREEN counted. The stop guard is satisfied; full-suite assurance remains the end-slice gate's job."
    else
      touch "$S/red-observed" 2>/dev/null; log "RED observed (exit $CODE): $CMD"
      if [ -f "$S/last-test-edit" ] || { [ -f "$S/refactor-license" ] && [ -f "$S/green-observed" ]; }; then
        emit_context "TDD ordering: RED counted (exit $CODE). A production write is now licensed for this cycle."
      else
        emit_context "TDD ordering: RED counted (exit $CODE) - but it licenses nothing yet: no test file has been edited this session, and a write license needs the test edit before its failing run."
      fi
    fi
    exit 0 ;;

  stop-check)
    # Stand down inside a forced continuation: never fight the documented block cap.
    if [ "$ACTIVE" = "true" ]; then
      log "stop: stop_hook_active set - standing down"
      exit 0
    fi
    # Session scoping (owner-decided 2026-08-08): the ordering G2 backstops is about
    # writes, so it binds only a session that made one - a production write that went
    # through (the pre-write marker), or a test edit (a written test never run is
    # exactly a never-ran stop). A planning, docs, or bookkeeping session runs no
    # tests by design; refusing its stop enforces a rule about writes against a
    # session that made none.
    if [ ! -f "$S/prod-write-observed" ] && [ ! -f "$S/last-test-edit" ]; then
      log "stop: clean (no production write or test edit this session - nothing to guard)"
      exit 0
    fi
    reason=""
    if [ ! -f "$S/green-observed" ]; then
      reason="no green test run has been observed in this session - run the test suite and get it green before finishing"
    elif [ -f "$S/red-observed" ] && [ "$S/red-observed" -nt "$S/green-observed" ]; then
      reason="the latest observed test run is red - get back to green before finishing"
    fi
    if [ -z "$reason" ]; then
      log "stop: clean (green observed, not stale)"
    elif [ -f "$S/deny-enabled" ]; then
      log "stop: BLOCK - $reason"
      emit_block "TDD ordering: $reason. (Run the tests as a single bare command so the guard can read that run's exit code.)"
    else
      log "stop: WOULD-BLOCK - $reason"
    fi
    exit 0 ;;

  *) log "unknown mode: $MODE"; exit 0 ;;
esac
