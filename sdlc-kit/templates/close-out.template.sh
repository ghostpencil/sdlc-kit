#!/bin/sh
# SDLC close-out evidence checker.
#
# Verifies that a slice commit's body carries the close-out evidence record the
# process mandates - the RED: / quality: / lenses: / mutation: / verify: lines, each
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
#   quality:  exactly one line, non-empty. Two lines fail: nobody knows which is
#   lenses:   the record. Zero lines or an empty payload fail: that is exactly the
#   mutation: silent absence this script exists to catch. lenses: carries the
#   verify:   review's lens verdicts or the zero-form "no lens triggered" - a lens
#             that ran clean has no other durable home, and a clock that deletes a
#             lens for finding nothing needs that denominator.
#
# THREE MODES, AND THEIR FAIL DIRECTIONS DIFFER - deliberately, each for the
# same reason pointed at its own seat:
#   check      the /end-slice command step. FAILS CLOSED on its own errors: a
#              command step's failure is seen and quoted by the session, and a
#              checker that silently passes on its own failure is not a checker.
#              Exit codes: 0 complete, 1 incomplete, 2 cannot check.
#   stop-check the stop-time backstop (agentStop on Copilot, Stop on Claude
#              Code). FAILS OPEN on its own errors: a hook that errors must not
#              block real work, so errors log to .git/sdlc-close-out/log and
#              exit 0. Classifies every unpushed commit by the record grammar,
#              after dropping the ones that cannot carry a record at all - a
#              commit touching only spec/ and the root kit documents is
#              bookkeeping, not a slice, and was 100% of this mode's measured
#              firing history before 0.29.0. Of what remains:
#              a DEFECTIVE record (some keys present, but one missing / empty /
#              duplicated) is an /end-slice escape and flags statelessly; a BARE
#              commit (no keys at all) flags only when the TDD guard's state
#              shows slice-loop evidence for this session, and bare-flagging is
#              log-only by design on every install. A flag is logged once per
#              commit per session, and an empty or wholly-filtered window logs
#              n/a rather than clean: nothing inspected is not nothing found. Blocking for
#              the defective class arms via .git/sdlc-close-out/deny-enabled;
#              absent, verdicts are logged as WOULD-BLOCK. Stands down
#              unconditionally when stop_hook_active is true.
#   docs-check the /end-slice bookkeeping step. LOG-ONLY, always exit 0: it
#              counts lines added to spec/PROJECT_INDEX.md by a close-out docs
#              commit and reports them against a budget. It observes a rule
#              whose payload legitimately varies, so it reports a number and
#              never a verdict - the bare class's seat, not the check mode's.
#
# Invocation:  sh .github/hooks/sdlc-close-out.sh check [<ref>]      (default HEAD)
#              sh .github/hooks/sdlc-close-out.sh docs-check [<ref>] (default HEAD)
#              sh .github/hooks/sdlc-close-out.sh stop-check         (payload on stdin)
# This file takes no per-project values - the five keys are fixed by the process,
# the index path is canonical, and the budget is a constant below - so it is
# copied verbatim.

MODE=$1

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

