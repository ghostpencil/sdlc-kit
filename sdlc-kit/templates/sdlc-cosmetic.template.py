#!/usr/bin/env python
"""SDLC cosmetic-edit classifier - tells a comment or formatting edit from a code change.

The TDD guard asks one question of it: is this write to a production source file a
comment or layout change only? If so the guard lets it through without the red-first
ceremony or a refactor licence, and logs it (`OK production write (cosmetic: ...)`).
`/end-slice` asks the same question of each source file in a docs-only slice.

THE INVARIANT EVERYTHING HERE KEEPS: this file can only GRANT an exemption. A missing
toolchain, a parse error, a failed or ambiguous match, a timeout, an unknown
extension, a comparator that breaks - each answers "cannot tell", which every caller
reads as "real change", so today's rule applies and the reason is logged. The worst
case is today's friction, never a write let through that should not be. It never runs
the test suite and never writes to the working tree.

TWO CHECKS, BOTH MUST PASS:
  1. The syntax trees match, with positions and comments ignored - per language:
       .py                    in-process `ast`, type_comments=True (`# type: ignore`
                              is a node there, so it counts)
       .ts .tsx .mts .cts     node + the project's own `typescript`, resolved upward
       .js .jsx .mjs .cjs     from the edited file, then from the root; no typescript,
                              no exemption
       .java                  the JDK's compiler API (javac parse only, no classpath)
       .cs                    the .NET SDK's Roslyn, plus every preprocessor directive
                              and inactive `#if` block compared verbatim - Roslyn
                              treats those as trivia, so an edit inside `#if DEBUG`
                              would otherwise compare equal
     A docstring is a string literal in the tree, so a docstring edit is REAL here.
  2. The directive lines match. Some comments steer a tool - `# noqa`,
     `// @ts-expect-error`, `#pragma warning disable` - and read as comments to every
     parser. Each language has a list (owner-approved, FEATURE_PLAN.md 82.9 ruling 5);
     a line matching it, case- and whitespace-insensitively, must appear in the same
     order with the same nearest code line above and below it before and after the
     edit. Moving a directive moves what it governs, so a move is real too.

The TS, Java and C# comparators are embedded below as source text. Java and C# compile
once into the git directory - `<git-dir>/sdlc-tdd/cosmetic/<lang>-<key>/`, keyed by
the toolchain and the comparator source, built under a temporary name and renamed -
never into the working tree. A cache entry that breaks is deleted and rebuilt on the
next call. Every subprocess has a timeout, and the two together stay inside the hook
configs' own 30 s: a hook that times out FAILS OPEN on Copilot, which would wave the
write through regardless of what this file would have said.

This file takes no per-project values, so it is copied verbatim, and both CLIs use
the same copy - the sdlc-close-out.sh pattern.

Usage:
  imported by path      check_write(root, path, tool, args, cache) / classify(...)
                        -> (code, detail); the Claude Code guard, which costs no process
  python .github/hooks/sdlc-cosmetic.py <before> <after> [--as <path>]
                        compare two files; --as names the file the pair stands for
                        (its extension picks the language, its directory resolves
                        typescript) and defaults to <after>
  python .github/hooks/sdlc-cosmetic.py write [<file>]  < hook payload
                        rebuild the post-edit file from an Edit/Write (Claude Code)
                        or edit/create (Copilot) payload and compare; <file> is the
                        target as the caller resolved it, else the payload's path
  Exit / code: 0 cosmetic, 1 real, 2 cannot tell. The detail line goes to stdout.
"""
import ast
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import warnings
from bisect import bisect_left

COSMETIC, REAL, CANNOT = 0, 1, 2

# Together they stay inside the 30 s the hook configs allow, with room for the guard
# itself. Measured: javac builds the comparator in ~2 s and csc in ~1 s, a compare
# costs 0.2-0.7 s; the margin is for a loaded machine, where a compare has been seen
# past 5 s.
COMPILE_TIMEOUT = 12
COMPARE_TIMEOUT = 8

LANG = {
    ".py": "python",
    ".ts": "typescript", ".tsx": "typescript", ".mts": "typescript", ".cts": "typescript",
    ".js": "typescript", ".jsx": "typescript", ".mjs": "typescript", ".cjs": "typescript",
    ".java": "java",
    ".cs": "csharp",
}

