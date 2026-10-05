# -*- coding: utf-8 -*-
"""Re-runnable proof for templates/sdlc-impact.template.py (FEATURE_PLAN.md §66).

Two passes, and the second is the point:

  1. a case pass driving the adapter through its real interface over per-case bench
     git repos, each with a real `.ua/` directory built from tools/impact-fixtures/ -
     the seed pair MINIMIZED FROM AN OBSERVED Understand Anything graph, never
     invented (§66.2 (a) is a blocker ruling on exactly that). Every negative case
     spec §23 requires is here, plus the two the kit's own deltas add: an un-ignored
     UA directory, and a slice base recorded on another branch;
  2. a mutation pass that breaks the adapter - the count derived from the MUTATIONS
     list at run time, never stated here - and requires pass 1 to notice each one. A
     suite that survives its own mutations is not testing the thing it claims to
     (invariant 13).

Why the fixture is real: cases 5, 6 and 7 are the ones an invented graph gets wrong
without anyone noticing. The seed carries genuine instances - usage_store.py with
five nodes; a file->class pair joined by BOTH `contains` and `exports`; that same
pair both-changed and adjacent - so "all nodes map", "emit the neighbour once" and
"a changed node is never also affected" are tested against structure that actually
occurred rather than structure written to make them pass.

Kit-development artifact: lives at the root, never ships inside sdlc-kit/.
Run from anywhere:  python tools/impact-check.py
"""

import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ADAPTER = os.path.join(REPO, "sdlc-kit", "templates", "sdlc-impact.template.py")
FIXTURES = os.path.join(REPO, "tools", "impact-fixtures")


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


def run_git(cwd, *args):
    p = subprocess.run(("git",) + args, cwd=cwd, capture_output=True)
    return p.returncode, p.stdout.decode("utf-8", "replace")


class Bench(object):
    """A throwaway git repo with a real UA directory, built per case."""

    def __init__(self, adapter_src, ua_dir=".ua", ignore_ua=True):
        self.root = tempfile.mkdtemp(prefix="impact-bench-")
        self.adapter = os.path.join(self.root, "adapter.py")
        with io.open(adapter_src, "rb") as fh:
            body = fh.read()
        with io.open(self.adapter, "wb") as fh:
            fh.write(body)
        run_git(self.root, "init", "-q", ".")
        run_git(self.root, "config", "user.email", "proof@example.invalid")
        run_git(self.root, "config", "user.name", "proof")
        self.ua_dir = ua_dir
        self.ua = os.path.join(self.root, ua_dir)
        os.makedirs(self.ua)
        self.write(".gitignore", ("%s/\nadapter.py\n" % ua_dir) if ignore_ua
                   else "adapter.py\n")

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        parent = os.path.dirname(path)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent)
        with io.open(path, "wb") as fh:
            fh.write(text.encode("utf-8"))

    def install_graph(self, graph=True, meta=True, overlay=False, malformed=False):
        if graph:
            src = os.path.join(FIXTURES, "knowledge-graph.json")
            dst = os.path.join(self.ua, "knowledge-graph.json")
            if malformed:
                with io.open(dst, "wb") as fh:
                    fh.write(b'{"nodes": [ this is not json')
            else:
                shutil.copyfile(src, dst)
        if meta:
            shutil.copyfile(os.path.join(FIXTURES, "meta.json"),
                            os.path.join(self.ua, "meta.json"))
        if overlay:
            shutil.copyfile(os.path.join(FIXTURES, "diff-overlay.json"),
                            os.path.join(self.ua, "diff-overlay.json"))

    def set_meta_commit(self, sha):
        path = os.path.join(self.ua, "meta.json")
        with io.open(path, "rb") as fh:
            meta = json.loads(fh.read().decode("utf-8"))
        meta["gitCommitHash"] = sha
        with io.open(path, "wb") as fh:
            fh.write((json.dumps(meta, indent=2) + "\n").encode("utf-8"))

    def commit(self, message="c"):
        run_git(self.root, "add", "-A")
        run_git(self.root, "commit", "-q", "-m", message)
        return self.head()

    def head(self):
        return run_git(self.root, "rev-parse", "HEAD")[1].strip()

    def branch(self, name):
        run_git(self.root, "checkout", "-q", "-b", name)

    def adapt(self, *args):
        p = subprocess.run([sys.executable, self.adapter] + list(args),
                           cwd=self.root, capture_output=True)
        return (p.returncode,
                p.stdout.decode("utf-8", "replace").replace("\r\n", "\n").strip())

    def overlay(self):
        path = os.path.join(self.ua, "diff-overlay.json")
        if not os.path.isfile(path):
            return None
        with io.open(path, "rb") as fh:
            return json.loads(fh.read().decode("utf-8"))

    def destroy(self):
        shutil.rmtree(self.root, ignore_errors=True)


