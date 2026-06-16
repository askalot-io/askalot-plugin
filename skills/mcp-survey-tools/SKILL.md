---
name: mcp-survey-tools
description: Use when completing a survey as a respondent. Covers get_survey_current_item (returns current step with folded options), submit_survey_response, and finish_survey tools.
---

# MCP Survey Completion Tools Reference

## Scope

**Covers**: Survey navigation and response submission via Portor MCP server.

**Does not cover**: Campaign management, sampling strategy, quality assessment.

## Available Tools

### get_survey_current_item

Get the current step to answer. Returns the question text, type, available options, and any constraints in a single folded response `{item, options, status}`.

**When to use**: At the start of the survey and after each response submission to get the next question.

### submit_survey_response

Submit your answer to the current question. The response value depends on the question type.

**When to use**: After deciding on your answer for the current question.

### finish_survey

Finalize the survey after all questions have been answered.

**When to use**: When `get_survey_current_item` indicates the survey is complete.

## Response Workflow

1. Call `get_survey_current_item` to see the current question (includes valid options in the response)
2. Call `submit_survey_response` with your chosen answer
3. Repeat until the survey reports completion
4. Call `finish_survey` to finalize
