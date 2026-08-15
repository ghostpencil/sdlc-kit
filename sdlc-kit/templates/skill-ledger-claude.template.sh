#!/bin/sh
# SDLC skill-activation ledger, Claude Code dialect - the hook BODY for the
# "Skill"-matcher PostToolUse block, which is a bare launcher
# (`sh .github/hooks/sdlc-skill-ledger.sh`) for the same measured reason as the
# gate hook's split (see claude-gate.template.sh: the per-hook "shell" pin was
# measured never firing on Claude Code 2.1.231, 2026-08-15). No placeholders -
# installed as-is when the ledger offer is accepted; setup removes the settings
# block AND does not install this file on a decline (the record of the decline
# lives in spec/SDLC.md, never here). Appends one line per tool-dispatched skill
# activation to .git/sdlc-skill-ledger.jsonl, and is LOUD when it cannot write.
i=$(cat); if [ -z "$CLAUDE_PROJECT_DIR" ] || [ ! -d "$CLAUDE_PROJECT_DIR/.git" ]; then echo "SDLC skill ledger did NOT record this activation: CLAUDE_PROJECT_DIR is unset or is not the repo root." >&2; exit 2; fi; printf '%s %s\n' "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "$i" >> "$CLAUDE_PROJECT_DIR/.git/sdlc-skill-ledger.jsonl"
