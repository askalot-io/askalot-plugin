---
name: survey-design
description: Use when designing survey questions, choosing response scales, ordering items, or applying cognitive foundations to questionnaire design. Covers question wording, scale design, response categories, filter patterns, and data quality.
---

# Survey Design Advice Index

Nine reference files sit beside this `SKILL.md`. Each stands alone: read the
one or two files the task needs (the tables below say which), not all nine.
`filter-patterns.md`, `declarative-data-quality.md` and
`adaptive-survey-design.md` contain QML examples; the QML language itself is
the `qml-syntax` skill.

## Available Files

| File | Topic | When to Use |
|------|-------|-------------|
| `adaptive-survey-design.md` | Large instruments (100+ items): screening-first architecture, module-based design, hub-and-spoke routing, item budgeting, planned missingness | Planning the module structure of a large or complex questionnaire |
| `cognitive-foundations.md` | Four-stage response model, context effects, priming, anchoring, cognitive load | Explaining why a wording or ordering choice matters |
| `declarative-data-quality.md` | Postcondition patterns: bounds a control cannot express, cross-item consistency, interlocking ranges, temporal order, sum-to-total; over-validation anti-patterns | Writing or reviewing postconditions |
| `filter-patterns.md` | Preconditions, block-level guards, screen-then-detail, multi-level screening, derived routing variables, when a screening question pays for itself | Writing or reviewing conditional routing |
| `question-ordering.md` | Thematic grouping, opening and sensitive items, filter-before-follow-up, fatigue-aware ordering, grid spacing, buffer questions | Sequencing questions within and across blocks |
| `question-wording.md` | Simple language and syntax, ambiguity, specificity, leading and double-barreled questions, recall and reference periods, response-order and acquiescence effects | Writing or reviewing question stems |
| `response-categories.md` | Exhaustive and exclusive categories, forced-choice vs. check-all, ranking, "Don't know" / "Not applicable", open-ended items | Designing answer options |
| `response-quality.md` | Satisficing, length and fatigue thresholds, straightlining, speeding, attention checks | Keeping data quality in a long survey |
| `scale-design.md` | Unipolar vs. bipolar, scale length, verbal labels, branching bipolar, scale by construct type | Building rating and ordinal scales |

## Which File for Which Problem

| Problem in the questionnaire | Read |
|------------------------------|------|
| Few items carry a precondition (under about 20%), or everyone is asked everything | `filter-patterns.md` |
| No postconditions | `declarative-data-quality.md` first, then `filter-patterns.md` for the preconditions that keep a check from firing on an unasked item |
| No `codeInit` or `codeBlock` although routing depends on several answers | `filter-patterns.md` |
| One block holding 8 or more items | `question-ordering.md` |
| Scale problems (length, labels, polarity) | `scale-design.md`, `question-wording.md` |
| Wording problems | `question-wording.md` |
| Answer-option problems | `response-categories.md` |
| A respondent's path exceeds about 20 minutes | `response-quality.md` |
| Long grids, or complex items late in the survey | `response-quality.md`, `question-ordering.md` |
| 100+ items without a screening block or module gates | `adaptive-survey-design.md`, `filter-patterns.md` |
| Collected data shows straightlining, speeding or late-survey quality loss | `response-quality.md` |
