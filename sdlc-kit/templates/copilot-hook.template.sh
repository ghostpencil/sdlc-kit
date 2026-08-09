#!/bin/sh
# SDLC edit-time gate hook (Copilot CLI dialect) - the script half.
#
# Runs the project's lint/typecheck on every source file an edit touches, and reports
# through postToolUse additionalContext. It CANNOT block (that event has no deny), and
# it reports loudly whenever it could not do its job - a hook that quietly exits 0
# because it could not find its file is indistinguishable from a clean edit.
#
# WHY THE LOGIC LIVES IN THIS FILE AND NOT IN sdlc-gate.json: the hook config's
# command line crosses the CLI-to-shell boundary, and when the hook shell is the WSL
# launcher that boundary re-parses the line - corrupting backslashes and returning
# empty for $(cat) (measured 2026-08-07; the observed symptom was a FALSE "no JSON
# parser" report on every edit). A script file is read from disk by the executing
# shell and never crosses that boundary, so everything here may use backslashes,
# quoting, and command substitution freely. The JSON keeps only a bare launcher line;
# it is the launcher's job to run this script from the repository root.
#
# JSON PARSER: needs python OR node - whichever is on the PATH of the shell the agent
# CLI runs hooks in, which is NOT necessarily the shell you type in. Detected at run
# time; with neither present the hook says so on every edit rather than passing
# quietly. What that shell offered at setup is recorded in spec/SDLC.md.
#
# PROJECT-OWNED after instantiation: {{SOURCE_GLOB}}, {{HOOK_LINT_CMD}} and
# {{HOOK_TYPECHECK_BLOCK}} hold this project's own commands, so /sdlc-update never
# rewrites this file - recipe changes reach it as changelog entries applied by hand.

IN=$(cat)

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

# emit - wrap stdin as {"additionalContext": ...}, capped at 8000 characters (the
# documented cap is 10 KB across all returning hooks), decoded with errors=replace
# because a Windows locale codec mangles non-ASCII lint output on the way through.
# When the cap bites, the capped text ends with a marker that says so - lint output
# cut mid-error with no marker reads as complete, which is the silent-failure shape
# this hook exists to refuse.
emit() {
  jr 'import sys,json
t=sys.stdin.buffer.read().decode("utf-8","replace")
m="...[truncated by the gate hook at 8000 chars]"
if len(t)>8000: t=t[:8000-len(m)]+m
sys.stdout.write(json.dumps({"additionalContext":t}))' 'const fs=require("fs");let t=fs.readFileSync(0,"utf8");const m="...[truncated by the gate hook at 8000 chars]";if(t.length>8000)t=t.slice(0,8000-m.length)+m;process.stdout.write(JSON.stringify({additionalContext:t}));'
}

if [ -z "$JP" ] && [ -z "$JN" ]; then
  printf '%s' 'SDLC gate hook did NOT run: no JSON parser (python or node) on the PATH of the shell this CLI runs hooks in. The gate did not check this file.' | sed 's/.*/{"additionalContext":"&"}/'
  exit 0
fi

