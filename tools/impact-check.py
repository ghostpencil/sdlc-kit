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

# The two plugin homes, as the adapter globs them (relative to the home directory).
CLAUDE_HOME = (".claude", "plugins", "cache", "understand-anything", "understand-anything")
COPILOT_HOME = (".copilot", "installed-plugins", "_direct")

# Stands in for Understand Anything's skills/understand/scan-project.mjs. It refuses an
# invocation the real scanner would answer differently - a root that is not the
# project, or a scan that would list the graph's own directory - and otherwise writes
# the entries the case chose from the observed scan (tools/impact-fixtures/SEED.md).
FIXTURE_SCANNER = r"""
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
const [root, out, ...rest] = process.argv.slice(2);
if (!rest.includes('--exclude-analysis-data')) {
  process.stderr.write('fixture scanner: --exclude-analysis-data not passed');
  process.exit(9);
}
if (!existsSync(join(root, '.git'))) {
  process.stderr.write('fixture scanner: root is not the project root');
  process.exit(8);
}
writeFileSync(out, readFileSync(new URL('./scan-output.json', import.meta.url)));
"""
FAILING_SCANNER = "process.stderr.write('scan blew up'); process.exit(3);\n"
GARBAGE_SCANNER = r"""
import { writeFileSync } from 'node:fs';
writeFileSync(process.argv[3], 'this is not json');
"""

# The graph's eight files, as the observed scan lists them - and four it lacks.
IN_GRAPH = ["spec/PRODUCT_CONTRACT.md", "spec/PROJECT_INDEX.md",
            "tests/test_usage_store.py", "tests/test_usage_wiring.py",
            "tfit_qa_server.py", "tfit_ratelimit.py", "tools/build_golden_set.py",
            "usage_store.py"]
CODE_NOT_IN_GRAPH = ".github/hooks/sdlc-cosmetic.py"
SCRIPT_NOT_IN_GRAPH = "docker-entrypoint.sh"
DOCS_NOT_IN_GRAPH = "README.md"
CONFIG_NOT_IN_GRAPH = "pyproject.toml"

# plugin-fix: the observed head of Understand Anything 2.9.4's skills/understand/SKILL.md
# (Copilot install, 2026-10-19), CRLF as installed, plus a body line that must survive.
HINT = ("[path] [--full|--auto-update|--no-auto-update|--review|--language <lang>"
        "|--exclude <patterns>]")
LISTED_SKILL = ("---\r\nname: understand\r\ndescription: Analyze a codebase to produce an "
                "interactive knowledge graph for understanding architecture, components, "
                "and relationships\r\nargument-hint: [\"%s\"]\r\n---\r\n\r\n# /understand"
                "\r\n\r\nargument-hint: [\"a body line, not frontmatter\"]\r\n" % HINT)
FIXED_SKILL = LISTED_SKILL.replace('argument-hint: ["%s"]' % HINT,
                                   'argument-hint: "%s"' % HINT)
STRING_SKILL = "---\nname: understand-chat\nargument-hint: \"[query]\"\n---\n\nbody\n"
# plugin-fix's hooks half: the plugin's hooks.json verbatim (2.9.4 = 2.9.7, CRLF; see
# tools/impact-fixtures/SEED.md), the script the adapter installs beside it, and a
# hooks.json from a plugin that no longer ships the two auto-update hooks.
with io.open(os.path.join(FIXTURES, "ua-hooks.json"), "rb") as _fh:
    UA_HOOKS = _fh.read().decode("utf-8")
