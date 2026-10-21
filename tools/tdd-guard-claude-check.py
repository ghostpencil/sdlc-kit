#!/usr/bin/env python
"""Re-runnable proof for templates/tdd-guard-claude.template.py.

Two passes, and the second is the point:

  1. a unit pass driving every state transition of both guards, using payload shapes
     measured on the bench (FEATURE_PLAN.md 50; raw payloads in the bench's
     ENF_PROBE_NOTES.md) rather than invented ones - the event split
     (PostToolUse = success only / PostToolUseFailure with an "Exit code N" text
     header), tool_input.file_path in absolute Windows form, stop_hook_active;
  2. a mutation pass that breaks the guard - one mutation per known regression, the
     count derived from the MUTATIONS list at run time, never stated here (a
     hardcoded count is the part that goes stale) - and requires the unit pass to
     notice each one. A suite that survives its own mutations is not testing the
     thing it claims to (invariant 13).

Kit-development artifact: lives at the root, never ships inside sdlc-kit/ (invariant 12).
Run from anywhere:  python tools/tdd-guard-claude-check.py
"""
import concurrent.futures
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import time
import traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(REPO, "sdlc-kit", "templates", "tdd-guard-claude.template.py")
COSMETIC = os.path.join(REPO, "sdlc-kit", "templates", "sdlc-cosmetic.template.py")

# Instantiated for a Python project, using the recipe's own per-language row - the
# same values the sh dialect's suite uses, because the placeholders are shared.
VALUES = {
    "{{TEST_PATH_PATTERN}}": "tests/*|test_*.py|*_test.py",
    "{{SOURCE_GLOB}}": "*.py",
    "{{TEST_CMD_PATTERN}}": "*pytest*",
    "{{TEST_REPORT_PATTERN}}": "=+ (FAILURES|ERRORS) =+",
    "{{GUARD_EXEMPT_PATTERN}}": "tools/*|*.config.*",
}
SID = "session-one"
# pytest's own report header, as both CLIs deliver it (FEATURE_PLAN.md 84.8).
REPORT = "=================================== FAILURES ===================================\n"


def rmtree(path):
    """shutil.rmtree that also removes a bench's git objects. Windows git writes them
    read-only, and rmtree(ignore_errors=True) skipped them without a word: by
    2026-10-21 the suites had left 19,211 bench directories in the temp dir. So a
    second pass clears the read-only bit on whatever survived and deletes again."""
    shutil.rmtree(path, ignore_errors=True)
    if os.path.isdir(path):
        for root, _, files in os.walk(path):
            for f in files:
                try:
                    os.chmod(os.path.join(root, f), stat.S_IWRITE)
                except OSError:
                    pass
        shutil.rmtree(path, ignore_errors=True)


class Bench:
    def __init__(self, base, guard_src):
        self.root = os.path.join(base, "proj")
        self.state = os.path.join(self.root, ".git", "sdlc-tdd")
        self.guard = os.path.join(self.root, ".github", "hooks", "sdlc-tdd-guard.py")
        os.makedirs(os.path.dirname(self.guard))
        os.makedirs(self.state)
        body = guard_src
        for k, v in VALUES.items():
            body = body.replace(k, v)
        assert "{{" not in body, "unresolved placeholder in instantiated guard"
        io.open(self.guard, "w", encoding="utf-8", newline="\n").write(body)

    def run(self, mode, payload, env=None, root_env=True, cwd=None):
        e = dict(os.environ)
        # The suite itself runs inside an agent session: scrub the real session's
        # hook variables so only what each case sets explicitly is visible.
        e.pop("SDLC_REPO_ROOT", None)
        e.pop("CLAUDE_PROJECT_DIR", None)
        if root_env:
            e["SDLC_REPO_ROOT"] = self.root
        if env:
            e.update(env)
        p = subprocess.run([sys.executable, self.guard, mode],
                           input=json.dumps(payload).encode(),
                           capture_output=True, env=e, cwd=cwd or self.root)
        self.rc = p.returncode
        return p.stdout.decode("utf-8", "replace").strip()

    def loglines(self):
        f = os.path.join(self.state, "guard.log")
        if not os.path.exists(f):
            return []
        return [l for l in io.open(f, encoding="utf-8").read().splitlines() if l.strip()]

    def tail(self):
        ls = self.loglines()
        return ls[-1] if ls else ""

    def state_has(self, name):
        return os.path.exists(os.path.join(self.state, name))

    def seed(self, name, content=""):
        io.open(os.path.join(self.state, name), "w").write(content)

    def reset_state(self):
        shutil.rmtree(self.state)
        os.makedirs(self.state)
        self.seed("session", SID)

    def arm_deny(self):
        self.seed("deny-enabled")


def guarded(label, default, fn, *a, **kw):
    """Run one pass; an unexpected exception REPORTS and the run continues.

    A crash used to end the run where it happened, and every case after it never ran -
    and never printed, so the loss did not show up in the output at all. That is how
    tools/skill-ledger-check.py silently lost three cases for six releases
    (FEATURE_PLAN.md 75; the rule is 75.7 ruling 3, generalized to all six suites).
    Correctness failures still fail; what they may no longer do is delete the coverage
    that follows them. `default` is what the caller unpacks when the pass crashed, and
    guarded.crashed carries the run's exit code obligation.
    """
    try:
        return fn(*a, **kw)
    except Exception:
        traceback.print_exc()
        print("CRASHED  %s  <-- pass did not complete; its remaining cases did not run"
              % label)
        guarded.crashed.append(label)
        return default


guarded.crashed = []


def win(root, rel):
    return (root.replace("/", "\\") + "\\" + rel.replace("/", "\\"))


def write(root, rel, sid=SID, tool="Edit"):
    return {"session_id": sid, "cwd": root, "hook_event_name": "PreToolUse",
            "tool_name": tool, "tool_input": {"file_path": win(root, rel)}}


def write_abs(root, abspath, sid=SID, tool="Edit"):
    """A write whose target is an absolute path NOT under the repo root."""
    return {"session_id": sid, "cwd": root, "hook_event_name": "PreToolUse",
            "tool_name": tool, "tool_input": {"file_path": abspath.replace("/", "\\")}}


def write_rel(root, rel, sid=SID, tool="Edit"):
    """A write whose target arrives repo-relative rather than absolute."""
    return {"session_id": sid, "cwd": root, "hook_event_name": "PreToolUse",
            "tool_name": tool, "tool_input": {"file_path": rel}}


