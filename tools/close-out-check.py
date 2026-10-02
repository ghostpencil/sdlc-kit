# -*- coding: utf-8 -*-
"""Re-runnable proof for templates/close-out.template.sh (FEATURE_PLAN.md §46, §52, §67).

Four passes, and the last is the point:

  1. a unit pass driving check mode over a fixture corpus of real commit bodies -
     every stated-skip form, the RED zero-form, each key missing / empty /
     duplicated, a mid-line key lookalike, a CRLF body, and two verbatim record
     bodies from the first adopter's armed arcs (ai-news-dashboard S6/S7) in BOTH
     directions - as filed, where they now fail on the 0.27.0 lenses: key alone
     (the update transition, pinned rather than asserted in prose), and with that
     line added, where they pass - each case committed into a bench git repo and
     checked through the script's real interface;
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
import io, json, os, shutil, subprocess, sys, tempfile, time, traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(REPO, "sdlc-kit", "templates", "close-out.template.sh")

FULL_TAIL = (
    "quality: nothing to do\n"
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
          "quality: 2 moves applied",
          "lenses: shared state under concurrency: clean",
          "mutation: 2 guards, each seen to fail",
          "verify: ran — CLI path green (Git Bash)"),
     ["check"], 0,
     "close-out record: COMPLETE - RED(2) quality lenses mutation verify - structural presence only; this does not verify the evidence is true.",
     []),
    ("red_not_observed_form",
     body("fix(y): hotfix", "RED: not observed — regression pinned by existing test",
          *FULL_TAIL.splitlines()),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("red_zero_form",
     body("docs(z): config-only slice", "RED: none — no behavior batches this slice",
          "quality: nothing to do", "lenses: no lens triggered",
          "mutation: none — no new guards",
          "verify: skipped — docs only, the gate fully pins it"),
     ["check"], 0, None, ["COMPLETE - RED(1)"]),
    ("all_skip_forms",
     body("chore(w): mechanical sweep", "RED: none — no behavior batches this slice",
          "quality: skipped — mechanical rename, nothing to weigh",
          "lenses: no lens triggered",
          "mutation: none — no new guards", "verify: skipped — covered by the gate"),
     ["check"], 0, None, ["COMPLETE"]),
    ("missing_red",
     body("feat(x): s", "quality: nothing to do", "lenses: no lens triggered",
          "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED",
     ["MISSING -", "Never invent", "git commit --amend"]),
    ("missing_quality",
     body("feat(x): s", "RED: not observed — reason", "lenses: no lens triggered",
          "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: quality", ["MISSING -"]),
    ("missing_lenses",
     body("feat(x): s", "RED: not observed — reason", "quality: nothing to do",
          "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: lenses", ["MISSING -"]),
    ("missing_mutation",
     body("feat(x): s", "RED: not observed — reason", "quality: nothing to do",
          "lenses: no lens triggered", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: mutation", ["MISSING -"]),
    ("missing_verify",
     body("feat(x): s", "RED: not observed — reason", "quality: nothing to do",
          "lenses: no lens triggered", "mutation: none — no new guards"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: verify", ["MISSING -"]),
    ("empty_red_payload",
     body("feat(x): s", "RED:", "quality: nothing to do",
          "lenses: no lens triggered", "mutation: none — no new guards",
          "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED", ["EMPTY -"]),
    ("empty_lenses_payload",
     body("feat(x): s", "RED: not observed — reason", "quality: nothing to do",
          "lenses:  ", "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: lenses", ["EMPTY -"]),
    ("empty_verify_payload",
     body("feat(x): s", "RED: not observed — reason", "quality: nothing to do",
          "lenses: no lens triggered", "mutation: none — no new guards",
          "verify:   "),
     ["check"], 1, "close-out record: INCOMPLETE - problems: verify", ["EMPTY -"]),
    ("duplicated_quality",
     body("feat(x): s", "RED: not observed — reason", "quality: 1 move applied",
          "quality: nothing to do", "lenses: no lens triggered",
          "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: quality",
     ["DUPLICATED (2 lines)"]),
    ("duplicated_lenses",
     # Two review passes each writing their own verdict line: nobody knows which
     # is the record, and the denominator this key exists for is the casualty.
     body("feat(x): s", "RED: not observed — reason", "quality: nothing to do",
          "lenses: untrusted input: clean", "lenses: no lens triggered",
          "mutation: none — no new guards", "verify: skipped — small"),
     ["check"], 1, "close-out record: INCOMPLETE - problems: lenses",
     ["DUPLICATED (2 lines)"]),
    ("anchors_midline_lookalikes_do_not_count",
     # Prose names "RED:", "quality:" and "lenses:" mid-line. Neither RED nor
     # quality has a real line, so both must read as missing. lenses: DOES have a
     # real line below, so with the anchor intact it reads as present-once — and
     # if the anchor were dropped the prose mention would make it duplicated,
     # which is what pins the anchor for this key rather than only for the other two.
     "feat(x): s\n\nCopy the RED: lines, the quality: line and the lenses: line\n"
     "from the record.\n\n"
     "lenses: no lens triggered\nmutation: none — no new guards\n"
     "verify: skipped — small\n",
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
    # Real field bodies, kept verbatim. Both predate the lenses: key (0.27.0), so
    # both are now INCOMPLETE on exactly that one line and nothing else — which is
    # the transition consequence stated in sdlc-update.md, pinned here rather than
    # asserted in prose: the first slice closed after updating fails until the line
    # is written. Editing the field evidence to make the suite green would delete
    # the only proof that the failure is narrow.
    ("adopter_s7_verbatim_pre_lenses", ADOPTER_S7, ["check"], 1,
     "close-out record: INCOMPLETE - problems: lenses",
     ["RED:      present (3 lines)", "quality:  present", "mutation: present",
      "verify:   present"]),
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
     ["check"], 1, "close-out record: INCOMPLETE - problems: RED quality lenses mutation verify", []),
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
    ("anchor_dropped_lenses", "/^lenses:/   { ln++;", "/lenses:/   { ln++;"),
    ("empty_check_disabled", "if ($0 ~ /^RED:[[:space:]]*$/) re++", ""),
    ("duplicate_check_disabled", '[ "$n" -gt 1 ]', '[ "$n" -gt 99 ]'),
    ("incomplete_exits_zero", "exit 1\n", "exit 0\n"),
    ("missing_not_recorded", 'line="MISSING - $AMEND"; bad="$bad $k"',
     'line="MISSING - $AMEND"'),
    ("ref_guard_bypassed", '--verify --quiet "$REF^{commit}"', "--verify --quiet HEAD"),
    ("mode_gate_loosened", '[ "$MODE" = "check" ]', '[ -n "$MODE" ]'),
    # --- stop-check (§52). Each models a plausible backstop defect.
    ("copilot_standdown_disabled",
     """    *'"hook_event_name"'*) case "$IN" in *'"timestamp"'*) exit 0 ;; esac ;;