HOOK_SCRIPT_NAME = "sdlc-kit-copilot-hooks.mjs"
OTHER_HOOKS = ('{\r\n  "hooks": {\r\n    "SessionStart": [\r\n      {\r\n        "hooks": '
               '[\r\n          {\r\n            "type": "command",\r\n            "command":'
               ' "node \\"${CLAUDE_PLUGIN_ROOT}/hooks/welcome.mjs\\""\r\n          }\r\n'
               '        ]\r\n      }\r\n    ]\r\n  }\r\n}\r\n')


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
        # Every run sees a throwaway home, so the machine's own plugin installs can
        # never answer a coverage case; the coverage cases build plugin homes in it.
        self.home = tempfile.mkdtemp(prefix="impact-home-")
        self.path = os.environ.get("PATH", "")

    def install_scanner(self, home_parts, version, files=None, body=None,
                        package=True):
        """A fixture scanner in a plugin home: by default it checks the arguments the
        real one is given and writes the chosen entries of the observed scan."""
        plugin = os.path.join(self.home, *home_parts)
        skill = os.path.join(plugin, "skills", "understand")
        os.makedirs(skill)
        if package:
            with io.open(os.path.join(plugin, "package.json"), "wb") as fh:
                fh.write(json.dumps({"name": "@understand-anything/skill",
                                     "version": version}).encode("utf-8"))
        with io.open(os.path.join(skill, "scan-project.mjs"), "wb") as fh:
            fh.write((body or FIXTURE_SCANNER).encode("utf-8"))
        if files is not None:
            with io.open(os.path.join(FIXTURES, "scan-result.json"), "rb") as fh:
                scan = json.loads(fh.read().decode("utf-8"))
            scan["files"] = [f for f in scan["files"] if f["path"] in files]
            missing = set(files) - set(f["path"] for f in scan["files"])
            assert not missing, "not in the observed scan: %s" % sorted(missing)
            with io.open(os.path.join(skill, "scan-output.json"), "wb") as fh:
                fh.write(json.dumps(scan).encode("utf-8"))

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

    def write_skill(self, plugin_parts, name, text):
        path = os.path.join(self.home, *(plugin_parts + ("skills", name, "SKILL.md")))
        if not os.path.isdir(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))
        with io.open(path, "wb") as fh:
            fh.write(text.encode("utf-8"))
        return path

    def adapt(self, *args):
        env = dict(os.environ, HOME=self.home, USERPROFILE=self.home, PATH=self.path)
        p = subprocess.run([sys.executable, self.adapter] + list(args),
                           cwd=self.root, capture_output=True, env=env)
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
        shutil.rmtree(self.home, ignore_errors=True)


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


# ---- coverage: the phase-end trigger for a full rebuild (FEATURE_PLAN.md §83).

def coverage_bench(b, files, plugin=CLAUDE_HOME + ("2.9.7",)):
    b.install_graph()
    b.commit("graph present")
    b.install_scanner(plugin, "2.9.7", files=files)
    return ("coverage",)


def c_cov_complete(b):
    return coverage_bench(b, IN_GRAPH)


def c_cov_code_missing(b):
    return coverage_bench(b, IN_GRAPH + [CODE_NOT_IN_GRAPH])


def c_cov_script_missing(b):
    return coverage_bench(b, IN_GRAPH + [SCRIPT_NOT_IN_GRAPH])


def c_cov_docs_never_trigger(b):
    return coverage_bench(b, IN_GRAPH + [DOCS_NOT_IN_GRAPH, CONFIG_NOT_IN_GRAPH])


def c_cov_newest_version_wins(b):
    """2.9.10 must beat 2.9.9: a string sort picks 2.9.9, whose scanner fails."""
    b.install_graph()
    b.commit("graph present")
    b.install_scanner(CLAUDE_HOME + ("2.9.9",), "2.9.9", body=FAILING_SCANNER)
    # No package.json here: the version must come from the directory name.
    b.install_scanner(CLAUDE_HOME + ("2.9.10",), "2.9.10", files=IN_GRAPH,
                      package=False)
    return ("coverage",)


def c_cov_newest_across_homes(b):
    """The newest install wins wherever it lives - here the Copilot one."""
    b.install_graph()
    b.commit("graph present")
    b.install_scanner(CLAUDE_HOME + ("2.9.4",), "2.9.4", body=FAILING_SCANNER)
    b.install_scanner(COPILOT_HOME + ("ua",), "2.9.7", files=IN_GRAPH)
    return ("coverage",)


def c_cov_copilot_only(b):
    return coverage_bench(b, IN_GRAPH, plugin=COPILOT_HOME + ("ua",))


def c_cov_no_plugin(b):
    b.install_graph()
    b.commit("graph present")
    return ("coverage",)


