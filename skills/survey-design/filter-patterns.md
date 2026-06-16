# Filter and Branching Patterns

Rules for designing conditional question flows in QML.

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

**Key advantages of the list format:**
- Each predicate can have its own descriptive hint
- Predicates are evaluated independently — the solver can pinpoint
  which specific constraint fails
- Easier to add or remove individual conditions without editing
  complex boolean expressions

## Progressive Disclosure

Every follow-up question must be gated by a precondition on the
screening answer. Respondents should never see questions that don't
apply to them.

Pattern in QML:
```yaml
- id: q_has_children
  type: Switch
  label: "Do you have any children under 18?"
  options: [Yes, No]

- id: q_num_children
  type: Number
  label: "How many children under 18 do you have?"
  precondition:
    - predicate: q_has_children.outcome == 1
  min: 1
  max: 20
```

## Screen-Then-Detail Pattern

The most common filter pattern is a binary Screen -> Detail flow:

1. **Screen** (Switch/Radio): binary or categorical gate question
2. **Detail** (any type): one or more follow-up items with preconditions

Multiple detail items can share the same precondition — overlapping
preconditions are normal and acceptable.

## Multi-Level Screening

For complex populations, use cascading filters:

1. Level 1: "Do you work?" (Yes/No)
2. Level 2: "Are you self-employed or employed by others?" (precondition: works)
3. Level 3: "How many employees does your business have?" (precondition: self-employed)

Each level narrows the eligible population. In QML, each item's
precondition references the answer from the previous screen.

## Multiple Predicates for Compound Conditions

Use multiple predicate entries instead of combining conditions into a
single boolean expression. This gives the solver and respondent clearer
feedback:

```yaml
precondition:
  - predicate: q_has_children.outcome == 1
    hint: "Only for parents"
  - predicate: q_employed.outcome == 1
    hint: "Only for employed respondents"
```

Both predicates must be true (conjunction). Each has its own hint
describing why that condition exists.

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
  type: Switch
  label: "Are you interested in topic A?"
  options: [Yes, No]
  codeBlock: |
    if q_interest_1.outcome == 0:
      consecutive_no = consecutive_no + 1
    else:
      consecutive_no = 0

- id: q_interest_2
  type: Switch
  label: "Are you interested in topic B?"
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

When branching logic becomes complex (3+ conditions), use codeBlock
items to compute a routing variable, then precondition on that variable:

```yaml
- id: calc_segment
  type: codeBlock
  codeBlock: |
    if q_age.outcome < 30 and q_income.outcome > 50000:
      segment = 1  # young_affluent
    elif q_age.outcome >= 65:
      segment = 2  # retired
    else:
      segment = 0  # general

- id: q_retirement_plan
  type: Radio
  label: "What is your primary retirement income source?"
  precondition:
    - predicate: segment == 2
      hint: "Retirement questions for respondents aged 65+"
  options: [Pension, Savings, Social Security, Other]
```

## Data Quality Validation

Use postconditions to enforce consistency between filter answers
and follow-up responses:

```yaml
- id: q_num_children
  type: Number
  label: "How many children under 18 do you have?"
  precondition:
    - predicate: q_has_children.outcome == 1
  postcondition:
    - predicate: q_num_children.outcome >= 1
      hint: "You indicated you have children — please enter at least 1."
    - predicate: q_num_children.outcome <= 20
      hint: "Please enter a realistic number of children."
```

## Per-Item Preconditions (No Inheritance)

**CRITICAL**: Blocks are displayed in their defined order, but items
within a block are ordered by dependency topology — items at the same
dependency level can appear in any order. Preconditions do NOT
cascade or inherit from earlier items.

Every conditional item must carry its own complete precondition list.
If an entire block of questions applies only to adults, EVERY item
in that block must have its own precondition — not just the first one:

```yaml
- id: q_employment_type
  precondition:
    - predicate: q_age.outcome >= 18
  ...

- id: q_employment_duration
  precondition:
    - predicate: q_age.outcome >= 18
  ...
```

When the precondition expression is complex, compute a flag variable
in a codeBlock and precondition all items on that flag:

```yaml
- id: calc_eligible
  type: codeBlock
  codeBlock: |
    eligible = 1 if (q_age.outcome >= 18 and q_consent.outcome == 1) else 0

- id: q_detailed_1
  type: Radio
  precondition:
    - predicate: eligible == 1
  ...

- id: q_detailed_2
  type: Slider
  precondition:
    - predicate: eligible == 1
  ...
```

This keeps each item self-contained while avoiding repetition of
long expressions.

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

## Routing Architecture for 500+ Item Surveys

### Hub-and-Spoke Pattern

For instruments with 10+ topic modules, use a central routing hub:

```
Universal Screening Hub (all respondents)
    │
    ├── compute eligibility flags (codeBlock items)
    │
    ├── Module A: Housing ── if is_homeowner == 1
    ├── Module B: Children ── if has_children == 1
    ├── Module C: Employment ── if is_employed == 1
    ├── Module D: Health ── if health_eligible == 1
    ├── Module E: Finance ── if has_financial_products == 1
    └── Module F: Retirement ── if age >= 55
```

The hub computes all eligibility flags in codeBlock items. Each spoke
module's items carry preconditions on the corresponding flag. A
respondent sees only the modules matching their profile.

In QML: the hub is the first block. Subsequent blocks correspond to
modules. All items in a module block share a precondition on the
eligibility flag.

### Sequential Gating

Within a spoke module, use sequential gates for sub-topics:

```yaml
# Module E: Finance (gated by has_financial_products == 1)

- id: q_has_savings
  type: Switch
  label: "Do you have a savings account?"
  precondition:
    - predicate: has_financial_products == 1

- id: q_has_investments
  type: Switch
  label: "Do you have any investment accounts?"
  precondition:
    - predicate: has_financial_products == 1

# Sub-gate: savings details (only if has savings)
- id: q_savings_amount
  type: Radio
  label: "Approximately how much do you have in savings?"
  precondition:
    - predicate: has_financial_products == 1
    - predicate: q_has_savings.outcome == 1
```

Keep nesting depth to 2-3 levels. Deeper nesting makes the survey
structure hard to maintain and validate.

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

# After screening block:
- id: calc_profile
  type: codeBlock
  codeBlock: |
    is_parent = 1 if q_has_children.outcome == 1 else 0
    is_employed = 1 if q_employment_status.outcome in [1, 2] else 0
    is_homeowner = 1 if q_housing_type.outcome in [1, 2] else 0
    household_complexity = is_parent + is_employed + is_homeowner
```

Later modules reference profile flags instead of re-evaluating raw
screening answers. This keeps preconditions simple and readable across
the entire instrument.
