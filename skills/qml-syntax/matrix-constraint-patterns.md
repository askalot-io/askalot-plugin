# Matrix Constraint Patterns

Three formal postcondition patterns for `MatrixQuestion` items, formalized in
the thesis "Formal Verification of Questionnaires" (Common Constraint Patterns,
Section "Extension to Complex Item Types"). Use these whenever a matrix item
must enforce structural integrity beyond simple cell-level domain bounds.

For a matrix item `I_i` with outcome `S_i ∈ ℤ^{m × n}`, cell `S_{i,j,k}` is
the value at row `j`, column `k`.

---

## Pattern 1 — Matrix Symmetry

**Use when:** correlation, similarity, or relationship matrices where the
value at (row j, column k) must equal the value at (row k, column j).
Characteristic of square matrices (m = n).

**Formal definition (thesis):**
```
Q_i := ⋀_{j=1..m} ⋀_{k=j+1..n} (S_{i,j,k} = S_{i,k,j})
```

**QML example — pairwise factor relationship strength:**

```yaml
- id: factor_relationships
  kind: MatrixQuestion
  title: "Rate the relationship strength between each pair of factors (0-10)"
  rows:
    - "Price"
    - "Quality"
    - "Brand"
    - "Service"
  columns:
    - "Price"
    - "Quality"
    - "Brand"
    - "Service"
  input:
    control: Slider
    min: 0
    max: 10
  postcondition:
    # Symmetry: cell (j,k) must equal cell (k,j) for all j < k
    - predicate: |
        all([factor_relationships.outcome[j][k] == factor_relationships.outcome[k][j]
             for j in range(4) for k in range(4) if k > j])
      hint: "The relationship between A and B must equal the relationship between B and A"
    # Optional: diagonal must be the maximum (self-relationship is total)
    - predicate: |
        all([factor_relationships.outcome[j][j] == 10 for j in range(4)])
      hint: "Each factor's relationship with itself is maximal (10)"
```

**Why it matters:** Without the symmetry postcondition, respondents can produce
contradictory matrices (e.g., Price↔Quality = 7 but Quality↔Price = 3) that
break downstream factor analysis or correlation computations.

**Validation coverage:** Runtime-enforced (FlowProcessor) + Static-validated
(ItemClassifier ≥ 1.14.0) — covers this pattern's exact form. Variants with
non-literal range bounds (e.g. `range(j+1, 4)`), `zip` / `enumerate`,
multi-range BinOp starts, or `min` / `max` folds fall back to runtime
enforcement only; `validate_qml_file` surfaces the gap via `coverage_gaps`.
Prefer the `if k > j` filter form shown above when authoring triangular
constraints — `range(j+1, 4)` runs at runtime but is invisible to Z3.

---

## Pattern 2 — Fixed-Sum Allocation

**Use when:** respondents distribute a fixed total (points, percentages,
budget) across cells. Applies to a single row, a single column, or every row
independently.

**Formal definition (thesis, vector form generalized to matrix rows):**
```
Q_i := ⋀_{j=1..m} ( Σ_{k=1..n} S_{i,j,k} = T_i ) ∧ ( S_{i,j,k} ≥ 0 )
```

**QML example — budget allocation per quarter:**

```yaml
- id: quarterly_budget
  kind: MatrixQuestion
  title: "Allocate $100,000 across departments for each quarter (must sum to 100 per row)"
  rows:
    - "Q1"
    - "Q2"
    - "Q3"
    - "Q4"
  columns:
    - "Engineering"
    - "Marketing"
    - "Sales"
    - "Operations"
  input:
    control: Editbox
    min: 0
    max: 100
  postcondition:
    # Each row (quarter) must sum to exactly 100
    - predicate: |
        all([sum([quarterly_budget.outcome[j][k] for k in range(4)]) == 100
             for j in range(4)])
      hint: "Each quarter's allocations must sum to exactly 100 (representing $100k)"
    # All values non-negative (already covered by min: 0, but documented as constraint)
    - predicate: |
        all([quarterly_budget.outcome[j][k] >= 0
             for j in range(4) for k in range(4)])
      hint: "All allocations must be non-negative"
```

