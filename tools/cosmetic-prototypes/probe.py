"""Measure difftastic (and Python ast.dump) as a "no syntactic change" classifier.

Usage: python -I probe.py <path-to-difft> <work-dir>

Each case is (name, ext, before, after, real) where `real` is the ground truth:
True  = the edit can change behavior / what the gate checks (guard must still apply)
False = comment / formatting only (guard could safely wave it through)
"""
import ast
import os
import subprocess
import sys
import time

DIFFT, WORK = sys.argv[1], sys.argv[2]
os.makedirs(WORK, exist_ok=True)

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
	total := a + b
	return total
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


def r(s, old, new):
    assert old in s, (old, s)
    return s.replace(old, new, 1)


CASES = [
    # ---- Python ----
    ("py comment text edited", "py", PY, r(PY, "# sum them", "# sum them up, capped at 10"), False),
    ("py comment line added", "py", PY, r(PY, "    total = a + b", "    # cap below\n    total = a + b"), False),
    ("py inline comment added", "py", PY, r(PY, "total = a + b", "total = a + b  # plain sum"), False),
    ("py blank lines changed", "py", PY, r(PY, "\n\n\ndef add", "\n\ndef add"), False),
    ("py reformat list (black-style)", "py", PY, r(PY, "NAMES = ['x', 'y', 'z']", "NAMES = [\n    'x',\n    'y',\n    'z',\n]"), False),
    ("py quote style ' -> \"", "py", PY, r(PY, "['x', 'y', 'z']", '["x", "y", "z"]'), False),
    ("py redundant parens", "py", PY, r(PY, "total = a + b", "total = (a + b)"), False),
    ("py operator spacing", "py", PY, r(PY, "total = a + b", "total=a+b"), False),
    ("py CRLF line endings", "py", PY, PY.replace("\n", "\r\n"), False),
    ("py `# type: ignore` added", "py", PY, r(PY, "import os", "import os  # type: ignore"), True),
    ("py `# noqa` added", "py", PY, r(PY, "import os", "import os  # noqa: F401"), True),
    ("py docstring edited", "py", PY, r(PY, "Add two numbers.", "Add two numbers, capped at 10."), True),
    ("py dedent out of if (semantic)", "py", PY, r(PY, "        total = 10\n", "    total = 10\n"), True),
    ("py operator changed", "py", PY, r(PY, "a + b", "a - b"), True),
    ("py string content changed", "py", PY, r(PY, "'z'", "'# z'"), True),
    ("py after has syntax error", "py", PY, r(PY, "total = a + b", "total = a + # b"), True),
    ("py new file (empty before)", "py", "", PY, True),
    # ---- TypeScript ----
    ("ts comment edited", "ts", TS, r(TS, "// sum them", "// sum them up"), False),
    ("ts block comment added", "ts", TS, r(TS, "export function", "/** Adds. */\nexport function"), False),
    ("ts reformat", "ts", TS, r(TS, '["x", "y", "z"]', '[\n  "x",\n  "y",\n  "z",\n]'), False),
    ("ts semicolon dropped (ASI)", "ts", TS, r(TS, "const total = a + b;", "const total = a + b"), False),
    ("ts `@ts-expect-error` added", "ts", TS, r(TS, "  const total", "  // @ts-expect-error\n  const total"), True),
    ("ts operator changed", "ts", TS, r(TS, "a + b", "a * b"), True),
    # ---- Go ----
    ("go comment edited", "go", GO, r(GO, "// Add sums two numbers.", "// Add sums two ints."), False),
    ("go reformat (gofmt-undo)", "go", GO, r(GO, "total := a + b", "total:=a+b"), False),
    ("go `//go:build` tag added", "go", GO, "//go:build linux\n\n" + GO, True),
    ("go operator changed", "go", GO, r(GO, "a + b", "a - b"), True),
    # ---- Java / C# / Rust ----
    ("java comment edited", "java", JAVA, r(JAVA, "// sum them", "// sum both"), False),
    ("java reformat", "java", JAVA, r(JAVA, "int total = a + b;", "int total=a+b;"), False),
    ("java operator changed", "java", JAVA, r(JAVA, "a + b", "a - b"), True),
    ("cs comment edited", "cs", CS, r(CS, "// sum them", "// sum both"), False),
    ("cs operator changed", "cs", CS, r(CS, "a + b", "a - b"), True),
    ("rs line comment edited", "rs", RS, r(RS, "// sum them", "// sum both"), False),
    ("rs doc comment edited", "rs", RS, r(RS, "/// Adds two numbers.", "/// Adds two i32s."), False),
    ("rs operator changed", "rs", RS, r(RS, "a + b", "a - b"), True),
]

VARIANTS = {
    "co+ic": ["--check-only", "--exit-code", "--ignore-comments"],
    "co": ["--check-only", "--exit-code"],
    "full+ic": ["--exit-code", "--ignore-comments"],
}


def difft(args, a, b):
    t = time.perf_counter()
    p = subprocess.run([DIFFT, *args, "--color=never", a, b],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    return p.returncode, (time.perf_counter() - t) * 1000, (p.stdout + p.stderr).strip()


def ast_same(before, after):
    try:
        return ast.dump(ast.parse(before)) == ast.dump(ast.parse(after))
    except SyntaxError:
        return None  # unparseable -> treat as a change


def verdict(changed, real):
    # changed=True means the classifier says "real change" (guard applies).
    if changed == real:
        return "ok"
    return "MISS(unsafe)" if real else "extra(safe)"


rows, times = [], []
for i, (name, ext, before, after, real) in enumerate(CASES):
    a = os.path.join(WORK, "c%02d_before.%s" % (i, ext))
    b = os.path.join(WORK, "c%02d_after.%s" % (i, ext))
    for path, text in ((a, before), (b, after)):
        with open(path, "w", encoding="utf-8", newline="") as f:
            f.write(text)
    row = [name, "REAL" if real else "cosmetic"]
    for v, args in VARIANTS.items():
        code, ms, out = difft(args, a, b)
        times.append(ms)
        if code not in (0, 1):
            row.append("ERR%d" % code)
            print("   [%s %s] exit %d: %s" % (name, v, code, out[:200]))
            continue
        row.append(verdict(code == 1, real))
        if v == "co+ic" and code == 1 and not real:
            row.append("") if False else None
    if ext == "py":
        s = ast_same(before, after)
        row.append(verdict(s is not True, real))
    else:
        row.append("-")
    rows.append(row)

hdr = ["case", "truth", *VARIANTS, "ast.dump"]
w = [max(len(str(x[j])) for x in rows + [hdr]) for j in range(len(hdr))]
for x in [hdr] + rows:
    print("  ".join(str(c).ljust(w[j]) for j, c in enumerate(x)))
times.sort()
print("\ndifft wall time per call: median %.0f ms, max %.0f ms (n=%d)"
      % (times[len(times) // 2], times[-1], len(times)))
for col in range(2, len(hdr)):
    miss = sum(1 for x in rows if x[col].startswith("MISS"))
    extra = sum(1 for x in rows if x[col].startswith("extra"))
    print("%-9s unsafe misses %d, safe extras %d" % (hdr[col], miss, extra))
