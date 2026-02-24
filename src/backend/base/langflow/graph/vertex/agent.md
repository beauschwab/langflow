# graph/vertex/ — Vertex (Node) Definitions

## Purpose
Defines vertex classes that wrap individual components within the flow graph. Each node in the visual flow editor becomes a `Vertex` instance at runtime.

## Key Files

| File | Description |
|------|-------------|
| `base.py` | `Vertex` base class — manages component lifecycle: initialization, parameter resolution, building, result storage. Key method: `build()` which invokes the underlying component. |
| `vertex_types.py` | Specialized vertex types for different component categories. |
| `param_handler.py` | Parameter resolution — resolves input values from upstream edges, environment variables, and defaults. |
| `schema.py` | Vertex serialization schemas. |
| `constants.py` | Vertex-related constants. |
| `exceptions.py` | Vertex-specific exceptions. |
| `utils.py` | Vertex utility functions. |

## Key Classes

- **`Vertex`**: The runtime wrapper around a component. Holds the component instance, manages input parameter resolution from upstream edges, triggers `component.build()`, and stores results.

## For LLM Coding Agents

- When debugging component execution issues, start here — `Vertex.build()` is where component code runs.
- `param_handler.py` handles how upstream results map to downstream inputs.
