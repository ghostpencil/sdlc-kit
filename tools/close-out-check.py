# -*- coding: utf-8 -*-
"""Re-runnable proof for templates/close-out.template.sh (FEATURE_PLAN.md §46, §67, §88).

Four passes, and the last is the point:

  1. a unit pass driving check mode over a fixture corpus of real commit bodies -
     every stated-skip form, the RED zero-form, each key missing / empty /
     duplicated, a mid-line key lookalike, a CRLF body, a pre-0.38.0 quality: line
     (ignored, single or doubled), the retired stop-check mode (silent, exit 0), and
     two verbatim record bodies from the first adopter's armed arcs (ai-news-dashboard
     S6/S7) in BOTH directions - as filed, where they fail on the 0.27.0 lenses: key
     alone, and with that line added, where they pass - each case committed into a
     bench git repo and checked through the script's real interface;
  2. a docs pass driving docs-check mode (the §67.3 observer) over per-case
     bench repos with real file writes, since the observer counts lines a commit
     actually added - under budget, exactly at it, over it, an index the commit
     never touched, a retirement commit that only deletes, an explicit ref, and
     a bad ref (which must still exit 0: log-only never fails a step);
  3. a worktree pass: docs-check from a REAL linked worktree, whose .git is a file;
  4. a mutation pass that breaks the checker - the count derived from the
     MUTATIONS list at run time, never stated here - and requires pass 1, 2 or 3
     to notice each one. A suite that survives its own mutations is not testing the
     thing it claims to (invariant 13).

The stop pass (stop-check, the §52 backstop) and its launcher cases went with the mode
in 0.38.0 (FEATURE_PLAN.md §87.7). Only the stub's silence is pinned now.

Kit-development artifact: lives at the root, never ships inside sdlc-kit/.
Run from anywhere:  python tools/close-out-check.py
"""
import concurrent.futures, io, os, shutil, stat, subprocess, sys, tempfile, time, traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(REPO, "sdlc-kit", "templates", "close-out.template.sh")

FULL_TAIL = (
    "lenses: no lens triggered\n"
    "mutation: 1 guard, seen to fail\n"
    "verify: ran — behavior exercised through the CLI, verdict green (Git Bash)\n")

ADOPTER_S7 = """feat(web): mobile responsiveness for dashboard and detail pages (S7)

Add viewport meta tags to dashboard and item-detail templates so mobile
browsers scale to device width.

RED: mvn -q test -Dtest=DashboardControllerTest#dashboardIncludesMobileViewportMeta — DashboardControllerTest.java:84 — exit 1
RED: mvn -q test -Dtest=DashboardControllerTest#detailIncludesMobileViewportMeta — DashboardControllerTest.java:291 — exit 1
RED: mvn -q test -Dtest=DashboardStylesheetTest — DashboardStylesheetTest.java:17 — exit 1
quality: nothing to do
mutation: 3 guards checked (dashboard viewport, detail viewport, mobile media query), each seen to fail
verify: ran — dashboard page serves viewport meta; detail page serves viewport meta; CSS serves @media (max-width: 480px) rule

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
"""

ADOPTER_S6 = """fix(stabilization): S6 dead-artifact cleanup and malformed URL key corruption

- Remove unused SourceRefreshStatus entity + repository
- Fix AbstractLabRssAdapter so malformed canonical URLs are skipped with a WARN

RED: mvn -q test -Dtest=OpenAiAdapterTest -- OpenAiAdapterTest.skipsEntryWithMalformedCanonicalUrlInsteadOfCorruptingStableKey:56 Expecting empty but was: [CandidateItem[...]] -- exit 1
quality: nothing to do
mutation: 1 guard, seen to fail
verify: app boot + dashboard observed working; malformed URL behavior not exercised through real caller (no production seam to inject malformed feed)

Co-authored-by: Copilot <223556219+Copilot@users.noreply.github.com>
"""


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


def body(subject, *record):
    return subject + "\n\nProse about what and why.\n\n" + "\n".join(record) + "\n"


