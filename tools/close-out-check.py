# -*- coding: utf-8 -*-
"""Re-runnable proof for templates/close-out.template.sh (FEATURE_PLAN.md §46, §52, §67).

Four passes, and the last is the point:

  1. a unit pass driving check mode over a fixture corpus of real commit bodies -
     every stated-skip form, the RED zero-form, each key missing / empty /
     duplicated, a mid-line key lookalike, a CRLF body, and two verbatim record
     bodies from the first adopter's armed arcs (ai-news-dashboard S6/S7) - each
     case committed into a bench git repo and checked through the script's real
     interface;
  2. a stop pass driving stop-check mode (the §52 backstop) over per-case bench
     repos - defective / complete / bare crossed with guard-state present /
     absent / stale-session, the no-upstream narrowing, pushed-commits-out-of-
     scope, the candidate cap, stand-down on stop_hook_active, both session-id
     casings, the armed block JSON, and fail-open on an empty payload - each
     through the script's real interface with the payload on stdin;
  3. a docs pass driving docs-check mode (the §67.3 observer) over per-case
     bench repos with real file writes, since the observer counts lines a commit
     actually added - under budget, exactly at it, over it, an index the commit
     never touched, a retirement commit that only deletes, an explicit ref, and
     a bad ref (which must still exit 0: log-only never fails a step);
  4. a mutation pass that breaks the checker - the count derived from the
     MUTATIONS list at run time, never stated here - and requires pass 1 or 2
     to notice each one - pass 1, 2 or 3. A suite that survives its own
     mutations is not testing the thing it claims to (invariant 13).

Kit-development artifact: lives at the root, never ships inside sdlc-kit/.
Run from anywhere:  python tools/close-out-check.py
"""
import io, json, os, subprocess, sys, tempfile, time

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

# One mutation per defect class the corpus pins; each must break >= 1 unit or
# stop case.
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
    # --- stop-check (§52). Each models a plausible backstop defect.
    ("standdown_disabled",
     '"stop_hook_active"[[:space:]]*:[[:space:]]*true',
     '"stop_hook_active_never"[[:space:]]*:[[:space:]]*true'),
    ("defective_counted_complete",
     'else defective="$defective $C($probs )"; fi',
     'else complete=$((complete + 1)); fi'),
    ("bare_ignores_guard_evidence",
     'if [ -n "$GUARD_EVID" ]; then bare_flagged="$bare_flagged $C"',
     'if [ -n "" ]; then bare_flagged="$bare_flagged $C"'),
    ("guard_session_not_matched",
     '[ "$(cat .git/sdlc-tdd/session 2>/dev/null)" = "$SID" ]',
     '[ -d .git/sdlc-tdd ]'),
    ("block_regardless_of_flag",
     'if [ -f "$SD/deny-enabled" ]; then',
     'if [ ! -f "$SD/deny-enabled.never" ]; then'),
    ("cap_unbounded", "rev-list --abbrev-commit -n 20", "rev-list --abbrev-commit -n 9999"),
    ("scope_ignores_upstream", "-n 20 '@{u}..HEAD'", "-n 20 HEAD"),
    ("red_treated_singleton", 'pk RED "$red_n" "$red_e" ""', 'pk RED "$red_n" "$red_e" s'),
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


SID = "11111111-2222-3333-4444-555555555555"
STALE_SID = "99999999-8888-7777-6666-555555555555"


def payload(sid=SID, active=False, camel=False):
    key = "sessionId" if camel else "session_id"
    return '{"%s":"%s","hook_event_name":"Stop","stop_hook_active":%s}' % (
        key, sid, "true" if active else "false")


FULL_BODY = body("feat(x): slice",
                 "RED: pytest -q — t.py:1 — exit 1",
                 "RED: pytest -q — t.py:9 — exit 1",
                 "quality: nothing to do",
                 "mutation: 2 guards, each seen to fail",
                 "verify: ran — CLI path green (Git Bash)")
