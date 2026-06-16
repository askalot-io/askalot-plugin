# Scale Design Principles

Rules for constructing ordinal and interval response scales.

## Unipolar vs. Bipolar

Choose the right scale type based on what you're measuring:

- **Unipolar**: measures gradation along one dimension (zero at one end).
  Examples: "Not at all satisfied" → "Extremely satisfied"; "Never" → "Always".
  Use when the concept has a natural zero point.

- **Bipolar**: measures gradation along two opposing dimensions (zero in the middle).
  Examples: "Strongly disagree" → "Strongly agree"; "Much worse" → "Much better".
  Use when the concept has two opposing poles.

Never force a unipolar concept onto a bipolar scale or vice versa.
"Satisfaction" is unipolar (zero = no satisfaction). "Agreement" is bipolar
(disagree ↔ agree with a neutral middle).

## Scale Length: 4-5 Categories

Limit ordinal scales to 4-5 categories as a default. This provides enough
discrimination without overwhelming respondents.

- 2-3 points: too few, respondents can't differentiate adequately
- 4-5 points: optimal for most research purposes
- 7+ points: only for expert populations or validated instruments
- 10-100 point scales: only when measuring magnitude (pain, satisfaction indices)

In QML: use Slider with appropriate min/max for numeric scales, or Radio
with 4-5 verbally labeled categories for ordinal scales.

## Construct-Specific Labels

Match the response labels to the question stem's construct. Don't ask
about frequency and offer agreement options.

- BAD: "How often do you exercise?" → "Strongly agree ... Strongly disagree"
- GOOD: "How often do you exercise?" → "Never ... Every day"
- GOOD: "Exercise is important to my health" → "Strongly disagree ... Strongly agree"

Direct labels (that match the question concept) improve cognitive processing
and produce more reliable data than generic agree/disagree scales.

## Balanced Scales

Provide equal numbers of positive and negative categories. The conceptual
distance between adjacent categories should be approximately equal.

- BAD: "Very good, Good, Fair, Poor" (3 positive, 1 negative — biased toward positive)
- GOOD: "Very good, Good, Fair, Poor, Very poor" (balanced)

For bipolar scales, include a midpoint only if a true neutral position
is meaningful (e.g., "Neither agree nor disagree").

## Verbal Labels on ALL Categories

Label every scale point with words, not just the endpoints. Fully labeled
scales are more reliable and less susceptible to context effects than
polar-point-only labels.

- BAD: "1 ——— 2 ——— 3 ——— 4 ——— 5" (only endpoints labeled)
- GOOD: "Very poor / Poor / Fair / Good / Very good"

## Avoid Numeric Labels on Non-Numeric Scales

Do not add numbers to vague quantifier scales (e.g., "1=Never, 2=Rarely").
Numbers imply equal intervals that may not exist between verbal categories.
Use numeric labels only for true numeric scales (age, frequency counts, etc.).

## Branching Bipolar Scales

For long bipolar scales, consider decomposing into two steps:
1. First ask the direction: "Overall, do you approve or disapprove?"
2. Then ask the intensity: "Would you say you strongly or somewhat [approve/disapprove]?"

This reduces cognitive load and improves data quality. In QML, implement as
a Switch item followed by a preconditioned Radio item.

## Natural Metrics Over Vague Quantifiers

When a natural numeric metric exists, use it instead of vague frequency labels.

- BAD: "How often do you visit the doctor?" → "Rarely / Sometimes / Often"
- GOOD: "How many times did you visit a doctor in the past 12 months?" → Numeric input

In QML: use a Number control with appropriate min/max rather than a Radio
with vague frequency labels.

## Scale Selection by Construct Type

Different constructs require different scale approaches. Match the
scale to what you're measuring:

| Construct | Recommended Scale | Example |
|-----------|-------------------|---------|
| Frequency | Natural metric (count) or frequency scale | "How many times per week...?" → Number |
| Satisfaction | Unipolar 5-point | "Not at all satisfied" → "Extremely satisfied" |
| Agreement | Bipolar 5-point or branching | "Strongly disagree" → "Strongly agree" |
| Likelihood | Unipolar 4-5 point | "Not at all likely" → "Extremely likely" |
| Importance | Unipolar 4-5 point | "Not at all important" → "Extremely important" |
| Amount | Natural metric or categories | Exact number or bracketed ranges |
| Comparison | Bipolar 5-point | "Much worse" → "Much better" |
| Yes/No fact | Binary Switch | "Yes" / "No" |

Avoid using agree/disagree scales for constructs that have more
natural response formats. "How satisfied are you?" with a satisfaction
scale produces better data than "I am satisfied with X" on an
agree/disagree scale.

## Scale Length vs. Survey Length Trade-Off

In long surveys (80+ items per respondent), fewer response categories
per question reduces total cognitive burden:

- For non-critical items: 4 categories may suffice
- For key research questions: use 5-7 categories for precision
- For screening/routing items: use binary (Yes/No) wherever possible

The cumulative time saved from shorter scales across many items can
be significant in large instruments.
