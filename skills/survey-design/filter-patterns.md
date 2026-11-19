# Filter and Branching Patterns

Rules for designing conditional question flows in QML.

## Contents

- Preconditions and Postconditions Are Lists
- Progressive Disclosure / Screen-Then-Detail / Multi-Level Screening
- Runtime State Accumulation
- Derived Variables for Complex Routing
- Data Quality Validation
- Gate a Run of Items at the Block (the rule for any guard shared by two or more items)
- Strategic Screening for Large Instruments (when to screen, cost-benefit)
- Routing Architecture for Large Instruments (hub-and-spoke, sequential gating, variable accumulation)

## Preconditions and Postconditions Are Lists

Preconditions and postconditions are **lists of predicates**, not single
strings. Each predicate has a `predicate` field and an optional `hint`.
Multiple predicates form a conjunction (all must be true).

```yaml
precondition:
  - predicate: q_has_children.outcome == 1
    hint: "Only for respondents with children"
  - predicate: q_age.outcome >= 18
    hint: "Adults only"
```

Postconditions use the same structure — the `hint` is shown to the
respondent when a validation rule is violated:

```yaml
postcondition:
  - predicate: q_income_contributors.outcome <= q_household_size.outcome
    hint: "Contributors cannot exceed household size"
  - predicate: q_income_contributors.outcome >= 1
    hint: "At least one person must contribute"
```

Write a compound condition as several predicates rather than one
`and` expression: each predicate carries its own hint, and the solver
can name the one that fails.

## Progressive Disclosure

Every follow-up question is gated on the screening answer, so that
respondents never see questions that don't apply to them. A single
follow-up carries the gate as its own precondition; two or more
follow-ups sharing the gate go in their own block with a block-level
`precondition` (see "Gate a Run of Items at the Block").

Pattern in QML:
```yaml
- id: q_has_children
  kind: Question
  title: "Do you have any children under 18?"
  input:
    control: Switch
    on: "Yes"
    off: "No"

- id: q_num_children
  kind: Question
  title: "How many children under 18 do you have?"
  precondition:
    - predicate: q_has_children.outcome == 1
  input:
    control: Editbox
    min: 1
    max: 20
```

## Screen-Then-Detail Pattern

The most common filter pattern is a binary Screen -> Detail flow:

1. **Screen** (Switch/Radio control): binary or categorical gate question
2. **Detail** (any control): one or more follow-up items with preconditions

When several detail items share the gate, put them in their own block
and write the gate once, as the block-level `precondition`.

## Multi-Level Screening

For complex populations, use cascading filters:

1. Level 1: "Do you work?" (Yes/No)
2. Level 2: "Are you self-employed or employed by others?" (precondition: works)
3. Level 3: "How many employees does your business have?" (precondition: self-employed)

Each level narrows the eligible population. In QML, each item's
precondition references the answer from the previous screen.

## Runtime State Accumulation

codeBlocks and variables are not just for routing — they track runtime
state as the respondent progresses through the questionnaire. Use cases:

- **Running counters**: count consecutive negative responses, track how
  many times a category was selected across items
- **Aggregation**: compute totals, averages, or indices from prior answers
- **Pattern detection**: detect response patterns and adapt the flow
- **Adaptive gating**: skip a section after N negative responses in a row

Example — stop asking after 3 consecutive "No" responses:

```yaml
codeInit: |
  consecutive_no = 0

- id: q_interest_1
  kind: Question
  title: "Are you interested in topic A?"
  input:
    control: Switch
    on: "Yes"
    off: "No"
  codeBlock: |
    if q_interest_1.outcome == 0:
      consecutive_no = consecutive_no + 1
    else:
      consecutive_no = 0

- id: q_interest_2
  kind: Question
  title: "Are you interested in topic B?"
  input:
    control: Switch
    on: "Yes"
    off: "No"
  precondition:
    - predicate: consecutive_no < 3
      hint: "Skipped after 3 consecutive negative responses"
  codeBlock: |
    if q_interest_2.outcome == 0:
      consecutive_no = consecutive_no + 1
    else:
      consecutive_no = 0
```

## Derived Variables for Complex Routing

When branching logic becomes complex (3+ conditions), compute a
routing variable in a `codeBlock`, then precondition on that variable.
A `codeBlock` is a key of an item, not an item kind (`kind` is one of
Comment/Question/QuestionGroup/MatrixQuestion). Attach it to the last
question whose answer it reads, or to a Comment; a Comment's title is
shown to the respondent, so give it text they can read (a section
introduction), not a description of the computation.

