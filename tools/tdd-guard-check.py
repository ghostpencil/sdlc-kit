#!/usr/bin/env python
"""Re-runnable proof for templates/tdd-guard.template.sh.

Two passes, and the second is the point:

  1. a unit pass driving every state transition of both guards, using payload shapes
     measured on the bench (FEATURE_PLAN.md 31.7) rather than invented ones;
  2. a mutation pass that breaks the guard thirteen ways and requires the unit pass to
     notice each one. A suite that survives its own mutations is not testing the thing
     it claims to (invariant 13).

Kit-development artifact: lives at the root, never ships inside sdlc-kit/ (invariant 12).
Run from anywhere:  python tools/tdd-guard-check.py
"""
import io, json, os, shutil, subprocess, sys, tempfile, time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(REPO, "sdlc-kit", "templates", "tdd-guard.template.sh")
JTPL = os.path.join(REPO, "sdlc-kit", "templates", "tdd-guard.template.json")


def _dir_of(exe):
    p = shutil.which(exe)
    return os.path.dirname(p) if p else None


# The guard picks its JSON parser at run time, so the suite has to run under a PATH that
# offers exactly one of them - otherwise whichever is found first is the only dialect
# ever tested, and the other ships unproven.
SHELL_DIR = _dir_of("sh")
PARSER_DIRS = {"python": _dir_of("python") or _dir_of("python3"), "node": _dir_of("node")}


def parser_path(name):
    """PATH exposing the shell utilities plus exactly one JSON parser."""
    parts = [d for d in (SHELL_DIR, PARSER_DIRS.get(name)) if d]
    return os.pathsep.join(parts)

# Instantiated for a Python project, using the recipe's own per-language row.
VALUES = {
    "{{TEST_PATH_PATTERN}}": "tests/*|test_*.py|*_test.py",
    "{{SOURCE_GLOB}}": "*.py",
    "{{TEST_CMD_PATTERN}}": "*pytest*",
}
SID = "session-one"


class Bench:
    path = None  # when set, the PATH every guard invocation runs under

    def __init__(self, base, guard_src):
        self.root = os.path.join(base, "proj")
        self.state = os.path.join(self.root, ".git", "sdlc-tdd")
        self.guard = os.path.join(self.root, ".github", "hooks", "sdlc-tdd-guard.sh")
        os.makedirs(os.path.dirname(self.guard))
        os.makedirs(self.state)
        body = guard_src
        for k, v in VALUES.items():
            body = body.replace(k, v)
        assert "{{" not in body, "unresolved placeholder in instantiated guard"
        io.open(self.guard, "w", encoding="utf-8", newline="\n").write(body)

    def run(self, mode, payload, env=None):
        e = dict(os.environ)
        e["SDLC_REPO_ROOT"] = self.root
        if self.path:
            e["PATH"] = self.path
        if env:
            e.update(env)
        p = subprocess.run(["sh", self.guard, mode], input=json.dumps(payload).encode(),
                           capture_output=True, env=e)
        return p.stdout.decode("utf-8", "replace").strip()

    def loglines(self):
        f = os.path.join(self.state, "guard.log")
        if not os.path.exists(f):
            return []
        return [l for l in io.open(f, encoding="utf-8").read().splitlines() if l.strip()]

    def tail(self):
        ls = self.loglines()
        return ls[-1] if ls else ""

    def reset_state(self):
        shutil.rmtree(self.state)
        os.makedirs(self.state)

    def arm_deny(self):
        io.open(os.path.join(self.state, "deny-enabled"), "w").write("")


def write(root, paths, sid=SID):
    patch = "*** Begin Patch\n" + "".join(
        "*** %s File: %s\n+x\n" % (k, p) for k, p in paths) + "*** End Patch\n"
    return {"sessionId": sid, "cwd": root, "toolName": "apply_patch", "toolArgs": patch}


