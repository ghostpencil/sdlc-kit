---
name: mutation-testing
description: Assess test suite strength by deliberately introducing bugs into production code and observing whether tests catch them.
argument-hint: "[file, directory, or description of what to test]"
---

# Mutation Testing

You are now in mutation-testing mode. Your job is to strengthen a test suite by
deliberately introducing bugs (mutations) into production code, running the test
suite, and observing which mutations escape undetected.

## Core Process

The workflow involves three main phases:

### Pre-flight checks

Before beginning mutations:

- Ensure a clean git working tree (`git status` shows no unstaged changes)
- Locate the test runner: identify the command that runs the full test suite
  (typically `pytest` or `npm test`)
- Confirm tests pass on unmodified code

### Per-file workflow

For each file in scope:

1. **Identify 3–8 meaningful mutations.** Read the production code and list
   mutations that reflect real developer mistakes:
   - Removing state-changing operations (assignments, method calls)
   - Inverting boolean conditions
   - Boundary and comparison adjustments
   - Hardcoding or swapping return values
   - Deleting guard clauses
   - Operator changes
   - Modifying constants or defaults
   - Reordering arguments

2. **Apply each mutation individually.** Edit the file (or request the user
   edit it), run the test suite, and record the result. After every test run,
   **revert the mutation before doing anything else.**

3. **Interpret results.** For each mutation:
   - **Caught:** the test suite detected it (good).
   - **Escaped:** no test caught it; a new test is needed.

### Reporting

After completing all mutations, produce a summary table with columns:

- File
- Mutation
- Result (Caught/Escaped)
- Diagnostic quality (which test(s) caught it, or which test is needed)

Follow the table with:

- **Mutation score:** `(caught / total) * 100`
- **Key findings:** which areas of the code are under-tested
- **Recommendations:** what new tests to write (with specific assertions and
  edge cases)

## Constraints

- **Never stack mutations:** apply only one mutation at a time.
- **Always revert:** after each test run, restore the original code
  immediately.
- **Don't mutate tests, imports, docstrings, or comments.** Mutations should
  target production logic only.
- **Don't mutate error-handling code** that isn't directly tested. If a guard
  clause would never be reached in the current test suite, note it but don't
  mutate it yet — leave it for user discussion.
- **Keep scope manageable:** work through files sequentially. For large files,
  consider breaking the work into multiple passes (e.g. module A functions
  1–5, then functions 6–10).

## Workflow for Escapes

When a mutation escapes, use `AskUserQuestion` to clarify:

1. Should a new test be written?
2. Is the code actually dead/unreachable?
3. Is the current behaviour a feature or a bug?

Then, when the user confirms, implement the missing test(s).

## Presenting Results

For each run, include:

**Summary table:**

| File | Mutation | Result | Diagnostic |
| --- | --- | --- | --- |
| `src/foo.py` | Remove assignment | Caught | `test_bar_updates` |
| `src/foo.py` | Invert condition | Escaped | Need test for `y < x` case |

**Mutation score:** 75% (3 caught, 1 escaped)

**Key findings:**
- Functions handling edge cases lack coverage
- Boundary conditions (off-by-one, empty lists) under-tested

**Recommendations:**
- Write test for empty input → should handle gracefully
- Write test for boundary case where `x == y`
- Add parametrized tests for common error paths

## After Completion

Once all files in scope have been tested, offer to:

1. Implement any missing tests identified during the analysis.
2. Re-run the mutation suite to confirm the new tests catch previously-escaped
   mutations.

(The user can decline and move on to the next task.)
