#!/usr/bin/env python
# SDLC TDD-ordering guards G1 + G2 (Claude Code dialect).
#
# Same state machine as the Copilot dialect (sdlc-tdd-guard.sh) - G1 observed-RED
# write guard with the refactor license, G2 premature-stop guard, session-scoped
# state in .git/sdlc-tdd/ (the git directory: in a linked worktree .git is a file
# naming it - see git_dir below) - with every signal path rebuilt from a 2026-08-12
# probe of the real hook payloads:
#
#   - Green and red arrive on DIFFERENT EVENTS, not as an exit-code trailer:
#     PostToolUse fires only when a command succeeds (its tool_response carries no
#     exit code at all), a failing command fires PostToolUseFailure instead, with
#     the exit code as a text header of its `error` field ("Exit code 1\n...").
#     The event type is the red/green signal; the header is read only to speak it.
#   - The shell tool's hook-visible name on Windows is `PowerShell`, not `Bash`
#     (the display-name trap a third time) - the hook config matches both.
#   - The DEFAULT Windows hook shell is PowerShell (Git Bash at a custom install
#     path is not found); a per-hook "shell" key exists but is undocumented. This
#     guard depends on neither: the hook config's command line is the
#     shell-neutral `python <this file> <mode>`, which runs identically under
#     PowerShell and any POSIX shell, and all logic lives here in python - the
#     same launcher-line discipline as the gate/guard split,
#     forced this time by the shell being unknowable rather than by a re-parse.
#   - Write paths arrive one per call in tool_input.file_path, absolute Windows
#     form; hooks run with the project root as cwd (measured, undocumented) and
#     $CLAUDE_PROJECT_DIR set (documented).
#
# G1 - observed-RED write guard: a production-source write is a violation unless a
#      test file has been edited this session AND a failing test run has been
#      observed since that edit. G1 carries a SECOND license for the refactor leg:
#      a production write is also allowed while .git/sdlc-tdd/refactor-license
#      exists AND a green run has been observed this session - the file is the
#      session's own declaration that the edits are behavior-preserving (refactor,
#      simplification, mutation testing - at any point in the cycle), revoked by a
#      test edit, cleared at session end, every write under it logged.
#      .git/sdlc-tdd/close-out-license is the same license scoped to /end-slice,
#      and differs in exactly one way: a test edit does NOT revoke it. Close-out's
#      own mandated order (review fixes tests -> mutation writes production and
#      restores tests -> verification writes a harness) cannot be executed under a
#      license a test edit revokes, and a real arc paid the re-declaration seven
#      times in one phase (field, 2026-09-01). Every test edit it survives is
#      COUNTED and logged, so a license held open past its step is visible in
#      review rather than silent.
# G2 - premature-stop guard: stopping is a violation while no green test run has
#      been observed, or the latest observed run is red. The green is ANY counted
#      green (division of labor: full-suite assurance is the end-slice gate's
#      job). G2 binds only a session that made a production write that went
#      through, or edited a test; planning and docs sessions stop clean.
#
# Every observe-test outcome is SPOKEN back as context, not only logged - state
# facts, never instructions (both lessons field-measured on the Copilot dialect,
# 2026-08-08/09, and inherited here).
#
# LOGGING MODE IS THE DEFAULT. The guards only deny/block when the flag file
# .git/sdlc-tdd/deny-enabled exists (shared with the Copilot dialect on purpose:
# arming one arms both). Without it they log and never block.
#
# This is a COOPERATIVE BACKSTOP, NOT A SECURITY BOUNDARY. The session can read
# and edit this script and its state; writes made through the shell tool are
# invisible to it. Never runs the test suite inline: state reads and writes only.
#
# Timeout fail direction is UNDOCUMENTED for Claude Code hooks (probe, 2026-08-12);
# the default hook timeout is 10 minutes and this script does no I/O beyond
# .git/sdlc-tdd/, so it should never approach it. Stated per invariant 15.

import json
import os
import re
import sys
import time
from fnmatch import fnmatch

