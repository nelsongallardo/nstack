---
name: cleanup
description: Strip slop from a diff before it is committed or reviewed, such as narrating comments, unsupported guards, dead compatibility paths, debug logs, lint suppressions, and unrelated edits. Use before committing, before opening a PR, on "clean this up before review", "remove the comments", or "deslop".
---

# Cleanup

The extra code is where the next bug hides. Cleanup is not optional polish.

**Run it from a fresh context, not as the agent that wrote the code.** An author defends its own comments. In Claude Code, spawn a subagent that reports only and edits nothing. The parent applies the accepted fixes.

Scope: the branch diff against its merge base, plus uncommitted changes.

## Comments

Delete every comment that isn't on the keep-list. When you're not sure a keep clause applies, delete it.

**Keep-list:**

- Legal or license headers.
- Non-obvious behavior forced by an external dependency, platform, vendor, or protocol we can't reshape.
- `// prettier-ignore`.
- Doc comments that define a public API contract.
- Issue or RFC links that explain a constraint the code can't express.

**Surprises in our own code are not exempt.** A comment explaining surprising behavior in our code is a refactor request. Delete it and flag the symbol for a rename, extraction, type, or restructure that makes the behavior obvious without prose.

`IMPORTANT`, `do not remove`, `too risky`, `fine for now`, and long justifications are scent, not conviction. Check the claim against the live code before keeping one. A long justification with no keep-list reason is a confession.

**Constraint comments** ("must run before X", "talk to Y before changing") get the cheapest encoding instead: a type, runtime check, test, or lint. Then delete the comment. If the encoding isn't done now, report the constraint as open.

Test scripts get no comments narrating their steps. The assertion message documents the step: `assert(ok, 'persisted across restart')`.

## Suppressions

`eslint-disable`, `@ts-ignore`, `@ts-expect-error`, `# type: ignore`, `# noqa`. Look up the rule. If it catches real bugs or protects correctness, remove the suppression and fix the code. A suppression survives only when its rule is faulty, pedantic, or style-only.

## Code

- **Guards for states that can't happen.** Fix the producer or the type instead, then delete the guard. A guard is legitimate only when the state it handles is legitimate.
- Dead compatibility paths, unused exports, and feature flags that are fully on.
- `console.log` and `print` debugging, leftover TODOs with no issue link, and commented-out code.
- Edits unrelated to the change: drive-by formatting and renames. Move them to their own commit or drop them.
- Defensive try/catch that swallows errors. Let errors propagate to the boundary that handles them.

## Report

- Files touched.
- Deletions, by count.
- Flagged symbols, one line each.
- Open constraints.
- What you skipped, and why.

Never bolt on symptom guards while cleaning.
