# Declarative Data Quality: Inline Validation During Administration

Instead of detecting and cleaning data quality problems after collection, use
QML postconditions to check answers while the respondent is still in the
interview and can correct them.

## Contents

- When a postcondition is the right tool
- Postcondition patterns: bounds that depend on another answer, consistency
  across related items, interlocking ranges, temporal consistency, sum-to-total
- Computed variables for complex validation
- What postconditions replace and what they cannot
- Anti-patterns: eligibility as a postcondition, over-validation, unhelpful
  hints, validating opinions

## When a Postcondition Is the Right Tool

A postcondition is checked when the respondent submits the answer; while a
predicate is false the hint is shown and the respondent is asked to correct the
answer. It replaces a cleaning step that would otherwise run after the
respondent has left. Use it for:

- relations between answers (children < household size, start year after birth
  year, parts summing to a total);
- bounds the control's `min`/`max` cannot express.

Do not use it to restate the control's own `min`/`max` (the validator reports
`duplicate_input_bound`), to screen respondents out (see Anti-Patterns), or to
police opinions.

A postcondition the engine cannot evaluate (it reads an item the respondent was
never asked, or skipped) lets the answer through unchecked and marks the survey
critical, which excludes it from datasets. Guard a reference to an item that may
be unasked with `q_x.outcome is None or (...)`; the `qml-syntax` and
`qml-preconditions` skills give the rule.

## Validation Categories and Postcondition Patterns

### 1. Range Checks and Logical Bounds

**Problem**: Respondents enter impossible or implausible values (negative
counts, unreasonable ages, values outside the logical range).

Fixed bounds belong on the control: an Editbox or Slider refuses an answer
outside its `min`/`max`. Add a postcondition only for a bound the control
cannot express, which is one that depends on another answer:

```yaml
- id: q_years_at_address
  kind: Question
  title: "How many years have you lived at your current address?"
  input:
    control: Editbox
    min: 0
    max: 120
  postcondition:
    - predicate: q_years_at_address.outcome <= q_age.outcome
      hint: "Years at this address cannot exceed your age."
```

### 2. Consistency Checks Across Related Items

**Problem**: Respondent gives contradictory answers (says "no children" then
reports children's ages, or household count doesn't align with family details).

```yaml
- id: q_has_children
  kind: Question
  title: "Do you have any children under 18?"
  input:
    control: Switch
    on: "Yes"
    off: "No"

- id: q_child_count
  kind: Question
  title: "How many children under 18 do you have?"
  precondition:
    - predicate: q_has_children.outcome == 1
  input:
    control: Editbox
    min: 1
    max: 20
```

When the respondent answers "No" to `q_has_children`, `q_child_count` is
skipped entirely (precondition). If they answer "Yes", the control's `min: 1`
enforces a count of at least 1. The impossible combinations are prevented by
routing and the control's domain, with no postcondition.

### 3. Interlocking Ranges

**Problem**: Multiple related numeric items should maintain ordering or sum
constraints (e.g., work hours across categories, household income
contributors vs. household size).

```yaml
- id: q_household_size
  kind: Question
  title: "Including yourself, how many people live in your household?"
  input:
    control: Editbox
    min: 1
    max: 15

- id: q_income_contributors
  kind: Question
  title: "How many household members contribute to income?"
  postcondition:
    - predicate: q_income_contributors.outcome <= q_household_size.outcome
      hint: "Income contributors cannot exceed total household size."
  input:
    control: Editbox
    min: 1
    max: 15
```

### 4. Temporal and Sequential Consistency

**Problem**: Respondent reports events in impossible order or with impossible
duration (e.g., graduation before enrollment, more work experience than age
allows).

```yaml
- id: q_birth_year
  kind: Question
  title: "What year were you born?"
  input:
    control: Editbox
    min: 1920
    max: 2010

- id: q_work_start_year
  kind: Question
  title: "What year did you start your first job?"
  postcondition:
    - predicate: q_work_start_year.outcome >= q_birth_year.outcome + 14
      hint: "Your first job must be at least 14 years after your birth year."
  input:
    control: Editbox
    min: 1940
    max: 2026

- id: q_years_experience
  kind: Question
  title: "How many years of total work experience do you have?"
  postcondition:
    - predicate: q_years_experience.outcome <= 2026 - q_work_start_year.outcome
      hint: "Work experience cannot exceed years since your first job."
  input:
    control: Editbox
    min: 0
    max: 60
```

The "not in the future" bound is the control's `max: 2026`; it is not repeated
as a postcondition.

### 5. Percentage and Proportion Validation

**Problem**: Respondent allocates percentages that don't sum to 100, or
proportions that exceed a total.