MODE = sys.argv[1] if len(sys.argv) > 1 else ""

# Instantiated by setup for THIS project - same five placeholders, same values,
# as the Copilot dialect's script (reference/GATE_RECIPES.md carries the recipe).
TEST_PATH_PATTERN = "{{TEST_PATH_PATTERN}}"
SOURCE_GLOB = "{{SOURCE_GLOB}}"
TEST_CMD_PATTERN = "{{TEST_CMD_PATTERN}}"
# A regular expression found in the test runner's OWN failure report, never in a
# wrapper's: a failing exit alone is a failing command, not a failing test.
TEST_REPORT_PATTERN = r"{{TEST_REPORT_PATTERN}}"
# Repo-relative paths that are neither production source nor tests: configs and
# scripts no test can turn red (owner ruling, 0.35.0).
GUARD_EXEMPT_PATTERN = "{{GUARD_EXEMPT_PATTERN}}"
# ...and in every project, whatever setup resolved: the graph tool's own directories.
# Its agents write scratch code there; none of it is the project's.
ALWAYS_EXEMPT = ".ua/*|.understand-anything/*"

# Commands that can NAME the runner without running it, so a substring pattern
# matched them: `cat vitest.config.ts`, `grep pytest pyproject.toml`, `pip install
# pytest`. A failure counted as a RED, and - worse - a success counted as a GREEN that
# satisfied the stop guard with no test run at all (found at 0.35.0's triage). Judged on
# the leading executable, after any `env` and `NAME=value` prefix. A fixed list on
# purpose: every mistake it makes lands on the not-counted side.
NEVER_RUNS = {"cat", "type", "more", "less", "head", "tail", "sed", "awk", "grep",
              "egrep", "fgrep", "rg", "find", "ls", "dir", "echo", "printf", "wc",
              "diff", "git", "gh", "jq", "code", "which", "where", "file", "stat",
              "pip", "pip3", "pipx", "conda", "get-content", "gc", "select-string",
              "sls", "get-childitem", "gci", "test-path", "write-output",
              "write-host"}
# A package manager runs tests only through its run/test/exec subcommands.
PACKAGE_MANAGERS = {"npm", "pnpm", "yarn", "bun", "uv", "poetry"}
NOT_A_RUN_SUBCOMMANDS = {"install", "i", "add", "ci", "remove", "rm", "uninstall",
                         "un", "update", "upgrade", "up", "list", "ls", "view",
                         "info", "show", "outdated", "audit", "why", "sync", "lock"}
ANSI = re.compile(r"\x1b\[[0-9;]*[A-Za-z]")


def match_any(value, patterns):
    return any(fnmatch(value, p) for p in patterns.split("|") if p)


def never_a_test_run(probe):
    """True for a command that cannot be the test's own run, whatever its text names."""
    # A heredoc's body is data handed to a command - a commit message, a file being
    # written - and the newline-joined body would otherwise be read as the command.
    # The operator itself is never quoted, so the quote-stripped probe still has it.
    if "<<" in probe:
        return True
    words = probe.split()
    while words and (words[0].lower() == "env"
                     or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0])):
        words = words[1:]
    if not words:
        return True
    exe = words[0].replace("\\", "/").rsplit("/", 1)[-1].lower()
    for ext in (".exe", ".cmd", ".bat", ".ps1"):
        if exe.endswith(ext):
            exe = exe[:-len(ext)]
    sub = words[1].lower() if len(words) > 1 else ""
    if exe in NEVER_RUNS:
        return True
    if exe in ("python", "python3", "py") and sub == "-m" and len(words) > 2 \
            and words[2].lower() == "pip":
        return True
    return exe in PACKAGE_MANAGERS and sub in NOT_A_RUN_SUBCOMMANDS


