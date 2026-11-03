---
name: catch-me-up
description: Catch the user up on what changed and list everything waiting on them, so they can decide from the reply alone. Also restates a message in plain words, or reconstructs recent work across sessions. Use for "catch me up", "what's left", "what do I need to answer", "repeat the questions", "where are we", "recall my work on X", "say that simpler", or "in your own words".
---

# Catch me up

Assume the user remembers their last message and nothing after it. Notifications, subagent results, and other sessions' reports are not their messages.

This turn is read-only.

## 1. Check the live state

Before writing, check every PR, CI run, deploy, issue, and agent this work touched, using `gh pr view`, `gh pr checks`, and the report files. Check each number you show against its source, and say so when you correct an earlier claim.

## 2. Find the action items

An action item is a call only the user can make: a product choice, an approval, an irreversible action, a login, or access you lack.

- Include items raised before their last message that are still waiting.
- Work you could still do yourself is not an action item. Do it, or say you're doing it.
- Never make up a call to fill the reply.
- Never cut items to stay short. No count in place of a list, and no link in place of an item. The reply alone must be enough to decide.

## 3. Write it

1. **One sentence** naming what's waiting on the user, or "nothing is waiting on you".
2. **What happened**, under ~100 words. One bullet per thing the user asked for, with its state, phrased the way you'd say it out loud: "Search was slow from a missing index; fixed and merged", not "Search review: done". Never mark something done that still waits on the user.
3. **Action items**, riskiest first, about 30 words each:
   - The call, plus your pick.
   - What must happen first, or can't be undone.
   - The risk, even when it's low ("Low risk: only the colors change").
   - Phrase each as a question they can answer in one line. Never ask for a shorthand token to type back.

Say "the tests pass", not "CI is green". Leave out hashes, paths, commands, and build numbers unless the user needs one to act. Call each PR or branch by a name the user would know.

## Across sessions ("recall my work on X")

1. **Lock the scope first:** window (default 7 days), topic, repo. State it back. Never quietly turn "all" into "recent".
2. Search transcripts by modification time, grepping for the topic first: `~/.claude/projects/<slug>/*.jsonl` and `~/.codex/sessions/`. Parse them in subagents, since raw transcripts stay out of the main thread. From each, take the goal, decisions, open threads, corrections, and artifacts.
3. Also sweep the shared record: GitHub issues and PRs, the decision log, and the docs repo's open questions.
4. **Output:**
   - **Capsule**: 5 bullets at most.
   - **Threads**, each tagged with exactly one of `[merged #N]`, `[open PR #N]`, `[in flight <branch>]`, `[verified, uncommitted]`, `[reverted #N]`, `[planned, not started]`. A thread with no tag isn't done yet.
   - **Problems**, including reverted fixes, so the next attempt starts where the last one failed.
   - **Next move**: one, concrete.
   
   Cut detail before cutting threads.

## Restate

- **In your own words:** restate what you think the user's goal is and what problem they're solving. A misreading shows up before any code exists.
- **Simpler:** restate the last message without jargon, shorter, the way one person talks to another.
