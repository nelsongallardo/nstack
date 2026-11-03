---
name: writing
description: Write technical prose people act on, such as READMEs, docs, runbooks, ADRs, PR descriptions, commit messages, issue bodies, and agent-facing instructions (skills, AGENTS.md). Use when writing or reviewing any of those. For general prose style, pair it with the humanizer skill.
---

# Writing

Write so a tired engineer understands it on the first read. A sentence that follows every rule but sounds machine-written has failed. Fix it some other way.

## Pick the mode first

Every doc is one of these. One document, one mode. Split and link rather than mixing.

| Mode | Serves | Examples |
|---|---|---|
| Tutorial | Learning by doing | Onboarding, first-run guide |
| How-to | A task at hand | Runbooks, "how to add a migration" |
| Reference | Lookup while working | API, config, CLI flags. Only describe, and mirror the structure of the thing described |
| Explanation | Understanding | ADRs, design rationale. The only mode where opinion belongs |

## Words

- **The codebase is the word list.** Write the real symbol, file, flag, or command, not a synonym or description: "`budget.mjs` reads `budget.json`", not "the budget script reads its config".
- **One name per thing, everywhere.** "The gate", "the ratchet", and "the budget check" for one thing teaches three things.
- No invented jargon: "move", not "evacuate"; "a budget that only goes down", not "ratchet". No abstract metaphor nouns (substrate, vector, primitive, surface, flywheel, north star).
- Be specific, not sterile. Write "a column rename fails the build", not "schema changes can cause issues". If a sentence could appear unchanged in another project's docs, it says nothing about this one.
- Name the mechanism or a number, not a feeling.

## Sentences

- One thought per sentence. Split a sentence carrying two thoughts. Keep a long sentence that carries one.
- Put the condition before the instruction: "To delete the document, click Delete."
- Never write "simply", "just", or "easy" in a procedure. If it were simple, the reader wouldn't be there.
- Keep "only" and "not" next to the word they modify. Break up noun stacks: "the script that checks the proto-import budget", not "the proto import budget check script". Never let "this" point at a whole clause.
- Don't over-compress. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing."
- Headings carry the point: "Pick the mode first", not "Modes".

## Before and after

> Configuration of the proto import ratchet budget script parameters is performed via budget.json. Note that it's important to remember that running with --write should only be done when lowering it. If exceeded, CI fails.

> `budget.mjs` reads the committed budget from `budget.json` and counts the files that import protos. If the count exceeds the budget, CI fails. Run `budget.mjs --write` only to lower the budget.

## PRs, commits, issues

- A PR body is a briefing a reviewer reads in under a minute. Use the `preflight` structure. Link logs, SHA lists, and metric tables. Don't paste them.
- Make every count or claim true at the commit that lands it. Include the command that regenerates it.
- Bug-fix PRs: repro steps, root cause, before and after evidence, blast radius.
- Issue titles state the symptom, never a guessed cause.
- Commit subject: `type(scope): imperative summary`. The body explains why, and doesn't restate the subject.

## Agent-facing prose (skills, AGENTS.md, briefs)

Agent-facing prose has a higher bar than human prose, because every unhelpful sentence becomes an instruction some future agent follows.

- Prefer a concrete rule with its trigger ("when X, do Y") over a value ("be careful with X").
- "Communicate clearly" is not a rule. "Short paragraphs. Tables when comparing options." is.
- Cut anything a mechanism (a lint or script) could enforce, and build the mechanism instead (`learn`).
- A skill's `description` decides whether it ever fires. Name the situations and the phrases a user would say.
