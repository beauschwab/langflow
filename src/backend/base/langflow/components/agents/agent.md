# components/agents/ — Agent Components

## Purpose
Pre-configured AI agent implementations. These components create agents that can use tools, follow instructions, and produce structured outputs.

## Key Files

| File | Description |
|------|-------------|
| `agent.py` | The main `Agent` component — configurable agent with model selection, tool binding, system prompt, and structured output support. |

## For LLM Coding Agents

- The `Agent` component extends `AgentComponent` from `base/agents/agent.py`.
- It supports any chat model, multiple tools, and streaming responses.
