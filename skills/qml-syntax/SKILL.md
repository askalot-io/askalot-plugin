---
name: qml-syntax
description: Use when generating, validating, or debugging QML questionnaire YAML. Covers all item types, controls, preconditions, postconditions, codeBlocks, and block structure.
---

# QML (Questionnaire Markup Language) Creation Guide

## Design Philosophy: Axiomatic Approach

QML uses an **axiomatic approach** to questionnaire design. Instead of manually constructing control flow and dependency graphs, you declare **constraints** (preconditions and postconditions) and let the SMT solver (Z3) verify consistency automatically.

**Think declaratively, not imperatively:**
- Define **what** must be true (postconditions), not **how** to enforce it
- Define **when** a question applies (preconditions), not **how** to navigate to it
- Define **valid values** for each answer (ranges or label sets), not **how** to validate input
- The Z3 solver automatically checks reachability, constraint satisfaction, and logical consistency

This lowers cognitive load: focus on translating requirements into constraints. The solver handles the rest.

## QML Overview

QML is a YAML-based markup language for creating formally verified survey questionnaires. All code blocks are statically analyzed by a Z3 SMT solver for reachability, constraint satisfaction, and logical consistency. This means **only the Python subset that Z3 can reason about** should be used in code blocks — features that work at runtime but are invisible to the solver undermine the formal verification model.

## Core Structure

### 1. Root Structure
Every QML file must begin with:
```yaml
qmlVersion: "2.0"
questionnaire:
  title: "Your Questionnaire Title"
  blocks:
    - # Block definitions
```

### 2. Blocks - The Primary Organization Unit
Blocks group related items (questions) together. Items within a block can depend on each other, but cross-block dependencies should be minimized for better maintainability and clearer survey flow.

```yaml
blocks:
  - id: b_demographics
    title: "Demographic Information"
    items:
      - # Item definitions
```

**Best Practices for Blocks:**
- Use meaningful block IDs that describe the section (e.g., `b_demographics`, `b_preferences`, `b_satisfaction`)
- Group thematically related questions together
- Keep dependencies within blocks whenever possible
- Consider blocks as logical survey sections or pages

**A block can carry its own `precondition` and `postcondition`.** A block-level
`precondition` gates every item in the block (it is AND-ed with each item's own
precondition at evaluation time, and the Z3 builder composes them the same way). It is
the sanctioned way to make a whole section depend on an earlier answer — an optional
module gated on a core item, a renter-costs block gated on tenure — without repeating the
gate on every item. A block-level `postcondition` is evaluated before each inner item's
own postconditions. Read `qml-preconditions` ("Hoisting Shared Gates") for when to hoist
a gate to the block and when to factor gated items into their own block.

```yaml
- id: b_renter_costs
  title: "Renter Costs"
  precondition:
    - predicate: q_tenure.outcome == 3   # only renters see this whole block
  items:
    - id: q_monthly_rent
      kind: Question
      title: "What is the monthly rent?"
      input:
        control: Editbox
        min: 1
        max: 99999
```

### 2b. Block Kinds

Every block has a `kind`. Two kinds exist; `kind` is optional and defaults to `Group`:

