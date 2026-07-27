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

- `get_bundle_quality` (bundle_id) -- The Bundle's three-measure quality story: (1) fielded respondents (Bronze) vs the current Sampling Strategy, with a per-campaign breakdown, (2) weighted respondents (Silver) vs the Bundle's Calibration Targets (an editable weighting spec, NOT the live Strategy -- reassigning the Strategy moves measure 1 but never measure 2), (3) response quality (entropy, straightlining, Cronbach's alpha, acquiescence). Non-measurable parts (ad-hoc voluntaries, missing Calibration Targets) are reported explicitly, never averaged over.
- `compare_bundle_quality` (bundle_id) -- Bronze vs Silver comparison for the Bundle's own chain, showing weighting improvement
- `assign_bundle_strategy` (bundle_id, strategy_id) -- Assign or clear the Bundle's current Strategy (the Bronze measure grades against it; null clears)
- `advance_sampling_strategy` (strategy_id, factors) -- Clone a strategy and append reality-grounded outcome factors (e.g. a party-preference benchmark from survey responses); the original is never edited

## Bundle Pipeline (Bundle-scoped datasets)

Datasets belong to a **Bundle** — a named binding of project + questionnaire +
campaign subset to one linear Bronze → Silver → Gold chain. Coding runs before
weighting; every dataset op targets the Bundle (no free dataset selection).

- `create_bundle` / `list_bundles` / `clone_bundle` / `delete_bundle` -- Bundle lifecycle
- `create_bronze_dataset` (bundle_id) -- Extract the Bundle's raw Bronze
- `code_open_ends` (bundle_id) -- Bronze → Silver: code open-ends, then rake on the coded case base. Returns the Silver in `processing`; poll `get_dataset` until `ready`. (Weighting a non-Bronze source is inexpressible — this is the only Silver-producing tool.)
- `create_gold_dataset` (bundle_id) -- Refine the Bundle's ready Silver into Gold

## What Is NOT Available (Use Reasoning Instead)

The platform does not yet compute: R-indicator, response propensities, cost functions, or adaptive allocation optimization. Use the campaign-strategy skill to reason about these concepts and advise the user on strategy decisions, but do not claim you can calculate them.
