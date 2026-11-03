---
max_turns: 40
timeout_seconds: 600
allowed_tools: [Read, Glob, Grep, Skill, Write, Edit, Bash]
tags: [activation]
---

You are a worker session started by a coordinator. Brief. Goal: profiles need a display name. Done when: npm test passes and PR.md holds the PR title and body. Scope: src/profile.ts, test/, supabase/migrations/ only. Method: 1) add a migration that adds a nullable text column display_name to public.profiles; 2) extend the Profile type and parseProfile to carry displayName; 3) write a red-first test for it, then make it pass; 4) commit; 5) write PR.md. Do not push. Report: what you built and the test output.
