---
name: mcp-document-tools
description: Use when you need to discover, search, or read indexed documents via MCP tools. Covers list_indexed_documents, get_document_summary, read_paper, search_document_chunks_by_keyword, and get_document_chunk.
---

# MCP Document Tools Reference

## Scope

**Covers**: Document discovery, summary reading (per-document and project-level), content search, and chunk reading via Portor MCP server.

**Does not cover**: Document ingestion, indexing, or conversion.

## Available Tools

### list_indexed_documents

Lists all documents indexed in the customer's workspace. Call this early in the conversation to understand what sources are available.

**When to use**: At the start of a session to inventory available documents.

### get_document_summary

Returns the per-document summary that the Armiger stitcher persisted on the `indexed_documents` row. The summary is a short Markdown body covering the document's scope, key topics, and operative facts; it is not a full retrieval and does not return chunks.

If the document has no stitched summary yet (pre-feature row, in-flight stitch, or the last stitch failed), the tool returns an empty-state placeholder body (`# <filename>\n\n_No summary available yet._`) rather than failing.

**When to use**: To get a one-shot orientation on a document before deciding whether to search its chunks.

### read_paper

Returns the project's research paper — its chapters as assembled text, plus the per-unit map you edit against. Signature: `read_paper(project_id, chapter_id=None, unit_key=None)`; supply at most one of `chapter_id` and `unit_key`, since a unit belongs to exactly one chapter.

```
{"success": true, "project_id", "scope",
 "chapters": [{"chapter_id", "title", "content", "written", "unit_keys"}],
 "units": {"<unit_key>": {"body", "anchor_basis", "base_hash", "content_hash",
                          "written", "version_number", "provenance",
                          "agent_kind", "stale", "stale_since"}}}
```

`base_hash` is the read token `edit_paper_unit` requires — an edit with no token, or a stale one, is refused. Injected paper context is a cache, **not** a read token: call `read_paper` for a current `base_hash` before every edit.

`anchor_basis` is what an anchored edit matches against. For a unit nothing has written yet it is an invisible sentinel comment, and anchoring `old_string` on that sentinel is how you write a unit's first content — an unwritten unit is present in the map, not absent from it.

A body over the inline threshold comes back as `{"success": true, "download_url", "size_bytes", "note"}` instead. Fetch it or narrow the read; content is never truncated.

The project-level stitched summary — the one-page synthesis spanning every indexed document — is a **unit of this paper**, not a document tool and not a separate envelope: read it with `read_paper(project_id, unit_key="source_material")`. There is no separate storage row behind it and no separate `is_stale` envelope flag; it is a paper unit like any other, carrying the same `written`, `base_hash` and `stale` / `stale_since` fields.

Staleness did **not** go away with the old envelope — it moved onto the unit, and `source_material` is the one unit it is ever set on. When a stitch run fails, the stitcher leaves the previous good body in place and sets `stale_since` on the unit; the body you read is then the last *successful* synthesis, not a description of what is indexed now. So when a unit's `stale` is true, say so — surface a "showing stale summary" warning rather than presenting the body as current.

**When to use**: once per session to anchor what the project is about, and again before every edit, for the token.

### search_document_chunks_by_keyword

Searches document content for topics, scales, definitions, or requirements across documents. The search is semantic (vector + knowledge-graph) -- it finds conceptually related content, not just literal keyword matches.

**Best practices**:
- Prefer 2-5 word topic phrases over single keywords
- Avoid long natural-language questions
- Supports optional file path filtering
- Keep `max_results` in the 5-10 range per call
- Batch related searches: issue multiple calls in a single response

**When to use**: To find specific content across all indexed documents.

### get_document_chunk

Reads a specific chunk of a document by file path and chunk index. Use this to read detailed content when you need exact quotes or full context.

**When to use**: To read detailed sections after identifying relevant chunks via search.

## Entity and Relation Signals

`search_document_chunks_by_keyword` results may include named entities (people, organizations, concepts, instruments, populations) and their relations. Use entities to identify canonical names for scales and populations. Use relations to discover which variables the documents associate with each other -- this is especially useful for conditional logic extraction (branching rules, skip patterns, validation constraints).

Entities and relations are surfaced proactively by the retrieval system -- you don't need to ask for them.

## Efficiency Guidelines

- **Anchor with summaries first**: `read_paper` once, then `get_document_summary` for the two or three documents you actually need to dig into.
- **Batch related searches**: When you need to search for multiple topics, issue all `search_document_chunks_by_keyword` calls in a single response rather than one at a time
- **Minimize iterations**: Aim to complete analysis in 5-7 tool calls total
- **Prefer broad keyword searches** over sequential chunk-by-chunk reading
