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
#      .git/sdlc-tdd/close-out-license is the same license scoped to /end-slice, and
#      differs in exactly one way: a test edit does NOT revoke it. Close-out's own
#      mandated order (review fixes tests -> mutation writes production and restores
#      tests -> verification writes a harness) cannot be executed under a license a
#      test edit revokes, and a real arc paid the re-declaration seven times in one
#      phase (field, 2026-09-01). Every test edit it survives is COUNTED and logged,
#      so a license held open past its step is visible in review rather than silent.
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
# This is a COOPERATIVE BACKSTOP, NOT A SECURITY BOUNDARY. A write made through the
# shell tool is not seen as it happens, only reported at the stop (outside_writes,
# below, 0.36.0), and the session can read or edit this script and its state. It
# exists to make TDD ordering the path of least resistance, not to make
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
# The hook config invokes this script from the repository root: its entries carry
# "cwd": ".", which the CLI resolves against the repository root - the worktree's own
# root in a linked worktree - on every build measured, 1.0.63 to 1.0.88. Without it
# the hook ran in the SESSION's cwd on 1.0.64-1.0.87, and a session started below
# the root guarded nothing (fixed in 0.31.1). The config passes nothing else: a
# richer command line is corrupted when the CLI's hook shell is the WSL launcher,
# which re-parses it. An explicit SDLC_REPO_ROOT still wins so a harness can pin it.
# With no root given and no .git here, do nothing rather than write state to an
# unrelated directory.
if [ -z "$SDLC_REPO_ROOT" ]; then
  [ -e .git ] || exit 0
  SDLC_REPO_ROOT=$(pwd)
fi

