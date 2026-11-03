---
name: decision-log
description: "The user's own way to record decisions, assumptions, and open questions: a per-run TSV trail and durable records linked to PRs. Load for 'document this decision', 'add the assumptions/open questions', long or unattended runs, or any decision someone will review later."
---

# Decision log

There are two layers. The **trail** is raw, per run, and local. The **record** is durable, curated, and shared. Promote from trail to record. Don't dump the trail into the record.

## 1. The trail (per run)

Append rows with `scripts/log.sh <file> <phase> <decision> <why> <evidence> <result>`. The script stamps UTC time, keeps cells on one line, and neutralizes spreadsheet formulas. Columns: `ts phase decision why evidence result`.

- **File:** `decisions.tsv` at the worktree root, or `.audit/<task-slug>.tsv` when several efforts run at once. Gitignored by default.
- **Log:** forks chosen, units completed with their verification result, pivots or reverts with their trigger, blockers surfaced, gates fixed. Don't log every action.
- `evidence` is a pointer: a SHA, PR #, `file:line`, or artifact path. Never a paragraph.
- `result` is an outcome: `tests green`, `reverted`, `INCONCLUSIVE`, `open`.
- Write it in plain words: `threw out a helper's work because its screenshots were blank | checked the real files instead of its summary`.
- Append only. A wrong call gets a new row that supersedes it. Never edit old rows.
- **Several sessions, one log** (parallel Claude/Codex panes): a session joining an existing log reads the last rows, then writes a `phase=start` row naming its session and the range it didn't write.
- View it with `column -s$'\t' -t < decisions.tsv`.

**Commit the trail** only when the work is ambitious enough that a reviewer needs the trail to trust the result: a big migration, a port, an overnight run.

**Before handing back:**

1. Walk the rows against what actually happened. Every row is a real decision, every pointer resolves, and unlogged forks get added. Correct the log, not the story.
2. Seek an independent review of the trail when a consequential decision still rests on uncertain evidence or conflicting records. Give the reviewer the relevant rows and artifacts to check for unsupported claims and gaps. Duration alone does not require another model.
3. If independently reviewed, end the reply with **Attention:** `reviewed by <model>`, then the flags pointing at rows. "No flags" is a valid value. Otherwise report unresolved evidence gaps directly without implying an independent review occurred.

## 2. The record (durable)

This is where decisions, assumptions, and open questions live for the team. Find the project's place:

1. Look for the project's docs location for decisions: a `docs/decisions/` or ADR folder in the repo, a separate knowledge/docs repo, or an open-questions doc.
2. If the project keeps several places (technical docs in the repo, non-technical material in a knowledge repo, status in GitHub issues), put each item in its home.
3. Check the user's personal rules about where project state may or may not be written before writing anywhere outside the repo.

**Entry shapes:**

```
### <Decision title>  (decided YYYY-MM-DD)
Decision: <one sentence>
Why: <the reason, with evidence or "assumption">
Alternatives: <rejected, one line each>
Implemented in: <PR links>
Revisit if: <the condition that would change it>
```

```
### <Assumption>  (status: unconfirmed | confirmed by <who> YYYY-MM-DD | rejected)
Assumption: <what we're acting as if were true>
Risk if wrong: <concrete consequence>
Implemented in: <PR links that depend on it>
Ask: <the exact question, and who can answer it>
```

- Each claim gets an evidence label: **Direct** (someone wrote the reason), **Supported** (several items agree), **Inferred** ("given A and B, C seems likely"), **Speculative**, or **Unknown** (say what was searched).
- Write each open question so the person can answer it without context: one question, a default you're acting on, and the risk.
- Keep review light for the people asked. Group questions per reviewer, put the riskiest first, and ask for a reply, not a checkbox per item.
- Link every PR that implements a decision or depends on an assumption. When an assumption is confirmed or rejected, update its status and open follow-up issues for any PR that now needs changing.

## Reply

- What was recorded, with links.
- Open questions and who they're waiting on.
- Any trail **Attention** flags.
