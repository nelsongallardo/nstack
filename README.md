# nstack

Engineering skills for Claude Code and Codex. Small, evidence-first, and grown from real mistakes.

## How it works

- **`core.md`** is always loaded: about 40 lines of defaults (start, build, prove, debug, autonomy, reply). Claude Code gets it from the plugin's SessionStart hook. Codex gets it from a marked block in `~/.codex/AGENTS.md`.
- **Skills** load on demand. Each one triggers from its `description` when the task matches, or by name (`/review`). There's no mode to switch on.
- **`coordinate`** is the entry point for big work spread across parallel sessions.

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

Claude Code:

```
/plugin marketplace add nelsongallardo/nstack
/plugin install nstack@nstack
```

Then turn on auto-update for the `nstack` marketplace in `/plugin` → Marketplaces.

Codex (and re-run after `git pull`):

```
git clone git@github.com:nelsongallardo/nstack.git ~/projects/nstack
~/projects/nstack/install.sh            # --dry-run to preview
```

## Adding to it

See [CONTRIBUTING.md](CONTRIBUTING.md). Usually the `learn` skill opens the PR.

## Credits

Much of this is adapted from [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan (MIT). See [NOTICE](NOTICE).
