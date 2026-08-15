#!/bin/sh
# SDLC edit-time gate hook, Claude Code dialect - the hook BODY. The block in
# .claude/settings.json is a bare launcher (`sh .github/hooks/sdlc-gate-claude.sh`)
# and all logic lives here, never crossing the launcher boundary - the same split
# the Copilot dialect got in 0.18.0 (copilot-hook.template.sh), applied to this
# dialect in 0.24.0 after a field measurement: on Claude Code 2.1.231 a hook
# carrying the per-hook "shell": "bash" pin never fired (Stop and PostToolUse,
# bench-probed 2026-08-15), so the pinned inline body this file replaces could be
# silently inert with no error, no log, and no feedback. A bare `sh <file>` line
# runs identically under the default hook shell and any POSIX one.
#
# Reads the hook payload on stdin; exits 2 with the failure framed (hook named,
# file named, expectation stated) so the model can act, and is LOUD for every
# case it cannot check - no parser, no path, missing file, unusable
# CLAUDE_PROJECT_DIR - because a silently green gate is indistinguishable from a
# clean edit (the 0.16.0 lesson). Proof: tools/gate-hook-check.py in the kit
# repo drives this template under both parsers, every silent case run dirty.
i=$(cat); JP=""; JN=""; for c in python python3; do if command -v "$c" >/dev/null 2>&1; then JP=$c; break; fi; done; if [ -z "$JP" ] && command -v node >/dev/null 2>&1; then JN=node; fi; jr(){ if [ -n "$JP" ]; then "$JP" -c "$1" 2>/dev/null | tr -d "\r"; elif [ -n "$JN" ]; then "$JN" -e "$2" 2>/dev/null | tr -d "\r"; else return 127; fi; }; if [ -z "$JP" ] && [ -z "$JN" ]; then echo "SDLC gate hook did NOT run: no JSON parser (python or node) on the PATH of the shell Claude Code runs hooks in. The gate did not check this file." >&2; exit 2; fi; o=$(printf '%s' "$i" | jr '
import sys,json
d=json.loads(sys.stdin.buffer.read().decode("utf-8","replace"))
a=d.get("tool_input") or {}
p=a.get("file_path") or a.get("path") or a.get("filePath") or ""
sys.stdout.write(("ok\n"+p+"\n") if p else "nopath\n")
' '
const d=JSON.parse(require("fs").readFileSync(0,"utf8"));
const a=d.tool_input||{};
const p=a.file_path||a.path||a.filePath||"";
process.stdout.write(p?("ok\n"+p+"\n"):"nopath\n");
'); st=$(printf '%s' "$o" | sed -n 1p); f=$(printf '%s' "$o" | sed -n 2p); if [ "$st" != "ok" ]; then echo "SDLC gate hook did NOT run on this edit: no file path found in the hook payload. The gate did not check this file - fix the hook before trusting it." >&2; exit 2; fi; case "$f" in {{SOURCE_GLOB}}) ;; *) exit 0 ;; esac; if [ -n "$CLAUDE_PROJECT_DIR" ]; then cd "$CLAUDE_PROJECT_DIR" || { echo "SDLC gate hook did NOT run: could not enter CLAUDE_PROJECT_DIR ($CLAUDE_PROJECT_DIR)." >&2; exit 2; }; fi; if [ ! -f "$f" ]; then echo "SDLC gate hook did NOT run: the edited file was not found from the project directory: $f" >&2; exit 2; fi; l=$({{HOOK_LINT_CMD}} 2>&1); lrc=$?; t=""; trc=0; {{HOOK_TYPECHECK_BLOCK}} if [ $lrc -ne 0 ] || [ $trc -ne 0 ]; then { echo "SDLC gate hook: lint/typecheck failed on the file just edited. Fix it before continuing: $f"; echo "$l"; if [ -n "$t" ]; then echo "$t"; fi; } >&2; exit 2; fi
