# {{PROJECT_NAME}} — Testing & TDD Protocol

Read this file fresh before every TDD-skill invocation. Do not rely on memory.

## The Vertical Slicing Mandate

**We follow a strict "Tracer Bullet" TDD workflow. Horizontal bulk-testing is prohibited.**

Do not write all tests for a module at once. Follow the **Red-Green-Refactor** loop for
one behavior at a time:

1. **Identify a Public Behavior:** Pick one specific capability from the current slice's
   exit criteria.
2. **RED:** Write **one** test targeting the public interface — then **run it and
   observe it fail.** The failing run is the evidence that the test can fail; a red
   never seen proves nothing about the green that follows. Record the observation as it
   happens — the exact test command, the failing test's line, the exit code — because
   an observed red cannot be reconstructed at close-out; `/end-slice` carries the
   record into the slice commit body.
3. **GREEN:** Implement the **minimal** application code required to pass that specific test.
4. **REFACTOR:** Clean the code while ensuring the test stays green.
5. **REPEAT:** Move to the next behavior.

---

## Test File Layout & Build Order

{{TEST_LAYOUT}}
<!-- State the convention concretely, e.g.:
     "Unit tests mirror the application package: tests/unit/<package>/test_<module>.py"
     or "Colocated: src/foo/bar.ts → src/foo/bar.test.ts".
     Existing Project mode: document the layout the project ACTUALLY uses. -->

**Build order is defined per phase in the phase spec's slice plan** — pure
models/domain logic first, persistence next, services, external-system seams, then
integration/wiring, and the user-facing surface last. Do not invent a global priority
order; follow the current phase's slices.

Run the suite with: `{{GATE_TEST_CMD}}`

---

## Strategy by Layer

{{LAYER_STRATEGY}}
<!-- One short subsection per architectural layer: what behavior the tests pin, and the
     protocol (real objects vs. what must be faked and at which seam). Examples:

     ### Domain / data layer
     * Behavior focus: data round-trips, invariants, validation.
     * Protocol: no mocking. Real objects + a temp dir / in-memory store.

     ### External services (APIs, LLMs, payment providers)
     * Behavior focus: our code assembles correct requests and handles errors.
     * Protocol: never call the real service in unit tests. The service is injected at a
       constructor seam — inject a fake there and assert on what our code hands it.
       Do not patch the vendor SDK inside feature tests; SDK-level patching belongs only
       in the adapter's own unit tests, where the adapter IS the unit.

     ### UI / rendering
     * Behavior focus: correct state → correct render/draw/DOM calls.
     * Protocol: fake only the layer that needs a display/GPU/browser. -->

---

## Mock Policy — Use Real Objects Whenever Possible

**Default: no mocks.** Only introduce a mock when a real component cannot run in the
test environment. If you find yourself mocking an internal application class, stop and
ask whether the real class can be used instead.

### When mocking is mandatory

| What | Why |
| :--- | :--- |
{{MANDATORY_MOCK_ROWS}}
<!-- Fill with this project's genuinely un-runnable dependencies, e.g.:
     | GPU/display rendering calls | needs a display context |
     | OS dialogs / blocking prompts | block the process waiting for input |
     | External network APIs | non-deterministic; slow; costs money |
     | System clock / randomness (where determinism matters) | flaky tests | -->

### When mocking is wrong

If a real object can be constructed — even awkwardly — **use it**. Mocking internal
application components means your test only verifies that one object calls a method on
a mock; it does not verify that the two real objects actually work together. Wiring
bugs live exactly where the mock is.

### When a double stands in, it must be as complicated as the truth

A double that replaces production code must reproduce its **side effects and its error
surface**, or the test must drive the real thing. A double that skips a side effect
(the flag production sets before raising; the state a write mutates) makes every
behavior depending on that effect *simulated everywhere and produced nowhere* — the
defect becomes structurally unreachable in tests while the suite stays green. The same
for errors: a hand-built exception one field simpler than the real one (no filename on
an `OSError`) tests a failure shape production never produces. Both halves of this rule
were paid for in one arc: a recorder that dropped one flag assignment hid a live
production bug through four reviews, and a bare `PermissionError` hid a path-disclosure
leak. Review asks it directly: *does any double omit a side effect or simplify the
error surface of what it replaces?*

### Skip discipline

A test must **fail**, not skip, when a tool or stand-in it requires is absent.
Conditional skip is the default idiom in most frameworks, which makes it the easy wrong
answer — a silently-skipped test is coverage that reads as present and is not, the same
false green as a test that quietly reached the real service. A legitimate skip
(platform-specific behavior on the other platform) is declared and visible in the run
summary, never silent.

---

## Test Isolation — Enforced, Not Promised

**Partial isolation is worse than none, because it reads as complete.** A mock policy
that lives only in prose will be violated, and the violation will not be visible: the
suite stays green while tests quietly reach something real. Isolation is therefore
enforced by a harness, and each check is trusted only because it has been made to fail.

The checks (specified by the kit; implemented for this stack by `/sdlc-setup`):

1. **Outbound network is blocked.** A test that opens a real connection fails loudly,
   naming the address it tried to reach.
2. **Credentials are unreachable.** Credential env vars are cleared and credential file
   paths point at nonexistent locations — a test that slips past a mock seam must be
   unable to authenticate as a side effect.
3. **Every home/data-dir seam is isolated** — config dirs, caches, state files, not
   just the obvious one. Enumerate the seams; sterilizing one env var and stopping is
   exactly the partial isolation the headline rule warns about.

### What a test may assert about errors

- **A test asserting "returns empty on error" is usually pinning a bug, not a
  behavior.** Prefer asserting that the error propagates. The rule's origin was a
  production outage: a missing dependency swallowed by `except SomeError: return []` —
  a mocked DB would have returned rows happily and kept the suite green through the
  entire outage. The same goes for asserting on an error's message string when its
  *type* and *propagation* are the behavior.
- **Check a new invariant against what the system already does, not against what
  sounds right.** A review-written test once asserted "no audit row on rejection" when
  the audit layer already recorded rejections as `action="fail"` — the test would have
  made one event produce two different histories.

### This project's harness

{{ISOLATION_HARNESS}}
<!-- Filled by /sdlc-setup: where the harness lives, what each check covers, and the
     recorded proof — the deliberate violation that made each check fail loudly (date +
     observed error). A check that has never been seen to fail is not yet a check;
     re-prove after any harness edit. If a check is deferred, say so here and put it in
     the backlog — never describe enforcement that does not exist. -->

---

## Integration vs. Unit Boundary

{{INTEGRATION_BOUNDARY}}
<!-- Where does the project draw the line, and where do integration tests live?
     e.g. "tests/integration/ may touch the real database file and real filesystem but
     still never the network; anything slower/flakier belongs to the smoke test or the
     owner acceptance checklist." -->

Every behavior in a phase spec must be pinnable by a deterministic test, or explicitly
assigned to the acceptance-review checklist. "Feels right" is not an exit criterion.
