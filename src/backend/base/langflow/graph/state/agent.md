# graph/state/ — Graph State Model

## Purpose
Defines the state model infrastructure for shared state across graph execution. Components can declare state variables that persist across the graph run.

## Key Files

| File | Description |
|------|-------------|
| `model.py` | State model definitions used by `GraphStateManager`. |

## For LLM Coding Agents

- State is used by loop components and listen/notify patterns.
- The state model is dynamically created from the graph's component declarations.