def c_cov_no_node(b):
    coverage_bench(b, IN_GRAPH)
    # git stays reachable; node does not. If node shares git's directory on this
    # machine the case cannot be built, and says so rather than passing.
    git_dir = os.path.dirname(shutil.which("git"))
    if shutil.which("node", path=git_dir):
        raise RuntimeError("node sits beside git in %s - no-node case unbuildable"
                           % git_dir)
    b.path = git_dir
    return ("coverage",)


def c_cov_scanner_fails(b):
    b.install_graph()
    b.commit("graph present")
    b.install_scanner(CLAUDE_HOME + ("2.9.7",), "2.9.7", body=FAILING_SCANNER)
    return ("coverage",)


def c_cov_scanner_garbage(b):
    b.install_graph()
    b.commit("graph present")
    b.install_scanner(CLAUDE_HOME + ("2.9.7",), "2.9.7", body=GARBAGE_SCANNER)
    return ("coverage",)


def c_cov_no_graph(b):
    b.write("usage_store.py", "x\n")
    b.commit("base")
    b.install_scanner(CLAUDE_HOME + ("2.9.7",), "2.9.7", files=IN_GRAPH)
    return ("coverage",)


def c_cov_malformed_graph(b):
    b.install_graph(malformed=True)
    b.commit("graph present")
    b.install_scanner(CLAUDE_HOME + ("2.9.7",), "2.9.7", files=IN_GRAPH)
    return ("coverage",)


# ---- refresh-check: whether the slice-end incremental refresh runs.

def c_rc_graph_behind(b):
    b.install_graph()
    b.write("usage_store.py", "original\n")
    built = b.commit("graph built here")
    b.set_meta_commit(built)
    b.write("usage_store.py", "the slice's change\n")
    b.commit("the slice")
    return ("refresh-check",)


def c_rc_graph_at_head(b):
    b.install_graph()
    b.write("usage_store.py", "original\n")
    head = b.commit("the slice, and the graph is already here")
    b.set_meta_commit(head)
    return ("refresh-check",)


def c_rc_no_meta(b):
    b.install_graph(meta=False)
    b.write("usage_store.py", "original\n")
    b.commit("the slice")
    return ("refresh-check",)


def c_rc_no_graph(b):
    b.write("usage_store.py", "original\n")
    b.commit("the slice")
    return ("refresh-check",)


# ---- plugin-fix: Copilot CLI drops a skill whose argument-hint is a list.

def write_hooks(b, plugin_parts, text):
    path = os.path.join(b.home, *(plugin_parts + ("hooks", "hooks.json")))
    os.makedirs(os.path.dirname(path))
    with io.open(path, "wb") as fh:
        fh.write(text.encode("utf-8"))
    return path


def plugin_fix_bench(b, hooks=UA_HOOKS):
    b.commit("a repository")
    copilot = COPILOT_HOME + ("ua",)
    b.install_scanner(copilot, "2.9.4", files=IN_GRAPH)
    b.listed = b.write_skill(copilot, "understand", LISTED_SKILL)
    b.string = b.write_skill(copilot, "understand-chat", STRING_SKILL)
    b.hooks = write_hooks(b, copilot, hooks)
    b.hooks_text = hooks
    b.script = os.path.join(os.path.dirname(b.hooks), HOOK_SCRIPT_NAME)
    return ("plugin-fix",)


def c_pf_fixes_copilot(b):
    return plugin_fix_bench(b)


def c_pf_idempotent(b):
    argv = plugin_fix_bench(b)
    b.adapt(*argv)
    return argv


def c_pf_claude_untouched(b):
    argv = plugin_fix_bench(b)
    claude = CLAUDE_HOME + ("2.9.7",)
    b.install_scanner(claude, "2.9.7", files=IN_GRAPH)
    b.claude = b.write_skill(claude, "understand", LISTED_SKILL)
    b.claude_hooks = write_hooks(b, claude, UA_HOOKS)
    return argv


def c_pf_no_install(b):
    b.commit("a repository")
    b.install_scanner(CLAUDE_HOME + ("2.9.7",), "2.9.7", files=IN_GRAPH)
    return ("plugin-fix",)


def c_pf_unrecognized_hooks(b):
    return plugin_fix_bench(b, hooks=OTHER_HOOKS)


