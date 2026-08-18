---
name: mcp-campaign-tools
description: Use when managing survey projects, campaigns, sampling strategies, respondent pools, or quality assessment via Askalot MCP tools.
---

# MCP Campaign Management Tools Reference

## Scope

**Covers**: Project setup, campaign creation, sampling strategy design, pool generation, survey operations, interviewer management, and quality assessment via Portor MCP server.

**Does not cover**: QML questionnaire generation, document analysis, survey completion.

## Project & Campaign Setup

- `create_project` -- Create research project with clear objectives
- `create_questionnaire` -- Register QML questionnaire
- `create_campaign` -- Create data collection campaign
- `send_campaign_invitations` -- Send survey invitations via email

## Sampling Strategy

- `create_sampling_strategy` -- Define demographic factors, targets, selection algorithm (greedy/random_constrained), oversample factor
- `create_default_strategy` -- Quick setup with standard gender + age factors
- `update_sampling_strategy` -- Adjust factors, targets, or algorithm
- `list_sampling_strategies` -- Browse existing strategies
- `get_sampling_strategy` -- Inspect strategy details and factor configuration

## Respondent & Pool Management

- `create_respondent` -- Add individual respondents
- `generate_pool_from_strategy` -- Select respondents using the strategy's algorithm to optimize representativeness
- `preview_pool_generation` -- Preview selection without persisting (dry run)
- `refresh_pool_from_strategy` -- Re-run selection with current respondent data
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
- `get_bundle_coding` (bundle_id) -- The Bundle's coding state BEFORE deriving Silver: `candidates` (every open-text unit its Bronze offers, each `{unit_key, title, control_type, roster_block_id, columns}` -- a Roster is ONE candidate covering all its iterations), `selected` (`null` = nobody has chosen yet, `[]` = "code nothing" -- a real decision), `discovered` columns keyed by UNIT, `units` (per unit: the dimensions proposed for it with their categories, which are `selected`, whether anyone has `reviewed` it, and `degraded` -- true when the round had no LLM credential and grouped the answers instead of reading the question), `awaiting_review` (selected units nobody has decided about), and `pending_review`, true while either decision is open. **You can read this and you can write the UNIT selection. You cannot select dimensions, rename them, or edit their categories -- there is no tool for it on any transport, and there will not be: choosing among proposed axes is judging generated content.** Report `awaiting_review` to the researcher and let them decide in Balansor. No verbatim respondent answers come out of this tool
- `set_coding_selection` (bundle_id, selected) -- Set which open-text units this Bundle codes. **Present the candidates to the researcher and write the answer they give you -- never choose on their behalf.** Which answers are worth a codebook is a research judgement about this analysis, not something readable off the questionnaire: a one-word "how did you feel?" is worth coding and a mailing address is not. The questionnaire does not declare it; every `Textarea` is offered and being offered implies nothing. A numeric question is never a candidate, so do not go looking for one. Takes the FULL replacement set of `unit_key` values; `[]` means "code nothing". Requires the manager role and a user identity, which rejects a service-token-only caller but NOT you -- your session carries the researcher's id, so nothing server-side stops you selecting on your own. That makes the instruction above the only thing standing between a researcher and a codebook they never asked for. A change invalidates the current Silver and applies on the next derive. **Dropping a unit from the set discards the researcher's dimension selection for it immediately** -- the proposed dimensions and their renames survive, but the decision about which become columns does not, and re-adding the unit leaves it awaiting review again. So a selection edit is never a safe way to "try something": send the full set you intend, and when you are only adding a unit, send the existing ones back with it
- `code_open_ends` (bundle_id) -- Bronze → Silver: code the selected units, then rake on the coded case base. Returns the Silver in `processing`; poll `get_dataset` until `ready`. (Weighting a non-Bronze source is inexpressible — this is the only Silver-producing tool.) With nothing selected it skips coding and rakes -- no error, so check `get_bundle_coding` first rather than reading an uncoded Silver as a failure. **A selected unit whose dimensions nobody has reviewed produces NO coded column and the derive still SUCCEEDS** -- check `awaiting_review` before reporting a Silver as complete, or you will hand back a file quietly missing exactly the coding that was asked for. It IS refused when a Calibration Target names a coded column whose dimension (`weighting_factor_dimension_deselected`) or whose whole unit (`weighting_factor_deselected`) is no longer selected -- re-select it or drop the factor
- `create_gold_dataset` (bundle_id) -- Refine the Bundle's ready Silver into Gold

## What Is NOT Available (Use Reasoning Instead)

The platform does not yet compute: R-indicator, response propensities, cost functions, or adaptive allocation optimization. Use the campaign-strategy skill to reason about these concepts and advise the user on strategy decisions, but do not claim you can calculate them.
