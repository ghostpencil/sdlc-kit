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
# PROJECT-OWNED after instantiation: the source glob, the lint command and the
# typecheck block hold this project's own commands, so /sdlc-update never rewrites
# this file - recipe changes reach it as changelog entries applied by hand. (Named in
# words, not as their markers: a multi-line typecheck block substituted into a
# comment leaves every line after its first as live code - the recipe's TypeScript
# block broke this file that way when it was first instantiated, 2026-10-20.)

IN=$(cat)

# SDLC state (89.4): `off` or `paused` in <git-dir>/sdlc-state -> stand down at once, before
# any work: no output, exit 0. Anything else - absent, empty, or an unknown word - checks
# as always. "cwd": "." puts .git in the working directory; a worktree pays one sed.
[ -d .git ] && f=.git/sdlc-state || f=$(sed -n 's/^gitdir:[[:space:]]*//p' .git 2>/dev/null | tr -d '\r')/sdlc-state
IFS= read -r st 2>/dev/null < "$f"
case $st in [Oo][Ff][Ff]|[Pp][Aa][Uu][Ss][Ee][Dd]) exit 0 ;; esac

# The string work below uses parameter expansion, not `printf | sed` or `tr`: every
# pipeline in a $(...) is two or three processes, and Windows sh pays tens of
# milliseconds for each, on every edit (measured 2026-10-21: ~1.5 s of a call was
# forks). Results go to TK and SL. The lint value and typecheck block must not assign
# any name this file sets for itself: TK SL _tk _sl RP RR rp g1-g3 h1-h3 k c cl.
NL='
'
# take: the first line of $_tk into TK, and $_tk loses it.
take() {
  case $_tk in
    *"$NL"*) TK=${_tk%%"$NL"*}; _tk=${_tk#*"$NL"} ;;
    *) TK=$_tk; _tk="" ;;
  esac
}
# slash: $1 with every backslash made a forward slash, into SL.
slash() {
  SL=""; _sl=$1
  while :; do
    case $_sl in
      *\\*) SL="$SL${_sl%%\\*}/"; _sl=${_sl#*\\} ;;
      *) SL="$SL$_sl"; return 0 ;;
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

_tk=$O
take; W=$TK
take; ST=$TK
FILES=$_tk

# Paths arrive in BOTH forms in one session - absolute-Windows and repo-relative
# (measured 2026-08-07) - and an absolute Windows
# path does not exist as written when this script runs under WSL bash. resolve_path
# prints an existing form of its argument or fails: slashes normalized first, then
# the drive-letter translation (D:/x -> /mnt/d/x -> /d/x) the TDD guard already
# proved. -f for files; -d via the second argument for the cwd below. The form found
# goes to RP rather than stdout, so a caller needs no $(...) to read it.
resolve_path() {
  slash "$1"; rp=$SL
  while :; do case $rp in *//*) rp=${rp%%//*}/${rp#*//} ;; *) break ;; esac; done
  rt=${2:--f}
  if [ "$rt" "$rp" ]; then RP=$rp; return 0; fi
  dl=$(printf '%s' "$rp" | sed -n 's|^\([A-Za-z]\):/.*|\1|p' | tr 'A-Z' 'a-z')
  rest=$(printf '%s' "$rp" | sed -n 's|^[A-Za-z]:/\(.*\)|\1|p')
  if [ -n "$dl" ]; then
    for cand in "/mnt/$dl/$rest" "/$dl/$rest"; do
      if [ "$rt" "$cand" ]; then RP=$cand; return 0; fi
    done
  fi
  return 1
}

# The launcher starts this script at the repository root ("cwd": "." on its entry);
# remember it before the move below, for the scope test.
ROOT=$(pwd)

