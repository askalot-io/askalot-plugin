---
name: questionnaire-logic
description: Use when planning or authoring a questionnaire's skip graph, analyzing reachability or dead-code, reasoning about logical consistency of filters and preconditions, or anticipating what the askalot_qml.z3 static validator will flag. Distilled from the graph-theoretic literature — Fagan & Greenberg (1988), Elliott (2012), Feeney & Feeney (2019), Schiopu-Kratina et al. (2015), Manski & Molinari (2008). Primary audience is the qml-planner sub-agent, but useful for any structural decision in the design-questionnaire flow.
---

# Questionnaire Logic — Graph-Theoretic Reference

The askalot platform validates QML via Z3/SMT — so authoring discipline
that prevents inconsistency pays off twice (the customer gets a
correct questionnaire *and* the validator runs clean on the first
pass). This skill distils the theory and gives you the heuristics
that fall out of it.

Reach for `methodology-library` for deeper proofs or author
comparisons; the five papers below are all in the corpus.

---

## 1. The questionnaire as a directed acyclic graph

**Model.** A questionnaire is a directed acyclic graph (DAG) with a
unique **source** $R$ (first question), a unique **terminal**
$\mathrm{END}$, and arcs $Q_a \to Q_b$ meaning "respondents with some
answer to $Q_a$ proceed to $Q_b$". Nodes are questions; arc labels
are the response(s) that trigger the transition
(fagan1988census, p.~20; schiopu2015survey, p.~286).

> "The questionnaire can be viewed as an acyclic directed graph with
> a source and sink. For each question on a questionnaire we
> associate a node in an associated graph... if some response to
> question Q_t allows a set of questions {Q_s} to be asked next, we
> set up the arc from node N_t to each node {N_s}."
> (fagan1988census, p.~20)

**Connectedness invariant.** For every node $x$: $R$ is an ancestor
of $x$ **and** $\mathrm{END}$ is a descendant of $x$
(schiopu2015survey, p.~286). Violating either side creates a bug:
- No path from $R$ to $x$ → $x$ is unreachable (dead code).
- No path from $x$ to $\mathrm{END}$ → $x$ is a trap (respondent
  gets stuck).

**Waist nodes.** Nodes that appear on *every* maximal path from $R$
to $\mathrm{END}$. Every questionnaire has at least two (the source
and terminal); well-structured questionnaires have waist nodes at
section boundaries. The qml-planner should design toward named waist
nodes — they're natural chapter boundaries and they stabilize
downstream variance analysis (fagan1988census, p.~16–17).

---

## 2. Reachability and dead-code detection

**Definition.** A question $q$ is **reachable** if at least one
consistent answer sequence from $R$ leads to $q$. A set of answers
$S$ is **consistent** if there exists at least one maximal chain
containing every arc in $S$ (fagan1988census, p.~13).

**Fagan–Greenberg algorithm.** The set of questions reachable under
answer set $S$ is the intersection of lower ideals across all
answers in $S$. Computable in $O(\log_2 N)$ multiplications via
successive squaring of the arc incidence matrix
(fagan1988census, p.~8–9, 28). This is cheap enough to run on every
pre-commit save.

> "The set of questions that must be answered given that questions
> corresponding to Q were answered is found by the intersection of
> lower ideals... Each maximal chain containing S corresponds to a
> completed response form."
> (fagan1988census, p.~28)

**Complexity caveat.** Identifying *all* paths is NP-hard in the
general DAG (reduction from Hamiltonian path). But the structured
subclass that survey questionnaires naturally fall into — "skip
trees" with consecutive branching and no back-edges — admits
polynomial DFS-based algorithms (feeney2019logical, p.~259–265).
In practice, complexity scales exponentially in the number of
*independent* branching questions, not in total questions. A
questionnaire with 200 items but only 5 independent branch points
runs in milliseconds.

**Empirical example.** Feeney & Feeney applied the structural-paths
algorithm to the 2008 Malawi Census person questionnaire:
**3,714 structural paths**, of which **160 were logically invalid**
— contradictory filters like `age ≥ 18` AND `age < 6` on the same
path (feeney2019logical, p.~298–300). Real questionnaires *do* carry
these bugs.

---

## 3. Logical consistency — what the Z3 validator will flag

**Definition.** A set of answers $S$ is **inconsistent** if no
maximal chain contains every arc in $S$. An edit check identifies
inconsistent subsets and flags them for correction
(fagan1988census, p.~13).

**Feeney's decomposition.** If a questionnaire is divided into
sections where:
- each section has a unique entry point (first question of section)
- branching within a section does not skip to questions beyond the
  next section,

then the number of paths through the whole questionnaire equals
the **product** of paths per section. This turns exponential
complexity into multiplicative — a well-sectioned 10-section
questionnaire with 3 paths per section has 59,049 total paths but
each section is independently verifiable
(feeney2019logical, p.~589–590).

**The "eligible persons" algorithm** (feeney2019logical, p.~513–536)
processes a progression table in topological order:

```
for each edge (From, Filter, To):
    eligible[To] |= eligible[From] AND Filter(true)
for merge nodes (multiple inbound edges):
    eligible[node] = union over all incoming flows
```

Linear in the number of edges, and produces the exact set of
respondents who can ever reach each question. This is the algorithm
the Z3 validator's reachability pass implements.

---

## 4. Authoring heuristics that fall out of the theory

Five rules every qml-planner output should obey. They're empirically
grounded, not stylistic preferences.

### 4.1 Prefer hub-and-spoke over deep nesting

Deep trees ($Q_1 \to Q_2 \to Q_3 \to \dots$) force many respondents
through long sequences they may not need. Clustering common
questions early (the "hub") and branching to specialised subsections
(the "spokes") reduces **expected questions asked** per respondent.

