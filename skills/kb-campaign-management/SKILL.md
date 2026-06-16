---
name: kb-campaign-management
description: Pointer to the public campaign-management guide at docs.askalot.io/guide/campaign-management. Use when an agent or CLI user needs the end-user explainer for campaign creation, pool assignment, invitations, monitoring, and closure. Complements the campaign-strategy and mcp-campaign-tools skills with reader-facing flow context.
disable-model-invocation: false
---

# Campaign Management Guide

The public campaign-management guide lives at
**<https://docs.askalot.io/guide/campaign-management/>**.

Use the live page when:

- A customer or operator is following an end-to-end campaign lifecycle for
  the first time and wants the prose narrative
- You need screenshots of the Targetor UI flow (not present in bundled skills)
- You want to point a non-engineering stakeholder at "how a campaign goes
  live" without exposing the MCP tool surface

The bundled skills cover the agent-facing angle:

- `campaign-strategy` — sampling design, quotas, allocation tradeoffs
- `mcp-campaign-tools` — the MCP tool surface (`create_campaign`,
  `assign_pool_to_campaign`, `send_campaign_invitations`, etc.) the manager
  agent calls to actually execute the plan

When the agent has Askalot MCP access, prefer
`mcp__askalot__get_documentation("guide/campaign-management.md")` over a raw
fetch — it returns the same content with `docs://...` and image links
rewritten for further chaining.
