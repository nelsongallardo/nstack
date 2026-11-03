# Dismissal patterns

These are recurring review comments that are usually noise. Promote `candidate` to `recurring` after several PRs confirm the pattern. None of these ever covers security, auth, data, or migration comments.

Format:

```
### <pattern name>
- Confidence: candidate | recurring
- Dismiss when: <conditions that must all be true>
- Don't dismiss when: <risk boundaries>
- Signal: <phrases that identify it>
- Source: <PR link>
```

### Unused export used later in the stack
- Confidence: candidate
- Dismiss when: the symbol is flagged unused, and a later PR in the same stack uses it. Verify this in that PR's diff.
- Don't dismiss when: it's not a stack, the symbol is public API, or you can't find the later use.
- Signal: "never used", "dead export".
- Source: pstack bugbot-triage

### Temporary duplication during a migration
- Confidence: candidate
- Dismiss when: the duplicate keeps a new path parallel to an old one that a tracked issue or PR deletes.
- Don't dismiss when: the copies already behave differently, or they guard auth, billing, or data access.
- Signal: "duplicated logic", "extract a shared helper".
- Source: pstack bugbot-triage

### Intentional visual change
- Confidence: candidate
- Dismiss when: the PR description or screenshots make the visual change explicit, and the comment only restates that a default changed.
- Don't dismiss when: it concerns accessibility, focus visibility, keyboard navigation, contrast, or a component API contract.
- Signal: comments about spacing, sizes, or outline changes on shared components.
- Source: pstack bugbot-triage

### An invariant already covers it
- Confidence: candidate
- Dismiss when: a shared component, framework contract, type, or single source of truth already guarantees the concern, and you can cite it with `file:line`.
- Don't dismiss when: the invariant is assumed rather than enforced, or it crosses async or state boundaries where values can diverge.
- Signal: "might be null", "missing bound" next to a value with one checked source.
- Source: pstack bugbot-triage

### Owner-declared follow-up
- Confidence: candidate
- Dismiss when: the user explicitly said it's a known follow-up, the PR doesn't make it worse, and it's not high-risk. Link the follow-up issue.
- Don't dismiss when: you're acting without the user's word, or deferring would merge a new regression.
- Signal: "we'll handle that later".
- Source: pstack bugbot-triage
