---
name: validity-reliability
description: Use when designing items for later psychometric validation, evaluating the reliability of a measurement scale (Cronbach's α, McDonald's ω, test-retest, inter-rater), demonstrating validity (content, criterion, construct), running Aithal's seven-step instrument development workflow, or interpreting Cronbach's α caveats and thresholds. Distilled from Taherdoost (2016) and Aithal & Aithal (2020).
---

# Validity & Reliability — Instrument Quality Reference

Practitioner-level guide for Designers (building items that *can* be
validated) and Analysts (evaluating whether a scale *is* valid and
reliable). If a question goes deeper, search the methodology library
(`search_methodology_library`; the `methodology-library` skill
describes the tools) for Taherdoost or Aithal directly. The citation
keys below (`taherdoost2016validity`, `aithal2020development`) are the
library's paper keys.

What the platform computes itself is narrow: Cronbach's α per battery
(the sub-items of one QuestionGroup or MatrixQuestion, three or more),
on the stored answer codes with out-of-scale answers left out; the Gold
scale score's α, computed after the analyst's chosen items are
reversed; plus straightlining, speeders and item nonresponse. CVR, factor analysis, McDonald's ω, test-retest and κ
are not computed; they need the exported data and the researcher's
own analysis. Recommend them, do not report them as available.

---

## 1. Validity — four types, each a separate claim

Validity is not one thing. A scale can be content-valid but construct-
invalid (measures a related but distinct concept), or internally
consistent but predictively useless. Demonstrate each type you claim.

### Content validity — does the instrument cover the construct?

**Content validity** requires a panel of subject-matter experts (5–30
people, typically ~10) rating each candidate item as **essential**,
**useful**, or **not necessary**. Compute Lawshe's **Content Validity
Ratio (CVR)**:

$$\mathrm{CVR} = \frac{n_e - N/2}{N/2}$$

where $n_e$ = count of experts rating the item "essential" and $N$ =
panel size. Lawshe's significance thresholds: for $N = 10$, retain
items with $\mathrm{CVR} \geq 0.62$; for $N = 20$, $\geq 0.42$; for
$N = 30$, $\geq 0.33$ (taherdoost2016validity, p.~3–4;
aithal2020development, p.~11).

> "Content validity involves evaluation of a new survey instrument in
> order to ensure that it includes all the items that are essential
> and eliminates undesirable items to a particular construct domain."
> (taherdoost2016validity, p.~3)

### Construct validity — does the scale measure the intended concept?

**Construct validity** decomposes into **convergent** and
**discriminant**:

- **Convergent**: items that should correlate *do* correlate. Use PCA
  or CFA with varimax rotation; require factor loadings $\geq 0.40$
  on the posited construct; preferably $\geq 0.60$ for robust scales
  (taherdoost2016validity, p.~5).
- **Discriminant**: items that should *not* correlate with a different
  construct don't. No cross-loading $> 0.40$ on unrelated factors.

> "Convergent validity tests that constructs that are expected to be
> related are, in fact, related… Discriminant validity tests that
> constructs that should have no relationship do, in fact, not have
> any relationship."
> (taherdoost2016validity, p.~5)

Items failing either criterion are deleted and the analysis is
re-run (aithal2020development, p.~11).

### Criterion validity — does the scale predict or align with a benchmark?

- **Concurrent**: scale correlates with an established measure
  administered at the same time.
- **Predictive**: scale predicts a future outcome.
- **Postdictive**: scale correlates with a past criterion measure.

Use Pearson's $r$ or intraclass correlation for concurrent; regression
or discriminant analysis for predictive
(taherdoost2016validity, p.~7).

---

## 2. Reliability — five instruments, different questions

**Reliability** is consistency: across time, across raters, across
items, across alternate forms. Pick the right one for the claim you
want to make.

| Method | What it measures | Typical statistic | When to use |
|---|---|---|---|
| Test-retest | Temporal stability | Pearson's $r$ | Stable constructs (personality, traits); not transitory (pain, mood) |
| Inter-rater | Agreement between raters | Cohen's κ | Coded open-ended, observational ratings |
| Internal consistency | Items cohere | Cronbach's α, McDonald's ω | Multi-item constructs on one declared rating scale |
| Split-half | Odd/even items cohere | Spearman-Brown corrected r | Older, simpler alternative to α |
| Parallel forms | Two equivalent forms cohere | Pearson's $r$ | Pre/post designs where retest would bias memory |

(taherdoost2016validity, p.~6; aithal2020development, p.~6–9)

### Cronbach's α — the most cited, most abused

**Thresholds** (aithal2020development, p.~7–8;
taherdoost2016validity for the exploratory floor):

