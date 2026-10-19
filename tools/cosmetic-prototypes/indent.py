"""Indentation-only semantic edits in Python: does difft --check-only see them?

Usage: python -I indent.py <path-to-difft> <work-dir>
"""
import ast
import os
import subprocess
import sys

DIFFT, WORK = sys.argv[1], sys.argv[2]
os.makedirs(WORK, exist_ok=True)

SRC = '''def f(items, flag):
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

# Each: (name, old line block, new line block) - every one changes behavior.
EDITS = [
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

print("%-22s %-10s %-10s %s" % ("edit", "co+ic", "co", "ast.dump"))
for i, (name, old, new) in enumerate(EDITS):
    assert SRC.count(old) == 1, name
    after = SRC.replace(old, new)
    a, b = os.path.join(WORK, "i%02d_a.py" % i), os.path.join(WORK, "i%02d_b.py" % i)
    for p, t in ((a, SRC), (b, after)):
        with open(p, "w", encoding="utf-8", newline="") as fh:
            fh.write(t)
    res = []
    for args in (["--check-only", "--exit-code", "--ignore-comments"],
                 ["--check-only", "--exit-code"]):
        c = subprocess.run([DIFFT, *args, a, b], capture_output=True).returncode
        res.append({0: "MISS", 1: "caught"}.get(c, "ERR%d" % c))
    try:
        same = ast.dump(ast.parse(SRC)) == ast.dump(ast.parse(after))
        res.append("MISS" if same else "caught")
    except SyntaxError:
        res.append("caught(syntax)")
    print("%-22s %-10s %-10s %s" % (name, *res))
