# graph/edge/ — Graph Edge Definitions

## Purpose
Defines edge classes that represent connections between vertices in the flow graph. Edges carry data from one component's output to another component's input.

## Key Files

| File | Description |
|------|-------------|
| `base.py` | `Edge` base class and `CycleEdge` subclass for handling loops. Manages source/target vertex references, data transfer, and validation. |
| `schema.py` | Pydantic schemas for edge serialization (`EdgeData`). |
| `utils.py` | Edge-related utility functions. |

## Key Classes

- **`Edge`**: Standard directed edge connecting source vertex output to target vertex input.
- **`CycleEdge`**: Special edge type for loop/cycle connections that allows data to flow backward in the graph for iterative processing.

## For LLM Coding Agents

- Edge logic is critical for data flow between components. Modify with care.
- `CycleEdge` enables the Loop component functionality.
