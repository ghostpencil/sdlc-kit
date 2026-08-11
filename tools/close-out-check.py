# -*- coding: utf-8 -*-
"""Re-runnable proof for templates/close-out.template.sh (FEATURE_PLAN.md §46).

Two passes, and the second is the point:

  1. a unit pass driving the checker over a fixture corpus of real commit bodies -
     every stated-skip form, the RED zero-form, each key missing / empty /
     duplicated, a mid-line key lookalike, a CRLF body, and two verbatim record
     bodies from the first adopter's armed arcs (ai-news-dashboard S6/S7) - each
     case committed into a bench git repo and checked through the script's real
     interface;
  2. a mutation pass that breaks the checker - the count derived from the
     MUTATIONS list at run time, never stated here - and requires the unit pass
     to notice each one. A suite that survives its own mutations is not testing
     the thing it claims to (invariant 13).

Kit-development artifact: lives at the root, never ships inside sdlc-kit/.
Run from anywhere:  python tools/close-out-check.py
"""
import io, os, subprocess, sys, tempfile, time

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(REPO, "sdlc-kit", "templates", "close-out.template.sh")

FULL_TAIL = (
    "quality: nothing to do\n"
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


def body(subject, *record):
    return subject + "\n\nProse about what and why.\n\n" + "\n".join(record) + "\n"


# (name, commit body or None to reuse the last commit, argv after the script path,
#  expected exit, expected first output line or None, must-contain substrings)
CASES = [
    ("observed_two_red",
     body("feat(x): two behaviors",
          "RED: pytest -q tests/test_a.py::test_one — test_a.py:12 — exit 1",
          "RED: pytest -q tests/test_a.py::test_two — test_a.py:31 — exit 1",
          "quality: 2 moves applied",
          "mutation: 2 guards, each seen to fail",
          "verify: ran — CLI path green (Git Bash)"),
     ["check"], 0,
     "close-out record: COMPLETE - RED(2) quality mutation verify - structural presence only; this does not verify the evidence is true.",
     []),
    ("red_not_observed_form",
     body("fix(y): hotfix", "RED: not observed — regression pinned by existing test",
          *FULL_TAIL.splitlines()),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("red_zero_form",
     body("docs(z): config-only slice", "RED: none — no behavior batches this slice",
          "quality: nothing to do", "mutation: none — no new guards",
          "verify: skipped — docs only, the gate fully pins it"),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("all_skip_forms",
     body("chore(w): mechanical sweep", "RED: none — no behavior batches this slice",
          "quality: skipped — mechanical rename, nothing to weigh",
          "mutation: none — no new guards", "verify: skipped — covered by the gate"),
     ["check"], 0, None, ["COMPLETE"]),
    ("missing_red",
     body("feat(x): s", "quality: nothing to do", "mutation: none — no new guards",
          "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED",
     ["MISSING -", "Never invent", "git commit --amend"]),
    ("missing_quality",
     body("feat(x): s", "RED: not observed — reason", "mutation: none — no new guards",
          "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: quality", ["MISSING -"]),
    ("missing_mutation",
     body("feat(x): s", "RED: not observed — reason", "quality: nothing to do",
          "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: mutation", ["MISSING -"]),
    ("missing_verify",
     body("feat(x): s", "RED: not observed — reason", "quality: nothing to do",
          "mutation: none — no new guards"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: verify", ["MISSING -"]),
    ("empty_red_payload",
     body("feat(x): s", "RED:", "quality: nothing to do",
          "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED", ["EMPTY -"]),
    ("empty_verify_payload",
     body("feat(x): s", "RED: not observed — reason", "quality: nothing to do",
          "mutation: none — no new guards", "verify:   "),
     ["check"], 1, "close-out record: INCOMPLETE - problems: verify", ["EMPTY -"]),
    ("duplicated_quality",
     body("feat(x): s", "RED: not observed — reason", "quality: 1 move applied",
          "quality: nothing to do", "mutation: none — no new guards",
          "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: quality",
     ["DUPLICATED (2 lines)"]),
    ("anchors_midline_lookalikes_do_not_count",
     # Prose names "RED:" and "quality:" mid-line; neither real line exists.
     "feat(x): s\n\nCopy the RED: lines and the quality: line from the record.\n\n"
     "mutation: none — no new guards\nverify: skipped — small\n",
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED quality", []),
    ("lookalikes_beside_full_record",
     body("feat(x): s", "Per the record contract the RED: and quality: lines follow.",
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
    ("adopter_s7_verbatim", ADOPTER_S7, ["check"], 0, None, ["COMPLETE - RED(3)"]),
    ("adopter_s6_verbatim", ADOPTER_S6, ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("no_record_at_all", "feat(x): subject only\n\nProse.\n",
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED quality mutation verify", []),
    ("bad_ref", None, ["check", "no-such-ref"], 2, None,
     ["CANNOT CHECK -", "does not resolve"]),
    ("unknown_mode", None, ["frob"], 2, None, ["CANNOT CHECK -", "unknown mode 'frob'"]),
    ("no_mode", None, [], 2, None, ["CANNOT CHECK -", "unknown mode ''"]),
]

# One mutation per defect class the corpus pins; each must break >= 1 unit case.
MUTATIONS = [
    ("anchor_dropped_RED", "/^RED:/      { rn++;", "/RED:/      { rn++;"),
    ("anchor_dropped_quality", "/^quality:/  { qn++;", "/quality:/  { qn++;"),
    ("empty_check_disabled", "if ($0 ~ /^RED:[[:space:]]*$/) re++", ""),
    ("duplicate_check_disabled", '[ "$n" -gt 1 ]', '[ "$n" -gt 99 ]'),
    ("incomplete_exits_zero", "exit 1\n", "exit 0\n"),
    ("missing_not_recorded", 'line="MISSING - $AMEND"; bad="$bad $k"',
     'line="MISSING - $AMEND"'),
    ("ref_guard_bypassed", '--verify --quiet "$REF^{commit}"', "--verify --quiet HEAD"),
    ("mode_gate_loosened", '[ "$MODE" = "check" ]', '[ -n "$MODE" ]'),
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

    via_powershell = False  # S4: same corpus through the PowerShell -> sh chain,
                            # the invocation a Copilot CLI shell tool would issue

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


def unit_pass(src, verbose):
    """Runs every case; returns (failures, max_seconds)."""
    failures, slowest = [], 0.0
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
    return failures, slowest


def main():
    src = io.open(TPL, encoding="utf-8").read()

    if "--via-powershell" in sys.argv:
        # S4 dialect run: unit corpus only (mutations re-prove nothing new here),
        # no S2 assert - the extra powershell spawn is the harness's cost, not
        # the script's.
        Bench.via_powershell = True
        print("== S4 unit pass via powershell -> sh (%d cases) ==" % len(CASES))
        failures, slowest = unit_pass(src, verbose=True)
        print("slowest invocation incl. powershell spawn: %.0f ms" % (slowest * 1000))
        if failures:
            for name, problems, out in failures:
                print("\nFAILED %s: %s\n--- output ---\n%s" % (name, "; ".join(problems), out))
            sys.exit(1)
        print("\nS4 green: %d cases, verdicts identical to the direct-sh pass" % len(CASES))
        return

    print("== unit pass (%d cases) ==" % len(CASES))
    failures, slowest = unit_pass(src, verbose=True)
    print("slowest warm invocation: %.0f ms (S2 budget: 1000 ms; cold first spawn: %.0f ms, uncounted)"
          % (slowest * 1000, unit_pass.cold * 1000))
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- output ---\n%s" % (name, "; ".join(problems), out))
        sys.exit(1)
    if slowest >= 1.0:
        print("S2 FAILED: slowest invocation %.2f s" % slowest)
        sys.exit(1)

    print("\n== mutation pass (%d mutations, count derived) ==" % len(MUTATIONS))
    survivors = []
    for name, old, new in MUTATIONS:
        assert old in src, "mutation %s no longer applies - update it" % name
        mutated = src.replace(old, new)
        broke, _ = unit_pass(mutated, verbose=False)
        print("  %-38s %s" % (name, "caught (%d case%s)" % (len(broke), "s" if len(broke) != 1 else "") if broke else "SURVIVED"))
        if not broke:
            survivors.append(name)
    if survivors:
        print("\nMUTATIONS SURVIVED: %s - the corpus does not pin what it claims" % ", ".join(survivors))
        sys.exit(1)

    print("\nall green: %d unit cases, %d mutations caught" % (len(CASES), len(MUTATIONS)))


if __name__ == "__main__":
    main()
