---
name: answerability-chain
description: Use when acting as Designer, Manager, or Analyst and you have edited (or are about to act on) a paper chain unit — research_goals/kpis/motivation, the campaign-design sections, or data_quality_assessment. Covers how to gather the inputs, call the read-only answerability_chain MCP tool, and act on the graded verdict before continuing.
---

# Answerability Chain

A research goal is *answerable* only if an unbroken chain holds across the
paper's chapters: **goal → audience → sampling/quota → instrument →
collected data → quality-sufficient**. The chain is a read-only derivation
over the existing paper — it never changes the paper or any proposal. The same
evaluator is the post-collection
`research-evaluator` pass; this is the *continuous, cross-agent* view of the
same relationship, not a separate mechanism.

## When to consult it

Call `mcp__plugin_askalot_askalot__answerability_chain` **within your turn,
right after you change a chain section and before you continue**:

- **Designer** — after editing `research_goals`, `kpis`, `motivation`,
  `target_audience` or `semantic_clustering_candidates`, or after
  producing/altering QML.
- **Manager** — after editing `sampling_strategy`,
  `respondent_pool_quality` or `data_collection_plan`, **before launching
  a campaign** (a `pre_launch` break must gate the spend).
- **Analyst** — before proposing `data_quality_assessment` and stating the
  verdict (the Analyst proposes that chapter; it does not edit the paper).

A missed break is worse than a redundant check — when in doubt, consult it;
do not wait for an explicit request and do not defer it to the Analyst's
terminal pass. Do not remediate on your own: the chain attributes breaks, and
you report them (below) so the researcher decides what to change.

## Surfacing a break

**Direct call.** Call the chain tool yourself, inside the turn that made the
chain-section change. A sub-agent's call does not count: its result reaches
you as prose at best.

**Confidence bar.** The tool does not use your `confidence` and does not
return it; you apply it when you report a break, to keep frequent checks from
becoming noise:

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

1. Read the current paper (`read_paper`) and the project's QML
   (`inspect_qml_file` / `get_qml_content`). Every call names `project_id`.
2. Build `goals_association`: one entry per `RQ-*`/`KPI-*`/`SC-*`/`REQ-*`
   the `research_goals`, `kpis` and `motivation` units name (the tool grades
   the goals it finds in those three units; one you give no entry for comes
   back `Not` with an `instrument` break):
   `{goal_id, qml_refs:[...], data_refs:[...], confidence:0–1,
   rationale, coverage:"full"|"partial"}`. `goal_id` and `confidence` are
   required. Give confidence as a number (`0.85`), or as `low` (0.25),
   `medium` (0.5) or `high` (0.85); "low confidence" in this skill means
   anything under 0.5. Use `coverage:"partial"` when
   only some sub-questions of the goal are covered — never collapse a
   partially-answerable goal into a dead one.
3. Pass `instrument_items` (`{ref, prompt_text, kind, is_open_ended,
   coding_unit_key}`), one per QML item. A `qml_refs` entry counts as
   coverage only when it equals the `ref` of an item you pass here (and a
   `data_refs` entry only when it equals a `data_dimensions` `ref`); a ref
   that matches nothing is dropped, and a goal left with none reads as an
   `instrument` break. The items also drive the orphaned-instrument list
   and the analyzability link. `coding_unit_key` is optional and only matters for an
   open-ended item: it is the codable unit the item's answers land in, as
   `get_bundle_coding` lists it. Supply it when the item sits in a Roster
   (whose iterations pool into one unit) or is one slot of a composite
   item; otherwise leave it out and the ref is the unit. Pass
   `data_dimensions` (`{ref, description}`) for goals answered by recorded
   data rather than a QML item; that counts as coverage too.
4. Pass `campaign_context` only with what you actually resolved from the
   campaign/pool/strategy entities. Its keys, all optional:
   - `campaign_present`, `data_collected` (booleans, default false). The
     audience and segment checks run only when one of them is true.
   - `audience_segments` — the segments the paper's target-audience unit names;
     `recruitable_segments` — those the Pool or quota plan can actually
     reach; `required_segments_by_goal` — `{goal_id: [segments]}` the goal
     needs. A required segment missing from the audience breaks `audience`;
     one in the audience but not recruitable breaks `sampling`.
   - `insufficient_data_goals` — goal ids whose collected data is too thin
     (breaks `data`); `quality_invalidated_goals` — goal ids a quality
     finding invalidates (breaks `quality`).
   - `selected_coding_units` — step 5.

   Omit it for a pre-campaign paper — audience and recruitment
   are then reported *indeterminate*, not falsely broken. Do not re-run
   quota math; consume what `field-supervisor`/the entities give.
   Precision is not an input: the tool checks each goal's saved sizing
   target against the planned completes of every campaign Pool of the
   Project (or, with no Pool yet, the eligible frame counted when the plan
   was applied) and breaks `sampling` for a goal the plan cannot meet,
   before any campaign exists. A Project with no saved targets gets no
   precision check, which is not the same as every goal being met.