**Worked example (Schiopu-Kratina 2015, p.~856):** Applying
Transformation 1 (reorder adjacent questions) and Transformation 2
(merge similar questions) to a 25-question employment module dropped
expected questions from 14.889 to 14.40 (3.4%), and a simplified
version down to 10.857 (27% total reduction). Small transformations
compound.

### 4.2 Minimize indegree — merge duplicates

If multiple paths lead to the same logical question (e.g.
"employment status" asked after two different branches), merge the
node. Multi-parent nodes are a common source of logical bugs and
make the graph harder to validate (schiopu2015survey, Transformation 2).

### 4.3 Avoid forward references in preconditions

A precondition on $Q_a$ that references the answer to a *later*
question $Q_b$ (backward arc) violates the DAG property and
introduces ambiguity about evaluation order. The platform's QML Z3
pass treats these as hard errors. Use `qml-preconditions` skill for
the concrete QML patterns that avoid forward refs.

### 4.4 Place high-coverage questions near the root

A question that appears on many paths (high "coverage" in Picard's
sense) should be asked early — it front-loads information the rest
of the questionnaire can filter on, and minimises expected question
count (schiopu2015survey, p.~841, Picard's rule R2).

### 4.5 Keep branching factor modest (≤ 3 outgoing arcs per question)

Hill (1991, 1993, cited in manski2008skip, p.~251–255) found that
**contagion errors** — a mistake on an opening question cascading
through subsequent answers — grow linearly with branch depth. Limit
explicit branching to 2–3 outgoing arcs; beyond that, convert to a
categorical question with a single downstream `case` block.

---

## 5. Skip sequencing as a decision problem

Manski & Molinari (2008) formalise the cost/information tradeoff
when deciding whether to ask item $y$ of *everyone* ($A$), only of
gated respondents ($S$), or no one ($N$):

$$\mathrm{loss}(\text{strategy}) = \text{cost} + \text{informativeness penalty}$$

Under nonresponse rate $\theta$ on the gating question $q$:
- **Ask all ($A$)**: identification-region width $= P(\text{nonresp. to } y)$
- **Skip-sequence ($S$)**: width $= P(\text{nonresp. to } q)
  + P(\text{nonresp. to } y \mid \text{gated})$
- **Ask none ($N$)**: width $= 1$ (uninformative)

Applied to HRS 2006 Social Security expectations data, skip-sequencing
is optimal when the cost coefficient $\gamma$ satisfies
$0.093 \leq \gamma \leq 1.04$; below, ask everyone; above, ask no one
(manski2008skip, p.~461–465). The practical takeaway: skip logic
*adds* a second nonresponse risk (to the gate), so the savings from
not asking downstream questions must justify that cost. Don't
reflexively add skips — they pay off most when downstream items are
expensive or sensitive.

---

## 6. Mapping to `askalot_qml.z3` static validation

The Z3 validator implements (roughly) these passes. Anticipate what
it will flag so qml-planner produces plans that pass on the first
run:

| Pass | What it checks | Theory backing |
|---|---|---|
| Reachability | Every question has at least one path from start under *some* answer pattern | Fagan–Greenberg ideal intersection |
| Dead-code | No question is unreachable under all answer patterns | Feeney's eligibility algorithm |
| Cycle detection | Graph is acyclic (no forward-referencing preconditions) | DAG invariant |
| Consistency | No path carries contradictory filters (e.g. `age<18` AND `employed=true` where `employed` implies `age≥16`) | Feeney's structural-paths check |
| Postcondition feasibility | Every postcondition has at least one satisfying answer | SMT-solver's built-in check |

If you find yourself about to hand a plan to qml-writer that would
trip any of these, revise the plan. Reaching the validator with a
broken structure wastes a full generation pass.

---

## 7. Planning checklist for qml-planner output

Before handing a plan to qml-writer, walk this list:

1. **Source and terminal identified.** First and last questions
   named; the plan specifies what "end of questionnaire" means
   (e.g. submit, thank-you page).
2. **Section decomposition.** Each section has a named entry
   question. No backward branches across section boundaries.
3. **Waist nodes.** Natural section boundaries are waist nodes
   (everyone hits them).
4. **Branch analysis.** Every branching question lists outgoing
   arcs with labels. Branching factor ≤ 3 unless justified.
5. **Precondition domain check.** Every precondition references a
   *prior* question's answer. No forward refs.
6. **Reachability plan.** You can narrate, in a sentence per
   section, under what answer patterns a respondent reaches each
   section.
7. **Dead-code check.** No question is reachable only under
   contradictory filters (e.g. `age<12` AND `employed=true`).
8. **Skip-sequencing justification.** For each skip, the plan
   states why — high nonresponse cost, sensitivity, respondent
   burden. Don't skip reflexively (manski2008skip).

If the plan fails any of these, revise before writing QML. The
validator will catch the error later anyway; catching it earlier
costs less.

---

## Cheatsheet

| Symptom | Root cause | Fix |
|---|---|---|
| Z3 reports unreachable question | Precondition too narrow or upstream branch misses a path | Widen the precondition or add an arc from the missing branch |
| Z3 reports contradictory filters on a path | Section boundary violated — a later filter contradicts an earlier one on the same path | Move the filter to a different section or relax the boundary |
| Deeply nested skip logic | Too many sequential `if` branches | Flatten to hub-and-spoke (§4.1, §4.2) |
| Customer complains respondents get stuck | Missing arc to terminal under some answer pattern | Check the connectedness invariant (§1) |
| High dropout after a gating question | Gate is too aggressive — skip-sequencing net cost exceeds savings | Revisit the gate against Manski's framework (§5) |