def green(root, cmd, sid=SID):
    # PostToolUse fires only on success; tool_response has NO exit-code field.
    return {"session_id": sid, "cwd": root, "hook_event_name": "PostToolUse",
            "tool_name": "PowerShell", "tool_input": {"command": cmd},
            "tool_response": {"stdout": "ok", "stderr": "",
                              "interrupted": False, "isImage": False}}


def red(root, cmd, code=1, sid=SID, interrupt=False, header=True, body=None):
    if body is None:
        body = REPORT + "AssertionError: boom"
    err = ("Exit code %d\n%s" % (code, body)) if header \
        else "tool failed for another reason"
    return {"session_id": sid, "cwd": root, "hook_event_name": "PostToolUseFailure",
            "tool_name": "PowerShell", "tool_input": {"command": cmd},
            "error": err, "is_interrupt": interrupt, "duration_ms": 5}


def stop(root, active=False, sid=SID):
    d = {"session_id": sid, "cwd": root, "hook_event_name": "Stop",
         "stop_hook_active": active, "last_assistant_message": "done"}
    return d


def copilot(root, event, sid="copilot-session", **fields):
    """Copilot's payload as it reaches this dialect's hooks: translated into the
    Claude shape, plus `timestamp`, never `permission_mode` (measured 2026-09-28)."""
    d = {"hook_event_name": event, "session_id": sid,
         "timestamp": "2026-09-28T14:34:33.394Z", "cwd": root}
    d.update(fields)
    return d


def reopen_git(root, mode, newline=None):
    """Rewrite a worktree's .git FILE. Windows git marks it hidden, and a hidden file
    cannot be opened for a truncating write there - so remove it, then create it."""
    p = os.path.join(root, ".git")
    if os.path.isfile(p):
        os.remove(p)
    return io.open(p, mode, newline=newline)


class _FirstFailure(BaseException):
    """Ends a first_only run at its first failing case. BaseException, so neither
    a case's own handler nor guarded() can mistake it for a crash."""


