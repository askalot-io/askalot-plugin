# Response Quality and Survey Fatigue

Principles for maintaining data quality in long surveys. Based on
satisficing theory (Krosnick) and survey fatigue research.

## Satisficing Theory

Respondents perform a cost-benefit calculation for each question.
When the cost of careful answering (cognitive effort) exceeds the
perceived benefit, they **satisfice** — give a "good enough" answer
instead of the best answer.

**Weak satisficing** (subtle degradation):
- Less thorough memory search
- Less careful evaluation of options
- Accepting the first plausible answer instead of the best one

**Strong satisficing** (visible patterns):
- Straightlining: same answer for every item in a grid
- Acquiescence: agreeing with every statement regardless of content
- Primacy/recency: always selecting the first or last option
- Non-differentiation: giving identical ratings across items
- Random responding: no consistent pattern

**Factors that increase satisficing:**
- Task difficulty (complex questions, many response options)
- Low respondent ability (education, language, cognitive load)
- Low respondent motivation (topic irrelevance, survey fatigue)
- Survey length (later questions get less effort)

**Design implications**: Every design choice that reduces cognitive
effort or increases motivation reduces satisficing. This includes
clearer wording, fewer options, shorter surveys, better routing
(skipping irrelevant questions), and engaging question formats.

## Survey Length and Fatigue

Research consistently shows that response quality degrades with survey
length. The relationship is not linear — quality holds relatively
steady, then drops sharply.

**Time-based thresholds** (web surveys):
- 5-10 minutes: optimal range, minimal quality degradation
- 10-15 minutes: moderate fatigue, slight increase in satisficing
- 15-20 minutes: significant fatigue, measurable quality drop
- 20+ minutes: major quality degradation, high abandonment risk
- 30+ minutes: only acceptable for highly motivated populations
  (e.g., employees in mandatory surveys, clinical patients)

**Item-based thresholds** (rough equivalents):
- 30-50 items: optimal for general population
- 50-80 items: acceptable with good routing and varied formats
- 80-100 items: requires strong topic interest or incentives
- 100+ items: must use adaptive routing so each respondent sees
  only a relevant subset

These thresholds apply to the items each respondent actually sees, not
the total instrument size. A 500-item instrument where each respondent
answers 60-80 items through adaptive routing can maintain good quality.

## Position Effects

Questions later in the survey receive lower-quality responses. This
manifests as:

- **Reduced differentiation**: Respondents use fewer distinct values
  on rating scales in the last third of the survey
- **Faster response times**: Later questions answered 20-30% faster
  than equivalent questions in the first third
- **More missing data**: Item nonresponse increases toward the end
- **More satisficing patterns**: Straightlining and acquiescence
  increase in later grid questions

**Mitigation strategies:**
- Place the most important questions in the first half
- Use adaptive routing to keep individual survey length under 15 minutes
- Vary question formats to maintain engagement (don't stack grids)
- Place engaging or novel questions at natural fatigue points

## Straightlining

Straightlining occurs when respondents select the same response
category for every item in a grid or matrix question. It is the most
common form of strong satisficing.

**Risk factors for straightlining:**
- Long grids: 8+ rows in a single matrix dramatically increase risk
- Repetitive content: items that seem similar encourage pattern responding
- Late placement: grids in the second half of the survey
- Mobile devices: small screens make grids harder to process carefully

**Prevention strategies:**
- Limit grids to 5-7 rows maximum
- Break long item batteries into multiple smaller grids with different
  topics or formats between them
- Mix positively and negatively worded items within a grid (forces
  attentive reading, but use cautiously — reverse-coded items have
  their own problems)
- Use individual items (Radio/Slider) instead of grids when the item
  count is small (under 5)

**Detection in data:**
- Zero variance across a grid's responses for a respondent
- Completion time below 2 seconds per grid row
- Pattern matches (all 1s, all 3s, alternating patterns)

## Speeding

Speeding (rushing through questions) indicates low engagement. Normal
response times vary by question type:

| Question Type | Expected Time | Speeder Threshold |
|---------------|---------------|-------------------|
| Yes/No (Switch) | 8-15 seconds | < 3 seconds |
| Single-select (Radio, 4-5 options) | 12-20 seconds | < 5 seconds |
| Rating scale (Slider) | 10-18 seconds | < 4 seconds |
| Numeric input (Number) | 12-20 seconds | < 5 seconds |
| Matrix row | 6-12 seconds/row | < 2 seconds/row |
| Open-ended text | 30-90 seconds | < 10 seconds |

These are rough benchmarks. Actual times depend on question complexity,
response option count, and respondent characteristics.

**Page-level speeding** (all items on a page answered too fast) is
more reliable than item-level speeding for identifying disengaged
respondents.

## Attention Checks

Attention checks verify that respondents are reading questions carefully.
Use sparingly — they can annoy attentive respondents.

**Types of attention checks:**

1. **Instructed response**: "Please select 'Strongly agree' for this
   item." Placed within a grid. Detects anyone not reading items.

2. **Consistency checks**: Ask the same question twice with different
   wording. Large discrepancies indicate inattention.

3. **Open-ended verification**: "In one word, what is this survey
   about?" Detects respondents who aren't processing content.

**Placement guidelines:**
- Place the first attention check at approximately the 1/3 point
- Place a second at the 2/3 point if the survey is long
- Never place more than 2-3 in a survey (they waste engaged
  respondents' time and can seem insulting)
- Don't place them at the very beginning (respondents are still engaged)
  or very end (too late to use the data)

## Designing for Quality in Long Surveys

When the instrument must be long, combine multiple strategies:

1. **Adaptive routing** (most impactful): ensure each respondent only
   sees relevant questions. Target 15-20 minutes of actual questions.

2. **Format variety**: alternate between question types (Switch, Radio,
   Slider, Number) to prevent monotony. Never stack more than 2
   matrix/grid questions consecutively.

3. **Engagement anchors**: place interesting or personally relevant
   questions at the 1/3 and 2/3 points to re-engage fatigued
   respondents.

4. **Progress indicators**: showing completion percentage helps
   respondents pace themselves and reduces abandonment.

5. **Section introductions**: brief (1-2 sentence) topic introductions
   between blocks help respondents mentally transition and re-engage.

6. **Front-load importance**: place the questions most critical to your
   research in the first half, before fatigue sets in.

7. **Save demographics for last**: simple factual questions (age,
   education, income) tolerate fatigue well and serve as a cool-down.