DEFECTIVE_BODY = body("feat(x): slice missing verify",
                      "RED: pytest -q — t.py:1 — exit 1",
                      "quality: nothing to do",
                      "mutation: 1 guard, seen to fail")
BARE_BODY = "docs(z): notes only\n\nProse, no record keys.\n"


class StopBench(Bench):
    """A per-case repo for stop-check: optional origin/upstream, guard state,
    arming flag, and the stop log - everything the backstop actually reads."""

    def base_commit(self):
        self.commit("chore: base\n\nPre-kit commit, no record.\n")

    def set_origin(self, base):
        origin = os.path.join(base, "origin.git")
        subprocess.run(["git", "init", "-q", "--bare", origin], capture_output=True)
        self.git("remote", "add", "origin", origin)
        p = self.git("push", "-q", "-u", "origin", "HEAD")
        assert p.returncode == 0, "bench push failed: " + p.stderr.decode()

    def push(self):
        p = self.git("push", "-q", "origin", "HEAD")
        assert p.returncode == 0, "bench push failed: " + p.stderr.decode()

    def guard_state(self, sid, evidence=True):
        d = os.path.join(self.root, ".git", "sdlc-tdd")
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "session"), "w", newline="\n").write(sid)
        if evidence:
            io.open(os.path.join(d, "prod-write-observed"), "w").write("")

    def arm(self):
        d = os.path.join(self.root, ".git", "sdlc-close-out")
        os.makedirs(d, exist_ok=True)
        io.open(os.path.join(d, "deny-enabled"), "w").write("")

    def run_stop(self, pl):
        p = subprocess.run(["sh", self.script, "stop-check"], cwd=self.root,
                           input=pl.encode("utf-8"), capture_output=True)
        log = os.path.join(self.root, ".git", "sdlc-close-out", "log")
        text = io.open(log, encoding="utf-8").read() if os.path.exists(log) else ""
        return p.returncode, p.stdout.decode("utf-8", "replace"), text


# (name, setup(bench, base) -> payload, stdout check: None | "block-json",
#  log must-contain, log must-NOT-contain)
def _s_standdown(b, base):
    b.base_commit(); b.set_origin(base); b.commit(DEFECTIVE_BODY)
    return payload(active=True)

def _s_defective(b, base):
    b.base_commit(); b.set_origin(base); b.commit(DEFECTIVE_BODY)
    return payload()

def _s_complete(b, base):
    b.base_commit(); b.set_origin(base); b.commit(FULL_BODY)
    return payload()

def _s_bare_no_guard(b, base):
    b.base_commit(); b.set_origin(base); b.commit(BARE_BODY)
    return payload()

def _s_bare_guard(b, base):
    b.base_commit(); b.set_origin(base); b.commit(BARE_BODY)
    b.guard_state(SID)
    return payload()

def _s_bare_guard_armed(b, base):
    # bare NEVER blocks: armed or not, no stdout verdict.
    b.base_commit(); b.set_origin(base); b.commit(BARE_BODY)
    b.guard_state(SID); b.arm()
    return payload()

def _s_bare_stale_session(b, base):
    b.base_commit(); b.set_origin(base); b.commit(BARE_BODY)
    b.guard_state(STALE_SID)
    return payload()

def _s_bare_guard_camel(b, base):
    b.base_commit(); b.set_origin(base); b.commit(BARE_BODY)
    b.guard_state(SID)
    return payload(camel=True)

def _s_defective_armed(b, base):
    b.base_commit(); b.set_origin(base); b.commit(DEFECTIVE_BODY)
    b.arm()
    return payload()

def _s_no_upstream(b, base):
    # HEAD-only narrowing: the older defective commit is out of scope, stated.
    b.base_commit(); b.commit(DEFECTIVE_BODY); b.commit(FULL_BODY)
    return payload()

