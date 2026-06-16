# Question Ordering Principles

Rules for sequencing questions within and across blocks.

## Group Related Questions Together

Organize the questionnaire like a conversation. Group questions covering
the same topic together in a block before moving to the next topic.
Jumping between unrelated topics confuses respondents and increases
cognitive burden.

In QML: use thematic blocks (3-8 blocks per questionnaire). Each block
should cover a coherent topic area.

## Start With Salient, Easy Questions

Begin with questions that are:
- Interesting and clearly relevant to the survey topic
- Easy to answer (not sensitive or complex)
- Applicable to ALL respondents (no filtering needed)

The first questions set expectations. If they seem irrelevant, boring,
or threatening, respondents disengage or abandon the survey.

NEVER start with demographics. Start with the survey's main topic.

## Place Sensitive Questions Late

Sensitive or potentially objectionable questions (income, health behaviors,
political opinions, illegal activities) should appear near the END of the
questionnaire. By then, respondents have invested effort and built rapport
with the survey instrument.

## Filter Questions Before Follow-Ups (Anti-Interleaving)

When using screening/filter questions with follow-ups, ask ALL filter
questions first, then ask ALL follow-up questions.

- BAD (interleaved):
  1. "Do you own a car?" → "What make is your car?"
  2. "Do you own a bicycle?" → "How often do you ride?"

- GOOD (grouped filters, then follow-ups):
  1. "Do you own a car?"
  2. "Do you own a bicycle?"
  3. "What make is your car?" (precondition: owns car)
  4. "How often do you ride your bicycle?" (precondition: owns bicycle)

Interleaving creates a choppy experience where respondents repeatedly
answer "Does not apply" for follow-ups to items they answered "No" to.
Grouping filters lets respondents move through screening quickly, then
only see relevant follow-ups.

In QML: place all Switch/Radio screening items early in the block,
then place preconditioned follow-up items after.

## Chronological Order for Events

When asking about events or processes, order questions chronologically.
People find it easier to recall events in the order they occurred.

## Avoid Unintended Order Effects

Be aware of how prior questions influence later ones:

- **Priming**: Earlier questions make certain information more accessible,
  biasing responses to later questions.
- **Anchoring**: A specific number in one question becomes a reference
  point for subsequent numeric questions.
- **Subtraction**: Respondents exclude topics already covered, narrowing
  their interpretation of later general questions.
- **Carryover/consistency**: Respondents try to appear consistent with
  their earlier answers.

Mitigation strategies:
- Place general questions BEFORE specific ones when both are on the same
  topic (to avoid subtraction)
- Vary question types and response formats to break response patterns
- Use block-level randomization when topic order doesn't matter

## Fatigue-Aware Ordering

In long surveys (50+ items per respondent), question placement directly
affects response quality. Later questions consistently receive less
thoughtful answers.

### Cognitive Load Distribution

Alternate between high-effort and low-effort questions. Never stack
more than 2-3 demanding questions in sequence.

**High effort**: matrix/grid questions, open-ended text, hypothetical
scenarios, estimation tasks, questions requiring calculation.

**Low effort**: yes/no switches, simple single-select, familiar factual
questions (demographics), numeric inputs with obvious answers.

After a complex grid or estimation question, follow with 1-2 simple
items before the next demanding question.

### Engagement Curve

Respondent engagement follows a predictable pattern:
- **First third**: highest engagement, most careful responses
- **Middle third**: gradual decline, some satisficing begins
- **Last third**: lowest quality, most satisficing and speedin

**Placement strategy by priority:**
1. Most important research questions → first third
2. Questions requiring careful judgment → first half
3. Standard topic questions → middle
4. Simple factual/demographic questions → last third
5. Validation and consistency checks → throughout

### Grid and Matrix Spacing

Matrix/grid questions are the highest fatigue risk. They require
sustained attention across multiple rows of similar items.

Rules:
- **Maximum 5-7 rows per grid** (break longer batteries into parts)
- **Never stack grids**: place at least 2-3 non-grid items between
  consecutive grids
- **Vary grid formats**: alternate the response scale or topic between
  grids to prevent pattern responding
- **Place grids in the first half** when possible — they tolerate
  fatigue poorly

### Mobile-Aware Ordering

On mobile devices, grids are harder to complete and fatigue sets in
faster. When the survey may be taken on mobile:
- Use individual items instead of grids when feasible
- Place any remaining grids earlier in the survey
- Keep grid rows under 5 for mobile
- Prefer vertical layouts (Radio) over horizontal layouts (Slider)
  for small screens

## Context Effect Management

### Buffer Questions

When two questions might contaminate each other through priming or
contrast effects, place 2-3 unrelated questions between them.

Example: questions about personal health and questions about healthcare
policy should not be adjacent. The personal health questions prime
healthcare-related thinking that biases policy opinions.

### Priming Avoidance

Don't ask knowledge/awareness questions immediately before attitude
questions on the same topic. The knowledge question activates specific
information that biases the attitude response.

- BAD: "Are you aware of the city's recycling program?" immediately
  followed by "How important is recycling to you?"
- BETTER: Place 3-4 unrelated questions between awareness and attitude,
  or place them in separate blocks
