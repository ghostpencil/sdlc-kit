#!/usr/bin/env python
"""Re-runnable proof for the skill-activation ledger hook, both dialects.

Drives the Copilot hook body (templates/skill-ledger.template.json) and the Claude Code
"Skill" block (templates/settings.template.json) with payload shapes measured on the
bench 2026-08-07 (FEATURE_PLAN.md 37.3 probes P1/P2) rather than invented ones. Every
silent case is also run dirty, so silence means something: the loud no-root branch is
exercised in each dialect, and the append is proven to end in a newline - the measured
payloads do not, and a ledger written without one becomes a single unparseable line.

Kit-development artifact: lives at the root, never ships inside sdlc-kit/ (invariant 12).
Run from anywhere:  python tools/skill-ledger-check.py
"""
import io, json, os, re, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPILOT_TPL = os.path.join(REPO, "sdlc-kit", "templates", "skill-ledger.template.json")
CLAUDE_TPL = os.path.join(REPO, "sdlc-kit", "templates", "settings.template.json")

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
    cla = json.load(io.open(CLAUDE_TPL, encoding="utf-8"))
    blocks = [b for b in cla["hooks"]["PostToolUse"] if b.get("matcher") == "Skill"]
    assert len(blocks) == 1, "settings template must carry exactly one Skill block"
    return entry["bash"], blocks[0]["hooks"][0]["command"]


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


def main():
    cop_body, cla_body = load_bodies()
    base = tempfile.mkdtemp(prefix="sldg-")
    repo = os.path.join(base, "proj")
    os.makedirs(os.path.join(repo, ".git"))
    fwd = repo.replace("\\", "/")

    # -- Copilot dialect --------------------------------------------------------
    # The body must stay free of backslashes: a hook body crosses the Windows-to-WSL
    # launcher boundary when the CLI was started from a shell whose PATH resolves bash
    # to the WSL launcher, and that boundary re-parses the command line - measured
    # 2026-08-07, it corrupted every backslash-carrying body it was given. The ledger
    # therefore keys on the hook process cwd (measured: the session cwd, in the
    # executing shell's own path flavour) rather than parsing the payload for a root.
    case("copilot: body carries no backslash to be eaten at the WSL launcher boundary",
         "\\" not in cop_body, cop_body)
    pay = copilot_payload(repo)  # backslashed Windows cwd, as measured
    rc, err = run(cop_body, pay, cwd=repo)
    lines = io.open(ledger_of(repo), encoding="utf-8").read() if os.path.exists(ledger_of(repo)) else ""
    case("copilot: activation at repo root appends a line, exit 0", rc == 0 and lines != "", "rc=%s err=%s" % (rc, err))
    case("copilot: line is ISO-stamped and carries the payload verbatim",
         bool(ISO_LINE.match(lines)) and pay in lines, lines[:120])
    case("copilot: appended line ends in a newline", lines.endswith("\n"), repr(lines[-20:]))
    rc, err = run(cop_body, copilot_payload(fwd), cwd=repo)
    n = io.open(ledger_of(repo), encoding="utf-8").read().count("\n")
    case("copilot: second activation is a second line, not a concatenation", rc == 0 and n == 2, "n=%s" % n)
    nogit = os.path.join(base, "nogit"); os.makedirs(nogit)
    rc, err = run(cop_body, copilot_payload(nogit), cwd=nogit)
    case("copilot: a hook shell not at the repo root is LOUD - stderr + nonzero, nothing written",
         rc != 0 and "did NOT record" in err and not os.path.exists(ledger_of(nogit)), "rc=%s err=%s" % (rc, err))

    # -- Claude Code dialect ----------------------------------------------------
    repo2 = os.path.join(base, "proj2")
    os.makedirs(os.path.join(repo2, ".git"))
    pay2 = claude_payload(repo2)
    rc, err = run(cla_body, pay2, env_extra={"CLAUDE_PROJECT_DIR": repo2})
    lines2 = io.open(ledger_of(repo2), encoding="utf-8").read() if os.path.exists(ledger_of(repo2)) else ""
    case("claude: valid payload appends an ISO-stamped line, exit 0",
         rc == 0 and bool(ISO_LINE.match(lines2)) and pay2 in lines2 and lines2.endswith("\n"),
         "rc=%s err=%s" % (rc, err))
    rc, err = run(cla_body, pay2, env_extra={"CLAUDE_PROJECT_DIR": repo2})
    n = io.open(ledger_of(repo2), encoding="utf-8").read().count("\n")
    case("claude: second activation is a second line", rc == 0 and n == 2, "n=%s" % n)
    rc, err = run(cla_body, pay2)  # CLAUDE_PROJECT_DIR unset
    case("claude: unset CLAUDE_PROJECT_DIR is LOUD - stderr + exit 2",
         rc == 2 and "did NOT record" in err, "rc=%s err=%s" % (rc, err))
    rc, err = run(cla_body, pay2, env_extra={"CLAUDE_PROJECT_DIR": nogit})
    case("claude: CLAUDE_PROJECT_DIR without .git is LOUD - exit 2",
         rc == 2 and "did NOT record" in err, "rc=%s" % rc)

    failed = [r for r in results if not r[1]]
    print("\n%d cases, %d failed" % (len(results), len(failed)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