# count_record <ref> - all eleven counters in ONE awk pass, into globals both
# modes read: the ten record counters, plus whether every path the commit changed
# is a process document this kit installs (anything under spec/, or the two root
# documents setup writes). That last one is stop-check's candidate filter, and it
# rides along here rather than in a helper of its own for the reason the next
# paragraph gives - a second `git show` per candidate measured 7.7 s against 4.1 s
# over a 20-candidate walk (Windows, 2026-08-27), inside a 30 s hook timeout. The
# marker line separating body from paths is chosen not to occur in prose; a body
# containing it would fail SAFE, since its remaining lines then read as non-kit
# paths and the commit stays a candidate. Not style: a per-pattern grep costs a process pair per counter,
# and process forks are expensive on Windows sh - the grep-per-counter draft of
# this script cost ~1.7 s per invocation there (measured 2026-08-10, Git Bash),
# against the design intent that a close-out check be effectively free; the
# stop-time path multiplies that by up to 20 candidates. The CR strip is
# defensive: a body written through a Windows shell can carry CRLF, and a stray
# CR turns the end-anchored empty-payload match false.
count_record() {
  COUNTS=$(git show --name-only --format='%B%n<<<SDLC-PATHS>>>' "$1" 2>/dev/null | awk '
  { sub(/\r$/, "") }
  /^<<<SDLC-PATHS>>>$/ { inp = 1; next }
  !inp && /^RED:/      { rn++; if ($0 ~ /^RED:[[:space:]]*$/) re++ }
  !inp && /^quality:/  { qn++; if ($0 ~ /^quality:[[:space:]]*$/) qe++ }
  !inp && /^lenses:/   { ln++; if ($0 ~ /^lenses:[[:space:]]*$/) le++ }
  !inp && /^mutation:/ { mn++; if ($0 ~ /^mutation:[[:space:]]*$/) me++ }
  !inp && /^verify:/   { vn++; if ($0 ~ /^verify:[[:space:]]*$/) ve++ }
  inp && NF > 0 { np++; if ($0 !~ /^spec\// && $0 != "CLAUDE.md" && $0 != "README.md") other = 1 }
  END { printf "%d %d %d %d %d %d %d %d %d %d %d", rn+0, re+0, qn+0, qe+0, ln+0, le+0, mn+0, me+0, vn+0, ve+0, (np > 0 && !other) ? 1 : 0 }')
  set -- $COUNTS
  red_n=$1; red_e=$2; qua_n=$3; qua_e=$4; len_n=$5; len_e=$6
  mut_n=$7; mut_e=$8; ver_n=$9; shift 9; ver_e=$1; bookkeeping=$2
}


if [ "$MODE" = "stop-check" ]; then
  # ---- the stop-time backstop: FAIL-OPEN from here on - every early return is
  # exit 0, and every error path logs rather than blocks.
  IN=$(cat 2>/dev/null)
  # Copilot CLI reads .claude/settings.json too, so a both-dialect project can
  # reach this mode twice per Copilot stop: once from its own agentStop entry
  # (native camelCase payload) and once from the Claude-dialect Stop entry, with
  # the payload translated into Claude's shape - the only payload carrying
  # hook_event_name AND timestamp without permission_mode (measured 2026-09-28,
  # Copilot 1.0.88 / Claude Code 2.1.283).
  # The translated call stands down; the native one is the check. A case match,
  # not grep: a fork costs on Windows sh, and this runs on every stop.
  case "$IN" in
    *'"permission_mode"'*) ;;
    *'"hook_event_name"'*) case "$IN" in *'"timestamp"'*) exit 0 ;; esac ;;
  esac
  [ -e .git ] || exit 0
  if [ -z "$GD" ]; then
    # A .git that names no git directory: nothing can be checked, and a backstop
    # that stands down here in silence is the defect 0.31.1 fixed in
    # the launchers - so say so at the one seat measured to reach anyone.
    if ! printf '%s' "$IN" | grep -q '"stop_hook_active"[[:space:]]*:[[:space:]]*true'; then
      printf '{"decision":"block","reason":"SDLC close-out backstop did not run: .git in %s names no git directory, so no commit in this session was checked for its close-out record. Tell the owner."}\n' "$(pwd)"
    fi
    exit 0
  fi
  SD="$GD/sdlc-close-out"
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
  # An empty window is NOT a clean inspection, and until 0.29.0 both printed the
  # word "clean" - 96 of one adoption's 125 stops were the empty kind, which is
  # how a control with zero reach and a control with nothing to report became
  # indistinguishable in its own log. The two verdicts now read differently, so
  # the log can be read for how often this check had anything to inspect at all.
  if [ -z "$CANDS" ]; then
    slog "stop: n/a (nothing to inspect: no candidate commits; $SCOPE)"
    exit 0
  fi

  # Slice-loop evidence for THIS session, read from the TDD guard's own
  # session-scoped state (shared by both guard dialects). Only the bare class
  # consults it; where the guard is absent or this session made no guarded
  # writes, bare commits are noted, never flagged.
  GUARD_EVID=""
  if [ -n "$SID" ] && [ "$(cat "$GD/sdlc-tdd/session" 2>/dev/null)" = "$SID" ]; then
    if [ -f "$GD/sdlc-tdd/prod-write-observed" ] || [ -f "$GD/sdlc-tdd/last-test-edit" ]; then
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

  # already_logged / mark_logged - one commit, one line, per session. A session
  # that stops 15 times with the same unrecorded commit logged it 15 times
  # before 0.29.0, inflating the event count ~10:1 for anyone reading the log to
  # count firings. De-dup governs LOGGING ONLY: the block path below always logs
  # and always blocks, because a still-defective commit must not be let through
  # merely because an earlier stop mentioned it.
  SEEN="$SD/seen"
  already_logged() {
    [ -n "$SID" ] || return 1
    [ -f "$SEEN" ] || return 1
    grep -qF "$SID $1" "$SEEN" 2>/dev/null
  }
  mark_logged() {
    [ -n "$SID" ] || return 0
    printf '%s %s\n' "$SID" "$1" >> "$SEEN" 2>/dev/null || true
  }
  # split <list> into new (not yet logged this session) and repeat, marking the
  # new ones. Sets NEW and REPEAT.
  split_logged() {
    NEW=""; REPEAT=""
    for _sl in $1; do
      if already_logged "$_sl"; then REPEAT="$REPEAT $_sl"
      else NEW="$NEW $_sl"; mark_logged "$_sl"; fi
    done
  }

  # ONE pass: classify each candidate and drop the bookkeeping ones as they are
  # met, so a commit costs a single git process whether it is filtered or not.
  # A commit whose changed paths are all kit process documents can never carry a
  # close-out record, because it is not a slice; classifying it produces a false
  # candidate and nothing else. Deliberately one-sided: one non-kit path, or no
  # paths at all (a merge, an empty commit), and it stays a candidate. The filter
  # removes certainties; it never guesses.
  defective=""; defective_shas=""; bare_flagged=""; bare_noted=0; complete=0
  skipped=0; inspected=0
  for C in $CANDS; do
    count_record "$C"
    if [ "$bookkeeping" = "1" ]; then skipped=$((skipped + 1)); continue; fi
    inspected=$((inspected + 1))
    if [ "$((red_n + qua_n + len_n + mut_n + ver_n))" -eq 0 ]; then
      if [ -n "$GUARD_EVID" ]; then bare_flagged="$bare_flagged $C"
      else bare_noted=$((bare_noted + 1)); fi
      continue
    fi
    probs=""
    pk RED "$red_n" "$red_e" ""
    pk quality "$qua_n" "$qua_e" s
    pk lenses "$len_n" "$len_e" s
    pk mutation "$mut_n" "$mut_e" s
    pk verify "$ver_n" "$ver_e" s
    probs=${probs%,}
    if [ -z "$probs" ]; then complete=$((complete + 1))
    else defective="$defective $C($probs )"; defective_shas="$defective_shas $C"; fi
  done

  # Bare-flagging is LOG-ONLY by design - it never blocks in this version,
  # armed or not: a docs commit made in the same session as slice work is a
  # real false-block shape, so this class logs until proven never to flag one.
  # Every candidate filtered out is the same verdict as an empty window, and for
  # the same reason: nothing was inspected, so nothing was found.
  if [ "$inspected" -eq 0 ]; then
    slog "stop: n/a (nothing to inspect: $skipped bookkeeping skipped; $SCOPE)"
    exit 0
  fi

  if [ -n "$bare_flagged" ]; then
    split_logged "$bare_flagged"
    if [ -n "$NEW" ]; then
      slog "stop: WOULD-BLOCK (bare, log-only by design) - no close-out record on$NEW while this session shows slice-loop evidence"
    else
      slog "stop: repeat (bare flag already logged this session on$REPEAT; $SCOPE)"
    fi
  fi

  if [ -n "$defective" ]; then
    reason="A commit body is missing part of its close-out evidence record:$defective. If the step ran, amend that commit with its real outcome; if it was skipped, amend with its stated-skip form - never invent evidence the session did not produce. Fix the body before pushing (git commit --amend while it is HEAD), then finish."
    if [ -f "$SD/deny-enabled" ]; then
      slog "stop: BLOCK - defective record on$defective"
      printf '{"decision":"block","reason":"%s"}' "$reason"
    else
      # Unarmed, this line is a log event and nothing else, so it de-dups per
      # commit. Armed, the branch above logs and blocks every time - a
      # still-defective commit must never be let through because an earlier stop
      # happened to mention it.
      split_logged "$defective_shas"
      if [ -n "$NEW" ]; then
        slog "stop: WOULD-BLOCK - defective record on$defective"
      else
        slog "stop: repeat (defective flag already logged this session on$REPEAT; $SCOPE)"
      fi
    fi
    exit 0
  fi

  if [ -z "$bare_flagged" ]; then
    slog "stop: clean (inspected $inspected, $skipped bookkeeping skipped; $complete complete, $bare_noted bare without slice-loop evidence; $SCOPE)"
  fi
  exit 0
fi

if [ "$MODE" = "docs-check" ]; then
  # ---- the docs-commit observer: LOG-ONLY on every install, fail-open on its
  # own errors. It joins the bare class above rather than the check mode below,
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

[ "$MODE" = "check" ] || cannot "unknown mode '$MODE' (usage: sdlc-close-out.sh check|docs-check [<ref>] | stop-check)"
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
status 'lenses:  ' lenses   "$len_n" "$len_e" s
status 'mutation:' mutation "$mut_n" "$mut_e" s
status 'verify:  ' verify   "$ver_n" "$ver_e" s

if [ -z "$bad" ]; then
  printf 'close-out record: COMPLETE - RED(%s) quality lenses mutation verify - structural presence only; this does not verify the evidence is true.\n' "$red_n"
  exit 0
fi

printf 'close-out record: INCOMPLETE - problems:%s\n' "$bad"
printf '%s' "$detail"
printf 'fix: git commit --amend on the slice commit (the branch is unpushed at this step)\n'
exit 1