def base_slice(bench):
    """The shared arrangement: graph installed, one commit, base recorded."""
    bench.install_graph()
    bench.write("usage_store.py", "original\n")
    bench.write("tfit_qa_server.py", "original\n")
    bench.commit("base")
    bench.adapt("record-base")


# ---- the cases. Each returns (bench, argv) and is asserted against must/must-not.

def c_no_graph(b):
    b.write("usage_store.py", "x\n")
    b.commit("base")
    return ("slice",)


def c_unmatched_new_file(b):
    base_slice(b)
    b.write("usage_store.py", "changed\n")
    b.write("usage_pricing.py", "brand new, absent from the graph\n")
    return ("slice",)


def c_untracked_new_file(b):
    base_slice(b)
    b.write("usage_store.py", "changed\n")
    b.write("never_added.py", "untracked and not ignored\n")
    return ("slice",)


def c_multiple_nodes_one_file(b):
    base_slice(b)
    b.write("usage_store.py", "changed\n")
    return ("slice",)


def c_intermediate_commit(b):
    base_slice(b)
    b.write("usage_store.py", "step one\n")
    b.commit("mid-slice commit")
    b.write("tfit_qa_server.py", "step two\n")
    return ("slice",)


def c_ua_files_excluded(b):
    base_slice(b)
    b.write("usage_store.py", "changed\n")
    # Regenerating UA's own artifacts must not enter the project's denominator.
    b.install_graph(overlay=True)
    return ("slice",)


def c_ua_not_ignored(b):
    base_slice(b)
    b.write("usage_store.py", "changed\n")
    return ("slice",)


def c_ua_files_excluded_when_visible(b):
    """The path exclusion, exercised where .gitignore is NOT doing the work.

    In an ignored UA directory git never reports those files at all, so a bench built
    that way pins nothing about the adapter's own exclusion — the mutation that
    deletes it survives, which is how this case came to exist. Here the directory is
    visible to git, so UA's regenerated artifacts are real untracked files in
    `git status`, and only the adapter's path rule can keep them out of the project's
    changed-file denominator.
    """
    base_slice(b)
    b.write("usage_store.py", "changed\n")
    b.install_graph(overlay=True)
    return ("slice",)


def c_malformed_graph(b):
    b.install_graph(malformed=True)
    b.write("usage_store.py", "x\n")
    b.commit("base")
    b.adapt("record-base")
    b.write("usage_store.py", "changed\n")
    return ("slice",)


def c_no_base_recorded(b):
    b.install_graph()
    b.write("usage_store.py", "x\n")
    b.commit("base")
    return ("slice",)


def c_base_on_other_branch(b):
    base_slice(b)
    b.branch("other-arc")
    b.write("usage_store.py", "changed\n")
    return ("slice",)


def c_stale_for_project_files(b):
    b.install_graph()
    b.write("usage_store.py", "original\n")
    old = b.commit("graph was built here")
    b.set_meta_commit(old)
    b.write("usage_store.py", "changed after the graph was built\n")
    b.commit("later work the graph never saw")
    b.adapt("record-base")
    b.write("usage_store.py", "and changed again in this slice\n")
    return ("slice",)


def c_graph_current_at_base(b):
    """A graph built AT the base is current, however much this slice then changes.

    This pins the rule delta (g) actually specifies: freshness is measured
    graph-commit against the BASE, never against the working tree. Measuring against
    the working tree calls this stale - the slice edits a file the graph has not seen
    - and COMPLETE becomes unreachable on virtually every slice.

    NOTE a deliberate gap: spec §23 case 3 wants an OLDER graph not called stale when
    only unrelated files changed in between. That needs the monorepo project-path
    scope delta (g) explicitly defers to a monorepo adopter, so under v1 any project
    file changed between graph commit and base counts - see c_stale_for_project_files.
    This case pins the half v1 does implement.
    """
    b.install_graph()
    b.write("usage_store.py", "original\n")
    b.write("unrelated_notes.md", "one\n")
    at_base = b.commit("the graph was built at exactly this commit")
    b.set_meta_commit(at_base)
    b.adapt("record-base")
    b.write("usage_store.py", "this slice's own change, unseen by the graph\n")
    return ("slice",)