| Kind | Description |
|------|-------------|
| `Group` | Default (omit `kind` for this). Asks each in-scope item once in canonical order. Optional `count: N` (positive integer literal) caps the block to the first N eligible items — a deterministic first-N cap, not random selection. |
| `Roster` | Repeat inner items per set bit in an `iterateOver` integer bitmask. Required: `iterateOver` (Python expression → non-negative int bitmask) and `labels` (map of power-of-2 keys to display strings). Optional: `subjectFrom` (the id of an inner item whose answer becomes the iteration's displayed subject). |

**`count` is a deterministic first-N cap.** The block walks its items in canonical order; an item whose precondition is true consumes a slot, an item whose precondition is false is a free pass, and the draw stops once `count` slots are filled or the pool is exhausted. There is no randomness — the same answers always yield the same asked set. Inner items of a `count`-capped Group **must be independent** (no inner item may depend on another inner item of the same Group); a Group without `count` may contain inner dependencies. `count` applies only to `Group` — a Roster must not declare it.

**Static validation (Z3) is kind-aware:**
- Roster unrolls per label-key into bit-guarded copies.
- A `count`-capped Group marks each inner item conditionally-present (any item beyond the cap is reachable, never dead code). A Group without `count` emits its items unconditionally.

#### Group with `count` example

```yaml
qmlVersion: "2.0"
questionnaire:
  title: "Knowledge Check"
  blocks:
    - id: question_pool
      kind: Group
      count: 3
      items:
        - id: q_topic_a
          kind: Question
          title: "Topic A question"
          input:
            control: Radio
            labels:
              1: "Correct"
              2: "Incorrect"
        - id: q_topic_b
          kind: Question
          title: "Topic B question"
          input:
            control: Radio
            labels:
              1: "Correct"
              2: "Incorrect"
        - id: q_topic_c
          kind: Question
          title: "Topic C question"
          input:
            control: Radio
            labels:
              1: "Correct"
              2: "Incorrect"
        - id: q_topic_d
          kind: Question
          title: "Topic D question"
          input:
            control: Radio
            labels:
              1: "Correct"
              2: "Incorrect"
```

With `count: 3`, the first 3 of the 4 independent items are asked in canonical order; the 4th is absent. An item whose precondition is false is skipped without consuming a slot. The four items are independent of one another, as a capped Group requires.

#### Roster example

```yaml
qmlVersion: "2.0"
questionnaire:
  title: "Meal Tracker"
  blocks:
    - id: meal_selection
      kind: Group
      items:
        - id: q_meals_eaten
          kind: Question
          title: "Which meals did you eat today?"
          input:
            control: Checkbox
            labels:
              1: "Breakfast"
              2: "Lunch"
              4: "Dinner"

    - id: per_meal
      kind: Roster
      iterateOver: "q_meals_eaten.outcome"
      labels:
        1: "Breakfast"
        2: "Lunch"
        4: "Dinner"
      items:
        - id: q_satisfaction
          kind: Question
          title: "How satisfied were you?"
          input:
            control: Slider
            min: 1
            max: 5
```

#### Roster subject: `subjectFrom`

Each Roster iteration is shown under its `labels` entry ("Person 2", "Lunch"). When the
respondent names the subject themselves — a household member, a product, an employer —
declare `subjectFrom: <inner item id>` and the iteration is titled with that item's
answer once it is given, falling back to the static label until then. The item it names
must be an inner item of the Roster that carries an outcome (a Question, typically a
Textarea for a name). Naming a Comment makes the subject unresolvable, and the validator
reports it (`roster_subject_not_answerable`) because every iteration would silently show
the static label instead of the thing it is about.

```yaml
- id: b_household_members
  kind: Roster
  iterateOver: "person_mask"
  subjectFrom: q_member_name
  labels:
    1: "Person 1"
    2: "Person 2"
    4: "Person 3"
  items:
    - id: q_member_name
      kind: Question
      title: "What is this person's name?"
      input:
        control: Textarea
    - id: q_member_age
      kind: Question
      title: "How old is this person?"
      input:
        control: Editbox
        min: 0
        max: 120
```

`iterateOver` may name a Checkbox outcome directly or a bitmask variable a codeBlock
derives (for example, widening a head-count into `person_mask`); either way the labels
must cover every bit the mask can set.

### 3. Items - The Question Types

QML supports four types of items:

#### 3.1 Comment (Information Display)
Used for instructions or informational text:
```yaml
- id: q_intro
  kind: Comment
  title: "Please answer the following questions honestly."
```

#### 3.2 Question (Single Response)
For individual questions with scalar outcomes:
```yaml
- id: q_age
  kind: Question
  title: "What is your age?"
  input:
    control: Editbox
    min: 18
    max: 120
```

#### 3.3 QuestionGroup (List of Related Questions)
For multiple questions sharing the same response format. The outcome is a list of integers:
```yaml
- id: q_satisfaction_aspects
  kind: QuestionGroup
  title: "Rate your satisfaction with:"
  questions:
    - "Customer service"
    - "Product quality"
    - "Delivery speed"
  input:
    control: Radio
    labels:
      1: "Very Dissatisfied"
      2: "Dissatisfied"
      3: "Neutral"
      4: "Satisfied"
      5: "Very Satisfied"
```

#### 3.4 MatrixQuestion (Grid of Responses)
For questions with row/column structure. The outcome is a table of integers.

For structural postcondition patterns specific to matrices — symmetry, fixed-sum
allocation, and ranking/distinctness — see [`matrix-constraint-patterns.md`](matrix-constraint-patterns.md).

```yaml
- id: q_language_proficiency
  kind: MatrixQuestion
  title: "Rate language proficiency for family members"
  rows:
    - "English"
    - "Spanish"
    - "French"
  columns:
    - "Mother"
    - "Father"
    - "Sibling"
  input:
    control: Radio
    labels:
      0: "None"
      1: "Basic"
      2: "Intermediate"
      3: "Fluent"
```

### 4. Input Controls

Every Question, QuestionGroup, and MatrixQuestion MUST have an `input` block. The required properties depend on the control type:

- **Range-based controls** (Editbox, Slider, Range): require `min` and `max`
- **Label-based controls** (Radio, Dropdown, Checkbox): require `labels` mapping integer keys to display text
- **Switch**: requires `on` and `off` display text

**`default` is a hint, never an answer.** The renderer shows it — a marked
Radio option, the Dropdown's placeholder, the Editbox's placeholder, the resting
position of a Slider or Range thumb — but records nothing until the respondent
interacts: Next on an untouched item stores no answer (`None`). So do not use
`default` to make an item "pre-answered", and do not rely on it to satisfy a
postcondition; a required answer is a postcondition's job, and "none of these"
is a declared option, not an untouched Checkbox.

#### 4.1 Switch (Binary Choice)
```yaml
input:
  control: Switch
  on: "Yes"
  off: "No"
  default: 0  # Optional, not rendered: a Switch starts on neither side
```

The outcome is `1` for `on` and `0` for `off`. `on`/`off` is the spelling the JSON
schema declares. The renderer also accepts `true`/`false` as label keys (a spelling many
existing instruments use — YAML parses them as booleans and the schema does not reject
them), so read either in a file you are editing; write `on`/`off` in new files so the
schema and the file say the same thing. Never leave a Switch without labels: it renders
as a bare toggle and the respondent cannot tell which way is "yes".

#### 4.2 Radio (Single Selection)
```yaml
input:
  control: Radio
  labels:
    1: "Option 1"
    2: "Option 2"
    3: "Option 3"
  default: 1  # Optional hint: must be a key from labels
```

#### 4.3 Checkbox (Multiple Selection)
```yaml
input:
  control: Checkbox
  labels:
    1: "Option A"   # Binary value: 1
    2: "Option B"   # Binary value: 2
    4: "Option C"   # Binary value: 4
    8: "Option D"   # Binary value: 8
  default: 0  # Optional, not rendered: every box starts unticked
```

#### 4.4 Dropdown (Single Selection from List)
```yaml
input:
  control: Dropdown
  labels:
    1: "High School"
    2: "Bachelor's Degree"
    3: "Master's Degree"
    4: "Doctorate"
  left: "Education:"  # Optional prefix
  right: ""           # Optional suffix
```

#### 4.5 Editbox (Numeric Input)
```yaml
input:
  control: Editbox
  min: 0
  max: 100
  left: "I am"
  right: "years old"
  default: 25  # Optional hint: must be between min and max
```

#### 4.6 Slider (Visual Range Selection)
```yaml
input:
  control: Slider
  min: 0
  max: 10
  step: 1
  default: 5
  labels:
    0: "Not at all"
    5: "Somewhat"
    10: "Extremely"
```

#### 4.7 Range (Interval Selection)
Captures a min-max interval from the respondent. The two values are encoded as a single integer via Szudzik pairing.
```yaml
input:
  control: Range
  min: 0
  max: 1000
  step: 50
  left: "$"
  right: ""
  labels:
    0: "$0"
    500: "$500"
    1000: "$1000"
```

#### 4.8 Textarea (Free Text)

Captures open-ended text. The outcome is a **string**, not an integer — Z3 ignores it
entirely (no variable is created), so a Textarea outcome must never appear in a
precondition, postcondition, or codeBlock predicate. Use it for verbatim answers only.

```yaml
input:
  control: Textarea
  placeholder: "Describe your experience in your own words"  # Optional
  maxLength: 500  # Optional: maximum characters
```

#### 4.9 Choosing the Right Control

| Use Case | Control | Value Definition |
|---|---|---|
| Yes/No binary choice | Switch | `on`/`off` labels |
| Precise number (age, children count) | Editbox | `min`/`max` range |
| Approximate/subjective scale (satisfaction, mood) | Slider | `min`/`max`/`step` range |
| Numeric interval (salary range, price range) | Range | `min`/`max`/`step` range |
| Multiple selection (hobbies, symptoms) | Checkbox | `labels` (power-of-2 keys) |
| Single selection, few options (2-5 items) | Radio | `labels` |
| Single selection, many options (6+ items) | Dropdown | `labels` |
| Open-ended text (verbatims, descriptions) | Textarea | optional `placeholder`/`maxLength`; string outcome, invisible to logic |

**Special case — MatrixQuestion cells:**
- 2-3 options per cell: use **Radio** (fits in the grid)
- 4+ options per cell: use **Dropdown** (prevents horizontal overflow)

### 5. Conditional Logic

#### 5.1 Preconditions (When to Show Items)
Control item visibility based on previous responses or variables:

```yaml
- id: q_children_count
  kind: Question
  title: "How many children do you have?"
  precondition:
    - predicate: q_has_children.outcome == 1
  input:
    control: Editbox
    min: 1
    max: 10
```

**Complex Preconditions:**
```yaml
precondition:
  - predicate: q_age.outcome >= 18 and q_marital_status.outcome == 2
  - predicate: employment_status == "employed"  # Using variables
```

**An item that was not asked has an outcome of `None`.** A predicate that reads the
outcome of an item whose own precondition was false sees `None`, not `0`. Equality
comparisons evaluate cleanly (`None == 1` is false, `None != 1` is true); an ordering
comparison (`q_x.outcome >= 18` with `q_x` unasked) and arithmetic (`q_x.outcome + 1`)
raise. A precondition that raises is treated as **unsatisfied**: the item is skipped and
a `degraded` warning is recorded. So the item you gated on a may-be-unasked item is
hidden from every respondent who did not answer the referenced one — not shown to
everyone, and not shown selectively; hidden, silently, for exactly the group you were
trying to reach.

The validator reports this as `none_unsafe_reference` (warning), naming both items.
Fix it by guarding the reference (`q_x.outcome is not None and (q_x.outcome >= 18)` —
parenthesised, because `and` binds tighter than `or`) or by
repeating the referenced item's own gate. The two differ: the guard leaves the owner
reachable wherever it was, while repeating the gate narrows the owner to the referent's
branch. Guard when the owner should stay independently reachable; repeat the gate when
the two belong together — if `q_pregnant` is asked only when
`q_sex.outcome == 2 and q_age.outcome <= 49`, an item gated on `q_pregnant.outcome != 1`
should repeat that gate rather than rely on `None != 1` happening to be true. This is the
same "no inheritance" rule `qml-preconditions` states for sibling items, applied across
gates.

An item that **was** asked and left unanswered is a separate, runtime case: see
`qml-preconditions`.

#### 5.2 Postconditions (Validation After Response)
Ensure data consistency and cross-item validation. A postcondition relates the answer
just given to other answers or to the item's own domain; the respondent is asked to
correct the answer until every predicate holds.

**A postcondition fails the OPPOSITE way from a precondition.** Returning false is what
refuses the answer, so a postcondition the engine cannot evaluate must let the
respondent through — the answer is accepted *unchecked* and the survey is recorded
`critical`, which excludes it from dataset extraction. An unguarded ordering against a
may-be-unasked item therefore costs the whole row, not one item. Write the guard as
`is None`, which reads as "the rule does not apply":

```yaml
postcondition:
  - predicate: q_dx_age.outcome is None or q_age.outcome >= q_dx_age.outcome
    hint: "Your age cannot be less than your age at diagnosis"
```

**A postcondition that admits only one answer is not validation — it is a gate that
ends the interview.** `q_consent.outcome == 1` on a yes/no item means a *No* can never be
submitted: the respondent is stuck, the survey never completes, and the *No* is not in
the data. If the research question wants to count the people who answer *No* (how many
merchants are out of scope, how many applicants decline), a mandated-answer postcondition
makes that count unobservable. Use routing instead — accept the answer, gate what follows
on it with a block-level precondition, and close with a screen-out Comment (see the
Screen-Out Routing pattern in §7.3). Reserve postconditions for **consistency**: relations
between answers (children ≤ household size, sentenced implies convicted) and bounds the
control cannot express.

```yaml
- id: q_income_contributors
  kind: Question
  title: "How many household members contribute to income?"
  postcondition:
    - predicate: q_income_contributors.outcome <= q_household_size.outcome
      hint: "Contributors cannot exceed household size"
    - predicate: q_income_contributors.outcome >= 1
      hint: "At least one person must contribute"
  input:
    control: Editbox
    min: 1
    max: 10
```

### 6. Code Blocks and Variables

#### 6.1 Variable Scope
**IMPORTANT**: All variables in QML are **global**. There is no variable scoping - any variable created or modified in any code block (including codeInit) is accessible and modifiable from any subsequent code block in the questionnaire.

**A variable holds a value only after a codeBlock that assigns it has actually run on the respondent's path.** Variable state follows the items that ran: if the assigning item was skipped by its precondition, sits later in the flow, or assigns on one `if` branch only, a later read raises `NameError`: in a precondition the reading item is skipped as degraded; in a postcondition the answer is accepted unchecked, and in a codeBlock the block stops part-way — both mark the survey critical and exclude it from datasets. When a respondent goes back and changes an answer, variables the new answer no longer produces are gone — not left over. The validator reports such a read as `uninitialized_read` (warning), naming the reader and the variable. Fix it by assigning a default in `codeInit` (`risk = 0`), assigning on both branches, or gating the reader on the same condition as the assignment (`q_b.outcome > 5 and risk == 1`).

```yaml
questionnaire:
  codeInit: |
    # These variables are global throughout the questionnaire
    total_score = 0
    risk_level = "low"
    
blocks:
  - id: b_first
    items:
      - id: q_first
        codeBlock: |
          # Can access and modify global variables
          total_score += 10
          new_var = 5  # This becomes globally accessible
          
  - id: b_second
    items:
      - id: q_second
        precondition:
          # Can reference any global variable in conditions
          - predicate: new_var > 3 and total_score >= 10
```

#### 6.2 Questionnaire Initialization (codeInit)
The `codeInit` section runs before any blocks or items are processed. Use it to:
- Initialize global variables
- Pre-set item outcomes (advanced use)
- Set up initial state for the questionnaire

```yaml
questionnaire:
  codeInit: |
    # Initialize routing/accumulator variables only. Do NOT pre-set an item's
    # outcome here — an outcome is produced by the respondent's answer (or a
    # later codeBlock that derives it), never seeded before the item runs.
    total_score = 0
    category = "standard"
```

#### 6.3 Item-Level Code Blocks
Execute Python code after item responses:
```yaml
- id: q_satisfaction_score
  kind: Question
  title: "Rate your overall satisfaction"
  codeBlock: |
    # All variables are global
    if q_satisfaction_score.outcome >= 8:
        satisfaction_category = "highly_satisfied"
        bonus_points = 10
    elif q_satisfaction_score.outcome >= 5:
        satisfaction_category = "satisfied"
        bonus_points = 5
    else:
        satisfaction_category = "unsatisfied"
        bonus_points = 0
    
    # Modifying global variable
    total_score += q_satisfaction_score.outcome + bonus_points
  input:
    control: Slider
    min: 0
    max: 10
```

#### 6.4 Supported Python Features (Z3-Verifiable Subset)

Code blocks are statically analyzed by the Z3 SMT solver. **Only use features listed here** — anything else either raises an error during validation or silently returns 0, creating unverifiable logic.

**Data Types:**
- **Integers**: All numeric values are treated as integers
- **Booleans**: Converted to integers (1=True, 0=False). Use `0`/`1` in code for clarity.
- **Strings**: Converted to integer hash values internally — usable for variable assignment and equality checks only
- **Lists/Tuples/Sets**: Supported only as **literal containers** in `for` loops and `in`/`not in` membership tests

**Operators:**
- **Arithmetic**: `+`, `-`, `*`, `//` (floor division), `%` (modulo)
- **Comparison**: `<`, `<=`, `>`, `>=`, `==`, `!=` (chained comparisons like `a < b < c` also work)
- **Boolean**: `and`, `or`, `not`
- **Membership**: `in`, `not in` (for list, tuple, set literals)
- **Unary**: `-` (negation), `+`

**Control Flow:**
- **Conditionals**: `if`, `elif`, `else` (nested to arbitrary depth)
- **Loops**: `for` loops with restrictions (loops are **unrolled** statically):
  - `for i in range(n)`: where n must be a constant 0-20
  - `for item in [list]`: literal container must have ≤20 elements
  - `for item in (tuple)`: literal container must have ≤20 elements
  - `for item in {set}`: literal container must have ≤20 elements

**Variable Operations:**
- **Assignment**: `variable = value`
- **Multi-target assignment**: `a = b = value`
- **Augmented Assignment**: `+=`, `-=`, `*=`, `//=`, `%=`
- **Item Outcome Access**: `item_id.outcome` (read)
- **Item Outcome Assignment**: `item_id.outcome = value` (write)

**Built-in Functions (Strict):**
- **`range(n)`**: Creates sequence from 0 to n-1 (n must be ≤20)
- **`int(expr)`**: Explicit cast (bool → int)
- **`bool(expr)`**: Explicit cast (int → bool, where 0=False)
- **In imperative code blocks, prefer explicit arithmetic** — `sum`, `len`, `max`, `min`, `abs`, `sorted`, `append` etc. are not lowered when used to *compute a code-block variable*, so a `total = sum([...])` in a codeBlock is invisible to the solver. **This does NOT apply to matrix postconditions:** the canonical *folded shapes* over matrix cells (`sum([...]) == K`, `len(set([...])) == N`, `all([...])`/`any([...])` over comprehensions with **literal** range bounds) ARE lowered to Z3 and verified — see `matrix-constraint-patterns.md`. Don't avoid them.

#### 6.5 NOT Supported in Code Blocks

The following features either raise validation errors or silently return 0 in the Z3 solver — do not use them.

**Forbidden (validation error):**
```python
import math                    # No imports
def calculate(): pass          # No function definitions
class MyClass: pass            # No class definitions
```

**Always forbidden — genuinely no Z3 model, never use anywhere:**
```python
my_list.append(value)          # No method calls (.append/.upper/.index ...)
lambda x: x*2                  # No lambda functions
data = {}                      # No dictionaries
name.upper()                   # No string operations
```

**Code-block-only restriction — works at runtime but NOT lowered when computing
a code-block variable (use explicit arithmetic instead):**
```python
total = sum(values)            # In a codeBlock: use q1.outcome + q2.outcome + ...
count = len(my_list)           # In a codeBlock: no length model
result = [x*2 for x in range(5)]   # In a codeBlock: unroll by hand
```

**BUT the canonical FOLDED SHAPES over matrix cells ARE verified — in
POSTCONDITIONS (see `matrix-constraint-patterns.md`):**
```python
sum([m.outcome[0][k] for k in range(4)]) == 100     # verified (z3.Sum)
len(set([m.outcome[j][0] for j in range(3)])) == 3  # verified (Distinct, K == N)
all([m.outcome[j][k] >= 1 for j in range(3) for k in range(4)])  # verified (And)
```
Runtime-only (fall back to a `coverage_gap`, not verified): `min`/`max` folds,
non-literal range bounds (`range(j+1, 4)`), partial distinctness
(`len(set(...)) == K` with `K < N`), runtime-bound totals (`== q_target.outcome`),
and any fold over a **QuestionGroup** vector (`qg.outcome[i]` has no per-question
Z3 model — see §9.3).

**Unsupported control flow:**
```python
while condition: pass          # No while loops
for i in range(5): break       # No break/continue
try: pass                      # No exception handling
except: pass
```

**Note:** `print()` is a no-op that returns 0 — harmless but useless.

**Allowed Examples:**
```python
# Simple arithmetic
total = q1.outcome + q2.outcome * 2

# Conditionals
if age >= 18:
    adult = 1
else:
    adult = 0

# Boolean logic
eligible = (age >= 18) and (income > 50000)

# For loops with range
count = 0
for i in range(5):
    count += i

# For loops with containers
scores = [10, 20, 30]
total = 0
for score in scores:
    total += score

# Membership tests
if q_choice.outcome in [1, 2, 3]:
    category = "low"
elif q_choice.outcome in [4, 5]:
    category = "high"

# Deriving a value from multiple outcomes (justified — not a pass-through copy)
age_difference = q_spouse_age.outcome - q_age.outcome

# Setting outcomes programmatically
if skip_section:
    q_optional.outcome = 0
```

#### 6.6 Item Lifecycle and Code Block Execution Order

Each item is processed in this strict order:

1. **Precondition** — evaluated to determine if the item is shown. Can reference other items' outcomes and variables set by prior items' code blocks. Cannot reference the current item's outcome (it hasn't been collected yet).
2. **Collect outcome** — the respondent answers the question (outcome is assigned).
3. **Postcondition** — evaluated after the outcome is collected. Can reference any outcome or variable, though most commonly used to validate the current item's outcome. Variables still hold their **prior** values from earlier items, since the current item's code block has not executed yet.
4. **Code block** — executes after the postcondition passes. Can read the current item's outcome and update global variables for use by subsequent items.

