---
name: coordinate
description: "The user's own procedure for multi-agent work: splitting work, briefs that name skills, worktrees, the build-review-fix loop, retries, pickup, pause. Load whenever work involves more than one agent or session: 'open/start N sessions', 'in parallel', 'delegate', 'hand this off', 'run it in another pane', 'finish the epic', briefing a subagent or a Herdr agent, or picking up another session's work."
---

# Coordinate

You run the program, not the code. Each PR has one owner, the only writer on its branch. You own the verdicts and the plan.

**Work that one agent could finish inside a session's budget is not a program.** Do it directly.

## 1. Throughput check before any fan-out

Write these four down. Mark any that don't apply as `n/a: <reason>`.

1. **Blocking first steps.** Gates that must land before anything else (shared types, a migration, a contract).
2. **Independent workstreams.** Disjoint files, services, or layers can run in parallel. Anything with shared writes runs in sequence.
3. **Shared mutable state.** Split the target by default: give each worker its own key, file, or branch. "We need a lock" is a design smell.
4. **Smallest safe split.** Code-coupled work (one feature, one migration) goes to a single owner. Fan out only independent artifacts: separate PRs, audits, investigations, competing experiments. If one worker is best, say why.

Use `issues` to find what's actually unblocked.

**Start with one unit.** Take it through brief, build, review, and merge before fanning out, so a flaw in the brief costs one agent instead of five.

## 2. The brief

Every brief stands alone, because workers can't see their siblings.

```
Goal: <the user's goal, one or two sentences>
Done when: <a command and its expected output, a page state, or an artifact>
Scope: <what this worker does; what it must not touch>
Branch/worktree: <name, based on <sha>>
May write: <paths> | Must not: push to main, merge, comment on GitHub, run prod migrations
Data shape: <the types / state machine / table this change is built around>
Skills: <the nstack skills to load, per step: e.g. typescript + supabase + tests while building, cleanup before commit, preflight before push, writing for the PR body>
Context: <upstream reports, pasted in full, not linked>
Report to: <path>, containing: head SHA, what was built, verification run + output, deferred items, anything the coordinator must know. Reply with only the path.
```

If you can't name the evidence for "done", the unit isn't scoped yet.

Always fill in the Skills line. A worker that receives a detailed brief treats it as complete and won't look for skills on its own.

## 3. Isolation

- Use one git worktree per writing agent: `herdr worktree create` under Herdr (section 4), Claude Code `isolation: "worktree"`, or `git worktree add ../<repo>-<slug> -b <branch> <sha>` for a separate terminal session or Codex. Create the worktree before starting the agent in it. Never run two writers in one worktree. They overwrite each other, and nobody can tell which agent changed what.
- Only the coordinator writes to shared external surfaces: GitHub comments, issues, merges, prod. Workers push their own branch at most.
- Freeze each target up front: capture the PR or issue number once, then check it before every external write.

## 4. Under Herdr, delegates run where the user can see them

Herdr is available when `HERDR_ENV=1` and `HERDR_PANE_ID` matches a pane in `herdr agent list`, or when `herdr` is on PATH and `herdr agent list` shows the pane you run in. Then the user's standing rule applies: delegate in a Herdr pane, tab, or worktree workspace, not an in-process background subagent. That rule is the explicit request the `herdr` skill asks for before it creates panes, tabs, or worktrees. Without Herdr, use the harness's own subagents.

| The work | Where it runs |
|---|---|
| A delegate that writes code in the same repo | A child worktree workspace, linked to the repo's workspace |
| A short delegate the user watches; work that needs the user's input (installs, logins, approvals); work in another repo, or in a repo with no open workspace | A sibling pane in the caller's tab |
| A long-running delegate the user checks now and then, with no separate worktree needed | A new tab in the same workspace |
| A short read-only lookup | An in-process subagent |

Never delegate into a separate Herdr session (`herdr session`). It runs its own server, which the user's view doesn't show.

Before you create the pane, tab, or workspace, read `references/herdr.md`. It holds the commands and the gotchas that stall a new agent.