def c_phase_scope(b):
    b.install_graph()
    b.write("usage_store.py", "original\n")
    b.commit("main")
    run_git(b.root, "branch", "-M", "main")
    b.branch("feat/phase-99")
    b.write("usage_store.py", "arc work\n")
    b.commit("slice 1")
    b.write("tfit_qa_server.py", "more arc work\n")
    b.commit("slice 2")
    return ("phase", "main")


def c_graph_inside_change_set(b):
    """The slice-end refresh: the graph was rebuilt at a commit INSIDE the arc. The
    phase view's base is where the arc branched, so the plain diff is non-empty - and
    reading that as stale would call every refreshed graph stale at every phase close."""
    b.install_graph()
    b.write("usage_store.py", "original\n")
    b.commit("main")
    run_git(b.root, "branch", "-M", "main")
    b.branch("feat/phase-99")
    b.write("usage_store.py", "slice 1\n")
    s1 = b.commit("slice 1 - the graph is refreshed here")
    b.set_meta_commit(s1)
    b.write("tfit_qa_server.py", "slice 2\n")
    b.commit("slice 2")
    return ("phase", "main")


def c_tracked_graph_refresh_commit(b):
    """A TRACKED graph directory: the slice-end refresh lands as its own commit, which
    touches only UA files. The next slice's base is that commit; the graph was built one
    commit earlier. Counting UA's own files would call a just-refreshed graph stale."""
    b.install_graph()
    b.write("usage_store.py", "original\n")
    built = b.commit("the slice the graph was rebuilt at")
    b.set_meta_commit(built)
    b.commit("chore(graph): refresh after the slice")
    b.adapt("record-base")
    b.write("usage_store.py", "the next slice's change\n")
    return ("slice",)


def c_graph_on_sibling_branch(b):
    """A graph built on ANOTHER branch also descends from the base, but describes a
    tree this branch never had - the ancestor test against HEAD is what refuses it."""
    b.install_graph()
    b.write("usage_store.py", "original\n")
    b.commit("main")
    run_git(b.root, "branch", "-M", "main")
    b.branch("elsewhere")
    b.write("usage_store.py", "a change this arc never had\n")
    other = b.commit("graph built on a sibling branch")
    run_git(b.root, "checkout", "-q", "main")
    b.branch("feat/phase-99")
    b.set_meta_commit(other)
    b.write("tfit_qa_server.py", "arc work\n")
    b.commit("slice 1")
    return ("phase", "main")


def c_phase_bad_ref(b):
    base_slice(b)
    return ("phase", "no-such-ref")


def c_clear_base(b):
    base_slice(b)
    b.adapt("clear-base")
    b.write("usage_store.py", "changed\n")
    return ("slice",)


def c_unknown_mode(b):
    base_slice(b)
    return ("frobnicate",)


# (name, setup, argv-from-setup, must-contain, must-NOT-contain, extra assertion)
CASES = [
    ("no_graph_is_unavailable", c_no_graph,
     # The reason must name the missing graph, not the missing slice base: a project
     # without UA would otherwise be told to run /next-slice, which would not record
     # a base either.
     ["SDLC IMPACT: UNAVAILABLE", "knowledge graph not found"],
     ["COMPLETE", "PARTIAL", "ERROR", "no slice base recorded"], None),

    ("unmatched_file_is_partial_and_named", c_unmatched_new_file,
     ["SDLC IMPACT: PARTIAL", "unmatched-files: 1", "usage_pricing.py",
      "changed-files: 2", "mapped-files: 1"],
     ["SDLC IMPACT: COMPLETE"], None),

    ("untracked_file_counts_in_denominator", c_untracked_new_file,
     # One tracked file modified plus one untracked file added = 2. The point is that
     # the untracked one is IN the denominator and named as unmatched, not that the
     # count is large.
     ["changed-files: 2", "never_added.py", "unmatched-files: 1"], [], None),

    ("all_nodes_of_a_changed_file_map", c_multiple_nodes_one_file,
     ["SDLC IMPACT: COMPLETE", "changed-files: 1", "mapped-files: 1",
      "changed-nodes: 5"], ["unmatched-files: 1"], None),

    ("intermediate_commit_still_in_change_set", c_intermediate_commit,
     ["changed-files: 2"], [], None),

    ("ua_generated_files_excluded", c_ua_files_excluded,
     ["changed-files: 1"], ["diff-overlay.json,", "knowledge-graph.json,"], None),

    ("malformed_graph_is_error_not_complete", c_malformed_graph,
     ["SDLC IMPACT: ERROR", "malformed"],
     ["COMPLETE", "PARTIAL", "UNAVAILABLE"], None),

    ("no_base_is_unavailable", c_no_base_recorded,
     ["SDLC IMPACT: UNAVAILABLE", "no slice base recorded"],
     ["COMPLETE", "PARTIAL"], None),

    ("base_from_another_branch_is_refused", c_base_on_other_branch,
     ["SDLC IMPACT: UNAVAILABLE", "recorded on", "HEAD is on"],
     ["COMPLETE", "PARTIAL"], None),

    ("stale_graph_says_so", c_stale_for_project_files,
     ["SDLC IMPACT: PARTIAL", "may be stale", "between graph commit"],
     ["SDLC IMPACT: COMPLETE"], None),

    ("graph_current_at_base_despite_slice_edits", c_graph_current_at_base,
     ["SDLC IMPACT: COMPLETE", "current at the base"],
     ["may be stale", "PARTIAL"], None),

    ("phase_scope_spans_the_arc", c_phase_scope,
     ["scope: phase", "changed-files: 2"], ["scope: slice"], None),

    ("graph_refreshed_inside_the_arc_is_current", c_graph_inside_change_set,
     ["built inside this change set"], ["may be stale"], None),

    ("tracked_graph_refresh_commit_is_not_staleness", c_tracked_graph_refresh_commit,
     ["current at the base"], ["may be stale"], None),

    ("graph_from_a_sibling_branch_is_stale", c_graph_on_sibling_branch,
     ["may be stale"], ["built inside this change set"], None),

    ("phase_bad_ref_is_unavailable", c_phase_bad_ref,
     ["SDLC IMPACT: UNAVAILABLE", "does not resolve"], ["COMPLETE"], None),

    ("cleared_base_is_unavailable", c_clear_base,
     ["SDLC IMPACT: UNAVAILABLE", "no slice base recorded"], ["COMPLETE"], None),

    ("unknown_mode_is_error", c_unknown_mode,
     ["SDLC IMPACT: ERROR", "unknown mode"], ["COMPLETE", "PARTIAL"], None),
]


