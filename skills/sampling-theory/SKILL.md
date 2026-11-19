---
name: sampling-theory
description: Use when advising on sampling design (SRS, stratified, cluster, multi-stage), sample-size determination, weighting fundamentals (design weights, nonresponse adjustment, post-stratification, raking), design effect (DEFF) interpretation, or why a naive standard error underestimates uncertainty under complex samples. Distilled from Heeringa, West & Berglund (2010) "Applied Survey Data Analysis" and Saris & Gallhofer (2007, library id bethlehem2012design). Cites Kish (1965) where load-bearing.
---

# Sampling Theory — Practitioner Reference

Dense reference for advanced-practitioner decisions. If the question goes
deeper than this skill covers, reach for `methodology-library` and search
Heeringa, Bethlehem, Kish, or Schouten directly.

---

## 1. Probability sampling families — picking the right design

**Simple Random Sampling (SRS)** is the analytical reference point, not
usually the operational choice. Under SRS the estimator
$\operatorname{SE}(\bar y) = \sqrt{(1 - n/N)\, S^2 / n}$ — the leading
factor is the **finite-population correction (fpc)**. For $n/N < 0.05$ the
fpc is effectively 1 and can be ignored (heeringa2010applied, p.~41). In
most general-population surveys $N \gg n$, so fpc rarely matters in
practice; it **does** matter for narrow frames (e.g. a 2,000-member
professional association sampled at 400).

**Stratified** — partition the frame into $H$ mutually exclusive
strata and sample independently within each. Gain:
$\operatorname{Var}(\bar y_{\mathrm{SRS}}) - \operatorname{Var}(\bar
y_{\mathrm{st, pr}}) = S^2_{\text{between}}$ (heeringa2010applied, p.~53).
Use when: (1) you want subgroup precision (disproportionate
allocation / oversampling), (2) the frame has strong between-strata
heterogeneity you can exploit, (3) administrative cost structure favors
stratum-level operations. Quote:

> "Stratification provides the survey statistician with a convenient
> framework to disproportionately allocate the sample to
> subpopulations, that is, to oversample specific subpopulations to
> ensure sufficient sample sizes for analysis."
> (heeringa2010applied, p.~53)

**Cluster / Multi-stage** — sample groups (geographic, institutional),
then sub-sample within. Cuts field cost and simplifies frame
construction but **inflates** variance via intra-class correlation
$\rho$. Don't reach for clustering on a web-panel survey where the
operational cost of SRS is already low. Quote:

> "While cluster sampling can reduce survey costs or simplify the
> logistics of the actual survey data collection, the survey data
> analyst must recognize that clustered selection of elements affects
> his or her approach to variance estimation and developing inferences
> from the sample data."
> (heeringa2010applied, p.~49)

**Decision rules of thumb:**
- If frame is a clean population list and you sample < 5%: SRS or
  lightly-stratified SRS.
- If the customer demands precision on a small subgroup: stratify on
  that variable and oversample.
- Only cluster when fieldwork cost makes SRS infeasible; always budget
  variance inflation.

---

## 2. Sample-size determination

Start from the target precision: a half-width $d$ at confidence
$100(1-\alpha)\%$ for a proportion $p$ gives
$n_{\mathrm{SRS}} = z_{1-\alpha/2}^2 \cdot p(1-p) / d^2$. Then adjust:

$$n_{\mathrm{complex}} = n_{\mathrm{SRS}} \cdot D^2(\hat\theta)$$

where $D^2$ is the anticipated design effect
(heeringa2010applied, p.~45). Typical empirical $D^2$ ranges **1.2 –
3.0** for complex general-population surveys; take the upper end if
you expect substantial weight variation or cluster sizes above 15.

**Subgroup oversampling.** If a subgroup occupies fraction $p_s$ of the
population and you want precision $d_s$ inside it, solve for the
subgroup first and back out the overall $n$. An 80:20 urban-rural
frame sampled 50:50 yields a weighting loss
$L_w \approx cv^2(w) \approx 0.36$ — i.e. you need ~36% more sample
than SRS for the same overall precision (heeringa2010applied, p.~66).
That's the price of oversampling; the customer should see it when you
explain the tradeoff.

**Quote — when to plan for DEFF:**

> "The sample designer can use the concept and its component models to
> optimize the cost and error properties of specific design
> alternatives or to adjust simple random sample size computations for
> the design effect anticipated under a specific sampling plan."
> (heeringa2010applied, p.~45)

