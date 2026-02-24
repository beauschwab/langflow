# graph/graph/ — Core Graph Class and Scheduling

## Purpose
Contains the main `Graph` class that orchestrates flow execution, the `RunnableVerticesManager` for vertex scheduling, and state management infrastructure.

## Key Files

| File | Description |
|------|-------------|
| `base.py` | **The `Graph` class** — the central runtime object. Key methods: `arun()` (async execution), `build_vertex()`, `prepare()`, `initialize()`. Handles topological sorting, vertex iteration, and result collection. |
| `runnable_vertices_manager.py` | `RunnableVerticesManager` — determines which vertices are ready to run based on completed dependencies. Manages the execution frontier. |
| `state_manager.py` | `GraphStateManager` — manages shared mutable state that vertices can read/write during execution. |
| `state_model.py` | `create_state_model_from_graph()` — dynamically creates a Pydantic model representing the graph's state schema. |
| `schema.py` | Schemas: `GraphData`, `GraphDump`, `StartConfigDict`, `VertexBuildResult`. |
| `constants.py` | Constants including `Finish` sentinel and lazy-loaded vertex type mapping. |
| `utils.py` | Graph utilities: cycle detection (`find_all_cycle_edges`, `find_cycle_vertices`), topological sorting (`get_sorted_vertices`), start component resolution. |
| `ascii.py` | ASCII art representation of the graph for debugging/logging. |

## Key Functions

- `Graph.arun(inputs, outputs, session_id, stream)`: Main async execution — runs the entire flow and returns `RunOutputs`.
- `Graph.build_vertex(vertex_id)`: Builds a single vertex and propagates results.
- `RunnableVerticesManager.get_ready_vertices()`: Returns vertices whose dependencies are satisfied.
- `GraphStateManager.update_state()` / `get_state()`: Thread-safe state access.

## For LLM Coding Agents

- This is the most performance-critical code in the backend. Changes here affect all flow executions.
- The `Graph` class is approximately 1000+ lines — understand the full lifecycle before modifying.
- State management is used by components that need to share data across the graph (e.g., Loop, Listen/Notify).