The key consequence: a postcondition referencing a variable that the same item's code block also updates will see the value from **before** this item — the code block's update only takes effect for subsequent items.

Code blocks execute in this global sequence:
1. **codeInit**: Runs once at questionnaire start
2. **Item codeBlocks**: Run after each item's postcondition passes, in topological order

```yaml
questionnaire:
  codeInit: |
    step = 1  # Global variable initialized
    
blocks:
  - id: b_main
    items:
      - id: q1
        codeBlock: |
          step = 2  # Modified globally
          result1 = q1.outcome * 10
          
      - id: q2
        precondition:
          - predicate: step == 2  # Can check the modified value
        codeBlock: |
          step = 3
          result2 = result1 + q2.outcome  # Can access result1
```

**Important Notes:**
- Variables don't need declaration - they're created on first assignment
- All numeric operations use integer arithmetic
- Boolean values are automatically converted to 0/1
- String values have very limited support (mainly for categorization)
- The Z3 constraint solver validates all code paths for consistency

#### 6.7 State Variable Discipline

Every `codeInit` variable narrows what the solver can prove, so the default is to
**reference `q_item.outcome` directly** and create a variable only when you genuinely
cannot. An outcome reference is inside the Z3-verified envelope — the solver knows its
domain from the input control and reasons about every gate on it. A variable is only as
verified as its wiring: if nothing produces it, or nothing reads it, the logic it was
meant to carry silently enforces nothing. **Every unnecessary variable removes logic from
formal verification.**