**FPC caveat.** By hand, apply $(1-n/N)$ only when $n/N > 0.05$; below that
the correction is negligible (heeringa2010applied, p.~41). `plan_sample_size`
applies it to margin goals whenever you pass `population_size`, so leave that
input out when the eligible population is unknown.

---

## 3. Weighting fundamentals

A production survey weight is the product of three sequential
components (heeringa2010applied, p.~58):

1. **Selection / design weight** $w_{\mathrm{sel}} = 1 / \pi_i$ — the
   reciprocal of the inclusion probability. Fixed at design time.
2. **Nonresponse adjustment** $w_{\mathrm{nr}} = 1 / \mathrm{rrate}_c$
   — correct for differential response within weighting cells $c$.
   Two implementations: (a) **weighting-class** (cells defined by
   frame variables), (b) logistic-regression propensity (cells defined
   by a response model). Weighting reduces bias from informative
   nonresponse but **increases variance** — it is never a free lunch
   (heeringa2010applied, p.~60).
3. **Post-stratification / raking** $w_{\mathrm{ps}}$ — align the
   sample's marginal distributions with known population totals.
   Raking is the iterative form for multiple marginals without joint
   control totals.

**Post-stratification is weaker than design stratification** but still
worth doing — especially when the frame has coverage bias you can
patch with external benchmarks (heeringa2010applied, p.~58):

> "While not as effective as estimation for samples that were
> stratified at the time that they were selected, the use of
> poststratification weight factors can lead to reduced standard
> errors (variance) for sample estimates."
> (heeringa2010applied, p.~58)

**Rule for the Analyst:** always check that the post-stratification /
raking step actually *reduced* quality-metric error on the targeted
factors. If RMSE increases after raking, the implementation is wrong —
either the targets are off or the factor definitions don't match.

---

## 4. Design Effect (DEFF) and effective sample size

Kish's classical decomposition
(heeringa2010applied, p.~44–45):

$$D^2(\hat\theta) = \frac{\operatorname{Var}(\hat\theta)_{\mathrm{complex}}}
{\operatorname{Var}(\hat\theta)_{\mathrm{SRS}}}
\approx 1 + f(G_{\text{strat}}, L_{\text{cluster}}, L_{\text{weighting}})$$

- **Stratification gain** $G_{\text{strat}}$ — a *reduction*, typically
  small for modest stratification but meaningful when strata are
  strongly homogeneous.
- **Cluster loss** $L_{\text{cluster}} \approx \rho(B-1)$ — where
  $\rho$ is intra-class correlation and $B$ is cluster size. Typical
  $\rho$ is 0.005–0.100 for general-population variables
  (heeringa2010applied, p.~50). **This dominates in clustered designs.**
- **Weighting loss** $L_w \approx cv^2(w) = \sigma^2(w) / \bar w^2$
  — Kish's weighting-effect formula (heeringa2010applied, p.~66).

**Effective sample size.** $n_{\mathrm{eff}} = n / D^2$. Quote:

> "For a fixed sample size, the statements 'the design effect for the
> proposed complex sample is 1.5' and 'the complex sample of size n =
> 1000 has an effective sample size of n_eff = 667' are equivalent
> statements of the precision loss expected from the complex sample
> design."
> (heeringa2010applied, p.~47)

**Interpretation thresholds:**
- $D^2 \leq 1.2$ — essentially SRS-equivalent.
- $D^2 \in (1.2, 2.0]$ — typical for stratified / lightly-clustered
  designs; no alarm.
- $D^2 \in (2.0, 3.0]$ — substantial cost; revisit weighting or
  cluster structure.
- $D^2 > 3.0$ — investigate: either extreme weight variation or
  dominant clustering. Consider weight trimming if $cv(w) > 1$.

**Counter-intuitive magnitude.** A classroom-level variable with
$\rho = 1.0$ and cluster size $B = 25$ yields $D^2 \approx 1 + 1.0
\cdot 24 = 25$ — i.e. a sample of 2,500 students has an effective
size of 100 (heeringa2010applied, p.~50). This is why cluster designs
for group-level outcomes are a warning sign, not a convenience.

**Weighting caveat.** Kish's $L_w \approx cv^2(w)$ assumes weight is
uncorrelated with outcome. Little & Vartivarian (2005, cited at
heeringa2010applied, p.~66) show weighting can *improve* precision
when weight variation tracks informative nonresponse. The Analyst
should report both the Kish DEFF *and* the empirical variance ratio
when evaluating weighting effectiveness.

