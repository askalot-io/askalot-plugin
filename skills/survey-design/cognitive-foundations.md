# Cognitive Foundations of Survey Response

How respondents process and answer survey questions. Based on
Tourangeau, Rips & Rasinski's cognitive model and Krosnick's
satisficing framework. Understanding these processes helps design
questions that produce accurate, reliable data.

## The Four-Stage Response Model

Every survey question triggers a four-stage cognitive process:

### Stage 1: Comprehension

The respondent interprets what the question is asking.

**What can go wrong:**
- Ambiguous terms ("regular exercise" — what counts?)
- Technical jargon the respondent doesn't know
- Complex sentence structure that obscures the question
- Mismatch between intended and perceived meaning

**Design implications:**
- Use simple, concrete language
- Define terms when precision matters
- Keep questions short — one idea per question
- Pilot test with target population to catch misinterpretations

### Stage 2: Retrieval

The respondent searches memory for relevant information.

**What can go wrong:**
- Recall failure for infrequent or distant events
- Telescoping: events seem more recent (forward) or more distant
  (backward) than they actually were
- Incomplete retrieval: respondent recalls some but not all instances

**Design implications:**
- Use bounded time frames ("in the past 7 days" vs. "recently")
- Shorter reference periods for frequent events, longer for rare events
- Provide memory cues when appropriate ("including visits to urgent
  care, emergency rooms, and telehealth appointments")
- Use recognition (lists of options) rather than recall (open-ended)
  for factual questions where feasible

### Stage 3: Judgment

The respondent evaluates retrieved information to form an answer.

**What can go wrong:**
- Estimation errors when exact answers aren't available
- Anchoring on numbers from earlier questions
- Heuristic shortcuts (rounding, averaging, guessing)
- Social desirability bias (adjusting answers to look good)

**Design implications:**
- Accept ranges or categories when exact numbers are unrealistic
  ("0-2 times, 3-5 times, 6+ times" vs. exact count for a year)
- Separate questions on related numeric topics to reduce anchoring
- Place sensitive questions later when rapport is established
- Use indirect question formats for sensitive topics when appropriate

### Stage 4: Response

The respondent maps their judgment onto the available answer options.

**What can go wrong:**
- No option matches the respondent's answer (non-exhaustive categories)
- Multiple options match (non-exclusive categories)
- Scale meaning is unclear (what does "3 out of 5" mean?)
- Satisficing: selecting first acceptable option instead of best one

**Design implications:**
- Provide exhaustive, mutually exclusive response categories
- Label every scale point with words, not just endpoints
- Match response format to the question construct (frequency questions
  get frequency scales, not agreement scales)
- Include "Not applicable" / "Don't know" when appropriate

## Context Effects

Earlier questions influence how respondents interpret and answer later
questions. These effects are systematic and predictable.

### Assimilation

Related questions make answers more similar. After answering several
questions about crime, a general "how safe do you feel?" question
produces lower safety ratings because crime is top-of-mind.

**When it occurs:** When the earlier question activates information
that feels relevant to the later question.

**Mitigation:** Place general questions BEFORE specific ones on the
same topic. Ask "How satisfied are you with your life overall?" before
asking about specific life domains (work, relationships, health).

### Contrast

Sometimes earlier questions make answers more different. After
rating their satisfaction with an exceptionally good marriage, a
respondent may rate their job satisfaction lower by comparison.

**When it occurs:** When the earlier question sets a high or low
reference point that makes the current topic look different by
comparison.

**Mitigation:** Separate strongly valenced questions from related
topics. Use buffer questions or section breaks between them.

### Priming and Anchoring

**Priming**: Earlier questions make certain concepts more mentally
accessible. Asking about environmental problems before asking about
government spending priorities increases the proportion naming
environment as a top priority.

**Anchoring**: A specific number in one question becomes a reference
point. Asking "Do you think the average family spends more or less
than $500 per month on groceries?" biases the next question about
the respondent's own grocery spending toward $500.

**Mitigation:**
- Be aware of what concepts earlier questions activate
- Vary question topics to avoid sustained priming on one theme
- Don't provide specific numbers before asking respondents to estimate
- Use section breaks and topic transitions as cognitive "resets"

### Carryover and Consistency

Respondents try to appear consistent with their previous answers.
After saying they support environmental protection, they are more
likely to support specific environmental policies in later questions.

**Mitigation:** When measuring attitudes on related topics, consider
whether earlier answers are contaminating later ones. Block
randomization (varying block order across respondents) can help
distinguish true attitudes from consistency effects.

## Cognitive Load and Question Difficulty

The total cognitive load of a question depends on all four stages.
High-load questions deplete respondent energy and increase satisficing
on subsequent questions.

**High cognitive load:**
- Long question stems with multiple clauses
- Abstract or hypothetical scenarios
- Large response grids (many rows and columns)
- Questions requiring calculation or estimation
- Unfamiliar topics requiring new mental models

**Low cognitive load:**
- Short, concrete questions about familiar topics
- Binary choices (yes/no)
- Simple ratings on clearly labeled scales
- Factual questions with obvious answers

**Design principle:** Alternate high-load and low-load questions.
Never stack multiple high-load questions in sequence. After a complex
grid or estimation question, follow with simple factual questions
to let the respondent recover.

## Implications for Adaptive Survey Design

These cognitive foundations directly inform large-survey design:

1. **Screening questions should be low-load** (Stage 1-2 easy):
   Binary, concrete, about familiar personal facts. This keeps the
   routing efficient and accurate.

2. **Place complex questions early in each module** (before fatigue):
   When a respondent enters a new topic module, they have a brief
   engagement boost from the novelty. Use it for the hardest questions.

3. **Routing reduces total cognitive load**: Every irrelevant question
   skipped is not just time saved — it preserves cognitive resources
   for relevant questions. Adaptive routing improves data quality
   even if total time is held constant.

4. **Context effects cross module boundaries**: Even with adaptive
   routing, the universal screening block primes certain topics. Be
   aware that screening questions about health may influence health
   module responses.

5. **Format variety counters habituation**: Varying question types
   (Switch, Radio, Slider, Number) across modules forces respondents
   to re-engage with each question rather than falling into patterns.