- $\alpha \leq 0$ — serious flaw; check reverse-coding
- $0 < \alpha < 0.5$ — discard or heavily revise
- $0.5 \leq \alpha < 0.7$ — moderate; revise items. From 0.6 it is
  acceptable for an exploratory or pilot study
- $0.7 \leq \alpha < 0.9$ — good; 0.7 is the minimum for confirmatory
  use
- $\alpha \geq 0.9$ — may indicate redundancy; inspect inter-item
  correlations and consider removing duplicates

> "The value of Cronbach's alpha is a function of length of
> questionnaire (i.e., number of items in the questionnaire) and will
> increase its value with increase in length and hence number of
> items."
> (aithal2020development, p.~7)

### Cohen's κ thresholds (inter-rater)

$\kappa$ 0.41–0.60 fair · 0.61–0.80 good · 0.81–0.92 very good ·
$\geq 0.93$ excellent (aithal2020development, p.~8–9).

---

## 3. Aithal's seven-step instrument development workflow

The full lifecycle for a new scale (aithal2020development, p.~4–12):

1. **Concept & construct mapping.** Systematic literature review;
   identify determinant issues and construct dimensionality
   (unidimensional vs multi-factor); choose administration mode
   (self vs interviewer).
2. **Item pool development.** Draft initial items — simple language,
   one issue per item, strategic reverse-coding with care (reverse
   items must have similar psychometrics to forward items).
3. **Expert content review.** 5–30 experts rate each item; compute
   CVR; retain items above the Lawshe threshold.
4. **Preliminary pilot (n = 30–50).** Detect confusion, check
   response variance (no floor/ceiling), refine wording and order.
5. **Full pilot (10% of main sample size, typically n ≥ 100).**
   Collect data sufficient for psychometrics.
6. **Statistical evaluation.** Run PCA / CFA (require loadings
   $\geq 0.40$, preferably $\geq 0.60$); compute Cronbach's α (or
   McDonald's ω for multi-dimensional scales). Delete items with low
   loadings or high cross-loadings.
7. **Refinement & final version.** If major changes (many items
   deleted or rewritten), repeat pilot + validation. If minor
   changes, proceed to main study.

**Sample-size rules** (aithal2020development, p.~13):
- $5:1$ ratio (5 respondents per item): minimum
- $10:1$: preferred for confirmatory analysis
- $15:1$ or $30:1$: high-precision construct studies
- Tabachnick/Comrey tier: 100 poor · 200 fair · 300 good · 500 very
  good · 1000+ excellent

> "A preliminary pilot test should be conducted to check the
> effectiveness of the questionnaire before conducting a full-fledged
> final pilot test. Usually, the preliminary pilot test is
> administered on small set of respondents and the sample size is
> about 30 to 50 numbers."
> (aithal2020development, p.~6)

---

## 4. Validity threats in web surveys — and mitigations

**Mode effects and social desirability.** Self-administered is
generally better than interviewer-administered for sensitive topics,
but phrasing still matters. Frame sensitive items as symptom
description ("do you feel you have a weight concern?") rather than
categorical labels ("are you obese?"); prefer scalar responses over
binary yes/no for affect-laden constructs
(aithal2020development, p.~5).

**Careless responding / straightlining.**
- Interleave **reverse-worded items** — but only with psychometric
  equivalents; naively reversed items can damage α (aithal2020development, p.~5).
  Reverse keying is chosen in analysis (the Gold scale score), not in QML.
- Embed **attention checks**: rephrase-and-repeat pairs, simple
  instructional manipulation checks ("choose option 3 for this item"
  — sparingly, not overused).
- Flag straightliners via response variance on matrix questions
  (the platform reports a straightlining score per battery and per run
  of standalone items declaring the same scale with the same labels; the `data-quality`
  skill describes it).

**Item-level threats.**
- **Avoid double-barreled**: "Have you experienced nausea *and*
  vomiting?" → split into two.
- **Minimize negatives** unless essential ("do not" scales test
  reading comprehension, not attitude).
- **Precise quantifiers**: "in the last 24 hours" > "usually";
  "at least 3 times per week" > "often".
- **Enough response anchors** (the source asks for 5+; 4 is allowed
  where a bipolar scale should force a side or a unipolar one needs no
  more) with verbal labels and equal spacing.
  Too few kills variance; too many (> 9) adds noise without signal
  (aithal2020development, p.~5).

**Questionnaire length.** Fatigue cascades into straightlining and
dropout. Trim aggressively during pilot.

---

## 5. Cronbach's α caveats — what the number does NOT tell you

Four places where α misleads:

