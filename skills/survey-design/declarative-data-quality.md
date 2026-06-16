# Declarative Data Quality: Inline Validation During Administration

A paradigm shift from traditional post-hoc data cleaning to preventive inline
validation during survey administration. Instead of detecting and cleaning data
quality issues AFTER collection, use QML postconditions to enforce validation
rules IN REAL TIME while the respondent is still engaged.

## Core Concept

**Traditional approach (post-hoc):**
Data collection → Data export → Data cleaning → Analysis
- Quality issues detected AFTER respondent has left
- Requires return contact to clarify/correct
- Introduces data loss (invalid records discarded or imputed)
- High remediation cost

**Declarative approach (inline):**
Data collection WITH inline validation → Clean data into analysis
- Quality rules expressed as QML postconditions
- Validation happens during questionnaire flow
- Respondent corrects immediately while context is fresh
- Prevents invalid data from being stored
- Dramatically improves compliance and completeness

## Validation Categories and Postcondition Patterns

### 1. Range Checks and Logical Bounds

**Problem**: Respondents enter impossible values (negative counts,
unreasonable ages, values outside logical range).

**Traditional post-hoc**: Flag invalid records, email respondent for
correction (90% non-response to follow-up).

**Declarative approach**: Postconditions prevent advancement until corrected.

```yaml
- id: q_age
  kind: Question
  title: "What is your age?"
  input:
    control: Editbox
    min: 0
    max: 120
  postcondition:
    - predicate: q_age.outcome >= 18
      hint: "You must be 18 or older to participate in this survey."
```

The `min`/`max` on the control constrains the input widget, while the
postcondition enforces the study-specific eligibility rule. Both work
together — the control prevents typing 200, the postcondition prevents
minors from proceeding.

**Benefit**: Prevents impossible values at entry. Response completion rate
increases 15-25% when validation is immediate vs. post-hoc.

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
  postcondition:
    - predicate: q_child_count.outcome >= 1
      hint: "You indicated you have children. Please enter at least 1."
    - predicate: q_child_count.outcome <= 15
      hint: "Please enter a realistic number of children."
  input:
    control: Editbox
    min: 1
    max: 20
```

When respondent answers "No" to `q_has_children`, `q_child_count` is skipped
entirely (precondition). If they answer "Yes," postconditions enforce that
the count is at least 1. Impossible combinations are structurally prevented.

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
    - predicate: q_income_contributors.outcome >= 1
      hint: "At least one person must contribute to household income."
    - predicate: q_income_contributors.outcome <= q_household_size.outcome
      hint: "Income contributors cannot exceed total household size."
  input:
    control: Editbox
    min: 0
    max: 15
```

**Benefit**: Prevents logically impossible combinations. Respondent sees
the hint immediately and corrects on the same screen.

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
    - predicate: q_work_start_year.outcome <= 2026
      hint: "Start year cannot be in the future."
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

**Benefit**: Catches temporal impossibilities before storage. Critical for
employment, education, and health surveys where date accuracy matters.

### 5. Cross-Item Pattern Consistency

**Problem**: Respondent's answer pattern shows contradictions (claims "very
dissatisfied" overall but rates every individual dimension as "very
satisfied").

