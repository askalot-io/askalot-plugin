# Weighting Methodology Guide

Reference material for evaluating post-stratification weighting effectiveness. Covers
when to weight, design effect interpretation, weight diagnostics, and improvement
recommendations. Sourced from ESS methodology, Kalton & Flores-Cervantes (2003),
and established survey weighting literature.

## When to Weight

### Raking vs Post-Stratification
- **Raking (iterative proportional fitting)**: Preferred when adjusting for 5-8 marginal
  variables simultaneously. Each variable adjusted independently, then iterated until
  convergence. This is the method used by Askalot's `apply_raking` tool
- **Post-stratification**: Preferred when adjusting for 2-3 cross-tabulated variables
  (e.g., age × gender cells). More precise but requires sufficient respondents per cell

### Decision Criteria
- Use raking when you have many adjustment variables but limited cross-tabulation cells
- Use post-stratification when you have few variables but need precise cell matching
- **Do not weight** when sample already matches targets (RMSE < 0.02) — adds variance
  without meaningful improvement
- **Do not weight** on outcome variables — only on demographic/design variables

## Design Effect (DEFF)

### Formula
DEFF = 1 + CV², where CV = standard deviation of weights / mean of weights

### Interpretation Thresholds
- **DEFF < 1.2**: Excellent — weighting barely affects variance. Weights are uniform
- **DEFF 1.2-1.5**: Good — modest efficiency loss, acceptable for most analyses
- **DEFF 1.5-2.0**: Acceptable — noticeable variance increase, report n_eff alongside n
- **DEFF 2.0-3.0**: Concerning — weighting compensates aggressively. Investigate which
  groups drive the high DEFF
- **DEFF > 3.0**: Problematic — effective sample size less than 1/3 of actual. Consider
  trimming weights or redesigning the sampling approach

### Effective Sample Size
n_eff = n / DEFF

**Example:** 500 respondents with DEFF = 2.0 → n_eff = 250. All confidence intervals,
significance tests, and margin-of-error calculations should use n_eff, not n.

## Weight Distribution Diagnostics

### Coefficient of Variation (CV) of Weights
- **CV < 0.3**: Excellent — weights are nearly uniform
- **CV 0.3-0.5**: Good — moderate weight variation
- **CV 0.5-1.0**: Acceptable but monitor — some respondents contribute disproportionately
- **CV > 1.0**: Concerning — high weight variability, consider trimming

### Max Weight Ratio
The ratio of the largest weight to the smallest weight (or to the mean weight).

- **Max/mean < 3:1**: Acceptable
- **Max/mean 3:1 to 4:1**: Review the heavily weighted group — why are they so rare?
- **Max/mean > 4:1**: Structural problem — the sampling frame is missing this group.
  Weighting cannot substitute for proper coverage

### Individual Weight Cap
No single respondent should carry > 1-2% of the total weight sum. If one respondent's
weight represents > 2% of total, their individual responses disproportionately influence
all survey estimates.

## Weight Trimming

### When to Trim
Apply trimming when:
- Max weight ratio exceeds 4:1
- CV of weights exceeds 1.0
- Individual respondent carries > 2% of total weight
- DEFF exceeds 2.5

### Trimming Methods
- **Percentile cap**: Cap weights at 95th or 99th percentile. Simplest, most common
- **Median + IQR**: Cap at median + 6 × IQR. Adapts to distribution shape
- **Hard trimming**: Replace extreme weights with the cap value. Fast, one-pass
- **Soft trimming**: Redistribute excess weight proportionally to non-trimmed cases.
  Preserves weighted totals

### Iterative Raking-then-Trimming
1. Run raking to convergence
2. Trim extreme weights
3. Re-run raking (trimmed weights break marginal constraints)
4. Repeat until weights converge and no trimming needed (usually 2-3 iterations)

**Caution:** Over-trimming can undo the representativeness gains from raking. Always
compare quality metrics before and after trimming.

## Evaluating Weighting Effectiveness

### Bronze vs Silver Comparison
The primary evaluation: compare quality metrics before (Bronze) and after (Silver) weighting.

**Key indicators of successful weighting:**
- Overall quality score improved (Silver > Bronze)
- RMSE decreased across most factors
- Max deviation reduced — worst-case category is closer to target
- No factor got substantially worse after weighting

**Warning signs:**
- DEFF > 2.0 despite only modest quality improvement → weighting costs more than it gains
- One factor improved but another degraded → weights are pulling in conflicting directions
- Quality improvement < 5% with DEFF > 1.5 → weighting adds variance without meaningful
  representativeness gain

### Sensitivity Analysis
To assess weighting robustness:
- Rerun key estimates excluding the top 5% most heavily weighted respondents
- If estimates change substantially, conclusions are fragile and dependent on a few cases
- Report both weighted and unweighted estimates for transparency

### What to Report
For any weighted analysis, always include:
- Unweighted sample size (n)
- Effective sample size (n_eff)
- Design effect (DEFF)
- Weight distribution summary (mean, SD, min, max, CV)
- Bronze vs Silver quality scores

## Common Pitfalls

### Too Many Adjustment Variables
Each additional raking variable increases weight variance. With > 8 variables:
- Weights may fail to converge
- DEFF increases substantially
- Small cells get extreme weights
- **Recommendation**: Limit to 5-6 factors. Prioritize factors that correlate most
  strongly with key survey outcomes

### Adjusting on Outcome Variables
Never weight on variables that are outcomes of interest (e.g., don't weight by
satisfaction level to study satisfaction drivers). This introduces circular bias.

### Assuming Weighting Fixes Everything
Weighting adjusts for measured differences between sample and target. It cannot correct:
- **Unmeasured confounders**: If non-respondents differ on unmeasured variables
- **Measurement error**: Straightlining, social desirability bias
- **Coverage error**: Groups absent from the sampling frame entirely

### Ignoring Weight Variability in Tests
Standard significance tests assume equal weights. With highly variable weights:
- Use design-adjusted standard errors
- Apply Bonferroni or similar corrections for multiple comparisons
- Report n_eff alongside test results

## Improvement Recommendations

### For Under-Represented Groups
1. **Adjust quota targets**: Set quotas 10-20% above target for hard-to-reach groups
2. **Over-recruit**: Plan for 2:1 oversample ratio in historically low-response segments
3. **Diversify channels**: Add recruitment channels that reach underrepresented demographics
4. **Extend fieldwork**: Allow more time for slow-filling quota cells
5. **Increase incentives**: Targeted higher incentives for underrepresented groups

### For High Weight Variance
1. **Reduce adjustment variables**: Focus on the 3-5 most impactful factors
2. **Use broader categories**: Collapse fine-grained categories (e.g., 5-year age bands
   instead of single years)
3. **Apply weight trimming**: Cap at 95th percentile with redistribution
4. **Improve sampling**: Better initial sampling reduces the need for aggressive weighting

### For Low Quality Scores
1. **Review sampling frame**: Does it cover the target population? Are any groups excluded?
2. **Check quotas**: Do they match current census/population data?
3. **Analyze nonresponse**: Which invited respondents declined? Any systematic pattern?
4. **Consider stratified sampling**: Pre-stratify by key demographics before random selection
5. **Multi-mode data collection**: Add phone or in-person for groups underrepresented online
