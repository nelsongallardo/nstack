# Running delegates in Herdr

Read this before you create a pane, tab, or workspace for a delegate. `coordinate` section 4 decides where the delegate runs. This file covers how. For syntax, `herdr <group>` and `herdr --skill` are the authority.

## Create the place

- **Child worktree workspace.** Run `herdr worktree create --workspace <repo workspace> --branch <b> --base <ref> --path <dir> --label <label> --trust-repository --no-focus`. Herdr links it to the repo's workspace, so the sidebar shows it as a child in the repo's tree with its own branch, and `workspace close --group` closes them together. Don't hand-make a `git worktree add` plus a pane split for this case.
- **The worktree already exists** (an earlier run or a human made it): `herdr worktree open --workspace <repo workspace> --path <dir> --label <label> --no-focus`. Never `herdr workspace create --cwd <worktree>` for repo work: it makes a standalone workspace that isn't nested under the repo.
- **Label** every delegate's workspace `<task id> · <3-5 word summary>` (an issue number, ticket key, or PR), so the user can tell them apart at a glance. Rename with `herdr workspace rename <id> <label>`.
- **Workspace ids are per session.** Look the repo's workspace up by label (`herdr workspace list`) each time; never hardcode an id in a brief or a loop file.
- **Sibling pane.** Read `herdr pane layout --pane <caller>`. Split a wide pane right and a narrow or tall pane down, and don't stack splits into unusably narrow columns: `herdr pane split --pane <caller> --direction right|down --cwd <dir> --no-focus`.
- **New tab.** Run `herdr tab create --cwd <dir> --no-focus`.

## Start and run the agent

- **Start it** in the new pane, or in the new workspace's or tab's root pane. Take the pane ID from the JSON output (or `herdr pane list --workspace <id>`), then run `herdr agent start <name> --kind claude|codex --pane <id>`. Use `--kind codex` for the second opinions and competing implementations in `coordinate` section 6.
- **Address agents explicitly.** Give each agent a unique name. Target it by that name or its pane ID, never by UI focus.
- **Brief and watch.** Write the brief to a file and send `herdr agent prompt <name> "Read <path> and carry it out. It is your full brief."`. An inline brief breaks on quoting and length, and the file is what you consolidate when a fresh agent takes over. Check progress with `herdr agent get`, `read`, and `wait`. The report still goes to a file path you read on the same machine.

## Gotchas

- **A big repo takes minutes to check out.** `herdr worktree create` can outlast a foreground command timeout. Run it in the background and read its JSON when it finishes; a timeout isn't a failure.

- **A timeout doesn't mean the prompt failed.** `agent prompt --wait` can return `timeout` while the agent is already working. Check `herdr agent get` before resending, and never resubmit blindly.
- **A new folder means a trust dialog.** Claude Code started in a fresh worktree stops at its folder-trust dialog. Read the pane. Accept only for a folder the user asked you to work in. Otherwise ask the user. For a worktree you create for the delegate, `--trust-repository` on `herdr worktree create` skips the dialog.
