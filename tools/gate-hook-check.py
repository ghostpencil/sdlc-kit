#!/usr/bin/env python
"""Re-runnable proof for both edit-time gate hooks.

Covers the Copilot pair (`templates/copilot-hook.template.sh` holding the logic, with
`copilot-hook.template.json` as its bare launcher - split 2026-08-07 because the WSL
launcher boundary corrupts any rich command line, FEATURE_PLAN.md 38) and the Claude
Code dialect in `templates/settings.template.json`, each under **both** JSON parser
dialects the hooks detect at run time (python and node). A dialect that is never
exercised is a dialect that is not proven, so the suite pins PATH to one parser at a
time and requires identical behaviour from each.

Every case drives the instantiated template rather than a hand-copied approximation.
Payload shapes come from the bench captures (FEATURE_PLAN.md 31.7) - including
`apply_patch`'s raw-patch-text form, whose mis-parse meant the Copilot gate never ran
on a single edit through 0.15.0. The launcher JSON gets the boundary-property case
(no backslash, no $, no quotes) plus wiring cases, mirroring the TDD-guard suite.

Every silent case is also run dirty: silence only proves something once the same case
has been made to speak (invariant 13).

Kit-development artifact: root only, never inside sdlc-kit/ (invariant 12).
Run from anywhere:  python tools/gate-hook-check.py
"""
import io, json, os, shutil, stat, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPILOT_TPL = os.path.join(REPO, "sdlc-kit", "templates", "copilot-hook.template.json")
COPILOT_SH_TPL = os.path.join(REPO, "sdlc-kit", "templates", "copilot-hook.template.sh")
CLAUDE_TPL = os.path.join(REPO, "sdlc-kit", "templates", "settings.template.json")

LINTER = ("#!/bin/sh\nif grep -q BAD \"$1\" 2>/dev/null; then\n"
          "  echo \"E001 bad token in $1\"; exit 1\nfi\nexit 0\n")


def _dir_of(exe):
    p = shutil.which(exe)
    return os.path.dirname(p) if p else None


SHELL_DIR = _dir_of("sh")
PARSER_DIRS = {"python": _dir_of("python") or _dir_of("python3"), "node": _dir_of("node")}


def parser_path(name):
    """PATH exposing the shell utilities plus exactly one JSON parser (or none)."""
    parts = [SHELL_DIR] if SHELL_DIR else []
    if name and PARSER_DIRS.get(name):
        parts.append(PARSER_DIRS[name])
    return os.pathsep.join(parts)


def patch(*entries):
    return "*** Begin Patch\n" + "".join(
        "*** %s File: %s\n+x\n" % (k, p) for k, p in entries) + "*** End Patch\n"


def instantiate(body, glob="*.py"):
    out = (body.replace("{{SOURCE_GLOB}}", glob)
               .replace("{{HOOK_LINT_CMD}}", 'stublint "$f"')
               .replace("{{HOOK_TYPECHECK_BLOCK}}", ""))
    assert "{{" not in out, "unresolved placeholder in instantiated hook"
    return out


class Project:
    def __init__(self, base, body):
        self.root = os.path.join(base, "proj")
        os.makedirs(os.path.join(self.root, "src"))
        self.script = os.path.join(base, "hook.sh")
        io.open(self.script, "w", encoding="utf-8", newline="\n").write(body + "\n")
        lint = os.path.join(self.root, "stublint")
        io.open(lint, "w", encoding="utf-8", newline="\n").write(LINTER)
        os.chmod(lint, os.stat(lint).st_mode | stat.S_IEXEC)

    def put(self, rel, dirty):
        p = os.path.join(self.root, rel.replace("/", os.sep))
        d = os.path.dirname(p)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        io.open(p, "w", encoding="utf-8", newline="\n").write("BAD\n" if dirty else "ok\n")

    def run(self, payload, parser, extra_env=None, raw=None):
        env = dict(os.environ)
        env["PATH"] = os.pathsep.join(
            [self.root] + ([parser_path(parser)] if parser_path(parser) else []))
        if extra_env:
            env.update(extra_env)
        data = raw if raw is not None else json.dumps(payload).encode()
        p = subprocess.run(["sh", self.script], input=data, capture_output=True, env=env)
        return p


