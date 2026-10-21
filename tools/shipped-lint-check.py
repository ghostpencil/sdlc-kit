# -*- coding: utf-8 -*-
"""Re-runnable proof that every Python file the kit ships passes a stock linter.

Why it exists: 0.34.0 shipped .github/hooks/sdlc-cosmetic.py with three ruff E741
findings (a loop variable named `l`) and a comment ruff read as a malformed `noqa`. No
kit suite ran a linter over the shipped hooks; the first adopter whose own gate lints
.github/hooks/ went red on updating, and the fix became 0.34.1 (FEATURE_PLAN.md 82.10).
A file copied verbatim into an adopter's tree is linted by the adopter's gate, so the
kit has to pass a default configuration before it ships, not after.

Two passes:

  1. a lint pass over `git ls-files sdlc-kit '*.py'` - the population is enumerated,
     never listed here, so a newly shipped .py is covered the day it lands. Each file is
     linted as an adopter holds it: a template's {{PLACEHOLDER}}s are resolved with the
     recipe's own Python row first (an unresolvable one fails the case, loudly). ruff
     runs with --isolated - its defaults, none of this repo's config - and a ruff
     WARNING fails the case too, because an adopter sees it on every lint run;
  2. a mutation pass that plants each defect class this suite exists to catch into a
     copy of a shipped file and requires pass 1 to notice it.

Needs ruff (`python -m ruff`); without it the run reports SKIPPED and exits 1 as
INCOMPLETE - an unrun proof is not a passing one.

Kit-development artifact: lives at the root, never ships inside sdlc-kit/.
Run from anywhere:  python tools/shipped-lint-check.py
"""

import os
import re
import subprocess
import sys
import tempfile
import traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The recipe's Python row (GATE_RECIPES.md, the per-language table) plus its source
# glob - the values setup would write into an instantiated guard on a Python project.
VALUES = {
    "TEST_PATH_PATTERN": "tests/*|test_*.py|*_test.py",
    "SOURCE_GLOB": "*.py",
    "TEST_CMD_PATTERN": "*pytest*",
    "TEST_REPORT_PATTERN": "=+ (FAILURES|ERRORS) =+",
    "GUARD_EXEMPT_PATTERN": "*.config.*|.*|tools/*",
}


def guarded(label, default, fn, *a, **kw):
    """Run one pass; an unexpected exception REPORTS and the run continues
    (FEATURE_PLAN.md 75.7 ruling 3, the rule every kit suite carries)."""
    try:
        return fn(*a, **kw)
    except Exception:
        traceback.print_exc()
        print("CRASHED  %s  <-- pass did not complete; its remaining cases did not run"
              % label)
        guarded.crashed.append(label)
        return default


guarded.crashed = []


def shipped():
    out = subprocess.run(["git", "-C", REPO, "ls-files", "sdlc-kit"], capture_output=True,
                         text=True, check=True).stdout.split()
    return sorted(p for p in out if p.endswith(".py"))


def ruff_available():
    try:
        return subprocess.run([sys.executable, "-m", "ruff", "--version"],
                              capture_output=True).returncode == 0
    except OSError:
        return False


def lint_text(text, name, where):
    """Lint one file's text as an adopter holds it. -> list of problems (empty = clean)."""
    left = set(re.findall(r"\{\{(\w+)\}\}", text)) - set(VALUES)
    if left:
        return ["unresolvable placeholder(s): %s" % ", ".join(sorted(left))]
    for k, v in VALUES.items():
        text = text.replace("{{%s}}" % k, v)
    path = os.path.join(where, os.path.basename(name).replace(".template", ""))
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)
    p = subprocess.run([sys.executable, "-m", "ruff", "check", "--isolated", "--no-cache",
                        "--output-format", "concise", path], capture_output=True, text=True,
                       cwd=where)
    problems = []
    if p.returncode != 0:
        problems += [ln for ln in p.stdout.splitlines() if ln.strip() and "Found " not in ln]
        problems = problems or ["ruff exit %d" % p.returncode]
    problems += ["ruff " + ln.strip() for ln in p.stderr.splitlines()
                 if "warning" in ln.lower()]
    return problems


