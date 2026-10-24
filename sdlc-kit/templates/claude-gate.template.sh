#!/bin/sh
# SDLC edit-time gate hook, Claude Code dialect - the hook BODY. The block in
# .claude/settings.json is a bare launcher (`sh .github/hooks/sdlc-gate-claude.sh`)
# and all logic lives here, never crossing the launcher boundary - the same split
# the Copilot dialect got in 0.18.0 (copilot-hook.template.sh), applied to this
# dialect in 0.24.0 after a field measurement: a hook carrying the per-hook
# "shell": "bash" pin never fired (Stop and PostToolUse, bench-probed 2026-08-15
# on both routes - 2.1.231 headless, 2.1.233 interactive), so the pinned inline
# body this file replaces could be
# silently inert with no error, no log, and no feedback. A bare `sh <file>` line
# runs identically under the default hook shell and any POSIX one.
#
# Reads the hook payload on stdin; exits 2 with the failure framed (hook named,
# file named, expectation stated) so the model can act, and is LOUD for every
# case it cannot check - no parser, no path, missing file, unusable
# CLAUDE_PROJECT_DIR - because a silently green gate is indistinguishable from a
# clean edit (the 0.16.0 lesson). This template is driven by a proof suite under
# both parsers, every silent case also run dirty; the suite lives with the kit's
# development tooling, not in the bundle - an adopter proves the instantiated
# copy per the setup step, not this file.
#
# Copilot CLI also runs this hook: it reads .claude/settings.json as repo config
# and hands over its payload translated into this dialect's shape. That payload is
# the only one carrying hook_event_name AND timestamp without permission_mode
# (measured 2026-09-28, Copilot 1.0.88 / Claude Code 2.1.283), and on it this hook
# exits 0 at once - the Copilot gate is the one gating that session. Silent by
# design: it is reached only on a payload that names its own CLI.
#
# The string work uses parameter expansion, not `printf | sed` or `tr`: every
# pipeline in a $(...) is two or three processes, and Windows sh pays tens of
# milliseconds for each, on every edit (measured 2026-10-21). Results go to TK and
# SL. The lint value and typecheck block must not assign any name this file sets for
# itself: TK SL _tk _sl c1-c3 l1-l3 k c cl.
NL='
'
take() { case $_tk in *"$NL"*) TK=${_tk%%"$NL"*}; _tk=${_tk#*"$NL"} ;; *) TK=$_tk; _tk="" ;; esac; }
slash() { SL=""; _sl=$1; while :; do case $_sl in *\\*) SL="$SL${_sl%%\\*}/"; _sl=${_sl#*\\} ;; *) SL="$SL$_sl"; return 0 ;; esac; done; }
i=$(cat)
# SDLC state (89.4): `off` or `paused` in <git-dir>/sdlc-state -> stand down at once, before
# the parser is spawned (where the per-edit cost lives): no output, exit 0. Anything else -
# absent, empty, or a word this hook does not know - checks as always. The launcher has
# already cd'd to the repository root, so .git is in the cwd; a worktree pays one sed.
[ -d .git ] && f=.git/sdlc-state || f=$(sed -n 's/^gitdir:[[:space:]]*//p' .git 2>/dev/null | tr -d '\r')/sdlc-state
IFS= read -r st 2>/dev/null < "$f"
case $st in [Oo][Ff][Ff]|[Pp][Aa][Uu][Ss][Ee][Dd]) exit 0 ;; esac
JP=""; JN=""; for c in python python3; do if command -v "$c" >/dev/null 2>&1; then JP=$c; break; fi; done; if [ -z "$JP" ] && command -v node >/dev/null 2>&1; then JN=node; fi; jr(){ if [ -n "$JP" ]; then "$JP" -c "$1" 2>/dev/null | tr -d "\r"; elif [ -n "$JN" ]; then "$JN" -e "$2" 2>/dev/null | tr -d "\r"; else return 127; fi; }; if [ -z "$JP" ] && [ -z "$JN" ]; then echo "SDLC gate hook did NOT run: no JSON parser (python or node) on the PATH of the shell Claude Code runs hooks in. The gate did not check this file." >&2; exit 2; fi; o=$(printf '%s' "$i" | jr '
import sys,json
d=json.loads(sys.stdin.buffer.read().decode("utf-8","replace"))
if "hook_event_name" in d and "timestamp" in d and "permission_mode" not in d: sys.stdout.write("copilot\n"); sys.exit(0)
a=d.get("tool_input") or {}
p=a.get("file_path") or a.get("path") or a.get("filePath") or ""
sys.stdout.write(("ok\n"+p+"\n") if p else "nopath\n")
' '
const d=JSON.parse(require("fs").readFileSync(0,"utf8"));
if("hook_event_name" in d&&"timestamp" in d&&!("permission_mode" in d)){process.stdout.write("copilot\n");process.exit(0);}
const a=d.tool_input||{};
const p=a.file_path||a.path||a.filePath||"";
process.stdout.write(p?("ok\n"+p+"\n"):"nopath\n");
'); _tk=$o; take; st=$TK; take; f=$TK; if [ "$st" = "copilot" ]; then exit 0; fi; if [ "$st" != "ok" ]; then echo "SDLC gate hook did NOT run on this edit: no file path found in the hook payload. The gate did not check this file - fix the hook before trusting it." >&2; exit 2; fi; case "$f" in {{SOURCE_GLOB}}) ;; *) exit 0 ;; esac; if [ -n "$CLAUDE_PROJECT_DIR" ]; then cd "$CLAUDE_PROJECT_DIR" || { echo "SDLC gate hook did NOT run: could not enter CLAUDE_PROJECT_DIR ($CLAUDE_PROJECT_DIR)." >&2; exit 2; }; fi
# Scope: a file outside the project is not this project's source - a session
# scratchpad, a temp file, another checkout - and linting it against this project's
# config fails for reasons that are not the edit's (two adopters, sdlc-kit#15 and #17:
# a scratch mutation driver had to satisfy the project's lint before it could be
# saved). The root test is the TDD guard's: separators normalized, compared without
# case because Windows hands back either case (on a case-sensitive host that only
# errs toward checking), tried against every form the root can take in this shell -
# `pwd`, MSYS's `pwd -W`, and CLAUDE_PROJECT_DIR as the CLI spelled it. A relative
# path is relative to the root and stays in scope. `r` is the repo-relative path,
# which a typecheck block may use to find the edited file in a project-wide report.
# A root matched in its exact case is stripped as a prefix; one matched only without
# case is cut by bytes on both sides, so a non-ASCII root cannot shift it. The file
# and the three roots are lowercased together, in one `tr`.
r=""; slash "$f"; fn=$SL
slash "$PWD"; c1=${SL%/}; slash "$(pwd -W 2>/dev/null)"; c2=${SL%/}; slash "$CLAUDE_PROJECT_DIR"; c3=${SL%/}
_tk=$(printf '%s\n%s\n%s\n%s' "$fn" "$c1" "$c2" "$c3" | tr '[:upper:]' '[:lower:]'); take; fl=$TK; take; l1=$TK; take; l2=$TK; take; l3=$TK
for k in 1 2 3; do
  eval "c=\$c$k; cl=\$l$k"; [ -n "$c" ] || continue
  case "$fl" in "$cl"/*)
    case "$fn" in "$c"/*) r=${fn#"$c"/} ;; *) r=$(printf '%s' "$fn" | LC_ALL=C cut -b "$(($(printf '%s' "$c" | LC_ALL=C wc -c) + 2))-") ;; esac
    break ;;
  esac
done
if [ -z "$r" ]; then case "$fl" in /*|?:/*) exit 0 ;; ./*) r=${fn#./} ;; *) r=$fn ;; esac; fi
if [ ! -f "$f" ]; then echo "SDLC gate hook did NOT run: the edited file was not found from the project directory: $f" >&2; exit 2; fi
# Each check is reported under its own name with only its own output: a lint failure
# printed under "lint/typecheck failed" beside a clean typecheck's text sent the
# reader to the wrong tool (sdlc-kit#14). The lint value runs inside a group so a
# compound one - lint && the format check, where the gate formats - has every
# command's stderr captured, not only the last one's. `tn` is the typecheck block's
# non-blocking note: errors a project-wide check found in OTHER files are context,
# never a failure of the file just edited (sdlc-kit#14: 20 blocks in ~35 edits, none a
# defect, 8 naming the wrong file). It goes back at exit 0 as additionalContext.
l=$( { {{HOOK_LINT_CMD}}; } 2>&1); lrc=$?; t=""; trc=0; tn=""
{{HOOK_TYPECHECK_BLOCK}}
w=""; if [ $lrc -ne 0 ]; then w="lint"; fi; if [ $trc -ne 0 ]; then w="${w:+$w and }typecheck"; fi
if [ -n "$w" ]; then { echo "SDLC gate hook: $w failed on the file just edited. Fix it before continuing: $f"; if [ $lrc -ne 0 ]; then echo "$l"; fi; if [ $trc -ne 0 ]; then echo "$t"; fi; } >&2; exit 2; fi
if [ -n "$tn" ]; then printf 'SDLC gate hook: %s passed. Not blocking: %s' "$r" "$tn" | jr 'import sys,json
t=sys.stdin.buffer.read().decode("utf-8","replace")
m="...[truncated by the gate hook at 8000 chars]"
if len(t)>8000: t=t[:8000-len(m)]+m
sys.stdout.write(json.dumps({"hookSpecificOutput":{"hookEventName":"PostToolUse","additionalContext":t}}))' 'const fs=require("fs");let t=fs.readFileSync(0,"utf8");const m="...[truncated by the gate hook at 8000 chars]";if(t.length>8000)t=t.slice(0,8000-m.length)+m;process.stdout.write(JSON.stringify({hookSpecificOutput:{hookEventName:"PostToolUse",additionalContext:t}}));'; fi
exit 0
