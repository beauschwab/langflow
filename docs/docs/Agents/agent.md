# Agents/ — Agent Documentation

## Purpose
Documentation for agent concepts, the Tool Calling Agent, and the Deep Agent component.

## Key Files
| File | Description |
|------|-------------|
| `agents-overview.md` | Overview of agents in Langflow — concepts and capabilities. |
| `agent-tool-calling-agent-component.md` | Tool Calling Agent component reference. |

## Deep Agent

The **Deep Agent** component extends the standard Tool Calling Agent with four capability toggles:

| Capability | Tool | Description |
|-----------|------|-------------|
| Planning | `write_todos` | Task breakdown into a checklist with pending/in-progress/done statuses. |
| Context Tools | `write_context` / `read_context` | Save and retrieve intermediate results by key. |
| Sub-Agents | `delegate_task` | Delegate focused subtasks to isolated sub-agents. |
| Summarization | `summarize` | Condense long text to manage context window limits. |

Each capability renders with a differentiated icon and specialized display in the Playground (see [Playground documentation](/concepts-playground#deep-agent-process-steps)).
