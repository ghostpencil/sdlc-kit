#!/usr/bin/env python
"""Re-runnable proof for `/sdlc-update`'s hook-script re-derive helper.

The helper lives inline in `sdlc-kit/commands/sdlc-update.md` (step 5, the hook-script
walk-through), between `cat > /tmp/kit-rederive.py <<'PY'` and its `PY` line. This
suite extracts that exact text, so the command and its proof cannot drift. It runs the
helper against a throwaway kit repository with two release tags and a throwaway
project holding an instantiated script.

The fixture is the one FEATURE_PLAN.md 84.16 ruled. The committed script carries three
local amendments: one a version note retires, one the target template now subsumes,
and one to keep. With `--drop` naming the first two, the proposal must equal the
target template, filled, plus the kept amendment only. Without `--drop`, every
amendment is carried by construction. That is the defect 84.16 found at a real update,
where the retired ones would have shipped silently.

Each mutation edits the helper's text as extracted, and the case pass must notice it
(invariant 13).

Kit-development artifact: root only, never inside sdlc-kit/ (invariant 12).
Run from anywhere:  python tools/rederive-check.py
"""
import io, os, shutil, stat, subprocess, sys, tempfile, traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATE = os.path.join(REPO, "sdlc-kit", "commands", "sdlc-update.md")
TPL = "fake.template.sh"
SCRIPT = "hooks/fake.sh"
VALUES = '{"{{ROOT}}": "/proj"}'

V1 = ("#!/bin/sh\n# a template\nROOT=\"{{ROOT}}\"\nstep_a\nstep_b\nstep_c\nstep_d\n"
      "step_e\nstep_f\nstep_g\nstep_h\nstep_i\ntail\n")
# The target release: it fixes step_d itself (what amendment 2 did locally) and adds a
# line well away from every amendment.
V2 = V1.replace("step_d\n", "step_d_fixed_in_kit\n").replace("tail\n",
                                                             "tail\nstep_new\n")
FILLED = lambda body: body.replace("{{ROOT}}", "/proj")
# Amendment 1 (retired by a version note): an added line the target never touches.
# Amendment 2 (subsumed): a local fix the target now makes itself.
# Amendment 3 (kept): a local change the target leaves alone.
INSTALLED = (FILLED(V1).replace("step_a\n", "step_a\namend_one_retired\n")
             .replace("step_d\n", "step_d_fixed_locally\n")
             .replace("step_g\n", "step_g_local\n"))
EXPECTED = FILLED(V2).replace("step_g\n", "step_g_local\n")


def rmtree(path):
    """Windows git writes its objects read-only; clear the bit and delete again."""
    shutil.rmtree(path, ignore_errors=True)
    if os.path.exists(path):
        for d, _, files in os.walk(path):
            for f in files:
                try:
                    os.chmod(os.path.join(d, f), stat.S_IWRITE)
                except OSError:
                    pass
        shutil.rmtree(path, ignore_errors=True)


def helper_text():
    lines = io.open(UPDATE, encoding="utf-8").read().split("\n")
    start = next(i for i, l in enumerate(lines)
                 if l.strip() == "cat > /tmp/kit-rederive.py <<'PY'")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "PY")
    body = lines[start + 1:end]
    indent = min(len(l) - len(l.lstrip()) for l in body if l.strip())
    return "\n".join(l[indent:] for l in body) + "\n"


def git(cwd, *args):
    p = subprocess.run(("git",) + args, cwd=cwd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), p.stderr.decode()))
    return p.stdout.decode()


def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    io.open(path, "w", encoding="utf-8", newline="").write(text)


def init(path):
    os.makedirs(path)
    git(path, "init", "-q", ".")
    git(path, "config", "user.email", "proof@example.invalid")
    git(path, "config", "user.name", "proof")
    git(path, "config", "core.autocrlf", "false")


