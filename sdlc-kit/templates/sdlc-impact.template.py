#!/usr/bin/env python
"""SDLC architecture-impact adapter — the Understand Anything read path.

Derives, mechanically, the architecture footprint of a slice or a phase: the git
change set, mapped onto an Understand Anything knowledge graph, one hop out through
its edges, written back as UA's own diff-overlay.json plus a compact printed summary
the daily commands quote.

WHAT THIS IS NOT. It is a comprehension aid for the owner and it is explicitly NOT
verification. Nothing it prints enters gate truth, no step passes or fails on it, and
it adds no owner halt. A green summary here says the picture was drawn, never that the
change is correct - so its output is phrased as a footprint, never as a check.

DETERMINISTIC BY CONSTRUCTION. The change set comes from git, the mapping from the
graph's own filePath/edge fields. No model decides what belongs in the picture; the
commands quote what this prints. Same tree plus same graph gives the same output.

FOUR STATES, and the distinction between the last two is the point:
  COMPLETE     every changed project file mapped to a graph node.
  PARTIAL      the footprint was computed, but something is missing and is NAMED -
               unmatched files, or a graph that may be stale. Counts are printed with
               their denominators so incompleteness is loud (spec 4.4, 12).
  UNAVAILABLE  the capability's environment is absent - no graph, no UA directory, a
               project that never adopted it. This is NOT failure: an optional
               capability that is not installed has nothing to report, and the SDLC
               continues untouched.
  ERROR        this adapter broke given a readable graph. Kit friction, worth
               reporting upstream.
A malformed graph is ERROR when it exists and cannot be parsed - never a silent
COMPLETE, and never UNAVAILABLE, which would read as "you do not have this feature"
when in fact you have a broken one.

This file takes no per-project values - the UA directory names are UA's, the output
grammar is fixed, and the state file lives under the resolved git dir - so it is
copied verbatim. It is launched shell-neutrally (`python <path>`), the same rationale
the settings template records for the guard launchers, and it is command-invoked
rather than hooked, so no per-CLI dialect exists.

Usage:
  python .github/hooks/sdlc-impact.py record-base            (at /next-slice)
  python .github/hooks/sdlc-impact.py slice                  (slice footprint)
  python .github/hooks/sdlc-impact.py phase <base-ref>       (arc footprint)
  python .github/hooks/sdlc-impact.py clear-base             (at /end-slice)
  python .github/hooks/sdlc-impact.py refresh-check          (at /end-slice, last)
  python .github/hooks/sdlc-impact.py coverage               (at /end-phase, last)
  python .github/hooks/sdlc-impact.py plugin-fix             (offered: Copilot CLI only)
"""

import glob
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

UA_DIRS = (".understand-anything", ".ua")  # legacy name first, current second
STATE_DIR = "sdlc-impact"
OVERLAY_NAME = "diff-overlay.json"
GRAPH_NAME = "knowledge-graph.json"
META_NAME = "meta.json"

# Where each CLI installs the Understand Anything plugin, relative to the home
# directory, as (glob, label). The scanner sits at the same place inside either install.
PLUGIN_HOMES = (
    ((".claude", "plugins", "cache", "understand-anything", "understand-anything", "*"),
     "Claude Code plugin cache"),
    ((".copilot", "installed-plugins", "*", "*"), "Copilot CLI plugins"),
)
SCANNER = ("skills", "understand", "scan-project.mjs")
# The categories whose absence from the graph calls for a full rebuild. The scanner
# also files every unrecognized extension under `code`, so this errs towards rebuilding.
TRIGGER_CATEGORIES = ("code", "script")
SCAN_TIMEOUT = 300
# A one-item YAML list as a skill's argument-hint - what Copilot CLI rejects (plugin-fix).
HINT_LIST = re.compile(r'^argument-hint:\s*\[\s*"((?:[^"\\]|\\.)*)"\s*\]\s*$')


def git(*args):
    """Run git and return (exit, stdout). Never raises: a git failure is a state to
    classify, not a crash - this adapter must never take down the step that quotes it."""
    try:
        p = subprocess.run(("git",) + args, capture_output=True)
    except OSError as exc:                       # git not on PATH at all
        return 127, "git unavailable: %s" % exc
    out = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n")
    return p.returncode, out.strip("\n")


