#!/bin/sh
# SDLC close-out evidence checker.
#
# Verifies that a slice commit's body carries the close-out evidence record the
# process mandates - the RED: / quality: / mutation: / verify: lines, each present
# or carrying its stated-skip form - and fails LOUDLY on silent absence. /end-slice
# runs it as its own step, right after the slice commit and before anything is
# pushed, and quotes its output either way: a pass not observed is not a pass.
#
# STRUCTURAL PRESENCE ONLY, never truth. This script cannot tell a real verify
# verdict from a characterization wearing a result's clothes; that is a semantic
# question for a different layer. Its pass output states this boundary so a
# COMPLETE is never read as "the evidence was verified".
#
# The grammar it enforces (presence-plus-non-empty; no shape policing - the
# payloads are prose, and a real field record legitimately varies its phrasing):
#   RED:      one or more lines, each with something after the colon - the observed
#             form, "not observed - <reason>", or the zero-form
#             "none - no behavior batches this slice".
#   quality:  exactly one line, non-empty. Two lines fail: nobody knows which is
#   mutation: the record. Zero lines or an empty payload fail: that is exactly the
#   verify:   silent absence this script exists to catch.
#
# TWO MODES, OPPOSITE FAIL DIRECTIONS - deliberately, and each for the same
# reason pointed at its own seat:
#   check      the /end-slice command step. FAILS CLOSED on its own errors: a
#              command step's failure is seen and quoted by the session, and a
#              checker that silently passes on its own failure is not a checker.
#              Exit codes: 0 complete, 1 incomplete, 2 cannot check.
#   stop-check the stop-time backstop (agentStop / Stop hook; kit FEATURE_PLAN
#              52). FAILS OPEN on its own errors: a hook that errors must not
#              block real work, so errors log to .git/sdlc-close-out/log and
#              exit 0. Classifies every unpushed commit by the record grammar:
#              a DEFECTIVE record (some keys present, but one missing / empty /
#              duplicated) is an /end-slice escape and flags statelessly; a BARE
#              commit (no keys at all) flags only when the TDD guard's state
#              shows slice-loop evidence for this session, and bare-flagging is
#              log-only until its own arming bar clears (52.2). Blocking for
#              the defective class arms via .git/sdlc-close-out/deny-enabled;
#              absent, verdicts are logged as WOULD-BLOCK. Stands down
#              unconditionally when stop_hook_active is true.
#
# Invocation:  sh .github/hooks/sdlc-close-out.sh check [<ref>]     (default HEAD)
#              sh .github/hooks/sdlc-close-out.sh stop-check        (payload on stdin)
# This file takes no per-project values - the four keys are fixed by the process -
# so it is copied verbatim.

MODE=$1

cannot() { printf 'close-out record: CANNOT CHECK - %s\n' "$1"; exit 2; }

