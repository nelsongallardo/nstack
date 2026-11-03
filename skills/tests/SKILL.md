---
name: tests
description: Decide whether a test is worth writing, then write or review it so it tests behavior rather than implementation. Use when writing, changing, or reviewing tests, when asked for TDD or a regression test, when a bug fix might need a test, or when deciding whether a change needs tests at all.
---

# Tests

Prefer no new test over a bad test. Proof that the change works is mandatory. A new test is one way to provide it, not the only one.

## 1. Should there be a test?

**Write one when:**

- There's a real behavior gap the existing tests don't cover.
- A bug fix has a cheap local test target. The test must fail on the old code.
- The user asked for TDD or a regression test.
- The logic is isolated and has clear failure modes. List the failure modes, then test them.

**Skip it for:**

- Docs, config, copy, and pure wiring changes.
- Cases where the test path is unclear, expensive, or integration-heavy and nobody asked for it. Prove the change with a real command, script, browser run, or log assertion instead, and say so.
- A test that would mostly test mocks, encode current internals, depend on timing or global state, or be deleted right after proving the fix.

## 2. Behavior, not implementation

**Behavior** is what the code's users can observe through the interface they use: return values, errors, state they can read back, and effects outside the code (a request sent, a row written, a message emitted).

**Implementation** is what they can't observe: private helpers, internal call order, intermediate data, and which collaborator did the work.

**The two imagined edits.** Run both against every test you write or keep:

1. **Break the behavior**: return a wrong value, skip the effect, do it twice. If the test still passes, it proves nothing. The usual causes:
   - an assertion looser than the contract;
   - an expected value computed by the code under test;
   - a restated constant;
   - an assertion on data the test built itself.
2. **Change the internals** while keeping the observable results. If the test fails, it is pinned to the implementation. It will need a rewrite on every refactor and still catches no bug.

Keep a test that catches the first edit and survives the second. Rewrite or delete the rest.

- Derive the expected value from the requirement, never from a run of the code.
- Callers branch on the error type, which is the contract. An exact error message pins wording no caller reads.
- A test can pin an invariant instead of a call, such as a key that must exist in two tables, or a compile-time type check.

## 3. Mocks

**Don't mock what you can run.** Use a real Postgres (local, disposable, or testcontainers) instead of a mocked repository. Call the real app over HTTP (supertest, FastAPI `TestClient`) instead of calling handlers directly.

Mock only what you can't run locally, such as third-party HTTP, at the transport layer (msw, nock, respx).

The contract decides what to assert, not the shape of the assertion:

- The payload a mocked external service receives is behavior. A call to an internal helper is implementation.
- "Payment client got no call" is behavior when the promise is "an empty cart never charges". Pair it with a case where the charge does happen, so the test shows it can see a call.

## 4. TDD flow (when it applies)

1. Pick the narrowest existing place to add the test.
2. Write the failing test, then **run it before fixing**. Confirm it fails for the intended reason. If it passes, or fails for an unrelated reason, fix the test or the repro first.
3. Make the smallest fix and rerun. Land the regression test first, then sibling coverage.
4. Never change a test to match a wrong implementation. Never weaken an assertion unless the expected behavior really changed.

## Reply

Name the failing-before run and the passing-after run. If you couldn't show it failing first, say why.
