# processing/ — Flow Orchestration

## Purpose
High-level flow orchestration — coordinates graph execution with proper input/output handling, session management, and event streaming.

## Key Files

| File | Description |
|------|-------------|
| `orchestrator.py` | `run_graph_with_orchestrator()` — the main entry point for flow execution. Normalizes inputs, configures the graph, and delegates to `Graph.arun()`. Supports legacy and future execution backends. |
| `process.py` | Lower-level processing functions. |
| `utils.py` | Processing utility functions. |

## Execution Flow

```
API endpoint → run_graph_with_orchestrator() → Graph.arun() → vertex builds → results
```

## For LLM Coding Agents

- The `backend` parameter in `run_graph_with_orchestrator()` supports `"legacy"` (current) and can be extended for future backends (e.g., LangGraph).
