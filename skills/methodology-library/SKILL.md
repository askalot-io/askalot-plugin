---
name: methodology-library
description: Use when a survey-methodology question exceeds the agent's distilled skills, when the customer asks for a peer-reviewed citation, when comparing author positions, or when backing a recommendation with evidence. Covers the four Askalot MCP tools that read the shared methodology library (Dillman, Krosnick, Groves, Tourangeau, Bethlehem, Heeringa, Schouten, and others).
---

# Methodology Library — Citation Discipline

## When to use

Reach for the library when one of these is true:

- The customer asks a methodology question that isn't covered by your
  distilled skills (`survey-design`, `research-methodology`,
  `campaign-strategy`, `sampling-theory`, `validity-reliability`,
  `data-quality`, `questionnaire-logic`).
- The customer explicitly wants a peer-reviewed citation — "show me
  the paper that backs this", "where does the 5-point-scale rule come
  from?"
- You need to compare how different authors treat a topic — e.g.
  Krosnick on satisficing vs. Tourangeau on the four-stage response
  model.
- You're recommending a decision with non-trivial consequences
  (oversampling a subgroup, accepting a short-form scale, publishing a
  quality report) and want the recommendation to stand on peer-reviewed
  ground rather than training memory.

If none of those are true, **do not** call the library. It's a
retrieval round-trip with meaningful latency; answering from your
distilled skills when they cover the question is the right default.

## The four tools, in the order you normally use them

1. `list_methodology_papers()` — free reconnaissance. Returns
   author, year, title, `paper_id`, and which agent consults
   each paper. Call this first when you're unsure which papers even
   exist for a topic; the tool does not hit LightRAG and is cheap.
2. `search_methodology_library(query, top_k?, mode?)` — full corpus
   semantic search. Use a 2–10 word conceptual phrase, not a single
   keyword ("acquiescence bias mitigation" > "bias"). Default
   `mode="mix"` blends vector + knowledge-graph retrieval and is
   right for most queries. Switch to `mode="global"` for broad
   "what-do-the-authors-say" questions, `mode="naive"` for
   fast keyword-style lookup.
3. `get_methodology_paper_summary(paper_id)` — 500-word orientation
   for a single paper you've identified. Useful when
   `search_methodology_library` surfaced a paper you haven't read
   before and you want a map of what's in it.
4. `get_methodology_chunk(paper_id, section_query)` — verbatim
   passage within one paper. Use this when you've picked a paper
   and want an exact quote for citation.

A common sequence:

```
list_methodology_papers()                    # see what's available
→ search_methodology_library("…topic…")      # find relevant passages
→ get_methodology_chunk(paper_id, "…topic…") # pull a verbatim quote
→ cite in your answer
```

## Citation discipline

Every time you quote or paraphrase the library in your reply:

- Include a citation stub: **`(paper_id, year)`** or
  **`(paper_id, year, p. ~N)`** if the chunk carried a `--- page N ---`
  marker. Use tilde `~` because rag-ingest chunks are approximate.
- **Mark direct quotes with quotation marks.** Paraphrase unless
  you need a precise wording.
- Don't attribute a claim to a paper if the library didn't surface
  it. If `search_methodology_library` returned nothing relevant,
  say so — do not manufacture a citation from training memory.
- When the library's answer contradicts your training memory, **defer
  to the library**. Your memory may be out of date or wrong; the
  library is the curated peer-reviewed source.

## When NOT to use the library

- **Mid-task, action-oriented requests.** If the customer is asking
  you to *do* something (create a campaign, validate a QML file,
  generate a questionnaire), answer the task first and consult the
  library only if the customer follows up with a methodology
  question.
- **Your own distilled skill covers it.** If the customer asks
  "what's a good 5-point Likert scale?" and `survey-design` already
  answers this, answer from the skill. Reserve library calls for
  topics the skills don't cover.
- **Questions about the customer's own documents.** Those live in the
  per-user `usr_<user_id>` workspace — use
  `search_document_chunks_by_keyword` / `get_document_summary` for
  those, not the methodology tools.
- **Basic platform questions.** "How do I create a respondent pool?"
  is a platform question, not a methodology question — use the docs
  tools (`search_documentation`) or your platform knowledge.

## What the library contains (scope)

The shared methodology library is a curated corpus of ~23
peer-reviewed textbooks and papers covering:

- Survey design fundamentals — Dillman (tailored design), Fowler,
  Tourangeau (psychology of response), Bradburn, Oppenheim
- Total Survey Error, quality, and costs — Groves (by reference via
  chapters in Marsden & Wright), de Leeuw/Hox/Dillman
- Sampling and weighting — Bethlehem & Biffignandi, Heeringa et al.
- Adaptive design, R-indicators — Schouten, Calinescu, Cobben
- Satisficing and response quality — Krosnick & Presser (chapter)
- Validity & reliability — Taherdoost, Aithal & Aithal
- Questionnaire logic and graph-theoretic structure — Fagan & Greenberg,
  Elliott, Schiopu-Kratina, Feeney, Manski & Molinari, Willenborg
- AI-assisted survey research — Olivos & Liu (ChatGPTest)

Call `list_methodology_papers` for the authoritative current list —
the catalog updates whenever papers are added to
`docs/methodology_library/` and the ops script is re-run.