# Matched case-insensitively against each line with all whitespace removed from both
# sides, so `#noqa` and `# noqa` are one directive. The lists are owner-approved
# (FEATURE_PLAN.md 82.9 ruling 5); C# also counts every preprocessor line except the
# #region pair, and Python a line-1 shebang and a coding line on lines 1-2.
DIRECTIVES = {
    "python": ("# noqa", "# ruff:", "# type:", "# pyright:", "# mypy:", "# pylint:",
               "# pragma:", "# nosec", "# fmt:", "# isort:"),
    "java": ("//noinspection", "NOPMD", "CHECKSTYLE:OFF", "CHECKSTYLE:ON",
             "CHECKSTYLE.OFF", "NOSONAR", "@formatter:off", "@formatter:on",
             "spotless:off", "spotless:on", "$NON-NLS-", "fallthru", "fall through",
             "falls through"),
    "csharp": ("ReSharper disable", "ReSharper restore", "<auto-generated", "NOSONAR"),
    "typescript": ("@ts-ignore", "@ts-expect-error", "@ts-nocheck", "@ts-check",
                   "/// <reference", "/// <amd-module", "@jsx", "@jsxImportSource",
                   "@jsxFrag", "@jsxRuntime", "eslint-disable", "eslint-enable",
                   "/* eslint ", "/* global", "prettier-ignore", "biome-ignore",
                   "istanbul ignore", "c8 ignore", "v8 ignore", "webpackChunkName",
                   "webpackIgnore", "@vite-ignore", "__PURE__"),
}
_WS = re.compile(r"\s+")
_SQUASHED = {k: tuple(_WS.sub("", p).lower() for p in v) for k, v in DIRECTIVES.items()}


def _is_directive(i, line, lang):
    s = _WS.sub("", line).lower()
    if lang == "python":
        if i == 0 and s.startswith("#!"):
            return True
        if i < 2 and s.startswith("#") and ("coding:" in s or "coding=" in s):
            return True
    if lang == "csharp" and s.startswith("#") and not s.startswith(("#region",
                                                                   "#endregion")):
        return True
    return any(p in s for p in _SQUASHED[lang])


def _comment_only(line, lang):
    if lang == "python":
        return line.startswith("#")
    return line.startswith(("//", "/*", "*"))


def _directive_view(text, lang):
    """Each directive line with the nearest code line above and below it, in order."""
    lines = [l.strip() for l in text.splitlines()]
    hits = [i for i, l in enumerate(lines) if l and _is_directive(i, l, lang)]
    if not hits:
        return []
    hit = set(hits)
    code = [i for i, l in enumerate(lines)
            if l and i not in hit and not _comment_only(l, lang)]
    view = []
    for i in hits:
        k = bisect_left(code, i)
        view.append((lines[i], lines[code[k - 1]] if k else "",
                     lines[code[k]] if k < len(code) else ""))
    return view


# --- Python, in-process -------------------------------------------------------------

def _python(before, after):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            a = ast.dump(ast.parse(before, type_comments=True))
            b = ast.dump(ast.parse(after, type_comments=True))
    except (SyntaxError, ValueError) as e:
        return CANNOT, "python could not parse the file (%s)" % e.__class__.__name__
    if a == b:
        return COSMETIC, "python-ast"
    return REAL, "python-ast: the syntax tree differs"


# --- The embedded comparators ---------------------------------------------------------
# Each takes <before> <after> and exits 10 equal, 11 different, 12 parse error, 13 the
# toolchain cannot run it (stdout says why). Distinct codes on purpose: a runtime that
# dies on its own exits 1, and 1 must never read as a verdict.

