# Contributing to nstack

These rules keep nstack small.

1. **A rule gets in only after a real miss.** Link the session, PR, or issue where the mistake happened twice. Things that merely sound useful stay out.
2. **Structure beats prose.** If a lint, type, script, or test could enforce it, build that in the project instead. Skills are for judgment calls.
3. **Find the narrowest home:**
   - repo-specific facts → that repo's AGENTS.md;
   - personal preferences → your global agent instructions (CLAUDE.md / AGENTS.md);
   - how to work → an nstack skill;
   - true everywhere → `core.md`.
4. **Edit before adding.** Extend the skill that should have caught the mistake. If its guidance was there and ignored, fix the `description` or the placement, not the content.
5. **Size limits.** `SKILL.md` stays under 150 lines, with detail in `references/`. `core.md` stays under ~80 lines.
6. **Descriptions decide triggering.** Open with "The user's own rules for …" so an agent sees the skill holds something it doesn't already know. Then name the situations and the phrases a user would actually say. Every skill also needs a row in the situation map in `core.md`: agents load skills reliably only when the always-on text names them.
7. **Delete rules whose mistake can no longer happen.**
8. **Keep it project-agnostic.** Nothing in nstack names a specific project, company, person, PR, or private repo. When a lesson comes from a project, write the general rule ("reset client stores when the user changes"), not the story. Tool and framework names (Next.js, Supabase, Codex) are fine.

Skill layout:

```
skills/<name>/
  SKILL.md          # frontmatter: name (matches the folder), description
  references/       # optional detail, loaded only when needed
  scripts/          # optional helpers, executable
```

Adding a skill has a fixed checklist in [AGENTS.md](AGENTS.md): core map row, directive description, eval case, path rule for file-type skills. `scripts/check.py` enforces it and runs as a pre-commit hook.

Bump `version` in `.claude-plugin/plugin.json` and `marketplace.json` when a change should reach installed copies.
