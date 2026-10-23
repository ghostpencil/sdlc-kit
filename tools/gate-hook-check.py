#!/usr/bin/env python
"""Re-runnable proof for both edit-time gate hooks.

Covers the Copilot pair (`templates/copilot-hook.template.sh` holding the logic, with
`copilot-hook.template.json` as its bare launcher - split 2026-08-07 because the WSL
launcher boundary corrupts any rich command line, FEATURE_PLAN.md 38) and the Claude
Code pair (`templates/claude-gate.template.sh` holding the logic, with the Edit|Write
block in `templates/settings.template.json` as its bare launcher - split 2026-08-15,
FEATURE_PLAN.md 61, after the per-hook "shell": "bash" pin was measured never firing
on Claude Code 2.1.231), each under **both** JSON parser
dialects the hooks detect at run time (python and node). A dialect that is never
exercised is a dialect that is not proven, so the suite pins PATH to one parser at a
time and requires identical behaviour from each.

The Claude wiring is located by MATCHER, never by array index: through 0.23.0 this
suite read `PostToolUse[0]`, which 0.21.0's guard blocks had silently re-pointed at
the observe-test launcher - the Claude gate hook was unproven from 0.21.0 until this
was caught 2026-08-15. The wiring cases below also pin the no-"shell"-key property,
so the measured-dead pin cannot be silently reintroduced.

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
import concurrent.futures, io, json, os, shutil, stat, subprocess, sys, tempfile, traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPILOT_TPL = os.path.join(REPO, "sdlc-kit", "templates", "copilot-hook.template.json")
COPILOT_SH_TPL = os.path.join(REPO, "sdlc-kit", "templates", "copilot-hook.template.sh")
CLAUDE_TPL = os.path.join(REPO, "sdlc-kit", "templates", "settings.template.json")
# Every Claude launcher starts at the repository root, wherever a shell `cd` left the
# session (0.36.0, FEATURE_PLAN.md 85.7). `;`, never `|| exit 2`: Copilot runs these
# through PowerShell, where Windows PowerShell 5.1 cannot parse `||`, and a PreToolUse
# launcher that fails to parse denies every edit there.
ANCHOR = 'cd "$(git rev-parse --show-toplevel)"; '
CLAUDE_SH_TPL = os.path.join(REPO, "sdlc-kit", "templates", "claude-gate.template.sh")

RECIPES = os.path.join(REPO, "sdlc-kit", "reference", "GATE_RECIPES.md")

# Speaks on a pass too, like the typecheck stub below, so a clean lint's text printed
# under a typecheck failure is caught.
LINTER = ("#!/bin/sh\nif grep -q BAD \"$1\" 2>/dev/null; then\n"
          "  echo \"E001 bad token in $1\"; exit 1\nfi\necho \"E000 lint clean\"\nexit 0\n")
# The format half of a compound lint value (0.35.0, FEATURE_PLAN.md 84.5 D). It speaks
# on STDERR, so a hook that captured only the last command's stdout - or only the
# first command's stderr - would lose it.
FORMATTER = ("#!/bin/sh\nif grep -q FMT \"$1\" 2>/dev/null; then\n"
             "  echo \"F001 not formatted: $1\" >&2; exit 1\nfi\nexit 0\n")
# Speaks on a pass too, as real checkers do ("Success: no issues found"), so a hook that
# printed a clean check's text under another check's failure is caught.
TYPECHECKER = ("#!/bin/sh\nif grep -q TYPE \"$1\" 2>/dev/null; then\n"
               "  echo \"T001 type error in $1\"; exit 1\nfi\necho \"T000 typecheck clean\"\n"
               "exit 0\n")
# Stands in for `npx tsc` under the recipe's TypeScript block: records its arguments
# and replays a canned report from .tsc-out at the project root.
NPX = ("#!/bin/sh\necho \"$@\" > .npx-args\n"
       "if [ -s .tsc-out ]; then cat .tsc-out; exit 2; fi\nexit 0\n")

# The stderr-writing command goes FIRST: a trailing `2>&1` without the hook's group
# attaches to the last command only, so with the formatter last the group was untested.
LINT_CMD = 'stubfmt "$f" && stublint "$f"'
# Exercises every channel a typecheck block has: `t`/`trc` from a stub checker, `tn`
# (the non-blocking note) on ELSEWHERE, and `$r` (the repo-relative path) on SHOWREL.
TC_BLOCK = ('t=$(stubtc "$f" 2>&1); trc=$?; '
            'if grep -q ELSEWHERE "$f"; then tn="2 type error(s) in other files"; fi; '
            'if grep -q SHOWREL "$f"; then t="rel=$r"; trc=1; fi;')


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


def ts_block():
    """The TypeScript typecheck block exactly as GATE_RECIPES.md prints it."""
    s = io.open(RECIPES, encoding="utf-8").read()
    s = s[s.index("## TypeScript / JavaScript (Node)"):]
    s = s[s.index("```sh\n") + len("```sh\n"):]
    return s[:s.index("```")]


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


def instantiate(body, glob="*.py", block=TC_BLOCK):
    out = (body.replace("{{SOURCE_GLOB}}", glob)
               .replace("{{HOOK_LINT_CMD}}", LINT_CMD)
               .replace("{{HOOK_TYPECHECK_BLOCK}}", block))
    assert "{{" not in out, "unresolved placeholder in instantiated hook"
    return out


class Project:
    def __init__(self, base, body):
        self.root = os.path.join(base, "proj")
        os.makedirs(os.path.join(self.root, "src"))
        self.script = os.path.join(base, "hook.sh")
        io.open(self.script, "w", encoding="utf-8", newline="\n").write(body + "\n")
        for name, src in (("stublint", LINTER), ("stubfmt", FORMATTER),
                          ("stubtc", TYPECHECKER), ("npx", NPX)):
            p = os.path.join(self.root, name)
            io.open(p, "w", encoding="utf-8", newline="\n").write(src)
            os.chmod(p, os.stat(p).st_mode | stat.S_IEXEC)

    def put(self, rel, dirty):
        """dirty: True (a lint error), False (clean), or the file's literal content."""
        p = os.path.join(self.root, rel.replace("/", os.sep))
        d = os.path.dirname(p)
        if d and not os.path.isdir(d):
            os.makedirs(d)
        text = dirty if isinstance(dirty, str) else ("BAD\n" if dirty else "ok\n")
        io.open(p, "w", encoding="utf-8", newline="\n").write(text)

    def run(self, payload, parser, extra_env=None, raw=None):
        env = dict(os.environ)
        env["PATH"] = os.pathsep.join(
            [self.root] + ([parser_path(parser)] if parser_path(parser) else []))
        if extra_env:
            env.update(extra_env)
        data = raw if raw is not None else json.dumps(payload).encode()
        # From the project root, as both launchers start it: the Copilot body takes its
        # root for the scope test from where it was started.
        p = subprocess.run(["sh", self.script], input=data, capture_output=True, env=env,
                           cwd=self.root)
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

        # 0.35.0 (FEATURE_PLAN.md 84.5 D). Out of scope: a dirty file outside the
        # project is skipped - run dirty, and beside the in-project absolute twin
        # above, which is checked.
        outside = os.path.join(base, "scratch", "probe.py")
        os.makedirs(os.path.dirname(outside))
        io.open(outside, "w", encoding="utf-8", newline="\n").write("BAD\n")
        check("dirty file outside the project (absolute path) -> silent, not linted",
              ctx(ap(("Update", outside))) == "")
        if os.name == "nt":
            pj.put("src/case.py", True)
            r = ctx(ap(("Update", pj.root.upper() + "\\src\\case.py")))
            check("root spelled in another case (Windows) -> still in scope, checked",
                  "E001" in r, r)
        pj.put("src/rel.py", "SHOWREL\n")
        r = ctx(ap(("Update", os.path.join(pj.root, "src", "rel.py"))))
        check("typecheck block reads $r: repo-relative, /-separated, from an absolute path",
              "rel=src/rel.py" in r, r)
        # A root matched only without case takes the byte cut, not the prefix strip.
        # The scope case above passes with $r empty - this dialect still lints the
        # file - so the cut's own result is pinned here.
        if os.name == "nt":
            r = ctx(ap(("Update", pj.root.upper() + "\\src\\rel.py")))
            check("...and from a root spelled in another case (Windows)",
                  "rel=src/rel.py" in r, r)

        # Each check named, with only its own output.
        pj.put("src/l.py", True)
        r = ctx(ap(("Update", "src/l.py")))
        check("lint-only failure -> 'lint failed', no typecheck text",
              "gate hook: lint failed" in r and "E001" in r and "T00" not in r, r)
        pj.put("src/t.py", "TYPE\n")
        r = ctx(ap(("Update", "src/t.py")))
        check("typecheck-only failure -> 'typecheck failed', with the checker's output",
              "gate hook: typecheck failed" in r and "T001" in r and "E00" not in r, r)
        pj.put("src/lt.py", "BAD\nTYPE\n")
        r = ctx(ap(("Update", "src/lt.py")))
        check("both fail -> 'lint and typecheck failed', both outputs",
              "lint and typecheck failed" in r and "E001" in r and "T001" in r, r)
        pj.put("src/fmt.py", "FMT\n")
        r = ctx(ap(("Update", "src/fmt.py")))
        check("compound lint value: the format check's stderr is captured",
              "gate hook: lint failed" in r and "F001" in r, r)
        pj.put("src/else.py", "ELSEWHERE\n")
        r = ctx(ap(("Update", "src/else.py")))
        check("clean file, errors elsewhere -> a 'Not blocking' note naming the file",
              "src/else.py passed. Not blocking: 2 type error(s)" in r
              and "failed" not in r, r)

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
        # corrupts backslashes and $-expansions, so the config body must contain
        # neither - and must still hand the payload to the script from a repo-root
        # cwd, and do nothing anywhere else. Quotes were banned here too as a
        # precaution; a quoted body was measured surviving both routes 2026-09-27
        # (FEATURE_PLAN.md 78.7), and this launcher still carries none.
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

        # FEATURE_PLAN.md 78: the entry pins "cwd": "." (Copilot 1.0.64-1.0.87 ran
        # hooks in the SESSION cwd otherwise), and the launcher must accept a .git
        # FILE - a linked worktree's - where it used to demand a directory and stand
        # the gate down in silence. The gate script itself reads no git state.
        entries = [h for hs in launcher["hooks"].values() for h in hs]
        check("launcher entry pins cwd to the repository root, no .git DIRECTORY test",
              all(h.get("cwd") == "." and "-d .git" not in h["bash"] for h in entries),
              json.dumps(entries))
        os.rmdir(os.path.join(pj.root, ".git"))
        io.open(os.path.join(pj.root, ".git"), "w", newline="\n").write(
            "gitdir: ../main/.git/worktrees/wt\n")
        p = subprocess.run(["sh", "-c", lbodies[0]],
                           input=json.dumps(ap(("Update", "src/e.py"))).encode(),
                           capture_output=True, env=lenv, cwd=pj.root)
        out = p.stdout.decode("utf-8", "replace")
        check("launcher at a worktree root (.git is a file) still runs the gate",
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
            rmtree(elsewhere)
    finally:
        rmtree(base)


def claude_suite(parser, check):
    """Claude Code dialect: feedback is stderr + exit 2."""
    tpl = json.load(io.open(CLAUDE_TPL, encoding="utf-8"))
    post = {g.get("matcher"): g["hooks"][0] for g in tpl["hooks"]["PostToolUse"]}
    check("gate launcher is the bare split line (located by matcher, not index)",
          post.get("Edit|Write", {}).get("command")
          == ANCHOR + "sh .github/hooks/sdlc-gate-claude.sh",
          repr(post.get("Edit|Write", {}).get("command")))
    check("ledger launcher is the bare split line",
          post.get("Skill", {}).get("command")
          == ANCHOR + "sh .github/hooks/sdlc-skill-ledger.sh",
          repr(post.get("Skill", {}).get("command")))
    every = [h["command"] for gs in tpl["hooks"].values() for g in gs for h in g["hooks"]]
    check("every Claude launcher starts with the root anchor, and none carries '||'",
          len(every) == 7 and all(c.startswith(ANCHOR) and "||" not in c for c in every),
          repr([c[:60] for c in every]))
    check("stop backstop invokes the checker's stop-check without the pin",
          any("sdlc-close-out.sh stop-check" in h["command"]
              for g in tpl["hooks"]["Stop"] for h in g["hooks"]))
    check("no hook anywhere carries a 'shell' key (pin measured dead 2026-08-15, "
          "Claude Code 2.1.231, Stop and PostToolUse)",
          '"shell"' not in json.dumps(tpl))
    body = instantiate(io.open(CLAUDE_SH_TPL, encoding="utf-8").read())
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
              "SDLC gate hook" in err and "lint failed" in err
              and "src/a.py" in err, "err=%r" % err[:160])
        pj.put("src/a.py", False)
        rc, err = run(edit("src/a.py"))
        check("...and goes silent once the file is clean", rc == 0 and err == "",
              "rc=%s err=%r" % (rc, err[:80]))

        pj.put("notes.md", True)
        rc, err = run(edit("notes.md"))
        check("non-source file -> silent", rc == 0 and err == "")

        # 0.35.0 (FEATURE_PLAN.md 84.5 D), as in the Copilot suite.
        pj.put("src/abs.py", True)
        rc, err = run(edit(os.path.join(pj.root, "src", "abs.py")))
        check("dirty file inside the project by absolute path -> checked",
              rc == 2 and "E001" in err, "rc=%s err=%r" % (rc, err[:80]))
        outside = os.path.join(base, "scratch", "probe.py")
        os.makedirs(os.path.dirname(outside))
        io.open(outside, "w", encoding="utf-8", newline="\n").write("BAD\n")
        rc, err = run(edit(outside))
        check("...and its dirty twin outside the project -> silent, not linted",
              rc == 0 and err == "", "rc=%s err=%r" % (rc, err[:80]))
        if os.name == "nt":
            rc, err = run(edit(pj.root.upper() + "\\src\\abs.py"))
            check("root spelled in another case (Windows) -> still in scope, checked",
                  rc == 2 and "E001" in err, "rc=%s err=%r" % (rc, err[:80]))
        pj.put("src/rel.py", "SHOWREL\n")
        rc, err = run(edit(os.path.join(pj.root, "src", "rel.py")))
        check("typecheck block reads $r: repo-relative, /-separated, from an absolute path",
              "rel=src/rel.py" in err, "err=%r" % err[:160])

        pj.put("src/l.py", True)
        rc, err = run(edit("src/l.py"))
        check("lint-only failure -> 'lint failed', no typecheck text",
              rc == 2 and "gate hook: lint failed" in err and "T00" not in err,
              "rc=%s err=%r" % (rc, err[:160]))
        pj.put("src/t.py", "TYPE\n")
        rc, err = run(edit("src/t.py"))
        check("typecheck-only failure -> 'typecheck failed', with the checker's output",
              rc == 2 and "gate hook: typecheck failed" in err and "T001" in err
              and "E00" not in err, "rc=%s err=%r" % (rc, err[:160]))
        pj.put("src/lt.py", "BAD\nTYPE\n")
        rc, err = run(edit("src/lt.py"))
        check("both fail -> 'lint and typecheck failed', both outputs",
              rc == 2 and "lint and typecheck failed" in err and "E001" in err
              and "T001" in err, "rc=%s err=%r" % (rc, err[:160]))
        pj.put("src/fmt.py", "FMT\n")
        rc, err = run(edit("src/fmt.py"))
        # Here the hook's own stderr IS the channel, so an uncaptured F001 would still
        # show up - ahead of the framing, unattributed. Captured, it follows it.
        check("compound lint value: the format check's stderr is captured, under the frame",
              rc == 2 and "lint failed" in err and "F001" in err
              and err.index("F001") > err.index("lint failed"),
              "rc=%s err=%r" % (rc, err[:160]))
        pj.put("src/else.py", "ELSEWHERE\n")
        p = pj.run(edit("src/else.py"), parser, extra_env=env)
        out = p.stdout.decode("utf-8", "replace").strip()
        try:
            note = json.loads(out)["hookSpecificOutput"]
            ok = (note.get("hookEventName") == "PostToolUse"
                  and "src/else.py passed. Not blocking: 2 type error(s)"
                  in note.get("additionalContext", ""))
        except Exception:
            ok = False
        check("clean file, errors elsewhere -> exit 0, the note as PostToolUse "
              "additionalContext", ok and p.returncode == 0 and not p.stderr.strip(),
              "rc=%s out=%r err=%r" % (p.returncode, out[:160], p.stderr[:80]))

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

        # FEATURE_PLAN.md 79: Copilot reads .claude/settings.json and runs this hook
        # on its own edits, payload translated into this shape plus `timestamp`,
        # never `permission_mode` (measured 2026-09-28, 1.0.88). The Copilot gate
        # gates that session; this one exits 0 at once - on a DIRTY file, so the
        # silence proves the stand-down rather than a clean lint. Run dirty below:
        # the same payload from Claude Code (permission_mode present) still gates.
        pj.put("src/a.py", True)
        cop = {"hook_event_name": "PostToolUse", "session_id": "s",
               "timestamp": "2026-09-28T14:34:35.696Z", "cwd": pj.root,
               "tool_name": "Write", "tool_input": {"path": "src/a.py", "file_text": "BAD\n"},
               "tool_result": {"result_type": "success"}}
        rc, err = run(cop)
        check("Copilot-translated payload on a dirty file -> silent stand-down",
              rc == 0 and err == "", "rc=%s err=%r" % (rc, err[:80]))
        rc, err = run(dict(cop, permission_mode="default"))
        check("...and the same payload carrying permission_mode still gates (run dirty)",
              rc == 2 and "E001" in err, "rc=%s err=%r" % (rc, err[:80]))

        pj.put("src/a.py", True)
        rc, err = run(edit("src/a.py"), e={"CLAUDE_PROJECT_DIR": os.path.join(base, "nope")})
        check("unusable CLAUDE_PROJECT_DIR -> LOUD, not a silent skip",
              rc == 2 and "did NOT run" in err, "rc=%s err=%r" % (rc, err[:80]))
    finally:
        rmtree(base)


