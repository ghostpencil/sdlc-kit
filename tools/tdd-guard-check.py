#!/usr/bin/env python
"""Re-runnable proof for templates/tdd-guard.template.sh.

Two passes, and the second is the point:

  1. a unit pass driving every state transition of both guards, using payload shapes
     measured on the bench (FEATURE_PLAN.md 31.7) rather than invented ones;
  2. a mutation pass that breaks the guard — one mutation per known regression, the
     count derived from the MUTATIONS list at run time, never stated here (a hardcoded
     count is the part that goes stale) — and requires the unit pass to notice each
     one. A suite that survives its own mutations is not testing the thing it claims
     to (invariant 13).

Kit-development artifact: lives at the root, never ships inside sdlc-kit/ (invariant 12).
Run from anywhere:  python tools/tdd-guard-check.py
"""
import concurrent.futures, io, json, os, shutil, subprocess, sys, tempfile, time, traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(REPO, "sdlc-kit", "templates", "tdd-guard.template.sh")
JTPL = os.path.join(REPO, "sdlc-kit", "templates", "tdd-guard.template.json")
COSMETIC = os.path.join(REPO, "sdlc-kit", "templates", "sdlc-cosmetic.template.py")
RECIPES = os.path.join(REPO, "sdlc-kit", "reference", "GATE_RECIPES.md")


def recipe_pattern_rows():
    """The recipe's per-language (TEST_PATH_PATTERN, TEST_CMD_PATTERN) table, as setup
    reads it: every row whose two pattern cells are code spans, markdown's `\\|` unescaped."""
    rows, inside = [], False
    for line in io.open(RECIPES, encoding="utf-8"):
        if line.startswith("| Language | `{{TEST_PATH_PATTERN}}`"):
            inside = True
            continue
        if inside and not line.startswith("|"):
            break
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        if inside and len(cells) == 3 and cells[1].startswith("`"):
            rows.append([cells[0]] + [c.strip("`").replace("\\|", "|") for c in cells[1:]])
    return rows


def sh_parses(guard_src, tpp, tcp, where, exempt="tools/*"):
    """Instantiate the guard with these patterns and ask sh -n whether it parses."""
    body = guard_src
    for k, v in (("{{TEST_PATH_PATTERN}}", tpp), ("{{TEST_CMD_PATTERN}}", tcp),
                 ("{{SOURCE_GLOB}}", "*.x"), ("{{GUARD_EXEMPT_PATTERN}}", exempt),
                 ("{{TEST_REPORT_PATTERN}}", "FAIL")):
        body = body.replace(k, v)
    f = os.path.join(where, "parse-probe.sh")
    io.open(f, "w", encoding="utf-8", newline="\n").write(body)
    return subprocess.run([shutil.which("sh") or "sh", "-n", f], stdin=subprocess.DEVNULL,
                          capture_output=True).returncode == 0


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
    "{{TEST_REPORT_PATTERN}}": "=+ (FAILURES|ERRORS) =+",
    "{{GUARD_EXEMPT_PATTERN}}": "tools/*|*.config.*",
}
SID = "session-one"
# pytest's own report header (FEATURE_PLAN.md 84.8).
REPORT = "=================================== FAILURES ===================================\n"


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

    def reset_state(self):
        shutil.rmtree(self.state)
        os.makedirs(self.state)

    def arm_deny(self):
        io.open(os.path.join(self.state, "deny-enabled"), "w").write("")


def write(root, paths, sid=SID):
    patch = "*** Begin Patch\n" + "".join(
        "*** %s File: %s\n+x\n" % (k, p) for k, p in paths) + "*** End Patch\n"
    return {"sessionId": sid, "cwd": root, "toolName": "apply_patch", "toolArgs": patch}


def shell(root, cmd, code, sid=SID, text=None):
    # Exit status arrives as a text trailer, not a structured field - measured, 31.7.1.
    # A failing run carries pytest's own report header, as Copilot delivers it (84.8);
    # `text` replaces the output to fake anything else.
    if text is None:
        text = (REPORT + "output...") if code else "output..."
    return {"sessionId": sid, "cwd": root, "toolName": "powershell",
            "toolArgs": json.dumps({"command": cmd}),
            "toolResult": {"resultType": "success",
                           "textResultForLlm":
                               "%s\n<shellId: 0 completed with exit code %d>" % (text, code)}}


def stop(root, active=False, sid=SID):
    d = {"sessionId": sid, "cwd": root, "stopReason": "end_turn"}
    if active:
        d["stop_hook_active"] = True
    return d


def reopen_git(root, mode, newline=None):
    """Rewrite a worktree's .git FILE. Windows git marks it hidden, and a hidden file
    cannot be opened for a truncating write there - so remove it, then create it."""
    p = os.path.join(root, ".git")
    if os.path.isfile(p):
        os.remove(p)
    return io.open(p, mode, newline=newline)


class _FirstFailure(BaseException):
    """Ends a first_only run at its first failing check. BaseException, so neither
    a case's own handler nor guarded() can mistake it for a crash."""


