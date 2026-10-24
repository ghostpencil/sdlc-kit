#!/usr/bin/env python
"""SDLC state - the one file the kit's hooks read to learn whether the process is in force.

Owns the format of `<git-dir>/sdlc-state`, its append-only log `<git-dir>/sdlc-state.log`,
and the `status` block the daily commands and /sdlc quote. spec/SDLC.md *Shape* is the
canonical statement of the states; this file only implements it.

THIS IS A COMMAND STEP, NOT A HOOK. The hooks never run it - they read the first line of
the state file themselves (`off` or `paused` -> stand down; anything else, an absent or
unreadable file included -> guard), so a defect here can never disarm a guard. Pausing
and turning off are owner acts; the commands that call this file never do either on
their own.

FAIL DIRECTION: closed. A bad verb, an unknown state word or an unwritable file prints
one error line and exits 2 - never swallowed, never a silent success. (The hooks fail
the other way, toward guarding, on a state they do not recognize.)

The state is per clone and per linked worktree, never committed: the git directory is
resolved the way the guards resolve it (a `.git` FILE names a worktree's directory).
It takes no per-project values, so it is copied verbatim; it is launched
shell-neutrally (`python <path>`) from the repository root.

Usage:
  python .github/hooks/sdlc-state.py status
  python .github/hooks/sdlc-state.py set <state> [--phase NN] [--slice Sn]
                                       [--by <name>] [--reason <text>]
  python .github/hooks/sdlc-state.py pause "<reason>"
  python .github/hooks/sdlc-state.py resume
  python .github/hooks/sdlc-state.py off [--force]
States: off phase slice close-out phase-end paused
"""

import os
import re
import sys
import time

sys.dont_write_bytecode = True
# The block is quoted by the commands, and an index line or a reason may hold a character
# the console's code page lacks: say UTF-8 rather than crash on the print.
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

WORDS = ("off", "phase", "slice", "close-out", "phase-end", "paused")
STATE_FILE = "sdlc-state"
LOG_FILE = "sdlc-state.log"
INDEX = os.path.join("spec", "PROJECT_INDEX.md")


class Fail(Exception):
    pass


def repo_root():
    r = os.environ.get("SDLC_REPO_ROOT")
    if r:
        return r
    r = os.environ.get("CLAUDE_PROJECT_DIR")
    if r and os.path.exists(os.path.join(r, ".git")):
        return r
    if os.path.exists(".git"):
        return os.getcwd()
    raise Fail("not at a repository root (no .git here); run from the project root")


def git_dir(root):
    p = os.path.join(root, ".git")
    if os.path.isdir(p):
        return p
    try:
        with open(p, encoding="utf-8") as f:
            line = f.read().strip()
    except OSError:
        raise Fail("cannot read %s" % p)
    if not line.startswith("gitdir:"):
        raise Fail("%s is neither a directory nor a gitdir pointer" % p)
    g = line[len("gitdir:"):].strip().replace("\\", "/")
    if not os.path.isabs(g):
        g = os.path.join(root, g)
    if not os.path.isdir(g):
        raise Fail("worktree git directory %s does not exist" % g)
    return g


def now():
    return time.strftime("%Y-%m-%dT%H:%MZ", time.gmtime())


def read_state(gd):
    """-> (word, keys) ; word is 'absent' for a missing or empty file."""
    try:
        with open(os.path.join(gd, STATE_FILE), encoding="utf-8") as f:
            lines = f.read().splitlines()
    except OSError:
        return "absent", {}
    if not lines or not lines[0].strip():
        return "absent", {}
    keys = {}
    for ln in lines[1:]:
        m = re.match(r"^([A-Za-z_-]+):\s*(.*)$", ln)
        if m:
            keys[m.group(1).lower()] = m.group(2).strip()
    return lines[0].strip().lower(), keys


