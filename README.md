# nstack

Engineering skills for Claude Code and Codex. Small, evidence-first, and grown from real mistakes.

## How it works

nstack is one plugin that works in both Claude Code and Codex:

- **`core.md`** is injected at the start of every session: a situation → skill map plus defaults for start, build, prove, debug, autonomy, and reply.
- **Skills** load on demand: from the map, from their `description`, or by name (`/nstack:review`).
- **File-type rules** in `rules/` fire once per session when the agent reads or edits a matching file (`.ts`, `.py`, SQL and migrations, tests) and tell it to load the matching skill.

## Skills

| Skill | Use it for |
|---|---|
| `review` | Defects only, each with a failure scenario and evidence. Optional Codex second opinion. Re-review a new head |
| `address-review` | Classify review comments as fix, dismiss, or ask. One push. Reply with SHA or disproof |
| `preflight` | Run CI locally before pushing. Shape commits. Write the PR body |
| `land` | PR status, CI triage, merge, and confirming deploy and migrations shipped |
| `coordinate` | Parallel sessions: briefs, worktrees, the review loop, retries, pickup, pause |
| `issues` | Checklist audit, what's unblocked, parallel lanes, bug triage |
| `debug` | Root cause from runtime evidence |
| `perf` | Measured performance work. Vet every number |
| `design` | Usage-first sketches, design it twice, red flags, prototype instead of debating |
| `refactor` | Pin behavior, subtract, reshape, migrate callers, delete |
| `tests` | Whether to write a test, and how it tests behavior |
| `cleanup` | Strip comments, guards, and slop from a diff before commit |
| `investigate` | How/why questions with cited, evidence-labeled answers |
| `decision-log` | Per-run decision trail, plus durable decisions, assumptions, and open questions |
| `catch-me-up` | What changed and what's waiting on me. Recall across sessions |
| `verify-ui` | Drive the real app with playwright-cli. Generate a per-repo `verify-<app>` skill |
| `learn` | Turn a repeated mistake into structure (a type, lint, or test), and prose last |
| `writing` | Docs, PRs, commits, and agent-facing prose |
| `types-and-boundaries` | Parse at boundaries, model the domain, idempotency, concurrency |
| `typescript` | TS rules, plus `references/patterns.md` and `references/react-next.md` |
| `python` | Python rules |
| `supabase` | Migrations, RLS and grants, auth, environments |

## Install

**Claude Code**, once:

```
/plugin marketplace add nelsongallardo/nstack
/plugin install nstack@nstack
```

Then in `/plugin` → Marketplaces → nstack, turn on auto-update. Updates arrive on their own.

**Codex**, once:

```
codex plugin marketplace add nelsongallardo/nstack
codex plugin add nstack@nstack
```

The next time you open Codex it says a hook needs review: approve the nstack hooks once. To update later: `codex plugin marketplace upgrade nstack`.

## Adding to it

See [CONTRIBUTING.md](CONTRIBUTING.md). Usually the `learn` skill opens the PR.

## Credits

Much of this is adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT). See [NOTICE](NOTICE).
