# base/agents/ — Agent Base Classes

## Purpose
Defines the `AgentComponent` base class that all agent components extend. Provides agent execution infrastructure including tool binding, prompt management, streaming, and error handling.

## Key Files

| File | Description |
|------|-------------|
| `agent.py` | `AgentComponent` base class — core agent logic with `run_agent()`, tool binding, model integration. |
| `callback.py` | Agent callback handlers for streaming tokens and intermediate steps. |
| `context.py` | Agent execution context management. |
| `default_prompts.py` | Default system/user prompt templates for agents. |
| `errors.py` | Agent-specific error types. |
| `events.py` | Agent event definitions for streaming. |
| `utils.py` | Agent utility functions. |

## Subdirectories

| Folder | Description |
|--------|-------------|
| `crewai/` | CrewAI multi-agent framework integration — `crew.py` (crew orchestration) and `tasks.py` (task definitions). |

## For LLM Coding Agents

- Extend `AgentComponent` when creating new agent types.
- The agent base class handles tool calling, streaming, and LLM integration automatically.
