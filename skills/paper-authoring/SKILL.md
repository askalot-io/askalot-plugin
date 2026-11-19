---
name: paper-authoring
description: Use when acting as Designer, Manager, or Analyst and you are about to write or edit a chapter of the project's research paper. Covers the HTML the paper accepts, the read-before-edit contract, how to anchor a first write on an empty chapter, and what gets your write refused.
---

# Writing the research paper

The project's research paper is a fixed set of chapters, each assembled from
one or more *units*. A unit is one versioned HTML fragment and is what you
read and edit; `read_paper` lists every chapter with its `unit_keys`. The paper
is the single record of the research from ideation to verdict, and it is read
by people — on a page, and printed to PDF.

You write it through two tools:

- `mcp__plugin_askalot_askalot__read_paper` — with `project_id` alone the whole
  paper, or one chapter (`chapter_id`) or one unit (`unit_key`), never both.
  Each unit comes with its `body`, the `anchor_basis` an edit matches against,
  and the `base_hash` token an edit needs.
- `mcp__plugin_askalot_askalot__edit_paper_unit` — replace an exact passage
  inside one unit: `project_id`, `unit_key`, `old_string`, `new_string`,
  `base_hash`. There is no whole-chapter write.

The Analyst flow is the exception: `edit_paper_unit` is denied to it, and its
chapters are written by the host from the blocks it emits. The HTML rules
below still apply to those blocks.

## Write in the paper's source language

The paper is authored in its source language (English), whatever language the
customer chats in: the source is what every agent reads and what translations
are made from. Translating the paper into a reader's language is a separate
pass with its own tools, described in the `translate-paper` skill; never write
a translation into a source unit.

## Read before you edit — always

`edit_paper_unit` refuses an edit that carries no `base_hash`
(`blind_edit_refused`), and refuses one whose token no longer matches what is
stored (`paper_stale`). That is not a formality: another agent or an approved
proposal may have written the same unit since you last looked, and an edit
applied blind would silently overwrite that work.

1. `read_paper` the unit you intend to change, **in this turn**. The paper text
   in your prompt is a copy for orientation and carries no token.
2. Edit using the `base_hash` it returned.
3. A successful edit answers `new_base_hash`: use it for your next edit of the
   same unit, since the token you read is now stale.
4. On `paper_stale`, re-read and reapply — never retry with the old token.

Your `old_string` must appear **exactly once** in the unit's `anchor_basis`.
If it appears zero times or more than once the edit is refused as
`anchor_not_unique` (with `match_count`) and nothing is written; quote more
surrounding text to make it unique rather than editing a shorter fragment and
hoping.

A `unit_key` the paper does not declare is refused as `invalid_paper_key`.
`paper_write_refused` means the paper cannot take this write at all (a sealed
organization, or a block that is not yours, below): do not retry it, and tell
the customer what the refusal said.

## Writing into an empty chapter

An unwritten unit has an empty `body` and `written: false`, and its
`anchor_basis` is a single HTML comment naming the unit:

```html
<!-- askalot:empty section=research_goals -->
```

That comment is the anchor for your first write. Use it verbatim as
`old_string`, with your opening HTML as `new_string`. Do not try to anchor on
an empty string.

## The "Sample size" block is not yours

The `sampling_strategy` chapter may carry a "Sample size" section
(`<section id="sample-size-plan">`). It is written by the one shared save of a
sizing plan, whichever door saves it: the Size Planner page in Targetor, or
`save_sizing_targets` over MCP or REST. Agents never rewrite it:
`edit_paper_unit` refuses an edit whose `old_string` overlaps it or whose
`new_string` contains its id. Write around it: anchor on the text before or
after the section, and never quote or restate its figures as your own. To
change the numbers, compute them with `plan_sample_size` and save the plan with
`save_sizing_targets` (on the user's stated answer), which re-writes the block.
A link to `#sample-size-plan` is fine as a citation.

A Study unit (`study:<bundle id>`) may likewise carry the platform's results
block (`<section id="study-results">`): each sized KPI's usable responses,
observed share or spread and achieved margin or power, the wave's yield and
design effect, computed by the platform after the Analyst's Study is
promoted. Only the newest wave's Study holds one. The same refusals apply;
write around it and never restate its numbers as your own.

## The HTML the paper accepts

Body-level fragments only, from a fixed allowlist. A construct outside it is
refused as `fragment_refused`, whose `rejections` name each construct and
where it is; nothing is stripped for you and nothing is written. Repair
exactly what it names and retry.

**Use**: `<h3>`–`<h6>`, `<p>`, `<ul>`/`<ol>`/`<li>`, `<dl>`/`<dt>`/`<dd>`,
`<table>` with `<thead>`/`<tbody>`/`<tr>`/`<th>`/`<td>`/`<caption>`,
`<blockquote>`, `<pre>`, `<code>`, `<em>`, `<strong>`, `<abbr>`, `<cite>`,
`<sub>`, `<sup>`, `<figure>`/`<figcaption>`, `<section>`, `<div>`, `<span>`,
`<a href="…">`.

Start headings at `<h3>`: the page prints each chapter's title as its `<h2>`,
so an `<h2>` of yours reads as a second chapter.

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
  `<h3>Heading</h3>` and `<strong>bold</strong>`.

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
tool result verbatim into a chapter. If a unit has grown long, add `<h3>` and
`<h4>` subheadings rather than a longer wall.
