# {{PROJECT_NAME}} — Testing & TDD Protocol

Read this file fresh before every TDD-skill invocation. Do not rely on memory.

## The Vertical Slicing Mandate

**We follow a strict "Tracer Bullet" TDD workflow. Horizontal bulk-testing is prohibited.**

Do not write all tests for a module at once. Follow the **Red-Green-Refactor** loop for
one behavior at a time:

1. **Identify a Public Behavior:** Pick one specific capability from the current slice's
   exit criteria.
2. **RED:** Write **one** test targeting the public interface.
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

---

## Integration vs. Unit Boundary

{{INTEGRATION_BOUNDARY}}
<!-- Where does the project draw the line, and where do integration tests live?
     e.g. "tests/integration/ may touch the real database file and real filesystem but
     still never the network; anything slower/flakier belongs to the smoke test or the
     owner acceptance checklist." -->

Every behavior in a phase spec must be pinnable by a deterministic test, or explicitly
assigned to the acceptance-review checklist. "Feels right" is not an exit criterion.