def emit(state, scope, fields, reason=None):
    """The spec-15 output contract, printed last and printed once.

    Field order is fixed so the block diffs cleanly between runs - an owner comparing
    a slice preview against the final footprint is reading two of these side by side.
    """
    print("SDLC IMPACT: %s" % state)
    print("scope: %s" % scope)
    if reason:
        print("reason: %s" % reason)
    for key, value in fields:
        print("%s: %s" % (key, value))
    return 0


def resolve_ua_dir(root):
    """The UA directory, legacy name winning when both exist.

    Returns (path, name) or (None, None). Both names are checked because an early
    adopter carries the long one and UA renamed it; guessing one would report
    UNAVAILABLE to a project that has the feature.
    """
    for name in UA_DIRS:
        candidate = os.path.join(root, name)
        if os.path.isdir(candidate):
            return candidate, name
    return None, None


def is_ignored(root, rel):
    """True when git ignores this path. Used for two different jobs: excluding UA's
    own generated files from the change-set denominator, and deciding whether writing
    the overlay would dirty a tree the phase close requires to be clean."""
    code, _ = git("-C", root, "check-ignore", "-q", rel)
    return code == 0


def change_set(root, base, ua_name):
    """Every project file changed since `base`, from four sources the spec names.

    Committed since base, staged, unstaged, and untracked-but-not-ignored. A slice
    that committed mid-way is covered by the first; a slice mid-flight by the rest.
    UA's own generated files are excluded by path, mechanically, so the denominator
    is the project's own changed files and regenerating the overlay can never inflate
    the next run's count.
    """
    files = set()
    for args in (("diff", "--name-only", base, "--"),
                 ("diff", "--name-only", "--cached", "--"),
                 ("diff", "--name-only", "--")):
        code, out = git("-C", root, *args)
        if code == 0 and out:
            files.update(out.split("\n"))
    code, out = git("-C", root, "ls-files", "--others", "--exclude-standard")
    if code == 0 and out:
        files.update(out.split("\n"))
    prefix = ua_name + "/" if ua_name else None
    return sorted(
        f for f in files
        if f and not (prefix and (f == ua_name or f.startswith(prefix)))
    )


def load_graph(ua_path):
    """(graph, error). A graph that exists and will not parse is an error string, not
    an absence - the caller turns the two into different states on purpose."""
    path = os.path.join(ua_path, GRAPH_NAME)
    if not os.path.isfile(path):
        return None, None
    try:
        with open(path, "rb") as fh:
            return json.loads(fh.read().decode("utf-8")), None
    except ValueError as exc:
        return None, "graph JSON is malformed (%s)" % exc
    except OSError as exc:
        return None, "graph could not be read (%s)" % exc


def map_nodes(graph, changed):
    """Changed files -> (changed node ids, files that matched nothing).

    EVERY node carrying a changed file is included, not the file node alone: a file
    with a class and four functions contributes all six, which is what makes the
    one-hop expansion below reach the things that actually depend on the changed unit.
    """
    changed_set = set(changed)
    ids, matched = [], set()
    for node in graph.get("nodes", []):
        path = node.get("filePath")
        if path in changed_set:
            ids.append(node.get("id"))
            matched.add(path)
    return [i for i in ids if i], sorted(changed_set - matched)


def one_hop(graph, changed_ids):
    """Nodes one edge away from any changed node, deduplicated, with the changed set
    removed from the result.

    Both rules exist because the real graph breaks them: a file and the class it
    exports are joined by two edges at once (`contains` and `exports`), so a naive
    walk emits that neighbour twice; and both ends of such a pair are frequently
    changed together, so a naive walk lists a changed node as affected by itself.
    A node is either changed or affected - never both, never twice.
    """
    changed_set = set(changed_ids)
    affected = set()
    for edge in graph.get("edges", []):
        src, dst = edge.get("source"), edge.get("target")
        if src in changed_set and dst:
            affected.add(dst)
        if dst in changed_set and src:
            affected.add(src)
    return sorted(affected - changed_set)


def layers_for(graph, node_ids):
    """Layer names touched by these nodes, in the graph's own layer order.

    Absent when the graph carries no layer membership: reporting "changed-layers: none"
    for a graph that never had layers would read as a finding about the change.
    """
    wanted, names = set(node_ids), []
    for layer in graph.get("layers", []):
        if wanted.intersection(layer.get("nodeIds", [])):
            names.append(layer.get("name") or layer.get("id"))
    return names


