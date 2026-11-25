# On-call config: <rotation name>

Copy to `ONCALL.md` in the repo, or `~/.config/oncall/<rotation>.md`. Delete sections that don't apply.
Write it for an agent: concrete names, IDs and paths beat prose.

## Coverage
- Rotation: <name>. Shift: <hours, timezone>. My role: <primary | secondary>.
- Covered: <e.g. "Tier 1 and 2 only at night"; "all services in the payments group">.
- Not covered → <what to do: ack and defer to day shift, reroute to X>.

## Where things are
- Alerts / incidents: <PagerDuty / Opsgenie / ... ; MCP server or CLI name>
- Metrics, logs, traces: <tool and how to query, e.g. "mcp__grafana__*", "datadog CLI">
- Deploy / change history: <tool, or "git log on <path>">
- Cloud status: <provider status source>
- Service catalog (service → owner, tier, runbook): <file path or URL>
- Escalation (who to page per team): <file path or URL>
- Runbooks: <location pattern, e.g. "<service>/docs/runbook.md">
- Incident process / playbook: <path or URL>

## Channels
- Alerts: <#channel (ID)>   Team: <#channel (ID)>   Incident: <#channel (ID)>

## Notes
- Notes location: <directory, e.g. ~/notes/oncall/> (holds incidents/, patterns/, briefs/, summaries/)

## Related skills / helpers
- Root cause: <skill name>   Severity: <skill>   Pods/deploys: <skill>
- Bots that can investigate: <e.g. "@ops-bot in the alert thread">

## House rules
- <e.g. "read wrapped.md before any Wrapped page">
- <e.g. "never roll back service X without paging its owner">
- <custom verdict format, if any>
