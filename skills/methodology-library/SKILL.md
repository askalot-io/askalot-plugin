---
name: methodology-library
description: Use when a survey-methodology question exceeds the agent's distilled skills, when the customer asks for a peer-reviewed citation, when comparing author positions, or when backing a recommendation with evidence. Covers the four Askalot MCP tools that read the shared methodology library (Dillman, Krosnick, Tourangeau, Bethlehem, Heeringa, Schouten, and others).
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

1. `list_methodology_papers()` — the catalog: author, year, title,
   `paper_id`, and which agent consults each paper. Call this first
   when you're unsure which papers exist for a topic, and whenever you
   need a `paper_id` or year for a citation; it reads a static list,
   runs no retrieval, and is fast.
2. `search_methodology_library(query, top_k=10, mode="mix")` — full
   corpus semantic search. Use a 2–10 word conceptual phrase, not a
   single keyword ("acquiescence bias mitigation" > "bias"). The
   default `mode="mix"` blends vector + knowledge-graph retrieval and
   is right for most queries. Switch to `mode="global"` for broad
   "what-do-the-authors-say" questions, `mode="naive"` for a fast
   vector-only lookup (`local` and `hybrid` are also accepted). The
   answer is retrieved text, up to about 6,000 characters, and it may
   arrive as one assembled block with no `paper_id` per passage; then
   identify the paper from the author and title in the text and look
   its `paper_id` up in the catalog.
3. `get_methodology_paper_summary(paper_id)` — orientation for a
   single paper: its citation line plus the top-ranked retrieved
   passages (up to about 4,000 characters), not a written summary.
   You write the summary from them. Useful when a search surfaced a
   paper you don't know and you want a map of what's in it.
4. `get_methodology_chunk(paper_id, section_query)` — the passage of
   one paper that best matches `section_query`. Use this when you've
   picked a paper and want an exact quote. When the answer opens with
   a note that the passage "may span papers", it is not confined to
   the paper you named: confirm from the text that the wording is that
   paper's before quoting it under its `paper_id`.

An unknown `paper_id` answers "Paper not found"; take ids from
`list_methodology_papers`, never from memory.

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
- An answer of "No passages found", "No passage matching …" or "No
  content retrieved" for a core topic usually means the library is not
  loaded on this tenant, not that the literature is silent. Tell the
  user the claim is not backed by the library; a failed call (a tool
  error) is the same case. The four tools need the AI-assistant
  capability, so if they are absent from your tool list, say the
  library is not available to this account.
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
- **Questions about the customer's own documents.** Those are indexed
  in the customer's own workspaces, not in this library — use
  `search_document_chunks_by_keyword` / `get_document_summary` for
  those, not the methodology tools.
- **Basic platform questions.** "How do I create a respondent pool?"
  is a platform question, not a methodology question — use the docs
  tools (`search_documentation`) or your platform knowledge.

## What the library contains (scope)

The shared methodology library is a curated corpus of about 25
peer-reviewed textbooks and papers covering:

- Survey design fundamentals — Dillman, Smyth & Christian (tailored
  design), Tourangeau, Rips & Rasinski (psychology of response),
  Oppenheim, Schwarz, Stantcheva, the Marsden & Wright handbook
- Question wording and scales — Krosnick & Presser, Krosnick, Likert,
  Saris & Gallhofer
- Analysis of complex samples and weighting — Heeringa, West & Berglund
- Adaptive design, R-indicators — Schouten, Calinescu, Cobben,
  Bethlehem
- Response quality, coding reliability, editing — Zhang & Conrad
  (speeding), Krippendorff (α), the EDIMBUS editing and imputation
  manual
- Validity & reliability — Taherdoost, Aithal & Aithal
- Questionnaire logic and graph-theoretic structure — Fagan & Greenberg,
  Elliott, Schiopu-Kratina, Feeney, Manski & Molinari, Bethlehem &
  Hundepool
- AI-assisted survey research — Olivos & Liu (ChatGPTest)

`list_methodology_papers` is the authoritative current list; this
outline can lag it.
