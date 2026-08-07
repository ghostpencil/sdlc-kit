# Review Lenses

Deep-dive lenses for slice review — plus one arc-scoped lens. This file is **not**
part of the per-slice read: `/end-slice` §4 points here conditionally, `/end-phase`'s
whole-arc review names the one arc-triggered lens (*the unconsumed artifact*), and
each lens names its own trigger. If no
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

## Lens: logging and swallowed errors

**Trigger:** the slice added or changed a catch/except, added a new failure path, or
added logging around one.

1. **Every new handler names where the signal goes.** For each catch this slice added:
   the error is re-raised, returned as an explicit error value, or logged at a level
   someone watches — and the handler can say which. A body of `pass`, a lone
   `log.debug`, or a silent default return is the finding: the failure still happens,
   only the evidence is deleted. This is *error propagation* point 2 made concrete —
   that lens asks what stopped being seen; this one asks where seeing now happens.
2. **The level is a routing decision, checked against the project's conventions**
   (`CLAUDE.md`, *Runtime Conventions*). ERROR claims someone should act; WARNING
   claims the system degraded and continued — and the code must be able to make its
   claim honestly, the same test the status-code rule applies. A failure logged below
   any level anyone watches is swallowed with a receipt.
3. **A log line at a failure point carries what its reader needs to act:** the
   operation, the identifying inputs (ids, paths, keys — never secrets or payloads),
   and the causing exception attached by the language's mechanism (`raise … from`,
   `exc_info`, cause-chaining) rather than flattened to a message. And the mirror
   bound: one failure, one ERROR — a failure re-logged at every layer it passes
   through reads as five incidents and buries the one line that had the context.

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

## Lens: shared state under concurrency

**Trigger:** the slice added or changed an object that outlives a request or is
reachable from more than one — a held connection, a cached client, a module-level
singleton, anything a handler keeps across calls.

**For every such object, name the runtime's concurrency model and state what
serializes access.** Not "is it thread-safe" — name the model (threading server, async
event loop, worker pool, single process) and the mechanism (a lock, a per-request
copy, a queue, the loop itself). "Nothing serializes access" is a legitimate answer
and it is the finding.

The specimen: a per-request retrieval object held **one** database connection and ran
four queries on it with no lock, under the stdlib threading HTTP server. Measured
against the real index: **410 of 600 concurrent selects returned the wrong question's
passages**, and 26 raised an error from column values crossing between queries — not
the database's own error type, so it escaped the narrow `except` and left the handler
with no response written at all. Two browser tabs is enough. Neither inline lens nor
either lens above can see this shape: it is not a changed consumer and not a
simplified double.

The measurement is half the lens. 410/600 is a measured consequence, where reviewers
have twice asserted CRITICAL on premises that turned out false — so a hit through this
lens is exercised concurrently (or otherwise reproduced) before it drives a fix,
severity read off the result rather than asserted.

## Lens: untrusted input

**Trigger:** the slice added or changed a place where outside data enters the process —
an HTTP/RPC handler, CLI argument, file or format parse, message consumer — or passes
such data onward to an interpreter.

1. **Name every interpreter the input reaches, and the mechanism that neutralizes it
   there.** SQL, a shell, a file path, a template, HTML, `eval`/deserialization — each
   hop named, each with its parameterization, escaping, or allowlist stated. Building
   the query or command by string assembly from input **is** the finding even when
   today's callers look safe: the review question is the mechanism, not the current
   values.
2. **A path built from input is canonicalized and prefix-checked before use.** Resolve
   first (realpath or the language's equivalent — `..`, absolute segments, and symlinks
   all fold in), then check the *result* sits under the intended root. Checking the raw
   string is the classic near-miss: it passes every test written against strings.
3. **Deserializers that can execute are not for untrusted data.** `pickle`,
   `yaml.load` without a safe loader, native object serialization, `eval` of any
   dialect: if the slice feeds one from outside the process, the fix is a different
   format, not a sanitizer in front of this one.

## Lens: secrets and exposure

**Trigger:** the slice touched credentials, tokens, or their configuration; added or
changed an externally reachable surface (endpoint, port, webhook, a CLI that runs
remote input); or added logging or error output near either.

1. **A secret has exactly one home** — the project's configured secret source — and
   appears in no code, no committed config, no default value, and no log line. The
   indirect paths are the ones that ship: an exception message embedding a connection
   string, a debug line dumping a config object whose repr includes the key.
2. **A new surface names who may call it and what enforces that.** "Internal-only"
   names the control that makes it internal — a network rule, auth middleware — as it
   is configured where the code will actually run, not the intention. A surface
   nobody restricted is public, whatever the docstring says.
3. **Error output to a caller is a disclosure decision.** Stack traces, raw queries,
   internal paths, and dependency versions go to the log; the caller gets the honest
   claim (*error propagation* point 3) plus an opaque reference to correlate with it.

Provenance note: the three lenses above (logging and swallowed errors, untrusted
input, secrets and exposure) shipped as standards in kit 0.13.0 rather than from a
measured field catch. The caveat on *error propagation* applies to them doubly:
lenses to look through, not defect-rate claims.

## Lens: the unconsumed artifact

**Trigger:** the arc introduced a new artifact — an entity or table/column, an
endpoint, a config key, a public method or factory — and this is the **whole-arc**
review (`/end-phase`), where everything the arc built is finally visible at once.

1. **Every new artifact names its consumer.** For each one, point at the production
   code that reads, calls, or renders it. "It will be used next phase" is an
   acceptable answer only when said out loud — it converts the artifact into a
   deferred-backlog entry with a phase pointer instead of silent inventory.
2. **A record-shaped artifact needs a writer AND a reader in production.** An entity
   persisted by nothing, or a column seeded once and never queried, passes every test
   that constructs it directly; only this question notices that the running system
   cannot produce or cannot see it.
3. **A public API only tests call is not public API.** A constructor overload or
   factory variant whose sole callers are tests manufactures states production cannot
   reach — the test double drifts from reality through the door it opened.

"No consumer" is a search-absence claim, so the *verify the denominator* lens applies
to the search that establishes it: say how consumers were enumerated, and remember
that on stacks wiring consumers by annotation, reflection, or configuration, a
caller-grep undercounts — a framework-wired reader is a consumer the grep never sees.

Provenance: a whole-tree audit of one adoption (2026-08-06, two merged phases) found
three in a ~55-class codebase — a status entity+repository with no production writer,
a seeded endpoint-URL column whose accessor did not exist, and result-factory
overloads only tests called. Slice reviews see changed paths; none of the three ever
appeared as a *changed* path.