# count_record <ref> - all eight counters in ONE awk pass, into globals both
# modes read. Not style: a per-pattern grep costs a process pair per counter,
# and process forks are expensive on Windows sh - the grep-per-counter draft of
# this script cost ~1.7 s per invocation there (measured 2026-08-10, Git Bash),
# against the design intent that a close-out check be effectively free; the
# stop-time path multiplies that by up to 20 candidates. The CR strip is
# defensive: a body written through a Windows shell can carry CRLF, and a stray
# CR turns the end-anchored empty-payload match false.
count_record() {
  COUNTS=$(git log -1 --format=%B "$1" | awk '
  { sub(/\r$/, "") }
  /^RED:/      { rn++; if ($0 ~ /^RED:[[:space:]]*$/) re++ }
  /^quality:/  { qn++; if ($0 ~ /^quality:[[:space:]]*$/) qe++ }
  /^mutation:/ { mn++; if ($0 ~ /^mutation:[[:space:]]*$/) me++ }
  /^verify:/   { vn++; if ($0 ~ /^verify:[[:space:]]*$/) ve++ }
  END { printf "%d %d %d %d %d %d %d %d", rn+0, re+0, qn+0, qe+0, mn+0, me+0, vn+0, ve+0 }')
  set -- $COUNTS
  red_n=$1; red_e=$2; qua_n=$3; qua_e=$4; mut_n=$5; mut_e=$6; ver_n=$7; ver_e=$8
}

if [ "$MODE" = "stop-check" ]; then
  # ---- the stop-time backstop: FAIL-OPEN from here on - every early return is
  # exit 0, and every error path logs rather than blocks.
  IN=$(cat 2>/dev/null)
  [ -d .git ] || exit 0
  SD=.git/sdlc-close-out
  mkdir -p "$SD" 2>/dev/null
  slog() { printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$1" >> "$SD/log" 2>/dev/null; }

  # Never fight the block cap (measured at 8 on both dialects): a forced
  # continuation stands down unconditionally.
  if printf '%s' "$IN" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
    slog "stop: stop_hook_active set - standing down"
    exit 0
  fi
  command -v git >/dev/null 2>&1 || { slog "stop: ERROR git not on PATH - standing down (fail-open)"; exit 0; }

  # Session id, either dialect's casing (Claude session_id, Copilot sessionId).
  # Used only to match the TDD guard's session marker for the bare class; a
  # miss degrades to bare-notes, never to a block.
  SID=$(printf '%s' "$IN" | sed -n 's/.*"session_id"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')
  [ -n "$SID" ] || SID=$(printf '%s' "$IN" | sed -n 's/.*"sessionId"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p')

  # Candidates: unpushed commits - also the remediation boundary, since the fix
  # is amending a body, legal exactly while unpushed. No upstream (or detached
  # HEAD) narrows to HEAD only, and the narrowing is stated in the log.
  if git rev-parse --abbrev-ref '@{u}' >/dev/null 2>&1; then
    CANDS=$(git rev-list --abbrev-commit -n 20 '@{u}..HEAD' 2>/dev/null)
    SCOPE="unpushed @{u}..HEAD, cap 20"
  else
    CANDS=$(git rev-parse --verify --quiet --short 'HEAD^{commit}' 2>/dev/null)
    SCOPE="HEAD only, no upstream configured"
  fi
  if [ -z "$CANDS" ]; then
    slog "stop: clean (no candidate commits; $SCOPE)"
    exit 0
  fi

  # Slice-loop evidence for THIS session, read from the TDD guard's own
  # session-scoped state (shared by both guard dialects). Only the bare class
  # consults it; where the guard is absent or this session made no guarded
  # writes, bare commits are noted, never flagged.
  GUARD_EVID=""
  if [ -n "$SID" ] && [ "$(cat .git/sdlc-tdd/session 2>/dev/null)" = "$SID" ]; then
    if [ -f .git/sdlc-tdd/prod-write-observed ] || [ -f .git/sdlc-tdd/last-test-edit ]; then
      GUARD_EVID=yes
    fi
  fi

  # pk <key> <n> <n_empty> <singleton?> - append this key's problem, if any, to
  # probs. Text stays inside the JSON-safe alphabet (no quotes, no backslashes):
  # the block reason below is emitted by printf, not a JSON encoder.
  pk() {
    if [ "$2" -eq 0 ]; then probs="$probs missing $1,"
    elif [ "$3" -gt 0 ]; then probs="$probs empty $1,"
    elif [ -n "$4" ] && [ "$2" -gt 1 ]; then probs="$probs duplicated $1,"
    fi
  }

  defective=""; bare_flagged=""; bare_noted=0; complete=0
  for C in $CANDS; do
    count_record "$C"
    if [ "$((red_n + qua_n + mut_n + ver_n))" -eq 0 ]; then
      if [ -n "$GUARD_EVID" ]; then bare_flagged="$bare_flagged $C"
      else bare_noted=$((bare_noted + 1)); fi
      continue
    fi
    probs=""
    pk RED "$red_n" "$red_e" ""
    pk quality "$qua_n" "$qua_e" s
    pk mutation "$mut_n" "$mut_e" s
    pk verify "$ver_n" "$ver_e" s
    probs=${probs%,}
    if [ -z "$probs" ]; then complete=$((complete + 1))
    else defective="$defective $C($probs )"; fi
  done

  # Bare-flagging is LOG-ONLY by design - it never blocks in this version,
  # armed or not: a docs commit made in the same session as slice work is a
  # real false-block shape, so this class logs until proven never to flag one.
  if [ -n "$bare_flagged" ]; then
    slog "stop: WOULD-BLOCK (bare, log-only by design) - no close-out record on$bare_flagged while this session shows slice-loop evidence"
  fi

  if [ -n "$defective" ]; then
    reason="A commit body is missing part of its close-out evidence record:$defective. If the step ran, amend that commit with its real outcome; if it was skipped, amend with its stated-skip form - never invent evidence the session did not produce. Fix the body before pushing (git commit --amend while it is HEAD), then finish."
    if [ -f "$SD/deny-enabled" ]; then
      slog "stop: BLOCK - defective record on$defective"
      printf '{"decision":"block","reason":"%s"}' "$reason"
    else
      slog "stop: WOULD-BLOCK - defective record on$defective"
    fi
    exit 0
  fi

  if [ -z "$bare_flagged" ]; then
    slog "stop: clean ($complete complete, $bare_noted bare without slice-loop evidence; $SCOPE)"
  fi
  exit 0
fi

REF=${2:-HEAD}

[ "$MODE" = "check" ] || cannot "unknown mode '$MODE' (usage: sdlc-close-out.sh check [<ref>])"
command -v git >/dev/null 2>&1 || cannot "git is not on this shell's PATH"
git rev-parse --verify --quiet "$REF^{commit}" >/dev/null 2>&1 \
  || cannot "'$REF' does not resolve to a commit in this repository"

count_record "$REF"

# Remediation text, kept anti-fabrication on purpose: steer to the true record -
# including its stated-skip form - never to manufacturing evidence.
AMEND="if the step ran, amend with its real outcome; if it was skipped or had
            nothing to check, amend with its stated form. Never invent
            evidence the session did not produce."

bad=""      # space-separated problem keys, in record order
detail=""   # the per-key report block, built by plain concatenation - command
            # substitution costs a fork each, the same budget the awk note guards
nl='
'

# status <padded-label> <key> <n> <n_empty> <singleton?> - appends the detail
# line, records problems.
status() {
  label=$1; k=$2; n=$3; e=$4; single=$5
  if [ "$n" -eq 0 ]; then
    line="MISSING - $AMEND"; bad="$bad $k"
  elif [ "$e" -gt 0 ]; then
    line="EMPTY - the key is there with nothing after the colon; state the outcome
            or the stated-skip form."; bad="$bad $k"
  elif [ -n "$single" ] && [ "$n" -gt 1 ]; then
    line="DUPLICATED ($n lines) - one line is the record; merge them."; bad="$bad $k"
  elif [ -n "$single" ]; then
    line="present"
  else
    line="present ($n lines)"
  fi
  detail="$detail  $label $line$nl"
}

status 'RED:     ' RED      "$red_n" "$red_e" ""
status 'quality: ' quality  "$qua_n" "$qua_e" s
status 'mutation:' mutation "$mut_n" "$mut_e" s
status 'verify:  ' verify   "$ver_n" "$ver_e" s

if [ -z "$bad" ]; then
  printf 'close-out record: COMPLETE - RED(%s) quality mutation verify - structural presence only; this does not verify the evidence is true.\n' "$red_n"
  exit 0
fi

printf 'close-out record: INCOMPLETE - problems:%s\n' "$bad"
printf '%s' "$detail"
printf 'fix: git commit --amend on the slice commit (the branch is unpushed at this step)\n'
exit 1
