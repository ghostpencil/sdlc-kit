#!/usr/bin/env python
"""Re-runnable proof for templates/sdlc-cosmetic.template.py (FEATURE_PLAN.md 82).

Two passes, and the second is the point:

  1. a unit pass driving the classifier through its real interfaces - classify(),
     check_write() and the CLI - over:
       - the 35-case corpus and the nine-edit indentation sweep that measured the
         design (82.1, 82.2; ported from tools/cosmetic-prototypes/), with the
         shipped design's expected answer per case, which is the ground truth
         except where a known SAFE extra is pinned as such;
       - per-language fixtures, including the fields a tree compare can drop
         without noticing (an operator, let/const, a break label);
       - one added and one removed case per directive in 82.9 ruling 5, plus a
         moved directive and a plain-comment control per language;
       - C# #if/#define/#region, and an edit inside an inactive #if that only the
         Roslyn trivia compare can see; TS triple-slash and @jsx; one JS-family
         case per extension;
       - every TypeScript case on every typescript it is given (the third adopter
         is on 6.x, the prototype ran on 5.9), and a pnpm-shaped workspace whose
         package pins its own version;
       - the payload rebuild for Claude Code Edit/Write and Copilot edit/create;
       - the failure paths: toolchain off PATH, a PATH java that is not the JDK's,
         compile and compare timeouts, a corrupt and a half-written cache entry,
         parse errors, an unknown extension - each must answer "cannot tell" or
         "real", never "cosmetic";
  2. a mutation pass that breaks the classifier - the count derived from the
     MUTATIONS list at run time, never stated here - and requires the unit pass to
     notice each one. A suite that survives its own mutations is not testing the
     thing it claims to (invariant 13).

A toolchain that is missing does not pass: its cases are reported SKIPPED and the run
exits 1 as INCOMPLETE. TypeScript is not vendored - point the suite at one or more
installs (a directory holding node_modules/typescript):

  npm install --prefix <dir> typescript@6.0.3
  python tools/cosmetic-check.py --ts <dir> [--ts <dir2> ...]     (or COSMETIC_TS,
                                                                   os.pathsep-separated)

Java needs a JDK (JAVA_HOME or javac on PATH), C# a .NET SDK (dotnet on PATH).
Kit-development artifact: lives at the root, never ships inside sdlc-kit/ (invariant 12).
"""
import importlib.util
import io
import json
import os
import stat
import shutil
import subprocess
import sys
import tempfile
import traceback
from concurrent.futures import ThreadPoolExecutor

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TPL = os.path.join(REPO, "sdlc-kit", "templates", "sdlc-cosmetic.template.py")
COSMETIC, REAL, CANNOT = 0, 1, 2
# An edit that leaves an empty block cannot parse at all; what matters is that it is
# never cosmetic (the prototype counted both answers as "caught").
NOT_COSMETIC = "real or cannot-tell"
NAMES = {0: "cosmetic", 1: "real", 2: "cannot-tell"}


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
    """Run one pass; an unexpected exception REPORTS and the run continues
    (FEATURE_PLAN.md 75.7 ruling 3, the same guard every sibling suite carries)."""
    try:
        return fn(*a, **kw)
    except Exception:
        traceback.print_exc()
        print("CRASHED  %s  <-- pass did not complete; its remaining cases did not run"
              % label)
        guarded.crashed.append(label)
        return default


guarded.crashed = []


def load(src, where):
    p = os.path.join(where, "sdlc_cosmetic_under_test.py")
    io.open(p, "w", encoding="utf-8", newline="\n").write(src)
    spec = importlib.util.spec_from_file_location("sdlc_cosmetic_under_test", p)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m, p


def r(s, old, new):
    assert s.count(old) == 1, (old, s)
    return s.replace(old, new, 1)


# --- the measured corpus (82.1), ported from tools/cosmetic-prototypes/probe.py ------

PY = '''import os


def add(a, b):
    """Add two numbers."""
    # sum them
    total = a + b
    if total > 10:
        total = 10
    return total


NAMES = ['x', 'y', 'z']
'''

TS = '''export function add(a: number, b: number): number {
  // sum them
  const total = a + b;
  return total;
}

export const NAMES = ["x", "y", "z"];
'''

GO = '''package calc

// Add sums two numbers.
func Add(a int, b int) int {
\ttotal := a + b
\treturn total
}
'''

JAVA = '''public class Calc {
    // sum them
    public static int add(int a, int b) {
        int total = a + b;
        return total;
    }
}
'''

CS = '''public static class Calc
{
    // sum them
    public static int Add(int a, int b)
    {
        var total = a + b;
        return total;
    }
}
'''

RS = '''/// Adds two numbers.
pub fn add(a: i32, b: i32) -> i32 {
    // sum them
    let total = a + b;
    total
}
'''