# The git directory. .git is a directory in an ordinary checkout and a one-line
# "gitdir: <path>" FILE in a linked worktree, whose path the creating git wrote in
# ITS flavour: a worktree made by Windows git names D:/..., which does not exist as
# written under WSL bash - and WSL's own git cannot follow it either (measured
# 2026-09-27). So the file is read here, not by git, and the path goes through the
# same drive-letter translation the gate hook uses. Relative gitdirs resolve
# against the root. In an ordinary checkout this is ROOT/.git, so every state path
# is exactly what it always was.
sdlc_git_dir() {
  if [ -d "$1/.git" ]; then printf '%s' "$1/.git"; return 0; fi
  [ -f "$1/.git" ] || return 1
  g=$(sed -n 's/^gitdir:[[:space:]]*//p' "$1/.git" | tr -d '\r' | tr '\\' '/')
  [ -n "$g" ] || return 1
  case $g in /*|[A-Za-z]:/*) ;; *) g="$1/$g" ;; esac
  if [ -d "$g" ]; then printf '%s' "$g"; return 0; fi
  dl=$(printf '%s' "$g" | sed -n 's|^\([A-Za-z]\):/.*|\1|p' | tr 'A-Z' 'a-z')
  rest=$(printf '%s' "$g" | sed -n 's|^[A-Za-z]:/\(.*\)|\1|p')
  if [ -n "$dl" ]; then
    for c in "/mnt/$dl/$rest" "/$dl/$rest"; do
      if [ -d "$c" ]; then printf '%s' "$c"; return 0; fi
    done
  fi
  return 1
}
# The ordinary checkout is tested inline: a $(...) is a fork, and on Windows sh every
# fork costs tens of milliseconds on a hook that runs on every write and every shell
# command (FORK, below).
if [ -d "$SDLC_REPO_ROOT/.git" ]; then GD="$SDLC_REPO_ROOT/.git"
else GD=$(sdlc_git_dir "$SDLC_REPO_ROOT") || GD=""
fi
# A harness-pinned SDLC_REPO_ROOT with no .git at all keeps its pre-0.31.1 meaning:
# state under ROOT/.git, created on demand (an adopter's own guard tests pin a bare
# temp directory - 0.31.1 made that guard nothing, silently, and 0.31.2 restores it).
# Unpinned, this cannot trigger: the no-.git exit above has already run.
[ -z "$GD" ] && [ ! -e "$SDLC_REPO_ROOT/.git" ] && GD="$SDLC_REPO_ROOT/.git"
if [ -z "$GD" ]; then
  # A .git that names no git directory: nowhere to keep state, so guard nothing -
  # but say so at stop, the one seat measured to reach anyone (measured 2026-09-27).
  if [ "$MODE" = "stop-check" ] && ! printf '%s' "$(cat)" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
    printf '{"decision":"block","reason":"SDLC TDD guard did not run: %s/.git names no git directory, so the writes in this session were not guarded. Tell the owner."}\n' "$SDLC_REPO_ROOT"
  fi
  exit 0
fi
S="$GD/sdlc-tdd"
# The licence directory as the deny message names it: the familiar relative form in
# an ordinary checkout, the real location in a worktree, where .git/ is a file.
# The agent writes that licence with its own tools, which take drive paths - so a
# worktree's git dir resolved under WSL (/mnt/d/...) is named in its drive form (D:/...).
# SDLC_WSL_MOUNT exists so a harness without a /mnt can pin the prefix; nothing sets it.
wm=${SDLC_WSL_MOUNT:-/mnt}
if [ "$GD" = "$SDLC_REPO_ROOT/.git" ]; then LIC=.git/sdlc-tdd; else
  LIC=$S
  case "$LIC" in "$wm"/?/*) LIC=$(printf '%s' "${LIC#"$wm"/}" | sed 's|^\(.\)/|\1:/|') ;; esac
fi
mkdir -p "$S" 2>/dev/null
LOG="$S/guard.log"
IN=$(cat)

log() { printf '%s [%s] %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$MODE" "$1" >> "$LOG" 2>/dev/null; }

# FORK: the string work below is done with parameter expansion, not `printf | sed` or
# `tr`, because every pipeline in a $(...) is two or three processes and Windows sh
# pays tens of milliseconds for each. Measured 2026-10-21 on the dev machine: a
# pre-write call cost ~2 s, ~40 forks with no single slow step.
NL='
'
# take: the first line of $rest into $v, and $rest loses it.
take() {
  case $rest in
    *"$NL"*) v=${rest%%"$NL"*}; rest=${rest#*"$NL"} ;;
    *) v=$rest; rest="" ;;
  esac
}
# slash: $1 with every backslash made a forward slash, into $r.
slash() {
  r=""; s=$1
  while :; do
    case $s in
      *\\*) r="$r${s%%\\*}/"; s=${s#*\\} ;;
      *) r="$r$s"; return 0 ;;
    esac
  done
}

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
u=re.sub(r"\x1b\[[0-9;]*[A-Za-z]","",t).replace(chr(13)+chr(10),chr(10))
try:
    o.append("1" if re.search(r"{{TEST_REPORT_PATTERN}}",u,re.M) else "0")
except re.error:
    o.append("E")
o.extend(paths)
sys.stdout.buffer.write(("\n".join(o)+"\n").encode("utf-8"))
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
const u=t.replace(/\x1b\[[0-9;]*[A-Za-z]/g,"").replace(/\r\n/g,"\n");
try{ o.push(new RegExp(String.raw`{{TEST_REPORT_PATTERN}}`,"m").test(u)?"1":"0"); }catch(e){ o.push("E"); }
o.push(...paths);
process.stdout.write(o.join("\n")+"\n");
'

# Every field this guard reads, one per line:
#   1 sessionId  2 stop_hook_active  3 shell command  4 exit-code trailer
#   5 the runner's own report found in the output: 1, 0, or E (the pattern is invalid)
#   6+ patch paths (Add/Update only - a Delete has nothing to write-guard)
# The report is matched in the parser, where a regular expression lives naturally, on
# the output with ANSI codes and CRLF removed: Copilot strips colour itself, but a
# project that forces it would wrap the marker (measured 2026-10-20).
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

rest=$F
take; SID=$v
take; ACTIVE=$v
take; CMD=$v
take; CODE=$v
take; REPORT=$v
PATHS=$rest

# Code that changed OUTSIDE the editor tools (0.36.0). This guard sees only the editor
# tools, so a shell write to source or a test was invisible to it: one adoption made
# about 28 unseen production writes in one armed phase (field report 11, finding 2).
# Detection, not prevention. The session's start is recorded, and at stop every code
# file whose CONTENT differs from that start, and that no pre-write saw, is reported.
# Content, never mtime, so the hash-verified mutation runner, which puts the same bytes
# back, never trips it. Commits dated before the session began (a pull, a merge) are
# not the session's. "Code" is the guard's own: SOURCE_GLOB minus the exempt paths,
# tests included. Fails open: any git failure reports nothing. Known costs: a
# formatter or generator writing into code nobody edited this session reads as a
# breach (the cure is the exempt pattern for generated directories); and so does a
# commit pulled in from elsewhere while the session runs. The session's FIRST tool
# call takes the snapshot, so a shell write in that very call is missed. The git
# directory and root are named outright: discovery could walk past a harness's bare
# temp root into whatever repository encloses it.
sdlc_git() {
  git -c core.quotepath=false -C "$SDLC_REPO_ROOT" --git-dir="$GD" --work-tree="$SDLC_REPO_ROOT" "$@" 2>/dev/null
}
is_code() {
  case "$1" in .ua/*|.understand-anything/*|{{GUARD_EXEMPT_PATTERN}}) return 1 ;; esac
  case "${1##*/}" in {{SOURCE_GLOB}}) return 0 ;; esac
  return 1
}
# Repo-relative paths git reports as changed or untracked; a rename's new name.
status_paths() {
  sdlc_git status --porcelain=v1 -uall | awk '{ p = substr($0, 4); i = index(p, " -> "); if (i) p = substr(p, i + 4); print p }'
}
# "<blob id><TAB><path>" for each path in the file $1 - an empty id for a file that is
# not there - in one git call.
blob_ids() {
  : > "$S/.there"; : > "$S/.gone"
  while IFS= read -r p; do
    [ -n "$p" ] || continue
    if [ -f "$SDLC_REPO_ROOT/$p" ]; then printf '%s\n' "$p" >> "$S/.there"
    else printf '\t%s\n' "$p" >> "$S/.gone"; fi
  done < "$1"
  if [ -s "$S/.there" ]; then
    sdlc_git hash-object --stdin-paths < "$S/.there" > "$S/.ids" || return 1
    paste "$S/.ids" "$S/.there"
  fi
  cat "$S/.gone"
}
record_start() {
  : > "$S/.cand"
  while IFS= read -r p; do
    [ -n "$p" ] && is_code "$p" && printf '%s\n' "$p" >> "$S/.cand"
  done <<STATUS
$(status_paths)
STATUS
  { sdlc_git rev-parse HEAD || echo; date +%s; blob_ids "$S/.cand"; } > "$S/session-start" 2>/dev/null
}
# The code files changed this session that no pre-write saw, not yet reported.
outside_writes() {
  [ -f "$S/session-start" ] || return 0
  { IFS= read -r h0; IFS= read -r t0; } < "$S/session-start"
  st=$(status_paths) || return 0
  now=$(sdlc_git rev-parse HEAD)
  if [ -n "$h0" ] && [ -n "$now" ] && [ "$now" != "$h0" ]; then
    st="$st$NL$(sdlc_git log --no-merges --since=@"$t0" --name-only --format= "$h0..HEAD")"
  fi
  : > "$S/.code"
  while IFS= read -r p; do
    [ -n "$p" ] && is_code "$p" && printf '%s\n' "$p" >> "$S/.code"
  done <<CANDIDATES
$(printf '%s\n' "$st" | awk 'NF && !seen[$0]++')
CANDIDATES
  # Seen or already reported drops out, case-folded because Windows reports either
  # case. One awk, not a grep per path: MSYS grep aborts on -i with -F (measured
  # 2026-10-22, Git for Windows), which read as "not seen" for every file.
  : >> "$S/seen-writes"; : >> "$S/reported-writes"
  awk 'FILENAME != ARGV[3] { skip[tolower($0)] = 1; next } !(tolower($0) in skip)' \
    "$S/seen-writes" "$S/reported-writes" "$S/.code" > "$S/.cand"
  [ -s "$S/.cand" ] || return 0
  blob_ids "$S/.cand" > "$S/.now" || return 0
  tail -n +3 "$S/session-start" > "$S/.start"
  : > "$S/.base"
  if [ -n "$h0" ]; then
    set --
    while IFS= read -r p; do set -- "$@" "$p"; done < "$S/.cand"
    sdlc_git ls-tree "$h0" -- "$@" | awk -F '\t' '{ split($1, m, " "); print m[3] "\t" $2 }' > "$S/.base"
  fi
  awk -F '\t' 'FILENAME == ARGV[1] { start[$2] = $1; had[$2] = 1; next }
               FILENAME == ARGV[2] { base[$2] = $1; next }
               { was = ($2 in had) ? start[$2] : base[$2]; if ($1 != was) print $2 }' \
    "$S/.start" "$S/.base" "$S/.now"
}

