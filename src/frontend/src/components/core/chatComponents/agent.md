# chatComponents/ — Chat UI Components

## Purpose
Chat interface components used in the playground and IO modal.

## Key Components

| Component | File | Description |
|-----------|------|-------------|
| `ContentBlockDisplay` | `ContentBlockDisplay.tsx` | Renders agent step-by-step progress with expand/collapse, animated border trail during loading, and duration tracking. Handles `state: "partial"` (streaming) vs `"complete"` (finished). |
| `ContentDisplay` | `ContentDisplay.tsx` | Renders individual content items by type: `text`, `code`, `json`, `error`, `tool_use`, `media`. Includes deep agent tool-specific renderers for `write_todos` (checklist), `write_context`/`read_context` (memory badges), `delegate_task` (nested sub-agent card), and `summarize` (compression ratio). |
| `DurationDisplay` | `DurationDisplay.tsx` | Shows execution duration in milliseconds for each step. |

## Deep Agent Tool Rendering

The `ContentDisplay` component provides differentiated rendering for deep agent tools:

- **write_todos** — Parsed checklist with ⬜/🔄/✅ status icons instead of raw JSON
- **write_context** — Compact "Key: name · N chars" display with expandable value
- **read_context** — Compact key display with expandable retrieved value
- **delegate_task** — Task description + context + nested sub-agent result card with muted border
- **summarize** — Compression ratio (e.g., "2,450 chars → 480 chars (80% reduction)") with expandable summary
- **Other tools** — Generic tool_use rendering with JSON input/output blocks

Backend icons are set per tool name in `events.py` via `DEEP_AGENT_TOOL_DISPLAY` mapping.