def shell(root, cmd, code, sid=SID):
    # Exit status arrives as a text trailer, not a structured field - measured, 31.7.1.
    return {"sessionId": sid, "cwd": root, "toolName": "powershell",
            "toolArgs": json.dumps({"command": cmd}),
            "toolResult": {"resultType": "success",
                           "textResultForLlm":
                               "output...\n<shellId: 0 completed with exit code %d>" % code}}


def stop(root, active=False, sid=SID):
    d = {"sessionId": sid, "cwd": root, "stopReason": "end_turn"}
    if active:
        d["stop_hook_active"] = True
    return d


def unit(guard_src, verbose=True, counter=None, parser=None):
    """Returns the list of failed case names; counts every case into `counter`.

    `parser` restricts PATH to one JSON dialect ("python" or "node"); None takes
    whatever the ambient PATH offers.
    """
    base = tempfile.mkdtemp(prefix="tddguard-")
    try:
        b = Bench(base, guard_src)
        if parser:
            b.path = parser_path(parser)
        R = b.root
        failed = []

        def check(name, cond, detail=""):
            if counter is not None:
                counter.append(name)
            if not cond:
                failed.append(name)
            if verbose:
                print(("PASS  " if cond else "FAIL  ") + name +
                      (("\n        " + detail) if not cond else ""))

        # G1: the write guard
        out = b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("1  prod write, no red -> VIOLATION", "VIOLATION" in b.tail(), b.tail())
        check("1b logging mode denies nothing", out == "", repr(out))

        # An exempt file must log NOTHING - asserted on new lines, because re-reading
        # the last line cannot tell silence from the previous case's violation.
        before = len(b.loglines())
        b.run("pre-write", write(R, [("Update", "README.md")]))
        check("2  non-source file -> silent",
              not any("VIOLATION" in l for l in b.loglines()[before:]))

        b.run("pre-write", write(R, [("Add", "tests/test_payments.py")]))
        check("3  test edit recorded", "test edit recorded" in b.tail(), b.tail())

        # The D3 defect: a compound's exit code is not the test's.
        out = b.run("observe-test", shell(R, "python -m pytest; echo done", 0))
        check("4  compound command NOT counted", "NOT counted" in b.tail(), b.tail())
        check("4b no false GREEN from a compound",
              not os.path.exists(os.path.join(b.state, "green-observed")))
        # The field defect (2026-08-08): a silent refusal left the session thrashing
        # and probing the guard instead of complying. The refusal must be spoken.
        j = json.loads(out) if out.startswith("{") else {}
        check("4c compound refusal is spoken, not silent",
              "NOT counted" in (j.get("additionalContext") or ""), repr(out))
        check("4d and says what IS allowed, not only what is not",
              "selectors are fine" in (j.get("additionalContext") or ""), repr(out))
        # The 0.18.0 list caught only the doubled forms (&&, ||): a single '&' slipped
        # it. The field's `cmd /c "... & ..."` probe was refused by the ';' inside its
        # expanded PATH value - luck, not design (sdlc-kit#5 triage, 2026-08-08).
        b.run("observe-test", shell(R, "python -m pytest & echo done", 0))
        check("4e single-'&' compound NOT counted (doubled-only was the 0.18.0 gap)",
              "NOT counted" in b.tail(), b.tail())
        check("4f no false GREEN from a single-'&' compound",
              not os.path.exists(os.path.join(b.state, "green-observed")))

        time.sleep(1.1)  # mtime ordering is 1s-granular on some filesystems
        out = b.run("observe-test", shell(R, "python -m pytest", 1))
        check("5  red observed", "RED observed (exit 1)" in b.tail(), b.tail())
        check("5b a counted run stays silent (no context noise on the happy path)",
              out == "", repr(out))

        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("6  prod write after red -> OK", "OK production write" in b.tail(), b.tail())

        b.run("observe-test", shell(R, "python -m pytest", 0))
        check("7  green observed", "GREEN observed" in b.tail(), b.tail())

        # G2: the stop guard
        out = b.run("stop-check", stop(R))
        check("8  stop clean after green", "stop: clean" in b.tail(), b.tail())
        check("8b stop clean blocks nothing", out == "", repr(out))

        time.sleep(1.1)
        b.run("pre-write", write(R, [("Update", "tests/test_payments.py")]))
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("9  a test edit makes the red stale -> VIOLATION",
              "VIOLATION" in b.tail(), b.tail())

        time.sleep(1.1)
        b.run("observe-test", shell(R, "python -m pytest", 2))
        b.run("stop-check", stop(R))
        check("10 stop would-block while latest run is red",
              "WOULD-BLOCK" in b.tail(), b.tail())

        b.run("stop-check", stop(R, active=True))
        check("11 stands down on stop_hook_active", "standing down" in b.tail(), b.tail())

        # The `.\`-prefixed form the deny ramp found invisible to the bench pattern.
        b.reset_state()
        b.run("observe-test", shell(R, r"python -m pytest .\tests\test_x.py", 1))
        check("12 `.\\`-prefixed test path still counted", "RED observed" in b.tail(), b.tail())

        # Deny mode: the schemas measured on the bench, not the ones in the docs.
        b.reset_state(); b.arm_deny()
        out = b.run("pre-write", write(R, [("Update", "payments.py")]))
        j = json.loads(out) if out.startswith("{") else {}
        check("13 deny emits the measured preToolUse schema",
              j.get("permissionDecision") == "deny" and bool(j.get("permissionDecisionReason")),
              repr(out))

        out = b.run("stop-check", stop(R))
        j = json.loads(out) if out.startswith("{") else {}
        check("14 block emits the measured agentStop schema",
              j.get("decision") == "block" and bool(j.get("reason")), repr(out))

        out = b.run("stop-check", stop(R, active=True))
        check("15 deny mode still stands down on stop_hook_active", out == "", repr(out))

        # Observations are session-scoped. The first session's state must be FULLY
        # licensing (test edit, then a newer red) or this case cannot tell the reset
        # from G1's own test-edit requirement - the fixed G1 refuses a bare leaked red
        # anyway, which is how the reset mutation went invisible on the first re-run.
        b.reset_state()
        b.run("pre-write", write(R, [("Add", "tests/test_payments.py")]))
        time.sleep(1.1)
        b.run("observe-test", shell(R, "python -m pytest", 1))
        b.run("pre-write", write(R, [("Update", "payments.py")], sid="session-two"))
        check("16 a new session clears the earlier red -> VIOLATION",
              "VIOLATION" in b.tail(), b.tail())

        # Criterion D5: the guard's own failure must never become a denial.
        b.reset_state(); b.arm_deny()
        out = b.run("pre-write", write(R, [("Update", "payments.py")]),
                    env={"PATH": "/nonexistent"})
        check("17 guard cannot parse -> does NOT deny", out == "", repr(out))
        check("17b and says so loudly in the log", "GUARD ERROR" in b.tail(), b.tail())
        check("17c and names the missing dependency, not just 'error'",
              "python or node" in b.tail(), b.tail())

        b.reset_state()
        b.run("pre-write", {"sessionId": SID, "cwd": R, "toolName": "apply_patch",
                            "toolArgs": "*** Begin Patch\n*** Delete File: payments.py\n"
                                        "*** End Patch\n"})
        check("18 delete-only patch -> nothing to guard", "VIOLATION" not in b.tail(), b.tail())

        # A path with a space is one path, not two.
        b.reset_state()
        b.run("pre-write", write(R, [("Update", "src/my module.py")]))
        check("19 path containing a space stays one path",
              "VIOLATION" in b.tail() and "my module.py" in b.tail(), b.tail())

        # ...and it must not be half-swallowed as a test file either.
        b.reset_state()
        b.run("pre-write", write(R, [("Update", "tests/my helper.py")]))
        check("19b spaced test path classifies as a test edit",
              "test edit recorded" in b.tail(), b.tail())

        # The field circumvention (FEATURE_PLAN.md 31.18): a red manufactured with no
        # test edit this session - a test-shaped command that exits non-zero because
        # nothing matched - must license nothing. "You changed a test, then watched it
        # fail" needs both halves.
        b.reset_state()
        b.run("observe-test", shell(R, "python -m pytest tests/test_nope.py", 1))
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("20 a red with no test edit this session licenses nothing",
              "VIOLATION" in b.tail(), b.tail())

        # The hook-config prelude (FEATURE_PLAN.md 38.3): the WSL launcher route
        # re-parses the hook command line, corrupting backslashes and returning empty
        # for $(cat), so the JSON bodies must contain nothing that boundary can eat -
        # and must still deliver the payload into the script from a repo-root cwd.
        jtpl = json.load(io.open(JTPL, encoding="utf-8"))
        bodies = [h["bash"] for hs in jtpl["hooks"].values() for h in hs]
        check("21 every hook-config body survives the WSL launcher boundary "
              "(no backslash, no $, no quotes)",
              bool(bodies) and all(not any(ch in bd for ch in "\\$'\"") for bd in bodies),
              " | ".join(bodies))

        pre_body = jtpl["hooks"]["preToolUse"][0]["bash"]
        e = dict(os.environ)
        e.pop("SDLC_REPO_ROOT", None)
        if b.path:
            e["PATH"] = b.path
        b.reset_state()
        subprocess.run(["sh", "-c", pre_body],
                       input=json.dumps(write(R, [("Update", "payments.py")])).encode(),
                       capture_output=True, env=e, cwd=R)
        check("22 prelude at repo root pipes the payload into the guard",
              "VIOLATION" in b.tail(), b.tail())

        elsewhere = tempfile.mkdtemp(prefix="tddguard-elsewhere-")
        try:
            before = len(b.loglines())
            p = subprocess.run(["sh", "-c", pre_body],
                               input=json.dumps(write(R, [("Update", "payments.py")])).encode(),
                               capture_output=True, env=e, cwd=elsewhere)
            check("23 prelude away from a repo root: silent, no deny, no state",
                  p.stdout.decode().strip() == "" and len(b.loglines()) == before
                  and not os.path.exists(os.path.join(elsewhere, ".git")),
                  repr(p.stdout.decode()))

            # The script's own half of the same contract, without the prelude.
            b.reset_state()
            subprocess.run(["sh", b.guard, "pre-write"],
                           input=json.dumps(write(R, [("Update", "payments.py")])).encode(),
                           capture_output=True, env=e, cwd=R)
            check("24 script with no SDLC_REPO_ROOT trusts a repo-root cwd",
                  "VIOLATION" in b.tail(), b.tail())

            p = subprocess.run(["sh", b.guard, "pre-write"],
                               input=json.dumps(write(R, [("Update", "payments.py")])).encode(),
                               capture_output=True, env=e, cwd=elsewhere)
            check("25 script with no root and no .git at cwd is a no-op",
                  p.stdout.decode().strip() == ""
                  and not os.path.exists(os.path.join(elsewhere, ".git")),
                  repr(p.stdout.decode()))
        finally:
            shutil.rmtree(elsewhere, ignore_errors=True)

        # The other refusal shape: a test-pattern command whose payload carries no
        # exit-code trailer. Same rule as the compound case - spoken, never silent -
        # because a format drift in the trailer would otherwise mute the guard on
        # every run while its log looked merely quiet.
        b.reset_state()
        out = b.run("observe-test",
                    {"sessionId": SID, "cwd": R, "toolName": "powershell",
                     "toolArgs": json.dumps({"command": "python -m pytest"}),
                     "toolResult": {"resultType": "success",
                                    "textResultForLlm": "output with no trailer"}})
        j = json.loads(out) if out.startswith("{") else {}
        check("26 missing exit-code trailer is spoken, not silent",
              "no exit-code trailer" in b.tail()
              and "could not be counted" in (j.get("additionalContext") or ""),
              b.tail() + " | " + repr(out))

        # The refactor license (2026-08-08 field): G1's second license - a declared
        # behavior-preserving edit behind an observed green. Armed close-out passes
        # (change-simplify, mutation testing) forced synthetic test-edit/red cycles or
        # suppressed legitimate quality moves without it.
        b.reset_state()
        # Plant the session marker first: reset_state also removes it, and the guard's
        # own new-session clear would otherwise delete the license before the case
        # runs - which is the session-scoping case 31 proves, not this one.
        io.open(os.path.join(b.state, "session"), "w").write(SID)
        io.open(os.path.join(b.state, "refactor-license"), "w").write(
            "change-simplify: drop the isNew flag\n")
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("27 a refactor license without a green licenses nothing",
              "VIOLATION" in b.tail(), b.tail())

        b.run("observe-test", shell(R, "python -m pytest", 0))
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("28 license + observed green -> OK, declared reason logged",
              "refactor license: change-simplify: drop the isNew flag" in b.tail(),
              b.tail())

        # The mutation-testing shape: an expected red (the mutant caught) must not
        # strand the revert - only a test edit or a new session ends the license.
        b.run("observe-test", shell(R, "python -m pytest", 1))
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("29 license survives a red (mutation revert stays licensed)",
              "OK production write (refactor license" in b.tail(), b.tail())

        b.run("pre-write", write(R, [("Update", "tests/test_payments.py")]))
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("30 a test edit revokes the license -> VIOLATION",
              "VIOLATION" in b.tail(), b.tail())
        check("30b and the revocation is logged",
              any("refactor license revoked" in l for l in b.loglines()))

        b.reset_state()
        io.open(os.path.join(b.state, "refactor-license"), "w").write("left over\n")
        b.run("observe-test", shell(R, "python -m pytest", 0, sid="session-lic"))
        b.run("pre-write", write(R, [("Update", "payments.py")], sid="session-lic"))
        check("31 a license left by an earlier session licenses nothing",
              "VIOLATION" in b.tail(), b.tail())

        b.reset_state(); b.arm_deny()
        out = b.run("pre-write", write(R, [("Update", "payments.py")]))
        j = json.loads(out) if out.startswith("{") else {}
        check("32 the deny message names both ways out (red cycle and refactor license)",
              "refactor-license" in (j.get("permissionDecisionReason") or ""), repr(out))

        return failed
    finally:
        shutil.rmtree(base, ignore_errors=True)