class Bench:
    def __init__(self, helper_src, installed, uncommitted=False):
        self.base = tempfile.mkdtemp(prefix="rederive-")
        self.kit = os.path.join(self.base, "kit")
        self.proj = os.path.join(self.base, "proj")
        init(self.kit)
        for tag, body in (("v1.0.0", V1), ("v1.1.0", V2)):
            write(os.path.join(self.kit, "sdlc-kit", "templates", TPL), body)
            git(self.kit, "add", "-A")
            git(self.kit, "commit", "-q", "-m", tag)
            git(self.kit, "tag", tag)
        init(self.proj)
        write(os.path.join(self.proj, SCRIPT), installed)
        git(self.proj, "add", "-A")
        git(self.proj, "commit", "-q", "-m", "adopt")
        if uncommitted:
            write(os.path.join(self.proj, SCRIPT), installed + "dirty\n")
        self.values = os.path.join(self.base, "values.json")
        write(self.values, VALUES)
        self.helper = os.path.join(self.base, "kit-rederive.py")
        write(self.helper, helper_src)

    def run(self, target, *extra):
        p = subprocess.run([sys.executable, self.helper, SCRIPT, TPL, self.values,
                            target, self.kit] + list(extra),
                           cwd=self.proj, capture_output=True)
        out = (p.stdout + p.stderr).decode("utf-8", "replace").replace("\r\n", "\n")
        proposed = None
        for line in out.split("\n"):
            if line.startswith("PROPOSED FILE: "):
                # git-dir relative, as the helper prints it: the project's own.
                where = os.path.join(self.proj, line[len("PROPOSED FILE: "):].strip())
                with io.open(where, encoding="utf-8", newline="") as fh:
                    proposed = fh.read()
        return p.returncode, out, proposed

    def destroy(self):
        rmtree(self.base)


# (name, installed, target, extra args, check(rc, out, proposed) -> problem or None)
def expect(*must, rc=None, proposed=None, absent=()):
    def check(code, out, prop):
        for m in must:
            if m not in out:
                return "missing %r" % m
        for a in absent:
            if a in out:
                return "unexpected %r" % a
        if rc == "fail" and code == 0:
            return "exit 0 on a stop"
        if rc == 0 and code != 0:
            return "exit %d" % code
        if proposed is not None and prop != proposed:
            return "proposal differs from the expected file:\n%s" % prop
        return None
    return check


CASES = [
    ("lists_every_amendment_numbered", INSTALLED, "v1.1.0", [],
     expect("derived from v1.0.0", "LOCAL AMENDMENTS (3,", "AMENDMENT 1 -",
            "+amend_one_retired", "AMENDMENT 2 -", "+step_d_fixed_locally",
            "AMENDMENT 3 -", "+step_g_local", rc=0, absent=("DROP",))),
    ("without_drop_every_amendment_is_carried", INSTALLED, "v1.1.0", [],
     # The 84.16 defect, pinned so a fix cannot quietly make it look solved: the
     # retired line is in the proposal unless --drop names it.
     lambda code, out, prop: None if prop and "amend_one_retired" in prop
     else "the retired amendment was not carried without --drop"),
    ("drop_yields_target_plus_the_kept_amendment", INSTALLED, "v1.1.0",
     ["--drop", "1,2"],
     expect("AMENDMENT 1 (DROPPED)", "AMENDMENT 2 (DROPPED)", "MERGE CONFLICTS: 0",
            "DROP 1: BEHAVIOR CHANGE",
            "DROP 2: the v1.1.0 template changes this region too", rc=0,
            proposed=EXPECTED, absent=("AMENDMENT 3 (DROPPED)", "DROP 3"))),
    ("drop_of_an_unprinted_number_stops", INSTALLED, "v1.1.0", ["--drop", "4"],
     expect("NO SUCH AMENDMENT: [4]", rc="fail", absent=("PROPOSED FILE",))),
    ("drop_works_when_the_template_did_not_change", FILLED(V2) + "local\n", "v1.1.0",
     ["--drop", "1"],
     # Base and target are the same release: CURRENT would hide the retirement.
     expect("derived from v1.1.0", "DROP 1: BEHAVIOR CHANGE", rc=0,
            proposed=FILLED(V2), absent=("CURRENT",))),
    ("current_without_drop", FILLED(V2), "v1.1.0", [],
     expect("CURRENT:", rc=0, absent=("PROPOSED FILE",))),
    ("no_target_stops", INSTALLED, "v9.9.9", [],
     expect("NO TARGET:", rc="fail")),
]
UNCOMMITTED_CASE = ("uncommitted_script_stops", INSTALLED, "v1.1.0", [],
                    expect("UNCOMMITTED:", rc="fail"))