5. Once the project has a Bundle, add `selected_coding_units` to
   `campaign_context`: `get_bundle_coding`'s `selected` passed through as
   it came. Omit the key when there is no Bundle — analyzability is then
   indeterminate — and pass `[]` when the Bundle chose to code nothing,
   which is a real answer and a real break for any goal only free text
   answers. **Do not** invent a per-item "this can be coded" claim: coding
   is a per-Bundle analysis choice a researcher makes in Balansor, not a
   property of the questionnaire, and nothing you can read off the QML
   tells you what was chosen. The same holds for what a free-text item
   holds: `get_bundle_coding`'s `kinds` records the researcher's
   classification (descriptive, nominal or identifier), an unclassified or
   identifier unit cannot be coded, and you cannot classify one. Report an
   unclassified candidate as a gap for the researcher to close, not as a
   finding about the item.

## Reading the verdict

The tool answers `{success, has_paper, structural_only, verdicts, orphaned}`.
`structural_only: true` means the project has no paper, or the paper names no
goal: there are no verdicts, and that is not the same as every goal being
answerable. A `goals_association` entry the tool cannot read is refused as
`validation_error`, naming the field.

Each entry of `verdicts` is
`{goal_id, state, broken_link, phase, newly_broken, evidence}`:

- `state` — `Answerable` / `Partial` / `Not` (graded, never binary).
  `Partial` is a goal you marked `coverage:"partial"` whose chain is intact
  or broken only at `data` or `quality`; any other break is `Not`.
- `broken_link` — the first severed link, checked in this order: `audience` ·
  `sampling` · `instrument` · `analyzability` · `data` · `quality`; `null`
  when none is.
- `phase` — `n/a` when nothing is broken. `pre_launch` breaks gate Manager
  spend now; `post_collection` breaks feed the next round's goal/sampling
  refinement. An `audience`, `sampling` or `instrument` break is `pre_launch`
  until `data_collected` is true, and `post_collection` after. `analyzability`
  is always `post_collection`: it says a goal's open-ended answers were
  left uncoded on this Bundle, which is a finding for the analysis and the
  next round, never a reason to hold a campaign.
- `newly_broken` — not `Answerable` now, and `Answerable` or absent in the
  paper as it stood before the last approved proposal that changed a chain
  unit; as opposed to a long-standing gap. Surface newly-broken breaks
  prominently. With no approved proposal on a chain unit there is no
  baseline and it is always false.

`orphaned` is a list beside `verdicts`: `{ref, kind}` for each QML item you
passed that no goal traces to. Each is a keep-or-cut scope decision.

**Act on it before continuing your turn:** state the break, which link,
for which goal, whether it is new and whether it is pre-launch. A
`pre_launch` break on the Manager's path means *do not launch yet*. A
low-confidence association (your `confidence` was low) is advisory, not a
hard chain break — say so rather than over-claiming.

## Why it works this way (rationale)

If you are tempted to "freeze the paper once goals are set", add a
"confirm scope before proceeding" gate, or stash cross-agent state in a
side JSON — don't. Those are deliberately rejected:

- The paper is **mutable by design**. The research spiral is
  bidirectional: findings and analysis lessons feed goals; QML evolution
  feeds scope. A frozen contract would break the loop the product exists
  to run.
- The HITL point is the **post-hoc `brief_proposals` review**, not a
  pre-flight scope interrogation — that fits the single continuous-thread
  UX.
- There is **no shared-state blackboard**. The chain is a read-only
  derivation over the paper + proposal history; "newly-broken"
  is recomputed by replay, never stored. A side JSON would re-introduce a
  dual source of truth.

You consume the verdict; you never build a parallel mechanism to compute
or store it.

## Scope

**Covers**: when to call the tool, how to shape its inputs, how to read
and act on the graded verdict, and why the surrounding design rejects
frozen states / pre-gates / orchestration JSON. **Does not cover**: the
verdict computation (done by the tool — you never re-derive it),
editing the paper (the `paper-authoring` skill), or remediation (a human
decision).
