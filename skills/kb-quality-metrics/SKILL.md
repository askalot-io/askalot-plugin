---
name: kb-quality-metrics
description: Pointer to the public quality-metrics reference at docs.askalot.io/guide/quality-metrics-reference. Use when an agent or CLI user needs the canonical definitions and interpretation thresholds for RMSE, MAE, Chi-Square, Max Deviation, and Quality Score in survey datasets.
disable-model-invocation: false
---

# Quality Metrics Reference

The public quality-metrics reference lives at
**<https://docs.askalot.io/guide/quality-metrics-reference/>**.

Use the live page when:

- A customer asks "what does RMSE = 0.04 mean for my campaign?" and you
  want the canonical threshold table
- You're explaining Quality Score (the composite 0-1 indicator) to a
  non-engineering reader
- You need the metric definitions in a form you can quote to a customer
  without paraphrasing

The bundled `data-quality` skill carries the same metric set with deeper
diagnostic interpretation (when to investigate, recommended interventions,
how to distinguish fixable issues from structural problems). Use the
bundled skill when the agent is reasoning about results; use this pointer
when the customer wants the reader-facing reference.

When the agent has Askalot MCP access, prefer
`get_documentation("guide/quality-metrics-reference.md")` over
a raw fetch.
