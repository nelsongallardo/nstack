---
name: preflight
description: "The user's own pre-push procedure: run what CI runs locally (CI costs money), prove the change, shape commits, write the PR body. Load before every git push, before opening a PR, after CI fails, and for 'is this ready'."
---

# Preflight

CI is not a testing ground. Every push restarts paid checks, so find failures locally and push once.

## 1. Run what CI runs, locally

1. Look for the repo's own local-CI entry point first: `yarn ci:local`, `make ci`, `scripts/ci-local.sh`, `just ci`, or a section in AGENTS.md / CONTRIBUTING.md. If one exists, run it. It is the contract.
2. Otherwise read `.github/workflows/*.yml` and run the same steps in the same order: install with the lockfile frozen, then lint, typecheck, test, build, and any boundary, contract, or codegen drift check. Skip only steps that truly need CI-only secrets or infrastructure, and list them.
3. If the change touches a migration, apply it to a local or disposable DB and read the affected rows back.
4. For generated artifacts (API contracts, OpenAPI, Prisma client, types), run the generator and confirm the tree is clean afterwards.
5. If a step fails, fix it and rerun from that step. Don't push to "see what CI says."

Keep git hooks on. Never `--no-verify`.

## 2. Prove the change itself

Checks passing isn't the same as the change working. Match the proof to the change:

| Change | Proof |
|---|---|
| CLI | Run the real command |
| HTTP endpoint | Call it (curl, or a test against the real app) |
| UI | Walk the changed flow in the running app (`verify-ui`) |
| Parser or migration | Replay a saved input, then read back the result |
| Storage | Read back the written value |
| Perf | A before and after number, vetted with `perf` |

State "done" as checks that can pass or fail, such as "text output stays byte-identical and the JSON parses". A mood is not a check.

## 3. Clean the diff

Before committing, run the `cleanup` pass on the diff: narrating comments, unsupported guards, dead compatibility paths, debug logs, unrelated edits.

## 4. Shape the commits

- Commit freely while working. Before opening the PR, rebase into small, ordered commits that each pass their relevant checks. Run the regression test against the old code first, then include the test and fix together in a landable commit.
- Titles: `type(scope): subject`. Imperative, no trailing period, naming a real symbol when one carries the change.
- Commit bodies don't restate the subject.
- Stage named files only. Never `git add -A` in a tree with scratch files.

## 5. Open the PR

Work from a branch off main. A dirty branch with unrelated work gets patched out into a fresh worktree.

Write the body as a one-minute briefing for a reviewer who has the diff, under ~40 lines, because it becomes the squash commit. Use these sections in this order and drop any that are empty:

- `## Why`: 1 to 3 sentences, opening with the user's goal. No SHAs and no "based on main" preamble.
- `## What changed`: 1 to 3 bullets. Name both sides of a rename.
- `## Scope`: always present. What the PR covers and what it deliberately leaves out.
- `## Tradeoffs`: only rejected alternatives a reviewer would ask about.
- `## Blast radius`: who or what it touches, and why that's safe.
- `## Verification`: 1 to 3 bullets, each a real run and its outcome. For perf, one `before → after`.

Add screenshots or video only when they prove a claim.

- Prefer five narrow PRs to one large one. A stacked child targets its parent branch (`gh pr create --base <parent>`). Branch from trunk only for independent work.
- Open PRs ready for review, not as drafts, unless the user says otherwise.
- Run `gh pr view <n>` before you state anything about a PR's status.

## 6. Pushing again after review or CI

- Batch every known fix into one push wave, so checks restart once.
- Don't rebase on every trunk move, because each rebase restarts CI. Rebase only to prepare a merge, on a real conflict (`git merge-tree --write-tree origin/main HEAD`), or when a CI failure is caused by trunk.
- A CI failure in untouched code can come from changed callers, dependencies, configuration, or a stale base. Compare the failing check on the base and changed branch under the same conditions before assigning cause. `git merge-base --is-ancestor origin/main HEAD` checks ancestry, not causality.

## Reply

- What ran locally and the result of each step.
- Steps skipped, and why.
- The proof of the change.
- The PR link.