def ts_recipe_suite(parser, check):
    """GATE_RECIPES.md's TypeScript block, read from the file, in both dialect bodies.

    The block is the recipe's answer to sdlc-kit#14 (FEATURE_PLAN.md 84.5 D): typecheck
    the one tsconfig project owning the file and block only on errors located in it, in
    that tsconfig, or with no location. Driven against a stub `npx` replaying a canned
    `tsc --pretty false` report, so what is proven is the selection and the filter.
    """
    block = ts_block()
    check("recipe block found in GATE_RECIPES.md", "npx tsc" in block and "tn=" in block,
          block[:120])
    for dialect, tpl in (("claude", CLAUDE_SH_TPL), ("copilot", COPILOT_SH_TPL)):
        body = instantiate(io.open(tpl, encoding="utf-8").read(), glob="*.ts", block=block)
        base = tempfile.mkdtemp(prefix="gatehook-ts-")
        try:
            pj = Project(base, body)
            pj.put("packages/app/tsconfig.json", "{}\n")
            pj.put("tsconfig.json", "{}\n")

            def go(rel, report):
                """-> (blocked, failure text, note, npx args)."""
                io.open(os.path.join(pj.root, ".tsc-out"), "w", encoding="utf-8",
                        newline="\n").write(report)
                pj.put(rel, False)
                path = os.path.join(pj.root, rel.replace("/", os.sep))
                if dialect == "claude":
                    p = pj.run({"tool_name": "Edit", "tool_input": {"file_path": path}},
                               parser, extra_env={"CLAUDE_PROJECT_DIR": pj.root})
                    err = p.stderr.decode("utf-8", "replace")
                    out = p.stdout.decode("utf-8", "replace").strip()
                    note = json.loads(out)["hookSpecificOutput"]["additionalContext"] \
                        if out else ""
                    res = (p.returncode == 2, err, note)
                else:
                    p = pj.run({"cwd": pj.root, "toolName": "apply_patch",
                                "toolArgs": patch(("Update", path))}, parser)
                    out = p.stdout.decode("utf-8", "replace").strip()
                    t = json.loads(out)["additionalContext"] if out else ""
                    res = ("failed on the file" in t, t if "failed" in t else "",
                           t if "Not blocking" in t else "")
                a = os.path.join(pj.root, ".npx-args")
                args = io.open(a, encoding="utf-8").read().strip() \
                    if os.path.exists(a) else ""
                if os.path.exists(a):
                    os.remove(a)
                return res + (args,)

            own = ("packages/app/src/a.ts(3,5): error TS2322: Type 'x' is not 'y'.\n"
                   "  The expected type comes from here.\n"
                   "packages/app/src/b.ts(1,1): error TS2307: Cannot find module.\n")
            bl, txt, note, args = go("packages/app/src/a.ts", own)
            check("[%s] own-file error -> blocks with it and its continuation line"
                  % dialect, bl and "TS2322" in txt and "expected type" in txt
                  and "TS2307" not in txt, txt)
            check("[%s] ...typechecking the nearest tsconfig upward" % dialect,
                  "-p packages/app/tsconfig.json" in args, args)
            bl, txt, note, args = go("packages/app/src/c.ts", own)
            check("[%s] errors only in other files -> passes, with a count in the note"
                  % dialect, not bl and "2 type error(s) in other files of "
                  "packages/app/tsconfig.json" in note, (txt, note))
            bl, txt, note, args = go(
                "packages/app/src/a.ts",
                "packages/app/tsconfig.json(2,3): error TS1005: ',' expected.\n")
            check("[%s] owning tsconfig unreadable -> blocks, never clean" % dialect,
                  bl and "TS1005" in txt, (txt, note))
            bl, txt, note, args = go("packages/app/src/a.ts",
                                     "error TS5058: The specified path does not exist.\n")
            check("[%s] unlocated error (tsc could not run) -> blocks" % dialect,
                  bl and "TS5058" in txt, (txt, note))
            bl, txt, note, args = go("packages/app/src/a.ts", "sh: tsc: not found\n")
            check("[%s] no TS error at all but a failed run -> blocks with its output"
                  % dialect, bl and "not found" in txt, (txt, note))
            bl, txt, note, args = go("test/x.ts", "")
            check("[%s] clean, root-project file -> silent, root tsconfig" % dialect,
                  not bl and not txt and not note and args.endswith("-p tsconfig.json"),
                  (txt, note, args))
        finally:
            rmtree(base)


