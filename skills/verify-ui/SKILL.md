---
name: verify-ui
description: Prove a web change works by driving the real app the way a user does, with playwright-cli, and capture evidence. Also generates and maintains a per-repo verify-<app> skill (launch, doctor, drive, evidence, cleanup, plus a feature map). Use to verify a UI change, reproduce a frontend bug, "check it in the browser", "show me it works", or "make a verification skill for this repo".
---

# Verify UI

An agent that can check its own work keeps going until the check passes. One that can't hands every result back to you.

If the repo already has a `verify-<app>` skill, use it. Otherwise drive the app ad hoc (section 1), and offer to generate one (section 2) when the repo will see repeated UI work.

## 1. Drive it now

1. **Launch** with the repo's own dev command, from a clean environment (`env -i HOME="$HOME" PATH="$PATH" …` when agent env vars interfere). Wait for a readiness signal that means usable, not just "a process answers". A DB health check can pass while init scripts are still running.
2. **Doctor**: is this instance worth driving? Check that the process you started owns the port, it's the right build or branch, the seed data is present, and you're not stuck on the login page.
3. **Drive** with a fresh, non-persistent playwright-cli session for localhost, named after the project. Use role and name locators. Walk the changed flow through the real UI. Don't use internal setters or test-only endpoints.
4. **Evidence:**
   - An ARIA snapshot and a screenshot with the app identity visible.
   - The action plus the resulting state, not only the final screen.
   - Side effects read back through a second, read-only view: an API call or DB select showing the row written.
   - For bugs: the broken state reproduced twice before the fix, and gone twice after, with the same data.
5. **Cleanup:** kill what you started, never by process name. Keep the evidence. A cleanup that deletes the proof fails.

Store artifacts in a gitignored `artifacts/<feature>/<step>.*`.

"An expected dialog, loading state, or setup step is not the bug." State inspection may confirm an observation, but it must never inject or force the symptom.

## 2. Generate `verify-<app>` for a repo

Interview the repo, not the user. Ask only what the code can't answer.

1. Find the surface (which apps, which ports), how it runs locally (migrations and seed included, from an empty data dir), what can drive it (existing Playwright specs first, otherwise playwright-cli), what to observe (DB, API), and how to isolate runs (a per-run data dir or schema). Refusing to double-drive a shared instance beats corrupting the user's session.
2. Write `.claude/skills/verify-<app>/SKILL.md` with exact **Launch**, **Doctor**, **Drive**, **Evidence**, and **Cleanup** sections, plus a **Helpers** section for any script it ships.
3. Write a feature map in `features/`:
   - `README.md`: baseline preconditions (fresh data dir per run; never drive an instance this run didn't start), proof rules, and an index.
   - One file per user-facing feature (start with the top 3 to 5). Each has an H1 and one paragraph, then exactly four H2s: `Sub-features` (short IDs), `How to get to it (user POV)` (every entry point), `Driving it` (starts with `Preconditions:`, then action → exact command → observable result), and `Gotchas`.
   - If seed data lacks a precondition, the journey fails and the gap goes in Gotchas. Never weaken the journey to make it pass.
4. **Prove it once before handing over:** launch, doctor, drive one feature, capture, clean up, and confirm the evidence survived. A generated skill that was never executed is a draft, not a deliverable.

**Proof rules:**

- UI proof: an ARIA snapshot plus a screenshot.
- Mutation proof: a read-only second view of the stored value.
- HTTP proof: the command, status, and body.
- Record the feature ID and entry point with every artifact. Don't report a skipped entry point as verified through a different path.

## 3. Maintain it

When the app has changed, walk the feature map.

1. One read-only subagent per feature file reports likely drift.
2. Then do one serial live pass that drives every feature. It's required even when the source looks clean.
3. Triage what you find:
   - **Doc drift:** fix the map.
   - **Harness gap:** fix it and re-drive.
   - **Product regression:** report it. Don't paper over it in the docs.

The outcome is exactly one of **clean**, **changed** (one PR, edits only inside the skill's directory), or **blocked** (with the exact blocker).