# Parse the payload: line 1 = cwd, line 2 = ok|nopath, lines 3+ = touched files.
# toolArgs arrives as a JSON-encoded STRING for most tools but as raw patch text for
# apply_patch - the only write tool that actually fires on the measured CLI - so
# anything that does not start like JSON is parsed as patch headers. Delete entries
# are skipped: there is nothing to lint. The VS Code payload shape (tool_input, an
# object) is accepted too, because both are documented and which arrives is not.
O=$(printf '%s' "$IN" | jr '
import sys,json,re
d=json.loads(sys.stdin.buffer.read().decode("utf-8","replace"))
o=[d.get("cwd") or ""]
a=d.get("toolArgs") or d.get("tool_input") or {}
if isinstance(a,str) and a.lstrip()[:1] not in "{[":
    h=re.findall(r"^\*\*\* (Add|Update|Delete) File: (.+)$",a,re.M)
    o.append("ok" if h else "nopath")
    o+=[v.strip() for k,v in h if k!="Delete"]
else:
    a=json.loads(a) if isinstance(a,str) else a
    p=a.get("path") or a.get("file_path") or a.get("filePath") or a.get("filename") or a.get("file") or ""
    o.append("ok" if p else "nopath")
    if p: o.append(p)
sys.stdout.write("\n".join(o)+"\n")
' '
const d=JSON.parse(require("fs").readFileSync(0,"utf8"));
const o=[d.cwd||""];
let a=d.toolArgs||d.tool_input||{};
if(typeof a==="string" && !"{[".includes(a.trimStart()[0]||"")){
  const h=[...a.matchAll(/^\*\*\* (Add|Update|Delete) File: (.+)$/gm)];
  o.push(h.length?"ok":"nopath");
  for(const m of h) if(m[1]!=="Delete") o.push(m[2].trim());
}else{
  if(typeof a==="string") a=JSON.parse(a);
  const p=a.path||a.file_path||a.filePath||a.filename||a.file||"";
  o.push(p?"ok":"nopath");
  if(p) o.push(p);
}
process.stdout.write(o.join("\n")+"\n");
')

W=$(printf '%s' "$O" | sed -n 1p)
ST=$(printf '%s' "$O" | sed -n 2p)

# Paths arrive in BOTH forms in one session - absolute-Windows and repo-relative
# (measured 2026-08-07) - and an absolute Windows
# path does not exist as written when this script runs under WSL bash. resolve_path
# prints an existing form of its argument or fails: slashes normalized first, then
# the drive-letter translation (D:/x -> /mnt/d/x -> /d/x) the TDD guard already
# proved. -f for files; -d via the second argument for the cwd below.
resolve_path() {
  rp=$(printf '%s' "$1" | tr '\\' '/' | tr -s '/')
  rt=${2:--f}
  if [ "$rt" "$rp" ]; then printf '%s' "$rp"; return 0; fi
  dl=$(printf '%s' "$rp" | sed -n 's|^\([A-Za-z]\):/.*|\1|p' | tr 'A-Z' 'a-z')
  rest=$(printf '%s' "$rp" | sed -n 's|^[A-Za-z]:/\(.*\)|\1|p')
  if [ -n "$dl" ]; then
    for cand in "/mnt/$dl/$rest" "/$dl/$rest"; do
      if [ "$rt" "$cand" ]; then printf '%s' "$cand"; return 0; fi
    done
  fi
  return 1
}

# Best-effort move to the payload cwd when it exists in this shell's path flavour;
# otherwise stay where the launcher started us, which is the repository root.
WD=$(resolve_path "$W" -d) && cd "$WD"

if [ "$ST" != "ok" ]; then
  printf '%s' 'SDLC gate hook did NOT run on this edit: no file path found in the hook payload. The gate did not check this file - fix the hook before trusting it (discovery procedure: COPILOT.md in the kit folder or the kit home repository).' | emit
  exit 0
fi

OUT=$(printf '%s\n' "$O" | tail -n +3 | while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$f" in {{SOURCE_GLOB}}) ;; *) continue ;; esac
  if rf=$(resolve_path "$f"); then f="$rf"; else
    printf 'SDLC gate hook did NOT run: the edited file was not found from the hook working directory: %s\n' "$f"
    continue
  fi
  l=$({{HOOK_LINT_CMD}} 2>&1); lrc=$?
  t=""; trc=0
  {{HOOK_TYPECHECK_BLOCK}}
  if [ $lrc -ne 0 ] || [ $trc -ne 0 ]; then
    printf 'SDLC gate hook: lint/typecheck failed on the file just edited. Fix it before continuing: %s\n%s\n%s\n' "$f" "$l" "$t"
  fi
done)

if [ -n "$OUT" ]; then printf '%s' "$OUT" | emit; fi
exit 0
