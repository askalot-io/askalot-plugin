---
name: gateway-routing
description: Use before deciding HOW to call Askalot for any task — one semantic action, a large byte payload, or a mass/bulk operation. Covers the three-lane routing rule (MCP tool / presigned handle / REST code-execution), the two async poll surfaces (task-status vs dataset-status), the upload-download handle recipe, code-execution safety guidance for mass work, and defer-loading guidance for the 100+-tool MCP surface.
---

# Gateway Routing

## Scope

**Covers**: How to pick the right transport for a given Askalot task —
MCP tool call, presigned-handle byte transfer, or a REST code-execution
loop — plus the two async poll surfaces and the safety rules for
agent-generated REST code.

**Does not cover**: The semantics of any individual tool (see
`mcp-campaign-tools`, `mcp-document-tools`, `mcp-survey-tools`, or a
flow skill like `design-questionnaire`). This skill is about *which
lane*, not *what the call does once you're in it*.

## Why Portor is hybrid

Portor is deliberately not a single-transport gateway. MCP tool calls
carry semantic verbs — one entity, one intent, a normal-sized JSON
payload, and every call round-trips through your context window. That's
the wrong shape for two things: (1) bytes too large to inline into a
tool result without blowing your turn's output budget, and (2) work
that touches dozens or hundreds of entities, where returning every row
through MCP would flood your context with data you don't need to reason
about individually. REST + presigned handles + code execution exist for
exactly those two cases. Routing correctly is not an optimization — an
oversized MCP call is *refused*, not slow, and a naive per-row MCP loop
over 500 respondents will exhaust your context long before it finishes.

## The three lanes — decide before you dispatch a single tool call

1. **Semantic verb, one entity, normal-sized payload** (create a
   project, update a campaign, read a Bundle's quality story, submit
   one survey response) → **MCP tool call**. This is the default lane —
   most of your work lives here.
2. **A byte payload above the inline threshold** (QML content over 32 KB,
   a dataset export file) → **presigned handle lane**. Mint the handle
   via MCP, move the bytes over plain HTTPS, never through a tool
   argument or tool result.
3. **A mass operation** — filter-then-act across many rows, a bulk
   create/delete, a scan-and-summarize over a large collection → **REST
   code-execution loop**, if your session has a code-execution/sandbox
   capability (Claude Code does). Loop and filter in the sandbox; return
   a summary to context, not a per-row dump.
4. **Mass operation, no code-execution capability** (a hosted pure-MCP
   session with no sandbox) → **fall back to the platform's `task_id`
   job tools** (`mass_fill_surveys` + `get_task_status`, or
   `code_open_ends`/`derive_silver` + `get_dataset` polling). Do not
   attempt to hand-write hundreds of sequential MCP calls in one turn as
   a substitute for either lane 3 or a task_id tool — that degrades to
   the same context-flooding problem lane 3 exists to avoid, just done
   by hand.

If you're unsure which lane a task falls into, default to MCP (lane 1)
for anything under roughly 20-50 entities and no oversized payload; the
threshold rules below (32 KB inline, `content_too_large_for_inline_save`)
tell you definitively when lane 2 is required, and a request that
explicitly says "all", "every", or names a three-digit-plus count is
almost always lane 3 or lane 4.

## Lane 2: byte transfer via presigned handles

**Write path (QML content)**: `save_qml_file`'s inline threshold is 32 KB
(`INLINE_THRESHOLD_BYTES`). Above it, the call is refused with
`content_too_large_for_inline_save` — never trim or drop content to fit
under the threshold. Use the handle recipe below instead.

**Read path (QML content)**: `get_qml_content` is the read-side mirror —
above the same 32 KB threshold it returns a short-lived signed
`download_url` instead of inlining the YAML.

**Read path (dataset exports)**: `export_dataset` always returns a
presigned `download_url` (never inlines file bytes) — fetch it directly
over HTTPS once the export completes.

### Handle-flow recipe (write side)

1. `request_upload_url(qml_name=..., project_id=...)` — mints a
   short-lived, single-use, size-capped handle:
   `{upload_url, artifact_id, max_size_bytes, expires_in}`.