# (name, ext, before, after, expected). Expected is the ground truth of 82.1 except:
# Go and Rust are out of scope (cannot tell - today's rule), and redundant parentheses
# in TS/Java/C# stay in the tree (a known SAFE extra, 82.3).
CORPUS = [
    ("py comment text edited", "py", PY, r(PY, "# sum them", "# sum them up, capped at 10"), COSMETIC),
    ("py comment line added", "py", PY, r(PY, "    total = a + b", "    # cap below\n    total = a + b"), COSMETIC),
    ("py inline comment added", "py", PY, r(PY, "total = a + b", "total = a + b  # plain sum"), COSMETIC),
    ("py blank lines changed", "py", PY, r(PY, "\n\n\ndef add", "\n\ndef add"), COSMETIC),
    ("py reformat list (black-style)", "py", PY, r(PY, "NAMES = ['x', 'y', 'z']", "NAMES = [\n    'x',\n    'y',\n    'z',\n]"), COSMETIC),
    ("py quote style", "py", PY, r(PY, "['x', 'y', 'z']", '["x", "y", "z"]'), COSMETIC),
    ("py redundant parens", "py", PY, r(PY, "total = a + b", "total = (a + b)"), COSMETIC),
    ("py operator spacing", "py", PY, r(PY, "total = a + b", "total=a+b"), COSMETIC),
    ("py CRLF line endings", "py", PY, PY.replace("\n", "\r\n"), COSMETIC),
    ("py `# type: ignore` added", "py", PY, r(PY, "import os", "import os  # type: ignore"), REAL),
    ("py `# noqa` added", "py", PY, r(PY, "import os", "import os  # noqa: F401"), REAL),
    ("py docstring edited", "py", PY, r(PY, "Add two numbers.", "Add two numbers, capped at 10."), REAL),
    ("py dedent out of if", "py", PY, r(PY, "        total = 10\n", "    total = 10\n"), NOT_COSMETIC),
    ("py operator changed", "py", PY, r(PY, "a + b", "a - b"), REAL),
    ("py string content changed", "py", PY, r(PY, "'z'", "'# z'"), REAL),
    ("py after has syntax error", "py", PY, r(PY, "total = a + b", "total = a + # b"), CANNOT),
    ("py new file (empty before)", "py", "", PY, REAL),
    ("ts comment edited", "ts", TS, r(TS, "// sum them", "// sum them up"), COSMETIC),
    ("ts block comment added", "ts", TS, r(TS, "export function", "/** Adds. */\nexport function"), COSMETIC),
    ("ts reformat", "ts", TS, r(TS, '["x", "y", "z"]', '[\n  "x",\n  "y",\n  "z",\n]'), COSMETIC),
    ("ts semicolon dropped (ASI)", "ts", TS, r(TS, "const total = a + b;", "const total = a + b"), COSMETIC),
    ("ts `@ts-expect-error` added", "ts", TS, r(TS, "  const total", "  // @ts-expect-error\n  const total"), REAL),
    ("ts operator changed", "ts", TS, r(TS, "a + b", "a * b"), REAL),
    ("go comment edited", "go", GO, r(GO, "// Add sums two numbers.", "// Add sums two ints."), CANNOT),
    ("go reformat", "go", GO, r(GO, "total := a + b", "total:=a+b"), CANNOT),
    ("go `//go:build` added", "go", GO, "//go:build linux\n\n" + GO, CANNOT),
    ("go operator changed", "go", GO, r(GO, "a + b", "a - b"), CANNOT),
    ("java comment edited", "java", JAVA, r(JAVA, "// sum them", "// sum both"), COSMETIC),
    ("java reformat", "java", JAVA, r(JAVA, "int total = a + b;", "int total=a+b;"), COSMETIC),
    ("java operator changed", "java", JAVA, r(JAVA, "a + b", "a - b"), REAL),
    ("cs comment edited", "cs", CS, r(CS, "// sum them", "// sum both"), COSMETIC),
    ("cs operator changed", "cs", CS, r(CS, "a + b", "a - b"), REAL),
    ("rs line comment edited", "rs", RS, r(RS, "// sum them", "// sum both"), CANNOT),
    ("rs doc comment edited", "rs", RS, r(RS, "/// Adds two numbers.", "/// Adds two i32s."), CANNOT),
    ("rs operator changed", "rs", RS, r(RS, "a + b", "a - b"), CANNOT),
]

# --- the indentation sweep (82.2), ported from tools/cosmetic-prototypes/indent.py ---

INDENT_SRC = '''def f(items, flag):
    out = []
    for x in items:
        if x:
            out.append(x)
        out.append(0)
    else:
        out.append(-1)
    while flag:
        flag = False
        out.append(1)
    with open("p") as h:
        data = h.read()
        out.append(data)
    try:
        g()
        out.append(2)
    except ValueError:
        out.append(3)
    return out


class C:
    def m(self):
        return 1

    def n(self):
        return 2
'''

INDENT = [
    ("last stmt out of if", "            out.append(x)\n", "        out.append(x)\n"),
    ("stmt into if", "        out.append(0)\n", "            out.append(0)\n"),
    ("stmt out of for", "        out.append(0)\n", "    out.append(0)\n"),
    ("stmt out of while", "        out.append(1)\n", "    out.append(1)\n"),
    ("stmt out of with", "        out.append(data)\n", "    out.append(data)\n"),
    ("stmt out of try", "        out.append(2)\n", "    out.append(2)\n"),
    ("stmt out of except", "        out.append(3)\n", "    out.append(3)\n"),
    ("return into except", "    return out\n", "        return out\n"),
    ("method out of class", "    def n(self):\n        return 2\n", "def n(self):\n    return 2\n"),
]

# --- per-language fixtures ----------------------------------------------------------

PY2 = '''#!/usr/bin/env python
import os


def add(a, b):
    total = a + b
    return total
'''

TS2 = '''import { thing } from "./thing";
import type { Shape } from "./shape";

export function step(xs: number[]): number {
  let n = 0;
  for (const x of xs) {
    n++;
  }
  outer: for (const y of xs) {
    if (y > 2) break outer;
  }
  return n + thing;
}

export function other(s: Shape): string {
  return 'ok';
}
'''

JAVA2 = '''package p;

import java.util.List;

/** Steps. */
public class Step {
  int step(List<Integer> xs) {
    int n = 0;
    outer:
    for (int x : xs) {
      inner:
      for (int y : xs) {
        if (y > 2) break outer;
        n++;
      }
    }
    return n;
  }
}
'''

CS2 = '''using System;

namespace P
{
    /// <summary>Steps.</summary>
    public static class Step
    {
        public static int Run(int[] xs)
        {
            var n = 0;
            foreach (var x in xs)
            {
                n++;
            }
#if NEVER
            Console.WriteLine("one");
            Console.WriteLine("two");
            Console.WriteLine("three");
#endif
            return n;
        }
    }
}
'''

JSX = '''import React from "react";

export function Hello({ name }) {
  // greet
  return <div className="hi">{name}</div>;
}
'''

JS = '''export function add(a, b) {
  // sum them
  const total = a + b;
  return total;
}
'''

