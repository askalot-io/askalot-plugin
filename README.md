# Askalot — Claude Code Plugin

Connect Claude to the **[Askalot](https://askalot.io)** Research Operating System. Design questionnaires with mathematically verified logic, build and run campaigns, manage respondents, conduct surveys, and weight and analyse the results — all through conversation.

This repository is the **public, read-only mirror** of the plugin that ships inside Askalot. It is published automatically on each release; the canonical source lives in Askalot's private monorepo. Pull requests against this mirror are not merged; report problems in the [public issue tracker](https://github.com/askalot-io/askalot-os/issues).

## What's in the plugin

| Component | What it gives Claude |
|-----------|----------------------|
| **Skills** | Methodology and tooling knowledge loaded when a task needs it: survey and questionnaire design, QML syntax and preconditions, sampling theory, validity and reliability, data quality, campaign simulation, paper authoring, translation, and guides for the MCP tools. Some skills carry role briefs (designer, reviewer, analyst and others) that Claude follows for a multi-step task. |
| **Respondent profiles** | Five text descriptions of example respondents, used when you ask Claude to simulate survey answers. |
| **MCP connection** | One remote MCP server, `https://askalot.io/mcp`, with more than 140 tools: projects, questionnaires and QML validation (Z3), campaigns, respondents and pools, sampling strategies, surveys, datasets and quality measures, the research paper, audit history and documentation search. |

The plugin contains text only: Markdown, JSON and one icon. It ships no hooks, no scripts and no local server, and it runs no code on your machine.

## Requirements

- **[Claude Code](https://claude.com/claude-code)**.
- An **Askalot account** — sign up at [askalot.io](https://askalot.io).

## Install (Claude Code)

```text
/plugin marketplace add askalot-io/askalot-plugin
/plugin install askalot@askalot
```

The first time Claude uses an Askalot tool, Claude Code opens a browser so you can sign in with your Askalot account (OAuth 2.1). There is one address for every account, `https://askalot.io/mcp`; the sign-in finds the environment and organization your work is in. Claude Code stores the access token and renews it; you do not copy any key.

## Use from Claude Desktop or Claude.ai

Claude Desktop and Claude.ai do not load plugins, so they get the tools without the skills. Add the same server as a custom connector:

1. **Settings → Connectors → Add custom connector**
2. **Name:** `Askalot` · **URL:** `https://askalot.io/mcp`
3. **Add**, then sign in when the browser opens.

Full walkthrough: **[docs.askalot.io → Integrations → Claude](https://docs.askalot.io/integrations/claude/)**.

## Data and privacy

Everything the plugin sends goes to Askalot, at `askalot.io` and its subdomains. Nothing is sent to any other party.

- **Tool calls.** When Claude calls an Askalot tool, the tool's arguments go to `https://askalot.io/mcp` and the result comes back into your conversation. The arguments are whatever the task needs: questionnaire text, respondent records you ask it to create, survey answers, analysis settings. Calls act in your account, in the organization your session is working in, with the permissions your account has.
- **Sign-in.** The browser sign-in happens on `askalot.io`. Claude Code keeps the resulting access and refresh tokens on your machine.
- **File uploads and downloads.** To import a document or export a dataset, a tool returns a short-lived signed link on an Askalot address, and the file travels over that link.
- **The REST lane (optional).** For bulk work, two skills (`gateway-routing`, `askalot-setup`) tell Claude that it may write a script that calls Askalot's REST API at `/api/v1` on your Askalot address. That script authenticates with a Personal Access Token you create yourself in Askalot's Profile Settings and pass in the `X-Api-Token` header. The plugin never creates, reads or stores such a token, and nothing uses this lane unless you ask for it.
- **Documentation.** Skills link to `docs.askalot.io`; Claude may read those public pages.

The plugin collects no analytics, and it has no code that reads files, environment variables or credentials on your machine. Claude reads a local file only when you ask it to, for example to import a questionnaire document. How Askalot handles the data it receives is described in the **[Privacy Statement](https://docs.askalot.io/about/privacy-statement/)** and the **[Terms of Service](https://docs.askalot.io/about/terms-of-services/)**.

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
- **Privacy Statement:** [docs.askalot.io → About → Privacy](https://docs.askalot.io/about/privacy-statement/)
- **Support:** [issue tracker](https://github.com/askalot-io/askalot-os/issues) or [info@askalot.io](mailto:info@askalot.io)