def run_suite(label, suite, parser):
    """One suite under one parser; returns (lines, failed). Each run is its own temp
    project, so the six run concurrently and buffer their lines for in-order output."""
    lines, failed = [], []

    def check(name, cond, detail=""):
        if not cond:
            failed.append(name)
        lines.append(("  PASS  " if cond else "  FAIL  ") + name +
                     (("\n          " + str(detail)) if not cond and detail else ""))

    guarded("%s [parser: %s]" % (label, parser), None, suite, parser, check)
    return lines, failed


def main():
    rc = 0
    jobs = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        for parser in ("python", "node"):
            if not PARSER_DIRS.get(parser):
                jobs.append((parser, None, None))
                continue
            for label, suite in (("copilot gate hook", copilot_suite),
                                 ("claude code gate hook", claude_suite),
                                 ("typescript recipe block", ts_recipe_suite)):
                jobs.append((parser, label, pool.submit(run_suite, label, suite, parser)))
        for parser, label, fut in jobs:
            if fut is None:
                print("=== %s === SKIPPED - not installed here, so this dialect is "
                      "UNPROVEN on this machine\n" % parser)
                rc = 1
                continue
            lines, failed = fut.result()
            print("=== %s [parser: %s] ===" % (label, parser))
            print("\n".join(lines))
            if failed:
                rc = 1
            print(flush=True)
    if guarded.crashed:
        print("CRASHED passes: %s" % ", ".join(guarded.crashed))
        rc = 1
    print("OK" if rc == 0 else "PROBLEMS ABOVE")
    return rc


if __name__ == "__main__":
    sys.exit(main())