## 5. The loop per PR

```
owner: build → preflight → push branch → open PR → report
reviewer (fresh session, not the owner; + Codex when large/risky): review → report
owner: address-review → preflight → one push → report with new head SHA
reviewer: review in re-review mode on the new head
PASS → land
```

- Green CI feeds into a verdict but isn't one. The verdict comes from a reviewer that didn't write the code, and it covers one head SHA.
- Spend verification in proportion to the change. A rebase, a conflict resolution, or a minor fix gets a single re-check at the new head. A wording-only change gets none. A full review repeats only for new behavior or a large new diff.
- Opening a PR doesn't start a watch. Post the URL and keep building.

## 6. Running agents

- **Own every delegate's work.** Read the diff and write your own summary. Don't pass through what the delegate said.
- **Use fresh agents with consolidated scope:** the original brief, every later directive, and the prior agent's report and branch. Resumed or interrupted agents silently drop directives. Reuse an agent only when the work needs state that lives in it (uncommitted changes, a running dev server).
- **A role outlives its agent.** When a pane's context is spent, start a fresh session in that pane with a consolidated brief.
- **Background by default.** Never message an agent just to check on it. Judge it by its side effects: commits, pushes, report files, PR activity, `herdr agent get`.
- **Keep agents rolling.** Start the next unit as each one finishes, not in batches. Three to five concurrent sessions is the practical ceiling.
- **Retry by cause.** After a context limit, retry with a smaller scope. After a dropped connection, reuse the same brief. After a tool error, switch models (Claude ↔ Codex). After two retries, drop the unit and replan around it.
- **Second opinions.** Give the same brief to the other model family (under Herdr, a `--kind codex` agent). Agreement is a strong signal.
- **Competing implementations.** When a design could take several valid shapes, give Claude and Codex the same brief in separate worktrees. Score both against 3 to 6 criteria you wrote down first (not shown to them). Pick the base a maintainer can extend most easily, and graft in one or two good ideas by hand. If they converge, ship that. If they diverge wildly, the brief was underspecified, so rewrite it instead of averaging.

## 7. What reaches the user

Ask the user only for irreversible actions, preference or product calls, and dead ends that survived a replan. Rebase mechanics, retries, CI flakes, review triage, and "should I keep going" never reach the user. Under "don't ask me anything, get it to production", apply defaults and report each one with what the user could have chosen instead.

## 8. Merge order and rebases

- Land through `land`: bottom-up, verdict current by patch-id, and the result read back.
- Rebase each branch onto main before its final review, so verification runs on the base it will land on. Don't rebase on every trunk move.
- Migration-bearing PRs: before merging, make sure their migration timestamps sort after everything already applied in each environment. Rename unapplied ones if needed.
- Force-push only your own branch, with `--force-with-lease=<branch>:<sha you last pushed>`. If you see a push you didn't make, stop and report it.

## 9. Long or unattended runs

- State the exit condition as a checkable predicate before iteration 1. A duration is not a finish condition.
- Keep a decision trail (`decision-log`). Push each finished unit before starting the next.
- On each check-in, re-read the plan, compare the actual state against it, and fix drift. Stay silent if nothing changed.
- Stuck after a real attempt? Stop and write up why. Don't reinterpret the goal.

## Picking up someone else's work

Read the prior trail; don't redo it. Get the branch, `git log` and `git diff` against base, the report files, the decision log, and the last messages of the transcript (`~/.claude/projects/<slug>/*.jsonl`, `~/.codex/sessions/`, parsed in a subagent). The trail is authoritative for what was done. Re-prove only the end result, on the real artifact.

## Pausing safely

Pause only on an explicit request. Finish or back out of the current step, start nothing new, and stop nested agents. Commit all edits as one `wip:` commit, noting in the body if the tree is broken. Write a resume note: intent, current step, what's verified, next steps, key files, gotchas.

## Reply

- Units and their owners.
- Each PR's state and verdict.
- What merged.
- Decisions taken under defaults.
- What waits on the user (see `catch-me-up`).