**A `codeInit` variable is justified by exactly one of four uses:**

1. **Accumulate** across items — a running counter or sum (`risk_score += 20`).
2. **Derive** a value from multiple outcomes (`actual_hours = q_end.outcome - q_break.outcome`).
3. **Classify** an outcome into a routing key (`if q_path.outcome == 1: track = "detailed"`).
4. **Consolidate** mutually exclusive producers into one name (`age` set by either `q_age_dob` or `q_age_manual`, never both).

If a variable does none of these, delete it and reference the outcome directly.

**Producer-and-consumer obligation.** Every `codeInit` variable must have at least one
`codeBlock` that assigns it (a producer) AND at least one precondition, postcondition, or
codeBlock that reads it (a consumer). A variable missing either half is a defect, not a
placeholder:

- No producer → a **frozen variable**: it keeps its `codeInit` constant for the whole run,
  so every gate on it is permanently true or permanently false while looking conditional.
  The usual cause is a planned producer (often in a stubbed or omitted section) that was
  never written.
- No consumer → a **write-only variable**: state computed and thrown away.

**Bare-name ban.** Every identifier in every predicate must resolve to an item id
(`q_x.outcome`) or a variable some `codeBlock` produces — nothing else exists at runtime.
A name with no producer anywhere in the file is a **phantom variable**: the predicate
evaluation namespace is closed (no runtime context is injected), so the predicate fails
open at runtime (treated as true) and is a free symbol to the validator (treated as
satisfiable). The intended logic enforces nothing, statically and at runtime.

