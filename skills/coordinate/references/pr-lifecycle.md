# Owner keeps the PR until it's live

Use this variant when a delegate should own its change from "PR open" all the way to production: queues of tickets, long-running programs, anything the user wants to hear about only at approval and at "it's live". For one-off delegations, the coordinator landing the PR (`land`) is still simpler.

## Who does what

| Phase | Owner (the delegate) | Coordinator | User |
|---|---|---|---|
| Review | Fixes CI (`debug`), addresses comments (`address-review`), one push per batch | Reads reports | Reviews or not |
| Approved | Reports once, names the approver; keeps handling new comments | Notifies the user: "approved, ready to merge" | Merges (default; the owner never merges unless the user granted it) |
| Deploying | Follows the rollout (`land`, `follow` mode) with the project's deploy-status tool | Moves the tracker to its "deploying" state | — |
| Live | Reports with evidence, stops its loop | Verifies the deploy itself, notifies, closes the tracker item, removes the workspace, worktree, and merged branch | — |
| Rollout failed | Reports with evidence, never reverts or redeploys | Notifies the user | Decides |
| PR closed unmerged | Reports, stops | Notifies | — |

Cleanup waits for a verified deploy, not the merge: the owner still has work while the change rolls out.

## The owner's loop

The owner runs a self-paced loop in its own session (Claude Code: `/loop` with no interval; Codex: re-check on each turn). Each tick it finds its phase and acts. Pace about 15 minutes while CI, a fresh comment, or a rollout is moving, and about 30 while waiting for a reviewer.

Rebases go onto trunk only when drift breaks the build or conflicts, with `--force-with-lease=<branch>:<last pushed sha>`. If the owner pushes after an approval, it says so in the report, because the approval may be dismissed.

Replies to review comments follow the repo's rules. Where they don't settle it, reply to bot reviewers after fixing, and list human comments (with what changed) in the report for the user to answer.

## The report

The report is one file per unit, overwritten in place, and written **only when the phase or something the user must know changes**. The coordinator watches the directory, so a write is a wake-up.

```
STATUS: pr-opened | updated | approved | merged | deployed | deploy-failed | blocked | closed
head SHA, PR
what changed since the last report
evidence: the command or tool and its real output (tests, CI, delivery status)
comments for the user to reply to
assumptions: each with its evidence and what changes if it's wrong
```

## Recovering a dead owner

If GitHub shows a phase the reports don't (merged, but no `merged` report), the owner died. Start a fresh owner in the same workspace with a consolidated brief: the original brief, later directives, the last report, and "you are in phase N".