def assert_overlay_disjoint(bench, out):
    """Cases 6 and 7, asserted on the artifact rather than on the summary.

    The counts can look right while the overlay is wrong, so this reads the written
    file: no id appears in both lists, and no list repeats an id. The seed's
    file->class pair is joined by two edges and is both-changed, so a regression in
    either rule shows up here.
    """
    o = bench.overlay()
    if o is None:
        return "overlay was not written"
    c, a = o["changedNodeIds"], o["affectedNodeIds"]
    problems = []
    if set(c) & set(a):
        problems.append("changed and affected overlap: %s" % sorted(set(c) & set(a)))
    if len(a) != len(set(a)):
        problems.append("affected has duplicates")
    if len(c) != len(set(c)):
        problems.append("changed has duplicates")
    if "class:usage_store.py:UsageStore" not in c:
        problems.append("the both-changed class is missing from changedNodeIds")
    return "; ".join(problems)


def assert_overlay_absent(bench, out):
    if bench.overlay() is not None:
        return "overlay was written into a UA directory git does not ignore"
    return ""


CASES[3] = CASES[3][:4] + (assert_overlay_disjoint,)
CASES.append(("not_ignored_ua_dir_writes_nothing", c_ua_not_ignored,
              ["not written", "not git-ignored"], [], assert_overlay_absent))
CASES.append(("ua_files_excluded_even_when_git_sees_them",
              c_ua_files_excluded_when_visible,
              ["changed-files: 1"],
              ["knowledge-graph.json", "meta.json"], None))

# Benches whose UA directory is deliberately NOT git-ignored, so git reports its
# contents and the adapter's own path rules are the only thing standing between
# UA's artifacts and the project's denominator.
UNIGNORED = {"not_ignored_ua_dir_writes_nothing",
             "ua_files_excluded_even_when_git_sees_them",
             "tracked_graph_refresh_commit_is_not_staleness"}


def case_pass(adapter_src, verbose=True):
    failures = []
    for entry in CASES:
        name, setup, must, must_not, extra = entry
        ignore = name not in UNIGNORED
        b = Bench(adapter_src, ignore_ua=ignore)
        try:
            argv = setup(b)
            code, out = b.adapt(*argv)
            problems = []
            for token in must:
                if token not in out:
                    problems.append("missing %r" % token)
            for token in must_not:
                if token in out:
                    problems.append("unexpected %r" % token)
            if code != 0:
                problems.append("exit %d (the adapter must never fail a step)" % code)
            if extra:
                extra_problem = extra(b, out)
                if extra_problem:
                    problems.append(extra_problem)
            if problems:
                failures.append((name, "; ".join(problems), out))
            elif verbose:
                print("  %-42s ok" % name)
        finally:
            b.destroy()
    return failures