def unit(guard_src, verbose=True, counter=None, parser=None, first_only=False):
    """Returns the list of failed case names; counts every case into `counter`.
    first_only ends the run at the first failing check - the mutation pass needs
    one, and the checks share one bench, so stopping only drops later checks.

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
                if first_only:
                    raise _FirstFailure()
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

        # Scope: a file outside the repository cannot be production source. This
        # dialect never reduced to a repo-relative path at all - it classified on the
        # full path and the basename, so an absolute path outside the root matched
        # the extension-only SOURCE_GLOB and was charged as production
        # (FIELD_REPORT_2026-08-17.md finding 3, measured in the Claude dialect;
        # this dialect reached the same end by a shorter route).
        outside = os.path.join(tempfile.gettempdir(), "sdlc-scratch", "mutate_s5.py")
        before = len(b.loglines())
        out = b.run("pre-write", write(R, [("Update", outside)]))
        check("2b absolute path outside the repo -> not production source",
              not any("VIOLATION" in l for l in b.loglines()[before:])
              and any("outside the repository" in l for l in b.loglines()[before:])
              and out == "", b.tail())

        # ...and the containment test must not become a hole.
        before = len(b.loglines())
        b.run("pre-write", write(R, [("Update", os.path.join(R, "payments.py"))]))
        check("2c absolute path INSIDE the repo is still production source",
              any("VIOLATION" in l for l in b.loglines()[before:]), b.tail())

        # The reduction also closes a live misclassification in this dialect: an
        # absolute path to a test file whose BASENAME does not look like a test
        # (tests/conftest.py) failed both TEST_PATH_PATTERN checks - `tests/*` cannot
        # match a full Windows path - and fell through to SOURCE_GLOB, so a test edit
        # was charged as a production write and licensed nothing.
        before = len(b.loglines())
        b.run("pre-write", write(R, [("Update", os.path.join(R, "tests", "conftest.py"))]))
        check("2d absolute path to tests/conftest.py is a test edit, not production",
              any("test edit recorded" in l for l in b.loglines()[before:])
              and not any("VIOLATION" in l for l in b.loglines()[before:]), b.tail())

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
        # FBK.2 (FEATURE_PLAN.md 44): counted observations are spoken as state facts.
        # Until 2026-08-09 this case pinned the opposite (counted runs silent) - the
        # same invisible-state shape the 2026-08-08 spoken-refusal fix closed for
        # refusals, pointed at the success side.
        j = json.loads(out) if out.startswith("{") else {}
        check("5b a counted RED is spoken and states the license it earned",
              "RED counted (exit 1)" in (j.get("additionalContext") or "")
              and "write is now licensed" in (j.get("additionalContext") or ""),
              repr(out))

        # The command, not its text (FIELD_REPORT_2026-08-17b.md finding 2).
        # TEST_CMD_PATTERN is substring-shaped, so matching it against the raw string
        # counted any command whose TEXT mentioned the runner - measured on a Java
        # adoption as a `git commit -m` quoting the RED command plus two appends
        # writing a RED record: three spurious notices in one phase, on a control
        # whose refusals have to be believed.
        before = len(b.loglines())
        out = b.run("observe-test",
                    shell(R, 'git commit -m "RED: python -m pytest exit 1"', 0))
        check("5c a runner named only inside a quoted argument counts nothing",
              b.loglines()[before:] == [] and out == "", b.tail())
        # The other direction: quoting an ARGUMENT must not hide a real run.
        b.run("observe-test", shell(R, 'python -m pytest -k "pay and not slow"', 1))
        check("5d a real run with a quoted argument still counts",
              "RED observed" in b.tail(), b.tail())

        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("6  prod write after red -> OK", "OK production write" in b.tail(), b.tail())

        out = b.run("observe-test", shell(R, "python -m pytest", 0))
        check("7  green observed", "GREEN observed" in b.tail(), b.tail())
        j = json.loads(out) if out.startswith("{") else {}
        check("7b a counted GREEN is spoken with the division-of-labor clause",
              "GREEN counted" in (j.get("additionalContext") or "")
              and "end-slice gate" in (j.get("additionalContext") or ""), repr(out))

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

        # G2 is session-scoped, and case 13's write was DENIED - the tree never
        # changed, so that write armed nothing (case 34 proves it). Arm the stop
        # guard the legitimate way before asking for the block schema.
        b.run("pre-write", write(R, [("Add", "tests/test_payments.py")]))
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
        out = b.run("observe-test", shell(R, "python -m pytest tests/test_nope.py", 1))
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("20 a red with no test edit this session licenses nothing",
              "VIOLATION" in b.tail(), b.tail())
        # The spoken observation must not claim a license the guard would refuse -
        # a red with no test edit is counted but licenses nothing, and the message
        # has to say exactly that or it is confidently wrong.
        j = json.loads(out) if out.startswith("{") else {}
        check("20b ...and its spoken observation says so, not 'licensed'",
              "licenses nothing" in (j.get("additionalContext") or "")
              and "write is now licensed" not in (j.get("additionalContext") or ""),
              repr(out))

        # The hook-config prelude (FEATURE_PLAN.md 38.3): the WSL launcher route
        # re-parses the hook command line, corrupting backslashes and returning empty
        # for $(cat), so the JSON bodies must contain nothing that boundary can eat -
        # and must still deliver the payload into the script from a repo-root cwd.
        jtpl = json.load(io.open(JTPL, encoding="utf-8"))
        bodies = [h["bash"] for hs in jtpl["hooks"].values() for h in hs]
        # Quotes were banned here as a precaution, never as a measurement; the
        # measured corruptions are backslashes, $(cat), and a $var defined in the body
        # (expanded to empty by the outer layer - 2026-09-27). D4's stop branch has to
        # print JSON, and a quoted body was measured surviving both launcher routes the
        # same day (FEATURE_PLAN.md 78.7), so the rule is now exactly what was measured.
        check("21 every hook-config body survives the WSL launcher boundary "
              "(no backslash, no $)",
              bool(bodies) and all(not any(ch in bd for ch in "\\$") for bd in bodies),
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

            # 24b is the case that mattered and did not exist: an ABSOLUTE in-repo
            # path with SDLC_REPO_ROOT UNSET - the configuration every real adopter
            # runs, since nothing sets that variable for them. Case 2c above covers
            # absolute-in-repo, but the bench PINS SDLC_REPO_ROOT to a
            # Python-flavoured root, so both sides agree by construction and the
            # comparison can never diverge. Unset, the guard falls back to `pwd`,
            # which on Windows answers `/c/foo` while the CLI reports `C:oo` -
            # different flavours, no prefix match, and every absolute path fell to
            # the "outside the repository" arm. The guard SKIPPED every write that
            # CLI reports by absolute path, which is how it reports them, and it
            # shipped that way in 0.25.0-0.28.0 (FEATURE_PLAN.md §72). A proof whose
            # only in-repo absolute case runs with the root pinned cannot see it.
            b.reset_state()
            subprocess.run(["sh", b.guard, "pre-write"],
                           input=json.dumps(write(R, [("Update", os.path.join(R, "payments.py"))])).encode(),
                           capture_output=True, env=e, cwd=R)
            check("24b absolute in-repo path is production with SDLC_REPO_ROOT unset",
                  "VIOLATION" in b.tail() and "outside the repository" not in b.tail(),
                  b.tail())

            # ...and the same path in the OTHER flavour the shell can report, so the
            # fix is pinned in both directions rather than for whichever one this
            # host happens to produce.
            alt = subprocess.run(["sh", "-c", "cd \"$1\" && pwd -W 2>/dev/null || pwd", "_", R],
                                 capture_output=True, text=True).stdout.strip()
            if alt:
                b.reset_state()
                subprocess.run(["sh", b.guard, "pre-write"],
                               input=json.dumps(write(R, [("Update", alt + "/payments.py")])).encode(),
                               capture_output=True, env=e, cwd=R)
                check("24c the same path in the shell's other flavour is also production",
                      "VIOLATION" in b.tail() and "outside the repository" not in b.tail(),
                      b.tail())

            # 24d: the WSL route (FEATURE_PLAN.md 78.7). Under WSL bash the root reads
            # /mnt/d/..., `pwd -W` is MSYS-only and prints nothing, and the CLI still
            # reports D:\... - so 0.28.1's two candidates matched neither and every
            # absolute write was "outside the repository". This host has no /mnt, so
            # the fixture lives under a temp .../mnt/<drive>/ and SDLC_WSL_MOUNT pins
            # the mount prefix there - the same kind of harness knob SDLC_REPO_ROOT is.
            wsl_base = tempfile.mkdtemp(prefix="tddguard-wsl-")
            try:
                wroot = os.path.join(wsl_base, "mnt", "q", "proj")
                os.makedirs(os.path.join(wroot, ".git"))
                posix = lambda d: subprocess.run(["sh", "-c", 'cd "$1" && pwd', "_", d],
                                                 capture_output=True, text=True).stdout.strip()
                we = dict(e)
                we["SDLC_REPO_ROOT"] = posix(wroot)
                we["SDLC_WSL_MOUNT"] = posix(os.path.join(wsl_base, "mnt"))
                subprocess.run(["sh", b.guard, "pre-write"],
                               input=json.dumps(write("Q:\\proj", [("Update", "Q:\\proj\\payments.py")])).encode(),
                               capture_output=True, env=we, cwd=wroot)
                wlog = os.path.join(wroot, ".git", "sdlc-tdd", "guard.log")
                wl = io.open(wlog, encoding="utf-8").read() if os.path.exists(wlog) else ""
                check("24d a drive-form path is production under a WSL-mount root",
                      "VIOLATION" in wl and "outside the repository" not in wl, wl)

                # 24e: a WORKTREE under the WSL mount, deny armed. The refusal tells the
                # agent where to declare a licence, and the agent writes it with its own
                # tools, which take drive paths - so the mount form must not leak into
                # that instruction (measured live: it named /mnt/d/..., 2026-09-27).
                wt2 = os.path.join(wsl_base, "mnt", "q", "wtproj")
                gd2 = os.path.join(wsl_base, "mnt", "q", "gd", "worktrees", "wt")
                os.makedirs(wt2)
                os.makedirs(os.path.join(gd2, "sdlc-tdd"))
                io.open(os.path.join(gd2, "sdlc-tdd", "deny-enabled"), "w").write("")
                io.open(os.path.join(wt2, ".git"), "w", newline="\n").write(
                    "gitdir: %s\n" % posix(gd2))
                we2 = dict(we)
                we2["SDLC_REPO_ROOT"] = posix(wt2)
                p = subprocess.run(["sh", b.guard, "pre-write"],
                                   input=json.dumps(write("Q:\\wtproj", [("Update", "Q:\\wtproj\\payments.py")])).encode(),
                                   capture_output=True, env=we2, cwd=wt2)
                out = p.stdout.decode("utf-8", "replace")
                check("24e a worktree's refusal under WSL names the licence in DRIVE form",
                      "q:/gd/worktrees/wt/sdlc-tdd/refactor-license" in out
                      and "/mnt/" not in out, out)
            finally:
                shutil.rmtree(wsl_base, ignore_errors=True)

            p = subprocess.run(["sh", b.guard, "pre-write"],
                               input=json.dumps(write(R, [("Update", "payments.py")])).encode(),
                               capture_output=True, env=e, cwd=elsewhere)
            check("25 script with no root and no .git at cwd is a no-op",
                  p.stdout.decode().strip() == ""
                  and not os.path.exists(os.path.join(elsewhere, ".git")),
                  repr(p.stdout.decode()))
            # 25b: the same, at STOP. Since 0.31.1 a .git that names no git directory
            # blocks at stop ("did not run"), so the early no-.git exit is what keeps a
            # stop OUTSIDE any repository silent - without it the guard would block
            # every stop of a session that merely started somewhere else.
            p = subprocess.run(["sh", b.guard, "stop-check"],
                               input=json.dumps(stop(elsewhere)).encode(),
                               capture_output=True, env=e, cwd=elsewhere)
            check("25b ...and stop-check there is silent too - no block outside a repo",
                  p.stdout.decode().strip() == "", repr(p.stdout.decode()))
            # 25c: the harness contract. A PINNED SDLC_REPO_ROOT with no .git at all
            # still guards, state created under it - an adopter's own guard tests pin a
            # bare temp directory, and 0.31.1 made that guard nothing, silently. Every
            # other fixture here creates a .git, which is why the suite could not see it.
            bare = tempfile.mkdtemp(prefix="tddguard-bare-")
            try:
                be = dict(e)
                be["SDLC_REPO_ROOT"] = subprocess.run(["sh", "-c", 'cd "$1" && pwd', "_", bare],
                                                      capture_output=True, text=True).stdout.strip()
                subprocess.run(["sh", b.guard, "pre-write"],
                               input=json.dumps(write(bare, [("Update", "payments.py")])).encode(),
                               capture_output=True, env=be, cwd=bare)
                bl = os.path.join(bare, ".git", "sdlc-tdd", "guard.log")
                blog = io.open(bl, encoding="utf-8").read() if os.path.exists(bl) else ""
                check("25c a pinned root with NO .git still guards, state created under it",
                      "VIOLATION" in blog, blog)
            finally:
                shutil.rmtree(bare, ignore_errors=True)
        finally:
            shutil.rmtree(elsewhere, ignore_errors=True)

        # FEATURE_PLAN.md 78: the launcher tested `[ -d .git ]` from whatever directory
        # the CLI started the hook in, and read "not at the root" as "not a repo". Two
        # measured ways to be there: a session launched below the root (every Copilot
        # build 1.0.64-1.0.87 ran hooks in the session cwd), and a linked worktree,
        # where .git is a FILE on every build. The entry now carries "cwd": "." and the
        # script resolves the git directory through that file. These cases build a
        # REAL worktree with git, because a hand-made .git directory - which is what
        # the Bench above is - is exactly the configuration that cannot see the defect.
        check("21b every hook-config entry pins cwd to the repository root and none "
              "tests for a .git DIRECTORY",
              all(h.get("cwd") == "." and "-d .git" not in h["bash"]
                  for hs in jtpl["hooks"].values() for h in hs),
              json.dumps(jtpl["hooks"]))

        wt_base = tempfile.mkdtemp(prefix="tddguard-wt-")
        try:
            main_r = os.path.join(wt_base, "main")
            wt_r = os.path.join(wt_base, "wt")
            os.makedirs(main_r)
            g = lambda *a, **k: subprocess.run(["git"] + list(a), capture_output=True,
                                               text=True, **k)
            g("init", "-q", main_r)
            io.open(os.path.join(main_r, "README"), "w").write("x\n")
            g("-C", main_r, "add", "README")
            g("-C", main_r, "-c", "user.email=t@t", "-c", "user.name=t",
              "commit", "-q", "-m", "init")
            g("-C", main_r, "worktree", "add", "-q", wt_r, "-b", "wt")
            gd = g("-C", wt_r, "rev-parse", "--absolute-git-dir").stdout.strip()
            wt_state = os.path.join(gd, "sdlc-tdd")
            wt_guard = os.path.join(wt_r, ".github", "hooks", "sdlc-tdd-guard.sh")
            os.makedirs(os.path.dirname(wt_guard))
            shutil.copy(b.guard, wt_guard)
            check("36 fixture: the worktree's .git is a file naming its own git dir",
                  os.path.isfile(os.path.join(wt_r, ".git")) and os.path.isdir(gd),
                  gd)

            def wt_log():
                f = os.path.join(wt_state, "guard.log")
                return io.open(f, encoding="utf-8").read() if os.path.exists(f) else ""

            def wt_pre():
                shutil.rmtree(wt_state, ignore_errors=True)
                subprocess.run(["sh", "-c", pre_body],
                               input=json.dumps(write(wt_r, [("Update", "payments.py")])).encode(),
                               capture_output=True, env=e, cwd=wt_r)
                return wt_log()

            check("36a launcher at a worktree root runs the guard, state in the "
                  "worktree's own git dir",
                  "VIOLATION" in wt_pre()
                  and not os.path.exists(os.path.join(main_r, ".git", "sdlc-tdd")),
                  wt_log())

            # The creating git writes the gitdir in ITS flavour; the guard must not
            # need git to follow it (WSL's git cannot follow a Windows-written one -
            # measured 2026-09-27). Two other forms a .git file legitimately takes:
            rel = os.path.relpath(gd, wt_r).replace(os.sep, "/")
            reopen_git(wt_r, "w", newline="\n").write("gitdir: %s\n" % rel)
            check("36b ...and through a RELATIVE gitdir (worktree.useRelativePaths)",
                  "VIOLATION" in wt_pre(), wt_log())
            # 36f: a relative gitdir is relative to the ROOT, not to wherever the
            # process happens to stand. Only observable with the root pinned and the
            # cwd elsewhere - the harness's own configuration, so pin that too.
            shutil.rmtree(wt_state, ignore_errors=True)
            pe = dict(e)
            pe["SDLC_REPO_ROOT"] = subprocess.run(["sh", "-c", 'cd "$1" && pwd', "_", wt_r],
                                                  capture_output=True, text=True).stdout.strip()
            subprocess.run(["sh", wt_guard, "pre-write"],
                           input=json.dumps(write(wt_r, [("Update", "payments.py")])).encode(),
                           capture_output=True, env=pe, cwd=wt_base)
            check("36f a relative gitdir resolves against the root, not the cwd",
                  "VIOLATION" in wt_log(), wt_log())
            reopen_git(wt_r, "w", newline="\r\n").write(
                "gitdir: %s\n" % gd.replace("/", "\\"))
            check("36c ...and through a backslashed, CRLF-terminated gitdir",
                  "VIOLATION" in wt_pre(), wt_log())

            reopen_git(wt_r, "w", newline="\n").write(
                "gitdir: %s\n" % os.path.join(wt_base, "nowhere").replace(os.sep, "/"))
            shutil.rmtree(wt_state, ignore_errors=True)
            p = subprocess.run(["sh", wt_guard, "pre-write"],
                               input=json.dumps(write(wt_r, [("Update", "payments.py")])).encode(),
                               capture_output=True, env=e, cwd=wt_r)
            check("36d a .git file naming no git dir: pre-write is a silent no-op",
                  p.returncode == 0 and p.stdout.decode().strip() == ""
                  and not os.path.exists(os.path.join(wt_r, ".git", "sdlc-tdd")),
                  repr(p.stdout.decode()))
            p = subprocess.run(["sh", wt_guard, "stop-check"],
                               input=json.dumps(stop(wt_r)).encode(),
                               capture_output=True, env=e, cwd=wt_r)
            out = p.stdout.decode().strip()
            j = json.loads(out) if out.startswith("{") else {}
            check("36e ...and stop-check says so, by block, rather than guarding nothing "
                  "in silence",
                  j.get("decision") == "block" and "did not run" in (j.get("reason") or ""),
                  repr(out))
        finally:
            shutil.rmtree(wt_base, ignore_errors=True)

        # D4: a broken install - the JSON present, the script not - must reach someone.
        # Exit codes do not (measured: a non-zero exit lands in the session log only);
        # an agentStop block does. Pre and post stay silent: a deny there would stop
        # every write, and the stop hook of the same family reports the same fault.
        broken = tempfile.mkdtemp(prefix="tddguard-broken-")
        try:
            os.makedirs(os.path.join(broken, ".git"))
            stop_body = jtpl["hooks"]["agentStop"][0]["bash"]
            p = subprocess.run(["sh", "-c", stop_body], input=json.dumps(stop(broken)).encode(),
                               capture_output=True, env=e, cwd=broken)
            out = p.stdout.decode().strip()
            j = json.loads(out) if out.startswith("{") else {}
            check("37 stop launcher with the guard script missing blocks, naming the fault",
                  j.get("decision") == "block" and "did not run" in (j.get("reason") or ""),
                  repr(out))
            p = subprocess.run(["sh", "-c", stop_body],
                               input=json.dumps(stop(broken, active=True)).encode(),
                               capture_output=True, env=e, cwd=broken)
            check("37b ...and stands down on stop_hook_active (one block, not eight)",
                  p.stdout.decode().strip() == "", repr(p.stdout.decode()))
            # ...and the other direction, which nothing else runs: at a root that HAS
            # the script, the stop launcher must take the script branch. A typo in the
            # launcher's -f path would otherwise block every stop of every session, and
            # only the static shape check above would be looking - it cannot see that.
            p = subprocess.run(["sh", "-c", stop_body], input=json.dumps(stop(R)).encode(),
                               capture_output=True, env=e, cwd=R)
            check("37d stop launcher with the script present runs the guard, no block",
                  "did not run" not in p.stdout.decode("utf-8", "replace")
                  and "stop:" in b.tail(), repr(p.stdout.decode()) + " | " + b.tail())
            for ev in ("preToolUse", "postToolUse"):
                body = jtpl["hooks"][ev][0]["bash"]
                p = subprocess.run(["sh", "-c", body],
                                   input=json.dumps(write(broken, [("Update", "x.py")])).encode(),
                                   capture_output=True, env=e, cwd=broken)
                check("37c %s launcher with the script missing is silent and exits 0" % ev,
                      p.returncode == 0 and p.stdout.decode().strip() == "",
                      repr(p.stdout.decode()))
        finally:
            shutil.rmtree(broken, ignore_errors=True)

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

        # The close-out license (FIELD_REPORT_2026-09-01 finding 1): the same license
        # scoped to /end-slice, differing in exactly one way - a test edit does NOT
        # revoke it. Close-out's mandated order is review (fixes tests) -> mutation
        # (writes production, restores tests) -> verify (writes a harness), so a
        # license a test edit revokes cannot survive its own step; a real arc paid the
        # re-declaration seven times in one phase. The survivals are counted so a
        # license held open past its step is visible rather than silent.
        b.reset_state()
        io.open(os.path.join(b.state, "session"), "w").write(SID)
        io.open(os.path.join(b.state, "close-out-license"), "w").write(
            "end-slice: mutation check\n")
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("30c a close-out license without a green licenses nothing either",
              "VIOLATION" in b.tail(), b.tail())

        b.run("observe-test", shell(R, "python -m pytest", 0))
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("30d close-out license + green -> OK, logged as close-out",
              "OK production write (close-out license: end-slice: mutation check"
              in b.tail(), b.tail())

        b.run("pre-write", write(R, [("Update", "tests/test_payments.py")]))
        check("30e a test edit does NOT revoke it, and the survival is counted",
              os.path.exists(os.path.join(b.state, "close-out-license"))
              and any("close-out license SURVIVED a test edit (1 this session)" in l
                      for l in b.loglines()), b.tail())

        b.run("pre-write", write(R, [("Update", "tests/test_other.py")]))
        check("30f each surviving test edit increments the count",
              any("close-out license SURVIVED a test edit (2 this session)" in l
                  for l in b.loglines()), b.tail())

        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("30g the license still licenses a write after the test edits",
              "OK production write (close-out license" in b.tail(), b.tail())

        b.reset_state()
        io.open(os.path.join(b.state, "close-out-license"), "w").write("left over\n")
        io.open(os.path.join(b.state, "close-out-survivals"), "w").write("4")
        b.run("observe-test", shell(R, "python -m pytest", 0, sid="session-colic"))
        b.run("pre-write", write(R, [("Update", "payments.py")], sid="session-colic"))
        check("30h a close-out license left by an earlier session licenses nothing",
              "VIOLATION" in b.tail()
              and not os.path.exists(os.path.join(b.state, "close-out-survivals")),
              b.tail())

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
        # §48/§50.1: the behavior-preserving route is named by CASE and never
        # narrowed by a phase word. 0.31.0 adds a genuinely close-out-scoped second
        # license, so "close-out" may appear - but only AFTER the unqualified case
        # sentence, never as its qualifier. Same re-pointing as the Claude suite's 4b.
        _r = j.get("permissionDecisionReason") or ""
        check("32b the case sentence stays unqualified, and close-out is an addition",
              "BEHAVIOR-PRESERVING" in _r and "at any point in the cycle" in _r
              and "close-out-license" in _r
              and _r.index("at any point in the cycle") < _r.index("close-out"),
              repr(out))

        # G2 session scoping (owner-decided 2026-08-08): the stop guard binds only a
        # session that wrote production code or edited a test. A planning, docs, or
        # bookkeeping session runs no tests by design and must stop clean - deny mode
        # included, since logging mode masks exactly this class of false block.
        b.reset_state(); b.arm_deny()
        out = b.run("stop-check", stop(R))
        check("33 a session with no writes stops clean, deny mode included",
              out == "" and "nothing to guard" in b.tail(), b.tail() + " | " + repr(out))

        b.run("pre-write", write(R, [("Update", "README.md")]))
        out = b.run("stop-check", stop(R))
        check("33b a docs-only session stops clean",
              out == "" and "nothing to guard" in b.tail(), b.tail() + " | " + repr(out))

        b.run("pre-write", write(R, [("Update", "payments.py")]))  # denied above
        out = b.run("stop-check", stop(R))
        check("34 a denied production write arms nothing (the tree never changed)",
              out == "" and "nothing to guard" in b.tail(), b.tail() + " | " + repr(out))

        b.run("pre-write", write(R, [("Add", "tests/test_payments.py")]))
        out = b.run("stop-check", stop(R))
        j = json.loads(out) if out.startswith("{") else {}
        check("35 a test edit alone arms the stop guard (a test never run is a "
              "never-ran stop)",
              j.get("decision") == "block" and bool(j.get("reason")), repr(out))

        # COSMETIC (FEATURE_PLAN.md 82): a comment or format edit needs no red. Real
        # edit/create payloads against a real file, deny armed, the shipped classifier
        # beside the guard (tools/cosmetic-check.py proves it alone). It needs python:
        # under the node-only PATH the stated limit is today's rule, and is asserted.
        has_py = parser != "node"
        c = Bench(os.path.join(base, "cos"), guard_src)
        c.path = b.path
        hooks = os.path.dirname(c.guard)
        shutil.copy(COSMETIC, os.path.join(hooks, "sdlc-cosmetic.py"))
        body = "def pay(a, b):\n    # sum them\n    return a + b\n"
        CR = c.root

        def cedit(old, new, tool="edit", tail=""):
            io.open(os.path.join(CR, "payments.py"), "w", encoding="utf-8",
                    newline="").write(body + tail)
            a = {"path": os.path.join(CR, "payments.py")}
            if tool == "create":
                a["file_text"] = new
            else:
                a.update({"old_str": old, "new_str": new})
            return {"sessionId": SID, "cwd": CR, "toolName": tool,
                    "toolArgs": json.dumps(a)}

        def denied(out):
            return '"permissionDecision":"deny"' in out

        c.reset_state(); c.arm_deny()
        out = c.run("pre-write", cedit("# sum them", "# add them"))
        if has_py:
            check("C1 armed: a comment-only edit is allowed and logged as cosmetic",
                  out == "" and "OK production write (cosmetic: python-ast)" in c.tail()
                  and not os.path.exists(os.path.join(c.state, "prod-write-observed")),
                  c.tail() + " | " + repr(out))
            out = c.run("stop-check", stop(CR))
            check("C2 ...and leaves the stop guard unarmed",
                  out == "" and "nothing to guard" in c.tail(), c.tail())
            out = c.run("pre-write", cedit(None, body.replace("# sum them", "# add them"),
                                           tool="create"))
            check("C3 armed: a comment-only create is allowed",
                  out == "" and "cosmetic: python-ast" in c.tail(), c.tail())
        else:
            check("C1 node-only: no python, no exemption - today's rule (stated limit)",
                  denied(out), c.tail() + " | " + repr(out))
        out = c.run("pre-write", cedit("a + b", "a - b"))
        check("C4 armed: a real edit is denied exactly as today",
              denied(out) and not os.path.exists(os.path.join(c.state,
                                                              "prod-write-observed")),
              c.tail() + " | " + repr(out))
        if has_py:
            check("C4b ...and the log says why it was not exempt",
                  any("not cosmetic (python-ast: the syntax tree differs)" in l
                      for l in c.loglines()), c.tail())
        out = c.run("pre-write", cedit("# sum them", "# x", tail="# sum them\n"))
        check("C5 armed: an ambiguous old_str is denied (cannot tell)", denied(out),
              c.tail())
        out = c.run("pre-write", write(CR, [("Update", "payments.py")]))
        check("C6 apply_patch: exactly today's rule", denied(out)
              and "cosmetic:" not in c.tail(), c.tail())
        io.open(os.path.join(hooks, "sdlc-cosmetic.py"), "w").write(
            "raise RuntimeError('broken classifier')\n")
        out = c.run("pre-write", cedit("# sum them", "# add them"))
        check("C7 a crashing classifier: exit 0, denied under today's rule",
              c.rc == 0 and denied(out), "rc=%s %r" % (c.rc, out))
        os.remove(os.path.join(hooks, "sdlc-cosmetic.py"))
        out = c.run("pre-write", cedit("# sum them", "# add them"))
        check("C8 no classifier installed: today's rule", c.rc == 0 and denied(out),
              repr(out))
        shutil.copy(COSMETIC, os.path.join(hooks, "sdlc-cosmetic.py"))
        if has_py:
            c.reset_state()
            out = c.run("pre-write", cedit("# sum them", "# add them"))
            check("C9 logging mode: cosmetic is logged OK, not as a VIOLATION",
                  out == "" and "cosmetic: python-ast" in c.tail(), c.tail())
            c.reset_state()
            c.run("pre-write", write(CR, [("Update", "tests/test_payments.py")]))
            c.run("observe-test", shell(CR, "pytest -q", 1))
            n = len(c.loglines())
            c.run("pre-write", cedit("a + b", "a - b"))
            check("C10 a write already licensed never consults the classifier",
                  "red observed since last test edit" in c.tail()
                  and not any("cosmetic" in l for l in c.loglines()[n:]), c.tail())

        # R: a RED needs the runner's own report (FEATURE_PLAN.md 84, sdlc-kit#16). A
        # wrapper failing before the runner starts exits with a failed test's code.
        def ctx(out):
            try:
                return (json.loads(out) if out.startswith("{") else {}).get(
                    "additionalContext") or ""
            except ValueError:
                return ""

        def has(name):
            return os.path.exists(os.path.join(b.state, name))

        b.reset_state()
        b.run("pre-write", write(R, [("Update", "tests/test_payments.py")]))
        time.sleep(1.1)
        out = b.run("observe-test", shell(
            R, "python -m pytest tests/test_payments.py", 1,
            text="[ERR_PNPM_IGNORED_BUILDS] Ignored build scripts: esbuild\n"
                 "pnpm: Command failed with exit code 1"))
        check("R1 a failure with no runner report counts no RED, and says why",
              not has("red-observed") and "no test-runner report in the output" in b.tail()
              and "NOT counted as a RED" in ctx(out) and "re-run it quieter" in ctx(out),
              b.tail() + " | " + repr(out))
        b.run("pre-write", write(R, [("Update", "payments.py")]))
        check("R1b ...so the write after it is still a violation",
              "VIOLATION" in b.tail(), b.tail())

        b.reset_state()
        b.run("observe-test", shell(
            R, "python -m pytest", 2,
            text="=========================== ERRORS ===========================\n"
                 "Interrupted: 1 error during collection"))
        check("R2 a collection error (exit 2) counts as the RED it is",
              "RED observed (exit 2)" in b.tail(), b.tail())

        # Copilot replaces a very long output with a 500-character preview (84.8).
        b.reset_state()
        b.run("observe-test", shell(
            R, "python -m pytest -s", 1,
            text="Output too large to read at once (1.3 MB). Saved to: C:\\t\\o.txt\n"
                 "Preview (first 500 chars):\nfiller line ....\n"))
        check("R3 a report cut off by Copilot's preview counts no RED",
              not has("red-observed"), b.tail())

        b.reset_state()
        b.run("observe-test", shell(R, "python -m pytest", 1,
                                    text="\x1b[31m=====\x1b[0m FAILURES =====\r\nboom"))
        check("R4 the report is matched with ANSI codes and CRLF removed",
              has("red-observed"), b.tail())

        bad = Bench(os.path.join(base, "badpattern"),
                    guard_src.replace("{{TEST_REPORT_PATTERN}}", "([unclosed"))
        if b.path:
            bad.path = b.path
        bad.run("observe-test", shell(bad.root, "python -m pytest", 1))
        check("R5 an invalid report pattern: exit 0, no RED, a GUARD ERROR logged",
              bad.rc == 0 and not os.path.exists(os.path.join(bad.state, "red-observed"))
              and any("TEST_REPORT_PATTERN is not a valid" in l for l in bad.loglines()),
              repr(bad.loglines()[-2:]))

        # N: commands that name the runner without running it (84.4(1)). Their
        # SUCCESS was the worse defect: a GREEN with no test run at all.
        for c in ("cat pytest.ini", "grep pytest pyproject.toml",
                  "sed -n 1,5p pytest.ini", "git log --grep pytest",
                  "gh api repos/pytest-dev/pytest/releases/latest",
                  "Get-Content pytest.ini", "pip install pytest",
                  "python -m pip install pytest", "uv add --dev pytest",
                  "PYTHONPATH=. cat pytest.ini", r"C:\Git\usr\bin\cat.exe pytest.ini",
                  "git commit -F - <<'EOF'\nfeat: pay\n\nGREEN: pytest -q passes\nEOF",
                  "python scripts/note.py <<'EOF'\nGREEN: pytest -q passes\nEOF",
                  'python scripts/note.py "RED: pytest -q"'):
            b.reset_state()
            o1 = b.run("observe-test", shell(R, c, 0))
            o2 = b.run("observe-test", shell(R, c, 1))
            check("N1 %r counts neither GREEN nor RED, silently" % c,
                  not has("green-observed") and not has("red-observed")
                  and o1 == "" and o2 == ""
                  and not [l for l in b.loglines() if "new session" not in l],
                  repr(b.loglines()))

        for c in ("uv run pytest -q", "python -m pytest -q", "env CI=1 pytest -q",
                  r"C:\proj\.venv\Scripts\pytest.exe -q"):
            b.reset_state()
            b.run("observe-test", shell(R, c, 0))
            check("N2 a real run through %r still counts" % c, has("green-observed"),
                  b.tail())

        # X: the exempt pattern (84.7 ruling 6).
        b.reset_state()
        b.arm_deny()
        out = b.run("pre-write", write(R, [("Update", "tools/measure_recall.py")]))
        check("X1 a write under GUARD_EXEMPT_PATTERN is not denied, and is logged exempt",
              out == "" and not has("prod-write-observed")
              and "exempt from the guard" in b.tail(), b.tail() + " | " + repr(out))
        out = b.run("pre-write", write(R, [("Update", "playwright.config.py")]))
        check("X2 a config file is exempt the same way",
              out == "" and "exempt from the guard" in b.tail(), b.tail())
        out = b.run("pre-write", write(R, [("Update", ".ua/tmp/build_batch.py")]))
        check("X3 the graph tool's directory is exempt in every project",
              out == "" and "exempt from the guard" in b.tail(), b.tail())
        b.run("pre-write", write(R, [("Update", "tools/tests/test_measure.py")]))
        check("X4 a test under an exempt directory is not a test edit either",
              not has("last-test-edit"), b.tail())
        n = len(b.loglines())
        b.run("pre-write", write(R, [("Update", "tools/README.md")]))
        check("X5 an exempt non-source file stays silent", len(b.loglines()) == n,
              b.tail())
        out = b.run("pre-write", write(R, [("Update", "src/payments.py")]))
        check("X6 code outside the pattern is still guarded",
              '"permissionDecision":"deny"' in out, repr(out))
        out = b.run("pre-write", write(R, [("Update", os.path.join(R, "tools", "x.py"))]))
        check("X7 an absolute in-repo path is reduced before the exempt test",
              out == "" and "exempt from the guard" in b.tail() and b.tail().endswith(": tools/x.py"), b.tail())

        # E: the deny message's bytes survive (a text-mode read made mojibake, 84.8).
        b.reset_state()
        b.arm_deny()
        out = b.run("pre-write", write(R, [("Update", "src/café.py")]))
        try:
            reason = json.loads(out).get("permissionDecisionReason") or ""
        except ValueError:
            reason = ""
        check("E1 a non-ASCII path reaches the deny message intact", "café.py" in reason,
              repr(out[:200]))
        b.reset_state()
        b.arm_deny()
        out = b.run("pre-write", write(R, [("Update", "src/日本.py")]))
        try:
            reason = json.loads(out).get("permissionDecisionReason") or ""
        except ValueError:
            reason = ""
        check("E2 a path outside cp1252 is still denied, named intact",
              "日本.py" in reason, repr(out[:200]) + " | " + b.tail())

        # P: pattern values are pasted into `case` arms unquoted, so a space is a syntax
        # error that Copilot reads as deny-everything (bench, 2026-10-19). Every row the
        # recipe offers setup must parse; the spaced control proves the probe bites.
        rows = recipe_pattern_rows()
        bad = [r[0] for r in rows if not sh_parses(guard_src, r[1], r[2], base)]
        check("P1 every pattern row in the recipe's table instantiates into a script sh -n accepts",
              len(rows) >= 6 and not bad, "rows=%d unparsable=%r" % (len(rows), bad))
        check("P2 ...and a spaced TEST_CMD_PATTERN does not (the probe bites)",
              not sh_parses(guard_src, "tests/*", "*node *test*", base))
        # The exempt pattern is a case arm too: an EMPTY value is a syntax error that
        # Copilot reads as deny-everything, so setup never writes one (84.7 ruling 6).
        check("P3 the recipe's exempt default parses, and an empty exempt value does not",
              sh_parses(guard_src, "tests/*", "*pytest*", base,
                        exempt="*.config.*|.*|tools/*|scripts/*")
              and not sh_parses(guard_src, "tests/*", "*pytest*", base, exempt=""))

        return failed
    except _FirstFailure:
        return failed
    finally:
        shutil.rmtree(base, ignore_errors=True)


MUTATIONS = [
    ("drop the second candidate root (reintroduces the §72 defect: an absolute "
     "in-repo path stops matching whenever the shell's pwd flavour differs from the "
     "CLI's, so the guard skips every write reported that way)",
     lambda s: s.replace(
         'for cand in "$SDLC_REPO_ROOT" "$(cd "$SDLC_REPO_ROOT" 2>/dev/null && pwd -W 2>/dev/null)" "$wroot"; do',
         'for cand in "$SDLC_REPO_ROOT" "$wroot"; do')),
    ("name a worktree's licence in WSL mount form (the agent's tools cannot write "
     "/mnt/d/... - they take drive paths)",
     lambda s: s.replace(
         '  case "$LIC" in "$wm"/?/*) LIC=$(printf',
         '  case "$LIC" in "@@never@@"/?/*) LIC=$(printf')),
    ("drop the WSL mount candidate (the 0.28.1 fix's blind route: under WSL bash "
     "every absolute write is 'outside the repository' - FEATURE_PLAN.md 78.7)",
     lambda s: s.replace(
         'for cand in "$SDLC_REPO_ROOT" "$(cd "$SDLC_REPO_ROOT" 2>/dev/null && pwd -W 2>/dev/null)" "$wroot"; do',
         'for cand in "$SDLC_REPO_ROOT" "$(cd "$SDLC_REPO_ROOT" 2>/dev/null && pwd -W 2>/dev/null)"; do')),
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
    # Both anchors below were RE-POINTED at 0.28.1, when the §72 fix replaced the
    # single `case` with a two-candidate loop. The suite reported them STALE rather
    # than counting them caught, which is the only reason these two defect classes
    # did not silently lose their coverage.
    ("charge out-of-repo writes as production (a session scratchpad costs the same "
     "license as an edit to the module guarding the database)",
     lambda s: s.replace(
         '          /*|?:/*)\n'
         '            log "write outside the repository - not production source: $p"\n'
         '            continue ;;\n',
         '')),
    ("drop the repo-relative reduction (an absolute path to tests/conftest.py is "
     "charged as a production write - this dialect's live misclassification)",
     lambda s: s.replace(
         '          "$cl"/*) rel=$(printf \'%s\' "$n" | cut -c $((${#c} + 2))-); break ;;',
         '          "$cl"/*) break ;;')),
    ("match the runner against the raw command text (a commit message quoting the "
     "RED command counts as a test run)",
     lambda s: s.replace('    case "$PROBE" in', '    case "$CMD" in')),
    ("trust any cwd when SDLC_REPO_ROOT is unset (state written to unrelated dirs)",
     lambda s: s.replace('  [ -e .git ] || exit 0\n', '')),
    ("test for a .git DIRECTORY again (a linked worktree, whose .git is a file, "
     "disarms the guard in silence - FEATURE_PLAN.md 78)",
     lambda s: s.replace('  [ -e .git ] || exit 0\n', '  [ -d .git ] || exit 0\n')),
    ("keep state under the root's literal .git (a worktree's state has nowhere to go)",
     lambda s: s.replace('S="$GD/sdlc-tdd"', 'S="$SDLC_REPO_ROOT/.git/sdlc-tdd"')),
    ("drop the pinned-root fallback (a harness pinning a bare directory guards nothing, "
     "silently - the 0.31.1 regression an adopter's own tests caught)",
     lambda s: s.replace(
         '[ -z "$GD" ] && [ ! -e "$SDLC_REPO_ROOT/.git" ] && GD="$SDLC_REPO_ROOT/.git"\n', '')),
    ("resolve a relative gitdir against the cwd instead of the root",
     lambda s: s.replace('*) g="$1/$g" ;;', '*) ;;')),
    ("guard nothing in silence when the git dir cannot be resolved at stop",
     lambda s: s.replace('  if [ "$MODE" = "stop-check" ] && ! printf', '  if false && ! printf')),
    ("re-silence the compound refusal (the 2026-08-08 field defect: the session "
     "thrashes and probes instead of complying)",
     lambda s: s.replace('        emit_context "TDD ordering: that test run was NOT counted',
                         '        : "TDD ordering: that test run was NOT counted')),
    ("drop the green requirement from either license (a bare declaration "
     "licenses with no gate behind it)",
     lambda s: s.replace(
         '{ [ -f "$S/refactor-license" ] || [ -f "$S/close-out-license" ]; } '
         '&& [ -f "$S/green-observed" ]',
         '{ [ -f "$S/refactor-license" ] || [ -f "$S/close-out-license" ]; }')),
    ("never revoke the refactor license on a test edit (the window outlives the "
     "cycle it was declared for)",
     lambda s: s.replace('        rm -f "$S/refactor-license" 2>/dev/null\n', '')),
    ("revoke the CLOSE-OUT license on a test edit too (close-out's own mandated "
     "order becomes unexecutable again - FIELD_REPORT_2026-09-01 finding 1)",
     lambda s: s.replace(
         '      if [ -f "$S/close-out-license" ]; then\n        k=$(',
         '      if [ -f "$S/close-out-license" ]; then\n'
         '        rm -f "$S/close-out-license" 2>/dev/null\n        k=$(')),
    ("stop counting the test edits a close-out license survives (a license held "
     "open past its step goes silent)",
     lambda s: s.replace(
         'log "close-out license SURVIVED a test edit ($k this session)',
         'log "close-out license survived ($k)')),
    ("log a close-out write as a refactor one (the two licenses stop being "
     "distinguishable in review)",
     lambda s: s.replace(
         '        if [ -f "$S/close-out-license" ]; then which=close-out; else which=refactor; fi\n',
         '        which=refactor\n')),
    ("leak either license across sessions (survives the new-session clear)",
     lambda s: s.replace(
         'rm -f "$S/red-observed" "$S/green-observed" "$S/last-test-edit" '
         '"$S/refactor-license" "$S/close-out-license" "$S/close-out-survivals" '
         '"$S/prod-write-observed" 2>/dev/null',
         'rm -f "$S/red-observed" "$S/green-observed" "$S/last-test-edit" '
         '"$S/prod-write-observed" 2>/dev/null')),
    ("drop G2's session scoping (the stop guard binds planning and docs sessions "
     "again)",
     lambda s: s.replace(
         'if [ ! -f "$S/prod-write-observed" ] && [ ! -f "$S/last-test-edit" ]; then',
         'if false; then')),
    ("arm the stop guard from a denied write (a rule about writes enforced against "
     "a session that made none)",
     lambda s: s.replace(
         '      elif [ -f "$S/deny-enabled" ]; then\n'
         '        log "DENY production write without observed red: $prod"',
         '      elif [ -f "$S/deny-enabled" ]; then\n'
         '        touch "$S/prod-write-observed" 2>/dev/null\n'
         '        log "DENY production write without observed red: $prod"')),
    ("re-silence the counted GREEN observation (the state machine goes invisible "
     "on the success side again - FEATURE_PLAN.md 44)",
     lambda s: s.replace('emit_context "TDD ordering: GREEN counted',
                         ': "TDD ordering: GREEN counted')),
    ("re-silence the counted RED observations, both variants (ditto)",
     lambda s: s.replace('emit_context "TDD ordering: RED counted',
                         ': "TDD ordering: RED counted')),
    ("let a cosmetic write arm the stop guard (a comment fix demands a green - "
     "82.9 ruling 2)",
     lambda s: s.replace('        log "OK production write (cosmetic: $cos): $prod"',
                         '        touch "$S/prod-write-observed" 2>/dev/null\n'
                         '        log "OK production write (cosmetic: $cos): $prod"')),
    ("read any classifier output as the verdict (a real edit, or a crash that "
     "printed, waves through)",
     lambda s: s.replace('if [ "$crc" = 0 ]; then cos=', 'if [ -n "$cout" ]; then cos=')),
    ("consult the classifier on an already licensed write (cost on every write, and "
     "a licensed write logged as something else)",
     lambda s: s.replace('if [ -z "$ok" ] && [ "$nprod" = 1 ] && [ -n "$JP" ]',
                         'if [ "$nprod" = 1 ] && [ -n "$JP" ]')),
    ("count any failing exit as a RED (a wrapper's failure licenses a production "
     "write - sdlc-kit#16)",
     lambda s: s.replace('elif [ "$REPORT" != "1" ]; then', 'elif false; then')),
    ("match the report against the raw output (colour codes split the marker)",
     lambda s: s.replace('u=re.sub(r"\\x1b\\[[0-9;]*[A-Za-z]","",t).replace(chr(13)+chr(10),chr(10))',
                         'u=t')),
    ("let an invalid report pattern crash the parser (the guard goes blind)",
     lambda s: s.replace('except re.error:\n    o.append("E")',
                         'except KeyError:\n    o.append("E")')),
    ("read a heredoc's body as the command (the commit recipe records a false GREEN)",
     lambda s: s.replace('case "$PROBE" in *"<<"*) exit 0 ;; esac', '')),
    ("count read-only commands that name the runner (cat/grep/git record a GREEN)",
     lambda s: s.replace('""|cat|type|more|', '""|')),
    ("count package-manager installs (`uv add pytest` records a GREEN)",
     lambda s: s.replace('case "$2" in install|i|add|', 'case "$2" in never|')),
    ("count `python -m pip` (an install records a GREEN)",
     lambda s: s.replace('[ "$3" = "pip" ] && exit 0', '[ "$3" = "never" ] && exit 0')),
    ("judge a NAME=value prefix as the executable",
     lambda s: s.replace('$i ~ /^[a-z_][a-z0-9_]*=/', '$i == "never"')),
    ("keep the .exe on the executable (a Windows path to cat counts)",
     lambda s: s.replace('exe=${exe%.exe}; ', '')),
    ("drop the always-on graph-directory exemption",
     lambda s: s.replace('case "$n" in .ua/*|.understand-anything/*|{{GUARD_EXEMPT_PATTERN}})',
                         'case "$n" in {{GUARD_EXEMPT_PATTERN}})')),
    ("ignore the project's exempt pattern",
     lambda s: s.replace('case "$n" in .ua/*|.understand-anything/*|{{GUARD_EXEMPT_PATTERN}})',
                         'case "$n" in .ua/*|.understand-anything/*)')),
    ("write the parser's fields in the locale's encoding (a non-cp1252 path crashes "
     "the parser and the write goes unguarded)",
     lambda s: s.replace('sys.stdout.buffer.write(("\\n".join(o)+"\\n").encode("utf-8"))',
                         'sys.stdout.write("\\n".join(o)+"\\n")')),
    ("read the deny message as text (a non-ASCII path arrives as mojibake)",
     lambda s: s.replace('"permissionDecisionReason":sys.stdin.buffer.read().decode("utf-8","replace")',
                         '"permissionDecisionReason":sys.stdin.read()')),
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
        failed = guarded("unit pass [%s]" % name, [], unit, src, counter=ran, parser=name)
        print("\n%d cases, %s\n" % (
            len(ran), "all passed" if not failed else "FAILED: " + "; ".join(failed)))
        if failed:
            rc = 1

    # Mutations exercise the guard's shell logic, which sits above the parser choice, so
    # they run once under the ambient PATH rather than once per dialect.
    #
    # Each mutation needs ONE failing check, and the mutations are independent - each
    # unit() run is its own temp bench. They used to run one at a time and every check
    # to the end, so each paid the whole scenario and its 1.1 s mtime sleeps after the
    # verdict was settled. Now each stops at its first failing check and they run
    # concurrently; nothing here is timed. TDDGUARD_JOBS=1 runs them serially.
    jobs = max(1, int(os.environ.get("TDDGUARD_JOBS", "8")))
    print("=== mutation pass (%d mutations; the unit suite must catch each; %d at a time,"
          " first failing check named) ===" % (len(MUTATIONS), jobs))
    live = []
    for name, fn in MUTATIONS:
        mutated = guarded("mutation build: %s" % name, None, fn, src)
        if mutated is None:
            rc = 1
            continue
        if mutated == src:
            print("STALE    mutation no longer applies - update it: " + name)
            rc = 1
            continue
        live.append((name, mutated))
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = [pool.submit(guarded, "mutation: %s" % name, [], unit, mutated,
                               verbose=False, first_only=True)
                   for name, mutated in live]
        for (name, _), fut in zip(live, futures):
            caught = fut.result()
            if caught:
                print("caught   %s\n           (by: %s)" % (name, "; ".join(caught)),
                      flush=True)
            else:
                print("SURVIVED %s  <-- the suite is blind to this" % name, flush=True)
                rc = 1

    if guarded.crashed:
        print("CRASHED passes: %s" % ", ".join(guarded.crashed))
        rc = 1
    print("\n%s" % ("OK" if rc == 0 else "PROBLEMS ABOVE"))
    return rc


if __name__ == "__main__":
    sys.exit(main())