# Observations are SESSION-scoped: a red observed in an earlier session does not
# license a production write in this one. A new sessionId resets them.
prev=""
[ -f "$S/session" ] && IFS= read -r prev < "$S/session"
if [ -n "$SID" ] && [ "$SID" != "$prev" ]; then
  rm -f "$S/red-observed" "$S/green-observed" "$S/last-test-edit" "$S/refactor-license" "$S/close-out-license" "$S/close-out-survivals" "$S/prod-write-observed" "$S/seen-writes" "$S/reported-writes" "$S/state-spoken" 2>/dev/null
  printf '%s' "$SID" > "$S/session" 2>/dev/null
  log "new session $SID - previous observations cleared"
  record_start
fi

# SDLC state (89.4): the first line of <git-dir>/sdlc-state says whether the process is
# in force. `off` or `paused` -> this guard stands down: no state written, no output,
# exit 0; a paused production write is logged, never charged (the flag is read inside
# pre-write). Anything else - `absent` and any word this file does not know included -
# guards exactly as before, so a typo in a hand edit costs a spoken line, never a
# silent disarm. Read AFTER the session bookkeeping above, so a session that begins
# paused still records its start. Spoken once per session from observe-test, the one
# seat of this dialect whose context output is measured; it rides that call's own
# output when there is one and is emitted alone at exit otherwise.
STATE=""; SNOTE=""; EMITTED=""
[ -f "$GD/sdlc-state" ] && IFS= read -r STATE < "$GD/sdlc-state"
STATE=$(printf '%s' "$STATE" | tr -d '\r' | tr '[:upper:]' '[:lower:]')
if [ "$MODE" = "observe-test" ] && [ "$STATE" != "off" ] && [ ! -f "$S/state-spoken" ]; then
  case "$STATE" in
    paused)
      sk=""; ss=""; sr=""
      while IFS= read -r sl; do
        case "$sl" in stage:*) sk=${sl#stage:} ;; since:*) ss=${sl#since:} ;; reason:*) sr=${sl#reason:} ;; esac
      done < "$GD/sdlc-state"
      SNOTE="SDLC paused since${ss} (${sr# }) - the kit's hooks are standing down; /sdlc resume re-enters${sk:- the saved stage}." ;;
    "") SNOTE="no SDLC state file - guards active by default; /sdlc status" ;;
    phase|slice|close-out|phase-end) ;;
    *) SNOTE="unrecognized SDLC state '$STATE' - guards active; /sdlc status" ;;
  esac