def _s_pushed_out_of_scope(b, base):
    b.base_commit(); b.set_origin(base); b.commit(DEFECTIVE_BODY); b.push()
    return payload()

def _s_defective_below_head(b, base):
    b.base_commit(); b.set_origin(base); b.commit(DEFECTIVE_BODY); b.commit(FULL_BODY)
    return payload()

def _s_crlf_defective(b, base):
    b.base_commit(); b.set_origin(base)
    b.commit(DEFECTIVE_BODY.replace("\n", "\r\n"))
    return payload()

def _s_cap(b, base):
    b.base_commit(); b.set_origin(base)
    for i in range(22):
        b.commit("docs(z): bare %d\n\nProse.\n" % i)
    return payload()

def _s_empty_payload(b, base):
    b.base_commit(); b.set_origin(base); b.commit(FULL_BODY)
    return ""

STOP_CASES = [
    ("stop_standdown", _s_standdown, None,
     ["standing down"], ["WOULD-BLOCK", "clean"]),
    ("stop_defective_logs_wouldblock", _s_defective, None,
     ["stop: WOULD-BLOCK - defective record on", "missing verify"], ["stop: BLOCK"]),
    ("stop_complete_clean", _s_complete, None,
     ["stop: clean (1 complete, 0 bare"], ["WOULD-BLOCK"]),
    ("stop_bare_without_guard_noted", _s_bare_no_guard, None,
     ["stop: clean (0 complete, 1 bare"], ["WOULD-BLOCK"]),
    ("stop_bare_with_guard_flagged", _s_bare_guard, None,
     ["stop: WOULD-BLOCK (bare, log-only by design)"], []),
    ("stop_bare_never_blocks_even_armed", _s_bare_guard_armed, None,
     ["stop: WOULD-BLOCK (bare, log-only by design)"], ["stop: BLOCK"]),
    ("stop_bare_stale_session_noted", _s_bare_stale_session, None,
     ["stop: clean (0 complete, 1 bare"], ["WOULD-BLOCK"]),
    ("stop_bare_camel_session_id", _s_bare_guard_camel, None,
     ["stop: WOULD-BLOCK (bare, log-only by design)"], []),
    ("stop_defective_armed_blocks", _s_defective_armed, "block-json",
     ["stop: BLOCK - defective record on"], []),
    ("stop_no_upstream_head_only", _s_no_upstream, None,
     ["stop: clean (1 complete, 0 bare", "no upstream configured"], ["WOULD-BLOCK"]),
    ("stop_pushed_out_of_scope", _s_pushed_out_of_scope, None,
     ["stop: clean (no candidate commits"], ["WOULD-BLOCK"]),
    ("stop_defective_below_head_flagged", _s_defective_below_head, None,
     ["stop: WOULD-BLOCK - defective record on", "missing verify"], []),
    ("stop_crlf_defective", _s_crlf_defective, None,
     ["stop: WOULD-BLOCK - defective record on"], []),
    ("stop_candidate_cap_20", _s_cap, None,
     ["20 bare without slice-loop evidence"], ["22 bare"]),
    ("stop_empty_payload_fails_open", _s_empty_payload, None,
     ["stop: clean (1 complete"], ["WOULD-BLOCK"]),
]


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


def docs_pass(src, verbose):
    """Runs every docs case in its own bench repo; returns (failures, slowest).

    Every case asserts exit 0: this mode is log-only, so a non-zero exit would
    fail an /end-slice step over a bookkeeping observation - the one thing the
    §67.3 ruling forbids it to do."""
    failures, slowest = [], 0.0
    for name, setup, contains, absent in DOCS_CASES:
        with tempfile.TemporaryDirectory() as base:
            b = DocsBench(base, src)
            argv = setup(b)
            code, out, dt = b.run(argv)
            slowest = max(slowest, dt)
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
    return failures, slowest


