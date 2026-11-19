---
name: translate-paper
description: Use when the customer asks to translate a project's research paper into another language, or to bring a paper translation up to date after its chapters changed. Covers the per-unit translation pass, the source and translation tokens, the Sample size block readers splice in, the reader's formal register, and what each refusal means.
---

# Translate the research paper

A research paper has one source text, which agents author with
`edit_paper_unit` in the paper's source language. Each paper unit can also hold
one translation per language, kept beside the source. A translation never
changes the source, and nothing you write in a translation reaches another
agent's context: agents read the source. People read the paper in their own
language when a translation exists.

Each unit's translation in a language is in one state:

| State | Meaning |
|---|---|
| `current` | made from the source text the unit holds now |
| `behind` | made from a different version of the source text; readers see it marked as such |
| `missing` | the unit has source text and no translation |
| `empty` | the unit has no source text yet; there is nothing to translate |

The source language itself (`source_language` in every read) takes no
translation. `locale` is one of `en`, `es`, `fr`, `de`, `hu`; the tools accept
no other language.

## The tools

- `mcp__plugin_askalot_askalot__read_paper_translation` with `project_id` and
  `locale` — every unit's state with its `source_base_hash` and `base_hash`,
  plus the per-language counts. No bodies.
- The same tool with `unit_key` — one unit's `source_body`, its
  `translation_body`, the `translation_anchor_basis` to anchor on, both tokens,
  and, for a `behind` unit, `translated_from_body`: the source the translation
  was made from.
- `mcp__plugin_askalot_askalot__edit_paper_translation` — an anchored edit of
  one unit's translation: `project_id`, `unit_key`, `locale`, `old_string`,
  `new_string`, `base_hash` and `source_base_hash`. The same contract as
  `edit_paper_unit` with one more token: `source_base_hash`, the source you
  translated.

The Analyst flow cannot run this pass: `edit_paper_translation` is denied to
it. Say so instead of attempting the edit.

## The pass, one unit at a time

1. Call `read_paper_translation` without a unit and work through the units
   that are `missing` or `behind`. Skip `current` and `empty` units.
2. Read the unit with `read_paper_translation` and `unit_key`, in this turn.
3. Translate `source_body` (below). For a `behind` unit, compare
   `translated_from_body` with `source_body`, change what the source changed
   and keep the rest of the existing translation as it is, in one new text of
   the whole unit.
4. Write it with `edit_paper_translation`:
   - a `missing` unit: `old_string` is the `translation_anchor_basis` (the
     empty-section comment) verbatim, `new_string` your whole translation;
   - a `behind` unit: replace it whole in one edit. `old_string` is its full
     `translation_body`, `new_string` the whole updated translation. A passage
     edit of a `behind` unit is refused: one edit records that all of the text
     renders the current source. When nothing in it needs to change, send the
     same text as `new_string`; that records it as current;
   - a `current` unit you are correcting: anchor on the passage you replace,
     exactly once in the `translation_anchor_basis`, as in `edit_paper_unit`;
   - `base_hash` and `source_base_hash` are the two tokens from step 2.
5. The answer's `new_base_hash` is the token for a further edit of the same
   unit in this pass.
6. When the pass ends, tell the customer how many units are now current and
   which, if any, are still missing or behind.

The researcher may be asked to approve each edit. A denied edit is their
decision: do not resend it; ask what they want changed.

## Writing the translation

- **Same content, same HTML.** Translate the words and keep every element,
  class and link of the source in the same structure. The paper accepts the
  restricted HTML described in the `paper-authoring` skill; anything else is
  refused by name.
- **Never include the Sample size block** (`<section id="sample-size-plan">`)
  in a translation of the `sampling_strategy` unit. Translate the text around
  it and leave it out: readers see the source's block in its place, and an
  edit carrying its id is refused.
- **Never include a Study's results block** (`<section id="study-results">`)
  in a translation of a Study unit (`study:<bundle id>`) either. The platform
  writes it from the Bundle's data in the source language; translate the
  Study's prose around it (its "Across waves" passage included) and leave the
  block out, as readers see the source's block in its place.
- **Keep identifiers and figures as written**: RQ-2, KPI names, numbers, units,
  dates and citations stay exactly as the source has them, in the visible
  text.
- **Write in the reader's formal register**, consistently across the paper:
  - `hu`: Ön; "read-only" is "írásvédett", never "csak olvasható"
  - `de`: Sie
  - `fr`: vous
  - `es`: usted

  Use the product's own words for its terms (Project, Campaign, Pool, Bundle,
  Study) as the product's pages in that language render them.
- Keep the meaning. Do not shorten, explain or improve the source; a
  translation that says more or less than the source misleads the reader.

Chat replies stay in the customer's own language, whatever language you
translate into.

## When an edit is refused

- **`blind_edit_refused`**: a token is missing or is not one a read answered.
  Read the unit with `unit_key` and send both tokens from that read.
- **`paper_stale`** naming the source: the source changed after you read it.
  Read the unit again and translate the new source text; never resend the old
  translation with new tokens.
- **`paper_stale`** naming the translation: someone wrote this translation
  since you read it. Read again and re-apply your change.
- **`anchor_not_unique`**: `old_string` occurs zero times or more than once
  (`match_count` says which). Quote more of the surrounding text so it occurs
  exactly once.
- **`fragment_refused`**: repair exactly the constructs it names, then retry
  once.
- **`paper_write_refused`** saying to replace it whole: the unit is `behind`;
  send its full text as `old_string` (step 4).
- **`paper_write_refused`** naming the Sample size or Study results block:
  your text carries the block's id. Remove the block and send the edit again.
- **`paper_write_refused`** otherwise: the language is the paper's source
  language, the unit has no source text, or the organization is sealed. Do not retry; tell
  the customer what the refusal said.