# An explicit SDLC_REPO_ROOT wins so a harness can pin it; then the documented
# CLAUDE_PROJECT_DIR; then the measured cwd - but only if .git sits there. With no
# root, do nothing rather than write state to an unrelated directory (the same
# trust-nothing default the Copilot dialect ships).
def repo_root():
    r = os.environ.get("SDLC_REPO_ROOT")
    if r:
        return r
    r = os.environ.get("CLAUDE_PROJECT_DIR")
    if r and os.path.exists(os.path.join(r, ".git")):
        return r
    if os.path.exists(".git"):
        return os.getcwd()
    return None


# The git directory (0.31.1). .git is a directory in an ordinary
# checkout and a one-line "gitdir: <path>" FILE in a linked worktree; testing for a
# directory disarmed the guard in every worktree session. Read here rather than by
# spawning git, which costs a process per tool call. In an ordinary checkout this is
# ROOT/.git, so every state path is exactly what it always was.
def git_dir(root):
    p = os.path.join(root, ".git")
    if os.path.isdir(p):
        return p
    try:
        with open(p, encoding="utf-8") as f:
            line = f.read().strip()
    except OSError:
        return None
    if not line.startswith("gitdir:"):
        return None
    g = line[len("gitdir:"):].strip().replace("\\", "/")
    if not os.path.isabs(g):
        g = os.path.join(root, g)
    return g if os.path.isdir(g) else None


ROOT = repo_root()
if not ROOT:
    sys.exit(0)
GD = git_dir(ROOT)
# A harness-pinned SDLC_REPO_ROOT with no .git at all keeps its pre-0.31.1 meaning:
# state under ROOT/.git, created on demand (an adopter's own guard tests pin a bare
# temp directory - 0.31.1 made that guard nothing, silently, and 0.31.2 restores it).
# The other two roots cannot reach this: both require a .git to exist.
if not GD and not os.path.exists(os.path.join(ROOT, ".git")):
    GD = os.path.join(ROOT, ".git")
if not GD:
    # A .git that names no git directory: nowhere to keep state, so guard nothing -
    # but say so at stop, the one seat measured to reach anyone (measured 2026-09-27).
    if MODE == "stop-check":
        raw = sys.stdin.buffer.read().decode("utf-8", "replace")
        if not re.search(r'"stop_hook_active"\s*:\s*true', raw):
            sys.stdout.write(json.dumps({
                "decision": "block",
                "reason": "SDLC TDD guard did not run: %s/.git names no git directory, "
                          "so this session's writes were not guarded. Tell the owner."
                          % ROOT.replace("\\", "/")}, separators=(",", ":")))
    sys.exit(0)
S = os.path.join(GD, "sdlc-tdd")
# The licence directory as the deny message names it: the familiar relative form in
# an ordinary checkout, the real location in a worktree, where .git/ is a file.
LIC = (".git/sdlc-tdd" if os.path.normcase(os.path.abspath(GD)) ==
       os.path.normcase(os.path.abspath(os.path.join(ROOT, ".git")))
       else S.replace("\\", "/"))
try:
    os.makedirs(S)
except OSError:
    pass
LOG = os.path.join(S, "guard.log")


def log(msg):
    # UTF-8, not the locale's: Windows python defaults to cp1252, so a path or command
    # outside it raised UnicodeEncodeError here - past the OSError handler - and the
    # guard died before its deny was emitted (84.8).
    try:
        with open(LOG, "a", encoding="utf-8") as f:
            f.write("%s [claude:%s] %s\n"
                    % (time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), MODE, msg))
    except OSError:
        pass


def sf(name):
    return os.path.join(S, name)


def present(name):
    return os.path.exists(sf(name))


def mark(name):
    try:
        with open(sf(name), "a"):
            pass
        os.utime(sf(name), None)
    except OSError:
        pass


def clear(name):
    try:
        os.remove(sf(name))
    except OSError:
        pass


def newer(a, b):
    try:
        return os.path.getmtime(sf(a)) > os.path.getmtime(sf(b))
    except OSError:
        return False


def emit(obj):
    sys.stdout.write(json.dumps(obj, separators=(",", ":")))


