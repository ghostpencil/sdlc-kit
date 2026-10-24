#!/usr/bin/env python
"""Re-runnable proof for templates/sdlc-state.template.py (FEATURE_PLAN.md 89.5, 89.9).

Two passes, and the second is the point:

  1. a unit pass driving every verb of the helper against a temp repository per case:
     the transitions and their log, `status` composed from a fixture sdlc-tdd/ and index,
     the worktree form of `.git`, the `off`-while-in-flight refusal, and `resume` with and
     without a saved stage;
  2. a mutation pass that breaks the helper - one mutation per way it could lie, the count
     derived from the MUTATIONS list at run time, never stated here - and requires the
     unit pass to notice each one (invariant 13).

Kit-development artifact: lives at the root, never ships inside sdlc-kit/ (invariant 12).
Run from anywhere:  python tools/sdlc-state-check.py
"""
import io
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import traceback

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except (AttributeError, OSError):
    pass

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(REPO, "sdlc-kit", "templates", "sdlc-state.template.py")

INDEX = ("# Index\n\n## Phase — *bounded*\n\n**%s**\n\n## Other\n\n**not this one**\n")


def rmtree(path):
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
    def __init__(self, base, src):
        self.root = os.path.join(base, "proj")
        self.git = os.path.join(self.root, ".git")
        os.makedirs(os.path.join(self.root, ".github", "hooks"))
        os.makedirs(os.path.join(self.root, "spec"))
        os.makedirs(os.path.join(self.git, "sdlc-tdd"))
        self.helper = os.path.join(self.root, ".github", "hooks", "sdlc-state.py")
        io.open(self.helper, "w", encoding="utf-8", newline="\n").write(src)
        self.rc = None
        self.gd = self.git

    def index(self, line):
        io.open(os.path.join(self.root, "spec", "PROJECT_INDEX.md"), "w",
                encoding="utf-8").write(INDEX % line)

    def run(self, *args):
        e = dict(os.environ)
        e.pop("CLAUDE_PROJECT_DIR", None)
        e["SDLC_REPO_ROOT"] = self.root
        e.pop("PYTHONUTF8", None)
        e.pop("PYTHONIOENCODING", None)
        p = subprocess.run([sys.executable, "-B", self.helper] + list(args),
                           capture_output=True, env=e, cwd=self.root)
        self.rc = p.returncode
        return p.stdout.decode("utf-8", "replace").strip()

    def state_path(self):
        return os.path.join(self.gd, "sdlc-state")

    def state(self):
        try:
            return io.open(self.state_path(), encoding="utf-8").read()
        except OSError:
            return None

    def first(self):
        s = self.state()
        return s.splitlines()[0] if s else None

    def log(self):
        f = os.path.join(self.gd, "sdlc-state.log")
        if not os.path.exists(f):
            return []
        return [l for l in io.open(f, encoding="utf-8").read().splitlines() if l.strip()]

    def clear(self):
        for n in ("sdlc-state", "sdlc-state.log"):
            p = os.path.join(self.gd, n)
            if os.path.exists(p):
                os.remove(p)

    def tdd(self, name, mtime=None):
        p = os.path.join(self.gd, "sdlc-tdd", name)
        io.open(p, "w").write("x")
        if mtime is not None:
            os.utime(p, (mtime, mtime))


def guarded(label, default, fn, *a, **kw):
    """A crash REPORTS and the run continues; its exit code obligation is kept in
    guarded.crashed (the rule is FEATURE_PLAN.md 75.7 ruling 3)."""
    try:
        return fn(*a, **kw)
    except Exception:
        traceback.print_exc()
        print("CRASHED  %s  <-- pass did not complete; its remaining cases did not run"
              % label)
        guarded.crashed.append(label)
        return default


guarded.crashed = []


class _FirstFailure(BaseException):
    pass