FIXTURES = [
    # Python
    ("py2 shebang added on line 1", "py", "#!/usr/bin/env python3\n" + PY, PY, REAL),
    ("py2 shebang removed", "py", PY2, PY2.replace("#!/usr/bin/env python\n", ""), REAL),
    ("py2 shebang edited", "py", PY2, r(PY2, "#!/usr/bin/env python", "#!/usr/bin/python3"), REAL),
    ("py2 coding line added on line 1", "py", PY, "# -*- coding: latin-1 -*-\n" + PY, REAL),
    ("py2 a #! below line 1 is a plain comment", "py", PY2,
     r(PY2, "import os\n", "import os\n#! not a shebang\n"), COSMETIC),
    ("py2 `#noqa` with no space still counts", "py", PY, r(PY, "import os", "import os  #noqa"), REAL),
    ("py2 directive moved to another line", "py", PY2 + "\n\nimport sys  # noqa\n",
     r(PY2, "import os", "import os  # noqa") + "\n\nimport sys\n", REAL),
    ("py2 comment next to a directive is a plain comment", "py",
     r(PY2, "import os", "# about os\nimport os  # noqa"),
     r(PY2, "import os", "# about the os module\nimport os  # noqa"), COSMETIC),
    # TypeScript
    ("ts2 n++ -> n--", "ts", TS2, r(TS2, "n++", "n--"), REAL),
    ("ts2 let -> const", "ts", TS2, r(TS2, "let n = 0", "const n = 0"), REAL),
    ("ts2 break label changed", "ts", TS2, r(TS2, "break outer", "break"), REAL),
    ("ts2 import type -> import", "ts", TS2, r(TS2, "import type { Shape }", "import { Shape }"), REAL),
    ("ts2 quote style", "ts", TS2, r(TS2, "'ok'", '"ok"'), COSMETIC),
    ("ts2 JSDoc text added", "ts", TS2, r(TS2, "export function other", "/** Other. @param s the shape */\nexport function other"), COSMETIC),
    ("ts2 JSDoc @deprecated added", "ts", TS2, r(TS2, "export function other", "/** @deprecated */\nexport function other"), REAL),
    ("ts2 reformatted block", "ts", TS2, r(TS2, "for (const x of xs) {\n    n++;\n  }", "for (const x of xs) { n++; }"), COSMETIC),
    ("ts2 triple-slash reference added", "ts", TS2, '/// <reference types="node" />\n' + TS2, REAL),
    ("ts2 `@jsx` pragma added", "ts", TS2, "/** @jsx h */\n" + TS2, REAL),
    ("ts2 directive moved", "ts", r(TS2, "  let n = 0;", "  // @ts-expect-error\n  let n = 0;"),
     r(TS2, "  return n + thing;", "  // @ts-expect-error\n  return n + thing;"), REAL),
    ("ts2 parse error", "ts", TS2, r(TS2, "return n + thing;", "return n + ;"), CANNOT),
    ("ts2 parens (safe extra)", "ts", TS2, r(TS2, "return n + thing;", "return (n + thing);"), REAL),
    # JS family, parsed by the same typescript (82.9, third-adopter ruling)
    ("js comment edited", "js", JS, r(JS, "// sum them", "// sum both"), COSMETIC),
    ("js operator changed", "js", JS, r(JS, "a + b", "a - b"), REAL),
    ("mjs comment edited", "mjs", JS, r(JS, "// sum them", "// sum both"), COSMETIC),
    ("mjs operator changed", "mjs", JS, r(JS, "a + b", "a - b"), REAL),
    ("cjs comment edited", "cjs", JS, r(JS, "// sum them", "// sum both"), COSMETIC),
    ("cjs operator changed", "cjs", JS, r(JS, "a + b", "a - b"), REAL),
    ("jsx comment edited", "jsx", JSX, r(JSX, "// greet", "// say hello"), COSMETIC),
    ("jsx attribute changed", "jsx", JSX, r(JSX, '"hi"', '"hey"'), REAL),
    ("jsx `@jsxImportSource` added", "jsx", JSX, "/** @jsxImportSource preact */\n" + JSX, REAL),
    ("tsx comment edited", "tsx", JSX, r(JSX, "// greet", "// say hello"), COSMETIC),
    ("mts comment edited", "mts", TS, r(TS, "// sum them", "// sum both"), COSMETIC),
    ("mts operator changed", "mts", TS, r(TS, "a + b", "a - b"), REAL),
    ("cts comment edited", "cts", TS, r(TS, "// sum them", "// sum both"), COSMETIC),
    ("cts operator changed", "cts", TS, r(TS, "a + b", "a - b"), REAL),
    # Java
    ("java2 n++ -> n--", "java", JAVA2, r(JAVA2, "n++", "n--"), REAL),
    ("java2 break label changed", "java", JAVA2, r(JAVA2, "break outer", "break inner"), REAL),
    ("java2 javadoc edited", "java", JAVA2, r(JAVA2, "/** Steps. */", "/** Steps through xs. */"), COSMETIC),
    # Ruled 2026-10-19 (82.10): a Javadoc @deprecated does not change execution.
    ("java2 javadoc @deprecated added", "java", JAVA2, r(JAVA2, "/** Steps. */", "/** Steps.\n * @deprecated use Walk */"), COSMETIC),
    ("java2 @SuppressWarnings added", "java", JAVA2, r(JAVA2, "  int step(", '  @SuppressWarnings("unused")\n  int step('), REAL),
    ("java2 import made static", "java", JAVA2, r(JAVA2, "import java.util.List;", "import static java.util.List.of;\nimport java.util.List;"), REAL),
    ("java2 reformatted", "java", JAVA2, r(JAVA2, "if (y > 2) break outer;", "if (y > 2)\n          break outer;"), COSMETIC),
    ("java2 parse error", "java", JAVA2, r(JAVA2, "return n;", "return n"), CANNOT),
    ("java2 parens (safe extra)", "java", JAVA2, r(JAVA2, "return n;", "return (n);"), REAL),
    # C#
    ("cs2 n++ -> n--", "cs", CS2, r(CS2, "n++", "n--"), REAL),
    ("cs2 XML doc comment edited", "cs", CS2, r(CS2, "<summary>Steps.</summary>", "<summary>Steps through xs.</summary>"), COSMETIC),
    ("cs2 #region added", "cs", CS2, r(CS2, "        public static int Run", "        #region run\n        public static int Run").replace(
        "            return n;\n        }\n", "            return n;\n        }\n        #endregion\n"), COSMETIC),
    ("cs2 #define added", "cs", CS2, "#define NEVER\n" + CS2, REAL),
    ("cs2 #pragma added", "cs", CS2, r(CS2, "            var n = 0;", "#pragma warning disable CS0168\n            var n = 0;"), REAL),
    ("cs2 #nullable added", "cs", CS2, "#nullable enable\n" + CS2, REAL),
    ("cs2 edit mid inactive #if (only the trivia compare sees it)", "cs", CS2,
     r(CS2, '"two"', '"TWO"'), REAL),
    ("cs2 edit adjacent to #if", "cs", CS2, r(CS2, '"one"', '"ONE"'), REAL),
    ("cs2 reformatted", "cs", CS2, r(CS2, "Run(int[] xs)", "Run( int[] xs )"), COSMETIC),
    ("cs2 reformat beside #if (safe extra: the directive's anchor moved)", "cs", CS2, r(CS2, "foreach (var x in xs)\n            {\n                n++;\n            }", "foreach (var x in xs) { n++; }"), REAL),
    ("cs2 parse error", "cs", CS2, r(CS2, "var n = 0;", "var n = ;"), CANNOT),
    # Out of scope by extension
    ("unknown extension", "kt", "val a = 1\n", "val a = 1 // one\n", CANNOT),
]


