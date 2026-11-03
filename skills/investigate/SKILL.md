---
name: investigate
description: "The user's own procedure for how/why questions: code anchors, evidence categories, labeled claims, no code changes. Load for 'how does X work', 'why is it built this way', 'why this number', 'when did this break', 'are we sure', or before changing unfamiliar code."
---

# Investigate

This is read-only. Change no code. An agent that edits without a traced model fixes the symptom at the first plausible spot. Investigating first is cheaper than the second bug.

- **How** questions (what it does, where it lives, which layer owns it) → section 1.
- **Why** questions (why this shape or number, regressions, postmortems) → section 2.
- Use **why first, then how** when you suspect the history explains the mess.

If the user embeds a guess ("I assume it's for performance?"), treat it as a lead to investigate, not a conclusion to confirm.

## 1. How

1. **Size it.** Start with one focused pass. Use read-only explorers when independent areas need separate investigation or unresolved uncertainty warrants another perspective. Give each a distinct question; a cross-cutting topic alone does not require multiple agents.
2. **If delegated, each explorer returns:** Components, Flow, Files Read, Boundaries, Non-obvious things, Open questions.
3. **Merge delegated findings yourself.** Resolve contradictions by checking the code.
4. **Answer format:**
   - Overview: someone can read only this and decide whether to keep reading.
   - Key concepts.
   - How it works: prose with real `file:function` references. Write "`UserService` calls `AuthClient.refresh()`", not "the service delegates to the client".
   - Where things live.
   - Gotchas.

## 2. Why

**Build the code anchor first**, before spawning anything, and give it to every investigator:

```
git blame -L <s>,<e> <file>
git log --follow -p -- <file>            # and --oneline -20 for PR numbers
git log -S '<exact string>' -- <file>    # pickaxe: when did this literal appear
git log -1 --format=%B <sha>
gh pr view <n> --json title,body,comments,reviews,closingIssuesReferences
rg -n -C2 '(TODO|FIXME|HACK|NOTE)' <file>
rg -l '<symbol>' --glob '*test*'         # tests encode the edge cases that motivated a change
```

**Search every evidence category.** Delegate independent searches only when the scope or unresolved uncertainty warrants it:

- Source control and PR reviews (always).
- The issue tracker: the business forcing function. Parent issues carry the why, sub-issues are tactical.
- The decisions, assumptions, and open questions in the project's docs or knowledge repo.
- Long-form docs. Specs are rarely updated after implementation, so doc-vs-code drift is a finding.
- Observability, analytics, and error tracking (hosting, database, and product-analytics logs): the runtime reality behind timeouts, retries, and clamps. If a p99 just before the PR matches a threshold constant, the number came from data.

Skip a category only with a written reason (no access, or provably irrelevant). Document the null, don't skip the search. An empty search is a finding.

If the target looks defensive (a null check, retry, timeout, rate limit, or flag), search for incidents: reverts, "add defensive check" commits, and re-applies.

**Investigator rules:**

- Boring and exact beats plausible. One verbatim quote with a precise citation is worth more than a paragraph of summary.
- Mechanics are not motivation. "limit 50→100" shows the change, not why.
- No silent substitutions. Evidence about Y is not an answer about X.
- If three items line up and a fourth contradicts them, the contradiction is the most interesting finding.
- Before calling a finding strong, ask whether you'd expect to find it even if your reading were wrong.

## 3. Label every claim

Each claim sits in exactly one tier:

| Tier | Phrasing |
|---|---|
| **Direct** | Someone wrote the reason down. "This exists because X." Cite it. |
| **Supported** | Several indirect items agree. "The evidence points strongly to X: …" |
| **Inferred** | "Given A and B, C seems likely because D." |
| **Speculative** | "One possibility is X, but we have no direct evidence." |
| **Unknown** | "We searched A and B, scanned the 6 PRs that touched this file, and grepped for the threshold. None surfaced a rationale." |

- "Because", "was designed to", "fixes", and "the team decided" need an adjacent citation. Never use them for inferences.
- Don't use "obviously", "clearly", "of course", or "just". They hide uncertainty.
- Absence of evidence is not evidence of absence.
- A consistent pattern may just be copy-paste, so don't retrofit a clean rationale onto it.
- When sources contradict each other, show both.
- Never cite code as evidence of its own intent.

## 4. Why-answer format

- **The question**
- **The code in question** (2 to 3 lines)
- **What we found**: Direct and Supported claims, cited.
- **What we can reasonably infer**: Inferred claims, with the reasoning.
- **Competing hypotheses**: each with evidence for and against.
- **What we don't know**, including who would likely know.
- **Sources consulted**: one line per category, including "not searched: <reason>".
- **Confidence**: 1 to 2 sentences.

If the question precedes a change, end with a **Preserve / Change / Avoid / Risk** list for the change.

The value of this output is its honesty, not its authority. A gap filled with a confident guess actively harms the user, because they'll act on the guess.

## Explaining to a person

Give the smallest complete answer first, then stop. With three or more moving parts, use a sequence of small diagrams that each add one part, not one big diagram at the end. Keep the hedges when rewording: they are findings, not style.
