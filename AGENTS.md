# nstack repo

This repo is a skills pack for Claude Code and Codex. Read CONTRIBUTING.md before changing it.

## Adding or renaming a skill (all steps, every time)

A skill that isn't wired in never gets invoked. Agents load skills reliably only when the always-on text names them. So a new skill (Java, Go, anything) is done only when all of these hold:

1. `skills/<name>/SKILL.md` exists, its frontmatter `name` matches the folder, and its `description` starts with "The user's own ..." and lists the situations and phrases that should trigger it.
2. `core.md` has a row for it in the situation → skill map.
3. If it applies to a file type (`.java`, `.go`, `.sql`...), `rules/nstack-<name>.md` has a `paths:` list and a one-line instruction to load `nstack:<name>`. The plugin hook `hooks/file-rules.py` fires it when an agent touches a matching file.
4. `evals/<case>/` has a realistic prompt (one that doesn't name the skill) and a `tool_used: Skill` grader for it.
5. `python3 scripts/check.py` passes. The pre-commit hook runs it (enable it once per clone: `git config core.hooksPath .githooks`).
6. Run the eval for the new case (`evals/README.md`) and confirm the skill fires.
7. Bump `version` in `.claude-plugin/plugin.json` and `marketplace.json`. Installed copies update through the plugin (see README).

Keep everything project-agnostic: no project, company, person, or PR names.