def stop_pass(src, verbose):
    """Runs every stop case in its own bench repo; returns (failures, {name: secs})."""
    failures, times = [], {}
    for name, setup, stdout_kind, contains, absent in STOP_CASES:
        with tempfile.TemporaryDirectory() as base:
            b = StopBench(base, src)
            pl = setup(b, base)
            t0 = time.perf_counter()
            code, out, log = b.run_stop(pl)
            times[name] = time.perf_counter() - t0
            problems = []
            if code != 0:
                problems.append("exit %d, expected 0 (stop-check must fail open)" % code)
            if stdout_kind == "block-json":
                try:
                    d = json.loads(out)
                    if d.get("decision") != "block" or not d.get("reason"):
                        problems.append("stdout is not a block verdict: %r" % out)
                except ValueError:
                    problems.append("stdout is not valid JSON: %r" % out)
            elif out.strip():
                problems.append("unexpected stdout (logging mode must stay silent): %r" % out)
            for c in contains:
                if c not in log:
                    problems.append("log lacks %r" % c)
            for c in absent:
                if c in log:
                    problems.append("log wrongly contains %r" % c)
            if problems:
                failures.append((name, problems, "stdout: %s\nlog:\n%s" % (out, log)))
            if verbose:
                print("  %-38s %s" % (name, "FAIL: " + "; ".join(problems) if problems else "ok"))
    return failures, times


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

    print("\n== docs pass (%d cases) ==" % len(DOCS_CASES))
    failures, slowest = docs_pass(src, verbose=True)
    print("slowest docs invocation: %.0f ms (S2 budget: 1000 ms)" % (slowest * 1000))
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- output ---\n%s" % (name, "; ".join(problems), out))
        sys.exit(1)
    if slowest >= 1.0:
        print("S2 FAILED: slowest docs invocation %.2f s" % slowest)
        sys.exit(1)

    print("\n== stop pass (%d cases) ==" % len(STOP_CASES))
    failures, times = stop_pass(src, verbose=True)
    # Two budgets, both against the 30 s hook timeout: typical sessions hold a
    # handful of unpushed commits (< 1.5 s), and the cap case's 20-candidate walk
    # pays ~2 Windows-sh forks per candidate (measured ~3.5 s at cap on the dev
    # machine - bounded by the cap, nowhere near the timeout's fail-open edge).
    cap_t = times.pop("stop_candidate_cap_20")
    typical = max(times.values())
    print("slowest typical stop invocation: %.0f ms (budget: 1500 ms); cap-20 walk: %.0f ms (budget: 5000 ms)"
          % (typical * 1000, cap_t * 1000))
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- detail ---\n%s" % (name, "; ".join(problems), out))
        sys.exit(1)
    if typical >= 1.5 or cap_t >= 5.0:
        print("S2 FAILED: stop invocation over budget")
        sys.exit(1)

    print("\n== mutation pass (%d mutations, count derived) ==" % len(MUTATIONS))
    survivors = []
    for name, old, new in MUTATIONS:
        assert old in src, "mutation %s no longer applies - update it" % name
        mutated = src.replace(old, new)
        broke, _ = unit_pass(mutated, verbose=False)
        where = "unit"
        if not broke:
            broke, _ = docs_pass(mutated, verbose=False)
            where = "docs"
        if not broke:
            broke, _ = stop_pass(mutated, verbose=False)
            where = "stop"
        print("  %-38s %s" % (name, "caught (%d %s case%s)" % (len(broke), where, "s" if len(broke) != 1 else "") if broke else "SURVIVED"))
        if not broke:
            survivors.append(name)
    if survivors:
        print("\nMUTATIONS SURVIVED: %s - the corpus does not pin what it claims" % ", ".join(survivors))
        sys.exit(1)

    print("\nall green: %d unit + %d docs + %d stop cases, %d mutations caught"
          % (len(CASES), len(DOCS_CASES), len(STOP_CASES), len(MUTATIONS)))


if __name__ == "__main__":
    main()