def hook_project(b, auto_update=True, current=False):
    """The bench as a project the hooks report on: a graph, autoUpdate as given, and a
    build commit that is HEAD or is not."""
    argv = plugin_fix_bench(b)
    b.install_graph()
    b.write(os.path.join(b.ua_dir, "config.json"),
            json.dumps({"autoUpdate": auto_update}))
    if current:
        b.set_meta_commit(b.head())
    return argv


def c_pf_hooks_stale(b):
    return hook_project(b)


def c_pf_hooks_current(b):
    return hook_project(b, current=True)


def c_pf_hooks_auto_update_off(b):
    return hook_project(b, auto_update=False)


def read_text(path):
    with io.open(path, "rb") as fh:
        return fh.read().decode("utf-8")


def fixed_hooks(bench):
    """The plugin's hooks.json with exactly the two command lines replaced, CRLF kept."""
    script = bench.script.replace(os.sep, "/")
    lines = []
    for line in UA_HOOKS.splitlines(True):
        for marker, mode in (("post-tool-use-auto-update.mjs", "post-tool-use"),
                             ("auto-update-prompt.md", "session-start")):
            if marker in line:
                line = ('            "command": "node \\"%s\\" %s"\r\n' % (script, mode))
        lines.append(line)
    return "".join(lines)


def assert_skills_fixed(bench, out):
    """Byte-exact: the frontmatter hint is a string, CRLF kept, the body line and the
    already-string skill untouched, hooks.json changed in its two commands only, and a
    Claude Code install never written."""
    problems = []
    if read_text(bench.listed) != FIXED_SKILL:
        problems.append("understand/SKILL.md is not exactly the fixed text: %r"
                        % read_text(bench.listed)[:300])
    if read_text(bench.string) != STRING_SKILL:
        problems.append("a skill that needed no fix was rewritten")
    if read_text(bench.hooks) != fixed_hooks(bench):
        problems.append("hooks.json is not exactly the fixed text: %r"
                        % read_text(bench.hooks)[:400])
    if not os.path.isfile(bench.script):
        problems.append("the hook script was not installed")
    if getattr(bench, "claude", None) and read_text(bench.claude) != LISTED_SKILL:
        problems.append("the Claude Code install was rewritten")
    if (getattr(bench, "claude_hooks", None)
            and read_text(bench.claude_hooks) != UA_HOOKS):
        problems.append("the Claude Code install's hooks.json was rewritten")
    return "; ".join(problems)


def assert_hooks_untouched(bench, out):
    problems = []
    if read_text(bench.hooks) != bench.hooks_text:
        problems.append("an unrecognized hooks.json was rewritten")
    if os.path.isfile(bench.script):
        problems.append("the hook script was installed with no hook pointing at it")
    return "; ".join(problems)


def run_hook(bench, mode, payload):
    """The installed script as Copilot runs it: from the plugin's own directory, the
    payload on stdin. Returns (stdout, the parsed context or None, problem)."""
    p = subprocess.run(["node", bench.script, mode], cwd=os.path.dirname(bench.hooks),
                       input=json.dumps(payload).encode("utf-8"), capture_output=True,
                       env=dict(os.environ, HOME=bench.home, USERPROFILE=bench.home))
    out = p.stdout.decode("utf-8", "replace").strip()
    if p.returncode != 0:
        return out, None, "%s exited %d: %s" % (mode, p.returncode, p.stderr[:200])
    if not out:
        return out, None, None
    try:
        parsed = json.loads(out)
    except ValueError:
        return out, None, "%s printed something Copilot discards (not JSON): %r" % (mode, out)
    if not isinstance(parsed, dict) or set(parsed) != {"additionalContext"}:
        return out, None, ("%s printed a form Copilot discards (not top-level "
                           "additionalContext): %r" % (mode, out))
    return out, parsed["additionalContext"], None


# What Copilot 1.0.100 hands a plugin's PostToolUse hook, as recorded 2026-10-20: the
# Claude payload, its powershell tool reported as Bash. Copilot's own hooks get
# toolArgs, a JSON string (GATE_RECIPES.md), which the script reads as well.
def tool_payload(bench, command):
    return {"hook_event_name": "PostToolUse", "cwd": bench.root, "tool_name": "Bash",
            "tool_input": {"command": command, "description": "a step"}}


