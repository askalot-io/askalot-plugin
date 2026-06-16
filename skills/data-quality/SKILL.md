---
name: data-quality
description: Use when analyzing survey data quality, evaluating representativeness, interpreting quality metrics (RMSE, MAE, Chi-Square), assessing weighting effectiveness, or reviewing response quality indicators.
---

# Data Quality Assessment Guide

Reference material for evaluating survey data quality. Covers response quality indicators,
sample representativeness metrics, and interpretation thresholds grounded in established
survey methodology (AAPOR, Krosnick, ESOMAR).

## Response Quality Indicators

### Straightlining Detection
Straightlining occurs when respondents select the same option across all items in a matrix
or grid question, indicating inattentive or satisficing behavior (Krosnick, 1991).

**Detection methods:**
- **Longest Identical String (LIS)**: Count the maximum consecutive identical responses in
  a matrix block. LIS ≥ 80% of items in a block = flag for review
- **Within-scale Standard Deviation**: Calculate SD of responses within each respondent's
  matrix block. SD = 0 across ≥ 3 items = probable straightliner
- **Cross-question consistency**: Reverse-coded items should show inverse pattern. Same
  direction on both regular and reverse items = acquiescence or straightlining

**Prevalence thresholds:**
- < 5% of respondents flagged: Normal, no action needed
- 5-15% flagged: Investigate — may indicate confusing question design
- > 15% flagged: Structural problem — redesign the matrix or add attention checks

### Speeding Detection
Respondents who complete pages or the entire survey too quickly are unlikely to have
read and considered the questions (satisficing theory). Speeding is a strong indicator
of reduced response quality and engagement.

**Comprehensive speeding thresholds** (based on Zhang & Conrad 2014, Krosnick 1991):

**Per-word-of-text metrics** (most precise measure):
- < 300 milliseconds per word = Flash-through (very strong speeding indicator)
- 300-500 ms per word = Quick but plausible (verify with other indicators)
- 500-1000 ms per word = Normal reading pace
- > 1000 ms per word = Deliberate, careful reading

**Education-stratified effects** (speeding varies significantly by education):
- **Less than high school**: Baseline speeding threshold 250 ms/word (process language more slowly)
- **High school**: Baseline 300 ms/word
- **College+**: Baseline 400 ms/word (faster readers)

Failure to adjust thresholds by education level will over-flag educated respondents and miss problems with less-educated respondents.

**Per-page thresholds:**
- < 2 seconds per page with any substantial content = definite speeder (regardless of word count)
- Response time in bottom 5th percentile of distribution = flag for review
- Pages with open-ended questions: allow 5+ seconds minimum (composition time needed)

**Overall completion time:**
- Completion time < 1/3 of median completion time = flag as speeder
- Completion time < 1/2 of median = review for quality issues
- Always calculate thresholds from the distribution itself, not external standards
- Use iterative trimming: calculate median excluding obvious speeders, then re-identify speeders

**Speeding-Straightlining correlation** (Zhang & Conrad 2014):
- Strong positive correlation exists: speeders are 2-3x more likely to straightline
- When speeding detected, pay special attention to Longest Identical String (LIS) in matrix blocks
- If both speeding AND straightlining present in same respondent: strong data quality concern

**Measurement quality impact**:
- Speeding reduces response variance by 15-25%
- Speeding increases acquiescence bias by 10-15%
- Speeding responses show lower variance on Likert scales (tendency to select midpoint)
- Real-time intervention evidence: showing speeding respondents a warning reduces speeding by 30-40% and improves quality

**Actions:**
- Flag speeders but don't automatically remove from analysis
- Report speeder percentage alongside quality metrics
- If > 20% speeders: investigate survey design (too long? repetitive? low engagement?)
- Consider implementing real-time warnings: "You completed this section very quickly. Please review your answers."
- For sensitive/important surveys: manually review 10% of speeders to assess if data is usable despite speed

### Item Nonresponse
High skip rates on specific questions indicate problems with question design, sensitivity,
or respondent fatigue.

**Thresholds:**
- < 5% skip rate per question: Normal
- 5-10% skip rate: Monitor — may be sensitive or confusing
- > 10% skip rate: Investigate wording, placement, or sensitivity
- > 20% skip rate: Redesign the question or make it optional explicitly

