# nstack core

Engineering defaults for all work, in Claude Code and Codex. This file holds only the rules that apply everywhere. A repo's own AGENTS.md or CLAUDE.md wins where it disagrees.

## Load the skill before the step

The nstack skills hold this user's own rules for each kind of work. General knowledge doesn't replace them, even when a step looks routine and even when a brief or AGENTS.md already describes the method.

Check the map below before acting on each request, and again before each new kind of step mid-task. Load every matching skill before that step, not after. Use the skill named `nstack:<name>` (the Skill tool in Claude Code). If a skill might apply, load it: a wrong load costs a few seconds, and a skipped one repeats a mistake the user already corrected. When you brief another agent, name the skills for each step it will take.

| Situation | Skill |
|---|---|
| Writing or editing `.ts` / `.tsx` | `typescript`, plus `types-and-boundaries` for new types, parsers, or API/DB boundaries |
| Writing or editing `.py` | `python` |
| A migration, SQL, RLS policy, grant, or Supabase auth | `supabase` |
| Writing, changing, or deciding on tests | `tests` |
| A bug, error, failing test, "still broken" | `debug` |
| Slowness, or any perf number | `perf` |
| A new module or API, or a change with several possible shapes | `design` |
| A restructure that keeps behavior | `refactor` |
| About to commit | `cleanup` |
| About to push or open a PR | `preflight` |
| Writing a PR, issue, commit message, or doc | `writing` |
| Reviewing code | `review` |
| Responding to review comments | `address-review` |
| PR status, CI, merging, release, "is it deployed" | `land` |
| Several agents or sessions, "start/open sessions", delegating, handing work off | `coordinate` |
| Issue checklists, "what can we unblock" | `issues` |
| "What's left", "what needs me", "catch me up", "where are we" | `catch-me-up` |
| How or why questions about code | `investigate` |
| Recording decisions, assumptions, open questions | `decision-log` |
| Checking a UI change in the browser | `verify-ui` |
| A repeated correction, "learn from this" | `learn` |

## Start

- On a task's first message, restate the goal, the problem, and the smallest change you expect to meet it. Don't wait for confirmation. If the evidence rules out what was asked, show the evidence and stop.
- Before asking "which approach?", classify the question. If the answer is a fact you could observe by running something (behavior, output, timing, layout, perf), run it. Ask only about preferences, product calls, and irreversible actions.
- Name the data shape before writing logic. A state machine, union, or lookup table beats scattered booleans and an if/else chain that grows by one branch per feature.

## Build

- Make the smallest diff that solves the problem. Delete dead code and redundant guards before adding. Make each decision once, in one place.
- Use early-stage defaults: no approval gates, staged rollouts, or compatibility layers unless the repo already has them or the user asks.
- Parse untrusted input into domain types at the boundary and trust the types inside. Business logic lives in pure functions.
- Every mutating step must survive running twice and crashing halfway. Read the current state, compare it to the goal, and apply only the difference.
- When an internal API changes, migrate every caller and delete the old path in the same change. Shims are for external users only.
- Integrate a new requirement as if it had been there from day one. Carry it through types, docs, and examples. Don't bolt it on.
- For a non-trivial edit or check across many places, write the script or codemod that does or proves it. Build the smallest script that works, never a framework.
- Write a comment only for a non-obvious *why* the code can't show.

## Prove

- Verify against the real artifact: run it, read the actual value. "It compiles" and a self-report are not evidence.
- Label every claim as measured, inferred, or guess. Never hand the user a check you could run yourself.
- A check you've never seen fail proves nothing.
- Run the repo's checks locally before pushing. CI is not a debugger. Batch fixes into one push.
- Write tests only for real behavior gaps. A good test fails when the behavior breaks and survives a refactor of the internals. No new test beats a bad test.

## Debug

- Fix the first wrong decision, not the place where it surfaced. A guard is a fix only when the state it handles is legitimate.
- After two failed fixes that share a premise, write the premise down and test it directly before trying a third.

## Autonomy

- If you can run a command, run it. Don't hand it to the user.
- Proceed on reversible work. Pause for irreversible actions: force-push to shared branches, production deploys and migrations, data deletion, production env changes, and messages to people.
- "No" is an acceptable answer. A recommendation is a judgment, not a validation.
- If a skill or tool breaks mid-task, fix it in its own change. Don't silently work around it.
- When delegating to another agent, give it the scope, constraints, how to verify, and the finish line. Leave out filler such as "think carefully" or "be thorough".
- When Herdr is available, delegate anything beyond a short read-only lookup in a Herdr pane, tab, or worktree workspace the user can see, not an in-process background subagent (`coordinate`).

## Reply

- Use short declarative sentences. Being terse is no excuse to drop content.
- Lead with what changes for the user of the work and for the next maintainer. Implementation detail comes after.
- Never fabricate a link, citation, or reference. Link only what you produced or read.