# A comment or formatting edit needs no red (GATE_RECIPES.md, cosmetic exemption).
# Asked only of a write that would otherwise be denied or logged as a violation, so a
# licensed write never pays for it. The classifier can only GRANT: missing, broken, unsure - each returns "" and
# today's rule applies. Imported in-process (no second python), with bytecode writing
# off - an import by path would otherwise drop __pycache__/ into the working tree.
def cosmetic(path, rel):
    f = os.path.join(ROOT, ".github", "hooks", "sdlc-cosmetic.py")
    if not os.path.isfile(f):
        return ""
    try:
        import importlib.util
        sys.dont_write_bytecode = True
        spec = importlib.util.spec_from_file_location("sdlc_cosmetic", f)
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        code, detail = m.check_write(ROOT, path, D.get("tool_name") or "", TOOL_INPUT,
                                     os.path.join(S, "cosmetic"))
    except Exception as e:
        log("cosmetic classifier failed (%s) - today's rule applies: %s"
            % (e.__class__.__name__, rel))
        return ""
    if code == 0:
        return detail
    log("not cosmetic (%s): %s" % (detail, rel))
    return ""


try:
    D = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
    if not isinstance(D, dict):
        raise ValueError
except Exception:
    # Never deny on the guard's own failure - a broken guard that denies reads as
    # enforcement and blocks real work.
    log("GUARD ERROR: could not parse the hook payload - not guarding this call")
    sys.exit(0)

# Copilot CLI reads .claude/settings.json as repo config (1.0.12+) and runs these
# hooks too, handing them its payload TRANSLATED into this dialect's shape - so a
# project carrying both dialects would have this guard reading Copilot's events
# into the state directory the Copilot guard owns, and a failing Copilot test run
# arrives here as a PostToolUse success, i.e. as a green. The Copilot guard is the
# one guarding that session; this one stands down, silently, before touching state.
# The translated payload is the only one carrying hook_event_name AND timestamp
# without permission_mode (measured 2026-09-28, Copilot 1.0.88 / Claude Code
# 2.1.283; Copilot's native payload is camelCase with no hook_event_name). Should
# Claude Code ever add a timestamp it still carries permission_mode, so a misfire
# here keeps guarding rather than going quiet.
if "hook_event_name" in D and "timestamp" in D and "permission_mode" not in D:
    sys.exit(0)

# Observations are SESSION-scoped: a red observed in an earlier session does not
# license a production write in this one. A new session_id resets them.
SID = D.get("session_id") or ""
if SID:
    prev = ""
    try:
        with open(sf("session")) as f:
            prev = f.read()
    except OSError:
        pass
    if SID != prev:
        for n in ("red-observed", "green-observed", "last-test-edit",
                  "refactor-license", "close-out-license",
                  "close-out-survivals", "prod-write-observed"):
            clear(n)
        try:
            with open(sf("session"), "w") as f:
                f.write(SID)
        except OSError:
            pass
        log("new session %s - previous observations cleared" % SID)

TOOL_INPUT = D.get("tool_input") or {}
if not isinstance(TOOL_INPUT, dict):
    TOOL_INPUT = {}
EVENT = D.get("hook_event_name") or ""


