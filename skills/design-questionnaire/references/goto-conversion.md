# Converting GOTO-Based Questionnaires to Declarative QML

A printed or CATI questionnaire says **where to go next**; QML says **when each
item is relevant**. This reference is the conversion: the patterns that turn a
source's jumps, filters and edit checks into preconditions, postconditions and
codeBlocks, and the pitfalls ten real conversions hit. The QML syntax itself is
the `qml-syntax` skill.

## The fundamental shift

```
Q1: "Do you smoke?" → If Yes, go to Q3. If No, go to Q5.
```

In the imperative version the logic lives at the SOURCE question ("from Q1, go
to …"). In the declarative version it lives at the TARGET: Q3 appears when the
respondent smokes. Every conversion is this inversion.

A jump gates **every question it skips**, not only its target's neighbour:
"If No, go to Q20" from Q10 means Q11 to Q19 are asked only when Q10 was not
No. When those skipped questions form a run, the gate belongs on a block.

## Pattern 1: a jump becomes a block guard

```
Q10: "Are you employed?" If No, go to Q20.
Q11: "What is your job title?"
Q12: "Years at current job?"
Q20: "What is your education level?"
```

The skipped run (Q11, Q12) goes in its own block, and the jump's negation is
that block's **block-level precondition**. Block and item conditions are
AND-ed at evaluation time, so the guard gates every item in the block; nothing
is copied onto the items.

```yaml
- id: b_screen
  items:
    - id: Q10
      kind: Question
      title: "Are you employed?"
      input:
        control: Switch
        "off": "No"
        "on": "Yes"
- id: b_employment
  title: "Employment"
  precondition:
    - predicate: Q10.outcome == 1
      hint: "Asked of employed respondents"
  items:
    - id: Q11
      kind: Question
      title: "What is your job title?"
      input:
        control: Textarea
    - id: Q12
      kind: Question
      title: "Years at current job?"
      input:
        control: Editbox
        min: 0
        max: 50
- id: b_education
  items:
    - id: Q20
      kind: Question
      title: "What is your education level?"
      input:
        control: Radio
        labels:
          1: "High School"
          2: "Bachelor's"
          3: "Master's"
```

A single skipped question keeps its gate on the item. An item carries its own
precondition only for what is specific to it (a follow-up to one answer
inside a guarded block).

### Multi-branch routing

```
Q5: "Employment status?"
  1=Full-time → Q10   2=Part-time → Q10   3=Unemployed → Q20   4=Retired → Q30
```

Each branch target section is its own block, guarded by the answers that lead
to it: `Q5.outcome in [1, 2]` on the Q10 block, `Q5.outcome == 3` on the Q20
block, `Q5.outcome == 4` on the Q30 block.

## Pattern 2: a classification variable (PATH)

Some CATI systems set a classification variable early (PATH, STATUS, TYPE) and
route on it for the rest of the survey. It maps to codeInit, a codeBlock that
assigns it, and block guards that read it.

```yaml
qmlVersion: "2.7"
questionnaire:
  title: "Labour force"
  codeInit: |
    path = 0
  blocks:
    - id: b_classification
      items:
        - id: q100_worked
          kind: Question
          title: "Did you work at a job or business last week?"
          input:
            control: Switch
            "off": "No"
            "on": "Yes"
          codeBlock: |
            if q100_worked.outcome == 1:
                path = 1
    - id: b_employed_details
      precondition:
        - predicate: path == 1
      items:
        - id: q110_class_of_worker
          kind: Question
          title: "In this job, is the person an employee or self-employed?"
          input:
            control: Radio
            labels:
              1: "Employee"
              2: "Self-employed"
```

Prefer a direct outcome reference whenever one item decides the route
(`q100_worked.outcome == 1`): a variable is only as verified as its wiring.
Use a variable only when the route depends on several items or computed state,
and give it a codeInit value every branch handles.

## Pattern 3: section skips

"If age < 16 or age > 65, skip the Labour Force section" is a block guard on
the section's block:

```yaml
- id: b_labour_force
  title: "Labour Force"
  precondition:
    - predicate: q_age.outcome >= 16 and q_age.outcome <= 65
  items:
    - id: q_lf_status
      kind: Question
      title: "Did you look for work in the past four weeks?"
      input:
        control: Switch
        "off": "No"
        "on": "Yes"
```

## Pattern 4: edit checks become postconditions

```
CATI CHECK at Q136: "If Q136 > 52, display error: layoff cannot exceed 52 weeks"
CATI CHECK at Q155: "If Q153 + Q154 + Q155 > Q152, display error"
```

```yaml
- id: q155_unpaid_extra
  kind: Question
  title: "Hours of unpaid extra work"
  postcondition:
    - predicate: q153_paid_overtime.outcome + q154_unpaid_overtime.outcome + q155_unpaid_extra.outcome <= q152_actual_hours.outcome
      hint: "Overtime and extra hours cannot exceed total actual hours worked"
  input:
    control: Editbox
    min: 0
    max: 80
```

- A **hard edit** (must fix) is a postcondition the source states.
- A **soft edit** (a warning) and a check taken from an interviewer instruction
  ("probe if hours > 80") are **invented**: the source does not state them as
  hard rules. An import marks each with `invented: true` on the postcondition;
  respondents and translators never see the marker.
- Prevent a contradiction rather than let it be corrected later: when an
  option is invalid whenever the item is reached, drop the option or check it.

Checks the source only implies (a part cannot exceed its whole, an age at an
event cannot exceed the current age) are mined in the inventory stage with six
trigger patterns; see the inventory builder's Constraint Mining.

## Pattern 5: converging paths

- All paths reach Q5 → Q5 has no precondition.
- Some paths reach Q200 → one `or` predicate:
  `path == 1 or path == 2 or path == 4`.
- A jump that bypasses the usual route ("If 'believes no work available', go
  to Q190 regardless of PATH") needs its own flag, set in a codeBlock and read
  in the target's guard.

## Pattern 6: chains

```
Q130 → if temporary layoff → Q132 → if business conditions → Q133 → if yes → Q134
```

Each item's precondition references its immediate predecessor only:
`q130.outcome == 8` on Q132, `q132.outcome == 6` on Q133, `q133.outcome == 1`
on Q134. Z3 handles the transitivity.

## Pattern 7: filter gates

A screener that gates a detailed sub-section is the most commonly missed
pattern, because it reads like just another routing step.

- **Count gates** ("count symptoms answered Yes; if fewer than 5, skip"): a
  counter in codeInit, one increment in each symptom item's codeBlock, and the
  count in the sub-section's block guard (`dep_symptom_count >= 5`). `sum()` is
  not available to the solver; increment item by item.
- **Severity gates** ("if Excellent or Very Good, skip the chronic-conditions
  module"): the module's block guard reads the rating directly
  (`q_health_rating.outcome >= 3`).

Any "if [condition], skip to [distant question]" over a detailed follow-up is
almost always a filter gate.

## Pattern 8: rosters

A loop over household members, children or jobs is a `kind: Roster` block: its
`iterateOver` is a bitmask (often a Checkbox answer) and its items are asked
once per set bit (see the `qml-syntax` skill, Block Kinds). A fixed small
maximum ("up to 4 children") can also be a QuestionGroup when every
sub-question shares one control.

## Pattern 9: composite scores

A score computed from several answers and routed on is computed in **one**
codeBlock, on the last scored item, never spread over partial sums:

```yaml
- id: q_symptom_3
  kind: Question
  title: "Rate symptom 3"
  input:
    control: Slider
    min: 1
    max: 5
  codeBlock: |
    risk_score = q_symptom_1.outcome + q_symptom_2.outcome + q_symptom_3.outcome
    if risk_score < 6:
        risk_level = 1
    else:
        risk_level = 2
```

The follow-up sections are blocks guarded by `risk_level == 1` and
`risk_level == 2`.

## Pattern 10: external inputs

A value the routing reads that no question collects (a sample-file prefill, a
proxy flag, a rotation status, a split-ballot group) becomes an item with
`external: true` in a preamble block, the first block of the file. The hosting
system supplies its value; when it cannot, the item is asked. Gates read its
outcome directly.

```yaml
- id: b_preamble
  title: "Interview setup"
  items:
    - id: q_pre_is_proxy
      kind: Question
      title: "Is this interview being completed by a proxy respondent?"
      external: true
      input:
        control: Switch
        "off": "No"
        "on": "Yes"
```

The two wrong ways: a bare name with no producer fails open at runtime and is
a free symbol to Z3 (`undefined_name`); a codeInit constant with no producer
is frozen, so every gate on it is statically decided (`frozen_variable`, and
its gated items unreachable).

## Variable feedback loops

A cycle forms when item A reads variable `v` in a condition and item B, which
depends on A, writes `v`. Trace the variable back to its source first: when a
single item set it, reference that item's outcome directly and the cycle is
gone (`q_100.outcome != 3` instead of `path != 7`). Keep a routing variable
only for state that depends on several items.

## Common pitfalls

### 1. A jump gates the whole skipped run

In GOTO, "go to Q5" skips everything up to Q5. Converting only the target's
neighbour leaves the rest of the skipped run asked of everyone:

```yaml
# WRONG: only Q11 is gated, Q12 is shown to everyone
- id: Q11
  kind: Question
  precondition:
    - predicate: Q10.outcome == 1
- id: Q12
  kind: Question
```

The fix is Pattern 1: the skipped run is a block whose block-level
precondition is the jump's negation.

### 2. Don't know / Refused

Keep DK and RF as label codes (`8: "Don't know"`, `9: "Refused"`) when they
route or matter to analysis, and exclude them in gates that need a substantive
answer (`q_answer.outcome in [1, 3]`).

### 3. Notes that route

"[females only]" or "Ask only if respondent is over 18" is not a GOTO, but it
is routing: a precondition on that item (`q_sex.outcome == 2`).

### 4. Parallel sections with hidden divergences

Near-identical sections (spouse and ex-partner modules) often differ in a skip
condition or a DK branch. Convert each from its own routing.

### 5. Age-gate boundaries

"Aged 15 to 64" is `q_age.outcome >= 15 and q_age.outcome <= 64`. Use the
source's exact boundaries; sections of one questionnaire often disagree.

### 6. Proxy and respondent-type exclusions

"ASK ONLY IF SELF-RESPONSE" gates read the proxy flag, which is an external
input (Pattern 10) unless a question asks it.

### 7. "Other (specify)"

An "Other" option almost always has a write-in follow-up: a Textarea item gated
on that option (`q_transport.outcome == 5`).

### 8. "First YES wins" cascades

A sequence of checks where the first Yes routes away and skips the rest must
not share one routing variable: every reader that also writes it forms a
cycle. Each later check reads the earlier checks' outcomes directly, so the
graph stays acyclic:

```yaml
- id: b_abcde
  items:
    - id: q_breathing_diff
      kind: Question
      title: "Breathing difficulty?"
      input:
        control: Switch
        "off": "No"
        "on": "Yes"
    - id: q_behavior
      kind: Question
      title: "Behaviour change?"
      precondition:
        - predicate: q_breathing_diff.outcome == 0
      input:
        control: Switch
        "off": "No"
        "on": "Yes"
    - id: q_seizures
      kind: Question
      title: "Seizures?"
      precondition:
        - predicate: q_breathing_diff.outcome == 0 and q_behavior.outcome == 0
      input:
        control: Switch
        "off": "No"
        "on": "Yes"
```
