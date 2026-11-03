---
name: land
description: Drive open PRs to merge-ready, merge them when asked, and confirm the result actually shipped (CI, deploy, migrations, issue checklists). Use for "check on PR X", "get it green", "babysit", "merge it", "land the stack", "watch the merge", "is it deployed", or "check everything is ok after merging".
---

# Land

Green is not the same as safe, and a merge command is not the same as merged. Read the real state back at every step.

## 1. Pick a mode first

| Mode | Use for | What it does |
|---|---|---|
| `check` | "check on X", "anything outstanding?", small or docs-only PRs | One status pass, then a report |
| `drive` | "get it green", "merge-ready" | Loop until merge-ready, then stop. Never merge |
| `threads` | "address the comments" | Use `address-review`, and touch nothing else |
| `ship` | "merge it", "land the stack", "get this to production" | Merge, then verify the release |

Only an explicit merge, land, or ship request authorizes merging. Owner approval is something you wait for, not a blocker to fix.

## 2. Status: the first blocker wins

```
gh pr view <n> --json state,isDraft,mergeable,mergeStateStatus,reviewDecision,headRefOid,baseRefName
gh pr checks <n>
```

Check blockers in this order:

1. **Conflicts.** `mergeable=CONFLICTING`, or `mergeStateStatus` is `DIRTY`.
2. **Unresolved review threads**, from any author.
3. **Failing checks.** `ACTION_REQUIRED` and unknown conclusions count as failing. `BLOCKED` with a passing rollup is not a CI failure, only a wait for approvals.
4. **Merge gate**: draft, `CHANGES_REQUESTED`, or closed.

Pending checks mean waiting. Nothing else means ready.

For a stack, scan the whole stack tier by tier before acting: a conflict anywhere outranks a red check at the bottom. Then work the frontier, the lowest unmerged PR. If you catch yourself fixing upstack while the frontier is red, go back down.

Report a conflict to the PR's owner. Don't fall through to CI to look busy. Mention the drift risk: trunk may have new callers of code the PR deletes or moves.

## 3. Classify CI before any retrigger

- **Failure in code the diff touched:** a real bug. Fix it locally (`preflight`), then push once.
- **Failure in code the diff never touched:** probably a stale base. Check `git merge-base --is-ancestor origin/main <head>`. Report that a rebase is needed instead of burning retries.
- **Flake or infrastructure:** one fresh run (`gh run rerun <id>`), once. An identical second failure means it was never a flake. Read the job logs (`gh run view <id> --log-failed`).

## 4. Before merging: is the verdict still current?

- A review verdict covers one patch. After a rebase, compare `git diff <base>...<sha> | git patch-id --stable` at the reviewed SHA and at the head. Same patch-id: the verdict holds. Different: re-review the delta (`review`, re-review mode).
- Decide whether to rebase only now, at merge time. Fetch trunk and check whether it can affect the patch:
  - Conflict, a file changed on both sides, or a change to which checks run: rebase, then wait for CI.
  - Lockfile changed on both sides: no rebase, if a frozen install passes on the merge result.
  - Trunk changed a caller or dependency of the patch: run the patch's checks locally on the merge result. Merge if they pass.
  - Otherwise, merge as is.
- Arm `--auto` only when the verdict covers the current head, because auto-merge lands whatever head is ready.

## 5. Merge and read it back

- Stacks land bottom-up, one PR at a time: `gh pr merge <n> --squash`. A PR whose base is still its parent's branch merges into that branch, not into main.
- Read the result back: `gh pr view <n> --json state,mergedAt,baseRefName`. A queued or auto-merge request is not a merge. A PR has landed only when it reads merged with main as its base.
- After each merge, retarget the child to main and rebase its patch (`git rebase --onto origin/main <old-parent-tip>`), then `git push --force-with-lease`. The patch-id decides whether its verdict survives.
- If a merge stalls, find out why before changing anything.

## 6. Confirm it shipped

Merged is not shipped. Check what the repo's release pipeline does:

- The release workflow run for the merge SHA (`gh run list --branch main --limit 5`). Watch until it finishes.
- Migrations applied in the target environment (check the migration table or the release job log).
- The production deployment for the merge SHA reached a ready state on the hosting platform. Check its runtime errors for a few minutes.
- Hit the changed behavior once in production when it's safe and read-only.

Production deploys, prod migrations, and promotions are always-pause actions unless the user granted them for this run.

## 7. Close the loop

- Tick off the linked issues' checklist items that this PR satisfied. Each tick needs evidence: a SHA, a run, a link.
- Close or move issues whose checklists are complete. Say why for any item left open.
- Update docs the change made stale.
- Record new decisions or open questions with `decision-log`.

## Reply

- Each PR's state, verdict, and merge SHA.
- What shipped, and how you confirmed it.
- Issues updated.
- What's still waiting on the user.
