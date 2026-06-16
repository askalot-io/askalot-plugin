---
name: campaign-strategy
description: Use when advising on adaptive survey design, sampling strategies, quota design, response propensity optimization, or cost-quality tradeoffs in data collection campaigns.
---

# Campaign Strategy and Sampling Design Knowledge Base

For use by campaign manager AI agents when advising on sampling strategies, quota design, and respondent pool optimization.

## Core Framework: Adaptive Survey Designs

Adaptive survey designs optimize data collection quality by assigning different strategies to different population units based on available information. The framework consists of five key ingredients:

### 1. Survey Strategies (Design Features)

A strategy is a specified set of design features that may involve a sequence of treatments only followed when previous treatments fail. Examples:

- **s₁** = (advance letter 1, web questionnaire, one reminder)
- **s₂** = (advance letter 1, web questionnaire, no reminder)
- **s₃** = (advance letter 2, CATI administered, max 6 call attempts)
- **s₄** = (advance letter 2, CATI administered, max 15 call attempts)

Strategies can vary across:
- Contact mode (mail, telephone, web, face-to-face)
- Survey mode (web, CATI, mail, interviewer)
- Contact timing protocols
- Number of contact attempts
- Incentives and their timing
- Advance letters and reminders
- Interviewer assignment (in face-to-face surveys)

### 2. Population Covariates (X_k and X̃_k)

**Available covariates (X_k)**: Characteristics known before data collection starts
- From registry/frame data or sampling frame itself
- Available for entire population before strategies are assigned
- Examples: age, gender, household type, education, house value, neighborhood urbanization

**Observed covariates (X̃_k)**: Characteristics observed during data collection (paradata)
- Only available for sampled units during fieldwork
- Interviewer assessments of propensity to respond
- Dwelling and neighborhood observations
- Presence of intercom systems
- Contact rates achieved

**Key distinction**: X̃_k known only for sampled units and cannot distinguish subpopulations a priori. X_k must be available in registrations or frame data to be used for pre-data-collection allocation.

### 3. Response Propensities ρ(x, s)

The probability a unit with characteristics X=x will respond when assigned strategy s.

**Estimation requirements**:
- Must be estimated from historic data (previous survey waves, similar surveys, or pilot studies)
- Can derive propensities from earlier phases of the same survey (responsive design approach)
- More uncertain propensities should be treated as random variables for sensitivity analysis

**Response propensity formula**:
```
ρ_x(x) = Σ_{x̃,s} q(x̃|x) p(s|x, x̃) ρ(x, x̃, s)
```

Where overall response propensity combines:
- Population density q(x)
- Strategy allocation probability p(s|x, x̃)
- Strategy-specific response propensities ρ(x, x̃, s)

### 4. Cost Functions c(x̃, s)

Costs associated with assigning strategy s to a unit with characteristics x̃.

**Cost components**:
- **Fixed costs**: Independent of sample size (data collection staff, sampling, processing infrastructure)
- **Variable costs**: Depend on sample size (training, mail/print, interviewer hours, travel expenses, incentives, telephone usage, computer servers)

**Cost structure**:
```
C(p) = C_F + C_v(p)
```

Where C_v(p) = Σ_{x̃,x,s} q(x, x̃) p(s|x, x̃) c(x̃, x, s)

**Key principle**: Restrict cost functions to design features that are varied. When optimizing incentive differentiation, omit traveling costs. When optimizing contact protocol, traveling times and costs play a dominant role.

**Real-world example** (Dutch Survey of Consumer Satisfaction):
- Monthly telephone survey with 1,500 household sample
- 60 interviewers with 280 household contacts per interviewer average
- Interviewer participation rates: 50% to 79% range (mean 67%)
- Non-contact and refusal are two most influential nonresponse causes
- Of 95% contacted: 71% participate (67% overall response rate)

### 5. Quality Objective Functions

**Response Rate** (simplest covariate-based quality function):
```
Q(p) = ρ̄ = Σ_{x,x̃,s} q(x, x̃) p(s|x, x̃) ρ(x, x̃, s)
```

**R-indicator** (representativeness metric - preferred for multiple uses):
```
Q(p) = R(ρ_z) = 1 - 2S(ρ_z)
```

Where S(ρ_z) is the standard deviation of response propensities:
```
S(ρ_x) = √[Σ_x q(x)(Σ_{x̃,s} q(x̃|x) p(s|x, x̃) ρ(x, x̃, s) - ρ̄)²]

S(ρ_{x,x̃}) = √[Σ_{x,x̃} q(x, x̃)(Σ_s p(s|x, x̃) ρ(x, x̃, s) - ρ̄)²]
```

**Coefficient of Variation** (for population means):
```
Q(p) = CV(ρ_z) = S(ρ_z) / ρ̄
```

