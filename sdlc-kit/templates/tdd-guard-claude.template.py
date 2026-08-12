#!/usr/bin/env python
# SDLC TDD-ordering guards G1 + G2 (Claude Code dialect).
#
# Same state machine as the Copilot dialect (sdlc-tdd-guard.sh) - G1 observed-RED
# write guard with the refactor license, G2 premature-stop guard, session-scoped
# state in .git/sdlc-tdd/ - with every signal path rebuilt from the 2026-08-12
# probe (kit FEATURE_PLAN.md 50; raw payloads in the bench's ENF_PROBE_NOTES.md):
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
#     same launcher-line discipline as the gate/guard split (FEATURE_PLAN.md 38.3),
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

# Instantiated by setup for THIS project - same three placeholders, same values,
# as the Copilot dialect's script (reference/GATE_RECIPES.md carries the recipe).
TEST_PATH_PATTERN = "{{TEST_PATH_PATTERN}}"
SOURCE_GLOB = "{{SOURCE_GLOB}}"
TEST_CMD_PATTERN = "{{TEST_CMD_PATTERN}}"


def match_any(value, patterns):
    return any(fnmatch(value, p) for p in patterns.split("|") if p)


# An explicit SDLC_REPO_ROOT wins so a harness can pin it; then the documented
# CLAUDE_PROJECT_DIR; then the measured cwd - but only if .git sits there. With no
# root, do nothing rather than write state to an unrelated directory (the same
# trust-nothing default the Copilot dialect ships, FEATURE_PLAN.md 38.6).
def repo_root():
    r = os.environ.get("SDLC_REPO_ROOT")
    if r:
        return r
    r = os.environ.get("CLAUDE_PROJECT_DIR")
    if r and os.path.isdir(os.path.join(r, ".git")):
        return r
    if os.path.isdir(".git"):
        return os.getcwd()
    return None


ROOT = repo_root()
if not ROOT:
    sys.exit(0)
S = os.path.join(ROOT, ".git", "sdlc-tdd")
try:
    os.makedirs(S)
except OSError:
    pass
LOG = os.path.join(S, "guard.log")


def log(msg):
    try:
        with open(LOG, "a") as f:
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


try:
    D = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
    if not isinstance(D, dict):
        raise ValueError
except Exception:
    # Never deny on the guard's own failure - a broken guard that denies reads as
    # enforcement and blocks real work.
    log("GUARD ERROR: could not parse the hook payload - not guarding this call")
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
                  "refactor-license", "prod-write-observed"):
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
    else:
        rel = n
    base = rel.rsplit("/", 1)[-1]
    if match_any(rel, TEST_PATH_PATTERN) or match_any(base, TEST_PATH_PATTERN):
        # A test edit invalidates any earlier red and revokes any refactor
        # license - a new test is a new cycle.
        mark("last-test-edit")
        log("test edit recorded (any earlier red is now stale)")
        if present("refactor-license"):
            clear("refactor-license")
            log("refactor license revoked (a test edit starts a new cycle)")
        sys.exit(0)
    if not match_any(base, SOURCE_GLOB):
        sys.exit(0)
    ok = ""
    if present("red-observed") and present("last-test-edit") \
            and newer("red-observed", "last-test-edit"):
        ok = "red"
    elif present("refactor-license") and present("green-observed"):
        # The declaration alone licenses nothing - without a counted green this
        # session there is no gate behind the claim.
        ok = "lic"
    # The marker records a production write that actually WENT THROUGH; the deny
    # branch sets nothing on purpose - a denied write leaves the tree unchanged,
    # and a stop guard armed by it would demand a green for code never written.
    if ok == "red":
        mark("prod-write-observed")
        log("OK production write (red observed since last test edit): %s" % rel)
    elif ok == "lic":
        first = ""
        try:
            with open(sf("refactor-license")) as f:
                first = f.readline().strip()
        except OSError:
            pass
        log("OK production write (refactor license: %s): %s" % (first, rel))
        mark("prod-write-observed")
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
                "naming the step and move to .git/sdlc-tdd/refactor-license, then "
                "retry. That license requires a counted green run this session, is "
                "revoked by the next test edit, ends with the session, and every "
                "write made under it is logged for review." % rel}})
    else:
        mark("prod-write-observed")
        log("VIOLATION production write without observed red: %s" % rel)
    sys.exit(0)


if MODE == "observe-test":
    cmd = (TOOL_INPUT.get("command") or "").replace("\n", " ")
    if not cmd or not match_any(cmd, TEST_CMD_PATTERN):
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
        mark("red-observed")
        log("RED observed (exit %s): %s" % (code, cmd))
        # The RED message claims a license only when G1 would actually grant one.
        if present("last-test-edit") or (present("refactor-license")
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
