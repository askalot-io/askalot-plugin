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

## Hoisting Shared Gates

When one predicate guards **every** item in a block, do not repeat it on each item --
hoist it to the block's `precondition`. A block-level precondition applies to every item
in the block (it is AND-ed with each item's own precondition at evaluation time), so one
gate covers them all and each item keeps only its **item-specific residual**.

This does not conflict with the per-item rule above. That rule forbids relying on a
*sibling item's* precondition to cascade -- it never does. Hoisting moves the shared gate
*up a level* to the block, which legitimately gates every item the block contains.

- **Shared by all items in a block** -> move the gate to the block `precondition`; items keep residuals only.
- **Shared by some items** (gated and ungated interleaved) -> factor the gated items into their own Group block carrying the shared gate. QML blocks do not nest inside an item's `items:`, so a dedicated sibling Group block is the scoping mechanism.
- **Not shared** -> keep the gate on the individual item.

### Shared gate -> block precondition

```yaml
# WRONG: q_adult.outcome == 1 repeated on every item in the block
- id: b_adult_module
  kind: Group
  items:
    - id: q_income
      kind: Question
      title: "What is your annual income?"
      precondition:
        - predicate: q_adult.outcome == 1
      input:
        control: Editbox
        min: 0
        max: 1000000
    - id: q_employment
      kind: Question
      title: "What is your employment status?"
      precondition:
        - predicate: q_adult.outcome == 1
      input:
        control: Radio
        labels:
          1: "Employed"
          2: "Unemployed"

# RIGHT: hoist the shared gate to the block; each item carries only its residual
- id: b_adult_module
  kind: Group
  precondition:
    - predicate: q_adult.outcome == 1
  items:
    - id: q_income
      kind: Question
      title: "What is your annual income?"
      # no item precondition -- the block gate covers it
      input:
        control: Editbox
        min: 0
        max: 1000000
    - id: q_employment
      kind: Question
      title: "What is your employment status?"
      precondition:
        # only the item-specific residual remains
        - predicate: q_income.outcome > 50000
      input:
        control: Radio
        labels:
          1: "Employed"
          2: "Unemployed"
```

### Interleaved gates -> dedicated Group block

When only some items share a gate, do not hoist it to the whole block -- that would gate
the ungated items too. Put the gated items in their own Group block with the shared gate
as the block precondition. Blocks display in their defined order, so place the follow-up
block immediately after the block that produces its gate:

```yaml
- id: b_health
  kind: Group
  items:
    - id: q_general_health
      kind: Question
      title: "How would you rate your general health?"
      input:
        control: Radio
        labels:
          1: "Poor"
          2: "Fair"
          3: "Good"
    - id: q_smokes
      kind: Question
      title: "Do you currently smoke?"
      input:
        control: Switch
        on: "Yes"
        off: "No"

- id: b_smoker_followup
  kind: Group
  precondition:
    - predicate: q_smokes.outcome == 1
  items:
    - id: q_cigs_per_day
      kind: Question
      title: "How many cigarettes per day?"
      input:
        control: Editbox
        min: 1
        max: 100
    - id: q_quit_attempts
      kind: Question
      title: "How many times have you tried to quit?"
      input:
        control: Editbox
        min: 0
        max: 50
```

The gated items move together under one block gate; each still carries any residual
unique to it.

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
