#!/bin/sh
# SDLC close-out evidence checker.
#
# Verifies that a slice commit's body carries the close-out evidence record the
# process mandates - the RED: / lenses: / mutation: / verify: lines, each
# present or carrying its stated-skip form - and fails LOUDLY on silent absence.
# /end-slice
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
#   lenses:   exactly one line, non-empty. Two lines fail: nobody knows which is
#   mutation: the record. Zero lines or an empty payload fail: that is exactly the
#   verify:   silent absence this script exists to catch. lenses: carries the
#             review's lens verdicts or the zero-form "no lens triggered" - a lens
#             that ran clean has no other durable home, and a clock that deletes a
#             lens for finding nothing needs that denominator.
#   A quality: line (the record of the change-simplify pass, retired in 0.38.0) is
#   ignored: older commits carry one and still read COMPLETE.
#
# TWO MODES, AND THEIR FAIL DIRECTIONS DIFFER - deliberately, each for the
# same reason pointed at its own seat:
#   check      the /end-slice command step. FAILS CLOSED on its own errors: a
#              command step's failure is seen and quoted by the session, and a
#              checker that silently passes on its own failure is not a checker.
#              Exit codes: 0 complete, 1 incomplete, 2 cannot check.
#   docs-check the /end-slice bookkeeping step. LOG-ONLY, always exit 0: it
#              counts lines added to spec/PROJECT_INDEX.md by a close-out docs
#              commit and reports them against a budget. It observes a rule
#              whose payload legitimately varies, so it reports a number and
#              never a verdict.
#
# Invocation:  sh .github/hooks/sdlc-close-out.sh check [<ref>]      (default HEAD)
#              sh .github/hooks/sdlc-close-out.sh docs-check [<ref>] (default HEAD)
# This file takes no per-project values - the four keys are fixed by the process,
# the index path is canonical, and the budget is a constant below - so it is
# copied verbatim.

MODE=$1

# stop-check was the stop-time backstop, retired in 0.38.0: across five field arcs it
# found no slice commit missing its record, and logged five false candidates. A Stop or
# agentStop launcher left behind by an older install still calls it, so the mode stays
# and does nothing, before reading anything - an unknown mode exits 2, and a Stop hook
# exiting 2 blocks every stop.
[ "$MODE" = "stop-check" ] && exit 0

cannot() { printf 'close-out record: CANNOT CHECK - %s\n' "$1"; exit 2; }

# The git directory (0.31.1) - every .git/ path this script names means
# it. .git is a directory in an ordinary checkout and a one-line "gitdir: <path>"
# FILE in a linked worktree, whose path the creating git wrote in ITS flavour: a
# worktree made by Windows git names D:/..., which does not exist as written under
# WSL bash. Read here rather than by git, with the drive-letter translation the gate
# hook uses; the TDD guard carries the same function. In an ordinary checkout it is
# ./.git, so every state path is exactly what it always was.
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
GD=""
if [ -e .git ]; then
  GD=$(sdlc_git_dir "$(pwd)") || GD=""
  # WSL's own git cannot follow a Windows-written gitdir either - "not a git
  # repository" on every call - but works when pointed at the translated one
  # (both measured 2026-09-27). Only a worktree git cannot resolve pays the spawn.
  if [ -n "$GD" ] && [ -f .git ] && ! git rev-parse --git-dir >/dev/null 2>&1; then
    GIT_DIR=$GD; GIT_WORK_TREE=$(pwd); export GIT_DIR GIT_WORK_TREE
  fi
fi