# (name, commit body or None to reuse the last commit, argv after the script path,
#  expected exit, expected first output line or None, must-contain substrings)
CASES = [
    ("observed_two_red",
     body("feat(x): two behaviors",
          "RED: pytest -q tests/test_a.py::test_one — test_a.py:12 — exit 1",
          "RED: pytest -q tests/test_a.py::test_two — test_a.py:31 — exit 1",
          "lenses: shared state under concurrency: clean",
          "mutation: 2 guards, each seen to fail",
          "verify: ran — CLI path green (Git Bash)"),
     ["check"], 0,
     "close-out record: COMPLETE - RED(2) lenses mutation verify - structural presence only; this does not verify the evidence is true.",
     []),
    ("red_not_observed_form",
     body("fix(y): hotfix", "RED: not observed — regression pinned by existing test",
          *FULL_TAIL.splitlines()),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("red_zero_form",
     body("docs(z): config-only slice", "RED: none — no behavior batches this slice",
          "lenses: no lens triggered",
          "mutation: none — no new guards",
          "verify: skipped — docs only, the gate fully pins it"),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("all_skip_forms",
     body("chore(w): mechanical sweep", "RED: none — no behavior batches this slice",
          "lenses: no lens triggered",
          "mutation: none — no new guards", "verify: skipped — covered by the gate"),
     ["check"], 0, None, ["COMPLETE"]),
    # A record written before 0.38.0 carries a quality: line. The checker no longer
    # counts it - present, doubled or empty - so a pre-0.38.0 commit reads exactly as
    # its other four keys say. Doubled and empty are the two forms a counted key
    # would fail on, which is what makes these cases discriminate.
    ("legacy_quality_line_ignored",
     body("feat(x): pre-0.38.0 slice", "RED: not observed — reason",
          "quality: 2 moves applied; reuse: searched helpers",
          *FULL_TAIL.splitlines()),
     ["check"], 0,
     "close-out record: COMPLETE - RED(1) lenses mutation verify - structural presence only; this does not verify the evidence is true.",
     []),
    ("legacy_quality_doubled_and_empty_ignored",
     body("feat(x): pre-0.38.0 slice", "RED: not observed — reason",
          "quality: 1 move applied", "quality:", *FULL_TAIL.splitlines()),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("missing_red",
     body("feat(x): s", "lenses: no lens triggered",
          "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED",
     ["MISSING -", "Never invent", "git commit --amend"]),
    ("missing_lenses",
     body("feat(x): s", "RED: not observed — reason",
          "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: lenses", ["MISSING -"]),
    ("missing_mutation",
     body("feat(x): s", "RED: not observed — reason",
          "lenses: no lens triggered", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: mutation", ["MISSING -"]),
    ("missing_verify",
     body("feat(x): s", "RED: not observed — reason",
          "lenses: no lens triggered", "mutation: none — no new guards"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: verify", ["MISSING -"]),
    ("empty_red_payload",
     body("feat(x): s", "RED:",
          "lenses: no lens triggered", "mutation: none — no new guards",
          "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED", ["EMPTY -"]),
    ("empty_lenses_payload",
     body("feat(x): s", "RED: not observed — reason",
          "lenses:  ", "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: lenses", ["EMPTY -"]),
    ("empty_verify_payload",
     body("feat(x): s", "RED: not observed — reason",
          "lenses: no lens triggered", "mutation: none — no new guards",
          "verify:   "),
     ["check"], 1, "close-out record: INCOMPLETE - problems: verify", ["EMPTY -"]),
    ("duplicated_mutation",
     body("feat(x): s", "RED: not observed — reason", "lenses: no lens triggered",
          "mutation: 1 guard, seen to fail", "mutation: none — no new guards",
          "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: mutation",
     ["DUPLICATED (2 lines)"]),
    ("duplicated_lenses",
     # Two review passes each writing their own verdict line: nobody knows which
     # is the record, and the denominator this key exists for is the casualty.
     body("feat(x): s", "RED: not observed — reason",
          "lenses: untrusted input: clean", "lenses: no lens triggered",
          "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: lenses",
     ["DUPLICATED (2 lines)"]),
    ("anchors_midline_lookalikes_do_not_count",
     # Prose names "RED:" and "lenses:" mid-line. RED has no real line, so it must
     # read as missing. lenses: DOES have a real line below, so with the anchor
     # intact it reads as present-once - and if the anchor were dropped the prose
     # mention would make it duplicated, which pins the anchor for that key too.
     "feat(x): s\n\nCopy the RED: lines and the lenses: line\n"
     "from the record.\n\n"
     "lenses: no lens triggered\nmutation: none — no new guards\n"
     "verify: skipped — small\n",
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED", []),
    ("lookalikes_beside_full_record",
     body("feat(x): s", "Per the record contract the RED: and lenses: lines follow.",
          "RED: not observed — reason", *FULL_TAIL.splitlines()),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("crlf_body",
     body("feat(x): windows shell", "RED: not observed — reason",
          *FULL_TAIL.splitlines()).replace("\n", "\r\n"),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("multi_red_mixed",
     body("feat(x): three batches",
          "RED: pytest -q — t.py:1 — exit 1", "RED: not observed — flaky fixture",
          "RED: pytest -q — t.py:9 — exit 2", *FULL_TAIL.splitlines()),
     ["check"], 0, None, ["COMPLETE - RED(3)"]),
    # Real field bodies, kept verbatim. Both predate the lenses: key (0.27.0), so
    # both are INCOMPLETE on exactly that one line and nothing else - their
    # quality: line, from before 0.38.0, is ignored. Editing the field evidence to
    # make the suite green would delete the only proof that the failure is narrow.
    ("adopter_s7_verbatim_pre_lenses", ADOPTER_S7, ["check"], 1,
     "close-out record: INCOMPLETE - problems: lenses",
     ["RED:      present (3 lines)", "mutation: present", "verify:   present"]),
    ("adopter_s6_verbatim_pre_lenses", ADOPTER_S6, ["check"], 1,
     "close-out record: INCOMPLETE - problems: lenses",
     ["RED:      present (1 lines)", "verify:   present"]),
    # The same two bodies with the line their next slice will carry: the forward
    # direction, so the pair proves the key discriminates rather than just fails.
    ("adopter_s7_verbatim_lensed",
     ADOPTER_S7.replace("quality: nothing to do\n",
                        "quality: nothing to do\nlenses: no lens triggered\n"),
     ["check"], 0, None, ["COMPLETE - RED(3)"]),
    ("adopter_s6_verbatim_lensed",
     ADOPTER_S6.replace("quality: nothing to do\n",
                        "quality: nothing to do\n"
                        "lenses: the unconsumed artifact: SourceRefreshStatus, "
                        "no production consumer\n"),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("no_record_at_all", "feat(x): subject only\n\nProse.\n",
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED lenses mutation verify", []),
    # The retired stop-time backstop. A Stop launcher left by a 0.22.0-0.37.1
    # install still calls this mode; it must print nothing and exit 0, because an
    # unknown mode exits 2 and a Stop hook exiting 2 blocks every stop.
    ("stop_check_retired_is_silent", None, ["stop-check"], 0, "", []),
    ("bad_ref", None, ["check", "no-such-ref"], 2, None,
     ["CANNOT CHECK -", "does not resolve"]),
    ("unknown_mode", None, ["frob"], 2, None, ["CANNOT CHECK -", "unknown mode 'frob'"]),
    ("no_mode", None, [], 2, None, ["CANNOT CHECK -", "unknown mode ''"]),
]

# One mutation per defect class the corpus pins; each must break >= 1 case.
MUTATIONS = [
    ("anchor_dropped_RED", "/^RED:/      { rn++;", "/RED:/      { rn++;"),
    ("anchor_dropped_lenses", "/^lenses:/   { ln++;", "/lenses:/   { ln++;"),
    ("empty_check_disabled", "if ($0 ~ /^RED:[[:space:]]*$/) re++", ""),
    ("duplicate_check_disabled", '[ "$n" -gt 1 ]', '[ "$n" -gt 99 ]'),
    ("incomplete_exits_zero", "exit 1\n", "exit 0\n"),
    ("missing_not_recorded", 'line="MISSING - $AMEND"; bad="$bad $k"',
     'line="MISSING - $AMEND"'),
    ("ref_guard_bypassed", '--verify --quiet "$REF^{commit}"', "--verify --quiet HEAD"),
    ("mode_gate_loosened", '[ "$MODE" = "check" ]', '[ -n "$MODE" ]'),
    ("red_treated_singleton", "status 'RED:     ' RED      \"$red_n\" \"$red_e\" \"\"",
     "status 'RED:     ' RED      \"$red_n\" \"$red_e\" s"),
    # --- the retired stop-check (§87.7): the stub must keep a leftover launcher silent.
    ("stop_stub_removed", '[ "$MODE" = "stop-check" ] && exit 0\n', ""),
    # --- linked worktrees (FEATURE_PLAN.md 78).
    ("docs_log_under_literal_dotgit", '"$MSG" >> "$GD/sdlc-close-out/log" 2>/dev/null',
     '"$MSG" >> .git/sdlc-close-out/log 2>/dev/null'),
    # --- docs-check (§67.3). Each models a plausible observer defect.
    ("docs_budget_relaxed", "  BUDGET=25 ", "  BUDGET=9999 "),
    ("docs_boundary_off_by_one", '[ "$ADDED" -gt "$BUDGET" ]', '[ "$ADDED" -ge "$BUDGET" ]'),
    ("docs_counts_deletions", "NR==1 { print $1 }", "NR==1 { print $2 }"),
    ("docs_ignores_ref_arg", "  REF=${2:-HEAD}", "  REF=HEAD"),
    ("docs_untouched_index_not_detected", 'if [ -z "$ADDED" ]; then', 'if [ -z "not empty" ]; then'),
    ("docs_pathspec_dropped", 'git show --numstat --format= "$REF" -- "$IDX"',
     'git show --numstat --format= "$REF"'),
]


class Bench:
    def __init__(self, base, src):
        self.root = os.path.join(base, "proj")
        script_dir = os.path.join(self.root, ".github", "hooks")
        os.makedirs(script_dir)
        self.script = os.path.join(script_dir, "sdlc-close-out.sh")
        assert "{{" not in src, "the template must carry no placeholders (copied verbatim)"
        io.open(self.script, "w", encoding="utf-8", newline="\n").write(src)
        self.git("init", "-q")
        self.git("config", "user.email", "bench@example.invalid")
        self.git("config", "user.name", "bench")

    def git(self, *args, **kw):
        return subprocess.run(["git", "-C", self.root] + list(args),
                              capture_output=True, **kw)

    def commit(self, message):
        p = self.git("commit", "--allow-empty", "--cleanup=verbatim", "-F", "-",
                     input=message.encode("utf-8"))
        assert p.returncode == 0, "bench commit failed: " + p.stderr.decode()

    via_powershell = False  # S4: same corpus through a PowerShell -> sh chain. This
                            # proves dialect agreement, not the Copilot environment:
                            # its shell tool resolves no bare `sh` (measured
                            # 2026-08-10), so the git-derived sh.exe form the docs
                            # mandate was proven separately, live in a Copilot
                            # session (FEATURE_PLAN.md 46.7).

    def run(self, args):
        t0 = time.perf_counter()
        if self.via_powershell:
            cmd = "sh '%s'%s; exit $LASTEXITCODE" % (
                self.script, "".join(" '%s'" % a for a in args))
            argv = ["powershell", "-NoProfile", "-Command", cmd]
        else:
            argv = ["sh", self.script] + args
        p = subprocess.run(argv, cwd=self.root, capture_output=True)
        return p.returncode, p.stdout.decode("utf-8", "replace"), time.perf_counter() - t0


class DocsBench(Bench):
    """A per-case repo for docs-check: real file writes, because the observer
    counts the lines a commit actually added - an --allow-empty bench commit
    (what the unit pass uses) has no numstat at all."""

    IDX = "spec/PROJECT_INDEX.md"

    def write_index(self, lines):
        path = os.path.join(self.root, "spec", "PROJECT_INDEX.md")
        d = os.path.dirname(path)
        if not os.path.isdir(d):
            os.makedirs(d)
        io.open(path, "w", encoding="utf-8", newline="\n").write(
            "".join(x + "\n" for x in lines))

    def add_commit(self, message):
        self.git("add", "-A")
        p = self.git("commit", "--cleanup=verbatim", "-F", "-",
                     input=message.encode("utf-8"))
        assert p.returncode == 0, "bench commit failed: " + p.stderr.decode()

    def log_text(self):
        log = os.path.join(self.root, ".git", "sdlc-close-out", "log")
        return io.open(log, encoding="utf-8").read() if os.path.exists(log) else ""


def _d_seed(b, n=1):
    b.write_index(["seed %d" % i for i in range(n)])
    b.add_commit("chore: seed the index\n")


def _d_under(b):
    _d_seed(b)
    b.write_index(["seed 0"] + ["backlog entry %d" % i for i in range(3)])
    b.add_commit("docs: PROJECT_INDEX - S1 done; next up S2\n")
    return ["docs-check"]

def _d_at_budget(b):
    # Exactly the budget is not over it: the observer flags growth PAST 25.
    _d_seed(b)
    b.write_index(["seed 0"] + ["entry %d" % i for i in range(25)])
    b.add_commit("docs: PROJECT_INDEX - S1 done; a heavy but legitimate close\n")
    return ["docs-check"]

def _d_over(b):
    # The measured shape: a per-slice write-up landing in the index.
    _d_seed(b)
    b.write_index(["seed 0"] + ["write-up line %d" % i for i in range(44)])
    b.add_commit("docs: PROJECT_INDEX - S1 done\n")
    return ["docs-check"]

def _d_untouched(b):
    _d_seed(b)
    io.open(os.path.join(b.root, "other.md"), "w", newline="\n").write("x\n")
    b.add_commit("chore: a commit that never touches the index\n")
    return ["docs-check"]

def _d_deletions_not_counted(b):
    # The retirement commit's shape: 58 lines out, none in. Not a budget event.
    _d_seed(b, 60)
    b.write_index(["seed 0", "seed 1"])
    b.add_commit("docs: retire closed items to PROJECT_INDEX_HISTORY.md\n")
    return ["docs-check"]

def _d_explicit_ref(b):
    # HEAD is small, HEAD~1 is over: the named ref must be the one read.
    _d_seed(b)
    b.write_index(["seed 0"] + ["w %d" % i for i in range(44)])
    b.add_commit("docs: the over-budget close\n")
    b.write_index(["seed 0"] + ["w %d" % i for i in range(44)] + ["one more line"])
    b.add_commit("docs: the small close\n")
    return ["docs-check", "HEAD~1"]

def _d_bad_ref(b):
    _d_seed(b)
    return ["docs-check", "no-such-ref"]


# (name, setup(bench) -> argv, stdout must-contain, stdout must-NOT-contain)
DOCS_CASES = [
    ("docs_under_budget", _d_under,
     ["docs budget: OK - 3 lines added"], ["OVER", "n/a"]),
    ("docs_at_budget_is_not_over", _d_at_budget,
     ["docs budget: OK - 25 lines added"], ["OVER"]),
    ("docs_over_budget_flags", _d_over,
     ["docs budget: OVER - 44 lines added", "against a budget of 25",
      "Log-only - nothing is blocked"], ["OK -"]),
    ("docs_index_untouched", _d_untouched,
     ["docs budget: n/a", "does not touch spec/PROJECT_INDEX.md"], ["OVER", "OK -"]),
    ("docs_deletions_are_not_additions", _d_deletions_not_counted,
     ["docs budget: OK - 0 lines added"], ["OVER"]),
    ("docs_explicit_ref_is_read", _d_explicit_ref,
     ["docs budget: OVER - 44 lines added"], ["OK -"]),
    ("docs_bad_ref_still_exits_zero", _d_bad_ref,
     ["docs budget: CANNOT CHECK", "log-only"], ["OVER", "OK -"]),
]


def docs_pass(src, verbose, first_only=False):
    """Runs every docs case in its own bench repo; returns (failures, slowest), and
    leaves the median in docs_pass.median - the number the S2 verdict reads.
    first_only stops at the first failing case: the mutation pass needs one.

    Every case asserts exit 0: this mode is log-only, so a non-zero exit would
    fail an /end-slice step over a bookkeeping observation - the one thing the
    §67.3 ruling forbids it to do."""
    failures, slowest, times = [], 0.0, []
    for name, setup, contains, absent in DOCS_CASES:
        with tempfile.TemporaryDirectory() as base:
            b = DocsBench(base, src)
            argv = setup(b)
            code, out, dt = b.run(argv)
            slowest = max(slowest, dt)
            times.append(dt)
            problems = []
            if code != 0:
                problems.append("exit %d, expected 0 (docs-check is log-only)" % code)
            for c in contains:
                if c not in out:
                    problems.append("output lacks %r" % c)
            for c in absent:
                if c in out:
                    problems.append("output wrongly contains %r" % c)
            # Whatever it printed, it also has to leave in the log - the record
            # a later session reads is the log, not this session's scrollback.
            if "CANNOT CHECK" not in out and out.strip() not in b.log_text():
                problems.append("verdict not appended to .git/sdlc-close-out/log")
            if problems:
                failures.append((name, problems, out))
            if verbose:
                print("  %-38s %s" % (name, "FAIL: " + "; ".join(problems) if problems else "ok"))
            if problems and first_only:
                break
    times.sort()
    docs_pass.median = times[len(times) // 2] if times else 0.0
    return failures, slowest


docs_pass.median = 0.0


def unit_pass(src, verbose, first_only=False):
    """Runs every case; returns (failures, max_seconds). first_only stops at the first
    failing case. The cases share one bench and its growing history, so stopping
    early only ever drops later cases - it never changes an earlier verdict."""
    failures, slowest, times = [], 0.0, []
    with tempfile.TemporaryDirectory() as base:
        b = Bench(base, src)
        # One uncounted warmup: the first sh spawn on Windows pays a cold-start
        # cost that says nothing about the script (S2 is measured warm, the
        # 31.8 precedent). Its cold time is still reported by main().
        b.commit("warmup\n\nRED: x\nquality: x\nmutation: x\nverify: x\n")
        _, _, unit_pass.cold = b.run(["check"])
        for name, message, args, exp_exit, exp_first, contains in CASES:
            if message is not None:
                b.commit(message)
            code, out, dt = b.run(args)
            slowest = max(slowest, dt)
            times.append(dt)
            first = out.splitlines()[0] if out.splitlines() else ""
            problems = []
            if code != exp_exit:
                problems.append("exit %d, expected %d" % (code, exp_exit))
            if exp_first is not None and first != exp_first:
                problems.append("first line %r, expected %r" % (first, exp_first))
            for c in contains:
                if c not in out:
                    problems.append("output lacks %r" % c)
            if problems:
                failures.append((name, problems, out))
            if verbose:
                print("  %-38s %s" % (name, "FAIL: " + "; ".join(problems) if problems else "ok"))
            if problems and first_only:
                break
    times.sort()
    unit_pass.median = times[len(times) // 2] if times else 0.0
    return failures, slowest


unit_pass.median = 0.0


# --- linked worktrees (FEATURE_PLAN.md 78) -----------------------------------------
# Every other pass builds an ordinary checkout, whose .git is a directory - the one
# configuration that cannot see this defect. In a linked worktree .git is a FILE
# naming the git directory, and the script once kept its state under a literal .git/
# that is not a directory there. This case builds a REAL worktree with git.


def wt_pass(src, verbose):
    """Returns (failures, 0.0) in the shape the other passes use."""
    failures = []

    def check(name, cond, detail=""):
        if verbose:
            print("  %-52s %s" % (name, "ok" if cond else "FAILED"))
        if not cond:
            failures.append((name, ["expectation not met"], detail))

    base = tempfile.mkdtemp(prefix="closeout-wt-")
    try:
        main_r = os.path.join(base, "main")
        wt_r = os.path.join(base, "wt")
        os.makedirs(main_r)
        g = lambda *a, **k: subprocess.run(["git"] + list(a), capture_output=True, **k)
        g("init", "-q", main_r)
        g("-C", main_r, "-c", "user.email=b@b", "-c", "user.name=b",
          "commit", "-q", "--allow-empty", "-m", "chore: base")
        g("-C", main_r, "worktree", "add", "-q", wt_r, "-b", "wt")
        gd = g("-C", wt_r, "rev-parse", "--absolute-git-dir").stdout.decode().strip()
        script = os.path.join(wt_r, ".github", "hooks", "sdlc-close-out.sh")
        os.makedirs(os.path.dirname(script))
        io.open(script, "w", encoding="utf-8", newline="\n").write(src)

        idx = os.path.join(wt_r, "spec", "PROJECT_INDEX.md")
        os.makedirs(os.path.dirname(idx))
        io.open(idx, "w", newline="\n").write("a\nb\nc\n")
        g("-C", wt_r, "add", "spec/PROJECT_INDEX.md")
        g("-C", wt_r, "-c", "user.email=b@b", "-c", "user.name=b", "commit", "-q",
          "-m", "docs: close")
        p = subprocess.run(["sh", script, "docs-check"], cwd=wt_r, capture_output=True)
        f = os.path.join(gd, "sdlc-close-out", "log")
        log = io.open(f, encoding="utf-8").read() if os.path.exists(f) else ""
        check("wt_docs_check_logs_to_worktree_gitdir",
              p.returncode == 0 and "docs budget: OK - 3 lines added" in log
              and not os.path.exists(os.path.join(main_r, ".git", "sdlc-close-out")), log)
    finally:
        rmtree(base)
    return failures, 0.0


def main():
    src = io.open(TPL, encoding="utf-8").read()

    if "--via-powershell" in sys.argv:
        # S4 dialect run: unit corpus only (mutations re-prove nothing new here),
        # no S2 assert - the extra powershell spawn is the harness's cost, not
        # the script's.
        Bench.via_powershell = True
        print("== S4 unit pass via powershell -> sh (%d cases) ==" % len(CASES))
        failures, slowest = guarded("S4 unit pass", ([], 0.0), unit_pass, src, verbose=True)
        print("slowest invocation incl. powershell spawn: %.0f ms" % (slowest * 1000))
        if failures:
            for name, problems, out in failures:
                print("\nFAILED %s: %s\n--- output ---\n%s" % (name, "; ".join(problems), out))
            sys.exit(1)
        if guarded.crashed:
            print("\nCRASHED passes: %s - those cases did not run"
                  % ", ".join(guarded.crashed))
            sys.exit(1)
        print("\nS4 green: %d cases, verdicts identical to the direct-sh pass" % len(CASES))
        return

    # Perf breaches accumulate and reach the exit code only at the END. They used to
    # exit the moment a budget was missed, which on a loaded machine ended the run
    # before the mutation pass — the only pass that tests whether the corpus can detect
    # a defect at all. A timing wobble silently switched off invariant 13's instrument,
    # three times in one day (FEATURE_PLAN.md §71). Correctness and speed are different
    # verdicts, and one must not be able to suppress the other.
    perf = []

    print("== unit pass (%d cases) ==" % len(CASES))
    failures, slowest = guarded("unit pass", ([], 0.0), unit_pass, src, verbose=True)
    # The verdict reads the MEDIAN, as the retired stop pass's did since §77: this machine adds
    # about one +5 s stall per suite run, landing on a random case, and a max over the
    # unit pass's ~26 samples catches it nearly every time. Ruled 2026-09-04 (§77.7) to
    # apply on this pass's first breach - which came at 0.32.0, 5340 ms slowest against
    # a sub-second typical. The slowest stays printed: a real regression moves both.
    print("median warm invocation: %.0f ms (S2 budget: 1000 ms; slowest: %.0f ms, observed"
          " not asserted; cold first spawn: %.0f ms, uncounted)"
          % (unit_pass.median * 1000, slowest * 1000, unit_pass.cold * 1000))
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- output ---\n%s" % (name, "; ".join(problems), out))
        sys.exit(1)
    if unit_pass.median >= 1.0:
        perf.append("median unit invocation %.2f s (budget 1.00 s)" % unit_pass.median)

    print("\n== docs pass (%d cases) ==" % len(DOCS_CASES))
    failures, slowest = guarded("docs pass", ([], 0.0), docs_pass, src, verbose=True)
    # The MEDIAN, like the unit pass (§77). This pass was the last to read
    # its max, and failed the 0.34.0 release run on exactly the §77 artifact: 5409 ms
    # slowest under concurrent suite load, against 412-424 ms slowest re-run idle three
    # times (FEATURE_PLAN.md 82.10). With 7 samples the median is the 4th, which one
    # stall cannot move. The slowest stays printed: a real regression moves both.
    print("median docs invocation: %.0f ms (S2 budget: 1000 ms; slowest: %.0f ms,"
          " observed not asserted)" % (docs_pass.median * 1000, slowest * 1000))
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- output ---\n%s" % (name, "; ".join(problems), out))
        sys.exit(1)
    if docs_pass.median >= 1.0:
        perf.append("median docs invocation %.2f s (budget 1.00 s)" % docs_pass.median)

    print("\n== worktree pass (FEATURE_PLAN.md 78) ==")
    failures, _ = guarded("worktree pass", ([], 0.0), wt_pass, src, verbose=True)
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- detail ---\n%s" % (name, "; ".join(problems), out))
        sys.exit(1)

    # The mutation pass needs ONE failing case per mutation, and the mutations are
    # independent - every bench is its own temp repo. It used to run every case of
    # every pass in order, one mutation at a time: ~46 minutes of a ~48-minute run,
    # nearly all of it after the verdict was settled (16 of its 35 mutations were
    # caught only by the since-retired stop pass, each paying a full unit + docs pass
    # first). So
    # each pass now stops at its first failing case, and the mutations run
    # concurrently. Nothing here is timed: the S2 budgets above were measured before
    # this pass started, on an otherwise idle suite. CLOSEOUT_JOBS=1 runs it serially.
    jobs = max(1, int(os.environ.get("CLOSEOUT_JOBS", "8")))
    print("\n== mutation pass (%d mutations, count derived; %d at a time,"
          " first failing case named) ==" % (len(MUTATIONS), jobs))
    survivors = []
    stale = []

    def run_mutation(name, mutated):
        for where, fn, default in (("unit", unit_pass, ([], 0.0)),
                                   ("docs", docs_pass, ([], 0.0)),
                                   ("worktree", wt_pass, ([], 0.0))):
            kw = {} if fn is wt_pass else {"first_only": True}
            broke, _ = guarded("mutation (%s): %s" % (where, name), default, fn, mutated,
                               verbose=False, **kw)
            if broke:
                return where, broke[0][0]
        return None, None

    live = []
    for name, old, new in MUTATIONS:
        if old not in src:
            # Reported, never raised. An assert aborts the run, so every mutation after
            # a stale one never executes and one bad anchor hides all of them. A stale
            # mutation is also NOT a pass: it is a defect class that has silently lost
            # its coverage — which is how the §72 regression reached four releases.
            stale.append(name)
            print("  %-38s STALE - anchor no longer applies, re-point it" % name)
            continue
        live.append((name, src.replace(old, new)))
    with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as pool:
        futures = [pool.submit(run_mutation, name, mutated) for name, mutated in live]
        for (name, _), fut in zip(live, futures):
            where, case = fut.result()
            print("  %-38s %s" % (name, "caught by %s case %s" % (where, case)
                                  if where else "SURVIVED"), flush=True)
            if not where:
                survivors.append(name)
    if survivors:
        print("\nMUTATIONS SURVIVED: %s - the corpus does not pin what it claims" % ", ".join(survivors))
    if stale:
        print("\nMUTATIONS STALE: %s - re-point the anchors" % ", ".join(stale))
    if perf:
        print("\nS2 PERF over budget: %s" % "; ".join(perf))
        # ASCII only: this prints to the operator's console, and on Windows that is
        # cp1252 - an em dash or a section sign arrives as a replacement character,
        # which is the same encoding trap change-verify's own guidance names.
        print("  (the correctness results above are unaffected - these are timing"
              " budgets. The unit and docs budgets read the median, so a single OS"
              " stall no longer breaches either; a breach here means the typical"
              " invocation really did slow down: FEATURE_PLAN 71, 77, 82.10)")

    if guarded.crashed:
        print("\nCRASHED passes: %s - those cases did not run"
              % ", ".join(guarded.crashed))

    if survivors or stale or perf or guarded.crashed:
        sys.exit(1)

    print("\nall green: %d unit + %d docs cases + the worktree pass, %d mutations caught"
          % (len(CASES), len(DOCS_CASES), len(MUTATIONS)))


if __name__ == "__main__":
    main()
