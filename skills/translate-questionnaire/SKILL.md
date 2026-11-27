---
name: translate-questionnaire
description: Use when the customer asks to translate a questionnaire version into another language, or to fill the untranslated items of an existing translation after the source changed. Covers reading the source texts, the text-only rule, the target locale's register, partial saves with base_updated_at, and what to do when a save is refused.
---

# Translate a questionnaire

A translation is translated text beside one questionnaire version, one per
language. The source QML is never changed: flow, preconditions,
postconditions, code blocks, option codes and every Z3 verdict stay the
source's, so answers in every language are directly comparable. Respondents
are offered a language only once its translation is complete, and nothing
falls back to the source text item by item, so an incomplete translation is
invisible to them.

The questionnaire's own `language` is the source language and takes no
translation; a change there is a change to the QML itself.

## The tools

- `mcp__plugin_askalot_askalot__get_qml_content` — the current version of the
  questionnaire. Translate the `version_id` it answers, unless the customer
  named another version.
- `mcp__plugin_askalot_askalot__list_qml_translations` — one entry per
  supported locale except the source language: `started`, `withdrawn` (its
  translation was deleted), `complete`, the `untranslated` text keys, `frozen`,
  `human_edited` and `updated_at`. For a locale with `started` false the
  `untranslated` list is empty although every key is untranslated; its keys are
  in `get_qml_translation`'s `source_texts`.
- `mcp__plugin_askalot_askalot__get_qml_translation` — one locale's stored
  `texts`, its `updated_at`, and `source_texts`: every translatable text key
  with its source text, in document order. A locale with no translation yet
  answers empty `texts` and `updated_at` null.
- `mcp__plugin_askalot_askalot__save_qml_translation` — saves `texts` for one
  locale. The save is partial: the keys you send are merged over the stored
  text and every key you leave out keeps its stored text.

The three translation tools name `questionnaire_id` and `version_id`, and the
get and the save also `locale`: one of `en`, `es`, `fr`, `de`, `hu`, and never
the questionnaire's own language. No other language can be stored.

## Whole version or gaps only

Decide which the customer asked for, and say which you are doing.

- **Gaps only** ("fill what is missing", "the source changed, update the
  Hungarian"): call `list_qml_translations`, then send exactly the keys in
  that locale's `untranslated` list, and never resend a key that already has
  text. Text that is there may be a researcher's edit, and a gap-fill keeps
  it. After a source edit, unchanged items keep their translation and only
  the changed or new ones are listed. When the entry says `started` false
  there is nothing to fill: tell the customer the locale has no translation
  yet and do the whole version.
- **Whole version** (the locale has no translation yet, or the customer asks
  to translate everything): translate every key in `source_texts`. When the
  locale already has a translation with `human_edited` true, a person has
  edited it: ask the customer before overwriting their text, and fill only the
  gaps unless they confirm.

A `frozen` translation takes no save: a survey has been answered in it.

## Steps

1. Read the version with `get_qml_content` and note its `version_id`.
2. Call `list_qml_translations` for that version and pick the locale's entry.
3. Call `get_qml_translation` for the locale. Draft from `source_texts`, and
   keep its `updated_at`.
4. Translate the keys the request covers (above).
5. Call `save_qml_translation` with those keys in `texts` and `base_updated_at`
   set to the `updated_at` you read: `null` when the read answered no stored
   translation. A large version may go in several saves; each next save names
   the `updated_at` the previous save answered.
6. Tell the customer what the save answered: `complete`, or how many keys are
   still `untranslated`. Only a complete translation is offered to
   respondents.

The researcher may be asked to approve each save before it is written. A
denied save is their decision: do not resend it; ask what they want changed.

## Writing the text

- **Change text only.** A key names one text of the source; the value is that
  text in the target language. Never add, drop or rename a key, and never
  translate ids, option codes, variable names or conditions: ids, option codes
  and the logic stay the source's in every language.
- **Keep every HTML tag** the source text carries (`<b>`, `<i>`, `<br>`,
  links), in the same structure around the translated words. Markup such as
  `<script>` is refused.
- **Keep every placeholder** verbatim: anything in braces, `%s`-style
  markers, and numbers, units or names that the sentence refers to.
- **A positional list goes whole.** Matrix `rows` and `columns`, QuestionGroup
  `questions` and postcondition hints are keyed by position (`/rows/0`,
  `/rows/1`, ...): send every entry of such a list in one save, or none.
  Option `labels` are keyed by option code and may go one by one.
- **Write in the target locale's formal register**, never the informal one,
  and keep it consistent across the whole questionnaire:
  - ``es``: usted
  - ``fr``: vous
  - ``de``: Sie
  - ``hu``: Ön; a seed's aim opens "Annak kiderítése, hogy …", never
    "Annak feltárása"; "what should we improve" is "Mit javítsunk", never
    "Min javítsunk"

  English has no register split; write plain, neutral English.
- **Every label of a rating scale is a key**, the out-of-scale answers
  ("Don't know", "Does not apply") included; the translation is complete
  only with every one. Nothing supplies a scale's wording in any language:
  you translate each label. Items that share one label set in the source
  get the same translated set, word for word, so a battery and its sibling
  items read as one scale. Keep each step's strength (a "Somewhat" stays
  weaker than a "Very") and the same number of distinct labels; where the
  target language has an established wording for the scale, use it.
- Keep the meaning, the response scale's direction and the answer options'
  order. Do not shorten, explain or improve a question: a translation that
  says something else measures something else.

Chat replies stay in the customer's own language (`_user_locale`), whatever
language you translate into.

## When a save is refused

Every refusal says what clears it. Read again and retry once; if the retry is
refused too, stop and tell the customer what the refusal said.

- **Invalid keys, codes, lists or markup** (the refusal names each key): fix
  exactly the keys it names, then retry once.
- **`translation_conflict`** (the translation changed since you read it,
  usually a researcher's edit): read again with `get_qml_translation`,
  re-apply only the keys that are still untranslated, and retry once with the
  new `updated_at`.
- **A version of another questionnaire** (not found): read the questionnaire
  again with `get_qml_content` and name the `version_id` it answers.
- **A sealed organization** (forbidden): do not retry; nothing in it can be
  written.
- **`translation_frozen`**: do not retry. A survey has been answered in that
  language on this version. The fix goes into a new version of the
  questionnaire, translated there, and the campaign is moved onto it; tell the
  customer so.
- **The source language**: do not retry; that text is the QML itself.