```yaml
- id: q_pct_work
  kind: Question
  title: "What percentage of your time do you spend on work?"
  input:
    control: Editbox
    min: 0
    max: 100

- id: q_pct_family
  kind: Question
  title: "What percentage of your time do you spend with family?"
  input:
    control: Editbox
    min: 0
    max: 100

- id: q_pct_leisure
  kind: Question
  title: "What percentage of your time do you spend on leisure?"
  postcondition:
    - predicate: q_pct_work.outcome + q_pct_family.outcome + q_pct_leisure.outcome == 100
      hint: "Your time allocation must total 100%. Currently it sums to a different amount."
  input:
    control: Editbox
    min: 0
    max: 100
```

Place the summation postcondition on the last item in the sequence so
all prior values are available. The respondent sees the constraint only
after entering the final value and can adjust any of the three items.

## Computed Variables for Complex Validation

When validation or routing logic becomes complex (3+ conditions, derived
scores), compute an intermediate variable in a `codeBlock`, then reference the
variable in the preconditions or postconditions of later items. Code blocks use
whole-number arithmetic only (`//`, never `/`).

```yaml
- id: calc_risk_score
  kind: Comment
  title: "Thank you. A few more questions about your health follow."
  codeBlock: |
    risk_score = 0
    if q_smoking.outcome == 1:
      risk_score = risk_score + 2
    if q_exercise_frequency.outcome < 3:
      risk_score = risk_score + 1
    if q_age.outcome >= 65:
      risk_score = risk_score + 1

- id: q_risk_acknowledgment
  kind: Question
  title: "Based on your responses, your health risk profile is elevated. Are you aware of preventive health programs in your area?"
  precondition:
    - predicate: risk_score >= 3
      hint: "Shown only for elevated risk profiles"
  input:
    control: Switch
    on: "Yes"
    off: "No"
```

This keeps each predicate simple. A Comment's title is shown to the
respondent, so word it for them; where no text is wanted, attach the
`codeBlock` to the last question whose answer it reads instead.

## The Postcondition Advantage: During vs. After Collection

### What Postconditions Replace

| Post-hoc cleaning step | QML postcondition equivalent |
|------------------------|------------------------------|
| Range check scripts | The control's `min` / `max` (not a postcondition) |
| Cross-variable consistency | `postcondition: predicate: q_a.outcome <= q_b.outcome` |
| Sum-to-total validation | `postcondition: predicate: q_x.outcome + q_y.outcome == 100` |
| Logical skip verification | Preconditions prevent invalid paths entirely |
| Impossible combination flags | Postconditions on dependent items |

### What Postconditions Cannot Replace

- **Outlier detection across respondents** — requires population-level analysis
- **Social desirability correction** — a measurement error, not a data error
- **Weighting adjustments** — requires comparing sample to target population
- **Interviewer effects** — not visible in one respondent's answers
- **Item nonresponse** — a respondent can still leave an item unanswered

## Anti-Patterns to Avoid

### Eligibility as a Postcondition

**Bad**: `q_age.outcome >= 18` as a postcondition on the age question. A minor
can never submit an answer: the interview is stuck, never completes, and the
screened-out answer is not in the data, so the eligibility rate cannot be
measured.

**Good**: accept the answer, gate the substantive blocks on it with a
block-level `precondition`, and close the screened-out path with a Comment (the
Screen-Out Routing pattern in the `qml-syntax` skill).

### Over-Validation

**Bad**: Too many postconditions frustrate respondents.

```yaml
# Don't do this — over-constrains a subjective response
- id: q_age_feel
  kind: Question
  title: "How old do you feel?"
  postcondition:
    - predicate: q_age_feel.outcome >= 18
    - predicate: q_age_feel.outcome <= 100
    - predicate: q_age_feel.outcome >= q_age.outcome - 20
    - predicate: q_age_feel.outcome <= q_age.outcome + 20
  input:
    control: Editbox
    min: 0
    max: 120
```

Only validate objective impossibilities, not subjective plausibility.
Someone aged 30 who "feels 80" is unusual but not invalid data.

**Good**: Validate only what is logically impossible.

```yaml
- id: q_age_feel
  kind: Question
  title: "How old do you feel?"
  input:
    control: Editbox
    min: 0
    max: 120
```

### Hidden Complexity in Hints

**Bad**: Complex postconditions with unhelpful hints.

```yaml
postcondition:
  - predicate: q_income.outcome * 35 // 100 <= q_taxes.outcome
    hint: "Inconsistent tax data."
```

The respondent has no idea what "inconsistent tax data" means or how to fix it.

**Good**: Simple rules with actionable hints.

```yaml
postcondition:
  - predicate: q_taxes.outcome <= q_income.outcome
    hint: "Taxes paid cannot exceed your total income. Please check both values."
```

### Validating Opinions

**Bad**: Using postconditions to enforce "logical" opinion patterns.

Opinions are inherently subjective. A respondent can be "very satisfied"
overall while dissatisfied with specific aspects — that's a legitimate
response pattern, not an error. Use consistency postconditions only for
factual contradictions, not attitudinal ones.

## Cost

Each failed check costs the respondent a correction, and every hint interrupts
the flow. Validate objective impossibilities only, and prefer routing and
control bounds, which cost the respondent nothing.