def freshness(root, ua_path, base):
    """v1 freshness: had the tree already moved on from the graph BEFORE this work began?

    A graph built between the base and HEAD answers no: it is newer than the start of
    the work (the slice-end refresh, `spec/SDLC.md` *Architecture impact view*).

    The comparison is graph-commit against the BASE, never against the working tree.
    That distinction is the whole rule: this change set's own edits are unseen by the
    graph by definition - that is what the overlay exists to draw - so measuring
    against the working tree would report "may be stale" on virtually every slice and
    make COMPLETE unreachable. What matters is whether the graph already
    mis-described the tree the work started from.

    Deliberately simpler than the spec's monorepo-aware version, which needs a project
    path scope nothing in the contract supplies: here ANY project file changed between
    the graph commit and the base counts. No metadata means unknown, said plainly -
    never "current", which would be a claim the artifact does not support.
    """
    path = os.path.join(ua_path, META_NAME)
    if not os.path.isfile(path):
        return "unknown - no %s beside the graph" % META_NAME, False
    try:
        with open(path, "rb") as fh:
            meta = json.loads(fh.read().decode("utf-8"))
    except (ValueError, OSError) as exc:
        return "unknown - %s unreadable (%s)" % (META_NAME, exc), False
    commit = meta.get("gitCommitHash") or meta.get("commit")
    if not commit:
        return "unknown - no build commit recorded in %s" % META_NAME, False
    code, out = git("-C", root, "cat-file", "-e", commit + "^{commit}")
    if code != 0:
        return "unknown - graph commit %s not in this repository" % commit[:8], False
    code, out = git("-C", root, "diff", "--name-only", commit, base, "--")
    if code != 0:
        return "unknown - could not diff graph commit %s against the base" % commit[:8], False
    # The graph directory's own files are excluded here exactly as change_set() excludes
    # them: where that directory is tracked, a refresh commit touches only UA files, and
    # counting them would call the graph stale for having been refreshed.
    ua_name = os.path.basename(ua_path)
    since = [f for f in out.split("\n")
             if f and f != ua_name and not f.startswith(ua_name + "/")] if out else []
    if not since:
        return "current at the base (graph at %s)" % commit[:8], False
    # A graph built INSIDE this change set - after the base, on the line HEAD is on - is
    # newer than the tree the work started from, never older: the slice-end refresh puts
    # it there by design, and the phase view's base is where the arc branched. Both
    # ancestry tests are needed: a graph built on a sibling branch descends from the base
    # too, but describes a tree this branch never had.
    inside = (git("-C", root, "merge-base", "--is-ancestor", base, commit)[0] == 0
              and git("-C", root, "merge-base", "--is-ancestor", commit, "HEAD")[0] == 0)
    if inside:
        return ("current - graph at %s, built inside this change set after the base"
                % commit[:8]), False
    return ("may be stale - %d project files changed between graph commit %s and the base"
            % (len(since), commit[:8])), True


def write_overlay(root, ua_path, ua_name, base_branch, changed, changed_ids, affected):
    """Write UA's overlay, but only where the UA directory is git-ignored.

    The phase close requires a clean tree and re-asserts it as load-bearing before the
    merge. Writing into a tracked UA directory would dirty the tree at exactly those
    checked moments, so an un-ignored directory means the summary still prints and the
    overlay does not get written - stated, never silent. The owner can git-ignore the
    directory and get the picture; nobody gets a surprise dirty tree.
    """
    if not is_ignored(root, ua_name):
        return "not written - %s is not git-ignored" % ua_name
    payload = {
        "version": "1.0.0",
        "baseBranch": base_branch,
        "generatedAt": None,
        "changedFiles": changed,
        "changedNodeIds": changed_ids,
        "affectedNodeIds": affected,
    }
    code, out = git("-C", root, "log", "-1", "--format=%cI")
    payload["generatedAt"] = out if code == 0 and out else "unknown"
    target = os.path.join(ua_path, OVERLAY_NAME)
    try:
        with open(target, "wb") as fh:
            fh.write((json.dumps(payload, indent=2) + "\n").encode("utf-8"))
    except OSError as exc:
        return "not written - %s (%s)" % (OVERLAY_NAME, exc)
    # Forward slash deliberately, not os.path.join: this is a repo-relative path the
    # owner reads and the commands quote, and it must be byte-identical whichever
    # platform produced it. A backslash here would make two runs of the same tree
    # differ on Windows alone.
    return "%s/%s" % (ua_name, OVERLAY_NAME)


