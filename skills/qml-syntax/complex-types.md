# QML Complex Type Examples

Examples of QuestionGroup and MatrixQuestion with preconditions on
vector/matrix elements and postconditions over them. Each block list below was
loaded through the validator; the comments say which conditions Z3 verifies and
which are enforced at runtime only.

## Example 1: Employee Satisfaction (QuestionGroup + constraints)

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

# Conditional follow-ups when any aspect rated below 5. Both share one gate, so
# they form their own block carrying it once. The gate reads the answers in the
# condition itself: a codeBlock that counted the low ratings into a variable
# would not be verified (a codeBlock read of QuestionGroup answers is
# runtime-only), and presentation (which areas, phrased as prose) is the UI's
# job, not a code block.
- id: satisfaction_followup
  precondition:
    - predicate: any([job_aspects.outcome[j] < 5 for j in range(5)])
  items:
    - id: followup_needed
      kind: Comment
      title: "Additional feedback needed"

    # Allocate 100 points with sum constraint
    - id: improvement_allocation
      kind: QuestionGroup
      title: "Allocate 100 points across areas for improvement"
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
        # Read each answer by index: sum(improvement_allocation.outcome) over the
        # whole list is runtime-only. Non-negativity is already min: 0.
        - predicate: sum([improvement_allocation.outcome[j] for j in range(5)]) == 100
          hint: "Points must sum to exactly 100"
```

**Patterns shown:** QuestionGroup with Slider, a block-level precondition on vector
elements (`outcome[j] < 5`) gating the follow-ups once, postcondition with a sum
constraint (allocation pattern). Both conditions are lowered to Z3 and reported as
`inexact_condition`, because an unanswered slot makes the comparison or the sum
raise; see "Unanswered cells" in `matrix-constraint-patterns.md`.

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
        # Pairwise != is verified; len(set(attribute_ranking.outcome)) == 3 says
        # the same and is runtime-only.
        - predicate: |
            (attribute_ranking.outcome[0] != attribute_ranking.outcome[1]
             and attribute_ranking.outcome[0] != attribute_ranking.outcome[2]
             and attribute_ranking.outcome[1] != attribute_ranking.outcome[2])
          hint: "Each attribute must have a unique rank"

    # Scalar gated by matrix cell value via dynamic index
    - id: weakest_rating
      kind: Question
      title: "Rate improvement priority for the weakest attribute"
      precondition:
        # Dynamic index (best_product.outcome-1) is a runtime value, so this
        # min-fold is runtime-enforced only (`skipped_condition`), not Z3-verified.
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
