# Response Categories Principles

Rules for designing answer options for closed-ended questions.

## Exhaustive Categories

Every answer list must include ALL reasonable possible answers. Missing
categories force respondents into inaccurate answers.

- Add "Other (please specify)" with a comment field when the list may not
  cover all cases.
- Always include "Not applicable" or "Does not apply" when the question
  may not apply despite passing preconditions.

## Mutually Exclusive Categories

Categories must not overlap. Respondents should never have to choose
between two options that both describe their situation.

- BAD: age ranges "25-35" and "35-45" (overlap at 35)
- GOOD: "25-34" and "35-44"

This applies to both single-answer and multiple-answer questions.

## Forced-Choice Over Check-All-That-Apply

Use separate yes/no forced-choice items instead of "check all that apply"
lists. Forced-choice format:
- Produces more accurate data (respondents evaluate each option individually)
- Reduces satisficing (respondents don't stop after checking a few)
- Transfers better across survey modes

In QML: use individual Switch items with Yes/No options instead of a single
Checkbox group. Gate follow-up questions on these with preconditions.

## Ranking Questions

When asking respondents to rank items, limit to 3-5 items maximum.
Longer ranking lists become cognitively overwhelming.

## Avoid Unequal Comparisons

All response options should carry equal weight and specificity. Don't
mix specific options with vague ones.

- BAD: "personal irresponsibility" vs. "economic conditions, poverty, and lack of jobs"
  (the second option bundles three concepts and is more sympathetic)
- GOOD: Break into balanced, parallel options of similar length and specificity.

## Randomize When Order Matters

If response option order might bias results (primacy/recency effects),
consider randomizing the display order. This is especially important for
nominal categorical questions where no natural ordering exists.

## "Not Sure" / "Don't Know" Placement

Place nonsubstantive options ("Not sure", "Don't know", "No opinion")
at the END of the response list, visually separated from substantive
options. Never place them in the middle of an ordinal scale.

## When to Offer "Don't Know" / "Not Applicable"

Including a "Don't Know" (DK) or "Not Applicable" (NA) option is a
design trade-off:

**Offer DK/NA when:**
- The question may genuinely not apply despite passing preconditions
  (e.g., "How satisfied are you with your commute?" for someone who
  works from home some days)
- The respondent may lack the knowledge to answer (factual questions
  about unfamiliar topics)
- Forcing an answer would produce meaningless data

**Omit DK/NA when:**
- The question is about the respondent's own behavior or opinion
  (everyone has an opinion, even if weak)
- You have proper preconditions ensuring the question applies
- DK would become a satisficing escape route (respondents select it
  to avoid thinking)

**Design guidelines:**
- Label it clearly: "Don't know" for knowledge gaps, "Does not apply"
  for inapplicable questions, "Prefer not to say" for sensitive topics
- Visually separate from substantive options (spacing or divider)
- In QML: include as the last option. For analysis, DK/NA responses
  are typically treated as missing data, not as a substantive category

## Open-Ended Response Guidance

Open-ended questions (free text) are powerful but expensive in
respondent time and analysis effort.

**When to use open-ended:**
- Exploratory research where you don't know the response space
- "Other (please specify)" as a catch-all after closed options
- Capturing verbatim quotes or narratives
- Questions where pre-defined categories would bias responses

**When to avoid:**
- When closed-ended alternatives exist and cover the response space
- Late in long surveys (fatigue produces low-quality open-ended data)
- When you lack resources to code/analyze text responses

**Design tips:**
- Provide a clear prompt: "In 1-2 sentences, describe..." rather
  than just a text box
- Set expectations for length: "briefly describe" vs. "please explain
  in detail"
- In long surveys, limit to 1-2 open-ended questions maximum
- Place open-ended questions in the first half where engagement is
  higher
