---
name: debug
description: "The user's own debugging procedure: recorded state first, reproduce on the user's surface, runtime evidence, fix at the root, what to do after two failed fixes. Load for any bug, error, failing test, leak, flaky behavior, 'still broken', 'why is X happening', or a stack trace."
---

# Debug

Ship only lines that trace to runtime evidence. A fix that "might help" is a hypothesis, not a fix. When evidence refutes a hypothesis, revert everything it motivated.

## 1. Inspect recorded state first

Before forming a theory, read what the system already recorded: logs, DB rows, queues, registries, state files, deploy and runtime logs from the hosting and database providers, CI logs. Follow the evidence. Don't fit it to a hypothesis.

- If it fails only after a restart, suspect persisted state first.
- A contradiction is evidence against your model. Trace the actual routing and data flow before proposing anything.
- Before changing state, find its readers, writers, caches, and persistence timing. Never delete sessions, clear overrides, disable features, or toggle settings to hide an unexplained symptom.

## 2. Reproduce on the surface the user hit

Reproduce it yourself, on the same surface: the same endpoint, page, CLI command, or job. Ask the user to reproduce only when there is a specific, stated reason you can't reach that surface.

If it won't fire, synthesize the trigger, tighten the conditions, or add instrumentation until it does. When a cheap local test path exists, write and run the failing repro before the fix. Include the regression test and fix together in a landable commit.

## 3. Narrow by runtime evidence

- Seed hypotheses from how the subsystem works and from its history: `git log -S '<symbol>'`, `git log -L :<fn>:<file>`, recent `fix:` commits in the area.
- Binary-search. On each pass, take the split that cuts the most remaining problem space, get runtime evidence, and eliminate.
- Instrument the live process instead of theorizing from source:
  - Node: `--inspect` + CDP, `--cpu-prof`
  - Python: `py-spy dump`
  - Postgres: `EXPLAIN ANALYZE`, `pg_stat_activity`
  - Temporary structured logs
- Confirm the surviving mechanism with runtime evidence before you design the fix.

## 4. Fix at the root

- Ask "why" until the answer is a wrong decision in the code, not a consequence of an earlier one. Fix it there.
- Guards, retries, swallowed errors, clamped values, and discarded state are the usual ways to hide a bug. A guard is a fix only when the state it handles is legitimate.
- If a workaround needs a paragraph-long comment to justify it, the code is wrong.
- Fix the pattern, not only the instance. Grep for siblings of the same mistake.
- Don't widen a deliberately narrow condition. A fallback gated on "binary not installed" (`ENOENT`) must not become "any non-zero exit", which would hide the real error behind the fallback's error.

## 5. When fixes keep failing

After two failed fixes in one direction, or repeated corrections from the user, stop stacking fixes.

1. Write down the premise the failed fixes share.
2. Find an observation that would come out differently if the premise were false, and make it. Look at how the failures are distributed, not only how large they are.
3. State what you don't know, collect fresh evidence, and re-derive the diagnosis.

When the user rejects a diagnosis, stop repeating it. Find the conflicting evidence and investigate another explanation. The user is authoritative about intent. Technical causality still needs verification.

## 6. Verify on the same surface

Rerun the original repro on the same surface. Unit tests show branch behavior, not that the bug is gone. An inconclusive result, or a check on the wrong surface, is not a pass, so say so.

If the deciding fact took a deep dig to find, propose the cheap, always-on signal that would have shown it at first look, such as a log field, metric, or error code.

## Captured artifacts (profiles, traces, heap snapshots)

- The artifact is a fixed dataset. Read it, don't re-run it.
- Make it queryable before reading: dump it into sqlite, one row per sample, frame, or node.
- A frame with no source mapping is not yet a diagnosis. Resolve the symbols or say they're missing.
- Without a paired before/after capture, call the result "the strongest hypothesis the artifact supports", not a confirmed cause.
- Map the finding to the file, symbol, and line that allocates or schedules. Diagnose only unless asked to fix.

## Reply

- Root cause, with its evidence.
- The fix.
- The failing-then-passing repro output, verbatim.
- What you ruled out.
- Any signal worth adding.
