---
name: answerability-chain
description: Use when acting as Designer, Manager, or Analyst and you have edited (or are about to act on) a paper chain unit — research_goals/kpis/motivation, the campaign-design sections, or data_quality_assessment. Covers how to call the read-only answerability_chain MCP tool, how it reads goal coverage from the item inventory, and how to act on the verdict before continuing.
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

- **Designer** — after editing `research_goals`, `kpis`, `motivation`
  or `target_audience`, or after producing/altering QML or its item
  inventory.
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

**No spurious surfacing.** If a chain-section edit breaks nothing (every
goal still `Answerable`), say so briefly or stay silent and continue — do
not manufacture a finding from a no-op edit. Surface only what changed or
is broken.

## How the instrument step is decided

You do not argue which question answers which goal, and the tool takes no
such argument. It reads the links that are already stated:

- **A KPI is covered when an asked item names it.** Each questionnaire's item
  inventory (`get_questionnaire_inventory`) lists, per item or battery row, the
  `KPI-*` tokens it collects. The tool loads every questionnaire of the project
  that has an inventory and reads those links itself. An entry whose item the
  QML does not ask covers nothing.
- **Which version is read follows the campaigns.** Before a campaign exists the
  chain reads the latest version of every questionnaire. Once campaigns field
  questionnaires it reads only what they field, at the version each campaign
  pinned when it was published, so a question added after launch does not
  count until that campaign is published again, and a questionnaire no
  campaign fields counts for nothing.
- **A KPI is also covered when a data link names it** (step 2 below): a KPI
  answered from panel or derived data has no question.
- **A research question follows its KPIs.** `RQ-n` is covered when at least one
  KPI the paper ties to it is covered, and breaks at `instrument` when it has
  KPIs and none is covered. The tie is read from the paper: the KPI's entry in
  `kpis` names the question it concludes (`Concludes: RQ-n`), the `kpis` unit
  lists each question's KPIs under a heading or first table cell naming the
  question, or the two tokens share a passage. An `RQ-*` the paper ties no KPI to is not judged at this
  step, and neither is any `SC-*` or `REQ-*`: they never read
  `Not @ instrument`.
- **A goal is covered or it is not.** There is no partial state.

So a missing link is fixed where it is stated, not in the call: when a KPI
breaks at `instrument` although a question collects it, the inventory entry of
that item does not name the KPI. Add it with `save_inventory_items` (Designer),
then call the chain again. When no question collects it, that is the finding.

**No inventory.** When no questionnaire of the project has an item inventory,
the answer carries `coverage: "no_inventory"`: nothing states which question
collects which KPI, so the instrument step is skipped for every goal. That is
not a pass. Say that the questionnaire's coverage of the goals is unknown until
an inventory exists; the other links are still judged.

**Unreadable.** When questionnaires have an inventory but none of them could
be read (a QML that does not load, an inventory that does not parse), the
answer carries `coverage: "unreadable"`, and the instrument step is skipped for
every goal in the same way. That is a fault of the read, not a finding about
the instrument and not a missing inventory: report which questionnaires could
not be read (`unreadable_questionnaires`) and do not say an item is missing.

## How to call it

Every call names `project_id`. Everything else is optional.

1. Read the current paper (`read_paper`) so you know the goals the verdict will
   name. The tool grades the `RQ-*`/`KPI-*`/`SC-*`/`REQ-*` tokens it finds in
   the `research_goals`, `kpis` and `motivation` units.
2. Pass `data_links` only for a KPI that is answered from data no question
   collects (a panel attribute, a derived or recorded value):
   `[{goal_id: "KPI-3", ref: "<the data dimension, in your words>"}]`. Each
   `goal_id` must be a `KPI-*` of the paper; a research question, a criterion
   or an unknown token is refused as `validation_error`, naming it. State a
   data link only when the paper or the user says the KPI comes from that
   data, never to silence a break.
3. Pass `campaign_context` only with what you actually resolved from the
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
   - `selected_coding_units` — step 4.

   Omit it for a pre-campaign paper — audience and recruitment
   are then reported *indeterminate*, not falsely broken. Do not re-run
   quota math; consume what `field-supervisor`/the entities give.
   Precision is not an input: the tool checks each goal's saved sizing
   target against the planned completes of every campaign Pool of the
   Project (or, with no Pool yet, the eligible frame counted when the plan
   was applied) and breaks `sampling` for a goal the plan cannot meet,
   before any campaign exists. A Project with no saved targets gets no
   precision check, which is not the same as every goal being met.
4. Once the project has a Bundle, add `selected_coding_units` to
   `campaign_context`: `get_bundle_coding`'s `selected` passed through as
   it came. Omit the key when there is no Bundle — analyzability is then
   indeterminate — and pass `[]` when the Bundle chose to code nothing,
   which is a real answer and a real break for any goal only free text
   answers. Whether a goal is answered only by free text is read from the
   links (an item whose control is a text area), so you state nothing about
   it. **Do not** invent a per-item "this can be coded" claim: coding
   is a per-Bundle analysis choice a researcher makes in Balansor, not a
   property of the questionnaire, and nothing you can read off the QML
   tells you what was chosen. The same holds for what a free-text item
   holds: `get_bundle_coding`'s `kinds` records the researcher's
   classification (descriptive, nominal or identifier), an unclassified or
   identifier unit cannot be coded, and you cannot classify one. Report an
   unclassified candidate as a gap for the researcher to close, not as a
   finding about the item.

## Reading the verdict

The tool answers `{success, has_paper, structural_only, coverage, verdicts,
unreadable_questionnaires}`. `structural_only: true` means the project has no
paper, or the paper names no goal: there are no verdicts, and that is not the
same as every goal being answerable. A structural-only answer carries neither
`coverage` nor `unreadable_questionnaires`, since no questionnaire was read.

`coverage` is one of three values:

- `inventory` — at least one inventoried questionnaire was read, and the
  instrument step is judged from its links.
- `no_inventory` — no questionnaire has an inventory; the step is skipped
  (above).
- `unreadable` — questionnaires have an inventory and none could be read; the
  step is skipped (above).

`unreadable_questionnaires` lists `{questionnaire_id, name, reason}` for each
inventoried questionnaire whose QML or inventory could not be read. Under
`inventory` its links are missing from the verdict, so a KPI only that
questionnaire collects reads as an `instrument` break. The `evidence` of every
goal that breaks there then ends by naming the questionnaires whose items were
not counted: report such a break as unconfirmed and name them, never as an
item the questionnaire lacks.

Each entry of `verdicts` is
`{goal_id, state, broken_link, phase, newly_broken, evidence}`:

- `state` — `Answerable` or `Not`. A goal the instrument step does not judge
  (an `SC-*`, a `REQ-*`, an `RQ-*` with no KPI tie, any goal under
  `no_inventory` or `unreadable`) is `Answerable` unless another link breaks; its `evidence`
  says the step was not judged.
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
- `evidence` — why: the items or data that cover the goal
  (`<questionnaire_id>@<version_id>:<item_id>`, with `#<row>` for a battery row;
  the version is the one that was read), or what
  broke.

Items that serve no stated goal are not part of this answer: the inventory
read reports them (an entry with neither a KPI nor a purpose).

**Act on it before continuing your turn:** state the break, which link,
for which goal, whether it is new and whether it is pre-launch. A
`pre_launch` break on the Manager's path means *do not launch yet*.

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
and act on the verdict, and why the surrounding design rejects
frozen states / pre-gates / orchestration JSON. **Does not cover**: the
verdict computation (done by the tool — you never re-derive it),
editing the paper (the `paper-authoring` skill), or remediation (a human
decision).
