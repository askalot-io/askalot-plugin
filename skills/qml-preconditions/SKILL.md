---
name: qml-preconditions
description: Use when writing preconditions, postconditions, or conditional logic in QML questionnaires. Covers block guards vs item preconditions, progressive disclosure patterns, and validation constraints.
---

# QML Preconditions and Conditional Logic Reference

## Scope

**Covers**: Precondition syntax, postcondition validation, progressive disclosure patterns, block guards vs item preconditions, conditional flow design.

**Does not cover**: QML item types, input controls, block structure (see qml-syntax skill), survey design methodology (see survey-design skill).

## Critical Rule: Gates Never Cascade From a Sibling Item

Blocks are displayed in their defined order, but items within a block are ordered by dependency topology -- items at the same dependency level can appear in any order. A precondition does NOT cascade from one item to the next: an item's gate covers that item only. Every conditional item must therefore be gated by its own complete condition -- either on the item, or by the block it sits in.

**If 5 questions apply only to adults, put them in one block whose block-level `precondition` is the adult gate (see "Hoisting Shared Gates") -- not the gate on the first question alone, and not 5 copies of it.** A block guard gates every item in its block; an item keeps its own precondition only for what is specific to it.

```yaml
# CORRECT: the shared adult gate sits on the block; q_income adds only its residual
- id: b_adult_employment
  precondition:
    - predicate: q_age.outcome >= 18
  items:
    - id: q_employment
      kind: Question
      title: "What is your employment status?"
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
        - predicate: q_employment.outcome == 1
      input:
        control: Editbox
        min: 0
        max: 1000000

# WRONG: outside a gated block, relying on q_employment's precondition to cascade
# - id: q_income
#   precondition:
#     - predicate: q_employment.outcome == 1
#   # Missing: q_age.outcome >= 18
```

The same rule reaches across gates. An item that was not asked has an outcome of
`None` at runtime. `None == 1` is false and `None != 1` is true, so an equality test
against an unasked item is safe; an ordering test (`q_x.outcome >= 18`) and arithmetic
(`q_x.outcome + 1`) raise. A precondition that raises is treated as **unsatisfied** and
the item is skipped -- the gate you could not check is honoured, not ignored -- and a
`degraded` warning is recorded against the survey. So a predicate that reads a
may-be-unasked item does not merely risk showing the wrong item: it reliably hides the
item for every respondent who did not answer the referenced one.

The validator flags this as `none_unsafe_reference` (a warning), naming both items,
whenever the referenced item is not asked on every path that reaches yours. Two ways to
fix it, and the lint accepts either:

```yaml
# 1. Guard the reference explicitly.
precondition:
  - predicate: q_dx_age.outcome is not None and q_dx_age.outcome >= 40
    hint: "Diagnosed at 40 or later"

# 2. Repeat the referenced item's own gate, so the two are always reached together.
precondition:
  - predicate: q_diabetes.outcome == 1        # the gate q_dx_age itself carries
    hint: "Diabetics only"
  - predicate: q_dx_age.outcome >= 40
    hint: "Diagnosed at 40 or later"
```

**They are not interchangeable — pick by what should happen to the owner item.** The
guard keeps the owner reachable exactly where it was, and only neutralises the reference.
Repeating the referent's gate narrows the owner's own reachability to match the
referent's, so anyone who reached the owner by another route stops seeing it. Guard when
the owner should stay reachable independently of the referent; repeat the gate when the
two items genuinely belong to the same branch and should always travel together.

An item gated on `q_pregnant.outcome != 1` needs neither: equality against `None` is
clean. Add the `q_sex.outcome == 2 and q_age.outcome <= 49` gate anyway when you mean
"asked and answered no", because `None != 1` and `2 != 1` are both true and the two say
very different things about the respondent.

**Asked and left unanswered is a different case, and the engine does not guess it.**
Everything above is about an item its own gate kept out. When the respondent was *shown*
an item and skipped it, its `None` means "unknown". A condition that reads it is then
decided only by the answers it has:
- `q_a.outcome == 1 or q_b.outcome == 1` still holds when `q_a` is 1 and `q_b` was
  skipped.
- A condition the skipped answer could still change is left undecided. A precondition
  then skips its item, and a postcondition lets the answer through. Both record a
  `degraded` warning (`precondition_unanswered_dependency` /
  `postcondition_unanswered_dependency`).

So `q_marital.outcome != 3` does **not** admit a respondent who skipped `q_marital`. If
an unknown answer should route somewhere specific, say so with an explicit `None` test,
which the engine evaluates as written:

