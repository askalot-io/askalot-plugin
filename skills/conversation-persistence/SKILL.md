---
name: conversation-persistence
description: Use when driving the Manager (run-campaign-simulation) or Analyst (analyze-quality) orchestration flow to persist the turn's events back to the project's `project_conversations` row via the append_conversation_event MCP tool — into the run the host opened, or, with no host, one bracketed by start_run / end_run. NOT for the Designer (design-questionnaire) — the Armiger host writes that timeline in-process. Covers the hosted-run rule, the event shape, the dedup contract, and the per-run event cap.
---

# Conversation Persistence

Persist your turn back to Askalot so the customer can audit the timeline that produced their brief, campaign decision, or quality assessment. Every meaningful step is recorded as a `project_conversation_events` row via `append_conversation_event`, into one run per turn.

## Who opens the run

**A hosted run.** When your first user turn carries a "Conversation persistence (hosted run)" block, the Askalot host already opened this turn's run and closes it when the turn ends, with what the turn cost (which an MCP call cannot report): do not call `start_run` or `end_run`. Append with the `project_id`, `agent_kind` and `run_id` the block names, `event_seq` from 0. If an append answers `run_not_running`, stop appending and open no other run.

**No host** (the plugin in your own Claude Code session): bracket the turn yourself with `start_run` and `end_run`, as described below.

## Scope

**Covers**: who opens the run, when to call each tool, the `event` shape, the `(run_id, event_seq)` dedup contract, the per-run 10 000-event cap, and the retry-on-error rule.