fi
flush_state_note() {
  if [ -n "$SNOTE" ] && [ -z "$EMITTED" ]; then
    sn=$SNOTE; SNOTE=""
    : > "$S/state-spoken" 2>/dev/null
    emit_context "$sn"
  fi
}
trap flush_state_note EXIT

# The output schemas below were measured against the CLI, not taken from documentation.
# The message is read as bytes and decoded as UTF-8: a text-mode read on Windows python
# is cp1252 with surrogateescape, which turned a non-ASCII path in the message into
# mojibake (measured 2026-10-20).
emit_deny() {
  EMITTED=1
  printf '%s' "$1" | jr '
import sys,json
sys.stdout.write(json.dumps({"permissionDecision":"deny","permissionDecisionReason":sys.stdin.buffer.read().decode("utf-8","replace")},separators=(",",":")))
' '
process.stdout.write(JSON.stringify({permissionDecision:"deny",permissionDecisionReason:require("fs").readFileSync(0,"utf8")}));
'
}
emit_block() {
  EMITTED=1
  printf '%s' "$1" | jr '
import sys,json
sys.stdout.write(json.dumps({"decision":"block","reason":sys.stdin.buffer.read().decode("utf-8","replace")},separators=(",",":")))
' '
process.stdout.write(JSON.stringify({decision:"block",reason:require("fs").readFileSync(0,"utf8")}));
'
}
# postToolUse context injection - the same measured schema the edit-time gate hook uses.
emit_context() {
  EMITTED=1
  if [ -n "$SNOTE" ]; then : > "$S/state-spoken" 2>/dev/null; set -- "$SNOTE $1"; SNOTE=""; fi
  printf '%s' "$1" | jr '
import sys,json
sys.stdout.write(json.dumps({"additionalContext":sys.stdin.buffer.read().decode("utf-8","replace")},separators=(",",":")))
' '
process.stdout.write(JSON.stringify({additionalContext:require("fs").readFileSync(0,"utf8")}));
'
}

# The stand-down sits below the emitters so the exit trap can still speak the notice.
case "$STATE" in off) exit 0 ;; paused) [ "$MODE" = "pre-write" ] || exit 0 ;; esac

