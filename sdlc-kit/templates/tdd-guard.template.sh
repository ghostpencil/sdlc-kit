#!/bin/sh
# SDLC TDD-ordering guards G1 + G2 (Copilot CLI dialect).
#
# G1 - observed-RED write guard: a production-source write is a violation unless a
#      test file has been edited this session AND a failing test run has been observed
#      since that edit. Both halves are required: a red alone proves nothing, because
#      any test-shaped command that exits non-zero (a pattern matching no tests)
#      manufactures one - found in the field on the first armed arc.
# G2 - premature-stop guard: stopping is a violation while no green test run has been
#      observed, or the latest observed run is red.
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
# Set by the hook config's prelude, which derives it from the payload's own cwd. Unset
# means this script was invoked some other way; do nothing rather than write state to an
# unrelated directory.
[ -n "$SDLC_REPO_ROOT" ] || exit 0
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
  rm -f "$S/red-observed" "$S/green-observed" "$S/last-test-edit" 2>/dev/null
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
      if [ -f "$S/red-observed" ] && [ -f "$S/last-test-edit" ] && [ "$S/red-observed" -nt "$S/last-test-edit" ]; then ok=1; fi
      if [ -n "$ok" ]; then
        log "OK production write (red observed since last test edit): $prod"
      elif [ -f "$S/deny-enabled" ]; then
        log "DENY production write without observed red: $prod"
        emit_deny "TDD ordering: the write to $prod was denied because this session has not edited a test file and then observed a failing test run. Write or edit one test, run it, watch it fail, then implement. Run the tests as a single bare command (no ';', '&&', '||' or pipes - the guard reads that run's own exit code, and a compound command's exit code is not the test's), then retry this edit."
      else
        log "VIOLATION production write without observed red: $prod"
      fi
    fi
    # A test edit invalidates any earlier red: the new test needs its own observed red.
    if [ -n "$test_touched" ]; then
      touch "$S/last-test-edit" 2>/dev/null
      log "test edit recorded (any earlier red is now stale)"
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
    case "$CMD" in
      *";"*|*"&&"*|*"||"*|*"|"*)
        log "test run NOT counted (compound command - the exit code would be the compound's, not the test's): $CMD"
        exit 0 ;;
    esac
    if [ -z "$CODE" ]; then
      log "test run seen but no exit-code trailer found: $CMD"
    elif [ "$CODE" = "0" ]; then
      touch "$S/green-observed" 2>/dev/null; log "GREEN observed: $CMD"
    else
      touch "$S/red-observed" 2>/dev/null; log "RED observed (exit $CODE): $CMD"
    fi
    exit 0 ;;

  stop-check)
    # Stand down inside a forced continuation: never fight the documented block cap.
    if [ "$ACTIVE" = "true" ]; then
      log "stop: stop_hook_active set - standing down"
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
