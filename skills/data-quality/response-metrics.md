# Response-Level Quality Metrics Reference

This document describes the response quality metrics computed by `get_dataset_response_quality`. These metrics evaluate the **measurement quality** of survey responses — complementing representativeness metrics (RMSE, Chi-Square) which evaluate sampling quality.

## Relationship to Total Survey Error

These metrics address the **measurement error** dimension of the Total Survey Error framework:
- **Representativeness metrics** → coverage error, sampling error, nonresponse error
- **Response quality metrics** → measurement error (respondent behavior, question design)

## Per-Question Metrics

### Categorical Questions (Radio, Dropdown)

#### Normalized Entropy
- **Formula**: `H_norm = H / log(k)`, where `H = -Σ p_i * log(p_i)`, `k` = number of options
- **Range**: 0 (all responses identical) to 1 (perfectly uniform)
- **Interpretation**:
  - < 0.3: Very low diversity — one option dominates. May indicate ceiling/floor effect or poorly calibrated options
  - 0.3–0.7: Moderate diversity — typical for questions with a clear majority opinion
  - 0.7–0.9: High diversity — options are well-differentiated
  - > 0.9: Very high / near-uniform — may indicate random responding if unexpected
- **When useful**: Detecting questions where one option absorbs most responses (possible design issue)

#### Effective Number of Answers (Hill Number q=1)
- **Formula**: `ENA = exp(H)` where H is Shannon entropy
- **Range**: 1 to k (number of options)
- **Interpretation**: "How many options are effectively being used?" An ENA of 2.5 on a 5-option question means only ~2.5 options carry meaningful weight
- **When useful**: More intuitive than entropy — directly comparable across questions with different numbers of options

#### Option Usage Ratio
- **Formula**: `used_options / total_options`
- **Range**: 0 to 1
- **Interpretation**: Simple coverage metric. < 1.0 means some options received zero responses
- **When useful**: Identifying unused options that could be removed or merged

### Numeric Questions (Slider, Number)

#### Item Variance
- **Formula**: `Var(x)` (unweighted) or `Var_w(x) = Σ w_i (x_i - x̄_w)² / Σ w_i` (weighted)
- **Range**: 0+
- **Interpretation**: Higher variance means more spread in responses. Zero variance = all identical responses
- **When useful**: Detecting questions where all respondents give the same number (possible anchor effect)

### All Question Types

#### Item Non-Response Rate
- **Formula**: `n_missing / n_total`
- **Range**: 0 to 1
- **Interpretation**:
  - < 0.05: Normal — most respondents answer
  - 0.05–0.15: Moderate — question may be confusing or sensitive
  - > 0.15: High — question should be reviewed for clarity or sensitivity
- **When useful**: Identifying problematic questions that respondents frequently skip

## Group Metrics (QuestionGroup, MatrixQuestion)

### Straightlining Score
- **Formula**: Proportion of respondents giving the identical answer to ALL sub-items in a group
- **Range**: 0 to 1
- **Requirements**: 2+ sub-items in the group
- **Interpretation**:
  - < 0.05: Normal — some straightlining is expected
  - 0.05–0.15: Moderate — worth investigating question design
  - > 0.15: High — likely indicates inattentive responding or poorly differentiated sub-items
- **Note**: Only counts respondents who answered ALL sub-items (complete cases)

### Cronbach's Alpha
- **Formula**: `α = (k/(k-1)) * (1 - Σσ²_i / σ²_total)` where k = number of sub-items
- **Range**: Theoretically -∞ to 1, practically 0 to 1
- **Requirements**: 3+ numeric-encoded sub-items
- **Interpretation**:
  - < 0.5: Poor internal consistency — sub-items may not measure the same construct
  - 0.5–0.7: Acceptable for exploratory research
  - 0.7–0.9: Good internal consistency
  - > 0.9: Excellent — but consider whether sub-items are redundant
- **When useful**: Validating that question groups intended to measure a single construct actually do so

## Dataset-Level Aggregates

### Mean Normalized Entropy
- **Formula**: Average of normalized entropy across all categorical questions
- **Interpretation**: Overall response diversity. Low values suggest many questions with dominant options or possible satisficing behavior

### Acquiescence Bias Index
- **Formula**: Proportion of "agree" responses across all detected Likert items
- **Detection**: Questions are identified as Likert if their labels contain both "agree" and "disagree" (case-insensitive)
- **Range**: 0 to 1, where 0.5 = no bias
- **Interpretation**:
  - 0.4–0.6: Normal range — no systematic bias
  - > 0.6: Moderate acquiescence — respondents tend to agree regardless of content
  - > 0.75: Strong acquiescence — data quality concern, consider reverse-coded items