def hook_answers(bench):
    """(problems, {name: context}) for the four payloads every hook case sends."""
    commit = "git commit -q -m 'a slice'"
    calls = {"session-start": ("session-start", {"hook_event_name": "SessionStart",
                                                 "cwd": bench.root, "source": "new"}),
             "commit": ("post-tool-use", tool_payload(bench, commit)),
             "commit (toolArgs a JSON string)": ("post-tool-use",
                                                 {"cwd": bench.root, "toolName":
                                                  "powershell", "toolArgs":
                                                  json.dumps({"command": commit})}),
             "status": ("post-tool-use", tool_payload(bench, "git status --short"))}
    problems, contexts = [], {}
    for name, (mode, payload) in calls.items():
        _, context, problem = run_hook(bench, mode, payload)
        if problem:
            problems.append(problem)
        contexts[name] = context
    return problems, contexts


def assert_hooks_speak(bench, out):
    """A stale graph with autoUpdate on: the session-start and commit hooks deliver the
    plugin's message, naming the prompt by absolute path; a non-commit says nothing."""
    problems, got = hook_answers(bench)
    prompt = os.path.join(os.path.dirname(bench.hooks), "auto-update-prompt.md")
    for name, phrase in (("session-start", "Knowledge graph is stale"),
                         ("commit", "Commit detected"),
                         ("commit (toolArgs a JSON string)", "Commit detected")):
        context = got[name] or ""
        if phrase not in context:
            problems.append("%s did not deliver %r: %r" % (name, phrase, context))
        elif prompt not in context:
            problems.append("%s does not name the prompt at %s: %r"
                            % (name, prompt, context))
    if got["status"]:
        problems.append("a non-commit command delivered a reminder")
    return "; ".join(problems)


def assert_hooks_silent(bench, out):
    """autoUpdate off: no hook says anything, whatever the graph's state."""
    problems, got = hook_answers(bench)
    problems += ["%s delivered %r" % (name, context)
                 for name, context in sorted(got.items()) if context]
    return "; ".join(problems)