def directive_cases():
    """One added and one removed case per directive in 82.9 ruling 5 - each placed in
    a standalone comment line, where the tree compare is blind and only the directive
    check can answer - plus a plain-comment control per language."""
    out = []
    plain = {"py": PY2, "ts": TS2, "java": JAVA2, "cs": CS2}
    anchor = {"py": "    total = a + b", "ts": "  let n = 0;", "java": "    int n = 0;",
              "cs": "            var n = 0;"}
    lead = {"py": "    # ", "ts": "  // ", "java": "    // ", "cs": "            // "}
    lists = {
        "py": ["noqa", "ruff: noqa", "type: ignore", "pyright: ignore", "mypy: ignore-errors",
               "pylint: disable=all", "pragma: no cover", "nosec", "fmt: off", "fmt: on",
               "fmt: skip", "isort: skip"],
        "java": ["//noinspection", "NOPMD", "CHECKSTYLE:OFF", "CHECKSTYLE:ON",
                 "CHECKSTYLE.OFF", "NOSONAR", "@formatter:off", "@formatter:on",
                 "spotless:off", "spotless:on", "$NON-NLS-1$", "fallthru",
                 "fall through", "falls through"],
        "cs": ["ReSharper disable All", "ReSharper restore All", "<auto-generated />",
               "NOSONAR"],
        "ts": ["@ts-ignore", "@ts-expect-error", "@ts-nocheck", "@ts-check",
               "/// <reference path=\"x.d.ts\" />", "/// <amd-module name=\"m\" />",
               "@jsx h", "@jsxImportSource preact", "@jsxFrag Fragment",
               "@jsxRuntime classic", "eslint-disable-next-line", "eslint-enable",
               "/* eslint no-console: 0 */", "/* global foo */", "prettier-ignore",
               "biome-ignore lint: x", "istanbul ignore next", "c8 ignore next",
               "v8 ignore next", "webpackChunkName: \"x\"", "webpackIgnore: true",
               "@vite-ignore", "__PURE__"],
    }
    for lang, items in lists.items():
        base = plain[lang]
        for d in items:
            # A directive that is itself a whole comment keeps only the indentation.
            if d.startswith(("/*", "///", "//")):
                line = lead[lang][:len(lead[lang]) - len(lead[lang].lstrip())] + d
            else:
                line = lead[lang] + d
            withd = r(base, anchor[lang], line + "\n" + anchor[lang])
            out.append(("%s directive added: %s" % (lang, d), lang, base, withd, REAL))
            out.append(("%s directive removed: %s" % (lang, d), lang, withd, base, REAL))
        ctl = r(base, anchor[lang], lead[lang] + "an ordinary note\n" + anchor[lang])
        out.append(("%s control: an ordinary comment is cosmetic" % lang, lang, base, ctl,
                    COSMETIC))
    # C#: every preprocessor directive but the region pair.
    for d in ("#pragma warning disable CS0168", "#warning look here", "#line 200",
              "#line default", "#nullable disable"):
        withd = r(CS2, anchor["cs"], d + "\n" + anchor["cs"])
        out.append(("cs directive added: %s" % d, "cs", CS2, withd, REAL))
        out.append(("cs directive removed: %s" % d, "cs", withd, CS2, REAL))
    return out


# --- the bench ------------------------------------------------------------------------

def ts_stub(at, real):
    """node_modules/typescript at `at` that loads the real install - the shape a
    workspace's own pin has, without links (no symlink privilege on Windows)."""
    d = os.path.join(at, "node_modules", "typescript")
    os.makedirs(d, exist_ok=True)
    io.open(os.path.join(d, "package.json"), "w").write(
        json.dumps({"name": "typescript", "version": "0.0.0-stub", "main": "index.js"}))
    io.open(os.path.join(d, "index.js"), "w").write(
        "module.exports = require(%s);\n" % json.dumps(os.path.join(real, "node_modules",
                                                                    "typescript")))


def ts_version(real):
    try:
        return json.load(io.open(os.path.join(real, "node_modules", "typescript",
                                              "package.json")))["version"]
    except (OSError, ValueError, KeyError):
        return None


