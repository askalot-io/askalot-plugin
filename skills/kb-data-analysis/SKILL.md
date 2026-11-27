---
name: kb-data-analysis
description: Pointer to the public data-analysis guide at docs.askalot.io/guide/data-analysis. Use when an agent or CLI user needs the end-user explainer for the Bronze/Silver/Gold medallion pipeline, raking, export formats, and quality metrics workflow. Complements the data-quality and sampling-theory skills with reader-facing context.
---

# Data Analysis Guide

The public data-analysis guide lives at
**<https://docs.askalot.io/guide/data-analysis/>**.

Use the live page when:

- A customer wants to know what Bronze / Silver / Gold mean for their
  campaign data and what each transition step does
- You're explaining raking (post-stratification weighting) to a
  non-engineering audience
- You need the export-format table (CSV, semicolon CSV, Excel, SPSS,
  Parquet, R `.rds`, JSON — what each is best for) without inlining it
  in chat
- You need what a dataset takes from the questionnaire's item inventory:
  each column records its question's construct, kind of measure, KPIs and
  reverse wording at Bronze extraction, the Gold page proposes one scale
  score per construct and scale, and the Excel schema sheet, JSON, Parquet
  and SPSS file notes carry those facts (CSV and R do not). The three
  layers behind this are on `guide/questionnaire-layers.md`

The bundled skills cover the agent-facing angle:

- `data-quality` — quality-metric interpretation (RMSE, MAE, Chi-Square,
  Quality Score), straightliner / speeder detection, weighting evaluation
- `sampling-theory` — design effect, weighted SE, raking convergence,
  why naive SEs underestimate uncertainty
- `validity-reliability` — Cronbach's α / McDonald's ω and the validity
  framework for instrument quality

When the agent has Askalot MCP access, prefer
`get_documentation("guide/data-analysis.md")` over a raw
fetch.