```yaml
- id: calc_segment
  kind: Comment
  title: "Thank you. The next questions depend on your answers so far."
  codeBlock: |
    if q_age.outcome < 30 and q_income.outcome > 50000:
      segment = 1  # young_affluent
    elif q_age.outcome >= 65:
      segment = 2  # retired
    else:
      segment = 0  # general

- id: q_retirement_plan
  kind: Question
  title: "What is your primary retirement income source?"
  precondition:
    - predicate: segment == 2
      hint: "Retirement questions for respondents aged 65+"
  input:
    control: Radio
    labels:
      1: "Pension"
      2: "Savings"
      3: "Social Security"
      4: "Other"
```

## Data Quality Validation

Use postconditions to enforce consistency between a follow-up and
other answers. Do not restate the control's own `min`/`max` in a
postcondition: the control already enforces them, and the validator
reports the duplicate as `duplicate_input_bound`. Patterns:
`declarative-data-quality.md`.

```yaml
- id: q_num_children
  kind: Question
  title: "How many children under 18 do you have?"
  precondition:
    - predicate: q_has_children.outcome == 1
  input:
    control: Editbox
    min: 1
    max: 20
  postcondition:
    - predicate: q_num_children.outcome < q_household_size.outcome
      hint: "The number of children must be smaller than your household size."
```

## Gate a Run of Items at the Block

A QML block has three jobs: **grouping** (a topical section),
**branching** (one guard for a run of items) and **repetition**
(`kind: Roster`, one pass per selected entity). Skip logic that
applies to a whole run of items is the second job.

**The rule:** a run of two or more items that share one guard
belongs in its own block carrying that guard as the block-level
`precondition`. The engine composes block + item conditions at
evaluation time (block first, then item, AND-ed), so the block guard
gates every item in the block, and the Z3 validator composes them
the same way. An item keeps its own precondition only for what is
specific to that item.

```yaml
- id: b_adult_employment
  title: "Employment"
  precondition:
    - predicate: q_age.outcome >= 18     # one guard for the whole run
  items:
    - id: q_employment_type
      kind: Question
      title: "..."                       # no item precondition needed
    - id: q_employment_duration
      kind: Question
      precondition:
        - predicate: q_employment_type.outcome == 1   # item-specific only
      title: "..."
```

What does **not** carry over is one *sibling item's* precondition to
the next: items within a block are ordered by dependency topology,
and an item's precondition never gates the item after it. If only
some items of a section share a guard, split them into their own
sibling block (QML blocks do not nest) rather than hoisting the guard
onto the whole section.

Two constraints on the guard:

- **Read only what is settled before the block.** The guard reads
  outcomes and variables produced by items *earlier* than the block.
  The guard is re-checked before every item, so one that reads a
  variable assigned by a codeBlock inside the same block changes
  mid-block, and once two items write it the publish gate reports a
  dependency cycle.
- **Place the block after its producer.** Blocks follow file order,
  so put the guarded block after the block that asks the screening
  question or computes the flag.

When the guard expression is complex, compute a flag in a codeBlock
before the block, and guard the block on the flag:

```yaml
- id: b_screening
  items:
    - id: calc_eligible
      kind: Comment
      title: "Thank you for these first answers."
      codeBlock: |
        eligible = 1 if (q_age.outcome >= 18 and q_consent.outcome == 1) else 0

- id: b_detailed
  precondition:
    - predicate: eligible == 1
  items:
    - id: q_detailed_1
      kind: Question
      title: "..."
      input:
        control: Radio
        labels: { 1: "...", 2: "..." }
    - id: q_detailed_2
      kind: Question
      title: "..."
      input:
        control: Slider
        min: 0
        max: 10
```

A Roster block can carry a block guard too: when the guard is false
the whole loop is skipped, and when it is true the Roster iterates
over `iterateOver` as usual.

## Strategic Screening for Large Instruments

In instruments with 100+ items, screening is not just about filtering
individual follow-ups — it determines which entire topic modules a
respondent sees. The screening strategy is the most important design
decision in a large survey.

### When to Screen vs. Ask All

Use screening when:
- The question applies to less than ~70% of respondents (screening
  saves more time than it costs)
- The answer is predictable from a short gate question
- The follow-up section has 3+ items (worth the cost of a gate)

Ask all respondents when:
- The question applies universally (e.g., general attitudes)
- Screening would take as long as the question itself
- You need complete data without imputation

### Multi-Stage Screening

For complex instruments, use coarse-to-fine screening:

1. **Stage 1 — Universal screening** (all respondents, 2-3 minutes):
   Demographics, household composition, key attributes. Produces
   eligibility flags for all major modules.