---

## 5. Complex-sample variance — why naive SE is wrong

**The failure mode.** Under clustering, observations within a cluster
are correlated, so $\sum \hat y_i$ has more variance than
$n \cdot \operatorname{Var}(\hat y_i) / n$ predicts. Naive
SE **underestimates** true variance; confidence intervals are
**too narrow**; null hypotheses are rejected too often
(heeringa2010applied, p.~39):

> "In general, the SRS assumption results in underestimation of
> variances of survey estimates of descriptive statistics and model
> parameters. Confidence intervals based on computed variances that
> assume independence of observations will be biased (generally too
> narrow)."
> (heeringa2010applied, p.~39)

**Two correct approaches:**

1. **Taylor Series Linearization (TSL).** For nonlinear estimators
   (ratios, regression coefficients), linearize around expected
   totals, then apply stratified-with-replacement-cluster variance
   formulas to the linearized form. Degrees of freedom
   $df = \sum_h (a_h - 1) = (\text{\# PSUs}) - (\text{\# strata})$
   (heeringa2010applied, p.~85).
2. **Replication — BRR, jackknife, bootstrap.** Build empirical
   sampling distributions by resampling PSUs. BRR balances half-samples;
   jackknife drops one PSU at a time; bootstrap resamples with
   replacement. Handles nonlinear statistics natively without
   distributional assumptions (heeringa2010applied, p.~87).

**Ultimate-cluster principle.** Treat the first-stage units (PSUs) as
the variance-bearing objects regardless of how many sub-stages
followed (heeringa2010applied, p.~88):

> "This greatly simplifies variance estimation through the use of
> formulae for stratified, with-replacement sampling of ultimate
> clusters of observations."
> (heeringa2010applied, p.~88)

**Practical guidance for the Analyst:** always use survey-aware
variance estimators (e.g. R `survey`, Python `samplics`, Stata `svy`)
on any complex-sample dataset. Do not report unweighted means or
naive SEs as headline findings — they will be wrong.

---

## 6. Decision flowchart for the Askalot platform

Given a brief from the customer (for a Project, start with *Sizing a
Project* below: the evidence and the saved plan come first):

1. **Frame audit.** Is the frame a clean list, a panel, or inferred?
   Web panels are convenience samples — weighting can reduce bias but
   never eliminates selection effects entirely.
2. **Precision requirement.** Half-width $d$ on what estimator, for
   what subgroup, at what confidence? The formulas below explain the
   arithmetic; do not do it by hand. Give `plan_sample_size` the goal
   targets and it returns the completes needed, the oversample factor and
   the number to invite.
3. **Subgroup requirements.** Does the customer care about
   subgroups? If yes — stratify and oversample. Budget the
   $L_w \approx cv^2(w)$ variance cost into the sample-size plan.
4. **Pick a DEFF anticipation.** For a Project, take it in the order
   `references/sizing-proposal.md` gives: the newest Study's results block,
   then the paper's sampling text, then a library figure, then the textbook
   default of 1.0. With none of those and a design you know will lose
   precision, propose 1.5 for a lightly-stratified panel, 2.0+ for
   oversampling, 3.0+ if clustering is unavoidable, as a value the user
   confirms, never tagged `textbook_default`.
5. **Compute $n$.** $n = n_{\mathrm{SRS}} \cdot D^2$ is what
   `plan_sample_size` computes (normal approximation, two-sided, per-goal
   completes rounded up before $D^2$ is applied). Call it with the goals'
   targets, `eligibility_rate`, `response_rate` and `design_effect`; all
   three are required, and a past wave's design effect comes from the newest
   Study's results block, never from a Bundle. Saving the plan is the user's
   decision (*Sizing a Project*, step 6).
6. **Plan weighting from the start.** Which frame variables drive
   design weights? Which external benchmarks will support
   post-stratification / raking? Targets must be defensible and
   current — mismatched targets create post-hoc bias.
7. **Tell the customer the effective sample size.**
   $n_{\mathrm{eff}} = n / D^2$ is what they're actually buying, and
   it's almost always smaller than the number on the invoice.

---

## Sizing a Project: the evidence and the saved plan first

Before giving sizing or fielding advice on a Project:

1. **Read what the plan rests on.** Call `get_sizing_evidence(project_id,
   strategy_id?)`: each goal with its own passage, the `target_audience` and
   `sampling_strategy` text, the newest non-stale Study's results block (the
   last wave's yield, design effect and each KPI's usable responses, observed
   share or spread and achieved margin) with that Study's *Across waves*
   passage, and with a Strategy its factor shares and eligible frame. It
   reads no campaign, survey or Bundle: a past wave speaks only through the
   paper. Call `plan_sample_size(project_id, ...)` too: its
   `saved` record holds the saved targets, their planning context and each
   value's `provenance` (source, citation, whether it needs confirmation, who
   confirmed it). A saved plan is where you start; say what you would change
   and why, rather than proposing from scratch.