case "$MODE" in

  pre-write)
    [ -n "$PATHS" ] || { log "no paths parsed from the write payload"; exit 0; }
    prod=""; test_touched=""; nprod=0; pfile=""; ntest=0; tfile=""; prel=""
    # The candidate repository roots (why there are three: inside the loop, below).
    # They depend only on the root, so they are built once per call, not per path:
    # separators normalized and the trailing slash dropped, plus each one lowercased,
    # all three in one `tr`.
    wroot=""
    case "$SDLC_REPO_ROOT" in
      "$wm"/?/*) wroot=$(printf '%s' "${SDLC_REPO_ROOT#"$wm"/}" | sed 's|^\(.\)/|\1:/|') ;;
    esac
    slash "$SDLC_REPO_ROOT"; c1=${r%/}
    slash "$(cd "$SDLC_REPO_ROOT" 2>/dev/null && pwd -W 2>/dev/null)"; c2=${r%/}
    slash "$wroot"; c3=${r%/}
    rest=$(printf '%s\n%s\n%s' "$c1" "$c2" "$c3" | tr '[:upper:]' '[:lower:]')
    take; l1=$v; take; l2=$v; take; l3=$v
    # One path per line, read with IFS cleared: a path containing a space is one path,
    # not two. The heredoc (rather than a pipe) keeps the loop in this shell, so what it
    # accumulates survives it.
    while IFS= read -r p; do
      [ -n "$p" ] || continue
      # Paths arrive absolute-Windows AND repo-relative. Classify on the normalized
      # relative path and on the basename, so both `tests/*` and `test_*.py` shaped
      # patterns work. Test check runs FIRST: SOURCE_GLOB is extension-only, so it
      # matches test files just as readily as production ones.
      slash "$p"; n=$r
      # Reduce to a repo-relative path first, and drop anything that is not in the
      # repository at all. This dialect never attempted the reduction: it classified
      # on the full path and the basename, so an absolute path outside the root
      # matched the extension-only SOURCE_GLOB and was charged as production source -
      # a session scratchpad costing the same license as an edit to the module
      # guarding the project's authoritative data. Measured in the Claude dialect
      # over one arc (13 denials, 5 on a scratchpad, one mandated /end-phase step
      # unexecutable as written); this dialect
      # reaches the same end by a shorter route and only escaped notice because that
      # adopter's SOURCE_GLOB does not match its scratch files. Owner ruling: a file
      # outside the repository cannot be production source. Compared case-insensitively
      # because Windows hands back either case for the same directory.
      nl=$(printf '%s' "$n" | tr '[:upper:]' '[:lower:]')
      # TWO candidate roots, tried in turn, because the hook shell's own path flavour
      # and the flavour the CLI reports paths in NEED NOT AGREE. On Windows an MSYS
      # shell answers `pwd` with `/d/foo` while the CLI reports `D:\foo`; normalizing
      # separators does not reconcile those, since the drive form differs too, so a
      # root taken from `pwd` alone matches nothing that CLI ever sends. Not
      # hypothetical: it shipped in 0.25.0 and made every absolute path fall to the
      # "outside the repository" arm below, so the guard SKIPPED every write this CLI
      # reports by absolute path - which is how it reports them. Measured on an
      # adopter's own recorded path: the pre-0.25.0 body denied
      # it, the 0.25.0 body allowed it. A fix meant to narrow the guard's scope opened
      # a hole in it. Trying both flavours costs one subshell and cannot regress a
      # POSIX host, where the two answers are identical.
      # ...and a THIRD, because `pwd -W` exists only in MSYS: under WSL bash - the
      # hook shell whenever the CLI was launched from PowerShell - the root reads
      # /mnt/d/foo, `pwd -W` prints nothing, and the same D:\foo matched neither, so
      # the 0.28.1 fix left that route skipping every absolute-path write exactly as
      # 0.25.0 had (measured live 2026-09-27: the Git Bash launch denied, the
      # PowerShell launch of the same build logged "outside the repository" and let
      # the write through). The mount form translates back to the drive form here
      # ($wm is set beside the licence path, above). The three are built before
      # this loop, as c1-c3 with their lowercase forms l1-l3.
      rel=""
      for k in 1 2 3; do
        eval "c=\$c$k; cl=\$l$k"
        [ -n "$c" ] || continue
        case "$nl" in
          "$cl"/*)
            # The exact-case prefix strips without a fork; only a path the CLI
            # reported in a different case than the root falls to `cut`.
            case "$n" in
              "$c"/*) rel=${n#"$c"/} ;;
              *) rel=$(printf '%s' "$n" | cut -c $((${#c} + 2))-) ;;
            esac
            break ;;
        esac
      done
      if [ -n "$rel" ]; then
        n=$rel
      else
        case "$nl" in
          /*|?:/*)
            log "write outside the repository - not production source: $p"
            continue ;;
          ./*) n=${n#./} ;;
        esac
      fi
      b=${n##*/}
      # Exempt BEFORE the test check: a matching file is neither production nor a
      # test, so a script directory's own tests start no cycle either. SOURCE_GLOB is
      # extension-only, so before this a one-off tools script, a config written in the
      # source language and the graph tool's scratch each needed a red no test could
      # produce - measured on two adopters (2026-10-20). The graph tool's
      # directories are exempt in every project; GUARD_EXEMPT_PATTERN is the project's.
      # Logged only for a file the guard would otherwise have charged.
      case "$n" in .ua/*|.understand-anything/*|{{GUARD_EXEMPT_PATTERN}})
        case "$b" in {{SOURCE_GLOB}}) log "exempt from the guard (not production source, not a test): $n" ;; esac
        continue ;;
      esac
      # A test write is never denied, so it is seen through the editor tools at once:
      # the stop-time detector leaves it alone.
      case "$n" in {{TEST_PATH_PATTERN}}) test_touched=1; ntest=$((ntest + 1)); tfile="$SDLC_REPO_ROOT/$n"; printf '%s\n' "$n" >> "$S/seen-writes"; continue ;; esac
      case "$b" in {{TEST_PATH_PATTERN}}) test_touched=1; ntest=$((ntest + 1)); tfile="$SDLC_REPO_ROOT/$n"; printf '%s\n' "$n" >> "$S/seen-writes"; continue ;; esac
      case "$b" in {{SOURCE_GLOB}})
        if [ -z "$prod" ]; then prod="$p"; else prod="$prod, $p"; fi
        nprod=$((nprod + 1)); pfile="$SDLC_REPO_ROOT/$n"; prel="$prel$n$NL" ;;
      esac
    done <<PATHLIST
$PATHS
PATHLIST
    if [ "$STATE" = paused ]; then
      [ -z "$prel" ] || while IFS= read -r pr; do [ -n "$pr" ] && log "paused: unguarded production write: $pr"; done <<PAUSEDLIST
$prel
PAUSEDLIST
      exit 0
    fi
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
      # The close-out license answers here too; it differs only in what a test edit
      # does to it.
      if [ -z "$ok" ] && { [ -f "$S/refactor-license" ] || [ -f "$S/close-out-license" ]; } && [ -f "$S/green-observed" ]; then ok=lic; fi
      # A comment or formatting edit needs no red (GATE_RECIPES.md, cosmetic
      # exemption). Asked only of a write that would otherwise be denied or logged as a
      # violation, and only of a single-file write: edit and create carry one path, and
      # apply_patch keeps today's rule (the classifier answers "cannot tell" to it in
      # any case). It can only GRANT - python missing, the file missing, any exit but 0 leaves today's rule.
      # Its file is passed in the root's own flavour, which the hook shell's python can
      # read; the payload's path may be a drive path a WSL python cannot. Needs python,
      # not node: a node-only shell gets no exemption (stated in COPILOT.md).
      cos=""
      if [ -z "$ok" ] && [ "$nprod" = 1 ] && [ -n "$JP" ] && [ -f "$SDLC_REPO_ROOT/.github/hooks/sdlc-cosmetic.py" ]; then
        cout=$(printf '%s' "$IN" | "$JP" "$SDLC_REPO_ROOT/.github/hooks/sdlc-cosmetic.py" write "$pfile" 2>/dev/null; printf '\n%s' "$?")
        crc=$(printf '%s\n' "$cout" | tail -n 1 | tr -d '\r')
        cdetail=$(printf '%s\n' "$cout" | sed '$d' | head -n 1 | tr -d '\r')
        if [ "$crc" = 0 ]; then cos=${cdetail:-cosmetic}; ok=cosmetic
        else log "not cosmetic (${cdetail:-classifier exit $crc}): $prod"
        fi
      fi
      # The marker below is what session-scopes G2: it records a production write that
      # actually WENT THROUGH. The deny branch sets nothing on purpose - a denied
      # write leaves the tree unchanged, and a stop guard armed by it would demand a
      # green for code that was never written.
      # Every branch but the deny lets the write through, so every branch but the deny
      # records it as seen. A denied write changed nothing; a shell retry of the same
      # file is exactly what the stop-time detector exists to catch.
      if [ -n "$ok" ] || [ ! -f "$S/deny-enabled" ]; then
        printf '%s' "$prel" >> "$S/seen-writes"
      fi
      if [ "$ok" = "red" ]; then
        touch "$S/prod-write-observed" 2>/dev/null
        log "OK production write (red observed since last test edit): $prod"
      elif [ "$ok" = "lic" ]; then
        touch "$S/prod-write-observed" 2>/dev/null
        if [ -f "$S/close-out-license" ]; then which=close-out; else which=refactor; fi
        log "OK production write ($which license: $(head -n 1 "$S/$which-license" 2>/dev/null | tr -d '\r')): $prod"
      elif [ "$ok" = "cosmetic" ]; then
        # Logged, and arms nothing: a comment edit needs no green to stop on (82.9
        # ruling 2), the same reason a docs session stops clean.
        log "OK production write (cosmetic: $cos): $prod"
      elif [ -f "$S/deny-enabled" ]; then
        log "DENY production write without observed red: $prod"
        emit_deny "TDD ordering: the write to $prod was denied because this session has not edited a test file and then observed a failing test run. For new behavior: write or edit one test, run it, watch it fail, then implement. Run the tests as a single bare command (no ';', '&' or '|' separators - the guard reads that run's own exit code, and a compound command's exit code is not the test's), then retry this edit. For a BEHAVIOR-PRESERVING edit at any point in the cycle (refactor, simplification, mutation testing - including a temporary mutation to prove a test of existing behavior bites): declare it instead - write one line naming the step and move to $LIC/refactor-license, then retry. That license requires a counted green run this session, is revoked by the next test edit, ends with the session, and every write made under it is logged for review. If you are running /end-slice, declare $LIC/close-out-license instead - same rules, except a test edit does NOT revoke it, because close-out's own step order edits tests between its production writes; each test edit it survives is counted in the log."
      else
        touch "$S/prod-write-observed" 2>/dev/null
        log "VIOLATION production write without observed red: $prod"
      fi
    fi
    # A comment or formatting edit to a test is not a new cycle. Before 0.36.0 the
    # edit-time hook's format fix on a test, landing after its red run, staled the red
    # and revoked the licence (one adoption, its own field report). Asked only of a
    # single-file test write, and only when something is at stake - a live red or a
    # refactor licence - so an edit that would cost nothing never pays for the
    # classifier. Like the production ask, it can only GRANT.
    if [ -n "$test_touched" ] && [ "$ntest" = 1 ] && [ "$nprod" = 0 ] && [ -n "$JP" ] \
       && [ -f "$SDLC_REPO_ROOT/.github/hooks/sdlc-cosmetic.py" ] \
       && { { [ -f "$S/red-observed" ] && [ -f "$S/last-test-edit" ] && [ "$S/red-observed" -nt "$S/last-test-edit" ]; } || [ -f "$S/refactor-license" ]; }; then
      cout=$(printf '%s' "$IN" | "$JP" "$SDLC_REPO_ROOT/.github/hooks/sdlc-cosmetic.py" write "$tfile" 2>/dev/null; printf '\n%s' "$?")
      crc=$(printf '%s\n' "$cout" | tail -n 1 | tr -d '\r')
      cdetail=$(printf '%s\n' "$cout" | sed '$d' | head -n 1 | tr -d '\r')
      if [ "$crc" = 0 ]; then
        log "test edit is cosmetic (${cdetail:-cosmetic}) - not a new cycle: the red stands and no license is revoked: $tfile"
        exit 0
      fi
      log "not cosmetic (${cdetail:-classifier exit $crc}): $tfile"
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
      # A CLOSE-OUT license survives, because close-out's own mandated order puts
      # test edits between its production writes. It is counted, not silent: a
      # license still open after many test edits is one held past its step.
      if [ -f "$S/close-out-license" ]; then
        k=$(head -n 1 "$S/close-out-survivals" 2>/dev/null | tr -dc '0-9')
        [ -n "$k" ] || k=0
        k=$((k + 1))
        printf '%s' "$k" > "$S/close-out-survivals" 2>/dev/null
        log "close-out license SURVIVED a test edit ($k this session) - close-out edits tests between its production writes by design"
      fi
    fi
    exit 0 ;;

  observe-test)
    [ -n "$CMD" ] || exit 0
    # Classify on the command with quoted arguments removed. TEST_CMD_PATTERN is
    # substring-shaped by design (`*pytest*`, `*mvn*test*`), so matching it against
    # the raw string fired on any command whose TEXT merely mentioned the runner: a
    # `git commit -m` whose body quotes the RED command, an append writing a RED
    # record. Measured: three spurious notices in one phase, on a control whose
    # refusals have to be believed. Quoted text is data, never what the shell
    # runs. Known cost, stated rather than hidden:
    # a runner reachable ONLY inside a quoted argument (`bash -c "pytest"`) no longer
    # counts - run it bare, which is what the compound rule below asks for anyway.
    # The compound check deliberately keeps reading the RAW command: a stripping bug
    # there would admit a genuine compound and record a false GREEN, so that check
    # stays conservative and this one does not feed it.
    PROBE=$(printf '%s' "$CMD" | sed -e 's/"[^"]*"/ /g' -e "s/'[^']*'/ /g")
    case "$PROBE" in
      {{TEST_CMD_PATTERN}}) ;;
      *) exit 0 ;;
    esac
    # Commands that NAME the runner without running it - silent, like any other
    # non-test command. A substring pattern matched them: `cat vitest.config.ts`,
    # `grep pytest pyproject.toml`, `pip install pytest`, and a heredoc whose body (a
    # commit message, a file being written) names the run. A failure counted as a
    # RED, and - worse - a success counted as a GREEN that satisfied the stop guard
    # with no test run at all (found at 0.35.0's triage). The heredoc operator is never
    # quoted, so the stripped probe keeps it. The rest is judged on the leading
    # executable, after any `env` and NAME=value prefix: a fixed list on purpose,
    # because every mistake it makes lands on the not-counted side.
    case "$PROBE" in *"<<"*) exit 0 ;; esac
    W=$(printf '%s' "$PROBE" | awk '{ gsub(/\\/, "/"); $0 = tolower($0); n = 0; for (i = 1; i <= NF; i++) { if (n == 0 && ($i == "env" || $i ~ /^[a-z_][a-z0-9_]*=/)) continue; w[n++] = $i; if (n == 3) break } for (j = 0; j < n; j++) printf "%s ", w[j] }')
    set -f; set -- $W; set +f
    exe=${1##*/}; exe=${exe%.exe}; exe=${exe%.cmd}; exe=${exe%.bat}; exe=${exe%.ps1}
    case "$exe" in
      ""|cat|type|more|less|head|tail|sed|awk|grep|egrep|fgrep|rg|find|ls|dir|echo|printf|wc|diff|git|gh|jq|code|which|where|file|stat|pip|pip3|pipx|conda|get-content|gc|select-string|sls|get-childitem|gci|test-path|write-output|write-host) exit 0 ;;
      python|python3|py) [ "$2" = "-m" ] && [ "$3" = "pip" ] && exit 0 ;;
      npm|pnpm|yarn|bun|uv|poetry)
        case "$2" in install|i|add|ci|remove|rm|uninstall|un|update|upgrade|up|list|ls|view|info|show|outdated|audit|why|sync|lock) exit 0 ;; esac ;;
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
    # A failing exit is the COMMAND's verdict; a RED is the test's. A wrapper that
    # fails before the runner starts - pnpm's install check, a bad flag, a missing
    # binary, a filter matching no tests - exits with the code a failed test uses, and
    # was counted as the red that licenses a production write (sdlc-kit#16). So the
    # runner's own report must be in the output. Copilot delivers only the first 500
    # characters of a very long one (measured 2026-10-20), so the pattern is a marker
    # the runner prints first, never its closing summary (measured on both CLIs).
    elif [ "$REPORT" != "1" ]; then
      [ "$REPORT" = "E" ] && log "GUARD ERROR: TEST_REPORT_PATTERN is not a valid regular expression - no failing run can count as a RED until it is fixed"
      log "test run NOT counted (exit $CODE, but no test-runner report in the output - the failure is the command's, not a test's): $CMD"
      emit_context "TDD ordering: that failing run was NOT counted as a RED - it exited $CODE, but its output carries no test-runner failure report, so the failure is the command's, not a test's: an install or environment check, a bad flag, a missing binary, or a filter matching no tests. Fix that and re-run. If a test really did fail, its report was cut off by a long output - re-run it quieter (the runner's quiet flag or a single-test selector) to register the RED."
    else
      touch "$S/red-observed" 2>/dev/null; log "RED observed (exit $CODE): $CMD"
      if [ -f "$S/last-test-edit" ] || { { [ -f "$S/refactor-license" ] || [ -f "$S/close-out-license" ]; } && [ -f "$S/green-observed" ]; }; then
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
    # The outside-writes report runs before that scoping on purpose: a session whose
    # only code writes went through the shell never arms G2, and is exactly the one to
    # report.
    outside=$(outside_writes)
    said=""
    if [ -n "$outside" ]; then
      printf '%s\n' "$outside" >> "$S/reported-writes"
      ol=$(printf '%s\n' "$outside" | awk 'NF { printf "%s%s", (n++ ? ", " : ""), $0 }')
      if [ -f "$S/deny-enabled" ]; then
        log "stop: BLOCK - code changed outside the editor tools: $ol"
        said="TDD ordering: code changed outside the editor tools this session: $ol. Code - source and tests - changes only through the editor tools, the only writes this guard can see (the project instructions, Always-Active Rules); a shell write leaves the TDD order unverifiable. Tell the owner which files changed that way, how, and why."
      else
        log "stop: WOULD-REPORT - code changed outside the editor tools: $ol"
      fi
    fi
    if [ ! -f "$S/prod-write-observed" ] && [ ! -f "$S/last-test-edit" ]; then
      log "stop: clean (no production write or test edit this session - nothing to guard)"
      [ -n "$said" ] && emit_block "$said"
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
      said="${said:+$said }TDD ordering: $reason. (Run the tests as a single bare command so the guard can read that run's exit code.)"
    else
      log "stop: WOULD-BLOCK - $reason"
    fi
    [ -n "$said" ] && emit_block "$said"
    exit 0 ;;

  *) log "unknown mode: $MODE"; exit 0 ;;
esac