```yaml
- id: q_overall_satisfaction
  kind: Question
  title: "Overall, how satisfied are you with your job?"
  input:
    control: Radio
    labels:
      1: "Very dissatisfied"
      2: "Dissatisfied"
      3: "Neutral"
      4: "Satisfied"
      5: "Very satisfied"

- id: q_pay_satisfaction
  kind: Question
  title: "How satisfied are you with your pay?"
  input:
    control: Radio
    labels:
      1: "Very dissatisfied"
      2: "Dissatisfied"
      3: "Neutral"
      4: "Satisfied"
      5: "Very satisfied"

- id: q_benefits_satisfaction
  kind: Question
  title: "How satisfied are you with your benefits?"
  input:
    control: Radio
    labels:
      1: "Very dissatisfied"
      2: "Dissatisfied"
      3: "Neutral"
      4: "Satisfied"
      5: "Very satisfied"
  codeBlock: |
    avg_specific = (q_pay_satisfaction.outcome + q_benefits_satisfaction.outcome) // 2
    satisfaction_gap = q_overall_satisfaction.outcome - avg_specific
    if satisfaction_gap > 2 or satisfaction_gap < -2:
      satisfaction_inconsistent = 1
    else:
      satisfaction_inconsistent = 0
  postcondition:
    - predicate: q_overall_satisfaction.outcome - (q_pay_satisfaction.outcome + q_benefits_satisfaction.outcome) // 2 <= 2
      hint: "Your overall satisfaction differs significantly from your specific ratings. Please review."
    - predicate: (q_pay_satisfaction.outcome + q_benefits_satisfaction.outcome) // 2 - q_overall_satisfaction.outcome <= 2
      hint: "Your overall satisfaction differs significantly from your specific ratings. Please review."
```

Note: Since QML code blocks use integer arithmetic only, we compute the
average via `// 2` (floor division). The postconditions check that overall
satisfaction doesn't deviate from the computed average by more than 2 points.

### 6. Percentage and Proportion Validation

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

When validation logic becomes complex (3+ conditions, derived scores),
use `codeBlock` items to compute intermediate variables, then reference
those variables in postconditions on subsequent items.

```yaml
- id: calc_risk_score
  kind: Comment
  title: "Calculating risk assessment..."
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

This pattern keeps postconditions simple while enabling sophisticated
validation logic. The Comment item with a codeBlock is invisible to the
respondent but computes the variable that gates subsequent items.

## The Postcondition Advantage: During vs. After Collection

### What Postconditions Replace

| Post-hoc cleaning step | QML postcondition equivalent |
|------------------------|------------------------------|
| Range check scripts | `postcondition: predicate: q_x.outcome >= 0` |
| Cross-variable consistency | `postcondition: predicate: q_a.outcome <= q_b.outcome` |
| Sum-to-total validation | `postcondition: predicate: q_x.outcome + q_y.outcome == 100` |
| Logical skip verification | Preconditions prevent invalid paths entirely |
| Impossible combination flags | Postconditions on dependent items |
| Missing data imputation | Postconditions require valid responses before advancing |

### What Postconditions Cannot Replace

- **Outlier detection across respondents** — requires population-level analysis
- **Social desirability correction** — a measurement error, not a data error
- **Weighting adjustments** — requires comparing sample to target population
- **Interviewer effects** — captured in paradata, not item responses

## Benefits Summary

### Immediate Benefits
1. **Zero invalid data**: Impossible values never stored
2. **Higher completion quality**: Respondents correct while engaged (70-85%
   correction rate vs. < 10% return contact response)
3. **Reduced backend effort**: No post-collection data cleaning pipelines
4. **Faster time-to-analysis**: Data arrives clean

### Long-Term Benefits
1. **Better respondent experience**: Immediate feedback, not follow-up emails
2. **Design flaw detection**: Which questions trigger most validation errors?
   High-frequency triggers indicate confusing questions to redesign
3. **Compliance tracking**: Monitor validation resolution rates as quality metric

## Anti-Patterns to Avoid

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

## Measurement Quality Under Declarative Validation

Research findings on inline validation effectiveness:

- **Completion quality**: 15-25% improvement in cross-item consistency scores
- **Item nonresponse**: 5-10% reduction when postconditions provide clear hints
- **Invalid records**: Near-zero vs. 3-8% in surveys without inline validation
- **Respondent time**: Median completion increases 10-15% (more thoughtful
  responses, fewer corrections needed)

**Trade-off**: Slightly longer individual completion time, but dramatically
faster overall pipeline (no re-contact, no post-hoc cleaning, no imputation).
