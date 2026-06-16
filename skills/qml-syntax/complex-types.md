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
        aspect_names = ["Work-life", "Compensation", "Career", "Management", "Environment"]
        problem_areas = [aspect_names[i] for i in range(5)
                       if job_aspects.outcome[i] < 5]

    # Conditional follow-up when any aspect rated below 5
    - id: followup_needed
      kind: Comment
      title: "Additional feedback needed"
      precondition:
        - predicate: any([job_aspects.outcome[j] < 5 for j in range(5)])
      codeBlock: |
        count = len(problem_areas)
        message = f"We identified {count} areas needing improvement:\n"
        for area in problem_areas:
          message += f"- {area}\n"
        print(message)

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
      codeBlock: |
        best_per_attribute = []
        for col in range(6):
          scores = [product_comparison.outcome[row][col] for row in range(4)]
          best_idx = scores.index(max(scores))
          best_per_attribute.append(best_idx)

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

    # Summary using codeBlock with derived data
    - id: best_summary
      kind: Comment
      title: "Analysis complete"
      codeBlock: |
        products = ["SmartPhone X", "SmartPhone Y", "SmartPhone Z", "SmartPhone W"]
        attributes = ["Battery", "Screen", "Camera", "Performance", "Build", "Value"]
        summary = "Best products by attribute:\n"
        for i in range(6):
          best_prod = products[best_per_attribute[i]]
          score = product_comparison.outcome[best_per_attribute[i]][i]
          summary += f"- {attributes[i]}: {best_prod} (score: {score})\n"
        print(summary)
```

**Patterns shown:** MatrixQuestion with rows/columns, precondition on matrix
aggregation (`all(... for k) for j`), codeBlock iterating over matrix cells,
derived state passed between items.

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
        - predicate: |
            min([product_ratings.outcome[best_product.outcome-1][j]
                 for j in range(3)]) < 4
      codeBlock: |
        prod_idx = best_product.outcome - 1
        scores = [product_ratings.outcome[prod_idx][j] for j in range(3)]
        weakest_idx = scores.index(min(scores))
        attr_names = ["Price", "Quality", "Service"]
        print(f"The weakest attribute is: {attr_names[weakest_idx]} (score: {scores[weakest_idx]})")
      input:
        control: Slider
        min: 1
        max: 10
```

**Patterns shown:** MatrixQuestion + QuestionGroup + Question combined,
precondition using matrix row sums, postcondition enforcing permutation
(unique ranks), precondition with dynamic index (`outcome[best_product.outcome-1][j]`),
multi-level dependencies (I2 depends on I1, I3 on I2, I4 on I1+I2).