**Estimated Nonresponse Bias** (for specific survey variables):
```
Q(p) = cov(Y, ρ_x) / ρ̄
```

With:
```
cov(Y, ρ_x) = [Σ_x q(x) ρ_x(x) (y(x) - ȳ_B)] / ρ̄
```

**Quality function selection guidance**:
- R-indicator: Best for surveys with multiple uses and no specific population parameter. Assumes missing-not-at-random on survey variables.
- Item-based functions: Tailor design to specific survey target variables but require assumptions about nonresponse mechanism.
- Coefficient of variation: Good for population means, independent of adjustment method.
- Focus on process quality (propensity representativeness) rather than product quality (unadjusted means) when auxiliary variables show strong nonresponse patterns.

### 6. Allocation Probabilities p(s|x, x̃)

Decision variables: Probability that population unit with characteristics x and x̃ receives strategy s.

**Constraints**:
```
0 ≤ p(s|x) ≤ 1
0 ≤ p(s|x, x̃) ≤ 1

Σ_s p(s|x) = 1        (all units assigned a strategy)
Σ_s p(s|x, x̃) = 1    (probabilistic allocation)
```

**Benefit of probabilistic allocation**: Allows for random assignment of subpopulations with same scores (increases flexibility for quality-cost tradeoffs).

## The Optimization Framework

### Dual Optimization Problems

**Problem 1: Maximize quality given cost constraint**
```
max_p Q(p)  subject to  C(p) ≤ C_max
```

**Problem 2: Minimize cost given quality constraint**
```
min_p C(p)  subject to  Q(p) ≥ Q_min
```

### Static vs. Dynamic Designs

**Static adaptive designs**: Allocate strategies based on X (registry/frame data) before survey starts
- Example: Assign difficult-to-contact age groups to more intensive phone protocols
- Suitable when: Registry data is comprehensive and predictive

**Dynamic adaptive designs**: Allocate strategies based on X̃ (paradata) observed during data collection
- Example: Re-assign refuses to different interviewers based on propensity assessment (easy/medium/difficult)
- Suitable when: Need to learn effectiveness during fieldwork
- Two phases minimum: Phase 1 identifies effective treatments, Phase 2 applies optimized allocation

### Practical Example: Dynamic Interviewer Re-assignment

**Setting**: Follow-up survey with refusal conversion opportunity

**Input data** (Dutch Consumer Satisfaction Survey):
- Sample size: n = 2,000
- Total interviewers: M = 80
- Max workload per interviewer: c = 30 cases
- Age distribution: 50% young, 50% old
- First phase results:
  - Young refusal types: Easy (50%), Medium (60%), Difficult (70% refusal probability)
  - Old refusal types: Easy (20%), Medium (30%), Difficult (40% refusal probability)
  - Cooperation rates if re-contacted: μ(easy) = 0.85, μ(medium) = 0.80, μ(difficult) = 0.76 (young); 0.95, 0.93, 0.91 (old)
- Interviewer split: 75% good performers, 25% less good

**Optimal allocation result**:
- Good interviewers: 83% assigned to medium-difficulty young cases, all easy young cases
- Less good interviewers: All difficult cases regardless of age, remaining old cases
- R-indicator improvement: 0.749 (random) → 0.827 (optimal) — 10.4% quality gain
- Response rates: 70.1% (random) → 72.0% (optimal)
- Coefficient of variation: 0.117 (regular) → 0.035 (re-assignment) → 0.034 (with interview time adjustment)

**Key finding**: Most re-assignments are deterministic (p(s|x, x̃) = 0 or 1), except young-medium-difficulty cases where mixed strategy (0.83 good, 0.17 less good) is optimal.

## Concrete Rules of Thumb for Campaign Design

### Response Rate Benchmarks by Mode

**Telephone surveys** (CATI):
- Base response rate target: 60-70% with standard protocol
- With optimized interviewer allocation: 70-72% achievable
- Interview participation rate variance: 50-79% across interviewers (mean 67%)
- Contact rate: 95% typical for general population samples

**Web surveys**:
- Lower response rates than telephone (60% gap exists)
- Higher quality-cost differential: cheap but lower propensities
- Best for: Mixed-mode designs targeting easy-to-reach subpopulations

**Mail surveys**:
- Support mode for web in mixed designs
- Lower response rates than telephone or face-to-face
- Higher quality-cost differential than telephone

**Face-to-face surveys**:
- Highest response rates but highest costs
- Travel costs dominate variable costs
- Re-assignment of interviewers difficult due to geographic clustering
- Within densely populated regions, re-assignment is feasible

### Quality Targets by Survey Type