**Pass-through aliases are not variables.** A variable whose only assignment copies one
outcome unchanged adds indirection for nothing and shrinks verification coverage:

```yaml
# WRONG — pass-through alias: the copy leaves the verified envelope
codeBlock: |
  smoking_status = q_smoking.outcome
precondition:
  - predicate: smoking_status == 1

# RIGHT — reference the outcome directly (its domain is verified)
precondition:
  - predicate: q_smoking.outcome == 1
```

**The validator enforces this discipline.** Undefined names are **errors** (the file fails
validation); a frozen gate classifies as dead code (an unreachable-item error); write-only
variables and pass-through aliases draw **warnings**. Treat every such finding as a
fix-item, not noise.

### 7. Best Practices and Design Patterns

#### 7.1 Creating Questionnaires from Requirements and Regulations

When transforming compliance rules, regulations, or requirements documents into QML questionnaires, follow this simplified approach:

**Focus on Three Core Elements:**
1. **Range**: Define the valid numeric range for each answer
2. **Preconditions**: Specify when a question should be asked
3. **Postconditions**: Define validation rules that must be satisfied

**Key Principle**: You do NOT need to manually construct complex dependency graphs between items. The built-in Z3 validator automatically handles logical coherence and path validation. Your role is to:
- Translate requirements into questions with integer outcomes
- Set appropriate ranges for responses
- Add preconditions for conditional requirements
- Add postconditions for compliance validation