class Toolchains:
    def __init__(self, m, ts_dirs):
        self.java = m._jdk() is not None
        self.cs = m._dotnet() is not None
        self.node = shutil.which("node") is not None
        self.ts = [(d, ts_version(d)) for d in ts_dirs if ts_version(d)]

    def skipped(self):
        s = []
        if not self.java:
            s.append("java: no JDK (JAVA_HOME or javac on PATH)")
        if not self.cs:
            s.append("csharp: no .NET SDK (dotnet on PATH)")
        if not self.node:
            s.append("typescript: node is not on PATH")
        elif not self.ts:
            s.append("typescript: no install given (--ts <dir> or COSMETIC_TS)")
        elif len(self.ts) < 2:
            s.append("typescript: one install given - the per-package pin case needs two")
        return s


def unit(src, ts_dirs, verbose=True, counter=None):
    """Returns the list of failed case names; counts every case into `counter`."""
    failures = []
    base = tempfile.mkdtemp(prefix="cosmetic-check-")

    def case(name, cond, got=None):
        if counter is not None:
            counter.append(name)
        if not cond:
            failures.append(name)
            if verbose:
                print("FAIL  %s%s" % (name, "  (got: %s)" % (got,) if got is not None else ""))

    try:
        m, mpath = load(src, base)
        tc = Toolchains(m, ts_dirs)
        cache = os.path.join(base, "git", "sdlc-tdd", "cosmetic")
        os.makedirs(cache)
        if counter is not None and verbose:
            unit.skipped = tc.skipped()
        langs = {"py": True, "java": tc.java, "cs": tc.cs,
                 "ts": tc.node and bool(tc.ts), "tsx": tc.node and bool(tc.ts),
                 "js": tc.node and bool(tc.ts), "jsx": tc.node and bool(tc.ts),
                 "mjs": tc.node and bool(tc.ts), "cjs": tc.node and bool(tc.ts),
                 "mts": tc.node and bool(tc.ts), "cts": tc.node and bool(tc.ts),
                 "go": True, "rs": True, "kt": True}

        # Every TS case runs once per typescript, in a workspace that resolves it.
        roots = {}
        for d, v in tc.ts:
            ws = os.path.join(base, "ws-" + v)
            ts_stub(ws, d)
            os.makedirs(os.path.join(ws, "src"))
            roots[v] = ws
        plain = os.path.join(base, "plain")
        os.makedirs(os.path.join(plain, "src"))

        jobs = []
        for name, ext, before, after, want in CORPUS + FIXTURES + directive_cases():
            if not langs.get(ext, True):
                continue
            if ext in ("ts", "tsx", "mts", "cts", "js", "jsx", "mjs", "cjs"):
                for v, ws in roots.items():
                    jobs.append(("%s [typescript %s]" % (name, v), ws,
                                 os.path.join(ws, "src", "f." + ext), before, after, want, v))
            else:
                jobs.append((name, plain, os.path.join(plain, "src", "f." + ext),
                             before, after, want, None))
        for i, (name, old, new) in enumerate(INDENT):
            jobs.append(("indent sweep: " + name, plain, os.path.join(plain, "src", "i.py"),
                         INDENT_SRC, INDENT_SRC.replace(old, new), NOT_COSMETIC, None))

        # Warm the compile caches one at a time: the pool below shares a process, and
        # the build's temporary name is per process.
        if tc.java:
            m.classify(os.path.join(plain, "W.java"), JAVA, JAVA + "\n", cache, plain)
        if tc.cs:
            m.classify(os.path.join(plain, "w.cs"), CS, CS + "\n", cache, plain)

        def one(j):
            name, root, path, before, after, want, v = j
            return j, m.classify(path, before, after, cache, root)

        with ThreadPoolExecutor(4) as pool:
            for (name, root, path, before, after, want, v), (code, detail) in pool.map(one, jobs):
                ok = code != COSMETIC if want == NOT_COSMETIC else code == want
                # A TS verdict must come from the typescript the case was placed under.
                if ok and v and code != CANNOT and ("typescript %s" % v) not in detail \
                        and detail != "identical" and "directive" not in detail:
                    ok = False
                case(name, ok, "%s - %s" % (NAMES.get(code, code), detail))

        # --- each layer on its own: a mutation masked by the other layer must still
        # be caught, so the layers are proven separately, not only in sequence -------
        code, detail = m._python(PY, r(PY, "import os", "import os  # type: ignore"))
        case("layer: the python tree alone sees `# type: ignore`", code == REAL, detail)
        code, detail = m._python(PY, r(PY, "import os", "import os  # noqa"))
        case("layer: the python tree alone is blind to `# noqa` (why the directive "
             "check exists)", code == COSMETIC, detail)
        if tc.cs:
            w = os.path.join(base, "layer")
            os.makedirs(w)
            a, b = os.path.join(w, "a.cs"), os.path.join(w, "b.cs")
            io.open(a, "w").write(CS2)
            io.open(b, "w").write("#define NEVER\n" + CS2)
            code, detail = m._csharp(a, b, cache)
            case("layer: the C# trivia compare alone sees #define", code == REAL, detail)
        v_a = m._directive_view(PY2 + "\n\nimport sys  # noqa\n", "python")
        v_b = m._directive_view(r(PY2, "import os", "import os  # noqa") + "\n\nimport sys\n",
                                "python")
        case("layer: the directive view orders and anchors, not just counts", v_a != v_b)

        # --- TypeScript resolves per file: a package's own pin wins (pnpm) -----------
        if len(tc.ts) >= 2:
            (d_root, v_root), (d_pkg, v_pkg) = tc.ts[0], tc.ts[1]
            ws = os.path.join(base, "pnpm")
            ts_stub(ws, d_root)
            pkg = os.path.join(ws, "packages", "a")
            ts_stub(pkg, d_pkg)
            for at in (os.path.join(ws, "src"), os.path.join(pkg, "src")):
                os.makedirs(at)
            before, after = TS, r(TS, "// sum them", "// sum both")
            code, detail = m.classify(os.path.join(pkg, "src", "f.ts"), before, after,
                                      cache, ws)
            case("pnpm: a package file uses the package's typescript (%s)" % v_pkg,
                 code == COSMETIC and ("typescript %s" % v_pkg) in detail, detail)
            code, detail = m.classify(os.path.join(ws, "src", "f.ts"), before, after,
                                      cache, ws)
            case("pnpm: a root file uses the root's typescript (%s)" % v_root,
                 code == COSMETIC and ("typescript %s" % v_root) in detail, detail)
        if tc.node:
            # Upward resolution can reach a typescript in the user's home (it does on
            # the machine this was written on), so "absent" cannot be staged portably;
            # a typescript that fails to load takes the same exit.
            broken = os.path.join(base, "broken")
            d = os.path.join(broken, "node_modules", "typescript")
            os.makedirs(d)
            os.makedirs(os.path.join(broken, "src"))
            io.open(os.path.join(d, "package.json"), "w").write('{"main": "index.js"}')
            io.open(os.path.join(d, "index.js"), "w").write('throw new Error("broken");\n')
            code, detail = m.classify(os.path.join(broken, "src", "f.ts"), TS,
                                      r(TS, "// sum them", "// sum both"), cache, broken)
            case("a typescript that will not load gives no exemption", code == CANNOT,
                 detail)

        # --- the payload rebuild, through check_write ------------------------------
        proj = os.path.join(base, "proj")
        os.makedirs(os.path.join(proj, ".git"))
        f = os.path.join(proj, "calc.py")
        io.open(f, "w", encoding="utf-8", newline="").write(PY)
        win = f.replace("/", "\\") if os.name == "nt" else f
        cw = lambda tool, args, path=win: m.check_write(proj, path, tool, args, cache)
        code, detail = cw("Edit", {"file_path": win, "old_string": "# sum them",
                                   "new_string": "# add them"})
        case("rebuild: Claude Edit of a comment is cosmetic", code == COSMETIC, detail)
        code, detail = cw("Edit", {"file_path": win, "old_string": "a + b",
                                   "new_string": "a - b"})
        case("rebuild: Claude Edit of code is real", code == REAL, detail)
        twice = PY + "\n# sum them\n"
        io.open(f, "w", encoding="utf-8", newline="").write(twice)
        code, detail = cw("Edit", {"file_path": win, "old_string": "# sum them",
                                   "new_string": "# add them"})
        case("rebuild: an ambiguous old_string is cannot-tell", code == CANNOT, detail)
        code, detail = cw("Edit", {"file_path": win, "old_string": "# sum them",
                                   "new_string": "# add them", "replace_all": True})
        case("rebuild: replace_all edits every match", code == COSMETIC, detail)
        io.open(f, "w", encoding="utf-8", newline="").write(PY)
        code, detail = cw("Edit", {"file_path": win, "old_string": "# not there",
                                   "new_string": "# x"})
        case("rebuild: an old_string not in the file is cannot-tell", code == CANNOT, detail)
        code, detail = cw("Edit", {"file_path": win, "old_string": "",
                                   "new_string": "# x"})
        case("rebuild: an empty old_string is cannot-tell", code == CANNOT, detail)
        code, detail = cw("Write", {"file_path": win,
                                    "content": r(PY, "# sum them", "# add them")})
        case("rebuild: Claude Write of a comment change is cosmetic", code == COSMETIC, detail)
        code, detail = cw("edit", {"path": win, "old_str": "# sum them",
                                   "new_str": "# add them"})
        case("rebuild: Copilot edit of a comment is cosmetic", code == COSMETIC, detail)
        io.open(f, "w", encoding="utf-8", newline="").write(twice)
        code, detail = cw("edit", {"path": win, "old_str": "# sum them", "new_str": "# x"})
        case("rebuild: Copilot edit with an ambiguous old_str is cannot-tell",
             code == CANNOT, detail)
        io.open(f, "w", encoding="utf-8", newline="").write(PY)
        code, detail = cw("create", {"path": win, "file_text": PY.replace("a + b", "b + a")})
        case("rebuild: Copilot create over code is real", code == REAL, detail)
        code, detail = cw("apply_patch", "*** Begin Patch\n*** Update File: calc.py\n")
        case("rebuild: apply_patch is today's rule (cannot tell), and the log says why",
             code == CANNOT and "apply_patch" in detail, detail)
        code, detail = cw("Write", {"content": PY}, os.path.join(proj, "new.py"))
        case("rebuild: a new file is real", code == REAL, detail)
        code, detail = cw("Edit", {"old_string": "# sum them", "new_string": "# x"},
                          "calc.py")
        case("rebuild: a repo-relative path resolves against the root", code == COSMETIC,
             detail)
        io.open(os.path.join(proj, "bin.py"), "wb").write(b"x = '\xff\xfe'\n")
        code, detail = cw("Edit", {"old_string": "x", "new_string": "y"}, "bin.py")
        case("rebuild: a file that is not UTF-8 is cannot-tell", code == CANNOT, detail)
        bom = os.path.join(proj, "bom.py")
        io.open(bom, "wb").write(b"\xef\xbb\xbf" + PY.encode())
        code, detail = cw("Edit", {"old_string": "# sum them", "new_string": "# x"}, bom)
        case("rebuild: a UTF-8 BOM does not defeat the parse", code == COSMETIC, detail)

        # --- the CLI, both modes, through a real process ---------------------------
        def cli(args, stdin=b"", root=proj):
            e = dict(os.environ)
            e["SDLC_REPO_ROOT"] = root
            p = subprocess.run([sys.executable, mpath] + args, input=stdin,
                               capture_output=True, cwd=root, env=e)
            return p.returncode, p.stdout.decode("utf-8", "replace").strip()

        payload = {"session_id": "s", "hook_event_name": "PreToolUse", "tool_name": "Edit",
                   "tool_input": {"file_path": win, "old_string": "# sum them",
                                  "new_string": "# add them"}}
        code, out = cli(["write"], json.dumps(payload).encode())
        case("cli write: a Claude Code payload", code == COSMETIC and out == "python-ast", out)
        payload = {"sessionId": "s", "toolName": "edit",
                   "toolArgs": json.dumps({"path": "calc.py", "old_str": "a + b",
                                           "new_str": "a - b"})}
        code, out = cli(["write"], json.dumps(payload).encode())
        case("cli write: a Copilot payload with string toolArgs", code == REAL, out)
        code, out = cli(["write", f], json.dumps(payload).encode())
        case("cli write: an explicit target path wins", code == REAL, out)
        code, out = cli(["write"], b"{not json")
        case("cli write: a broken payload exits 2, never 0", code == CANNOT, out)
        g = os.path.join(proj, "after.tmp")
        io.open(g, "w", encoding="utf-8").write(r(PY, "# sum them", "# add them"))
        code, out = cli([f, g, "--as", f])
        case("cli pair: --as names the language", code == COSMETIC, out)
        code, out = cli([f, g])
        case("cli pair: without --as a .tmp after-file has no classifier", code == CANNOT, out)
        code, out = cli([f])
        case("cli pair: a bad argument list exits 2", code == CANNOT, out)
        cached = os.path.join(proj, ".git", "sdlc-tdd", "cosmetic")
        if tc.java:
            j1, j2 = os.path.join(proj, "A.java"), os.path.join(proj, "B.java")
            io.open(j1, "w").write(JAVA)
            io.open(j2, "w").write(r(JAVA, "// sum them", "// sum both"))
            code, out = cli([j1, j2])
            case("cli pair: the compile cache lands in the git dir, not the tree",
                 code == COSMETIC and os.path.isdir(cached)
                 and not any(n.endswith(".class") for n in os.listdir(proj)), out)

        # --- failure paths: each must be cannot-tell (or real), never cosmetic -----
        saved = dict(os.environ)
        try:
            os.environ["PATH"] = ""
            os.environ.pop("JAVA_HOME", None)
            if tc.node:
                code, detail = m.classify(os.path.join(plain, "f.ts"), TS,
                                          r(TS, "// sum them", "// x"), cache, plain)
                case("off PATH: no node is cannot-tell", code == CANNOT, detail)
            code, detail = m.classify(os.path.join(plain, "A.java"), JAVA,
                                      r(JAVA, "// sum them", "// x"), cache, plain)
            case("off PATH: no JDK is cannot-tell", code == CANNOT, detail)
            code, detail = m.classify(os.path.join(plain, "a.cs"), CS,
                                      r(CS, "// sum them", "// x"), cache, plain)
            case("off PATH: no .NET SDK is cannot-tell", code == CANNOT, detail)
            code, detail = m.classify(os.path.join(plain, "a.py"), PY,
                                      r(PY, "# sum them", "# x"), cache, plain)
            case("off PATH: python needs nothing and still answers", code == COSMETIC,
                 detail)
        finally:
            os.environ.clear()
            os.environ.update(saved)

        if tc.java:
            # A java on PATH that is not the JDK's. It answers "equal" to everything; the
            # classifier must run the java beside javac, so the operator change stays real.
            fake = os.path.join(base, "fakebin")
            os.makedirs(fake)
            if os.name == "nt":
                io.open(os.path.join(fake, "java.bat"), "w").write("@exit /b 10\r\n")
            else:
                p = os.path.join(fake, "java")
                io.open(p, "w").write("#!/bin/sh\nexit 10\n")
                os.chmod(p, 0o755)
            jdk_bin = os.path.dirname(m._jdk()[0])
            try:
                os.environ.pop("JAVA_HOME", None)
                os.environ["PATH"] = os.pathsep.join([fake, jdk_bin, saved.get("PATH", "")])
                code, detail = m.classify(os.path.join(plain, "A.java"), JAVA,
                                          r(JAVA, "a + b", "a - b"), cache, plain)
                case("a java on PATH that is not the JDK's is never the one run",
                     code == REAL, detail)
            finally:
                os.environ.clear()
                os.environ.update(saved)

            # Compile timeout, on an empty cache: nothing half-built is left behind.
            fresh = os.path.join(base, "fresh-cache")
            os.makedirs(fresh)
            m.COMPILE_TIMEOUT = 0.01
            try:
                code, detail = m.classify(os.path.join(plain, "A.java"), JAVA,
                                          r(JAVA, "// sum them", "// x"), fresh, plain)
            finally:
                m.COMPILE_TIMEOUT = 12
            case("compile timeout is cannot-tell", code == CANNOT, detail)
            case("compile timeout leaves no cache entry behind", os.listdir(fresh) == [],
                 os.listdir(fresh))
            m.COMPARE_TIMEOUT = 0.001
            try:
                code, detail = m.classify(os.path.join(plain, "A.java"), JAVA,
                                          r(JAVA, "// sum them", "// x"), cache, plain)
            finally:
                m.COMPARE_TIMEOUT = 8
            case("compare timeout is cannot-tell", code == CANNOT, detail)

            # A corrupt entry: cannot-tell once, then rebuilt.
            entry = [n for n in os.listdir(cache) if n.startswith("java-")][0]
            io.open(os.path.join(cache, entry, "SdlcJavaCmp.class"), "wb").write(b"\0garbage")
            code, detail = m.classify(os.path.join(plain, "A.java"), JAVA,
                                      r(JAVA, "// sum them", "// x"), cache, plain)
            case("a corrupt java cache entry is cannot-tell", code == CANNOT, detail)
            code, detail = m.classify(os.path.join(plain, "A.java"), JAVA,
                                      r(JAVA, "// sum them", "// x"), cache, plain)
            case("...and the next call rebuilds it", code == COSMETIC, detail)
            # A half-written entry (no `ok` marker) is rebuilt, not trusted.
            os.remove(os.path.join(cache, entry, "ok"))
            io.open(os.path.join(cache, entry, "SdlcJavaCmp.class"), "wb").write(b"\0garbage")
            code, detail = m.classify(os.path.join(plain, "A.java"), JAVA,
                                      r(JAVA, "// sum them", "// x"), cache, plain)
            case("a half-written cache entry is rebuilt, not trusted", code == COSMETIC,
                 detail)
        if tc.cs:
            entry = [n for n in os.listdir(cache) if n.startswith("csharp-")][0]
            io.open(os.path.join(cache, entry, "SdlcCsCmp.dll"), "wb").write(b"\0garbage")
            code, detail = m.classify(os.path.join(plain, "a.cs"), CS,
                                      r(CS, "// sum them", "// x"), cache, plain)
            case("a corrupt C# cache entry is cannot-tell", code == CANNOT, detail)
            code, detail = m.classify(os.path.join(plain, "a.cs"), CS,
                                      r(CS, "// sum them", "// x"), cache, plain)
            case("...and the next call rebuilds it", code == COSMETIC, detail)
    finally:
        rmtree(base)
    return failures