2. **Stage 2 — Module-level gates** (start of each eligible module):
   One question confirming the topic applies. Example: screening
   flags that the respondent is employed, but the finance module
   gate asks "Do you have any retirement savings accounts?"

3. **Stage 3 — Sub-topic gates** (within modules): Further refinement.
   Example: within the housing module, a gate for mortgage vs. rental
   questions.

Each stage narrows the population. The cost of each screening question
(10-15 seconds) is justified by the time saved from skipping irrelevant
items.

### Attribute Discovery Questions

Some questions exist primarily for routing, not data collection. These
**attribute discovery** questions should be:

- **Binary or low-cardinality**: Yes/No or 3-4 clear categories.
  More options mean more routing paths to maintain.
- **Unambiguous**: The answer must clearly determine downstream
  eligibility. Avoid "sometimes" or "partly" options.
- **Cheap to answer**: Under 15 seconds. The respondent's time
  investment should go toward substantive questions.
- **Grouped early**: Place all attribute discovery questions before
  the modules they gate.

### Cost-Benefit of Screening

Every screening question costs respondent time (~12 seconds) but
saves the time of all gated questions for ineligible respondents.

Rule of thumb: add a screening question when:
```
(gated_item_count * avg_seconds_per_item * pct_ineligible) > 12 seconds
```

Example: 8 gated items * 15 sec each * 40% ineligible = 48 seconds
saved > 12 seconds cost. Screening is worthwhile.

If only 10% of respondents are ineligible and the gated section has
2 items, the savings (2 * 15 * 0.10 = 3 seconds) don't justify the
12-second screening question.

## Routing Architecture for Large Instruments

### Hub-and-Spoke Pattern

For instruments with 10+ topic modules, use a central routing hub:

```
Universal Screening Hub (all respondents)
    │
    ├── compute eligibility flags (codeBlocks)
    │
    ├── Module A: Housing ── if is_homeowner == 1
    ├── Module B: Children ── if has_children == 1
    ├── Module C: Employment ── if is_employed == 1
    ├── Module D: Health ── if health_eligible == 1
    ├── Module E: Finance ── if has_financial_products == 1
    └── Module F: Retirement ── if age >= 55
```

The hub computes all eligibility flags in codeBlocks. Each spoke
module is a block guarded by a block-level precondition on its flag.
A respondent sees only the modules matching their profile.

In QML: the hub is the first block. Subsequent blocks correspond to
modules, and each module block carries its eligibility flag as its
block `precondition`, written once rather than on every item.

### Sequential Gating

Within a spoke module, use sequential gates for sub-topics:

```yaml
# Module E: Finance: the module gate sits on the block
- id: b_finance
  precondition:
    - predicate: has_financial_products == 1
  items:
    - id: q_has_savings
      kind: Question
      title: "Do you have a savings account?"
      input:
        control: Switch
        on: "Yes"
        off: "No"

    - id: q_has_investments
      kind: Question
      title: "Do you have any investment accounts?"
      input:
        control: Switch
        on: "Yes"
        off: "No"

    # Sub-gate: savings details (only if has savings), item-specific
    - id: q_savings_amount
      kind: Question
      title: "Approximately how much do you have in savings?"
      precondition:
        - predicate: q_has_savings.outcome == 1
      input:
        control: Radio
        labels:
          1: "Under $1,000"
          2: "$1,000–$10,000"
          3: "Over $10,000"
```

A sub-gate that covers two or more items becomes its own sibling
block after `b_finance`, guarded by `q_has_savings.outcome == 1`
(the module gate already holds for anyone who answered it).

Keep gate depth (module gate, sub-topic gate, item gate) to 2-3
levels. Deeper gating makes the survey structure hard to maintain and
validate.

### Variable Accumulation

As the respondent progresses, accumulate derived variables that
simplify downstream routing:

```yaml
codeInit: |
  # Profile flags computed in screening hub
  is_parent = 0
  is_employed = 0
  is_homeowner = 0
  household_complexity = 0  # sum of applicable modules

# Last item of the screening block (a Comment carrying the computation;
# its title is shown to the respondent):
- id: calc_profile
  kind: Comment
  title: "Thank you. The next sections depend on your answers so far."
  codeBlock: |
    is_parent = 1 if q_has_children.outcome == 1 else 0
    is_employed = 1 if q_employment_status.outcome in [1, 2] else 0
    is_homeowner = 1 if q_housing_type.outcome in [1, 2] else 0
    household_complexity = is_parent + is_employed + is_homeowner
```

Later modules reference profile flags instead of re-evaluating raw
screening answers. This keeps preconditions simple and readable across
the entire instrument.
