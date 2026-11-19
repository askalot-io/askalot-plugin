---
name: mcp-survey-tools
description: Use when completing a survey as a simulated respondent (a preview or synthetic run). Covers get_survey_current_item (returns current step with folded options), submit_survey_response, and finish_survey tools.
---

# MCP Survey Completion Tools Reference

## Scope

**Covers**: Survey navigation and response submission via Portor MCP server.

**Does not cover**: Campaign management, sampling strategy, quality assessment.

**Simulated respondents only.** These tools walk previews and synthetic test runs. They never answer for a real person: the server refuses them on a survey that has been sent to a respondent. A real respondent who wants to take their survey with an AI assistant connects their own assistant to the survey's respondent connector (`/respond/mcp`), and there the respondent clicks every answer themselves.

## Available Tools

### get_survey_current_item

Input: `survey_id`. Returns the current step as one folded response:

- `status` -- `in_progress` or `completed`. `completed` means there is no further item.
- `item` -- `{id, kind, text, extras}`. `id` is the `item_id` you submit against; `kind` is `Question`, `QuestionGroup` or `MatrixQuestion`; `extras.input` holds the control's configuration (`min`, `max`, `step`, `labels`).
- `control_type` -- lowercase control name: `radio`, `dropdown`, `listbox`, `checkbox`, `slider`, `switch`, `editbox`, `range`, `textarea`.
- `options` -- for a choice control `[{value, text}]`, where `value` is the answer code to submit; for a slider `[{type: "range", min, max, step}]`; for a switch `[{value: true, text: "Yes"}, {value: false, text: "No"}]`; empty for `editbox`, `range` and `textarea` (read the bounds from `item.extras.input`).
- `required` -- whether the item must be answered.

Comment items are skipped by the server, so every step returned is one to answer.

**When to use**: Once, at the start of the survey. After that, `submit_survey_response` returns the next step itself; read again only when you no longer hold the current step (for example after a refused submission you cannot place).

### submit_survey_response

Input: `survey_id`, `item_id` (the current step's `item.id`) and `outcome`. Returns `{status, output, next}`: `next` is the following step in the same shape `get_survey_current_item` returns, and is null once `status` is `completed`.

The shape of `outcome` follows the item's `kind` and `control_type`:

| Control | `outcome` |
|---|---|
| `radio`, `dropdown`, `listbox` | The chosen option's `value` (an integer code) |
| `checkbox` | One integer: the sum of the selected options' `value` codes (a bitmask), not a list |
| `slider`, `editbox` | A number within the item's `min`..`max` |
| `range` | A pair `[low, high]` within `min`..`max`, `low <= high` |
| `switch` | `true` or `false` |
| `textarea` | Free text (the only control answered with text) |

A `QuestionGroup` takes a list with one such value per sub-question; a `MatrixQuestion` takes a nested list, rows x columns.

A value the engine refuses comes back as a tool error carrying the reason, and the survey does not advance: correct the value and submit the same `item_id` again.

**When to use**: After deciding on your answer for the current question.

### finish_survey

Input: `survey_id`. Marks the survey completed and returns `status: "completed"`, or `"already_completed"` when the last submission had already closed it. Calling it twice is harmless.

**When to use**: Once, when a step reports `status: "completed"`.

## Response Workflow

1. Call `get_survey_current_item` once to see the first question and its options
2. Call `submit_survey_response` with the step's `item.id` and your answer
3. Answer the step returned in `next`; repeat until a response has `status: "completed"`
4. Call `finish_survey` to finalize