2. `PUT` the raw QML bytes to `upload_url` over HTTPS, out-of-band —
   any HTTP-capable tool works (Claude Code's own request capability is
   enough); the content never appears in a tool argument or MCP context.
3. `finalize_upload(artifact_id=...)` — lands the file with the exact
   same warn-only validation / publish-gate re-check / atomic-write
   guarantees as a normal `save_qml_file` call. Idempotent on retry.

This requires HTTP egress from the calling agent. A pure-MCP hosted
session with no egress capability cannot complete an above-threshold
save at all — `save_qml_file`'s error names that limitation explicitly
rather than failing silently; reduce the content below the threshold, or
drive the task from an egress-capable session instead.

## Lane 3: mass operations via REST code execution

Reach for this lane when a task needs you to read, filter, decide, and
write across many entities and returning each one through MCP would
either exceed a reasonable turn budget or flood your context with rows
you don't need to individually reason about — e.g. "delete every
respondent from source X older than 6 months", "audit all 500 surveys
in this campaign and report which ones have inconsistent answers",
"bulk-create 200 respondents from this CSV".

**Pattern**:

1. Authenticate the sandbox's REST calls with a **scoped API token**
   (`aslat_...`, minted via Profile Settings — see the `askalot-setup`
   skill), not by extracting your interactive session's live OAuth
   bearer token into generated code. A minted API token is a separate,
   revocable credential purpose-built for non-interactive REST callers;
   your OAuth session token authorizes your MCP connection and should
   stay there.
2. Discover the REST surface via `/api/v1/docs` (Swagger UI) or
   `/api/v1/openapi.json` — every entity has REST CRUD, and the bulk
   endpoints (`bulk_create_respondents`, `bulk_delete_respondents`,
   `bulk_create_surveys`, `bulk_delete_surveys`) are REST+MCP
   dual-projected, so the same operation is available either way; REST
   is simply the shape that lets your generated code paginate and loop
   without a context round-trip per row.
3. Write the loop/filter/decide logic in the sandbox. Fetch pages, apply
   your filter, decide per-row, issue writes.
4. Return a **summary** to context — counts, a handful of representative
   IDs, and any exceptions. Never paste the full row set into your
   response; that defeats the point of using this lane.

### Two accepted risks — name and mitigate them explicitly

**1. Token exposure.** The credential your generated code uses to call
REST is live and powerful. **Never print, log, or transmit it outside
the REST call that needs it** — not to stdout, not to a file the agent
later reads back, not embedded in the summary you return to context. Pass
it via an environment variable directly to the script process; reference
that variable only in the `Authorization` header construction.

**2. Bulk-mutation blast radius.** Agent-scripted bulk mutations have no
throttle beyond generic network-level rate limiting — Portor does not
yet enforce a server-side cap on agent-scripted REST call volume, so
loop discipline is what stands between an oversized selector and a
runaway mutation. Before running any destructive bulk verb:

- **Prefer dry-run/count-first.** `bulk_delete_respondents` and
  `bulk_delete_surveys` already default to `dry_run=true` — a call that
  omits `dry_run` returns a count + sample preview without deleting;
  you must explicitly re-call with `dry_run=false` to commit. Use that
  default, don't bypass it. For operations with no built-in dry-run,
  issue a `GET`/list call first and inspect the count before looping
  writes.
- **Cap loop iteration counts.** Bound the number of write calls a
  single script run will issue (a few hundred, not an unbounded `while`
  over every matching row) so a mis-scoped filter fails small rather
  than mutating the whole tenant.

Both of these are documentation-level mitigations ahead of real
server-side rate limiting — they only work if you actually follow them.

## Lane 4: no code-execution — task_id job tools

When your session has no sandbox/code-execution capability, mass work
still exists — you just reach for the platform's own async job tools
instead of hand-rolling a loop:

- **`mass_fill_surveys`** — enqueues synthetic survey-response
  generation across a campaign; returns `{task_id, status: "pending"}`
  immediately.