# repo_rel <path> - prints the path relative to the project root, or fails for an
# absolute path outside it. A file outside the project is not this project's source -
# a session scratchpad, a temp file, another checkout - and linting it against this
# project's config fails for reasons that are not the edit's (two adopters,
# sdlc-kit#15 and #17). The root test is the TDD guard's, root forms included:
# separators normalized, compared without case because Windows hands back either
# case (on a case-sensitive host that only errs toward checking), and tried against
# `pwd`, MSYS's `pwd -W`, and the WSL mount form translated back to a drive, because
# the hook shell's path flavour and the CLI's need not agree. A relative path is
# relative to the root and stays in scope. A root matched in its exact case is
# stripped as a prefix; one matched only without case is cut by bytes on both sides,
# so a non-ASCII root cannot shift it. The relative path goes to RR.
#
# The three root forms depend only on the root, so they are built once per call,
# with their lowercase forms in one `tr`, rather than once per edited file.
wm=${SDLC_WSL_MOUNT:-/mnt}
wroot=""
case "$ROOT" in "$wm"/?/*) wroot=$(printf '%s' "${ROOT#"$wm"/}" | sed 's|^\(.\)/|\1:/|') ;; esac
slash "$ROOT"; g1=${SL%/}
slash "$(cd "$ROOT" 2>/dev/null && pwd -W 2>/dev/null)"; g2=${SL%/}
slash "$wroot"; g3=${SL%/}
_tk=$(printf '%s\n%s\n%s' "$g1" "$g2" "$g3" | tr '[:upper:]' '[:lower:]')
take; h1=$TK; take; h2=$TK; take; h3=$TK
repo_rel() {
  slash "$1"; rn=$SL; rl=$(printf '%s' "$rn" | tr '[:upper:]' '[:lower:]')
  for k in 1 2 3; do
    eval "c=\$g$k; cl=\$h$k"
    [ -n "$c" ] || continue
    case "$rl" in "$cl"/*)
      case "$rn" in
        "$c"/*) RR=${rn#"$c"/} ;;
        *) RR=$(printf '%s' "$rn" | LC_ALL=C cut -b "$(($(printf '%s' "$c" | LC_ALL=C wc -c) + 2))-") ;;
      esac
      return 0 ;;
    esac
  done
  case "$rl" in /*|?:/*) return 1 ;; ./*) RR=${rn#./} ;; *) RR=$rn ;; esac
}

# Best-effort move to the payload cwd when it exists in this shell's path flavour;
# otherwise stay where the launcher started us, which is the repository root.
resolve_path "$W" -d && cd "$RP"

if [ "$ST" != "ok" ]; then
  printf '%s' 'SDLC gate hook did NOT run on this edit: no file path found in the hook payload. The gate did not check this file - fix the hook before trusting it (discovery procedure: COPILOT.md in the kit folder or the kit home repository).' | emit
  exit 0
fi

OUT=$(while IFS= read -r f; do
  [ -n "$f" ] || continue
  case "$f" in {{SOURCE_GLOB}}) ;; *) continue ;; esac
  repo_rel "$f" || continue
  r=$RR
  if resolve_path "$f"; then f="$RP"; else
    printf 'SDLC gate hook did NOT run: the edited file was not found from the hook working directory: %s\n' "$f"
    continue
  fi
  # Each check is reported under its own name with only its own output (sdlc-kit#14).
  # The lint value runs inside a group so a compound one - lint && the format check,
  # where the gate formats - has every command's stderr captured. `tn` is the
  # typecheck block's non-blocking note: errors a project-wide check found in OTHER
  # files are context, never a failure of the file just edited. This event cannot
  # block either way, so the note differs from a failure only in what it says.
  l=$( { {{HOOK_LINT_CMD}}; } 2>&1); lrc=$?
  t=""; trc=0; tn=""
  {{HOOK_TYPECHECK_BLOCK}}
  w=""; if [ $lrc -ne 0 ]; then w="lint"; fi; if [ $trc -ne 0 ]; then w="${w:+$w and }typecheck"; fi
  if [ -n "$w" ]; then
    printf 'SDLC gate hook: %s failed on the file just edited. Fix it before continuing: %s\n' "$w" "$f"
    if [ $lrc -ne 0 ]; then printf '%s\n' "$l"; fi
    if [ $trc -ne 0 ]; then printf '%s\n' "$t"; fi
  elif [ -n "$tn" ]; then
    printf 'SDLC gate hook: %s passed. Not blocking: %s\n' "$r" "$tn"
  fi
done <<FILELIST
$FILES
FILELIST
)

if [ -n "$OUT" ]; then printf '%s' "$OUT" | emit; fi
exit 0
