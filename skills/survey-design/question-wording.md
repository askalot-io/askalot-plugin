# Question Wording Principles

Evidence-based rules for writing clear, unambiguous survey questions that reduce cognitive burden and misinterpretation.

## Conventional Wisdom: 8 Core Rules

### 1. Use Simple Language

Avoid jargon, abbreviations, technical terms, and low-frequency words unless the target audience routinely uses them. If technical terms are necessary, provide explicit definitions in the question text or introduce them in preceding screening questions.

- BAD: "What is your BMI?" (most respondents don't know this term)
- GOOD: "What is your approximate height and weight?" (calculate BMI later via codeBlock)
- BAD: "Do you use SSRIs?" (unclear to non-medically trained respondents)
- GOOD: "Do you take any antidepressant medications?"

**Why**: Simple language reduces cognitive load. Complex or unfamiliar words force respondents into "satisficing" mode (choosing answers without full comprehension) and increase unreliable data.

### 2. Use Simple Syntax

Avoid complex sentence structures, multiple clauses, and embedded modifiers. Keep sentences short (under 20 words when possible) and avoid phrases that require parsing multiple concepts before answering.

- BAD: "Considering the range of services available to you at the community center, including but not limited to fitness classes, recreational programs, and family activities, how frequently do you utilize these facilities?"
- GOOD: "How often do you visit the community center?" (follow-up: "What do you usually do there?")

**Why**: Complex syntax increases working memory demands and comprehension errors. Shorter sentences reduce errors by 20-30%.

### 3. Avoid Ambiguity

Words with multiple meanings (ambiguous reference), vague noun phrases, and unclear antecedents create different interpretations across respondents.

- BAD: "How often does the family visit relatives?" (unclear: which family members? whose relatives?)
- GOOD: "How often do you visit your parents, siblings, or extended family members?"

- BAD: "Do you think the government is doing a good job?" (good at what? which government level?)
- GOOD: "How would you rate the job the federal government is doing on managing the economy?"

**Detection**: Search for pronouns without clear antecedents (it, they, this, that), undefined scope ("the family," "the community"), and domain-specific terms with layered meanings.

### 4. Be Specific and Concrete

Specify time frames, reference periods, units of measurement, and concrete examples. Vague quantifiers ("regularly," "often," "a lot," "usually") produce highly unreliable data with 30-50% coefficient of variation.

- BAD: "Do you exercise regularly?" (respondents define "regularly" differently)
- GOOD: "In a typical week, how many days do you exercise for at least 30 minutes?"

- BAD: "How much do you spend on entertainment?" (unclear: per month? per year? what counts?)
- GOOD: "In the past 7 days, approximately how much did you spend on movies, concerts, or entertainment events? (Please include tickets, not food or parking)"

**Specificity benefits**: Frequency estimates become 40-60% more accurate. Time frame precision reduces errors in recall.

**Reference periods**: Bounded recall (past 7 days, past month) is more accurate than unbounded (lifetime). Days 1-7 recall error: ~10%; Days 8-30: ~20%; Days 31+: ~40%+ error.

### 5. Ensure Exhaustive Response Categories

Closed questions must offer response options that cover all possible answers. Missing categories force respondents to select "Other" or pick wrong categories.

- BAD: "What is your employment status?" with options: [Full-time, Part-time, Retired] (missing: student, homemaker, looking for work, unable to work)
- GOOD: Provide complete list: [Full-time, Part-time, Self-employed, Retired, Student, Homemaker, Looking for work, Unable to work, Other ___]

If closed categories are incomplete, always include "Other (please specify)" with a text field.

### 6. Avoid Leading Questions

Questions that suggest a desired answer or make assumptions about the respondent's views reduce data reliability and introduce acquiescence bias. Leading questions have built-in pressure toward agreement.

- BAD: "Most people believe that privacy is important. Do you agree?" (suggests "yes" is the right answer)
- GOOD: "How important is privacy to you?" with options [Very important, Somewhat important, Not very important, Not at all important]

- BAD: "Don't you think traffic congestion is a serious problem?" (the "don't" creates negative expectancy)
- GOOD: "How serious a problem is traffic congestion in your area?"

**Acquiescence bias**: When questions suggest agreement, 10-15% more respondents agree than would with neutral wording.

### 7. Ask Single Questions, Not Double-Barreled

Each question must ask about ONE concept only. Combining two or more ideas prevents accurate responses — respondents with mixed opinions cannot answer truthfully.

- BAD: "How satisfied are you with the price and quality of this product?" (respondent might like price but hate quality, or vice versa)
- GOOD: Ask as two separate items:
  - "How satisfied are you with the price of this product?"
  - "How satisfied are you with the quality of this product?"

- BAD: "Do you read books and magazines?" (someone reads books but not magazines cannot answer accurately)
- GOOD:
  - "Do you read books?"
  - "Do you read magazines?"

**Detection**: Look for "and," "or," "as well as" in the question stem — these often signal compound questions. If you can logically answer "yes" to one part and "no" to another, split it.

### 8. Avoid Double Negatives

Never require respondents to agree with a negative statement to express a positive position. Double negatives force extra cognitive processing and produce errors.

- BAD: "Do you disagree that schools should not reduce funding?" (requires parsing: disagree + not reduce = support maintaining funding — cognitively complex)
- GOOD: "Do you think schools should maintain their current level of funding?"

- BAD: "It is not unusual for me to feel anxious." (double negative: "not unusual" = "usual")
- GOOD: "I often feel anxious."

## Psycholinguistic Text Features Increasing Cognitive Burden

Seven measurable text features increase cognitive load and reduce data quality. Each feature correlates with longer response times and higher item nonresponse.

### 1. Low-Frequency Words

Words that appear rarely in everyday English force respondents to slow down, retrieve definitions from memory, or guess at meaning.

- BAD: "Do you ruminate about your fiscal exigencies?" (ruminate, exigencies are low-frequency)
- GOOD: "Do you worry about your money?"

**Indicator**: Words in bottom 10th percentile of English frequency (e.g., "acquiesce," "endeavor," "manifold," "propitious," "sequester")

### 2. Vague or Imprecise Relative Terms

Adjectives and adverbs without objective referents ("somewhat," "fairly," "rather," "quite," "considerably") create different interpretations across respondents. These words lack frequency anchors.

- BAD: "Do you feel fairly anxious about your job?" (what does "fairly" mean? 5 out of 10? 6 out of 10?)
- GOOD: "How often do you feel anxious about your job?" with response options [Daily, Several times a week, About once a week, A few times a month, Never]

**Examples of vague terms**: fairly, somewhat, rather, quite, considerably, moderately, slightly, reasonably, relatively

### 3. Vague or Ambiguous Noun Phrases

Nouns without clear scope or with multiple possible referents create interpretation divergence.

- BAD: "How do you feel about the government's policies?" (which government? federal, state, local? which policies? fiscal, environmental, social?)
- GOOD: "How do you feel about the federal government's environmental policies?" or break into separate questions

- BAD: "How often do you exercise?" (does "exercise" include walking, housework, or only structured activity?)
- GOOD: "How often do you do physical exercise such as jogging, aerobics, or sports?" with explicit examples

### 4. Complex Syntax

Multiple clauses, embedded modifiers, passive voice, and non-standard word order increase working memory demands.

- BAD: "Having considered the various recreational opportunities that are available, which activities would you, if given the opportunity to choose, prefer?"
- GOOD: "What recreational activity would you most like to do?"

- BAD: "By whom are you currently employed?" (passive voice, inverted subject-object order)
- GOOD: "Who is your current employer?" or "What company do you work for?"

**Syntax complexity markers**: Multiple subordinate clauses (more than 2), passive voice constructions, subject-verb separation > 8 words

### 5. Working Memory Overload

Questions that require respondents to hold multiple pieces of information in mind simultaneously (e.g., comparing across time periods, comparing multiple dimensions) overload working memory.

- BAD: "Compared to five years ago, how has your overall satisfaction with your job changed in terms of salary, benefits, and job security?" (requires holding: current satisfaction, past satisfaction, three dimensions)
- GOOD: First: "How satisfied are you with your current job?" Then: "Compared to five years ago, is your job more satisfying, less satisfying, or about the same?"

**Overload indicators**: Questions combining temporal comparison + multiple dimensions, questions requiring mental math or complex comparisons

### 6. Low Syntactic Redundancy

Repetition of key grammatical structures (parallel construction) aids comprehension. Questions that vary structure unnecessarily increase processing load.

- BAD: "How satisfied are you with your pay, the benefits provided, and your ability to advance?" (satisfaction + three different noun structures: pay, benefits provided, ability to advance)
- GOOD: "How satisfied are you with: your pay, your benefits, and your advancement opportunities?" (parallel structure throughout)

- BAD: "Do you watch television, read books, or enjoy playing sports?" (three different verbs: watch, read, enjoy)
- GOOD: "Do you engage in these activities: watching television, reading books, playing sports?"

### 7. Bridging Inferences

Questions that require respondents to generate bridging inferences (unstated logical connections) increase cognitive load. The question assumes background knowledge the respondent may not have.

- BAD: "How accurate is your assessment of the organization's effectiveness?" (requires knowledge of what "effectiveness" means in context; requires belief that one CAN assess organizational effectiveness)
- GOOD: "To what extent do you agree with this statement: 'Our organization is achieving its stated goals'?" (explicit and bounded)

- BAD: "Do you support free trade?" (requires knowledge of what "free trade" means, its effects, current policies)
- GOOD: "Do you support reducing tariffs on imported goods?" (concrete policy, not abstract concept)

**Indicator**: Questions asking about concepts without concrete examples or situations defined

## Psychometric Effects and Response Quality

### Satisficing vs. Optimizing

**Optimizers** use full cognitive effort: they interpret the question carefully, retrieve relevant information, evaluate all response options, and select the best answer.

**Satisficers** use minimal effort: they use the first acceptable answer, don't retrieve detailed information, use mental shortcuts, and are susceptible to response order effects.

**Conditions triggering satisficing** (and reducing data quality by 20-40%):
- Questions requiring high cognitive effort (long, complex, ambiguous)
- Respondents with limited cognitive ability or motivation (age 65+, low education, survey fatigue)
- Survey context (long questionnaire, time pressure, boring topic)
- High number of response options (7+ points increases satisficing; 5-point scales optimal)

**Prevention**:
- Simplify question wording
- Reduce response option number to 5-7 points
- Reduce questionnaire length or break into multiple sessions
- Use engaging introductions and progress indicators

### Response Order Effects

The order of response options influences choice distribution, especially with longer lists and for respondents using satisficing strategies.

**Primacy effect** (first options more likely): Occurs with lists of 5+ options, self-administered surveys (web, mail)

**Recency effect** (last options more likely): Occurs with short lists, oral interviews

**Magnitude**: Order effects can shift response distributions by 5-15% depending on option number and survey mode.

**Mitigation**:
- Randomize response order in web surveys (different randomization per respondent)
- For fixed-order lists (demographics), don't randomize
- Use balanced lists where all options are equally desirable
- Keep option number at 4-7 (avoid 2-3 option lists with strong order bias)

### Acquiescence Bias (Yea-Saying)

Respondents tend to agree with yes/no questions at rates 10-15% higher than logically implied by the opinion distribution. This bias is stronger for:
- Older respondents
- Lower education levels
- Respondents in phone interviews
- Positive-framed items vs. negative-framed items

**Mitigation**:
- Use agree/disagree scales (not yes/no)
- Use balanced item sets (mix positive and negative frames — but NOT double negatives)
- Validate with behavioral items or objective questions
- Use balanced response scales with neutral midpoint

## Recall and Reference Period Guidelines

### Bounded Recall Strategy

Limit recall to a specific, recent time period. Accuracy declines sharply beyond the specified horizon:

- **Past 7 days**: ~10% error (most reliable for frequency data)
- **Past 30 days**: ~20% error
- **Past 3 months**: ~30% error
- **Past 1 year**: ~40% error
- **Lifetime/5+ years**: 50%+ error, unreliable

**Recommendation**: Use past 7 days or past month for frequency behavior questions; use past 3-6 months for healthcare/medical events; use past year for rare events.

### Landmarks Strategy

Anchor recall to significant events or time markers to reduce memory errors:

- BAD: "How many times did you visit a doctor in the past year?"
- GOOD: "How many times did you visit a doctor since [holiday/event reference date]?" or "In 2024, how many times did you visit a doctor?"

### Decomposition Strategy

Break complex behaviors into specific components rather than asking for totals:

- BAD: "How much do you spend on health and personal care?" (respondent must calculate across many categories)
- GOOD: "In the past month:
  - How much did you spend on prescriptions?
  - How much on over-the-counter medications?
  - How much on dental care?
  - How much on haircuts or grooming?"

(Then sum responses for analysis if needed)

## Detecting Problematic Question Types

### Double-Barreled Questions

**Detection patterns**:
- Multiple concepts connected by "and," "or," "as well as"
- Different concepts with logically independent answers
- Question admitting "yes to part, no to part" responses

**Test**: "Can someone logically answer yes to one part and no to another?" If yes, it's double-barreled.

### Leading Questions

**Detection patterns**:
- Opening with "Doesn't it seem..." or "Don't you think..."
- Statements followed by "Do you agree?"
- Use of loaded adjectives ("obviously," "surely," "terrible," "wonderful")
- Questions presupposing agreement or knowledge
- Questions attributing opinions to majorities ("Most people believe...")

**Test**: Would neutral wording substantially change the distribution of answers? If yes, it's leading.

### Loaded Questions

**Detection patterns**:
- Emotionally charged language ("horrific," "disgusting," "brilliant," "utopian")
- Implicit evaluation ("wasteful government spending" vs. "government spending")
- Attributing negative motives ("Do you support allowing corporations to pollute?" vs. "environmental policies")

**Test**: Would replacing emotionally laden words with neutral language change expected responses? If yes, it's loaded.

## Response Task Organization

Organize the question stem so the core question comes first, with context and clarifying instructions after:

- BAD: "Considering that many factors influence satisfaction, including price, quality, service, and availability, how would you rate your satisfaction with this product?"
- GOOD: "How satisfied are you with this product?" [If rating scale] "Consider: price, quality, service, and availability."

**Principle**: Respondents process the first words of a question first; lead with the core question, not with context or qualifiers.

## Conventional Wisdom Summary Table

| Principle | Error | Mitigation | Impact |
|-----------|-------|-----------|--------|
| Simple language | 20-30% comprehension error | Avoid low-frequency words, define jargon | Data quality +20-30% |
| Simple syntax | 15-25% parsing errors | Keep < 20 words, avoid embedded clauses | Error reduction 15-25% |
| Unambiguous | 30-50% interpretation divergence | Define scope, avoid pronouns without antecedents | Reliability +30-50% |
| Specific time frame | 20-40% recall error | Use bounded recall (7-30 days), landmarks | Accuracy +20-40% |
| Exhaustive categories | Loss of valid responses | Complete list + "Other" option | Response validity +15-25% |
| No leading language | 10-15% acquiescence bias | Neutral framing, balanced agree/disagree | Bias reduction 10-15% |
| Single concept | Loss of usable data | Split compound questions | Data utility +25-40% |
| No double negatives | 15-20% comprehension error | Positive frames, avoid negation | Accuracy +15-20% |
