---
name: mcp-document-tools
description: Use when you need to discover, search, or read indexed documents via MCP tools. Covers list_indexed_documents, get_document_summary, read_paper, search_document_chunks_by_keyword, get_document_chunk, get_questionnaire_inventory, and get_questionnaire_import_source.
---

# MCP Document Tools Reference

## Scope

**Covers**: Document discovery, summary reading (per-document and project-level), content search, chunk reading, and a questionnaire's inventory via Portor MCP server.

**Does not cover**: Document ingestion, indexing, or conversion.

## Available Tools

### list_indexed_documents

Lists all documents indexed in the customer's workspace. Call this early in the conversation to understand what sources are available.

**When to use**: At the start of a session to inventory available documents.

Each document is listed with its **document key**, such as `projects/<project-id>/report.pdf`. The other document tools name a document by that key: `get_document_summary(document_key)`, `get_document_chunk(document_key, chunk_index)` and `search_document_chunks_by_keyword(query, document_keys=[...])`. Copy the key exactly as listed; an unknown key is answered "Document not found" and nothing is searched.

### get_document_summary

Returns the per-document summary that the Armiger stitcher persisted on the `indexed_documents` row. The summary is a short Markdown body covering the document's scope, key topics, and operative facts; it is not a full retrieval and does not return chunks.

A document with no summary answers one italic sentence instead of failing, and the sentence says which of three cases it is: no summary was generated yet (the next workspace stitch writes it); the last attempt failed (the sentence gives the time); or the account the summary runs as has to finish its AI setup or sign in to its AI provider again (the sentence names whose account). In all three the document's text is still searchable with `search_document_chunks_by_keyword`. Pass the sentence on as a status; do not present it as the document's content.

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

The project-level stitched summary — the one-page synthesis spanning every indexed document — is a **unit of this paper**, not a document tool: read it with `read_paper(project_id, unit_key="source_material")`. It is a paper unit like any other, carrying the same `written`, `base_hash` and `stale` / `stale_since` fields.

`source_material` is the one unit `stale` is ever set on. When a stitch run fails, the stitcher leaves the previous good body in place and sets `stale_since` on the unit; the body you read is then the last *successful* synthesis, not a description of what is indexed now. So when the unit's `stale` is true, tell the user the summary is out of date rather than presenting the body as current.

**When to use**: once per session to anchor what the project is about, and again before every edit, for the token.

### search_document_chunks_by_keyword

Searches document content for topics, scales, definitions, or requirements across documents: `search_document_chunks_by_keyword(query, document_keys=None, max_results=10)`. Despite the name, the search is semantic (vector similarity over chunks) -- it finds conceptually related content, not just literal keyword matches. `query` needs at least 2 characters. Each match is shown with its file and score and is cut at 800 characters; read the whole chunk with `get_document_chunk`. Without `document_keys` the search covers one workspace: the project the session is bound to, or, for a session bound to none, your own uploads that belong to no project. To search a specific project's documents from such a session, pass their keys.

**Best practices**:
- Prefer 2-5 word topic phrases over single keywords
- Avoid long natural-language questions
- Optionally limited to `document_keys` from `list_indexed_documents`
- Keep `max_results` in the 5-10 range per call
- Batch related searches: issue multiple calls in a single response

**When to use**: To find specific content across all indexed documents.

### get_document_chunk

Reads one chunk of a document: `get_document_chunk(document_key, chunk_index)`. `chunk_index` is 0-based and is a relevance rank, not a position in the document: index 0 is the chunk the retrieval ranks highest for that file, and at most 20 are reachable. So raising the index does not read the document in order, and an index past the end answers "Chunk not found" with the available range. Use it for exact quotes or the full text of a match the search cut short.

**When to use**: To read detailed sections after identifying relevant chunks via search.

### get_questionnaire_inventory

Reads what a questionnaire's inventory records: `get_questionnaire_inventory(questionnaire_id)`. An inventory lists every question before any QML existed, with the routing, the checks and a scope table of what was kept and what was left out; a new questionnaire is created from one, designed or imported. The answer is a summary of it, not the whole inventory (`in` and `out` are counts of the source units kept and left out):

```
{"success": true, "questionnaire_id", "inventory_version_id",
 "describes_version_id", "describes_version_number",
 "id_map": [{"source_id", "qml_id"}],
 "invented": [{"qml_id", "predicate", "hint"}],
 "report": {"scope": {"in", "out", "out_units": [{"unit", "reason"}]},
            "import": <the import report, or null>}}
```

- `id_map` pairs each printed (or planned) question id with the QML item it is asked under.
- `invented` lists the checks the source did not state as hard rules, which the inventory stage added.
- `out_units` names every source unit left out, with why.

The inventory is written once, with version 1, and never changes: `describes_version_number` is 1, and later saves change only the QML. Read it as a dated record of version 1, and `get_qml_content` as the questionnaire now. Access follows the same Project checks as `read_paper`. A questionnaire created without one answers `inventory_not_found`; an unknown or unreachable id answers `not_found`.

**When to use**: To explain where an imported questionnaire's items came from, which checks were invented, or what the import left out; or to compare the current QML against what version 1 was built from.

### get_questionnaire_import_source

Reads the source a PDF import read: `get_questionnaire_import_source(questionnaire_id, from_page=1, max_chars=32000)`. A questionnaire imported from a PDF keeps it as one Markdown document, answers already removed, each page opened by a marker `<!-- page N printed="36" read_by="text_layer" -->` (`N` is the page of the file, `printed` the number printed on it when there is one, `read_by` `text_layer` or `vision`). The inventory's `page` fields are these `N`.

```
{"success": true, "questionnaire_id", "front_matter", "pages",
 "content", "next_page"}
```

- `front_matter` names the file, its page count, the pages read by vision and the normalizer's counts (answers discarded, running headers and footers dropped, printed page numbers found).
- `content` holds whole pages from `from_page` until about `max_chars` (1000 to 100000), never a cut page; a single page over the budget comes whole. Call again from `next_page` until it is null.

The document is written once, with the questionnaire, and never changes. Access follows the inventory's checks. A questionnaire not imported from a PDF (written by hand, designed, or imported from Markdown, which is not kept) answers `import_source_not_found`; an unknown or unreachable id answers `not_found`, and a `from_page` below 1 or a `max_chars` outside its range `invalid_request`.

**When to use**: To check an imported question, a routing instruction or an invented check against the page the import read it from; start at the page the inventory names.

## Efficiency Guidelines

- **Anchor with summaries first**: `read_paper` once, then `get_document_summary` for the two or three documents you actually need to dig into.
- **Batch related searches**: When you need to search for multiple topics, issue all `search_document_chunks_by_keyword` calls in a single response rather than one at a time
- **Minimize iterations**: Aim to complete analysis in 5-7 tool calls total
- **Prefer broad topic searches** over stepping through `get_document_chunk` indices, which does not read a document in order