def state_path(root):
    code, out = git("-C", root, "rev-parse", "--git-dir")
    if code != 0:
        return None
    git_dir = out if os.path.isabs(out) else os.path.join(root, out)
    return os.path.join(git_dir, STATE_DIR, "slice-base")


def cmd_record_base(root):
    """Record branch + SHA as the slice base - only where a graph exists.

    Conditional on purpose: a project without Understand Anything gets exactly zero
    footprint from this feature, which is what "optional capability" has to mean. The
    honest cost is that a graph installed mid-slice waits one slice.
    The branch travels beside the SHA so a base recorded on a different branch is
    detectably stale rather than silently wrong, and the path comes from git rather
    than a literal .git/ so a worktree resolves correctly.
    """
    ua_path, _ = resolve_ua_dir(root)
    if not ua_path or not os.path.isfile(os.path.join(ua_path, GRAPH_NAME)):
        print("sdlc-impact: no knowledge graph - slice base not recorded")
        return 0
    path = state_path(root)
    if not path:
        print("sdlc-impact: could not resolve the git directory - slice base not recorded")
        return 0
    _, sha = git("-C", root, "rev-parse", "HEAD")
    _, branch = git("-C", root, "rev-parse", "--abbrev-ref", "HEAD")
    try:
        os.makedirs(os.path.dirname(path))
    except OSError:
        pass
    try:
        with open(path, "wb") as fh:
            fh.write(("%s %s\n" % (branch, sha)).encode("utf-8"))
    except OSError as exc:
        print("sdlc-impact: slice base not recorded (%s)" % exc)
        return 0
    print("sdlc-impact: slice base recorded - %s at %s" % (branch, sha[:8]))
    return 0


def cmd_clear_base(root):
    path = state_path(root)
    if path and os.path.isfile(path):
        try:
            os.remove(path)
        except OSError:
            pass
    print("sdlc-impact: slice base cleared")
    return 0


def read_base(root):
    """(base_sha, problem). A base recorded on another branch is refused rather than
    used: the spec requires the ambiguous-or-stale case to fail loudly, and a footprint
    computed from another branch's base is worse than no footprint - it looks right."""
    path = state_path(root)
    if not path or not os.path.isfile(path):
        return None, "no slice base recorded - run /next-slice on this slice first"
    try:
        with open(path, "rb") as fh:
            parts = fh.read().decode("utf-8").strip().split()
    except OSError as exc:
        return None, "slice base unreadable (%s)" % exc
    if len(parts) != 2:
        return None, "slice base is malformed"
    branch, sha = parts
    _, current = git("-C", root, "rev-parse", "--abbrev-ref", "HEAD")
    if current != branch:
        return None, ("slice base was recorded on '%s' but HEAD is on '%s'"
                      % (branch, current))
    return sha, None


def named(paths):
    """Up to ten paths, then a count - the members, not just the number."""
    return (", ".join(paths[:10])
            + (" (+%d more)" % (len(paths) - 10) if len(paths) > 10 else ""))


def version_key(text):
    """Numeric, so 2.9.10 sorts above 2.9.9; anything unparseable sorts lowest."""
    try:
        return tuple(int(part) for part in text.split("."))
    except ValueError:
        return ()


def find_scanner():
    """(scanner path, "understand-anything <version> (<home>)") or (None, None).

    Both CLIs' plugin homes are searched and the newest version wins, wherever it
    lives: a machine can carry an old project-scoped install beside a newer user-scoped
    one, and the scan should list what the newest analysis would. The version comes
    from the install's own package.json, else its directory name.
    """
    home = os.path.expanduser("~")
    found = []
    for parts, label in PLUGIN_HOMES:
        for plugin in sorted(glob.glob(os.path.join(home, *parts))):
            scanner = os.path.join(plugin, *SCANNER)
            if not os.path.isfile(scanner):
                continue
            version = os.path.basename(plugin)
            try:
                with open(os.path.join(plugin, "package.json"), "rb") as fh:
                    version = json.loads(fh.read().decode("utf-8")).get("version") or version
            except (ValueError, OSError, AttributeError):
                pass
            found.append((version_key(version), version, label, scanner))
    if not found:
        return None, None
    found.sort(key=lambda entry: entry[0], reverse=True)
    _, version, label, scanner = found[0]
    return scanner, "understand-anything %s (%s)" % (version, label)