**Patterns to watch:**
- Increasing skip rates toward end of survey = fatigue effect
- High skip rate on single question = sensitivity or confusing wording
- High skip rate across demographic subgroup = cultural sensitivity or access issue

### Acquiescence Bias
Systematic tendency to agree with statements regardless of content, especially prevalent
in agree/disagree Likert scales.

**Detection:**
- > 70% agreement rate across all Likert items = potential acquiescence
- Check both positively and negatively worded items — true acquiescers agree with both
- Compare agreement rates between educational/literacy subgroups

**Mitigation in analysis:**
- Cannot be "fixed" by weighting — it's a measurement error
- Report as limitation
- Recommend balanced scales (forced choice) for future surveys

## Sample Representativeness Metrics

### RMSE (Root Mean Square Error)
Overall measure of deviation between sample and target distributions across all categories.

**Formula:** RMSE = √(Σ(actual_i - target_i)² / N_categories)

**Interpretation thresholds:**
- < 0.02 (< 2pp): Excellent — sample closely matches targets
- 0.02-0.05 (2-5pp): Acceptable — minor deviations, weighting should correct
- 0.05-0.10 (5-10pp): Concerning — significant deviations, investigate causes
- > 0.10 (> 10pp): Problematic — structural sampling issues, weighting may not suffice

**Notes:**
- RMSE penalizes large deviations more than many small ones (squared term)
- Sensitive to outlier categories — one very off category inflates RMSE
- Always report alongside MAE for context

### MAE (Mean Absolute Error)
Average per-category deviation. More robust to outlier categories than RMSE.

**Formula:** MAE = Σ|actual_i - target_i| / N_categories

**Interpretation:**
- < 0.02: Excellent per-category match
- 0.02-0.05: Acceptable — average category off by 2-5 percentage points
- > 0.05: Several categories substantially off-target

**When MAE << RMSE:** One or two categories are severely off while others are fine.
**When MAE ≈ RMSE:** Deviations are uniformly distributed across categories.

### Chi-Square Test
Tests whether observed deviations from targets are statistically significant versus
random sampling noise.

**Interpretation:**
- p > 0.05: Deviations consistent with random sampling — no systematic bias detected
- p ≤ 0.05: Statistically significant deviation — systematic sampling issue likely
- **Always consider df and sample size**: With large samples, even trivial deviations
  become "significant." A significant chi-square with RMSE < 0.02 may not be actionable

**Caution:** Chi-square is sensitive to sample size. With N > 500, almost any deviation
will be significant. Use RMSE/MAE for practical significance, chi-square for statistical.

### Max Deviation
The worst single-category gap between actual and target proportions.

**Interpretation:**
- < 0.05 (< 5pp): All categories within acceptable range
- 0.05-0.10 (5-10pp): One category moderately off — likely correctable by weighting
- > 0.10 (> 10pp): Structural gap — at least one demographic group is substantially
  misrepresented. Weighting may introduce excessive variance for this group

**Action guidance:**
- Identify which category has max deviation
- If over-represented: reduce quota for that group in next wave
- If under-represented: increase recruitment effort for that group

## Quality Score Interpretation

### Composite Score (0-1)
The overall quality score combines RMSE across all factors with factor-specific weights.

**Thresholds:**
- > 0.8: Good quality — sample adequately represents target population
- 0.6-0.8: Acceptable — some factors off-target, weighting recommended
- 0.4-0.6: Poor — significant representativeness issues, investigate root causes
- < 0.4: Critical — sample does not represent target population, results unreliable

### Per-Factor vs Overall Assessment
- A high overall score can mask one poorly represented factor
- Always review per-factor breakdown even when overall score is acceptable
- The factor with the lowest score often drives the most bias in survey estimates

### Effective Sample Size
After weighting, the effective sample size accounts for variance introduced by weights.

**Formula:** n_eff = n / DEFF, where DEFF = 1 + CV² (CV = coefficient of variation of weights)

