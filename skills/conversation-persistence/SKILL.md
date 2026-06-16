---
name: conversation-persistence
description: Use when running as a top-level super-agent (Designer, Manager, Analyst) to persist the turn's events back to the project's `project_conversations` row via the start_run / append_conversation_event / end_run MCP tools. Covers the event shape, the dedup contract, and the per-run event cap.
---

# Conversation Persistence

Persist your turn back to Askalot so the customer can audit the timeline that produced their brief, campaign decision, or quality assessment. Each turn is bracketed by `start_run` and `end_run`; between them, every meaningful step is recorded as a `project_conversation_events` row via `append_conversation_event`.

## Scope

**Covers**: when to call each tool, the `event` shape, the `(run_id, event_seq)` dedup contract, the per-run 10 000-event cap, and the retry-on-error rule.

**Does not cover**: project ownership / authentication (the MCP tool gates on `CAP_AI_ASSISTANT` + project membership; you don't manage that), the storage backend (Postgres `project_conversation_events` table), or the read surfaces (Conversation history tab in Armiger; Manager/Analyst tabs deferred to v1.1).

## The three tools

### `start_run`

Call this **once, at the very start of your turn**, before any other tool calls or sub-agent invocations.

**Arguments:**
- `project_id` (required) — the project UUID. Always the raw UUID (`529eb0bf-57ed-434f-9604-9482d1c5f8f6`), never the RAG workspace identifier.
- `agent_kind` (required) — one of `designer`, `manager`, `analyst`. Match it to your own identity. `respondent` is rejected server-side (Respondent is not a persisted conversation).
- `run_id` (required) — a fresh UUID4 you generate at the start of the turn. **Reuse the same `run_id` for every subsequent `append_conversation_event` and `end_run` call within this turn.**

The call is idempotent on `run_id`: if you retry on a flaky connection and the run row already exists, the existing row is returned unchanged.

### `append_conversation_event`

Call this **after every meaningful step** in your turn:

- Each MCP tool call (the call itself + the result it returned)
- Each `Agent(sub_agent)` invocation
- Each user-facing reply you produce
- Each significant internal reasoning step you want recorded as "thinking"

**Arguments:**
- `project_id` (required) — same UUID you passed to `start_run`.
- `agent_kind` (required) — same value you passed to `start_run`.
- `run_id` (required) — the UUID you generated at `start_run`.
- `event` (required) — the event dict described below.

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

**Kind selection:**

| `kind` | When to use |
|--------|-------------|
| `user_prompt` | The customer's incoming message that triggered this turn (event_seq = 0 unless the runtime already wrote it). |
| `thinking` | An internal reasoning step you want preserved. Plain text in `content`. |
| `tool_use` | You're about to call an MCP tool. Put the tool name in `tool_name` and its arguments in `tool_args`. |
| `tool_result` | The MCP tool returned. Put the result body (truncated to readable size) in `tool_result_preview`. |
| `assistant_text` | A user-facing reply chunk. Put the message in `content`. |

### `end_run`

Call this **once, at the end of your turn**, after the last `append_conversation_event`.

**Arguments:**
- `project_id` (required)
- `agent_kind` (required)
- `run_id` (required) — the same UUID.

The run row transitions from `running` to `closed`. Idempotent on terminal states: calling `end_run` on an already-closed or already-orphaned run is a no-op.

## The dedup contract (R-12) — never increment on retry

`event_seq` is a per-run monotonic counter starting at **0**. Increment by 1 for each successful `append_conversation_event` call.

**If `append_conversation_event` returns `success: false` with a transient error code (NOT `invalid_event_kind`, `validation_error`, `tool_args_too_large`, `run_not_running`, or `run_event_limit_exceeded`), retry with the SAME `event_seq` — do not increment.**

The server's `(run_id, event_seq)` UNIQUE index plus `INSERT ... ON CONFLICT DO NOTHING` makes same-seq retries safe: a duplicate insert is dropped silently. If you increment on retry, the server records `seq=N+1` but its earlier write of `seq=N` may or may not have committed, leaving a permanent gap in the visible timeline. Gaps are not a hard error but break the "no skipped tool calls" guarantee the audit surface relies on.

**Response classification:**

- `invalid_event_kind` / `validation_error` / `tool_args_too_large` — the payload itself is wrong. **Do not retry.** Fix the event shape and emit a different event.
- `run_not_running` (HTTP 409) — the run was orphaned by a `reset_conversation` or by Seneschal's 15-minute timeout. **Do not retry.** Stop emitting events for this run; the turn is effectively cancelled.
- `run_event_limit_exceeded` (HTTP 429) — the 10 000-event-per-run cap was hit. **Do not retry.** Call `end_run`, start a fresh `run_id` via `start_run`, and continue there. The customer will see two adjacent run rows.
- Transient network error, unexpected 500, other 5xx — retry with the SAME `event_seq`.

## The per-run event cap (10 000)

Each `run_id` is capped at 10 000 events. Beyond that, `append_conversation_event` returns 429 `RUN_EVENT_LIMIT_EXCEEDED` and refuses further inserts. This protects the server against runaway loops; a legitimate Designer turn rarely emits more than a few hundred events.

If you hit the cap, call `end_run`, generate a fresh `run_id`, call `start_run` for the new run, and continue. The customer will see two adjacent run rows in the timeline.

## The size caps

- `tool_args` — 16 KB serialized JSON. Oversized payloads return 400 `TOOL_ARGS_TOO_LARGE`. Truncate or summarize.
- `tool_result_preview` — 32 KB truncated server-side. Anything longer is silently cut at 32 KB; pass the head of the result.

These caps are per-event, not per-run.

## What NOT to do

- **Do not invent `run_id`s mid-turn.** Generate one UUID4 at `start_run` and reuse it for every subsequent call in that turn.
- **Do not set `actor_user_id`.** The server injects it from the authenticated JWT subject; any value you submit is ignored (SEC-07).
- **Do not skip `end_run`.** A run that never closes will eventually be flagged `orphaned` by Seneschal's 15-minute timeout, which surfaces as a red "Incomplete — connection lost" badge in the read surface.
- **Do not call these tools as `respondent`.** Respondent conversations are not persisted; the server rejects `agent_kind="respondent"` at the MCP layer.
