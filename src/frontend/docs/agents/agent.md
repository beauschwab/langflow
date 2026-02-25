# docs/agents/ — Agent Documentation

## Purpose
Documentation for AI agent features in the frontend.

## Deep Agent Process Steps

The Deep Agent component provides advanced capabilities with differentiated UI rendering:

| Capability | Tool Name | Icon | Frontend Renderer |
|-----------|-----------|------|-------------------|
| Planning | `write_todos` | `ListTodo` | Parsed checklist with ⬜/🔄/✅ status items |
| Context Write | `write_context` | `Save` | Compact key + char count, expandable value |
| Context Read | `read_context` | `BookOpen` | Compact key, expandable retrieved value |
| Sub-Agent Delegation | `delegate_task` | `Users` | Task + context + nested result card |
| Summarization | `summarize` | `FileText` | Compression ratio + expandable summary |
| Tool Errors | (any) | `AlertCircle` | Error text with tool name context |

## Architecture

- **Backend:** `base/agents/events.py` — `DEEP_AGENT_TOOL_DISPLAY` maps tool names to icons/headers
- **Frontend:** `components/core/chatComponents/ContentDisplay.tsx` — tool-name-aware renderers
- **Streaming:** Partial message updates via same message ID reuse (see `messagesStore.ts`)
