---
name: kb-qml-syntax-reference
description: Pointer to the public QML syntax reference at docs.askalot.io/guide/qml-syntax. Use when an agent or CLI user needs the canonical reader-facing QML grammar (item kinds, controls, preconditions, postconditions, code blocks) rather than the distilled qml-syntax skill that ships with this plugin. Live page; if it disagrees with this skill, trust the live page.
disable-model-invocation: false
---

# QML Syntax Reference

The canonical public reference for QML (Questionnaire Markup Language) syntax
lives at **<https://docs.askalot.io/guide/qml-syntax/>**.

Use the live page when:

- You need a worked example a customer can read alongside their own draft
- You need the latest grammar (the bundled `qml-syntax` skill ships with the
  plugin and is updated on each plugin release; the live page tracks main)
- You're answering a methodology question from a non-engineering audience —
  the public docs use plain English; the bundled skill is denser

When the agent has Askalot MCP access, prefer
`mcp__askalot__get_documentation("guide/qml-syntax.md")` over a raw fetch —
the MCP tool already speaks docs-relative paths and gives the agent the
rewritten markdown ready for further chaining via `docs://...` references.

The bundled distilled skill remains the right starting point for in-context
authoring: it carries the exact field names, kinds, and patterns the
Askalot Z3 validator expects.