# count_record <ref> - all eight counters in ONE awk pass. Not style: a
# per-pattern grep costs a process pair per counter, and process forks are
# expensive on Windows sh - the grep-per-counter draft of this script cost ~1.7 s
# per invocation there (measured 2026-08-10, Git Bash), against the design intent
# that a close-out check be effectively free. The CR strip is defensive: a body
# written through a Windows shell can carry CRLF, and a stray CR turns the
# end-anchored empty-payload match false.
count_record() {
  COUNTS=$(git log -1 --format='%B' "$1" 2>/dev/null | awk '
  { sub(/\r$/, "") }
  /^RED:/      { rn++; if ($0 ~ /^RED:[[:space:]]*$/) re++ }
  /^lenses:/   { ln++; if ($0 ~ /^lenses:[[:space:]]*$/) le++ }
  /^mutation:/ { mn++; if ($0 ~ /^mutation:[[:space:]]*$/) me++ }
  /^verify:/   { vn++; if ($0 ~ /^verify:[[:space:]]*$/) ve++ }
  END { printf "%d %d %d %d %d %d %d %d", rn+0, re+0, ln+0, le+0, mn+0, me+0, vn+0, ve+0 }')
  set -- $COUNTS
  red_n=$1; red_e=$2; len_n=$3; len_e=$4; mut_n=$5; mut_e=$6; ver_n=$7; ver_e=$8
}

if [ "$MODE" = "docs-check" ]; then
  # ---- the docs-commit observer: LOG-ONLY on every install, fail-open on its
  # own errors. It is log-only rather than a check like the mode below,
  # because the rule it watches has a legitimately variable payload: a close-out
  # docs commit carries one status line PLUS however many backlog and friction
  # entries the slice really produced. What it catches is the other shape - a
  # slice writing its whole per-slice write-up into the index, measured at 44 to
  # 87 added lines across five closes of one real adoption, each one paid for
  # again by an archiving step at phase close. The prose rule said "one line"
  # the whole time; prose cannot count, and this is the smallest thing that can.
  # It reports a number and never a verdict: over budget is an observation for
  # the hand-back, and "more entries than usual" is a fine answer to it.
  REF=${2:-HEAD}
  BUDGET=25                # added index lines per close-out docs commit
  IDX=spec/PROJECT_INDEX.md

  if ! command -v git >/dev/null 2>&1; then
    printf 'docs budget: CANNOT CHECK - git is not on this shell PATH (log-only; nothing is blocked)
'
    exit 0
  fi
  if ! git rev-parse --verify --quiet "$REF^{commit}" >/dev/null 2>&1; then
    printf 'docs budget: CANNOT CHECK - %s does not resolve to a commit (log-only)
' "$REF"
    exit 0
  fi

  # --numstat with an emptied --format prints one "added deleted path" row per
  # changed path, and nothing at all when the commit never touched the index.
  ADDED=$(git show --numstat --format= "$REF" -- "$IDX" 2>/dev/null | awk 'NR==1 { print $1 }')

  if [ -z "$ADDED" ]; then
    MSG="docs budget: n/a - $REF does not touch $IDX"
  elif [ "$ADDED" = "-" ]; then
    MSG="docs budget: n/a - $IDX counted as binary in $REF"
  elif [ "$ADDED" -gt "$BUDGET" ]; then
    MSG="docs budget: OVER - $ADDED lines added to $IDX against a budget of $BUDGET. The close-out writes one status line plus the backlog and friction entries this slice really produced; a per-slice write-up belongs in the phase spec, and the commit message is already the better record. Log-only - nothing is blocked. State in the hand-back which shape it was."
  else
    MSG="docs budget: OK - $ADDED lines added to $IDX against a budget of $BUDGET"
  fi

  printf '%s
' "$MSG"
  if [ -n "$GD" ]; then
    mkdir -p "$GD/sdlc-close-out" 2>/dev/null
    printf '%s %s
' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$MSG" >> "$GD/sdlc-close-out/log" 2>/dev/null
  fi
  exit 0
fi

REF=${2:-HEAD}

[ "$MODE" = "check" ] || cannot "unknown mode '$MODE' (usage: sdlc-close-out.sh check|docs-check [<ref>])"
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
status 'lenses:  ' lenses   "$len_n" "$len_e" s
status 'mutation:' mutation "$mut_n" "$mut_e" s
status 'verify:  ' verify   "$ver_n" "$ver_e" s

if [ -z "$bad" ]; then
  printf 'close-out record: COMPLETE - RED(%s) lenses mutation verify - structural presence only; this does not verify the evidence is true.\n' "$red_n"
  exit 0
fi

printf 'close-out record: INCOMPLETE - problems:%s\n' "$bad"
printf '%s' "$detail"
printf 'fix: git commit --amend on the slice commit (the branch is unpushed at this step)\n'
exit 1