def unit(guard_src, verbose=True, counter=None, first_only=False):
    """Returns the list of failed case names; counts every case into `counter`.
    first_only ends the run at the first failing case - the mutation pass needs
    one, and the cases share one bench, so stopping only drops later cases."""
    failures = []
    base = tempfile.mkdtemp(prefix="tdd-guard-claude-")
    b = Bench(base, guard_src)
    b.seed("session", SID)

    def case(name, cond):
        if counter is not None:
            counter.append(name)
        if not cond:
            failures.append(name)
            if verbose:
                print("FAIL  %s" % name)
            if first_only:
                raise _FirstFailure()

    try:
        # --- session scoping -------------------------------------------------
        b.seed("red-observed")
        b.seed("refactor-license", "step: change-simplify\n")
        b.run("stop-check", stop(b.root, sid="session-two"))
        case("1 a new session clears prior observations",
             not b.state_has("red-observed") and not b.state_has("refactor-license")
             and any("previous observations cleared" in l for l in b.loglines()))

        # --- pre-write: logging mode ----------------------------------------
        b.reset_state()
        out = b.run("pre-write", write(b.root, "pay.py"))
        case("2 unlicensed production write logs VIOLATION and stays silent",
             "VIOLATION production write" in b.tail() and out == ""
             and b.state_has("prod-write-observed"))

        b.reset_state()
        out = b.run("pre-write", write(b.root, "notes.md"))
        case("3 a non-source file is ignored", b.loglines() == [] and out == "")

        # --- pre-write: scope (FIELD_REPORT_2026-08-17.md finding 3) ---------
        # A file outside the repository cannot be production source. Before this,
        # such a path kept its absolute form, failed TEST_PATH_PATTERN, matched the
        # extension-only SOURCE_GLOB, and was charged the price of a source edit.
        outside = os.path.join(tempfile.gettempdir(), "sdlc-scratch", "mutate_s5.py")
        b.reset_state()
        out = b.run("pre-write", write_abs(b.root, outside))
        case("3b an absolute path outside the repo is not production source",
             out == "" and not b.state_has("prod-write-observed")
             and any("outside the repository" in l for l in b.loglines()))

        b.reset_state()
        b.arm_deny()
        out = b.run("pre-write", write_abs(b.root, outside))
        case("3c ...and armed, it is not denied either", out == "")

        # The other direction, and the reason the fix is a containment test rather
        # than a bare else: a relative path is relative to the resolved root, so it
        # stays in scope. Skipping it would be a hole in the guard, not a scoping fix.
        b.reset_state()
        out = b.run("pre-write", write_rel(b.root, "pay.py"))
        case("3d a repo-relative path stays in scope",
             "VIOLATION production write" in b.tail()
             and b.state_has("prod-write-observed"))

        # --- pre-write: deny mode -------------------------------------------
        b.reset_state()
        b.arm_deny()
        out = b.run("pre-write", write(b.root, "pay.py"))
        try:
            j = json.loads(out)
        except ValueError:
            j = {}
        hso = j.get("hookSpecificOutput") or {}
        case("4 armed unlicensed write emits the documented deny JSON",
             hso.get("permissionDecision") == "deny"
             and hso.get("hookEventName") == "PreToolUse"
             and "refactor-license" in (hso.get("permissionDecisionReason") or ""))
        # 4b pins FEATURE_PLAN_HISTORY.md §48/§50.1: the behavior-preserving route
        # is named by CASE, never narrowed by a phase word, because operators who
        # read "close-out" concluded the license was close-out-only. 0.31.0 adds a
        # genuinely close-out-scoped second license, so "close-out" may now appear
        # - but only AFTER the unqualified case sentence, never as its qualifier.
        # Re-pointed, not dropped: the defect §48 fixed is still available.
        _r = hso.get("permissionDecisionReason") or ""
        case("4b the deny names the case, not the phase",
             "BEHAVIOR-PRESERVING" in _r and "at any point in the cycle" in _r
             and ("close-out" not in _r
                  or _r.index("at any point in the cycle") < _r.index("close-out")))
        case("5 a denied production write arms nothing (the tree never changed)",
             not b.state_has("prod-write-observed"))
        b.run("stop-check", stop(b.root))
        case("5b ...so the stop after it is clean",
             "stop: clean (no production write or test edit" in b.tail())

        # --- the red path ----------------------------------------------------
        b.reset_state()
        b.run("pre-write", write(b.root, "tests/test_pay.py"))
        case("6 a test edit is recorded",
             b.state_has("last-test-edit")
             and "test edit recorded" in b.tail())
        time.sleep(0.05)
        out = b.run("observe-test", red(b.root, "pytest tests/test_pay.py"))
        case("7 a failing test-pattern run counts a RED off the event split",
             b.state_has("red-observed") and "RED observed (exit 1)" in b.tail())
        case("7b the spoken RED claims the license it earned",
             "now licensed" in out)

        # --- observe-test: the command, not its text (…-17b.md finding 2) ----
        # TEST_CMD_PATTERN is substring-shaped, so matching it against the raw
        # string counted any command whose TEXT mentioned the runner. Measured:
        # a `git commit -m` quoting the RED command, twice an append writing a
        # RED record - three spurious notices in one phase.
        b.reset_state()
        b.run("pre-write", write(b.root, "tests/test_pay.py"))
        time.sleep(0.05)
        out = b.run("observe-test",
                    red(b.root, 'git commit -m "RED: pytest tests/test_pay.py"'))
        case("7c a runner named only inside a quoted argument counts nothing",
             not b.state_has("red-observed") and out == "")

        # The other direction: quoting an ARGUMENT must not hide a real run.
        out = b.run("observe-test", red(b.root, 'pytest -k "pay and not slow"'))
        case("7d a real run with a quoted argument still counts",
             b.state_has("red-observed"))
        out = b.run("pre-write", write(b.root, "pay.py"))
        case("8 red-after-test-edit licenses the production write",
             "OK production write (red observed since last test edit)" in b.tail())

        b.reset_state()
        out = b.run("observe-test", red(b.root, "pytest tests/test_pay.py"))
        case("9 a red with no test edit counts but licenses nothing, and says so",
             b.state_has("red-observed") and "licenses nothing yet" in out)
        out = b.run("pre-write", write(b.root, "pay.py"))
        case("9b ...and the write is still a violation",
             "VIOLATION production write" in b.tail())

        # --- the green path and the refactor license -------------------------
        b.reset_state()
        out = b.run("observe-test", green(b.root, "pytest -q"))
        case("10 a succeeding test-pattern run counts a GREEN off the event split",
             b.state_has("green-observed") and "GREEN observed" in b.tail()
             and "GREEN counted" in out)

        b.seed("refactor-license", "step: change-simplify, move: inline helper\n")
        b.run("pre-write", write(b.root, "pay.py"))
        case("11 license + green licenses a behavior-preserving write, logged with its line",
             "OK production write (refactor license: step: change-simplify" in b.tail())

        b.reset_state()
        b.arm_deny()
        b.seed("refactor-license", "step: change-simplify\n")
        b.run("pre-write", write(b.root, "pay.py"))
        case("12 a refactor license without a green licenses nothing",
             "DENY production write" in b.tail())

        b.reset_state()
        b.seed("refactor-license", "step: mutation-testing\n")
        b.run("pre-write", write(b.root, "test_pay.py"))
        case("13 a test edit revokes the license",
             not b.state_has("refactor-license")
             and any("refactor license revoked" in l for l in b.loglines()))

        # --- the close-out license (FIELD_REPORT_2026-09-01.md finding 1) -----
        # Close-out's mandated order is review (fixes tests) -> mutation (writes
        # production, restores tests) -> verify (writes a harness), so a license a
        # test edit revokes cannot survive its own step. A real arc re-declared it
        # seven times in one phase. This license differs from the refactor one in
        # exactly one way, and the survivals are counted so it cannot be silent.
        b.reset_state()
        out = b.run("observe-test", green(b.root, "pytest -q"))
        b.seed("close-out-license", "step: end-slice mutation check\n")
        b.run("pre-write", write(b.root, "pay.py"))
        case("13a a close-out license + green licenses a write, logged as close-out",
             "OK production write (close-out license: step: end-slice mutation check"
             in b.tail())

        b.run("pre-write", write(b.root, "test_pay.py"))
        case("13b a test edit does NOT revoke the close-out license, and is counted",
             b.state_has("close-out-license")
             and any("close-out license SURVIVED a test edit (1 this session)" in l
                     for l in b.loglines()))

        b.run("pre-write", write(b.root, "test_other.py"))
        case("13c each surviving test edit increments the count",
             any("close-out license SURVIVED a test edit (2 this session)" in l
                 for l in b.loglines()))

        b.run("pre-write", write(b.root, "pay.py"))
        case("13d the license still licenses a write after the test edits",
             "OK production write (close-out license:" in b.tail())

        b.reset_state()
        b.arm_deny()
        b.seed("close-out-license", "step: end-slice mutation check\n")
        b.run("pre-write", write(b.root, "pay.py"))
        case("13e a close-out license without a green licenses nothing either",
             "DENY production write" in b.tail())

        b.reset_state()
        b.seed("close-out-license", "step: end-slice\n")
        b.seed("close-out-survivals", "4")
        b.run("stop-check", stop(b.root, sid="session-three"))
        case("13f a new session clears the close-out license and its count",
             not b.state_has("close-out-license")
             and not b.state_has("close-out-survivals"))
        b.seed("session", SID)

        b.reset_state()
        b.arm_deny()
        out = b.run("pre-write", write(b.root, "pay.py"))
        # Defensive exactly as case 4 is: a mutation that re-silences the deny makes
        # this empty, and an unguarded parse would crash the pass and take every
        # later case with it (the §75.7 failure shape).
        try:
            _hso = (json.loads(out) or {}).get("hookSpecificOutput") or {}
        except ValueError:
            _hso = {}
        case("13g the deny message names the close-out license as the close-out route",
             "close-out-license" in (_hso.get("permissionDecisionReason") or ""))

        # --- observation refusals --------------------------------------------
        for sep, label in ((";", "semicolon"), ("&", "single ampersand"), ("|", "pipe")):
            b.reset_state()
            out = b.run("observe-test", green(b.root, "pytest -q %s echo done" % sep))
            case("14 compound command (%s) is refused, spoken, and counts nothing" % label,
                 "NOT counted (compound command" in b.tail()
                 and "NOT counted" in out and not b.state_has("green-observed"))

        b.reset_state()
        b.run("observe-test", green(b.root, "ls -la"))
        case("15 a non-test command observes nothing", b.loglines() == [])

        b.reset_state()
        b.run("observe-test", red(b.root, "pytest -q", interrupt=True))
        case("16 an interrupted failure counts nothing",
             not b.state_has("red-observed") and "NOT counted (interrupted" in b.tail())

        b.reset_state()
        out = b.run("observe-test", red(b.root, "pytest -q", header=False))
        case("17 a failure without the exit-code header counts nothing and says why",
             not b.state_has("red-observed")
             and "no exit-code header found" in b.tail()
             and "could not be counted" in out)

        # --- stop-check -------------------------------------------------------
        b.reset_state()
        b.run("stop-check", stop(b.root))
        case("18 a session with no writes stops clean",
             "stop: clean (no production write or test edit" in b.tail())

        b.reset_state()
        b.run("pre-write", write(b.root, "pay.py"))  # VIOLATION, marks the session
        b.run("stop-check", stop(b.root))
        case("19 no green observed logs WOULD-BLOCK in logging mode",
             "stop: WOULD-BLOCK - no green test run" in b.tail())
        b.arm_deny()
        out = b.run("stop-check", stop(b.root))
        try:
            j = json.loads(out)
        except ValueError:
            j = {}
        case("20 armed no-green stop emits the documented block JSON",
             j.get("decision") == "block" and "no green test run" in (j.get("reason") or ""))
        out = b.run("stop-check", stop(b.root, active=True))
        case("21 stop_hook_active stands down, deny mode included",
             out == "" and "standing down" in b.tail())

        b.reset_state()
        b.arm_deny()
        b.run("pre-write", write(b.root, "tests/test_pay.py"))
        time.sleep(0.05)
        b.run("observe-test", green(b.root, "pytest -q"))
        time.sleep(0.05)
        b.run("observe-test", red(b.root, "pytest -q"))
        out = b.run("stop-check", stop(b.root))
        try:
            j = json.loads(out)
        except ValueError:
            j = {}
        case("22 a red newer than the green blocks the stop",
             j.get("decision") == "block" and "is red" in (j.get("reason") or ""))
        time.sleep(0.05)
        b.run("observe-test", green(b.root, "pytest -q"))
        out = b.run("stop-check", stop(b.root))
        case("23 back to green stops clean", out == "" and "stop: clean (green observed" in b.tail())

        # --- roots and rot ----------------------------------------------------
        outside = os.path.join(base, "elsewhere")
        os.makedirs(outside)
        b.run("pre-write", write(b.root, "pay.py"), root_env=False, cwd=outside)
        case("24 no root and no .git at cwd is a no-op",
             not os.path.exists(os.path.join(outside, ".git")))
        # 24b: the same at STOP. Since 0.31.1 a .git that names no git directory blocks
        # at stop ("did not run"), so declining to take a non-repo cwd as the root is
        # what keeps a stop outside any repository silent.
        out = b.run("stop-check", stop(b.root), root_env=False, cwd=outside)
        case("24b ...and stop-check there is silent too - no block outside a repo", out == "")

        b.reset_state()
        b.run("pre-write", write(b.root, "pay.py"), root_env=False,
              env={"CLAUDE_PROJECT_DIR": b.root}, cwd=os.path.join(base))
        case("25 CLAUDE_PROJECT_DIR locates the root when the env var is all there is",
             "VIOLATION production write" in b.tail())

        # 25c: the harness contract. A PINNED SDLC_REPO_ROOT with no .git at all still
        # guards, state created under it - the exact harness an adopter's own guard
        # tests use (a bare tmp_path), which 0.31.1 made guard nothing, silently.
        bare = os.path.join(base, "bare-root")
        os.makedirs(bare)
        e = dict(os.environ)
        e.pop("CLAUDE_PROJECT_DIR", None)
        e["SDLC_REPO_ROOT"] = bare
        subprocess.run([sys.executable, b.guard, "pre-write"],
                       input=json.dumps(write(bare, "pay.py")).encode(),
                       capture_output=True, env=e, cwd=bare)
        bl = os.path.join(bare, ".git", "sdlc-tdd", "guard.log")
        case("25c a pinned root with NO .git still guards, state created under it",
             os.path.exists(bl) and "VIOLATION" in io.open(bl, encoding="utf-8").read())

        b.reset_state()
        p = subprocess.run([sys.executable, b.guard, "pre-write"], input=b"not json",
                           capture_output=True,
                           env=dict(os.environ, SDLC_REPO_ROOT=b.root))
        case("26 an unparseable payload is spoken in the log and never denies",
             p.returncode == 0 and "GUARD ERROR: could not parse" in b.tail())

        b.reset_state()
        b.run("pre-write", write(b.root, "src/my module.py"))
        case("27 a path containing a space is one path",
             "VIOLATION production write" in b.tail() and "my module.py" in b.tail())

        # --- Copilot running this dialect (FEATURE_PLAN.md 79) -------------------
        # Copilot reads .claude/settings.json and hands these hooks its payload
        # translated into this shape - measured 2026-09-28, 1.0.88. The guard must
        # stand down before touching state: a new session id would clear the
        # Copilot guard's observations, and a failing test run arrives as a
        # PostToolUse success, i.e. as a green.
        b.reset_state()
        b.seed("red-observed")
        b.run("pre-write", copilot(b.root, "PreToolUse", tool="Write",
                                   tool_input={"path": win(b.root, "pay.py"),
                                               "file_text": "a\n"}))
        b.run("observe-test", copilot(b.root, "PostToolUse", tool="Bash",
                                      tool_input={"command": "pytest -q"},
                                      tool_result={"result_type": "success",
                                                   "text_result_for_llm": "1 failed"}))
        b.arm_deny()
        b.seed("prod-write-observed")
        out = b.run("stop-check", copilot(b.root, "Stop", stop_hook_active=False,
                                          stop_reason="end_turn"))
        case("29 a Copilot-translated payload: no log, no state change, no block",
             b.loglines() == [] and out == "" and b.state_has("red-observed")
             and not b.state_has("green-observed")
             and io.open(os.path.join(b.state, "session")).read() == SID)

        b.reset_state()
        p = write(b.root, "pay.py")
        p.update(timestamp="2026-09-28T14:34:33.394Z", permission_mode="default")
        b.run("pre-write", p)
        case("30 a Claude payload that gains a timestamp still guards",
             "VIOLATION production write" in b.tail())

        # --- a RED needs the runner's own report (FEATURE_PLAN.md 84, sdlc-kit#16) --
        # A wrapper that fails before the runner starts exits with the code a failed
        # test uses; it was counted as the red that licenses a production write.
        b.reset_state()
        b.run("pre-write", write(b.root, "tests/test_pay.py"))
        time.sleep(0.05)
        out = b.run("observe-test", red(
            b.root, "pytest tests/test_pay.py",
            body="[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: esbuild\n"
                 "pnpm: Command failed with exit code 1"))
        case("31 a failure with no runner report counts no RED, and says why",
             not b.state_has("red-observed")
             and "no test-runner report in the output" in b.tail()
             and "NOT counted as a RED" in out and "re-run it quieter" in out)
        out = b.run("pre-write", write(b.root, "pay.py"))
        case("31b ...so the write after it is still a violation",
             "VIOLATION production write" in b.tail())

        b.reset_state()
        b.run("pre-write", write(b.root, "tests/test_pay.py"))
        time.sleep(0.05)
        b.run("observe-test", red(
            b.root, "pytest -q", code=2,
            body="=========================== ERRORS ===========================\n"
                 "ImportError while importing test module\n"
                 "Interrupted: 1 error during collection"))
        case("31c a collection error (exit 2) is the commonest first red, and counts",
             b.state_has("red-observed") and "RED observed (exit 2)" in b.tail())

        # Claude Code keeps about the first 10,000 characters of a long output: a red
        # whose report comes after that much streamed output arrives without one.
        b.reset_state()
        b.run("observe-test", red(b.root, "pytest -q -s",
                                  body="filler line ....\n" * 600))
        case("31d a report cut off by a long output counts no RED",
             not b.state_has("red-observed"))

        # Colour codes inside the marker: jest colours its frames with no terminal.
        b.reset_state()
        b.run("observe-test", red(b.root, "pytest -q",
                                  body="\x1b[31m=====\x1b[0m FAILURES =====\r\nboom"))
        case("31e the report is matched with ANSI codes and CRLF removed",
             b.state_has("red-observed"))

        bad = Bench(os.path.join(base, "badpattern"),
                    guard_src.replace("{{TEST_REPORT_PATTERN}}", "([unclosed"))
        bad.seed("session", SID)
        bad.run("observe-test", red(bad.root, "pytest -q"))
        case("31f an invalid report pattern: exit 0, no RED, a GUARD ERROR logged",
             bad.rc == 0 and not bad.state_has("red-observed")
             and any("TEST_REPORT_PATTERN is not a valid" in l for l in bad.loglines()))

        # --- commands that name the runner without running it (84.4(1)) --------
        # Their SUCCESS was the worse defect: a GREEN that satisfied the stop guard
        # with no test run at all.
        for c in ("cat pytest.ini", "grep pytest pyproject.toml",
                  "sed -n 1,5p pytest.ini", "git log --grep pytest",
                  "gh api repos/pytest-dev/pytest/releases/latest",
                  "Get-Content pytest.ini", "pip install pytest",
                  "python -m pip install pytest", "uv add --dev pytest",
                  "PYTHONPATH=. cat pytest.ini", r"C:\Git\usr\bin\cat.exe pytest.ini"):
            b.reset_state()
            o1 = b.run("observe-test", green(b.root, c))
            o2 = b.run("observe-test", red(b.root, c))
            case("32 '%s' counts neither GREEN nor RED, silently" % c,
                 not b.state_has("green-observed") and not b.state_has("red-observed")
                 and o1 == "" and o2 == "" and b.loglines() == [])

        for c in ("uv run pytest -q", "python -m pytest -q", "env CI=1 pytest -q",
                  r"C:\proj\.venv\Scripts\pytest.exe -q"):
            b.reset_state()
            b.run("observe-test", green(b.root, c))
            case("32b a real run through '%s' still counts" % c,
                 b.state_has("green-observed"))

        b.reset_state()
        out = b.run("observe-test", green(
            b.root, "git commit -F - <<'EOF'\nfeat: pay\n\nGREEN: pytest -q passes\nEOF"))
        case("33 a heredoc naming the runner counts nothing (the commit-recipe false GREEN)",
             not b.state_has("green-observed") and out == "" and b.loglines() == [])
        # The two checks above each have a case of their own whose executable the
        # read-only list does NOT cover - `git` would mask either one's removal.
        b.reset_state()
        b.run("observe-test", green(
            b.root, "python scripts/note.py <<'EOF'\nGREEN: pytest -q passes\nEOF"))
        case("33b ...whatever executable reads it",
             not b.state_has("green-observed") and b.loglines() == [])
        b.reset_state()
        b.run("observe-test", green(b.root, 'python scripts/note.py "RED: pytest -q"'))
        case("33c a runner named only in a quoted argument of another program counts "
             "nothing", not b.state_has("green-observed") and b.loglines() == [])

        # --- the exempt pattern (84.7 ruling 6) ---------------------------------
        b.reset_state()
        b.arm_deny()
        out = b.run("pre-write", write(b.root, "tools/measure_recall.py"))
        case("34 a write under GUARD_EXEMPT_PATTERN is not denied, and is logged exempt",
             out == "" and not b.state_has("prod-write-observed")
             and "exempt from the guard" in b.tail())
        out = b.run("pre-write", write(b.root, "playwright.config.py"))
        case("34b a config file is exempt the same way", out == ""
             and "exempt from the guard" in b.tail())
        out = b.run("pre-write", write(b.root, ".ua/tmp/build_batch.py"))
        case("34c the graph tool's directory is exempt in every project",
             out == "" and "exempt from the guard" in b.tail())
        b.run("pre-write", write(b.root, "tools/tests/test_measure.py"))
        case("34d a test under an exempt directory is not a test edit either",
             not b.state_has("last-test-edit"))
        n = len(b.loglines())
        b.run("pre-write", write(b.root, "tools/README.md"))
        case("34e an exempt non-source file stays silent", len(b.loglines()) == n)
        out = b.run("pre-write", write(b.root, "src/pay.py"))
        case("34f code outside the pattern is still guarded",
             '"permissionDecision":"deny"' in out)
        out = b.run("pre-write", write(b.root, "src/日本.py"))
        case("35 a path outside cp1252 is still denied (the log write cannot kill it)",
             b.rc == 0 and '"permissionDecision":"deny"' in out)

        # --- linked worktrees (FEATURE_PLAN.md 78) ------------------------------
        # A REAL worktree, because the Bench's hand-made .git directory is exactly
        # the configuration that cannot see this defect: in a worktree .git is a
        # file naming the git directory, and a directory test disarmed the guard.
        wt_base = os.path.join(base, "wt-fixture")
        main_r = os.path.join(wt_base, "main")
        wt_r = os.path.join(wt_base, "wt")
        os.makedirs(main_r)
        g = lambda *a: subprocess.run(["git"] + list(a), capture_output=True, text=True)
        g("init", "-q", main_r)
        io.open(os.path.join(main_r, "README"), "w").write("x\n")
        g("-C", main_r, "add", "README")
        g("-C", main_r, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", "i")
        g("-C", main_r, "worktree", "add", "-q", wt_r, "-b", "wt")
        gd = g("-C", wt_r, "rev-parse", "--absolute-git-dir").stdout.strip()
        wt_state = os.path.join(gd, "sdlc-tdd")
        os.makedirs(os.path.join(wt_r, ".github", "hooks"))
        shutil.copy(b.guard, os.path.join(wt_r, ".github", "hooks", "sdlc-tdd-guard.py"))

        def wt_run(mode, payload):
            if mode == "pre-write":
                rmtree(wt_state)
            e = dict(os.environ)
            e.pop("SDLC_REPO_ROOT", None)
            e["CLAUDE_PROJECT_DIR"] = wt_r
            p = subprocess.run([sys.executable, os.path.join(wt_r, ".github", "hooks",
                                                             "sdlc-tdd-guard.py"), mode],
                               input=json.dumps(payload).encode(), capture_output=True,
                               env=e, cwd=wt_r)
            return p.stdout.decode("utf-8", "replace").strip()

        def wt_log():
            f = os.path.join(wt_state, "guard.log")
            return io.open(f, encoding="utf-8").read() if os.path.exists(f) else ""

        wt_run("pre-write", write(wt_r, "pay.py"))
        case("28 worktree via CLAUDE_PROJECT_DIR: guarded, state in the worktree's git dir",
             os.path.isfile(os.path.join(wt_r, ".git"))
             and "VIOLATION production write" in wt_log()
             and not os.path.exists(os.path.join(main_r, ".git", "sdlc-tdd")))

        rel = os.path.relpath(gd, wt_r).replace(os.sep, "/")
        reopen_git(wt_r, "w", newline="\n").write("gitdir: %s\n" % rel)
        wt_run("pre-write", write(wt_r, "pay.py"))
        case("28b ...and through a RELATIVE gitdir",
             "VIOLATION production write" in wt_log())

        os.makedirs(wt_state, exist_ok=True)
        io.open(os.path.join(wt_state, "deny-enabled"), "w").write("")
        io.open(os.path.join(wt_state, "session"), "w").write(SID)
        e = dict(os.environ)
        e.pop("SDLC_REPO_ROOT", None)
        e["CLAUDE_PROJECT_DIR"] = wt_r
        p = subprocess.run([sys.executable, os.path.join(wt_r, ".github", "hooks",
                                                         "sdlc-tdd-guard.py"), "pre-write"],
                           input=json.dumps(write(wt_r, "pay.py")).encode(),
                           capture_output=True, env=e, cwd=wt_r)
        reason = p.stdout.decode("utf-8", "replace")
        case("28c the deny names the worktree's REAL licence directory, not .git/",
             "refactor-license" in reason and ".git/sdlc-tdd/" not in reason
             and "/worktrees/" in reason.replace("\\\\", "/").replace("\\", "/"))

        reopen_git(wt_r, "w", newline="\n").write(
            "gitdir: %s\n" % os.path.join(wt_base, "nowhere").replace(os.sep, "/"))
        out = wt_run("stop-check", stop(wt_r))
        try:
            j = json.loads(out)
        except ValueError:
            j = {}
        case("28d a .git naming no git dir: stop-check blocks, saying the guard did not run",
             j.get("decision") == "block" and "did not run" in (j.get("reason") or ""))
        out = wt_run("stop-check", stop(wt_r, active=True))
        case("28e ...and stands down on stop_hook_active", out == "")

        # --- COSMETIC (FEATURE_PLAN.md 82): a comment or format edit needs no red ---
        # Real payloads against a real file, deny armed. The classifier is the shipped
        # sdlc-cosmetic.py beside the guard; tools/cosmetic-check.py proves it alone.
        c = Bench(os.path.join(base, "cos"), guard_src)
        hooks = os.path.dirname(c.guard)
        shutil.copy(COSMETIC, os.path.join(hooks, "sdlc-cosmetic.py"))
        body = "def pay(a, b):\n    # sum them\n    return a + b\n"
        src_f = os.path.join(c.root, "pay.py")

        def edit(old, new, tool="Edit", **extra):
            io.open(src_f, "w", encoding="utf-8", newline="").write(body + extra.pop("tail", ""))
            ti = {"file_path": win(c.root, "pay.py")}
            if tool == "Write":
                ti["content"] = new
            else:
                ti.update({"old_string": old, "new_string": new})
            return {"session_id": SID, "cwd": c.root, "hook_event_name": "PreToolUse",
                    "tool_name": tool, "tool_input": ti, "permission_mode": "default"}

        c.reset_state()
        c.arm_deny()
        out = c.run("pre-write", edit("# sum them", "# add them"))
        case("29 armed: a comment-only Edit is allowed and logged as cosmetic",
             out == "" and "OK production write (cosmetic: python-ast): pay.py" in c.tail()
             and not c.state_has("prod-write-observed"))
        out = c.run("stop-check", stop(c.root))
        case("29b ...and leaves the stop guard unarmed", out == ""
             and "nothing to guard" in c.tail())
        out = c.run("pre-write", edit(None, body.replace("# sum them", "# add them"),
                                      tool="Write"))
        case("29c armed: a comment-only Write is allowed", out == ""
             and "cosmetic: python-ast" in c.tail())
        out = c.run("pre-write", edit("a + b", "a - b"))
        case("29d armed: a real Edit is denied exactly as today, and says why it was "
             "not exempt",
             '"permissionDecision":"deny"' in out
             and any("not cosmetic (python-ast: the syntax tree differs)" in l
                     for l in c.loglines())
             and not c.state_has("prod-write-observed"))
        out = c.run("pre-write", edit("# sum them", "# x", tail="# sum them\n"))
        case("29e armed: an ambiguous old_string is denied (cannot tell)",
             '"permissionDecision":"deny"' in out)
        out = c.run("pre-write", edit("# sum them", "# add them"), cwd=c.root)
        case("29f the import by path leaves no __pycache__ in the working tree",
             not os.path.exists(os.path.join(hooks, "__pycache__")))
        io.open(os.path.join(hooks, "sdlc-cosmetic.py"), "w").write(
            "raise RuntimeError('broken classifier')\n")
        out = c.run("pre-write", edit("# sum them", "# add them"))
        case("29g a crashing classifier: exit 0, denied under today's rule, reason logged",
             c.rc == 0 and '"permissionDecision":"deny"' in out
             and any("cosmetic classifier failed" in l for l in c.loglines()))
        os.remove(os.path.join(hooks, "sdlc-cosmetic.py"))
        out = c.run("pre-write", edit("# sum them", "# add them"))
        case("29h no classifier installed: today's rule", c.rc == 0
             and '"permissionDecision":"deny"' in out)
        shutil.copy(COSMETIC, os.path.join(hooks, "sdlc-cosmetic.py"))
        c.reset_state()
        out = c.run("pre-write", edit("# sum them", "# add them"))
        case("29i logging mode: cosmetic is logged OK, not as a VIOLATION",
             out == "" and "cosmetic: python-ast" in c.tail()
             and not c.state_has("prod-write-observed"))
        c.reset_state()
        c.run("pre-write", write(c.root, "tests/test_pay.py"))
        c.run("observe-test", red(c.root, "pytest -q"))
        n = len(c.loglines())
        c.run("pre-write", edit("a + b", "a - b"))
        case("29j a write already licensed never consults the classifier",
             "red observed since last test edit" in c.tail()
             and not any("cosmetic" in l for l in c.loglines()[n:]))
    except _FirstFailure:
        pass
    finally:
        rmtree(base)
    return failures


# One mutation per known regression; the unit pass must notice each. Suite fails
# if any mutation survives (invariant 13).
MUTATIONS = [
    ("drop the green requirement from either license (a bare declaration "
     "licenses with no gate behind it)",
     '    elif (present("refactor-license") or present("close-out-license")) \\\n'
     '            and present("green-observed"):',
     '    elif (present("refactor-license") or present("close-out-license")):'),
    ("never revoke the refactor license on a test edit (the window outlives the "
     "cycle it was declared for)",
     'if present("refactor-license"):\n            clear("refactor-license")',
     'if False:\n            clear("refactor-license")'),
    ("revoke the CLOSE-OUT license on a test edit too (close-out's own mandated "
     "order becomes unexecutable again - FIELD_REPORT_2026-09-01 finding 1)",
     '        if present("close-out-license"):\n            k = 0',
     '        if present("close-out-license"):\n            clear("close-out-license")\n            k = 0'),
    ("stop counting the test edits a close-out license survives (a license held "
     "open past its step goes silent)",
     'log("close-out license SURVIVED a test edit (%d this session) - "',
     'log("close-out license survived (%d) - "'),
    ("let the close-out license write without a green (the one bound both "
     "licenses share)",
     'elif (present("refactor-license") or present("close-out-license")) \\\n'
     '            and present("green-observed"):\n        # The declaration alone',
     'elif present("refactor-license") or present("close-out-license"):\n        # The declaration alone'),
    ("leak observations across sessions (survives the new-session clear)",
     'if SID != prev:',
     'if False:'),
    ("count compound commands (a red test behind `; echo done` records a false GREEN)",
     'if any(c in cmd for c in (";", "&", "|")):',
     'if False:'),
    ("count interrupted failures as reds",
     'if D.get("is_interrupt"):',
     'if False:'),
    ("arm the stop guard from a denied write (a rule about writes enforced against "
     "a session that made none)",
     'log("DENY production write without observed red: %s" % rel)',
     'mark("prod-write-observed")\n        '
     'log("DENY production write without observed red: %s" % rel)'),
    ("drop the stop_hook_active stand-down (the guard fights the block cap)",
     'if str(D.get("stop_hook_active")).lower() == "true":',
     'if False:'),
    ("re-silence the deny (logging-mode behavior shipped under an armed flag)",
     'emit({"hookSpecificOutput": {\n            "hookEventName": "PreToolUse",',
     'emit({"ignored": {\n            "hookEventName": "PreToolUse",'),
    ("count a headerless failure as a red (a tool error becomes the test's result)",
     'if not m:',
     'if False:'),
    ("read the event split backwards (a failing run counts as the green)",
     'if EVENT == "PostToolUse":',
     'if EVENT == "PostToolUseFailure":'),
    ("classify production before tests (SOURCE_GLOB is extension-only and eats "
     "test files)",
     'if match_any(rel, TEST_PATH_PATTERN) or match_any(base, TEST_PATH_PATTERN):',
     'if False and (match_any(rel, TEST_PATH_PATTERN) or match_any(base, TEST_PATH_PATTERN)):'),
    ("charge out-of-repo writes as production (a session scratchpad costs the "
     "same license as an edit to the module guarding the database)",
     'elif os.path.isabs(p):',
     'elif False:'),
    ("skip relative paths as out-of-repo (a real production write escapes the "
     "guard entirely - the hole the containment test exists to avoid)",
     'rel = n[2:] if n.startswith("./") else n',
     'sys.exit(0)'),
    ("match the runner against the raw command text (a commit message quoting "
     "the RED command counts as a test run)",
     'if not cmd or not match_any(probe, TEST_CMD_PATTERN):',
     'if not cmd or not match_any(cmd, TEST_CMD_PATTERN):'),
    # RE-POINTED at 0.31.1: the cwd test became os.path.exists (a worktree's .git is a
    # file); reported STALE by the suite rather than silently counted, as designed.
    ("trust any cwd when no root is given (state written to unrelated dirs)",
     'if os.path.exists(".git"):\n        return os.getcwd()',
     'return os.getcwd()\n    if os.path.exists(".git"):\n        return os.getcwd()'),
    ("stop reading a worktree's .git file (every worktree session guarded nothing, "
     "in silence - FEATURE_PLAN.md 78)",
     '    if os.path.isdir(p):\n        return p\n    try:',
     '    if os.path.isdir(p):\n        return p\n    return None\n    try:'),
    ("drop the pinned-root fallback (a harness pinning a bare directory guards nothing, "
     "silently - the 0.31.1 regression an adopter's own tests caught)",
     'if not GD and not os.path.exists(os.path.join(ROOT, ".git")):\n    GD = os.path.join(ROOT, ".git")\n',
     ''),
    ("keep state under the root's literal .git (a worktree's state has nowhere to go)",
     'S = os.path.join(GD, "sdlc-tdd")',
     'S = os.path.join(ROOT, ".git", "sdlc-tdd")'),
    ("name the literal .git/ licence path in a worktree's deny (an instruction the "
     "agent cannot follow - .git is a file there)",
     '% (rel, LIC, LIC)',
     '% (rel, ".git/sdlc-tdd", ".git/sdlc-tdd")'),
    ("guard Copilot's translated payloads (its failing run records a green, its "
     "session id clears the Copilot guard's state - FEATURE_PLAN.md 79)",
     'if "hook_event_name" in D and "timestamp" in D and "permission_mode" not in D:\n'
     '    sys.exit(0)',
     ''),
    ("stand down on ANY payload with a timestamp (a Claude session that gains the "
     "key would go unguarded, in silence)",
     'if "hook_event_name" in D and "timestamp" in D and "permission_mode" not in D:',
     'if "hook_event_name" in D and "timestamp" in D:'),
    ("let a cosmetic write arm the stop guard (a comment fix demands a green - "
     "82.9 ruling 2)",
     'log("OK production write (cosmetic: %s): %s" % (label, rel))',
     'mark("prod-write-observed")\n        '
     'log("OK production write (cosmetic: %s): %s" % (label, rel))'),
    ("let 'cannot tell' grant the exemption (an ambiguous edit waves through)",
     "if code == 0:\n        return detail",
     "if code in (0, 2):\n        return detail"),
    ("let a crashing classifier crash the guard (a broken file blocks real work)",
     '    except Exception as e:\n        log("cosmetic classifier failed',
     '    except ImportError as e:\n        log("cosmetic classifier failed'),
    ("write bytecode on the import by path (__pycache__/ lands in the working tree)",
     "sys.dont_write_bytecode = True",
     "pass"),
    ("consult the classifier on an already licensed write (cost on every write, and "
     "a licensed write logged as something else)",
     'label = "" if ok else cosmetic(p, rel)',
     'label = cosmetic(p, rel)'),
    ("count any failing exit as a RED (a wrapper's failure licenses a production "
     "write - sdlc-kit#16)",
     "if not reported:",
     "if False:"),
    ("match the report against the raw output (colour codes split the marker)",
     'text = ANSI.sub("", D.get("error") or "").replace("\\r\\n", "\\n")',
     'text = (D.get("error") or "")'),
    ("let an invalid report pattern crash the guard",
     "except re.error:",
     "except KeyError:"),
    ("read a heredoc's body as the command (the commit recipe records a false GREEN)",
     'if "<<" in probe:',
     'if False:'),
    ("count read-only commands that name the runner (cat/grep/git record a GREEN)",
     "if exe in NEVER_RUNS:\n        return True",
     "if False:\n        return True"),
    ("count package-manager installs (`uv add pytest` records a GREEN)",
     "return exe in PACKAGE_MANAGERS and sub in NOT_A_RUN_SUBCOMMANDS",
     "return False"),
    ("count `python -m pip` (an install records a GREEN)",
     'and words[2].lower() == "pip":',
     'and words[2].lower() == "never":'),
    ("judge a NAME=value prefix as the executable",
     'or re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0])):',
     'or False):'),
    ("keep the .exe on the executable (a Windows path to cat counts)",
     "            exe = exe[:-len(ext)]",
     "            pass"),
    ("write the log in the locale's encoding (a non-cp1252 path kills the guard "
     "before its deny)",
     'with open(LOG, "a", encoding="utf-8") as f:',
     'with open(LOG, "a") as f:'),
    ("drop the always-on graph-directory exemption",
     "if match_any(rel, ALWAYS_EXEMPT) or match_any(rel, GUARD_EXEMPT_PATTERN):",
     "if match_any(rel, GUARD_EXEMPT_PATTERN):"),
    ("ignore the project's exempt pattern",
     "if match_any(rel, ALWAYS_EXEMPT) or match_any(rel, GUARD_EXEMPT_PATTERN):",
     "if match_any(rel, ALWAYS_EXEMPT):"),
    ("guard nothing in silence when the git dir cannot be resolved at stop",
     """if not re.search(r'"stop_hook_active"\\s*:\\s*true', raw):""",
     'if False:'),
]


def main():
    src = io.open(TPL, encoding="utf-8").read()

    names = []
    failures = guarded("unit pass", [], unit, src, counter=names)
    print("unit pass: %d/%d cases green" % (len(names) - len(failures), len(names)))
    if failures:
        print("FAILED unit cases:")
        for f in failures:
            print("  " + f)
        return 1

    # Each mutation needs ONE failing case, and the mutations are independent - each
    # unit() run is its own temp bench. They used to run one at a time and every case
    # to the end, so each paid the whole corpus and its mtime sleeps after the verdict
    # was settled. Now each stops at its first failing case and they run concurrently;
    # nothing here is timed. TDDGUARD_JOBS=1 runs them serially.
    jobs = max(1, int(os.environ.get("TDDGUARD_JOBS", "8")))
    print("mutation pass: %d at a time, first failing case named" % jobs)
    survived = []
    stale = []
    live = []
    for label, old, new in MUTATIONS:
        if old not in src:
            # Reported, never raised: an assert here aborts the run, so one drifted
            # anchor takes every mutation after it with it. A stale mutation is a
            # defect class that has silently lost its coverage, not a pass - the
            # sibling suites already report it this way (close-out-check.py).
            stale.append(label)
            print("STALE    %s - anchor no longer applies, re-point it" % label)
            continue
        live.append((label, src.replace(old, new, 1)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = [pool.submit(guarded, "mutation: %s" % label, [], unit, mutated,
                               verbose=False, first_only=True)
                   for label, mutated in live]
        for (label, _), fut in zip(live, futures):
            caught = fut.result()
            if caught:
                print("caught   %s" % label)
                print("           (by: %s)" % "; ".join(caught[:3]), flush=True)
            else:
                survived.append(label)
                print("SURVIVED %s" % label, flush=True)
    print()
    if stale:
        print("STALE: %d mutation anchor(s) need re-pointing" % len(stale))
    if guarded.crashed:
        print("CRASHED passes: %s" % ", ".join(guarded.crashed))
    if survived:
        print("FAILED: %d mutation(s) survived the suite" % len(survived))
    if survived or stale or guarded.crashed:
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