def copilot_suite(parser, check):
    """Copilot dialect: feedback arrives as JSON additionalContext on stdout."""
    body = instantiate(io.open(COPILOT_SH_TPL, encoding="utf-8").read())
    base = tempfile.mkdtemp(prefix="gatehook-cop-")
    try:
        pj = Project(base, body)

        def ctx(payload=None, raw=None, prs=parser):
            p = pj.run(payload, prs, raw=raw)
            out = p.stdout.decode("utf-8", "replace").strip()
            if not out:
                return ""
            try:
                return json.loads(out)["additionalContext"]
            except Exception:
                return "UNPARSEABLE HOOK OUTPUT: " + out

        def ap(*entries):
            return {"cwd": pj.root, "toolName": "apply_patch", "toolArgs": patch(*entries)}

        pj.put("src/a.py", True)
        check("apply_patch (raw patch text) -> the gate runs and reports",
              "E001" in ctx(ap(("Update", "src/a.py"))))
        pj.put("src/a.py", False)
        check("...and goes silent once the file is clean", ctx(ap(("Update", "src/a.py"))) == "")

        pj.put("src/b.py", True)
        r = ctx(ap(("Add", "src/a.py"), ("Update", "src/b.py"), ("Delete", "src/gone.py")))
        check("multi-file patch -> lints each, names only the dirty one",
              "src/b.py" in r and "src/a.py" not in r, r)
        check("delete-only patch -> silent, not a false alarm",
              ctx(ap(("Delete", "src/gone.py"))) == "")

        pj.put("src/c.py", True)
        check("VS Code dialect (tool_input object)",
              "E001" in ctx({"cwd": pj.root, "toolName": "edit",
                             "tool_input": {"file_path": "src/c.py"}}))
        check("JSON-encoded-string toolArgs",
              "E001" in ctx({"cwd": pj.root, "toolName": "create",
                             "toolArgs": json.dumps({"path": "src/c.py"})}))

        pj.put("src/d.py", True)
        check("absolute path in the patch header",
              "E001" in ctx(ap(("Update", os.path.join(pj.root, "src", "d.py")))))
        pj.put("src/f.py", True)
        check("backslashed relative path in the patch header (normalized before lookup)",
              "E001" in ctx(ap(("Update", "src\\f.py"))))
        pj.put("src/my file.py", True)
        check("path containing a space",
              "E001" in ctx(ap(("Update", "src/my file.py"))))

        pj.put("notes.md", True)
        check("non-source file -> silent", ctx(ap(("Update", "notes.md"))) == "")

        check("no recognisable path -> says the gate did NOT run",
              "did NOT run" in ctx({"cwd": pj.root, "toolName": "create",
                                    "toolArgs": json.dumps({"unknown": 1})}))
        check("patch with no file headers -> says the gate did NOT run",
              "did NOT run" in ctx({"cwd": pj.root, "toolName": "apply_patch",
                                    "toolArgs": "*** Begin Patch\n*** End Patch\n"}))
        r = ctx(ap(("Update", "src/missing.py")))
        check("path not found from the hook cwd -> says so, names the file",
              "did NOT run" in r and "missing.py" in r, r)

        p = pj.run(None, parser, raw=b"not json at all")
        out = p.stdout.decode("utf-8", "replace")
        check("unparseable payload -> loud, and still exit 0",
              "did NOT run" in out and p.returncode == 0, repr(out[:100]))

        # The whole point of dual parsers: with neither present it must say which
        # dependency is missing, not fail silently.
        r = ctx(ap(("Update", "src/b.py")), prs=None)
        check("no parser on PATH -> names the missing dependency",
              "no JSON parser" in r and "python or node" in r, r)

        # FBK.4 (FEATURE_PLAN.md 44): output cut at the 8000-char cap with no marker
        # reads as complete - truncation must say so, inside the cap.
        lint_path = os.path.join(pj.root, "stublint")
        io.open(lint_path, "w", encoding="utf-8", newline="\n").write(
            "#!/bin/sh\ni=0\nwhile [ $i -lt 400 ]; do\n"
            '  echo "E001 oversized diagnostic line $i with padding padding padding"\n'
            "  i=$((i+1))\ndone\nexit 1\n")
        pj.put("src/big.py", False)
        r = ctx(ap(("Update", "src/big.py")))
        check("over-cap output carries the truncation marker, inside the cap",
              "truncated by the gate hook" in r and len(r) <= 8000,
              "len=%d tail=%r" % (len(r), r[-80:]))
        io.open(lint_path, "w", encoding="utf-8", newline="\n").write(LINTER)

        # The launcher JSON (FEATURE_PLAN.md 38.5.4): the WSL launcher boundary
        # corrupts backslashes, $-expansions and quoting, so the config body must
        # contain none of them - and must still hand the payload to the script from
        # a repo-root cwd, and do nothing anywhere else.
        launcher = json.load(io.open(COPILOT_TPL, encoding="utf-8"))
        lbodies = [h["bash"] for hs in launcher["hooks"].values() for h in hs]
        check("launcher body survives the WSL launcher boundary (no backslash/$/quotes)",
              bool(lbodies) and all(not any(ch in bd for ch in "\\$'\"") for bd in lbodies),
              " | ".join(lbodies))

        gate_installed = os.path.join(pj.root, ".github", "hooks", "sdlc-gate.sh")
        os.makedirs(os.path.dirname(gate_installed))
        os.makedirs(os.path.join(pj.root, ".git"))
        shutil.copy(pj.script, gate_installed)
        lenv = dict(os.environ)
        lenv["PATH"] = os.pathsep.join([pj.root, parser_path(parser)])
        pj.put("src/e.py", True)
        p = subprocess.run(["sh", "-c", lbodies[0]],
                           input=json.dumps(ap(("Update", "src/e.py"))).encode(),
                           capture_output=True, env=lenv, cwd=pj.root)
        out = p.stdout.decode("utf-8", "replace")
        check("launcher at repo root pipes the payload into the gate script",
              "E001" in out, repr(out[:120]))
        elsewhere = tempfile.mkdtemp(prefix="gatehook-elsewhere-")
        try:
            p = subprocess.run(["sh", "-c", lbodies[0]],
                               input=json.dumps(ap(("Update", "src/e.py"))).encode(),
                               capture_output=True, env=lenv, cwd=elsewhere)
            check("launcher away from a repo root: silent, exit 0",
                  p.returncode == 0 and p.stdout.decode().strip() == "",
                  repr(p.stdout.decode()[:120]))
        finally:
            shutil.rmtree(elsewhere, ignore_errors=True)
    finally:
        shutil.rmtree(base, ignore_errors=True)