**Panel surveys** (repeated measurements):
- Attrition is critical: target 85%+ retention per wave for longitudinal validity
- R-indicator target: 0.70+ to control differential nonresponse across waves
- Adaptive design most effective: historic response propensities from prior waves are strongest

**One-time surveys** (limited pilot data):
- Use uncertainty in propensity estimates: treat as random variables, run sensitivity analyses
- Responsive design preferred: learn from early phases, adapt subsequent phases
- Start conservative on allocation (avoid over-optimistic propensity assumptions)

**Repeated cross-sectional surveys** (ongoing survey program):
- R-indicator target: 0.75+ (better predictive data than one-time surveys)
- Can update propensities quarterly or annually as historic data accumulates
- Re-estimate cost functions regularly: interviewer wages, incentive effectiveness, technology costs change

### Nonresponse Bias Control Thresholds

**When R-indicator approach is reliable**:
- Auxiliary variables show clear stratification (young/old, urban/rural, etc.)
- At least 2-3 variables available for representativeness assessment
- Survey is repeated or has comparable predecessors for propensity estimation

**When item-based bias approach needed**:
- Survey has single key variable (e.g., satisfaction rating)
- Nonresponse mechanism differs across survey topics
- Limited auxiliary data but strong theory about Y-propensity relationship

**Bias estimate formula** (for specific survey variables):
```
Estimated bias ≤ cov(Y, ρ_x) / ρ̄
            = [Σ_x q(x) ρ_x(x) (y(x) - ȳ_B)] / ρ̄
```

Interpret as: If respondents differ from nonrespondents on Y proportional to their propensity differences, bias will be minimized when propensities are balanced across X.

### Cost-Quality Trade-offs

**Linear programming approach**:
- For response rate as quality function: linear in allocation probabilities
- Use standard LP solvers (R linprog, SAS proc optmodel, Xpress, Baron, AMPL)
- Feasible for most practical problems with up to hundreds of subgroups

**Nonlinear optimization required when**:
- Using R-indicator or coefficient of variation (nonlinear, nonconvex functions)
- Including response propensity variance in quality function
- Estimating nonresponse bias on specific variables

**Specialized solvers needed**: Xpress, Baron, AMPL for nonconvex problems. May converge to local optima—use sensitivity analysis and multiple starting points.

**Practical constraint**: Adaptive designs work best when
- Strong historic data available (minimize uncertainty in ρ(x, s) estimates)
- Similar surveys provide reference propensities
- Repeated survey program (propensities update over time)

## Responsive Design Framework (Learning-Based Adaptation)

When limited historic data available, use **responsive design**:

### Two-Phase Approach

**Phase 1: Learning phase** (first 10-30% of fieldwork)
- Use baseline strategy allocation across all sample units
- Collect paradata on contact rates, refusal patterns, interviewer performance
- Estimate propensities ρ(x̃, s) from outcomes observed in Phase 1

**Phase 2: Adapted fieldwork** (remaining 70-90% of fieldwork)
- Re-allocate remaining sampled units and Phase 1 non-contacts based on Phase 1 learning
- Optimize allocation using estimated propensities and cost data from Phase 1
- Monitor convergence toward quality targets

**Trade-off**: Efficiency loss from Phase 1 (conducting some units with non-optimal strategy) versus information gain that enables optimal Phase 2 allocation. Generally breaks even or improves total survey error when response propensity heterogeneity is high.

## Design Feature Interactions and Constraints

### Contact Protocol Optimization (Sequential Design)

Example strategy sequence:
1. Attempt 1: Weekday evening, after 6pm
2. Attempt 2: Weekend, before 5pm
3. Attempt 3: Weekday afternoon, before 6pm
4. Follow-up: After refusal assessment (if difficult), offer incentive

**Key principle**: Sequence high-efficiency attempts first (lowest cost, highest propensity). Reserve expensive treatments (incentives, repeated callbacks, interviewer re-assignment) for hard-to-reach subpopulations identified in early attempts.

### Mixed-Mode Design with Allocation

**Mode selection by subpopulation**:
- Easy-to-reach via web: allocate to web (cheap, fast)
- Difficult-to-reach, high education: allocate to web with phone follow-up
- Difficult-to-reach, lower education: allocate to phone or face-to-face
- Very difficult: face-to-face with incentive

**Constraint**: Interview time consistency. If switching modes mid-survey, standardize questionnaire length to avoid systematic measurement differences across modes.

## Implementation Checklist

### Before Survey Launch

- [ ] Identify key survey variables (Y) for bias assessment
- [ ] Select auxiliary variables (X) available in frame and during fieldwork
- [ ] Determine quality function: R-indicator (general surveys) vs. item-based (single-topic surveys)
- [ ] Estimate response propensities ρ(x, s) from historic data or pilot
- [ ] Cost out each strategy: fixed costs + variable costs per assignment
- [ ] Define strategies S={s₁, s₂, ...} as specific design feature combinations
- [ ] Set constraints: budget C_max OR quality target Q_min
- [ ] Formulate optimization problem and verify feasibility
- [ ] Conduct sensitivity analysis: varies propensity estimates ±20%, examine solution stability