MUTATIONS = [
    ("drop the compound-command check (reintroduces the D3 false-GREEN defect)",
     lambda s: s.replace('*";"*|*"&"*|*"|"*)', '*"@@never@@"*)')),
    ("regress the separator list to the doubled-only 0.18.0 forms (a single '&' "
     "slips through again)",
     lambda s: s.replace('*";"*|*"&"*|*"|"*)', '*";"*|*"&&"*|*"||"*|*"|"*)')),
    ("drop the session reset (observations leak across sessions)",
     lambda s: s.replace(
         'if [ -n "$SID" ] && [ "$SID" != "$(cat "$S/session" 2>/dev/null)" ]; then',
         'if false; then')),
    ("deny on the guard's own parse failure (violates criterion D5)",
     lambda s: s.replace(
         '  exit 0\nfi\n\nSID=$(printf',
         '  printf \'%s\\n\' \'{"permissionDecision":"deny",'
         '"permissionDecisionReason":"guard error"}\'\n  exit 0\nfi\n\nSID=$(printf')),
    ("classify by source glob before test pattern (the defect ENF.2 predicted)",
     lambda s: s.replace(
         'case "$n" in {{TEST_PATH_PATTERN}}) test_touched=1; continue ;; esac',
         'case "$b" in {{SOURCE_GLOB}}) prod="$prod $p"; continue ;; esac')),
    ("never stand down on stop_hook_active (fights the documented block cap)",
     lambda s: s.replace('if [ "$ACTIVE" = "true" ]; then', 'if false; then')),
    ("word-split the path list (a path with a space becomes two paths)",
     lambda s: s.replace("while IFS= read -r p; do", "for p in $PATHS; do")
                .replace("    done <<PATHLIST\n$PATHS\nPATHLIST", "    done")),
    ("drop the test-edit requirement (reintroduces the G1 hole 31.18 found in the field)",
     lambda s: s.replace(
         '[ -f "$S/red-observed" ] && [ -f "$S/last-test-edit" ] && '
         '[ "$S/red-observed" -nt "$S/last-test-edit" ]',
         '[ -f "$S/red-observed" ]')),
    ("trust any cwd when SDLC_REPO_ROOT is unset (state written to unrelated dirs)",
     lambda s: s.replace('  [ -d .git ] || exit 0\n', '')),
    ("re-silence the compound refusal (the 2026-08-08 field defect: the session "
     "thrashes and probes instead of complying)",
     lambda s: s.replace('        emit_context "TDD ordering: that test run was NOT counted',
                         '        : "TDD ordering: that test run was NOT counted')),
    ("drop the green requirement from the refactor license (a bare declaration "
     "licenses with no gate behind it)",
     lambda s: s.replace('[ -f "$S/refactor-license" ] && [ -f "$S/green-observed" ]',
                         '[ -f "$S/refactor-license" ]')),
    ("never revoke the refactor license on a test edit (the window outlives the "
     "cycle it was declared for)",
     lambda s: s.replace('        rm -f "$S/refactor-license" 2>/dev/null\n', '')),
    ("leak the refactor license across sessions (survives the new-session clear)",
     lambda s: s.replace(
         'rm -f "$S/red-observed" "$S/green-observed" "$S/last-test-edit" '
         '"$S/refactor-license" 2>/dev/null',
         'rm -f "$S/red-observed" "$S/green-observed" "$S/last-test-edit" 2>/dev/null')),
]