**Example: Transforming a Regulation into QML**

Given regulation: "Companies with more than 50 employees must have a safety officer. The safety officer must have at least 3 years of experience if the company operates in manufacturing."

```yaml
- id: q_employee_count
  kind: Question
  title: "How many employees does your company have?"
  input:
    control: Editbox
    min: 1
    max: 10000
    
- id: q_has_safety_officer
  kind: Question
  title: "Does your company have a designated safety officer?"
  precondition:
    - predicate: q_employee_count.outcome > 50
  input:
    control: Switch
    on: "Yes"
    off: "No"

# The regulation says a >50-employee company MUST have one. That is a finding to
# record, not an answer to refuse: a postcondition `== 1` here would stop every
# non-compliant company at this item and leave no row behind. Ask, then route.
- id: q_no_officer_notice
  kind: Comment
  title: "Companies with more than 50 employees are required to designate a safety officer. Your answers will be recorded as non-compliant on this point."
  precondition:
    - predicate: q_employee_count.outcome > 50 and q_has_safety_officer.outcome == 0
    
- id: q_industry_type
  kind: Question
  title: "What is your primary industry?"
  input:
    control: Radio
    labels:
      1: "Manufacturing"
      2: "Services"
      3: "Retail"
      4: "Technology"
      5: "Other"
      
- id: q_safety_officer_experience
  kind: Question
  title: "Years of experience of your safety officer:"
  precondition:
    - predicate: q_has_safety_officer.outcome == 1
  postcondition:
    - predicate: q_industry_type.outcome != 1 or q_safety_officer_experience.outcome >= 3
      hint: "Manufacturing companies require safety officers with 3+ years experience"
  input:
    control: Editbox
    min: 0
    max: 50
```

`q_safety_officer_experience` above is a genuine postcondition: it relates the officer's
experience to the industry, and a respondent can always satisfy it by correcting a
mistyped number. The safety-officer requirement is not — no correction exists for "we do
not have one" — so it is recorded through routing and counted at analysis.

**What the Validator Handles Automatically:**
- Path exploration and reachability analysis
- Constraint satisfaction checking
- Logical consistency verification
- Dead-end detection
- Circular dependency resolution

**What You Should Focus On:**
- Clear question formulation
- Appropriate value definitions (ranges for Editbox/Slider/Range, labels for Radio/Dropdown/Checkbox)
- Simple, direct preconditions
- Validation rules as postconditions
- Integer-based outcomes for all responses

#### 7.2 Block Organization
```yaml
blocks:
  # Screening/Qualification Block
  - id: b_screening
    title: "Eligibility Check"
    items:
      # Questions to determine eligibility
      
  # Main Content Blocks
  - id: b_demographics
    title: "About You"
    items:
      # Core demographic questions
      
  - id: b_experience
    title: "Your Experience"
    items:
      # Main survey questions
      
  # Closing Block
  - id: b_closing
    title: "Final Questions"
    items:
      # Wrap-up questions and comments
```

#### 7.3 Progressive Disclosure Pattern
Show questions progressively based on previous answers:
```yaml
- id: q_has_car
  kind: Question
  title: "Do you own a car?"
  input:
    control: Switch
    
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

#### 7.3b Screen-Out Routing Pattern
A screener decides who continues. Gate the substantive blocks on the screener with
block-level preconditions, and give the screened-out respondent a closing Comment so the
interview ends legibly. The screened-out answer is stored — which is what makes
eligibility rates, mis-scope counts and refusal rates measurable at all.

```yaml
- id: b_screening
  items:
    - id: q_age_ok
      kind: Question
      title: "Are you 18 or older?"
      input:
        control: Switch
        on: "Yes"
        off: "No"
    - id: q_screened_out
      kind: Comment
      title: "Thank you — this survey is for adults only, and your answers end here."
      precondition:
        - predicate: q_age_ok.outcome == 0