**Does not cover**: project ownership / authentication (the server checks that you may write to the project; you don't manage that), the storage backend, or the pages that show the timeline.

## The three tools

### `start_run`

Only for a turn with no host. Call this **once, at the very start of your turn**, before any other tool calls or sub-agent invocations.

**Arguments:**
- `project_id` (required) — the project UUID. Always the raw UUID (`529eb0bf-57ed-434f-9604-9482d1c5f8f6`), never the RAG workspace identifier.
- `agent_kind` (required) — `manager` or `analyst`, lowercase, matching the flow you are driving. The server also accepts `designer`, but the Designer flow never calls these tools. Any other value, `respondent` included, is refused as `invalid_agent_kind`.
- `run_id` (required) — a fresh UUID4 you generate at the start of the turn. **Reuse the same `run_id` for every subsequent `append_conversation_event` and `end_run` call within this turn.**

It answers `{success, run_id, conversation_id, status}`. The call is idempotent on `run_id`: if you retry on a flaky connection and the run row already exists, the existing row is returned unchanged.

### `append_conversation_event`

Call this **after every meaningful step** in your turn:

- Each MCP tool call (the call itself + the result it returned)
- Each `Agent(sub_agent)` invocation
- Each user-facing reply you produce
- Each significant internal reasoning step you want recorded as "thinking"

**Arguments:**
- `project_id` (required) — the one the hosted-run block names, or the UUID you passed to `start_run`.
- `agent_kind` (required) — the one the hosted-run block names, or the value you passed to `start_run`.
- `run_id` (required) — the UUID the hosted-run block names, or the one you generated at `start_run`.
- `event` (required) — the event dict described below.

It answers `{success: true, stored}`. `stored: false` means an event with that `event_seq` was already recorded and this one was dropped as its duplicate; it is still a success, so move on to the next `event_seq`.

**Event shape:**

```json
{
  "event_seq": 0,
  "role": "assistant" | "user" | "system" | "tool",
  "kind": "user_prompt" | "thinking" | "tool_use" | "tool_result" | "assistant_text",
  "content": "<text body — required for user_prompt, thinking, assistant_text>",
  "tool_name": "<MCP tool name — required for tool_use>",
  "tool_args": { ... },
  "tool_result_preview": "<truncated result body — required for tool_result>"
}
```

The server refuses an event without an integer `event_seq` ≥ 0, a non-empty `role` and one of the five kinds. It does not check the per-kind fields: an event missing its `content` or `tool_name` is stored as it came, so fill them.

**Kind selection:**

| `kind` | When to use |
|--------|-------------|
| `user_prompt` | The customer's incoming message that triggered this turn (event_seq = 0 unless the runtime already wrote it). |
| `thinking` | An internal reasoning step you want preserved. Plain text in `content`. |
| `tool_use` | You're about to call an MCP tool. Put the tool name in `tool_name` and its arguments in `tool_args`. |
| `tool_result` | The MCP tool returned. Put the result body (truncated to readable size) in `tool_result_preview`. |
| `assistant_text` | A user-facing reply chunk. Put the message in `content`. |

### `end_run`

Only for a turn with no host. Call this **once, at the end of your turn**, after the last `append_conversation_event`.

**Arguments:**
- `project_id` (required)
- `agent_kind` (required)
- `run_id` (required) — the same UUID.

The run row transitions from `running` to `closed`, and the call answers `{success, transitioned, status}`. Idempotent on terminal states: calling `end_run` on an already-closed or already-orphaned run is a no-op (`transitioned: false`).

## The dedup contract — never increment on retry

`event_seq` is a per-run monotonic counter starting at **0**. Increment by 1 for each successful `append_conversation_event` call.

**If `append_conversation_event` fails transiently (`internal_error`, another 5xx, or the call failing in transit), retry with the SAME `event_seq` — do not increment.** Every other code is classified below and is not retried unchanged.

The server keeps one event per `(run_id, event_seq)`, which makes same-seq retries safe: a duplicate is dropped silently. If you increment on retry, the server records `seq=N+1` but its earlier write of `seq=N` may or may not have committed, leaving a permanent gap in the visible timeline. Gaps are not a hard error but break the "no skipped tool calls" guarantee the audit surface relies on.

**Response classification:**

- `invalid_event_kind` / `validation_error` / `invalid_agent_kind` — the payload itself is wrong. **Do not retry** unchanged. Fix the event and send it again with the same `event_seq`: a refused event was not stored, so the number is still free.
- `not_found` / `forbidden` — the project does not exist or you may not write to it. **Do not retry**; the same call fails the same way.
- `run_not_running` (HTTP 409) — the run is not open: it ended (a `reset_conversation`, a cancel, or the orphan sweep that takes a run left open past the longest turn), or the `run_id` names no run of this organization. **Do not retry.** Stop appending and open no other run in this turn; the turn is effectively cancelled.
- `run_event_limit_exceeded` (HTTP 429) — the 10 000-event-per-run cap was hit. **Do not retry.** In a hosted run, stop appending. With no host, call `end_run`, start a fresh `run_id` via `start_run`, and continue there; the customer will see two adjacent run rows.
- Transient network error, `internal_error` (HTTP 500), other 5xx — retry with the SAME `event_seq`.

## The per-run event cap (10 000)

Each `run_id` is capped at 10 000 events. Beyond that, `append_conversation_event` returns `run_event_limit_exceeded` (HTTP 429) and refuses further inserts. This protects the server against runaway loops; a legitimate turn rarely emits more than a few hundred events. What to do when you hit it is under *Response classification* above; in the fresh run `event_seq` starts at 0 again.

## The size caps

- `tool_args` — 16 KB serialized JSON. An oversized payload is **accepted and elided**, never rejected: the event is stored with its small identifying arguments intact and each oversize value replaced by a `{"__elided__": true, "bytes": N}` marker. Send the real arguments; do not pre-truncate or summarize them, and do not treat a large payload as an error to handle.
- `tool_result_preview` — 32 KB truncated server-side. Anything longer is silently cut at 32 KB; pass the head of the result.

These caps are per-event, not per-run.

## What NOT to do

- **Do not invent `run_id`s mid-turn.** Use the hosted run's, or generate one UUID4 at `start_run` and reuse it for every subsequent call in that turn.
- **Do not bracket a hosted run.** A `start_run` beside the host's opens a second run the host never closes.
- **Do not set `actor_user_id`.** The server sets it from your authenticated identity; any value you submit is ignored.
- **Do not skip `end_run` when you opened the run.** A run that never closes is eventually flagged `orphaned` by Seneschal's orphan sweep, which surfaces as a red "Incomplete — connection lost" badge in the read surface.
- **Do not call these tools as `respondent`.** Respondent conversations are not persisted; the server refuses `agent_kind="respondent"`.
