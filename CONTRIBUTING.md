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
5. **Size limits.** `SKILL.md` stays under 150 lines, with detail in `references/`. `core.md` stays under ~50 lines.
6. **Descriptions decide triggering.** Name the situations and the phrases a user would actually say.
7. **Delete rules whose mistake can no longer happen.**
8. **Keep it project-agnostic.** Nothing in nstack names a specific project, company, person, PR, or private repo. When a lesson comes from a project, write the general rule ("reset client stores when the user changes"), not the story. Tool and framework names (Next.js, Supabase, Codex) are fine.

Skill layout:

```
skills/<name>/
  SKILL.md          # frontmatter: name (matches the folder), description
  references/       # optional detail, loaded only when needed
  scripts/          # optional helpers, executable
```

Bump `version` in `.claude-plugin/plugin.json` when a change should reach installed copies.
