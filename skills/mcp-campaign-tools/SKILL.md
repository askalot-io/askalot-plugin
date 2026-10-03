---
name: mcp-campaign-tools
description: Use when managing survey projects, campaigns, sampling strategies, respondent pools, or quality assessment via Askalot MCP tools.
---

# MCP Campaign Management Tools Reference

## Scope

**Covers**: Project setup, campaign creation, sampling strategy design, pool generation, survey operations, interviewer management, and quality assessment via Portor MCP server.

**Does not cover**: QML questionnaire generation, document analysis, survey completion.

## Three chains have one call each

Each of the three sequences below is also a single tool. They are not shortcuts
that skip anything: every step is the same registered tool you would call by
hand, so the same rows are written, the same audit events land, and every
refusal the raw tool gives you is given here unchanged -- plus `stopped_at_step`,
naming which step a stop came from. Nothing unwinds: a chain that stops partway
leaves what the earlier steps built, and you resume by calling the remaining
tools yourself.

| Chain | One call | Raw steps it runs |
|---|---|---|
| Prepare a campaign for fielding | `prepare_campaign_fielding(campaign_id, admits_volunteers, strategy_name, target_size)` -- `target_size` is the pool draw's requested size; the draw settings go to the pool, not the strategy | `create_sampling_strategy` -> `generate_pool_from_strategy` -> `assign_pool_to_campaign` -> `publish_qml_file` -> `bulk_create_surveys` |
| Simulate a campaign's responses | `simulate_campaign_responses(campaign_id, distribution, profiles, max_surveys)` | `bulk_create_surveys` -> `mass_fill_surveys` (returns a `task_id`; poll `get_task_status`) |
| Run the dataset chain | `run_bundle_pipeline(bundle_id, include_demographics, gold_name)` | `create_bronze_dataset` -> `code_open_ends` -> `create_gold_dataset` (returns a `task_id`; poll `get_task_status`) |

Two things to know before you use them:

- **`prepare_campaign_fielding` stops one step short of the send.** It does not
  call `send_campaign_invitations`, and that is deliberate: putting the send
  inside a chain would make "prepare the fielding" indistinguishable from
  "mail every respondent", and mail cannot be unsent. You send explicitly, as a
  separate decision, after reading what the chain returned. It also runs
  `publish_qml_file`, which a hand-built chain routinely forgets -- a campaign
  fielding an unpinned questionnaire serves whatever the head says at each
  moment.
- **A chain is a capability boundary, not a convenience wrapper.** The composite
  re-asks each step's capability before running it, so a caller who cannot
  afford step four is refused *before* step one rather than handed a half-built
  fielding. That is the opposite of the `?toolsets=` selector in the connection
  URL, which scopes what you see and grants nothing.

## Project & Campaign Setup

- `create_project` -- Create research project with clear objectives
- `create_questionnaire` -- Register QML questionnaire
- `create_campaign` -- Create data collection campaign. `offers_ai_channel` is required with no default (whether respondents may also answer in their own AI assistant); when true, `intro_text` and `consent_text` are required too
- `send_campaign_invitations` -- Send survey invitations via email

## Sampling Strategy

- `create_sampling_strategy` -- Define the target population (demographic factors and their target distributions) and how fit is graded (`quality_metric`). A strategy carries no draw setting: size, oversample, algorithm, email requirement and exclusions belong to each pool draw
- `create_default_strategy` -- Quick setup with standard gender + age factors
- `update_sampling_strategy` -- Adjust factors, targets, or the quality metric
- `list_sampling_strategies` -- Browse existing strategies
- `get_sampling_strategy` -- Inspect strategy details and factor configuration

## Respondent & Pool Management