def scan(root, scanner):
    """(files, problem). The plugin's own deterministic file list - no model, no tokens
    - written to a temporary file and read back. Every way the scan can fail is a
    reason the coverage cannot be checked, never an empty list: an empty list would
    read as "nothing is missing"."""
    node = shutil.which("node")
    if not node:
        return None, "node is not on PATH"
    tmp = tempfile.mkdtemp(prefix="sdlc-impact-scan-")
    out = os.path.join(tmp, "scan.json")
    try:
        try:
            p = subprocess.run([node, scanner, root, out, "--exclude-analysis-data"],
                               capture_output=True, timeout=SCAN_TIMEOUT)
        except subprocess.TimeoutExpired:
            return None, "the scanner ran past %d s" % SCAN_TIMEOUT
        except OSError as exc:
            return None, "the scanner could not start (%s)" % exc
        if p.returncode != 0 or not os.path.isfile(out):
            tail = p.stderr.decode("utf-8", "replace").strip()[-200:]
            return None, "the scanner exited %d%s" % (p.returncode,
                                                      (": " + tail) if tail else "")
        try:
            with open(out, "rb") as fh:
                files = json.loads(fh.read().decode("utf-8"))["files"]
            return [(f["path"], f.get("fileCategory")) for f in files], None
        except (ValueError, OSError, KeyError, TypeError, AttributeError) as exc:
            return None, "the scanner's output is unreadable (%s)" % exc
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def cmd_coverage(root):
    """Is every code and script file a full analysis would cover in the graph?

    The phase-end trigger for a full rebuild (`spec/SDLC.md`, *Architecture impact
    view*). An incremental analysis re-analyses changed files but cannot be trusted to
    add one its saved inventory never listed, so a graph can read current while whole
    files are absent. This compares the plugin's own scan with the graph's file nodes.
    It measures what is MISSING, not what was added this phase, so an earlier gap heals
    at the next full rebuild. Docs, config and the rest are named but never trigger
    one. "Cannot check" is UNAVAILABLE with the reason: it never blocks the step.
    """
    ua_path, ua_name = resolve_ua_dir(root)
    if not ua_path:
        return emit("UNAVAILABLE", "coverage", [],
                    reason="no Understand Anything directory (%s) in this project"
                           % " or ".join(UA_DIRS))
    graph, err = load_graph(ua_path)
    if err:
        return emit("ERROR", "coverage", [], reason=err)
    if graph is None:
        return emit("UNAVAILABLE", "coverage", [],
                    reason="Understand Anything knowledge graph not found in %s" % ua_name)
    scanner, label = find_scanner()
    if not scanner:
        return emit("UNAVAILABLE", "coverage", [],
                    reason="cannot check - no Understand Anything scanner in either "
                           "plugin home (~/.claude/plugins, ~/.copilot/installed-plugins)")
    files, problem = scan(root, scanner)
    if problem:
        return emit("UNAVAILABLE", "coverage", [("scanner", label)],
                    reason="cannot check - %s" % problem)
    graphed = {n.get("filePath") for n in graph.get("nodes", []) if n.get("filePath")}
    trigger = sorted(p for p, cat in files if cat in TRIGGER_CATEGORIES)
    missing = [p for p in trigger if p not in graphed]
    other = sorted(p for p, cat in files
                   if cat not in TRIGGER_CATEGORIES and p not in graphed)
    fields = [("scanner", label),
              ("scanned-code-files", len(trigger)),
              ("missing-code-files", len(missing))]
    if missing:
        fields.append(("missing", named(missing)))
    fields.append(("missing-other-files", len(other)))
    if other:
        fields.append(("missing-other", named(other)))
    fields.append(("full-rebuild", "needed - /understand --full" if missing
                   else "not needed"))
    return emit("PARTIAL" if missing else "COMPLETE", "coverage", fields)


