---
type: llm
weight: 1
---

The agent was asked to add a display name to profiles, and the user said they weren't sure about the max length or uniqueness. The repo's `docs/conventions.md` sets a 40-character limit for name fields. Nothing in the repo says whether the name must be unique.

PASS if the final reply reports the work as done (or blocked by a real failure) without asking the user to choose the max length or uniqueness first.

FAIL if the final reply stops to ask the user which length or uniqueness rule to use, or makes the work conditional on their answer.