```yaml
precondition:
  - predicate: q_marital.outcome is None or q_marital.outcome != 3
    hint: "Unknown or not single"
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

Multiple predicates in a list are ANDed -- all must be true for the item to show. A
precondition's `hint` is a note for authors (no respondent sees it); a postcondition's
`hint` is the message the respondent gets when the answer is refused.

## Postcondition Syntax

Postconditions validate responses after they are collected:

```yaml
postcondition:
  - predicate: q_children.outcome <= q_household_size.outcome
    hint: "Number of children cannot exceed household size"
```

Do not restate the control's own `min`/`max` as a postcondition (the validator reports
`duplicate_input_bound`).

A postcondition that cannot be evaluated fails the **other** way from a precondition:
the answer is accepted unchecked, and the survey is recorded `critical`, which excludes
it from dataset extraction. This is why a postcondition that orders against a
may-be-unasked item is the more expensive version of the mistake -- it costs the whole
row, not one item. Guard it with `is None`, which reads as "the rule does not apply":

```yaml
postcondition:
  - predicate: q_dx_age.outcome is None or q_age.outcome >= q_dx_age.outcome
    hint: "Your age cannot be less than your age at diagnosis"
```

Conditions live on **items and blocks only**. A block-level `precondition` /
`postcondition` applies to every item in the block and is evaluated before the item's
own. There is no questionnaire-level condition -- a root-level `precondition:` key is
never evaluated by anything, and the validator reports it as
`questionnaire_level_condition`.

## Progressive Disclosure Pattern

Use Switch/Radio as screening items, then gate the follow-ups. The follow-ups share one
guard, so they form their own block carrying it:

```yaml
- id: b_car
  items:
    - id: q_has_car
      kind: Question
      title: "Do you own a car?"
      input:
        control: Switch
        on: "Yes"
        off: "No"

- id: b_car_details
  precondition:
    - predicate: q_has_car.outcome == 1
  items:
    - id: q_car_brand
      kind: Question
      title: "What is your car's brand?"
      input:
        control: Dropdown
        labels:
          1: "Toyota"
          2: "Honda"
          3: "Ford"

    - id: q_car_satisfaction
      kind: Question
      title: "How satisfied are you with your car?"
      input:
        control: Slider
        min: 0
        max: 10
```

## Variable-Based Preconditions

Preconditions can reference variables set by codeBlocks. The variable must hold a value
on every path that reaches the reader (initialize it in `codeInit`), or the read raises
and the item is skipped; see qml-syntax §6.1:

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

This does not conflict with the critical rule above. That rule forbids relying on a
*sibling item's* precondition to cascade -- it never does. Hoisting moves the shared gate
*up a level* to the block, which legitimately gates every item the block contains.

The block guard reads only outcomes and variables produced **before** the block. It is
re-checked before every item, so a guard on a variable that a codeBlock inside the same
block assigns changes mid-block, and once two items write it the publish gate reports a
dependency cycle. A
Roster block can carry a guard as well -- false skips the whole loop, true lets it iterate
over `iterateOver` as usual.

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

### Screening Gate -- route, do not refuse
A screener's job is to decide who continues, and the screened-out answer is data (an
eligibility rate needs its denominator). A postcondition `q_eligible.outcome == 1` on the
screener refuses the *No*: the respondent cannot leave the item, the survey never
completes, and the *No* is never stored. Gate the substantive blocks on the screener
instead and close the screened-out path with a Comment:

```yaml
- id: b_screening
  items:
    - id: q_eligible
      kind: Question
      title: "Are you 18 or older?"
      input:
        control: Switch
        on: "Yes"
        off: "No"
    - id: q_screened_out
      kind: Comment
      title: "Thank you -- this survey is for adults only, and your answers end here."
      precondition:
        - predicate: q_eligible.outcome == 0

- id: b_main
  precondition:
    - predicate: q_eligible.outcome == 1
  items:
    # every substantive item; each still carries any residual gate of its own
```

Keep postconditions for **consistency** between answers (children <= household size,
sentenced implies convicted). A postcondition whose only satisfying answer is one value of
a two-value control is a mandated answer, and a mandated answer makes the other answer
unmeasurable.

### Multi-Level Screening
The outermost gate goes on the block; each inner item carries its residual in full,
because a sibling's gate does not cascade (`kind`, `title` and `input` omitted):
```yaml
- id: b_children
  precondition:
    - predicate: q_household_size.outcome > 1
  items:
    - id: q_has_children
    - id: q_children_count
      precondition:
        - predicate: q_has_children.outcome == 1
    - id: q_youngest_age
      precondition:
        - predicate: q_has_children.outcome == 1 and q_children_count.outcome >= 2
```

### Cross-Item Validation
```yaml
postcondition:
  - predicate: q_years_experience.outcome <= (q_age.outcome - 16)
    hint: "Work experience cannot exceed your working age"
```