def unlist_argument_hint(text):
    """(text, changed) with a one-item list `argument-hint: ["..."]` in the frontmatter
    made a plain string. The frontmatter is the block between the first two `---`
    lines; nothing after it is touched, and every line keeps its own ending."""
    lines = text.splitlines(True)
    if not lines or lines[0].strip() != "---":
        return text, False
    changed = False
    for i in range(1, len(lines)):
        body = lines[i].rstrip("\r\n")
        if body.strip() == "---":
            break
        match = HINT_LIST.match(body)
        if match:
            lines[i] = 'argument-hint: "%s"%s' % (match.group(1),
                                                 lines[i][len(body):])
            changed = True
    return "".join(lines), changed


def cmd_plugin_fix():
    """Make Understand Anything's skills loadable by Copilot CLI. Idempotent.

    Measured 2026-10-19 on CLI 1.0.100: the plugin's `understand` skill declares
    `argument-hint` as a YAML list, Copilot requires a string, and drops the skill -
    the agent sees "Skill not found" and the graph can never be refreshed from a
    Copilot session. Claude Code accepts the list, so only the Copilot install is
    rewritten. A plugin update restores the list, so this is re-run after one; it
    takes effect at the next session. It writes outside the repository, which is why
    the commands offer it rather than run it.
    """
    home = os.path.expanduser("~")
    parts, label = PLUGIN_HOMES[1]
    plugins = sorted(p for p in glob.glob(os.path.join(home, *parts))
                     if os.path.isfile(os.path.join(p, *SCANNER)))
    if not plugins:
        print("sdlc-impact: plugin-fix - no Understand Anything install in the %s home"
              % label)
        return 0
    for plugin in plugins:
        fixed, checked = [], 0
        for path in sorted(glob.glob(os.path.join(plugin, "skills", "*", "SKILL.md"))):
            checked += 1
            try:
                with open(path, "rb") as fh:
                    text = fh.read().decode("utf-8")
                new, changed = unlist_argument_hint(text)
                if changed:
                    with open(path, "wb") as fh:
                        fh.write(new.encode("utf-8"))
                    fixed.append(os.path.basename(os.path.dirname(path)))
            except (OSError, ValueError) as exc:
                print("sdlc-impact: plugin-fix - %s not fixed (%s)" % (path, exc))
        where = "%s (%s)" % (plugin, label)
        if fixed:
            print("sdlc-impact: plugin-fix - argument-hint made a string in %s, %s; "
                  "takes effect at the next Copilot session" % (", ".join(fixed), where))
        else:
            print("sdlc-impact: plugin-fix - nothing to fix (%d skills checked) in %s"
                  % (checked, where))
    return 0


def cmd_refresh_check(root):
    """Should the slice-end incremental refresh run? One line, read before it does.

    Understand Anything's `/understand` stops to ASK the user when the graph is already
    at HEAD, and an automated close-out must never stall on a prompt - so that state is
    "skip". A graph with no recorded build commit is also "skip": `/understand` would
    run a full analysis, which is the phase end's job, not a slice's.
    """
    ua_path, _ = resolve_ua_dir(root)
    if not ua_path or not os.path.isfile(os.path.join(ua_path, GRAPH_NAME)):
        print("sdlc-impact: no knowledge graph - nothing to refresh")
        return 0
    commit = None
    try:
        with open(os.path.join(ua_path, META_NAME), "rb") as fh:
            meta = json.loads(fh.read().decode("utf-8"))
        commit = meta.get("gitCommitHash") or meta.get("commit")
    except (ValueError, OSError, AttributeError):
        pass
    if not commit:
        print("sdlc-impact: refresh skipped - no build commit in %s, so /understand "
              "would run a full analysis rather than an incremental one" % META_NAME)
        return 0
    _, head = git("-C", root, "rev-parse", "HEAD")
    if commit == head:
        print("sdlc-impact: refresh skipped - the graph is already at HEAD (%s); "
              "/understand would stop to ask" % head[:8])
        return 0
    print("sdlc-impact: refresh needed - graph at %s, HEAD at %s: run /understand"
          % (commit[:8], head[:8]))
    return 0


