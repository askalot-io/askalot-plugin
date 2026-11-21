---
name: kb-getting-started
description: Pointer to the public getting-started guide at docs.askalot.io/getting-started/quick-start. Use when an agent or CLI user is new to Askalot and needs an end-to-end onboarding overview — what the platform is, how to connect, and how to take a first survey live.
---

# Getting Started

The public getting-started guide lives at
**<https://docs.askalot.io/getting-started/quick-start/>**.

Use the live page when:

- The customer has just installed this Claude Code plugin and wants the
  product-level orientation (vs. the install-and-sign-in guidance in the
  `askalot-setup` skill)
- You need the canonical glossary entry for an Askalot concept (Project,
  Campaign, Pool, Sampling Strategy, Questionnaire, Survey, Dataset) —
  see also `docs.askalot.io/getting-started/glossary/`
- A non-engineer is asking "where do I start?" and the answer is reading
  the live docs before opening any MCP tool

The bundled `askalot-setup` skill covers install-time configuration
(the single connection address, the OAuth browser sign-in, verification, the active
organization, ending a sign-in, and API tokens for REST use).
The getting-started page covers the **product** — what to do *after* you
have a working install.

When the agent has Askalot MCP access, prefer
`get_documentation("getting-started/quick-start.md")` over a
raw fetch.
