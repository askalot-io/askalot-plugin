---
name: qml-preconditions
description: Use when writing preconditions, postconditions, or conditional logic in QML questionnaires. Covers per-item precondition rules, progressive disclosure patterns, and validation constraints.
---

# QML Preconditions and Conditional Logic Reference

## Scope

**Covers**: Precondition syntax, postcondition validation, progressive disclosure patterns, per-item precondition rules, conditional flow design.

**Does not cover**: QML item types, input controls, block structure (see qml-syntax skill), survey design methodology (see survey-design skill).

## Critical Rule: Per-Item Preconditions Required

Blocks are displayed in their defined order, but items within a block are ordered by dependency topology -- items at the same dependency level can appear in any order. Preconditions do NOT cascade or inherit from earlier items. Every conditional item must carry its own complete precondition list.

**If 5 questions apply only to adults, ALL 5 must have their own `precondition:` -- not just the first one.**

```yaml
# CORRECT: Each item has its own precondition
- id: q_employment
  kind: Question
  title: "What is your employment status?"
  precondition:
    - predicate: q_age.outcome >= 18
  input:
    control: Radio
    labels:
      1: "Employed"
      2: "Unemployed"
      3: "Student"

- id: q_income
  kind: Question
  title: "What is your annual income?"
  precondition:
    - predicate: q_age.outcome >= 18
    - predicate: q_employment.outcome == 1
  input:
    control: Editbox
    min: 0
    max: 1000000

# WRONG: Relying on q_employment's precondition to cascade
# - id: q_income
#   precondition:
#     - predicate: q_employment.outcome == 1
#   # Missing: q_age.outcome >= 18
```

## Precondition Syntax

Preconditions and postconditions are **lists of predicates**, each with a `predicate` field and optional `hint`:

```yaml
precondition:
  - predicate: q_age.outcome >= 18
    hint: "Adults only"
  - predicate: q_consent.outcome == 1
    hint: "Requires consent"
```

Multiple predicates in a list are ANDed -- all must be true for the item to show.

## Postcondition Syntax

Postconditions validate responses after they are collected:

```yaml
postcondition:
  - predicate: q_children.outcome <= q_household_size.outcome
    hint: "Number of children cannot exceed household size"
  - predicate: q_children.outcome >= 0
    hint: "Cannot be negative"
```

## Progressive Disclosure Pattern

Use Switch/Radio as screening items, then gate follow-up items with preconditions:

```yaml
- id: q_has_car
  kind: Question
  title: "Do you own a car?"
  input:
    control: Switch
    on: "Yes"
    off: "No"

- id: q_car_brand
  kind: Question
  title: "What is your car's brand?"
  precondition:
    - predicate: q_has_car.outcome == 1
  input:
    control: Dropdown
    labels:
      1: "Toyota"
      2: "Honda"
      3: "Ford"

- id: q_car_satisfaction
  kind: Question
  title: "How satisfied are you with your car?"
  precondition:
    - predicate: q_has_car.outcome == 1
  input:
    control: Slider
    min: 0
    max: 10
```

## Variable-Based Preconditions

Preconditions can reference variables set by codeBlocks:

```yaml
- id: q_risk_followup
  kind: Question
  title: "Would you like a detailed risk assessment?"
  precondition:
    - predicate: risk_score >= 30
  input:
    control: Switch
    on: "Yes"
    off: "No"
```

## Complex Preconditions

Combine multiple conditions with `and`/`or`:

```yaml
precondition:
  - predicate: q_age.outcome >= 18 and q_marital_status.outcome == 2
  - predicate: employment_status == "employed"
```

## Overlapping Preconditions

Overlapping preconditions across multiple items are explicitly OK. Do not optimize or deduplicate -- cover the research brief thoroughly. Each item must be independently conditional.

## Common Patterns

### Screening Gate
```yaml
- id: q_eligible
  kind: Question
  title: "Are you 18 or older?"
  input:
    control: Switch
    on: "Yes"
    off: "No"
  postcondition:
    - predicate: q_eligible.outcome == 1
      hint: "You must be 18 or older to participate"
```

### Multi-Level Screening
```yaml
- id: q_has_children
  precondition:
    - predicate: q_household_size.outcome > 1
- id: q_children_count
  precondition:
    - predicate: q_household_size.outcome > 1
    - predicate: q_has_children.outcome == 1
- id: q_children_ages
  precondition:
    - predicate: q_household_size.outcome > 1
    - predicate: q_has_children.outcome == 1
    - predicate: q_children_count.outcome >= 1
```

### Cross-Item Validation
```yaml
postcondition:
  - predicate: q_years_experience.outcome <= (q_age.outcome - 16)
    hint: "Work experience cannot exceed your working age"
```