def claude_suite(parser, check):
    """Claude Code dialect: feedback is stderr + exit 2."""
    hook = json.load(io.open(CLAUDE_TPL, encoding="utf-8"))
    body = instantiate(hook["hooks"]["PostToolUse"][0]["hooks"][0]["command"])
    base = tempfile.mkdtemp(prefix="gatehook-cc-")
    try:
        pj = Project(base, body)
        env = {"CLAUDE_PROJECT_DIR": pj.root}

        def run(payload=None, raw=None, prs=parser, e=None):
            p = pj.run(payload, prs, extra_env=(e if e is not None else env), raw=raw)
            return p.returncode, p.stderr.decode("utf-8", "replace").strip()

        def edit(path):
            return {"tool_name": "Edit", "tool_input": {"file_path": path}}

        pj.put("src/a.py", True)
        rc, err = run(edit("src/a.py"))
        check("dirty source -> exit 2 with the linter output", rc == 2 and "E001" in err,
              "rc=%s err=%r" % (rc, err[:80]))
        # FBK.1 (FEATURE_PLAN.md 44): raw linter output with no framing tells the
        # model nothing about which hook fired, which file it checked, or what is
        # expected - the Copilot dialect always framed; this one must match it.
        check("...and the failure is framed: hook named, expectation stated, file named",
              "SDLC gate hook" in err and "lint/typecheck failed" in err
              and "src/a.py" in err, "err=%r" % err[:160])
        pj.put("src/a.py", False)
        rc, err = run(edit("src/a.py"))
        check("...and goes silent once the file is clean", rc == 0 and err == "",
              "rc=%s err=%r" % (rc, err[:80]))

        pj.put("notes.md", True)
        rc, err = run(edit("notes.md"))
        check("non-source file -> silent", rc == 0 and err == "")

        # The three cases this dialect used to swallow with a silent exit 0.
        rc, err = run({"tool_name": "Edit", "tool_input": {}})
        check("no path in payload -> LOUD (was a silent exit 0)",
              rc == 2 and "did NOT run" in err, "rc=%s err=%r" % (rc, err[:80]))
        rc, err = run(edit("src/missing.py"))
        check("missing file -> LOUD, names the file",
              rc == 2 and "did NOT run" in err and "missing.py" in err,
              "rc=%s err=%r" % (rc, err[:80]))
        rc, err = run(raw=b"not json at all")
        check("unparseable payload -> LOUD (was a silent exit 0)",
              rc == 2 and "did NOT run" in err, "rc=%s err=%r" % (rc, err[:80]))
        rc, err = run(edit("src/a.py"), prs=None)
        check("no parser on PATH -> LOUD, names the missing dependency",
              rc == 2 and "no JSON parser" in err and "python or node" in err,
              "rc=%s err=%r" % (rc, err[:80]))

        pj.put("src/a.py", True)
        rc, err = run(edit("src/a.py"), e={"CLAUDE_PROJECT_DIR": os.path.join(base, "nope")})
        check("unusable CLAUDE_PROJECT_DIR -> LOUD, not a silent skip",
              rc == 2 and "did NOT run" in err, "rc=%s err=%r" % (rc, err[:80]))
    finally:
        shutil.rmtree(base, ignore_errors=True)


def main():
    rc = 0
    for parser in ("python", "node"):
        if not PARSER_DIRS.get(parser):
            print("=== %s === SKIPPED - not installed here, so this dialect is "
                  "UNPROVEN on this machine\n" % parser)
            rc = 1
            continue
        for label, suite in (("copilot gate hook", copilot_suite),
                             ("claude code gate hook", claude_suite)):
            print("=== %s [parser: %s] ===" % (label, parser))
            failed = []

            def check(name, cond, detail=""):
                if not cond:
                    failed.append(name)
                print(("  PASS  " if cond else "  FAIL  ") + name +
                      (("\n          " + str(detail)) if not cond and detail else ""))

            suite(parser, check)
            if failed:
                rc = 1
            print()
    print("OK" if rc == 0 else "PROBLEMS ABOVE")
    return rc


if __name__ == "__main__":
    sys.exit(main())
