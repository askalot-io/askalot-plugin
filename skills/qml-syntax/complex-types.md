# QML Complex Type Examples

Realistic examples demonstrating QuestionGroup and MatrixQuestion with
preconditions on vector/matrix elements, postconditions with constraints,
and codeBlock for dynamic logic.

## Example 1: Employee Satisfaction (QuestionGroup + codeBlock + constraints)

```yaml
- id: satisfaction_assessment
  items:
    # Vector[5] rating — each element in [1,10]
    - id: job_aspects
      kind: QuestionGroup
      title: "Rate your satisfaction with each aspect"
      questions:
        - "Work-life balance"
        - "Compensation and benefits"
        - "Career development"
        - "Management support"
        - "Work environment"
      input:
        control: Slider
        min: 1
        max: 10
      codeBlock: |
        # Supported subset only: int() casts + explicit addition. A code block
        # CANNOT build lists of strings, use len()/comprehensions, or format
        # messages (f-strings / print) — those are invisible to the sandbox.
        # Count how many aspects were rated below 5, for downstream routing.
        problem_count = (int(job_aspects.outcome[0] < 5) + int(job_aspects.outcome[1] < 5)
                         + int(job_aspects.outcome[2] < 5) + int(job_aspects.outcome[3] < 5)
                         + int(job_aspects.outcome[4] < 5))

    # Conditional follow-up when any aspect rated below 5. Presentation (which
    # areas, phrased as prose) is the UI's job, not a code block — the item is
    # simply gated on the precondition.
    - id: followup_needed
      kind: Comment
      title: "Additional feedback needed"
      precondition:
        - predicate: any([job_aspects.outcome[j] < 5 for j in range(5)])

    # Allocate 100 points with sum constraint
    - id: improvement_allocation
      kind: QuestionGroup
      title: "Allocate 100 points across areas for improvement"
      precondition:
        - predicate: any([job_aspects.outcome[j] < 5 for j in range(5)])
      questions:
        - "Points for Work-life balance"
        - "Points for Compensation"
        - "Points for Career development"
        - "Points for Management"
        - "Points for Work environment"
      input:
        control: Editbox
        min: 0
        max: 100
      postcondition:
        - predicate: sum(improvement_allocation.outcome) == 100
          hint: "Points must sum to exactly 100"
        - predicate: all([improvement_allocation.outcome[j] >= 0 for j in range(5)])
          hint: "All values must be non-negative"
```

**Patterns shown:** QuestionGroup with Slider, precondition on vector elements
(`outcome[j] < 5`), codeBlock tracking state across items, postcondition with
sum constraint, allocation pattern.

## Example 2: Product Comparison (MatrixQuestion + derived calculations)

```yaml
- id: comparison
  items:
    # Matrix[4][6] — 4 products x 6 attributes, each in [0,100]
    - id: product_comparison
      kind: MatrixQuestion
      title: "Rate each product on these attributes (0-100)"
      rows:
        - "SmartPhone X"
        - "SmartPhone Y"
        - "SmartPhone Z"
        - "SmartPhone W"
      columns:
        - "Battery life"
        - "Screen quality"
        - "Camera"
        - "Performance"
        - "Build quality"
        - "Value for money"
      input:
        control: Editbox
        min: 0
        max: 100

    # Precondition on matrix aggregation
    - id: perfect_product
      kind: Question
      title: "You rated a product perfectly! Tell us why."
      precondition:
        - predicate: |
            any([all([product_comparison.outcome[j][k] == 100
                 for k in range(6)]) for j in range(4)])
      input:
        control: Radio
        labels:
          1: "It meets all my needs"
          2: "Best in its category"
          3: "Exceptional value"
          4: "Other reason"

    # A closing Comment. Note there is NO codeBlock building a summary string:
    # argmax (scores.index(max(scores))), list building, and f-string / print
    # formatting are all outside the supported subset — presentation belongs to
    # the UI, not a code block.
    - id: best_summary
      kind: Comment
      title: "Analysis complete"
```

**Patterns shown:** MatrixQuestion with rows/columns, precondition on matrix
aggregation (`all(... for k) for j` — a verified fold over matrix cells).
Presentation logic (which product won each attribute) is intentionally NOT a
code block — it is outside the supported subset.

## Example 3: Combined Types with Inter-Item Dependencies

```yaml
- id: product_evaluation
  items:
    # Matrix[4][3] ratings
    - id: product_ratings
      kind: MatrixQuestion
      title: "Rate each product on these attributes"
      rows:
        - "Product A"
        - "Product B"
        - "Product C"
        - "Product D"
      columns:
        - "Price"
        - "Quality"
        - "Service"
      input:
        control: Radio
        labels:
          1: "Poor"
          2: "Below Average"
          3: "Average"
          4: "Good"
          5: "Excellent"

    # Scalar selection based on matrix row sums
    - id: best_product
      kind: Question
      title: "Which product has the best overall score?"
      precondition:
        - predicate: |
            any([sum([product_ratings.outcome[i][j]
                  for j in range(3)]) >= 6
                  for i in range(4)])
      input:
        control: Radio
        labels:
          1: "Product A"
          2: "Product B"
          3: "Product C"
          4: "Product D"

    # Vector[3] ranking with uniqueness constraint
    - id: attribute_ranking
      kind: QuestionGroup
      title: "Rank these attributes by importance"
      precondition:
        - predicate: best_product.outcome == 1 or best_product.outcome == 2
      questions:
        - "Price"
        - "Quality"
        - "Service"
      input:
        control: Dropdown
        labels:
          1: "Most important"
          2: "Second most important"
          3: "Least important"
      postcondition:
        - predicate: len(set(attribute_ranking.outcome)) == 3
          hint: "Each attribute must have a unique rank"

    # Scalar gated by matrix cell value via dynamic index
    - id: weakest_rating
      kind: Question
      title: "Rate improvement priority for the weakest attribute"
      precondition:
        # Dynamic index (best_product.outcome-1) is a runtime value, so this
        # min-fold is runtime-enforced only (a coverage_gap), not Z3-verified.
        - predicate: |
            min([product_ratings.outcome[best_product.outcome-1][j]
                 for j in range(3)]) < 4
      input:
        control: Slider
        min: 1
        max: 10
```

Note there is no codeBlock finding the weakest attribute for display: argmin
(`scores.index(min(scores))`), string lists, and f-string / print formatting are
outside the supported subset. Presentation is the UI's job.

**Patterns shown:** MatrixQuestion + QuestionGroup + Question combined,
precondition using matrix row sums, postcondition enforcing permutation
(unique ranks), precondition with dynamic index (`outcome[best_product.outcome-1][j]`,
runtime-only), multi-level dependencies (I2 depends on I1, I3 on I2, I4 on I1+I2).
