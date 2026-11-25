# nstack

Engineering skills for AI coding agents. Small, evidence-first, and grown from real mistakes.

## How it works

Agents that support Agent Skills can load the skills on demand. The plugins also wire them into the session:

- **`core.md`** is loaded in new Claude Code, Codex, and Hermes sessions: a situation → skill map plus defaults for engineering work.
- **Skills** load on demand. With a plugin, they use the `nstack:<name>` namespace.
- **File-type rules** in `rules/` remind Claude Code and Codex to load the matching skill when they touch TypeScript, Python, SQL, or tests. The Hermes plugin does not load `rules/`.

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
| `incident-triage` | On-call verdict for a page, shift brief/summary/handoff, drills, alert patterns |
| `learn` | Turn a repeated mistake into structure (a type, lint, or test), and prose last |
| `writing` | Docs, PRs, commits, and agent-facing prose |
| `types-and-boundaries` | Parse at boundaries, model the domain, idempotency, concurrency |
| `typescript` | TS rules, plus `references/patterns.md` and `references/react-next.md` |
| `python` | Python rules |
| `supabase` | Migrations, RLS and grants, auth, environments |

## Install

### Hermes Agent

On the machine that runs Hermes 0.23.2 or newer (the gateway host if you use Telegram or other messaging), run:

```sh
hermes plugins install nelsongallardo/nstack --enable
```

If Hermes pauses for a security review, read the findings before approving the install.

For a named profile, use `hermes -p <profile> plugins install nelsongallardo/nstack --enable`.

Start a new chat to apply `core.md`. The plugin registers the skills as `nstack:<name>`, without editing `AGENTS.md` or requiring Node.js.

To update, run `hermes plugins update nstack`. To disable, run `hermes plugins disable nstack`. Pass the same `-p <profile>` to either, then start a new chat.

### Pi and other agents (skills only)

With Node.js installed, run this and select your agents and skills:

```sh
npx skills add nelsongallardo/nstack --global
```

This installs the skill files without loading `core.md` or running hooks. If you use the Hermes, Claude Code, or Codex plugin, you don't need the skills-only install for that agent.

### Claude Code and Codex plugin

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
