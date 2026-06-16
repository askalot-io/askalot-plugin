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
qmlVersion: "1.1"
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

### 2b. Block Kinds

Every block declares a mandatory `kind`. Three kinds are supported:

| Kind | Description |
|------|-------------|
| `Sequence` | Default. Visit inner items once in declared (topological) order. |
| `Roster` | Repeat inner items per set bit in an `iterateOver` integer bitmask. Required: `iterateOver` (Python expression → non-negative int bitmask) and `labels` (map of power-of-2 keys to display strings). |
| `Sample` | Ask up to N inner items from the eligible pool. Required: `count` (positive integer literal — loader rejects missing/non-positive values loudly, no silent default). Optional: `is_random` (bool, default false). |

**Static validation (Z3) is kind-aware:**
- Roster unrolls per label-key into bit-guarded copies.
- Sample treats inner items as conditionally-present with up-to-N draw; when `is_random=true`, enumerates orderings with a cap of 7 independent dependency components.

#### Roster example

```yaml
qmlVersion: "1.1"
questionnaire:
  title: "Meal Tracker"
  blocks:
    - id: meal_selection
      kind: Sequence
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

#### Sample example

```yaml
qmlVersion: "1.1"
questionnaire:
  title: "Knowledge Check"
  blocks:
    - id: question_pool
      kind: Sample
      count: 3
      is_random: true
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

With `count: 3` and `is_random: true`, 3 of the 4 items are asked per execution in a randomised-but-frozen order. Items skipped by preconditions don't consume a slot. Documents using Sample blocks require `qmlVersion: "1.1"`.

**7-component cap**: `is_random: true` blocks with more than 7 independent dependency components are rejected at validation time. To recover: split the block into sub-blocks with fewer independent components, or set `is_random: false`.

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

#### 4.1 Switch (Binary Choice)
```yaml
input:
  control: Switch
  on: "Yes"
  off: "No"
  default: 0  # Optional: 0 for off, 1 for on
```

#### 4.2 Radio (Single Selection)
```yaml
input:
  control: Radio
  labels:
    1: "Option 1"
    2: "Option 2"
    3: "Option 3"
  default: 1  # Optional: must be a key from labels
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
  default: 0  # Optional: bit mask of selected options
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
  default: 25  # Optional: must be between min and max
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

#### 4.8 Choosing the Right Control

| Use Case | Control | Value Definition |
|---|---|---|
| Yes/No binary choice | Switch | `on`/`off` labels |
| Precise number (age, children count) | Editbox | `min`/`max` range |
| Approximate/subjective scale (satisfaction, mood) | Slider | `min`/`max`/`step` range |
| Numeric interval (salary range, price range) | Range | `min`/`max`/`step` range |
| Multiple selection (hobbies, symptoms) | Checkbox | `labels` (power-of-2 keys) |
| Single selection, few options (2-5 items) | Radio | `labels` |
| Single selection, many options (6+ items) | Dropdown | `labels` |

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

#### 5.2 Postconditions (Validation After Response)
Ensure data consistency and cross-item validation:

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
    # Initialize variables
    total_score = 0
    category = "standard"

    # Pre-initialize outcomes (advanced)
    q_default_age.outcome = 25  # Pre-fill an item's outcome
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
- **No other built-in functions** — `len`, `sum`, `max`, `min`, `abs`, `sorted`, `append`, etc. all return 0 in the solver

#### 6.5 NOT Supported in Code Blocks

The following features either raise validation errors or silently return 0 in the Z3 solver — do not use them.

**Forbidden (validation error):**
```python
import math                    # No imports
def calculate(): pass          # No function definitions
class MyClass: pass            # No class definitions
```

**Invisible to solver (silently returns 0 — never use):**
```python
my_list.append(value)          # No method calls
len(my_list)                   # No built-in functions (except range, int, bool)
sum(values)                    # Returns 0 in solver
max(a, b)                      # Returns 0 in solver
[x*2 for x in range(5)]       # No list comprehensions
lambda x: x*2                  # No lambda functions
data = {}                      # No dictionaries
name.upper()                   # No string operations
arr[0]                         # No subscript access (use item.outcome directly)
```

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

# Variable assignment from outcomes
previous_answer = q_age.outcome
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
  postcondition:
    - predicate: q_has_safety_officer.outcome == 1
      hint: "Companies with >50 employees must have a safety officer"
  input:
    control: Switch
    on: "Yes"
    off: "No"
    
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

#### Avoid Cross-Block Dependencies
```yaml
# BAD: Item in block2 depends on item in block1
blocks:
  - id: block1
    items:
      - id: q_income
  - id: block2
    items:
      - id: q_loan_eligible
        precondition:
          - predicate: q_income.outcome > 50000  # Cross-block dependency
```

#### Better: Keep Related Items Together
```yaml
# GOOD: Related items in same block
blocks:
  - id: b_financial
    items:
      - id: q_income
      - id: q_loan_eligible
        precondition:
          - predicate: q_income.outcome > 50000
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
Since `sum()` and `len()` are not available in the Z3-verifiable subset, compute totals manually using explicit addition:
```yaml
- id: q_service_ratings
  kind: QuestionGroup
  title: "Rate our services"
  questions:
    - "Speed"
    - "Quality"
    - "Support"
  codeBlock: |
    # Sum ratings explicitly (Z3 can verify this)
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

**Why not `sum()` / `len()`?** These built-in functions are not part of the Z3-verifiable subset. They execute at runtime but return `0` in static analysis, making any logic that depends on them invisible to the solver.

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
qmlVersion: "1.0"
questionnaire:
  title: "Customer Demographics and Preferences"
  codeInit: |
    # Initialize tracking variables
    total_household_income = 0
    customer_segment = "standard"
    eligible_for_offers = 0
    
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
            total_household_income = q_income.outcome
            if q_income.outcome >= 100000:
                customer_segment = "premium"
                eligible_for_offers = 1
            elif q_income.outcome >= 50000:
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
              
        - id: q_thank_you
          kind: Comment
          title: "Thank you for completing the survey!"
```

## Summary

When creating QML questionnaires, think declaratively:
1. **Declare constraints, not flow** - Preconditions and postconditions define the logic; the Z3 solver verifies consistency
2. **Always define valid values** - `min`/`max` for range-based controls, `labels` for selection controls
3. **Use preconditions** - Define when a question applies, not how to navigate to it
4. **Use postconditions** - Define what must be true, not how to enforce it
5. **Choose the right control** - Match the UI to the data type (see Section 4.8)
6. **Keep code blocks Z3-verifiable** - Only use the supported Python subset (no `sum`, `len`, `append`, etc.)
7. **Minimize cross-block dependencies** - Keep related items in the same block
8. **Provide helpful hints** - Make postcondition messages user-friendly