def write_state(gd, word, keys, by, reason):
    old, _ = read_state(gd)
    since = now()
    body = [word]
    for k in ("stage", "phase", "slice"):
        if keys.get(k):
            body.append("%s: %s" % (k, keys[k]))
    body.append("since: %s" % since)
    body.append("by: %s" % by)
    if reason:
        body.append("reason: %s" % reason)
    try:
        with open(os.path.join(gd, STATE_FILE), "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(body) + "\n")
        with open(os.path.join(gd, LOG_FILE), "a", encoding="utf-8", newline="\n") as f:
            f.write("%s %s -> %s %s — %s\n" % (since, old, word, by, reason or "-"))
    except OSError as e:
        raise Fail("cannot write the state under %s: %s" % (gd, e))


def index_phase(root):
    """First bold line of the index's Phase section, or '' when there is none."""
    try:
        with open(os.path.join(root, INDEX), encoding="utf-8") as f:
            text = f.read()
    except OSError:
        return ""
    m = re.search(r"^## Phase\b.*?^\*\*(.+?)\*\*", text, re.S | re.M)
    return m.group(1).strip() if m else ""


def tdd_leg(gd):
    d = os.path.join(gd, "sdlc-tdd")

    def mt(n):
        try:
            return os.path.getmtime(os.path.join(d, n))
        except OSError:
            return None
    if mt("close-out-license") is not None:
        return "CLOSE-OUT"
    if mt("refactor-license") is not None:
        return "REFACTOR"
    red, green, edit = mt("red-observed"), mt("green-observed"), mt("last-test-edit")
    if red is not None and (edit is None or red > edit) and (green is None or red > green):
        return "RED"
    if green is not None:
        return "GREEN"
    return "none observed this session"


def parse_opts(args):
    opts, rest, i = {}, [], 0
    while i < len(args):
        a = args[i]
        if a == "--force":
            opts["force"] = True
        elif a in ("--phase", "--slice", "--by", "--reason"):
            if i + 1 >= len(args):
                raise Fail("%s needs a value" % a)
            opts[a[2:]] = args[i + 1]
            i += 1
        elif a.startswith("--"):
            raise Fail("unknown option %s" % a)
        else:
            rest.append(a)
        i += 1
    return opts, rest


def cmd_status(root, gd):
    word, keys = read_state(gd)
    out = []
    if word == "absent":
        out.append("state: absent - guards active by default")
    else:
        out.append("state: %s%s" % (word, "" if word in WORDS else " (unrecognized - hooks guard)"))
        for k in ("stage", "phase", "slice", "since", "by", "reason"):
            if keys.get(k):
                out.append("  %s: %s" % (k, keys[k]))
    out.append("tdd: %s" % tdd_leg(gd))
    out.append("deny: %s" % ("armed" if os.path.exists(
        os.path.join(gd, "sdlc-tdd", "deny-enabled")) else "logging"))
    out.append("index: %s" % (index_phase(root) or "no Phase line found"))
    print("\n".join(out))


def cmd_set(gd, args):
    opts, rest = parse_opts(args)
    if len(rest) != 1 or rest[0] not in WORDS:
        raise Fail("set needs one state word: %s" % " ".join(WORDS))
    word = rest[0]
    keys = {}
    if word == "phase" and not opts.get("phase"):
        keys["stage"] = "planning"
    if opts.get("phase"):
        keys["phase"] = opts["phase"]
    if opts.get("slice"):
        keys["slice"] = opts["slice"]
    if word in ("phase", "slice", "close-out", "phase-end") and not keys.get("phase"):
        _, old = read_state(gd)
        if old.get("phase") and word != "phase":
            keys["phase"] = old["phase"]
    write_state(gd, word, keys, opts.get("by", "hand"), opts.get("reason", ""))
    print("state: %s" % word)


def cmd_pause(gd, args):
    opts, rest = parse_opts(args)
    reason = " ".join(rest).strip() or opts.get("reason", "")
    if not reason:
        raise Fail('pause needs a reason: pause "<reason>"')
    word, keys = read_state(gd)
    if word == "off":
        raise Fail("nothing is in flight (state is off); there is nothing to pause")
    if word == "paused":
        raise Fail("already paused (stage: %s)" % keys.get("stage", "?"))
    new = {k: keys[k] for k in ("phase", "slice") if keys.get(k)}
    new["stage"] = word if word in WORDS else "phase"
    write_state(gd, "paused", new, opts.get("by", "/sdlc pause"), reason)
    print("state: paused (stage: %s)" % new["stage"])


def cmd_resume(root, gd, args):
    opts, _ = parse_opts(args)
    word, keys = read_state(gd)
    stage = keys.get("stage")
    if word == "paused" and stage in WORDS and stage != "paused":
        new = {k: keys[k] for k in ("phase", "slice") if keys.get(k)}
        write_state(gd, stage, new, opts.get("by", "/sdlc resume"), "resumed")
        print("state: %s (restored from stage:)" % stage)
        return
    if word not in ("paused", "absent"):
        print("state: %s (nothing to resume)" % word)
        return
    line = index_phase(root)
    low = line.lower()
    if "between phases" in low or "pre-phase" in low:
        pick = "off"
    elif low.startswith("build") or low.startswith("stabilization"):
        pick = "phase"
    else:
        raise Fail("no saved stage and the index Phase line is unreadable (%r); "
                   "use `set <state>`" % line)
    write_state(gd, pick, {}, opts.get("by", "/sdlc resume"),
                "resumed from the index Phase line")
    print("state: %s (no saved stage; chosen from the index: %s)" % (pick, line))


def cmd_off(gd, args):
    opts, _ = parse_opts(args)
    word, keys = read_state(gd)
    over = keys.get("stage") if word == "paused" else word
    if over not in (None, "off", "absent") and not opts.get("force"):
        raise Fail("an arc is in flight (%s, phase %s): pass --force to turn the state "
                   "off, or /sdlc pause <reason>" % (over, keys.get("phase", "?")))
    write_state(gd, "off", {}, opts.get("by", "/sdlc off"), opts.get("reason", ""))
    print("state: off")


def main(argv):
    if not argv:
        raise Fail("usage: sdlc-state.py status|set|pause|resume|off")
    verb, rest = argv[0], argv[1:]
    root = repo_root()
    gd = git_dir(root)
    if verb == "status":
        cmd_status(root, gd)
    elif verb == "set":
        cmd_set(gd, rest)
    elif verb == "pause":
        cmd_pause(gd, rest)
    elif verb == "resume":
        cmd_resume(root, gd, rest)
    elif verb == "off":
        cmd_off(gd, rest)
    else:
        raise Fail("unknown verb %r" % verb)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except Fail as e:
        print("sdlc-state: %s" % e)
        sys.exit(2)