def unit(src, verbose=True, counter=None, first_only=False):
    failures = []
    base = tempfile.mkdtemp(prefix="sdlc-state-")
    b = Bench(base, src)

    def case(name, cond, detail=""):
        if counter is not None:
            counter.append(name)
        if not cond:
            failures.append(name)
            if verbose:
                print("FAIL  %s%s" % (name, ("\n        " + detail) if detail else ""))
            if first_only:
                raise _FirstFailure()

    try:
        # --- status ---------------------------------------------------------
        b.index("BUILD — Phase 12 Foo (spec/PHASE_12_foo.md)")
        out = b.run("status")
        case("1 status on an absent file says so and composes the rest",
             b.rc == 0 and "state: absent - guards active by default" in out
             and "tdd: none observed this session" in out and "deny: logging" in out
             and "index: BUILD — Phase 12 Foo" in out and "not this one" not in out, out)

        b.tdd("deny-enabled")
        b.tdd("last-test-edit", 1000)
        b.tdd("red-observed", 2000)
        out = b.run("status")
        case("1b a red newer than the last test edit reads RED; deny reads armed",
             "tdd: RED" in out and "deny: armed" in out, out)
        b.tdd("green-observed", 3000)
        case("1c a green newer than the red reads GREEN", "tdd: GREEN" in b.run("status"))
        b.tdd("refactor-license", 3500)
        case("1d a refactor licence reads REFACTOR", "tdd: REFACTOR" in b.run("status"))
        b.tdd("close-out-license", 3600)
        case("1e a close-out licence reads CLOSE-OUT and outranks the refactor one",
             "tdd: CLOSE-OUT" in b.run("status"))
        shutil.rmtree(os.path.join(b.gd, "sdlc-tdd"))
        os.makedirs(os.path.join(b.gd, "sdlc-tdd"))
        b.tdd("last-test-edit", 5000)
        b.tdd("red-observed", 4000)
        case("1f a red OLDER than the last test edit is not a RED",
             "tdd: RED" not in b.run("status"))

        # --- set -----------------------------------------------------------
        b.clear()
        out = b.run("set", "slice", "--phase", "12", "--slice", "S4", "--by", "next-slice")
        s = b.state() or ""
        case("2 set writes the word, then keys, then since/by",
             b.rc == 0 and b.first() == "slice" and "phase: 12" in s and "slice: S4" in s
             and "since: 20" in s and "by: next-slice" in s, s)
        lg = b.log()
        case("2b set appends one log line naming the transition",
             len(lg) == 1 and "absent -> slice next-slice" in lg[0], repr(lg))
        b.run("set", "close-out", "--by", "end-slice")
        s = b.state() or ""
        case("2c a later set keeps the phase the state already held",
             b.first() == "close-out" and "phase: 12" in s and len(b.log()) == 2, s)
        b.clear()
        b.run("set", "phase", "--by", "plan-phase")
        case("2d set phase without --phase records stage: planning",
             b.first() == "phase" and "stage: planning" in (b.state() or ""), b.state() or "")
        before = b.state()
        out = b.run("set", "banana")
        case("2e an unknown state word is exit 2 and writes nothing",
             b.rc == 2 and b.state() == before and "state word" in out, out)

        # --- pause / resume ---------------------------------------------------
        b.clear()
        b.run("set", "slice", "--phase", "12", "--slice", "S4")
        out = b.run("pause")
        case("3 pause without a reason is exit 2 and writes nothing",
             b.rc == 2 and b.first() == "slice", out)
        out = b.run("pause", "dependency", "bump", "on", "main")
        s = b.state() or ""
        case("3b pause saves the word as stage:, keeps phase and slice, records the reason",
             b.rc == 0 and b.first() == "paused" and "stage: slice" in s
             and "phase: 12" in s and "slice: S4" in s
             and "reason: dependency bump on main" in s and "by: /sdlc pause" in s, s)
        out = b.run("pause", "again")
        case("3c pausing a paused state is exit 2", b.rc == 2 and "already paused" in out, out)
        b.run("resume")
        s = b.state() or ""
        case("3d resume restores stage: with its phase and slice, and logs it",
             b.first() == "slice" and "phase: 12" in s and "slice: S4" in s
             and "stage:" not in s and "paused -> slice" in b.log()[-1], s)
        b.clear()
        b.run("set", "off")
        out = b.run("pause", "nothing running")
        case("3e pausing an off state is exit 2 - nothing is in flight",
             b.rc == 2 and b.first() == "off" and "nothing is in flight" in out, out)
        b.clear()
        out = b.run("pause", "fresh clone")
        case("3f pausing an absent state saves stage: phase",
             b.rc == 0 and "stage: phase" in (b.state() or ""), out)
        # §91: any caller, with a reason - and the caller travels with the change.
        b.clear()
        b.run("set", "slice", "--phase", "12", "--slice", "S4")
        b.run("pause", "docs sweep, not the slice", "--by", "agent")
        s = b.state() or ""
        case("3g pause --by agent records the caller in the file and the log",
             b.first() == "paused" and "by: agent" in s
             and "-> paused agent — docs sweep, not the slice" in b.log()[-1], s)
        b.run("resume", "--by", "agent")
        case("3h resume --by agent is logged as the agent's",
             b.first() == "slice" and "paused -> slice agent" in b.log()[-1], b.log()[-1])

        # --- resume from the index --------------------------------------------
        for line, want in (("BUILD — Phase 12 Foo (spec/PHASE_12_foo.md)", "phase"),
                           ("BUILD — between phases. Phase 12 MERGED", "off"),
                           ("PRE-PHASE-1. Project scaffolded 2026-01-01", "off"),
                           ("STABILIZATION. SDLC adopted 2026-01-01", "phase")):
            b.clear()
            b.index(line)
            out = b.run("resume")
            case("4 resume with no saved stage reads the index: %s -> %s" % (line[:24], want),
                 b.rc == 0 and b.first() == want and "chosen from the index" in out, out)
        b.clear()
        b.index("something unreadable")
        out = b.run("resume")
        case("4b resume with no stage and an unreadable index is exit 2, writes nothing",
             b.rc == 2 and b.state() is None, out)
        b.clear()
        b.run("set", "slice", "--phase", "1", "--slice", "S1")
        out = b.run("resume")
        case("4c resume on an unpaused state changes nothing",
             b.first() == "slice" and "nothing to resume" in out, out)

        # --- off -------------------------------------------------------------
        b.clear()
        b.run("set", "slice", "--phase", "12", "--slice", "S4")
        out = b.run("off", "done for today")
        case("5 off while an arc is in flight is exit 2 with the way out, and writes nothing",
             b.rc == 2 and b.first() == "slice" and "--force" in out and "phase 12" in out, out)
        b.run("pause", "tidy")
        out = b.run("off", "done for today")
        case("5b off while PAUSED over a slice refuses too",
             b.rc == 2 and b.first() == "paused", out)
        b.run("off", "done for today", "--force", "--by", "agent")
        case("5c off --force writes off, and the log keeps the abandoned stage and the caller",
             b.first() == "off" and b.rc == 0
             and "paused -> off agent — done for today (in flight: slice)" in b.log()[-1],
             b.log()[-1])
        b.clear()
        b.run("off", "fresh clone, nothing running")
        case("5d off from an absent state writes without asking",
             b.first() == "off" and b.rc == 0)
        b.run("set", "phase", "--phase", "3")
        out = b.run("off", "done")
        case("5e off from `phase` also refuses - an arc is in flight",
             b.rc == 2 and b.first() == "phase", out)
        # §91: a reason is required from every caller, the owner included.
        b.clear()
        out = b.run("off")
        case("5f off without a reason is exit 2 and writes nothing (who and why are logged)",
             b.rc == 2 and b.state() is None and "needs a reason" in out, out)
        b.run("set", "slice", "--phase", "1", "--slice", "S1")
        out = b.run("off", "--force")
        case("5g ...and --force does not excuse the reason",
             b.rc == 2 and b.first() == "slice" and "needs a reason" in out, out)

        # --- file hygiene -------------------------------------------------------
        b.clear()
        b.run("set", "off", "--reason", "café → 日本")
        out = b.run("status")
        case("6 a non-ASCII reason round-trips (UTF-8 on every open)",
             "café → 日本" in out and b.rc == 0, out)
        case("6b no bytecode is dropped beside the helper",
             not os.path.isdir(os.path.join(b.root, ".github", "hooks", "__pycache__")))
        io.open(b.state_path(), "w", encoding="utf-8").write("PAUSED\nstage: slice\n")
        out = b.run("status")
        case("6c a word in capitals is read as its lowercase form", "state: paused" in out, out)
        io.open(b.state_path(), "w", encoding="utf-8").write("pausd\n")
        out = b.run("status")
        case("6d an unrecognized word is reported as one the hooks guard on",
             "unrecognized" in out and "hooks guard" in out, out)

        # --- worktree -------------------------------------------------------
        wt = os.path.join(base, "wt")
        gd = os.path.join(base, "main-git", "worktrees", "wt")
        os.makedirs(os.path.join(gd, "sdlc-tdd"))
        os.makedirs(os.path.join(wt, ".github", "hooks"))
        os.makedirs(os.path.join(wt, "spec"))
        io.open(os.path.join(wt, ".github", "hooks", "sdlc-state.py"), "w",
                encoding="utf-8", newline="\n").write(src)
        io.open(os.path.join(wt, ".git"), "w", encoding="utf-8").write(
            "gitdir: %s\n" % gd.replace("\\", "/"))
        e = dict(os.environ)
        e["SDLC_REPO_ROOT"] = wt
        p = subprocess.run([sys.executable, "-B",
                            os.path.join(wt, ".github", "hooks", "sdlc-state.py"),
                            "set", "slice", "--phase", "2", "--slice", "S1"],
                           capture_output=True, env=e, cwd=wt)
        written = os.path.join(gd, "sdlc-state")
        case("7 a worktree's .git FILE resolves to its git directory",
             p.returncode == 0 and os.path.exists(written)
             and io.open(written, encoding="utf-8").read().startswith("slice"),
             p.stdout.decode() + p.stderr.decode())
        case("7b ...and nothing is written into the worktree itself",
             not os.path.exists(os.path.join(wt, "sdlc-state")))

        # --- fail direction -----------------------------------------------------
        out = b.run("frobnicate")
        case("8 an unknown verb is exit 2, not a silent success", b.rc == 2, out)
        e = dict(os.environ)
        e.pop("SDLC_REPO_ROOT", None)
        e.pop("CLAUDE_PROJECT_DIR", None)
        empty = tempfile.mkdtemp(prefix="sdlc-state-nogit-")
        try:
            p = subprocess.run([sys.executable, "-B", b.helper, "status"],
                               capture_output=True, env=e, cwd=empty)
            case("8b outside a repository root it is exit 2 with a stated reason",
                 p.returncode == 2 and b"no .git" in p.stdout, p.stdout.decode())
        finally:
            rmtree(empty)
    except _FirstFailure:
        pass
    finally:
        rmtree(base)
    return failures