def lint_pass(files, transform=None, verbose=True):
    """-> failed file names. `transform(name, text)` lets the mutation pass plant a defect."""
    failed = []
    where = tempfile.mkdtemp(prefix="shipped-lint-")
    for name in files:
        with open(os.path.join(REPO, name), encoding="utf-8", newline="") as f:
            text = f.read()
        if transform:
            text = transform(name, text)
        problems = lint_text(text, name, where)
        if problems:
            failed.append(name)
        if verbose:
            print(("PASS  " if not problems else "FAIL  ") + name)
            for pr in problems:
                print("        " + pr)
    return failed


def _append(snippet):
    return lambda name, text: text + snippet


# Each plants one defect class into every shipped file; pass 1 must fail on each.
MUTATIONS = [
    ("an ambiguous name (E741 - the 0.34.0 defect)", _append("\n\nl = 1\n")),
    ("an unused import (F401)", _append("\n\nimport this_module_is_unused  # planted\n")),
    ("a comment ruff reads as a malformed noqa (the 0.34.0 warning)",
     _append("\n\n# so `#noqa` and `# noqa` are one directive\n")),
    ("a syntax error (E999 - a file the adopter's python cannot import)",
     _append("\n\ndef broken(:\n    pass\n")),
    ("a placeholder this suite cannot resolve (an unseen template value)",
     _append('\n\nNEW_VALUE = "{{NOT_A_KNOWN_PLACEHOLDER}}"\n')),
]


# The real thing, not a plant: the classifier exactly as 0.34.0 shipped it. If this
# lints clean, the suite has stopped catching the defect it was written for.
SPECIMEN = ("v0.34.0", "sdlc-kit/templates/sdlc-cosmetic.template.py")


def specimen_caught():
    tag, path = SPECIMEN
    text = subprocess.run(["git", "-C", REPO, "show", "%s:%s" % (tag, path)],
                          capture_output=True, text=True, encoding="utf-8",
                          check=True).stdout
    problems = lint_text(text, path, tempfile.mkdtemp(prefix="shipped-lint-"))
    print("%s  the %s classifier, as shipped (%d problems)"
          % ("caught  " if problems else "SURVIVED", tag, len(problems)))
    return bool(problems)


def mutation_pass(files, verbose=True):
    survived = [] if specimen_caught() else ["the %s specimen" % SPECIMEN[0]]
    for label, transform in MUTATIONS:
        failed = lint_pass(files, transform, verbose=False)
        caught = len(failed) == len(files)
        print("%s  %s (%d/%d files)" % ("caught  " if caught else "SURVIVED", label,
                                        len(failed), len(files)))
        if not caught:
            survived.append(label)
    return survived


def main():
    files = shipped()
    print("== shipped Python files: %d (git ls-files sdlc-kit '*.py') ==" % len(files))
    if not files:
        print("FAIL  no shipped .py file found - the enumeration is broken, not clean")
        return 1
    if not ruff_available():
        print("SKIPPED  ruff is not installed (python -m ruff) - INCOMPLETE, not green")
        return 1
    print(subprocess.run([sys.executable, "-m", "ruff", "--version"], capture_output=True,
                         text=True).stdout.strip())

    print("\n== lint pass ==")
    failed = guarded("lint pass", ["(crashed)"], lint_pass, files)
    if failed:
        print("\nFAILED: %s - an adopter whose gate lints .github/hooks/ goes red on these"
              % ", ".join(failed))
        return 1

    print("\n== mutation pass (%d mutations) ==" % len(MUTATIONS))
    survived = guarded("mutation pass", ["(crashed)"], mutation_pass, files)
    if survived:
        print("\nMUTATIONS SURVIVED: %s - the lint pass does not catch what it claims"
              % ", ".join(survived))
        return 1

    if guarded.crashed:
        print("\nCRASHED passes: %s - those cases did not run" % ", ".join(guarded.crashed))
        return 1
    print("\nall green: %d files, %d mutations caught" % (len(files), len(MUTATIONS)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