TS_SRC = r'''
const fs = require("fs"), path = require("path");
const [a, b, name, ...from] = process.argv.slice(1);
let ts;
try { ts = require(require.resolve("typescript", {paths: from})); }
catch (e) { process.stdout.write("typescript did not resolve from the edited file or the root"); process.exit(13); }
const ext = path.extname(name).toLowerCase();
const kind = ext === ".tsx" ? ts.ScriptKind.TSX : ext === ".jsx" ? ts.ScriptKind.JSX
  : [".js", ".mjs", ".cjs"].includes(ext) ? ts.ScriptKind.JS : ts.ScriptKind.TS;
// Positions, caches, block layout and quote style are not the program; every other
// primitive field is - an operator, let/const, @deprecated, a heritage keyword.
const SKIP = new Set(["pos", "end", "id", "modifierFlagsCache", "transformFlags",
                      "multiLine", "singleQuote"]);
function sig(file) {
  const sf = ts.createSourceFile(name, fs.readFileSync(file, "utf8"),
                                 ts.ScriptTarget.Latest, false, kind);
  if (!Array.isArray(sf.parseDiagnostics) || sf.parseDiagnostics.length) return null;
  const out = [];
  (function walk(n) {
    out.push(n.kind);
    if (n.kind !== ts.SyntaxKind.SourceFile)
      for (const k of Object.keys(n).sort()) {
        const v = n[k];
        if (!SKIP.has(k) && ["string", "number", "boolean", "bigint"].includes(typeof v))
          out.push(k + "=" + JSON.stringify(String(v)));
      }
    out.push("(");
    ts.forEachChild(n, walk);
    out.push(")");
  })(sf);
  return out.join(" ");
}
process.stdout.write(String(ts.version));
const x = sig(a), y = sig(b);
process.exit(x === null || y === null ? 12 : x === y ? 10 : 11);
'''

JAVA_SRC = r'''
import com.sun.source.tree.*;
import com.sun.source.util.*;
import javax.tools.*;
import java.lang.reflect.Method;
import java.lang.reflect.Modifier;
import java.net.URI;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class SdlcJavaCmp {
  static final Map<Class<?>, List<Method>> PROPS = new HashMap<>();

  // Every no-argument getter of the public tree interfaces that returns a value rather
  // than a subtree: a name, an operator kind, a literal, modifier flags, a break label,
  // case -> versus case :. Subtrees are walked by the scanner itself.
  static List<Method> props(Class<?> c) {
    return PROPS.computeIfAbsent(c, k -> {
      Map<String, Method> found = new TreeMap<>();
      Deque<Class<?>> todo = new ArrayDeque<>();
      for (Class<?> s = k; s != null; s = s.getSuperclass())
        todo.addAll(Arrays.asList(s.getInterfaces()));
      while (!todo.isEmpty()) {
        Class<?> i = todo.pop();
        todo.addAll(Arrays.asList(i.getInterfaces()));
        if (!i.getPackageName().equals("com.sun.source.tree")) continue;
        for (Method m : i.getMethods()) {
          Class<?> r = m.getReturnType();
          if (m.getParameterCount() != 0 || Modifier.isStatic(m.getModifiers())
              || r == void.class || Tree.class.isAssignableFrom(r)
              || List.class.isAssignableFrom(r) || r == JavaFileObject.class
              || r == LineMap.class) continue;
          found.putIfAbsent(m.getName(), m);
        }
      }
      return new ArrayList<>(found.values());
    });
  }

  static String sig(Path p) throws Exception {
    String src = new String(Files.readAllBytes(p), StandardCharsets.UTF_8);
    JavaCompiler jc = ToolProvider.getSystemJavaCompiler();
    DiagnosticCollector<JavaFileObject> diags = new DiagnosticCollector<>();
    JavaFileObject fo = new SimpleJavaFileObject(URI.create("string:///Cmp.java"),
                                                 JavaFileObject.Kind.SOURCE) {
      @Override public CharSequence getCharContent(boolean b) { return src; }
    };
    JavacTask task = (JavacTask) jc.getTask(null, null, diags, List.of("-proc:none"),
                                            null, List.of(fo));
    Iterable<? extends CompilationUnitTree> units = task.parse();
    for (Diagnostic<?> d : diags.getDiagnostics())
      if (d.getKind() == Diagnostic.Kind.ERROR) return null;
    StringBuilder sb = new StringBuilder();
    TreeScanner<Void, Void> scanner = new TreeScanner<Void, Void>() {
      @Override public Void scan(Tree t, Void v) {
        if (t == null) { sb.append('_'); return null; }
        sb.append('(');
        for (Method m : props(t.getClass())) {
          Object o;
          try { o = m.invoke(t); } catch (Exception e) { o = "?"; }
          sb.append(m.getName()).append('=').append(String.valueOf(o)).append(';');
        }
        super.scan(t, v);
        sb.append(')');
        return null;
      }
    };
    for (CompilationUnitTree u : units) scanner.scan(u, null);
    return sb.toString();
  }

  public static void main(String[] a) {
    try {
      String x = sig(Path.of(a[0])), y = sig(Path.of(a[1]));
      System.exit(x == null || y == null ? 12 : x.equals(y) ? 10 : 11);
    } catch (Throwable e) {
      System.out.print("java comparator failed: " + e);
      System.exit(13);
    }
  }
}
'''

