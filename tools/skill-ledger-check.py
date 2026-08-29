#!/usr/bin/env python
"""Re-runnable proof for the skill-activation ledger hook, both dialects.

Drives the Copilot hook body (templates/skill-ledger.template.json) and the Claude Code
body (templates/skill-ledger-claude.template.sh) with payload shapes measured on the
bench 2026-08-07 (FEATURE_PLAN.md 37.3 probes P1/P2) rather than invented ones. Every
silent case is also run dirty, so silence means something: the loud no-root branch is
exercised in each dialect, and the append is proven to end in a newline - the measured
payloads do not, and a ledger written without one becomes a single unparseable line.

The Claude body is read from its OWN template, never from the "Skill" block in
templates/settings.template.json - split 2026-08-15 (FEATURE_PLAN.md 61), which left
that block holding a bare launcher line. Through 0.29.0 this suite still ran the
launcher string as the body: rc=127, then an uncaught FileNotFoundError aborted the run
and took the three Claude cases after it, so one dialect of one control was unexercised
for six releases (FEATURE_PLAN.md 75). The wiring cases below pin the split in both
directions - the block must hold the bare launcher, and the launcher must name the file
sdlc-setup.md installs - so it cannot silently reverse. This is the same repair
gate-hook-check.py took for the same reason; that suite is the sibling, and it was the
only other one reading settings.template.json for a body.

Kit-development artifact: lives at the root, never ships inside sdlc-kit/ (invariant 12).
Run from anywhere:  python tools/skill-ledger-check.py
"""
import io, json, os, re, subprocess, sys, tempfile, traceback

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPILOT_TPL = os.path.join(REPO, "sdlc-kit", "templates", "skill-ledger.template.json")
CLAUDE_TPL = os.path.join(REPO, "sdlc-kit", "templates", "settings.template.json")
CLAUDE_SH_TPL = os.path.join(REPO, "sdlc-kit", "templates", "skill-ledger-claude.template.sh")
SETUP_MD = os.path.join(REPO, "sdlc-kit", "commands", "sdlc-setup.md")
LAUNCHER = "sh .github/hooks/sdlc-skill-ledger.sh"

ISO_LINE = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z ")

# Payload shapes as captured on the bench (Copilot 1.0.78) and from a live Claude Code
# session, 2026-08-07. Neither ends with a newline - that fact is part of the fixture.
# Compact separators, because the wire format is compact: the prelude's sed keys on
# '"cwd":"' with no space, and a pretty-printed fixture would test a payload the CLI
# never sends (first run of this suite proved exactly that, the useful way).
def copilot_payload(cwd):
    return json.dumps({
        "sessionId": "c0f41498-6038-4534-89bf-1db2bde3275e",
        "timestamp": 1786116785190,
        "cwd": cwd,
        "toolName": "skill",
        "toolArgs": "{\"skill\":\"p1-probe-skill\"}",
        "toolResult": {"resultType": "success", "textResultForLlm": "Skill loaded."},
    }, separators=(",", ":"))

def claude_payload(cwd):
    return json.dumps({
        "session_id": "80c28ecb-041b-4269-b13c-187bc100d7d5",
        "cwd": cwd,
        "hook_event_name": "PostToolUse",
        "tool_name": "Skill",
        "tool_input": {"skill": "p2-probe-skill"},
        "tool_response": {"success": True, "commandName": "p2-probe-skill"},
    }, separators=(",", ":"))


def load_bodies():
    cop = json.load(io.open(COPILOT_TPL, encoding="utf-8"))
    entry = cop["hooks"]["postToolUse"][0]
    assert entry["matcher"] == "skill", "Copilot matcher must be the measured tool name"
    # Claude: the BODY comes from its own template; the settings block is only wiring,
    # and the wiring is checked as wiring by claude_wiring() below.
    return entry["bash"], io.open(CLAUDE_SH_TPL, encoding="utf-8", newline="").read()


def claude_launcher_command():
    """The "Skill" block's command, located by matcher and never by array index."""
    cla = json.load(io.open(CLAUDE_TPL, encoding="utf-8"))
    blocks = [b for b in cla["hooks"]["PostToolUse"] if b.get("matcher") == "Skill"]
    assert len(blocks) == 1, "settings template must carry exactly one Skill block"
    return blocks[0]["hooks"][0]["command"]


def run(body, payload, env_extra=None, cwd=None):
    env = dict(os.environ)
    env.pop("CLAUDE_PROJECT_DIR", None)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(["sh", "-c", body], input=payload.encode("utf-8"),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                       env=env, cwd=cwd or REPO)
    return p.returncode, p.stderr.decode("utf-8", "replace")


results = []

def case(name, ok, detail=""):
    results.append((name, ok, detail))
    print(("PASS  " if ok else "FAIL  ") + name + (("  - " + detail) if (detail and not ok) else ""))


def ledger_of(root):
    return os.path.join(root, ".git", "sdlc-skill-ledger.jsonl")


def read_ledger(root):
    """The ledger as written, or "" when the hook wrote nothing.

    A missing file is a VERDICT here, never an exception: reading it unguarded is what
    turned one failing case into an aborted run in 0.24.0-0.29.0 (FEATURE_PLAN.md 75.1).
    """
    path = ledger_of(root)
    return io.open(path, encoding="utf-8").read() if os.path.exists(path) else ""


