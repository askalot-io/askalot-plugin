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

## Interviewer Management

- `add_interviewers_to_campaign` / `remove_interviewers_from_campaign` -- Assign interviewers
- `assign_respondents_to_interviewer` / `unassign_respondents_from_interviewer` -- Distribute workload
- `get_interviewer_workload` -- Check assigned respondents and status
- `get_unassigned_respondents` -- Find respondents needing assignment

## Quality Assessment (Post-Collection)

- `get_dataset_quality` -- Representativeness metrics (RMSE, MAE, Chi-Square, Max Deviation) comparing sample to strategy targets
- `compare_dataset_quality` -- Bronze vs Silver comparison showing weighting improvement
- `get_dataset_response_quality` -- Response patterns: entropy, straightlining, Cronbach's alpha, speeding, acquiescence
- `create_bronze_dataset` -- Extract raw survey data
- `apply_raking` -- Post-stratification weighting -> Silver dataset

## What Is NOT Available (Use Reasoning Instead)

The platform does not yet compute: R-indicator, response propensities, cost functions, or adaptive allocation optimization. Use the campaign-strategy skill to reason about these concepts and advise the user on strategy decisions, but do not claim you can calculate them.
