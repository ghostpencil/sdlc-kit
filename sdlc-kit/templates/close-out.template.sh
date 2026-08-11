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
# FAILS CLOSED on its own errors - deliberately opposite to the hook fail-open
# rule. A hook that errors must not block real work; a command step that errors is
# seen and quoted by the session, and a checker that silently passes on its own
# failure is not a checker. Exit codes: 0 complete, 1 incomplete, 2 cannot check.
#
# Invocation:  sh .github/hooks/sdlc-close-out.sh check [<ref>]     (default HEAD)
# The mode argument exists so a later stop-time hook can share this file's parse
# logic under another mode instead of forking it. This file takes no per-project
# values - the four keys are fixed by the process - so it is copied verbatim.

MODE=$1
REF=${2:-HEAD}

cannot() { printf 'close-out record: CANNOT CHECK - %s\n' "$1"; exit 2; }

[ "$MODE" = "check" ] || cannot "unknown mode '$MODE' (usage: sdlc-close-out.sh check [<ref>])"
command -v git >/dev/null 2>&1 || cannot "git is not on this shell's PATH"
git rev-parse --verify --quiet "$REF^{commit}" >/dev/null 2>&1 \
  || cannot "'$REF' does not resolve to a commit in this repository"

# All eight counters in ONE awk pass. Not style: a per-pattern grep costs a
# process pair per counter, and on a Windows sh that is ~1.7 s of fork overhead
# per invocation - measured against this script's own sub-second budget. The CR
# strip is defensive: a body written through a Windows shell can carry CRLF, and
# a stray CR turns the end-anchored empty-payload match false.
COUNTS=$(git log -1 --format=%B "$REF" | awk '
  { sub(/\r$/, "") }
  /^RED:/      { rn++; if ($0 ~ /^RED:[[:space:]]*$/) re++ }
  /^quality:/  { qn++; if ($0 ~ /^quality:[[:space:]]*$/) qe++ }
  /^mutation:/ { mn++; if ($0 ~ /^mutation:[[:space:]]*$/) me++ }
  /^verify:/   { vn++; if ($0 ~ /^verify:[[:space:]]*$/) ve++ }
  END { printf "%d %d %d %d %d %d %d %d", rn+0, re+0, qn+0, qe+0, mn+0, me+0, vn+0, ve+0 }')
set -- $COUNTS
red_n=$1; red_e=$2; qua_n=$3; qua_e=$4; mut_n=$5; mut_e=$6; ver_n=$7; ver_e=$8

# Remediation text, kept anti-fabrication on purpose: steer to the true record -
# including its stated-skip form - never to manufacturing evidence.
AMEND="if the step ran, amend with its real outcome; if it was skipped or had
            nothing to check, amend with its stated-skip form. Never invent
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
