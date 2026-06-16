# Adaptive Survey Design for Large Instruments

Principles for designing questionnaires with 100+ items where not every
respondent answers every question. Routing logic determines which
questions are relevant based on respondent attributes discovered during
the survey.

## Core Principle: Screen Before You Ask

In large instruments, many questions apply only to specific subpopulations.
The primary design challenge is discovering which questions are relevant
to each respondent without wasting their time.

**Every question in the instrument serves one of two roles:**

1. **Routing questions** — discover respondent attributes to determine
   which later questions are relevant. These are short, closed-ended,
   and placed early. Their primary value is enabling routing, though
   they may also produce useful data.

2. **Substantive questions** — collect the data you actually need.
   These are gated by preconditions derived from routing questions.

Design the routing questions first, then organize substantive questions
around the routing structure.

## Screening-First Architecture

Structure the questionnaire as a funnel:

1. **Universal screening block** (all respondents): demographics,
   household composition, employment status, key lifestyle attributes.
   Keep this under 3 minutes. These answers define the respondent's
   profile and unlock relevant modules.

2. **Topic eligibility gates** (per module): a single question or
   short sequence that determines whether an entire topic module
   applies. Example: "Do you have any outstanding loans?" gates the
   entire financial obligations module.

3. **Detail questions** (eligible respondents only): the substantive
   questions within each module, gated by preconditions.

This architecture ensures no respondent sees irrelevant questions while
maximizing data collection from relevant subpopulations.

## Module-Based Design

Organize the instrument into **independent topic modules** of 10-30
items each. Each module has:

- An **eligibility gate**: a routing question or computed variable that
  determines whether the module applies
- **Internal routing**: additional screening within the module for
  sub-topics
- **Self-contained logic**: modules should not depend on answers from
  other modules (except via the universal screening block)

Benefits:
- Modules can be added, removed, or reordered without affecting others
- Different respondent profiles see different module combinations
- Parallel development: different researchers can own different modules
- Testing: each module can be validated independently

In QML: each module maps to a block. The eligibility gate is a
codeBlock or Switch item in the universal screening block, and all
items in the module carry a precondition on the eligibility variable.

## Hub-and-Spoke Routing Pattern

For instruments with 10+ modules, use a central routing hub:

```
Universal Screening (hub)
  ├── Module A: Housing (spoke) — if owns/rents property
  ├── Module B: Children (spoke) — if has children under 18
  ├── Module C: Employment (spoke) — if currently employed
  ├── Module D: Health (spoke) — if opted into health section
  ├── Module E: Finance (spoke) — if has financial products
  └── Module F: Retirement (spoke) — if age >= 55
```

The hub computes eligibility flags for all modules. Each spoke is
activated only when its flag is set. A respondent who owns property,
has no children, is employed, and is under 55 would see modules A, C,
and potentially D and E — skipping B and F entirely.

In QML: the hub is a block of codeBlock items that compute eligibility
variables from the screening answers. Each spoke block's items carry
preconditions on the corresponding eligibility variable.

## Sequential Gating Within Modules

Within a module, use progressive refinement:

1. **Broad filter**: "Do you have any insurance policies?" (Yes/No)
2. **Type discovery**: "Which types of insurance do you have?"
   (forced-choice per type: health, life, home, auto, other)
3. **Detail per type**: Questions about each insurance type, gated on
   having that type

This avoids the common mistake of asking a long battery of questions
when a quick screen could eliminate the entire section.

## Item Budgeting

Not every respondent should answer the same number of questions. Design
for a **target completion time** per respondent, not a fixed item count.

Guidelines for estimating respondent time:
- Simple yes/no or single-select: 10-15 seconds per item
- Rating scales (Slider, Radio with 4-7 options): 15-20 seconds
- Numeric input: 15-20 seconds
- Open-ended text: 30-60 seconds
- Matrix/grid rows: 8-12 seconds per row

For a 20-minute target, budget approximately 60-80 items per respondent.
The total instrument can be much larger (500+ items) as long as routing
ensures no individual respondent exceeds the time budget.

**Track the estimated path length** for each respondent profile. If
a profile that triggers many modules exceeds the time budget, either:
- Split the profile into sub-profiles with additional routing
- Make some modules probabilistic (randomly assigned to a subset)
- Shorten the longest modules for high-burden profiles

## Planned Missingness

When the instrument contains items you want to ask broadly but can't
ask everyone due to time constraints, use **planned missingness**:

**Rotating module design**: Divide non-essential modules into groups.
Randomly assign each respondent to a subset of groups. Every module
gets asked of a representative subset, but no respondent answers all
of them.

Example with 3 rotation groups:
- All respondents: core screening + 2 mandatory modules
- Group A (1/3 of respondents): modules X and Y
- Group B (1/3 of respondents): modules X and Z
- Group C (1/3 of respondents): modules Y and Z

Each optional module reaches 2/3 of respondents. The random assignment
ensures unbiased estimates for each module.

In QML: implement rotation via a codeInit variable set from an external
respondent attribute or a random assignment at survey start. Gate
rotating modules with preconditions on this variable.

## Variable Accumulation Strategy

In large instruments, routing decisions often depend on combinations
of earlier answers. Use codeBlock items to accumulate derived variables
as the respondent progresses:

**Profile variables**: Computed from screening answers, used throughout.
```yaml
codeInit: |
  is_parent = 0
  is_employed = 0
  is_homeowner = 0
  risk_profile = 0  # 0=low, 1=medium, 2=high
```

**Accumulation codeBlocks**: Update profile variables after each
screening section.
```yaml
- id: calc_risk_profile
  type: codeBlock
  codeBlock: |
    risk_score = 0
    if q_age.outcome < 30:
      risk_score = risk_score + 1
    if q_income.outcome > 100000:
      risk_score = risk_score + 1
    if q_has_investments.outcome == 1:
      risk_score = risk_score + 1
    risk_profile = 0 if risk_score == 0 else (1 if risk_score <= 2 else 2)
```

This pattern keeps routing logic readable and maintainable as the
instrument grows. Each module only needs to check one or two profile
variables rather than re-evaluating raw screening answers.

## Designing Routing Questions

Routing questions are optimized for branching, not just data collection.
Design them to maximize routing value:

- **Binary or low-cardinality**: Yes/No or 3-4 options. More categories
  means more routing paths to maintain.
- **Unambiguous eligibility**: The answer should clearly determine
  whether subsequent questions apply. Avoid "sometimes" or "it depends"
  options that leave eligibility unclear.
- **Front-loaded**: Place routing questions before the content they gate.
  Never ask a routing question after the questions it would have gated.
- **Cheap to answer**: Routing questions should be fast (10-15 seconds).
  The respondent's time investment should go toward substantive questions.

## Anti-Patterns to Avoid

**Asking everything from everybody**: In a 500-item instrument, if the
average respondent answers more than 30% of items, the routing is
probably insufficient. Most respondents should skip large sections.

**Deep nesting without escape**: If routing creates paths 5+ levels
deep, the survey becomes a maze. Keep nesting to 2-3 levels maximum.
Use the hub-and-spoke pattern instead of deep trees.

**Routing on open-ended answers**: Never gate questions on free-text
responses. Use closed-ended routing questions that produce predictable,
machine-readable outcomes.

**Redundant screening**: Don't re-screen within a module for attributes
already established in the universal screening block. Pass eligibility
via computed variables.

**Asymmetric burden**: If some respondent profiles see 80 questions and
others see 15, the data quality for the long path will be lower. Balance
path lengths across profiles.
