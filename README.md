# Askalot — Claude Code Plugin

Connect Claude to the **[Askalot](https://askalot.io)** survey research platform. Design questionnaires with mathematically verified logic, build and run campaigns, manage respondents, conduct surveys, and weight and analyse the results — all through conversation.

This repository is the **public, read-only mirror** of the plugin that ships inside Askalot. It is published automatically on each release; the canonical source lives in Askalot's private monorepo. For issues or feedback, contact [info@askalot.io](mailto:info@askalot.io) — pull requests against this mirror are not merged.

## What's in the plugin

| Component | What it gives Claude |
|-----------|----------------------|
| **Agents** | Autonomous sub-agents for the research workflow: **Designer** (research + questionnaire generation), **Manager** (campaign strategy + field supervision), **Analyst** (data quality + research evaluation), and **Respondent** (survey simulation) — each delegating to specialised helpers (QML planning/writing, research assistance/evaluation, quality analysis). |
| **Skills** | Just-in-time methodology and tooling knowledge: survey and questionnaire design, QML syntax and preconditions, sampling theory, validity/reliability, data quality, knowledge-base lookups, and guides for the MCP tools. |
| **MCP tools** | **78 tools across 13 categories** — projects, campaigns, questionnaires, respondents, surveys, pools, sampling strategies, datasets, QML validation (Z3), audit, and documentation search — served by Askalot's Portor API gateway over OAuth 2.1. |

The MCP layer is the only part that talks to your data; the agents and skills are local guidance Claude uses to drive those tools well.

## Requirements

- **[Claude Code](https://claude.com/claude-code)** (CLI).
- An **Askalot account** — sign up at [askalot.io](https://askalot.io). The MCP tools authenticate to your tenant via OAuth 2.1; there are **no API keys to manage**.

## Install (Claude Code)

```text
/plugin marketplace add askalot-io/askalot-plugin
/plugin install askalot@askalot
```

Point the bundled MCP server at your tenant before launching Claude Code:

```bash
export ASKALOT_MCP_URL="https://portor.<tenant>.askalot.io/mcp"
```

Replace `<tenant>` with your tenant identifier:

- `dev` — free trial and demo (ACME Corp organization)
- `eu1` — EU production (paying customers and universities)

On first MCP use, Claude Code opens a browser to log in at `oidc.platform.askalot.io`. The access token is stored and refreshed automatically.

## Use from Claude Desktop or Claude.ai

Claude Desktop and Claude.ai (web) **do not load plugins** — no agents, skills, or slash commands. They connect to the **same MCP server** as a remote *custom connector*, giving you the tool/API surface only:

1. **Settings → Connectors → Add custom connector**
2. **Name:** `Askalot` · **URL:** `https://portor.<tenant>.askalot.io/mcp`
3. **Add** — a browser opens for OAuth login; authorize access.

There is no desktop extension (`.mcpb`) to install — Portor is a remote OAuth server you add by URL. Full walkthrough: **[docs.askalot.io → Integrations → Claude](https://docs.askalot.io/integrations/claude/)**.

## Example prompts

```text
Create a customer-satisfaction campaign with 50 test respondents.
```

```text
Check my new questionnaire for logical errors.
  → validates the QML with Z3 and reports unreachable items or contradictions.
```

```text
Extract and weight the results from my latest campaign, then show the quality delta.
```

## License

[PolyForm Shield 1.0.0](LICENSE) — source-available, **not** an OSI-approved open-source license. You may read, run, and modify the plugin, but not use it to build a competing product. See [LICENSE](LICENSE) for the full terms.

## Links

- **Website:** [askalot.io](https://askalot.io)
- **Documentation:** [docs.askalot.io](https://docs.askalot.io)
- **MCP tool reference:** [docs.askalot.io → API → MCP](https://docs.askalot.io/api/mcp/)