**Variant — column-wise totals (each column sums to fixed value):**

```yaml
postcondition:
  - predicate: |
      all([sum([quarterly_budget.outcome[j][k] for j in range(4)]) == 100
           for k in range(4)])
    hint: "Each department's annual share must sum to exactly 100"
```

**Why it matters:** Without the sum constraint, respondents can produce
allocations that don't add up, making weighted aggregation meaningless.

**Validation coverage:** Runtime-enforced (FlowProcessor) + Static-validated
(ItemClassifier ≥ 1.14.0) — covers `sum([...]) == K` and `>= K` / `<= K`
shapes shown above. Variants with `min` / `max` folds, runtime-bound totals
(`sum([...]) == q_target.outcome`), or non-literal range bounds fall back
to runtime enforcement only; `validate_qml_file` surfaces the gap via
`coverage_gaps`.

---

## Pattern 3 — Ranking (Distinct-Value) Constraint

**Use when:** each row (or column) must be a permutation of `[1..k]` —
respondents rank the columns by importance/preference for each row, with no
ties allowed.

**Formal definition (thesis, vector form per row):**
```
Q_i := ⋀_{j=1..m} ( ⋀_{k=1..n} 1 ≤ S_{i,j,k} ≤ n )
              ∧ Distinct(S_{i,j,1}, ..., S_{i,j,n})
```

**QML example — ranking attributes per product:**

```yaml
- id: product_attribute_ranks
  kind: MatrixQuestion
  title: "For each product, rank the attributes 1-4 (1 = most important, 4 = least)"
  rows:
    - "Smartphone"
    - "Laptop"
    - "Tablet"
  columns:
    - "Price"
    - "Performance"
    - "Battery"
    - "Design"
  input:
    control: Dropdown
    labels:
      1: "1 (most important)"
      2: "2"
      3: "3"
      4: "4 (least important)"
  postcondition:
    # Each row must contain a permutation of [1,2,3,4]: no duplicate ranks
    - predicate: |
        all([len(set([product_attribute_ranks.outcome[j][k] for k in range(4)])) == 4
             for j in range(3)])
      hint: "Each rank (1-4) must be used exactly once per product"
    # Each value must be in valid range (already covered by labels, but explicit)
    - predicate: |
        all([1 <= product_attribute_ranks.outcome[j][k] <= 4
             for j in range(3) for k in range(4)])
      hint: "Ranks must be between 1 and 4"
```

**Variant — distinct values across the entire matrix** (e.g., assigning unique
priority numbers to every cell):

```yaml
postcondition:
  - predicate: |
      len(set([product_attribute_ranks.outcome[j][k]
               for j in range(3) for k in range(4)])) == 12
    hint: "Each priority slot (1-12) must be assigned exactly once"
```

**Why it matters:** Without the distinctness postcondition, ranking degenerates
into rating — respondents straightline (e.g., all 1s) and the ordinal
information is lost.

**Validation coverage:** Runtime-enforced (FlowProcessor) + Static-validated
(ItemClassifier ≥ 1.14.0) — covers `len(set([...])) == K` shape shown above
where the literal `K` matches the unrolled list length (canonical "all
distinct" form). Variants with `set(...)` outside the `len(...) == K`
pattern, or partial-distinctness shapes (`len(set(...)) == K` with `K < N`),
fall back to runtime enforcement only; `validate_qml_file` surfaces the gap
via `coverage_gaps`.

---

## Combining Patterns

A single matrix item can carry multiple postconditions. For example, a
correlation matrix that is both symmetric AND has unit diagonal AND has
bounded off-diagonals would combine all three pattern fragments. Each
predicate is ANDed; supply a specific `hint:` for each so the respondent
knows which constraint failed.

## Reference

Saghelyi, P. — "Formal Verification of Questionnaires", Section "Extension to
Complex Item Types — Common Constraint Patterns". The patterns are formalized
in `definitions.tex` (Ranking, Allocation, Matrix Symmetry) and demonstrated
in concrete QML in `appendix.tex` (Product Comparison Matrix; Market Research
Survey).