- id: b_main
  precondition:
    - predicate: q_age_ok.outcome == 1
  items:
    - id: q_first_substantive
      kind: Question
      title: "..."
      input:
        control: Radio
        labels:
          1: "..."
          2: "..."
```

Do not write `postcondition: q_age_ok.outcome == 1` on the screener: it refuses the *No*
instead of routing it, and the respondent cannot leave the item.

#### 7.4 Data Quality Patterns
Ensure response quality with validation:
```yaml
- id: q_age
  kind: Question
  title: "Enter your age"
  input:
    control: Editbox
    min: 18
    max: 120
    
- id: q_years_experience
  kind: Question  
  title: "Years of work experience"
  postcondition:
    - predicate: q_years_experience.outcome <= (q_age.outcome - 16)
      hint: "Work experience cannot exceed your working age"
  input:
    control: Editbox
    min: 0
    max: 60
```

#### 7.5 Scoring and Categorization Pattern
Use integer variables for accumulating scores. The Z3 solver can reason about integer arithmetic and conditionals, enabling full verification of scoring logic.
```yaml
questionnaire:
  codeInit: |
    risk_score = 0

blocks:
  - id: b_risk_assessment
    items:
      - id: q_smoking
        kind: Question
        title: "Do you smoke?"
        codeBlock: |
          if q_smoking.outcome == 1:
              risk_score += 20
        input:
          control: Switch

      - id: q_exercise_frequency
        kind: Question
        title: "Weekly exercise frequency"
        codeBlock: |
          if q_exercise_frequency.outcome < 3:
              risk_score += 10
        input:
          control: Editbox
          min: 0
          max: 7

      - id: q_risk_result
        kind: Comment
        title: "Risk Assessment Complete"
        precondition:
          - predicate: risk_score > 0
        codeBlock: |
          if risk_score >= 30:
              risk_category = "high"
          elif risk_score >= 15:
              risk_category = "medium"
          else:
              risk_category = "low"
```

**Do NOT use `list.append()` or other method calls** — they execute at runtime but are invisible to the Z3 solver, creating unverifiable dead spots in your questionnaire logic.

### 8. Common Pitfalls to Avoid

#### Prefer Block-Level Gates over Scattered Cross-Block Item Gates
A later block depending on an earlier answer is normal — every optional module in a
large instrument does it. What makes a file hard to maintain is many *item-level* gates
in one block each reaching back to different earlier blocks. Prefer one of two shapes:

```yaml
# GOOD: the dependency is one block-level gate, read in one place
blocks:
  - id: b_financial
    items:
      - id: q_income
  - id: b_loan
    precondition:
      - predicate: q_income.outcome > 50000
    items:
      - id: q_loan_amount
      - id: q_loan_term

# ALSO GOOD: an item that depends on a sibling stays in the sibling's block
blocks:
  - id: b_financial
    items:
      - id: q_income
      - id: q_loan_eligible
        precondition:
          - predicate: q_income.outcome > 50000
```

```yaml
# AVOID: item-level gates scattered across blocks, each reaching back differently
blocks:
  - id: b_financial
    items:
      - id: q_income
  - id: b_misc
    items:
      - id: q_loan_eligible
        precondition:
          - predicate: q_income.outcome > 50000
      - id: q_unrelated
      - id: q_other_gated
        precondition:
          - predicate: q_income.outcome > 20000
```

#### Avoid Missing Value Definitions
```yaml
# BAD: Editbox without min/max
input:
  control: Editbox
  # Missing min and max!

# BAD: Radio without labels
input:
  control: Radio
  # Missing labels!
```

#### Always Define Valid Values
```yaml
# GOOD: Editbox with range
input:
  control: Editbox
  min: 0
  max: 100

# GOOD: Radio with labels
input:
  control: Radio
  labels:
    1: "Option A"
    2: "Option B"
    3: "Option C"
```

#### Avoid Unclear Postcondition Messages
```yaml
# BAD: Generic error message
postcondition:
  - predicate: value > 0
    hint: "Invalid input"
```

#### Provide Helpful Validation Messages
```yaml
# GOOD: Specific guidance
postcondition:
  - predicate: q_children.outcome <= q_household_size.outcome
    hint: "Number of children cannot exceed total household size"
```

### 9. Advanced Techniques

#### 9.1 Dynamic Question Text with Variables
While QML doesn't support dynamic text interpolation directly, you can use Comments with preconditions:
```yaml
- id: q_high_income_msg
  kind: Comment
  title: "As a high-income earner, you may qualify for premium services"
  precondition:
    - predicate: income_category == "high"
```

#### 9.2 Complex Branching Logic
```yaml
- id: q_initial_path
  kind: Question
  title: "Choose your survey path"
  codeBlock: |
    if q_initial_path.outcome == 1:
        survey_path = "detailed"
        questions_to_show = 20
    else:
        survey_path = "quick"
        questions_to_show = 5
  input:
    control: Radio
    labels:
      1: "Detailed Survey (20 questions)"
      2: "Quick Survey (5 questions)"

# Show different questions based on path
- id: q_detailed_1
  kind: Question
  precondition:
    - predicate: survey_path == "detailed"
  # ...
```

#### 9.3 Aggregating QuestionGroup Responses
A **QuestionGroup** carries a single scalar Z3 var — its per-question outcomes
(`q_service_ratings.outcome[i]`) have **no per-question model** in the solver, so
any aggregation over them (whether `sum([...])` or explicit `outcome[0] +
outcome[1] + ...`) is **runtime-only**, not statically verified. Compute the
total explicitly and rely on runtime enforcement:
```yaml
- id: q_service_ratings
  kind: QuestionGroup
  title: "Rate our services"
  questions:
    - "Speed"
    - "Quality"
    - "Support"
  codeBlock: |
    # Runtime-only: the per-question outcomes are not modelled in Z3, so the
    # solver treats total_rating as unconstrained (a coverage gap, not a proof).
    total_rating = q_service_ratings.outcome[0] + q_service_ratings.outcome[1] + q_service_ratings.outcome[2]

    # Categorize based on total (3 questions, scale 1-5, so range 3-15)
    if total_rating >= 12:
        service_satisfaction = "excellent"
    elif total_rating >= 9:
        service_satisfaction = "good"
    else:
        service_satisfaction = "needs_improvement"
  input:
    control: Radio
    labels:
      1: "Poor"
      2: "Fair"
      3: "Good"
      4: "Very Good"
      5: "Excellent"
