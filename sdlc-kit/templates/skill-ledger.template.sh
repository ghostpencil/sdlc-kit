#!/bin/sh
# SDLC skill-activation ledger - the hook BODY for BOTH CLIs since 0.31.1, installed as
# .github/hooks/sdlc-skill-ledger.sh. Claude Code runs it from the "Skill"-matcher
# PostToolUse block's bare launcher (`sh .github/hooks/sdlc-skill-ledger.sh` - split
# for the same measured reason as the gate hook: the per-hook "shell" pin was measured
# never firing on Claude Code 2.1.231, 2026-08-15); Copilot CLI runs it from
# .github/hooks/sdlc-skill-ledger.json, whose inline body it replaced (0.31.1:
# an inline body cannot follow a linked worktree's .git file without a $ the WSL
# launcher route eats). No placeholders - installed as-is when the ledger offer is
# accepted; setup removes the wiring AND does not install this file on a decline (the
# record of the decline lives in spec/SDLC.md, never here). Appends one line per
# tool-dispatched skill activation to <git dir>/sdlc-skill-ledger.jsonl.
#
# Its failure branch exits 2 with stderr: on Claude Code that reaches the agent; on
# Copilot CLI a non-zero PostToolUse exit reaches only the session's own log
# (~/.copilot/session-state/<id>/events.jsonl - measured 2026-09-27), which is as loud
# as that dialect lets a PostToolUse hook be.
i=$(cat)
# Claude Code names the root; Copilot CLI starts the hook in it ("cwd": "." in the
# config, resolved against the repository root on every build measured).
if [ -n "$CLAUDE_PROJECT_DIR" ]; then R=$CLAUDE_PROJECT_DIR; else R=$(pwd); fi

# The git directory: .git is a directory in an ordinary checkout and a one-line
# "gitdir: <path>" FILE in a linked worktree, written in the creating git's path
# flavour - read here, not by git, with the drive-letter translation the gate hook
# uses (the TDD guard and the close-out checker carry the same function).
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

if ! GD=$(sdlc_git_dir "$R"); then
  echo "SDLC skill ledger did NOT record this activation: $R is not a repository root with a resolvable git directory." >&2
  exit 2
fi
printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$i" >> "$GD/sdlc-skill-ledger.jsonl"
