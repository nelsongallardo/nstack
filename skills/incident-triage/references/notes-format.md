# Notes and patterns format

When the config sets a notes location:

**Incident note** `incidents/<YYYY-MM-DD>-<service>.md`: frontmatter `service`, `severity`, `incident`,
`status`; sections `## Timeline` (`- HH:MM — ...`), `## Findings`, `## Actions taken`, `## Handoff`.

**Patterns** `patterns/<service>.md`, one section per known alert behaviour:

```
## <alert name, or a distinctive substring of it>
verdict: <one line: what to do, e.g. "flapper — wait 15 min" | "real — roll back">
last: <YYYY-MM-DD> · seen: <N>
<2–5 lines: how to recognise it, what fixed it, links to incident notes>
```

Update the pattern at handoff (create if missing, bump `seen`/`last`, refine `verdict`), or right away
on "pattern: …". Patterns record only what happened in real incidents; an invented one will mislead a
future responder at the worst possible moment.
