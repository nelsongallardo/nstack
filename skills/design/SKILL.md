---
name: design
description: "The user's own design procedure: caller usage first, types and signatures, design it twice, red flags, prototype instead of debating. Load before building a new module, service, endpoint, shared component, or any change with more than one plausible structure, and for 'where should this live'."
---

# Design

Most changes need none of this. Use it when the change crosses function boundaries, moves ownership, or could take several shapes. A one-file change with an obvious approach goes straight to code: say so and move on.

**Assume the next contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles.** Prefer the design where a change that looks right from one file is right for the whole repo.

## 1. Ground

Build a real model of every system the change touches. Naming a file isn't grounding. If the design moves ownership or layering, find out why the current shape exists (`investigate`), so the rationale becomes a constraint instead of a guess.

## 2. Write the caller's usage first

Write the README snippet or two or three realistic call sites the consumer will write. Derive the types from that usage. When the sketch and the usage disagree, fix the sketch. The caller's experience is the spec, and the types serve it.

## 3. Sketch types and signatures

- Data structures first. Trace each dominant access pattern. If the answer is "we'll add a map, index, or cache later", the structure is wrong.
- Write signatures with `throw new Error("not implemented")` bodies (or `raise NotImplementedError`) and pseudocode. A reader should trace data from input to output by reading the types alone.
- One source of truth per invariant. Derive instead of syncing. If two lists must agree and can't be derived from each other, make the build fail when they disagree.
- Small change: one file. Larger: a module map plus the types.

## 4. Design it twice

Sketch at least two structurally different whole shapes, even when the first looks good enough. Point fixes inside one shape don't count. Compare on interface depth: prefer the design that hides more complexity behind a smaller public surface. A deep module is not a deep call chain. If tracing a flow takes more than three files, flatten it.

For a high-stakes or contested shape, run the second candidate on the other model family (`coordinate`, competing implementations).

## 5. Screen against the red flags

- **Shallow module.** The interface is as complex as the implementation.
- **Information leakage.** Wire, ORM, or transport types appear on the public API.
- **Temporal decomposition.** Modules named after steps (load, validate, transform, save) that repeat the same domain rules. Execution order is not ownership.
- **Pass-through method.** A layer that only forwards.
- **Split ownership.** Two places own one piece of state.
- **Two ways to do one task.** Agents copy whichever they find first, so both keep gaining callers.
- **Importable internals.** The wrong import compiles.
- **Hand-synced list.** Two lists that must be kept in step by hand.

## 6. Prototype instead of debating

If an open question could be answered by running something (behavior, timing, layout, feel, perf), build a throwaway prototype instead of arguing about it.

- No decision, no prototype. Name the decision first.
- Build in a scratch dir. For UI, use plain HTML/JS with CDN deps and put the alternatives behind one labeled switcher. Propose a variation the user didn't ask for. For behavior, use the smallest script that exercises the question.
- The observation is the test. The output is a decision plus a throwaway artifact. Say plainly that the artifact is throwaway.
- Don't adversarially review an abstract plan. Reviewers invent risks that never happen.

## 7. Write the rationale (one page)

- **Problem**
- **Usage** (the snippet from step 2)
- **Shape**
- **Tradeoffs**: "we accept X in exchange for Y"
- **Alternatives**: at least one, or "this was the only viable shape because…"
- **Open questions**, phrased as questions
- **Next step**, one sentence

Put durable decisions in the docs repo (`decision-log`). Proceed to implementation by default. Check in with the user only if they asked for it.

## 8. Implement against the sketch

The sketch is the contract. A deviation is a signal to surface, not friction to absorb. If a function needs a parameter the sketch didn't anticipate, ask whether the sketch was wrong, the requirement was missed, or the implementation is overreaching.

Sketch doc comments are scaffolding. Replace them with types or delete them during implementation.

**Scrap and redesign** when you see:

- The same workaround shape in unrelated places.
- Unrelated edge cases that all need special branches.
- Types that need `any`, casts, or optional fields that are always set.
- A lock reflex where the sketch said nothing was shared.
- Callers that must know internal rules.

A few edge cases don't condemn a design, because complexity in the data isn't complexity in the design. When you redesign, the new sketch should be smaller than the old one before it grows.
