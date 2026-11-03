---
name: types-and-boundaries
description: "The user's own rules for types and data modeling: parse at boundaries, identity from the session, branded IDs, unions and state machines, idempotent operations, concurrency. Load when adding or changing types, parsers, API or DB boundaries, workers, webhooks, or state logic."
---

# Types and boundaries

Make the compiler reject impossible states, mixed-up primitives, and unhandled variants. Define errors and special cases out of existence instead of adding handlers for them.

**The tiebreaker against ceremony is the simplest total type.** Strengthen a type only where the loose one already forces a lie today: a `!`, a cast, or a "should never happen" throw. Fewer lines beat elegant boilerplate.

## Parse at the boundary, trust inside

External data is untyped until parsed. That covers HTTP and RPC payloads, JSON, webhooks, queue messages, CLI args, config files, environment variables, and **database rows**.

- Every boundary has a parse function that turns raw input into a named domain type. Untyped maps (`Record<string, unknown>`, `dict[str, Any]`) stop at that parse.
- Inside the system: typed data, errors propagate, nothing is re-validated. A deep null check for something the boundary already guaranteed hides bugs.
- Keep business logic in pure functions. The shell (controllers, handlers, framework glue) stays thin and mechanical.
- Expose domain concepts across a boundary, not the boundary's private representation. Never let ORM rows, wire DTOs, or framework request objects leak into the service layer or the public API.
- Wire input: ignore unknown fields so older clients keep working. Config files: reject unknown fields, because a typo should fail.
- Persisted JSON is a versioned blob, parsed with failure handled.

Two questions decide where code goes:

1. Is this data crossing a system boundary right now? If not, validating it again is redundant.
2. Can this be a pure function the shell just calls? If yes, extract it.

## Identity and authority come from the session

The caller's authority comes from the verified session and server-side authorization. Request contracts may carry target IDs, organization selections, invitation emails, and other business data; none of those fields proves the caller's identity, membership, or role. Authorize access to the requested target on the server for every operation, including reads.

## Brand what gets mixed up

When two arguments share a primitive type but mean different things (`userId` and `orgId`, both strings), give each its own type. Create it only inside a verifying parse function, then trust it downstream. Don't brand by reflex. A lone string that can't be confused with anything stays a string.

## Model the domain as data

Encode the domain in a data structure instead of scattering it across conditionals. Choosing the structure at write time is cheap. Recovering it later reads as a refactor and gets deferred.

- A state machine (an enum or union plus a transition table) instead of scattered booleans or phase checks.
- A discriminated union instead of a bag of optional fields.
- A map, registry, or lookup table instead of branching spread across files.
- A reducer or command/event model instead of ad hoc mutations.
- A module per body of domain knowledge, not per step. Execution order is not ownership.

**The tells that you skipped this:**

- A feature that adds one more branch to an existing if/else chain.
- A second boolean that must stay in sync with the first.
- Phase-named modules repeating the same rules.

**Restraint:** prefer boring code when the shape is already clear, local, and unlikely to grow. Be skeptical of an abstraction that adds indirection without removing branches, duplicated rules, invalid states, or lifecycle risk.

## Exhaust variants

Every switch over a union handles every case, and the compiler fails when a new variant appears. Never use a silent `default` that swallows new cases.

## Construct, don't check

Build shapes where the illegal value can't exist:

- A non-empty list as head plus tail.
- Pairs as a list of 2-tuples.
- A range constructed from a valid start and a validated finite, nonnegative duration. Plain numeric fields alone do not enforce the invariant.

Apply the simplest-total-type rule. Otherwise return `T | undefined` / `Optional[T]` and let the caller handle it.

## Derive types from the source of truth

When a DB schema, OpenAPI spec, zod or pydantic schema, protobuf, or GraphQL schema owns a shape, generate or derive the type from it. A hand-written parallel type drifts. Add a drift check in CI (generate, then `git diff --exit-code`).

## Idempotent operations

Every mutating step (migration, worker, webhook handler, cron job, seed script) must survive running twice and crashing at any point.

- Read the current state, compare it to the goal, and apply only the difference. Derive each step from the state that exists, not from what the previous run meant to do.
- Write to a temp path and rename it into place. Compare artifacts by content, not creation order.
- Use upserts with natural keys, `IF NOT EXISTS`, and dedupe keys for webhooks.
- Test with three questions: Twice in a row? Crashed at every point? Converges? If any answer is "it depends on what was left behind", add a reconciliation step.

## Concurrency

Ask: what happens if another actor modifies this at the same time? If the answer isn't "nothing", isolate. Give each writer its own key, row, or file, and merge at read time. Treat "we need a lock" as a design smell.

When one shared writer is a real invariant, serialize it structurally, in this order of preference: a single-writer actor or queue, sequential phases, then an atomic compare-and-swap or `SELECT … FOR UPDATE`. Every DB transaction gets a statement timeout and an idle-in-transaction timeout.