**Interpretation:**
- n_eff / n > 0.80: Minimal efficiency loss from weighting
- n_eff / n = 0.50-0.80: Moderate loss — some groups heavily weighted
- n_eff / n < 0.50: Severe loss — weighting compensating too aggressively

## AAPOR Standards Reference

### Response Rate Categories
- **RR1**: Minimum response rate (completed / eligible)
- **RR3**: Includes partial completes as partial responses
- **RR6**: Maximum, assigns estimated eligibility to unknowns

### Total Survey Error Framework
Quality issues arise from four error sources:
1. **Coverage error**: Target population members missing from sampling frame
2. **Sampling error**: Random variation from selecting a subset (reducible by larger n)
3. **Nonresponse error**: Systematic differences between respondents and non-respondents
4. **Measurement error**: Inaccurate responses due to question design, mode effects

Quality metrics (RMSE, MAE) primarily detect coverage and nonresponse error.
Response quality indicators (straightlining, speeding) detect measurement error.

## ESOMAR Benchmarks

### Online Panel Quality
- Minimum panel size: 5,000 for national representativeness
- Recruitment diversity: ≥ 3 independent recruitment channels
- Average survey length: 15-20 minutes optimal, > 30 minutes = quality degradation
- Incentive consistency: Same incentive structure across demographic groups

### Quota Sampling Validation
- Quotas should match census targets within ±2pp per cell
- Interlocking quotas (age × gender) preferred over independent quotas
- Monitor fill rates — quotas that fill slowly indicate hard-to-reach groups

## Satisficing and Response Strategy Detection

### Conditions Triggering Satisficing

Respondents shift from "optimizing" (careful, thoughtful responses) to "satisficing" (quick, minimally-considered responses) when conditions create cognitive burden or low motivation.

**High-burden conditions** (increase satisficing 30-50%):
- Questionnaire length > 25 minutes
- Matrix questions with > 10 rows
- Complex skip logic or conditionals
- Scales with > 7 points
- Open-ended questions without clear boundaries

**Low-motivation conditions** (increase satisficing 20-40%):
- Topic perceived as irrelevant to respondent
- No incentive or low incentive value
- Survey administered in low-attention context (mobile, divided attention)
- End of survey (fatigue effect)

**Respondent vulnerability to satisficing**:
- Age 65+ (cognitive processing slower)
- Lower education (language processing difficulty)
- Non-native language speakers (comprehension burden)
- Low income (competing time demands)

**Detection indicators**:
1. **Non-differentiation pattern**: Same response across all items in matrix (straightlining)
2. **Primacy bias**: Systematic selection of first options (especially on long lists)
3. **Recency bias**: Systematic selection of last options
4. **Acquiescence**: Agreeing with all statements in agree/disagree scale (> 85% agreement rate)
5. **Moderate response bias**: Always selecting middle option on 5+ point scales
6. **Speeding** (above thresholds): Completion time too fast for content amount
7. **Item nonresponse variance**: Skips items inconsistently rather than at logical boundaries

### Prevention Strategies (Effectiveness by Condition)

**Design-level** (prevent satisficing):
- Reduce survey length to < 20 minutes (effectiveness: 25-35% reduction in satisficing)
- Limit matrix width to ≤ 6 columns (effectiveness: 20-30% reduction)
- Use 5-7 point scales not 10-point (effectiveness: 15-20% reduction in non-differentiation)
- Randomize scale direction (prevent mechanical responding): effectiveness: 30-40%
- Remove "Don't know" option for knowledge questions (forces meaningful response): effectiveness: 10-15% increase in data quality for non-knowledgeable respondents

**Presentation-level** (motivate respondents):
- Emphasize survey relevance and purpose (effectiveness: 15-20% reduction in satisficing)
- Use progress indicators (visual proof of completion): effectiveness: 10-15% engagement boost
- Break survey into multiple sessions if possible (effectiveness: 25-30% quality improvement)
- Use conditional branching to show only applicable questions (perceived burden reduction): effectiveness: 20-25%

**Incentive-level** (increase motivation):
- Provide upfront incentive rather than promised incentive (effectiveness: 15-25% quality improvement)
- Contingent incentives ("Complete all items for bonus"): effectiveness: 20-30%
- Match incentive to population values (effectiveness: varies, 10-40%)

