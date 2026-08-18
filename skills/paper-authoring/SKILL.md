---
name: paper-authoring
description: Use when acting as Designer, Manager, or Analyst and you are about to write or edit a chapter of the project's research paper. Covers the HTML the paper accepts, the read-before-edit contract, how to anchor a first write on an empty chapter, and what gets your write refused.
---

# Writing the research paper

The project's research paper is one versioned document per chapter, stored as
sanitized HTML fragments. It is the single record of the research from ideation
to verdict, and it is read by people — on a page, and printed to PDF.

You write it through two tools:

- `mcp__plugin_askalot_askalot__read_paper` — read a chapter or a unit, and get
  the `base_hash` token an edit needs.
- `mcp__plugin_askalot_askalot__edit_paper_unit` — replace an exact passage
  inside one unit.

## Read before you edit — always

`edit_paper_unit` refuses an edit that carries no `base_hash`, and refuses one
whose token no longer matches what is stored. That is not a formality: another
agent or a researcher may have written the same unit since you last looked, and
an edit applied blind would silently overwrite their work.

1. `read_paper` the unit you intend to change, **in this turn**.
2. Edit using the `base_hash` it returned.
3. If you get a staleness refusal, re-read and reapply — never retry with the
   old token.

Your `old_string` must appear **exactly once** in the unit. If it appears zero
times or more than once the edit is refused and nothing is written; quote more
surrounding text to make it unique rather than editing a shorter fragment and
hoping.

## Writing into an empty chapter

An unwritten unit is not empty text — it reads back as a single HTML comment:

```html
<!-- askalot:empty section=research_goals -->
```

That comment is the anchor for your first write. Use it verbatim as
`old_string`, with your opening HTML as `new_string`. Do not try to anchor on
an empty string, and do not assume the unit contains nothing.

## The HTML the paper accepts

Body-level fragments only, from a fixed allowlist. A construct outside it is
**refused with the name of what was rejected** — you can repair your own output
and retry.

**Use**: `<h2>`–`<h6>`, `<p>`, `<ul>`/`<ol>`/`<li>`, `<dl>`/`<dt>`/`<dd>`,
`<table>` with `<thead>`/`<tbody>`/`<tr>`/`<th>`/`<td>`/`<caption>`,
`<blockquote>`, `<pre>`, `<code>`, `<em>`, `<strong>`, `<abbr>`, `<cite>`,
`<sub>`, `<sup>`, `<figure>`/`<figcaption>`, `<section>`, `<div>`, `<span>`,
`<a href="…">`.

**Never**:

- **Document scaffolding** — no `<!DOCTYPE>`, `<html>`, `<head>`, `<title>`,
  `<body>`. You are writing a fragment that is placed inside a page, not a page.
- **Anything that executes or styles** — no `<script>`, no `<style>`, no
  `style="…"` attribute, no `onclick` or any other event handler.
- **Anything that fetches** — no `<img>`, `<iframe>`, `<object>`, `<video>`,
  `<embed>`. A paper renders offline and must not pull a resource from anywhere.
- **SVG.** Figures are generated server-side from the quality readings captured
  when a Study was written. You never author one, and an SVG you write is
  refused rather than drawn.
- **Markdown.** `## Heading` and `**bold**` are literal text in HTML. Write
  `<h2>Heading</h2>` and `<strong>bold</strong>`.

### Links

`href` accepts exactly two shapes: an in-document anchor (`#some-id`) or an
absolute `https://` URL. `http://`, protocol-relative (`//host`), `mailto:`,
`data:` and `javascript:` are all refused. Do not add `rel` — it is set for you.

### Classes

`class` is allowed but only from the paper's own vocabulary, and the stylesheet
styles exactly these names. The useful ones:

| Class | Use it for |
|---|---|
| `paper-lead` | The opening paragraph of a chapter |
| `paper-finding` / `paper-findings` | A finding, and the list of them |
| `paper-limitation` / `paper-limitations` | A limitation, and the list |
| `paper-recommendation` / `paper-recommendations` | A recommendation, and the list |
| `paper-verdict` | A judgement the reader should not miss |
| `paper-note` / `paper-callout` / `paper-warning` | Set-apart remarks, by weight |
| `paper-definition` | A term being defined |
| `paper-metric` / `paper-metrics` | A single figure, and a row of them |
| `paper-numeric` | A table cell holding a number (aligns the digits) |
| `paper-quote` | A quoted respondent or source |
| `paper-reference` / `paper-references` | A citation, and the list |
| `paper-caption` | A caption under a table or figure |
| `paper-no-break` | A block that must not split across printed pages |

A class outside the vocabulary is refused. Inventing one would target a
stylesheet you do not own, so it renders as nothing — which reads to the
customer as content that failed to save.

## Identifiers go in the visible text

When you write about a research goal, a KPI, or a research question, put its
identifier in the **prose the reader sees** — `<p>RQ-2 asks whether …</p>`, not
an `id` or a `data-` attribute. The answerability chain reads the paper's text,
the customer reads the same text, and an identifier hidden in markup is invisible
to both.

## Write for a reader, not for a log

A chapter is read by a person and printed to PDF. Prefer full sentences to
bullet fragments, name what a number means before quoting it, and do not paste a
tool result verbatim into a chapter. If a chapter has grown long, add `<h3>`
subheadings rather than a longer wall.
