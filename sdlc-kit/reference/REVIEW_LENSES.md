# Review Lenses

Deep-dive lenses for slice review. This file is **not** part of the per-slice read:
`/end-slice` §3 points here conditionally, and each lens names its own trigger. If no
trigger matches the slice, close this file — reading it "just in case" is the context
bloat the pointer exists to avoid.

Unlike the rest of `reference/`, this file is **installed** into `.claude/commands/` by
`/sdlc-setup`, so the pointer resolves in every adopted project even after the kit
folder is removed. It is kit-owned and tracks upstream like the commands.

---

## Lens: error propagation

**Trigger:** the slice added or removed a raise, changed exception handling, or changed
an error status code.

1. **Making a call raise is not done when the raise is correct — it is done when every
   caller's control flow has been re-read.** A new exception travels; the unit of review
   is the set of callers, not the raising line.
2. **The mirror question: when you stop something from raising, ask *what did I stop
   seeing?* — not just *who now crashes?*** Handling an error deletes a signal; name
   what the signal was and where it goes now.
3. **A status code is a claim about fault.** 4xx claims the caller is wrong; 5xx claims
   the service is. Check the code can honestly make its claim: a handler that returns
   400 while parsing data read from its own database blames a perfectly valid request
   whenever the *stored* data is corrupt.

Caveat: on the project that surfaced this lens it went 3-for-3 — but during a
STABILIZATION phase, which is by definition when swallowed errors get fixed. It is a
lens to look through, not a claim about universal defect rates.

## Lens: verify the denominator

**Trigger:** the slice swept the codebase for a pattern (an audit, a bulk fix, a
"find all X" pass) — or wrote a script or check whose output will be trusted.

**When auditing a pattern, enumerate by symbol or structure and verify the denominator.**
A textual match undercounts, and the sweep then reports success against the wrong total.
The sweep that named this lens matched `except duckdb.Error:` literally, missed seven
sites written `except (duckdb.Error, ValueError, TypeError):`, and reported found-26,
fixed-26 — no error, no signal, wrong denominator.

The failure mode is sharper than a miscount, and it hit the kit's own verification
tooling three times in one session. In each case the check returned a **plausible
answer**, so nothing prompted a second look:

- A drift check hashed the working tree instead of committed content. On a Windows
  checkout without pinned line endings it reported *every* file as drifted — a
  clean-looking, uniformly wrong result.
- A script probed for a path's existence with `git cat-file … | sha256sum`. A pipeline
  reports the *last* command's status, so missing paths hashed empty input and silently
  "matched": seven files classified against paths that do not exist.
- A coverage check matched template placeholders to setup questions by literal name.
  Most are asked for semantically, so it reported 24 of 32 as unasked — false positives
  that "fixing" would have meant adding 24 redundant questions.

Two rules fall out:

1. **Count the population independently of the match.** The audit must show that the
   number of sites it *examined* equals the number that *exist*, established by a second
   route (symbol search, structural listing, `wc -l` of an independent enumeration) —
   not by the pattern that did the finding.
2. **A check is only trustworthy once it has been made to disagree.** Feed it a case it
   must flag and watch it flag that case and only that case. "All clean" from a checker
   that has never failed is indistinguishable from "all clean" from a broken one.

Both apply to verification code with extra force: a wrong audit script does not error —
it succeeds at the wrong task.
