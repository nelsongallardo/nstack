---
name: learn
description: "The user's own procedure for turning repeated mistakes into structure (types, lint, tests) and skill edits. Load for 'reflect', 'learn from this', 'remember this', 'don't do this again', 'you keep doing X', or after the user corrects the same thing twice."
---

# Learn

Assume every future contributor is an agent that sees only the files it opened, copies the nearest example, and takes the shortest path that compiles. Make the right path the easy one.

**A class of mistake counts once it has happened twice.** One weird session is an anecdote, not a rule. A fix written from one bad session tends to overfit that session.

## 1. Find the lesson

From the session, recent commits, reverts, review comments, and the user's corrections, look through three lenses (use parallel subagents for a long session, and run the third on Codex for real diversity):

- **Judgment:** the durable principle behind a specific incident. State the rule, not a label.
- **Tooling:** the concrete command, path, or flag a future agent would otherwise re-derive. Flag every moment the user pasted context the agent could have fetched itself. The owning skill should fetch it next time.
- **Divergent:** the session's "obvious" learning is rarely the most useful one, so look for the one beneath it. Look for decisions that survived only because a test path was lucky, verification that was self-reported, and missed second-order effects.

## 2. Fix at the highest level that works

1. **Architecture:** give state one owner and each task one supported way. Hide internals so the wrong import fails. Delete old ways and dead code an agent would copy.
2. **Types:** make the bad state impossible to write.
3. **Lint or CI check:** use one whose error message names the fix (the file, type, or function to use instead). If the pattern is already common, fail only when a change adds more.
4. **Test:** one that fails when the behavior breaks.
5. **Written rule, last.** Nothing fails when an agent skips prose, so use it only for judgment calls. Pick the narrowest home:
   - the repo's AGENTS.md / CLAUDE.md for repo facts;
   - an nstack skill for how to work;
   - the user's global instructions for personal preferences.

Prove each new check fails on a real past mistake: revert to the bad code, or replay the bad input, and watch it fail.

## 3. Filter before proposing

Each candidate must pass all of these:

- **Durable:** still true in 6 months.
- **Decision-changing:** a future agent does something different because of it, not just reads more text.
- **Existing home first:** edit the skill that should have caught it. If the guidance already exists and was ignored, the issue is execution, not the skill. Fix its placement or trigger (the `description`), not its content.
- **Structural check:** if a lint, script, or runtime check could enforce it, propose that instead of prose.
- **Routes only to skills the session actually used**, or to the description of a skill that should have triggered and didn't.

## 4. Propose, then apply on approval

- An **Accepted** table (Problem | Proposal | Where) with one sentence per cell.
- A **Rejected** list with a reason each (one-off, already covered, not durable).
- A **Backlog** of structural fixes too big for now, filed as GitHub issues.

Wait for the user's approval, row by row. Apply trivial edits directly. For an nstack skill change over ~10 lines, open a PR to the nstack repo with the evidence (the session or PR where the mistake happened twice), and keep each skill under 150 lines. A new skill follows the checklist in the nstack repo's AGENTS.md (core map row, description, eval case, path rule), or it will never be invoked.

When a rule's mistake can no longer happen, delete the rule.