""",
     ""),
    ("copilot_standdown_ignores_permission_mode",
     """    *'"permission_mode"'*) ;;
""", ""),
    ("copilot_standdown_catches_native",
     """    *'"hook_event_name"'*) case "$IN" in""", """    *'"timestamp"'*) case "$IN" in"""),
    ("standdown_disabled",
     '"stop_hook_active"[[:space:]]*:[[:space:]]*true',
     '"stop_hook_active_never"[[:space:]]*:[[:space:]]*true'),
    # RE-POINTED for 0.29.0: the anchor gained the defective_shas list that the
    # de-dup reads. §72's lesson - re-point a mutation when the fix restructures
    # what it targets, or a defect class silently loses its coverage.
    ("defective_counted_complete",
     'else defective="$defective $C($probs )"; defective_shas="$defective_shas $C"; fi',
     'else complete=$((complete + 1)); fi'),
    # --- the candidate filter and de-dup (§73.8).
    ("filter_disabled",
     'if [ "$bookkeeping" = "1" ]; then skipped=$((skipped + 1)); continue; fi',
     'if [ "$bookkeeping" = "never" ]; then skipped=$((skipped + 1)); continue; fi'),
    ("filter_too_greedy",
     'if ($0 !~ /^spec\// && $0 != "CLAUDE.md" && $0 != "README.md") other = 1',
     'if (0) other = 1'),
    ("filter_swallows_pathless_commits",
     '(np > 0 && !other) ? 1 : 0',
     '(!other) ? 1 : 0'),
    ("dedup_disabled",
     '    [ -f "$SEEN" ] || return 1',
     '    return 1'),
    ("empty_window_still_says_clean",
     'slog "stop: n/a (nothing to inspect: no candidate commits; $SCOPE)"',
     'slog "stop: clean (no candidate commits; $SCOPE)"'),
    ("bare_ignores_guard_evidence",
     'if [ -n "$GUARD_EVID" ]; then bare_flagged="$bare_flagged $C"',
     'if [ -n "" ]; then bare_flagged="$bare_flagged $C"'),
    ("guard_session_not_matched",
     '[ "$(cat "$GD/sdlc-tdd/session" 2>/dev/null)" = "$SID" ]',
     '[ -d "$GD/sdlc-tdd" ]'),
    ("block_regardless_of_flag",
     'if [ -f "$SD/deny-enabled" ]; then',
     'if [ ! -f "$SD/deny-enabled.never" ]; then'),
    # --- linked worktrees (FEATURE_PLAN.md 78).
    ("stop_tests_for_git_directory", '  [ -e .git ] || exit 0\n  if [ -z "$GD" ]; then',
     '  [ -d .git ] || exit 0\n  if [ -z "$GD" ]; then'),
    ("stop_state_under_literal_dotgit", 'SD="$GD/sdlc-close-out"', 'SD=.git/sdlc-close-out'),
    # Aimed at the WRITE, not the mkdir: the worktree pass's earlier stop cases create
    # the log directory, so a mutated mkdir alone changes nothing observable and first
    # survived the full run (0.31.1).
    ("docs_log_under_literal_dotgit", '"$MSG" >> "$GD/sdlc-close-out/log" 2>/dev/null',
     '"$MSG" >> .git/sdlc-close-out/log 2>/dev/null'),
    ("unresolvable_gitdir_silent",
     "printf '{\"decision\":\"block\",\"reason\":\"SDLC close-out backstop did not run",
     "true '{\"decision\":\"block\",\"reason\":\"SDLC close-out backstop did not run"),
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
                 "lenses: no lens triggered",
                 "mutation: 2 guards, each seen to fail",
                 "verify: ran — CLI path green (Git Bash)")
DEFECTIVE_BODY = body("feat(x): slice missing verify",
                      "RED: pytest -q — t.py:1 — exit 1",
                      "quality: nothing to do",
                      "lenses: no lens triggered",
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

    def commit_files(self, message, paths):
        """A commit that really touches paths - the candidate filter's only input.
        Every other stop case commits --allow-empty, i.e. no paths at all, which
        the filter deliberately treats as NOT bookkeeping (a certainty is what it
        removes; it never guesses). Without this helper the filter's cases cannot
        exist, which is how the corpus came to pin only what the mode fires ON."""
        for rel in paths:
            full = os.path.join(self.root, *rel.split("/"))
            d = os.path.dirname(full)
            if d and not os.path.isdir(d):
                os.makedirs(d)
            with io.open(full, "a", encoding="utf-8", newline="\n") as fh:
                fh.write("a line\n")
            self.git("add", "--", rel)
        p = self.git("commit", "--cleanup=verbatim", "-F", "-",
                     input=message.encode("utf-8"))
        assert p.returncode == 0, "bench commit_files failed: " + p.stderr.decode()

    def seen(self, sid, ref="HEAD"):
        """Pre-seed the per-session de-dup ledger, so one bench run stands in for
        the second stop of a session."""
        d = os.path.join(self.root, ".git", "sdlc-close-out")
        os.makedirs(d, exist_ok=True)
        sha = self.git("rev-parse", "--short", ref).stdout.decode().strip()
        with io.open(os.path.join(d, "seen"), "a", encoding="utf-8", newline="\n") as fh:
            fh.write("%s %s\n" % (sid, sha))

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

def _s_bookkeeping_skipped(b, base):
    # THE case the corpus lacked: a commit that CANNOT carry a record, in the
    # window, with slice-loop evidence present - the exact configuration that
    # produced 19 of one adoption's 19 flag lines. It must be skipped, silently
    # and by name in the verdict.
    b.base_commit(); b.set_origin(base)
    b.commit_files(BARE_BODY, ["spec/PHASE_01_X.md", "spec/PROJECT_INDEX.md", "CLAUDE.md"])
    b.guard_state(SID)
    return payload()

def _s_bookkeeping_beside_candidate(b, base):
    # Filtering must not cost a real catch standing next to it.
    b.base_commit(); b.set_origin(base)
    b.commit_files(BARE_BODY, ["spec/PROJECT_INDEX.md"])
    b.commit_files(DEFECTIVE_BODY, ["src/app.py"])
    return payload()

def _s_spec_plus_code_not_bookkeeping(b, base):
    # Conservative in one direction on purpose: one non-spec path and it stays a
    # candidate. A slice that also edits its phase spec is still a slice.
    b.base_commit(); b.set_origin(base)
    b.commit_files(BARE_BODY, ["spec/PROJECT_INDEX.md", "src/app.py"])
    b.guard_state(SID)
    return payload()

def _s_repeat_flag_dedups(b, base):
    # The second stop of a session that already logged this flag.
    b.base_commit(); b.set_origin(base); b.commit(BARE_BODY)
    b.guard_state(SID); b.seen(SID)
    return payload()

def _s_dedup_never_suppresses_block(b, base):
    # Armed: a still-defective commit blocks at EVERY stop. De-dup governs
    # logging only - being mentioned once must never buy a pass.
    b.base_commit(); b.set_origin(base); b.commit(DEFECTIVE_BODY)
    b.arm(); b.seen(SID)
    return payload()

# FEATURE_PLAN.md 79: Copilot reads .claude/settings.json, so a both-dialect
# project can reach stop-check from the Claude Stop entry with Copilot's payload
# translated into Claude's shape (measured 2026-09-28, 1.0.88). That call stands
# down - armed and defective, so a missing stand-down BLOCKS - while the two
# payloads it must not be confused with still check.
COPILOT_TRANSLATED = ('{"hook_event_name":"Stop","session_id":"%s",'
                      '"timestamp":"2026-09-28T14:40:02.101Z","cwd":"D:\\p",'
                      '"transcript_path":"x","stop_reason":"end_turn",'
                      '"stop_hook_active":false}' % SID)
COPILOT_NATIVE = ('{"sessionId":"%s","timestamp":1790606402101,"cwd":"D:\\p",'
                  '"transcriptPath":"x","stopReason":"end_turn",'
                  '"stop_hook_active":false}' % SID)

def _s_copilot_translated(b, base):
    b.base_commit(); b.set_origin(base); b.commit(DEFECTIVE_BODY)
    b.arm()
    return COPILOT_TRANSLATED

def _s_copilot_native(b, base):
    b.base_commit(); b.set_origin(base); b.commit(DEFECTIVE_BODY)
    b.arm()
    return COPILOT_NATIVE

def _s_claude_with_timestamp(b, base):
    b.base_commit(); b.set_origin(base); b.commit(DEFECTIVE_BODY)
    b.arm()
    return ('{"session_id":"%s","hook_event_name":"Stop","permission_mode":"default",'
            '"timestamp":"2026-09-28T14:40:02.101Z","stop_hook_active":false}' % SID)

def _s_empty_payload(b, base):
    b.base_commit(); b.set_origin(base); b.commit(FULL_BODY)
    return ""

STOP_CASES = [
    ("stop_standdown", _s_standdown, None,
     ["standing down"], ["WOULD-BLOCK", "clean"]),
    ("stop_defective_logs_wouldblock", _s_defective, None,
     ["stop: WOULD-BLOCK - defective record on", "missing verify"], ["stop: BLOCK"]),
    ("stop_complete_clean", _s_complete, None,
     ["stop: clean (inspected 1, 0 bookkeeping skipped; 1 complete, 0 bare"],
     ["WOULD-BLOCK"]),
    ("stop_bare_without_guard_noted", _s_bare_no_guard, None,
     ["stop: clean (inspected 1, 0 bookkeeping skipped; 0 complete, 1 bare"],
     ["WOULD-BLOCK"]),
    ("stop_bare_with_guard_flagged", _s_bare_guard, None,
     ["stop: WOULD-BLOCK (bare, log-only by design)"], []),
    ("stop_bare_never_blocks_even_armed", _s_bare_guard_armed, None,
     ["stop: WOULD-BLOCK (bare, log-only by design)"], ["stop: BLOCK"]),
    ("stop_bare_stale_session_noted", _s_bare_stale_session, None,
     ["stop: clean (inspected 1, 0 bookkeeping skipped; 0 complete, 1 bare"],
     ["WOULD-BLOCK"]),
    ("stop_bare_camel_session_id", _s_bare_guard_camel, None,
     ["stop: WOULD-BLOCK (bare, log-only by design)"], []),
    ("stop_defective_armed_blocks", _s_defective_armed, "block-json",
     ["stop: BLOCK - defective record on"], []),
    ("stop_no_upstream_head_only", _s_no_upstream, None,
     ["stop: clean (inspected 1, 0 bookkeeping skipped; 1 complete, 0 bare",
      "no upstream configured"], ["WOULD-BLOCK"]),
    # "clean" is ABSENT on purpose: an empty window is not a clean inspection,
    # and the two printing the same word is finding 5's opening sentence.
    ("stop_pushed_out_of_scope", _s_pushed_out_of_scope, None,
     ["stop: n/a (nothing to inspect: no candidate commits"],
     ["WOULD-BLOCK", "clean"]),
    ("stop_defective_below_head_flagged", _s_defective_below_head, None,
     ["stop: WOULD-BLOCK - defective record on", "missing verify"], []),
    ("stop_crlf_defective", _s_crlf_defective, None,
     ["stop: WOULD-BLOCK - defective record on"], []),
    ("stop_candidate_cap_20", _s_cap, None,
     ["inspected 20", "20 bare without slice-loop evidence"], ["22 bare"]),
    ("stop_empty_payload_fails_open", _s_empty_payload, None,
     ["stop: clean (inspected 1, 0 bookkeeping skipped; 1 complete"], ["WOULD-BLOCK"]),
    # --- the candidate filter and the per-session de-dup (§73.8, 0.29.0).
    ("stop_bookkeeping_skipped_not_flagged", _s_bookkeeping_skipped, None,
     ["stop: n/a (nothing to inspect: 1 bookkeeping skipped"],
     ["WOULD-BLOCK", "clean"]),
    ("stop_bookkeeping_beside_candidate", _s_bookkeeping_beside_candidate, None,
     ["stop: WOULD-BLOCK - defective record on", "missing verify"], ["n/a"]),
    ("stop_spec_plus_code_not_bookkeeping", _s_spec_plus_code_not_bookkeeping, None,
     ["stop: WOULD-BLOCK (bare, log-only by design)"], ["n/a", "bookkeeping skipped"]),
    ("stop_repeat_flag_dedups", _s_repeat_flag_dedups, None,
     ["stop: repeat (bare flag already logged this session on"], ["WOULD-BLOCK"]),
    ("stop_dedup_never_suppresses_block", _s_dedup_never_suppresses_block,
     "block-json", ["stop: BLOCK - defective record on"], ["repeat"]),
    # --- Copilot running the Claude dialect's Stop entry (§79). The stand-down
    # is silent: no stdout, no log line, on an armed defective commit.
    ("stop_copilot_translated_stands_down", _s_copilot_translated, None,
     [], ["stop:"]),
    ("stop_copilot_native_still_checks", _s_copilot_native, "block-json",
     ["stop: BLOCK - defective record on"], []),
    ("stop_claude_with_timestamp_still_checks", _s_claude_with_timestamp,
     "block-json", ["stop: BLOCK - defective record on"], []),
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


def stop_pass(src, verbose, only=None):
    """Runs every stop case (or just the one named by `only`) in its own bench repo;
    returns (failures, {name: secs})."""
    failures, times = [], {}
    for name, setup, stdout_kind, contains, absent in STOP_CASES:
        if only is not None and name != only:
            continue
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
    times.sort()
    unit_pass.median = times[len(times) // 2] if times else 0.0
    return failures, slowest


unit_pass.median = 0.0


# --- linked worktrees and the launchers (FEATURE_PLAN.md 78) ------------------------
# Every other pass builds an ordinary checkout, whose .git is a directory - the one
# configuration that cannot see this defect. In a linked worktree .git is a FILE
# naming the git directory: the launchers tested for a directory and stood down in
# silence, and the script kept its state under a literal .git/ that is not a
# directory there. These cases build a REAL worktree with git.
HOOK_JSON = os.path.join(REPO, "sdlc-kit", "templates", "close-out-hook.template.json")
SETTINGS = os.path.join(REPO, "sdlc-kit", "templates", "settings.template.json")


def _reopen_git(root, text):
    """Rewrite a worktree's .git FILE. Windows git marks it hidden, and a hidden file
    cannot be opened for a truncating write there - so remove it, then create it."""
    p = os.path.join(root, ".git")
    if os.path.isfile(p):
        os.remove(p)
    io.open(p, "w", newline="\n").write(text)


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

        def commit(message):
            g("-C", wt_r, "-c", "user.email=b@b", "-c", "user.name=b", "commit", "-q",
              "--allow-empty", "--cleanup=verbatim", "-F", "-", input=message.encode())

        def stop(pl):
            p = subprocess.run(["sh", script, "stop-check"], cwd=wt_r,
                               input=pl.encode(), capture_output=True)
            f = os.path.join(gd, "sdlc-close-out", "log")
            return (p.stdout.decode("utf-8", "replace"),
                    io.open(f, encoding="utf-8").read() if os.path.exists(f) else "")

        os.makedirs(os.path.join(gd, "sdlc-close-out"))
        io.open(os.path.join(gd, "sdlc-close-out", "deny-enabled"), "w").write("")
        commit(DEFECTIVE_BODY)
        out, log = stop(payload())
        check("wt_stop_blocks_from_worktree_gitdir",
              out.strip().startswith("{") and '"decision":"block"' in out
              and "stop: BLOCK - defective record on" in log
              and not os.path.exists(os.path.join(main_r, ".git", "sdlc-close-out")),
              out + "\n--- log ---\n" + log)

        os.remove(os.path.join(gd, "sdlc-close-out", "deny-enabled"))
        os.makedirs(os.path.join(gd, "sdlc-tdd"))
        io.open(os.path.join(gd, "sdlc-tdd", "session"), "w", newline="\n").write(SID)
        io.open(os.path.join(gd, "sdlc-tdd", "prod-write-observed"), "w").write("")
        commit(BARE_BODY)
        out, log = stop(payload())
        check("wt_stop_reads_guard_evidence_from_worktree_gitdir",
              "stop: WOULD-BLOCK (bare, log-only by design)" in log, log)

        idx = os.path.join(wt_r, "spec", "PROJECT_INDEX.md")
        os.makedirs(os.path.dirname(idx))
        io.open(idx, "w", newline="\n").write("a\nb\nc\n")
        g("-C", wt_r, "add", "spec/PROJECT_INDEX.md")
        commit("docs: close\n")
        p = subprocess.run(["sh", script, "docs-check"], cwd=wt_r, capture_output=True)
        f = os.path.join(gd, "sdlc-close-out", "log")
        log = io.open(f, encoding="utf-8").read() if os.path.exists(f) else ""
        check("wt_docs_check_logs_to_worktree_gitdir",
              p.returncode == 0 and "docs budget: OK - 3 lines added" in log, log)

        _reopen_git(wt_r, "gitdir: %s\n" % os.path.join(base, "nowhere").replace(os.sep, "/"))
        p = subprocess.run(["sh", script, "stop-check"], cwd=wt_r,
                           input=payload().encode(), capture_output=True)
        out = p.stdout.decode("utf-8", "replace")
        check("wt_unresolvable_gitdir_blocks_saying_it_did_not_run",
              '"decision":"block"' in out and "did not run" in out, out)
        p = subprocess.run(["sh", script, "stop-check"], cwd=wt_r,
                           input=payload(active=True).encode(), capture_output=True)
        check("wt_unresolvable_gitdir_stands_down_when_active",
              p.stdout.decode().strip() == "", p.stdout.decode())

        # The launchers. A broken install - the config present, the script not - must
        # reach someone: an exit code does not (measured: session log only); a stop
        # block does. Both dialects' stop launchers carry the same branch.
        broken = os.path.join(base, "broken")
        os.makedirs(os.path.join(broken, ".git"))
        hj = json.load(io.open(HOOK_JSON, encoding="utf-8"))
        entries = [h for hs in hj["hooks"].values() for h in hs]
        check("launcher_copilot_pins_cwd_and_no_dir_test",
              all(h.get("cwd") == "." and "-d .git" not in h["bash"]
                  and not any(c in h["bash"] for c in "\\$") for h in entries),
              json.dumps(entries))
        st = json.load(io.open(SETTINGS, encoding="utf-8"))
        claude_cmd = [h["command"] for blk in st["hooks"]["Stop"] for h in blk["hooks"]
                      if "sdlc-close-out.sh" in h["command"]]
        check("launcher_claude_no_dir_test", len(claude_cmd) == 1
              and "-d .git" not in claude_cmd[0], repr(claude_cmd))
        for label, argv in (("copilot", ["sh", "-c", entries[0]["bash"]]),
                            ("claude", ["sh", "-c", claude_cmd[0] if claude_cmd else "false"])):
            p = subprocess.run(argv, cwd=broken, input=payload().encode(), capture_output=True)
            out = p.stdout.decode("utf-8", "replace").strip()
            try:
                j = json.loads(out)
            except ValueError:
                j = {}
            check("launcher_%s_missing_script_blocks" % label,
                  j.get("decision") == "block" and "did not run" in (j.get("reason") or ""),
                  out)
            p = subprocess.run(argv, cwd=broken, input=payload(active=True).encode(),
                               capture_output=True)
            check("launcher_%s_missing_script_stands_down_when_active" % label,
                  p.stdout.decode().strip() == "", p.stdout.decode())
            # The other direction: at a root that HAS the script (the worktree above,
            # its .git a file), the launcher must take the script branch - a typo in its
            # -f path would otherwise block every stop, unseen by the shape check.
            _reopen_git(wt_r, "gitdir: %s\n" % gd.replace(os.sep, "/"))
            f = os.path.join(gd, "sdlc-close-out", "log")
            n0 = io.open(f, encoding="utf-8").read().count("\n") if os.path.exists(f) else 0
            p = subprocess.run(argv, cwd=wt_r, input=payload().encode(), capture_output=True)
            n1 = io.open(f, encoding="utf-8").read().count("\n") if os.path.exists(f) else 0
            check("launcher_%s_present_script_runs_it_no_block" % label,
                  "did not run" not in p.stdout.decode("utf-8", "replace") and n1 > n0,
                  p.stdout.decode("utf-8", "replace"))
    finally:
        shutil.rmtree(base, ignore_errors=True)
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
    # The verdict reads the MEDIAN, as the stop pass's has since §77: this machine adds
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
    print("slowest docs invocation: %.0f ms (S2 budget: 1000 ms)" % (slowest * 1000))
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- output ---\n%s" % (name, "; ".join(problems), out))
        sys.exit(1)
    if slowest >= 1.0:
        perf.append("docs invocation %.2f s (budget 1.00 s)" % slowest)

    print("\n== stop pass (%d cases) ==" % len(STOP_CASES))
    failures, times = guarded("stop pass", ([], {}), stop_pass, src, verbose=True)
    # Two budgets, both against the 30 s hook timeout: typical sessions hold a
    # handful of unpushed commits (< 1.5 s), and the cap case's 20-candidate walk
    # pays ~2 Windows-sh forks per candidate (measured ~3.5 s at cap on the dev
    # machine - bounded by the cap, nowhere near the timeout's fail-open edge).
    #
    # The typical verdict reads the MEDIAN, not the slowest (FEATURE_PLAN.md 77,
    # ruled 2026-09-04). It read the slowest for five releases and failed every run
    # at a suspiciously stable ~6.3 s, blamed first on load and then on nothing.
    # Bisected across v0.26.0..v0.31.0 in per-tag worktrees, the median does not
    # move - 1129 ms then, 1132 ms now - and this machine adds about ONE +5 s
    # stall per suite run, landing on a random case: the same case run 40 times in
    # one process gave median 1132 / p90 1263 with exactly one sample at 6203 ms.
    # A max over ~19 samples catches that stall nearly every time, which is why the
    # number looked stable across releases and identical loaded vs idle. The
    # slowest is still printed, because a real regression would move the median AND
    # show up there - it is an observation, not a verdict.
    #
    # The cap walk keeps its max: it is ONE case, so its max IS its measurement.
    # .pop with a default and guarded statistics: a crashed stop pass returns no
    # timings, and a KeyError here would re-create the abort this guard prevents.
    cap_t = times.pop("stop_candidate_cap_20", 0.0)
    ordered = sorted(times.values())
    typical = ordered[len(ordered) // 2] if ordered else 0.0
    worst = ordered[-1] if ordered else 0.0
    print("median stop invocation: %.0f ms (budget: 1500 ms; slowest of %d: %.0f ms,"
          " observed not asserted - FEATURE_PLAN 77); cap-20 walk: %.0f ms (budget: 5000 ms)"
          % (typical * 1000, len(ordered), worst * 1000, cap_t * 1000))
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- detail ---\n%s" % (name, "; ".join(problems), out))
        sys.exit(1)
    if typical >= 1.5:
        perf.append("median stop invocation %.2f s (budget 1.50 s)" % typical)
    if cap_t >= 5.0:
        # Best-of-2 for this one case (§77.7): it is a single sample, so the one stall
        # per run can land on it. A second walk that also breaches is a real breach.
        _, again = guarded("cap-20 re-walk", ([], {}), stop_pass, src, verbose=False,
                           only="stop_candidate_cap_20")
        retry = again.get("stop_candidate_cap_20", cap_t)
        print("cap-20 walk breached at %.0f ms; best-of-2 re-walk: %.0f ms"
              % (cap_t * 1000, retry * 1000))
        cap_t = min(cap_t, retry)
    if cap_t >= 5.0:
        perf.append("cap-20 stop walk %.2f s (budget 5.00 s)" % cap_t)

    print("\n== worktree + launcher pass (FEATURE_PLAN.md 78) ==")
    failures, _ = guarded("worktree pass", ([], 0.0), wt_pass, src, verbose=True)
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- detail ---\n%s" % (name, "; ".join(problems), out))
        sys.exit(1)

    print("\n== mutation pass (%d mutations, count derived) ==" % len(MUTATIONS))
    survivors = []
    stale = []
    for name, old, new in MUTATIONS:
        if old not in src:
            # Reported, never raised. An assert aborts the run, so every mutation after
            # a stale one never executes and one bad anchor hides all of them. A stale
            # mutation is also NOT a pass: it is a defect class that has silently lost
            # its coverage — which is how the §72 regression reached four releases.
            stale.append(name)
            print("  %-38s STALE - anchor no longer applies, re-point it" % name)
            continue
        mutated = src.replace(old, new)
        broke, _ = guarded("mutation (unit): %s" % name, ([], 0.0), unit_pass, mutated, verbose=False)
        where = "unit"
        if not broke:
            broke, _ = guarded("mutation (docs): %s" % name, ([], 0.0), docs_pass, mutated, verbose=False)
            where = "docs"
        if not broke:
            broke, _ = guarded("mutation (stop): %s" % name, ([], {}), stop_pass, mutated, verbose=False)
            where = "stop"
        if not broke:
            broke, _ = guarded("mutation (worktree): %s" % name, ([], 0.0), wt_pass, mutated, verbose=False)
            where = "worktree"
        print("  %-38s %s" % (name, "caught (%d %s case%s)" % (len(broke), where, "s" if len(broke) != 1 else "") if broke else "SURVIVED"))
        if not broke:
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
              " budgets. The stop budget now reads the median, so a single OS stall"
              " no longer breaches it; a breach here means the typical invocation"
              " really did slow down: FEATURE_PLAN 71, 77)")

    if guarded.crashed:
        print("\nCRASHED passes: %s - those cases did not run"
              % ", ".join(guarded.crashed))

    if survivors or stale or perf or guarded.crashed:
        sys.exit(1)

    print("\nall green: %d unit + %d docs + %d stop cases, %d mutations caught"
          % (len(CASES), len(DOCS_CASES), len(STOP_CASES), len(MUTATIONS)))


if __name__ == "__main__":
    main()