def assert_hooks_commit_only(bench, out):
    """A graph at HEAD: no session-start reminder, but a commit - which moves HEAD past
    the graph - still gets one."""
    problems, got = hook_answers(bench)
    if got["session-start"]:
        problems.append("session-start reminded with the graph at HEAD")
    if "Commit detected" not in (got["commit"] or ""):
        problems.append("the commit reminder did not arrive with the graph at HEAD")
    return "; ".join(problems)


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

    ("coverage_complete_needs_no_rebuild", c_cov_complete,
     ["SDLC IMPACT: COMPLETE", "scope: coverage",
      "scanner: understand-anything 2.9.7 (Claude Code plugin cache)",
      "scanned-code-files: 6", "missing-code-files: 0", "missing-other-files: 0",
      "full-rebuild: not needed"], ["PARTIAL", "needed -"], None),

    ("coverage_missing_code_file_triggers_rebuild", c_cov_code_missing,
     ["SDLC IMPACT: PARTIAL", "scanned-code-files: 7", "missing-code-files: 1",
      "missing: " + CODE_NOT_IN_GRAPH, "full-rebuild: needed - /understand --full"],
     ["COMPLETE", "not needed"], None),

    ("coverage_missing_script_triggers_rebuild", c_cov_script_missing,
     ["SDLC IMPACT: PARTIAL", "missing-code-files: 1",
      "missing: " + SCRIPT_NOT_IN_GRAPH, "full-rebuild: needed"],
     ["COMPLETE", "not needed"], None),

    ("coverage_docs_and_config_never_trigger", c_cov_docs_never_trigger,
     # Named, so the owner sees them - but the rebuild stays off.
     ["SDLC IMPACT: COMPLETE", "missing-code-files: 0", "missing-other-files: 2",
      DOCS_NOT_IN_GRAPH, CONFIG_NOT_IN_GRAPH, "full-rebuild: not needed"],
     ["PARTIAL", "needed -"], None),

    ("coverage_newest_version_wins_numerically", c_cov_newest_version_wins,
     ["SDLC IMPACT: COMPLETE", "understand-anything 2.9.10 (Claude Code"],
     ["2.9.9", "cannot check"], None),

    ("coverage_newest_install_wins_across_homes", c_cov_newest_across_homes,
     ["SDLC IMPACT: COMPLETE", "understand-anything 2.9.7 (Copilot CLI plugins)"],
     ["2.9.4", "cannot check"], None),

    ("coverage_finds_the_copilot_home", c_cov_copilot_only,
     ["SDLC IMPACT: COMPLETE", "(Copilot CLI plugins)"], ["cannot check"], None),

    ("coverage_without_the_plugin_cannot_check", c_cov_no_plugin,
     ["SDLC IMPACT: UNAVAILABLE", "cannot check", "no Understand Anything scanner"],
     ["COMPLETE", "PARTIAL", "ERROR"], None),

    ("coverage_without_node_cannot_check", c_cov_no_node,
     ["SDLC IMPACT: UNAVAILABLE", "cannot check", "node is not on PATH"],
     ["COMPLETE", "PARTIAL", "ERROR"], None),

    ("coverage_scanner_failure_cannot_check", c_cov_scanner_fails,
     # Never an empty scan read as "nothing missing".
     ["SDLC IMPACT: UNAVAILABLE", "cannot check", "exited 3", "scan blew up"],
     ["COMPLETE", "PARTIAL", "ERROR"], None),

    ("coverage_unreadable_scan_cannot_check", c_cov_scanner_garbage,
     ["SDLC IMPACT: UNAVAILABLE", "cannot check", "unreadable"],
     ["COMPLETE", "PARTIAL", "ERROR"], None),

    ("coverage_without_a_graph_is_unavailable", c_cov_no_graph,
     ["SDLC IMPACT: UNAVAILABLE", "knowledge graph not found"],
     ["COMPLETE", "PARTIAL", "scanner:"], None),

    ("coverage_malformed_graph_is_error", c_cov_malformed_graph,
     ["SDLC IMPACT: ERROR", "malformed"], ["COMPLETE", "PARTIAL"], None),

    ("refresh_runs_when_the_graph_is_behind", c_rc_graph_behind,
     ["refresh needed", "run /understand"], ["skipped"], None),

    ("refresh_skipped_when_the_graph_is_at_head", c_rc_graph_at_head,
     ["refresh skipped", "already at HEAD", "would stop to ask"], ["needed"], None),

    ("refresh_skipped_without_a_build_commit", c_rc_no_meta,
     ["refresh skipped", "full analysis"], ["needed"], None),

    ("refresh_without_a_graph_has_nothing_to_do", c_rc_no_graph,
     ["no knowledge graph - nothing to refresh"], ["needed", "skipped"], None),

    ("plugin_fix_makes_the_hint_a_string", c_pf_fixes_copilot,
     ["argument-hint made a string in understand,", "Copilot CLI plugins",
      "next Copilot session", "auto-update hooks rewritten to run on Copilot"],
     ["understand-chat,", "nothing to fix", "left as they were"],
     assert_skills_fixed),

    ("plugin_fix_is_idempotent", c_pf_idempotent,
     ["nothing to fix (2 skills checked, hooks already fixed)"],
     ["made a string", "rewritten"], assert_skills_fixed),

    ("plugin_fix_never_writes_the_claude_install", c_pf_claude_untouched,
     ["made a string in understand,", "hooks rewritten"],
     ["Claude Code plugin cache"], assert_skills_fixed),

    ("plugin_fix_without_a_copilot_install", c_pf_no_install,
     ["no Understand Anything install in the Copilot CLI plugins home"],
     ["made a string", "rewritten"], None),

    ("plugin_fix_leaves_hooks_it_does_not_recognize", c_pf_unrecognized_hooks,
     ["hooks left as they were: no auto-update hook recognized"],
     ["hooks rewritten", "hooks already fixed"], assert_hooks_untouched),

    # The installed script, run the way Copilot runs it (FEATURE_PLAN §83.4).
    ("fixed_hooks_remind_on_a_stale_graph", c_pf_hooks_stale,
     ["hooks rewritten"], [], assert_hooks_speak),

    ("fixed_hooks_skip_session_start_at_head", c_pf_hooks_current,
     ["hooks rewritten"], [], assert_hooks_commit_only),

    ("fixed_hooks_obey_auto_update_off", c_pf_hooks_auto_update_off,
     ["hooks rewritten"], [], assert_hooks_silent),
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
    # coverage and refresh-check (§83)
    ("docs_trigger_a_full_rebuild",
     'TRIGGER_CATEGORIES = ("code", "script")',
     'TRIGGER_CATEGORIES = ("code", "script", "docs", "config")'),
    ("scripts_never_trigger",
     'TRIGGER_CATEGORIES = ("code", "script")',
     'TRIGGER_CATEGORIES = ("code",)'),
    ("missing_code_reported_complete",
     '    return emit("PARTIAL" if missing else "COMPLETE", "coverage", fields)',
     '    return emit("COMPLETE", "coverage", fields)'),
    ("versions_sorted_as_strings",
     '    found.sort(key=lambda entry: entry[0], reverse=True)',
     '    found.sort(key=lambda entry: entry[1], reverse=True)'),
    ("version_ignores_package_json",
     '                    version = json.loads(fh.read().decode("utf-8")).get("version") or version',
     '                    pass'),
    ("copilot_home_not_searched",
     '    ((".copilot", "installed-plugins", "*", "*"), "Copilot CLI plugins"),',
     ''),
    ("analysis_data_flag_dropped",
     '            p = subprocess.run([node, scanner, root, out, "--exclude-analysis-data"],',
     '            p = subprocess.run([node, scanner, root, out],'),
    ("failed_scan_read_as_empty",
     '        if p.returncode != 0 or not os.path.isfile(out):',
     '        if not os.path.isfile(out):\n            return [], None\n        if False:'),
    ("missing_node_not_detected",
     '    node = shutil.which("node")\n    if not node:',
     '    node = "node"\n    if not node:'),
    ("refresh_never_skipped_at_head",
     '    if commit == head:',
     '    if False:'),
    ("refresh_without_meta_runs_a_full_analysis",
     '    if not commit:\n        print("sdlc-impact: refresh skipped',
     '    if False:\n        print("sdlc-impact: refresh skipped'),
    # plugin-fix
    ("plugin_fix_reaches_past_the_frontmatter",
     '        if body.strip() == "---":\n            break',
     '        if False:\n            break'),
    ("plugin_fix_drops_the_line_ending",
     "                                                 lines[i][len(body):])",
     '                                                 "\\n")'),
    ("plugin_fix_writes_the_claude_install",
     "    parts, label = PLUGIN_HOMES[1]",
     "    parts, label = PLUGIN_HOMES[0]"),
    ("plugin_fix_never_writes",
     "                if changed:\n                    with open(path, \"wb\") as fh:",
     "                if changed:\n                    with open(os.devnull, \"wb\") as fh:"),
    # plugin-fix: the hooks half, and the script it installs
    ("hooks_rewrite_drops_the_crlf",
     "                fh.write(new_text.encode(\"utf-8\"))",
     "                fh.write(new_text.replace(\"\\r\\n\", \"\\n\").encode(\"utf-8\"))"),
    ("hooks_rewrite_never_writes",
     "        if new_text != text:\n            with open(path, \"wb\") as fh:",
     "        if False:\n            with open(path, \"wb\") as fh:"),
    ("hooks_rewrite_takes_any_command",
     "                elif marker in command:",
     "                elif command:"),
    ("hook_reads_the_plugin_directory",
     "  const project = payload.cwd || process.env.COPILOT_PROJECT_DIR || process.cwd();",
     "  const project = process.cwd();"),
    ("hook_prints_plain_text",
     "  process.stdout.write(JSON.stringify({ additionalContext: message }));",
     "  process.stdout.write(message);"),
    ("hook_prints_the_claude_form",
     "  process.stdout.write(JSON.stringify({ additionalContext: message }));",
     "  process.stdout.write(JSON.stringify({ hookSpecificOutput: { additionalContext:"
     " message } }));"),
    ("hook_ignores_auto_update",
     "?.autoUpdate !== true) return;",
     "?.autoUpdate === 'never') return;"),
    ("hook_ignores_tool_input",
     "  let args = payload.tool_input ?? payload.toolArgs;",
     "  let args = payload.toolArgs;"),
    ("hook_misses_string_tool_args",
     "  if (typeof args === 'string') {",
     "  if (false) {"),
    ("hook_reminds_at_head",
     "    if (!meta || meta.gitCommitHash === headOf(project)) return;",
     "    if (!meta) return;"),
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