```

**QuestionGroup vs Matrix.** This runtime-only limitation is specific to
QuestionGroup vector outcomes. A **`MatrixQuestion`** DOES model each cell
(`m.outcome[j][k]`), so the canonical folded shapes over its cells — `sum([...])
== K`, `len(set([...])) == N`, `all([...])` with literal range bounds — **are
Z3-verified** (see `matrix-constraint-patterns.md`). If you need a statically
verified aggregate, model the items as a matrix, not a QuestionGroup.

### 10. Testing and Validation Guidelines

When creating QML questionnaires, ensure:

1. **All paths are reachable**: Test that every question can be reached through at least one valid response path
2. **Postconditions are satisfiable**: Verify that validation rules don't create impossible situations
3. **Variables are initialized**: Ensure all variables used in conditions are defined in codeInit or prior code blocks
4. **Value definitions are correct**: Check that min/max make sense for range controls, and label keys are valid integers for selection controls
5. **Variable producers before consumers**: Items that set a variable (via response or codeBlock) must appear before items whose preconditions or postconditions reference that variable. Blocks are displayed in their defined order, but items within a block are ordered by dependency topology — items at the same dependency level have no guaranteed order, so every conditional item must carry its own complete precondition (no inheritance)
6. **Labels are complete**: All referenced label keys must be defined in the labels map

### Example: Complete Demographic Questionnaire

```yaml
qmlVersion: "2.0"
questionnaire:
  title: "Customer Demographics and Preferences"
  codeInit: |
    # Classification key: produced in b_employment (q_income) and read by the
    # closing premium-offer message. Every codeInit variable must be both
    # produced by a codeBlock and read by a consumer (see §6.7).
    customer_segment = "standard"
    
  blocks:
    - id: b_basic_info
      title: "Basic Information"
      items:
        - id: q_welcome
          kind: Comment
          title: "Welcome! This survey will take approximately 5 minutes."
          
        - id: q_age
          kind: Question
          title: "What is your age?"
          input:
            control: Editbox
            min: 18
            max: 120
            left: "I am"
            right: "years old"
            
        - id: q_gender
          kind: Question
          title: "What is your gender?"
          input:
            control: Radio
            labels:
              1: "Male"
              2: "Female"
              3: "Non-binary"
              4: "Prefer not to say"
              
    - id: b_household
      title: "Household Information"
      items:
        - id: q_marital_status
          kind: Question
          title: "What is your marital status?"
          input:
            control: Radio
            labels:
              1: "Single"
              2: "Married/Partnership"
              3: "Divorced"
              4: "Widowed"
              
        - id: q_household_size
          kind: Question
          title: "Including yourself, how many people live in your household?"
          input:
            control: Editbox
            min: 1
            max: 15
            
        - id: q_children
          kind: Question
          title: "How many children under 18 live in your household?"
          precondition:
            - predicate: q_household_size.outcome > 1
          postcondition:
            - predicate: q_children.outcome < q_household_size.outcome
              hint: "Number of children must be less than household size"
          input:
            control: Editbox
            min: 0
            max: 10
            
    - id: b_employment
      title: "Employment and Income"
      items:
        - id: q_employment_status
          kind: Question
          title: "What is your employment status?"
          input:
            control: Dropdown
            labels:
              1: "Employed full-time"
              2: "Employed part-time"
              3: "Self-employed"
              4: "Unemployed"
              5: "Retired"
              6: "Student"
              
        - id: q_income
          kind: Question
          title: "What is your annual household income?"
          codeBlock: |
            # Classify the income bracket into a routing key (justification: classify).
            # q_income.outcome is the label key (1-6), not a dollar amount.
            if q_income.outcome >= 5:
                customer_segment = "premium"
            elif q_income.outcome >= 3:
                customer_segment = "standard_plus"
          input:
            control: Dropdown
            labels:
              1: "Under $25,000"
              2: "$25,000 - $49,999"
              3: "$50,000 - $74,999"
              4: "$75,000 - $99,999"
              5: "$100,000 - $149,999"
              6: "$150,000 or more"

        - id: q_premium_offer
          kind: Comment
          title: "As a premium customer, you qualify for our exclusive offers."
          precondition:
            # Consumer: customer_segment is produced in q_income and read here.
            - predicate: customer_segment == "premium"

        - id: q_thank_you
          kind: Comment
          title: "Thank you for completing the survey!"
```

## Summary

When creating QML questionnaires, think declaratively:
1. **Declare constraints, not flow** - Preconditions and postconditions define the logic; the Z3 solver verifies consistency
2. **Always define valid values** - `min`/`max` for range-based controls, `labels` for selection controls
3. **Use preconditions** - Define when a question applies, not how to navigate to it
4. **Use postconditions for consistency, routing for eligibility** - A postcondition relates answers; one that admits a single answer ends the interview and hides the answer you wanted to count
5. **Choose the right control** - Match the UI to the data type (see Section 4.9)
6. **Keep code blocks Z3-verifiable** - Only use the supported Python subset (no `sum`, `len`, `append`, etc.)
7. **Gate sections at the block** - A later block that depends on an earlier answer carries one block-level precondition; item-level gates stay beside the item they depend on
8. **Provide helpful hints** - Make postcondition messages user-friendly