- `create_respondent` -- Add individual respondents
- `generate_pool_from_strategy` -- Draw a pool from a strategy. `requested_size` is required; `oversample_factor` (default 1.0, >= 1), `selection_algorithm` (`greedy` default, or `random_constrained`), `require_email` (default false) and `exclude_respondent_ids` (default none) are optional. The pool stores these settings, so one strategy can feed a 200-person pilot and a 1,000-person main wave
- `preview_pool_generation` -- Same draw inputs, nothing persisted (dry run); reports `requested_size`, `effective_size` (requested x oversample) and `eligible_count`
- `refresh_pool_from_strategy` (pool_id) -- Redraw with current respondent data using the pool's own stored settings; it takes none. To draw at a different size, generate a new pool
- `assign_pool_to_campaign` -- Link pool to campaign
- `add_respondents_to_pool` / `remove_respondents_from_pool` -- Manual pool adjustments

## Survey Operations

- `bulk_create_surveys` -- Create surveys for all campaign respondents
- `list_surveys` -- Monitor completion progress
- `list_campaigns` -- Track active campaigns

`bulk_create_surveys`, `bulk_delete_respondents`, and `bulk_delete_surveys`
are also REST-projected (dual-projection); the bulk-delete tools default to
`dry_run=true`. For a task that needs to filter/decide/write across many
entities (not just one bulk call), see the `gateway-routing` skill for when
to drive a REST code-execution loop instead of iterating individual MCP
calls.

## Interviewer Management

- `add_interviewers_to_campaign` / `remove_interviewers_from_campaign` -- Assign interviewers
- `assign_respondents_to_interviewer` / `unassign_respondents_from_interviewer` -- Distribute workload
- `get_interviewer_workload` -- Check assigned respondents and status
- `get_unassigned_respondents` -- Find respondents needing assignment

## Quality Assessment (Post-Collection, Bundle-scoped)

- `get_bundle_quality` (bundle_id) -- The Bundle's Representativeness story: one sample traced from design intent to deliverable. (1) `selection` Strategy -> Pool: did sampling achieve the design? (2) `fielded` Strategy -> Actual: how far off was the realized base before weighting, with a per-campaign breakdown. (3) `weighted` Strategy -> Weighted: did weighting recover the design? Graded against the SAME Strategy as (2), so the two differ by exactly what weighting recovered. (4) `fielding_shift` Pool -> Actual: what fielding itself contributed -- Pool-referenced, so never read it as a fourth point on the Strategy scale. (5) `response`: entropy, straightlining, Cronbach's alpha, acquiescence. Plus `excluded_profile`: who the completeness threshold removed, compared against who it kept. The Calibration Targets are the weighting INSTRUCTION, not a benchmark -- a weighting that targeted none of the design reads as `no_weighted_factors`, not as a perfect score. Non-measurable parts are reported explicitly with a reason, never averaged over and never scored zero.
- `compare_bundle_quality` (bundle_id) -- Bronze vs Silver for the Bundle's own chain. Read its `recovery` field: composite error closed over the factors measured on both sides, comparable across Bundles. Null with a `recovery_reason` means the two shared no measured factor -- report that as "not comparable", never as "weighting achieved nothing".
- `assign_bundle_strategy` (bundle_id, strategy_id) -- Assign or clear the Bundle's current Strategy (all three Strategy-referenced measures grade against it; null clears)
- `advance_sampling_strategy` (strategy_id, factors) -- Clone a strategy and append reality-grounded outcome factors (e.g. a party-preference benchmark from survey responses); the original is never edited

## Bundle Pipeline (Bundle-scoped datasets)

Datasets belong to a **Bundle** — a named binding of project + questionnaire +
campaign subset to one linear Bronze → Silver → Gold chain. Coding runs before
weighting; every dataset op targets the Bundle (no free dataset selection).

