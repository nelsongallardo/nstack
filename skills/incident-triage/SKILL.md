---
name: incident-triage
description: "The user's own procedure for on-call incident triage: a one-glance verdict (impact, status, tested cause, one action, who to escalate to), a per-rotation config for tools and ownership, read-only until the user says yes. Load when the user got paged, pastes an alert or incident link or ID (PagerDuty, Opsgenie, incident.io, Grafana, Datadog, Sentry, CloudWatch), says 'triage', 'oncall', 'is this real', 'what's on fire', or asks for a pre-shift 'brief', end-of-shift 'summary', 'handoff', a 'drill', or to record a 'pattern'."
---

# Incident triage

The reader may have just been woken up. In one glance they need: is this real, how bad, what do I do
now, and who do I wake up. You are the investigator; they decide anything that changes production.

## 0. Load the rotation config

Everything environment-specific (tools, channels, runbooks, ownership, coverage rules, where notes go)
lives in a rotation config, so this skill works for any team. Look for it in this order:

1. A path the user gives, or one named in their CLAUDE.md / AGENTS.md.
2. `ONCALL.md` or `.oncall/config.md` in the current repo.
3. `~/.config/oncall/*.md` (if several, pick by the alert's service or ask once).

If none exists, don't block a live page on setup. Triage with whatever you can discover (connected
MCP servers, CLIs such as `kubectl`/`gcloud`/`aws`/`gh`, runbooks or `docs/` in the repo), mention in one
line that no config was found, and afterwards offer to write one from `references/config-template.md`
using what you learned.

The config may also include house rules (coverage tiers, mandatory steps, banned actions). Follow them
over the defaults here.

## 1. Triage a page

### Questions to answer

In whatever order the evidence suggests:

1. **Is it ours right now?** Service, owner, severity/tier, and whether this shift covers it (per config).
   If it isn't covered, say so on line 1 and recommend ack-and-defer unless user impact is obvious.
2. **Is it real, and how big?** Still firing? The service's key signals (errors, latency, saturation,
   traffic) against normal, and the trend: rising, flat or recovering. Who or what is affected.
3. **Seen before?** Check the pattern notes and the runbook for this alert. A known pattern is a strong
   prior that can short-circuit most of the work, but confirm it against live data.
4. **Bigger than this service?** Other firing alerts, upstream dependencies, cloud-provider status. If
   many things are red at once, the cause is probably shared; say that instead of triaging one leaf.
5. **What changed?** Deploys, config or feature-flag changes, traffic shifts, dependency changes,
   infra events near the start time.
6. **What should the human do right now?**

### How to investigate

Use whatever read-only tools the environment offers. Start with a broad parallel sweep (independent
lookups cost nothing extra when batched), then follow what looks anomalous and drop what clearly
doesn't apply. Many observability platforms have their own automated investigation; if one is
available, start it early and check back.

Aim for a first verdict within a few minutes. If something important is still unknown, give the
verdict with honest confidence and keep digging rather than holding it back.

### Verdict

Lead with this block, nothing above it:

```
🚨 <service> (<severity/tier>, <owner>) — <alert in plain words>
Impact:   <who/what is affected, how much; "none visible" is a valid answer>
Status:   <still firing? trend: rising / flat / recovering>
Cause:    <tested hypothesis, or "unknown — testing <X>"> — confidence <low|med|high> — evidence: <1 line>
Do now:   <ONE action: wait & watch N min | roll back <change> | follow runbook step X | escalate>
Escalate: <who to page + where>
Runbook:  <link, or "none found">
```

A stable shape lets a half-asleep reader find the line they need without reading prose. If the config
defines its own verdict format, use that instead. If a known pattern matched, say so in `Cause:`.

After the block, up to ~5 bullets of the strongest supporting evidence. If you can think of a read-only
check that would sharpen the verdict, run it and fold in the result instead of suggesting it; a menu of
investigations at 3am is a chore, not help. End with a question only when it asks for a write action.

### Hypotheses vs. causes

Correlation in time is the classic trap. A deploy, flag flip or traffic spike near the start is a
hypothesis until tested: compare the change against the last good state, and check that errors actually
begin at the change and in the paths it touched. If you can't test it, say "unknown — testing X" with
low confidence. That beats a confident wrong answer that sends the responder down the wrong path.

### Record it

If the config defines a notes location, append a timestamped entry to the incident note (format below),
creating it on first triage. If not, keep the timeline in the conversation and offer it at handoff.

## 2. Root cause

After the verdict the question often becomes *why*: the user pastes logs or a trace, asks why, says
"dig", or the alert resolved but errors continue. Switch without asking: load `troubleshoot` and follow its
Root cause section, passing along what you've gathered so nothing is fetched twice. The safety rules below
still apply.

## 3. Other modes

Run these when asked. Adapt to what the config provides; skip parts with no data source.

- **Brief** (pre-shift): what's firing, open incidents and handovers, risky recent changes to the
  most critical services, provider incidents, and a compact table of covered services (owner, runbook,
  escalation). Write it to the notes location if configured; reply with ~5 lines.
- **Summary** (end of shift): pages (time, service, verdict, action, outcome), what's still open, and
  **runbook gaps**, places where the runbook was missing, wrong or outdated for what actually happened.
  Gaps are the most valuable output because they make the next shift easier. Draft (don't send) a
  team message; offer doc changes for each gap and make them only after a yes.
- **Handoff**: what happened, current state, what the next shift should watch, ready to paste into
  the team channel. Update the pattern for the alert (see Patterns).
- **Drill**: pick a resolved page from the recent past, present it as if it just fired with the
  outcome hidden, let the user drive using only data up to the alert time, then reveal and compare.
  Log the lesson and offer to turn it into a pattern.

## Safety rules

Firm, because a wrong write during an incident costs far more than a slow one.

- **Read-only by default.** Rollbacks, deploys, scaling, restarts, flag changes, merges, posting
  messages, changing incident state: prepare the exact command or step, show it, and wait for an
  explicit yes.
- Messages to people: drafts only unless the user says send.
- Don't call something fixed without a metric showing recovery.
- If a source is unavailable (auth, missing runbook), say so in one line and continue with what exists.
- Ask a clarifying question only when you genuinely can't identify the service.

## Notes and patterns

When the config sets a notes location, keep an incident note per page and a pattern file per service.
The formats are in `references/notes-format.md`; read it before writing either. Update the pattern at
handoff, or right away on "pattern: …". Patterns record only what happened in real incidents; an invented
one will mislead a future responder at the worst possible moment.