def run(scope, root, base, base_branch):
    ua_path, ua_name = resolve_ua_dir(root)
    if not ua_path:
        return emit("UNAVAILABLE", scope, [],
                    reason="no Understand Anything directory (%s) in this project"
                           % " or ".join(UA_DIRS))
    graph, err = load_graph(ua_path)
    if err:
        return emit("ERROR", scope, [], reason=err)
    if graph is None:
        return emit("UNAVAILABLE", scope, [],
                    reason="Understand Anything knowledge graph not found in %s" % ua_name)

    changed = change_set(root, base, ua_name)
    changed_ids, unmatched = map_nodes(graph, changed)
    affected = one_hop(graph, changed_ids)
    layer_names = layers_for(graph, changed_ids + affected)
    fresh_text, stale = freshness(root, ua_path, base)
    overlay = write_overlay(root, ua_path, ua_name, base_branch,
                            changed, changed_ids, affected)

    fields = [
        ("changed-files", len(changed)),
        ("mapped-files", len(changed) - len(unmatched)),
        ("changed-nodes", len(changed_ids)),
        ("affected-nodes", len(affected)),
    ]
    if layer_names:
        fields.append(("changed-layers", ", ".join(layer_names)))
    fields.append(("unmatched-files", len(unmatched)))
    if unmatched:
        # Named, not just counted: "2 unmatched" tells the owner nothing actionable,
        # and the second field report's whole lesson is that a count without its
        # members is a denominator nobody can check.
        fields.append(("unmatched", named(unmatched)))
    fields.append(("graph-freshness", fresh_text))
    fields.append(("overlay", overlay))

    state = "COMPLETE" if not unmatched and not stale else "PARTIAL"
    return emit(state, scope, fields)


def main(argv):
    mode = argv[1] if len(argv) > 1 else ""
    code, root = git("rev-parse", "--show-toplevel")
    if code != 0:
        return emit("UNAVAILABLE", mode or "slice", [],
                    reason="not a git repository (or git is unavailable in this shell)")

    if mode == "record-base":
        return cmd_record_base(root)
    if mode == "clear-base":
        return cmd_clear_base(root)
    if mode == "refresh-check":
        return cmd_refresh_check(root)
    if mode == "plugin-fix":
        return cmd_plugin_fix()
    if mode == "coverage":
        return cmd_coverage(root)
    if mode == "slice":
        # The graph is checked first on purpose: a project that never adopted
        # Understand Anything must be told THAT, not told to run /next-slice - which
        # would not record a base either, since record-base is conditional on a graph.
        # The commonest UNAVAILABLE deserves the actionable reason.
        ua_path, ua_name = resolve_ua_dir(root)
        if not ua_path or not os.path.isfile(os.path.join(ua_path, GRAPH_NAME)):
            return run("slice", root, None, None)
        base, problem = read_base(root)
        if problem:
            return emit("UNAVAILABLE", "slice", [], reason=problem)
        _, branch = git("-C", root, "rev-parse", "--abbrev-ref", "HEAD")
        return run("slice", root, base, branch)
    if mode == "phase":
        if len(argv) < 3 or not argv[2]:
            return emit("ERROR", "phase", [],
                        reason="phase mode needs the base ref the project's own records name")
        base_ref = argv[2]
        code, base = git("-C", root, "rev-parse", "--verify", "--quiet",
                         base_ref + "^{commit}")
        if code != 0:
            return emit("UNAVAILABLE", "phase", [],
                        reason="base ref '%s' does not resolve in this repository" % base_ref)
        return run("phase", root, base, base_ref)

    return emit("ERROR", "unknown", [],
                reason="unknown mode '%s' (usage: record-base | slice | "
                       "phase <base-ref> | clear-base | refresh-check | coverage | "
                       "plugin-fix)" % mode)


def guarded(argv):
    """Any unexpected exception becomes ERROR, never a traceback.

    This adapter is quoted by a step, and a comprehension aid that takes down the step
    quoting it has cost more than it returns. ERROR is exactly the state reserved for
    "the adapter broke given a readable graph" - so an unhandled fault is reported in
    the same grammar as everything else, with the exception named so the friction is
    reportable upstream rather than mysterious. A traceback on stderr and a non-zero
    exit would be indistinguishable, to the step, from the tool being broken beyond
    use. This existed as a docstring promise and not as code until the proof crashed
    the adapter and the harness saw exit 1 with empty output.
    """
    try:
        return main(argv)
    except Exception as exc:                     # deliberately broad: see above
        return emit("ERROR", "unknown", [],
                    reason="the adapter raised %s: %s"
                           % (type(exc).__name__, exc))


if __name__ == "__main__":
    sys.exit(guarded(sys.argv))