# The helper's own text, mutated. Each must break >= 1 case.
MUTATIONS = [
    ("drop_never_applied",
     "\"\".join(b_lines[o[1]:o[2]] if o in dropped else i_lines[o[3]:o[4]])",
     "\"\".join(i_lines[o[3]:o[4]])"),
    ("merge_reads_the_committed_file_not_the_dropped_one",
     '(("installed", committed), ("base", base)',
     '(("installed", installed), ("base", base)'),
    ("every_drop_reported_as_subsumed",
     "    if any(t1 <= i2 and i1 <= t2 for _, t1, t2, _, _ in t_ops):",
     "    if True:"),
    ("every_drop_reported_as_a_behavior_change",
     "    if any(t1 <= i2 and i1 <= t2 for _, t1, t2, _, _ in t_ops):",
     "    if False:"),
    ("unprinted_drop_number_accepted",
     "if drop - set(range(1, len(amends) + 1)):",
     "if False:"),
    ("current_hides_a_drop",
     "if base == new and not drop:",
     "if base == new:"),
    ("amendments_not_numbered",
     "    print(\"AMENDMENT %d%s - template lines",
     "    print(\"AMENDMENT%.0d%s - template lines"),
]


def run_case(helper_src, case):
    name, installed, target, extra, check = case
    b = Bench(helper_src, installed, uncommitted=(case is UNCOMMITTED_CASE))
    try:
        code, out, prop = b.run(target, *extra)
        return check(code, out, prop), out
    finally:
        b.destroy()


def case_pass(helper_src, verbose=True):
    failures = []
    for case in CASES + [UNCOMMITTED_CASE]:
        try:
            problem, out = run_case(helper_src, case)
        except Exception:
            problem, out = "crashed:\n" + traceback.format_exc(), ""
        if problem:
            failures.append((case[0], problem, out))
            if not verbose:
                break
        elif verbose:
            print("  %-48s ok" % case[0], flush=True)
    return failures


SDLC_TPL = os.path.join(REPO, "sdlc-kit", "templates", "SDLC.template.md")


def marker_problems(update_text, template_text):
    """84.18's fold markers: each must occur exactly once in SDLC.template.md, or the
    update's grep asks a question nobody can answer (absent) or answers it for the
    wrong rule (more than once). A template rewrite that drops a marker fails here."""
    lines = update_text.split("\n")
    start = next(i for i, l in enumerate(lines) if l.startswith("| Version | Rule | Marker |"))
    problems, rows = [], 0
    for l in lines[start + 2:]:
        if not l.startswith("|"):
            break
        cells = [c.strip() for c in l.strip("|").split("|")]
        marker = cells[2].strip("`")
        rows += 1
        n = template_text.count(marker)
        if n != 1:
            problems.append("%s %r occurs %d times in SDLC.template.md" % (cells[0], marker, n))
    if rows == 0:
        problems.append("no marker rows found")
    return rows, problems


def marker_pass():
    upd = io.open(UPDATE, encoding="utf-8").read()
    tpl = io.open(SDLC_TPL, encoding="utf-8").read()
    rows, problems = marker_problems(upd, tpl)
    print("== fold markers (%d rows) ==" % rows)
    for p in problems:
        print("  FAILED " + p)
    # The check must be seen to fail: a template that lost one rule's wording.
    victim = "inverting the edit that made it"
    _, neg = marker_problems(upd, tpl.replace(victim, "undoing the edit"))
    seen = any(victim in p for p in neg)
    print("  %-48s %s" % ("a marker the template lost is reported",
                          "ok" if seen else "FAILED"))
    return not problems and seen


def main():
    if not marker_pass():
        return 1
    src = helper_text()
    print("== case pass (%d cases) ==" % (len(CASES) + 1))
    failures = case_pass(src)
    if failures:
        for name, problem, out in failures:
            print("\nFAILED %s: %s\n--- output ---\n%s" % (name, problem, out))
        return 1
    print("\n== mutation pass (%d mutations) ==" % len(MUTATIONS))
    survived = []
    for name, old, new in MUTATIONS:
        if src.count(old) != 1:
            survived.append("%s (anchor found %d times - the mutation is stale)"
                            % (name, src.count(old)))
            print("  %-48s STALE" % name, flush=True)
            continue
        caught = case_pass(src.replace(old, new), verbose=False)
        if caught:
            print("  %-48s caught by %s" % (name, caught[0][0]), flush=True)
        else:
            survived.append(name)
            print("  %-48s SURVIVED" % name, flush=True)
    if survived:
        print("\nMUTATIONS SURVIVED: %s" % ", ".join(survived))
        return 1
    print("\nall green: %d cases, %d mutations caught"
          % (len(CASES) + 1, len(MUTATIONS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
