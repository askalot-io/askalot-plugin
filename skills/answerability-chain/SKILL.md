---
name: answerability-chain
description: Use when acting as Designer, Manager, or Analyst and you have edited (or are about to act on) a brief chain section — research_goals/kpis/motivation, the campaign-design sections, or data_quality_assessment. Covers how to gather the inputs, call the read-only answerability_chain MCP tool, and act on the graded verdict before continuing.
---

# Answerability Chain

A research goal is *answerable* only if an unbroken chain holds across the
brief's aspect sections: **goal → audience → sampling/quota → instrument →
collected data → quality-sufficient**. The chain is a read-only derivation
over the existing brief.md — it never mutates the brief, the schema, or the
`brief_proposals` state machine. The same evaluator is the post-collection
`research-evaluator` pass; this is the *continuous, cross-agent* view of the
same relationship, not a separate mechanism.

## When to consult it

Call `mcp__plugin_askalot_askalot__answerability_chain` **within your turn,
right after you change a chain section and before you continue**:

- **Designer** — after editing `research_goals`, `kpis`, or `motivation`,
  or after producing/altering QML.
- **Manager** — after editing `target_audience`, `sampling_strategy`,
  `respondent_pool_quality`, or `data_collection_plan`, **before launching
  a campaign** (a `pre_launch` break must gate the spend).
- **Analyst** — after writing `data_quality_assessment`.

A missed break is worse than a redundant check — when in doubt, consult it.
Do **not** auto-remediate: the chain attributes breaks; the human or the
acting agent decides what to do.

## Round-transition surfacing (cadence)

The spiral has no single "verify now" moment, so surfacing is **always-on,
within your own turn**: every time you change a chain section, consult the
chain *before you continue*. A missed break is worse than a redundant
check — do not wait for an explicit request and do not defer it to the
Analyst's terminal pass.

**Direct call — do not rely on bubbling.** Call the chain tool *yourself*,
inside the turn that made the chain-section change. Do not assume a
sub-agent's tool call will bubble up to surface the break for you; whether
or not it does, R9 is satisfied because *you* called it directly.

**Confidence bar — keep always-on from meaning always-noisy.** Your
association `confidence` per goal is the noise control:

- A break on a goal you associated with **low confidence** is surfaced as
  **"low-confidence, advisory"** — name it as a possible gap to check, not
  as a hard chain break, and do not let it gate Manager spend.
- A break on a goal you associated with adequate confidence is a real
  chain break — surface it as a decision (especially newly-broken and
  pre-launch).

**No spurious surfacing.** If a chain-section edit breaks nothing (every
goal still `Answerable`), say so briefly or stay silent and continue — do
not manufacture a finding from a no-op edit. Surface only what changed or
is broken.

## How to call it

The tool does the deterministic chain logic server-side. You supply the one
LLM-mediated input — your judgment of which QML item or collected dimension
answers each goal:

1. Read the current brief and the project's QML (use the brief read +
   `inspect_qml_file` / `get_qml_content` tools you already have).
2. Build `goals_association`: one entry per `RQ-*`/`SC-*`/`REQ-*`:
   `{goal_id, qml_refs:[...], data_refs:[...], confidence:0–1,
   rationale, coverage:"full"|"partial"}`. Use `coverage:"partial"` when
   only some sub-questions of the goal are covered — never collapse a
   partially-answerable goal into a dead one.
3. Pass `instrument_items` (`{ref, prompt_text, kind, is_open_ended,
   has_coding_path}`) so orphaned instrument and the analyzability link
   are detected. Pass `data_dimensions` for goals answered by recorded
   data rather than a QML item (that still counts — R4).
4. Pass `campaign_context` only with what you actually resolved from the
   campaign/pool/strategy entities (segments, recruitability, precision,
   quality findings). Omit it for a pre-campaign brief — the sampling
   link is then reported *indeterminate*, not falsely broken. Do not
   re-run quota math; consume what `field-supervisor`/the entities give.

## Reading the verdict

Each goal returns `{state, broken_link, phase, newly_broken, evidence}`:

- `state` — `Answerable` / `Partial` / `Not` (graded, never binary).
- `broken_link` — the first severed link: `audience` · `sampling` ·
  `instrument` · `analyzability` · `data` · `quality` · `null`.
- `phase` — `pre_launch` breaks gate Manager spend now; `post_collection`
  breaks feed the next round's goal/sampling refinement.
- `newly_broken` — broke *this round* (replay-and-recompute against the
  last approved chain-section change), as opposed to a long-standing
  deferred gap. Surface newly-broken breaks prominently.
- `orphaned` — QML items tracing to no goal: a keep-or-cut scope decision.

**Act on it before continuing your turn:** state the break, which link,
for which goal, whether it is new and whether it is pre-launch. A
`pre_launch` break on the Manager's path means *do not launch yet*. A
low-confidence association (your `confidence` was low) is advisory, not a
hard chain break — say so rather than over-claiming.

## Why it works this way (rationale)

If you are tempted to "freeze the brief once goals are set", add a
"confirm scope before proceeding" gate, or stash cross-agent state in a
side JSON — don't. Those are deliberately rejected:

- The brief is **mutable by design**. The research spiral is
  bidirectional: findings and analysis lessons feed goals; QML evolution
  feeds scope. A frozen contract would break the loop the product exists
  to run.
- The HITL point is the **post-hoc `brief_proposals` review**, not a
  pre-flight scope interrogation — that fits the single continuous-thread
  UX.
- There is **no shared-state blackboard**. The chain is a read-only
  derivation over the Markdown brief + proposal history; "newly-broken"
  is recomputed by replay, never stored. A side JSON would re-introduce a
  dual source of truth.
- CE (the reference system) is not "linear vs. our spiral" — the real
  difference is loop *radius and cadence*: CE's feedback is cross-project
  and slow; yours is within-project and every-round. Surfacing the chain
  every round is exactly that fast inner loop.

You consume the verdict; you never build a parallel mechanism to compute
or store it.

## Scope

**Covers**: when to call the tool, how to shape its inputs, how to read
and act on the graded verdict, and why the surrounding design rejects
frozen states / pre-gates / orchestration JSON. **Does not cover**: the
verdict computation (single-sited in
`askalot_common.research_brief.answerability` — you never re-derive it),
brief mutation (a separate tool), or remediation (a human decision).