CS_SRC = r'''
using System;
using System.IO;
using System.Linq;
using System.Text;
using Microsoft.CodeAnalysis;
using Microsoft.CodeAnalysis.CSharp;

static class SdlcCsCmp {
  // IsEquivalentTo ignores trivia, and to Roslyn a preprocessor directive and the body
  // of an inactive #if are trivia - so both are compared here, line by line, trimmed.
  // #region and #endregion are layout (FEATURE_PLAN.md 82.9 ruling 5).
  static string Trivia(SyntaxTree t) {
    var sb = new StringBuilder();
    foreach (var tr in t.GetRoot().DescendantTrivia(descendIntoTrivia: true)) {
      var k = tr.Kind();
      if (k == SyntaxKind.RegionDirectiveTrivia || k == SyntaxKind.EndRegionDirectiveTrivia) continue;
      if (!tr.IsDirective && k != SyntaxKind.DisabledTextTrivia) continue;
      foreach (var line in tr.ToFullString().Replace("\r", "").Split('\n')) {
        var s = line.Trim();
        if (s.Length > 0) sb.Append(s).Append('\n');
      }
      sb.Append('\u0001');
    }
    return sb.ToString();
  }

  static int Main(string[] a) {
    try {
      var t1 = CSharpSyntaxTree.ParseText(File.ReadAllText(a[0]));
      var t2 = CSharpSyntaxTree.ParseText(File.ReadAllText(a[1]));
      if (t1.GetDiagnostics().Concat(t2.GetDiagnostics())
            .Any(d => d.Severity == DiagnosticSeverity.Error)) return 12;
      if (!t1.IsEquivalentTo(t2, topLevel: false)) return 11;
      return Trivia(t1) == Trivia(t2) ? 10 : 11;
    } catch (Exception e) {
      Console.Write("csharp comparator failed: " + e.GetType().Name);
      return 13;
    }
  }
}
'''


def _exe(d, name):
    for n in (name + ".exe", name):
        p = os.path.join(d, n)
        if os.path.isfile(p):
            return p
    return None


def _key(*parts):
    h = hashlib.sha256()
    for p in parts:
        h.update(p.encode("utf-8", "replace"))
        h.update(b"\0")
    return h.hexdigest()[:16]


def _stamp(path):
    try:
        st = os.stat(path)
        return "%s|%d|%d" % (os.path.realpath(path), st.st_size, int(st.st_mtime))
    except OSError:
        return path