2. **Propose by the shared rules** in
   [references/sizing-proposal.md](references/sizing-proposal.md): the source
   tags, how a target is read from a goal's prose, the newest Study's
   results block before the library before a textbook default, and the
   defaults table. Each goal is sized on its own and the largest need sets
   the size; a KPI that only part of the completes answer (a question asked
   only of car owners) is sized through its group share, a Strategy factor's
   or, for a group no factor holds, the share the paper states (a `paper:`
   key, always *check this*), so it needs more completes. Follow that
   file, not this skill's rules of thumb, so you and the planner's own
   proposal reason from the same evidence by the same rules.
3. **Ground the library values.** Search the methodology library
   (`search_methodology_library`, e.g. "response rate by survey mode",
   "design effect cluster sampling") and cite each passage you use by author,
   year and the `paper_id` the result names for its chunk; that is the
   `library` tag's citation.
4. **Show the numbers.** Run `plan_sample_size` on the values, so the user
   sees completes and invites with every value's tag.
5. **Confirm only what the user says.** Both rates, every group share and
   every value marked `needs_confirmation` (*check this*) are the user's
   decision. Ask. Mark a value `confirmed_via: "agent"` in the
   `save_sizing_targets` provenance only when the user has stated or accepted
   that value in this conversation, never on your own judgement; the save
   records the user as the one confirming it and is audited. A save with an
   unconfirmed value is refused, naming it.
6. **Save on request.** Call `save_sizing_targets` when the user asks to
   save, with `base_revision` set to the `revision` `plan_sample_size`
   returned (a stale one is a conflict: read again and re-apply). The save
   also writes the paper's "Sample size" block. The researcher can review the
   saved plan on the Size Planner page in Targetor.

---

## Worked example — oversampling young adults

The arithmetic below is illustration; for a real Project pass the same goals to `plan_sample_size`.

Customer: 3,000-respondent online survey, US general adults, wants
95% CI half-width 3% on a headline proportion but 4% on 18–24 adults
(who are ~12% of the population).

1. Overall $n_{\mathrm{SRS}} = 1.96^2 \cdot 0.25 / 0.03^2 \approx 1,068$.
2. 18–24 subgroup at $d_s = 0.04$: $n_s^{\mathrm{SRS}} = 1.96^2 \cdot
   0.25 / 0.04^2 \approx 600$ young-adult completes.
3. If we allocate proportionally, 12% of 3,000 = 360 — not enough.
4. Oversample 18–24 to get 600 completes; that's 20% of the sample
   vs 12% of the population. The weights are $0.12/0.20 = 0.6$ for young
   adults and $0.88/0.80 = 1.1$ for everyone else (mean 1), so
   $cv^2(w) = 0.20 \cdot 0.6^2 + 0.80 \cdot 1.1^2 - 1 = 0.04$
   — a modest weighting loss.
5. Effective sample size for headline estimates
   ≈ $3000 / 1.04 \approx 2,885$. Tell the customer up-front.

---

## Quick answer cheatsheet

| Customer asks… | Answer this way |
|---|---|
| "How many respondents do I need?" | For a Project, read `get_sizing_evidence` and the saved plan first (*Sizing a Project*); then call `plan_sample_size` (SRS precision inflated by DEFF, subgroup and two-group goals included), explain its justification, and call out subgroup requirements. |
| "Why is the subgroup estimate wobbly?" | Effective sample size for that subgroup — show $n_{\mathrm{eff}}$. |
| "Is raking doing anything?" | Compare Bronze vs Silver quality metrics on the raked factors. If RMSE went up, the implementation is wrong. |
| "Why can't we just ignore the weights for the regression?" | Naive SE underestimates variance under complex samples; use `svyglm` or equivalent. |
| "What's a good DEFF?" | < 2.0 is routine for stratified designs; > 3.0 means revisit weights or clustering. |
| "Can we oversample the priority segment?" | Yes — plan for $cv^2(w)$ weighting loss; show the sample-size tradeoff. |