### During Fieldwork (Static Adaptive Design)

- [ ] Monitor allocation coverage: are designed strategy frequencies matching actual assignments?
- [ ] Track propensity accuracy: compare actual response rates by subpopulation against assumed ρ(x, s)
- [ ] Flag large deviations: if actual response rate for subpopulation s deviates >5% from estimate, adjust subsequent allocation
- [ ] Track costs: verify variable costs align with budget projections
- [ ] Assess quality convergence: is R-indicator or target bias magnitude tracking toward goals?

### During Fieldwork (Dynamic/Responsive Design)

- [ ] Phase 1 (first 10-30%): Accumulate paradata X̃_k for all Phase 1 sample units
- [ ] Estimate Phase 1 propensities: fit models for ρ(x̃, s) from Phase 1 outcomes
- [ ] Optimize Phase 2 allocation: use estimated propensities to solve allocation problem for remaining units
- [ ] Re-allocate Phase 1 non-contacts: use Phase 1 learning to decide follow-up strategy
- [ ] Monitor Phase 2 effectiveness: track whether optimized allocation is delivering expected quality gains
- [ ] Adjust in real-time if: actual propensities diverge >10% from Phase 1 estimates OR costs exceed budget projection by >5%

### Post-Survey

- [ ] Document achieved R-indicator and response rate vs. targets
- [ ] Estimate nonresponse bias using final response propensities and design weights
- [ ] Update propensity models for next survey: were Phase 1/early-phase estimates predictive of later propensities?
- [ ] Retain cost data for next survey cycle: actual costs vs. budgeted costs by strategy
- [ ] Publish results by propensity quartile: demonstrate achieved representativeness via auxiliary variable distributions

## Mapping Theory to Available Platform Tools

The adaptive survey design framework above provides reasoning foundations.
Not all concepts are computable on the Askalot platform today. Use this
mapping to ground your advice in what can actually be measured.

### Computable via MCP Tools

| Theoretical Concept | Platform Equivalent | MCP Tool |
|---|---|---|
| Sample representativeness | RMSE, MAE, Chi-Square, Max Deviation vs. strategy targets | `get_dataset_quality` |
| Weighting effectiveness | Bronze vs Silver quality comparison | `compare_dataset_quality` |
| Design effect (DEFF) | 1 + CV²(weights), included in weighting diagnostics | `apply_raking` → diagnostics |
| Effective sample size | n / DEFF | Included in weighting diagnostics |
| Response quality | Entropy, straightlining, Cronbach's alpha, speeder detection | `get_dataset_response_quality` |
| Strategy factor design | Demographic factors with target distributions | `create_sampling_strategy` |
| Pool generation | Greedy (error-minimizing) or random constrained (quota-based) selection | `generate_pool_from_strategy` |

### Reasoning Only (Not Yet Computable)

| Concept | How to Apply Without Tools |
|---|---|
| R-indicator | Use RMSE across all factors as a proxy — low RMSE implies balanced propensities |
| Response propensities ρ(x, s) | Reason from demographic composition: which groups historically under-respond? Recommend over-sampling accordingly |
| Cost functions | Ask the user about per-contact costs by mode. Use the framework qualitatively to advise on budget allocation |
| Nonresponse bias | When quality metrics show systematic under-representation (high max deviation on one factor), explain the bias implications using the TSE framework |
| Adaptive re-allocation | Monitor quality at milestones. If a demographic group is under-represented, advise the user to adjust recruitment — the platform doesn't automate this yet |

### Practical Advice Pattern

When advising on campaign design without adaptive optimization tools:
1. **Over-sample hard-to-reach groups** by 20-30% using `oversample_factor` in strategy
2. **Use greedy selection** (`selection_algorithm: greedy`) to maximize initial representativeness
3. **Check quality at milestones** (25%, 50%, 75% completion) via `get_dataset_quality`
4. **Apply raking** post-collection to correct residual imbalances
5. **Report DEFF** alongside sample size so the user understands effective precision

## References and Further Reading

Key papers for campaign strategy research:
- **Schouten et al. (2013)**: Optimizing quality of response through adaptive survey designs (foundational framework)
- **Groves & Heeringa (2006)**: Responsive design for household surveys
- **Dillman (2007)**: Mail and internet surveys — tailored design method (mode selection guidance)
- **Stantcheva (2023)**: How to run surveys (practical implementation)
- **Cobben et al. (2009)**: Indicators for representativeness of survey response (R-indicator development)