- **`code_open_ends` / `derive_silver`** — enqueues the Bronze→Silver
  coding+raking job for a Bundle; returns the Silver dataset row in
  `processing`.

Never substitute a hand-written sequence of dozens of individual MCP
calls for one of these enqueue tools — the enqueue exists precisely
because the underlying work is bulk-shaped.

## Async poll surfaces at a glance

Two distinct poll surfaces exist; they are not interchangeable and a
task_id from one is meaningless to the other tool.

| Surface | Poll tool | Backs | Terminal states | Cadence |
|---|---|---|---|---|
| **task-status** | `get_task_status(task_id)` | Mass-fill jobs: `mass_fill_surveys` | `completed`, `partial`, `failed` | Response carries `suggested_poll_interval_seconds` — a `[2, 30]`s heuristic hint while pending/running, `null` once terminal |
| **dataset-status** | `get_dataset(dataset_id)` | Pipeline jobs: `code_open_ends`/`derive_silver`, `create_bronze_dataset`, `create_gold_dataset` | `ready` (via `processing_status`) | No computed hint — poll every few seconds |

`partial` (task-status only) means a bulk task finished with a mixed
succeeded/failed outcome (e.g. 480 of 500 surveys filled) — its result
summary carries succeeded/failed counts and failed IDs, never a per-item
dump. Treat it as terminal: stop polling, then decide whether to retry
the failed subset.

## Tool-surface size and defer-loading

Askalot's MCP surface is large — well over 100 tools across projects,
campaigns, questionnaires, respondents, pools, strategies, surveys,
datasets, bundles, documents, methodology library, paper, conversation
persistence, and audit. Preloading every tool's full schema into context
up front is wasteful when a given turn only needs a handful.

If your harness supports deferred tool loading (Claude Code does — tools
beyond a threshold surface as names only, with full schemas fetched
on demand via a search/discovery mechanism), **do not fabricate a tool's
parameters from memory or a half-remembered schema**. Resolve the
concrete schema first (e.g. a tool-search call naming the exact tool, or
a handful of relevant keywords), then call it. A tool name appearing in
a deferred listing is not yet callable — treat it the same as an
undiscovered tool until its schema has actually loaded.

## Degraded cues without this skill (R17)

Every lane rule above has a twin that surfaces directly in tool output
or a structured error, so a raw-MCP session with no plugin loaded still
routes correctly — this skill accelerates that routing, it does not
gate it:

- `save_qml_file` above 32 KB → `content_too_large_for_inline_save`,
  carrying `threshold_bytes`, `content_bytes`, and a `next_step` field
  that names `request_upload_url` + `finalize_upload` explicitly, plus a
  `detail` string that calls out the HTTP-egress requirement and the
  Claude-Code-only posture for pure-MCP sessions without egress.
- `get_qml_content` above 32 KB → returns `download_url` with a `note`
  field explaining why content wasn't inlined and that the URL expires.
- `export_dataset` → always returns `download_url` (never inlines file
  bytes) — the tool never had an inline path to begin with, so there's
  no threshold error to degrade from.
- `get_task_status` → `suggested_poll_interval_seconds` and the
  `partial` state are self-describing in the returned envelope; a
  caller with no skill loaded still sees the cadence hint and the
  distinct terminal state.
- `bulk_delete_respondents` / `bulk_delete_surveys` → `dry_run=true` is
  the *default*, not opt-in — a caller who never reads this skill still
  gets the count-first safety behavior by doing nothing extra.

This coverage was verified against the current tool docstrings while
writing this skill (plan 2026-07-11-001 U8) — it was not assumed.

## What this skill does not change

This is a routing/documentation skill only. It introduces no new MCP
tools, REST endpoints, or server-side behavior — every mechanism it
describes (the 32 KB threshold, the handle lane, `dry_run` defaults, the
two poll surfaces) already exists and was shipped by earlier units in
plan 2026-07-11-001 (U1-U7). If a task needs a lane this skill doesn't
describe, that's a signal the underlying capability doesn't exist yet —
surface it as a gap rather than improvising a workaround.