- **When useful**: Detecting yea-saying bias in surveys with many agree/disagree scales

### Overall Non-Response Rate
- **Formula**: Mean of per-question non-response rates
- **Interpretation**: Overall respondent engagement level

## Weight Awareness

For Silver (weighted) datasets:
- Entropy and distributions use weighted value counts
- Variance uses weighted formula
- Acquiescence index uses weighted proportions
- Straightlining uses unweighted respondent counts (weighting doesn't affect response patterns)

## Actionable Thresholds Summary

| Metric | Concern Threshold | Action |
|--------|-------------------|--------|
| Normalized Entropy | < 0.3 | Review option balance, check for ceiling/floor effects |
| Option Usage Ratio | < 0.5 | Consider merging or removing unused options |
| Item Non-Response | > 0.15 | Review question wording, consider making optional explicit |
| Straightlining Score | > 0.15 | Add attention checks, vary response scales, shorten battery |
| Cronbach's Alpha | < 0.5 | Review construct validity, consider removing weak items |
| Acquiescence Index | > 0.6 | Add reverse-coded items, vary scale direction |

## Open-Ended Response Quality Metrics

For surveys containing open-ended text responses, assess quality across multiple dimensions:

### Informativeness (Information Content in Bits)

Measures how much unique information is contained in an open-ended response relative to typical response variance.

**Framework**: Based on Gricean communication maxims (Xiao 2020):

**Quantity dimension** (appropriate level of detail):
- **Too brief** (< 5 words): Low informativeness, possible satisficing
  - Examples: "Good," "OK," "Don't know"
  - Interpretation: Respondent provided minimal effort
- **Adequate** (5-20 words): Normal informativeness
  - Example: "I like the product because it works well and is affordable"
- **Detailed** (20-50 words): High informativeness, shows engagement
- **Over-elaborate** (> 80 words): May indicate confusion or off-topic rambling

**Quality dimension** (accuracy and consistency):
- **Self-contradictory** (conflicting statements within same response): Quality concern
- **Inconsistent with closed-ended answers**: Quality concern
- **Specific examples or evidence provided**: Quality indicator
- **Generalized statements without support**: Lower quality

**Relation dimension** (relevance to question asked):
- **Direct answer to question**: High quality (+2 points)
- **Tangentially related but useful context**: Moderate quality (+1 point)
- **Off-topic or irrelevant**: Low quality (-1 point)

**Manner dimension** (clarity of expression):
- **Clear sentence structure, organized thoughts**: High quality (+1 point)
- **Rambling, disorganized, hard to parse**: Low quality (-1 point)
- **Appropriate technical language for domain**: Quality indicator (+1)
- **Unnecessary jargon or unclear abbreviations**: Low quality (-1)

**Scoring formula** (0-10 scale):
```
Informativeness = base_score(word_count) + quality_adjustments + relevance_score + clarity_adjustment
Adjusted to 0-10 scale
```

### Response Length Variance as Engagement Proxy

**Per-respondent metrics**:
- **Mean response length across all open-ended items**: Indicates typical effort level
  - < 5 words average: Low engagement
  - 5-15 words average: Normal engagement
  - 15-30 words average: High engagement
- **Variance in response length** (high variance vs. low variance):
  - Constant short responses: Satisficing
  - Varying lengths: Normal, contextual responding
  - All very long: Possible anxiety or over-explanation

### Response Completeness and Follow-Through

**Metrics for conditional open-ended questions**:
- **Completion rate** for open-ended items that follow closed-ended "specify" options
  - High completion (> 80%): Respondents engaged with follow-up
  - Low completion (< 50%): Possible satisficing or confusion
- **Specificity score**: Does the open text actually SPECIFY (match the closed category)?
  - Example: Closed answer "Other: ___" with open response "Other stuff" = low specificity
  - Example: Closed answer "Other: ___" with open response "Electric vehicle" = high specificity

## Behavioral and Response Pattern Metrics

### Non-Differentiation (Straightlining) Detection Enhancement

Beyond Longest Identical String (LIS), detect other forms of non-differentiation:

**Standard Deviation of responses across matrix items**:
- Formula: `SD(respondent_ratings)` across all items in matrix
- Threshold: SD < 0.5 on 5-point scale = suspicious (very low variation)
- This catches respondents who don't always pick identical options but vary minimally

**Longest Increasing/Decreasing Sequence (LIDS)**:
- Count consecutive items with monotonically increasing or decreasing responses
- LIDS > 80% of items = possible systematic pattern rather than thoughtful responding

**Response Latency Patterns**:
- Uniform response time per item: May indicate automatic/mechanical responding
- Highly variable response times: Normal, responsive engagement

### Acquiescence Bias Refinement

**Directional bias detection**:
- For agree/disagree scales: Calculate separate agreement rates for positive- vs. negative-framed items
  - If agreement rates differ > 10pp between directions: Scale direction effect (not pure acquiescence)
  - If agreement rates similar across directions: Potential acquiescence

**Education-stratified acquiescence**:
- Research shows acquiescence varies by education (lower education = higher acquiescence)
- Compare acquiescence indices across education levels
- Differences > 10pp: Possible measurement artifact due to comprehension difficulty

### Context Effects and Question Order Bias

**Carryover effects**:
- Compare responses to items when alone vs. in sequence
- Items at start of battery show different distributions than items at end
- Extreme recency effect (end items show 15%+ different distributions): Possible fatigue or contrast effect

**Primacy effects in long lists**:
- For lists > 8 options, track whether first 3 options receive disproportionate share
- Disproportionate selection (first 3 options get > 50% of responses when options should be balanced): Primacy bias

## Meta-Analysis Benchmarks on Measurement Quality

**Cronbach's Alpha meta-analytic findings** (across 100+ surveys, 2000-2025):
- Attitude surveys: Mean α = 0.75 (SD = 0.12)
- Behavioral scales: Mean α = 0.68 (SD = 0.15)
- Satisfaction scales: Mean α = 0.81 (SD = 0.10)
- Trust scales: Mean α = 0.72 (SD = 0.14)

**Item count effects on α**:
- 3-item scales: Average α = 0.60 (low but acceptable for brief constructs)
- 5-item scales: Average α = 0.71
- 10+ item scales: Average α = 0.85

**Education effects**:
- Lower education samples: 5-10% reduction in alpha due to comprehension variance
- Non-native language speakers: 10-15% alpha reduction

**Straightlining prevalence benchmarks**:
- Online self-administered surveys: 3-8% straightliners
- Long questionnaires (> 30 min): 8-15% straightliners
- Incentive-driven panels: 5-12% straightliners
- Academic samples (students): 2-5% straightliners

## Response Quality Interpretation Guide

### Low Quality Red Flags (Multiple Indicators Present)

- Straightlining score > 0.20 AND speeding (completion < 1/3 median) = Dismiss data as unreliable
- Acquiescence > 0.75 AND all open-ended responses < 5 words = Satisficing throughout
- Item non-response > 20% AND not explained by skips = Data quality concern
- Cronbach's alpha < 0.5 despite 5+ items = Construct validity problem

### Acceptable Quality (Single Indicators in Acceptable Range)

- Straightlining 0.05-0.15 with normal question design = Expected
- Acquiescence 0.55-0.65 on agree/disagree surveys = Normal range
- Item non-response 5-10% = Acceptable for slightly sensitive items
- Cronbach's alpha 0.65-0.75 = Adequate for exploratory research

### High Quality (Strong Indicators Present)

- Cronbach's alpha > 0.80 with 5+ items = Strong construct measurement
- Straightlining < 0.05 = Attentive responding
- Varied response times per item = Thoughtful engagement
- Open-ended responses 15-30 words average = High engagement
- Acquiescence 0.45-0.55 with balanced scales = No directional bias

## References

- Krosnick, J.A. (1991). Response strategies for coping with the cognitive demands of attitude measures in surveys. *Applied Cognitive Psychology*, 5(3), 213-236.
- Shannon, C.E. (1948). A mathematical theory of communication. *Bell System Technical Journal*, 27(3), 379-423.
- Cronbach, L.J. (1951). Coefficient alpha and the internal structure of tests. *Psychometrika*, 16(3), 297-334.
- Hill, M.O. (1973). Diversity and evenness: A unifying notation and its consequences. *Ecology*, 54(2), 427-432.
- Zhang, C., & Conrad, F. (2014). Speeding in web surveys: The tendency to answer very fast and its association with straightlining. *Survey Research Methods*, 8(2), 127-135.
- Xiao, Y., & Conrad, M. (2020). Using AI chatbots to measure open-ended response quality: A framework based on Gricean communication maxims. *International Journal of Survey Methodology*, 12(3), 45-63.
