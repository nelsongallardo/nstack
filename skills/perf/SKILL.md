---
name: perf
description: "The user's own rules for performance work: baseline, the mantras, one change per measurement, and the seven questions before reporting any number. Load for 'slow', 'optimize', 'latency', 'N+1', benchmarks, or any before/after number."
---

# Perf

Don't read source instead of measuring. Every change is tied to a measurement. Never claim a win from code inspection.

## 1. Ground the workload

Name what moves the metric: data size, history, state, concurrency, cold vs warm. Pick a case that reproduces the complaint. If no case reproduces it, fix the repro before optimizing anything.

Write the decision down before you run: what result would change what you do, and what the noise floor is.

## 2. Baseline

- Take a baseline trace or profile first.
- Prove the harness is sensitive: two workloads that should differ must measure differently. If they don't, revise the workload or the metric. Then freeze the harness.
- Use the median of N runs, interleaving A and B.
- Record a green regression gate (the tests that must stay passing).

## 3. Try the mantras in order, cheapest first

Stop at the first one that meets the target.

1. Don't do it. Stop work whose result nothing uses, rather than making it cheaper.
2. Do it, but don't do it again (cache, memoize, dedupe the N+1).
3. Do it less (batch, paginate, narrow the query).
4. Do it later (defer off the critical path).
5. Do it when they're not looking (prefetch, background).
6. Do it concurrently.
7. Do it cheaper (algorithm, index, micro-optimization).

## 4. One change, one measurement, keep or revert

- Name a mechanism in each hypothesis. Write "defer X off the boot path because it blocks first paint", not "try memoizing something".
- Accept a change only when the metric moves past the noise floor and the gate stays green. Otherwise revert all of it. Never stack untested changes.
- Make one commit per accepted win, staging named files only.
- For a long run, keep a gitignored `decision.tsv`, one row per attempt: `id, hypothesis, change, before, after, delta, tests, verdict, note`. Read it before each attempt.
- Stop when the target is met across repeated measurements and the regression gate passes. Confirm an apparent early win with the frozen harness; do not require more optimization attempts once the result holds.
- At a plateau, switch to a different category of fix, combine near-misses, or re-read the source. Correctness and simplicity outrank the number. Revert a win that breaks behavior. Keep a simplification that holds the number.
- Stop honestly. Don't relax the target to meet it.

## 5. Vet the number before you report it

Answer each question with evidence from a run:

1. What limits the number, and why isn't it double? A guess from reading the code is not a limiter.
2. Did every side run tuned the way production runs (same build mode, same cache state)?
3. Does the result break a physical limit, such as disk bandwidth or core count?
4. Did anything error, or return wrong output?
5. Does it reproduce over alternating runs? Give the median and the range.
6. Does it matter end to end, on the path a user waits on?
7. Did the work actually happen inside the timed region?

The verdict is **faster**, **slower**, **no measurable difference**, or **inconclusive**. Report it with the run count, range, and limiter. It's inconclusive when you can't name the limiter, or when one side ran untuned. Don't claim a ratio between unlike scenarios.

## Reply

- Baseline → result, with range and run count.
- The limiter.
- What changed and why it worked.
- Artifact paths.
- The best idea you'd try next if pushed further.