1. **Sample-dependence.** α is *this-sample-specific*. A scale with
   α = 0.88 in study A can have α = 0.67 in study B with a different
   population. Report α with the sample it was estimated on, never as
   a scale-level property (aithal2020development, p.~8–9).

   > "A questionnaire with excellent reliability with one set sample
   > needs not have same amount reliability with another set of
   > samples. Hence, the reliability of a questionnaire should be
   > estimated every time when the questionnaire is administered to
   > the respondents."
   > (aithal2020development, p.~8–9)

2. **Unidimensionality assumption.** α only behaves well on
   single-construct scales. A two-factor scale with strong loadings
   can yield high α that masks the two-factor structure. **Verify
   unidimensionality via PCA or CFA before interpreting α**
   (aithal2020development, p.~7–9). Consider McDonald's ω for
   multi-dimensional scales.

3. **Item-count inflation.** More items → higher α, holding mean
   inter-item correlation constant. α = 0.92 on a 40-item scale is
   not obviously better than α = 0.80 on a 10-item scale
   (aithal2020development, p.~7).

4. **Reliability without validity is useless.** A consistently wrong
   measurement is still wrong (aithal2020development, p.~9):

   > "Performing a reliability test on a questionnaire is meaningful
   > if and only it is combined with the validity test."
   > (aithal2020development, p.~9)

---

## 6. QML design patterns that support later validation

Check for these when reviewing a questionnaire, and build them in when
writing one. They decide whether the collected data can support a
reliability or validity claim:

1. **Reverse-worded items.** For any multi-item construct on one
   declared rating scale, include ≥ 1 reverse-worded item
   (aithal2020development, p.~5). Code every item the same way (the
   lowest code = the negative or low end) and declare the scale;
   reverse keying is not a QML attribute. The analyst ticks the
   reverse-worded items when building the Gold scale score, which
   reverses them (2 × start + points − 1 − code) and reports α on that
   matrix. The per-battery α on the quality
   page reads the stored codes unreversed, so a reverse-worded item
   lowers it: name every reversed item in the review or the paper, so
   whoever builds the score knows which to tick.
2. **One battery per construct.** Put a construct's items in one
   QuestionGroup or MatrixQuestion with three or more sub-items: that
   is the unit the platform computes α and straightlining over. Declare
   its scale (`qml-syntax` §4.10).
3. **Attention checks.** 1–2 embedded checks per ~30 items, and no
   more than 2–3 in the whole survey (`survey-design`,
   `response-quality.md`).
4. **Parallel forms** for sensitive or stable constructs. Two
   equivalent batteries on one declared scale, balanced across respondents — enables
   alternate-form reliability (aithal2020development, p.~9–10).
5. **A declared scale with the construct's own standard labels**
   (`survey-design`, `standard-scales.md`): 5 or 7 points when bipolar,
   4 or 5 when unipolar; a bipolar scale has a midpoint exactly when
   the count is odd. Don't collapse scales in
   code — the Analyst wants the raw ordinal data.
6. **Short open-ended follow-up** for headline constructs (optional
   one-sentence "anything else we missed?"). Lets the Analyst check
   discriminant validity qualitatively when closed-ended scales seem
   contradictory.
7. **Pilot waves in the fielding plan.** Pre-pilot (n = 30–50)
   before full pilot (n ≥ 100). Don't skip — pilot data catches the
   items the expert review missed.

---

## 7. Cheatsheet — customer asks, you answer

| Customer asks… | Answer this way |
|---|---|
| "Is α = 0.68 good enough?" | For an exploratory / new-construct scale, yes; for confirmatory use, revise items. Also check unidimensionality via PCA before trusting α at all (aithal2020development, p.~7–8). |
| "Why α = 0.93 on this scale is 'too high'?" | Likely item redundancy; inspect inter-item correlations, drop duplicates, aim for the 0.7–0.9 band (aithal2020development, p.~7–8). |
| "Can we skip the pilot?" | No — the pilot is where item-level psychometric problems show up. Skipping it means discovering them in the main study when fixing is expensive (aithal2020development, p.~6). |
| "Why do we need reverse-worded items?" | They flag careless responders and guard against acquiescence bias, but only if the reverse items have psychometrics similar to forward items (aithal2020development, p.~5). Tick them as reversed in the Gold scale score. |
| "How many experts for content validity?" | 5–30, typically ~10. Compute Lawshe's CVR; retain items above the threshold for your panel size (taherdoost2016validity, p.~3–4). |
| "Is a single Cronbach's α enough to call the scale 'validated'?" | No. α is reliability, not validity. You also need content validity (CVR), construct validity (factor structure), and ideally criterion validity (correlation with a benchmark) (aithal2020development, p.~9). |