def main():
    src = io.open(TPL, encoding="utf-8", newline="").read()

    rc = 0

    # The guard ships two parser dialects and picks one at run time. Both get the whole
    # suite: a dialect that is never exercised is a dialect that is not proven, and the
    # two must agree case for case or they have drifted.
    for name in ("python", "node"):
        if not PARSER_DIRS.get(name):
            print("=== unit pass [%s] === SKIPPED - not installed on this machine, so "
                  "this dialect is UNPROVEN here\n" % name)
            rc = 1
            continue
        print("=== unit pass [%s] ===" % name)
        ran = []
        failed = unit(src, counter=ran, parser=name)
        print("\n%d cases, %s\n" % (
            len(ran), "all passed" if not failed else "FAILED: " + "; ".join(failed)))
        if failed:
            rc = 1

    # Mutations exercise the guard's shell logic, which sits above the parser choice, so
    # they run once under the ambient PATH rather than once per dialect.
    print("=== mutation pass (%d mutations; the unit suite must catch each) ==="
          % len(MUTATIONS))
    for name, fn in MUTATIONS:
        mutated = fn(src)
        if mutated == src:
            print("STALE    mutation no longer applies - update it: " + name)
            rc = 1
            continue
        caught = unit(mutated, verbose=False)
        if caught:
            print("caught   %s\n           (by: %s)" % (name, "; ".join(caught)))
        else:
            print("SURVIVED %s  <-- the suite is blind to this" % name)
            rc = 1

    print("\n%s" % ("OK" if rc == 0 else "PROBLEMS ABOVE"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