if MODE == "pre-write":
    p = TOOL_INPUT.get("file_path") or ""
    if not p:
        log("no path parsed from the write payload")
        sys.exit(0)
    # Paths arrive absolute-Windows (measured). Classify on the normalized
    # repo-relative path and on the basename, so both `tests/*` and `test_*.py`
    # shaped patterns work. Test check runs FIRST: SOURCE_GLOB is extension-only,
    # so it matches test files just as readily as production ones.
    n = p.replace("\\", "/")
    root_n = ROOT.replace("\\", "/").rstrip("/")
    if n.lower().startswith(root_n.lower() + "/"):
        rel = n[len(root_n) + 1:]
    elif os.path.isabs(p):
        # An absolute path outside the repository is not this project's source: a
        # session scratchpad, a temp file, another checkout. It used to keep its
        # absolute form as `rel`, fail TEST_PATH_PATTERN, match the extension-only
        # SOURCE_GLOB, and be charged as production - so a throwaway mutation runner
        # under Temp/ cost the same license as an edit to the module guarding the
        # project's authoritative database. A control that cannot tell those two
        # acts apart charges the same price for both, which is how a license stops
        # meaning anything. Measured over one arc: 13 denials, 5 of them on a
        # session scratchpad, and a mandated /end-phase verification step that could
        # not be executed as written (owner ruling: a file outside the
        # repository cannot be production source).
        log("write outside the repository - not production source: %s" % p)
        sys.exit(0)
    else:
        # A relative path can only be relative to the root the guard resolved, so it
        # stays in scope. Skipping it here would be a hole in the guard, not a
        # scoping fix - the Copilot dialect measured both path shapes arriving.
        rel = n[2:] if n.startswith("./") else n
    base = rel.rsplit("/", 1)[-1]
    # Exempt BEFORE the test check: a matching file is neither production nor a test,
    # so a script directory's own tests do not start a cycle either. SOURCE_GLOB is
    # extension-only, so before this a one-off tools script, a config written in the
    # source language and the graph tool's scratch each needed a red no test could
    # produce - measured on two adopters (2026-10-20). Logged only for a
    # file the guard would otherwise have charged; anything else stays silent.
    if match_any(rel, ALWAYS_EXEMPT) or match_any(rel, GUARD_EXEMPT_PATTERN):
        if match_any(base, SOURCE_GLOB):
            log("exempt from the guard (not production source, not a test): %s" % rel)
        sys.exit(0)
    if match_any(rel, TEST_PATH_PATTERN) or match_any(base, TEST_PATH_PATTERN):
        # A test edit invalidates any earlier red and revokes any refactor
        # license - a new test is a new cycle.
        mark("last-test-edit")
        log("test edit recorded (any earlier red is now stale)")
        if present("refactor-license"):
            clear("refactor-license")
            log("refactor license revoked (a test edit starts a new cycle)")
        # A CLOSE-OUT license survives, because close-out's own mandated order puts
        # test edits between its production writes. It is counted, not silent: a
        # license still open after many test edits is one held past its step.
        if present("close-out-license"):
            k = 0
            try:
                with open(sf("close-out-survivals")) as f:
                    k = int((f.read() or "0").strip() or "0")
            except (OSError, ValueError):
                k = 0
            k += 1
            try:
                with open(sf("close-out-survivals"), "w") as f:
                    f.write(str(k))
            except OSError:
                pass
            log("close-out license SURVIVED a test edit (%d this session) - "
                "close-out edits tests between its production writes by design" % k)
        sys.exit(0)
    if not match_any(base, SOURCE_GLOB):
        sys.exit(0)
    ok = ""
    if present("red-observed") and present("last-test-edit") \
            and newer("red-observed", "last-test-edit"):
        ok = "red"
    elif (present("refactor-license") or present("close-out-license")) \
            and present("green-observed"):
        # The declaration alone licenses nothing - without a counted green this
        # session there is no gate behind the claim. Both licenses answer here;
        # they differ only in what a test edit does to them.
        ok = "lic"
    label = "" if ok else cosmetic(p, rel)
    # The marker records a production write that actually WENT THROUGH; the deny
    # branch sets nothing on purpose - a denied write leaves the tree unchanged,
    # and a stop guard armed by it would demand a green for code never written.
    if ok == "red":
        mark("prod-write-observed")
        log("OK production write (red observed since last test edit): %s" % rel)
    elif ok == "lic":
        which = "close-out" if present("close-out-license") else "refactor"
        first = ""
        try:
            with open(sf(which + "-license")) as f:
                first = f.readline().strip()
        except OSError:
            pass
        log("OK production write (%s license: %s): %s" % (which, first, rel))
        mark("prod-write-observed")
    elif label:
        # Logged, and arms nothing: a comment edit needs no green to stop on (82.9
        # ruling 2), the same reason a docs session stops clean.
        log("OK production write (cosmetic: %s): %s" % (label, rel))
    elif present("deny-enabled"):
        log("DENY production write without observed red: %s" % rel)
        emit({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason":
                "TDD ordering: the write to %s was denied because this session has "
                "not edited a test file and then observed a failing test run. For "
                "new behavior: write or edit one test, run it, watch it fail, then "
                "implement. Run the tests as a single bare command (no ';', '&' or "
                "'|' separators - the guard counts that run only if it is the "
                "test's own), then retry this edit. For a BEHAVIOR-PRESERVING edit "
                "at any point in the cycle (refactor, simplification, mutation "
                "testing - including a temporary mutation to prove a test of "
                "existing behavior bites): declare it instead - write one line "
                "naming the step and move to %s/refactor-license, then "
                "retry. That license requires a counted green run this session, is "
                "revoked by the next test edit, ends with the session, and every "
                "write made under it is logged for review. If you are running "
                "/end-slice, declare %s/close-out-license instead - "
                "same rules, except a test edit does NOT revoke it, because "
                "close-out's own step order edits tests between its production "
                "writes; each test edit it survives is counted in the log."
                % (rel, LIC, LIC)}})
    else:
        mark("prod-write-observed")
        log("VIOLATION production write without observed red: %s" % rel)
    sys.exit(0)


