# Scale Design Principles

How to build a rating scale and declare it in QML. The label sets, the
"what am I measuring, which scale" guide, the out-of-scale options and the
evidence behind each rule are in `standard-scales.md`: read it before you
write the labels of any rating item. This file keeps the working rules and
the QML side.

## Decide What the Item Measures

Every rating item measures one of five things, and the choice is the
Designer's: nothing in QML states it or checks it.

| The item measures | Scale to take from `standard-scales.md` |
|---|---|
| An opinion on a statement | Agreement (A1), only for a battery of statements or a validated instrument |
| A feeling | Satisfaction (B), or an intensity scale (G1) |
| A behaviour | Frequency (D), or a count in an Editbox |
| An evaluation | Quality (C), comparison (I) |
| An intention | Likelihood or probability (E) |

Ask about the thing itself. An item-specific scale is easier to answer and
less prone to acquiescence than the same content rewritten as a statement to
agree with.

- BAD: "How often do you exercise?" → "Strongly disagree ... Strongly agree"
- BAD: "I am satisfied with the service" → agree/disagree
- GOOD: "How often do you exercise?" → "Never ... Always"
- GOOD: "How satisfied are you with the service?" → "Very dissatisfied ... Very satisfied"
- GOOD: "Exercise is important to my health" (an opinion on a statement) → "Strongly disagree ... Strongly agree"

## Polarity, Length, Midpoint

- **Bipolar**: two opposite sides around a neutral point (agree and disagree,
  better and worse). **Unipolar**: from none to the most of one thing
  (frequency, importance, concern). Satisfaction and likelihood have a
  standard form of each kind; pick one per questionnaire.
- **Length**: about 7 points for a bipolar key measure, 5 otherwise; 4 or 5
  for a unipolar scale. A validated instrument keeps its own length (an
  11-point 0 to 10 item, a 4-point symptom scale).
- **Midpoint**: a bipolar scale has one exactly when its point count is odd.
  Choose an even count only to force a direction. The middle of a unipolar
  scale is a real amount, never "Neutral".
- Keep one length and one direction for the same kind of item through a
  questionnaire.

## Declaring the Scale in QML

A Radio or Dropdown Question, QuestionGroup or MatrixQuestion declares the
structure of its scale with one `scale` key, and you write every label
yourself (`qml-syntax` §4.10 has the full rules):

```yaml
- id: q_service
  kind: QuestionGroup
  title: "How satisfied are you with each of the following?"
  questions:
    - "Customer service"
    - "Delivery speed"
    - "Product quality"
  scale:
    polarity: bipolar
    points: 5
  input:
    control: Radio
    labels:
      1: "Very dissatisfied"
      2: "Somewhat dissatisfied"
      3: "Neither satisfied nor dissatisfied"
      4: "Somewhat satisfied"
      5: "Very satisfied"
      8: "Did not use"
```

- `polarity` and `points` are required. `start: 0` is for a scale published
  from 0; the default is 1. `order: descending` shows the highest code first
  and changes no code.
- **Codes run from the negative or low end to the positive or high end.**
  Never code "Strongly agree" as 1. Nothing checks the wording, so a scale
  coded the wrong way loads and turns every measure upside down.
- The declaration is what the quality measures, the exports and the Gold
  scale score read, in any questionnaire language. An undeclared rating item
  is just a list of labels to them.
- A Slider is not a declared scale. Use a declared Radio or Dropdown for a
  subjective rating; keep the Slider for magnitudes that are numbers.

## Out-of-Scale Answers ("Don't know", "Does not apply", "Prefer not to say")

A label whose code is above the scale's range is an out-of-scale answer; in
the example above, `8: "Did not use"`. You choose the code and the wording,
and keep one code per meaning through the questionnaire. It is shown after
the points, never as a midpoint. It counts as answered, so it never pushes a
respondent under a completeness threshold, and its value is missing in every
quality measure, reliability figure and scale score. When to offer which one:
`standard-scales.md`, section 2.

## Reverse-Worded Items

A battery may mix positively and negatively worded statements to counter
acquiescence; write the opposite without a negation, since naively reversed
items can lower reliability. Every item of a battery is coded in the same
direction and declared once; which items are reverse-worded is not written in
QML. The analyst ticks them when building the Gold scale score, which
reverses them as `2 * start + points - 1 - code` and reports the score's
reliability. Name the reverse-worded statements in the design notes so the
analyst knows which to tick.

## Verbal Labels on Every Point

Label every scale point with words up to 7 points. Fully labelled scales are
more reliable and less open to context effects than end-labelled ones.

- BAD: "1 ——— 2 ——— 3 ——— 4 ——— 5" (only the ends labelled)
- GOOD: "Poor / Fair / Good / Very good / Excellent"

Do not add numbers to a verbal scale ("1 = Never, 2 = Rarely"): numbers imply
equal intervals the words may not have. The exception is an end-labelled
numeric instrument (a 0 to 10 item), where the numbers are the labels.

## Branching Bipolar Scales

For a long bipolar scale asked by voice, consider two steps:
1. First ask the direction: "Overall, do you approve or disapprove?"
2. Then ask the intensity: "Would you say you strongly or somewhat [approve/disapprove]?"

In QML, implement as a Switch item followed by a preconditioned Radio item.
The two items are not a declared scale; prefer one declared item unless the
mode needs the split.

## Natural Metrics Over Vague Quantifiers

When a natural numeric metric exists, use it instead of vague frequency labels.

- BAD: "How often do you visit the doctor?" → "Rarely / Sometimes / Often"
- GOOD: "How many times did you visit a doctor in the past 12 months?" → Numeric input

In QML: use an Editbox with appropriate `min`/`max` rather than a Radio
with vague frequency labels. Keep a frequency scale for habits that have no
countable unit.

## Scale Length vs. Survey Length Trade-Off

In long surveys (80+ items per respondent), fewer response categories
per question reduces total cognitive burden:

- For non-critical items: 4 points may suffice
- For key research questions: 5 points, or 7 on a bipolar scale, for precision
- For screening/routing items: use binary (Yes/No) wherever possible

The cumulative time saved from shorter scales across many items can
be significant in large instruments.