# One mutation per way the helper could lie; the unit pass must notice each. The suite
# fails if any mutation survives (invariant 13).
MUTATIONS = [
    ("a set that does not log (a retro cannot count pauses, /end-slice cannot see a "
     "forgotten one)",
     'with open(os.path.join(gd, LOG_FILE), "a", encoding="utf-8", newline="\\n") as f:',
     'with open(os.devnull, "a", encoding="utf-8", newline="\\n") as f:'),
    ("a resume that ignores stage: (it restores nothing and falls through to the index)",
     'if word == "paused" and stage in WORDS and stage != "paused":',
     "if False:"),
    ("an off that never asks while an arc is in flight",
     'if over not in (None, "off", "absent") and not opts.get("force"):',
     "if False:"),
    ("an off that needs no reason (who asked, and why, are lost to the retro)",
     '''raise Fail('off needs a reason: off "<reason>" (who and why are logged)')''',
     "pass"),
    ("a pause that is allowed on an off state (nothing is in flight to suspend)",
     'if word == "off":\n        raise Fail("nothing is in flight',
     'if False:\n        raise Fail("nothing is in flight'),
    ("a set that accepts any word (a typo is written, and the hooks guard on it)",
     "rest[0] not in WORDS",
     "False"),
    ("a pause that forgets the saved stage",
     'new["stage"] = word if word in WORDS else "phase"',
     'new["stage"] = "phase"'),
    ("a red older than the last test edit still reads RED",
     "(edit is None or red > edit)",
     "True"),
    ("a licence that does not outrank the other (close-out read as refactor)",
     'if mt("close-out-license") is not None:\n        return "CLOSE-OUT"',
     'if False:\n        return "CLOSE-OUT"'),
    ("a worktree .git file read as a plain directory (the state lands nowhere)",
     "    g = line[len(\"gitdir:\"):].strip().replace(\"\\\\\", \"/\")",
     "    g = os.path.join(root, \"nowhere\")"),
    ("a helper that writes the locale's encoding (a non-cp1252 reason crashes it)",
     'with open(os.path.join(gd, STATE_FILE), "w", encoding="utf-8", newline="\\n") as f:',
     'with open(os.path.join(gd, STATE_FILE), "w", newline="\\n") as f:'),
]


def main():
    src = io.open(TPL, encoding="utf-8", newline="").read()
    names = []
    failures = guarded("unit pass", [], unit, src, counter=names)
    print("unit pass: %d/%d cases green" % (len(names) - len(failures), len(names)))
    if failures:
        print("FAILED unit cases:")
        for f in failures:
            print("  " + f)
        return 1
    survived, stale = [], []
    for label, old, new in MUTATIONS:
        if old not in src:
            stale.append(label)
            print("STALE    %s - anchor no longer applies, re-point it" % label)
            continue
        caught = guarded("mutation: %s" % label, [], unit, src.replace(old, new, 1),
                         verbose=False, first_only=True)
        if caught:
            print("caught   %s\n           (by: %s)" % (label, "; ".join(caught[:3])))
        else:
            survived.append(label)
            print("SURVIVED %s" % label)
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
