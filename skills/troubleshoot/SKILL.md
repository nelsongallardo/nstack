---
name: troubleshoot
description: "The user's own procedure for problems in running systems: intake from a link, where to start by problem type, a cited root-cause chain, and a note to park and resume. Load when something is wrong in production, a deploy, CI, or a data pipeline: the user pastes an alert, dashboard, CI run, deploy, ticket or chat-thread link, or a production log line, and asks what's wrong or why; says 'troubleshoot', 'root cause', 'dig'; or says 'resume', 'park', 'close' or 'pattern:' about an investigation. Also the root-cause step after incident-triage."
---

# Troubleshoot

Find out what is wrong in a running system and why, with evidence that holds up in an incident review. Say what you know early, then go deep. This is read-only: you diagnose, the user decides anything that changes production.

Lanes: when the cause turns out to be in code, load `debug` to reproduce and narrow it, and stay diagnosis-only unless the user asks for a fix. For "why was it built this way", load `investigate`. Label claims with `investigate`'s tiers (Direct, Supported, Inferred, Speculative, Unknown).

## Context

Tools, ownership, chat and the notes location come from the project: CLAUDE.md / AGENTS.md, `ONCALL.md` or `.oncall/config.md` in the repo, or `~/.config/oncall/*.md`. Without one, discover what's connected (MCP servers, `gh`, `kubectl`, cloud CLIs, runbooks in the repo) and say in one line what you couldn't reach. Read known-issue notes (patterns, runbooks, past incidents) for the component before concluding; they tell you where to look first, not the answer.

## 1. Intake

1. Read the input: a link, pasted logs, or text. When resuming, read the note and continue from its "Next step".
2. Classify as a starting guess: `service`, `deploy`, `ci`, `data`, or whatever fits. Reclassify, and say so, when evidence points elsewhere.
3. Start a note if the project has a notes location (format below).

## 2. Where to start

Suggestions, not a checklist. Batch independent lookups, follow what looks anomalous, drop what doesn't apply.

- **service**: error and latency breakdowns, log patterns, traces, recent deploys and config changes, dependency health.
- **deploy**: the failing stage and its logs, canary metrics, whether the old version still serves, whether the same change failed elsewhere.
- **ci**: the failing step's log, whether the base branch fails too, flakiness history, what the change touched.
- **data**: job status and logs, late or wrong upstream inputs, downstream consumers and their deadlines.

## 3. First report

```
🔍 <slug> · <type> · <component or area>
Symptom:  <what is wrong, since when>
Cause:    <best current hypothesis> · confidence low|med|high · evidence: <1 line>
Next:     <ONE next step, mine or theirs>
Owner:    <who should act>
```

Then up to ~6 evidence bullets with links. Run any read-only check you'd list as "Next" before replying; a menu of investigations hands your work back to the user.

## 4. Root cause

**Start from what the user brought.** A pasted error or trace is the thread to pull. Measure it: count over a stated window, first occurrence, still happening or not, and the affected slice (region, client, endpoint, tenant, version). A low aggregate error ratio is not a reason to call the user's evidence noise.

**Trace from trigger to failure, one cited hop at a time.** Hops depend on the problem: request through each service step, inputs through transforms, deploy stages, change to failing test. Cite a `file:line` you opened, a log query, a metric or a config for each. Find out what is upstream instead of assuming, and explain why it started *then* by lining a change up against the first occurrence and checking that the change touches the failing path.

**Stop** when every hop is Direct or Supported, when you reach a source you can't read (name it and its owner), or when another hop wouldn't change the conclusion or who acts. Don't ask whether to continue before that.

```
🔬 Root cause · <component> · <problem in plain words>
Count:    <N over window, first seen, still happening?, affected slice>
Source:   <who/what triggers it> — evidence: <link or query>
Chain:    1) <hop> → 2) <hop, with file:line / query> → … (one hop per line)
Trigger:  <what changed and when> — <tier>
Open:     <what's unproven and which source would settle it>
```

No fix proposals unless asked; at most one line under "Open".

## Safety

- Rollbacks, deploys, reruns, scaling, flag changes, ticket transitions and messages: prepare the exact step, show it, wait for an explicit yes.
- Messages are drafts unless the user says send.
- Don't call something fixed without a metric or test showing it.

## Note and commands

`issues/<YYYY-MM-DD>-<slug>.md` under the notes location. Frontmatter `type`, `status` (open | parked | closed). Sections: `## Symptom`, `## Hypotheses` (✅ confirmed / ❌ ruled out + why), `## Evidence`, `## Next step` (one line), `## Timeline` (`- HH:MM <what>`), `## Outcome`. Update it after each meaningful step so a fresh agent can resume without redoing work.

- `park`: write enough state to resume from the note alone; `status: parked`.
- `close`: fill Outcome (cause, fix, follow-ups), `status: closed`, offer a reply draft for the thread or ticket and a `pattern:` if the lesson will recur.
- `pattern: <lesson>`: append to `patterns/<component>.md` under `## <symptom>` with verdict, signal to check, date. Only what actually happened.
- `handoff`: a chat-ready draft (symptom, cause, status, next, owner).