# One mutation per defect class the corpus pins. Each must break >= 1 case.
MUTATIONS = [
    ("changed_nodes_leak_into_affected",
     "    return sorted(affected - changed_set)",
     "    return sorted(affected)"),
    ("affected_not_deduplicated",
     "    changed_set = set(changed_ids)\n    affected = set()",
     "    changed_set = set(changed_ids)\n    affected = []"),
    ("only_the_file_node_maps",
     '        if path in changed_set:',
     '        if path in changed_set and node.get("type") == "file":'),
    ("unmatched_files_not_reported",
     "    return [i for i in ids if i], sorted(changed_set - matched)",
     "    return [i for i in ids if i], []"),
    ("untracked_files_dropped",
     '    code, out = git("-C", root, "ls-files", "--others", "--exclude-standard")',
     '    code, out = git("-C", root, "ls-files", "--others", "--no-such-flag")'),
    ("ua_files_enter_the_denominator",
     '        if f and not (prefix and (f == ua_name or f.startswith(prefix)))',
     '        if f'),
    ("malformed_graph_reported_unavailable",
     '        return None, "graph JSON is malformed (%s)" % exc',
     '        return None, None'),
    ("wrong_branch_base_accepted",
     '    if current != branch:',
     '    if False:'),
    # RE-POINTED at 0.33.0: the since-list gained the graph-directory exclusion, so the
    # old anchor no longer applied - reported STALE by the suite, as designed.
    ("staleness_never_detected",
     '    if not since:\n        return "current at the base',
     '    since = []\n    if not since:\n        return "current at the base'),
    ("freshness_measured_against_the_working_tree",
     '    code, out = git("-C", root, "diff", "--name-only", commit, base, "--")',
     '    code, out = git("-C", root, "diff", "--name-only", commit, "--")'),
    ("graph_refresh_commit_counted_as_staleness",
     '             if f and f != ua_name and not f.startswith(ua_name + "/")] if out else []',
     '             if f] if out else []'),
    ("graph_inside_the_arc_called_stale",
     '    if inside:',
     '    if False:'),
    ("sibling_branch_graph_called_current",
     '              and git("-C", root, "merge-base", "--is-ancestor", commit, "HEAD")[0] == 0)',
     '              and True)'),
    ("overlay_written_into_tracked_dir",
     '    if not is_ignored(root, ua_name):',
     '    if False:'),
    ("partial_reported_as_complete",
     '    state = "COMPLETE" if not unmatched and not stale else "PARTIAL"',
     '    state = "COMPLETE"'),
    ("phase_base_not_verified",
     '        code, base = git("-C", root, "rev-parse", "--verify", "--quiet",\n'
     '                         base_ref + "^{commit}")',
     '        code, base = 0, base_ref'),
]


def mutation_pass(verbose=True):
    with io.open(ADAPTER, encoding="utf-8", newline="") as fh:
        original = fh.read()
    survived = []
    tmp = tempfile.mkdtemp(prefix="impact-mut-")
    try:
        for name, old, new in MUTATIONS:
            if old not in original:
                survived.append("%s (anchor not found - the mutation is stale)" % name)
                continue
            path = os.path.join(tmp, "mutant.py")
            with io.open(path, "w", encoding="utf-8", newline="") as fh:
                fh.write(original.replace(old, new, 1))
            failures = case_pass(path, verbose=False)
            if failures:
                if verbose:
                    print("  %-42s caught (%d cases)" % (name, len(failures)))
            else:
                survived.append(name)
                if verbose:
                    print("  %-42s SURVIVED" % name)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return survived


def main():
    if not os.path.isfile(ADAPTER):
        print("CANNOT RUN: adapter not found at %s" % ADAPTER)
        return 2
    print("== case pass (%d cases) ==" % len(CASES))
    failures = guarded("case pass", [], case_pass, ADAPTER, verbose=True)
    if failures:
        for name, problems, out in failures:
            print("\nFAILED %s: %s\n--- output ---\n%s" % (name, problems, out))
        return 1

    print("\n== mutation pass (%d mutations) ==" % len(MUTATIONS))
    survived = guarded("mutation pass", [], mutation_pass, verbose=True)
    if survived:
        print("\nMUTATIONS SURVIVED: %s - the corpus does not pin what it claims"
              % ", ".join(survived))
        return 1

    if guarded.crashed:
        print("\nCRASHED passes: %s - those cases did not run"
              % ", ".join(guarded.crashed))
        return 1
    print("\nall green: %d cases, %d mutations caught"
          % (len(CASES), len(MUTATIONS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