def guarded(label, default, fn, *a, **kw):
    """Run one pass; an unexpected exception REPORTS and the run continues.

    A crash used to end the run where it happened, and every case after it never ran -
    and never printed, so the loss did not show up in the output at all. That is how
    this suite silently lost three cases for six releases (FEATURE_PLAN.md 75; the rule
    is 75.7 ruling 3, generalized to all six suites, and this file is where it was
    found). Correctness failures still fail; what they may no longer do is delete the
    coverage that follows them. `default` is what the caller unpacks when the pass
    crashed, and guarded.crashed carries the run's exit code obligation.
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


def copilot_suite(cop_body, base, repo):
    # The body must stay free of backslashes: a hook body crosses the Windows-to-WSL
    # launcher boundary when the CLI was started from a shell whose PATH resolves bash
    # to the WSL launcher, and that boundary re-parses the command line - measured
    # 2026-08-07, it corrupted every backslash-carrying body it was given. The ledger
    # therefore keys on the hook process cwd (measured: the session cwd, in the
    # executing shell's own path flavour) rather than parsing the payload for a root.
    case("copilot: body carries no backslash to be eaten at the WSL launcher boundary",
         "\\" not in cop_body, cop_body)
    fwd = repo.replace("\\", "/")
    pay = copilot_payload(repo)  # backslashed Windows cwd, as measured
    rc, err = run(cop_body, pay, cwd=repo)
    lines = read_ledger(repo)
    case("copilot: activation at repo root appends a line, exit 0", rc == 0 and lines != "", "rc=%s err=%s" % (rc, err))
    case("copilot: line is ISO-stamped and carries the payload verbatim",
         bool(ISO_LINE.match(lines)) and pay in lines, lines[:120])
    case("copilot: appended line ends in a newline", lines.endswith("\n"), repr(lines[-20:]))
    rc, err = run(cop_body, copilot_payload(fwd), cwd=repo)
    n = read_ledger(repo).count("\n")
    case("copilot: second activation is a second line, not a concatenation", rc == 0 and n == 2, "n=%s" % n)
    nogit = os.path.join(base, "nogit"); os.makedirs(nogit)
    rc, err = run(cop_body, copilot_payload(nogit), cwd=nogit)
    case("copilot: a hook shell not at the repo root is LOUD - stderr + nonzero, nothing written",
         rc != 0 and "did NOT record" in err and not os.path.exists(ledger_of(nogit)), "rc=%s err=%s" % (rc, err))


def claude_wiring():
    """The launcher split, pinned in both directions.

    The block must hold the bare launcher (so a future edit cannot quietly move a body
    back into settings.template.json, which is what this suite would then have run), and
    the launcher must name the file setup actually installs (so the launcher itself is
    under test rather than merely unused). gate-hook-check.py pins the first half for
    both of its hooks; the ledger's own proof should not have to borrow it.
    """
    cmd = claude_launcher_command()
    case("claude: the Skill block holds the bare launcher, not a hook body "
         "(the 0.24.0 split, pinned so it cannot reverse)", cmd == LAUNCHER, repr(cmd))
    installed = LAUNCHER.split(" ", 1)[1]          # .github/hooks/sdlc-skill-ledger.sh
    setup = io.open(SETUP_MD, encoding="utf-8").read()
    tpl = os.path.basename(CLAUDE_SH_TPL)
    i = setup.find(tpl)
    window = setup[i:i + 240] if i >= 0 else ""
    case("claude: the launcher names the path sdlc-setup.md installs the body to",
         i >= 0 and installed in window,
         "mapping %s -> %s not found in sdlc-setup.md" % (tpl, installed))


def claude_suite(cla_body, base):
    repo2 = os.path.join(base, "proj2")
    os.makedirs(os.path.join(repo2, ".git"))
    nogit = os.path.join(base, "nogit2"); os.makedirs(nogit)
    pay2 = claude_payload(repo2)
    rc, err = run(cla_body, pay2, env_extra={"CLAUDE_PROJECT_DIR": repo2})
    lines2 = read_ledger(repo2)
    case("claude: valid payload appends an ISO-stamped line, exit 0",
         rc == 0 and bool(ISO_LINE.match(lines2)) and pay2 in lines2 and lines2.endswith("\n"),
         "rc=%s err=%s" % (rc, err))
    rc, err = run(cla_body, pay2, env_extra={"CLAUDE_PROJECT_DIR": repo2})
    n = read_ledger(repo2).count("\n")
    case("claude: second activation is a second line", rc == 0 and n == 2, "n=%s" % n)
    rc, err = run(cla_body, pay2)  # CLAUDE_PROJECT_DIR unset
    case("claude: unset CLAUDE_PROJECT_DIR is LOUD - stderr + exit 2",
         rc == 2 and "did NOT record" in err, "rc=%s err=%s" % (rc, err))
    rc, err = run(cla_body, pay2, env_extra={"CLAUDE_PROJECT_DIR": nogit})
    case("claude: CLAUDE_PROJECT_DIR without .git is LOUD - exit 2",
         rc == 2 and "did NOT record" in err, "rc=%s" % rc)


def main():
    try:
        cop_body, cla_body = load_bodies()
    except Exception:
        traceback.print_exc()
        print("\nCANNOT RUN: neither dialect could be loaded - nothing below was proven")
        return 2

    base = tempfile.mkdtemp(prefix="sldg-")
    repo = os.path.join(base, "proj")
    os.makedirs(os.path.join(repo, ".git"))

    guarded("copilot", None, copilot_suite, cop_body, base, repo)
    guarded("claude wiring", None, claude_wiring)
    guarded("claude", None, claude_suite, cla_body, base)

    failed = [r for r in results if not r[1]]
    if guarded.crashed:
        print("\nCRASHED passes: %s - those cases did not run"
              % ", ".join(guarded.crashed))
    print("\n%d cases, %d failed" % (len(results), len(failed)))
    return 1 if (failed or guarded.crashed) else 0


if __name__ == "__main__":
    sys.exit(main())