if MODE == "observe-test":
    cmd = (TOOL_INPUT.get("command") or "").replace("\n", " ")
    # Classify on the command with quoted arguments removed. TEST_CMD_PATTERN is
    # substring-shaped by design (`*pytest*`, `*mvn*test*`), so matching it against
    # the raw string fired on any command whose TEXT merely mentioned the runner: a
    # `git commit -m` whose body quotes the RED command, an append writing a RED
    # record. Measured: three spurious notices in one phase, on a control whose
    # refusals have to be believed. Quoted text is data, never what the shell
    # runs. Known cost, stated rather than
    # hidden: a runner reachable ONLY inside a quoted argument (`bash -c "pytest"`)
    # no longer counts - run it bare, which is what the compound rule below asks for
    # anyway. The compound check deliberately keeps reading the RAW command: a
    # stripping bug there would admit a genuine compound and record a false GREEN,
    # so that check stays conservative and this one does not feed it.
    probe = re.sub(r'"[^"]*"|\'[^\']*\'', " ", cmd)
    if not cmd or not match_any(probe, TEST_CMD_PATTERN):
        sys.exit(0)
    # Silent, like any other non-test command: nothing ran that could be counted.
    if never_a_test_run(probe):
        sys.exit(0)

    def speak(text):
        emit({"hookSpecificOutput": {
            "hookEventName": EVENT or "PostToolUse",
            "additionalContext": text}})

    # A compound command's outcome is the compound's, not the test's: under the
    # event split a `<red test>; echo done` SUCCEEDS and would record a false
    # GREEN - the exact defect the Copilot dialect measured via its trailer, in
    # event form. Single-character classes on purpose: "&" catches & and &&.
    if any(c in cmd for c in (";", "&", "|")):
        log("test run NOT counted (compound command - the outcome would be the "
            "compound's, not the test's): %s" % cmd)
        speak("TDD ordering: that test run was NOT counted - the command is "
              "compound (contains ';', '&' or '|'), so its outcome is not the "
              "test's. The run itself is unaffected; it just registers nothing. "
              "Flags and single-test selectors are fine - to trim output use the "
              "runner's quiet flag, not a pipe. Re-run as one bare command to "
              "register the RED or GREEN.")
        sys.exit(0)
    if EVENT == "PostToolUse":
        # This event fires only when the command succeeded (measured 2026-08-12);
        # success IS the exit-0 signal, no code field exists to read.
        mark("green-observed")
        log("GREEN observed: %s" % cmd)
        speak("TDD ordering: GREEN counted. The stop guard is satisfied; "
              "full-suite assurance remains the end-slice gate's job.")
    elif EVENT == "PostToolUseFailure":
        if D.get("is_interrupt"):
            log("test run NOT counted (interrupted, not failed): %s" % cmd)
            sys.exit(0)
        m = re.match(r"Exit code (\d+)", D.get("error") or "")
        if not m:
            # A failure event without the measured header may be a tool error
            # rather than the test's own result - the conservative branch the
            # Copilot dialect ships for a missing trailer, same reason.
            log("test run failed but no exit-code header found: %s" % cmd)
            speak("TDD ordering: that failing run could not be counted - no exit "
                  "code was found in the hook payload, so the guard cannot tell "
                  "the test's own result from a tool failure. If this repeats on "
                  "every run, the payload format has changed and the guard needs "
                  "fixing before its ordering can be trusted.")
            sys.exit(0)
        code = m.group(1)
        # A failing exit is the COMMAND's verdict; a RED is the test's. A wrapper that
        # fails before the runner starts - pnpm's install check, a bad flag, a missing
        # binary, a filter matching no tests - exits with the code the runner uses for
        # a failed test, and was counted as the red that licenses a production write
        # (sdlc-kit#16, twice in one adoption). So the runner's own report must be in
        # the output. Both CLIs deliver only the HEAD of a long output (Claude Code
        # about the first 10,000 characters, measured 2026-10-20), so the pattern is a
        # marker the runner prints first, never its closing summary (84.8).
        text = ANSI.sub("", D.get("error") or "").replace("\r\n", "\n")
        try:
            reported = re.search(TEST_REPORT_PATTERN, text, re.M) is not None
        except re.error:
            log("GUARD ERROR: TEST_REPORT_PATTERN is not a valid regular expression - "
                "no failing run can count as a RED until it is fixed")
            reported = False
        if not reported:
            log("test run NOT counted (exit %s, but no test-runner report in the output "
                "- the failure is the command's, not a test's): %s" % (code, cmd))
            speak("TDD ordering: that failing run was NOT counted as a RED - it exited "
                  "%s, but its output carries no test-runner failure report, so the "
                  "failure is the command's, not a test's: an install or environment "
                  "check, a bad flag, a missing binary, or a filter matching no "
                  "tests. Fix that and re-run. If a test really did fail, its report "
                  "was cut off by a long output - re-run it quieter (the runner's "
                  "quiet flag or a single-test selector) to register the RED." % code)
            sys.exit(0)
        mark("red-observed")
        log("RED observed (exit %s): %s" % (code, cmd))
        # The RED message claims a license only when G1 would actually grant one.
        if present("last-test-edit") or ((present("refactor-license")
                                          or present("close-out-license"))
                                         and present("green-observed")):
            speak("TDD ordering: RED counted (exit %s). A production write is "
                  "now licensed for this cycle." % code)
        else:
            speak("TDD ordering: RED counted (exit %s) - but it licenses nothing "
                  "yet: no test file has been edited this session, and a write "
                  "license needs the test edit before its failing run." % code)
    sys.exit(0)


if MODE == "stop-check":
    # Stand down inside a forced continuation: never fight the documented
    # 8-block cap.
    if str(D.get("stop_hook_active")).lower() == "true":
        log("stop: stop_hook_active set - standing down")
        sys.exit(0)
    if not present("prod-write-observed") and not present("last-test-edit"):
        log("stop: clean (no production write or test edit this session - "
            "nothing to guard)")
        sys.exit(0)
    reason = ""
    if not present("green-observed"):
        reason = ("no green test run has been observed in this session - run the "
                  "test suite and get it green before finishing")
    elif present("red-observed") and newer("red-observed", "green-observed"):
        reason = "the latest observed test run is red - get back to green before finishing"
    if not reason:
        log("stop: clean (green observed, not stale)")
    elif present("deny-enabled"):
        log("stop: BLOCK - %s" % reason)
        emit({"decision": "block",
              "reason": "TDD ordering: %s. (Run the tests as a single bare "
                        "command so the guard can count that run as the test's "
                        "own.)" % reason})
    else:
        log("stop: WOULD-BLOCK - %s" % reason)
    sys.exit(0)


log("unknown mode: %s" % MODE)
sys.exit(0)
