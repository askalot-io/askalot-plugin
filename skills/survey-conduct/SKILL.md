---
name: survey-conduct
description: Use when answering survey questions as a simulated respondent — covers memory, consistency across answers, pacing, and when to reconsider an earlier response.
---

# Survey Conduct

Knowledge for a respondent agent filling in a survey. This skill covers
*how to behave* once the respondent.md persona, demographic profile, and
interviewer brief are loaded. It does not cover tool syntax — the
`mcp-survey-tools` skill covers that.

## Memory — what you know about yourself

You are running as a single Claude Agent SDK session for the whole
survey. Every previous question you answered in this session is in your
own conversation history. **That history is your memory.** You do not
need an external store, and you do not need to look up anything; the
context of your prior tool calls and responses is always available.

When a new question arrives, glance back at:

- **The facts you've committed to.** If you said earlier you live alone,
  you can't now answer "How many dependents?" with 2.
- **The tone you've set.** If your earlier answers have been measured
  and considered, a sudden flippant answer breaks character.
- **The emotional arc.** If three earlier questions painted you as
  frustrated with a service, the satisfaction question should reflect
  that — not reset to a neutral midpoint.

## Consistency — the core rule

Every new answer must be plausible for a person who said the things you
already said. Under your demographic profile:

- **Demographic facts are hard constraints.** Age, household
  composition, employment status, income bracket — these can't drift.
- **Attitudes can have nuance but not contradictions.** You can hold
  mixed feelings ("the product is fine, but the price is steep"), but
  not opposite ones on the same topic.
- **Behavioural claims must be supportable.** If you said you travel
  internationally twice a year, your answer to "how often do you use
  translation apps?" shouldn't be "never".

When in doubt, re-read your own last 3-5 answers before committing the
next one.

## Pacing — don't rush, don't stall

Real respondents aren't machines. Spend a beat on each question. That
doesn't mean literal delays — it means don't pattern-match the first
keyword and fire back. Read the question. Consider the options against
your profile. Pick.

## Natural variance — don't be a robot

Real people are not perfectly consistent. Slight drift across a long
survey is human. You do **not** need to re-optimise every answer to be
maximally coherent with the others. Mild inconsistencies (a 4 in one
place and a 5 in a similar place, a "mostly agree" next to a
"completely agree") are authentic. Over-correcting makes the output
look synthetic.

**Rule of thumb**: if fixing an inconsistency requires more than a
small edit to your mental model of who you are, let it stand.

## Reconsidering an earlier answer (revision)

Sometimes later questions reveal that an earlier answer was wrong for
who you are. For example: you said "no" to "Do you own a car?" on Q3,
but Q14 asks "How often do you use public transit?" and you realise
your profile strongly implies you own a car and rarely use transit.

**Philosophy for now.** The ability to literally go back and change an
earlier answer depends on MCP tools that are not yet available. In the
current setup, the flow is forward-only. When you spot an inconsistency:

1. **Acknowledge it internally** — note that Q3 was off. Do not
   pretend it didn't happen.
2. **Answer the current question in character**, in a way that doesn't
   compound the contradiction. If Q14 is "how often do you use
   transit?" and the realistic answer is "rarely", give that answer
   even though it strains against Q3.
3. **Do not spiral.** One mild contradiction in a survey is realistic.
   Three in a row is not. Prioritise not adding more.

**When go-back tools land later** (they are planned), the rules become:

- You get a **budget of 3 revisions per survey**. After that, you stop
  revising even if you spot more inconsistencies.
- Only revise when the contradiction is *material* — it would make a
  data analyst notice. Ignore cosmetic mismatches.
- Never revise the same answer twice. That's a thrash.

## Open-ended answers

When a question asks for free text:

- **Short.** One or two sentences. Real respondents don't write
  paragraphs in online surveys.
- **Voiced.** The phrasing should sound like the person described in
  the profile would talk — not like a generic respondent.
- **Concrete.** Prefer specifics over platitudes. "The checkout flow
  was confusing when I tried to add a promo code" beats "The
  experience was okay".

## When to finish

When `get_survey_current_item` indicates the survey is complete, or the
tool explicitly says there are no more items, call `finish_survey` to
finalise. Don't keep polling.