- `create_bundle` / `list_bundles` / `clone_bundle` / `delete_bundle` -- Bundle lifecycle
- `create_bronze_dataset` (bundle_id) -- Extract the Bundle's raw Bronze
- `get_bundle_coding` (bundle_id) -- The Bundle's coding state BEFORE deriving Silver: `candidates` (every open-text unit its Bronze offers, each `{unit_key, title, control_type, roster_block_id, columns}` -- a Roster is ONE candidate covering all its iterations), `kinds` (the researcher's classification of each candidate: `descriptive` = prose coded by meaning, `nominal` = a fixed vocabulary coded by exact value, `identifier` = names a person or record and is never coded; a candidate with no entry is UNCLASSIFIED and `null` means none has been classified), `selected` (`null` = nobody has chosen yet, `[]` = "code nothing" -- a real decision), `discovered` columns keyed by UNIT, `units` (per unit: the dimensions proposed for it with their categories, which are `selected`, whether anyone has `reviewed` it, and `degraded` -- true when the round had no LLM credential and grouped the answers instead of reading the question), `awaiting_review` (selected units nobody has decided about), and `pending_review`, true while either decision is open. **You can read this and you can write the UNIT selection. You cannot classify a column, select dimensions, rename them, or edit their categories -- there is no tool for any of it on any transport, and there will not be: what a column holds and which proposed axes matter are the researcher's judgements.** A nominal unit's categories come back as ids with counts and no labels, because each label would be a respondent's answer Report `awaiting_review` to the researcher and let them decide in Balansor. No verbatim respondent answers come out of this tool
- `set_coding_selection` (bundle_id, selected) -- Set which open-text units this Bundle codes. **Present the candidates to the researcher and write the answer they give you -- never choose on their behalf.** What an open-text column holds is the researcher's classification, made in the Balansor picker from evidence about the answers, and you cannot make it: a candidate is selectable only once it is classified `descriptive` or `nominal`. A unit that is unclassified or classified `identifier` is refused with the reason -- do not retry it, tell the researcher which columns need classifying in Balansor. Present the candidates with their `kinds` and never choose. A numeric question is never a candidate, so do not go looking for one. Takes the FULL replacement set of `unit_key` values; `[]` means "code nothing". Requires the manager role and a user identity, which rejects a service-token-only caller but NOT you -- your session carries the researcher's id, so nothing server-side stops you selecting on your own. That makes the instruction above the only thing standing between a researcher and a codebook they never asked for. A change invalidates the current Silver and applies on the next derive. **Dropping a unit from the set discards the researcher's dimension selection for it immediately** -- the proposed dimensions and their renames survive, but the decision about which become columns does not, and re-adding the unit leaves it awaiting review again. So a selection edit is never a safe way to "try something": send the full set you intend, and when you are only adding a unit, send the existing ones back with it
- `code_open_ends` (bundle_id) -- Bronze → Silver: code the selected units, then rake on the coded case base. Returns the Silver in `processing`; poll `get_dataset` until `ready`. (Weighting a non-Bronze source is inexpressible — this is the only Silver-producing tool.) With nothing selected it skips coding and rakes -- no error, so check `get_bundle_coding` first rather than reading an uncoded Silver as a failure. **A selected unit whose dimensions nobody has reviewed produces NO coded column and the derive still SUCCEEDS** -- check `awaiting_review` before reporting a Silver as complete, or you will hand back a file quietly missing exactly the coding that was asked for. It IS refused when a Calibration Target names a coded column whose dimension (`weighting_factor_dimension_deselected`) or whose whole unit (`weighting_factor_deselected`) is no longer selected -- re-select it or drop the factor
- `create_gold_dataset` (bundle_id) -- Refine the Bundle's ready Silver into Gold
- `get_dataset_schema` (dataset_id, columns?, detail?) -- The column schema, which `get_dataset` does NOT carry: `get_dataset` is the poll surface and the schema is the one field that grows with the questionnaire (134 KB on 293 columns). A whole real schema will not fit a tool result, so call with `detail=false` first (every column name and control type, ~7 KB) and then pass the `columns` you need. Needed for exactly two things: which column a Calibration Target should name (and what its `labels` map calls each code), and which columns a Gold operations catalog can rename, remove or reorder

## What Is NOT Available (Use Reasoning Instead)

The platform does not yet compute: R-indicator, response propensities, cost functions, or adaptive allocation optimization. Use the campaign-strategy skill to reason about these concepts and advise the user on strategy decisions, but do not claim you can calculate them.
