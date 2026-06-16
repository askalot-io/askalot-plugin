---
name: mcp-document-tools
description: Use when you need to discover, search, or read indexed documents via MCP tools. Covers list_indexed_documents, get_document_summary, read_project_summary, search_document_chunks_by_keyword, and get_document_chunk.
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

### read_project_summary

Returns the project-level stitched summary: a one-page Markdown overview that spans every indexed document in the project. The stitcher writes it back to the `research_projects` row, so reads are a single DB round-trip — no LightRAG query.

The response envelope carries an `is_stale` boolean that flips true when the last stitch run failed and the persisted body is the previous good output. Surface a "showing stale summary" warning to the user when this is set.

Empty-state semantics match `get_document_summary` — a project with no stitched summary yet returns a short placeholder body.

**When to use**: Once per session to anchor what the project as a whole is about before drilling into individual documents.

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

- **Anchor with summaries first**: `read_project_summary` once, then `get_document_summary` for the two or three documents you actually need to dig into.
- **Batch related searches**: When you need to search for multiple topics, issue all `search_document_chunks_by_keyword` calls in a single response rather than one at a time
- **Minimize iterations**: Aim to complete analysis in 5-7 tool calls total
- **Prefer broad keyword searches** over sequential chunk-by-chunk reading