def _run(cmd, timeout):
    """-> (returncode, stdout) or (None, reason)."""
    try:
        p = subprocess.run(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                           stderr=subprocess.DEVNULL, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "timed out after %ss" % timeout
    except OSError as e:
        return None, "could not start (%s)" % e.__class__.__name__
    return p.returncode, p.stdout.decode("utf-8", "replace").strip()


def _cached(cache, name, build):
    """The compiled comparator directory, building it on a miss. -> (dir, None) or
    (None, reason). An entry without its `ok` marker is a half-written or broken one."""
    final = os.path.join(cache, name)
    if os.path.isfile(os.path.join(final, "ok")):
        return final, None
    shutil.rmtree(final, ignore_errors=True)
    tmp = "%s.tmp-%d" % (final, os.getpid())
    try:
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        why = build(tmp)
        if why:
            return None, why
        io.open(os.path.join(tmp, "ok"), "w").close()
        try:
            os.rename(tmp, final)
        except OSError:
            # Another guard process built it first - use theirs.
            if not os.path.isfile(os.path.join(final, "ok")):
                return None, "could not place the compiled comparator in the cache"
        return final, None
    except OSError as e:
        return None, "could not build in the cache (%s)" % e.__class__.__name__
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _verdict(rc, out, label, drop=None):
    if rc == 10:
        return COSMETIC, label
    if rc == 11:
        return REAL, "%s: the syntax tree differs" % label
    if rc == 12:
        return CANNOT, "%s could not parse the file" % label
    if rc == 13:
        return CANNOT, out or "%s cannot run here" % label
    if rc is None:
        return CANNOT, "%s %s" % (label, out)
    # Anything else is the comparator or its runtime breaking - a corrupt cache entry,
    # a runtime the class files do not fit. Drop the entry so the next call rebuilds.
    # (A timeout is not breakage: a slow machine keeps its build.)
    if drop:
        shutil.rmtree(drop, ignore_errors=True)
    return CANNOT, "%s broke (exit %s)" % (label, rc)


def _typescript(a, b, path, root):
    node = shutil.which("node")
    if not node:
        return CANNOT, "node is not on PATH"
    full = os.path.abspath(path)
    rc, out = _run([node, "-e", TS_SRC, a, b, full, os.path.dirname(full),
                    root or os.path.dirname(full)], COMPARE_TIMEOUT)
    return _verdict(rc, out, "typescript %s" % out if rc in (10, 11, 12) else "typescript")


def _jdk():
    """(javac, java, version) from JAVA_HOME, else from the javac on PATH. The java
    beside javac, never the java on PATH: on a machine with a JRE ahead of the JDK
    (measured here, 2026-10-19: Java 8 first on PATH, javac 20) PATH's java cannot run
    what javac compiled."""
    dirs = []
    if os.environ.get("JAVA_HOME"):
        dirs.append(os.path.join(os.environ["JAVA_HOME"], "bin"))
    w = shutil.which("javac")
    if w:
        dirs.append(os.path.dirname(os.path.realpath(w)))
    for d in dirs:
        javac, java = _exe(d, "javac"), _exe(d, "java")
        if javac and java:
            ver = ""
            try:
                with io.open(os.path.join(os.path.dirname(d), "release"),
                             encoding="utf-8", errors="replace") as f:
                    m = re.search(r'JAVA_VERSION="([^"]+)"', f.read())
                    ver = m.group(1) if m else ""
            except OSError:
                pass
            return javac, java, ver
    return None


def _java(a, b, cache):
    jdk = _jdk()
    if not jdk:
        return CANNOT, "no JDK found (JAVA_HOME, or javac on PATH)"
    javac, java, ver = jdk
    label = "javac %s" % ver if ver else "javac"

    def build(d):
        src = os.path.join(d, "SdlcJavaCmp.java")
        io.open(src, "w", encoding="utf-8", newline="\n").write(JAVA_SRC)
        rc, out = _run([javac, "-nowarn", "-d", d, src], COMPILE_TIMEOUT)
        if rc != 0 or not os.path.isfile(os.path.join(d, "SdlcJavaCmp.class")):
            return "javac could not build the comparator (%s)" % (out or "exit %s" % rc)
        return None

    d, why = _cached(cache, "java-" + _key(_stamp(javac), _stamp(java), JAVA_SRC), build)
    if not d:
        return CANNOT, why
    rc, out = _run([java, "-XX:TieredStopAtLevel=1", "-cp", d, "SdlcJavaCmp", a, b],
                   COMPARE_TIMEOUT)
    return _verdict(rc, out, label, drop=d)


def _vtuple(v):
    return tuple(int(x) if x.isdigit() else 0 for x in re.split(r"[.-]", v)[:3])


def _dotnet():
    """(dotnet, csc.dll, sdk version, reference assemblies, runtime major) or None."""
    w = shutil.which("dotnet")
    if not w:
        return None
    home = os.path.dirname(os.path.realpath(w))
    try:
        sdks = sorted((v for v in os.listdir(os.path.join(home, "sdk"))
                       if os.path.isfile(os.path.join(home, "sdk", v, "Roslyn", "bincore",
                                                      "csc.dll"))),
                      key=_vtuple, reverse=True)
    except OSError:
        return None
    for sdk in sdks:
        major = sdk.split(".")[0]
        packs = os.path.join(home, "packs", "Microsoft.NETCore.App.Ref")
        try:
            refs = sorted((v for v in os.listdir(packs) if v.split(".")[0] == major),
                          key=_vtuple, reverse=True)
        except OSError:
            refs = []
        for r in refs:
            rd = os.path.join(packs, r, "ref", "net%s.0" % major)
            if os.path.isdir(rd):
                dlls = sorted(os.path.join(rd, f) for f in os.listdir(rd)
                              if f.endswith(".dll"))
                return (w, os.path.join(home, "sdk", sdk, "Roslyn", "bincore", "csc.dll"),
                        sdk, dlls, major)
    return None


def _csharp(a, b, cache):
    net = _dotnet()
    if not net:
        return CANNOT, "no .NET SDK with Roslyn and reference assemblies found"
    dotnet, csc, sdk, refs, major = net
    bincore = os.path.dirname(csc)
    roslyn = [os.path.join(bincore, n) for n in ("Microsoft.CodeAnalysis.dll",
                                                 "Microsoft.CodeAnalysis.CSharp.dll")]
    config = ('{"runtimeOptions":{"tfm":"net%s.0","framework":{"name":'
              '"Microsoft.NETCore.App","version":"%s.0.0"}}}' % (major, major))

    def build(d):
        src = os.path.join(d, "SdlcCsCmp.cs")
        io.open(src, "w", encoding="utf-8", newline="\n").write(CS_SRC)
        rsp = os.path.join(d, "build.rsp")
        io.open(rsp, "w", encoding="utf-8").write("\n".join(
            ["-nologo", "-nowarn:CS1701,CS1702", '-out:"%s"' % os.path.join(d, "SdlcCsCmp.dll")]
            + ['-r:"%s"' % r for r in refs + roslyn] + ['"%s"' % src]) + "\n")
        rc, out = _run([dotnet, csc, "@" + rsp], COMPILE_TIMEOUT)
        if rc != 0 or not os.path.isfile(os.path.join(d, "SdlcCsCmp.dll")):
            return "csc could not build the comparator (%s)" % (out[-300:] or "exit %s" % rc)
        for r in roslyn:
            shutil.copy2(r, d)
        io.open(os.path.join(d, "SdlcCsCmp.runtimeconfig.json"), "w").write(config)
        return None

    d, why = _cached(cache, "csharp-" + _key(_stamp(csc), sdk, config, CS_SRC), build)
    if not d:
        return CANNOT, why
    rc, out = _run([dotnet, os.path.join(d, "SdlcCsCmp.dll"), a, b], COMPARE_TIMEOUT)
    return _verdict(rc, out, "roslyn %s" % sdk, drop=d)


# --- The entry points -----------------------------------------------------------------

def git_dir(root):
    """The git directory: .git itself, or what a linked worktree's .git file names."""
    p = os.path.join(root, ".git")
    if os.path.isdir(p):
        return p
    try:
        with io.open(p, encoding="utf-8") as f:
            line = f.read().strip()
    except OSError:
        return None
    if not line.startswith("gitdir:"):
        return None
    g = line[len("gitdir:"):].strip()
    if not os.path.isabs(g):
        g = os.path.join(root, g)
    return g if os.path.isdir(g) else None


def default_cache(start):
    """<git-dir>/sdlc-tdd/cosmetic for the repository holding `start`; the system temp
    directory if there is none - never the working tree."""
    d = os.path.abspath(start)
    while True:
        g = git_dir(d)
        if g:
            return os.path.join(g, "sdlc-tdd", "cosmetic")
        up = os.path.dirname(d)
        if up == d:
            return os.path.join(tempfile.gettempdir(), "sdlc-cosmetic")
        d = up


def classify(path, before, after, cache=None, root=None):
    """Compare two versions of the source file `path`. -> (code, detail)."""
    try:
        lang = LANG.get(os.path.splitext(path)[1].lower())
        if not lang:
            return CANNOT, "no classifier for %s files" % (os.path.splitext(path)[1] or
                                                           "extensionless")
        if before == after:
            return COSMETIC, "identical"
        if _directive_view(before, lang) != _directive_view(after, lang):
            return REAL, "a directive comment was added, removed, changed or moved"
        if lang == "python":
            return _python(before, after)
        cache = cache or default_cache(root or os.path.dirname(os.path.abspath(path)))
        work = tempfile.mkdtemp(prefix="sdlc-cosmetic-")
        try:
            name = os.path.basename(path)
            a = os.path.join(work, "before", name)
            b = os.path.join(work, "after", name)
            for f, text in ((a, before), (b, after)):
                os.makedirs(os.path.dirname(f))
                io.open(f, "w", encoding="utf-8", newline="").write(text)
            if lang == "typescript":
                return _typescript(a, b, path, root)
            os.makedirs(cache, exist_ok=True)
            return (_java if lang == "java" else _csharp)(a, b, cache)
        finally:
            shutil.rmtree(work, ignore_errors=True)
    except Exception as e:
        return CANNOT, "classifier error (%s)" % e.__class__.__name__


def rebuild(before, tool, args):
    """The file as the write would leave it. -> (text, None) or (None, reason). Requires
    exactly the match the tool itself requires; anything else is "cannot tell"."""
    if not isinstance(args, dict):
        return None, "no tool arguments in the payload"
    if tool in ("Write", "create"):
        key = "content" if tool == "Write" else "file_text"
        text = args.get(key)
        return (text, None) if isinstance(text, str) else (None, "no %s in the payload" % key)
    if tool in ("Edit", "edit"):
        old = args.get("old_string" if tool == "Edit" else "old_str")
        new = args.get("new_string" if tool == "Edit" else "new_str")
        if not isinstance(old, str) or not isinstance(new, str) or not old:
            return None, "no old/new text in the payload"
        n = before.count(old)
        if tool == "Edit" and args.get("replace_all") is True:
            if n == 0:
                return None, "the old text is not in the file"
            return before.replace(old, new), None
        if n != 1:
            return None, "the old text matches %d times, the tool requires exactly one" % n
        return before.replace(old, new, 1), None
    return None, "no rebuild for the %s tool" % (tool or "unnamed")


def check_write(root, path, tool, args, cache=None):
    """Classify one write as the guard sees it. -> (code, detail)."""
    try:
        full = path if os.path.isabs(path) else os.path.join(root, path)
        try:
            with io.open(full, "rb") as f:
                before = f.read().decode("utf-8-sig")
        except FileNotFoundError:
            return REAL, "a new file - nothing to compare against"
        except (OSError, UnicodeDecodeError) as e:
            return CANNOT, "could not read the file (%s)" % e.__class__.__name__
        after, why = rebuild(before, tool, args)
        if after is None:
            return CANNOT, why
        return classify(full, before, after, cache, root)
    except Exception as e:
        return CANNOT, "classifier error (%s)" % e.__class__.__name__


def _read(p):
    with io.open(p, "rb") as f:
        return f.read().decode("utf-8-sig")


def main(argv):
    if argv[:1] == ["write"]:
        d = json.loads(sys.stdin.buffer.read().decode("utf-8", "replace"))
        tool = d.get("tool_name") or d.get("toolName") or ""
        args = d.get("tool_input") or d.get("toolArgs") or {}
        if isinstance(args, str) and args.lstrip()[:1] == "{":
            args = json.loads(args)
        root = os.environ.get("SDLC_REPO_ROOT") or os.getcwd()
        path = argv[1] if len(argv) > 1 else (
            (args.get("file_path") or args.get("path") or "") if isinstance(args, dict)
            else "")
        if not path:
            return CANNOT, "no path in the payload"
        return check_write(root, path, tool, args, default_cache(root))
    pos, name = [], None
    i = 0
    while i < len(argv):
        if argv[i] == "--as" and i + 1 < len(argv):
            name = argv[i + 1]
            i += 2
            continue
        pos.append(argv[i])
        i += 1
    if len(pos) != 2:
        return CANNOT, "usage: sdlc-cosmetic.py <before> <after> [--as <path>] | write [<file>]"
    name = name or pos[1]
    try:
        before, after = _read(pos[0]), _read(pos[1])
    except (OSError, UnicodeDecodeError) as e:
        return CANNOT, "could not read the files (%s)" % e.__class__.__name__
    root = os.environ.get("SDLC_REPO_ROOT") or os.getcwd()
    return classify(name, before, after, default_cache(root), root)


if __name__ == "__main__":
    try:
        code, detail = main(sys.argv[1:])
    except Exception as e:
        code, detail = CANNOT, "classifier error (%s)" % e.__class__.__name__
    sys.stdout.write(detail + "\n")
    sys.exit(code)
