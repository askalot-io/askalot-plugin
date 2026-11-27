# Standard Response Scales

Verbatim label sets for rating questions, with the polarity and length each
one usually takes. Read this before writing the labels of any rating item.

**You decide what the item measures first.** An item measures an opinion, a
feeling, a behaviour, an evaluation or an intention. That decision is yours
(the Designer's), and nothing in QML states it or checks it. Once it is made,
take the polarity, the length and the labels from this file. Do not invent a
label ladder.

**How the sets are written.**

- Every set runs from the lowest code to the highest: from the negative or
  low end to the positive or high end. Copy the labels in that order into
  `input.labels`.
- Codes start at 1 unless the entry says **start 0**. An instrument published
  on 0 to N keeps its codes: declare `start: 0`, so the stored answer is the
  published score.
- On a unipolar scale the high end means "more of the thing". On frequency,
  concern, severity, pain and symptom scales the highest code is the most
  frequent or most severe answer, not the desirable one.
- "Ends only" means the instrument labels only its two end points. QML needs a
  label for every point, so write the number itself on the points between
  (`3: "3"`) and the number with its anchor on the two ends
  (`0: "0 - Not at all likely"`).
- The labels are English. A questionnaire in another language gets its labels
  from the translation agent, per questionnaire (`translate-questionnaire`
  skill); no skill holds translated label sets.
- Clinical and other validated instruments (section Q, NPS, the Cantril
  ladder, Juster) are used verbatim: same wording, same length, same order.
- Each set names its source in brackets. A length that is not listed for a
  construct has no standard wording in these sources: use the nearest listed
  length.

The QML declaration is in `qml-syntax` §4.10. In short:

```yaml
- id: q_delivery
  kind: Question
  title: "How satisfied are you with the delivery?"
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

## 1. What Am I Measuring, Which Scale

| What the question is about | Scale | Polarity | Usual length | Entry |
|---|---|---|---|---|
| An opinion on a statement (a battery of statements, or a validated instrument) | Agree/disagree | bipolar | 5 or 7 | A1 |
| A position for or against a policy, proposal or object | Favor/oppose, favorable/unfavorable, acceptable | bipolar | 4, 5 or 7 | A2, A3 |
| A feeling of contentment with something experienced | Satisfaction | bipolar (classic) or unipolar | 5 or 7 bipolar, 5 unipolar | B1, B2, B3 |
| How good something is | Quality | unipolar (poor to excellent) or bipolar (very bad to very good) | 4 or 5 | C1, C2 |
| How often a behaviour happens, roughly | Verbal frequency | unipolar | 5 | D1 |
| How often, when the rate matters | Calendar frequency, or a count in an Editbox | unipolar | 5 to 7 | D2 |
| A future behaviour or intention | Likelihood, purchase intent, Juster probability | unipolar or bipolar | 4, 5 or 11 | E1 to E4 |
| How much something matters | Importance | unipolar | 4 or 5 | F1 |
| How much, to what extent, how X | "Not at all X" to "Extremely X" | unipolar | 5 | G1, G2 |
| The effort or ease of a task | Difficult/easy | bipolar | 5 or 7 | H1, H2 |
| A comparison with something else, or with expectations | Worse/better, expectations | bipolar | 5 (4 for expectations) | I1, I2 |
| How true a description is | True/untrue, "like me" | bipolar or unipolar | 6 or 7 | J1, J2 |
| Knowledge of or exposure to something | Familiarity, awareness, interest | unipolar | 5 | K1 |
| Worry, concern, how serious a problem is | Concern, worry, problem | unipolar | 4 or 5 | L1, L2 |
| Urgency | Priority | unipolar | 5 | M1 |
| Change over time | Worse/better | bipolar | 5 | N1 |
| Trust or confidence | "Not at all" to "A great deal" | unipolar | 4, 5 or 11 | O1 |
| Overall wellbeing, recommendation, pain: one numeric item | End-labelled 0 to 10 | see entry | 11 | P1 to P5 |
| Clinical symptom frequency in a recall window | The instrument's own scale, unaltered | unipolar | 3 to 6 | Q1 to Q5 |
| Connotative meaning of a concept | Semantic differential | bipolar | 7 | R1 |

Rules of thumb:

1. Ask about the thing itself. When an item can be rephrased as a direct
   question, an item-specific scale is better than a statement to agree with:
   "The facilitator was knowledgeable" becomes "How knowledgeable was the
   facilitator?" on "Not at all knowledgeable" to "Extremely knowledgeable".
2. A **behaviour** gets a frequency scale or a count, never agreement. An
   **evaluation** gets a quality scale. A **feeling** gets satisfaction or an
   intensity scale. An **intention** gets likelihood or probability. An
   **opinion** on a statement gets agreement.
3. A construct with a true opposite and a meaningful neutral point (agree and
   disagree, favor and oppose, easier and harder, better and worse) is
   **bipolar**. One that runs from none to a lot of one thing (importance,
   frequency, concern, familiarity) is **unipolar**.

## 2. Out-of-Scale Answers

"Don't know", "Does not apply" and the like are not points on the scale. In
QML they are labels whose codes are above the scale's range: on a five-point
scale coded 1 to 5, any label at 6 or higher. You choose the code and the
wording. Use one code per meaning throughout a questionnaire (a common habit
is 97, 98, 99; a single digit such as 8 or 9 works as well).

They are shown after the last scale point, set apart from the points, never
in the middle. Such an answer counts as answered, and is treated as missing
in every quality measure, reliability figure, scale score and statistical
export.

| Option | Offer it when | Do not offer it when |
|---|---|---|
| Don't know | Knowledge questions; evaluations of things the respondent may never have met; low-salience topics | Attitude questions where every respondent can form a view: it attracts satisficers and people with real but weak opinions (Krosnick & Presser) |
| No opinion | Attitude items about obscure issues | The same caution as "Don't know"; never as the midpoint |
| Not applicable / Does not apply | The item presupposes an experience not everyone has. Prefer a precondition that skips the item when the questionnaire already knows | Everyone is eligible |
| Did not use / Have not used / No experience | Batteries rating several services or features; more informative than a generic "Not applicable" | A single item that a precondition can skip |
| Prefer not to say / Prefer not to answer | Sensitive items (income, health, sexuality, gender, politics) | Routine attitude items: it invites nonresponse |
| Not sure / Unable to judge / Can't say | Evaluations of other people or of institutions, as a softer "Don't know" | |
| Haven't thought much about this | Self-placement items (the ANES ideology item): a "Don't know" without the stigma | |

Sources: Krosnick & Presser 2010; Pew 2023; Iowa/Qualtrics guide; Wisconsin
guide; ESS Round 11 showcards; ANES codebook.

## 3. Design Guidance

### 3.1 Bipolar or Unipolar

- A **bipolar** scale measures direction and intensity around a neutral
  point: two opposite poles, the same number of categories on each side. A
  **unipolar** scale measures the amount of one attribute from none upward
  (Krosnick et al. 2006; Wisconsin guide).
- Test: can a respondent sensibly be "neither X nor the opposite of X"? If
  yes, bipolar. If the low end is simply the absence of X, unipolar.
- Unipolar scales are easier to answer. Use one when people rate themselves
  or other people: answers bunch on the positive half of a bipolar scale, and
  a unipolar scale spreads them out (SurveyMonkey; Wisconsin guide).
- **Satisfaction can be asked either way.** The classic form is bipolar
  ("Very dissatisfied" to "Very satisfied"); it records active
  dissatisfaction and is the form most benchmarks use. The unipolar form
  ("Not at all satisfied" to "Extremely satisfied") has no ambiguous midpoint
  and differentiates more at the positive end, where most answers fall. Pick
  one form per questionnaire and never mix the two.
- **Likelihood** has the same two forms: bipolar "Very unlikely" to "Very
  likely", unipolar "Not at all likely" to "Extremely likely".

### 3.2 Number of Points

- Bipolar scales are most reliable and valid at about 7 points, unipolar
  scales at about 5 (Krosnick & Fabrigar 1997, as summarised in Krosnick et
  al. 2006). Point meanings become unclear above seven.
- Dillman, Smyth & Christian (2014): 5 or 7 for bipolar, 4 or 5 for unipolar.
- Practitioner guides default to 5 and keep one length across a
  questionnaire.
- By phone or voice, branch a 7-point bipolar scale: ask the direction first,
  then the strength (Krosnick & Berent 1993).
- 0 to 10 end-labelled scales are an established form for single global
  items (ESS, Cantril, NPS, pain): see P1 to P5.

### 3.3 Midpoint

- Only a bipolar scale has a midpoint, and it has one exactly when its point
  count is odd. An even count forces a direction.
- A midpoint lets neutral respondents answer accurately. Without one they
  pick a neighbouring point at random; offering midpoints improved
  reliability and validity (O'Muircheartaigh, Krosnick & Helic 1999). The
  cost is an easy satisficing answer; the evidence on that is mixed.
- Use an even bipolar scale only on purpose: when everyone can be expected
  to lean one way and the direction is needed from everyone.
- The middle of a unipolar scale ("Moderately", "Sometimes") is a real
  amount. Never label it "Neutral".

### 3.4 Labels

- Label every point with words up to 7 points. Fully labelled scales are more
  reliable than end-labelled ones, and the labels should divide the continuum
  into roughly equal steps (Krosnick & Presser 2010).
- Avoid near-synonyms on one scale: "rarely" with "seldom", "often" with
  "frequently", "some of the time" with "occasionally" (Rohrmann 2007).
- Very extreme end labels may go unused and shrink a five-point scale to
  three (Rohrmann 2007).
- End-labelled numeric scales are standard at 10 or 11 points, where no
  verbal label exists for every point. Juster is the exception: all 11 points
  are labelled.

### 3.5 Reverse-Worded Items

- A battery of statements may mix items keyed in both directions to cancel
  acquiescence and expose straightlining.
- The harms are known: respondents misread negated items or forget to
  reverse their answer, and researchers miscode (Sauro & Lewis 2011 found 3
  of 27 SUS datasets miscoded; an all-positive SUS showed no more
  acquiescence and slightly higher reliability). Negations are burdensome and
  error-prone (Krosnick & Presser 2010).
- Prefer removing the cause: an item-specific scale has no acquiescence to
  balance.
- When reversing, write the polar opposite without a negation ("I found the
  system cumbersome", not "I did not find the system easy").
- Keep the response scale identical for every item: same labels, same order,
  same codes. Only the stem is reversed. QML does not mark an item as
  reversed and you never store reversed codes. The analyst ticks the
  reverse-worded items in the Gold scale score, which reverses them as
  `2 * start + points - 1 - code`. Name them in the design notes.
- A validated instrument keeps its reversals (SUS items 2, 4, 6, 8 and 10).

### 3.6 Item-Specific Scales Rather Than Agree/Disagree

- Acquiescence, agreeing whatever the content, averages about 10% in the
  studies Krosnick & Presser review. It is stronger among respondents with
  less education, with harder questions and with an interviewer present.
- Answering agree/disagree means first answering the underlying rating
  question and then translating it. "I am usually pretty calm: disagree" can
  mean always calm or never calm.
- Agree/disagree answers were of much lower quality than item-specific ones
  in the experiments of Saris, Revilla, Krosnick & Shaeffer (2010).
- Agree/disagree is legitimate only for validated instruments built on it
  (SUS, CES 2.0) and for a battery of heterogeneous statements where one
  common scale is the point.

### 3.7 Display Order

- A rating scale is never randomised. It has two orders, ascending and
  descending.
- The stored codes always run from the negative or low end upward. QML shows
  the points in that order unless the item says `order: descending`, which
  shows the highest code first and changes no code.
- Descending scales (positive first) draw more positive answers; ascending
  order is the simplest remedy (Chyung, Kennedy & Campbell 2018). Some
  instruments print positive first (the ESS agree scale, WHO-5).
- Whichever you choose, keep one direction through the whole questionnaire.

### 3.8 Offering "Don't know"

Offer it for knowledge, for evaluations that need experience, and on
sensitive items. Do not offer it by default on attitude scales. Never make it
the midpoint. Always give it a code above the scale's range (section 2).

## 4. The Scales

Each set is one line: the number of points, the source in brackets, then the
labels from the lowest code to the highest, separated by `|`.

### A. Opinion and Agreement

#### A1. Agreement (Likert)

Agreement with a statement. Bipolar. Fully labelled. Offer "Don't know" or
"Not applicable" only where the statement may not apply.

- **4 points** (SurveyMonkey): Strongly disagree | Somewhat disagree | Somewhat agree | Strongly agree
- **5 points** (Iowa/Qualtrics): Strongly disagree | Disagree | Neither agree nor disagree | Agree | Strongly agree
- **5 points** (ESS): Disagree strongly | Disagree | Neither agree nor disagree | Agree | Agree strongly
- **5 points** (Wisconsin): Strongly disagree | Moderately disagree | Neither agree nor disagree | Moderately agree | Strongly agree
- **5 points** (Rohrmann, equidistant): Fully disagree | Mainly disagree | Neutral | Mainly agree | Fully agree
- **7 points** (Vagias): Strongly disagree | Disagree | Somewhat disagree | Neither agree nor disagree | Somewhat agree | Agree | Strongly agree
- **7 points** (SurveyMonkey): Strongly disagree | Moderately disagree | Slightly disagree | Neither agree nor disagree | Slightly agree | Moderately agree | Strongly agree

#### A2. Support and Opposition

Position on a policy or proposal. Bipolar. "Don't know" fits low-salience
policies.

- **5 points** (Vagias): Strongly oppose | Somewhat oppose | Neutral | Somewhat favor | Strongly favor
- **5 points** (ESS): Strongly against | Somewhat against | Neither in favour nor against | Somewhat in favour | Strongly in favour

#### A3. Favorability and Acceptability

Overall evaluation of a person, group, institution or action. Bipolar.

- **4 points** (Pew, favorability): Very unfavorable | Mostly unfavorable | Mostly favorable | Very favorable
- **4 points** (Pew, legality): Illegal in all cases | Illegal in most cases | Legal in most cases | Legal in all cases
- **5 points** (Vagias, desirability): Very undesirable | Undesirable | Neutral | Desirable | Very desirable
- **7 points** (Vagias, acceptability): Totally unacceptable | Unacceptable | Slightly unacceptable | Neutral | Slightly acceptable | Acceptable | Perfectly acceptable
- **7 points** (Vagias, appropriateness): Absolutely inappropriate | Inappropriate | Slightly inappropriate | Neutral | Slightly appropriate | Appropriate | Absolutely appropriate

#### A4. Political Ideology (ANES)

Self-placement. Bipolar. Which end takes the low code is a convention;
neither end is negative. Out-of-scale: "Haven't thought much about this".

- **7 points** (ANES): Extremely liberal | Liberal | Slightly liberal | Moderate; middle of the road | Slightly conservative | Conservative | Extremely conservative

### B. Satisfaction

#### B1. Satisfaction, Bipolar

Dissatisfaction is the opposite of satisfaction, with a neutral middle.
"Not applicable" or "Did not use" fits service batteries.

- **5 points** (Iowa/Qualtrics): Very dissatisfied | Somewhat dissatisfied | Neither satisfied nor dissatisfied | Somewhat satisfied | Very satisfied
- **5 points** (Wisconsin): Very dissatisfied | Moderately dissatisfied | Neither satisfied nor dissatisfied | Moderately satisfied | Very satisfied
- **7 points** (Vagias): Completely dissatisfied | Mostly dissatisfied | Somewhat dissatisfied | Neither satisfied nor dissatisfied | Somewhat satisfied | Mostly satisfied | Completely satisfied
- **11 points, ends only** (ESS life satisfaction, start 0): Extremely dissatisfied ... Extremely satisfied

#### B2. Satisfaction, Unipolar

The amount of satisfaction from none upward. See 3.1 for the choice.

- **5 points** (SurveyMonkey, Vagias): Not at all satisfied | Slightly satisfied | Moderately satisfied | Very satisfied | Extremely satisfied
- **5 points** (Iowa/Qualtrics): Not at all satisfied | Not very satisfied | Somewhat satisfied | Very satisfied | Extremely satisfied

#### B3. CSAT (Customer Satisfaction Score)

Satisfaction with a transaction or product. Bipolar. Question: "How would you
rate your overall satisfaction with the [goods/service] you received?" The
score is the share of codes 4 and 5 among all answers, times 100. It is not
comparable across scale lengths.

- **5 points** (Qualtrics): Very unsatisfied | Unsatisfied | Neutral | Satisfied | Very satisfied

### C. Quality and Evaluation

#### C1. Quality (Poor to Excellent)

Unipolar: the amount of quality, with no neutral point. The steps are not
equally spaced; use the set because it is understood everywhere. Out-of-scale:
"Don't know", "Did not use", "Not applicable".

- **4 points** (Pew): Poor | Only fair | Good | Excellent
- **5 points** (Vagias, Iowa/Qualtrics): Poor | Fair | Good | Very good | Excellent
- **5 points** (Wisconsin): Poor | Fair | Average | Good | Excellent
- **5 points** (Wisconsin, relative): Poor | Below average | Average | Above average | Excellent
- **5 points** (Rohrmann, equidistant): Bad | Inadequate | Fair | Good | Excellent

The SF-36 and BRFSS self-rated health item uses the Vagias five ("In general,
would you say your health is:").

#### C2. Good and Bad

Bipolar.

- **5 points** (WHO self-rated health): Very bad | Bad | Moderate | Good | Very good
- **7 points, ends only** (ESS, start 0): Very bad ... Very good

### D. Frequency

#### D1. Verbal Frequency

Unipolar, from never upward. "Not applicable" may be offered. Never put
"rarely" with "seldom" or "often" with "frequently" on one scale.

- **5 points** (Vagias, SurveyMonkey): Never | Rarely | Sometimes | Often | Always
- **5 points** (Rohrmann, equidistant): Never | Seldom | Sometimes | Often | Always
- **5 points** (ESS): Never | Hardly ever | Sometimes | Often | Always
- **5 points** (Wisconsin): Never | Rarely | Occasionally | Often | Always
- **5 points** (Iowa/Qualtrics, proportion): Never | Sometimes | About half of the time | Most of the time | Always
- **7 points** (Vagias): Never | Rarely, in less than 10% of the chances when I could have | Occasionally, in about 30% of the chances when I could have | Sometimes, in about 50% of the chances when I could have | Frequently, in about 70% of the chances when I could have | Usually, in about 90% of the chances I could have | Every time

#### D2. Calendar Frequency

Unipolar. Use it when the rate matters, because vague quantifiers mean
different rates to different people. The categories must not overlap and
must cover every case. When a count exists, ask for the count in an Editbox.

- **5 points** (AUDIT items 3 to 8): Never | Less than monthly | Monthly | Weekly | Daily or almost daily
- **5 points** (AUDIT item 1): Never | Monthly or less | 2-4 times a month | 2-3 times a week | 4 or more times a week
- **6 points** (Wisconsin): Never | Once a year | Once a semester | Monthly | Weekly | Daily
- **7 points** (ESS, religious attendance): Never | Less often | Only on special holy days | At least once a month | Once a week | More than once a week | Every day

### E. Likelihood, Intention, Probability

#### E1. Likelihood, Unipolar

From no likelihood upward.

- **4 points** (ESS): Not at all likely | Not likely | Likely | Very likely
- **5 points** (SurveyMonkey): Not at all likely | Slightly likely | Moderately likely | Very likely | Extremely likely
- **5 points** (Iowa/Qualtrics): Not at all likely | Not very likely | Somewhat likely | Very likely | Extremely likely
- **11 points, ends only** (ESS, start 0): Not at all likely ... Extremely likely

#### E2. Likelihood, Bipolar

Unlikely against likely.

- **5 points** (Wisconsin): Very unlikely | Moderately unlikely | Neither likely nor unlikely | Moderately likely | Very likely
- **5 points** (Vagias): Extremely unlikely | Unlikely | Neutral | Likely | Extremely likely
- **5 points** (Rohrmann, probability): Certainly not | Unlikely | About 50:50 | Likely | For sure
- **5 points** (Vagias, probability): Not probable | Somewhat improbable | Neutral | Somewhat probable | Very probable

#### E3. Behavioural Intention

Bipolar: will not against will.

- **3 points** (Vagias, consideration): Would not consider | Might or might not consider | Definitely consider
- **4 points** (Wisconsin): Definitely wouldn't | Probably wouldn't | Probably would | Definitely would

#### E4. Juster Purchase Probability

The subjective probability of a future purchase or behaviour. Unipolar,
start 0, every point labelled. It predicts purchase rates better than an
intention scale, because people with no intention still report some chance.

- **11 points** (Juster, via Befurt & Silk; start 0): No chance, almost no chance (1 in 100) | Very slight possibility (1 in 10) | Slight possibility (2 in 10) | Some possibility (3 in 10) | Fair possibility (4 in 10) | Fairly good possibility (5 in 10) | Good possibility (6 in 10) | Probable (7 in 10) | Very probable (8 in 10) | Almost sure (9 in 10) | Certain, practically certain (99 in 100)

### F. Importance

#### F1. Importance

Unipolar: unimportance is the absence of importance, not its opposite.

- **4 points** (Pew): Not at all important | Not too important | Somewhat important | Very important
- **5 points** (Wisconsin): Not at all important | Slightly important | Moderately important | Very important | Extremely important
- **6 points** (SurveyMonkey): Not at all important | Slightly important | Somewhat important | Moderately important | Very important | Extremely important
- **7 points, ends only** (ESS, start 0): Not at all important ... Extremely important

### G. Amount, Extent, Intensity

#### G1. Generic Intensity ("How X")

The degree of any attribute the question names: helpful, interested,
informative, comfortable, knowledgeable, effective, trustworthy. Unipolar.
Replace X with the attribute. This is the usual replacement for an
agree/disagree item, to be preferred over it.

- **5 points** (Wisconsin, SurveyMonkey): Not at all X | Slightly X | Moderately X | Very X | Extremely X
- **5 points** (Iowa/Qualtrics): Not at all X | Not very X | Somewhat X | Very X | Extremely X
- **5 points** (Rohrmann, equidistant): Not | A little | Moderately | Quite a bit | Very
- **5 points** (Rohrmann, extreme ends): Not at all | Slightly | Moderately | Considerably | Extremely
- **5 points** (ESS, confidence): Not at all confident | A little confident | Quite confident | Very confident | Completely confident
- **11 points, ends only** (ESS, start 0): Not at all ... Completely

#### G2. Amount and Extent ("How Much", "To What Extent")

Unipolar.

- **4 points** (Wisconsin): Not at all | Slightly | Moderately | Significantly
- **4 points** (Vagias, responsibility): Not at all responsible | Somewhat responsible | Mostly responsible | Completely responsible
- **5 points** (Wisconsin): Not at all | Slightly | Moderately | Considerably | A great deal
- **5 points** (ESS): Not at all | Very little | Some | A lot | A great deal
- **5 points** (Vagias, influence): Not at all influential | Slightly influential | Somewhat influential | Very influential | Extremely influential

### H. Difficulty and Ease

#### H1. Difficulty and Ease

Bipolar: difficult and easy are opposites.

- **5 points** (Vagias): Very difficult | Difficult | Neutral | Easy | Very easy
- **5 points** (Wisconsin): Very difficult | Moderately difficult | Neither easy nor difficult | Moderately easy | Very easy

Two unipolar relatives, where the high code is not the easy end:

- **4 points** (PHQ-9 functional difficulty; high = more difficulty): Not difficult at all | Somewhat difficult | Very difficult | Extremely difficult
- **4 points** (ESS income adequacy): Finding it very difficult on present income | Finding it difficult on present income | Coping on present income | Living comfortably on present income

#### H2. Customer Effort Score (CES 2.0)

Agreement with "[Company] made it easy for me to handle my issue", on the
seven-point agreement labels of A1 (Vagias). Bipolar. Vendors score it as the
mean or as the share of codes 5 to 7.

### I. Comparison and Expectation

#### I1. Comparison

Bipolar around "about the same".

- **5 points** (Vagias, Iowa/Qualtrics): Much worse | Somewhat worse | About the same | Somewhat better | Much better
- **5 points** (Wisconsin, generic): Much less X | Slightly less X | About the same | Slightly more X | Much more X
- **5 points** (ESS): Much less than most | Less than most | About the same | More than most | Much more than most

#### I2. Expectations

Bipolar in concept: below against above expectations.

- **4 points** (Wisconsin): Does not meet expectations | Partially meets expectations | Fully meets expectations | Exceeds expectations

### J. Truth and Self-Description

#### J1. True and Untrue of Me

Bipolar.

- **7 points** (Vagias): Very untrue of me | Untrue of me | Somewhat untrue of me | Neutral | Somewhat true of me | True of me | Very true of me
- **7 points** (Vagias, beliefs): Very untrue of what I believe | Untrue of what I believe | Somewhat untrue of what I believe | Neutral | Somewhat true of what I believe | True of what I believe | Very true of what I believe
- **7 points** (Vagias, frequency of truth): Never true | Rarely true | Sometimes but infrequently true | Neutral | Sometimes true | Usually true | Always true

#### J2. "Like Me" (Schwartz Portrait Values, ESS)

Unipolar: the degree of similarity.

- **6 points** (ESS): Not like me at all | Not like me | A little like me | Somewhat like me | Like me | Very much like me

### K. Familiarity and Awareness

#### K1. Familiarity, Awareness, Interest

Unipolar. "Never heard of it" usually belongs in the lowest point, not out of
scale. For a new item the G1 ladder (Slightly, Moderately, Very) is the safer
choice: the Vagias sets place "Somewhat" below "Moderately", which is
debatable.

- **5 points** (Vagias, familiarity): Not at all familiar | Slightly familiar | Somewhat familiar | Moderately familiar | Extremely familiar
- **5 points** (Vagias, awareness): Not at all aware | Slightly aware | Somewhat aware | Moderately aware | Extremely aware
- **5 points** (Wisconsin, interest): Not at all interested | Slightly interested | Moderately interested | Very interested | Extremely interested
- **5 points** (Wisconsin, proficiency): Beginner | Developing | Competent | Advanced | Expert

### L. Concern, Worry, Problem Severity

#### L1. Concern and Worry

Unipolar. The high code is more concern.

- **5 points** (Vagias, concern): Not at all concerned | Slightly concerned | Somewhat concerned | Moderately concerned | Extremely concerned
- **5 points** (ESS, worry): Not at all worried | Not very worried | Somewhat worried | Very worried | Extremely worried

#### L2. Problem and Barrier Severity

Unipolar. The high code is more severe.

- **4 points** (Vagias, problem): Not at all a problem | Minor problem | Moderate problem | Serious problem
- **4 points** (Vagias, barrier): Not a barrier | Somewhat of a barrier | Moderate barrier | Extreme barrier
- **4 points** (pain verbal rating): None | Mild | Moderate | Severe

### M. Priority

#### M1. Priority

Unipolar.

- **5 points** (Vagias): Not a priority | Low priority | Medium priority | High priority | Essential

### N. Change Over Time

#### N1. Change

Bipolar around "about the same". The comparison set of I1 is the one with a
source.

- **5 points** (Vagias, Iowa/Qualtrics): Much worse | Somewhat worse | About the same | Somewhat better | Much better

### O. Trust and Confidence

#### O1. Trust and Confidence

Unipolar: the amount of trust.

- **4 points** (Pew): None at all | Not too much | A fair amount | A great deal
- **4 points** (Pew): Not at all | Not too much | Some | A lot
- **5 points** (ESS): Not at all | Very little | Some | A lot | A great deal
- **11 points, ends only** (ESS, start 0): No trust at all ... Complete trust
- **11 points, ends only** (ESS generalised trust, start 0): You can't be too careful ... Most people can be trusted

### P. Numeric End-Labelled Scales

All start at 0. Write the number on every point and the anchor on the two
ends.

#### P1. Net Promoter Score

Likelihood to recommend. Unipolar. Question: "How likely are you to recommend
us to a friend or colleague?" The score is the share of promoters (9 and 10)
minus the share of detractors (0 to 6). Never label the points between or
change the length: the metric is defined on 11 points.

- **11 points, ends only** (Bain; Qualtrics; start 0): Not at all likely ... Extremely likely

#### P2. Cantril Ladder

Life evaluation. Bipolar anchors. Wording: "Please imagine a ladder with
steps numbered from zero at the bottom to 10 at the top. The top of the
ladder represents the best possible life for you and the bottom of the ladder
represents the worst possible life for you. On which step of the ladder would
you say you personally feel you stand at this time?" Future item: "On which
step do you think you will stand about five years from now?" Gallup reads
present 7 or more with future 8 or more as thriving, and both at 4 or less as
suffering.

- **11 points, ends only** (Gallup, start 0): The worst possible life for you ... The best possible life for you

#### P3. ESS 0 to 10 Items

"Extremely" on both ends of a bipolar item; "Not at all" to "Extremely",
"Completely" or "Very" on a unipolar one.

- **11 points, ends only** (ESS life satisfaction, start 0): Extremely dissatisfied ... Extremely satisfied
- **11 points, ends only** (ESS happiness, start 0): Extremely unhappy ... Extremely happy

#### P4. Pain Numeric Rating Scale

Unipolar. The high code is worse. Common banding: 0 none, 1 to 3 mild, 4 to 6
moderate, 7 to 10 severe.

- **11 points, ends only** (VA, start 0): No pain ... Worst pain imaginable

#### P5. Wong-Baker FACES

Unipolar. A licensed instrument whose face images are part of the scale, and
whose six faces are scored 0, 2, 4, 6, 8, 10. Without the images it is not
the instrument; with codes 0 to 5 the published score is twice the code.

- **6 points** (Wong-Baker, start 0): No hurt | Hurts a little bit | Hurts a little more | Hurts even more | Hurts a whole lot | Hurts worst

### Q. Clinical and Standard Instruments

Use them verbatim. Never relabel, reorder or resize them, and offer no
out-of-scale answer the instrument does not print.

#### Q1. PHQ-9 and GAD-7

Symptom frequency over two weeks. Unipolar, start 0. Stem: "Over the last 2
weeks, how often have you been bothered by any of the following problems?"

- **4 points** (PHQ-9, GAD-7; start 0): Not at all | Several days | More than half the days | Nearly every day

```yaml
- id: q_phq9
  kind: QuestionGroup
  title: "Over the last 2 weeks, how often have you been bothered by any of the following problems?"
  questions:
    - "Little interest or pleasure in doing things"
    - "Feeling down, depressed, or hopeless"
  scale:
    polarity: unipolar
    points: 4
    start: 0
  input:
    control: Radio
    labels:
      0: "Not at all"
      1: "Several days"
      2: "More than half the days"
      3: "Nearly every day"
```

#### Q2. WHO-5 Well-Being Index

Unipolar, start 0, two-week recall. The raw sum times 4 gives 0 to 100.
Reproduced forms vary between "half the time" and "half of the time".

- **6 points** (WHO-5, start 0): At no time | Some of the time | Less than half of the time | More than half of the time | Most of the time | All of the time

#### Q3. AUDIT

Unipolar, start 0. Items 1 and 3 to 8 use the sets in D2 with `start: 0`.
Items 9 and 10 are scored 0, 2 and 4: with codes 0 to 2 the published score
is twice the code.

- **5 points** (AUDIT item 2, quantity; start 0): 1 or 2 | 3 or 4 | 5 or 6 | 7 to 9 | 10 or more
- **3 points** (AUDIT items 9 and 10; start 0): No | Yes, but not in the past year | Yes, during the past year

#### Q4. System Usability Scale

Bipolar agreement. Ten statements, the odd ones positive and the even ones
negative. Score: `code - 1` for an odd item, `5 - code` for an even one; the
sum times 2.5 gives 0 to 100. Code all ten the same way; the analyst ticks
the even items as reverse-worded in the Gold scale score.

- **5 points, ends only** (SUS): Strongly disagree ... Strongly agree

#### Q5. Participation Stage

Ordinal, unipolar.

- **3 points** (Vagias): No, and not considered | No, but considered | Yes

### R. Semantic Differential

#### R1. Semantic Differential (Osgood)

The connotative meaning of a concept on pairs of opposite adjectives.
Bipolar. Each item is one pair, for example Bad ... Good (evaluation),
Weak ... Strong (potency), Passive ... Active (activity). Put the negative
adjective at the lowest code of every pair.

- **7 points, ends only** (Osgood): Bad ... Good

## Sources

Vagias (2006), Likert-type scale response anchors. Krosnick & Presser (2010),
Question and questionnaire design. Krosnick et al. (2006), in *When I'm 64*.
Rohrmann (2007), Verbal qualifiers for rating scales. Pew Research Center,
Writing survey questions; "Don't know" options (2023); toplines. SurveyMonkey,
Likert scale guide. State of Iowa, Qualtrics rating-scale guide. Qualtrics,
CSAT and Net Promoter Score pages. Bain & Company, Measuring your Net
Promoter Score. University of Wisconsin System (2018), Selecting scales for
survey questions. European Social Survey, Round 11 source showcards. Gallup,
the Cantril scale. Befurt & Silk (2019), on Juster (1966). PHQ-9, GAD-7,
AUDIT and WHO-5 forms. Sauro & Lewis (2011). Saris, Revilla, Krosnick &
Shaeffer (2010). Chyung, Kennedy & Campbell (2018). Dillman, Smyth &
Christian (2014). ANES 2024 codebook. VA pain numeric rating scale.