unit.skipped = []


# One mutation per known defect class; the unit pass must notice each. The run fails if
# any mutation survives (invariant 13). The first five are 82.9 ruling 7's own list.
MUTATIONS = [
    ("drop type_comments (a `# type: ignore` is invisible to the python tree)",
     "a = ast.dump(ast.parse(before, type_comments=True))\n"
     "            b = ast.dump(ast.parse(after, type_comments=True))",
     "a = ast.dump(ast.parse(before))\n"
     "            b = ast.dump(ast.parse(after))"),
    ("drop the directive check (`# noqa`, `@ts-expect-error` wave through)",
     "if _directive_view(before, lang) != _directive_view(after, lang):",
     "if False:"),
    ("drop the C# trivia compare (an edit inside an inactive #if compares equal - "
     "82.3)",
     "return Trivia(t1) == Trivia(t2) ? 10 : 11;",
     "return 10;"),
    ("treat a python parse error as equal",
     'return CANNOT, "python could not parse the file (%s)" % e.__class__.__name__',
     'return COSMETIC, "python could not parse the file (%s)" % e.__class__.__name__'),
    ("treat a comparator's parse error as equal",
     'return CANNOT, "%s could not parse the file" % label',
     'return COSMETIC, "%s could not parse the file" % label'),
    ("accept an ambiguous old_str match (the guard classifies an edit the tool would "
     "refuse, or a different one)",
     "if n != 1:",
     "if n == 0:"),
    ("compare directives as a multiset (a moved `@ts-expect-error` governs another "
     "line, unseen)",
     "view.append((lines[i], lines[code[k - 1]] if k else \"\",\n"
     "                     lines[code[k]] if k < len(code) else \"\"))",
     "view.append((lines[i],))\n    view.sort()"),
    ("match directives with their whitespace (`#noqa` slips past `# noqa`)",
     's = _WS.sub("", line).lower()',
     's = line.lower()'),
    ("count every C# directive including #region (a layout marker costs a licence)",
     'not s.startswith(("#region",\n'
     '                                                                   "#endregion"))',
     'True'),
    ("fingerprint only TS node kinds (n++ -> n--, let -> const, import type compare "
     "equal)",
     'if (!SKIP.has(k) && ["string", "number", "boolean", "bigint"].includes(typeof v))',
     'if (k === "kind")'),
    ("let positions into the TS fingerprint (every comment edit becomes real - the "
     "exemption silently never fires)",
     'const SKIP = new Set(["pos", "end", "id",',
     'const SKIP = new Set(["id",'),
    ("fingerprint only Java tree kinds (a break label or a static import compares "
     "equal)",
     "for (Method m : props(t.getClass())) {",
     "for (Method m : new ArrayList<Method>()) {"),
    ("resolve typescript from the root only (a workspace package's own pin is "
     "ignored)",
     "full, os.path.dirname(full),",
     "full,"),
    ("drop the JS family (.mjs gets no exemption the owner ruled it should)",
     '".mjs": "typescript", ',
     ""),
    ("run the java on PATH (a JRE ahead of the JDK answers for it)",
     'javac, java = _exe(d, "javac"), _exe(d, "java")',
     'javac, java = _exe(d, "javac"), shutil.which("java")'),
    ("read a runtime's own exit 1 as a verdict (a JVM that cannot load the class "
     "says 'real' forever, and a host that dies says 'different')",
     "    if rc == 11:\n        return REAL,",
     "    if rc in (1, 11):\n        return REAL,"),
    ("keep a broken cache entry (one corrupt build disables the exemption until "
     "someone deletes it by hand)",
     "return _verdict(rc, out, label, drop=d)",
     "return _verdict(rc, out, label)"),
    ("trust a cache entry without its ok marker (a half-written build is run)",
     'if os.path.isfile(os.path.join(final, "ok")):\n        return final, None',
     'if os.path.isdir(final):\n        return final, None'),
    ("read a timeout as equal",
     'return None, "timed out after %ss" % timeout',
     'return 10, ""'),
    ("compare without a BOM strip (a BOM file never parses, so never exempts)",
     'before = f.read().decode("utf-8-sig")',
     'before = f.read().decode("utf-8")'),
]


def main(argv):
    ts_dirs = [d for d in os.environ.get("COSMETIC_TS", "").split(os.pathsep) if d]
    i = 0
    while i < len(argv):
        if argv[i] == "--ts" and i + 1 < len(argv):
            ts_dirs.append(argv[i + 1])
            i += 2
        else:
            print("usage: cosmetic-check.py [--ts <dir>]...")
            return 2
    ts_dirs = [os.path.abspath(d) for d in ts_dirs]
    src = io.open(TPL, encoding="utf-8").read()

    names = []
    failures = guarded("unit pass", [], unit, src, ts_dirs, counter=names)
    print("unit pass: %d/%d cases green" % (len(names) - len(failures), len(names)))
    for s in unit.skipped:
        print("SKIPPED  %s" % s)
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
                         ts_dirs, verbose=False)
        if caught:
            print("caught   %s" % label)
            print("           (by: %s)" % "; ".join(caught[:3]))
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
    if unit.skipped:
        print("INCOMPLETE: %d toolchain gap(s) - their cases did not run" % len(unit.skipped))
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
