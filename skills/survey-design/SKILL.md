---
name: survey-design
description: Use when designing survey questions, choosing response scales, ordering items, or applying cognitive foundations to questionnaire design. Covers question wording, scale design, response categories, filter patterns, and data quality.
---

# Survey Design Advice Index

Maps quality issues to relevant advice files for selective injection.

## Available Files

| File | Topic | When to Use |
|------|-------|-------------|
| `adaptive_survey_design.md` | Large instruments (100+ items), screening-first architecture, module-based design, hub-and-spoke routing, item budgeting | Large or complex questionnaires |
| `cognitive_foundations.md` | Four-stage response model, context effects, priming, anchoring, cognitive load | Understanding why design choices matter |
| `declarative_data_quality.md` | Inline validation via postconditions, range checks, cross-item consistency, interlocking ranges, temporal validation, the paradigm shift from post-hoc cleaning to during-collection enforcement | Designing postcondition patterns for data quality |
| `filter_patterns.md` | Preconditions, progressive disclosure, multi-level screening, derived variables, strategic screening for large instruments | Conditional routing and branching |
| `question_ordering.md` | Thematic grouping, fatigue-aware ordering, grid spacing, context effect management | Sequencing questions within and across blocks |
| `question_wording.md` | Single-barreled questions, simple language, specificity, completeness, construct operationalization, response bias mitigation | Writing clear question stems and operationalizing constructs |
| `response_categories.md` | Exhaustive/exclusive categories, forced-choice, DK/NA guidance, open-ended response tips | Designing answer options |
| `response_quality.md` | Satisficing theory, survey fatigue thresholds, straightlining, speeding, attention checks | Maintaining data quality in long surveys |
| `scale_design.md` | Unipolar vs. bipolar, scale length, verbal labels, branching bipolar, construct-specific scales | Rating and ordinal scale construction |

## Issue Mapping

| Quality Issue Key      | Advice File(s)                        | When to Inject |
|------------------------|---------------------------------------|----------------|
| `low_preconditions`    | `filter_patterns.md`                  | <20% precondition ratio |
| `no_postconditions`    | `declarative_data_quality.md`, `filter_patterns.md` | Zero postconditions |
| `no_code_blocks`       | `filter_patterns.md`                  | No codeInit or codeBlock items |
| `single_block`         | `question_ordering.md`                | Single block with 8+ items |
| `poor_scales`          | `scale_design.md`, `question_wording.md` | Detected scale design issues |
| `poor_wording`         | `question_wording.md`                 | Detected wording issues |
| `poor_categories`      | `response_categories.md`              | Detected category issues |
| `data_quality_concern` | `response_quality.md`                 | Post-collection quality metrics below threshold |
| `too_many_items`       | `adaptive_survey_design.md`           | 100+ items without sufficient routing |
| `survey_too_long`      | `response_quality.md`                 | Estimated completion > 20 minutes |
| `high_satisficing_risk`| `response_quality.md`                 | Long grids, late-survey complex items |
| `no_screening`         | `adaptive_survey_design.md`, `filter_patterns.md` | Large instrument without screening hub |

## Default Injection

For `low_preconditions`, inject `filter_patterns.md` as it contains
the most actionable QML patterns for progressive disclosure.

For `no_postconditions`, inject `declarative_data_quality.md` first
(postcondition patterns and the inline validation paradigm) and
`filter_patterns.md` second (precondition patterns that complement
postconditions).

For `single_block`, inject `question_ordering.md` to guide block
organization.

For large instruments (`too_many_items`, `no_screening`), inject
`adaptive_survey_design.md` for module-based routing architecture.

For quality concerns in long surveys (`survey_too_long`,
`high_satisficing_risk`), inject `response_quality.md` for fatigue
management and satisficing prevention strategies.