## Advanced Measurement Quality Metrics

### Multi-Trait Multi-Method (MTMM) Analysis for Scale Validation

When multiple items are designed to measure the same construct, validate convergent and discriminant validity:

**Cronbach's Alpha (internal consistency)**:
- α ≥ 0.80: Excellent consistency (reliable measurement)
- α 0.70-0.80: Acceptable (adequate for research)
- α 0.60-0.70: Marginal (acceptable if construct is multidimensional)
- α < 0.60: Problematic (items don't measure same construct)

**Meta-analytic findings on Cronbach's alpha**:
- By survey context: Attitude surveys average α = 0.75; behavioral scales average α = 0.68
- By item count: 3-item scales average α = 0.60; 10+ item scales average α = 0.85
- Education effect: Lower education samples show 5-10% lower alpha due to comprehension variance
- Test-retest reliabilities typically 0.15-0.25 lower than internal consistency

### Acquiescence as Method Effect

Acquiescence bias — systematic tendency to agree with statements — is a form of measurement error, not a respondent trait:

**Prevalence**:
- Affects 10-30% of respondents across surveys
- Higher in: older respondents (+15-20%), lower education (+10-15%), interview mode (+15-25% vs. self-administered)
- Effect size: Inflates agreement rates 10-15 percentage points above true underlying opinion

**Detection**:
- Implement reverse-coded items in same scale (e.g., both "I enjoy my job" AND "I dislike my job")
- Compare agreement rates on positively-worded vs. negatively-worded items
- True acquiescers show > 80% agreement with BOTH positive AND negative statements on same topic

**Measurement approach - agree/disagree vs. forced choice**:
- Agree/disagree scales: 10-15% higher agreement rates than forced choice (agree/disagree) on same items
- Forced-choice scales show less acquiescence: respondents must choose between two options
- Meta-analysis: ~50% reduction in acquiescence bias when switching from agree/disagree to forced choice format

### Missing Data Patterns as Quality Indicator

Item-level missing data patterns reveal respondent engagement and construct clarity:

**Monotone missing patterns** (row i has missing, all subsequent rows have missing):
- Indicates fatigue or dropout
- Respondent stopped engaging partway through
- Analysis impact: Higher standard errors, potential bias if monotone missing correlates with values of interest

**Random missing patterns** (scattered across items):
- Indicates sensitivity or confusion on specific items
- Acceptable when < 5% per item
- Suggests targeted redesign for high-missing items

**Section-specific missing** (all items in one block have high missing):
- Matrix blocks missing more than adjacent blocks: possible layout or comprehension problem
- Sensitive topic block missing more: understandable if topic very sensitive
- Late-survey block missing more: fatigue effect

**Threshold interpretation**:
- < 1% missing per item: Minimal concern
- 1-5% per item: Normal, acceptable
- 5-10% per item: Investigate (sensitive? unclear?)
- > 10% per item: Serious concern (redesign or exclude item)

### Open-Ended Response Quality Metrics

For surveys with open-ended questions, assess informativeness using Gricean maxims framework:

**Gricean maxims-based informativeness scoring** (Xiao 2020, AI chatbot survey work):

1. **Quantity maxim** (appropriate amount of information):
   - Too brief (< 5 words): Likely satisficing or insufficient effort
   - Adequate (5-20 words): Normal response
   - Very detailed (> 50 words): Over-explanation or elaboration

2. **Quality maxim** (truthfulness and accuracy):
   - Self-contradictions within response: quality concern
   - Inconsistent with closed-ended answers: quality concern
   - Specific examples provided: quality indicator (+ quality)

3. **Relation maxim** (relevance to question):
   - Off-topic responses: Quality concern
   - Addresses specific question asked: Quality indicator
   - Tangential but related: Acceptable

4. **Manner maxim** (clarity and organization):
   - Clear sentence structure: Quality indicator
   - Rambling or disorganized: Quality concern
   - Jargon or technical language appropriate to topic: Quality indicator

**Measurement**:
- Score each open response 0-10 on combined maxim adherence
- Average scores by respondent identify high-quality vs. low-quality respondents
- Items with consistent low informativeness scores: redesign for closed-ended or clearer guidance
